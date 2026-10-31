/* Mogify Studio — Project Planner. Builds a brief step by step and sends it to WhatsApp / email. */
(function(){
  var root = document.getElementById('planner'); if (!root) return;
  var DATA = JSON.parse(document.getElementById('pl-data').textContent);
  var C = window.MOGIFY || {};
  var WA = C.whatsapp || root.dataset.wa, EMAIL = C.email || root.dataset.email;
  var IC = DATA.icons, SV = {}; DATA.services.forEach(function(s){ SV[s.id] = s; });
  var $ = function(s,c){ return (c||document).querySelector(s); }, $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };
  var esc = function(t){ return String(t==null?'':t).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); };
  var TIERS = ['starter','growth','premium'], TNAME = {starter:'Starter', growth:'Growth', premium:'Premium'};

  // ---- per-service detail questions. Option = [label, tierWeight 0|1|2]
  var Q = {
    web: [
      {k:'pages', t:'single', l:'How many pages?', o:[['One-page landing',0],['2–5 pages',1],['6–10 pages',2],['10+ pages',2],['Not sure yet',1]]},
      {k:'features', t:'multi', l:'Features you want', o:[['WhatsApp chat button',0],['Contact / enquiry form',0],['Gallery / portfolio',0],['Google Maps location',0],['Blog or news',1],['SEO setup',1],['Animations & 3D effects',1],['English + Urdu',1],['Online store / payments',2],['Booking / appointments',2],['Edit content myself (CMS)',2]]},
      {k:'domain', t:'single', l:'Domain', o:[['I have a domain',0],['Help me buy one',0],['Not sure',0]]}
    ],
    logo: [
      {k:'kind', t:'single', l:'New or redesign?', o:[['Brand new logo',0],['Redesign my current logo',0]]},
      {k:'style', t:'multi', l:'Logo style you like', o:[['Wordmark (name only)',0],['Icon + name',0],['Emblem / badge',0],['Mascot / character',1],['Not sure, guide me',0]]},
      {k:'extras', t:'multi', l:'Also need', o:[['Business card',1],['Social media kit',1],['Favicon / app icon',1],['Brand guide',2],['Logo animation',2]]}
    ],
    brand: [
      {k:'stage', t:'single', l:'Where are you?', o:[['New business',0],['Rebrand / refresh',1]]},
      {k:'need', t:'multi', l:'What should the identity include?', o:[['Logo suite',0],['Colours & fonts',0],['Business cards & stationery',0],['Social media kit',1],['Brand guidelines',1],['Tagline & brand voice',1],['Packaging design',2],['Signage / shopfront',2],['Logo animation',2]]}
    ],
    uiux: [
      {k:'platform', t:'multi', l:'Platform', o:[['iOS app',0],['Android app',0],['Web app / SaaS',0],['Dashboard / admin',1],['Website',0]]},
      {k:'screens', t:'single', l:'Roughly how many screens?', o:[['Up to 5',0],['5–15',1],['15–30',2],['Not sure yet',1]]},
      {k:'need', t:'multi', l:'Also need', o:[['Wireframes',0],['Clickable prototype',1],['Design system',2],['UX review of my current app',2]]}
    ],
    motion: [
      {k:'type', t:'multi', l:'What kind of video?', o:[['Logo animation',0],['Social reel / ad',0],['YouTube intro / outro',0],['Product promo',1],['Explainer video',1],['Kinetic typography',1]]},
      {k:'length', t:'single', l:'Length', o:[['Up to 10 s',0],['10–30 s',1],['30–60 s',2],['Longer',2]]},
      {k:'format', t:'multi', l:'Formats', o:[['Vertical 9:16',0],['Square 1:1',0],['Widescreen 16:9',0]]}
    ],
    anim3d: [
      {k:'subject', t:'single', l:'What should we animate?', o:[['Logo reveal',0],['Product shot',1],['Satisfying / ASMR loop',1],['A scene or story',2]]},
      {k:'length', t:'single', l:'Length', o:[['Up to 10 s',0],['10–20 s',1],['20–45 s',2]]},
      {k:'extras', t:'multi', l:'Extras', o:[['Photoreal materials',0],['Sound design',0],['Cloth / liquid / physics',1],['4K export',2]]}
    ],
    social: [
      {k:'platforms', t:'multi', l:'Platforms', o:[['Instagram',0],['Facebook',0],['TikTok',0],['LinkedIn',0],['X',0]]},
      {k:'volume', t:'single', l:'How much content?', o:[['A starter set (about 6)',0],['A month of posts (about 12)',1],['A full content set (20+)',2]]},
      {k:'need', t:'multi', l:'Include', o:[['Posts & carousels',0],['Stories / reel covers',1],['Ad creatives',1],['Captions & hashtags',2],['Animated posts',2],['Editable templates',2]]}
    ],
    book: [
      {k:'format', t:'multi', l:'Formats', o:[['E-book / Kindle',0],['Paperback',1],['Hardcover',2],['Audiobook cover',2]]},
      {k:'genre', t:'single', l:'Genre', o:[["Children's",0],['Fiction',0],['Memoir',0],['Business / self-help',0],['Poetry',0],['Other',0]]},
      {k:'art', t:'single', l:'Artwork', o:[['Photo or typographic',0],['Custom illustration',2],['Not sure',0]]}
    ],
    video: [
      {k:'type', t:'multi', l:'What are we editing?', o:[['Reels / Shorts / TikTok',0],['Ad / promo',0],['YouTube video',1],['Podcast',1],['Course / tutorial',1]]},
      {k:'length', t:'single', l:'Final length', o:[['Under 60 s',0],['Up to 10 min',1],['Up to 20 min',2],['Longer',2]]},
      {k:'extras', t:'multi', l:'Extras', o:[['Captions',0],['Thumbnail',1],['Motion graphics',1],['Shorts cut-downs',2]]},
      {k:'volume', t:'single', l:'How often?', o:[['One video',0],['A few videos',0],['Every week',0]]}
    ]
  };
  var GOALS = ['Launch a new business','Look more professional','Get more leads & enquiries','Sell online','Grow on social media','Rebrand / refresh','Grow my YouTube','Pitch to investors','Publish my book'];
  var VIBES = [
    ['Minimal & clean','#FFFFFF','#121927','Aa',"'Manrope',sans-serif",400],
    ['Bold & loud','#FF5C39','#111111','AA',"'Manrope',sans-serif",800],
    ['Luxury & elegant','#1C1A17','#C9A96E','Aa',"'Fraunces',serif",500],
    ['Playful & fun','#FFD84D','#2B0B3F','Aa!',"'Manrope',sans-serif",800],
    ['Corporate & trusted','#0B2A4A','#FFFFFF','Aa',"'Manrope',sans-serif",700],
    ['Futuristic & tech','#0A0F1C','#5FE0D5','A/a',"'Manrope',sans-serif",300],
    ['Desi & cultural','#7A1F3D','#F2C14E','آ',"'Noto Nastaliq Urdu','Geeza Pro',serif",400],
    ['Natural & organic','#E9E4D6','#2F4A3A','Aa',"'Fraunces',serif",400]
  ];
  var COLORS = ['Use my brand colours','Blues','Greens & teal','Black & gold','Warm reds & oranges','Pastels','Black & white','Surprise me'];
  var ASSETS = ['Logo','Brand colours & fonts','Photos / videos','Written content','Domain','Nothing yet'];
  var TIMES = ['ASAP / urgent','Within 2 weeks','Within a month','1–3 months','Flexible'];
  var BUDGET = {PKR:['Under PKR 25k','PKR 25k–50k','PKR 50k–100k','PKR 100k–250k','PKR 250k+','Not sure yet'], USD:['Under $150','$150–$500','$500–$1,500','$1,500–$5,000','$5,000+','Not sure yet']};
  var CONTACT = ['WhatsApp','Email','Phone call'];
  var STEPS = ['Services','Goals','Details','Style','Timeline','Contact','Review'];

  // ---- state
  var KEY = 'mogify-planner-v1';
  var S = load() || fresh();
  function fresh(){ return {step:0, max:0, services:[], goals:[], business:'', industry:'', details:{}, vibes:[], colors:[], refs:'', assets:[], time:'', date:'', cur:'PKR', budget:'', name:'', email:'', phone:'', city:'', prefer:'WhatsApp', notes:'', tierHint:{}, ref: makeRef()}; }
  function makeRef(){ var d = new Date(), p = function(n){ return (n<10?'0':'')+n; }; return 'MGF-' + String(d.getFullYear()).slice(2) + p(d.getMonth()+1) + p(d.getDate()) + '-' + Math.random().toString(36).slice(2,6).toUpperCase(); }
  function load(){ try { var s = JSON.parse(localStorage.getItem(KEY)); return s && s.ref ? s : null; } catch(e){ return null; } }
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e){} }

  // prefill from URL (?service=web&tier=growth&name=Chai)
  (function(){
    var u = new URLSearchParams(location.search), sv = u.get('service'), tier = u.get('tier'), nm = u.get('name');
    if (sv && SV[sv]) { if (S.services.indexOf(sv) < 0) S.services.push(sv); if (tier && TIERS.indexOf(tier) >= 0) S.tierHint[sv] = tier; if (S.step === 0 && !nm) { S.step = 0; } }
    if (nm) S.business = nm.slice(0, 60);
    if (sv || nm) { save(); if (history.replaceState) history.replaceState(null, '', location.pathname); }
  })();

  var form = $('#pl-form'), bar = $('#pl-bar'), cnt = $('#pl-count'), back = $('#pl-back'), next = $('#pl-next'), stepsEl = $('#pl-steps'), sum = $('#pl-summary'), side = $('#pl-side'), peek = $('#pl-peek'), peekSub = $('#pl-peek-sub');
  $('#pl-ref').textContent = S.ref;

  // ---- helpers to render controls
  function opt(group, val, label, sub, icon, on, multi){
    return '<button type="button" class="opt" role="'+(multi?'checkbox':'radio')+'" aria-checked="'+(on?'true':'false')+'" data-g="'+group+'" data-v="'+esc(val)+'">'+(icon?'<span class="oi">'+icon+'</span>':'')+'<b>'+esc(label)+'</b>'+(sub?'<small>'+esc(sub)+'</small>':'')+'<span class="tick">'+IC.check+'</span></button>';
  }
  function chip(group, val, on, multi){ return '<button type="button" class="chip sm" role="'+(multi?'checkbox':'radio')+'" aria-checked="'+(on?'true':'false')+'" data-g="'+group+'" data-v="'+esc(val)+'">'+esc(val)+'</button>'; }
  function grp(label, inner, sub){ return '<div class="pl-group"><span class="lbl">'+esc(label)+(sub?'<small>'+esc(sub)+'</small>':'')+'</span>'+inner+'</div>'; }
  function head(h, p){ return '<div class="pl-q"><h2 tabindex="-1">'+h+'</h2>'+(p?'<p>'+p+'</p>':'')+'</div>'; }
  function input(id, label, val, type, ph, req, ac){ return '<div class="field"><label for="'+id+'">'+esc(label)+(req?' *':'')+'</label><input class="inp" id="'+id+'" data-f="'+id.replace('pl-','')+'" type="'+(type||'text')+'" value="'+esc(val)+'" placeholder="'+esc(ph||'')+'"'+(ac?' autocomplete="'+ac+'"':'')+(type==='email'?' inputmode="email"':type==='tel'?' inputmode="tel"':'')+'></div>'; }

  function detailVal(sid, k){ return ((S.details[sid]||{})[k]); }

  // ---- step renderers
  var R = [
    function(){ // services
      return head('What do you need?', 'Pick one or more. You can combine services into one project.') +
        '<div class="pl-svc" role="group" aria-label="Services">' + DATA.services.map(function(s){ return opt('services', s.id, s.name, s.card, s.icon, S.services.indexOf(s.id) >= 0, true); }).join('') + '</div><p class="pl-err" id="pl-err" role="alert"></p>';
    },
    function(){ // goals
      return head('What should this project do for you?', 'Pick your main goals and tell us a little about your business.') +
        grp('Main goals', '<div class="chips" role="group">' + GOALS.map(function(g){ return chip('goals', g, S.goals.indexOf(g) >= 0, true); }).join('') + '</div>', 'pick any') +
        '<div class="pl-two">' + input('pl-business', 'Business or brand name', S.business, 'text', 'e.g. Chai Corner', false, 'organization') + input('pl-industry', 'Industry', S.industry, 'text', 'e.g. Café, clinic, fashion, SaaS') + '</div>';
    },
    function(){ // details
      if (!S.services.length) return head('Details', 'Pick at least one service first.');
      return head('A few details', 'Quick taps for each service. Skip anything you are not sure about.') +
        S.services.map(function(sid){
          var s = SV[sid];
          return '<div class="pl-svcblock"><h3><span>' + s.icon + '</span>' + esc(s.name) + '</h3>' + Q[sid].map(function(q){
            var cur = detailVal(sid, q.k), multi = q.t === 'multi';
            return grp(q.l, '<div class="chips" role="group">' + q.o.map(function(o){ var on = multi ? (cur||[]).indexOf(o[0]) >= 0 : cur === o[0]; return chip('d:'+sid+':'+q.k, o[0], on, multi); }).join('') + '</div>', multi ? 'pick any' : 'pick one');
          }).join('') + '</div>';
        }).join('');
    },
    function(){ // style
      return head('What style feels like you?', 'Choose up to two moods, colours you like, and share any references.') +
        grp('Mood', '<div class="pl-vibes" role="group">' + VIBES.map(function(v){
          var on = S.vibes.indexOf(v[0]) >= 0;
          return '<button type="button" class="opt vibe" role="checkbox" aria-checked="'+on+'" data-g="vibes" data-v="'+esc(v[0])+'"><span class="vv" style="background:'+v[1]+';color:'+v[2]+';font-family:'+v[4]+';font-weight:'+v[5]+'">'+v[3]+'</span><span class="vt"><b>'+esc(v[0])+'</b></span><span class="tick">'+IC.check+'</span></button>';
        }).join('') + '</div>', 'up to 2') +
        grp('Colours', '<div class="chips" role="group">' + COLORS.map(function(c){ return chip('colors', c, S.colors.indexOf(c) >= 0, true); }).join('') + '</div>', 'pick any') +
        '<div class="field"><label for="pl-refs">References you like</label><textarea class="inp" id="pl-refs" data-f="refs" placeholder="Links to websites, logos, Instagram accounts or videos you like">' + esc(S.refs) + '</textarea></div>' +
        grp('I already have', '<div class="chips" role="group">' + ASSETS.map(function(c){ return chip('assets', c, S.assets.indexOf(c) >= 0, true); }).join('') + '</div>', 'pick any');
    },
    function(){ // timeline + budget
      return head('Timeline and budget', 'Your preferences help us suggest the right package and plan.') +
        grp('When do you need it?', '<div class="chips" role="group">' + TIMES.map(function(t){ return chip('time', t, S.time === t, false); }).join('') + '</div>', 'pick one') +
        '<div class="field" style="max-width:320px"><label for="pl-date">Launch date or deadline (optional)</label><input class="inp" id="pl-date" data-f="date" type="date" value="' + esc(S.date) + '"></div>' +
        '<div class="pl-group"><span class="lbl">Your budget range<small>pick one</small></span><div class="pl-seg" role="group" aria-label="Currency"><button type="button" data-cur="PKR" aria-pressed="'+(S.cur==='PKR')+'">PKR</button><button type="button" data-cur="USD" aria-pressed="'+(S.cur==='USD')+'">USD</button></div>' +
        '<div class="chips" role="group" id="pl-budget">' + BUDGET[S.cur].map(function(b){ return chip('budget', b, S.budget === b, false); }).join('') + '</div>' +
        '<p class="pl-hint">' + IC.wallet + '<span>This is your own range so we can match the scope to it. It is not our price: you get a fixed quote after we see your brief.</span></p></div>';
    },
    function(){ // contact
      return head('Where should we reply?', 'Only your name is required. Nothing is saved on our side until you send it.') +
        '<div class="pl-two">' + input('pl-name', 'Your name', S.name, 'text', 'Full name', true, 'name') + input('pl-city', 'City / country', S.city, 'text', 'e.g. Karachi, Pakistan', false, 'address-level2') + '</div>' +
        '<div class="pl-two">' + input('pl-phone', 'WhatsApp / phone', S.phone, 'tel', '+92 3xx xxxxxxx', false, 'tel') + input('pl-email', 'Email', S.email, 'email', 'you@company.com', false, 'email') + '</div>' +
        grp('Best way to reach you', '<div class="chips" role="group">' + CONTACT.map(function(c){ return chip('prefer', c, S.prefer === c, false); }).join('') + '</div>') +
        '<div class="field"><label for="pl-notes">Anything else?</label><textarea class="inp" id="pl-notes" data-f="notes" placeholder="Ideas, must-haves, questions…">' + esc(S.notes) + '</textarea></div><p class="pl-err" id="pl-err" role="alert"></p>';
    },
    function(){ // review
      var sc = scope();
      return head('Your brief is ready', 'Here is your project scope. Send it to Moiz and you will get a fixed quote and timeline back.') +
        '<div class="pl-review"><div class="pl-scopebig">' + sc.map(function(x){
          return '<div class="sc"><div class="sc-h"><b>' + esc(x.name) + '</b><em>Closest package: ' + x.tierName + '</em></div><ul>' + x.items.map(function(i){ return '<li>' + IC.check + '<span>' + esc(i) + '</span></li>'; }).join('') + '</ul></div>';
        }).join('') + '</div>' +
        grp('How it will run', '<div class="pl-phases"><span>Brief</span><i>→</i><span>Fixed quote</span><i>→</i><span>Design</span><i>→</i><span>' + (S.services.indexOf('web')>=0 ? 'Build' : 'Produce') + '</span><i>→</i><span>Revisions</span><i>→</i><span>Launch</span></div>') +
        '<div class="pl-send"><a class="btn btn-wa btn-lg" id="pl-wa" href="' + waLink() + '" target="_blank" rel="noopener">' + DATA.wa + ' Send brief on WhatsApp</a><a class="btn btn-ghost" id="pl-mail" href="' + mailLink() + '">' + IC.mail + ' Send by email</a><button type="button" class="btn btn-ghost" id="pl-copy">' + IC.copy + ' Copy brief</button></div>' +
        '<div class="pl-mini"><button type="button" id="pl-dl">' + IC.download + ' Download brief</button><button type="button" id="pl-reset">' + IC.x + ' Start over</button></div></div>';
    }
  ];

  // ---- scope estimate (deliverables, NOT price)
  function tierFor(sid){
    var w = -1, d = S.details[sid] || {};
    Q[sid].forEach(function(q){
      var v = d[q.k]; if (v == null) return; var vs = Array.isArray(v) ? v : [v];
      vs.forEach(function(x){ q.o.forEach(function(o){ if (o[0] === x) w = Math.max(w, o[1]); }); });
    });
    if (w < 0) w = 1; // nothing picked -> middle package as a starting point
    var hint = S.tierHint[sid]; if (hint) w = Math.max(w, TIERS.indexOf(hint));
    return TIERS[w];
  }
  function scope(){
    return S.services.map(function(sid){
      var s = SV[sid], t = tierFor(sid), ti = TIERS.indexOf(t), items = [], d = S.details[sid] || {};
      s.compare.forEach(function(r){ var v = r[1+ti]; if (v === false) return; if (/^Revision/.test(r[0])) return; items.push(v === true ? r[0] : r[0] + ': ' + v); });
      var picks = [];
      Q[sid].forEach(function(q){ var v = d[q.k]; if (v == null || (Array.isArray(v) && !v.length)) return; picks.push((Array.isArray(v) ? v.join(', ') : v)); });
      var rev = s.compare.filter(function(r){ return /^Revision/.test(r[0]); })[0];
      if (rev) items.push(rev[1+ti] + ' revision rounds');
      return {id:sid, name:s.name, tier:t, tierName:TNAME[t], items:items, picks:picks};
    });
  }

  // ---- brief text
  function briefText(){
    var L = [], sc = scope();
    L.push('Hi Mogify Studio! Here is my project brief (' + S.ref + '):', '');
    L.push('*Services:* ' + (S.services.map(function(id){ return SV[id].name; }).join(', ') || 'Not chosen yet'));
    if (S.business || S.industry) L.push('*Business:* ' + [S.business, S.industry ? '(' + S.industry + ')' : ''].filter(Boolean).join(' '));
    if (S.goals.length) L.push('*Goals:* ' + S.goals.join(', '));
    sc.forEach(function(x){
      L.push('', '*' + x.name + '* (closest package: ' + x.tierName + ')');
      if (S.tierHint[x.id]) L.push('- Package I clicked on: ' + TNAME[S.tierHint[x.id]]);
      var d = S.details[x.id] || {};
      Q[x.id].forEach(function(q){ var v = d[q.k]; if (v == null || (Array.isArray(v) && !v.length)) return; L.push('- ' + q.l.replace(/\?$/, '') + ': ' + (Array.isArray(v) ? v.join(', ') : v)); });
    });
    L.push('');
    if (S.vibes.length) L.push('*Style:* ' + S.vibes.join(', '));
    if (S.colors.length) L.push('*Colours:* ' + S.colors.join(', '));
    if (S.refs.trim()) L.push('*References:* ' + S.refs.trim());
    if (S.assets.length) L.push('*I already have:* ' + S.assets.join(', '));
    if (S.time || S.date) L.push('*Timeline:* ' + [S.time, S.date ? 'deadline ' + S.date : ''].filter(Boolean).join(', '));
    if (S.budget) L.push('*Budget range:* ' + S.budget);
    L.push('', '*Name:* ' + (S.name || '-'));
    if (S.city) L.push('*Location:* ' + S.city);
    if (S.phone) L.push('*Phone:* ' + S.phone);
    if (S.email) L.push('*Email:* ' + S.email);
    L.push('*Best way to reach me:* ' + S.prefer);
    if (S.notes.trim()) L.push('*Notes:* ' + S.notes.trim());
    L.push('', '(Sent from the Project Planner on the Mogify Studio website)');
    return L.join('\n');
  }
  function waLink(){ return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(briefText()); }
  function mailLink(){ return 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Project brief ' + S.ref + (S.business ? ' – ' + S.business : '')) + '&body=' + encodeURIComponent(briefText().replace(/\*/g, '')); }
  window.MOGIFY_PLANNER = {brief: briefText, wa: waLink, state: function(){ return S; }};

  // ---- live summary card
  function row(h, inner){ return '<div class="pl-row"><h4>' + h + '</h4>' + inner + '</div>'; }
  function renderSummary(){
    var h = '';
    if (!S.services.length && !S.goals.length && !S.business) {
      sum.innerHTML = '<div class="pl-empty">' + IC.doc + '<p>Your brief builds here as you pick.<br>Start by choosing a service.</p></div>';
    } else {
      if (S.services.length) h += row('Services', '<div class="pl-pills">' + S.services.map(function(id){ return '<span>' + esc(SV[id].short) + '</span>'; }).join('') + '</div>');
      if (S.business || S.industry) h += row('Business', '<p>' + esc([S.business, S.industry].filter(Boolean).join(' · ')) + '</p>');
      if (S.goals.length) h += row('Goals', '<p>' + esc(S.goals.join(', ')) + '</p>');
      var sc = scope();
      if (sc.length) h += row('Estimated scope', '<div class="pl-scope">' + sc.map(function(x){ return '<div class="sc"><div class="sc-h"><b>' + esc(x.name) + '</b><em>' + x.tierName + '</em></div><ul>' + x.items.slice(0, 5).map(function(i){ return '<li>' + esc(i) + '</li>'; }).join('') + (x.items.length > 5 ? '<li>+' + (x.items.length - 5) + ' more</li>' : '') + '</ul></div>'; }).join('') + '</div>');
      if (S.vibes.length || S.colors.length) h += row('Style', '<p>' + esc(S.vibes.concat(S.colors).join(', ')) + '</p>');
      if (S.time || S.date) h += row('Timeline', '<p>' + esc([S.time, S.date].filter(Boolean).join(' · ')) + '</p>');
      if (S.budget) h += row('Budget range', '<p>' + esc(S.budget) + '</p>');
      if (S.name) h += row('Contact', '<p>' + esc([S.name, S.phone, S.email].filter(Boolean).join(' · ')) + '</p>');
      sum.innerHTML = h;
    }
    var n = S.services.length;
    peekSub.textContent = n ? (S.services.map(function(id){ return SV[id].short; }).join(' + ') + (S.budget ? ' · ' + S.budget : '')) : 'Nothing picked yet';
    var wa = $('#pl-wa'); if (wa) wa.href = waLink();
    var ml = $('#pl-mail'); if (ml) ml.href = mailLink();
  }

  // ---- navigation
  var dir = 1;
  function render(focus){
    form.innerHTML = '<div class="pl-step' + (dir < 0 ? ' back' : '') + '">' + R[S.step]() + '</div>';
    var pct = Math.round(S.step / (STEPS.length - 1) * 100);
    bar.style.width = Math.max(pct, 4) + '%'; bar.parentElement.setAttribute('aria-valuenow', pct);
    cnt.textContent = 'Step ' + (S.step + 1) + ' of ' + STEPS.length + ' · ' + STEPS[S.step];
    stepsEl.innerHTML = STEPS.map(function(n, i){ return '<button type="button" data-step="' + i + '" class="' + (i === S.step ? 'cur' : i <= S.max ? 'done' : '') + '"' + (i > S.max ? ' disabled' : '') + '><i>' + (i < S.step || (i <= S.max && i !== S.step) ? '✓' : i + 1) + '</i>' + n + '</button>'; }).join('');
    back.hidden = S.step === 0;
    var last = S.step === STEPS.length - 1;
    next.style.display = last ? 'none' : '';
    next.innerHTML = (S.step === STEPS.length - 2 ? 'Review brief ' : 'Next ') + IC.arrow;
    renderSummary(); save();
    if (focus) { var h2 = form.querySelector('h2'); if (h2) h2.focus({preventScroll:true}); var top = root.getBoundingClientRect().top + scrollY - 90; if (scrollY > top) scrollTo({top: top, behavior: 'smooth'}); }
    if (last) bindReview();
  }
  function err(m){ var e = $('#pl-err'); if (e) e.textContent = m; }
  function valid(){
    if (S.step === 0 && !S.services.length) { err('Pick at least one service to continue.'); return false; }
    if (S.step === 5 && !S.name.trim()) { err('Please add your name so Moiz knows who to reply to.'); var n = $('#pl-name'); if (n) n.focus(); return false; }
    return true;
  }
  function go(i){ if (i < 0 || i >= STEPS.length) return; dir = i > S.step ? 1 : -1; S.step = i; S.max = Math.max(S.max, i); render(true); }
  next.addEventListener('click', function(){ if (valid()) go(S.step + 1); });
  back.addEventListener('click', function(){ go(S.step - 1); });
  stepsEl.addEventListener('click', function(e){ var b = e.target.closest('[data-step]'); if (!b || b.disabled) return; var i = +b.dataset.step; if (i > S.step && !valid()) return; go(i); });

  // ---- input handling (delegated)
  function toggle(arr, v, max){ var i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else { arr.push(v); if (max && arr.length > max) arr.shift(); } return arr; }
  form.addEventListener('click', function(e){
    var b = e.target.closest('[data-g]'); if (!b) return;
    var g = b.dataset.g, v = b.dataset.v, multi = b.getAttribute('role') === 'checkbox';
    if (g.indexOf('d:') === 0) {
      var p = g.split(':'), sid = p[1], k = p[2]; S.details[sid] = S.details[sid] || {};
      if (multi) S.details[sid][k] = toggle(S.details[sid][k] || [], v); else S.details[sid][k] = S.details[sid][k] === v ? undefined : v;
    } else if (g === 'services') { toggle(S.services, v); err(''); }
    else if (g === 'vibes') toggle(S.vibes, v, 2);
    else if (Array.isArray(S[g])) toggle(S[g], v);
    else S[g] = (S[g] === v && g !== 'prefer') ? '' : v;
    // reflect state on siblings without re-rendering the whole step
    var box = b.parentElement;
    $$('[data-g="' + g + '"]', form).forEach(function(x){
      var on;
      if (g.indexOf('d:') === 0) { var p2 = g.split(':'), cur = (S.details[p2[1]] || {})[p2[2]]; on = Array.isArray(cur) ? cur.indexOf(x.dataset.v) >= 0 : cur === x.dataset.v; }
      else on = Array.isArray(S[g]) ? S[g].indexOf(x.dataset.v) >= 0 : S[g] === x.dataset.v;
      x.setAttribute('aria-checked', on ? 'true' : 'false');
    });
    b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop');
    renderSummary(); save();
  });
  form.addEventListener('input', function(e){ var f = e.target.dataset.f; if (!f) return; S[f] = e.target.value; if (f === 'name') err(''); renderSummary(); save(); });
  form.addEventListener('click', function(e){
    var c = e.target.closest('[data-cur]'); if (!c) return;
    S.cur = c.dataset.cur; S.budget = '';
    $$('[data-cur]', form).forEach(function(x){ x.setAttribute('aria-pressed', x.dataset.cur === S.cur); });
    $('#pl-budget').innerHTML = BUDGET[S.cur].map(function(b){ return chip('budget', b, false, false); }).join('');
    renderSummary(); save();
  });
  form.addEventListener('keydown', function(e){ if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); next.click(); } });

  // ---- review actions
  function toast(m){ var t = $('#pl-toast'); t.textContent = m; t.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(function(){ t.classList.remove('on'); }, 2600); }
  function bindReview(){
    var wa = $('#pl-wa'); if (wa) wa.addEventListener('click', function(){ confetti(); toast('Opening WhatsApp with your brief…'); });
    var cp = $('#pl-copy'); if (cp) cp.addEventListener('click', function(){
      var t = briefText().replace(/\*/g, '');
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function(){ toast('Brief copied'); }, function(){ var ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); toast('Brief copied'); } catch(e){} ta.remove(); });
    });
    var dl = $('#pl-dl'); if (dl) dl.addEventListener('click', function(){ var blob = new Blob([briefText().replace(/\*/g, '')], {type:'text/plain'}); var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'Mogify-brief-' + S.ref + '.txt'; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 500); });
    var rs = $('#pl-reset'); if (rs) rs.addEventListener('click', function(){ if (!confirm('Start a new brief? Your current answers will be cleared.')) return; S = fresh(); $('#pl-ref').textContent = S.ref; dir = -1; render(true); toast('Fresh brief started'); });
  }
  function confetti(){
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var cv = document.createElement('canvas'); cv.className = 'confetti'; document.body.appendChild(cv);
    var x = cv.getContext('2d'), W = cv.width = innerWidth, H = cv.height = innerHeight, P = [], cols = ['#00A99D', '#5FE0D5', '#121927', '#FFFFFF', '#FFD84D'];
    for (var i = 0; i < 120; i++) P.push({x: W/2, y: H*0.7, vx: (Math.random()-.5)*14, vy: -Math.random()*16-6, r: Math.random()*6+3, c: cols[i%cols.length], a: Math.random()*6});
    var t0 = performance.now();
    (function f(t){ x.clearRect(0,0,W,H); P.forEach(function(p){ p.vy += .45; p.x += p.vx; p.y += p.vy; p.a += .2; x.save(); x.translate(p.x,p.y); x.rotate(p.a); x.fillStyle = p.c; x.fillRect(-p.r/2,-p.r/2,p.r,p.r*.6); x.restore(); }); if (t - t0 < 2200) requestAnimationFrame(f); else cv.remove(); })(t0);
  }

  // ---- mobile summary sheet
  peek.addEventListener('click', function(){ var o = !side.classList.contains('open'); side.classList.toggle('open', o); peek.setAttribute('aria-expanded', o); });

  render(false);
})();
