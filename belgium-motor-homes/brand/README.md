# Belgium Motor Homes Store · merkpakket

Logo, merkteken, badge, panelen, Facebook-omslag en profielfoto. Zwart `#141414`, geel `#FFD400`, crème `#F2EDE1`. Lettertypes: Big Shoulders Display 900 (titels), Archivo (tekst).

- `merkbord.html` : overzicht van het hele pakket (ook gepubliceerd als artifact).
- `svg/` : vectorbestanden. `logo-sticker.svg` is het hoofdlogo.
- `png/` : afbeeldingen, favicons (32/180/512), `facebook-cover-nl.png`, `facebook-cover-fr.png`, `profielfoto.png`.
- `src/gen.py` : genereert alles. Vereist `pip install fonttools uharfbuzz brotli` en de `.ttf`-instanties in `src/fonts/` (zie onder). Dan `OUT=../svg python3 gen.py`.

## Fonts
`src/fonts/` bevat de twee woff2 van Google Fonts (Big Shoulders Display 900, Archivo variabel). Het script leest `.ttf`: maak ze zo aan:

```python
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
t = TTFont('big-shoulders-display.woff2'); t.flavor = None; t.save('big-shoulders-display.ttf')
for name, w, wd in [('arch-black', 900, 100), ('arch-black-n', 900, 88), ('arch-xb', 800, 100), ('arch-bold', 700, 100), ('arch-sb', 600, 100)]:
    i = instancer.instantiateVariableFont(TTFont('archivo-var.woff2'), {'wght': w, 'wdth': wd}); i.flavor = None; i.save(name + '.ttf')
```
