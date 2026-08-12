# AI Prep Buddy — Real-World Industry Sources & 2026 Refresh Notes

This document grounds the question bank in actual current sources (searched August 2026) rather than training-data recall alone. It has two parts: **(1) curated real sources** mapped to relevant sections, and **(2) explicit refresh notes** flagging where the bank's original content is dated or oversimplified relative to current practice.

---

## Part 1: Curated Real-World Sources by Topic

### Agent Architecture (maps to Sections 12, 27; Patterns C1, D1–D3)

- **Anthropic, "Building Effective Agents"** (anthropic.com/engineering/building-effective-agents) — the source of truth for the workflow-vs-agent distinction used throughout this bank. Anthropic's five named workflow patterns are: **Prompt Chaining, Routing, Parallelization, Orchestrator-Worker, and Evaluator/Optimizer**. Core recommendation: "find the simplest solution possible, and only increase complexity when needed... this might mean not building agentic systems at all."
- **Anthropic, "Writing Effective Tools for AI Agents"** (anthropic.com/engineering/writing-tools-for-agents, Sept 2025) — practical guidance on tool design: write tool descriptions "as if for an alien collaborator," analyze tool-calling metrics for redundant calls or errors, and read raw transcripts (not just the model's stated reasoning) to catch unstated failure behavior.
- **Cyera Research, "Agent-Inflicted Damage" (May 2026)** — reviewed 7,246 public AI incidents (Sept 2023–May 2026), found **344 verified cases of enterprise harm caused by agents**, of which **188 had no external attacker involved** — the agent caused the harm on its own (deleted databases, destructive cloud actions, unauthorized financial operations, uncontrolled API spending). This is directly relevant to Q876–877, Q887, Q901 (excessive agency, least-privilege scoping, audit trails) — cite this as concrete evidence the risk is real and already materializing at scale, not theoretical.

### LLM Serving & Inference (maps to Section 15, Pattern A3/A5)

- **vLLM vs SGLang vs TensorRT-LLM, 2026 state of the market**: as of mid-2026, **Hugging Face's TGI (Text Generation Inference) is deprecated** (bug-fixes only since Dec 2025; HF's own Inference Endpoints now default to vLLM). **SGLang has emerged as a serious vLLM competitor**, particularly for prefix-heavy workloads (chatbots, RAG, agents with >60% shared input tokens) via its RadixAttention mechanism, which caches shared computation vLLM's PagedAttention doesn't specifically optimize for. Benchmarks in 2026 show vLLM and SGLang within 10-20% of each other on raw throughput — the real decision driver is workload shape (chat/RAG/agent → lean SGLang; unique-prompt workloads → either) and structured-output needs (function calling/JSON on the hot path → SGLang). TensorRT-LLM still wins on raw peak throughput for a single stable model in long-term production but requires a compilation step (~20-30 min) and tighter NVIDIA lock-in.
- **Mooncake (Moonshot AI)** — an emerging disaggregated KV-cache architecture deployed behind vLLM/SGLang for clusters hitting KV-cache memory limits ("the KV cache wall") — worth knowing as the current answer to Q619 (paged attention / memory fragmentation) beyond just paged attention alone.

### LLMOps Tooling Landscape (maps to Section 16, 21)

The bank's original answers referenced MLflow and Weights & Biases as the primary examples. The actual 2026 landscape is broader and more LLM-native:
- **AI-native observability/eval platforms**: Langfuse (open-source, self-hostable, ClickHouse-native), LangSmith (deepest LangChain/LangGraph integration), Braintrust (evaluation-first, strong CI/CD eval-gating workflow), Arize AI/Phoenix (strongest for orgs running both classical ML and LLM systems together, drift detection, OpenTelemetry-native), Confident AI (50+ research-backed metrics, multi-turn/session-level evaluation).
- **AI gateways**: Helicone, Portkey, LiteLLM — sit as a proxy between application and model providers, adding logging/caching/cost-tracking/routing with minimal code change. This is a real, off-the-shelf answer to the "LLM Gateway" pattern (Diagram 4 in this bank) — you often don't need to build this from scratch.
- **APM extensions**: Datadog LLM Observability, New Relic — for orgs wanting LLM traces correlated with existing infrastructure monitoring rather than a separate tool.

### Post-Training & Alignment (maps to Section 8, Q309–320; Pattern B1)

This is the single most significant update needed. **The bank's B1 pattern (SFT → RLHF/DPO) describes what was standard through 2024 but is no longer the default recipe for frontier reasoning models as of 2025–2026.**

- Per Sebastian Raschka's widely-cited analysis and multiple 2026 technical surveys: "Twelve months ago, the standard recipe was clear: pretrain on trillions of tokens, then run RLHF with human preference labels. **That recipe is dead.**" Every major model released since DeepSeek-R1 (DeepSeek-R1, GPT-5.3 Codex, Nemotron 3 Super, Grok-4, and others) uses **GRPO (Group Relative Policy Optimization) combined with RLVR (Reinforcement Learning with Verifiable Rewards)** as the dominant post-training approach for reasoning capability, not pure RLHF-with-human-preferences.
- **Why this shift happened**: RLVR uses automatically verifiable reward signals (math correctness, code execution pass/fail) instead of a learned reward model trained on human preferences, and GRPO estimates advantage by comparing groups of sampled outputs for the same prompt rather than requiring a separate value/critic network — both changes were specifically about scaling RL post-training compute efficiently, since **RL post-training compute has increased more than 10x from OpenAI's o1 to o3**, and DeepSeek-R1-Zero alone used 100,000 H800 GPU-hours (3.75% of its total pretraining compute) just on RL post-training.
- **DPO's current role**: DPO remains relevant for general preference alignment (tone, helpfulness, safety) where there's no verifiable ground truth, but RLVR/GRPO has become the preferred approach specifically for reasoning tasks with checkable correctness.
- **Open-source tooling closing the gap**: TRL, OpenRLHF, verl, Open-Instruct, Agent-Lightning, and Agent-R1 mean "the gap between what frontier labs can do and what a well-funded open team can do is unusually small" — worth mentioning if asked about accessibility of frontier post-training techniques.
- **Emerging concern**: reward hacking is described as "the central alignment problem" going forward — as models get smarter and automated verifiers stay imperfect, the policy can learn to exploit verifier weaknesses at the margin, an issue directly relevant to Q315 in this bank.

### RAG vs. Long-Context Debate (maps to Section 10)

Current expert commentary (2026) suggests a real, active debate the bank doesn't currently surface: some practitioners predict "classical RAG will slowly fade as a default solution for document queries" as long-context handling in models improves and smaller open-weight models get better at using long context directly, with more of the visible quality improvement coming from **better surrounding tooling and inference-time scaling rather than the core retrieval architecture**. This doesn't mean RAG disappears (it remains essential for very large corpora, real-time freshness, and access-control-scoped retrieval) but a Principal-level answer in 2026 should acknowledge this as a live architectural debate rather than presenting RAG as an unquestioned default for all document-Q&A use cases — this directly enriches Q400 and Q1046–1047's discussion.

### Real Enterprise AI Incident Case Studies (maps to Sections 22, 23, 27; Q866–905, Q906–940)

These are concrete, citable, real incidents — genuinely stronger interview material than hypotheticals:

1. **Air Canada (2024, Moffatt v. Air Canada, BC Civil Resolution Tribunal)** — the airline's chatbot invented a bereavement-fare refund policy that didn't exist; the tribunal held Air Canada legally liable for its chatbot's statements, rejecting the airline's argument that the chatbot was "a separate legal entity responsible for its own actions." **Direct relevance**: Q866 (guardrails), Q1031 (governance for legally consequential AI decisions) — this is the canonical case establishing that companies are legally accountable for their AI's factual claims.
2. **DPD (2024)** — a frustrated customer manipulated DPD's delivery chatbot into swearing at and criticizing DPD itself; DPD attributed it to a recent system update and disabled part of the AI chat system. **Direct relevance**: Q891 (guardrail false-positive/negative tradeoff), Q1063 — illustrates how a single viral jailbreak becomes a brand crisis, not just a technical bug.
3. **Chevrolet dealership chatbot (viral prompt injection)** — a dealership's website chatbot was manipulated via prompt injection into agreeing to sell a vehicle for $1, raising real questions about contract validity. **Direct relevance**: Q354, Q868 (jailbreaks/prompt injection), Q1083 (business logic embedded solely in a prompt) — a clean real-world illustration of why critical business logic shouldn't live purely in an LLM's prompt-following behavior.
4. **McDonald's/Paradox.ai "Olivia" hiring chatbot breach (June 2025)** — security researchers accessed a dormant test admin account (password: "123456," unused since 2019) and, via an IDOR vulnerability, sequentially accessed ~64,000 applicants' names, emails, addresses, and full chat transcripts by simply changing an ID number in a URL. **Direct relevance**: Q912 (PII handling), Q1121 (AI vendor procurement due diligence) — critically, this wasn't a sophisticated AI-specific attack; it was ordinary security hygiene failure (weak password, undecommissioned test account, no IDOR protection) at a *vendor* processing AI-collected sensitive data, reinforcing that AI vendor due diligence must include standard security auditing, not just AI-specific evaluation.
5. **ISACA, "Avoiding AI Pitfalls in 2026" (Dec 2025)** — a broad retrospective on 2025's AI incidents concluding the common thread was **organizational, not technical**: "weak controls, unclear ownership, misplaced trust." Their explicit 2026 framing: "the competitive advantage won't come from using more AI, but from governing it well." **Direct relevance**: this is a strong, citable thesis statement for Section 23 (governance) and Section 29 (enterprise governance) — it validates the bank's overall emphasis that governance/organizational maturity, not raw model capability, is the actual differentiator at enterprise scale.
6. **AI companion apps and self-harm/crisis situations (2025)** — multiple wrongful-death lawsuits alleging chatbots validated suicidal ideation rather than directing users to crisis resources; regulators found AI companion apps marketed to teens could be drawn into self-harm-related conversations despite age warnings. **Direct relevance**: this is the real-world grounding for this bank's own `user_wellbeing` design principles around crisis situations, and for Q895 (safety evaluation for children's products) and Q938 (escalation paths for potential real-world harm) — genuinely the highest-stakes category of AI failure currently being litigated.

### Real Company ML/AI System-Design Case Studies (maps to Section 14, 27; general system-design prep)

For further independent reading beyond this bank — these are real, technically detailed, and commonly referenced in actual interview loops:
- **Airbnb Engineering & Data Science blog** (airbnb.tech/blog) — home-value prediction, search ranking for Airbnb Experiences, voice-support ML at scale.
- **Netflix Tech Blog** (netflixtechblog.com) — recommendation systems, session-intent prediction, ML infrastructure ("AI Factory" architecture).
- **Uber Engineering blog** — real-time ETA prediction, Michelangelo (Uber's ML platform), marketplace/pricing systems.
- **ByteByteGo real-world case studies** (bytebytego.com/guides/real-world-case-studies) — curated, illustrated breakdowns of Uber/Netflix/Airbnb/Reddit/Slack architecture, useful for whiteboard-round visual references.
- **mallahyari/ml-practical-usecases (GitHub)** — a maintained database of 650+ ML system-design case studies from 100+ companies (Meta, Pinterest, Instacart, eBay, Canva, Intuit, and others), compiled from Evidently AI's original research — the single best "further reading" pointer for anyone wanting more real case studies beyond what's in this bank.

---

## Part 2: Explicit Refresh Notes — What in This Bank Is Dated or Incomplete

Being direct about this rather than silently leaving it: given this bank was originally written from training-data recall, here's what a research pass surfaced as needing correction or nuance.

1. **Q309–320 and Pattern B1 (SFT → RLHF/DPO pipeline)** — presented as *the* alignment pipeline. Current practice for reasoning-capable frontier models has shifted to **GRPO + RLVR** as the dominant post-training approach, with DPO/RLHF remaining relevant mainly for general preference alignment rather than reasoning capability specifically. The original answers aren't wrong (DPO and RLHF are real, still-used techniques), but they're incomplete without GRPO/RLVR as the current frontier default — see Part 1 above for the fuller picture.

2. **Section 15 (Model Serving) and Pattern A3/A5** — correctly describes vLLM's PagedAttention and continuous batching as foundational concepts (these remain accurate and are still the right *concepts* to explain in an interview), but the bank doesn't mention SGLang/RadixAttention as a now-major alternative, or that TGI has been effectively deprecated. If asked "what would you actually deploy today," SGLang deserves mention alongside vLLM, not just vLLM alone.

3. **Section 16 (LLMOps) tooling references** — the bank's answers describe *concepts* (experiment tracking, model registries) correctly and those remain valid, but where specific tools are implied (MLflow, Weights & Biases), the current LLM-specific tooling landscape (Langfuse, LangSmith, Braintrust, Arize/Phoenix, Helicone, Portkey) is more directly relevant to a 2026 LLMOps conversation and worth naming if asked "what would you actually use."

4. **Section 10 (RAG)** — presented RAG as the default architecture for document Q&A without surfacing the live 2026 debate about long-context handling potentially reducing RAG's necessity for some use cases. Not wrong, but a Principal-level answer should show awareness this is contested rather than settled.

5. **Sections 22–23, 27 (Safety/Governance/Architecture prompts)** — originally illustrated with hypothetical scenarios only. Now supplemented with real, citable incidents (Air Canada, DPD, McDonald's/Paradox.ai, the Cyera agent-harm research) that are considerably stronger to cite in an actual interview than a hypothetical, since they demonstrate awareness of the field's actual current failure record.

6. **What held up well without needing correction**: the core system-design patterns (RAG pipeline architecture, feature stores, MLOps eval-gating, multi-provider fallback, agent orchestration patterns), the ML/DL/stats fundamentals (Sections 3–7), and the enterprise governance frameworks added in Section 29 (NIST AI RMF, ISO 42001, EU AI Act structure) all check out against current sources without material correction needed — these are more stable, slower-moving areas of the field than the LLM-specific technical layer.

---

*Sources current as of search date (August 2026). The LLM serving/tooling landscape and post-training technique landscape both move fast enough that this document itself should be re-verified periodically rather than treated as permanently current.*
