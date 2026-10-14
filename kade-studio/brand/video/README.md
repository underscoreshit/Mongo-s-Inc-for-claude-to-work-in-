# Video ads

## 1. Ad (13.5 s): "Bij de buren?" / "Chez le voisin ?"
| File | Size | Use |
|---|---|---|
| `kade-ad-nl-9x16.mp4` / `kade-ad-fr-9x16.mp4` | 1080×1920 | Reels, Stories |
| `kade-ad-nl-4x5.mp4` / `kade-ad-fr-4x5.mp4` | 1080×1350 | Instagram and Facebook feed |

Story: 0-3 s "Your customer is looking for you", a search with no website and a 404 stamp. 3-4.8 s "At the neighbours?". 4.8-7.8 s "We build your website." 7.8-10.6 s fixed price from 690 € with the "online in 3 weeks" sticker. 10.6-13.5 s logo, cursor clicks "Request a quote", "Link in bio".

## 2. Portfolio video (15 s): example sites in a phone
| File | Size | Use |
|---|---|---|
| `kade-portfolio-nl-9x16.mp4` / `kade-portfolio-fr-9x16.mp4` | 1080×1920 | Reels, Stories, Fiverr gig video |
| `kade-portfolio-nl-4x5.mp4` / `kade-portfolio-fr-4x5.mp4` | 1080×1350 | Feed |

Five example sites (bakery, barber, florist, garage, friterie) scroll one after another in a phone, 2.4 s each, with a "Concept" + name + city label. Ends on "Your business is next?" with logo and button.
The five sites live in `source/sites.py`, each with its own fonts, colours and layout (hero, products, reviews, opening hours, map, footer). Extra fonts in `source/fonts/`.
Adding real client work: replace a site in `sites.py` (or drop in a screenshot) and remove "Concept" in `make_portfolio.py`.

## Rebuilding
H.264, 30 fps, silent audio track (add music in Instagram or Meta Ads Manager). The MP4s are not in git (too large).

```bash
cd kade-studio/brand/video/source
python3 make_ad.py                     # ad; texts in the T table at the top
python3 make_portfolio.py              # portfolio
node render.js nl frames-ad-nl                             # ad, 405 frames (Playwright)
AD=portfolio node render.js nl frames-pf-nl                # portfolio 9:16
FEED=1 AD=portfolio node render.js nl frames-pf-nl-feed    # portfolio 4:5 layout, then crop=1080:1350:0:285
ffmpeg -framerate 30 -i frames-pf-nl/%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 ../kade-portfolio-nl-9x16.mp4
ffmpeg -framerate 30 -i frames-pf-nl-feed/%04d.jpg -vf crop=1080:1350:0:285 -c:v libx264 -pix_fmt yuv420p -crf 20 ../kade-portfolio-nl-4x5.mp4
```

## Ad copy for Meta Ads Manager
**NL**
- Primary text: Uw klanten zoeken u op Google. Vinden ze iets? Kade Studio maakt heldere websites voor kleine Belgische bedrijven, in het Nederlands en het Frans. Vaste prijs, online in 3 weken.
- Headline: Uw website, vanaf 690 € excl. btw
- Button: Offerte aanvragen

**FR**
- Primary text: Vos clients vous cherchent sur Google. Ils trouvent quoi ? Kade Studio crée des sites clairs pour les petites entreprises belges, en français et en néerlandais. Prix fixe, livré en 3 semaines.
- Headline: Votre site web, dès 690 € HTVA
- Button: Demander un devis
