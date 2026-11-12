/* TrustRoute Technologies · site behaviour */

// Calendly booking link for "Book a call" buttons, e.g. 'https://calendly.com/your-name/intro-call'.
// While empty, those buttons simply go to the Contact page.
var CALENDLY_URL = 'https://calendly.com/najusmani/30min';

(function () {
  // Booking popup: Calendly's script and styles load only when a visitor clicks a booking link.
  var calendlyLoading = null;
  function loadCalendly() {
    if (window.Calendly) return Promise.resolve();
    if (calendlyLoading) return calendlyLoading;
    calendlyLoading = new Promise(function (resolve, reject) {
      var css = document.createElement('link');
      css.rel = 'stylesheet';
      css.href = 'https://assets.calendly.com/assets/external/widget.css';
      document.head.appendChild(css);
      var js = document.createElement('script');
      js.src = 'https://assets.calendly.com/assets/external/widget.js';
      js.async = true;
      js.onload = function () { resolve(); };
      js.onerror = function () { calendlyLoading = null; reject(); };
      document.head.appendChild(js);
    });
    return calendlyLoading;
  }
  document.addEventListener('click', function (e) {
    var link = e.target.closest && e.target.closest('[data-calendly]');
    if (!link || !CALENDLY_URL) return; // no link configured: follow the normal href
    e.preventDefault();
    var url = CALENDLY_URL + (CALENDLY_URL.indexOf('?') === -1 ? '?' : '&') +
      'hide_gdpr_banner=1&primary_color=a8833f&text_color=1a2133&background_color=ffffff';
    loadCalendly()
      .then(function () { window.Calendly.initPopupWidget({ url: url }); })
      .catch(function () { window.open(CALENDLY_URL, '_blank', 'noopener'); });
  });
})();

(function () {
  var nav = document.getElementById('nav');
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');

  // Header: switch to solid white once the page scrolls
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 60);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = !drawer.classList.contains('open');
      drawer.classList.toggle('open', open);
      nav.classList.toggle('open', open);
      document.body.classList.toggle('locked', open);
      burger.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) burger.click();
    });
  }

  // Reveal on scroll (robust to fast scrolling)
  var pending = [].slice.call(document.querySelectorAll('.rv, .reveal')), ticking = false;
  function check() {
    ticking = false;
    var limit = window.innerHeight * 0.9;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top < limit) { el.classList.add('in'); return false; }
      return true;
    });
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(check); } }
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  window.addEventListener('load', check);
  check();

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Contact form: sends to the Supabase "contact" function and shows the result in place
  var form = document.getElementById('enquiry');
  if (form) {
    // Pre-select the area of interest from links such as contact.html?interest=sms
    var interest = new URLSearchParams(window.location.search).get('interest');
    var select = document.getElementById('interest');
    if (interest && select && select.querySelector('option[value="' + interest.replace(/[^a-z]/g, '') + '"]')) {
      select.value = interest;
    }

    var status = document.getElementById('form-status');
    var button = form.querySelector('button[type="submit"]');
    var fallback = 'Please email hello@trustroutetechnologies.com instead.';

    function show(text, ok) {
      status.textContent = text;
      status.classList.add('show');
      status.classList.toggle('ok', !!ok);
      status.classList.toggle('err', !ok);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var action = form.getAttribute('action') || '';
      if (action.indexOf('YOUR-PROJECT-REF') !== -1 || action === '#') {
        show('This form is not connected yet. ' + fallback, false);
        return;
      }

      button.disabled = true;
      var label = button.textContent;
      button.textContent = 'Sending…';

      fetch(action, { method: 'POST', body: new FormData(form) })
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (body) { return { res: res, body: body }; });
        })
        .then(function (r) {
          if (r.res.ok && r.body.ok) {
            form.reset();
            show('Thank you. Your enquiry has been received and we will be in touch shortly.', true);
          } else {
            show((r.body && r.body.error) || ('Something went wrong. ' + fallback), false);
          }
        })
        .catch(function () {
          show('We could not reach our server. ' + fallback, false);
        })
        .then(function () {
          button.disabled = false;
          button.textContent = label;
        });
    });
  }
})();

// Product scenes (e.g. SettleDesk): play once when scrolled into view; [data-loop] scenes replay while visible.
(function () {
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  // Hold each scene at its first frame until it is well into the viewport (position check, so it also works
  // when scrolling fast or when the browser skips intersection updates).
  var scenes = [].slice.call(document.querySelectorAll('[data-scene]'));
  scenes.forEach(function (el) { el.setAttribute('data-armed', ''); });
  var sceneTick = false;
  function playVisible() {
    sceneTick = false;
    var limit = window.innerHeight * 0.8;
    scenes = scenes.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < limit) { el.setAttribute('data-play', ''); return false; }
      return true;
    });
  }
  function requestScenes() { if (!sceneTick) { sceneTick = true; requestAnimationFrame(playVisible); } }
  window.addEventListener('scroll', requestScenes, { passive: true });
  window.addEventListener('resize', requestScenes);
  window.addEventListener('load', playVisible);
  playVisible();
  document.querySelectorAll('[data-loop]').forEach(function (el) {
    var visible = true;
    var watch = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.target === el) visible = en.isIntersecting; });
    });
    watch.observe(el);
    var every = (parseFloat(el.getAttribute('data-loop')) || 10) * 1000;
    setInterval(function () {
      if (!visible || document.hidden || !el.isConnected) return;
      // restart every CSS animation inside by swapping in a fresh copy of the scene
      var fresh = el.cloneNode(true);
      watch.unobserve(el);
      el.parentNode.replaceChild(fresh, el);
      el = fresh;
      watch.observe(el);
    }, every);
  });
})();
