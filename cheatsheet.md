---
layout: default
title: Cheat Sheet
---

[← Back to Home](index.html) · [Question Bank →](questions.html) · [Answers →](answers.html) · [Diagrams →](diagrams.html) · [Patterns →](patterns.html) · [Sources →](sources.html) · [Simulator →](simulator.html) · [Cheat Sheet →](cheatsheet.html) · [Glossary →](glossary.html) · [Company Prep →](company-prep.html)

# AI Prep Buddy — Day-of-Interview Cheat Sheet

The condensed version. Read this in the 20 minutes before your interview, not the full 1140-question bank. Organized around the questions you're most likely to actually get.

---

## The 5 Anthropic Agent Patterns (memorize the names)

**Prompt Chaining → Routing → Parallelization → Orchestrator-Worker → Evaluator/Optimizer.** If asked "how would you architect an agent," name the pattern that fits before describing it. Default answer to "should I build an agent for this": *"find the simplest solution possible — often this means not building agentic systems at all."*

## System Design: The Universal Opening Move

For **any** system-design question: clarify scale → state your latency/cost budget → sketch data flow → call out the failure mode you're most worried about → name the eval/monitoring plan. Interviewers grade the *process*, not whether you land on the "right" architecture.

## The 6 Patterns That Answer 80% of System-Design Questions

1. **Two-stage retrieve-then-rank** (RAG, search, recsys) — cheap broad candidate generation → expensive precise re-ranking on a shortlist.
2. **Gateway + fallback chain** — one abstraction layer, provider-agnostic, automatic failover, never single-source a dependency.
3. **Eval-gated CI/CD** — golden dataset → shadow → canary → full rollout, with rollback at every stage.
4. **Human-in-the-loop risk tiering** — auto-execute low-risk/reversible actions, gate high-risk/irreversible ones.
5. **Online + offline feature store from one definition** — eliminates training/serving skew by construction.
6. **Defense-in-depth guardrails** — input filter → hardened system prompt → output filter → structural validation. No single layer is ever sufficient alone.

## Post-Training, Current State (say this, not just RLHF)

`SFT → alignment stage`. For **reasoning capability**: GRPO + RLVR is now the frontier default (DeepSeek-R1, GPT-5.3, Nemotron 3) — verifiable rewards (math/code correctness), no separate reward model, no critic network. For **general preference alignment** (tone, safety, helpfulness): DPO/RLHF still used. Don't just say "RLHF" as the whole answer in 2026 — it reads as dated.

## Inference/Serving, Current State

vLLM = production default (PagedAttention, broad compatibility). **SGLang** = real competitor now, wins on prefix-heavy workloads (chat/RAG/agents) via RadixAttention. TensorRT-LLM = max throughput, single stable model, NVIDIA lock-in, compile step. TGI = deprecated (Dec 2025). If asked "what would you deploy today" — mention SGLang, not just vLLM.

## The One-Liner Definitions You'll Get Asked Cold

- **Why scale attention by √d_k**: prevents large dot products from pushing softmax into vanishing-gradient regions as dimension grows.
- **Why GQA over MHA**: cuts KV-cache memory/bandwidth (the real serving bottleneck) while keeping most of MHA's quality.
- **Why KL penalty in RLHF/DPO**: stops the policy from drifting so far from the reference model that it reward-hacks.
- **Why LoRA works**: the *update* to pretrained weights for a new task is usually low-rank, so you don't need full-rank trainable weights.
- **Bias-variance tradeoff**: high bias = underfits (too simple); high variance = overfits (too sensitive to training noise).
- **Why RAG can worsen hallucination**: bad retrieval → confident answer grounded in the wrong context. RAG only helps if retrieval quality is genuinely high.

## Real Incidents Worth Citing (stronger than hypotheticals)

- **Air Canada (2024)**: chatbot invented a refund policy; tribunal held the airline legally liable. → *Companies own their AI's claims.*
- **Cyera Research (May 2026)**: 344 verified enterprise-harm cases from AI agents, 188 with zero external attacker — the agent did it alone. → *Excessive agency is a live risk, not theoretical.*
- **McDonald's/Paradox.ai breach (2025)**: 64,000 applicants exposed via a weak password + IDOR, not a sophisticated AI attack. → *AI vendor due diligence = standard security hygiene too.*

## Governance Framework Names (drop these, don't over-explain)

**NIST AI RMF** (Govern/Map/Measure/Manage) · **ISO/IEC 42001** (AI management system, not a one-time checklist) · **EU AI Act** high-risk obligations (currently a live compliance deadline — Annex III enforcement was slated for Aug 2, 2026, with a proposed-but-not-fully-enacted delay to Dec 2027 in play; say *"the exact date is in flux, but the obligation categories are what matter architecturally"* if pressed) · **SR 11-7** (banking model risk — independent validation + ongoing monitoring).

## Behavioral: The Structure That Actually Works

STAR, but the **Action** should show *judgment under ambiguity* and the **Result** should include *what you'd do differently* — interviewers weight self-awareness about failure more than a clean success story.

## Questions to Ask Them (don't skip this)

One specific, current question about their architecture/research direction — not about perks or generic "what's the culture like." Shows you did homework, not just interview prep.

## If You Freeze

Say the pattern name out loud even if you haven't fully worked out the details — "this looks like a two-stage retrieve-then-rank problem, let me think through the ranking stage" buys you thinking time and shows structured reasoning, which is what's actually being graded.

---

*Full depth on every topic here: `README.md` (questions) → `ANSWERS.md` (frameworks) → `ARCHITECTURE_DIAGRAMS.md` + `DESIGN_PATTERNS_CATALOG.md` (diagrams) → `REAL_WORLD_SOURCES.md` (citations).*
