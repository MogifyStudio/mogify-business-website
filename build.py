#!/usr/bin/env python3
"""Build the Mogify Studio business site into ./site.
DOMAIN SWAP: change BASE_URL below, run `python3 build.py`, republish. That's it.
PRICES: edit site/assets/js/config.js (no rebuild needed)."""
BASE_URL = "https://mogify-business.sites.tab.bot"   # <-- the ONE domain variable (no trailing slash)
LASTMOD = "2026-10-31"

import html, json, os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
exec(open(os.path.join(HERE, "content.py"), encoding="utf-8").read())
WORK = json.load(open(os.path.join(HERE, "work.json"), encoding="utf-8"))
SVC = {s["id"]: s for s in SERVICES}
WA_NUM = "923232194013"
EMAIL = "mogifystudio@gmail.com"
e = html.escape
PAGES = []  # (path, priority)

def ic(name, cls=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}>{ICONS[name]}</svg>'
def bi(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{BRAND_ICONS[name]}</svg>'
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
def wa(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text={quote(text)}"

def url(path): return BASE_URL + path

ORG_ID = BASE_URL + "/#org"
def org_ld():
    return {"@type": ["Organization", "ProfessionalService"], "@id": ORG_ID, "name": "Mogify Studio", "alternateName": "Mogify",
      "url": BASE_URL + "/", "logo": {"@type": "ImageObject", "url": BASE_URL + "/logo.png", "width": 880, "height": 880},
      "image": BASE_URL + "/og.png", "slogan": "Modify your brand with Mogify.",
      "description": "Web design, branding, UI/UX, motion graphics and 3D animation studio in Karachi, Pakistan, working with businesses in Pakistan and worldwide.",
      "email": EMAIL, "telephone": "+92 323 2194013",
      "address": {"@type": "PostalAddress", "addressLocality": "Karachi", "addressRegion": "Sindh", "addressCountry": "PK"},
      "areaServed": [{"@type": "City", "name": "Karachi"}, {"@type": "Country", "name": "Pakistan"}, "Worldwide"],
      "founder": {"@type": "Person", "name": "Muhammad Moiz Ali", "jobTitle": "Founder & Creative Director"},
      "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+92 323 2194013", "email": EMAIL, "availableLanguage": ["English", "Urdu"]},
      "knowsAbout": [s["name"] for s in SERVICES],
      "sameAs": [s[2] for s in SOCIALS]}

def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}
def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}

NAV = [("Services", "/services"), ("Packages", "/packages"), ("Work", "/work"), ("Planner", "/planner"), ("About", "/about"), ("Contact", "/contact")]

def header(active):
    links = []
    for n, p in NAV:
        cur = ' aria-current="page"' if active == p else ""
        if p == "/planner":
            links.append(f'<a href="{p}" class="nav-plan"{cur}>Project Planner <b>New</b></a>')
        else:
            links.append(f'<a href="{p}"{cur}>{n}</a>')
    mlinks = "".join(f'<a class="ml" href="{p}">{"Project Planner" if p=="/planner" else n}{" <small>NEW</small>" if p=="/planner" else ""}</a>' for n, p in [("Home","/")] + NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="hdr" id="top"><div class="wrap hdr-in">
  <a class="brand" href="/" aria-label="Mogify Studio home"><img src="/assets/brand/mogify-logo-dark.png" alt="Mogify Studio" width="751" height="233"></a>
  <nav class="nav" aria-label="Main">{''.join(links)}</nav>
  <div class="hdr-cta">
    <button class="lang-btn" type="button" data-lang-toggle aria-label="Switch key text to Urdu" lang="ur">اردو</button>
    <a class="btn btn-teal btn-sm btn-hdr" href="/planner" data-ur="پروجیکٹ شروع کریں">Start your project</a>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
</div></header>
<div class="mnav" id="mnav" aria-label="Mobile">{mlinks}
  <div class="mnav-ctas"><a class="btn btn-teal btn-lg" href="/planner">Start your project {ARR}</a><a class="btn btn-wa btn-lg" href="{wa('Hi Mogify Studio! I found you on your website and want to discuss a project.')}" target="_blank" rel="noopener">{bi('wa')} Chat on WhatsApp</a></div>
  <p class="mnav-meta">Mogify Studio · Karachi, Pakistan<br>{EMAIL}</p>
</div>"""

def footer():
    svc_links = "".join(f'<li><a href="/services/{s["slug"]}">{e(s["name"])}</a></li>' for s in SERVICES)
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Mogify Studio on {n}">{bi(k)}</a>' for k, n, u, h in SOCIALS)
    return f"""<footer class="ftr"><div class="wrap">
  <div class="ftr-top">
    <div class="fb"><img src="/assets/brand/mogify-logo-white.png" alt="Mogify Studio" width="592" height="187" loading="lazy"><p>A design and development studio in Karachi, Pakistan. Websites, brands, motion and 3D for businesses in Pakistan and worldwide.</p><div class="socials">{soc}</div></div>
    <div><h4>Services</h4><ul>{svc_links}</ul></div>
    <div><h4>Studio</h4><ul><li><a href="/packages">Packages</a></li><li><a href="/planner">Project Planner</a></li><li><a href="/work">Work</a></li><li><a href="/about">About</a></li><li><a href="/faq">FAQ</a></li><li><a href="/contact">Contact</a></li></ul></div>
    <div><h4>Contact</h4><ul><li><a href="{wa('Hi Mogify Studio! I want to discuss a project.')}" target="_blank" rel="noopener">WhatsApp +92 323 2194013</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><span>Karachi, Pakistan</span></li><li><a href="/contact#call">Book a call</a></li></ul></div>
  </div>
  <div class="ftr-big"><p>Modify your brand <em class="s">with Mogify.</em></p><a class="btn btn-teal btn-lg" href="/planner">Start your project {ARR}</a></div>
  <div class="ftr-bot"><span>© <span data-year>2026</span> Mogify Studio. All rights reserved.</span><span><a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="/sitemap.xml">Sitemap</a></span></div>
</div></footer>
<a class="fab" href="{wa('Hi Mogify Studio! I found you on your website and want to discuss a project.')}" target="_blank" rel="noopener" aria-label="Chat with Mogify Studio on WhatsApp">{bi('wa')}<span data-ur="واٹس ایپ پر بات کریں">Chat on WhatsApp</span></a>"""

def page(path, title, desc, body, ld=None, active=None, body_class="", scripts=(), priority=0.7, og_image="/og.png", noindex=False):
    graph = [org_ld(), {"@type": "WebPage", "@id": url(path) + "#page", "url": url(path), "name": title, "description": desc, "isPartOf": {"@type": "WebSite", "@id": BASE_URL + "/#site", "url": BASE_URL + "/", "name": "Mogify Studio", "publisher": {"@id": ORG_ID}}, "inLanguage": "en"}] + (ld or [])
    ldj = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    sc = "".join(f'<script src="{s}" defer></script>' for s in scripts)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    doc = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="Mogify Studio">
<meta name="theme-color" content="#121927">
<link rel="canonical" href="{url(path)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Mogify Studio"><meta property="og:locale" content="en_US">
<meta property="og:url" content="{url(path)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{url(og_image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Mogify Studio, web design, branding and motion studio in Karachi">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@mogifystudio"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{url(og_image)}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v=__V__">
<script>document.documentElement.classList.remove('no-js')</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body class="{body_class}">
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/config.js?v=__V__"></script>
<script src="/assets/js/site.js?v=__V__" defer></script>{sc}
</body>
</html>
"""
    out = os.path.join(SITE, "index.html" if path == "/" else path.strip("/") + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    if not noindex: PAGES.append((path, priority))

def sec_head(eyebrow, h, p="", center=False, tag="h2", hid=None):
    return f'<div class="sec-head{" center" if center else ""} rv"><span class="eyebrow">{eyebrow}</span><{tag} class="h2"{(" id=%s" % chr(34)+hid+chr(34)) if hid else ""}>{h}</{tag}>{f"<p class=lead>{p}</p>" if p else ""}</div>'

def crumbs(items):
    parts = []
    for i, (n, p) in enumerate(items):
        if i: parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{p}">{e(n)}</a>' if i < len(items)-1 else f'<span aria-current="page">{e(n)}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'

def phero(eyebrow, h1, lead, items, ctas="", extra="", h1_ur=None, lead_ur=None, side=""):
    u1 = f' data-ur="{e(h1_ur)}"' if h1_ur else ""
    u2 = f' data-ur="{e(lead_ur)}"' if lead_ur else ""
    return f"""<section class="phero{' has-side' if side else ''}"><div class="hero-bg" aria-hidden="true"></div><div class="wrap{' sh-grid' if side else ''}"><div class="phero-in">
{crumbs(items)}{extra}<span class="eyebrow">{eyebrow}</span><h1 class="h1"{u1}>{h1}</h1><p class="lead"{u2}>{lead}</p>{f'<div class="hero-ctas">{ctas}</div>' if ctas else ''}
</div>{side}</div></section>"""

def faq_block(faqs, open_first=True):
    return '<div class="faq">' + "".join(f'<details class="qa rv"{" open" if (i==0 and open_first) else ""}><summary>{e(q)}<i aria-hidden="true"></i></summary><div class="ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(faqs)) + "</div>"

def cta_band(h="Your project could be <em class='s'>next.</em>", p="Tell us what you need in about two minutes with the Project Planner, or just say hi on WhatsApp. Moiz, the founder, replies personally.", wa_text="Hi Mogify Studio! I want to start a project."):
    return f"""<section class="sec"><div class="wrap"><div class="cta-band rv">
<span class="eyebrow">Let's work together</span>
<h2 class="h2" data-ur="اگلا پروجیکٹ آپ کا ہو سکتا ہے۔">{h}</h2>
<p data-ur="پروجیکٹ پلانر میں دو منٹ میں بتائیں کہ آپ کو کیا چاہیے، یا واٹس ایپ پر سلام کریں۔ معیز خود جواب دیتے ہیں۔">{p}</p>
<div class="row"><a class="btn btn-teal btn-lg" href="/planner"><span data-ur="اپنا پروجیکٹ شروع کریں">Start your project</span> {ARR}</a><a class="btn btn-ghost btn-lg" href="{wa(wa_text)}" target="_blank" rel="noopener">{bi('wa')} <span data-ur="واٹس ایپ پر بات کریں">Chat on WhatsApp</span></a></div>
</div></div></section>"""

def svc_card(s, i):
    return f"""<a class="svc rv{' d'+str(i%3) if i%3 else ''}" href="/services/{s['slug']}"><span class="svc-num">{i+1:02d}</span><span class="svc-ic">{ic(s['id'])}</span><h3>{e(s['name'])}</h3><p>{e(s['card'])}</p><span class="svc-go">Explore {e(s['short']) if s['id'] in ('uiux','anim3d') else e(s['short'].lower())} {ic('arrow')}</span></a>"""

def val_html(v):
    if v is True: return ic("check")
    if v is False: return '<span class="no" aria-label="Not included"></span>'
    return e(str(v))

def tier_cards(s):
    out = []
    for tid, tname, tfor in s["tiers"]:
        idx = ["starter", "growth", "premium"].index(tid)
        feats = []
        for row in s["compare"]:
            v = row[1 + idx]
            if v is False: continue
            label = row[0]
            feats.append(f'<li>{ic("check")}<span>{e(label)}{": <b>"+e(str(v))+"</b>" if v is not True else ""}</span></li>')
        rec = tid == RECOMMENDED
        msg = f"Hi Mogify Studio! I'm interested in the {s['name']} {tname} package. Can you share a quote?"
        steps = "".join(f"<li>{e(x)}</li>" for x in TIER_STEPS[tid])
        out.append(f"""<article class="tier{' rec' if rec else ''} rv{' d'+str(idx) if idx else ''}">{'<span class="rec-tag">Recommended</span>' if rec else ''}
<div class="tier-head"><span class="tn">{tname}</span><h3>{e(s['short'] if s['id']!='uiux' else 'UI/UX')} {tname}</h3><p class="for">{e(tfor)}</p></div>
<div class="price"><span class="pv" data-price="{s['id']}.{tid}">Price on request</span><span class="pn" data-price-note>Fixed quote after a quick brief</span></div>
<ul class="tier-feats">{''.join(feats)}</ul>
<div class="tier-acts"><a class="btn {'btn-teal' if rec else 'btn-ghost' if not rec else ''} btn-block" href="{wa(msg)}" target="_blank" rel="noopener" data-quote="{s['id']}.{tid}" data-pkg="{e(s['name'])} {tname}">{bi('wa')} <span data-ur="کوٹ حاصل کریں">Get a quote</span></a><a class="btn {'btn-white' if rec else 'btn-ghost'} btn-block btn-sm" href="/planner?service={s['id']}&amp;tier={tid}">Plan this in detail {ARR}</a></div>
<details><summary>How it's delivered</summary><ol>{steps}</ol></details>
</article>""")
    return '<div class="tiers">' + "".join(out) + "</div>"

def compare_table(s):
    rows = [f'<div class="cmp-row hd" role="row"><span class="f" role="columnheader">What\'s included</span>' + "".join(f'<span class="v{" rec" if tid==RECOMMENDED else ""}" role="columnheader">{tn}</span>' for tid, tn, _ in s["tiers"]) + "</div>"]
    for r in s["compare"]:
        rows.append(f'<div class="cmp-row" role="row"><span class="f" role="rowheader">{e(r[0])}</span>' + "".join(f'<span class="v" role="cell">{val_html(v)}</span>' for v in r[1:]) + "</div>")
    rows.append('<div class="cmp-row" role="row"><span class="f" role="rowheader">Price</span>' + "".join(f'<span class="v" role="cell" data-price="{s["id"]}.{tid}" data-short>On request</span>' for tid, _, _ in s["tiers"]) + "</div>")
    return f'<div class="cmp rv" role="table" aria-label="{e(s["name"])} packages compared">' + "".join(rows) + "</div>"

def work_tiles(items, cls="gal"):
    out = []
    for w in items:
        if w.get("href"):
            out.append(f'<a class="{"web" if w["cat"]=="web" else ""}" href="{w["href"]}"{" target=_blank rel=noopener" if w["href"].startswith("http") else ""} aria-label="{e(w["title"])}"><img src="{w["img"]}" alt="{e(w["alt"])}" loading="lazy" decoding="async" width="{w["w"]}" height="{w["h"]}"></a>')
        else:
            out.append(f'<button type="button" class="{"web" if w["cat"]=="web" else ""}" data-lb data-full="{w["full"]}" data-title="{e(w["title"])}" data-sub="{e(w["sub"])}"{" data-video" if w.get("video") else ""} aria-label="Open {e(w["title"])}"><img src="{w["img"]}" alt="{e(w["alt"])}" loading="lazy" decoding="async" width="{w["w"]}" height="{w["h"]}"></button>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"

LIGHTBOX = f'<div class="lb" role="dialog" aria-modal="true" aria-label="Work viewer" hidden><button class="lb-x" type="button" aria-label="Close">{ic("x")}</button><button class="lb-p" type="button" aria-label="Previous">{ic("left")}</button><button class="lb-n" type="button" aria-label="Next">{ic("right")}</button><figure><div class="lb-media"></div><figcaption></figcaption></figure></div>'

def W_(cat=None, n=None, sub3=None):
    xs = [w for w in WORK if (cat is None or w["cat"] == cat) and (sub3 is None or w.get("sub3") == sub3)]
    return xs[:n] if n else xs

# ============================== HOME ==============================
def build_home():
    def card(img, cls, tag, alt):
        return f'<div class="card3d {cls}" data-depth><img src="{img}" alt="{e(alt)}" width="720" height="900" decoding="async"{" fetchpriority=high" if cls=="c1" else " loading=lazy"}><span class="tag">{tag}</span></div>'
    stack = f"""<div class="stack" aria-label="A stack of Mogify Studio work" role="img">
  <div class="stack-scene" id="stack">
    {card('/assets/img/work/social-fermentation-found-fire-12.webp','c2','Social campaign','Fermentation Found Fire social campaign')}
    {card('/assets/img/work/book-z-steals-the-spotlight-45.webp','c3','Book cover','Z Steals the Spotlight book cover')}
    {card('/assets/img/work/brand-the-notceb-financial-group-4-lg.webp','c1','Brand identity','The Notceb Financial Group brand identity')}
    {card('/assets/img/work/logo-pizza-cat-32.webp','c4','Logo','Pizza Cat mascot logo')}
    {card('/assets/video/cloth-reveal.webp','c5','3D motion','3D cloth reveal animation')}
  </div>
  <div class="chip-float chip-a"><span class="dot">{ic('doc')}</span><span>Plan your project<small>Brief to WhatsApp in 1 tap</small></span></div>
  <div class="chip-float chip-b"><span class="dot">{ic('check')}</span><span>See your scope<small>Deliverables before you pay</small></span></div>
</div>"""
    words = ["websites", "brands", "logos", "reels", "3D ads"]
    rot = "".join(f'<span{" class=on" if i==0 else ""}>{w}</span>' for i, w in enumerate(words))
    hero = f"""<section class="hero"><div class="hero-bg" aria-hidden="true"></div><div class="wrap hero-grid">
<div class="hero-copy">
  <span class="hero-badge rv"><i>Booking projects</i> <span><span class="hb-long">Web · Brand · Motion </span>Studio in Karachi</span></span>
  <h1 class="h1 rv d1" data-ur="ویب سائٹس، برانڈز اور موشن جو آپ کو کلائنٹس دلائیں۔">We build <span class="rot teal" aria-hidden="true">{rot}</span><span class="sr-only">websites, brands, logos, reels and 3D ads</span><br>that win you <em class="s">clients.</em></h1>
  <p class="lead rv d2" data-ur="موگیفائی اسٹوڈیو کراچی کا ڈیزائن اور ڈیولپمنٹ اسٹوڈیو ہے۔ ہم پاکستان اور دنیا بھر کے اسٹارٹ اپس اور بڑھتے ہوئے کاروباروں کے لیے ویب سائٹس، برانڈ آئیڈینٹیٹی اور موشن ڈیزائن بناتے ہیں۔">Mogify Studio is a design and development studio in Karachi. We create websites, brand identities, motion and 3D for startups and growing businesses in Pakistan and worldwide.</p>
  <div class="hero-ctas rv d2"><a class="btn btn-teal btn-lg" href="/planner"><span data-ur="اپنا پروجیکٹ شروع کریں">Start your project</span> {ARR}</a><a class="btn btn-ghost btn-lg" href="/packages"><span data-ur="پیکجز دیکھیں">See packages</span></a></div>
  <ul class="hero-points rv d3"><li>{ic('check-c')}Fixed quote before we start</li><li>{ic('check-c')}Talk directly to the founder</li><li>{ic('check-c')}Hand-coded, mobile-first</li></ul>
</div>
{stack}
</div></section>"""
    mq_items = [s["name"] for s in SERVICES]
    marquee = '<div class="marquee" aria-hidden="true"><div class="marquee-track">' + "".join(f"<span>{e(x)}</span>" for x in mq_items*2) + "</div></div>"
    principles = [("wallet","Clear scope, fixed quote","You see exactly what is included before any work begins. No surprise invoices."),("user","Founder-led","You work with Muhammad Moiz Ali directly. No middlemen, no lost messages."),("spark","Made from scratch","No templates. Every logo, layout and animation is designed for your brand."),("bolt","Built for phones","Mobile-first, hand-coded and fast, because that is where your customers are.")]
    why = f"""<section class="sec" aria-labelledby="why-t"><div class="wrap">
{sec_head("Why Mogify", "One studio for your whole brand, <em class='s'>start to launch.</em>", "Website, logo, brand identity, motion and 3D under one roof, so everything looks like it belongs to the same serious business.", hid="why-t")}
<div class="principles rv">{''.join(f'<div class="principle">{ic(a)}<h3>{e(b)}</h3><p>{e(c)}</p></div>' for a,b,c in principles)}</div>
</div></section>"""
    services = f"""<section class="sec sec-soft" aria-labelledby="svc-t"><div class="wrap">
<div class="sec-head-row">{sec_head("Services", "Everything your brand needs to <em class='s'>look the part.</em>", hid="svc-t")}<a class="link-arrow rv" href="/services">All services {ic('arrow')}</a></div>
<div class="svc-grid">{''.join(svc_card(s,i) for i,s in enumerate(SERVICES))}</div>
</div></section>"""
    pals = [("Mogify","#121927","#00A99D","#FFFFFF","Manrope"),("Luxe","#1C1A17","#C9A96E","#F6F1E7","Fraunces"),("Fresh","#0E3B2E","#B6F09C","#FFFFFF","Manrope"),("Bold","#2B0B3F","#FF5C39","#FFFFFF","Manrope"),("Ocean","#0B2A4A","#5BC0EB","#FFFFFF","Manrope")]
    sw = "".join(f'<button type="button" class="sw" aria-pressed="{"true" if i==0 else "false"}" data-a="{a}" data-b="{b}" data-c="{c}" data-f="{f}"><i style="--a:{a};--b:{b}"></i>{n}</button>' for i,(n,a,b,c,f) in enumerate(pals))
    play = f"""<section class="sec sec-dark" aria-labelledby="play-t" id="playground"><div class="wrap play">
<div class="play-ctrl">
  <div class="sec-head rv" style="margin-bottom:0"><span class="eyebrow">Brand playground</span><h2 class="h2" id="play-t">See your name, <em class="s teal">Mogified.</em></h2><p class="lead">Type your business name and pick a mood. Watch one name carry across a card, a post, a website and an app icon, the way a real identity should.</p></div>
  <div class="field rv"><label for="pg-name">Your business name</label><input class="inp" id="pg-name" maxlength="28" placeholder="e.g. Chai Corner" autocomplete="organization"></div>
  <div class="field rv"><span class="lbl" id="pg-mood">Pick a mood</span><div class="swatches" role="group" aria-labelledby="pg-mood">{sw}</div></div>
  <div class="rv"><a class="btn btn-teal btn-lg" id="pg-go" href="/planner?service=brand">Make it real {ARR}</a></div>
  <p class="play-note rv">A quick preview only. Your real logo and identity are designed by hand, from scratch.</p>
</div>
<div class="mock-grid rv" id="mocks" aria-live="polite">
  <div class="mock mk-card"><div class="row"><span class="mono" data-mono>YB</span><span class="mk-name" data-name>Your Brand</span></div><div class="meta">Your Name · Founder<br>hello@<span data-slug>yourbrand</span>.com</div></div>
  <div class="mock mk-post"><span class="pill">NOW OPEN</span><span class="big"><span data-name>Your Brand</span><br>is here.</span></div>
  <div class="mock mk-web"><div class="bar"><i></i><i></i><i></i><span>www.<span data-slug>yourbrand</span>.com</span></div><div class="pg"><div class="nv"><span class="mono" data-mono>YB</span><b data-name>Your Brand</b><em>Order now</em></div><h4>Made for you. <span>Loved by Karachi.</span></h4><div class="ln"></div><div class="ln s"></div></div></div>
  <div class="mock mk-app"><span class="ico" data-mono>YB</span><small data-name>Your Brand</small></div>
</div>
</div></section>"""
    sel = [
      ("t-a", "/assets/img/work/brand-the-notceb-financial-group-4-lg.webp", "The Notceb Financial Group", "Brand identity", "/work#brand", ""),
      ("t-b t-web", "/assets/img/web/aurelle-coffee.webp", "Aurelle Coffee", "Concept website", "/work/aurelle-coffee", ""),
      ("t-c", "/assets/img/work/brand-sho-es-game-on-5-lg.webp", "Sho'es: Game On", "Brand identity", "/work#brand", ""),
      ("t-d", "/assets/img/work/social-fermentation-found-fire-12.webp", "Fermentation Found Fire", "Social campaign", "/work#social", ""),
      ("t-e", "/assets/img/work/brand-paula-etc-maison-de-beaut-6-lg.webp", "Paula Etc. Maison de Beauté", "Brand identity", "/work#brand", ""),
    ]
    tiles = "".join(f'<a class="tile {c} rv" href="{h}"><img src="{im}" alt="{e(t)}, {e(s.lower())} by Mogify Studio" loading="lazy" decoding="async"><span class="cap"><b>{e(t)}<small>{e(s)}</small></b><span class="go">{ic("arrow-ur")}</span></span></a>' for c,im,t,s,h,_ in sel)
    work = f"""<section class="sec" aria-labelledby="work-t"><div class="wrap">
<div class="sec-head-row">{sec_head("Selected work", "Work that makes brands <em class='s'>look expensive.</em>", hid="work-t")}<a class="link-arrow rv" href="/work">See all work {ic('arrow')}</a></div>
<div class="bento">{tiles}</div>
</div></section>"""
    pt = f"""<section class="sec sec-soft" aria-labelledby="pt-t"><div class="wrap pt">
<div class="sec-head rv" style="margin-bottom:0"><span class="eyebrow">Project Planner · New</span><h2 class="h2" id="pt-t">Plan your project in <em class="s">two minutes.</em></h2><p class="lead">Pick what you need, choose your style, timeline and budget range, and watch your project scope build itself as you go. One tap sends the full brief to Moiz on WhatsApp.</p>
<ul class="checks" style="margin-top:8px"><li>{ic('check-c')}See your deliverables list before you talk to anyone</li><li>{ic('check-c')}Your goals, your timeline, your budget range, in one clear brief</li><li>{ic('check-c')}No forms lost in an inbox: it lands straight in WhatsApp</li></ul>
<div style="margin-top:10px"><a class="btn btn-teal btn-lg" href="/planner"><span data-ur="پروجیکٹ پلان کریں">Plan my project</span> {ARR}</a></div></div>
<div class="pt-demo rv d1" aria-hidden="true">
 <div class="pt-bar"><i></i></div>
 <p class="pt-q">What do you need?</p>
 <div class="pt-opts"><span class="pt-opt on">{ic('web')}Website</span><span class="pt-opt on">{ic('logo')}Logo</span><span class="pt-opt">{ic('motion')}Motion</span><span class="pt-opt">{ic('social')}Social posts</span><span class="pt-opt">{ic('anim3d')}3D animation</span><span class="pt-opt">{ic('book')}Book cover</span></div>
 <div class="pt-sum"><span class="wa">{bi('wa')}</span><span>Brief ready to send<small>Website (up to 5 pages) · Logo · Minimal style</small></span></div>
</div>
</div></section>"""
    s = SVC["web"]
    pk = f"""<section class="sec" aria-labelledby="pk-t"><div class="wrap">
{sec_head("Packages", "Clear packages. <em class='s'>No guesswork.</em>", "Every service comes in three packages with exactly what is included. Here is web design; see packages for logos, branding, motion, 3D and more.", center=True, hid="pk-t")}
{tier_cards(s)}
<p class="rv" style="text-align:center;margin-top:36px"><a class="link-arrow" href="/packages">Compare all packages {ic('arrow')}</a></p>
</div></section>"""
    proc = [("01","Brief","Tell us what you need in the Project Planner or on WhatsApp. We ask the right questions."),("02","Quote & plan","You get a clear scope, fixed quote and timeline. Work starts when you are happy."),("03","Design & build","We design, build and share progress at clear checkpoints for your feedback."),("04","Launch & handover","Final files, launch and a walkthrough, so you own everything and know how to use it.")]
    process = f"""<section class="sec sec-dark" aria-labelledby="pr-t"><div class="wrap">
{sec_head("How it works", "From first message to launch, <em class='s teal'>in four clear steps.</em>", hid="pr-t")}
<div class="process">{''.join(f'<div class="step rv{" d"+str(i) if i else ""}"><span class="n">STEP {n}</span><h3>{t}</h3><p>{d}</p></div>' for i,(n,t,d) in enumerate(proc))}</div>
</div></section>"""
    faq = f"""<section class="sec sec-soft" aria-labelledby="faq-t"><div class="wrap faq-grid">
<div class="sec-head rv"><span class="eyebrow">FAQ</span><h2 class="h2" id="faq-t">Questions, <em class="s">answered.</em></h2><p class="lead">Anything else? Ask on WhatsApp and you will hear back from Moiz.</p><div><a class="link-arrow" href="/faq">All FAQs {ic('arrow')}</a></div></div>
{faq_block(HOME_FAQS[:6])}
</div></section>"""
    body = hero + marquee + why + services + play + work + pt + pk + process + faq + cta_band()
    page("/", "Mogify Studio | Web Design, Branding & Motion Agency in Karachi", "Mogify Studio is a web design and branding agency in Karachi, Pakistan. Websites, logo design, brand identity, UI/UX, motion graphics and 3D animation with clear packages.", body, ld=[faq_ld(HOME_FAQS[:6])], active="/", body_class="home", priority=1.0)

# ============================== SERVICES ==============================
def build_services():
    body = phero("Services", "Design, development and motion, <em class='s teal'>all in one studio.</em>", "Nine services that work together, so your website, logo, social posts and videos all look like the same brand. Pick one, or combine them in the Project Planner.", [("Home","/"),("Services","/services")], ctas=f'<a class="btn btn-teal btn-lg" href="/planner">Start your project {ARR}</a><a class="btn btn-ghost btn-lg" href="/packages">See packages</a>')
    body += f'<section class="sec" style="padding-top:20px"><div class="wrap"><div class="svc-grid">{"".join(svc_card(s,i) for i,s in enumerate(SERVICES))}</div></div></section>'
    proc = [("01","Brief"),("02","Quote & plan"),("03","Design & build"),("04","Launch & handover")]
    body += cta_band()
    ld = [crumbs_ld([("Home","/"),("Services","/services")]), {"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":url("/services/"+s["slug"]),"name":s["name"]} for i,s in enumerate(SERVICES)]}]
    page("/services", "Services | Web Design, Branding, Motion & 3D | Mogify Studio", "Website design and development, logo design, brand identity, UI/UX, motion graphics, 3D animation, social media creatives, book covers and video editing from Mogify Studio, Karachi.", body, ld=ld, active="/services", priority=0.9)

def work_for(s):
    m = {"web": W_("web"), "logo": W_("logo", 8), "brand": W_("brand"), "product": W_("product"), "motion": W_("motion", sub3="motion"), "motion3d": W_("motion"), "social": W_("social", 8), "book": W_("book")}
    xs = []
    for k in s["work"]: xs += m[k]
    if s["id"] == "video": xs = W_("motion") + W_("social", 4)
    return xs[:8]

def build_service(s):
    path = f"/services/{s['slug']}"
    items = [("Home","/"),("Services","/services"),(s["name"], path)]
    extra = f'<span class="svc-hero-ic">{ic(s["id"])}</span>'
    ctas = f'<a class="btn btn-teal btn-lg" href="/planner?service={s["id"]}">Plan your {s["noun"]} project {ARR}</a><a class="btn btn-ghost btn-lg" href="/packages#{s["id"]}">See packages</a>'
    wk = work_for(s)
    side = ""
    if len(wk) >= 2:
        a, b2 = wk[0], wk[1]
        side = f'<div class="sh-vis" aria-hidden="true"><img class="sv1" src="{a["img"]}" alt="" width="{a["w"]}" height="{a["h"]}"><img class="sv2" src="{b2["img"]}" alt="" width="{b2["w"]}" height="{b2["h"]}" loading="lazy"></div>'
    body = phero(e(s["name"]), e(s["tagline"]), e(s["intro"]), items, ctas=ctas, extra=extra, side=side)
    dv = "".join(f'<div class="dv rv{" d"+str(i%3) if i%3 else ""}"><span class="k">{ic("check")}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i,(a,b) in enumerate(s["deliverables"]))
    body += f'<section class="sec sec-soft" aria-labelledby="dv-t"><div class="wrap">{sec_head("What you get", "Everything included, <em class=s>spelled out.</em>", hid="dv-t")}<div class="deliv">{dv}</div></div></section>'
    steps = "".join(f'<div class="step rv{" d"+str(i) if i else ""}"><span class="n">STEP 0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i,(a,b) in enumerate(s["process"]))
    body += f'<section class="sec sec-dark" aria-labelledby="pr-t"><div class="wrap"><div class="split" style="margin-bottom:clamp(36px,5vw,56px)"><div class="sec-head rv" style="margin-bottom:0"><span class="eyebrow">Process</span><h2 class="h2" id="pr-t">How a {s["noun"]} project <em class="s teal">runs.</em></h2></div><div class="rv"><p class="lead" style="margin-bottom:18px">Ideal for:</p><ul class="ideal">{"".join(f"<li>{e(x)}</li>" for x in s["ideal"])}</ul></div></div><div class="process">{steps}</div></div></section>'
    body += f'<section class="sec" aria-labelledby="pk-t" id="packages"><div class="wrap">{sec_head("Packages", e(s["name"])+" <em class=s>packages.</em>", "Three clear starting points. Not sure which fits? The Project Planner suggests one for you.", center=True, hid="pk-t")}{tier_cards(s)}{compare_table(s)}</div></section>'
    wk = work_for(s)
    if wk:
        body += f'<section class="sec sec-soft" aria-labelledby="wk-t"><div class="wrap"><div class="sec-head-row">{sec_head("Work", "Recent <em class=s>work.</em>", hid="wk-t")}<a class="link-arrow rv" href="/work">See all work {ic("arrow")}</a></div>{work_tiles(wk)}</div></section>'
    body += f'<section class="sec" aria-labelledby="fq-t"><div class="wrap faq-grid"><div class="sec-head rv"><span class="eyebrow">FAQ</span><h2 class="h2" id="fq-t">{e(s["short"]) if s["id"]!="uiux" else "UI/UX"} <em class="s">questions.</em></h2></div>{faq_block(s["faqs"] + HOME_FAQS[:2])}</div></section>'
    others = "".join(f'<a href="/services/{o["slug"]}">{ic(o["id"])}{e(o["name"])}</a>' for o in SERVICES if o["id"] != s["id"])
    body += f'<section class="sec sec-soft" style="padding-block:clamp(56px,7vw,96px)"><div class="wrap"><h2 class="h3 rv" style="margin-bottom:24px">More from Mogify</h2><div class="svc-more rv">{others}</div></div></section>'
    body += cta_band(wa_text=f"Hi Mogify Studio! I'm interested in {s['name']}.")
    body += LIGHTBOX
    svc_ld = {"@type":"Service","@id":url(path)+"#service","name":s["name"],"serviceType":s["name"],"description":s["intro"],"provider":{"@id":ORG_ID},"areaServed":[{"@type":"City","name":"Karachi"},{"@type":"Country","name":"Pakistan"},"Worldwide"],"url":url(path),
      "hasOfferCatalog":{"@type":"OfferCatalog","name":s["name"]+" packages","itemListElement":[{"@type":"Offer","name":f"{s['short']} {tn}","description":tf,"url":url(path)+"#packages","seller":{"@id":ORG_ID}} for tid,tn,tf in s["tiers"]]}}
    page(path, f"{s['title']} | Mogify Studio", (s["tagline"] + " " + s["card"] + " Packages from Mogify Studio, Karachi.")[:300], body, ld=[svc_ld, crumbs_ld(items), faq_ld(s["faqs"] + HOME_FAQS[:2])], active="/services", priority=0.8)

# ============================== PACKAGES ==============================
def build_packages():
    items = [("Home","/"),("Packages","/packages")]
    body = phero("Packages & pricing", "Clear packages for <em class='s teal'>every stage</em> of your brand.", "Pick a service to see its three packages and exactly what is included. Every quote is fixed before work starts, and you can mix services into one custom package in the Project Planner.", items, ctas=f'<a class="btn btn-teal btn-lg" href="/planner">Build a custom package {ARR}</a>', h1_ur="ہر مرحلے کے لیے واضح پیکجز", lead_ur="سروس منتخب کریں اور دیکھیں ہر پیکج میں کیا شامل ہے۔ کام شروع ہونے سے پہلے قیمت طے ہو جاتی ہے۔")
    tabs = "".join(f'<button class="tab" role="tab" type="button" id="tab-{s["id"]}" aria-controls="panel-{s["id"]}" aria-selected="{"true" if i==0 else "false"}" data-tab="{s["id"]}">{ic(s["id"])}{e(s["short"])}</button>' for i,s in enumerate(SERVICES))
    panels = "".join(f'<div class="pkg-panel" role="tabpanel" id="panel-{s["id"]}" aria-labelledby="tab-{s["id"]}"{"" if i==0 else " hidden"}><div class="sec-head-row" style="margin:36px 0 40px"><div class="sec-head" style="margin:0"><h2 class="h2">{e(s["name"])}</h2><p class="lead">{e(s["tagline"])}</p></div><a class="link-arrow" href="/services/{s["slug"]}">About this service {ic("arrow")}</a></div>{tier_cards(s)}{compare_table(s)}</div>' for i,s in enumerate(SERVICES))
    body += f'<section class="sec" style="padding-top:8px" aria-label="Packages by service"><div class="wrap"><div class="tabs" role="tablist" aria-label="Choose a service">{tabs}</div>{panels}</div></section>'
    ad = "".join(f'<div class="addon rv{" d"+str(i%3) if i%3 else ""}"><h3>{e(n)}</h3><p>{e(d)}</p><div class="ap"><span data-addon="{k}">On request</span><a href="{wa("Hi Mogify Studio! I would like to add: " + n + ". Can you share a quote?")}" target="_blank" rel="noopener">Ask {ic("arrow")}</a></div></div>' for i,(k,n,d) in enumerate(ADDONS))
    body += f'<section class="sec sec-soft" aria-labelledby="ad-t"><div class="wrap">{sec_head("Add-ons", "Extras you can add <em class=s>to any package.</em>", hid="ad-t")}<div class="addons">{ad}</div></div></section>'
    body += f"""<section class="sec" aria-labelledby="cu-t"><div class="wrap"><div class="pt">
<div class="sec-head rv" style="margin-bottom:0"><span class="eyebrow">Custom package</span><h2 class="h2" id="cu-t">Need a mix? <em class="s">Build your own.</em></h2><p class="lead">Launching a business usually needs more than one thing: a logo, a website, social posts and a launch reel. Pick everything in the Project Planner and get one package and one quote for all of it.</p><div style="margin-top:10px"><a class="btn btn-teal btn-lg" href="/planner">Open the Project Planner {ARR}</a></div></div>
<div class="rv d1"><ul class="checks">{''.join(f'<li>{ic("check-c")}{x}</li>' for x in ['Every quote is fixed before work starts','Revision rounds included in every package','Pay in clear milestones, agreed in your quote','Final files are handed over at the end'])}</ul></div>
</div></div></section>"""
    pfaq = [("Why does it say “Price on request”?", "Every project is a little different, so we confirm a fixed price after a quick brief. Send your brief through the Project Planner or tap “Get a quote” and you will get a clear number before anything starts."),("Can I change what is in a package?", "Yes. Packages are starting points. Tell us what you need to add or remove and we will adjust the quote."), ("Can I combine several services into one project?", "Yes. Pick everything you need in the Project Planner and Moiz will quote it as one project, with one plan and one point of contact.")] + HOME_FAQS[1:2] + HOME_FAQS[4:5]
    body += f'<section class="sec sec-soft" aria-labelledby="pf-t"><div class="wrap faq-grid"><div class="sec-head rv"><span class="eyebrow">FAQ</span><h2 class="h2" id="pf-t">About <em class="s">pricing.</em></h2></div>{faq_block(pfaq)}</div></section>'
    body += cta_band()
    offers = {"@type":"OfferCatalog","name":"Mogify Studio packages","itemListElement":[{"@type":"OfferCatalog","name":s["name"],"itemListElement":[{"@type":"Offer","name":f"{s['short']} {tn}","description":tf,"url":url("/services/"+s["slug"])+"#packages","itemOffered":{"@type":"Service","name":s["name"]},"seller":{"@id":ORG_ID}} for tid,tn,tf in s["tiers"]]} for s in SERVICES]}
    page("/packages", "Packages & Pricing | Website, Logo & Branding Packages | Mogify Studio", "Website, logo, branding, UI/UX, motion, 3D, social media, book cover and video editing packages from Mogify Studio, Karachi. See what is included and get a fixed quote.", body, ld=[crumbs_ld(items), offers, faq_ld(pfaq)], active="/packages", priority=0.9, scripts=["/assets/js/packages.js?v=__V__"])

# ============================== PLANNER ==============================
def build_planner():
    items = [("Home","/"),("Project Planner","/planner")]
    body = f"""<section class="phero pl-hero"><div class="hero-bg" aria-hidden="true"></div><div class="wrap"><div class="phero-in">
{crumbs(items)}<span class="eyebrow">Project Planner</span><h1 class="h1" data-ur="دو منٹ میں اپنا پروجیکٹ پلان کریں۔">Plan your project in <em class="s teal">two minutes.</em></h1>
<p class="lead" data-ur="سروس، مقاصد، اسٹائل، ٹائم لائن اور بجٹ منتخب کریں۔ آپ کا مکمل بریف ایک ٹیپ میں واٹس ایپ پر معیز تک پہنچ جائے گا۔">Answer a few quick taps. Your brief and project scope build live as you go, and one tap sends everything to Moiz on WhatsApp or email.</p>
</div></div></section>
<section class="sec planner-sec" style="padding-top:0"><div class="wrap">
<div class="planner" id="planner" data-wa="{WA_NUM}" data-email="{EMAIL}">
  <div class="pl-main">
    <div class="pl-top"><div class="pl-steps" id="pl-steps" aria-hidden="true"></div><div class="pl-progress" role="progressbar" aria-label="Planner progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="pl-bar"></i></div><p class="pl-count" id="pl-count" aria-live="polite">Step 1 of 7</p></div>
    <form class="pl-form" id="pl-form" novalidate autocomplete="on"><noscript><p>The planner needs JavaScript. You can also <a href="{wa('Hi Mogify Studio! I want to start a project.')}">send your brief on WhatsApp</a>.</p></noscript></form>
    <div class="pl-nav"><button type="button" class="btn btn-ghost" id="pl-back">{ic('left')} Back</button><button type="button" class="btn btn-teal" id="pl-next">Next {ARR}</button></div>
  </div>
  <aside class="pl-side" id="pl-side" aria-label="Your brief">
    <button type="button" class="pl-peek" id="pl-peek" aria-expanded="false" aria-controls="pl-card"><span><b>Your brief</b><small id="pl-peek-sub">Nothing picked yet</small></span><span class="pl-peek-ic">{ic('right')}</span></button>
    <div class="pl-card" id="pl-card">
      <div class="pl-card-hd"><img src="/assets/brand/mogify-mark-w.png" alt="" width="148" height="172"><div><b>Project brief</b><small id="pl-ref">MGF-0000</small></div></div>
      <div class="pl-card-body" id="pl-summary"></div>
    </div>
  </aside>
</div>
</div></section>
<div class="pl-toast" id="pl-toast" role="status" aria-live="polite"></div>
<script type="application/json" id="pl-data">""" + json.dumps({"services":[{"id":s["id"],"name":s["name"],"short":s["short"],"card":s["card"],"icon":ic(s["id"]),"tiers":[[a,b_,c] for a,b_,c in s["tiers"]],"compare":s["compare"]} for s in SERVICES],"icons":{k:ic(k) for k in ["check","arrow","left","copy","mail","doc","spark","palette","clock","wallet","user","x","download","calendar"]},"wa":bi("wa")}, ensure_ascii=False).replace("</","<\\/") + "</script>"
    page("/planner", "Project Planner | Plan Your Website, Logo or Video Project | Mogify Studio", "Plan your website, logo, branding, motion or 3D project in two minutes. Pick services, goals, style, timeline and budget range, see your project scope, and send the brief to Mogify Studio on WhatsApp.", body, ld=[crumbs_ld(items), {"@type":"WebApplication","name":"Mogify Studio Project Planner","url":url("/planner"),"applicationCategory":"BusinessApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"PKR"},"provider":{"@id":ORG_ID}}], active="/planner", body_class="planner-page no-fab", priority=0.9, scripts=["/assets/js/planner.js?v=__V__"])

# ============================== WORK ==============================
CATS = [("all","All"),("web","Websites"),("brand","Brand identity"),("logo","Logos"),("social","Social & ads"),("book","Book covers"),("product","UI/UX"),("motion","Motion & 3D")]
def build_work():
    items = [("Home","/"),("Work","/work")]
    counts = {c: len([w for w in WORK if w["cat"] == c]) for c, _ in CATS}
    counts["all"] = len(WORK)
    filt = "".join(f'<button type="button" class="chip" data-filter="{c}" aria-pressed="{"true" if c=="all" else "false"}">{n} <span class="muted">{counts[c]}</span></button>' for c, n in CATS)
    order = ["brand","web","motion","logo","social","product","book"]
    ws = sorted(WORK, key=lambda w: order.index(w["cat"]))
    cards = []
    for i, w in enumerate(ws):
        badge = '<span class="badge">CONCEPT</span>' if w.get("concept") else ('<span class="badge">LIVE</span>' if w.get("href","").startswith("http") else "")
        play = f'<span class="play-ic"><i>{ic("play")}</i></span>' if w.get("video") else ""
        img = f'<span class="im" style="display:block"><img src="{w["img"]}" alt="{e(w["alt"])}" loading="lazy" decoding="async" width="{w["w"]}" height="{w["h"]}"></span>'
        meta = f'<span class="wm"><span><b>{e(w["title"])}</b><small>{e(w["sub"])}</small></span></span>'
        if w.get("href"):
            ext = w["href"].startswith("http")
            cards.append(f'<li class="witem" data-cat="{w["cat"]}"><a class="wcard webshot" href="{w["href"]}"{" target=_blank rel=noopener" if ext else ""}>{badge}{img}{meta}</a></li>')
        else:
            cards.append(f'<li class="witem" data-cat="{w["cat"]}"><button type="button" class="wcard" data-lb data-full="{w["full"]}" data-title="{e(w["title"])}" data-sub="{e(w["sub"])}"{" data-video" if w.get("video") else ""}>{badge}{play}{img}{meta}</button></li>')
    body = phero("Work", "Selected work from <em class='s teal'>the studio.</em>", "Brand identities, websites, logos, campaigns, covers, app designs and motion. Concept projects are marked as concepts: they show what we can build for you.", items)
    body += f'<section class="sec" style="padding-top:8px"><div class="wrap"><div class="filters" role="group" aria-label="Filter work">{filt}</div><ul class="wgrid" id="wgrid">{"".join(cards)}</ul></div></section>'
    body += cta_band() + LIGHTBOX
    page("/work", "Work & Portfolio | Websites, Logos, Branding & Motion | Mogify Studio", "Selected work by Mogify Studio, Karachi: brand identities, websites, logo design, social media campaigns, book covers, UI/UX and motion design.", body, ld=[crumbs_ld(items)], active="/work", priority=0.8)

# ============================== ABOUT ==============================
def build_about():
    items = [("Home","/"),("About","/about")]
    body = phero("About Mogify", "We help good businesses <em class='s teal'>look as good as they are.</em>", "Mogify Studio is a creative and digital studio in Karachi, Pakistan, founded by Muhammad Moiz Ali. We design websites, brand identities, logos, UI/UX, motion and 3D for startups and growing businesses in Pakistan and worldwide.", items)
    body += f"""<section class="sec" style="padding-top:8px" aria-labelledby="fd-t"><div class="wrap founder">
<figure class="founder-img rv" style="margin:0"><img src="/assets/img/founder.webp" alt="Muhammad Moiz Ali, founder of Mogify Studio" width="800" height="800" loading="lazy"><figcaption>Muhammad Moiz Ali<small>Founder & Creative Director</small></figcaption></figure>
<div class="sec-head rv" style="margin:0"><span class="eyebrow">The founder</span><h2 class="h2" id="fd-t">Hi, I'm Moiz. <em class="s">I run Mogify.</em></h2>
<p class="lead">I started Mogify Studio in Karachi with a simple belief: brand identities and websites are not decoration. They are how customers decide whether to trust a business.</p>
<p class="lead">At Mogify you work with me directly, from the first message to the final files. Websites are hand-coded and built mobile-first. Logos, identities, motion and 3D are made in-house, from scratch, for your brand only.</p>
<p class="lead">The name says what we do: we <em class="s">modify</em> brands until they stand out. Modify your brand with Mogify.</p>
<div class="hero-ctas" style="margin-top:8px"><a class="btn btn-teal btn-lg" href="/planner">Start your project {ARR}</a><a class="btn btn-wa btn-lg" href="{wa('Hi Moiz! I found Mogify Studio on your website and want to talk about a project.')}" target="_blank" rel="noopener">{bi('wa')} Message Moiz</a></div></div>
</div></section>"""
    vals = [("01","Craft over templates","Every logo, layout and frame is designed for your brand. Nothing is pulled from a template library."),("02","Clarity over surprises","Clear packages, a fixed quote and agreed checkpoints, so you always know what is happening next."),("03","Business over decoration","Design exists to win trust, enquiries and sales. That is how we judge our own work.")]
    vh = sec_head("What we stand for", "Three things we <em class='s teal'>never compromise on.</em>", hid="vl-t")
    vc = "".join(f'<div class="value rv"><b>{a}</b><h3>{b_}</h3><p>{c}</p></div>' for a,b_,c in vals)
    body += f'<section class="sec sec-dark" aria-labelledby="vl-t"><div class="wrap">{vh}<div class="values">{vc}</div></div></section>'
    sl = "".join(f'<a href="/services/{o["slug"]}">{ic(o["id"])}{e(o["name"])}</a>' for o in SERVICES)
    body += f'<section class="sec" aria-labelledby="sv-t"><div class="wrap">{sec_head("What we do", "Nine services, <em class=s>one studio.</em>", hid="sv-t")}<div class="svc-more rv">{sl}</div></div></section>'
    body += cta_band()
    person = {"@type":"Person","name":"Muhammad Moiz Ali","jobTitle":"Founder & Creative Director","worksFor":{"@id":ORG_ID},"image":url("/assets/img/founder.webp"),"address":{"@type":"PostalAddress","addressLocality":"Karachi","addressCountry":"PK"},"sameAs":["https://www.linkedin.com/in/muhammad-moiz-ali-167102412/"]}
    page("/about", "About Mogify Studio | Founded by Muhammad Moiz Ali, Karachi", "Mogify Studio is a creative and digital studio in Karachi, Pakistan, founded by Muhammad Moiz Ali. Websites, branding, UI/UX, motion and 3D made in-house.", body, ld=[crumbs_ld(items), person], active="/about", priority=0.7)

# ============================== CONTACT ==============================
def build_contact():
    items = [("Home","/"),("Contact","/contact")]
    body = phero("Contact", "Let's talk about <em class='s teal'>your project.</em>", "The fastest way to reach us is WhatsApp. Prefer email or a call? Everything you need is below.", items, h1_ur="آئیے آپ کے پروجیکٹ پر بات کریں۔", lead_ur="ہم سے رابطے کا سب سے تیز طریقہ واٹس ایپ ہے۔")
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{bi(k)}</a>' for k,n,u,h in SOCIALS)
    svcs = "".join(f'<button type="button" class="chip" aria-pressed="false" data-v="{e(s["name"])}">{e(s["short"])}</button>' for s in SERVICES)
    days = ["Mon","Tue","Wed","Thu","Fri","Sat"]
    times = ["Morning","Afternoon","Evening"]
    body += f"""<section class="sec" style="padding-top:8px"><div class="wrap ct-grid">
<div style="display:grid;gap:28px;min-width:0">
 <div class="ct-cards">
  <a class="ct-card rv" href="{wa('Hi Mogify Studio! I want to discuss a project.')}" target="_blank" rel="noopener"><span class="ci wa">{bi('wa')}</span><span><b>WhatsApp</b><span>+92 323 2194013 · fastest reply</span></span></a>
  <a class="ct-card rv" href="mailto:{EMAIL}?subject=Project%20enquiry"><span class="ci">{ic('mail')}</span><span><b>Email</b><span>{EMAIL}</span></span></a>
  <a class="ct-card rv" href="/planner"><span class="ci">{ic('doc')}</span><span><b>Project Planner</b><span>Build a full brief in two minutes</span></span></a>
  <div class="ct-card rv"><span class="ci">{ic('pin')}</span><span><b>Studio</b><span>Karachi, Pakistan · working worldwide</span></span></div>
 </div>
 <div class="rv"><h2 class="h3" style="margin-bottom:14px">Follow the studio</h2><div class="socials">{soc}</div></div>
 <div class="form rv" id="call"><h2 class="h3">Book a quick call</h2><p class="muted" style="font-size:15px">Pick a day and time that suits you. We will confirm on WhatsApp.</p>
  <div class="field"><span class="lbl">Day</span><div class="slots" data-group="day">{''.join(f'<button type="button" class="chip" aria-pressed="false" data-v="{d}">{d}</button>' for d in days)}</div></div>
  <div class="field"><span class="lbl">Time (Pakistan time)</span><div class="slots" data-group="time" style="grid-template-columns:repeat(3,1fr)">{''.join(f'<button type="button" class="chip" aria-pressed="false" data-v="{t}">{t}</button>' for t in times)}</div></div>
  <a class="btn btn-wa btn-block btn-lg" id="call-btn" href="{wa('Hi Mogify Studio! I would like to book a quick call about a project.')}" target="_blank" rel="noopener">{bi('wa')} Request this call</a>
 </div>
</div>
<form class="form rv" id="ct-form" novalidate>
 <h2 class="h3">Send a message</h2>
 <p class="muted" style="font-size:15px;margin-top:-6px">Your message opens ready to send in WhatsApp or your email app. Nothing is stored on this website.</p>
 <div class="two"><div class="field"><label for="cf-name">Your name *</label><input class="inp" id="cf-name" name="name" autocomplete="name" required></div><div class="field"><label for="cf-biz">Business name</label><input class="inp" id="cf-biz" name="business" autocomplete="organization"></div></div>
 <div class="two"><div class="field"><label for="cf-email">Email</label><input class="inp" id="cf-email" name="email" type="email" autocomplete="email" inputmode="email"></div><div class="field"><label for="cf-phone">Phone / WhatsApp</label><input class="inp" id="cf-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div></div>
 <div class="field"><span class="lbl">What do you need?</span><div class="chips" id="cf-svcs">{svcs}</div></div>
 <div class="field"><label for="cf-msg">Project details *</label><textarea class="inp" id="cf-msg" name="message" required placeholder="Tell us about your business and what you have in mind"></textarea></div>
 <p class="muted" id="cf-err" role="alert" style="font-size:14px;color:#C0392B;display:none">Please add your name and a short message.</p>
 <div class="acts"><button type="submit" class="btn btn-wa" data-via="wa">{bi('wa')} Send on WhatsApp</button><button type="submit" class="btn btn-ghost" data-via="mail">{ic('mail')} Send by email</button></div>
</form>
</div></section>"""
    body += f'<section class="sec sec-soft" aria-labelledby="cq-t"><div class="wrap faq-grid"><div class="sec-head rv"><span class="eyebrow">FAQ</span><h2 class="h2" id="cq-t">Before you <em class="s">message.</em></h2></div>{faq_block(HOME_FAQS[:4])}</div></section>'
    cp = {"@type":"ContactPage","name":"Contact Mogify Studio","url":url("/contact"),"about":{"@id":ORG_ID}}
    page("/contact", "Contact Mogify Studio | WhatsApp +92 323 2194013 | Karachi", "Contact Mogify Studio in Karachi on WhatsApp (+92 323 2194013) or email (mogifystudio@gmail.com). Book a call or send your project details.", body, ld=[crumbs_ld(items), cp, faq_ld(HOME_FAQS[:4])], active="/contact", priority=0.8, scripts=["/assets/js/contact.js?v=__V__"])

# ============================== FAQ ==============================
def build_faq():
    items = [("Home","/"),("FAQ","/faq")]
    allf = HOME_FAQS + [("Can you build my website in Urdu or both languages?", "Yes, a bilingual English and Urdu version with proper right-to-left layout is available as an add-on."), ("Do you only work on big projects?", "No. Packages start from a single logo, a one-page website or a short video. Tell us what you need and we will tell you honestly what fits.")]
    sv = []
    for s in SERVICES: sv += s["faqs"][:1]
    body = phero("FAQ", "Frequently asked <em class='s teal'>questions.</em>", "Quick answers about working with Mogify Studio. Anything else, ask on WhatsApp.", items)
    body += f'<section class="sec" style="padding-top:8px"><div class="wrap-n"><h2 class="h3 rv" style="margin-bottom:20px">Working with us</h2>{faq_block(allf)}<h2 class="h3 rv" style="margin:56px 0 20px">About our services</h2>{faq_block(sv, open_first=False)}</div></section>'
    body += cta_band()
    page("/faq", "FAQ | Website, Logo & Branding Questions | Mogify Studio", "Answers about pricing, timelines, revisions, payments and how Mogify Studio in Karachi works on websites, logos, branding, motion and 3D projects.", body, ld=[crumbs_ld(items), faq_ld(allf + sv)], active=None, priority=0.6)

# ============================== LEGAL ==============================
def build_legal():
    upd = "31 October 2026"
    priv = f"""<section class="sec" style="padding-top:8px"><div class="wrap-n prose">
<p><b>Last updated:</b> {upd}</p>
<p>This website belongs to Mogify Studio, Karachi, Pakistan. We keep it simple and collect as little as possible.</p>
<h2>What this website collects</h2>
<ul><li>This website has no user accounts, no database and no advertising trackers.</li><li>The Project Planner saves your answers only in your own browser (local storage) so you do not lose progress. You can clear it any time with the “Start over” button or by clearing your browser data.</li><li>When you tap “Send on WhatsApp” or “Send by email”, your message opens in WhatsApp or your email app. Nothing is sent until you press send there.</li></ul>
<h2>Information you send us</h2>
<p>If you message us on WhatsApp or by email, we use your details only to reply, prepare a quote and work on your project. We do not sell or share your details with anyone for marketing.</p>
<h2>Third-party services</h2>
<p>WhatsApp, email providers and social networks you choose to contact us through have their own privacy policies.</p>
<h2>Your choices</h2>
<p>You can ask us to delete your messages and project details at any time: email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>"""
    terms = f"""<section class="sec" style="padding-top:8px"><div class="wrap-n prose">
<p><b>Last updated:</b> {upd}</p>
<p>These are the general terms for working with Mogify Studio. Your written quote for a project sets out the specific scope, price, timeline and payment plan, and it takes priority over this page.</p>
<h2>Quotes and scope</h2>
<p>Package contents on this website are starting points. Your project's final scope and fixed price are confirmed in writing before work begins. Work outside the agreed scope is quoted separately.</p>
<h2>Revisions</h2>
<p>Each package includes the revision rounds listed on it. Extra rounds can be added.</p>
<h2>Payments</h2>
<p>The payment plan and milestones are agreed in your written quote.</p>
<h2>Files and ownership</h2>
<p>Final files are delivered once the project is complete and paid. Ownership and usage rights for final deliverables are confirmed in your quote. Whether a finished project can be shown in our portfolio is agreed with you.</p>
<h2>Concept work</h2>
<p>Projects marked “Concept” on this website are self-initiated designs that show our skills; they are not client projects.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp +92 323 2194013.</p>
</div></section>"""
    page("/privacy", "Privacy Policy | Mogify Studio", "How the Mogify Studio website handles your information: no accounts, no trackers, planner answers stay in your browser.", phero("Legal", "Privacy policy", "Short and plain: what this website does and does not collect.", [("Home","/"),("Privacy","/privacy")]) + priv, priority=0.3)
    page("/terms", "Terms of Service | Mogify Studio", "General terms for working with Mogify Studio, Karachi: quotes, scope, revisions, payments and files.", phero("Legal", "Terms of service", "The general terms for working with Mogify Studio.", [("Home","/"),("Terms","/terms")]) + terms, priority=0.3)
    nf = f'<section class="sec nf"><div class="wrap"><span class="eyebrow">404</span><h1 class="h1" style="margin:16px 0">This page <em class="s teal">got modified.</em></h1><p class="lead" style="margin-bottom:28px">We could not find that page. Try one of these instead.</p><div class="hero-ctas" style="justify-content:center"><a class="btn btn-teal btn-lg" href="/">Home</a><a class="btn btn-ghost btn-lg" href="/packages">Packages</a><a class="btn btn-ghost btn-lg" href="/planner">Project Planner</a></div></div></section>'
    page("/404", "Page not found | Mogify Studio", "This page could not be found.", nf, noindex=True)

# ============================== CONCEPT WORK PAGES ==============================
def build_work_pages():
    src_dir = os.path.join(SITE, "work")
    for f in glob.glob(os.path.join(src_dir, "*.html")):
        t = open(f, encoding="utf-8").read()
        t = re.sub(r"https://(mogifystudio|mogifystudio-business|mogify-business)\.sites\.tab\.bot", BASE_URL, t)
        # concept pages were designed desktop-first: show the full design scaled to fit phones (no clipping, no sideways scroll)
        t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=1200">')
        if "data-bizfix" not in t:
            t = t.replace("</head>", '<style data-bizfix>html,body{overflow-x:clip!important;max-width:100%}img,video{max-width:100%}.mgf-back{position:fixed;left:18px;bottom:18px;z-index:9999;display:inline-flex;align-items:center;gap:8px;background:#121927;color:#fff;font:700 18px/1 Manrope,system-ui,sans-serif;padding:16px 22px;border-radius:999px;text-decoration:none;box-shadow:0 10px 30px -10px rgba(0,0,0,.5)}</style></head>', 1)
            t = t.replace("</body>", '<a class="mgf-back" href="/work">← Mogify Studio work</a></body>', 1)
        open(f, "w", encoding="utf-8").write(t)
        PAGES.append(("/work/" + os.path.basename(f)[:-5], 0.5))

def build_meta():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in PAGES:
        sm.append(f"<url><loc>{url(p)}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr:.1f}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(SITE, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

def stamp_version():
    import hashlib
    h = hashlib.sha1()
    for f in sorted(glob.glob(os.path.join(SITE, "assets", "*", "*.*"))):
        if f.endswith((".css", ".js")): h.update(open(f, "rb").read())
    v = h.hexdigest()[:8]
    for f in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
        t = open(f, encoding="utf-8").read()
        if "__V__" in t: open(f, "w", encoding="utf-8").write(t.replace("__V__", v))
    return v

if __name__ == "__main__":
    build_home(); build_services()
    for s in SERVICES: build_service(s)
    build_packages(); build_planner(); build_work(); build_about(); build_contact(); build_faq(); build_legal(); build_work_pages(); build_meta()
    print("built", len(PAGES), "pages, assets v", stamp_version())
