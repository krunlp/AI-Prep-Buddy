/*
 * question-answers.js — reveal the answer for a question on the question bank
 * page, on hover (pointer devices) or tap (touch devices).
 *
 * Design notes:
 *
 * - Question numbers are NOT read from the rendered list. Kramdown renumbers
 *   ordered lists, so the number shown for "Q1091" may render as "1". Instead
 *   the script maps list items to question numbers by DOCUMENT ORDER within
 *   each section, using data/questions.json (generated in the same order).
 *   As a side effect it also corrects the visible numbering.
 *
 * - Answers are fetched lazily on first interaction, not on page load, so the
 *   bank stays fast to open on a phone.
 *
 * - Touch devices get tap-to-toggle inline panels; hover does not exist there.
 */
(function () {
  'use strict';

  var QUESTIONS_URL = 'data/questions.json';
  var ANSWERS_URL = 'data/answers.json';
  var MAX_CHARS = 900;

  var answers = null;
  var loading = null;
  var tip = null;
  var activeItem = null;
  var canHover = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var debug = { items: 0, bound: 0, byText: 0, byOrder: 0, reason: null };

  // ---------------------------------------------------------------- styling
  function injectStyles() {
    var css = [
      '.qa-item { position: relative; }',
      '.qa-item.qa-ready { cursor: help; }',
      '.qa-item.qa-ready:hover > .qa-q, .qa-item.qa-open > .qa-q { text-decoration: underline dotted; text-underline-offset: 3px; }',
      '.qa-badge { display: inline-block; margin-left: 6px; font-size: .72em; opacity: .5; vertical-align: middle; }',
      '.qa-tip { position: absolute; z-index: 9999; max-width: min(560px, 92vw); padding: 12px 14px;',
      '  border-radius: 10px; font-size: .88rem; line-height: 1.55; white-space: pre-wrap;',
      '  background: #171a23; color: #e8eaed; border: 1px solid rgba(255,255,255,.16);',
      '  box-shadow: 0 10px 32px rgba(0,0,0,.45); }',
      '.qa-tip .qa-tip-head { font-size: .72rem; text-transform: uppercase; letter-spacing: .5px;',
      '  opacity: .6; margin-bottom: 6px; }',
      '.qa-tip .qa-tip-more { display: block; margin-top: 9px; font-size: .8rem; opacity: .85; }',
      '.qa-inline { margin: 8px 0 4px; padding: 11px 13px; border-radius: 9px; font-size: .9em;',
      '  line-height: 1.55; white-space: pre-wrap; background: rgba(99,102,241,.07);',
      '  border: 1px solid rgba(99,102,241,.28); }',
      '.qa-inline .qa-tip-more { display: block; margin-top: 8px; font-size: .82em; }',
      '.qa-loading { opacity: .6; font-style: italic; }'
    ].join('\n');
    var el = document.createElement('style');
    el.textContent = css;
    document.head.appendChild(el);
  }

  // ------------------------------------------------------------- data layer
  function fetchJson(url) {
    return fetch(url, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function loadAnswers() {
    if (answers) return Promise.resolve(answers);
    if (loading) return loading;
    loading = fetchJson(ANSWERS_URL).then(function (data) {
      answers = data && data.answers ? data.answers : data;
      return answers;
    });
    return loading;
  }

  function truncate(text) {
    if (text.length <= MAX_CHARS) return text;
    var cut = text.lastIndexOf(' ', MAX_CHARS);
    return text.slice(0, cut > 0 ? cut : MAX_CHARS) + '…';
  }

  // ------------------------------------------------------------------- bind
  // Matching is done on QUESTION TEXT, not on DOM structure. The bank is not
  // uniform: early sections are tight lists (no blank lines), later sections
  // are loose lists, and sections 43+ have a bold title line plus a
  // description continuation. Any structural assumption breaks on one of them.
  // Text matching survives all three. Document order is only a fallback.
  function normText(s) {
    return String(s || '')
      .replace(/\u2b50/g, ' ')            // difficulty stars
      .replace(/[*`_]/g, ' ')             // markdown syntax kept in the JSON
      .replace(/[\u2010-\u2015]/g, '-')  // dash variants
      .replace(/[\u2018\u2019]/g, "'")
      .replace(/[\u201c\u201d]/g, '"')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
  }

  function bindItems(index) {
    var exact = Object.create(null);
    var prefix = Object.create(null);
    var bySection = {};
    index.forEach(function (q) {
      var n = normText(q.question);
      if (!n) return;
      exact[n] = q.id;
      var pre = n.slice(0, 60);
      if (prefix[pre] === undefined) prefix[pre] = q.id;
      else prefix[pre] = -1;             // ambiguous, don't use
      (bySection[q.section] = bySection[q.section] || []).push(q.id);
    });

    var items = Array.prototype.slice.call(document.querySelectorAll('li'));
    if (!items.length) {
      debug.reason = 'no <li> elements found on the page';
      return 0;
    }

    var bound = 0, matchedByText = 0;
    var unmatched = [];
    items.forEach(function (li) {
      if (li.closest('nav') || li.closest('.site-nav')) return;
      var t = normText(li.textContent);
      if (!t) return;
      var id = exact[t];
      if (id === undefined) {
        var p = prefix[t.slice(0, 60)];
        if (p !== undefined && p !== -1) id = p;
      }
      if (id === undefined) { unmatched.push(li); return; }
      attach(li, id);
      matchedByText++;
      bound++;
    });

    // Fallback for anything text matching missed: map the still-unbound items
    // to the remaining question numbers of their section, in document order.
    if (unmatched.length) {
      var used = Object.create(null);
      items.forEach(function (li) { if (li.dataset.qnum) used[li.dataset.qnum] = 1; });
      var headings = Array.prototype.filter.call(document.querySelectorAll('h2'),
        function (h) { return /^Section\s+\d+/.test((h.textContent || '').trim()); });
      unmatched.forEach(function (li) {
        var h = null, node = li;
        while (node) {
          if (node.previousElementSibling) node = node.previousElementSibling;
          else node = node.parentElement;
          if (!node) break;
          if (node.tagName === 'H2' && headings.indexOf(node) !== -1) { h = node; break; }
        }
        if (!h) return;
        var htext = (h.textContent || '').replace(/\s*\(\d+[\u2013-]\d+\)\s*$/, '').trim();
        var key = Object.keys(bySection).find(function (s) {
          return htext.indexOf(s.trim()) === 0 || s.trim().indexOf(htext) === 0;
        });
        if (!key) return;
        var free = bySection[key].filter(function (n) { return !used[n]; });
        if (!free.length) return;
        var id = free[0];
        used[id] = 1;
        attach(li, id);
        bound++;
      });
    }

    debug.items = items.length;
    debug.bound = bound;
    debug.byText = matchedByText;
    debug.byOrder = bound - matchedByText;
    if (!bound) debug.reason = 'no list item text matched any question';
    return bound;
  }

  function attach(li, num) {
    if (li.dataset.qnum) return;
    li.classList.add('qa-item', 'qa-ready');
    li.dataset.qnum = String(num);
    li.setAttribute('tabindex', '0');
    li.setAttribute('aria-label', 'Question ' + num + '. Reveal answer.');
    var span = document.createElement('span');
    span.className = 'qa-q';
    while (li.firstChild) span.appendChild(li.firstChild);
    li.appendChild(span);
    var badge = document.createElement('span');
    badge.className = 'qa-badge';
    badge.textContent = canHover ? '\u00b7 hover for answer' : '\u00b7 tap for answer';
    li.appendChild(badge);
  }

  // ------------------------------------------------------------------- view
  function answerFor(num) {
    var a = answers && answers[num];
    return a ? String(a) : null;
  }

  function moreLink() {
    var a = document.createElement('a');
    a.className = 'qa-tip-more';
    a.href = 'answers.html';
    a.textContent = 'Read the full answer →';
    return a;
  }

  function showTip(li) {
    hideTip();
    var num = li.dataset.qnum;
    tip = document.createElement('div');
    tip.className = 'qa-tip';
    var head = document.createElement('div');
    head.className = 'qa-tip-head';
    head.textContent = 'Answer · Q' + num;
    tip.appendChild(head);
    var body = document.createElement('div');
    var text = answerFor(num);
    if (text) {
      body.textContent = truncate(text);
    } else {
      body.className = 'qa-loading';
      body.textContent = 'Loading…';
    }
    tip.appendChild(body);
    if (text) tip.appendChild(moreLink());
    li.appendChild(tip);
    position(li, tip);
    activeItem = li;

    if (!text) {
      loadAnswers().then(function () {
        if (activeItem !== li || !tip) return;
        var t = answerFor(num);
        body.className = '';
        body.textContent = t || 'No answer found for this question.';
        if (t) tip.appendChild(moreLink());
        position(li, tip);
      }).catch(function () {
        if (activeItem !== li || !tip) return;
        body.className = '';
        body.textContent = 'Could not load answers.';
      });
    }
  }

  function position(li, node) {
    node.style.left = '0px';
    node.style.top = (li.offsetHeight + 6) + 'px';
    var rect = node.getBoundingClientRect();
    if (rect.right > window.innerWidth - 8) {
      node.style.left = Math.min(0, window.innerWidth - 8 - rect.right) + 'px';
    }
    if (rect.bottom > window.innerHeight - 8 && rect.height < li.getBoundingClientRect().top) {
      node.style.top = (-rect.height - 6) + 'px';
    }
  }

  function hideTip() {
    if (tip && tip.parentNode) tip.parentNode.removeChild(tip);
    tip = null;
    activeItem = null;
  }

  function toggleInline(li) {
    var existing = li.querySelector(':scope > .qa-inline');
    if (existing) {
      existing.parentNode.removeChild(existing);
      li.classList.remove('qa-open');
      return;
    }
    var num = li.dataset.qnum;
    var panel = document.createElement('div');
    panel.className = 'qa-inline';
    var text = answerFor(num);
    panel.textContent = text ? truncate(text) : 'Loading…';
    if (!text) panel.classList.add('qa-loading');
    li.appendChild(panel);
    li.classList.add('qa-open');
    if (text) panel.appendChild(moreLink());
    else {
      loadAnswers().then(function () {
        var t = answerFor(num);
        panel.classList.remove('qa-loading');
        panel.textContent = t || 'No answer found for this question.';
        if (t) panel.appendChild(moreLink());
      }).catch(function () {
        panel.classList.remove('qa-loading');
        panel.textContent = 'Could not load answers.';
      });
    }
  }

  function wireEvents() {
    if (canHover) {
      document.addEventListener('mouseover', function (e) {
        var li = e.target.closest && e.target.closest('.qa-item');
        if (!li || li === activeItem) return;
        showTip(li);
      });
      document.addEventListener('mouseout', function (e) {
        var li = e.target.closest && e.target.closest('.qa-item');
        if (!li) return;
        if (e.relatedTarget && li.contains(e.relatedTarget)) return;
        hideTip();
      });
      // Prefetch once the pointer enters the list, so the first hover is instant.
      document.addEventListener('mouseover', function once(e) {
        if (e.target.closest && e.target.closest('.qa-item')) {
          loadAnswers().catch(function () {});
          document.removeEventListener('mouseover', once);
        }
      });
    }

    // Tap / click / keyboard works on every device, including hover-capable
    // ones, so a touchscreen laptop is not left without a way in.
    document.addEventListener('click', function (e) {
      var li = e.target.closest && e.target.closest('.qa-item');
      if (!li) return;
      if (e.target.tagName === 'A') return;
      if (canHover) return; // hover already handles pointer devices
      e.preventDefault();
      toggleInline(li);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var li = document.activeElement;
      if (!li || !li.classList || !li.classList.contains('qa-item')) return;
      e.preventDefault();
      toggleInline(li);
    });
    window.addEventListener('scroll', function () { if (canHover) hideTip(); }, { passive: true });
  }

  // Append ?qadebug=1 to the URL to see why binding did or did not happen.
  function showDebug() {
    var d = document.createElement('div');
    d.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:99999;padding:10px 14px;' +
      'background:#111;color:#0f0;font:12px/1.5 monospace;border-top:2px solid #0f0';
    d.textContent = 'qa-debug · list items: ' + debug.items + ' · bound: ' + debug.bound +
      ' (text ' + debug.byText + ', order ' + debug.byOrder + ')' +
      (debug.reason ? ' · ' + debug.reason : '');
    document.body.appendChild(d);
  }

  function init() {
    if (!document.querySelector('h2')) return;
    fetchJson(QUESTIONS_URL).then(function (data) {
      var index = data && data.questions ? data.questions : data;
      if (!Array.isArray(index) || !index.length) return;
      injectStyles();
      var n = bindItems(index);
      if (n > 0) wireEvents();
      window.__qaDebug = debug;
      if (/[?&]qadebug=1/.test(window.location.search)) showDebug();
    }).catch(function (err) {
      debug.reason = 'could not load data/questions.json: ' + (err && err.message);
      window.__qaDebug = debug;
      if (/[?&]qadebug=1/.test(window.location.search)) showDebug();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
