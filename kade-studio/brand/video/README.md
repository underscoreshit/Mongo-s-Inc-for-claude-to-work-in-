# Video-advertentie (13,5 s)

| Bestand | Formaat | Gebruik |
|---|---|---|
| `kade-ad-nl-9x16.mp4` / `kade-ad-fr-9x16.mp4` | 1080×1920 | Reels, Stories |
| `kade-ad-nl-4x5.mp4` / `kade-ad-fr-4x5.mp4` | 1080×1350 | Feed Instagram en Facebook |

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
7,8-10,6 s: Vaste prijs vanaf 690 € excl. btw, sticker "Online in 3 weken".
10,6-13,5 s: Logo, cursor klikt op "Offerte aanvragen", "Link in bio".

Alle bewegingen zijn vloeiend (ease-out); scènes schuiven over elkaar zonder pauze.

## Advertentietekst voor Meta Ads Manager
**NL**
- Primaire tekst: Uw klanten zoeken u op Google. Vinden ze iets? Kade Studio maakt heldere websites voor kleine Belgische bedrijven, in het Nederlands en het Frans. Vaste prijs, online in 3 weken.
- Kop: Uw website, vanaf 690 € excl. btw
- Knop: Offerte aanvragen

**FR**
- Texte principal : Vos clients vous cherchent sur Google. Ils trouvent quoi ? Kade Studio crée des sites clairs pour les petites entreprises belges, en français et en néerlandais. Prix fixe, livré en 3 semaines.
- Titre : Votre site web, dès 690 € HTVA
- Bouton : Demander un devis
