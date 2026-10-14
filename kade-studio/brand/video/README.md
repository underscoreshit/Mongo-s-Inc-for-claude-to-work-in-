# Video-advertenties

## 1. Advertentie (13,5 s): "Bij de buren?"
| Bestand | Formaat | Gebruik |
|---|---|---|
| `kade-ad-nl-9x16.mp4` / `kade-ad-fr-9x16.mp4` | 1080×1920 | Reels, Stories |
| `kade-ad-nl-4x5.mp4` / `kade-ad-fr-4x5.mp4` | 1080×1350 | Feed Instagram en Facebook |

## 2. Portfolio-video (15 s): voorbeeldsites in een gsm
| Bestand | Formaat | Gebruik |
|---|---|---|
| `kade-portfolio-nl-9x16.mp4` / `kade-portfolio-fr-9x16.mp4` | 1080×1920 | Reels, Stories |
| `kade-portfolio-nl-4x5.mp4` / `kade-portfolio-fr-4x5.mp4` | 1080×1350 | Feed |

Vijf voorbeeldsites (bakkerij, barbier, bloemist, garage, frituur) scrollen na elkaar in een gsm, elk 2,3 s, met een label "Concept" + naam + stad. Eindigt op "Uw zaak is de volgende?" met logo en knop.
De vijf sites staan in `source/sites.py`, elk met eigen lettertype, kleuren en opbouw (hero, producten, reviews, openingsuren, kaart, footer). Extra lettertypes in `source/fonts/`.
Echt klantenwerk toevoegen: vervang een site in `sites.py` (of zet er een screenshot in) en haal "Concept" weg in `make_portfolio.py`.

```bash
python3 make_portfolio.py
AD=portfolio node render.js nl frames-pf-nl              # 9:16
FEED=1 AD=portfolio node render.js nl frames-pf-nl-feed  # 4:5-layout, daarna crop=1080:1350:0:285
```

H.264, 30 fps, stille audiotrack (voeg muziek toe in Instagram of in Meta Ads Manager).
De MP4's staan niet in git (te groot). Opnieuw maken:

```bash
cd kade-studio/brand/video/source
python3 make_ad.py                      # teksten aanpassen in de T-tabel bovenaan
node render.js nl frames-nl             # 405 beelden (Playwright)
ffmpeg -framerate 30 -i frames-nl/%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 22 ../kade-ad-nl-9x16.mp4
ffmpeg -framerate 30 -i frames-nl/%04d.jpg -vf crop=1080:1350:0:285 -c:v libx264 -pix_fmt yuv420p -crf 22 ../kade-ad-nl-4x5.mp4
```

## Verhaal
0-3 s: "Uw klant zoekt u." Cursor typt een zoekopdracht, er is geen website, met een 404-stempel.
3-4,8 s: "Bij de buren?"
4,8-7,8 s: "Wij maken uw website." Voor kleine Belgische zaken. Helder, snel, NL + FR.
7,8-10,6 s: Vaste prijs vanaf 490 € excl. btw, sticker "Online in 1-2 dagen".
10,6-13,5 s: Logo, cursor klikt op "Offerte aanvragen", "Link in bio".

Alle bewegingen zijn vloeiend (ease-out); scènes schuiven over elkaar zonder pauze.

## Advertentietekst voor Meta Ads Manager
**NL**
- Primaire tekst: Uw klanten zoeken u op Google. Vinden ze iets? Kade Studio maakt heldere websites voor kleine Belgische bedrijven, in het Nederlands en het Frans. Vaste prijs, online in 1-2 dagen.
- Kop: Uw website, vanaf 490 € excl. btw
- Knop: Offerte aanvragen

**FR**
- Texte principal : Vos clients vous cherchent sur Google. Ils trouvent quoi ? Kade Studio crée des sites clairs pour les petites entreprises belges, en français et en néerlandais. Prix fixe, livré en 1-2 jours.
- Titre : Votre site web, dès 490 € HTVA
- Bouton : Demander un devis
