# Contributing to AI Prep Buddy

Thanks for your interest in contributing! This project aims to be the most comprehensive, current AI/ML interview preparation resource available.

## How to Contribute

### 🐛 Report Issues
- Found an outdated answer or incorrect information? [Open an issue](https://github.com/krunlp/AI-Prep-Buddy/issues/new).
- Include the question number (e.g., Q342) and what needs correction.

### 📝 Content Contributions

**Questions & Answers**
- New questions should fit one of the existing 31 sections.
- Answers should follow the existing framework style: concise, structured, with tradeoffs called out.
- Cite real-world sources where possible (see `sources.md` for the style).

**Code Solutions**
- Solutions in `code-solutions.md` should be self-contained, runnable Python.
- Use only standard library + numpy + torch (no obscure dependencies).
- Include docstrings, edge-case handling, and complexity analysis.

**Diagrams & Patterns**
- Diagrams use Mermaid syntax (see `diagrams.md` for examples).
- New patterns should follow the ID scheme in `patterns.md` (e.g., A1, B2, H4).

### 🔧 Technical Contributions
- Fix typos, broken links, or formatting issues.
- Improve the simulator (`simulator.html`).
- Improve GitHub Pages styling or navigation.

## Submission Process

1. Fork the repository.
2. Create a feature branch (`git checkout -b add-question-1207`).
3. Make your changes.
4. Commit with a clear message (`git commit -m "Add Q1207: multi-modal RAG evaluation"`).
5. Open a Pull Request with a description of what you changed and why.

## Style Guidelines

- **Answers**: Framework-first, not wall-of-text. Lead with the key insight, then elaborate.
- **Tone**: Direct and practical. Write for someone prepping the night before, not a textbook.
- **Currency**: Always note the date if citing time-sensitive information (model releases, framework versions, regulatory deadlines).
- **Difficulty tags**: Use ⭐ (foundational), ⭐⭐ (intermediate), ⭐⭐⭐ (advanced) on new questions.

## Code of Conduct

Be respectful, constructive, and focused on making this resource better for everyone preparing for AI/ML interviews.

## Questions?

Open a [Discussion](https://github.com/krunlp/AI-Prep-Buddy/discussions) or reach out via Issues.
