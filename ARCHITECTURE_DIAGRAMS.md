# AI Prep Buddy — Architecture Diagrams, Flows & Worked Examples

Diagrams for the highest-value system-design questions in the bank (Sections 13, 14, 27). GitHub renders Mermaid natively — view this file directly on github.com to see the diagrams.

---

## 1. RAG System (Q376, Q499, Q552) — Document Q&A at Scale

```mermaid
flowchart TD
    U[User Query] --> QR[Query Rewrite / Expansion]
    QR --> EMB[Embed Query]
    EMB --> HYB{Hybrid Retrieval}
    HYB --> DENSE[Dense Vector Search]
    HYB --> SPARSE[BM25 Keyword Search]
    DENSE --> FUSE[Reciprocal Rank Fusion]
    SPARSE --> FUSE
    FUSE --> META[Metadata / Access-Control Filter]
    META --> RERANK[Cross-Encoder Re-ranker]
    RERANK --> TOPK[Top-K Chunks]
    TOPK --> PROMPT[Assemble Grounded Prompt]
    PROMPT --> LLM[LLM Generation]
    LLM --> CITE[Citation Validation]
    CITE --> RESP[Response to User]

    DOC[Documents] --> CHUNK[Chunking + Metadata]
    CHUNK --> EMBIDX[Embed]
    EMBIDX --> VDB[(Vector DB)]
    CHUNK --> BM25IDX[(BM25 Index)]
    VDB --> DENSE
    BM25IDX --> SPARSE
```

**Flow:** Query gets rewritten for retrieval, embedded, searched via both dense (semantic) and sparse (keyword) paths in parallel, fused via reciprocal rank fusion, filtered by access-control metadata, then re-ranked by a cross-encoder before the top chunks are assembled into a grounded prompt. Citation validation checks the final answer's claims are actually supported before returning to the user.

**Worked example:** A 50M-document internal knowledge base. Query "What's our refund policy for enterprise customers signed before 2023?" → hybrid search catches both semantic matches ("refund policy") and exact terms ("enterprise", "2023") → metadata filter restricts to policy-type documents the requesting user's role can see → re-ranker promotes the specific enterprise-tier clause over general consumer refund text → LLM generates an answer citing the exact clause number → citation validator confirms that clause actually contains the stated terms before returning.

---

## 2. Customer Support Agent with Escalation (Q496)

```mermaid
flowchart TD
    MSG[Incoming Message] --> INTENT[Intent Classification]
    INTENT -->|Informational| RAG[RAG: Knowledge Base]
    INTENT -->|Account Action| TOOLS[Tool-Calling Layer]
    INTENT -->|Ambiguous/Low Confidence| HUMAN1[Escalate: Human]

    TOOLS --> ORDERSTATUS[Order Status Tool]
    TOOLS --> REFUND{Refund within policy?}
    REFUND -->|Yes, auto-approvable| EXECUTE[Execute Action]
    REFUND -->|No / exceeds limit| CONFIRM[Human Confirmation Required]

    RAG --> CONF{Confidence Check}
    CONF -->|High| RESPOND[Respond to User]
    CONF -->|Low| HUMAN2[Escalate: Human]

    EXECUTE --> LOG[Audit Log]
    CONFIRM --> LOG
    HUMAN1 --> LOG
    HUMAN2 --> LOG
```

**Flow:** Every message is classified by intent first. Informational queries go through RAG with a confidence gate before responding; account actions go through scoped tools where anything outside pre-approved policy limits requires human confirmation. Every path — automated or escalated — writes to an audit log.

**Worked example:** "Where's my order #4521?" → intent = account action → order-status tool called directly, low-risk read-only action, auto-executed. "I want a $2,000 refund" → intent = account action → refund tool checks policy limit (say $200 auto-approval cap) → exceeds limit → routes to human agent with full context (order history, conversation so far) pre-loaded, rather than the user having to repeat themselves.

---

## 3. Multi-Agent Orchestration (Q455, Q456, Q472)

```mermaid
flowchart TD
    TASK[Complex Task] --> ORCH[Orchestrator Agent]
    ORCH --> PLAN[Decompose into Sub-tasks]
    PLAN --> A1[Worker Agent: Research]
    PLAN --> A2[Worker Agent: Analysis]
    PLAN --> A3[Worker Agent: Writing]

    A1 --> STATE[(Shared State / Blackboard)]
    A2 --> STATE
    A3 --> STATE

    STATE --> CRITIC[Critic / Verifier Agent]
    CRITIC -->|Pass| AGG[Aggregate Final Output]
    CRITIC -->|Fail| REPLAN[Re-plan / Retry Sub-task]
    REPLAN --> PLAN

    ORCH -.budget/step limit.-> KILL[Hard Stop if Exceeded]
```

**Flow:** The orchestrator decomposes a task into sub-tasks handed to specialized worker agents, each reading/writing to shared state rather than passing messages point-to-point. A critic agent validates the combined output before final aggregation; failures trigger targeted re-planning of just the failed sub-task, not the whole pipeline. A hard step/budget limit bounds worst-case cost regardless of how re-planning goes.

**Worked example:** "Write a competitive analysis of three SaaS products." Orchestrator splits into: Research agent (gathers facts per product via web search/tool calls), Analysis agent (compares features/pricing against shared state), Writing agent (drafts the final report). Critic checks the draft against the original research for unsupported claims. If it flags an unsupported claim about Product B's pricing, only the Research agent re-runs that specific lookup — not the whole pipeline.

---

## 4. LLM Gateway / Model Routing (Q502, Q503, Q517, Q519)

```mermaid
flowchart TD
    REQ[Incoming Request] --> GW[LLM Gateway]
    GW --> AUTH[Auth + Rate Limit]
    AUTH --> CLASSIFY{Complexity Classifier}
    CLASSIFY -->|Simple| SMALL[Small/Cheap Model]
    CLASSIFY -->|Complex| LARGE[Large Model]
    CLASSIFY -->|High-stakes| VERIFY[Large Model + Verifier Pass]

    GW --> CACHE{Semantic Cache Hit?}
    CACHE -->|Yes| RETURN1[Return Cached Response]
    CACHE -->|No| CLASSIFY

    SMALL --> HEALTH{Provider Healthy?}
    LARGE --> HEALTH
    VERIFY --> HEALTH
    HEALTH -->|No| FALLBACK[Fallback Provider]
    HEALTH -->|Yes| RESPOND[Response]
    FALLBACK --> RESPOND

    GW --> LOG[Cost / Latency / Trace Logging]
```

**Flow:** All requests pass through a single gateway handling auth, rate limiting, and semantic caching before any model call. A complexity classifier routes simple queries to a cheap model and complex/high-stakes ones to a larger model (with an added verifier pass for the latter). Every path checks provider health and fails over automatically; every request is logged centrally for cost/latency observability regardless of which model served it.

**Worked example:** 50 internal teams share one gateway. Team A's "summarize this ticket" requests get classified as simple → routed to a small model at $0.10/1M tokens. Team B's "draft this legal clause" requests get classified as high-stakes → routed to a large model plus a verifier pass checking the output against a compliance rubric before returning. If the primary large-model provider is down, the gateway automatically fails over to a secondary provider — neither team's integration code changes.

---

## 5. Feature Store: Online + Offline Paths (Q559, Q615, Q701)

```mermaid
flowchart LR
    subgraph Sources
        BATCH[Batch Data Warehouse]
        STREAM[Kafka Event Stream]
    end

    BATCH --> OFFLINE[(Offline Store)]
    STREAM --> ONLINE[(Online Store - Low Latency)]
    STREAM --> OFFLINE

    OFFLINE --> TRAIN[Training Pipeline]
    TRAIN --> MODEL[Trained Model]

    ONLINE --> SERVE[Real-Time Inference]
    MODEL --> SERVE
    SERVE --> PRED[Prediction]

    DEF[Shared Feature Definitions] -.governs.-> OFFLINE
    DEF -.governs.-> ONLINE
```

**Flow:** Both the online (low-latency, point-lookup) and offline (batch, historical-scan) stores are populated from the same shared feature definitions, so a feature computed for training matches exactly what's computed at serving time — eliminating training/serving skew by construction rather than by discipline alone.

**Worked example:** A "user's 7-day average order value" feature is defined once. The offline store computes it in nightly batch for generating training data (with point-in-time correctness — only orders before each historical training-example date). The online store computes the same definition incrementally from the Kafka order-event stream, so a fraud model scoring a live transaction sees a feature computed identically to what it was trained on.

---

## 6. Real-Time Fraud Detection (Q557, Q575)

```mermaid
flowchart TD
    TXN[Transaction Event] --> STREAM[Streaming Feature Pipeline]
    STREAM --> VELOCITY[Velocity Checks: cached]
    STREAM --> DEVICE[Device Fingerprint: cached]
    VELOCITY --> MODEL[Lightweight GBM Model]
    DEVICE --> MODEL
    MODEL --> SCORE{Risk Score}
    SCORE -->|Low| APPROVE[Approve <100ms]
    SCORE -->|Medium| RULES[Rule-Based Secondary Check]
    SCORE -->|High| BLOCK[Block + Review Queue]

    MODEL -.fallback if unavailable.-> RULEFALLBACK[Rule-Based-Only Fallback]

    MONITOR[Drift Monitor] -.watches.-> MODEL
    MONITOR -->|Drift Detected| RETRAIN[Trigger Retraining]
```

**Flow:** Precomputed/cached features (velocity, device fingerprint) feed a lightweight model chosen specifically to fit the sub-100ms latency budget. Scores route to approve/secondary-check/block tiers. A rule-based fallback exists for if the model service itself is unavailable — fraud detection can't simply fail open. Continuous drift monitoring triggers retraining given how fast fraud patterns evolve.

**Worked example:** A $9,000 transaction from a new device in a new country scores high risk (device + velocity signals both fire) → blocked and routed to a human review queue in under 100ms, while a $12 transaction from a recognized device with normal velocity approves automatically in the same latency budget.

---

## 7. Two-Stage Recommendation System (Q556, Q965)

```mermaid
flowchart TD
    USER[User Context] --> CANDGEN[Candidate Generation]
    CANDGEN --> CF[Collaborative Filtering]
    CANDGEN --> TWOTOWER[Two-Tower Embedding Retrieval]
    CF --> CANDIDATES[~500 Candidates]
    TWOTOWER --> CANDIDATES

    CANDIDATES --> RANK[Ranking Model]
    RANK --> FEATURES[Rich Features: user+item+context]
    FEATURES --> RANK
    RANK --> RERANK[Business Rules: diversity, margin]
    RERANK --> TOP[Top-N Shown to User]

    TOP --> FEEDBACK[Click/Purchase Feedback]
    FEEDBACK -.retrains.-> CF
    FEEDBACK -.retrains.-> RANK
```

**Flow:** Candidate generation cheaply narrows millions of items to a few hundred plausible ones (via CF and/or embedding retrieval); a more expensive, feature-rich ranking model then precisely orders that shortlist; a final business-rules pass adjusts for diversity/margin before display. Feedback closes the loop back into both stages.

**Worked example:** An e-commerce homepage. Candidate generation narrows 2M products to 500 based on the user's embedding similarity to past purchases. The ranking model scores those 500 using richer features (recency, price sensitivity, current session behavior) unavailable to the cheap candidate-generation stage. A final diversity rule ensures the top 20 shown aren't all the same product category, even if the raw ranking model would have clustered them.

---

## 8. MLOps CI/CD Pipeline with Eval Gates (Q646, Q663, Q810)

```mermaid
flowchart LR
    PR[Pull Request: prompt/model/code change] --> CI[CI Pipeline]
    CI --> UNIT[Unit Tests]
    CI --> GOLDEN[Golden Eval Suite]
    GOLDEN --> SCORE{Score >= Threshold?}
    SCORE -->|No| BLOCK[Block Merge]
    SCORE -->|Yes| MERGE[Merge to Main]
    MERGE --> STAGE[Deploy to Staging]
    STAGE --> SHADOW[Shadow Traffic Test]
    SHADOW --> CANARY[Canary: 5% Production Traffic]
    CANARY --> MONITOR{Quality/Cost/Latency OK?}
    MONITOR -->|No| ROLLBACK[Auto-Rollback]
    MONITOR -->|Yes| FULL[Full Production Rollout]
```

**Flow:** Every prompt, model, or code change touching the AI system runs through the same eval-gated pipeline as standard software: unit tests plus a golden eval suite must pass before merge, then staged rollout (staging → shadow → canary → full) with automated rollback if quality/cost/latency metrics degrade at any stage.

**Worked example:** An engineer tweaks a system prompt to be more concise. CI runs the golden eval suite automatically — if the tweak accidentally drops required disclaimers on 3 test cases, the merge is blocked with a specific failure report, not just a pass/fail flag. Once fixed and merged, the change goes to 5% of production traffic first; if cost drops as intended with no quality regression in monitored metrics, it ramps to 100%.

---

## 9. Multi-Provider Fallback / Disaster Recovery (Q527, Q555, Q1025)

```mermaid
flowchart TD
    REQ[Request] --> GW[Gateway]
    GW --> P1{Primary Provider Healthy?}
    P1 -->|Yes| CALL1[Call Primary]
    P1 -->|No| P2{Secondary Provider Healthy?}
    P2 -->|Yes| CALL2[Call Secondary]
    P2 -->|No| P3[Self-Hosted Small Model]
    P3 --> DEGRADED[Degraded Mode: clear UX messaging]

    CALL1 --> HEALTHCHECK[Continuous Health Check]
    CALL2 --> HEALTHCHECK
    HEALTHCHECK -.updates.-> P1
    HEALTHCHECK -.updates.-> P2
```

**Flow:** A layered fallback chain — primary provider, secondary provider, then a self-hosted last-resort model — ensures the product degrades gracefully rather than failing outright even if every external dependency is down simultaneously. Continuous health checks (not just reactive failure detection) keep routing decisions current.

**Worked example:** Primary provider has a regional outage. Health checks detect elevated error rates within seconds and route new requests to the secondary provider automatically — users experience slightly different response style but no visible outage. If both external providers were somehow down, the self-hosted fallback model keeps core functionality alive with a UI banner: "Running in reduced-capacity mode."

---

## 10. Cost-Optimized Serving: Caching + Batching + Quantization (Q502, Q610, Q622)

```mermaid
flowchart TD
    REQ[Request] --> EXACTCACHE{Exact Cache Hit?}
    EXACTCACHE -->|Yes| RETURN1[Return Instantly]
    EXACTCACHE -->|No| SEMCACHE{Semantic Cache Hit?}
    SEMCACHE -->|Yes, above threshold| RETURN2[Return Cached]
    SEMCACHE -->|No| BATCH[Continuous Batching Queue]
    BATCH --> QUANT[Quantized Model - INT8]
    QUANT --> KVCACHE[Paged Attention / KV Cache]
    KVCACHE --> GEN[Generate Response]
    GEN --> STORECACHE[Write to Cache]
    STORECACHE --> RETURN3[Return Response]
```

**Flow:** Cheapest option checked first (exact cache), then semantic cache (catches paraphrased repeats), only falling through to actual inference — which itself uses continuous batching, a quantized model, and paged-attention KV cache management to maximize throughput per GPU-dollar.

**Worked example:** An FAQ-heavy support bot gets "how do I reset my password" 10,000 times a day phrased 50 different ways. Exact-match cache catches identical repeats; semantic cache (embedding similarity above 0.92) catches "I forgot my password, help" as effectively the same query — only genuinely novel queries reach the model, cutting inference volume by ~70% in this example.

---

## 11. Evaluation Pipeline: Offline + Judge + Online (Q831, Q865)

```mermaid
flowchart TD
    CHANGE[Prompt/Model Change] --> OFFLINE[Offline: Golden Dataset]
    OFFLINE --> AUTOMETRIC[Task-Specific Metrics: exact match, execution tests]
    OFFLINE --> JUDGE[LLM-as-Judge: rubric scoring]
    JUDGE --> CALIBRATE{Calibrated vs Human Ratings?}
    CALIBRATE -->|Drift Detected| RECALIBRATE[Recalibrate Judge]

    AUTOMETRIC --> GATE{Pass Threshold?}
    JUDGE --> GATE
    GATE -->|Yes| SHADOW[Shadow on Real Traffic]
    SHADOW --> CANARY[Canary A/B]
    CANARY --> IMPLICIT[Implicit Signals: thumbs down, retry rate]
    IMPLICIT --> DECISION{Ship Full?}
    DECISION -->|Yes| PROD[Full Production]
    DECISION -->|No| REVERT[Revert / Iterate]
```

**Flow:** Offline task-specific metrics (fast, cheap, unambiguous where possible) combine with LLM-as-judge scoring (periodically recalibrated against human ratings to catch judge drift) as a pre-deployment gate. Only after passing does a change proceed to shadow testing on real traffic, then canary A/B with implicit online signals as the final real-world check before full rollout.

**Worked example:** A new prompt variant scores well on the golden dataset and passes judge calibration. In shadow mode it looks fine. In canary (5% traffic), thumbs-down rate ticks up 2x versus control even though offline scores were equal — revealing the offline eval set didn't cover a real usage pattern. The team reverts, adds the missed pattern to the golden dataset, and re-runs the full pipeline before trying again.

---

## 12. Agentic RAG with Self-Correction (Q397, Q402)

```mermaid
flowchart TD
    Q[Query] --> AGENT[Agent Reasoning Loop]
    AGENT --> DECIDE{Need to Retrieve?}
    DECIDE -->|Yes| RETRIEVE[Retrieve Chunks]
    DECIDE -->|No, have enough info| GENERATE[Generate Answer]
    RETRIEVE --> ASSESS{Retrieved Content Sufficient/Relevant?}
    ASSESS -->|No| REFORMULATE[Reformulate Query]
    REFORMULATE --> RETRIEVE
    ASSESS -->|Yes| GENERATE
    GENERATE --> SELFCHECK{Self-Check: Grounded?}
    SELFCHECK -->|No| RETRIEVE
    SELFCHECK -->|Yes| RESPOND[Final Answer]
```

**Flow:** Unlike single-shot RAG, the agent decides for itself whether retrieved content is sufficient, reformulating and re-retrieving if not, and self-checks whether its draft answer is actually grounded in what was retrieved before finalizing — trading latency/cost for meaningfully higher reliability on hard multi-hop questions.

**Worked example:** "Which of our three EU offices has the highest attrition, and what's the top cited reason?" First retrieval finds attrition rate documents but not exit-interview reason data. The agent's assessment step recognizes the gap, reformulates a second query specifically for "exit interview reasons," retrieves that separately, and only then generates a combined answer — rather than a single-shot system generating a plausible-but-incomplete answer from the first retrieval alone.

---

## 13. Multi-Region, Data-Residency-Compliant Architecture (Q529, Q630, Q791)

```mermaid
flowchart TD
    USER_EU[EU User] --> LB[Geo-Routing Load Balancer]
    USER_US[US User] --> LB
    LB --> EUREGION[EU Region: EU-hosted model, EU data only]
    LB --> USREGION[US Region: independent stack]

    EUREGION --> EUDATA[(EU Data Store)]
    USREGION --> USDATA[(US Data Store)]

    EUREGION -.no cross-region data transit.-x USDATA
    USREGION -.no cross-region data transit.-x EUDATA

    GLOBAL[Global Config/Prompt Repo] -.non-sensitive config only.-> EUREGION
    GLOBAL -.non-sensitive config only.-> USREGION
```

**Flow:** Users are geo-routed to a fully independent regional stack — model, data store, and logging all contained within that region — with an explicit architectural rule that no user data crosses regions. Only non-sensitive configuration (prompt templates, feature flags) syncs globally.

**Worked example:** An EU customer's document gets processed entirely by EU-hosted model endpoints and stored only in the EU data store, satisfying GDPR data-residency requirements. Even the gateway/logging infrastructure is regionally scoped — a common failure mode this design explicitly avoids is a "global" logging pipeline that inadvertently pipes EU request content through a US-based observability tool.

---

*These 13 diagrams cover the core recurring architecture patterns across Sections 13, 14, and 27. The same patterns (gateway/routing, caching layers, fallback chains, eval-gated CI/CD, two-stage retrieval-then-rank, and human-in-the-loop escalation) recombine to answer most of the remaining open-ended system-design questions in the bank.*
