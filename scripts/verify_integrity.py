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
    #     Regression guard: questions.md kept advertising 1,613 in its H1 long
    #     after the bank grew, because this check only looked at two files.
    #     Regression guard 2: _layouts/default.html is the site-wide shell, so
    #     one stale number there is stale on EVERY page. It was advertising
    #     1,613 in both the nav and the footer while every check passed.
    page_files = ["README.md", "index.html", "questions.md", "answers.md",
                  "cheatsheet.md", "study-paths.md", "simulator.html",
                  "_layouts/default.html", "_config.yml", "roles.html"]
    for name in page_files:
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

    # 8b. The question page's hover/tap reveal depends on a generated answer
    #     lookup and a client script. Both must exist and match the source.
    ans_json = qa_lib.REPO_ROOT / "data" / "answers.json"
    hover_js = qa_lib.REPO_ROOT / "assets" / "js" / "question-answers.js"
    if not hover_js.exists():
        fail("hover-answers", "assets/js/question-answers.js is missing")
    else:
        qmd = (qa_lib.REPO_ROOT / "questions.md").read_text(encoding="utf-8")
        if "question-answers.js" not in qmd:  # version query tolerated
            fail("hover-answers", "questions.md does not load question-answers.js")
    if not ans_json.exists():
        fail("hover-answers", "data/answers.json is missing — run scripts/sync_derived.py")
    else:
        try:
            blob = json.loads(ans_json.read_text(encoding="utf-8"))
            got = len(blob.get("answers", {}))
            if got != total:
                fail(
                    "hover-answers",
                    f"data/answers.json holds {got} answers but source has {total} "
                    f"— run scripts/sync_derived.py",
                )
        except json.JSONDecodeError as exc:
            fail("hover-answers", f"data/answers.json is not valid JSON: {exc}")

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

    # 8b2. README must stay a landing page, not a second copy of the bank.
    #      Regression guard: it silently held a stale duplicate of 1,206
    #      questions across 31 sections while the bank had 1,716 across 54.
    readme = qa_lib.REPO_ROOT / "README.md"
    if readme.exists():
        rtext = readme.read_text(encoding="utf-8")
        rq = len(set(re.findall(r"^(\d+)\.\s", rtext, re.MULTILINE)))
        if rq > 50:
            fail(
                "readme-duplication",
                f"README.md contains {rq} numbered questions — it must link to "
                f"questions.md, not duplicate it (the copy silently goes stale)",
            )

    # 8c. Diagram-count claims must match the actual number of diagrams.
    #     Regression guard: diagrams.md carried interim notes claiming "13
    #     diagrams" and "28 diagrams" long after it held 39.
    for name, pattern in (("diagrams.md", r"^## \d+\."), ("patterns.md", r"^### [A-Z]\d+\.")):
        path = qa_lib.REPO_ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        actual = len(re.findall(pattern, text, re.MULTILINE))
        claims = {int(n) for n in re.findall(r"\b(\d{1,3}) diagrams\b", text)}
        wrong = sorted(c for c in claims if c != actual)
        if wrong:
            fail(
                "diagram-count",
                f"{name} claims {wrong} diagrams but contains {actual}",
            )

    # 8d. Every section must be assigned to at least one role, or it is
    #     invisible on the role map. Regression guard: Section 50 was added
    #     without being mapped to any role.
    try:
        sys.path.insert(0, str(qa_lib.REPO_ROOT / "scripts"))
        from roles_data import ROLES as _ROLES

        assigned = set()
        for r in _ROLES:
            for t in ("core", "important", "optional"):
                assigned |= set(r.get(t, []))
        all_secs = set()
        for r in qa_lib.section_ranges():
            m = re.match(r"Section (\d+)", r["section"])
            if m:
                all_secs.add(int(m.group(1)))
        unassigned = sorted(all_secs - assigned)
        unknown = sorted(assigned - all_secs)
        if unassigned:
            fail("role-coverage",
                 f"sections not assigned to any role: {_fmt(unassigned)}")
        if unknown:
            fail("role-coverage",
                 f"roles_data.py references non-existent sections: {_fmt(unknown)}")
    except ImportError:
        warn("role-coverage", "scripts/roles_data.py not importable")

    # 9b. The shared layout's nav must reach every published page. It is the
    #     only navigation on markdown pages, so a page missing here is
    #     effectively unreachable while browsing.
    layout = qa_lib.REPO_ROOT / "_layouts" / "default.html"
    if layout.exists():
        lt = layout.read_text(encoding="utf-8")
        nav_links = set(re.findall(r'href="\{\{ site\.baseurl \}\}/([a-z0-9\-]+)\.html"', lt))
        published_pages = {p.stem for p in qa_lib.REPO_ROOT.glob("*.md")
                           if p.name not in {"README.md", "CONTRIBUTING.md"}}
        published_pages |= {p.stem for p in qa_lib.REPO_ROOT.glob("*.html")}
        missing_nav = sorted(published_pages - nav_links - {"index"})
        if missing_nav:
            fail(
                "layout-nav",
                "pages missing from the shared layout nav: "
                + ", ".join(p + ".html" for p in missing_nav),
            )

    # 9c. Standalone HTML pages don't use the shared layout, so each carries
    #     its own nav. Regression guard: simulator.html shipped without links
    #     to roles, study-paths and code-solutions.
    standalone = ["simulator.html", "roles.html", "index.html"]
    all_pages = {p.stem for p in qa_lib.REPO_ROOT.glob("*.md")
                 if p.name not in {"README.md", "CONTRIBUTING.md"}}
    all_pages |= {p.stem for p in qa_lib.REPO_ROOT.glob("*.html")}
    for name in standalone:
        path = qa_lib.REPO_ROOT / name
        if not path.exists():
            continue
        linked = set(re.findall(r'href="([a-z0-9\-]+)\.html"',
                                path.read_text(encoding="utf-8")))
        gap = sorted(all_pages - linked - {path.stem})
        if gap:
            fail(
                "standalone-nav",
                f"{name} nav is missing: " + ", ".join(p + ".html" for p in gap),
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

    # 11. Jekyll builds every front-matter file through Liquid BEFORE markdown,
    #     so template syntax inside a fenced code block still gets parsed. A
    #     code sample containing {{$input}} (Semantic Kernel) or {% ... %} is a
    #     Liquid syntax error and breaks the GitHub Pages build silently — the
    #     site keeps serving the last good commit while pushes appear to work.
    #     Regression guard: this broke Pages for 30+ builds undetected.
    RE_FENCE = re.compile(r"^(?:```|~~~)")
    RE_RAW_OPEN = re.compile(r"\{%-?\s*raw\s*-?%\}")
    RE_RAW_CLOSE = re.compile(r"\{%-?\s*endraw\s*-?%\}")

    for path in sorted(qa_lib.REPO_ROOT.glob("*.md")) + sorted(
        qa_lib.REPO_ROOT.glob("*.html")
    ):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue  # no front matter: Jekyll copies it verbatim, Liquid never runs
        lines = text.split("\n")
        in_fence = False
        in_raw = False
        opens = closes = 0
        for lineno, line in enumerate(lines, 1):
            if RE_RAW_OPEN.search(line):
                in_raw, opens = True, opens + 1
            if RE_RAW_CLOSE.search(line):
                in_raw, closes = False, closes + 1
            if RE_FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence and not in_raw and ("{{" in line or "{%" in line):
                fail(
                    "liquid-safety",
                    f"{path.name}:{lineno} has Liquid syntax in an unguarded code "
                    f"block — wrap the block in {{% raw %}} / {{% endraw %}} or the "
                    f"Jekyll build fails",
                )
        if opens != closes:
            fail(
                "liquid-safety",
                f"{path.name}: unbalanced raw guards ({opens} raw, {closes} endraw)",
            )

    # 12. Liquid raw guards are a Jekyll build concern only; they must never
    #     leak into derived artifacts that the simulator and JSON consumers read.
    for rec in qa_lib.build_dataset():
        if RE_RAW_OPEN.search(rec["a"]) or RE_RAW_CLOSE.search(rec["a"]):
            fail(
                "liquid-safety",
                f"Q{rec['n']}: derived answer text contains a Liquid raw guard — "
                f"qa_lib must strip these",
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
