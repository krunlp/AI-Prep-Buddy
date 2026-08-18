"""
qa_lib.py — canonical parser for the AI Prep Buddy question bank.

THIS IS THE SINGLE SOURCE OF TRUTH FOR PARSING.

Every script that reads questions.md / answers.md must import from here rather
than writing its own regex. The Aug 2026 numbering-collision incident happened
precisely because one script's regex knew about the `**N.**` answer format but
not the `### Question N:` format, so a renumbering pass silently updated half
the file and corrupted the mapping.

Source of truth:
    questions.md  — human-authored, canonical question text
    answers.md    — human-authored, canonical answer text

Derived artifacts (NEVER hand-edit; regenerate with scripts/sync_derived.py):
    data/questions.json
    simulator.html  (embedded QA_DATA block)
    README.md badge counts, index.html nav counts

Supported answer formats (both are valid; parser handles both):
    **123. Short title.** Answer body...
    ### Question 123: Long Title
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

QUESTIONS_MD = REPO_ROOT / "questions.md"
ANSWERS_MD = REPO_ROOT / "answers.md"
QUESTIONS_JSON = REPO_ROOT / "data" / "questions.json"
SIMULATOR_HTML = REPO_ROOT / "simulator.html"

# --- Canonical patterns. Change them HERE and nowhere else. ---------------

# A question line: "123. Some question text ⭐⭐"
RE_QUESTION = re.compile(r"^(\d+)\.\s+(.+?)\s*$", re.MULTILINE)

# Section header: "## Section 12 — Agentic AI (451–495)"
RE_SECTION = re.compile(r"^## (Section \d+\s*[—-][^\n]*)$", re.MULTILINE)

# Answer format A: "**123. Title.** body"
RE_ANSWER_INLINE = re.compile(r"^\*\*(\d+)\.\s+(.+?)\*\*", re.MULTILINE)

# Answer format B: "### Question 123: Title"
RE_ANSWER_HEADING = re.compile(r"^### Question (\d+):\s*(.*?)\s*$", re.MULTILINE)

# Trailing difficulty stars on a question
RE_STARS = re.compile(r"\s*⭐+\s*$")

# Bold-wrapped question title: "**Some Topic**"
RE_BOLD_WRAP = re.compile(r"^\*\*(.+?)\*\*$")

# Liquid raw guards. answers.md wraps code blocks containing Liquid-looking
# syntax (e.g. Semantic Kernel's {{$input}}) in {% raw %} tags so Jekyll can
# build the site. They must never reach derived artifacts.
RE_LIQUID_RAW = re.compile(r"\{%-?\s*(?:end)?raw\s*-?%\}")


# Numeric range in a section header: "(451–495)"
RE_HDR_RANGE = re.compile(r"\s*\(\d+\s*[–-]\s*\d+\)")


def _difficulty(text: str) -> int:
    """1 = Standard, 2 = Hard, 3 = Principal. 0 when untagged."""
    m = RE_STARS.search(text or "")
    return m.group(0).count("\u2b50") if m else 0


def _clean_question_text(text: str) -> str:
    text = RE_STARS.sub("", text).strip()
    m = RE_BOLD_WRAP.match(text)
    if m:
        text = m.group(1).strip()
    return text


def _clean_section_name(name: str) -> str:
    return RE_HDR_RANGE.sub("", name).strip()


def parse_questions(path: Path = QUESTIONS_MD) -> list[dict]:
    """Return [{n, section, question}] in document order."""
    text = path.read_text(encoding="utf-8")
    parts = RE_SECTION.split(text)

    out: list[dict] = []
    current_section = None
    for chunk in parts:
        if chunk.startswith("Section "):
            current_section = chunk.strip()
            continue
        if current_section is None:
            continue
        for m in RE_QUESTION.finditer(chunk):
            out.append(
                {
                    "n": int(m.group(1)),
                    "section": _clean_section_name(current_section),
                    "section_raw": current_section,
                    "question": _clean_question_text(m.group(2)),
                    "difficulty": _difficulty(m.group(2)),
                }
            )
    return out


def parse_answers(path: Path = ANSWERS_MD) -> dict[int, dict]:
    """Return {n: {n, title, body, format}} covering BOTH answer formats."""
    text = path.read_text(encoding="utf-8")
    answers: dict[int, dict] = {}

    # Collect every answer anchor from both formats, then slice bodies by the
    # next anchor. Doing it in one pass is what keeps the two formats in sync.
    anchors = []
    for m in RE_ANSWER_INLINE.finditer(text):
        anchors.append((m.start(), m.end(), int(m.group(1)), m.group(2).strip(), "inline"))
    for m in RE_ANSWER_HEADING.finditer(text):
        anchors.append((m.start(), m.end(), int(m.group(1)), m.group(2).strip(), "heading"))
    anchors.sort(key=lambda a: a[0])

    for i, (start, end, num, title, fmt) in enumerate(anchors):
        body_end = anchors[i + 1][0] if i + 1 < len(anchors) else len(text)
        body = text[end:body_end].strip()
        answers[num] = {"n": num, "title": title, "body": body, "format": fmt}

    return answers


def parse_all() -> tuple[list[dict], dict[int, dict]]:
    return parse_questions(), parse_answers()


def build_dataset() -> list[dict]:
    """Merged question+answer records used by every derived artifact."""
    questions = parse_questions()
    answers = parse_answers()
    dataset = []
    for q in questions:
        a = answers.get(q["n"])
        answer_text = ""
        if a:
            answer_text = RE_LIQUID_RAW.sub(" ", f"{a['title']} {a['body']}")
            answer_text = re.sub(r"\s+", " ", answer_text).strip()
        dataset.append(
            {
                "n": q["n"],
                "section": q["section"],
                "q": q["question"],
                "a": answer_text,
                "d": q.get("difficulty", 0),
            }
        )
    return dataset


def section_ranges(questions: list[dict] | None = None) -> list[dict]:
    """Per-section min/max question number, in document order."""
    if questions is None:
        questions = parse_questions()
    seen: dict[str, dict] = {}
    order: list[str] = []
    for q in questions:
        key = q["section_raw"]
        if key not in seen:
            seen[key] = {"section": key, "min": q["n"], "max": q["n"], "count": 0}
            order.append(key)
        seen[key]["min"] = min(seen[key]["min"], q["n"])
        seen[key]["max"] = max(seen[key]["max"], q["n"])
        seen[key]["count"] += 1
    return [seen[k] for k in order]


if __name__ == "__main__":
    qs, ans = parse_all()
    print(f"questions.md : {len(qs)} questions")
    print(f"answers.md   : {len(ans)} answers")
    fmts = {}
    for a in ans.values():
        fmts[a["format"]] = fmts.get(a["format"], 0) + 1
    print(f"answer formats: {fmts}")
