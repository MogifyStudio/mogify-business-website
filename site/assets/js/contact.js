(function(){
  var C = window.MOGIFY || {}, WA = C.whatsapp || '923232194013', EM = C.email || 'mogifystudio@gmail.com';
  function picked(box){ return Array.prototype.slice.call(box.querySelectorAll('[aria-pressed="true"]')).map(function(b){ return b.dataset.v; }); }
  document.querySelectorAll('#cf-svcs .chip, .slots .chip').forEach(function(b){
    b.addEventListener('click', function(){
      var grp = b.closest('.slots');
      if (grp) grp.querySelectorAll('.chip').forEach(function(x){ if (x !== b) x.setAttribute('aria-pressed','false'); });
      b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      updCall();
    });
  });
  var callBtn = document.getElementById('call-btn');
  function updCall(){
    if (!callBtn) return;
    var day = picked(document.querySelector('[data-group="day"]'))[0], time = picked(document.querySelector('[data-group="time"]'))[0];
    var t = 'Hi Mogify Studio! I would like to book a quick call about a project' + (day || time ? ' on ' + [day, time ? time.toLowerCase() : ''].filter(Boolean).join(' ') + ' (Pakistan time)' : '') + '. Please confirm a time that works.';
    callBtn.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(t);
  }
  var f = document.getElementById('ct-form'); if (!f) return;
  var via = 'wa';
  f.querySelectorAll('[data-via]').forEach(function(b){ b.addEventListener('click', function(){ via = b.dataset.via; }); });
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var g = function(id){ return (document.getElementById(id).value || '').trim(); };
    var name = g('cf-name'), msg = g('cf-msg'), err = document.getElementById('cf-err');
    if (!name || !msg) { err.style.display = 'block'; (name ? document.getElementById('cf-msg') : document.getElementById('cf-name')).focus(); return; }
    err.style.display = 'none';
    var svcs = picked(document.getElementById('cf-svcs'));
    var lines = ['Hi Mogify Studio! New enquiry from your website.', '', 'Name: ' + name];
    if (g('cf-biz')) lines.push('Business: ' + g('cf-biz'));
    if (g('cf-email')) lines.push('Email: ' + g('cf-email'));
    if (g('cf-phone')) lines.push('Phone: ' + g('cf-phone'));
    if (svcs.length) lines.push('Needs: ' + svcs.join(', '));
    lines.push('', msg);
    var text = lines.join('\n');
    if (via === 'mail') location.href = 'mailto:' + EM + '?subject=' + encodeURIComponent('Project enquiry from ' + name) + '&body=' + encodeURIComponent(text);
    else window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
  });
})();
