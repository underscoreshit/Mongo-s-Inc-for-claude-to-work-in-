# Kade Studio, website

Static site, nothing to install. Upload the whole `kade-studio/` folder to your hosting (Netlify, Vercel, Cloudflare Pages, Combell, OVH...).

| Path | What |
|---|---|
| `index.html` | French page, and the **source** for everything |
| `nl/index.html` | Dutch page, **generated**: do not edit by hand |
| `i18n/nl.json` | Dutch texts |
| `build.py` | Rebuilds `nl/index.html`: `python3 build.py` |
| `fonts/` | Self-hosted fonts (no Google request, GDPR) |
| `brand/` | Logos, social media, video, Fiverr kit, share image |
| `sitemap.xml`, `robots.txt` | For Google |

## Changing text
1. French text: in `index.html`.
2. Dutch text: in `i18n/nl.json`, same key as `data-i18n="..."` in `index.html`.
3. Run `python3 build.py`. It stops with a message if a translation is missing.

## Before launch
- [ ] **Form**: create a free form on formspree.io or web3forms.com and paste the URL into `data-endpoint=""` in `index.html`. While empty, the visitor's mail app opens instead.
- [ ] **Domain**: `https://kadestudio.be` is used everywhere (index.html, sitemap.xml, robots.txt). Different domain? Find and replace, then run `build.py`.
- [ ] **Email**: `hello@kadestudio.be` (index.html and `STR` at the bottom of the script).
- [ ] **Company number**: `BE 0XXX.XXX.XXX` in the footer. Legally required on a Belgian business website, together with your address.
- [ ] **Analytics**: uncomment the Plausible lines in `<head>`. Click and lead events are already sent.
- [ ] **Prices and timings** to check: 690 €, 1 490 €, from 2 900 €, 39 €/month, 3 weeks, 24 h.

## What is measured (`dataLayer` and Plausible)
| Event | When |
|---|---|
| `cta_click` | click on "Demander un devis" / "Offerte aanvragen" (`id`: nav_cta, hero_cta, hero_examples) |
| `lead_submit` | form sent through the form service |
| `lead_mailto` | form handed to the mail app |
| `lead_error` | sending failed |
| `lang_switch` | FR/NL switch |
