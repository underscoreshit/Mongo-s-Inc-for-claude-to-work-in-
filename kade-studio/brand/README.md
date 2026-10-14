# Kade Studio, brand & social media

## Logo (`logo/`)
| File | Use |
|---|---|
| `kade-logo.svg/.png` | Main logo: white with black outline, orange "STUDIO" label. On green, yellow, pink, blue or black. |
| `kade-logo-ink.svg/.png` | One colour black: stamps, invoices, light backgrounds. |
| `kade-logo-white.svg/.png` | One colour white: on photos or dark backgrounds. |
| `kade-mark.svg/.png` | Sticker with "K": profile picture, favicon, small spaces. |

PNGs are transparent and 3x size. SVGs are vectors (text converted to paths, no font needed).

## Colours
| Name | Hex |
|---|---|
| Acid green | `#74DB4B` |
| Tomato | `#FF5426` |
| Sun | `#FFD43A` |
| Bubblegum | `#FFB8E0` |
| Cobalt | `#3B6BFF` |
| Ink | `#151515` |
| Paper | `#F1F2EC` |

## Fonts (free, Google Fonts, self-hosted in `../fonts/`)
- **Big Shoulders Display Black**: poster titles, logo
- **Bricolage Grotesque** (500 and 800): headings and body
- **Courier Prime**: small labels, @handle

## Social (`social/`, each in `fr/` and `nl/`)
| File | Size | Where |
|---|---|---|
| `profile-picture.png` | 1080×1080 | Instagram + Facebook profile picture |
| `facebook-cover.png` | 1640×624 | Facebook cover |
| `post-1` to `post-6` | 1080×1350 (4:5) | Instagram/Facebook posts |
| `story-1`, `story-2` | 1080×1920 | Stories |
| `highlight-1` to `-4` | 1080×1080 | Instagram highlight covers |
| `first-post/slide-1` to `-5` | 1080×1350 | First Instagram post (carousel). Caption: `social/first-post-caption.md` |
| `og-image.png` | 1200×630 | Preview image when the site is shared (WhatsApp, Facebook, LinkedIn) |

`post-5-nouveau-projet` and `story-2-projet` are templates: put your screenshot on the white area (Canva, Figma or Photoshop).

## Video (`video/`), Fiverr (`fiverr/`)
See the README in each folder.

## Regenerating
`source/` contains the scripts (Python + Playwright) that build everything. Change texts in `social.py`.
