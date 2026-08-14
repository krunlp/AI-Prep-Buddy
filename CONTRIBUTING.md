# Contributing to AI Prep Buddy

Thanks for your interest in contributing! This project aims to be the most comprehensive, current AI/ML interview preparation resource available.

## How to Contribute

### 🐛 Report Issues
- Found an outdated answer or incorrect information? [Open an issue](https://github.com/krunlp/AI-Prep-Buddy/issues/new).
- Include the question number (e.g., Q342) and what needs correction.

### 📝 Content Contributions

**Questions & Answers**
- New questions should fit one of the existing 49 sections (or propose a new one in an issue first).
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

## ⚠️ Source of Truth — read before editing content

Only two files are hand-edited:

| File | Role |
|---|---|
| `questions.md` | **Source of truth** for question text and numbering |
| `answers.md` | **Source of truth** for answer text |

Role definitions live in `scripts/roles_data.py` (sections referenced by number,
so they survive renumbering).

Everything else is **generated**. Do not hand-edit these — your changes will be
overwritten:

- `roles.html`
- `data/questions.json`
- the `QA_DATA` block inside `simulator.html`
- question counts in `README.md` and `index.html`

### Workflow

```bash
# 1. edit questions.md and/or answers.md
# 2. regenerate every derived artifact
python3 scripts/sync_derived.py

# 3. check structural integrity
python3 scripts/verify_integrity.py

# 4. stage the regenerated files along with your edits
git add questions.md answers.md data/questions.json simulator.html README.md index.html
```

Install the pre-commit hook once and steps 2–3 are enforced automatically:

```bash
ln -sf ../../scripts/pre-commit .git/hooks/pre-commit
```

### What CI enforces

`scripts/verify_integrity.py` runs on every push and PR. It fails the build on:

- **duplicate question numbers** — two questions sharing one number
- **numbering gaps** — a number missing from the sequence
- **unanswered questions** — a question with no matching answer
- **orphan answers** — an answer with no matching question
- **section range overlaps** — one section's numbers colliding with another's
- **header/content mismatch** — a section header claiming a range it doesn't contain
- **stale derived artifacts** — generated files out of sync with the source

Every one of these checks exists because that bug actually shipped to `main`.
Please fix the data rather than weakening a check.

### Numbering rules

- Question numbers are globally sequential across the whole bank, **not**
  per-section. A new section starts at `previous_section_max + 1`.
- Section headers must declare their true range, e.g.
  `## Section 44 — AI Hardware … (1472–1496)`.
- Never renumber existing questions casually — answers, the simulator, and
  external links all key off these numbers.

### Answer formats

Two formats are supported, and `scripts/qa_lib.py` parses both:

```markdown
**123. Short title.** Answer body…

### Question 123: Longer Title
Multi-section deep-dive body…
```

Use the `**N.**` form for standard answers and the `### Question N:` form for
long-form answers with sub-headings or diagrams. If you write a script that
touches answer numbering, **import `qa_lib` rather than writing your own
regex** — a script that knew only one of the two formats is exactly what caused
the Section 43 numbering collision.

## Running locally

A local HTTP server is required: `interview.html` and `simulator.html` fetch
`data/*.json`, and browsers block `fetch()` over `file://`, so opening the files
directly will leave those pages blank.

```bash
# Full Jekyll build — mirrors GitHub Pages, renders the markdown pages too
./scripts/serve.sh
#   -> http://localhost:4000/AI-Prep-Buddy/

# No Ruby? Static mode covers the hand-written HTML pages
./scripts/serve.sh static
#   -> http://localhost:8000
```

On macOS, if you don't have bundler:

```bash
gem install bundler
./scripts/serve.sh
```

Static mode serves `index.html`, `interview.html`, `simulator.html` and
`roles.html` correctly. Markdown pages (`questions`, `answers`, `diagrams`,
`patterns`, ...) only render under full Jekyll.

**Worth testing in a real browser**, because the automated checks cannot reach it:
voice input and output, microphone permissions, the answer-reveal panel position
near screen edges, and layout on a narrow viewport.

## Submission Process

1. Fork the repository.
2. Create a feature branch (`git checkout -b add-question-1622`).
3. Make your changes to `questions.md` / `answers.md`.
4. Run `python3 scripts/sync_derived.py && python3 scripts/verify_integrity.py`.
5. Commit with a clear message (`git commit -m "Add Q1622: multi-modal RAG evaluation"`).
6. Open a Pull Request with a description of what you changed and why.

## Style Guidelines

- **Answers**: Framework-first, not wall-of-text. Lead with the key insight, then elaborate.
- **Tone**: Direct and practical. Write for someone prepping the night before, not a textbook.
- **Currency**: Always note the date if citing time-sensitive information (model releases, framework versions, regulatory deadlines).
- **Difficulty tags**: Use ⭐ (foundational), ⭐⭐ (intermediate), ⭐⭐⭐ (advanced) on new questions.

## Code of Conduct

Be respectful, constructive, and focused on making this resource better for everyone preparing for AI/ML interviews.

## Questions?

Open a [Discussion](https://github.com/krunlp/AI-Prep-Buddy/discussions) or reach out via Issues.
