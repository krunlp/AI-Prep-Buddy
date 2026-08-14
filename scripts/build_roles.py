#!/usr/bin/env python3
"""
build_roles.py — generate roles.html (role → sections to complete) from
questions.md plus scripts/roles_data.py.

Never hand-edit roles.html. Edit roles_data.py and re-run
scripts/sync_derived.py, which calls this.
"""

import html
import json
import re
import sys

import qa_lib
from roles_data import ROLES

OUT = qa_lib.REPO_ROOT / "roles.html"

NAV = [
    ("index.html", "Home"),
    ("questions.html", "Questions"),
    ("answers.html", "Answers"),
    ("interview.html", "🎙️ Live Interview"),
    ("simulator.html", "🎤 Simulator"),
    ("study-paths.html", "Study Paths"),
    ("diagrams.html", "Diagrams"),
    ("patterns.html", "Patterns"),
    ("code-solutions.html", "Code"),
    ("cheatsheet.html", "Cheat Sheet"),
    ("glossary.html", "Glossary"),
    ("company-prep.html", "Companies"),
    ("sources.html", "Sources"),
]


def section_index():
    """{section_number: {num, title, min, max, count, raw}}"""
    out = {}
    for r in qa_lib.section_ranges():
        m = re.match(r"Section (\d+)\s*[—-]\s*(.+)", r["section"])
        if not m:
            continue
        num = int(m.group(1))
        title = re.sub(r"\s*\(\d+\s*[–-]\s*\d+\)\s*$", "", m.group(2)).strip()
        out[num] = {
            "num": num,
            "title": title,
            "min": r["min"],
            "max": r["max"],
            "count": r["count"],
            "raw": r["section"],
        }
    return out


def build_payload(sections):
    roles = []
    for role in ROLES:
        tiers = {}
        total = 0
        for tier in ("core", "important", "optional"):
            items = []
            for n in role.get(tier, []):
                s = sections.get(n)
                if not s:
                    print(f"  ! role {role['id']}: unknown section {n}", file=sys.stderr)
                    continue
                items.append(s)
                if tier in ("core", "important"):
                    total += s["count"]
            items.sort(key=lambda s: s["num"])
            tiers[tier] = items
        roles.append({
            "id": role["id"],
            "name": role["name"],
            "level": role["level"],
            "blurb": role["blurb"],
            "tiers": tiers,
            "requiredQuestions": total,
            "coreQuestions": sum(s["count"] for s in tiers["core"]),
        })
    return roles


TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Role-Based Section Map — AI Prep Buddy</title>
<meta name="description" content="Pick your target role and see exactly which of the __TOTAL_SECTIONS__ sections to complete, with progress tracking.">
<style>
  :root {
    --bg: #0f1117; --card: #171a23; --border: rgba(255,255,255,0.12);
    --text-primary: #e8eaed; --text-secondary: #9aa4b2;
    --accent-indigo: #6366f1; --accent-emerald: #10b981;
    --accent-amber: #f59e0b; --accent-rose: #ef4444;
  }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    max-width: 900px; margin: 0 auto; padding: 20px; background: var(--bg); color: var(--text-primary); line-height: 1.6; }
  header { text-align: center; margin-bottom: 18px; }
  h1 { margin-bottom: 6px; }
  header p { color: var(--text-secondary); margin-top: 0; }
  nav { text-align: center; margin-bottom: 26px; font-size: 0.9em; }
  nav a { color: var(--accent-indigo); text-decoration: none; margin: 0 6px; white-space: nowrap; }
  nav a:hover { text-decoration: underline; }
  .picker { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; justify-content: center; margin-bottom: 18px; }
  select, button { padding: 9px 13px; border-radius: 8px; border: 1px solid var(--border);
    background: var(--card); color: var(--text-primary); font-size: 0.95em; cursor: pointer; }
  select { min-width: 280px; }
  .role-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 18px; margin-bottom: 18px; }
  .role-level { display: inline-block; font-size: 0.72em; text-transform: uppercase; letter-spacing: 0.6px;
    padding: 3px 9px; border-radius: 20px; background: rgba(99,102,241,0.16); color: var(--accent-indigo); }
  .role-blurb { color: var(--text-secondary); margin: 10px 0 0; }
  .progress-wrap { margin-top: 16px; }
  .progress-bar { height: 10px; border-radius: 6px; background: rgba(255,255,255,0.08); overflow: hidden; }
  .progress-fill { height: 100%; width: 0%; background: linear-gradient(90deg, var(--accent-indigo), var(--accent-emerald)); transition: width .25s ease; }
  .progress-text { font-size: 0.85em; color: var(--text-secondary); margin-top: 7px; text-align: center; }
  .tier { margin-top: 22px; }
  .tier h2 { font-size: 1.02em; margin: 0 0 4px; display: flex; align-items: center; gap: 8px; }
  .tier-note { font-size: 0.83em; color: var(--text-secondary); margin: 0 0 10px; }
  .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
  .dot.core { background: var(--accent-rose); }
  .dot.important { background: var(--accent-amber); }
  .dot.optional { background: var(--text-secondary); }
  .sec { display: flex; align-items: flex-start; gap: 11px; padding: 10px 12px; border: 1px solid var(--border);
    border-radius: 9px; margin-bottom: 8px; background: rgba(255,255,255,0.02); }
  .sec input { margin-top: 5px; width: 17px; height: 17px; flex: none; cursor: pointer; }
  .sec-body { flex: 1; min-width: 0; }
  .sec-title { font-weight: 600; }
  .sec.done .sec-title { text-decoration: line-through; opacity: 0.55; }
  .sec-meta { font-size: 0.82em; color: var(--text-secondary); margin-top: 2px; }
  .sec-meta a { color: var(--accent-indigo); text-decoration: none; }
  .sec-meta a:hover { text-decoration: underline; }
  footer { text-align: center; margin-top: 34px; font-size: 0.84em; color: var(--text-secondary); }
  footer a { color: var(--accent-indigo); }
  @media (max-width: 600px) { select { min-width: 100%; } body { padding: 14px; } }

  /* Light theme. This page is standalone (no Jekyll layout), so it reads the
     theme the shared layout's toggle stored in localStorage. */
  html[data-theme="light"] {
    --bg: #f6f8fb;
    --card: #ffffff;
    --border: rgba(16,32,46,0.14);
    --text-primary: #16202e;
    --text-secondary: #55627a;
  }
</style>
<script>
(function () {
  try {
    var t = localStorage.getItem('theme');
    if (t === 'light' || t === 'dark') {
      document.documentElement.setAttribute('data-theme', t);
    }
  } catch (e) {}
})();
</script>
</head>
<body>

<header>
<h1>🎯 Role-Based Section Map</h1>
<p>Pick your target designation and see exactly which sections to complete. Progress saves in this browser.</p>
</header>

<nav>__NAV__</nav>

<div class="picker">
  <select id="roleSelect"></select>
  <button id="resetBtn">Reset progress</button>
</div>

<div id="roleView"></div>

<footer>
Progress is stored in this browser only (localStorage) — nothing is uploaded.<br>
Want a day-by-day plan instead? See <a href="study-paths.html">Study Paths</a>.<br>
Generated from the question bank — <a href="https://github.com/krunlp/AI-Prep-Buddy">source</a>.
</footer>

<script>
const ROLES = __ROLES_JSON__;
const STORE = 'aiPrepBuddyRoleProgress';
const LAST_ROLE = 'aiPrepBuddyLastRole';

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (e) { return {}; }
}
function saveProgress(p) {
  try { localStorage.setItem(STORE, JSON.stringify(p)); } catch (e) {}
}
function esc(s) {
  return String(s).replace(/[&<>"']/g, c =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

const sel = document.getElementById('roleSelect');
ROLES.forEach(r => {
  const o = document.createElement('option');
  o.value = r.id;
  o.textContent = r.name + ' — ' + r.level;
  sel.appendChild(o);
});

const TIER_NOTE = {
  core: 'Must complete. This is what the loop actually tests.',
  important: 'Should complete. Commonly probed and expected at this level.',
  optional: 'Nice to have. Breadth and differentiation.'
};

function render(roleId) {
  const role = ROLES.find(r => r.id === roleId) || ROLES[0];
  const progress = loadProgress();
  const done = progress[role.id] || {};

  let required = 0, doneCount = 0, doneQuestions = 0;
  ['core', 'important'].forEach(t => role.tiers[t].forEach(s => {
    required++;
    if (done[s.num]) { doneCount++; doneQuestions += s.count; }
  }));
  const pct = required ? Math.round((doneCount / required) * 100) : 0;

  let html = '';
  html += '<div class="role-card">';
  html += '<span class="role-level">' + esc(role.level) + '</span>';
  html += '<h2 style="margin:9px 0 0">' + esc(role.name) + '</h2>';
  html += '<p class="role-blurb">' + esc(role.blurb) + '</p>';
  html += '<div class="progress-wrap"><div class="progress-bar">' +
          '<div class="progress-fill" style="width:' + pct + '%"></div></div>' +
          '<div class="progress-text">' + doneCount + ' of ' + required +
          ' required sections complete (' + pct + '%) · ' +
          doneQuestions + ' of ' + role.requiredQuestions + ' questions covered</div></div>';
  html += '</div>';

  ['core', 'important', 'optional'].forEach(tier => {
    const list = role.tiers[tier];
    if (!list.length) return;
    const label = tier.charAt(0).toUpperCase() + tier.slice(1);
    const qs = list.reduce((a, s) => a + s.count, 0);
    html += '<div class="tier"><h2><span class="dot ' + tier + '"></span>' + label +
            ' <span style="font-weight:400;color:var(--text-secondary);font-size:.85em">(' +
            list.length + ' sections · ' + qs + ' questions)</span></h2>';
    html += '<p class="tier-note">' + TIER_NOTE[tier] + '</p>';
    list.forEach(s => {
      const isDone = !!done[s.num];
      html += '<label class="sec' + (isDone ? ' done' : '') + '" data-sec="' + s.num + '">' +
        '<input type="checkbox" data-sec="' + s.num + '"' + (isDone ? ' checked' : '') + '>' +
        '<span class="sec-body">' +
          '<span class="sec-title">Section ' + s.num + ' — ' + esc(s.title) + '</span>' +
          '<span class="sec-meta">Q' + s.min + '–Q' + s.max + ' · ' + s.count + ' questions · ' +
            '<a href="questions.html">read</a> · ' +
            '<a href="simulator.html?section=' + s.num + '">practice</a>' +
          '</span>' +
        '</span></label>';
    });
    html += '</div>';
  });

  document.getElementById('roleView').innerHTML = html;

  document.querySelectorAll('#roleView input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', () => {
      const p = loadProgress();
      p[role.id] = p[role.id] || {};
      if (cb.checked) p[role.id][cb.dataset.sec] = 1;
      else delete p[role.id][cb.dataset.sec];
      saveProgress(p);
      render(role.id);
    });
  });
}

sel.addEventListener('change', () => {
  localStorage.setItem(LAST_ROLE, sel.value);
  render(sel.value);
});

document.getElementById('resetBtn').addEventListener('click', () => {
  if (!confirm('Reset progress for this role?')) return;
  const p = loadProgress();
  delete p[sel.value];
  saveProgress(p);
  render(sel.value);
});

const last = localStorage.getItem(LAST_ROLE);
if (last && ROLES.some(r => r.id === last)) sel.value = last;
render(sel.value);
</script>

</body>
</html>
"""


def main() -> int:
    sections = section_index()
    roles = build_payload(sections)
    nav = " · ".join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in NAV)

    page = (TEMPLATE
            .replace("__ROLES_JSON__", json.dumps(roles, ensure_ascii=False))
            .replace("__NAV__", nav)
            .replace("__TOTAL_SECTIONS__", str(len(sections))))

    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if old == page:
        return 0
    OUT.write_text(page, encoding="utf-8")
    print(f"  - roles.html ({len(roles)} roles, {len(sections)} sections)")
    return 1


if __name__ == "__main__":
    sys.exit(0 if main() >= 0 else 1)
