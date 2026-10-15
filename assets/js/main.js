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
