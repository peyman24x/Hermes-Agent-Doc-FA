/* اسکریپت مشترک مرجع فارسی Hermes Agent */
(function () {
  'use strict';
  var ROOT = document.documentElement.dataset.root || '.';

  /* ── تم شب/روز ── */
  var themeBtn = document.getElementById('themeToggle');
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    if (themeBtn) themeBtn.textContent = (t === 'dark') ? '☀️ حالت روز' : '🌙 حالت شب';
    try { localStorage.setItem('hermes-doc-theme', t); } catch (e) { }
  }
  var saved = null;
  try { saved = localStorage.getItem('hermes-doc-theme'); } catch (e) { }
  if (!saved) saved = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
  applyTheme(saved);
  if (themeBtn) themeBtn.addEventListener('click', function () {
    applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  var printBtn = document.getElementById('printBtn');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });

  /* ── ساخت سایدبار از دادهٔ ناوبری ── */
  var sidebarEl = document.getElementById('sidebar');
  function pageUrl(p) { return ROOT + '/' + p; }
  function currentKey() {
    var path = location.pathname.split('#')[0].split('?')[0];
    return path.replace(/\/index\.html$/, '/').replace(/\.html$/, '').replace(/\/$/, '');
  }
  function linkKey(url) {
    try {
      var u = new URL(url, location.href);
      return u.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '').replace(/\/$/, '');
    } catch (e) { return url; }
  }

  if (sidebarEl && window.HERMES_NAV) {
    var isOpenStored = {};
    try { isOpenStored = JSON.parse(localStorage.getItem('hermes-nav-open') || '{}'); } catch (e) { }
    var cur = currentKey();
    var frag = document.createDocumentFragment();

    var homeLink = document.createElement('a');
    homeLink.href = ROOT + '/';
    homeLink.className = 'nav-home';
    homeLink.innerHTML = '🏠 <strong>صفحهٔ اصلی</strong>';
    homeLink.style.cssText = 'display:block;padding:.4rem .55rem;margin-bottom:.5rem;color:var(--accent);text-decoration:none;font-size:.87rem;border-radius:.45rem';
    frag.appendChild(homeLink);

    window.HERMES_NAV.forEach(function (group) {
      var g = document.createElement('div');
      g.className = 'nav-group';
      g.id = 'navg-' + group.id;

      var btn = document.createElement('button');
      btn.className = 'nav-cat';
      btn.innerHTML = '<span class="arrow">◀</span> ' + group.cat;
      g.appendChild(btn);

      var ul = document.createElement('ul');
      ul.className = 'nav-pages';
      var hasCurrent = false;
      group.pages.forEach(function (pg) {
        var li = document.createElement('li');
        if (pg.d) {
          var a = document.createElement('a');
          a.href = pageUrl(pg.p);
          a.innerHTML = '<span>' + pg.t + '</span><span class="badge-status done">آماده</span>';
          if (linkKey(a.href) === cur) { a.classList.add('active'); hasCurrent = true; }
          li.appendChild(a);
        } else {
          var s = document.createElement('span');
          s.className = 'pend';
          s.innerHTML = '<span>' + pg.t + '</span><span class="badge-status todo">به‌زودی</span>';
          li.appendChild(s);
        }
        ul.appendChild(li);
      });
      g.appendChild(ul);

      var open = (typeof isOpenStored[group.id] === 'boolean') ? isOpenStored[group.id] : false;
      if (hasCurrent) open = true;
      if (open) g.classList.add('open');

      btn.addEventListener('click', function () {
        g.classList.toggle('open');
        var store = {};
        try { store = JSON.parse(localStorage.getItem('hermes-nav-open') || '{}'); } catch (e) { }
        store[group.id] = g.classList.contains('open');
        try { localStorage.setItem('hermes-nav-open', JSON.stringify(store)); } catch (e) { }
      });
      frag.appendChild(g);
    });
    sidebarEl.appendChild(frag);
  }

  /* ── منوی موبایل ── */
  var navToggle = document.getElementById('navToggle');
  var overlay = document.getElementById('overlay');
  function closeNav() { document.body.classList.remove('nav-open'); }
  if (navToggle) navToggle.addEventListener('click', function () { document.body.classList.toggle('nav-open'); });
  if (overlay) overlay.addEventListener('click', closeNav);

  /* ── کپی کد ── */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus(); ta.select();
      try { document.execCommand('copy') ? resolve() : reject(new Error('copy failed')); }
      catch (err) { reject(err); }
      document.body.removeChild(ta);
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll('.codebox'), function (box) {
    var btn = box.querySelector('.copy-btn');
    var pre = box.querySelector('pre');
    if (!btn || !pre) return;
    btn.addEventListener('click', function () {
      copyText(pre.textContent).then(function () {
        btn.classList.add('ok'); btn.textContent = 'کپی شد ✓';
        setTimeout(function () { btn.classList.remove('ok'); btn.textContent = 'کپی'; }, 1800);
      }).catch(function () {
        btn.textContent = 'خطا!';
        setTimeout(function () { btn.textContent = 'کپی'; }, 1800);
      });
    });
  });

  /* ── کپی آدرس‌های دونیت ── */
  Array.prototype.forEach.call(document.querySelectorAll('.copy-addr'), function (btn) {
    var box = btn.parentElement;
    var addr = box.querySelector('.addr');
    if (!addr) return;
    btn.addEventListener('click', function () {
      copyText(addr.textContent.trim()).then(function () {
        btn.classList.add('ok'); btn.textContent = 'کپی شد ✓';
        setTimeout(function () { btn.classList.remove('ok'); btn.textContent = 'کپی'; }, 1800);
      }).catch(function () {
        btn.textContent = 'خطا!';
        setTimeout(function () { btn.textContent = 'کپی'; }, 1800);
      });
    });
  });

  /* ── بازگشت به بالا ── */
  var toTop = document.getElementById('toTop');
  if (toTop) {
    window.addEventListener('scroll', function () {
      toTop.classList.toggle('show', window.scrollY > 500);
    }, { passive: true });
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }
})();
