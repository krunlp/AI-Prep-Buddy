# scripts/

Tooling that keeps the question bank structurally sound.

| Script | Purpose |
|---|---|
| `qa_lib.py` | **Canonical parser.** Single source of truth for reading `questions.md` / `answers.md`. Handles both answer formats. Import this instead of writing your own regex. |
| `verify_integrity.py` | Fails on duplicates, numbering gaps, unanswered questions, orphan answers, section overlaps, header/content mismatch, and stale derived artifacts. Runs in CI. |
| `sync_derived.py` | Regenerates `data/questions.json`, the `QA_DATA` block in `simulator.html`, and the counts in `README.md` / `index.html`. Use `--check` to report drift without writing. |
| `pre-commit` | Git hook running both checks before every commit. |

## Usage

```bash
python3 scripts/sync_derived.py          # regenerate derived artifacts
python3 scripts/sync_derived.py --check  # report drift, change nothing
python3 scripts/verify_integrity.py      # structural checks
python3 scripts/qa_lib.py                # quick parse summary

ln -sf ../../scripts/pre-commit .git/hooks/pre-commit   # install hook
```

## Why this exists

In August 2026 five structural bugs shipped to `main` at once: a nine-question
numbering gap, a duplicated question number, a section whose range collided
with the previous section's, seventy-five unanswered questions, and a simulator
embedding a stale dataset. The root cause was that several ad-hoc scripts each
carried their own parsing regex, and one of them did not know about the
`### Question N:` answer format.

`qa_lib.py` exists so there is exactly one parser. `verify_integrity.py` exists
so those five bug classes cannot reach `main` again.
