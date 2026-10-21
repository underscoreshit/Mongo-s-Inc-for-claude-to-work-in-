# Kade Studio, website

Statische site, geen installatie nodig. Upload de hele map `kade-studio/` naar je hosting (Netlify, Vercel, Cloudflare Pages, Combell, OVH...).

| Pad | Wat |
|---|---|
| `index.html` | Franse pagina, en de **bron** voor alles. Bezoekers zonder taalvoorkeur en Google (`x-default`) gaan naar `/nl/`: de streek is Nederlandstalig. |
| `nl/index.html` | Nederlandse pagina, **gegenereerd**: niet met de hand aanpassen |
| `i18n/nl.json` | Nederlandse teksten |
| `build.py` | Maakt `nl/index.html` opnieuw: `python3 build.py` |
| `v2/index.html` | **Versie 2** (illustratief, naar het moodboard van oktober 2026): zelfde teksten en sleutels als v1, eigen fonts in `v2/fonts/`, demo-screenshots in `v2/img/`. Staat op `noindex` zolang v1 de hoofdsite is. |
| `v2/nl/index.html` | NL van versie 2, **gegenereerd** door `build.py` |
| `fonts/` | Lettertypes op eigen server (geen Google-verbinding, GDPR) |
| `brand/` | Logo's, social media, deelbeeld |
| `demos/<naam>/` | Zes volledige demosites voor **fictieve** zaken, elk met eigen stijl, lettertypes (`fonts/`) en stockfoto's (`img/`, bronnen in `img/CREDITS.md`). De kaarten in de rail linken ernaar. Echte prospect-demo's staan in de repo `Kade-Business`. |
| `sitemap.xml`, `robots.txt` | Voor Google |

## Tekst wijzigen
1. Franse tekst: in `index.html`.
2. Nederlandse tekst: in `i18n/nl.json`, met dezelfde sleutel als `data-i18n="..."` in `index.html`.
3. Draai `python3 build.py`. Het bouwt `nl/index.html` én `v2/nl/index.html`, en stopt met een melding als er een vertaling ontbreekt.
4. Versie 2 testen: open `v2/index.html?intro=1` (de intro speelt anders één keer per sessie).
5. Versie 2 wordt de hoofdsite: haal `noindex` weg in `v2/index.html`, zet de canonical op `https://kadestudio.be/`, en verplaats de map (of laat de hosting `/` naar `/v2/` sturen).

## Voor de lancering invullen
- [ ] **Formulier**: maak een gratis formulier aan op formspree.io of web3forms.com en plak de URL in `data-endpoint=""` in `index.html`. Zolang dit leeg is, opent het mailprogramma van de bezoeker.
- [ ] **Domein**: overal staat `https://kadestudio.be` (index.html, sitemap.xml, robots.txt). Is je domein anders? Zoek en vervang, en draai dan `build.py`.
- [ ] **E-mail**: `hello@kadestudio.be` (index.html en `STR` onderaan in het script).
- [ ] **Ondernemingsnummer**: `BE 0XXX.XXX.XXX` in de footer. Wettelijk verplicht op een Belgische zakelijke website, samen met je adres.
- [ ] **Statistieken**: haal de commentaartekens weg rond de Plausible-regels in `<head>`. De klik- en aanvraag-events worden al verstuurd.
- [ ] **Prijzen en termijnen** nakijken: 490 €, 1 490 €, vanaf 2 900 €, 19 en 39 €/maand, 48 uur, 24 uur. Ook: 100 € doorverwijskorting, "vanaf 490 €" voor kapotte sites.
- [ ] **Demo's in de rail**: zes fictieve concepten (dakwerker, barbier, broodjesbar, museum, fietsenwinkel, kunstatelier). Wil je een echte klantsite tonen? Voeg pas een kaart toe als de klant akkoord is.

## Wat er gemeten wordt (`dataLayer` en Plausible)
| Event | Wanneer |
|---|---|
| `cta_click` | klik op "Demander un devis" / "Offerte aanvragen" (`id`: nav_cta, hero_cta, hero_examples) |
| `lead_submit` | formulier verstuurd via de formulierdienst |
| `lead_mailto` | formulier doorgestuurd naar het mailprogramma |
| `lead_error` | verzenden mislukt |
| `lang_switch` | wissel FR/NL |
| `cta_click` met `id` `demo_<naam>` | klik op een demokaart in de rail |

## Positionering (oktober 2026)
Na de marktanalyse (zie repo `Kade-Business`): lokaal in plaats van heel België, demo vóór het eerste gesprek, online in 48 uur, bouw & ambacht eerst.
- Eén pagina 490 € (Designer@Work Westerlo zit op 350 €, de markt op 500-1 500 €).
- Etalage 1 490 € met meer erin (offerteformulier, Google-profiel, 1 uur foto's) om boven Adworkx/Webily (699-895 €) te verantwoorden.
- Onderhoud in twee stappen: 19 €/maand (domein, hosting, mail) en 39 €/maand (+ onbeperkt aanpassen, Google-profiel).
