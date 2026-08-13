#!/usr/bin/env python3
"""
verify_integrity.py — fails the build on any structural corruption of the bank.

Every check here exists because the corresponding bug ACTUALLY HAPPENED and
shipped to main. Do not weaken a check to make CI green; fix the data.

Run locally:  python3 scripts/verify_integrity.py
"""

import json
import re
import sys
from collections import Counter

import qa_lib

FAILURES: list[str] = []
WARNINGS: list[str] = []


def fail(check: str, msg: str) -> None:
    FAILURES.append(f"[{check}] {msg}")


def warn(check: str, msg: str) -> None:
    WARNINGS.append(f"[{check}] {msg}")


def _fmt(nums, limit=15):
    nums = list(nums)
    shown = ", ".join(str(n) for n in nums[:limit])
    return shown + (f" … (+{len(nums) - limit} more)" if len(nums) > limit else "")


def main() -> int:
    questions = qa_lib.parse_questions()
    answers = qa_lib.parse_answers()

    q_nums = [q["n"] for q in questions]
    q_set = set(q_nums)
    a_set = set(answers)

    print(f"questions.md : {len(q_nums)} question lines, {len(q_set)} unique")
    print(f"answers.md   : {len(a_set)} answers")

    # 1. Duplicate question numbers.
    #    Regression guard: Q610 appeared twice with two different questions.
    dupes = sorted(n for n, c in Counter(q_nums).items() if c > 1)
    if dupes:
        fail("duplicate-questions", f"question numbers used more than once: {_fmt(dupes)}")

    # 2. Gaps in the numbering sequence.
    #    Regression guard: Q441-449 silently vanished (twice).
    expected = set(range(1, max(q_set) + 1))
    gaps = sorted(expected - q_set)
    if gaps:
        fail("numbering-gaps", f"missing question numbers: {_fmt(gaps)}")

    # 3. Every question has an answer.
    #    Regression guard: Sections 47-49 shipped with 75 unanswered questions.
    unanswered = sorted(q_set - a_set)
    if unanswered:
        fail("unanswered", f"{len(unanswered)} questions have no answer: {_fmt(unanswered)}")

    # 4. No answer without a matching question.
    orphans = sorted(a_set - q_set)
    if orphans:
        fail("orphan-answers", f"{len(orphans)} answers have no question: {_fmt(orphans)}")

    # 5. Sections must occupy contiguous, non-overlapping ranges.
    #    Regression guard: Section 43 restarted at 1439 and collided with
    #    Section 42's tail (1439-1446), giving 8 numbers two meanings.
    ranges = qa_lib.section_ranges(questions)
    prev = None
    for r in ranges:
        if prev is not None and r["min"] <= prev["max"]:
            fail(
                "section-overlap",
                f"'{r['section'][:60]}' starts at {r['min']} but "
                f"'{prev['section'][:60]}' already ends at {prev['max']}",
            )
        prev = r

    # 6. Section header declared range must match actual contents.
    for r in ranges:
        m = re.search(r"\((\d+)\s*[–-]\s*(\d+)\)", r["section"])
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if (lo, hi) != (r["min"], r["max"]):
                fail(
                    "header-range",
                    f"'{r['section'][:60]}' header says ({lo}–{hi}) "
                    f"but contains {r['min']}–{r['max']}",
                )

    # 7. Derived artifacts must be in sync with source.
    #    Regression guard: simulator.html shipped a stale pre-fix dataset.
    total = len(q_set)
    try:
        blob = json.loads(qa_lib.QUESTIONS_JSON.read_text(encoding="utf-8"))
        if blob.get("total_questions") != total:
            fail(
                "derived-json",
                f"data/questions.json total_questions={blob.get('total_questions')} "
                f"but source has {total} — run scripts/sync_derived.py",
            )
        if len(blob.get("questions", [])) != total:
            fail(
                "derived-json",
                f"data/questions.json holds {len(blob.get('questions', []))} records "
                f"but source has {total} — run scripts/sync_derived.py",
            )
    except FileNotFoundError:
        warn("derived-json", "data/questions.json not found")
    except json.JSONDecodeError as exc:
        fail("derived-json", f"data/questions.json is not valid JSON: {exc}")

    try:
        html = qa_lib.SIMULATOR_HTML.read_text(encoding="utf-8")
        m = re.search(
            r"const QA_DATA = /\*QA_DATA_START\*/(.*?)/\*QA_DATA_END\*/;", html, re.DOTALL
        ) or re.search(r"const QA_DATA = (\[.*\]);", html, re.DOTALL)
        if not m:
            fail("derived-simulator", "could not find embedded QA_DATA in simulator.html")
        else:
            sim = json.loads(m.group(1))
            if len(sim) != total:
                fail(
                    "derived-simulator",
                    f"simulator.html embeds {len(sim)} questions but source has "
                    f"{total} — run scripts/sync_derived.py",
                )
            missing_a = [r["n"] for r in sim if not r.get("a")]
            if missing_a:
                fail(
                    "derived-simulator",
                    f"{len(missing_a)} simulator entries have an empty answer: "
                    f"{_fmt(missing_a)}",
                )

        # The simulator's JS must survive data injection.
        # Regression guard: a greedy `const QA_DATA = \[.*\];` substitution
        # matched to the last `];` in the file and deleted every function
        # defined after the data block, leaving a syntactically broken page
        # whose data still parsed perfectly.
        required_symbols = [
            "function pickQuestion",
            "function startTimer",
            "function grade",
            "function renderStats",
            "function loadStats",
            "function saveStats",
            "getElementById('sectionFilter')",
            "addEventListener('click', pickQuestion)",
            # voice features
            "function speakQuestion",
            "function startRecording",
            "function stopRecording",
            "function resetVoiceForNewQuestion",
            "speechSynthesis",
            "webkitSpeechRecognition",
            # answer evaluation
            "function localScore",
            "function extractConcepts",
            "function evaluateWithLLM",
            "function evaluateAnswer",
            "openrouter.ai/api/v1/chat/completions",
        ]
        for sym in required_symbols:
            if sym not in html:
                fail("simulator-js", f"simulator.html is missing required code: {sym!r}")

        if "/*QA_DATA_START*/" not in html or "/*QA_DATA_END*/" not in html:
            fail(
                "simulator-js",
                "simulator.html QA_DATA is not delimited — sync_derived.py cannot "
                "safely locate the array bounds",
            )

        # Rough brace/paren balance inside the script block catches truncation.
        try:
            script = html[html.index("<script>") + len("<script>") : html.rindex("</script>")]
            body = re.sub(
                r"/\*QA_DATA_START\*/.*?/\*QA_DATA_END\*/", "[]", script, flags=re.DOTALL
            )
            if body.count("{") != body.count("}"):
                fail(
                    "simulator-js",
                    f"unbalanced braces in simulator script "
                    f"({body.count('{')} open vs {body.count('}')} close) — likely truncated",
                )
        except ValueError:
            fail("simulator-js", "simulator.html has no <script> block")
    except FileNotFoundError:
        warn("derived-simulator", "simulator.html not found")

    # 8. Advertised counts in human-facing files must match reality.
    #    Regression guard: README badge and index.html nav sat at 1613.
    for name in ("README.md", "index.html"):
        path = qa_lib.REPO_ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        # Only look at places that genuinely advertise a bank-wide total:
        #   "1621 Questions", "Questions-1621-blue" (badge), "Questions (1621)"
        # Deliberately NOT bare "(1035)", which is a legitimate section range.
        # Non-capturing inner alternation, then one capturing group around it.
        # An unparenthesised alternation would split every enclosing pattern.
        num = r"((?:\d{1,3}(?:,\d{3})+|\d{3,5}))"
        candidates = re.findall(rf"{num}\s*\+?\s*(?:questions|Questions)\b", text)
        candidates += re.findall(rf"Questions-{num}-", text)
        candidates += re.findall(rf"Questions\s*\({num}\)", text)
        candidates += re.findall(rf'stat-number[^>]*>\s*{num}\s*<', text)
        stale = {int(n.replace(",", "")) for n in candidates if int(n.replace(",", "")) != total}
        if stale:
            fail(
                "advertised-count",
                f"{name} advertises {_fmt(sorted(stale))} but source has {total} "
                f"— run scripts/sync_derived.py",
            )

    # 9. No two source pages may render to the same URL.
    #    Regression guard: index.md and index.html both rendered to /index.html,
    #    so Jekyll silently dropped one and the surviving homepage was arbitrary.
    from collections import defaultdict

    outputs = defaultdict(list)
    for p in qa_lib.REPO_ROOT.glob("*.md"):
        if p.name in {"README.md", "CONTRIBUTING.md"}:
            continue
        outputs[p.stem + ".html"].append(p.name)
    for p in qa_lib.REPO_ROOT.glob("*.html"):
        outputs[p.name].append(p.name)
    for url, sources in sorted(outputs.items()):
        if len(sources) > 1:
            fail(
                "page-conflict",
                f"/{url} is produced by multiple files: {sorted(sources)} — "
                f"Jekyll will drop one non-deterministically",
            )

    # 10. Every published page must be reachable from the homepage.
    #     Regression guard: code-solutions.html and sources.html existed but
    #     nothing linked to them, so the content was effectively invisible.
    index_path = qa_lib.REPO_ROOT / "index.html"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        linked = set(re.findall(r'href="([a-z0-9\-]+)\.html"', index_text))
        published = {u[:-5] for u in outputs} - {"index"}
        unlinked = sorted(published - linked)
        if unlinked:
            fail(
                "orphan-page",
                f"published but not linked from index.html: "
                f"{', '.join(p + '.html' for p in unlinked)}",
            )

    # --- report -----------------------------------------------------------
    print()
    for w in WARNINGS:
        print(f"WARN  {w}")
    if FAILURES:
        print()
        for f in FAILURES:
            print(f"FAIL  {f}")
        print(f"\n{len(FAILURES)} integrity check(s) failed.")
        return 1

    print(f"All integrity checks passed — {total} questions, {len(a_set)} answers, "
          f"{len(ranges)} sections, no gaps/duplicates/overlaps.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
