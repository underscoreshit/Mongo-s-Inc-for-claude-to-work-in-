# Kade Studio, huisstijl & social media

## Logo (`logo/`)
| Bestand | Gebruik |
|---|---|
| `kade-logo.svg/.png` | Hoofdlogo: wit met zwarte rand, oranje "STUDIO"-label. Op groen, geel, roze, blauw of zwart. |
| `kade-logo-ink.svg/.png` | Eén kleur zwart: stempels, facturen, lichte achtergrond. |
| `kade-logo-white.svg/.png` | Eén kleur wit: op foto's of donkere achtergrond. |
| `kade-mark.svg/.png` | Sticker met "K": profielfoto, favicon, kleine plekken. |

PNG's zijn transparant en 3x vergroot. SVG's zijn vectoren (tekst omgezet naar paden, geen lettertype nodig).

## Kleuren
| Naam | Hex |
|---|---|
| Zuurgroen | `#74DB4B` |
| Tomaat | `#FF5426` |
| Zon | `#FFD43A` |
| Kauwgom | `#FFB8E0` |
| Kobalt | `#3B6BFF` |
| Inkt | `#151515` |
| Papier | `#F1F2EC` |

## Lettertypes (gratis, Google Fonts)
- **Big Shoulders Display Black**: affichetitels, logo
- **Bricolage Grotesque** (500 en 800): koppen en tekst
- **Courier Prime**: kleine labels, @handle

## Social (`social/`, elk in `fr/` en `nl/`)
| Bestand | Formaat | Waar |
|---|---|---|
| `profile-picture.png` | 1080×1080 | Instagram + Facebook profielfoto |
| `facebook-cover.png` | 1640×624 | Facebook omslagfoto |
| `post-1` tot `post-6` | 1080×1350 (4:5) | Instagram/Facebook posts |
| `story-1`, `story-2` | 1080×1920 | Stories |
| `highlight-1` tot `-4` | 1080×1080 | Instagram highlight-covers |

`post-5-nouveau-projet` en `story-2-projet` zijn sjablonen: zet je screenshot op het witte vlak (Canva, Figma of Photoshop).

## Opnieuw genereren
`source/` bevat de scripts (Python + Playwright) die alles maken. Teksten aanpassen in `social.py`.
