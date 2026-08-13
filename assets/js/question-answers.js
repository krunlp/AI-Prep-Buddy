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
  // Walk each section heading, collect the list items that follow it, and pair
  // them with that section's question numbers in order.
  function bindItems(index) {
    var bySection = {};
    var order = [];
    index.forEach(function (q) {
      if (!bySection[q.section]) { bySection[q.section] = []; order.push(q.section); }
      bySection[q.section].push(q.id);
    });

    var headings = Array.prototype.filter.call(
      document.querySelectorAll('h2'),
      function (h) { return /^Section\s+\d+/.test((h.textContent || '').trim()); }
    );

    var bound = 0;
    headings.forEach(function (h) {
      var text = (h.textContent || '').trim();
      var key = Object.keys(bySection).find(function (s) {
        return text.indexOf(s.replace(/\s*\(\d+[–-]\d+\)\s*$/, '').trim()) === 0 ||
               s.indexOf(text.replace(/\s*\(\d+[–-]\d+\)\s*$/, '').trim()) === 0;
      });
      if (!key) return;
      var nums = bySection[key];

      // Gather <li> elements between this heading and the next one.
      var items = [];
      var node = h.nextElementSibling;
      while (node && node.tagName !== 'H2') {
        if (node.tagName === 'OL' || node.tagName === 'UL') {
          Array.prototype.push.apply(items, node.querySelectorAll(':scope > li'));
        }
        node = node.nextElementSibling;
      }
      if (!items.length) return;

      // Correct the visible numbering, which kramdown restarts at 1.
      var firstList = items[0].parentElement;
      if (firstList && firstList.tagName === 'OL' && nums.length) {
        firstList.setAttribute('start', String(nums[0]));
      }

      items.forEach(function (li, i) {
        if (i >= nums.length) return;
        var num = nums[i];
        li.classList.add('qa-item', 'qa-ready');
        li.dataset.qnum = String(num);
        li.setAttribute('tabindex', '0');
        li.setAttribute('aria-label', 'Question ' + num + '. Reveal answer.');
        // Wrap existing content so hover underline targets only the question.
        var span = document.createElement('span');
        span.className = 'qa-q';
        while (li.firstChild) span.appendChild(li.firstChild);
        li.appendChild(span);
        var badge = document.createElement('span');
        badge.className = 'qa-badge';
        badge.textContent = canHover ? '· hover for answer' : '· tap for answer';
        li.appendChild(badge);
        bound++;
      });
    });
    return bound;
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

  function init() {
    if (!document.querySelector('h2')) return;
    fetchJson(QUESTIONS_URL).then(function (data) {
      var index = data && data.questions ? data.questions : data;
      if (!Array.isArray(index) || !index.length) return;
      injectStyles();
      if (bindItems(index) > 0) wireEvents();
    }).catch(function () {
      /* offline or opened via file:// — page still works, just without reveal */
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
