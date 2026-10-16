(function () {
  var toggle = document.querySelector('.burger');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var filters = document.querySelectorAll('.filters button');
  var items = document.querySelectorAll('.proj');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filters.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      items.forEach(function (it) {
        var cats = (it.getAttribute('data-cats') || '').split(' ');
        it.hidden = !(f === 'all' || cats.indexOf(f) !== -1);
      });
    });
  });

  var main = document.getElementById('gal-main');
  var thumbs = document.querySelectorAll('.thumb');
  thumbs.forEach(function (th) {
    th.addEventListener('click', function () {
      if (main) main.src = th.getAttribute('data-src');
      thumbs.forEach(function (x) { x.removeAttribute('aria-current'); });
      th.setAttribute('aria-current', 'true');
    });
  });
})();

(function () {
  var root = document.querySelector('.hero-slider');
  if (!root) return;
  var slides = root.querySelectorAll('.slide'), dots = root.querySelectorAll('.dots button');
  var n = slides.length, i = 0, timer = null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function go(k) {
    i = (k + n) % n;
    slides.forEach(function (s, x) { s.classList.toggle('is-active', x === i); });
    dots.forEach(function (d, x) { if (x === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
  }
  function play() { if (reduce || timer) return; timer = setInterval(function () { go(i + 1); }, 6000); }
  function stop() { clearInterval(timer); timer = null; }
  root.querySelector('.prev').addEventListener('click', function () { go(i - 1); });
  root.querySelector('.next').addEventListener('click', function () { go(i + 1); });
  dots.forEach(function (d, x) { d.addEventListener('click', function () { go(x); }); });
  root.addEventListener('mouseenter', stop); root.addEventListener('mouseleave', play);
  root.addEventListener('focusin', stop); root.addEventListener('focusout', play);
  var x0 = null;
  root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  root.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var d = e.changedTouches[0].clientX - x0;
    if (Math.abs(d) > 50) go(d < 0 ? i + 1 : i - 1);
    x0 = null;
  });
  go(0); play();
})();
