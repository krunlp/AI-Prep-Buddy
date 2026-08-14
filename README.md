# AI Prep Buddy

**1,716 interview questions with answer frameworks for AI/ML engineering, system design and architecture loops.**

[![CI Verification](https://github.com/krunlp/AI-Prep-Buddy/actions/workflows/ci.yml/badge.svg)](https://github.com/krunlp/AI-Prep-Buddy/actions/workflows/ci.yml)
[![Questions](https://img.shields.io/badge/Questions-1716-blue?style=flat-square)](questions.md)
[![Sections](https://img.shields.io/badge/Sections-54-green?style=flat-square)](questions.md)
[![Diagrams](https://img.shields.io/badge/Diagrams-69-orange?style=flat-square)](diagrams.md)
[![JSON Dataset](https://img.shields.io/badge/Dataset-JSON-orange?style=flat-square)](data/questions.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

### ▶ [**Open the site**](https://krunlp.github.io/AI-Prep-Buddy/) · [Questions](https://krunlp.github.io/AI-Prep-Buddy/questions.html) · [Answers](https://krunlp.github.io/AI-Prep-Buddy/answers.html) · [Find your role](https://krunlp.github.io/AI-Prep-Buddy/roles.html) · [Mock simulator](https://krunlp.github.io/AI-Prep-Buddy/simulator.html)

---

## What this is

Most interview banks are lists of questions. This one pairs every question with an **answer framework** — the mechanism, the tradeoff, the follow-up the interviewer asks next, and the trap — because knowing a definition rarely survives the second question.

It covers the full modern surface: classic ML and statistics through transformers, RAG, agents, MCP/A2A interoperability, serving and inference optimisation, LLMOps, evaluation, safety, governance, cloud agent deployment, and the leadership and communication rounds that decide senior offers.

## What's inside

| | |
|---|---|
| 📋 **[Question bank](questions.md)** | 1,716 questions across 54 sections, difficulty-tagged (⭐ Standard, ⭐⭐ Hard, ⭐⭐⭐ Principal). Hover or tap any question on the site to reveal its answer. |
| ✅ **[Answer frameworks](answers.md)** | An answer for every question — not a definition, but what a strong candidate actually says. |
| 🎯 **[Role-based map](https://krunlp.github.io/AI-Prep-Buddy/roles.html)** | Pick your target role (Staff MLE, Principal AI Lead, GenAI Engineer, Platform, MLOps, Research, Security, Solutions Architect, Data Scientist, EM) and see exactly which sections to complete, with progress tracking. |
| 🎙️ **[Live Interview](https://krunlp.github.io/AI-Prep-Buddy/interview.html)** | An agentic interviewer: asks aloud, listens, then follows up on what you actually said — adaptive with an API key, gap-based without one. Ends with a scored summary. |
| 🎤 **[Mock simulator](https://krunlp.github.io/AI-Prep-Buddy/simulator.html)** | Voice-enabled. Questions read aloud, answer out loud with live transcription, then get scored — local concept-coverage analysis built in, or LLM feedback with a free API key. |
| 🏗️ **[Diagrams](diagrams.md)** + **[Patterns](patterns.md)** | 69 Mermaid architecture diagrams and conceptual patterns, each with flow, worked example and real-world industry usage. |
| 💻 **[Code solutions](code-solutions.md)** | Runnable implementations for the coding round. |
| 🗺️ **[Study paths](study-paths.md)** | Day-by-day 2-week plans for three role tracks. |
| ⚡ **[Cheat sheet](cheatsheet.md)** · **[Glossary](glossary.md)** | Day-of revision and 60+ acronyms. |
| 🏢 **[Company prep](company-prep.md)** | Reported loop structures for Anthropic, OpenAI, Google DeepMind and enterprise tracks. |
| 📚 **[Sources](sources.md)** | Cited industry sources and honest notes on what has been fact-checked and what hasn't. |

## Where to start

You are not meant to read 1,716 questions.

1. **[Pick your role](https://krunlp.github.io/AI-Prep-Buddy/roles.html)** — it narrows 54 sections down to the ones your loop actually tests, split into Core / Important / Optional.
2. **Work the Core sections**, reading questions and revealing answers as you go.
3. **[Drill in the simulator](https://krunlp.github.io/AI-Prep-Buddy/simulator.html)** — answer out loud and self-grade. Articulation under pressure is the thing being tested, not recognition.
4. **The week before:** [cheat sheet](cheatsheet.md), [multi-turn drills](questions.md) (Section 51), and [company prep](company-prep.md).

## Question formats

Beyond standard recall and design questions, the bank includes formats that senior loops actually use to separate candidates:

- **Multi-turn interviewer drills** (Section 51) — full transcripts where the interviewer pushes back turn after turn as each hypothesis is eliminated.
- **Production incident triage** (Section 50) — "429s appeared in production, what do you check, and what does each signal rule out?"
- **Spot the flaw** (Section 52) — plausible-looking designs and code with real defects to find.
- **Estimation and capacity arithmetic** (Section 53) — KV cache sizing, GPU counts, cost per task, latency budgets.
- **Executive communication** (Section 54) — explaining to a board, a CFO, a regulator, a security team.

## Data

The bank is available as JSON for building your own tools:

- [`data/questions.json`](data/questions.json) — every question with id, section and text
- [`data/answers.json`](data/answers.json) — answer lookup keyed by question id

## Sections

<details>
<summary>All 54 sections</summary>

| # | Section | Questions | Range |
|---|---|---|---|
| 1 | Strategy, Vision & Technical Leadership | 25 | 1–25 |
| 2 | Leadership & Behavioral | 40 | 26–65 |
| 3 | Classic ML Fundamentals | 70 | 66–135 |
| 4 | Statistics & Probability | 35 | 136–170 |
| 5 | Deep Learning Fundamentals | 55 | 171–225 |
| 6 | Computer Vision | 30 | 226–255 |
| 7 | NLP Fundamentals (Pre-LLM) | 30 | 256–285 |
| 8 | LLM & Transformer Fundamentals | 60 | 286–345 |
| 9 | Prompt Engineering & Structured Outputs | 30 | 346–375 |
| 10 | RAG & Retrieval | 45 | 376–420 |
| 11 | Vector Databases & Embeddings | 30 | 421–450 |
| 12 | Agentic AI & Multi-Agent Systems | 45 | 451–495 |
| 13 | LLM System Design / GenAI Architecture | 60 | 496–555 |
| 14 | Classic ML System Design | 45 | 556–600 |
| 15 | Model Serving & Inference Optimization | 45 | 601–645 |
| 16 | LLMOps & MLOps | 55 | 646–700 |
| 17 | Feature Stores & Feature Engineering | 25 | 701–725 |
| 18 | Data Engineering for AI | 40 | 726–765 |
| 19 | Cloud ML Platforms | 30 | 766–795 |
| 20 | DevOps & Infrastructure for AI | 35 | 796–830 |
| 21 | LLM Evaluation | 35 | 831–865 |
| 22 | Safety, Guardrails & LLM Security | 40 | 866–905 |
| 23 | Governance, Ethics & Responsible AI | 35 | 906–940 |
| 24 | Time Series & Forecasting | 20 | 941–960 |
| 25 | Recommender Systems | 20 | 961–980 |
| 26 | Coding & Algorithms for ML | 25 | 981–1005 |
| 27 | Open-Ended Architecture Design Prompts | 30 | 1006–1035 |
| 28 | Rapid-Fire Depth Probes | 55 | 1036–1090 |
| 29 | Enterprise AI Governance, Frameworks, Platforms & Executive Communication | 50 | 1091–1140 |
| 30 | Enterprise Agent Interoperability (MCP, A2A) & Advanced RAG | 40 | 1141–1180 |
| 31 | Cloud-Native Agent Deployment: AWS, Azure, GCP | 26 | 1181–1206 |
| 32 | Multimodal AI & Vision-Language Models | 30 | 1207–1236 |
| 33 | Fine-Tuning, Adaptation & Model Compression | 30 | 1237–1266 |
| 34 | Responsible AI: Fairness, Bias & Explainability | 25 | 1267–1291 |
| 35 | Generative AI: Image, Video & Code Generation | 25 | 1292–1316 |
| 36 | Speech, Audio & Conversational AI | 20 | 1317–1336 |
| 37 | Edge AI, On-Device ML & Federated Learning | 20 | 1337–1356 |
| 38 | Distributed Training & Large-Scale ML Infrastructure | 20 | 1357–1376 |
| 39 | Data-Centric AI, Labeling & Synthetic Data | 20 | 1377–1396 |
| 40 | Search, Ranking & Information Retrieval | 20 | 1397–1416 |
| 41 | Causal Inference & Experimentation | 15 | 1417–1431 |
| 42 | Graph ML & Knowledge Graphs | 15 | 1432–1446 |
| 43 | Advanced Agentic Systems, Tool Use & Multi-Agent Frameworks | 25 | 1447–1471 |
| 44 | AI Hardware Acceleration, Low-Level Kernels & Compute Engineering | 25 | 1472–1496 |
| 45 | AI Security, Red Teaming, Adversarial ML & Guardrails | 25 | 1497–1521 |
| 46 | Long-Context Mechanics, State Space Models (SSMs) & KV-Cache Optimizations | 25 | 1522–1546 |
| 47 | Domain-Specific AI Architecture (Robotics, Bio, Finance & Software Agents) | 25 | 1547–1571 |
| 48 | Deep-Dive Agentic Frameworks, AI Gateway Architecture & Token Budget Engineering | 25 | 1572–1596 |
| 49 | Enterprise Cloud AI Deployment Architectures (AWS, Azure & GCP) | 25 | 1597–1621 |
| 50 | Production Incident Triage & Live Debugging | 25 | 1622–1646 |
| 51 | Multi-Turn Interviewer Drills | 15 | 1647–1661 |
| 52 | Spot the Flaw: Design & Code Critique | 20 | 1662–1681 |
| 53 | Estimation, Capacity & Cost Arithmetic | 20 | 1682–1701 |
| 54 | Executive & Stakeholder Communication | 15 | 1702–1716 |

</details>

## Honest limitations

- **Most answers have not been independently fact-checked.** One research pass verified roughly 30 answers against current sources; the rest are written from model knowledge. [`sources.md`](sources.md) documents what was checked and what changed. Verify anything you plan to state as fact.
- **Fast-moving areas go stale.** Serving frameworks, agent protocols and regulatory deadlines shift within months. Treat 2025–2026 specifics as needing a re-check.
- **Depth is uneven.** Recently written sections are substantially deeper than some older ones; this is being addressed section by section.
- **Company prep is community-reported**, not official, and interview processes change.

## Running locally

```bash
git clone https://github.com/krunlp/AI-Prep-Buddy.git
cd AI-Prep-Buddy
./scripts/serve.sh          # → http://localhost:8000   (no dependencies)
```

That serves `index.html`, `interview.html`, `simulator.html` and `roles.html` — everything interactive. For the markdown pages too:

```bash
./scripts/serve.sh jekyll   # → http://localhost:4000/AI-Prep-Buddy/
```

**A server is required** — the interview and simulator pages fetch `data/*.json`, and browsers block `fetch()` over `file://`, so opening the files directly leaves them blank. `localhost` is a secure context, so the microphone works without HTTPS.

On macOS, don't use the system Ruby at `/usr/bin/ruby` (2.6.x — too old for Jekyll and needs `sudo`). The script detects it and tells you what to do; `brew install ruby` is the fix.

## Contributing

Corrections are especially welcome — a wrong answer in an interview bank is worse than a missing one. See [CONTRIBUTING.md](CONTRIBUTING.md) for the source-of-truth workflow and the integrity checks that run in CI.

## License

[MIT](LICENSE)
