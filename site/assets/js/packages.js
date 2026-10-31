(function(){
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-tab]'));
  if (!tabs.length) return;
  function sel(id, scroll){
    var ok = false;
    tabs.forEach(function(t){ var on = t.dataset.tab === id; if (on) ok = true; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
      var p = document.getElementById('panel-' + t.dataset.tab); if (p) p.hidden = !on;
      if (on && t.scrollIntoView) { var bar = t.parentElement; bar.scrollTo({left: t.offsetLeft - 24, behavior: 'smooth'}); } });
    return ok;
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){ sel(t.dataset.tab); history.replaceState(null, '', '#' + t.dataset.tab); });
    t.addEventListener('keydown', function(e){ var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!k) return; var n = tabs[(i + k + tabs.length) % tabs.length]; n.focus(); n.click(); });
  });
  var h = location.hash.slice(1); if (h) sel(h);
})();
