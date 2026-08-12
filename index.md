---
layout: default
title: Home — Master AI/ML Interview Question Bank
description: "1600+ AI/ML interview questions with answer frameworks, architecture diagrams, code solutions, and study paths. Principal-level prep for 2026."
image: https://repository-images.githubusercontent.com/AI-Prep-Buddy/social-preview.png
---

<style>
  .hero-section {
    text-align: center;
    padding: 3rem 1rem 2rem;
    background: radial-gradient(circle at top, rgba(99, 102, 241, 0.15) 0%, rgba(15, 23, 42, 0) 70%);
    border-radius: var(--radius-lg);
    margin-bottom: 2.5rem;
    border: 1px solid var(--border-color);
  }

  .hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 1rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
    color: var(--text-secondary);
    max-width: 800px;
    margin: 0 auto 2rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.25rem;
    margin-bottom: 3rem;
  }

  .stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease;
  }

  .stat-card:hover {
    transform: translateY(-3px);
    border-color: var(--accent-primary);
  }

  .stat-number {
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
  }

  .stat-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
  }

  .feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
  }

  .feature-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent-primary);
    box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.25);
    text-decoration: none;
  }

  .feature-icon {
    width: 46px;
    height: 46px;
    border-radius: var(--radius-md);
    background: rgba(99, 102, 241, 0.1);
    color: var(--accent-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 1.25rem;
  }

  .feature-card h3 {
    font-size: 1.35rem;
    margin-top: 0;
    margin-bottom: 0.6rem;
  }

  .feature-card p {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-bottom: 0;
    line-height: 1.55;
  }

  .cta-bar {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
    margin-top: 2rem;
  }
</style>

<div class="hero-section">
  <h1 class="hero-title">AI Prep Buddy</h1>
  <p class="hero-subtitle">
    The ultimate principal-level interview preparation bank for AI/ML System Design, LLMs, Agents, Hardware Acceleration, and Cloud AI Architecture.
  </p>
</div>

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number" style="color: #6366f1;">1,613</div>
    <div class="stat-label">Questions</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" style="color: #10b981;">49</div>
    <div class="stat-label">Sections</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" style="color: #f59e0b;">39</div>
    <div class="stat-label">Architecture Diagrams</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" style="color: #ec4899;">10</div>
    <div class="stat-label">Company Guides</div>
  </div>
</div>

<h2 style="margin-bottom: 1.5rem;"><i class="fa-solid fa-compass" style="color: var(--accent-primary);"></i> Explore the Knowledge Base</h2>

<div class="card-grid">

  <a href="questions.html" class="feature-card">
    <div class="feature-icon"><i class="fa-solid fa-list-check"></i></div>
    <h3>Master Question Bank</h3>
    <p>All 1,613 questions across 49 sections — strategy, ML/DL, LLMs, RAG, agents, MLOps, safety, hardware kernels, AI security, long-context, and cloud deployments.</p>
  </a>

  <a href="answers.html" class="feature-card">
    <div class="feature-icon" style="background: rgba(16, 185, 129, 0.1); color: #10b981;"><i class="fa-solid fa-lightbulb"></i></div>
    <h3>Answer Frameworks</h3>
    <p>A rigorous, strong-answer framework for every single question — what a Principal or Staff candidate should hit under pressure, not generic filler.</p>
  </a>

  <a href="simulator.html" class="feature-card">
    <div class="feature-icon" style="background: rgba(236, 72, 153, 0.1); color: #ec4899;"><i class="fa-solid fa-microphone"></i></div>
    <h3>🎤 Interactive Simulator</h3>
    <p>High-tech mock interview practice studio — random draws, timer, self-grading, and weak-spot tracking across all 1,613 questions.</p>
  </a>

  <a href="company-prep.html" class="feature-card">
    <div class="feature-icon" style="background: rgba(245, 158, 11, 0.1); color: #f59e0b;"><i class="fa-solid fa-building-columns"></i></div>
    <h3>🏢 Company-Specific Guides</h3>
    <p>Candidate-reported interview loops for Meta, NVIDIA, Microsoft, Apple, Tesla/Waymo, Mistral AI, Cohere, OpenAI, Anthropic, and Google DeepMind.</p>
  </a>

  <a href="diagrams.html" class="feature-card">
    <div class="feature-icon"><i class="fa-solid fa-diagram-project"></i></div>
    <h3>System Architecture Diagrams</h3>
    <p>39 rendered architecture diagrams (RAG, agents, LLM gateways, feature stores, MLOps CI/CD) with flow walkthroughs and real-world trade-offs.</p>
  </a>

  <a href="patterns.html" class="feature-card">
    <div class="feature-icon"><i class="fa-solid fa-cubes"></i></div>
    <h3>Design Patterns Catalog</h3>
    <p>19 conceptual pattern diagrams spanning transformer internals, RLHF alignment, agent architectures, and guardrails.</p>
  </a>

  <a href="code-solutions.html" class="feature-card">
    <div class="feature-icon"><i class="fa-solid fa-code"></i></div>
    <h3>Python Code Solutions</h3>
    <p>Production-grade Python code for core ML coding interview algorithms (k-means, attention, BPE tokenizer, beam search, reservoir sampling).</p>
  </a>

  <a href="study-paths.html" class="feature-card">
    <div class="feature-icon"><i class="fa-solid fa-map-location-dot"></i></div>
    <h3>2-Week Study Paths</h3>
    <p>Curated 14-day study schedules for Staff MLEs, Principal AI Architects, and Frontier ML Researchers with daily hand-picked question quotas.</p>
  </a>

  <a href="cheatsheet.html" class="feature-card">
    <div class="feature-icon"><i class="fa-solid fa-bolt"></i></div>
    <h3>Day-of-Interview Cheat Sheet</h3>
    <p>Condensed 20-minute quick-reference summary covering key one-liners for all 49 sections.</p>
  </a>

</div>

<div class="cta-bar">
  <h2>Ready to Start Practicing?</h2>
  <p>Jump directly into the Mock Simulator or follow a 2-week structured study path.</p>
  <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1.25rem; flex-wrap: wrap;">
    <a href="simulator.html" style="background: var(--accent-gradient); color: white; padding: 0.75rem 1.5rem; border-radius: var(--radius-md); font-weight: 600; text-decoration: none;">Launch Simulator</a>
    <a href="study-paths.html" style="background: var(--bg-card-hover); color: var(--text-primary); padding: 0.75rem 1.5rem; border-radius: var(--radius-md); font-weight: 600; text-decoration: none; border: 1px solid var(--border-color);">View Study Paths</a>
  </div>
</div>
