/* Mogify Studio — shared site script */
(function(){
  var C = window.MOGIFY || {prices:{},addons:{}};
  var d = document, $ = function(s,c){return (c||d).querySelector(s)}, $$ = function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // header + mobile menu
  var hdr = $('.hdr');
  var onScroll = function(){ if(hdr) hdr.classList.toggle('scrolled', scrollY > 8); };
  addEventListener('scroll', onScroll, {passive:true}); onScroll();
  var burger = $('.burger');
  if (burger) burger.addEventListener('click', function(){
    var open = !d.body.classList.contains('menu-open');
    d.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open); burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  $$('.mnav a').forEach(function(a){ a.addEventListener('click', function(){ d.body.classList.remove('menu-open'); }); });
  addEventListener('keydown', function(e){ if(e.key==='Escape') d.body.classList.remove('menu-open'); });

  // reveal on scroll
  var rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target);} }); }, {rootMargin:'0px 0px -8% 0px', threshold:0.06});
    rv.forEach(function(el){ io.observe(el); });
  } else rv.forEach(function(el){ el.classList.add('in'); });

  // year
  $$('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });

  // prices from config (one object in config.js)
  function priceFor(key, isAddon){
    var v = null;
    if (isAddon) v = (C.addons||{})[key];
    else { var p = key.split('.'); v = ((C.prices||{})[p[0]]||{})[p[1]]; }
    return (v === undefined || v === null || v === '') ? null : String(v);
  }
  $$('[data-price]').forEach(function(el){
    var v = priceFor(el.getAttribute('data-price'));
    if (v) { el.textContent = v; el.classList.add('has-price'); }
    else el.textContent = el.hasAttribute('data-short') ? 'On request' : (C.noPriceText || 'Price on request');
  });
  $$('[data-price-note]').forEach(function(el){ if (C.priceNote) el.textContent = C.priceNote; });
  $$('[data-addon]').forEach(function(el){ var v = priceFor(el.getAttribute('data-addon'), true); el.textContent = v || 'On request'; });
  window.MOGIFY_PRICE = priceFor;

  // hero rotating word
  var rot = $('.hero .rot');
  if (rot && !reduce) {
    var i = 0;
    setInterval(function(){
      var r = $('.hero .rot'); if (!r) return; var ws = $$('span', r); if (!ws.length) return; i = i % ws.length;
      var cur = ws[i]; cur.classList.remove('on'); cur.classList.add('off');
      i = (i+1) % ws.length; var nx = ws[i]; nx.classList.remove('off'); nx.classList.add('on');
      setTimeout(function(){ cur.classList.remove('off'); }, 650);
    }, 2200);
  }

  // 3D work stack: pointer tilt + scroll drift
  var stack = $('#stack');
  if (stack && !reduce) {
    var tx = 0, ty = 0, cx = 0, cy = 0, raf;
    var host = stack.parentElement;
    function loop(){ cx += (tx-cx)*.08; cy += (ty-cy)*.08; stack.style.transform = 'rotateX('+cy.toFixed(2)+'deg) rotateY('+cx.toFixed(2)+'deg)'; raf = (Math.abs(tx-cx)>.01||Math.abs(ty-cy)>.01) ? requestAnimationFrame(loop) : null; }
    function kick(){ if(!raf) raf = requestAnimationFrame(loop); }
    addEventListener('pointermove', function(e){ if (e.pointerType !== 'mouse') return; var r = host.getBoundingClientRect(); tx = ((e.clientX - (r.left + r.width/2)) / innerWidth) * 18; ty = -((e.clientY - (r.top + r.height/2)) / innerHeight) * 12; kick(); }, {passive:true});
    addEventListener('scroll', function(){ var r = host.getBoundingClientRect(); if (r.bottom < 0) return; if (matchMedia('(pointer:coarse)').matches) { tx = Math.sin(scrollY/220)*6; ty = 6 - Math.min(scrollY/40, 10); kick(); } }, {passive:true});
    // gentle intro
    tx = -8; ty = 6; kick();
  }

  // brand playground
  var pg = $('#pg-name');
  if (pg) {
    var mocks = $('#mocks'), go = $('#pg-go');
    function initials(n){ var p = n.trim().split(/\s+/).filter(Boolean); if(!p.length) return 'YB'; return (p.length>1 ? p[0][0]+p[1][0] : p[0].slice(0,2)).toUpperCase(); }
    function upd(){
      var n = pg.value.trim() || 'Your Brand';
      $$('[data-name]', mocks).forEach(function(el){ el.textContent = n; });
      $$('[data-mono]', mocks).forEach(function(el){ el.textContent = initials(n); });
      var slug = n.toLowerCase().replace(/[^a-z0-9]+/g,'') || 'yourbrand';
      $$('[data-slug]', mocks).forEach(function(el){ el.textContent = slug; });
      go.href = '/planner?service=brand' + (pg.value.trim() ? '&name=' + encodeURIComponent(pg.value.trim()) : '');
    }
    pg.addEventListener('input', upd);
    $$('.sw').forEach(function(b){ b.addEventListener('click', function(){
      $$('.sw').forEach(function(x){ x.setAttribute('aria-pressed','false'); }); b.setAttribute('aria-pressed','true');
      mocks.style.setProperty('--a', b.dataset.a); mocks.style.setProperty('--b', b.dataset.b); mocks.style.setProperty('--c', b.dataset.c);
      mocks.style.setProperty('--f', b.dataset.f === 'Fraunces' ? 'var(--serif)' : 'var(--font)');
    }); });
  }

  // lightbox (images + videos)
  var lb = $('.lb');
  if (lb) {
    var list = [], idx = 0, media = $('.lb-media', lb), cap = $('figcaption', lb), lastFocus;
    function vis(){ return $$('[data-lb]').filter(function(b){ var li = b.closest('.witem'); return !li || !li.hidden; }); }
    function show(i){
      list = vis(); if (!list.length) return; idx = (i + list.length) % list.length; var b = list[idx];
      media.innerHTML = '';
      if (b.hasAttribute('data-video')) { var v = d.createElement('video'); v.src = b.dataset.full; v.controls = true; v.autoplay = true; v.playsInline = true; v.setAttribute('playsinline',''); media.appendChild(v); }
      else { var im = d.createElement('img'); im.src = b.dataset.full; im.alt = b.dataset.title || ''; media.appendChild(im); }
      cap.innerHTML = ''; var t = d.createElement('span'); t.textContent = b.dataset.title || ''; var s = d.createElement('small'); s.textContent = b.dataset.sub || ''; cap.appendChild(t); cap.appendChild(s);
    }
    function open(b){ lastFocus = b; show(vis().indexOf(b)); lb.hidden = false; lb.classList.add('open'); d.body.style.overflow = 'hidden'; $('.lb-x', lb).focus(); }
    function close(){ lb.classList.remove('open'); lb.hidden = true; media.innerHTML = ''; d.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
    d.addEventListener('click', function(e){ var b = e.target.closest('[data-lb]'); if (b) { e.preventDefault(); open(b); } });
    $('.lb-x', lb).addEventListener('click', close);
    $('.lb-p', lb).addEventListener('click', function(){ show(idx-1); });
    $('.lb-n', lb).addEventListener('click', function(){ show(idx+1); });
    lb.addEventListener('click', function(e){ if (e.target === lb) close(); });
    addEventListener('keydown', function(e){ if (!lb.classList.contains('open')) return; if (e.key==='Escape') close(); if (e.key==='ArrowLeft') show(idx-1); if (e.key==='ArrowRight') show(idx+1); });
    var sx = null; lb.addEventListener('touchstart', function(e){ sx = e.touches[0].clientX; }, {passive:true});
    lb.addEventListener('touchend', function(e){ if (sx===null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(idx + (dx<0?1:-1)); sx = null; });
  }

  // work filters
  var fb = $$('[data-filter]');
  if (fb.length) {
    function apply(cat){
      fb.forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.filter===cat ? 'true':'false'); });
      $$('#wgrid .witem').forEach(function(li){ li.hidden = !(cat==='all' || li.dataset.cat===cat); });
    }
    fb.forEach(function(b){ b.addEventListener('click', function(){ apply(b.dataset.filter); history.replaceState(null,'', b.dataset.filter==='all' ? location.pathname : '#'+b.dataset.filter); }); });
    var h = location.hash.slice(1); if (h && fb.some(function(b){ return b.dataset.filter===h; })) apply(h);
  }

  // English / Urdu toggle for key text
  var LKEY = 'mogify-lang';
  function setLang(ur){
    $$('[data-ur]').forEach(function(el){
      if (!el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      if (ur) { el.textContent = el.getAttribute('data-ur'); el.setAttribute('lang','ur'); el.setAttribute('dir','rtl'); el.classList.add('is-ur'); }
      else { el.innerHTML = el.getAttribute('data-en'); el.removeAttribute('lang'); el.removeAttribute('dir'); el.classList.remove('is-ur'); }
    });
    $$('[data-lang-toggle]').forEach(function(b){ b.textContent = ur ? 'English' : 'اردو'; b.setAttribute('lang', ur ? 'en' : 'ur'); b.setAttribute('aria-label', ur ? 'Switch back to English' : 'Switch key text to Urdu'); });
    d.documentElement.classList.toggle('ur-mode', ur);
    try { localStorage.setItem(LKEY, ur ? 'ur' : 'en'); } catch(e){}
  }
  $$('[data-lang-toggle]').forEach(function(b){ b.addEventListener('click', function(){ setLang(!d.documentElement.classList.contains('ur-mode')); }); });
  try { if (localStorage.getItem(LKEY) === 'ur') setLang(true); } catch(e){}
})();
