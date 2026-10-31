/* ============================================================
   MOGIFY STUDIO — SITE CONFIG  (the ONE place to edit prices)
   ------------------------------------------------------------
   PRICES: put a string to show it, or null to show "Price on request".
     Examples:  "PKR 45,000"   "From PKR 25,000"   "$299"   "From $499"
   Key format: prices[serviceId][tierId]  and  addons[addonId]
   Service ids: web, logo, brand, uiux, motion, anim3d, social, book, video
   Tier ids:    starter, growth, premium
   Nothing else needs to change; every price spot on the site reads from here.
   ============================================================ */
window.MOGIFY = {
  whatsapp: "923232194013",            // wa.me number, digits only
  email: "mogifystudio@gmail.com",
  priceNote: "Fixed quote after a quick brief", // small line under a price
  noPriceText: "Price on request",       // shown when a price is null
  prices: {
    web:    { starter: null, growth: null, premium: null },
    logo:   { starter: null, growth: null, premium: null },
    brand:  { starter: null, growth: null, premium: null },
    uiux:   { starter: null, growth: null, premium: null },
    motion: { starter: null, growth: null, premium: null },
    anim3d: { starter: null, growth: null, premium: null },
    social: { starter: null, growth: null, premium: null },
    book:   { starter: null, growth: null, premium: null },
    video:  { starter: null, growth: null, premium: null }
  },
  addons: {
    "extra-page": null,
    "urdu-version": null,
    "copywriting": null,
    "domain-hosting": null,
    "website-care": null,
    "logo-animation": null,
    "social-kit": null,
    "brand-guidelines": null,
    "extra-revision": null,
    "source-files": null,
    "priority": null,
    "thumbnail-pack": null
  }
};
