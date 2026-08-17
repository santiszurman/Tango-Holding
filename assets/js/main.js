/* Tango Holding — interacciones del sitio */
(function () {
  'use strict';

  /* ---------------- Menú desplegable ---------------- */
  var menuBtn = document.querySelector('.menu-btn');
  var navPanel = document.querySelector('.nav-panel');

  if (menuBtn && navPanel) {
    menuBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = navPanel.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navPanel.addEventListener('click', function () {
      navPanel.classList.remove('open');
      menuBtn.setAttribute('aria-expanded', 'false');
    });
  }

  /* ---------------- Selector de idioma ---------------- */
  var lang = document.querySelector('.lang');
  var langBtn = document.querySelector('.lang-btn');

  if (lang && langBtn) {
    langBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = lang.classList.toggle('open');
      langBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  document.addEventListener('click', function () {
    if (navPanel) { navPanel.classList.remove('open'); }
    if (menuBtn) { menuBtn.setAttribute('aria-expanded', 'false'); }
    if (lang) { lang.classList.remove('open'); }
    if (langBtn) { langBtn.setAttribute('aria-expanded', 'false'); }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') { return; }
    if (navPanel) { navPanel.classList.remove('open'); }
    if (lang) { lang.classList.remove('open'); }
  });

  /* ---------------- Slideshow del hero ---------------- */
  var slides = [].slice.call(document.querySelectorAll('.hero-slide'));
  var copies = [].slice.call(document.querySelectorAll('.hero-copy .slide-copy'));
  var dots = [].slice.call(document.querySelectorAll('.hero-dots button'));
  var current = 0;
  var timer = null;
  var DELAY = 5000;

  var zTop = 1;

  function show(i, instant) {
    current = (i + slides.length) % slides.length;
    // La foto entrante se apila ARRIBA de todo y aparece con un fundido; la
    // anterior nunca se desvanece, se queda opaca abajo. Así el fondo nunca
    // llega a verse y no hay parpadeo negro.
    var slide = slides[current];
    if (slide) {
      zTop += 1;
      slide.style.transition = 'none';
      slide.classList.remove('shown');
      slide.style.zIndex = zTop;
      void slide.offsetHeight;                 // fuerza el recálculo
      if (!instant) { slide.style.transition = ''; }
      slide.classList.add('shown');
      if (instant) { void slide.offsetHeight; slide.style.transition = ''; }
    }
    copies.forEach(function (s, n) { s.classList.toggle('active', n === current); });
    dots.forEach(function (d, n) {
      d.classList.toggle('active', n === current);
      d.setAttribute('aria-selected', n === current ? 'true' : 'false');
    });
  }

  function play() {
    stop();
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }
    timer = setInterval(function () { show(current + 1); }, DELAY);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }

  var slidesBox = document.querySelector('.hero-slides');
  if (slidesBox) { slidesBox.classList.add('js'); }

  if (slides.length) {
    dots.forEach(function (d, n) {
      d.addEventListener('click', function () { show(n); play(); });
    });
    show(0, true);
    play();
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stop(); } else { play(); }
    });
  }

  /* ---------------- Galería de proyectos ---------------- */
  var gallery = document.querySelector('.gallery');
  var prev = document.querySelector('.gal-arrow.prev');
  var next = document.querySelector('.gal-arrow.next');

  function step() {
    var item = gallery && gallery.querySelector('.gallery-item');
    return item ? item.getBoundingClientRect().width + 12 : 380;
  }
  if (gallery && prev && next) {
    prev.addEventListener('click', function () {
      gallery.scrollBy({ left: -step() * 2, behavior: 'smooth' });
    });
    next.addEventListener('click', function () {
      gallery.scrollBy({ left: step() * 2, behavior: 'smooth' });
    });
  }

  /* ---------------- Puntos de navegación lateral ---------------- */
  var sections = [].slice.call(document.querySelectorAll('[data-section]'));
  var navDots = [].slice.call(document.querySelectorAll('.dots-nav button'));

  navDots.forEach(function (d, i) {
    d.addEventListener('click', function () {
      if (sections[i]) { sections[i].scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

  function syncDots() {
    var y = window.scrollY + window.innerHeight * 0.4;
    var active = 0;
    sections.forEach(function (s, i) { if (s.offsetTop <= y) { active = i; } });
    navDots.forEach(function (d, i) { d.classList.toggle('active', i === active); });
  }
  if (sections.length && navDots.length) {
    window.addEventListener('scroll', syncDots, { passive: true });
    syncDots();
  }

  /* ---------------- Formulario de contacto (Netlify Forms) ---------------- */
  var form = document.querySelector('.contact-form');

  if (form) {
    [].slice.call(form.querySelectorAll('input, textarea')).forEach(function (el) {
      var wrap = el.closest('.field');
      if (!wrap) { return; }
      var sync = function () { wrap.classList.toggle('filled', el.value.trim() !== ''); };
      el.addEventListener('input', sync);
      el.addEventListener('focus', function () { wrap.classList.add('filled'); });
      el.addEventListener('blur', sync);
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.form-msg');
      var btn = form.querySelector('.btn-send');
      var data = new URLSearchParams(new FormData(form)).toString();

      btn.disabled = true;
      msg.classList.remove('error');
      msg.textContent = '';

      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: data
      }).then(function (r) {
        if (!r.ok) { throw new Error(r.status); }
        form.reset();
        [].slice.call(form.querySelectorAll('.field')).forEach(function (f) {
          f.classList.remove('filled');
        });
        msg.textContent = form.getAttribute('data-thanks');
      }).catch(function () {
        msg.classList.add('error');
        msg.textContent = form.getAttribute('data-error');
      }).then(function () {
        btn.disabled = false;
      });
    });
  }

  /* ---------------- Ventana emergente de proyecto ---------------- */
  var lbData = null;
  var dataTag = document.getElementById('lb-data');
  if (dataTag) {
    try { lbData = JSON.parse(dataTag.textContent); } catch (e) { lbData = null; }
  }

  var overlay = document.querySelector('.lb-overlay');

  function fillLightbox(item) {
    if (!overlay || !item) { return; }
    overlay.querySelector('.lb-title').textContent = item.t || '';
    overlay.querySelector('.lb-place').textContent = item.p || '';

    var textBox = overlay.querySelector('.lb-text');
    textBox.innerHTML = '';
    (item.d || []).forEach(function (line) {
      var el = document.createElement('p');
      el.textContent = line;
      textBox.appendChild(el);
    });

    var gal = overlay.querySelector('.lb-gallery');
    gal.innerHTML = '';
    (item.i || []).forEach(function (src, n) {
      var img = document.createElement('img');
      img.src = src;
      img.alt = (item.t || '') + ' ' + (n + 1);
      img.loading = 'lazy';
      img.decoding = 'async';
      gal.appendChild(img);
    });
    gal.scrollLeft = 0;
    overlay.querySelector('.lb-gallery-wrap').style.display =
      (item.i && item.i.length) ? '' : 'none';
  }

  function openLightbox(n) {
    if (!lbData || !lbData[n] || !overlay) { return; }
    fillLightbox(lbData[n]);
    overlay.classList.add('open');
    document.body.classList.add('lb-open');
    var btn = overlay.querySelector('.lb-close');
    if (btn) { btn.focus(); }
  }

  function closeLightbox() {
    if (!overlay) { return; }
    overlay.classList.remove('open');
    document.body.classList.remove('lb-open');
  }

  if (overlay) {
    [].slice.call(document.querySelectorAll('.gallery-item')).forEach(function (fig, n) {
      fig.setAttribute('role', 'button');
      fig.setAttribute('tabindex', '0');
      fig.addEventListener('click', function () { openLightbox(n); });
      fig.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(n); }
      });
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) { closeLightbox(); }
    });
    overlay.querySelector('.lb-close').addEventListener('click', closeLightbox);

    var lbGal = overlay.querySelector('.lb-gallery');
    var lbStep = function () {
      var im = lbGal.querySelector('img');
      return im ? im.getBoundingClientRect().width + 12 : 350;
    };
    overlay.querySelector('.lb-arrow.prev').addEventListener('click', function () {
      lbGal.scrollBy({ left: -lbStep(), behavior: 'smooth' });
    });
    overlay.querySelector('.lb-arrow.next').addEventListener('click', function () {
      lbGal.scrollBy({ left: lbStep(), behavior: 'smooth' });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeLightbox(); }
    });
  }
})();
