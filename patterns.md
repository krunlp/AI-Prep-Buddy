---
layout: default
title: Design Patterns Catalog
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

[← Back to Home](index.html) · [Question Bank →](questions.html) · [Answer Frameworks →](answers.html) · [System-Design Diagrams →](diagrams.html) · [Design Patterns Catalog →](patterns.html)

# AI Prep Buddy — Design Patterns Catalog

While `ARCHITECTURE_DIAGRAMS.md` covers *system-design questions* (Sections 13, 14, 27), this catalog covers recurring *conceptual/technical patterns* that show up across the rest of the bank — transformer internals, training/alignment, prompting, agent reasoning, MLOps, and safety. These are the patterns you should be able to draw and explain from memory in a whiteboard round.

---

## A. Transformer & LLM Internals Patterns

### A1. Scaled Dot-Product Attention (Q287–289)

```mermaid
flowchart LR
    X[Input Embeddings] --> Q[Query Projection]
    X --> K[Key Projection]
    X --> V[Value Projection]
    Q --> DOT[Q · Kᵀ]
    K --> DOT
    DOT --> SCALE[÷ √d_k]
    SCALE --> SOFTMAX[Softmax]
    SOFTMAX --> WEIGHT[Attention Weights]
    WEIGHT --> MULT[Weighted Sum]
    V --> MULT
    MULT --> OUT[Attention Output]
```

**When to draw this:** Any question about "explain attention," transformer architecture, or why attention scales quadratically with sequence length. The scaling by √d_k is the detail people forget — it prevents large dot products from pushing softmax into near-zero-gradient regions as dimensionality grows.

---

### A2. MHA vs MQA vs GQA (Q291–292)

```mermaid
flowchart TD
    subgraph MHA["Multi-Head Attention"]
    H1[Head 1: own Q,K,V] 
    H2[Head 2: own Q,K,V]
    H3[Head 3: own Q,K,V]
    end
    subgraph MQA["Multi-Query Attention"]
    M1[Head 1: own Q] --> SHK[Shared K,V]
    M2[Head 2: own Q] --> SHK
    M3[Head 3: own Q] --> SHK
    end
    subgraph GQA["Grouped-Query Attention"]
    G1[Head 1,2: own Q] --> GK1[Shared K,V - Group A]
    G2[Head 3,4: own Q] --> GK2[Shared K,V - Group B]
    end
```

**When to draw this:** Any KV-cache or serving-cost question. The core tradeoff: MHA = best quality, largest KV cache; MQA = smallest KV cache, most quality loss; GQA = the practical middle ground almost every modern production LLM actually uses.

---

### A3. KV Cache & Prefill vs Decode (Q293, Q332)

```mermaid
sequenceDiagram
    participant User
    participant Model
    participant KVCache
    User->>Model: Full prompt (prefill)
    Model->>KVCache: Compute & store K,V for all prompt tokens (parallel, compute-bound)
    Model->>User: Token 1
    Model->>KVCache: Append K,V for token 1
    Note over Model,KVCache: Decode: one token at a time, memory-bandwidth-bound
    Model->>User: Token 2
    Model->>KVCache: Append K,V for token 2
    Model->>User: Token 3 (...continues...)
```

**When to draw this:** Any inference-optimization question. Prefill is parallel and compute-bound (high GPU utilization); decode is sequential and memory-bandwidth-bound (low utilization per step) — this asymmetry is *why* continuous batching and paged attention exist as separate optimizations.

---

### A4. Mixture-of-Experts Routing (Q306–308)

```mermaid
flowchart TD
    TOKEN[Input Token] --> ROUTER[Router Network]
    ROUTER --> SCORE[Score All Experts]
    SCORE --> TOPK[Select Top-2 Experts]
    TOPK --> E1[Expert 3: Active]
    TOPK --> E2[Expert 7: Active]
    SCORE -.not selected, no compute.-> EINACTIVE[Experts 1,2,4,5,6,8...: Inactive]
    E1 --> COMBINE[Weighted Combine]
    E2 --> COMBINE
    COMBINE --> OUT[Output]
    ROUTER -.aux loss.-> BALANCE[Load Balancing Loss: prevents expert collapse]
```

**When to draw this:** Any question about MoE, dense vs sparse serving cost, or why a huge-parameter-count model can be cheap to serve. Key point: total parameters ≠ active parameters per token — that's the entire value proposition of MoE.

---

### A5. Speculative Decoding (Q328)

```mermaid
sequenceDiagram
    participant Draft as Small Draft Model
    participant Target as Large Target Model
    Draft->>Draft: Generate 4 candidate tokens quickly
    Draft->>Target: Propose tokens [A, B, C, D]
    Target->>Target: Verify all 4 in ONE parallel forward pass
    Target->>Draft: Accept A, B, C — Reject D
    Note over Target: Target generates correct replacement for D
    Draft->>Draft: Resume drafting from corrected point
```

**When to draw this:** Any latency-optimization question. Key insight: the target model's output distribution is unchanged (it's still doing the verification) — this is a pure speedup, not an approximation.

---

### A6. Quantization Precision Pipeline (Q201, Q336–337)

```mermaid
flowchart LR
    FP32[Original Weights: FP32] --> OUTLIER{Outlier Channels?}
    OUTLIER -->|Yes| SMOOTH[SmoothQuant: migrate difficulty to weights]
    OUTLIER -->|No| DIRECT[Direct Quantization]
    SMOOTH --> QUANT[Quantize to INT8/INT4]
    DIRECT --> QUANT
    QUANT --> VALIDATE{Accuracy Drop Acceptable?}
    VALIDATE -->|No| QAT[Quantization-Aware Training: fine-tune with quantization simulated]
    VALIDATE -->|Yes| DEPLOY[Deploy Quantized Model]
    QAT --> DEPLOY
```

**When to draw this:** Any cost/serving question involving self-hosted models. Post-training quantization is cheap but riskier for accuracy; QAT is expensive but more robust — the outlier problem is the specific technical reason naive quantization fails.

---

## B. Training & Alignment Patterns

### B1. SFT → RLHF/DPO Pipeline (Q309–320)

```mermaid
flowchart TD
    BASE[Base Model: pretrained, next-token prediction only] --> SFT[Supervised Fine-Tuning: instruction-response pairs]
    SFT --> SFTMODEL[SFT Model / Reference Model]
    SFTMODEL --> BRANCH{Alignment Method}
    BRANCH -->|RLHF| REWARD[Train Reward Model on Human Preferences]
    REWARD --> PPO[PPO: optimize policy against reward model + KL penalty to reference]
    BRANCH -->|DPO| DIRECT[Direct Preference Optimization: skip reward model, optimize directly on preference pairs]
    PPO --> ALIGNED[Aligned Chat Model]
    DIRECT --> ALIGNED
```

**When to draw this:** Any question about how ChatGPT-style models are built, RLHF vs DPO, or alignment in general. The KL penalty to the reference model is the detail that prevents reward hacking — always mention it.

---

### B2. LoRA / Parameter-Efficient Fine-Tuning (Q318–320)

```mermaid
flowchart TD
    FROZEN[Frozen Pretrained Weights W] --> ADD[+]
    INPUT[Input] --> FROZEN
    INPUT --> LORAPATH[LoRA Path]
    LORAPATH --> A[Low-Rank Matrix A: d × r]
    A --> B[Low-Rank Matrix B: r × d]
    B --> ADD
    ADD --> OUTPUT[Output]
    TRAIN[Training] -.only updates A, B.-> A
    TRAIN -.W stays frozen.-> FROZEN
```

**When to draw this:** Any fine-tuning-cost question. The rank `r` is typically tiny (4-64) compared to `d` (thousands), which is why trainable parameters drop by 100-1000x versus full fine-tuning while retaining most of the quality.

---

### B3. Knowledge Distillation (Q200, Q335)

```mermaid
flowchart TD
    INPUT[Training Input] --> TEACHER[Large Teacher Model - frozen]
    INPUT --> STUDENT[Small Student Model - training]
    TEACHER --> SOFTLABELS[Soft Probability Distribution]
    STUDENT --> STUDENTOUT[Student Predictions]
    SOFTLABELS --> LOSS[Distillation Loss: match distributions]
    STUDENTOUT --> LOSS
    GROUNDTRUTH[Ground Truth Labels - optional] --> LOSS2[Standard Loss]
    STUDENTOUT --> LOSS2
    LOSS --> COMBINED[Combined Loss]
    LOSS2 --> COMBINED
    COMBINED --> UPDATE[Update Student Only]
```

**When to draw this:** Any model-compression or cost-reduction question. Key point: soft labels (full probability distributions) carry more information than hard labels alone — that's why distillation outperforms just training a small model from scratch on the same hard labels.

---

## C. Prompting & Reasoning Patterns

### C1. ReAct Loop (Q348, Q451)

```mermaid
flowchart TD
    START[Task] --> THOUGHT[Thought: reason about what to do]
    THOUGHT --> ACTION[Action: call a tool]
    ACTION --> OBSERVE[Observation: tool result]
    OBSERVE --> DONE{Task Complete?}
    DONE -->|No| THOUGHT
    DONE -->|Yes| FINAL[Final Answer]
```

**When to draw this:** Any agent question. This is the single most important loop to be able to draw cold — nearly every agent framework is a variation of Thought → Action → Observation → repeat.

---

### C2. Chain-of-Thought vs Tree-of-Thought vs Self-Consistency (Q324–325, Q349–350)

```mermaid
flowchart TD
    subgraph CoT["Chain-of-Thought"]
    S1[Step 1] --> S2[Step 2] --> S3[Step 3] --> A1[Answer]
    end
    subgraph ToT["Tree-of-Thought"]
    T0[Start] --> T1a[Branch A]
    T0 --> T1b[Branch B]
    T1a --> T2a[Evaluate: prune]
    T1b --> T2b[Evaluate: continue]
    T2b --> A2[Answer]
    end
    subgraph SC["Self-Consistency"]
    Q0[Same Prompt] --> P1[Sample Path 1: Answer X]
    Q0 --> P2[Sample Path 2: Answer X]
    Q0 --> P3[Sample Path 3: Answer Y]
    P1 --> VOTE[Majority Vote]
    P2 --> VOTE
    P3 --> VOTE
    VOTE --> A3[Final: Answer X]
    end
```

**When to draw this:** Any reasoning-technique comparison question. Cost ordering: CoT is cheapest (1 pass), self-consistency is moderate (N parallel passes + vote), Tree-of-Thought is most expensive (branching search with evaluation) — match the technique to how much the accuracy gain justifies the cost.

---

### C3. Self-RAG / Corrective Retrieval Loop (Q402)

```mermaid
flowchart TD
    Q[Query] --> RETRIEVE[Retrieve]
    RETRIEVE --> SELFCHECK{Model Assesses: Is this actually relevant/sufficient?}
    SELFCHECK -->|No| REFORMULATE[Reformulate Query]
    REFORMULATE --> RETRIEVE
    SELFCHECK -->|Yes| GENERATE[Generate Draft Answer]
    GENERATE --> GROUNDCHECK{Is Draft Grounded in Retrieved Content?}
    GROUNDCHECK -->|No| RETRIEVE
    GROUNDCHECK -->|Yes| FINAL[Final Answer]
```

**When to draw this:** Any "how do you reduce RAG hallucination" question. The two self-check gates (retrieval-sufficiency and generation-groundedness) are what distinguish this from naive single-pass RAG.

---

## D. Agent Architecture Patterns

### D1. Plan-and-Execute vs Reactive Single-Loop (Q453–454)

```mermaid
flowchart TD
    subgraph PlanExecute["Plan-and-Execute"]
    G1[Goal] --> PLAN[Generate Full Plan Upfront]
    PLAN --> EX1[Execute Step 1] --> EX2[Execute Step 2] --> EX3[Execute Step 3]
    EX2 -.step fails.-> REPLAN[Re-plan remaining steps]
    end
    subgraph Reactive["Reactive Single-Loop"]
    G2[Goal] --> R1[Decide Next Step] --> R2[Act] --> R3[Observe] --> R1
    end
```

**When to draw this:** Any "how would you architect a complex agent" question. Plan-and-execute is more efficient/predictable for well-understood tasks; reactive is more robust to genuinely novel/surprising situations.

---

### D2. Orchestrator-Worker Multi-Agent Pattern (Q456, Q466)

```mermaid
flowchart TD
    TASK[Complex Task] --> ORCH[Orchestrator]
    ORCH --> DECOMPOSE[Decompose]
    DECOMPOSE --> W1[Worker: Domain A]
    DECOMPOSE --> W2[Worker: Domain B]
    W1 --> RESULT1[Result A]
    W2 --> RESULT2[Result B]
    RESULT1 --> ORCH
    RESULT2 --> ORCH
    ORCH --> CRITIC[Critic Agent: reviews combined output]
    CRITIC -->|Reject| REDO[Orchestrator re-dispatches failed piece]
    CRITIC -->|Accept| FINAL[Final Output]
```

**When to draw this:** Any multi-agent system-design question. The critic-gate-before-finalization detail is what separates a robust design from a naive "agents talking to each other" answer.

---

### D3. Human-in-the-Loop Checkpoint Pattern (Q461, Q477)

```mermaid
flowchart TD
    AGENT[Agent Reasoning] --> ACTIONTYPE{Action Risk Tier}
    ACTIONTYPE -->|Read-only| AUTO[Execute Automatically]
    ACTIONTYPE -->|Reversible, low-cost| AUTO
    ACTIONTYPE -->|Irreversible or high-cost| GATE[Human Approval Gate]
    GATE -->|Approved| EXECUTE[Execute]
    GATE -->|Rejected| ABORT[Abort + Log Reason]
    AUTO --> LOG[Audit Log]
    EXECUTE --> LOG
    ABORT --> LOG
```

**When to draw this:** Any agent-safety question. The key design decision to always call out explicitly: risk tiering is what makes this scalable — gating *everything* kills usability, gating *nothing* is unsafe.

---

## E. MLOps & Deployment Patterns

### E1. Canary → Shadow → Full Rollout (Q607–609, Q625)

```mermaid
flowchart LR
    NEW[New Model/Prompt Version] --> SHADOW[Shadow: mirrors real traffic, no user impact]
    SHADOW -->|Validated| CANARY[Canary: 5% real traffic]
    CANARY -->|Metrics OK| RAMP[Ramp: 25% → 50%]
    RAMP -->|Metrics OK| FULL[Full: 100%]
    SHADOW -.issue found.-> ABORT1[Abort, zero user impact]
    CANARY -.issue found.-> ROLLBACK1[Instant Rollback]
    RAMP -.issue found.-> ROLLBACK2[Instant Rollback]
```

**When to draw this:** Any deployment/rollout question. The progression matters: shadow catches obvious issues with zero risk, canary catches subtler issues with bounded risk, full rollout only happens after both gates clear.

---

### E2. Medallion Data Architecture (Q733)

```mermaid
flowchart LR
    RAW[Raw Sources] --> BRONZE[(Bronze: raw, unprocessed)]
    BRONZE --> SILVER[(Silver: cleaned, validated, joined)]
    SILVER --> GOLD[(Gold: business-level aggregates)]
    GOLD --> ML[ML Feature Pipelines]
    GOLD --> BI[BI Dashboards]
    GOLD --> RAG[RAG Document Corpus]
```

**When to draw this:** Any data-engineering question. Each layer has a distinct purpose: bronze preserves the raw source of truth for reprocessing, silver is where quality/validation happens, gold is what consumers actually query.

---

### E3. Eval-Gated CI/CD (repeated pattern, Q646, Q810, Q831)

```mermaid
flowchart LR
    CHANGE[Prompt/Model/Code Change] --> GOLDEN[Golden Eval Suite]
    GOLDEN --> THRESHOLD{Meets Quality Threshold?}
    THRESHOLD -->|No| BLOCKED[Merge Blocked]
    THRESHOLD -->|Yes| MERGED[Merged]
    MERGED --> SHADOW_STAGE[Shadow → Canary → Full]
```

**When to draw this:** Any question about safely shipping AI changes. This is the connective tissue between "how do you eval" questions and "how do you deploy" questions — eval gates *are* the deployment gate, not a separate concern.

---

## F. Safety & Governance Patterns

### F1. Defense-in-Depth Guardrails (Q866–869)

```mermaid
flowchart TD
    INPUT[User Input] --> L1[Layer 1: Input Filtering - known attack patterns]
    L1 --> L2[Layer 2: System Prompt Hardening - explicit anti-injection instructions]
    L2 --> LLM[LLM Processing]
    LLM --> L3[Layer 3: Output Filtering - content safety classifier]
    L3 --> L4[Layer 4: Structural Validation - schema/action-permission checks]
    L4 --> OUTPUT[Safe Output]
    L1 -.blocked.-> REJECT1[Reject]
    L3 -.blocked.-> REJECT2[Reject]
    L4 -.blocked.-> REJECT3[Reject]
```

**When to draw this:** Any prompt-injection or safety-architecture question. The point to emphasize: no single layer is sufficient alone — this is why it's called "defense in depth," not "defense in one really good filter."

---

### F2. Red-Team → Eval-Suite Feedback Loop (Q843–844)

```mermaid
flowchart TD
    REDTEAM[Red-Team Exercise] --> FINDINGS[Categorized Findings by Severity]
    FINDINGS --> FIX[Guardrail/Prompt Fixes]
    FINDINGS --> EVALADD[Add to Adversarial Eval Suite]
    EVALADD --> REGRESSION[Standing Regression Test]
    REGRESSION -.runs on every future change.-> CI[CI Pipeline]
    FIX --> VALIDATE[Validate Fix Against New Eval Case]
    VALIDATE --> REDTEAM
```

**When to draw this:** Any "how do you handle discovered vulnerabilities" question. The critical detail: every red-team finding becomes a *permanent* regression test, not just a one-time fix — otherwise the same vulnerability can silently reappear after a future change.

---

### F3. Fairness Audit Cycle (Q909, Q932)

```mermaid
flowchart TD
    DEFINE[Define Protected Groups + Fairness Metrics with Legal/Ethics] --> BASELINE[Baseline Audit: pre-launch]
    BASELINE --> LAUNCH{Passes Threshold?}
    LAUNCH -->|No| REMEDIATE[Remediate: reweighting, debiasing]
    REMEDIATE --> BASELINE
    LAUNCH -->|Yes| DEPLOY[Deploy]
    DEPLOY --> ONGOING[Ongoing Production Monitoring]
    ONGOING -.periodic.-> REAUDIT[Scheduled Re-Audit]
    REAUDIT -->|Drift detected| REMEDIATE
```

**When to draw this:** Any governance/bias question. The point that separates a strong answer: fairness auditing is a *cycle*, not a one-time pre-launch checkbox — data and population shift over time, so the audit has to repeat.

---

*This catalog covers the recurring conceptual patterns underlying Sections 1–12 and 15–28. Combined with `ARCHITECTURE_DIAGRAMS.md` (system-design patterns for Sections 13, 14, 27), between the two files nearly every diagrammable concept in the bank now has a visual reference.*

---

## G. Enterprise Governance & Operating-Model Patterns

### G1. AI Maturity Model (Q1093)

```mermaid
flowchart LR
    L1[Level 1: Ad Hoc<br/>scattered experiments] --> L2[Level 2: Repeatable<br/>team-level patterns]
    L2 --> L3[Level 3: Defined<br/>shared platform + governance]
    L3 --> L4[Level 4: Managed<br/>quantitative metrics drive decisions]
    L4 --> L5[Level 5: Optimizing<br/>continuous improvement, proactive risk]
```

**When to draw this:** Any "how do you assess where an org stands" or roadmap-planning question. Most enterprises today sit at Level 2–3; a Principal-level answer should be able to place a hypothetical org on this scale and articulate the specific gap to the next level, not just describe the levels abstractly.

---

### G2. TCO Framework for an Enterprise AI System (Q1094)

```mermaid
flowchart TD
    BUILD[Initial Build Cost] --> TCO[Total Cost of Ownership]
    RUN[Annual Run Cost × Expected Lifespan] --> TCO
    subgraph RunCosts["Commonly Underestimated Run Costs"]
    EVAL[Ongoing Eval Maintenance]
    ONCALL[Incident Response / On-Call]
    DATA[Data Pipeline Upkeep]
    ITER[Prompt/Model Iteration Over Time]
    end
    RunCosts --> RUN
    RISK[Risk-Adjusted Incident Cost] --> TCO
```

**When to draw this:** Any cost-justification or build-vs-buy question. The point that separates a strong answer: most people only budget the "Build" box — the run-cost sub-boxes are where enterprise AI TCO is chronically underestimated.

---

### G3. Build-vs-Buy-vs-Partner Weighted Scorecard (Q1095)

```mermaid
flowchart TD
    OPTION[Candidate Option: Build / Buy / Partner] --> D1[Differentiation Value - weight: high]
    OPTION --> D2[Time to Value - weight: medium]
    OPTION --> D3[TCO - weight: high]
    OPTION --> D4[Data/IP Control - weight: medium]
    OPTION --> D5[Lock-in Risk - weight: medium]
    OPTION --> D6[Internal Maintain Capability - weight: medium]
    D1 --> SCORE[Weighted Composite Score]
    D2 --> SCORE
    D3 --> SCORE
    D4 --> SCORE
    D5 --> SCORE
    D6 --> SCORE
    SCORE --> DECISION[Decision: filled out BEFORE the team has a preference]
```

**When to draw this:** Any build-vs-buy question. The critical caveat to always state out loud: the scorecard only has integrity if it's filled out before the team's emotional preference forms — otherwise it's theater justifying a decision already made.

---

### G4. Enterprise System Integration Pattern (SAP/Salesforce/ServiceNow) (Q1098–1100)

```mermaid
flowchart TD
    AI[AI Feature] --> NATIVE{Integration Approach}
    NATIVE -->|Preferred| EXTENSION[Native Extension Framework: SAP BTP / Salesforce Apex / ServiceNow Virtual Agent]
    NATIVE -->|Avoid| PARALLEL[Parallel External Tool: shadow-IT risk]
    EXTENSION --> INHERIT[Inherits Existing Permission Model + Audit Trail]
    EXTENSION --> READONLY{Write Action?}
    READONLY -->|Yes| APPROVAL[Routes Through Existing Business-Process Approval]
    READONLY -->|No| DIRECT[Direct Read Access]
    PARALLEL -.x.-> RISK[Separate access-control system to maintain, audit gaps]
```

**When to draw this:** Any enterprise-integration question (SAP, Salesforce, ServiceNow, or similar). The core principle generalizes beyond any single vendor: build inside the system of record's native extension framework so permissions/audit are inherited, never build a parallel tool that requires a second access-control system to keep in sync.

---

### G5. AI Center of Excellence RACI (Q1101)

```mermaid
flowchart TD
    subgraph CoE["AI Center of Excellence"]
    PLATFORM[ML Platform Team: Responsible - shared infra, gateway, eval, guardrails]
    end
    subgraph Governance
    LEGAL[Legal/Compliance: Accountable - regulatory interpretation]
    SECURITY[Security: Accountable - data/access controls]
    end
    subgraph Delivery
    PRODUCT[Product Teams: Responsible + Accountable - their own feature outcomes]
    DATAENG[Data Engineering: Responsible - pipeline/data quality]
    end
    EXEC[Executive Sponsor: Accountable - overall strategy, Informed on projects]

    PLATFORM -.provides platform to.-> PRODUCT
    LEGAL -.consulted on.-> PRODUCT
    SECURITY -.consulted on.-> PRODUCT
    EXEC -.sponsors.-> CoE
```

**When to draw this:** Any AI CoE or organizational-design question. The detail that distinguishes a strong answer: Product teams remain accountable for *their own* outcomes — the CoE's job is to provide platform and guardrails, not to own every team's product decisions, which is the most common design mistake in real enterprise AI CoE rollouts.

---

*These five patterns extend the catalog into enterprise governance/operating-model territory, complementing the technical patterns in sections A–F above. Combined with Section 29 in the question bank, this closes the gap between "can build the system" and "can operate AI at true enterprise scale."*

<script>
document.addEventListener("DOMContentLoaded", function () {
  mermaid.initialize({ startOnLoad: false, theme: "default" });
  var blocks = document.querySelectorAll("pre code.language-mermaid, code.language-mermaid");
  blocks.forEach(function (code, i) {
    var text = code.textContent;
    var container = code.closest("div.highlighter-rouge") || code.closest("pre");
    var div = document.createElement("div");
    div.className = "mermaid";
    div.id = "mermaid-" + i;
    div.textContent = text;
    container.parentNode.replaceChild(div, container);
  });
  mermaid.run({ querySelector: ".mermaid" });
});
</script>
