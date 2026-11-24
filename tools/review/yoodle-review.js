/* Yoodle review mode. Drop-in feedback tool for sites under review on Netlify.
   Tap Review, tap anything on the page, talk or type, save. Notes land in the site's
   Netlify form "yoodle-review". Include before </body>:
   <script src="/yoodle-review.js" data-project="Client name"></script>
   and deploy yoodle-review-form.html at the site root so Netlify registers the form. */
(function () {
  'use strict';
  if (window.__yoodleReview) return; window.__yoodleReview = true;
  var script = document.currentScript || {};
  // Only runs on Netlify preview hosts and local builds, so it can never show on a live domain.
  // Override with data-always="true" on the script tag, or add ?yoodle-review=on to the URL once per browser session.
  try { if (/yoodle-review=on/.test(location.search)) sessionStorage.setItem('yoodle-review', 'on'); } catch (e) {}
  var allowed = /\.netlify\.app$|^localhost$|^127\./.test(location.hostname) || (script.dataset && script.dataset.always === 'true');
  try { allowed = allowed || sessionStorage.getItem('yoodle-review') === 'on'; } catch (e) {}
  if (!allowed) return;
  var PROJECT = (script.dataset && script.dataset.project) || document.title || location.host;
  var FORM = (script.dataset && script.dataset.form) || 'yoodle-review';
  var KEY = 'yr:' + location.host;
  // data-round on the script tag starts a fresh review round: pins and numbering reset for everyone; the reviewer's name is kept.
  var ROUND = (script.dataset && script.dataset.round) || '';
  var store = function (k, v) { var key = KEY + (ROUND && k !== 'name' ? ':r' + ROUND : '') + ':' + k; try { if (v === undefined) return JSON.parse(localStorage.getItem(key) || 'null'); localStorage.setItem(key, JSON.stringify(v)); } catch (e) { return null; } };
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  var css = '\
.yr-ui{font:500 15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:#111;box-sizing:border-box}.yr-ui *{box-sizing:border-box}\
.yr-fab{position:fixed;right:16px;bottom:calc(16px + var(--yr-offset,0px));z-index:2147483000;display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 18px;border:0;border-radius:999px;background:#111;color:#fff;font:600 15px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.35);cursor:pointer}\
.yr-fab.on{background:#C8102E}.yr-fab .yr-n{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;padding:0 6px;border-radius:999px;background:#fff;color:#111;font-size:12px}\
.yr-on *{cursor:crosshair!important}.yr-hover{outline:2px dashed #C8102E!important;outline-offset:2px!important}.yr-sel{outline:3px solid #C8102E!important;outline-offset:3px!important}\
.yr-pin{position:absolute;z-index:2147482000;display:flex;align-items:center;justify-content:center;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:999px;background:#C8102E;color:#fff;font:700 13px/1 -apple-system,Helvetica,Arial,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.4);pointer-events:none}\
.yr-pop{position:fixed;z-index:2147483001;width:min(380px,calc(100vw - 24px));padding:14px;border-radius:14px;background:#fff;color:#111;box-shadow:0 12px 40px rgba(0,0,0,.35)}\
.yr-pop .yr-what{font-size:13px;color:#555;margin:0 0 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\
.yr-pop textarea{width:100%;min-height:96px;padding:10px;border:1px solid #bbb;border-radius:10px;font:inherit;resize:vertical}\
.yr-pop input{width:100%;padding:10px;border:1px solid #bbb;border-radius:10px;font:inherit;margin-top:8px}\
.yr-row{display:flex;gap:8px;align-items:center;margin-top:10px}.yr-row .yr-sp{flex:1}\
.yr-photo{display:flex;align-items:center;gap:10px;margin-top:8px;font-size:13px;color:#555}.yr-photo img{width:44px;height:44px;object-fit:cover;border-radius:8px}.yr-photo .yr-btn{min-height:40px;padding:0 12px;font-size:13px}.yr-photo input[type=file]{display:none}.yr-photo .yr-x{min-height:32px;padding:0 10px;border-color:#bbb;font-size:12px}\
.yr-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:44px;padding:0 16px;border:1px solid #111;border-radius:999px;background:#fff;color:#111;font:600 14px/1 inherit;cursor:pointer}\
.yr-btn.yr-pri{background:#111;color:#fff}.yr-btn.yr-mic.on{background:#C8102E;border-color:#C8102E;color:#fff;animation:yrpulse 1s infinite}\
@keyframes yrpulse{50%{box-shadow:0 0 0 8px rgba(200,16,46,.25)}}\
.yr-toast{position:fixed;left:50%;bottom:calc(76px + var(--yr-offset,0px));z-index:2147483002;transform:translateX(-50%);padding:10px 16px;border-radius:999px;background:#111;color:#fff;font-size:14px;box-shadow:0 6px 24px rgba(0,0,0,.35)}\
@media (max-width:600px){.yr-pop{left:12px!important;right:12px!important;top:auto!important;bottom:calc(76px + var(--yr-offset,0px))!important;width:auto}}';
  var style = document.createElement('style'); style.textContent = css; document.head.appendChild(style);

  // Sit above a fixed bottom bar (the Yoodle option switcher) if there is one.
  function offset() {
    var h = 0;
    document.querySelectorAll('body *').forEach(function (n) {
      if (n.closest('.yr-ui')) return;
      var cs = getComputedStyle(n); if (cs.position !== 'fixed' && cs.position !== 'sticky') return;
      var r = n.getBoundingClientRect(); if (r.height > 0 && r.height < 160 && r.bottom >= window.innerHeight - 2 && r.width > window.innerWidth / 2) h = Math.max(h, r.height);
    });
    document.documentElement.style.setProperty('--yr-offset', h + 'px');
  }
  offset(); window.addEventListener('resize', offset);

  var notes = store('notes:' + location.pathname) || [];
  // Note numbers keep counting up per page even after resolved pins are cleared, so numbers never repeat.
  var count = store('count:' + location.pathname) || notes.reduce(function (m, n) { return Math.max(m, +n.n || 0); }, 0);
  var queue = store('queue') || [];
  var fab = el('button', 'yr-ui yr-fab', '<span>Review</span><span class="yr-n">' + notes.length + '</span>');
  fab.type = 'button'; fab.title = 'Tap, then tap anything on the page to leave a note'; document.body.appendChild(fab);
  var on = false, hover = null, sel = null, pop = null, rec = null;

  fab.addEventListener('click', function () { on ? off() : start(); });
  function start() { on = true; fab.classList.add('on'); fab.firstChild.textContent = 'Tap something'; document.documentElement.classList.add('yr-on'); toast('Review on. Tap any part of the page.'); }
  function off() { on = false; fab.classList.remove('on'); fab.firstChild.textContent = 'Review'; document.documentElement.classList.remove('yr-on'); clearHover(); closePop(); }

  document.addEventListener('mouseover', function (e) { if (!on || inUI(e.target) || pop) return; clearHover(); hover = e.target; hover.classList.add('yr-hover'); }, true);
  function clearHover() { if (hover) hover.classList.remove('yr-hover'); hover = null; }
  document.addEventListener('click', function (e) {
    if (!on || inUI(e.target)) return;
    e.preventDefault(); e.stopPropagation();
    if (pop) return;
    clearHover(); sel = e.target; sel.classList.add('yr-sel');
    openPop(sel, e.clientX, e.clientY);
  }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && pop) closePop(); });
  function inUI(t) { return !!(t.closest && t.closest('.yr-ui')); }

  function openPop(target, x, y) {
    var name = store('name') || '';
    pop = el('div', 'yr-ui yr-pop',
      '<p class="yr-what">' + esc(describe(target)) + '</p>' +
      '<textarea placeholder="What should change here?" aria-label="Your note"></textarea>' +
      (name ? '' : '<input placeholder="Your name (once)" aria-label="Your name">') +
      '<div class="yr-photo"><button type="button" class="yr-btn yr-add">&#128247; Add a photo</button><input type="file" accept="image/*"><span class="yr-pname"></span></div>' +
      '<div class="yr-row">' + (SR ? '<button type="button" class="yr-btn yr-mic">&#9679; Talk</button>' : '') + '<span class="yr-sp"></span>' +
      '<button type="button" class="yr-btn yr-cancel">Cancel</button><button type="button" class="yr-btn yr-pri yr-save">Save</button></div>');
    document.body.appendChild(pop);
    var ta = pop.querySelector('textarea'), photo = null;
    var fin = pop.querySelector('input[type=file]'), pname = pop.querySelector('.yr-pname'), prow = pop.querySelector('.yr-photo');
    pop.querySelector('.yr-add').addEventListener('click', function () { fin.click(); });
    fin.addEventListener('change', function () {
      var f = fin.files && fin.files[0]; if (!f) return;
      shrink(f).then(function (out) {
        photo = out; pname.innerHTML = ''; var im = document.createElement('img'); im.src = URL.createObjectURL(out); im.alt = '';
        var x = el('button', 'yr-btn yr-x', 'Remove'); x.type = 'button'; x.addEventListener('click', function () { photo = null; fin.value = ''; pname.innerHTML = ''; });
        pname.appendChild(im); pname.appendChild(document.createTextNode(' ' + out.name + ' (' + Math.round(out.size / 1024) + ' KB) ')); pname.appendChild(x);
        position(pop, x0, y0);
      }, function () { toast('That file could not be read. Try a JPG, PNG or HEIC photo.'); });
    });
    var x0 = x, y0 = y;
    position(pop, x, y);
    pop.querySelector('.yr-cancel').addEventListener('click', closePop);
    pop.querySelector('.yr-save').addEventListener('click', function () {
      var text = ta.value.trim(); if (!text) { ta.focus(); return; }
      var inp = pop.querySelector('input:not([type=file])');
      if (inp) { if (!inp.value.trim()) { inp.focus(); toast('Add your name once so we know whose note this is.'); return; } store('name', inp.value.trim()); }
      save(target, text, photo); closePop();
    });
    var mic = pop.querySelector('.yr-mic');
    if (mic) mic.addEventListener('click', function () { rec ? stopRec() : startRec(ta, mic); });
    if (SR) startRec(ta, mic); else ta.focus();
  }
  function closePop() { stopRec(); if (pop) pop.remove(); pop = null; if (sel) sel.classList.remove('yr-sel'); sel = null; }
  function position(p, x, y) {
    if (window.innerWidth <= 600) return;
    var w = p.offsetWidth, h = p.offsetHeight;
    var left = Math.min(Math.max(12, x + 12), window.innerWidth - w - 12);
    var top = y + 12 + h > window.innerHeight - 12 ? Math.max(12, y - h - 12) : y + 12;
    p.style.left = left + 'px'; p.style.top = top + 'px';
  }

  function startRec(ta, mic) {
    if (!SR) return;
    try {
      rec = new SR(); rec.continuous = true; rec.interimResults = true; rec.lang = 'en-US';
      var base = ta.value ? ta.value.replace(/\s+$/, '') + ' ' : '';
      rec.onresult = function (ev) {
        var fin = '', interim = '';
        for (var i = 0; i < ev.results.length; i++) { var r = ev.results[i]; if (r.isFinal) fin += r[0].transcript + ' '; else interim += r[0].transcript; }
        ta.value = base + fin + interim;
      };
      rec.onend = function () { if (rec) { rec = null; if (mic) { mic.classList.remove('on'); mic.innerHTML = '&#9679; Talk'; } } };
      rec.onerror = function (ev) { if (ev.error === 'not-allowed') toast('Microphone blocked. Type instead, or allow the mic in the address bar.'); };
      rec.start(); if (mic) { mic.classList.add('on'); mic.textContent = 'Listening… tap to stop'; }
    } catch (e) { rec = null; ta.focus(); }
  }
  function stopRec() { if (rec) { var r = rec; rec = null; try { r.stop(); } catch (e) {} } var m = pop && pop.querySelector('.yr-mic'); if (m) { m.classList.remove('on'); m.innerHTML = '&#9679; Talk'; } }

  function save(target, text, photo) {
    var r = target.getBoundingClientRect();
    var note = {
      'form-name': FORM, project: PROJECT, page: location.pathname, url: location.href,
      number: String(count + 1), reviewer: store('name') || 'Unknown',
      element: selector(target), what: describe(target), section: section(target),
      note: text, viewport: window.innerWidth + 'x' + window.innerHeight,
      position: Math.round(window.scrollX + r.left) + ',' + Math.round(window.scrollY + r.top),
      device: /Mobi|Android|iPhone|iPad/.test(navigator.userAgent) ? 'phone' : 'desktop',
      created: new Date().toISOString()
    };
    count++; store('count:' + location.pathname, count);
    notes.push({ n: note.number, c: note.created, x: window.scrollX + r.left, y: window.scrollY + r.top, el: note.element }); store('notes:' + location.pathname, notes);
    fab.querySelector('.yr-n').textContent = notes.length; drawPin(notes[notes.length - 1]);
    if (photo) note.photo_name = photo.name;
    send(note, photo).then(function () { toast('Saved note ' + note.number + (photo ? ' with photo' : '')); }, function () {
      if (photo) { toast('Note ' + note.number + ' saved, but the photo did not upload. Try again with a smaller image.'); send(note).catch(function () { queue.push(note); store('queue', queue); }); }
      else { queue.push(note); store('queue', queue); toast('Saved note ' + note.number + ' (will send when online)'); }
    });
  }
  function send(note, photo) {
    var opts = { method: 'POST' };
    if (photo) { var fd = new FormData(); Object.keys(note).forEach(function (k) { fd.append(k, note[k]); }); fd.append('photo', photo, photo.name); opts.body = fd; }
    else { opts.headers = { 'Content-Type': 'application/x-www-form-urlencoded' }; opts.body = new URLSearchParams(note).toString(); }
    return fetch('/', opts).then(function (res) { if (!res.ok) throw new Error(res.status); });
  }
  // Netlify accepts uploads up to 8 MB. Phone photos are often bigger, so anything over 6 MB or 2400px is resized (site images are 1600px at most).
  function shrink(file) {
    return new Promise(function (resolve, reject) {
      if (file.size <= 6 * 1024 * 1024 && !/heic|heif/i.test(file.type + file.name)) { var img0 = new Image(); img0.onload = function () { if (img0.naturalWidth <= 2400 && img0.naturalHeight <= 2400) resolve(file); else draw(img0); }; img0.onerror = function () { resolve(file); }; img0.src = URL.createObjectURL(file); return; }
      var img = new Image(); img.onload = function () { draw(img); }; img.onerror = reject; img.src = URL.createObjectURL(file);
      function draw(im) {
        var k = Math.min(1, 2400 / Math.max(im.naturalWidth, im.naturalHeight)), c = document.createElement('canvas');
        c.width = Math.round(im.naturalWidth * k); c.height = Math.round(im.naturalHeight * k);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height);
        c.toBlob(function (b) { if (!b) return reject(); b.name = file.name.replace(/\.[^.]+$/, '') + '.jpg'; resolve(b); }, 'image/jpeg', 0.9);
      }
    });
  }
  (function flush() { if (!queue.length) return; var q = queue.slice(); queue = []; store('queue', queue); q.forEach(function (n) { send(n).catch(function () { queue.push(n); store('queue', queue); }); }); })();

  function drawPin(n) { var p = el('div', 'yr-ui yr-pin', n.n); p.setAttribute('data-yr-pin', n.n); p.style.left = n.x + 'px'; p.style.top = n.y + 'px'; document.body.appendChild(p); }
  notes.forEach(function (n) { var t = null; try { t = document.querySelector(n.el); } catch (e) {} if (t) { var r = t.getBoundingClientRect(); n.x = window.scrollX + r.left; n.y = window.scrollY + r.top; } drawPin(n); });
  // Two ways pins clear: data-round on the script tag wipes every pin for everyone (a new review round), and
  // Resolved notes: /yoodle-resolved.json lists notes that have been handled ([{page, number, created}]).
  // Their pins are removed from this browser, so only open notes stay on the page.
  fetch('/yoodle-resolved.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : []; }).then(function (done) {
    if (!done || !done.length) return;
    var gone = 0;
    notes = notes.filter(function (n) {
      var hit = done.some(function (d) { return n.c ? d.created === n.c : (d.page === location.pathname && String(d.number) === String(n.n)); });  // timestamp when the pin has one; page + number only for older pins
      if (hit) { gone++; var p = document.querySelector('[data-yr-pin="' + n.n + '"]'); if (p) p.remove(); }
      return !hit;
    });
    if (gone) { store('notes:' + location.pathname, notes); fab.querySelector('.yr-n').textContent = notes.length; toast(gone + (gone === 1 ? ' note' : ' notes') + ' resolved'); }
  }).catch(function () {});

  function describe(t) {
    var tag = t.tagName.toLowerCase(), role = { a: 'Link', button: 'Button', img: 'Image', h1: 'Heading', h2: 'Heading', h3: 'Heading', p: 'Text', li: 'List item', input: 'Field', select: 'Field', textarea: 'Field' }[tag] || tag;
    var txt = tag === 'img' ? (t.alt || t.src.split('/').pop()) : (t.innerText || t.textContent || '').trim().replace(/\s+/g, ' ');
    if (!txt) { var im = t.querySelector && t.querySelector('img'); if (im) { role = 'Image'; txt = im.alt || im.src.split('/').pop(); } else { var bg = getComputedStyle(t).backgroundImage; if (bg && bg !== 'none') { role = 'Image'; txt = (bg.match(/[^/]+(?=["')]*\)$)/) || [''])[0]; } } }
    return role + ': ' + (txt ? '“' + txt.slice(0, 70) + (txt.length > 70 ? '…' : '') + '”' : '(no text)');
  }
  function section(t) {
    var s = t.closest('[aria-labelledby], [aria-label], section, article, header, footer, main, nav, aside'); if (!s) return '';
    var lb = s.getAttribute('aria-labelledby'), lbEl = lb && document.getElementById(lb.split(' ')[0]);
    var h = lbEl || s.querySelector('h1, h2, h3'); var label = s.getAttribute('aria-label') || s.id || '';
    return ((h && h.textContent.trim().replace(/\s+/g, ' ').slice(0, 60)) || label || s.tagName.toLowerCase());
  }
  function selector(t) {
    var parts = [];
    while (t && t.nodeType === 1 && t !== document.body) {
      if (t.id && !/\d{5,}/.test(t.id)) { parts.unshift('#' + CSS.escape(t.id)); break; }
      var tag = t.tagName.toLowerCase(), i = 1, s = t;
      while ((s = s.previousElementSibling)) if (s.tagName === t.tagName) i++;
      parts.unshift(tag + ':nth-of-type(' + i + ')'); t = t.parentElement;
    }
    return parts.join(' > ');
  }
  var toastEl = null, toastT = null;
  function toast(msg) { if (!toastEl) { toastEl = el('div', 'yr-ui yr-toast', ''); document.body.appendChild(toastEl); } toastEl.textContent = msg; toastEl.style.display = ''; clearTimeout(toastT); toastT = setTimeout(function () { toastEl.style.display = 'none'; }, 2600); }
  function el(tag, cls, html) { var e = document.createElement(tag); e.className = cls; e.innerHTML = html; return e; }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
})();
