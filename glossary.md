---
layout: default
title: Glossary
---

[← Back to Home](index.html) · [Question Bank →](questions.html) · [Answers →](answers.html) · [Diagrams →](diagrams.html) · [Patterns →](patterns.html) · [Sources →](sources.html) · [Simulator →](simulator.html) · [Cheat Sheet →](cheatsheet.html) · [Glossary →](glossary.html) · [Company Prep →](company-prep.html)

# AI Prep Buddy — Glossary of Acronyms

A quick-lookup reference for the 60+ acronyms used across this bank. Alphabetical.

| Acronym | Full Term | One-Line Definition |
|---|---|---|
| A2A | Agent2Agent Protocol | Google/Linux Foundation open standard for agent-to-agent discovery, task delegation, and coordination across vendors |
| ABAC | Attribute-Based Access Control | Access control model using attributes (role, department, sensitivity) rather than fixed permission lists |
| ACP | Agent Communication Protocol | IBM Research's multi-agent protocol with formal negotiation semantics (propose/accept/reject/counter) |
| ADF | Augmented Dickey-Fuller (test) | Statistical test for stationarity in a time series |
| AI/ML acronyms continued below alphabetically | | |
| ANP | Agent Network Protocol | Community-driven protocol aimed at decentralized agent marketplaces |
| ANN | Approximate Nearest Neighbor | Fast, approximate similarity search algorithm class (e.g., HNSW, IVF) |
| RAGAS | Retrieval-Augmented Generation Assessment | Open-source framework for automated RAG evaluation metrics |
| ANOVA | Analysis of Variance | Statistical test comparing means across 3+ groups |
| API | Application Programming Interface | Contract for how software components communicate |
| AUC | Area Under the Curve | Aggregate performance metric (usually ROC or PR curve) |
| BLEU | Bilingual Evaluation Understudy | N-gram overlap metric for translation quality |
| BM25 | Best Matching 25 | Classic sparse/keyword ranking function, improves on TF-IDF |
| BPE | Byte-Pair Encoding | Subword tokenization algorithm merging frequent character pairs |
| CDC | Change Data Capture | Streaming incremental changes from a source database |
| CI/CD | Continuous Integration / Continuous Deployment | Automated build-test-deploy pipeline |
| CLIP | Contrastive Language-Image Pretraining | Joint text-image embedding model (OpenAI) |
| CoT | Chain-of-Thought | Prompting technique eliciting step-by-step reasoning |
| CRF | Conditional Random Field | Sequence-labeling model used in classic NER/POS tagging |
| CTR | Click-Through Rate | Probability a shown item is clicked |
| DPO | Direct Preference Optimization | Alignment method optimizing directly on preference pairs, no reward model |
| ELT / ETL | Extract-Load-Transform / Extract-Transform-Load | Data pipeline ordering patterns |
| EM | Expectation-Maximization | Iterative algorithm for latent-variable model fitting |
| F1 | F1 Score | Harmonic mean of precision and recall |
| FDA SaMD | Software as a Medical Device (FDA framework) | US regulatory framework for AI/ML medical software |
| FLOPs | Floating Point Operations | Unit of computational cost |
| GAN | Generative Adversarial Network | Generator vs. discriminator adversarial training architecture |
| GDPR | General Data Protection Regulation | EU data privacy law |
| GELU | Gaussian Error Linear Unit | Smooth activation function common in transformers |
| GMM | Gaussian Mixture Model | Probabilistic soft-clustering model |
| GNN | Graph Neural Network | Neural network operating over graph-structured data |
| GQA | Grouped-Query Attention | Attention variant sharing K/V across grouped heads — the modern default |
| GRPO | Group Relative Policy Optimization | RL post-training method comparing grouped samples, no critic network — dominant for reasoning models as of 2025–2026 |
| HNSW | Hierarchical Navigable Small World | Graph-based ANN indexing algorithm |
| HyDE | Hypothetical Document Embeddings | RAG technique embedding a generated hypothetical answer for retrieval |
| IoU | Intersection over Union | Overlap metric for bounding boxes/segmentation |
| IVF | Inverted File Index | Cluster-based ANN indexing algorithm |
| KL (divergence) | Kullback-Leibler Divergence | Measure of how one probability distribution diverges from another |
| KNN | K-Nearest Neighbors | Instance-based classification/regression by proximity |
| KTO | Kahneman-Tversky Optimization | Preference-alignment method using binary (not paired) feedback |
| KV cache | Key-Value Cache | Stored attention keys/values reused across autoregressive decoding steps |
| LDA | Latent Dirichlet Allocation | Probabilistic topic-modeling technique |
| LLM | Large Language Model | — |
| LLMOps | LLM Operations | MLOps practices adapted specifically for LLM-based systems |
| LoRA | Low-Rank Adaptation | Parameter-efficient fine-tuning via small trainable low-rank matrices |
| LSTM | Long Short-Term Memory | Gated RNN architecture mitigating vanishing gradients |
| MAP | Maximum a Posteriori (also: Mean Average Precision) | Context-dependent — Bayesian point estimate, or a ranking-quality metric |
| MCMC | Markov Chain Monte Carlo | Sampling method for complex posterior distributions |
| MCP | Model Context Protocol | Anthropic's open standard (Nov 2024) for agent-to-tool/data access — the "USB-C port for AI" |
| METEOR | Metric for Evaluation of Translation with Explicit ORdering | Translation-quality metric adding synonym/stem matching to BLEU |
| MHA / MQA | Multi-Head Attention / Multi-Query Attention | Attention variants — MHA gives every head its own K/V, MQA shares one K/V across all heads |
| MLA | Multi-Head Latent Attention | KV-cache-compressing attention variant (DeepSeek-style) |
| MLE | Maximum Likelihood Estimation | Parameter estimation maximizing data likelihood |
| MoE | Mixture-of-Experts | Sparse architecture activating only a subset of "expert" sub-networks per token |
| MRR | Mean Reciprocal Rank | Retrieval metric based on the rank of the first relevant result |
| NDCG | Normalized Discounted Cumulative Gain | Graded-relevance ranking-quality metric |
| NER | Named Entity Recognition | Extracting named entities (people, orgs, dates) from text |
| NIST AI RMF | NIST AI Risk Management Framework | US framework: Govern, Map, Measure, Manage |
| NMS | Non-Max Suppression | Removes duplicate overlapping bounding boxes in object detection |
| OWASP | Open Web Application Security Project | Publishes the "OWASP Top 10 for LLM Applications" risk list |
| PCA | Principal Component Analysis | Linear dimensionality-reduction technique |
| PEFT | Parameter-Efficient Fine-Tuning | Umbrella term for LoRA, prefix-tuning, prompt-tuning, etc. |
| PII | Personally Identifiable Information | Data that can identify a specific individual |
| POS | Part-of-Speech (tagging) | Classic NLP task labeling grammatical role of each token |
| PPO | Proximal Policy Optimization | On-policy RL algorithm; classic RLHF optimizer, largely superseded by GRPO for reasoning tasks |
| PR-AUC | Precision-Recall Area Under Curve | Threshold-independent metric, more informative than ROC-AUC under class imbalance |
| QAT | Quantization-Aware Training | Fine-tuning that simulates quantization effects during training |
| QLoRA | Quantized LoRA | LoRA fine-tuning on a quantized (e.g., 4-bit) frozen base model |
| RACI | Responsible, Accountable, Consulted, Informed | Organizational role-clarity framework |
| RAG | Retrieval-Augmented Generation | Grounding LLM generation in retrieved external documents |
| RAGAS | RAG Assessment (framework) | Open-source library for automated RAG evaluation metrics |
| ReAct | Reasoning + Acting | Agent prompting pattern interleaving thought, action, and observation |
| RLAIF | Reinforcement Learning from AI Feedback | Using AI-generated (not human) preference labels for alignment |
| RLHF | Reinforcement Learning from Human Feedback | Classic alignment method using a human-preference-trained reward model |
| RLVR | Reinforcement Learning with Verifiable Rewards | RL using automatically checkable rewards (math/code correctness) instead of a learned reward model |
| RMSE | Root Mean Squared Error | Regression error metric penalizing large errors more heavily |
| RoPE | Rotary Position Embedding | Positional encoding via rotation of query/key vectors |
| ROUGE | Recall-Oriented Understudy for Gisting Evaluation | N-gram/LCS overlap metric for summarization quality |
| SaaS | Software as a Service | — |
| SFT | Supervised Fine-Tuning | Fine-tuning on labeled instruction-response pairs |
| SHAP | SHapley Additive exPlanations | Game-theoretic model-explainability method |
| SLA / SLO / SLI | Service-Level Agreement / Objective / Indicator | Reliability commitment / target / measured metric |
| SMOTE | Synthetic Minority Oversampling Technique | Class-imbalance mitigation via synthetic minority-class samples |
| SOC2 | Service Organization Control 2 | Security/compliance audit standard |
| SR 11-7 | Supervisory Guidance on Model Risk Management | US Federal Reserve/OCC banking model-governance standard |
| SVM | Support Vector Machine | Max-margin classification/regression algorithm |
| TCO | Total Cost of Ownership | Full lifecycle cost, not just initial build cost |
| TF-IDF | Term Frequency-Inverse Document Frequency | Classic sparse text-relevance weighting scheme |
| TGI | Text Generation Inference | Hugging Face's LLM serving framework (deprecated as of Dec 2025) |
| ToT | Tree-of-Thought | Reasoning technique exploring/evaluating multiple branching thought paths |
| TPS | Tokens Per Second | LLM inference throughput unit |
| VAE | Variational Autoencoder | Generative autoencoder with a probabilistic latent space |
| VIF | Variance Inflation Factor | Multicollinearity-detection metric |
| ViT | Vision Transformer | Transformer architecture applied to image patches |
| WAPE | Weighted Absolute Percentage Error | Volume-weighted forecast-accuracy metric |
| YaRN | Yet another RoPE extensioN method | Technique extending RoPE-based models to longer context lengths |
| ASR | Automatic Speech Recognition | Converting spoken audio to text (e.g., Whisper, Conformer) |
| ATE | Average Treatment Effect | Expected difference in outcomes between treatment and control groups |
| AWQ | Activation-aware Weight Quantization | Quantization method preserving salient weights identified by activation patterns |
| C2PA | Coalition for Content Provenance and Authenticity | Standard for cryptographic content provenance/watermarking |
| CFG | Classifier-Free Guidance | Diffusion-model technique steering generation toward the text prompt without a separate classifier |
| ColBERT | Contextualized Late Interaction over BERT | Late-interaction re-ranking model computing token-level similarity efficiently |
| CTC | Connectionist Temporal Classification | Loss function for sequence-to-sequence without explicit alignment (used in ASR) |
| DDPM | Denoising Diffusion Probabilistic Model | Core architecture behind modern image/video generation models |
| DiD | Difference-in-Differences | Causal inference method comparing pre/post changes across treatment and control groups |
| DiT | Diffusion Transformer | Transformer-based architecture for diffusion models (replaces U-Net) |
| DoRA | Weight-Decomposed Low-Rank Adaptation | LoRA variant decomposing weights into magnitude and direction components |
| DVC | Data Version Control | Git-like versioning for ML datasets and pipelines |
| FID | Fréchet Inception Distance | Image generation quality metric comparing feature distributions |
| FSDP | Fully Sharded Data Parallel | PyTorch's distributed training strategy sharding parameters, gradients, and optimizer states |
| GAT | Graph Attention Network | GNN variant using attention-weighted neighbor aggregation |
| GCN | Graph Convolutional Network | Foundational GNN architecture using spectral/spatial convolutions on graphs |
| GGUF | GPT-Generated Unified Format | Quantized model file format for efficient CPU/edge inference (llama.cpp ecosystem) |
| GPTQ | GPT Quantization | Post-training quantization method using approximate second-order information |
| HTE | Heterogeneous Treatment Effect | Treatment effect that varies across subpopulations |
| IPW | Inverse Probability Weighting | Causal inference technique reweighting samples by propensity score |
| MOS | Mean Opinion Score | Subjective quality metric for speech synthesis (1-5 human rating scale) |
| NAS | Neural Architecture Search | Automated search for optimal model architectures |
| NPU | Neural Processing Unit | Dedicated on-device hardware accelerator for ML inference (Apple Neural Engine, Snapdragon NPU) |
| RRF | Reciprocal Rank Fusion | Simple score-based method for combining multiple ranked lists |
| SUTVA | Stable Unit Treatment Value Assumption | A/B testing assumption that one unit's treatment doesn't affect another's outcome |
| TEE | Trusted Execution Environment | Secure hardware enclave for privacy-preserving computation (H100, SEV-SNP) |
| TTS | Text-to-Speech | Converting text to spoken audio (neural TTS: VALL-E, XTTS) |
| VLA | Vision-Language-Action (model) | Multimodal model mapping visual and language inputs to robotic actions (RT-2, OpenVLA) |
| WER | Word Error Rate | Primary ASR accuracy metric (insertions + deletions + substitutions / total words) |
| AST | Abstract Syntax Tree | Tree representation of source code structure used by coding agents |
| DP-SGD | Differentially Private SGD | Stochastic gradient descent with clip-and-noise privacy guarantees |
| GCG | Greedy Coordinate Gradient | Adversarial prompt optimization attack technique |
| HBM | High Bandwidth Memory | Stacked 3D DRAM memory used on modern GPUs (H100/H200 HBM3e) |
| MCTS | Monte Carlo Tree Search | Heuristic search algorithm used for decision processes and long-horizon agent planning |
| NVLink | NVIDIA Interconnect | High-speed point-to-point interconnect between GPUs (up to 900 GB/s on NVLink-4) |
| PaI | Prompt Injection | Security vulnerability where untrusted input overrides system instructions |
| ReAct | Reasoning + Acting | Interleaved paradigm for LLM agent reasoning and execution |
| SIMT | Single Instruction, Multiple Threads | CUDA execution architecture where threads execute instructions in warps |
| SSM | State Space Model | Sub-quadratic sequence modeling architecture (Mamba, S4, RWKV) |
| ToT | Tree-of-Thought | Agent planning framework maintaining multiple reasoning branches |
| ACA | Azure Container Apps | Serverless container platform supporting GPU workloads |
| CMI | Custom Model Import | AWS Bedrock feature for importing fine-tuned custom weights |
| CUD | Committed Use Discount | GCP pricing model providing volume discounts for reserved compute |
| DLC | Deep Learning Container | Pre-configured Docker images optimized by AWS/GCP for ML serving |
| GKE | Google Kubernetes Engine | Google Cloud managed Kubernetes platform with TPU/GPU auto-provisioning |
| KEDA | Kubernetes Event-driven Autoscaling | Autoscaler scaling pod count based on external metrics (queue depth, token latency) |
| PSC | Private Service Connect | GCP private data plane networking for securely reaching Google AI APIs |
| PTU | Provisioned Throughput Unit | Reserved latency and throughput capacity model in Azure OpenAI Service |

---

*Cross-reference: most of these terms are explained in fuller context in `answers.md` (search the term) or diagrammed directly in `patterns.md` Section A (Transformer & LLM Internals Patterns).*



