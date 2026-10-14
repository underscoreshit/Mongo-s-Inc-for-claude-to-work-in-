# Kade Studio, website

Statische site, geen installatie nodig. Upload de hele map `kade-studio/` naar je hosting (Netlify, Vercel, Cloudflare Pages, Combell, OVH...).

| Pad | Wat |
|---|---|
| `index.html` | Franse pagina, en de **bron** voor alles |
| `nl/index.html` | Nederlandse pagina, **gegenereerd**: niet met de hand aanpassen |
| `i18n/nl.json` | Nederlandse teksten |
| `build.py` | Maakt `nl/index.html` opnieuw: `python3 build.py` |
| `fonts/` | Lettertypes op eigen server (geen Google-verbinding, GDPR) |
| `brand/` | Logo's, social media, deelbeeld |
| `sitemap.xml`, `robots.txt` | Voor Google |

## Tekst wijzigen
1. Franse tekst: in `index.html`.
2. Nederlandse tekst: in `i18n/nl.json`, met dezelfde sleutel als `data-i18n="..."` in `index.html`.
3. Draai `python3 build.py`. Het script stopt met een melding als er een vertaling ontbreekt.

## Voor de lancering invullen
- [ ] **Formulier**: maak een gratis formulier aan op formspree.io of web3forms.com en plak de URL in `data-endpoint=""` in `index.html`. Zolang dit leeg is, opent het mailprogramma van de bezoeker.
- [ ] **Domein**: overal staat `https://kadestudio.be` (index.html, sitemap.xml, robots.txt). Is je domein anders? Zoek en vervang, en draai dan `build.py`.
- [ ] **E-mail**: `hello@kadestudio.be` (index.html en `STR` onderaan in het script).
- [ ] **Ondernemingsnummer**: `BE 0XXX.XXX.XXX` in de footer. Wettelijk verplicht op een Belgische zakelijke website, samen met je adres.
- [ ] **Statistieken**: haal de commentaartekens weg rond de Plausible-regels in `<head>`. De klik- en aanvraag-events worden al verstuurd.
- [ ] **Prijzen en termijnen** nakijken: 490 €, 1 490 €, vanaf 2 900 €, 39 €/maand, 1-2 dagen (webshop 1 week), 24 uur.

## Wat er gemeten wordt (`dataLayer` en Plausible)
| Event | Wanneer |
|---|---|
| `cta_click` | klik op "Demander un devis" / "Offerte aanvragen" (`id`: nav_cta, hero_cta, hero_examples) |
| `lead_submit` | formulier verstuurd via de formulierdienst |
| `lead_mailto` | formulier doorgestuurd naar het mailprogramma |
| `lead_error` | verzenden mislukt |
| `lang_switch` | wissel FR/NL |
