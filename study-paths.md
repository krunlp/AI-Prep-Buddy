---
layout: default
title: Study Paths
---

# AI Interview Study Paths

Welcome to the curated study paths! With over 1,716 questions in the bank, it's impossible to review everything in a short timeframe. We have created three distinct 2-week study plans tailored to specific roles. 

## How to use this plan
1. **Identify your target role:** Choose the path that closest matches your upcoming interview.
2. **Stick to the daily quota:** Each day provides 15-20 hand-picked, high-signal questions, requiring about 2-3 hours on weekdays and 4-5 hours on weekends. 
3. **Mix breadth and depth:** Some days focus on wide knowledge, while weekend mock interviews demand deep, structured answers.
4. **Use diagrams & patterns:** Visualizing answers is crucial for system design rounds. We've indicated which diagrams and patterns to study on specific days.

## Adapting the plan
- **Shorter Timeline?** See the "Emergency 3-Day Condensed Version" at the bottom of each path.
- **Longer Timeline?** Use the remaining questions in the sections as extra practice, or do full mock interviews every 3 days.

---

## Path 1: Staff Machine Learning Engineer (2 weeks)
**Focus Areas:** Classic ML Fundamentals (Sec 3-7), System Design, Serving, MLOps (Sec 14-16), Time Series, RecSys, Coding (Sec 24-26).

#### Day 1: Deep Dive into ML Fundamentals
**Questions**: Q66–Q75, Q84, Q89, Q91, Q101, Q114 (15 questions)
**Diagrams**: Diagram 1 (Bias-Variance Tradeoff), Diagram 4 (ROC Curve)
**Patterns**: Pattern ML-1 (Ensemble Methods)
**Time**: ~2.5 hours
**Focus tip**: Make sure you can explain the bias-variance tradeoff and regularization as if explaining it to a junior engineer.

#### Day 2: Statistics, Probability, & A/B Testing
**Questions**: Q122–Q128, Q136–Q141, Q163–Q164 (15 questions)
**Diagrams**: Diagram 7 (A/B Testing Architecture)
**Patterns**: Pattern STAT-2 (Bayesian A/B Testing)
**Time**: ~2 hours
**Focus tip**: Focus heavily on A/B testing pitfalls (Simpson's paradox, peeking, network effects) as these are highly tested for Staff roles.

#### Day 3: Deep Learning Core & Optimization
**Questions**: Q171–Q182, Q202, Q212, Q214, Q225 (16 questions)
**Diagrams**: Diagram 12 (Backpropagation Flow)
**Patterns**: Pattern DL-3 (Gradient Management)
**Time**: ~2.5 hours
**Focus tip**: Connect architectural choices (like residual connections or normalization) directly to solving optimization problems (vanishing gradients).

#### Day 4: Vision & NLP (Pre-LLM) Fundamentals
**Questions**: Q226–Q231, Q239, Q240, Q256–Q260, Q271, Q277 (15 questions)
**Diagrams**: Diagram 18 (Transformer Encoder vs Decoder)
**Patterns**: Pattern NLP-1 (Embeddings Evolution)
**Time**: ~2 hours
**Focus tip**: Understand the transition from CNNs to ViTs and Word2Vec to Contextual Embeddings.

#### Day 5: Classic ML System Design - Part 1
**Questions**: Q556–Q565, Q570, Q572, Q575, Q580, Q582 (15 questions)
**Diagrams**: Diagram 22 (Standard ML System Architecture)
**Patterns**: Pattern SYS-1 (Batch vs Real-time Prediction)
**Time**: ~3 hours
**Focus tip**: Always start with clarifying requirements and scale before jumping into model selection.

#### Day 6: Classic ML System Design - Part 2
**Questions**: Q585–Q595, Q598, Q599, Q600 (15 questions)
**Diagrams**: Diagram 24 (Data Leakage Prevention)
**Patterns**: Pattern SYS-3 (Cold Start Handling)
**Time**: ~3 hours
**Focus tip**: Be prepared to discuss failure modes: what happens when the model goes stale or input distributions shift?

#### Day 7: Mock Interview & Weekly Review
**Questions**: Q70, Q110, Q208, Q560, Q590 (5 deep-dive questions)
**Diagrams**: Review all week 1 diagrams
**Patterns**: Review all week 1 patterns
**Time**: ~4 hours (simulate a real interview environment)
**Focus tip**: Record yourself answering a system design prompt end-to-end in 45 minutes on a whiteboard or virtual pad.

#### Day 8: Model Serving & Inference Optimization
**Questions**: Q601–Q610, Q615, Q620, Q625, Q630, Q640 (15 questions)
**Diagrams**: Diagram 28 (Model Serving Architectures)
**Patterns**: Pattern INF-2 (Quantization & Pruning)
**Time**: ~2.5 hours
**Focus tip**: Contrast Triton, TF Serving, and ONNX Runtime; know when to use GPU vs CPU for inference.

#### Day 9: MLOps, CI/CD, and Monitoring
**Questions**: Q646–Q655, Q660, Q670, Q680, Q690, Q700 (15 questions)
**Diagrams**: Diagram 32 (MLOps Lifecycle)
**Patterns**: Pattern OPS-4 (Shadow Deployment & Canary)
**Time**: ~2.5 hours
**Focus tip**: Differentiate between data drift, concept drift, and model decay, with specific metrics to monitor each.

#### Day 10: Time Series & Forecasting
**Questions**: Q941–Q955 (15 questions)
**Diagrams**: Diagram 40 (Time Series Cross-Validation)
**Patterns**: Pattern TS-1 (Stationarity & Differencing)
**Time**: ~2 hours
**Focus tip**: Focus on how time-series cross-validation differs from standard k-fold, and how to handle seasonality.

#### Day 11: Recommender Systems Deep Dive
**Questions**: Q961–Q975 (15 questions)
**Diagrams**: Diagram 42 (Two-Tower Recommendation System)
**Patterns**: Pattern REC-2 (Candidate Generation vs Ranking)
**Time**: ~3 hours
**Focus tip**: The two-stage funnel (retrieval/candidate generation -> ranking) is the holy grail of RecSys interviews.

#### Day 12: Coding & Algorithms for ML
**Questions**: Q981–Q995 (15 questions)
**Diagrams**: N/A
**Patterns**: Pattern CODE-1 (Vectorized Operations)
**Time**: ~3 hours
**Focus tip**: Write out the code for standard ML algorithms (K-means, KNN, decision tree splits) from scratch in NumPy.

#### Day 13: Edge Cases & Staff-Level Nuances
**Questions**: Q130–Q135, Q251, Q502, Q612, Q622, Q635, Q958, Q978, Q998, Q1002 (15 questions)
**Diagrams**: Diagram 45 (System Trade-offs)
**Patterns**: Pattern ARCH-5 (Handling Data Sparsity)
**Time**: ~2 hours
**Focus tip**: Staff engineers are evaluated on identifying edge cases and operational reality, not just the happy path.

#### Day 14: Final Mock Interview & Synthesis
**Questions**: Q557, Q605, Q650, Q965 (4 complex system design prompts)
**Diagrams**: Whiteboard your own architectures
**Patterns**: Synthesize your own cheat sheet
**Time**: ~5 hours
**Focus tip**: Treat this as a full 4-hour loop. Don't look at answers until you've fully drawn out your designs and justified trade-offs.

**Emergency 3-Day Condensed Version:**
- **Day 1:** Q66-Q80, Q122-Q128 (ML/Stats core).
- **Day 2:** Q556-Q570, Q601-Q610 (System Design & Serving).
- **Day 3:** Q646-Q655, Q961-Q970 (MLOps & RecSys).

---

## Path 2: Principal AI/ML Lead (2 weeks)
**Focus Areas:** Strategy, Behavioral, GenAI/LLM Depth, Agents, Safety, Enterprise Architecture (Sections 1-2, 8-13, 21-23, 27-31).

#### Day 1: Strategy, Vision & Build vs. Buy
**Questions**: Q1–Q15 (15 questions)
**Diagrams**: Diagram 50 (AI Platform ROI Matrix)
**Patterns**: Pattern LDR-1 (Sequencing AI Capabilities)
**Time**: ~2.5 hours
**Focus tip**: Frame your answers in terms of business outcomes, ROI, and technical debt.

#### Day 2: Technical Leadership & Behavioral
**Questions**: Q16–Q25, Q26–Q35 (20 questions)
**Diagrams**: N/A
**Patterns**: Pattern LDR-3 (Managing Up & Cross-Functional)
**Time**: ~2 hours
**Focus tip**: Use the STAR method, but over-index on the "Trade-offs" and "Lessons Learned" for your past projects.

#### Day 3: LLM & Transformer Architecture Mastery
**Questions**: Q286–Q305 (20 questions)
**Diagrams**: Diagram 55 (Multi-Query vs Grouped-Query Attention)
**Patterns**: Pattern LLM-2 (KV Cache Optimization)
**Time**: ~3 hours
**Focus tip**: Understand exactly where the memory bottlenecks are in training vs. inference.

#### Day 4: Fine-Tuning, RLHF, and PEFT
**Questions**: Q306–Q321, Q335–Q338 (20 questions)
**Diagrams**: Diagram 58 (RLHF vs DPO Pipeline)
**Patterns**: Pattern LLM-4 (LoRA and Quantization)
**Time**: ~2.5 hours
**Focus tip**: Be ready to justify when to use prompt engineering vs RAG vs fine-tuning.

#### Day 5: Advanced Prompting & Structured Outputs
**Questions**: Q346–Q365 (20 questions)
**Diagrams**: Diagram 60 (Function Calling Flow)
**Patterns**: Pattern PRMP-3 (Grammar Constrained Decoding)
**Time**: ~2 hours
**Focus tip**: Detail how you enforce deterministic, parseable outputs from stochastic models in production.

#### Day 6: RAG Pipelines & Vector Databases
**Questions**: Q376–Q390, Q421–Q425 (20 questions)
**Diagrams**: Diagram 65 (Advanced RAG Architecture)
**Patterns**: Pattern RAG-2 (Retrieve-then-Rerank)
**Time**: ~3 hours
**Focus tip**: The naive RAG pipeline is trivial; focus on chunking strategies, hybrid search, and resolving conflicting context.

#### Day 7: Mock Interview - GenAI System Design
**Questions**: Q496, Q498, Q503 (3 extensive design prompts)
**Diagrams**: Draw full end-to-end GenAI architectures
**Patterns**: Pattern ARCH-8 (Multi-Model Routing)
**Time**: ~4 hours
**Focus tip**: Practice narrating your design choices out loud, anticipating scaling bottlenecks.

#### Day 8: Agentic AI & Multi-Agent Systems
**Questions**: Q451–Q470 (20 questions)
**Diagrams**: Diagram 70 (ReAct Agent Loop vs Plan-and-Execute)
**Patterns**: Pattern AGT-1 (Agent State Management)
**Time**: ~3 hours
**Focus tip**: Focus on memory management and preventing infinite loops in autonomous agents.

#### Day 9: LLM System Design Deep Dive
**Questions**: Q504–Q523 (20 questions)
**Diagrams**: Diagram 75 (LLM Gateway Architecture)
**Patterns**: Pattern SYS-6 (Streaming & Backpressure)
**Time**: ~3 hours
**Focus tip**: Connect agentic concepts from yesterday into scalable microservice architectures today.

#### Day 10: LLM Evaluation, Safety & Governance
**Questions**: Q831–Q840, Q866–Q875 (20 questions)
**Diagrams**: Diagram 80 (LLM Evaluation Harness)
**Patterns**: Pattern EVAL-1 (LLM-as-a-Judge)
**Time**: ~2 hours
**Focus tip**: Differentiate between offline evaluation, online metrics, and guardrail enforcement.

#### Day 11: Enterprise Architecture & A2A/MCP
**Questions**: Q1091–Q1100, Q1141–Q1150 (20 questions)
**Diagrams**: Diagram 85 (Model Context Protocol Integration)
**Patterns**: Pattern ENT-2 (Multi-Tenant AI Platforms)
**Time**: ~2.5 hours
**Focus tip**: Understand how agents communicate securely across enterprise trust boundaries (Agent-to-Agent).

#### Day 12: Open-Ended Architecture Probes
**Questions**: Q1006–Q1025 (20 questions)
**Diagrams**: N/A
**Patterns**: Pattern ARCH-10 (Design Pattern Synthesis)
**Time**: ~3 hours
**Focus tip**: These are intentionally vague. Practice your framework for narrowing down the scope before answering.

#### Day 13: Rapid-Fire Depth & Cloud-Native Deployment
**Questions**: Q1036–Q1045, Q1181–Q1190 (20 questions)
**Diagrams**: Diagram 90 (Cloud-Native GenAI Stack)
**Patterns**: Pattern CLD-3 (Serverless Inference)
**Time**: ~2 hours
**Focus tip**: Demonstrate deep knowledge of specific cloud offerings (Bedrock, Vertex, Azure OpenAI) vs OSS deployments.

#### Day 14: Final Mock Interview (Leadership + Architecture)
**Questions**: Q33, Q57, Q517, Q1145 (Behavioral + System Design)
**Diagrams**: Synthesize your architectural viewpoints
**Patterns**: Review strategy matrices
**Time**: ~5 hours
**Focus tip**: As a Principal Lead, your answers must balance technical rigor with organizational influence and cost-awareness.

**Emergency 3-Day Condensed Version:**
- **Day 1:** Q1-Q10, Q286-Q300 (Strategy & LLM Architecture).
- **Day 2:** Q376-Q385, Q451-Q460, Q496-Q500 (RAG, Agents, LLM Sys Design).
- **Day 3:** Q831-Q840, Q1091-Q1100 (Evaluation & Enterprise Architecture).

---

## Path 3: AI Platform / Infrastructure Engineer (2 weeks)
**Focus Areas:** System Design, Serving, MLOps, Data Engineering, Cloud, DevOps (Sections 14-20, 26, 31).

#### Day 1: ML System Architecture & Serving Basics
**Questions**: Q556–Q565, Q601–Q605 (15 questions)
**Diagrams**: Diagram 22 (ML System Architecture)
**Patterns**: Pattern SYS-1 (Batch vs Real-time)
**Time**: ~2.5 hours
**Focus tip**: Master the transition from a Jupyter notebook to a scalable inference endpoint.

#### Day 2: Inference Optimization Deep Dive
**Questions**: Q606–Q620 (15 questions)
**Diagrams**: Diagram 29 (TensorRT & ONNX Pipelines)
**Patterns**: Pattern INF-3 (Continuous Batching)
**Time**: ~3 hours
**Focus tip**: Understand hardware bottlenecks (memory bandwidth vs compute) and optimization techniques like FlashAttention.

#### Day 3: MLOps Core & Model Registry
**Questions**: Q646–Q660 (15 questions)
**Diagrams**: Diagram 32 (MLOps Lifecycle)
**Patterns**: Pattern OPS-1 (Model Versioning)
**Time**: ~2 hours
**Focus tip**: Clearly articulate how you link a deployed model back to its exact training data and code commit.

#### Day 4: CI/CD for ML & Shadow Deployments
**Questions**: Q661–Q675 (15 questions)
**Diagrams**: Diagram 34 (CI/CD Pipeline for Models)
**Patterns**: Pattern OPS-4 (Shadow Deployment)
**Time**: ~2.5 hours
**Focus tip**: Differentiate between software CI/CD and ML CI/CD (which includes data and model validation).

#### Day 5: Feature Stores & Feature Engineering
**Questions**: Q701–Q715 (15 questions)
**Diagrams**: Diagram 36 (Feature Store Architecture)
**Patterns**: Pattern FEAT-2 (Online vs Offline Stores)
**Time**: ~2.5 hours
**Focus tip**: Explain how a feature store prevents point-in-time leakage and standardizes features across training/serving.

#### Day 6: Data Engineering for AI (Pipelines & Streaming)
**Questions**: Q726–Q740 (15 questions)
**Diagrams**: Diagram 38 (Kafka + Spark Streaming)
**Patterns**: Pattern DATA-3 (Lambda Architecture)
**Time**: ~3 hours
**Focus tip**: Be ready to design robust streaming pipelines for real-time feature computation.

#### Day 7: Mock Interview - Infrastructure Design
**Questions**: Q590, Q625, Q685 (3 massive infra questions)
**Diagrams**: End-to-end data+ML architecture
**Patterns**: Synthesize pipeline patterns
**Time**: ~4 hours
**Focus tip**: Build a complete architecture on a whiteboard, focusing on throughput, latency, and fault tolerance.

#### Day 8: Data Engineering at Scale (Storage & Compute)
**Questions**: Q741–Q755 (15 questions)
**Diagrams**: Diagram 39 (Data Lakehouse vs Warehouse)
**Patterns**: Pattern DATA-4 (Parquet/Iceberg Optimization)
**Time**: ~2.5 hours
**Focus tip**: Contrast Delta Lake, Iceberg, and Hudi. Understand columnar storage formats deeply.

#### Day 9: Cloud ML Platforms (AWS, GCP, Azure)
**Questions**: Q766–Q780 (15 questions)
**Diagrams**: Diagram 41 (Sagemaker vs Vertex AI)
**Patterns**: Pattern CLD-1 (Managed vs Self-Hosted)
**Time**: ~2.5 hours
**Focus tip**: Compare the managed offerings of major cloud providers against deploying Kubernetes (EKS/GKE) yourself.

#### Day 10: DevOps, Kubernetes, and GPU Orchestration
**Questions**: Q796–Q810 (15 questions)
**Diagrams**: Diagram 43 (Kubeflow / K8s Architecture)
**Patterns**: Pattern DEV-2 (GPU Time-Slicing)
**Time**: ~3 hours
**Focus tip**: Understand how to schedule, scale, and monitor GPU workloads efficiently in a Kubernetes cluster.

#### Day 11: Monitoring, Logging, and Alerting
**Questions**: Q676–Q685, Q811–Q815 (15 questions)
**Diagrams**: Diagram 44 (Observability Stack)
**Patterns**: Pattern OPS-5 (Drift Detection)
**Time**: ~2 hours
**Focus tip**: Focus on Prometheus/Grafana stacks and setting actionable alert thresholds for model drift.

#### Day 12: Coding & Algorithms for Infrastructure
**Questions**: Q981–Q995 (15 questions)
**Diagrams**: N/A
**Patterns**: Pattern CODE-2 (Concurrency & Async)
**Time**: ~3 hours
**Focus tip**: Write performant code focusing on multithreading, async I/O, and efficient memory usage.

#### Day 13: Cloud-Native Agent & LLM Deployment
**Questions**: Q1181–Q1195 (15 questions)
**Diagrams**: Diagram 90 (Cloud-Native GenAI Stack)
**Patterns**: Pattern CLD-4 (Multi-Region LLM Routing)
**Time**: ~2.5 hours
**Focus tip**: Apply your infrastructure knowledge to the specific constraints of large language models (vLLM, TGI).

#### Day 14: Final Infra Mock Interview
**Questions**: Q750, Q795, Q825, Q1199 (4 infra design prompts)
**Diagrams**: Whiteboard full platform designs
**Patterns**: Review all scaling patterns
**Time**: ~4 hours
**Focus tip**: Design a platform that serves hundreds of models and processes terabytes of data daily, while maintaining strict SLAs.

**Emergency 3-Day Condensed Version:**
- **Day 1:** Q601-Q615, Q701-Q705 (Serving & Feature Stores).
- **Day 2:** Q646-Q660, Q726-Q735 (MLOps & Data Engineering).
- **Day 3:** Q796-Q810, Q1181-Q1185 (Kubernetes, GPUs & LLM Infra).
