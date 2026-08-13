/*
 * smoke_test.js — load every interactive page and RUN its JavaScript.
 *
 * Why this exists:
 *
 * A sync script once replaced the simulator's data block with a greedy regex
 * that matched to the last `];` in the file, deleting every function defined
 * after it. The embedded JSON still parsed perfectly, so every data-integrity
 * check passed while the page was completely dead. That broken build shipped.
 *
 * Data checks answer "is the content correct". This answers "does the program
 * still run". Both are needed; only the second would have caught that.
 *
 * Usage:  node scripts/smoke_test.js
 * Requires: npm install --no-save jsdom
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const REPO = path.resolve(__dirname, '..');
const failures = [];
const notes = [];

function fail(page, msg) { failures.push(`[${page}] ${msg}`); }
function ok(page, msg) { notes.push(`  ✓ ${page}: ${msg}`); }

function readJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(REPO, rel), 'utf8'));
}

function makeDom(file, { url = 'https://example.com/', hover = true } = {}) {
  const html = fs.readFileSync(path.join(REPO, file), 'utf8');
  const dom = new JSDOM(html, { url, runScripts: 'outside-only', pretendToBeVisual: true });
  const w = dom.window;
  w.matchMedia = (q) => ({ matches: hover && /hover: hover/.test(q), addListener() {}, removeListener() {} });
  const store = {};
  Object.defineProperty(w, 'localStorage', {
    value: {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: (k) => { delete store[k]; },
    },
    configurable: true,
  });
  w.speechSynthesis = { cancel() {}, speak() { w.__spoke = (w.__spoke || 0) + 1; } };
  w.SpeechSynthesisUtterance = function (t) { this.text = t; };
  w.webkitSpeechRecognition = function () { this.start = () => {}; this.stop = () => {}; };
  w.confirm = () => true;
  return dom;
}

/** Extract and execute the page's inline script, returning selected globals. */
function runInline(dom, page, exportNames) {
  const html = dom.serialize();
  // Pages carry more than one inline block (e.g. an early theme-restore
  // script plus the main one). Grabbing from the first <script> to the last
  // </script> would swallow the tags in between and fail to parse.
  const blocks = [];
  const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1] && m[1].trim()) blocks.push(m[1]);
  }
  if (!blocks.length) { fail(page, 'no inline <script> block found'); return null; }
  const js = blocks.join('\n;\n');
  try {
    return dom.window.eval(js + '\n;({' + exportNames.map(n => `${n}: typeof ${n} !== "undefined" ? ${n} : undefined`).join(',') + '})');
  } catch (e) {
    fail(page, 'threw while executing: ' + e.message);
    return null;
  }
}

// --------------------------------------------------------------- simulator
function testSimulator() {
  const page = 'simulator.html';
  const dom = makeDom(page, { url: 'https://example.com/simulator.html' });
  const api = runInline(dom, page, [
    'QA_DATA', 'pickQuestion', 'grade', 'localScore', 'speakQuestion',
    'startRecording', 'stopRecording', 'evaluateAnswer',
  ]);
  if (!api) return;

  for (const fn of ['pickQuestion', 'grade', 'localScore', 'speakQuestion',
                    'startRecording', 'stopRecording', 'evaluateAnswer']) {
    if (typeof api[fn] !== 'function') fail(page, `${fn}() is missing after load`);
  }
  if (!Array.isArray(api.QA_DATA) || api.QA_DATA.length === 0) {
    fail(page, 'QA_DATA is empty or not an array');
    return;
  }
  const expected = readJson('data/questions.json').total_questions;
  if (api.QA_DATA.length !== expected) {
    fail(page, `QA_DATA has ${api.QA_DATA.length} records, data/questions.json says ${expected}`);
  }
  if (api.QA_DATA.some(r => !r.q || !r.a)) fail(page, 'some QA_DATA records have empty q or a');

  const d = dom.window.document;
  try {
    api.pickQuestion();
    if (!d.getElementById('questionText').textContent.trim()) {
      fail(page, 'pickQuestion() left the question text empty');
    } else {
      ok(page, `pickQuestion() renders (${api.QA_DATA.length} questions loaded)`);
    }
  } catch (e) { fail(page, 'pickQuestion() threw: ' + e.message); }

  try {
    const strong = api.localScore('continuous batching gpu slots free up sequence', 'Continuous batching lets requests join an in-flight batch as GPU slots free up, avoiding waiting on the longest sequence.');
    const weak = api.localScore('i think it is faster', 'Continuous batching lets requests join an in-flight batch as GPU slots free up, avoiding waiting on the longest sequence.');
    if (!(strong.pct > weak.pct)) fail(page, `localScore not discriminating (strong ${strong.pct}% vs weak ${weak.pct}%)`);
    else ok(page, `localScore discriminates (${strong.pct}% vs ${weak.pct}%)`);
  } catch (e) { fail(page, 'localScore threw: ' + e.message); }

  try { api.grade('got'); ok(page, 'grade() runs and persists'); }
  catch (e) { fail(page, 'grade() threw: ' + e.message); }

  try { api.startRecording(); api.stopRecording(); ok(page, 'voice recording toggles'); }
  catch (e) { fail(page, 'recording threw: ' + e.message); }
}

// ------------------------------------------------------------------- roles
function testRoles() {
  const page = 'roles.html';
  const dom = makeDom(page, { url: 'https://example.com/roles.html' });
  const api = runInline(dom, page, ['ROLES', 'render']);
  if (!api) return;

  if (!Array.isArray(api.ROLES) || !api.ROLES.length) { fail(page, 'ROLES is empty'); return; }
  const view = dom.window.document.getElementById('roleView');
  if (!view || view.innerHTML.length < 200) { fail(page, 'roleView did not render'); return; }
  if (!/Section \d+ —/.test(view.innerHTML)) fail(page, 'no sections rendered in role view');
  if (!/simulator\.html\?section=\d+/.test(view.innerHTML)) fail(page, 'practice deep links missing');

  const known = new Set(readJson('data/questions.json').questions.map(q => q.section));
  api.ROLES.forEach(r => {
    ['core', 'important', 'optional'].forEach(t => {
      (r.tiers[t] || []).forEach(s => {
        if (!s.count || s.count < 1) fail(page, `${r.id}/${t}: section ${s.num} has no questions`);
      });
    });
    if (!r.requiredQuestions) fail(page, `${r.id}: requiredQuestions is 0`);
  });
  ok(page, `${api.ROLES.length} roles render with valid section data`);
}

// -------------------------------------------------- questions hover script
function testHoverAnswers() {
  const page = 'questions.md + question-answers.js';
  const qjson = readJson('data/questions.json');
  const ajson = readJson('data/answers.json');
  const script = fs.readFileSync(path.join(REPO, 'assets/js/question-answers.js'), 'utf8');

  // Rebuild kramdown-shaped output: <ol> restarts at 1, which the script must
  // not depend on.
  const bySec = {}; const order = [];
  qjson.questions.forEach(q => {
    if (!bySec[q.section]) { bySec[q.section] = []; order.push(q.section); }
    bySec[q.section].push(q);
  });
  let body = '';
  order.slice(0, 3).forEach(sec => {
    body += `<h2>${sec}</h2><ol>`;
    bySec[sec].forEach(q => { body += `<li>${q.question.replace(/</g, '&lt;')}</li>`; });
    body += '</ol>';
  });

  const dom = new JSDOM(`<!doctype html><html><head></head><body>${body}</body></html>`,
    { url: 'https://example.com/questions.html', runScripts: 'outside-only', pretendToBeVisual: true });
  dom.window.matchMedia = () => ({ matches: true });
  dom.window.fetch = (u) => Promise.resolve({
    ok: true, status: 200, json: async () => (String(u).includes('answers') ? ajson : qjson),
  });
  try { dom.window.eval(script); } catch (e) { fail(page, 'script threw: ' + e.message); return; }

  return new Promise(resolve => setTimeout(() => {
    const d = dom.window.document;
    const items = d.querySelectorAll('.qa-item');
    if (!items.length) { fail(page, 'no questions were bound for answer reveal'); return resolve(); }

    const secondList = d.querySelectorAll('h2')[1].nextElementSibling;
    const secondFirst = secondList.querySelector('li');
    const expectedSecond = bySec[order[1]][0].id;
    if (String(secondFirst.dataset.qnum) !== String(expectedSecond)) {
      fail(page, `section 2 first item mapped to Q${secondFirst.dataset.qnum}, expected Q${expectedSecond}`);
    }
    if (secondList.getAttribute('start') !== String(expectedSecond)) {
      fail(page, `ol start not corrected (got ${secondList.getAttribute('start')}, expected ${expectedSecond})`);
    }

    const first = items[0];
    first.querySelector('.qa-q').dispatchEvent(new dom.window.MouseEvent('mouseover', { bubbles: true }));
    setTimeout(() => {
      const tip = first.querySelector('.qa-tip');
      if (!tip) fail(page, 'hover did not produce an answer panel');
      else if (tip.textContent.length < 40) fail(page, 'answer panel is suspiciously empty');
      else ok(page, `${items.length} questions bound, hover reveals answers, numbering corrected`);
      resolve();
    }, 120);
  }, 200));
}

// -------------------------------------------------------------------- main
(async () => {
  testSimulator();
  testRoles();
  await testHoverAnswers();

  notes.forEach(n => console.log(n));
  if (failures.length) {
    console.log('');
    failures.forEach(f => console.log('FAIL  ' + f));
    console.log(`\n${failures.length} smoke test failure(s).`);
    process.exit(1);
  }
  console.log('\nAll smoke tests passed — every interactive page executes and works.');
})();
