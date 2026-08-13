#!/usr/bin/env python3
"""
sync_derived.py — regenerate every derived artifact from the source of truth.

Source of truth : questions.md, answers.md
Derived         : data/questions.json
                  simulator.html   (embedded QA_DATA)
                  README.md        (title + badge counts)
                  index.html       (nav/hero/stat counts)

Run this after ANY edit to questions.md or answers.md, then run
scripts/verify_integrity.py. CI enforces that this has been done: if a derived
artifact is out of date, the build fails.

    python3 scripts/sync_derived.py
    python3 scripts/sync_derived.py --check   # report drift, change nothing
"""

import argparse
import json
import re
import sys

import qa_lib


def _fmt_thousands(n: int) -> str:
    return f"{n:,}"


def sync_questions_json(dataset, total, sections, dry_run=False):
    path = qa_lib.QUESTIONS_JSON
    if path.exists():
        blob = json.loads(path.read_text(encoding="utf-8"))
    else:
        blob = {"name": "AI Prep Buddy Question Bank", "version": "1.0"}

    blob["total_questions"] = total
    blob["total_sections"] = sections
    blob["questions"] = [
        {"id": r["n"], "section": r["section"], "question": r["q"]} for r in dataset
    ]

    new_text = json.dumps(blob, indent=2, ensure_ascii=False) + "\n"
    old_text = path.read_text(encoding="utf-8") if path.exists() else ""
    if new_text == old_text:
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8")
    return True


def sync_simulator(dataset, total, dry_run=False):
    path = qa_lib.SIMULATOR_HTML
    if not path.exists():
        return False
    html = path.read_text(encoding="utf-8")
    original = html

    payload = json.dumps(dataset, ensure_ascii=False)
    block = (
        "const QA_DATA = /*QA_DATA_START*/" + payload + "/*QA_DATA_END*/;"
    )

    # The payload contains `];` sequences, so a bare regex cannot be trusted to
    # find the end of the array. Only the explicitly delimited form is written
    # or matched. A greedy `const QA_DATA = \[.*\];` fallback used to exist here
    # and matched to the LAST `];` in the file, silently deleting every function
    # defined after the data block. Do not reintroduce it.
    if "/*QA_DATA_START*/" not in html:
        print(
            "  ! simulator.html: QA_DATA delimiters missing. Wrap the array as\n"
            "      const QA_DATA = /*QA_DATA_START*/[...]/*QA_DATA_END*/;\n"
            "    and re-run. Refusing to guess the array bounds.",
            file=sys.stderr,
        )
        return False

    html, n = re.subn(
        r"const QA_DATA = /\*QA_DATA_START\*/.*?/\*QA_DATA_END\*/;",
        lambda m: block,
        html,
        flags=re.DOTALL,
    )
    if n == 0:
        print("  ! simulator.html: QA_DATA block not found, skipping", file=sys.stderr)
        return False

    # Keep human-facing copy in step with the dataset.
    html = re.sub(r"all [\d,]+ questions", f"all {_fmt_thousands(total)} questions", html)
    html = re.sub(r"[\d,]+-question bank", f"{_fmt_thousands(total)}-question bank", html)

    if html == original:
        return False
    if not dry_run:
        path.write_text(html, encoding="utf-8")
    return True


def sync_readme(total, dry_run=False):
    path = qa_lib.REPO_ROOT / "README.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    original = text

    text = re.sub(r"\(([\d,]+) Questions\)", f"({_fmt_thousands(total)} Questions)", text, count=1)
    text = re.sub(r"Questions-[\d,]+-", f"Questions-{total}-", text)

    if text == original:
        return False
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True


def sync_index_html(total, dry_run=False):
    path = qa_lib.REPO_ROOT / "index.html"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    original = text

    pretty = _fmt_thousands(total)
    # MUST stay wrapped in a non-capturing group: an unparenthesised
    # alternation here silently splits every enclosing pattern it is
    # interpolated into (this caused runaway "Questions (Questions (…" growth).
    num = r"(?:\d{1,3}(?:,\d{3})+|\d{3,5})"

    text = re.sub(rf"({num})(\s*\+?\s*)(questions|Questions)\b", rf"{pretty}\2\3", text)
    # Idempotent: collapse any accumulated "Questions (Questions (…" prefixes
    # back to a single canonical form.
    text = re.sub(rf"(?:Questions\s*\(\s*)+{num}\s*\)", f"Questions ({total})", text)
    text = re.sub(
        rf"(stat-number[^>]*>)\s*(?:{num})\s*(<)", rf"\g<1>{pretty}\g<2>", text
    )
    # Prose forms: "1,613 principal-grade questions", "1,613 principal-level
    # AI/ML interview questions" — any count within a short span before the
    # word "question(s)".
    text = re.sub(
        rf"\b(?:{num})\b(?=[^<>.]{{0,60}}?questions\b)", pretty, text
    )

    if text == original:
        return False
    if not dry_run:
        path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    args = ap.parse_args()

    dataset = qa_lib.build_dataset()
    total = len(dataset)
    sections = len(qa_lib.section_ranges())

    missing = [r["n"] for r in dataset if not r["a"]]
    if missing:
        print(
            f"refusing to sync: {len(missing)} questions have no answer "
            f"(first: {missing[:10]}). Fix answers.md first.",
            file=sys.stderr,
        )
        return 1

    print(f"source of truth: {total} questions across {sections} sections")

    changed = {
        "data/questions.json": sync_questions_json(dataset, total, sections, args.check),
        "simulator.html": sync_simulator(dataset, total, args.check),
        "README.md": sync_readme(total, args.check),
        "index.html": sync_index_html(total, args.check),
    }

    drifted = [name for name, did in changed.items() if did]
    if args.check:
        if drifted:
            print("\nout of date (run scripts/sync_derived.py):")
            for name in drifted:
                print(f"  - {name}")
            return 1
        print("all derived artifacts are up to date.")
        return 0

    if drifted:
        print("\nregenerated:")
        for name in drifted:
            print(f"  - {name}")
    else:
        print("\nall derived artifacts were already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
