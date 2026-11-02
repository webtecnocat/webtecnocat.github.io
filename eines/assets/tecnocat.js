(function () {
  // Menú per a mòbil
  var boto = document.querySelector('.obre-menu');
  if (boto) boto.addEventListener('click', function () {
    var nav = boto.parentNode;
    var obert = nav.classList.toggle('obert');
    boto.setAttribute('aria-expanded', obert);
  });

  // Subwebs eXeLearning: l'índex passa a ser un desplegable a sobre del contingut
  var index = document.getElementById('siteNav');
  if (index) {
    var plegable = document.createElement('details');
    plegable.className = 'index-subweb';
    var capIndex = document.createElement('summary');
    var actual = index.querySelector('a.active');
    capIndex.innerHTML = '<b>Índex</b><span></span>';
    capIndex.querySelector('span').textContent = actual ? actual.textContent : '';
    plegable.appendChild(capIndex);
    index.parentNode.insertBefore(plegable, index);
    plegable.appendChild(index);
  }

  // Botó per tornar a dalt de la pàgina
  var amunt = document.createElement('button');
  amunt.type = 'button';
  amunt.className = 'amunt';
  amunt.textContent = '↑';
  amunt.title = 'Torna a dalt';
  amunt.setAttribute('aria-label', 'Torna a dalt de la pàgina');
  document.body.appendChild(amunt);
  amunt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  function mostraAmunt() { amunt.classList.toggle('visible', window.scrollY > window.innerHeight); }
  window.addEventListener('scroll', mostraAmunt, { passive: true });
  mostraAmunt();

  // Visor de diapositives
  document.querySelectorAll('.diapos').forEach(function (v) {
    var imgs = v.querySelectorAll('.diapos-marc img');
    var ant = v.querySelector('.ant'), seg = v.querySelector('.seg'), num = v.querySelector('.num');
    var i = 0;
    function mostra(n) {
      imgs[i].classList.remove('vista');
      i = Math.max(0, Math.min(imgs.length - 1, n));
      imgs[i].classList.add('vista');
      imgs[i].loading = 'eager';
      num.textContent = (i + 1) + ' / ' + imgs.length;
      ant.disabled = i === 0;
      seg.disabled = i === imgs.length - 1;
    }
    ant.addEventListener('click', function () { mostra(i - 1); });
    seg.addEventListener('click', function () { mostra(i + 1); });
    v.querySelector('.diapos-marc').addEventListener('click', function () { mostra(i + 1); });
    mostra(0);
  });

  // Vídeos de YouTube. Des de file:// YouTube no deixa reproduir-los incrustats
  // (error 153, falta la capçalera Referer), així que l'enllaç obre YouTube en una pestanya.
  // Publicat a GitHub Pages (https) es reprodueixen dins la pàgina.
  var web = /^https?:$/.test(location.protocol);
  document.querySelectorAll('a.video[data-embed]').forEach(function (v) {
    if (!web) return;
    v.addEventListener('click', function (e) {
      e.preventDefault();
      var f = document.createElement('iframe');
      f.src = v.dataset.embed + '&autoplay=1';
      f.title = v.title || 'Vídeo de YouTube';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      var marc = document.createElement('div');
      marc.className = 'video';
      marc.appendChild(f);
      v.replaceWith(marc);
    });
  });

  // Cerca (cerca.html?q=...)
  var caixa = document.getElementById('cerca-resultats');
  if (!caixa || !window.TECNOCAT_CERCA) return;
  var q = (new URLSearchParams(location.search).get('q') || '').trim();
  document.querySelectorAll('.cerca input[name=q]').forEach(function (i) { i.value = q; });
  var resum = document.getElementById('cerca-resum');
  if (!q) { resum.textContent = 'Escriu què vols trobar al quadre de cerca.'; return; }

  var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var pla = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  var paraules = pla(q).split(/\s+/).filter(Boolean);
  var marca = function (text) {
    var t = esc(text);
    paraules.forEach(function (p) {
      var re = new RegExp('(' + p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      t = t.replace(re, '<mark>$1</mark>');
    });
    return t;
  };
  var lloc = function (u) { return u.indexOf('linkat/') === 0 ? 'Linkat per coordinadors' : u.indexOf('ia/') === 0 ? 'Recursos d\'IA' : 'Tecnocat'; };

  var res = window.TECNOCAT_CERCA.map(function (d) {
    var t = pla(d.t), x = pla(d.x), punts = 0;
    for (var i = 0; i < paraules.length; i++) {
      var p = paraules[i];
      if (t.indexOf(p) < 0 && x.indexOf(p) < 0) return null;
      if (t.indexOf(p) >= 0) punts += 10;
      punts += x.split(p).length - 1;
    }
    var pos = x.indexOf(paraules[0]);
    var tros = pos < 0 ? d.x.slice(0, 180) : (pos > 70 ? '…' : '') + d.x.slice(Math.max(0, pos - 70), pos + 130) + '…';
    return { d: d, punts: punts, tros: tros };
  }).filter(Boolean).sort(function (a, b) { return b.punts - a.punts; });

  resum.textContent = res.length + (res.length === 1 ? ' resultat' : ' resultats') + ' per «' + q + '»';
  caixa.innerHTML = res.map(function (r) {
    return '<a href="' + r.d.u + '"><span class="lloc">' + lloc(r.d.u) + '</span><br><b>' + marca(r.d.t) + '</b><small>' + marca(r.tros) + '</small></a>';
  }).join('');
})();
