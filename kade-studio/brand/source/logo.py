import sys,math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F=sys.argv[1]; OUT=sys.argv[2]
INK="#151515";ACID="#74DB4B";TOM="#FF5426";WHITE="#FFFFFF";SUN="#FFD43A"
def text_path(ttf,text,size,x,y,track=0):
    f=TTFont(ttf);gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f['head'].unitsPerEm;s=size/upm
    pen=SVGPathPen(gs);cx=0
    for ch in text:
        g=cmap[ord(ch)];
        tp=TransformPen(pen,(s,0,0,-s,x+cx,y))
        gs[g].draw(tp);cx+=gs[g].width*s+track
    return pen.getCommands(),cx-track
BS=F+'/f1.ttf';BR=F+'/f2.ttf'
def star(cx,cy,R,r,n=14):
    pts=[]
    for i in range(2*n):
        rr=R if i%2==0 else r;a=math.pi*i/n-math.pi/2
        pts.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return " ".join(pts)

# --- wordmark ---
d,w=text_path(BS,"KADE",400,40,330,track=6)
ds,ws=text_path(BR,"STUDIO",62,0,0,track=6)
W=int(w+80+40);H=470
def wordmark(fill,stroke,shadow,pill_bg,pill_fg,pill_bd):
    sh=f'<path d="{d}" transform="translate(16,16)" fill="{shadow}" stroke="{shadow}" stroke-width="16" stroke-linejoin="round"/>' if shadow else ''
    st=f' stroke="{stroke}" stroke-width="16" stroke-linejoin="round" paint-order="stroke fill"' if stroke else ''
    pw=ws+70;ph=96
    pill=(f'<g transform="translate({W-pw-30},{H-ph-14}) rotate(-5 {pw/2} {ph/2})">'
          f'<rect x="0" y="0" width="{pw:.0f}" height="{ph}" rx="{ph/2}" fill="{pill_bg}" stroke="{pill_bd}" stroke-width="7"/>'
          f'<path d="{ds}" transform="translate(35,{ph/2+23})" fill="{pill_fg}"/></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{sh}<path d="{d}" fill="{fill}"{st}/>{pill}</svg>'
open(OUT+'/kade-logo.svg','w').write(wordmark(WHITE,INK,INK,TOM,INK,INK))
open(OUT+'/kade-logo-ink.svg','w').write(wordmark(INK,None,None,"none",INK,INK))
open(OUT+'/kade-logo-white.svg','w').write(wordmark(WHITE,None,None,"none",WHITE,WHITE))
# --- mark (sticker K) ---
dk,wk=text_path(BS,"K",560,0,0)
M=1000
mark=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {M} {M}" width="{M}" height="{M}">'
 f'<polygon points="{star(520,520,470,380)}" fill="{INK}"/>'
 f'<polygon points="{star(500,500,470,380)}" fill="{WHITE}" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>'
 f'<g transform="rotate(-8 500 500)"><path d="{dk}" transform="translate({500-wk/2:.1f},{500+560*0.36:.1f})" fill="{INK}"/></g></svg>')
open(OUT+'/kade-mark.svg','w').write(mark)
print(W,H)
