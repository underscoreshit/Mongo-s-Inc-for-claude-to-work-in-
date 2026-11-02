/* ---------- pixel village ---------- */
// Each category is a building. The world is drawn at 480×270 "pixels" and scaled up crisply.
const net = (() => {
  const WW = 480, WH = 270;
  const ROW = [78, 150, 228], ROAD = [86, 158, 236], VROADS = [80, 240, 398];
  const PLAZA = { x:240, y:122, r:20 };
  const cv = $("net"), ctx = cv.getContext("2d"), tip = $("tip");
  const sc = document.createElement("canvas"); sc.width = WW; sc.height = WH;   // static scene
  const wc = document.createElement("canvas"); wc.width = WW; wc.height = WH;   // per-frame scene
  const sg = sc.getContext("2d"), wg = wc.getContext("2d");
  let g = sg, bb = null;
  const R = (x, y, w, h, c) => {
    x = Math.round(x); y = Math.round(y); w = Math.round(w); h = Math.round(h);
    if (w <= 0 || h <= 0) return;
    g.fillStyle = c; g.fillRect(x, y, w, h);
    if (bb){ bb.x0 = Math.min(bb.x0, x); bb.y0 = Math.min(bb.y0, y); bb.x1 = Math.max(bb.x1, x+w); bb.y1 = Math.max(bb.y1, y+h); }
  };
  const C = { grass:"#6f9a3e", grassL:"#83ad4a", grassD:"#5c8433", grassDD:"#4b6f2a", dirt:"#c99a5b", dirtL:"#dbb173", dirtD:"#a47843",
    water:"#3e7fa6", waterL:"#6aaed3", waterD:"#2f6489", foam:"#d8eef6", sand:"#dcc58e", wood:"#8a5a2b", woodD:"#5e3b1c", woodL:"#b07a42",
    stone:"#a39b8e", stoneD:"#7a7268", stoneL:"#c6beb0", plaster:"#ecd8ad", plasterD:"#cfb787", roof:"#b4472f", roofD:"#86321f", roofL:"#c8583b",
    glass:"#2b3440", lit:"#ffd77a", door:"#56361a", trunk:"#6b4423", leaf:"#3f7a34", leafL:"#5d9a40", leafD:"#2f5e29", ink:"#2a1d12", white:"#f4efe4" };
  function seeded(seed){ return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  let rnd = seeded(11);
  const riverTop = x => 249 + Math.round(2*Math.sin(x/19) + Math.sin(x/7));

  /* --- per-frame registries filled while drawing buildings --- */
  let wins = [], smokes = [], lamps = [], anims = [];

  /* --- building helpers --- */
  function walls(x0, yb, w, h, c, cd){ R(x0, yb-h, w, h, c); R(x0+w-2, yb-h, 2, h, cd); R(x0, yb-2, w, 2, cd); }
  function gable(x0, ytop, w, c, cd, cl){ let l = x0-2, r = x0+w+2, i = 0; while (r - l > 1){ R(l, ytop-i, r-l, 1, i === 0 ? cd : (i % 2 ? c : cl)); l += 2; r -= 2; i++; } return ytop - i; }
  function win(x, y){ R(x-1, y-1, 6, 6, C.woodD); R(x, y, 4, 4, C.glass); R(x, y, 1, 1, "#4d5d70"); R(x+2, y, 1, 4, C.woodD); R(x, y+2, 4, 1, C.woodD); wins.push([x, y]); }
  function door(x, yb, w = 5, h = 8){ R(x-1, yb-h-1, w+2, h+1, C.woodD); R(x, yb-h, w, h, C.door); R(x+w-2, yb-(h>>1), 1, 1, C.lit); }
  function chimney(x, y, heavy){ R(x, y-7, 4, 8, "#8e4a35"); R(x-1, y-8, 6, 2, "#5c2f22"); smokes.push({ x:x+2, y:y-9, rate: heavy ? .5 : .16, heavy }); }
  function texture(x0, y0, w, h, c, n){ for (let i = 0; i < n; i++) R(x0 + rnd()*w, y0 + rnd()*h, 1, 1, c); }
  function shadow(x0, yb, w){ R(x0-1, yb, w+2, 2, "rgba(40,52,20,.35)"); }

  const B = {
    rising(x, yb){
      const x0 = x-20;
      shadow(x0, yb, 30);
      R(x0, yb-3, 28, 3, C.stoneD);
      R(x0+1, yb-10, 26, 7, C.plaster); R(x0+1, yb-10, 26, 1, C.plasterD); texture(x0+1, yb-9, 26, 6, C.plasterD, 10);
      for (const px of [x0, x0+9, x0+18, x0+27]) R(px, yb-22, 1, 22, C.woodL);
      for (const py of [yb-22, yb-15]) R(x0, py, 28, 1, C.woodL);
      for (let i = 0; i < 7; i++) R(x0+10+i, yb-15-i, 1, 1, C.wood);
      R(x0+29, yb-4, 8, 4, "#b0573c"); R(x0+30, yb-6, 6, 2, "#c46a4a"); R(x0+31, yb-4, 1, 4, "#8e4430");
      const mx = x+16;
      for (let y = yb-52; y < yb; y++) R(mx, y, 3, 1, y % 4 === 0 ? "#a07a12" : "#e0b230");
      R(mx-1, yb-2, 5, 2, C.stoneD);
      R(mx-26, yb-52, 38, 2, "#e0b230"); for (let i = mx-26; i < mx+12; i += 3) R(i, yb-51, 1, 1, "#a07a12");
      R(mx+8, yb-50, 4, 4, C.stoneD); R(mx, yb-56, 3, 4, "#e0b230");
      R(mx-2, yb-49, 7, 4, "#e9e2d2"); R(mx-1, yb-48, 2, 2, C.glass);
      anims.push(t => {
        const hx = mx-20 + Math.round(Math.sin(t*0.6)*2), len = 18 + Math.round(Math.sin(t*0.35)*6);
        for (let i = 0; i < len; i++) R(hx, yb-50+i, 1, 1, "#4a4a4a");
        R(hx-1, yb-50+len, 3, 2, "#4a4a4a"); R(hx-5, yb-48+len, 11, 2, C.woodL); R(hx-5, yb-48+len, 11, 1, C.wood);
      });
      return { door:[x0+13, yb] };
    },
    ai(x, yb){
      const x0 = x-11;
      shadow(x0, yb, 22);
      walls(x0, yb, 22, 24, C.stone, C.stoneD);
      for (let y = yb-22, k = 0; y < yb; y += 4, k++) for (let i = (k % 2) * 3; i < 20; i += 6) R(x0+i, y, 1, 3, C.stoneD);
      const cy = yb-24;
      for (let dy = 0; dy < 12; dy++){ const hw = Math.round(Math.sqrt(144 - dy*dy)); R(x-hw, cy-dy-1, hw*2, 1, dy < 1 ? "#3d3266" : "#5b4b8a"); if (dy > 1 && dy < 10) R(x-hw+2, cy-dy-1, 2, 1, "#7f6fb6"); }
      R(x-1, cy-12, 2, 11, "#1d1733");
      for (let i = 0; i < 9; i++) R(x+1+i, cy-8-Math.round(i*.7), 2, 2, i > 6 ? "#e8e2f0" : "#c9c2d6");
      win(x0+3, yb-17); door(x-2, yb, 5, 8);
      anims.push(t => {
        const a = .5 + .5*Math.sin(t*2.2);
        R(x+10, cy-15, 2, 2, `rgba(200,170,255,${.4 + a*.6})`);
        R(x+9, cy-16, 4, 4, `rgba(170,130,255,${a*.25})`);
        for (const [sx, sy, p] of [[x-14, cy-22, 0], [x+16, cy-26, 1.3], [x-4, cy-30, 2.1]]) if (Math.sin(t*1.7 + p) > .3) R(sx, sy, 1, 1, "#fff7d6");
      });
      return { door:[x, yb] };
    },
    awesome(x, yb){
      const x0 = x-28;
      shadow(x0, yb, 56);
      walls(x0, yb, 56, 22, C.plaster, C.plasterD);
      R(x0, yb-22, 56, 1, C.woodD); R(x0, yb-12, 56, 1, C.woodD);
      for (const bx of [x0, x0+13, x0+42, x0+55]) R(bx, yb-22, 1, 22, C.woodD);
      for (let i = 0; i < 9; i++){ R(x0+1+i, yb-21+i, 1, 1, C.woodD); R(x0+54-i, yb-21+i, 1, 1, C.woodD); }
      gable(x0, yb-23, 56, C.roof, C.roofD, C.roofL);
      const tx = x-6;
      R(tx, yb-50, 12, 30, C.stoneL); R(tx+10, yb-50, 2, 30, C.stone);
      gable(tx, yb-51, 12, "#3f5f8a", "#2d4566", "#5175a8");
      R(tx+2, yb-46, 8, 8, C.stoneD); R(tx+3, yb-45, 6, 6, C.white); R(tx+5, yb-44, 1, 3, C.ink); R(tx+6, yb-42, 2, 1, C.ink);
      R(tx+5, yb-64, 1, 10, C.ink);
      win(x0+4, yb-18); win(x0+18, yb-18); win(x0+34, yb-18); win(x0+47, yb-18);
      win(x0+18, yb-9); win(x0+34, yb-9);
      R(x-5, yb-11, 10, 11, C.woodD); R(x-4, yb-10, 8, 10, C.door); R(x, yb-10, 1, 10, C.woodD); R(x-2, yb-5, 1, 1, C.lit); R(x+2, yb-5, 1, 1, C.lit);
      R(x-7, yb, 14, 2, C.stoneL);
      anims.push(t => { for (let i = 0; i < 7; i++){ const off = Math.round(Math.sin(t*4 - i*.8) * 1); R(tx+6+i, yb-64+off, 1, 4, i < 6 ? "#c0392b" : "#962d22"); } });
      lamps.push([x-10, yb+1], [x+10, yb+1]);
      return { door:[x, yb] };
    },
    learn(x, yb){
      const x0 = x-21;
      shadow(x0, yb, 42);
      walls(x0, yb, 42, 18, "#b5654a", "#8f4b36");
      for (let y = yb-17, k = 0; y < yb-2; y += 3, k++){ R(x0, y, 40, 1, "#a2583f"); for (let i = (k % 2) * 3; i < 40; i += 6) R(x0+i, y-2, 1, 2, "#a2583f"); }
      gable(x0, yb-19, 42, "#4d5d78", "#384559", "#5f7091");
      const bx = x0+5;
      R(bx, yb-38, 9, 16, C.plaster); R(bx+7, yb-38, 2, 16, C.plasterD); R(bx+2, yb-35, 5, 5, "#3a2a1c");
      gable(bx, yb-39, 9, "#4d5d78", "#384559", "#5f7091");
      win(x0+18, yb-14); win(x0+27, yb-14); win(x0+35, yb-14);
      door(x0+6, yb, 6, 9);
      R(x0+44, yb-8, 1, 8, C.woodD); R(x0+42, yb-12, 8, 5, "#2f4a35"); R(x0+43, yb-11, 3, 1, C.white); R(x0+43, yb-9, 5, 1, C.white);
      anims.push(t => { const s = Math.round(Math.sin(t*3) * (Math.sin(t*.4) > .7 ? 1 : 0)); R(bx+3+s, yb-34, 3, 3, "#e1b12c"); R(bx+4+s, yb-31, 1, 1, "#b8901d"); });
      return { door:[x0+9, yb] };
    },
    python(x, yb){
      const x0 = x-22;
      shadow(x0, yb, 44);
      walls(x0, yb, 44, 20, C.stoneL, C.stone);
      gable(x0, yb-21, 44, "#4f7a3a", "#3a5c2a", "#5f8f46");
      R(x0-1, yb-22, 46, 2, C.stone);
      win(x0+8, yb-15); win(x0+32, yb-15);
      for (const cx of [x0+3, x0+14, x0+27, x0+38]){ R(cx, yb-19, 3, 17, C.white); R(cx+2, yb-19, 1, 17, C.stoneL); R(cx-1, yb-19, 5, 1, C.stone); }
      R(x-7, yb-18, 14, 5, C.woodD);
      R(x-6, yb-17, 4, 1, "#3b6fb6"); R(x-3, yb-16, 3, 1, "#3b6fb6"); R(x-1, yb-17, 3, 1, "#f2c641"); R(x+2, yb-16, 4, 1, "#f2c641"); R(x-6, yb-16, 1, 1, "#f2c641");
      door(x-3, yb, 6, 10);
      R(x0+1, yb, 42, 2, C.stoneL);
      lamps.push([x0-3, yb+1]);
      return { door:[x, yb] };
    },
    linux(x, yb){
      R(x-20, yb-1, 40, 3, "#e3edf1");
      for (let dy = 0; dy < 15; dy++){ const hw = Math.round(Math.sqrt(225 - dy*dy)); R(x-hw, yb-dy-1, hw*2, 1, "#eaf2f6"); R(x+hw-3, yb-dy-1, 3, 1, "#c5d6de"); }
      for (const dy of [4, 8, 12]){ const hw = Math.round(Math.sqrt(225 - dy*dy)); R(x-hw, yb-dy-1, hw*2, 1, "#b4c8d2"); for (let i = -hw + ((dy/4) % 2) * 3; i < hw; i += 6) R(x+i, yb-dy-4, 1, 3, "#b4c8d2"); }
      R(x-13, yb-9, 9, 9, "#eaf2f6"); R(x-13, yb-9, 9, 1, "#c5d6de");
      R(x-11, yb-6, 5, 6, "#2c3a46"); R(x-10, yb-7, 3, 1, "#2c3a46");
      anims.push(t => {
        const px = x + 12 + Math.round((Math.sin(t*.45) + 1) * 6), step = Math.floor(t*4) % 2;
        R(px, yb-7, 4, 6, "#1f2329"); R(px+1, yb-5, 2, 4, "#f4f4f4"); R(px+1, yb-7, 1, 1, "#f4f4f4");
        R(px+ (Math.cos(t*.45) > 0 ? 3 : 0), yb-6, 1, 1, "#f2a33a");
        R(px + step, yb-1, 1, 1, "#f2a33a"); R(px + 2 + step, yb-1, 1, 1, "#f2a33a");
      });
      return { door:[x-8, yb] };
    },
    systems(x, yb){
      const x0 = x-20;
      shadow(x0, yb, 40);
      walls(x0, yb, 40, 16, "#8a8176", "#6b635a"); texture(x0, yb-16, 38, 14, "#756d63", 40);
      gable(x0, yb-17, 40, "#4a3b33", "#352a24", "#5a4a40");
      R(x0+28, yb-36, 7, 14, "#7a5444"); R(x0+27, yb-37, 9, 2, "#4f3429"); smokes.push({ x:x0+31, y:yb-39, rate:.5, heavy:true });
      R(x0+5, yb-12, 16, 12, "#3a2a20"); R(x0+6, yb-11, 14, 11, "#1e130d");
      R(x0-8, yb-4, 7, 2, "#3b3b40"); R(x0-6, yb-2, 3, 2, "#3b3b40"); R(x0-9, yb-4, 1, 1, "#3b3b40");
      win(x0+28, yb-12);
      anims.push(t => {
        for (let i = 0; i < 26; i++){ const fx = x0+7 + ((i*7 + Math.floor(t*9)) % 12), fy = yb-1 - ((i*5 + Math.floor(t*13)) % 7); R(fx, fy, 1, 1, ["#ff8a2a", "#ffb347", "#d9531e", "#ffd27a"][(i + Math.floor(t*8)) % 4]); }
        R(x0+6, yb-3, 14, 3, `rgba(255,140,50,${.55 + .25*Math.sin(t*9)})`);
        if (Math.sin(t*5) > .85) R(x0-5 + Math.round(Math.sin(t*20)*2), yb-6 - Math.round((t*20) % 4), 1, 1, "#ffd27a");
      });
      return { door:[x0+13, yb] };
    },
    web(x, yb){
      const x0 = x-22;
      const stripes = [["#d6453a", C.white], ["#3f7fbf", C.white], ["#e8a838", C.white]];
      shadow(x0, yb, 44);
      stripes.forEach(([c1, c2], i) => {
        const sx = x0 + i*15;
        R(sx, yb-14, 1, 14, C.woodD); R(sx+13, yb-14, 1, 14, C.woodD);
        for (let row = 0; row < 4; row++) for (let col = 0; col < 16; col++) R(sx-1+col, yb-18+row, 1, 1, (col >> 1) % 2 ? c2 : c1);
        for (let col = 0; col < 16; col += 2) R(sx-1+col, yb-14, 1, 1, c1);
        R(sx, yb-6, 14, 6, C.wood); R(sx, yb-6, 14, 1, C.woodL);
        for (let k = 0; k < 6; k++) R(sx+1+k*2, yb-8, 2, 2, ["#d9412b", "#f08a24", "#7cbf3c", "#f2c641", "#9b59b6", "#d9412b"][(k + i*2) % 6]);
        lamps.push([sx+7, yb-15]);
      });
      R(x0+46, yb-5, 6, 5, C.woodL); R(x0+46, yb-5, 6, 1, C.wood); R(x0+47, yb-7, 4, 2, "#7cbf3c");
      return { door:[x, yb] };
    },
    tools(x, yb){
      const x0 = x-19;
      shadow(x0, yb, 38);
      walls(x0, yb, 38, 16, "#9a6a3c", "#7a5230");
      for (let y = yb-15; y < yb-2; y += 3) R(x0, y, 36, 1, "#86592f");
      gable(x0, yb-17, 38, "#6b4423", "#4f311a", "#7f5530");
      chimney(x0+7, yb-21);
      win(x0+24, yb-12); door(x0+8, yb, 6, 9);
      R(x0+40, yb-5, 9, 1, C.woodL); R(x0+41, yb-4, 1, 4, C.woodD); R(x0+47, yb-4, 1, 4, C.woodD); R(x0+42, yb-6, 5, 1, "#c9c2b5");
      for (const [lx, ly] of [[x0-9, yb-4], [x0-5, yb-4], [x0-7, yb-7]]){ R(lx, ly, 4, 4, "#7a4f2a"); R(lx+1, ly+1, 2, 2, "#c99a5b"); R(lx+2, ly+2, 1, 1, "#7a4f2a"); }
      return { door:[x0+11, yb] };
    },
    data(x, yb){
      shadow(x-14, yb, 40);
      for (const sx of [x-14, x-2]){
        R(sx, yb-24, 11, 24, "#d3cec2"); R(sx+8, yb-24, 3, 24, "#aca79b");
        for (const by of [yb-20, yb-13, yb-6]) R(sx, by, 11, 1, "#9b968a");
        for (let dy = 0; dy < 6; dy++){ const hw = Math.round(Math.sqrt(36 - dy*dy)) - (dy === 0 ? 0 : 0); R(sx+5.5-hw, yb-25-dy, hw*2, 1, dy % 2 ? "#b84a35" : "#a3412f"); }
        R(sx+2, yb-22, 1, 22, C.woodD); for (let y = yb-21; y < yb; y += 3) R(sx+1, y, 3, 1, C.woodD);
      }
      R(x+13, yb-10, 12, 10, "#a3392b"); R(x+13, yb-10, 12, 1, C.white); gable(x+13, yb-11, 12, "#6e5a48", "#5c4a3a", "#7d6855");
      R(x+16, yb-7, 6, 7, "#2a1d12"); R(x+16, yb-7, 6, 1, C.white);
      return { door:[x+19, yb] };
    },
    security(x, yb){
      const x0 = x-24;
      shadow(x0, yb, 48);
      walls(x0+6, yb, 36, 14, C.stone, C.stoneD); texture(x0+6, yb-14, 34, 12, C.stoneD, 30);
      for (let i = 0; i < 36; i += 4) R(x0+6+i, yb-16, 2, 2, C.stone);
      for (const tx of [x0, x0+38]){
        R(tx, yb-26, 10, 26, C.stoneL); R(tx+8, yb-26, 2, 26, C.stone); texture(tx, yb-26, 8, 24, C.stone, 14);
        for (let i = 0; i < 10; i += 3) R(tx+i, yb-28, 2, 2, C.stoneL);
        R(tx+4, yb-21, 1, 4, C.ink); win(tx+3, yb-13);
        R(tx+4, yb-37, 1, 9, C.ink);
      }
      R(x-4, yb-10, 8, 10, "#2a1d12"); R(x-3, yb-11, 6, 1, "#2a1d12");
      for (let i = 0; i < 4; i++) R(x-3+i*2, yb-10, 1, 10, "#6a6058"); R(x-4, yb-6, 8, 1, "#6a6058");
      anims.push(t => { for (const tx of [x0, x0+38]) for (let i = 0; i < 6; i++){ const off = Math.round(Math.sin(t*3.6 - i*.9 + tx)); R(tx+5+i, yb-37+off, 1, 4, i === 2 && off === 0 ? "#f2c641" : "#b03a2e"); } });
      lamps.push([x-7, yb-12], [x+7, yb-12]);
      return { door:[x, yb] };
    },
    devops(x, yb){
      const x0 = x-20;
      for (let y = yb+8; y < 266; y += 2){ R(x-6, y, 12, 2, (y/2) % 2 ? C.woodL : C.wood); }
      for (const px of [x-6, x+5]) R(px, yb+8, 1, 30, C.woodD);
      shadow(x0, yb, 40);
      const box = (bx, by, c, cd) => { R(bx, by, 12, 7, c); for (let i = 1; i < 12; i += 2) R(bx+i, by+1, 1, 5, cd); R(bx, by, 12, 1, cd); R(bx+11, by, 1, 7, cd); };
      box(x0, yb-7, "#c0392b", "#952c21"); box(x0+13, yb-7, "#2e86c1", "#22679a"); box(x0+26, yb-7, "#27ae60", "#1e8449");
      box(x0+6, yb-14, "#f39c12", "#c27d0e"); box(x0+19, yb-14, "#8e44ad", "#6c3483");
      R(x0+39, yb-3, 2, 3, C.stoneD); R(x0+38, yb-4, 4, 1, C.stoneD);
      anims.push(t => {
        const wx = x+16 + Math.round(Math.sin(t*.3)*6), wy = 259 + Math.round(Math.sin(t*1.4));
        R(wx, wy, 14, 4, "#2496ed"); R(wx+1, wy-1, 12, 1, "#2496ed"); R(wx-2, wy+1, 3, 2, "#2496ed"); R(wx-3, wy, 1, 2, "#2496ed");
        R(wx+2, wy+3, 10, 1, "#1b78c2"); R(wx+11, wy+1, 1, 1, C.white);
        for (let i = 0; i < 3; i++) R(wx+3+i*3, wy-3, 2, 2, ["#f39c12", "#c0392b", "#27ae60"][i]);
        const sp = (t*2) % 3; if (sp < 1.6) for (let i = 0; i < 3; i++) R(wx+12 + (i-1)*Math.round(sp*1.5), wy-3 - Math.round(sp*3) + Math.abs(i-1), 1, 1, C.foam);
      });
      return { door:[x, yb] };
    },
    network(x, yb){
      shadow(x-7, yb, 30);
      for (let i = 0; i < 56; i++){
        const y = yb-i, hw = Math.round(6 - i*5/56), col = Math.floor(i/8) % 2 ? "#d64a3b" : "#efe7da";
        R(x-hw, y, 1, 1, col); R(x+hw, y, 1, 1, col);
        if (i % 6 === 0) R(x-hw, y, hw*2+1, 1, col);
        else { const f = (i % 6) / 6; R(x-hw + Math.round(f*hw*2), y, 1, 1, col); }
      }
      walls(x+6, yb, 16, 10, C.plaster, C.plasterD); R(x+5, yb-11, 18, 2, C.stoneD);
      win(x+15, yb-8); door(x+8, yb, 4, 7);
      anims.push(t => {
        if (Math.sin(t*3) > 0) { R(x-1, yb-58, 3, 2, "#ff3b30"); R(x-2, yb-59, 5, 4, "rgba(255,70,50,.25)"); } else R(x-1, yb-58, 3, 2, "#7a1f19");
        for (let k = 0; k < 2; k++){
          const r = ((t*14 + k*12) % 24) + 4, a = 1 - r/28;
          for (let ang = -2.6; ang < -.5; ang += .18) R(x + Math.round(Math.cos(ang)*r), yb-57 + Math.round(Math.sin(ang)*r*.7), 1, 1, `rgba(255,236,190,${a*.8})`);
        }
      });
      return { door:[x+10, yb] };
    },
    homelab(x, yb){
      const x0 = x-20;
      shadow(x0, yb, 40);
      walls(x0, yb, 40, 16, "#a3392b", "#7e2a20");
      for (let i = 1; i < 38; i += 3) R(x0+i, yb-16, 1, 14, "#8f3125");
      R(x0, yb-16, 40, 1, C.white);
      let l = x0-2, r = x0+42, i = 0;
      while (r - l > 4){ R(l, yb-17-i, r-l, 1, i % 2 ? "#5c4a3a" : "#6e5a48"); const s = i < 3 ? 1 : 3; l += s; r -= s; i++; }
      R(x-3, yb-25, 6, 5, "#2a1d12"); R(x-4, yb-26, 8, 1, C.white);
      R(x-9, yb-13, 18, 13, C.white); R(x-8, yb-12, 16, 12, "#121820");
      for (const rx of [x-7, x+1]){ R(rx, yb-11, 6, 11, "#2c343c"); for (let y = yb-10; y < yb; y += 2) R(rx+1, y, 4, 1, "#1a2026"); }
      win(x0+3, yb-12); win(x0+33, yb-12);
      anims.push(t => {
        const f = Math.floor(t*6);
        for (const rx of [x-7, x+1]) for (let y = yb-10, k = 0; y < yb; y += 2, k++){
          const h = (k*7 + rx*3 + f) % 5;
          R(rx+1, y, 1, 1, h < 3 ? "#5fe37a" : "#24402c");
          R(rx+3, y, 1, 1, h === 4 ? "#ffb347" : (h % 2 ? "#5fe37a" : "#24402c"));
        }
      });
      return { door:[x, yb] };
    },
    health(x, yb){
      const x0 = x-20;
      R(x0, yb-18, 40, 18, "#7a5232");
      for (let r = 0; r < 6; r++){
        const y = yb-17 + r*3;
        R(x0+1, y+1, 38, 1, "#634126");
        const crop = ["#f08a24", "#5aa83c", "#d9412b", "#5aa83c", "#f2c641", "#5aa83c"][r];
        for (let cx = x0+2; cx < x0+38; cx += 3){ R(cx, y, 1, 1, "#5aa83c"); R(cx+1, y-1, 1, 1, "#6fc04a"); if (r % 2 === 0) R(cx, y+1, 1, 1, crop); }
      }
      R(x0-1, yb-20, 42, 1, C.woodL); R(x0-1, yb+1, 17, 1, C.woodL); R(x0+24, yb+1, 17, 1, C.woodL);
      for (let px = x0-1; px <= x0+41; px += 6){ R(px, yb-21, 1, 3, C.woodD); R(px, yb, 1, 3, C.woodD); }
      R(x0-1, yb-20, 1, 22, C.woodL); R(x0+40, yb-20, 1, 22, C.woodL);
      const sx = x0+29;
      R(sx+2, yb-26, 1, 11, C.woodD); R(sx-1, yb-22, 7, 1, C.woodD); R(sx+1, yb-28, 3, 3, "#e9c46a"); R(sx, yb-29, 5, 1, C.woodD); R(sx+1, yb-22, 3, 4, "#4f7fbf");
      R(x0-8, yb-3, 1, 3, "#3b3b40"); R(x0-7, yb-2, 4, 1, "#6b6b72"); R(x0-3, yb-3, 1, 3, "#3b3b40");
      anims.push(t => {
        const cx = x0+8 + Math.round((Math.sin(t*.5) + 1) * 8), peck = Math.sin(t*5) > .6 ? 1 : 0;
        R(cx, yb+3, 4, 3, C.white); R(cx+3, yb+1+peck, 2, 2, C.white); R(cx+4, yb+1+peck, 1, 1, "#d9412b"); R(cx+5, yb+2+peck, 1, 1, "#f2a33a"); R(cx+1, yb+6, 1, 1, "#f2a33a"); R(cx+2, yb+6, 1, 1, "#f2a33a");
        const bx = x0+14 + Math.round(Math.sin(t*1.3)*10), by = yb-24 + Math.round(Math.sin(t*2.7)*3);
        R(bx, by, 1, 1, "#f6f0a0"); R(bx + (Math.floor(t*8) % 2 ? 1 : -1), by-1, 1, 1, "#f6f0a0");
      });
      return { door:[x, yb+2] };
    },
  };
  const DEF = [
    { id:"rising",   name:"New Builds",       x:50,  row:0 },
    { id:"ai",       name:"Observatory",      x:134, row:0 },
    { id:"awesome",  name:"Town Hall",        x:240, row:0 },
    { id:"learn",    name:"Schoolhouse",      x:345, row:0 },
    { id:"python",   name:"Serpent Library",  x:434, row:0 },
    { id:"linux",    name:"Penguin Lodge",    x:44,  row:1 },
    { id:"systems",  name:"The Forge",        x:130, row:1 },
    { id:"web",      name:"Market Hall",      x:330, row:1 },
    { id:"tools",    name:"Tinker Workshop",  x:432, row:1 },
    { id:"data",     name:"Granary",          x:34,  row:2 },
    { id:"security", name:"Watch Keep",       x:128, row:2 },
    { id:"devops",   name:"Container Docks",  x:198, row:2 },
    { id:"network",  name:"Radio Tower",      x:280, row:2 },
    { id:"homelab",  name:"Server Barn",      x:356, row:2 },
    { id:"health",   name:"Green Farm",       x:446, row:2 },
  ].filter(d => CAT[d.id]);
  const NAME = Object.fromEntries(DEF.map(d => [d.id, d.name]));

  let buildings = [], trees = [], nodes = [], villagers = [], particles = [], birds = [];
  let built = false;

  function drawTree(t){
    const { x, y, r, kind } = t;
    R(x-r, y, r*2, 2, "rgba(40,52,20,.35)");
    if (kind === "pine"){
      R(x, y-3, 2, 3, C.trunk);
      for (let i = 0; i < r+3; i++){ const hw = Math.round((i+1) * r / (r+3)); R(x+1-hw, y-4-(r+3)+i, hw*2, 1, i % 3 === 0 ? "#2f5e29" : "#3a6e30"); }
      return;
    }
    R(x, y-4, 2, 4, C.trunk);
    for (let dy = -r; dy <= r; dy++){ const hw = Math.round(Math.sqrt(r*r - dy*dy)); R(x+1-hw, y-4-r+dy, hw*2, 1, dy > r*.35 ? C.leafD : C.leaf); }
    for (let i = 0; i < r*2; i++){ const a = rnd()*6.28, d = rnd()*r*.7; R(x+1 + Math.cos(a)*d - 1, y-4-r + Math.sin(a)*d - 2, 1, 1, C.leafL); }
    if (kind === "fruit") for (let i = 0; i < 3; i++) R(x-2 + rnd()*5, y-4-r + rnd()*r, 1, 1, "#d9412b");
  }

  function buildStatic(){
    rnd = seeded(11);
    g = sg; bb = null;
    // ground
    R(0, 0, WW, WH, C.grass);
    for (let i = 0; i < 3200; i++) R(rnd()*WW, rnd()*WH, 1, 1, rnd() < .5 ? C.grassL : C.grassD);
    for (let i = 0; i < 300; i++){ const x = rnd()*WW, y = rnd()*WH; R(x, y, 1, 2, C.grassDD); R(x+1, y-1, 1, 2, C.grassD); }
    // river
    for (let x = 0; x < WW; x++){ const t = riverTop(x); R(x, t-3, 1, 3, C.sand); R(x, t, 1, WH-t, C.water); R(x, t, 1, 1, C.foam); R(x, t+7, 1, WH-t-7, C.waterD); }
    // roads: outlines first, then fill, then pebbles
    const segs = [];
    for (const y of ROAD) segs.push([14, y, 466, y]);
    for (const x of VROADS) segs.push([x, ROAD[0], x, ROAD[2]]);
    for (const d of DEF){ /* door stubs filled after buildings are measured */ }
    const outline = ([x1, y1, x2, y2]) => R(Math.min(x1, x2)-4, Math.min(y1, y2)-4, Math.abs(x2-x1)+9, Math.abs(y2-y1)+9, C.dirtD);
    const fill = ([x1, y1, x2, y2]) => R(Math.min(x1, x2)-3, Math.min(y1, y2)-3, Math.abs(x2-x1)+7, Math.abs(y2-y1)+7, C.dirt);

    // measure buildings on a scratch canvas so trees can avoid them
    const scratch = document.createElement("canvas").getContext("2d");
    const measured = DEF.map(d => {
      g = scratch; bb = { x0:1e9, y0:1e9, x1:-1e9, y1:-1e9 }; wins = []; smokes = []; lamps = []; anims = [];
      const info = B[d.id](d.x, ROW[d.row]);
      const box = bb; bb = null;
      return { ...d, yb:ROW[d.row], box, door:info.door };
    });
    g = sg;
    const stubs = measured.map(m => [m.door[0], m.door[1], m.door[0], ROAD[m.row]]);
    [...segs, ...stubs].forEach(outline);
    [...segs, ...stubs].forEach(fill);
    for (const s of [...segs, ...stubs]){
      const [x1, y1, x2, y2] = s, n = (Math.abs(x2-x1) + Math.abs(y2-y1)) * .25;
      for (let i = 0; i < n; i++){ const f = rnd(); R(x1 + (x2-x1)*f + (rnd()*5|0) - 2, y1 + (y2-y1)*f + (rnd()*5|0) - 2, 1, 1, rnd() < .5 ? C.dirtL : C.dirtD); }
    }
    // plaza
    for (let dy = -PLAZA.r; dy <= PLAZA.r; dy++) for (let dx = -PLAZA.r; dx <= PLAZA.r; dx++){
      const d = Math.hypot(dx, dy); if (d > PLAZA.r) continue;
      const x = PLAZA.x+dx, y = PLAZA.y+dy;
      R(x, y, 1, 1, d > PLAZA.r-1.2 ? C.stoneD : ((x % 5 === 0 || y % 4 === 0) ? C.stone : ((x*7 + y*3) % 11 === 0 ? "#b5ad9f" : C.stoneL)));
    }
    for (let dy = -8; dy <= 8; dy++) for (let dx = -8; dx <= 8; dx++){ const d = Math.hypot(dx, dy); if (d <= 8) R(PLAZA.x+dx, PLAZA.y+dy, 1, 1, d > 6.4 ? (dy > 0 ? C.stoneD : "#8d857a") : C.water); }
    R(PLAZA.x-1, PLAZA.y-4, 3, 6, C.stoneL); R(PLAZA.x-2, PLAZA.y-5, 5, 1, C.stone);
    for (const [bx, by] of [[PLAZA.x-17, PLAZA.y+8], [PLAZA.x+11, PLAZA.y+8], [PLAZA.x-17, PLAZA.y-11], [PLAZA.x+11, PLAZA.y-11]]){ R(bx, by, 7, 2, C.wood); R(bx, by+2, 1, 1, C.woodD); R(bx+6, by+2, 1, 1, C.woodD); }
    // flowers
    for (let i = 0; i < 160; i++){ const x = rnd()*WW|0, y = rnd()*240|0; R(x, y, 1, 1, ["#f2c641", "#f4efe4", "#e86a8a", "#9b7be0"][i % 4]); }

    // trees: avoid buildings, roads, plaza and river
    const clear = (x, y) => {
      if (y > 238 || y < 14 || x < 4 || x > WW-4) return false;
      for (const m of measured){ const b = m.box; if (x > b.x0-7 && x < b.x1+7 && y > b.y0-2 && y < b.y1+12) return false; }
      for (const yy of ROAD) if (Math.abs(y - yy) < 9) return false;
      for (const xx of VROADS) if (Math.abs(x - xx) < 9 && y > ROAD[0]-6 && y < ROAD[2]+6) return false;
      for (const s of stubs) if (Math.abs(x - s[0]) < 7 && y > s[1]-2 && y < s[3]+8) return false;
      if (Math.hypot(x - PLAZA.x, y - PLAZA.y) < PLAZA.r + 9) return false;
      return true;
    };
    trees = [];
    for (let i = 0; i < 900 && trees.length < 64; i++){
      const x = 6 + rnd()*(WW-12) | 0, y = 18 + rnd()*222 | 0;
      if (!clear(x, y) || trees.some(t => Math.hypot(t.x - x, t.y - y) < 11)) continue;
      const k = rnd();
      trees.push({ x, y, r: 4 + (rnd()*3|0), kind: k < .25 ? "pine" : k < .35 ? "fruit" : "oak" });
    }
    // lamp posts along the roads
    const roadLamps = [[64, ROAD[0]-5], [190, ROAD[0]-5], [300, ROAD[0]-5], [404, ROAD[0]-5], [24, ROAD[1]-5], [200, ROAD[1]-5], [282, ROAD[1]-5], [384, ROAD[1]-5], [70, ROAD[2]-5], [240, ROAD[2]-5], [318, ROAD[2]-5], [410, ROAD[2]-5], [PLAZA.x-22, PLAZA.y-16], [PLAZA.x+22, PLAZA.y-16]];

    // y-sorted draw: buildings, trees and lamp posts
    wins = []; smokes = []; lamps = []; anims = [];
    const items = [
      ...measured.map(m => ({ y:m.yb, draw: () => { bb = { x0:1e9, y0:1e9, x1:-1e9, y1:-1e9 }; B[m.id](m.x, m.yb); m.box = bb; bb = null; } })),
      ...trees.map(t => ({ y:t.y, draw: () => drawTree(t) })),
      ...roadLamps.map(([x, y]) => ({ y, draw: () => { R(x, y-9, 1, 9, C.ink); R(x-1, y-11, 3, 2, "#3a3020"); R(x, y-10, 1, 1, "#f6d27a"); lamps.push([x, y-10]); } })),
    ].sort((a, b) => a.y - b.y);
    for (const it of items) it.draw();
    buildings = measured.map(m => ({ id:m.id, name:m.name, x:m.x, yb:m.yb, row:m.row, box:m.box, door:m.door, match:0 }));

    // walking graph
    const map = new Map(); nodes = [];
    const node = (x, y) => { const k = x + "," + y; let n = map.get(k); if (!n){ n = { x, y, adj:[], b:null }; map.set(k, n); nodes.push(n); } return n; };
    const link = (a, b) => { if (a !== b && !a.adj.includes(b)){ a.adj.push(b); b.adj.push(a); } };
    ROAD.forEach((y, r) => {
      const xs = new Set([14, 466, ...VROADS, ...buildings.filter(b => b.row === r).map(b => b.door[0])]);
      const sorted = [...xs].sort((a, b) => a - b);
      for (let i = 1; i < sorted.length; i++) link(node(sorted[i-1], y), node(sorted[i], y));
    });
    for (const x of VROADS) for (let r = 1; r < ROAD.length; r++) link(node(x, ROAD[r-1]), node(x, ROAD[r]));
    for (const b of buildings){ const d = node(b.door[0], b.door[1]); d.b = b; link(d, node(b.door[0], ROAD[b.row])); }

    // villagers
    const vr = seeded(5);
    const shirts = ["#c0392b", "#2e86c1", "#27ae60", "#f39c12", "#8e44ad", "#e86a8a", "#16a085", "#d35400", "#f4efe4", "#34495e"];
    const hairs = ["#2a1d12", "#6b4423", "#e1b12c", "#b5452b", "#1a1a1a", "#d9d2c3"];
    const skins = ["#f1c9a0", "#d9a77c", "#a8754e", "#7a4f32", "#f5d5b5"];
    villagers = [];
    const starts = nodes.filter(n => !n.b);
    for (let i = 0; i < 16; i++){
      const n = starts[(vr()*starts.length)|0];
      villagers.push({ x:n.x, y:n.y, from:n, to:n.adj[(vr()*n.adj.length)|0], inside:0, dist:0, speed:.35 + vr()*.25,
        shirt:shirts[i % shirts.length], hair:hairs[(vr()*hairs.length)|0], skin:skins[(vr()*skins.length)|0], pants: vr() < .5 ? "#3b4a6b" : "#4a3b2a", carry: vr() < .25 ? ["#c99a5b", "#7cbf3c", "#e8e2d0"][(vr()*3)|0] : null, pause:0 });
    }
    // capture the anims of the y-sorted pass (these are the ones we run each frame)
    built = true;
  }

  /* --- simulation --- */
  function stepVillagers(dt){
    for (const v of villagers){
      if (v.inside > 0){ v.inside -= dt; continue; }
      if (v.pause > 0){ v.pause -= dt; continue; }
      const dx = v.to.x - v.x, dy = v.to.y - v.y, d = Math.hypot(dx, dy), sp = v.speed * dt * 20;
      if (d <= sp){
        v.x = v.to.x; v.y = v.to.y;
        const at = v.to;
        if (at.b && Math.random() < .55){ v.inside = 2 + Math.random()*6; }
        else if (Math.random() < .08) v.pause = 1 + Math.random()*2;
        const opts = at.adj.filter(n => n !== v.from);
        v.from = at; v.to = (opts.length ? opts : at.adj)[(Math.random() * (opts.length || at.adj.length))|0];
      } else { v.x += dx/d*sp; v.y += dy/d*sp; v.dist += sp; }
    }
  }
  function drawVillager(v){
    if (v.inside > 0) return;
    const x = Math.round(v.x) - 1, y = Math.round(v.y) + 1, step = Math.floor(v.dist/2.5) % 2;
    R(x-1, y+1, 5, 1, "rgba(30,40,15,.35)");
    if (step){ R(x, y-1, 1, 2, v.pants); R(x+2, y, 1, 1, v.pants); } else { R(x, y, 1, 1, v.pants); R(x+2, y-1, 1, 2, v.pants); }
    R(x, y-4, 3, 3, v.shirt);
    R(x, y-6, 3, 2, v.skin);
    R(x, y-7, 3, 1, v.hair);
    if (v.carry) R(x+3, y-4, 2, 2, v.carry);
  }
  function stepParticles(dt, t){
    for (const s of smokes){ s.acc = (s.acc || 0) + dt * (s.rate * 6); while (s.acc > 1){ s.acc--; particles.push({ x:s.x + (Math.random()-.5)*2, y:s.y, life:0, max: s.heavy ? 3.4 : 2.6, heavy:s.heavy, seed:Math.random()*6 }); } }
    particles = particles.filter(p => (p.life += dt) < p.max);
    for (const p of particles){ p.y -= dt * (p.heavy ? 6 : 5); p.x += Math.sin(t*1.5 + p.seed) * dt * 3 + dt*2; }
    if (Math.random() < dt * .08 && birds.length < 3) birds.push({ x:-8, y:12 + Math.random()*70, v:18 + Math.random()*12, f:Math.random()*6 });
    birds = birds.filter(b => (b.x += b.v*dt) < WW + 10);
  }

  /* --- light: follow the viewer's local time --- */
  const KEYS = [[0,[132,112,158],1],[5,[140,118,160],1],[6.5,[255,200,172],.35],[8,[255,246,232],0],[16,[255,242,222],0],[18,[255,210,158],.15],[19.6,[238,170,148],.45],[21,[150,124,162],.9],[24,[132,112,158],1]];
  let timeMode = "live";
  const MODES = { live:null, day:12, golden:18.4, night:23 };
  function light(){
    const now = new Date();
    const h = MODES[timeMode] ?? (now.getHours() + now.getMinutes()/60);
    let i = 0; while (i < KEYS.length-2 && KEYS[i+1][0] <= h) i++;
    const [h0, c0, d0] = KEYS[i], [h1, c1, d1] = KEYS[i+1], f = (h - h0) / (h1 - h0 || 1);
    return { tint: c0.map((v, k) => Math.round(v + (c1[k]-v)*f)), dark: d0 + (d1-d0)*f, hour:h };
  }

  /* --- view --- */
  let W = 0, H = 0, dpr = 1, s = 2, panX = 0, panY = 0, tpanX = null, small = false;
  let hover = null, visible = true, raf = 0, last = 0, acc = 0, T = 0, L = light();
  function size(){
    const rect = cv.getBoundingClientRect();
    small = innerWidth <= 900;
    W = rect.width;
    H = small ? Math.max(360, Math.min(560, innerHeight * .62)) : Math.max(440, Math.min(innerHeight * .8, W / 1.78));
    cv.style.height = H + "px";
    dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr);
    s = Math.max(W/WW, H/WH);
    clampPan(true);
  }
  function clampPan(center){
    const mx = Math.max(0, WW*s - W), my = Math.max(0, WH*s - H);
    if (center){ panX = mx/2; panY = my/2; }
    panX = Math.max(0, Math.min(mx, panX)); panY = Math.max(0, Math.min(my, panY));
  }
  const toScreen = (x, y) => [x*s - panX, y*s - panY];
  const toWorld = (sx, sy) => [(sx + panX)/s, (sy + panY)/s];

  function frame(){
    // world layer
    g = wg; bb = null;
    wg.globalCompositeOperation = "source-over";
    wg.drawImage(sc, 0, 0);
    // water shimmer
    for (let i = 0; i < 70; i++){ const x = (i*37 + Math.floor(T*8)*(i%3+1)) % WW, y = riverTop(x) + 2 + ((i*13) % 18); if (y < WH) R(x, y, 2, 1, i % 4 ? "rgba(140,200,235,.55)" : "rgba(230,245,255,.7)"); }
    // fountain
    for (let i = 0; i < 6; i++){ const ph = (T*1.6 + i/6) % 1, a = i/6*6.283; R(PLAZA.x + Math.round(Math.cos(a)*ph*5), PLAZA.y - 5 + Math.round(ph*ph*9 - ph*6), 1, 1, "rgba(220,240,255,.9)"); }
    if (Math.floor(T*4) % 2) R(PLAZA.x-4, PLAZA.y+2, 2, 1, "rgba(220,240,255,.7)"); else R(PLAZA.x+3, PLAZA.y-2, 2, 1, "rgba(220,240,255,.7)");
    for (const a of anims) a(T);
    // smoke
    for (const p of particles){ const k = p.life / p.max, sz = p.heavy ? (k < .4 ? 2 : 3) : (k < .5 ? 1 : 2); R(p.x, p.y, sz, sz, `rgba(${p.heavy ? "150,140,132" : "205,200,192"},${(1-k)*.75})`); }
    // villagers, sorted for depth
    for (const v of [...villagers].sort((a, b) => a.y - b.y)) drawVillager(v);
    // birds
    for (const b of birds){ const up = Math.floor(T*6 + b.f) % 2; const x = Math.round(b.x), y = Math.round(b.y); R(x, y + (up ? 0 : 1), 1, 1, "#2a241c"); R(x+1, y+1, 1, 1, "#2a241c"); R(x+2, y + (up ? 0 : 1), 1, 1, "#2a241c"); }
    // light
    const [tr, tg, tb] = L.tint;
    wg.globalCompositeOperation = "multiply"; wg.fillStyle = `rgb(${tr},${tg},${tb})`; wg.fillRect(0, 0, WW, WH);
    wg.globalCompositeOperation = "source-over";
    if (L.dark > .12){
      const d = L.dark;
      wins.forEach(([x, y], i) => { if ((i*7 + 3) % 9 === 0 && d < .8) return; const flick = (i*13 + Math.floor(T*.5)) % 23 === 0 ? .7 : 1;
        R(x, y, 4, 4, `rgba(255,214,120,${Math.min(1, d*1.4)*flick})`); R(x+2, y, 1, 4, C.woodD); R(x, y+2, 4, 1, C.woodD); });
      wg.globalCompositeOperation = "lighter";
      wins.forEach(([x, y]) => R(x-2, y-2, 8, 8, `rgba(255,170,60,${d*.12})`));
      lamps.forEach(([x, y]) => { R(x-4, y-3, 9, 7, `rgba(255,170,70,${d*.14})`); R(x-2, y-1, 5, 3, `rgba(255,200,110,${d*.25})`); R(x, y, 1, 1, `rgba(255,236,170,${d})`); });
      const forge = buildings.find(b => b.id === "systems");
      if (forge) R(forge.box.x0+2, forge.box.y1-14, 22, 14, `rgba(255,120,40,${d*.18 + .04*Math.sin(T*9)})`);
      if (d > .6) for (let i = 0; i < 10; i++){ const fx = (i*53 + Math.sin(T*.7 + i)*14 + 400) % WW, fy = 30 + (i*41) % 200 + Math.sin(T + i*2)*6; if (Math.sin(T*2.3 + i*1.7) > .2) R(fx, fy, 1, 1, "rgba(220,255,140,.9)"); }
      wg.globalCompositeOperation = "source-over";
    }

    // screen
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(wc, 0, 0, WW, WH, -panX, -panY, WW*s, WH*s);
    drawOverlay();
  }

  function sign(text, sx, sy, opt){
    ctx.font = `600 ${small ? 11 : 12.5}px "Pixelify Sans", ui-monospace, monospace`;
    const w = Math.ceil(ctx.measureText(text).width) + 14, h = small ? 18 : 20;
    const x = Math.round(sx - w/2), y = Math.round(sy - h);
    ctx.globalAlpha = opt.alpha;
    ctx.fillStyle = "#1f150c"; ctx.fillRect(x-1, y+1, w+2, h-2); ctx.fillRect(x+1, y-1, w-2, h+2);
    ctx.fillStyle = opt.active ? "#6a4523" : "#4a311b"; ctx.fillRect(x, y, w, h);
    ctx.fillStyle = opt.active ? "#8a5d31" : "#5e3f23"; ctx.fillRect(x, y, w, 2);
    ctx.fillStyle = opt.active ? "#fff1cf" : "#f3e3c2"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(text, x + w/2, y + h/2 + 1);
    ctx.globalAlpha = 1;
    return { x, y, w, h };
  }
  function drawOverlay(){
    const filtering = !!(S.q || S.view !== "all" || S.fresh || S.lib);
    for (const b of buildings){
      const [cx] = toScreen((b.box.x0 + b.box.x1)/2, 0), [, ty] = toScreen(0, b.box.y0);
      if (cx < -100 || cx > W+100) continue;
      const sel = S.cat === b.id, hot = hover?.b === b;
      const alpha = filtering && !b.match && !sel ? .5 : 1;
      const r = sign(b.name, cx, Math.max(small ? 24 : 26, ty - 4), { alpha, active: sel || hot });
      if (filtering && b.match){
        const bob = Math.round(Math.sin(T*4 + b.x) * 2);
        const txt = String(b.match);
        ctx.font = `700 ${small ? 11 : 12}px "Pixelify Sans", ui-monospace, monospace`;
        const w = Math.ceil(ctx.measureText(txt).width) + 12, x = Math.round(r.x + r.w - 4), y = r.y - 12 + bob;
        ctx.fillStyle = "#1f150c"; ctx.fillRect(x-1, y-1, w+2, 18);
        ctx.fillStyle = "#f2b544"; ctx.fillRect(x, y, w, 16);
        ctx.fillStyle = "#2a1d12"; ctx.textAlign = "center"; ctx.fillText(txt, x + w/2, y + 9);
      }
      if (sel || hot){
        const [x0, y0] = toScreen(b.box.x0 - 2, b.box.y0 - 2), [x1, y1] = toScreen(b.box.x1 + 2, b.box.y1 + 2);
        const L2 = Math.max(8, s*4);
        ctx.fillStyle = sel ? "#f2b544" : "#fff1cf";
        for (const [px, py, dx, dy] of [[x0, y0, 1, 1], [x1, y0, -1, 1], [x0, y1, 1, -1], [x1, y1, -1, -1]]){
          ctx.fillRect(dx > 0 ? px : px - L2, dy > 0 ? py : py - 3, L2, 3);
          ctx.fillRect(dx > 0 ? px : px - 3, dy > 0 ? py : py - L2, 3, L2);
        }
        if (sel){
          const bob = Math.round(Math.sin(T*5) * 3), ax = Math.round(cx), ay = r.y - 10 + bob;
          ctx.fillStyle = "#1f150c"; ctx.fillRect(ax-7, ay-9, 14, 6); ctx.fillRect(ax-5, ay-3, 10, 2); ctx.fillRect(ax-3, ay-1, 6, 2); ctx.fillRect(ax-1, ay+1, 2, 2);
          ctx.fillStyle = "#f2b544"; ctx.fillRect(ax-6, ay-8, 12, 4); ctx.fillRect(ax-4, ay-4, 8, 2); ctx.fillRect(ax-2, ay-2, 4, 2);
        }
      }
    }
  }

  function loop(now){
    raf = 0;
    const dt = Math.min(.1, (now - (last || now)) / 1000); last = now;
    acc += dt;
    if (acc >= 1/20){
      const step = reduceMotion ? 0 : acc; acc = 0;
      T += step;
      if (step){ stepVillagers(step); stepParticles(step, T); }
      if (tpanX != null){ panX += (tpanX - panX) * .2; if (Math.abs(tpanX - panX) < .5){ panX = tpanX; tpanX = null; } clampPan(); }
      if (Math.floor(T) % 10 === 0) L = light();
      frame();
    }
    if (visible && (!reduceMotion || tpanX != null)) raf = requestAnimationFrame(loop);
  }
  function kick(){ if (!raf && visible){ if (reduceMotion){ frame(); if (tpanX == null) return; } raf = requestAnimationFrame(loop); } }

  /* --- input --- */
  function pick(sx, sy){
    const [x, y] = toWorld(sx, sy);
    for (const v of villagers){ if (v.inside > 0) continue; if (Math.abs(v.x - x) < 3.5 && y > v.y - 8 && y < v.y + 2.5) return { v }; }
    // signs first (they float above the buildings)
    ctx.font = `600 ${small ? 11 : 12.5}px "Pixelify Sans", ui-monospace, monospace`;
    for (const b of buildings){
      const [cx] = toScreen((b.box.x0 + b.box.x1)/2, 0), [, ty] = toScreen(0, b.box.y0);
      const w = ctx.measureText(b.name).width + 14, h = small ? 18 : 20, sy0 = Math.max(small ? 24 : 26, ty - 4) - h;
      if (sx > cx - w/2 && sx < cx + w/2 && sy > sy0 && sy < sy0 + h) return { b };
    }
    let best = null, area = Infinity;
    for (const b of buildings){ const bx = b.box; if (x > bx.x0-2 && x < bx.x1+2 && y > bx.y0-2 && y < bx.y1+4){ const a = (bx.x1-bx.x0)*(bx.y1-bx.y0); if (a < area){ area = a; best = b; } } }
    return best ? { b:best } : null;
  }
  let down = null;
  cv.addEventListener("pointerdown", e => { down = { x:e.clientX, y:e.clientY, px:panX, py:panY, drag:false, id:e.pointerId }; });
  cv.addEventListener("pointermove", e => {
    const r = cv.getBoundingClientRect(), sx = e.clientX - r.left, sy = e.clientY - r.top;
    if (down){
      const dx = e.clientX - down.x, dy = e.clientY - down.y;
      if (!down.drag && Math.hypot(dx, dy) > 6 && (WW*s > W + 1 || WH*s > H + 1)){ down.drag = true; try{ cv.setPointerCapture(down.id); }catch{} tip.hidden = true; }
      if (down.drag){ tpanX = null; panX = down.px - dx; panY = down.py - (e.pointerType === "touch" ? 0 : dy); clampPan(); cv.style.cursor = "grabbing"; if (reduceMotion) frame(); return; }
    }
    if (e.pointerType === "touch") return;
    const p = pick(sx, sy), prev = hover;
    hover = p;
    if (p?.b){
      const b = p.b, c = CAT[b.id];
      tip.innerHTML = `<b>${esc(b.name)}</b><p>${esc(c.name)} · ${esc(c.desc)}</p><div class="m">${(ALL.filter(r => r.cats.includes(b.id)).length)} repos${b.match && (S.q || S.view !== "all") ? ` · ${b.match} match` : ""} · click to go inside</div>`;
    } else if (p?.v){
      tip.innerHTML = `<b>A villager</b><p>They know a good repo. Click to ask.</p>`;
    }
    if (p){
      tip.hidden = false;
      const tw = tip.offsetWidth, th = tip.offsetHeight;
      let tx = sx + 16, ty = sy + 16;
      if (tx + tw > W - 8) tx = sx - tw - 16;
      if (ty + th > H - 8) ty = sy - th - 16;
      tip.style.left = Math.max(8, tx) + "px"; tip.style.top = Math.max(8, ty) + "px";
      cv.style.cursor = "pointer";
    } else { tip.hidden = true; cv.style.cursor = (WW*s > W + 1) ? "grab" : "default"; }
    if (reduceMotion && (prev?.b !== p?.b)) frame();
  });
  const up = e => {
    const d = down; down = null; cv.style.cursor = "";
    if (!d || d.drag) return;
    const r = cv.getBoundingClientRect(), p = pick(e.clientX - r.left, e.clientY - r.top);
    if (p?.b) openCategory(p.b.id);
    else if (p?.v){ const pool = ALL.filter(x => x.k); const r2 = pool[(Math.random()*pool.length)|0]; if (r2){ toast("A villager recommends " + r2.name); openDrawer(r2); } }
  };
  cv.addEventListener("pointerup", up);
  cv.addEventListener("pointercancel", () => { down = null; });
  cv.addEventListener("pointerleave", () => { if (!down){ hover = null; tip.hidden = true; } });

  $("timeBtn").addEventListener("click", () => {
    const order = ["live", "day", "golden", "night"];
    timeMode = order[(order.indexOf(timeMode) + 1) % order.length];
    L = light(); renderClock(); kick(); if (reduceMotion) frame();
  });
  function renderClock(){
    const lbl = { live:"Live time", day:"Midday", golden:"Golden hour", night:"Night" }[timeMode];
    const hh = Math.floor(L.hour), mm = Math.round((L.hour - hh)*60) % 60;
    $("timeBtn").innerHTML = `<span class="sun" style="background:${L.dark > .6 ? "#cdd6ff" : L.dark > .2 ? "#ff9f5a" : "#ffd75e"}"></span>${lbl}${timeMode === "live" ? ` · ${String(hh).padStart(2, "0")}:${String(mm).padStart(2, "0")}` : ""}`;
  }

  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) kick(); }).observe(cv);
  document.addEventListener("visibilitychange", () => { visible = !document.hidden; if (visible) kick(); });
  let rt; new ResizeObserver(() => { clearTimeout(rt); rt = setTimeout(() => { size(); if (built) frame(); }, 60); }).observe(cv);
  setInterval(() => { L = light(); renderClock(); }, 60000);

  function focusOn(id){
    const b = buildings.find(x => x.id === id); if (!b) return;
    const mx = Math.max(0, WW*s - W);
    if (mx > 0) tpanX = Math.max(0, Math.min(mx, ((b.box.x0 + b.box.x1)/2)*s - W/2));
    if (reduceMotion && tpanX != null){ panX = tpanX; tpanX = null; clampPan(); }
  }

  return {
    build(){
      if (!built) buildStatic(); size(); L = light(); renderClock(); frame(); kick(); renderHud();
      $("jump").innerHTML = DEF.map(d => `<button type="button" data-b="${d.id}" style="--h:${rgb(d.id)}"><i></i>${esc(d.name)}</button>`).join("");
      $("jump").addEventListener("click", e => { const b = e.target.closest("[data-b]"); if (!b) return; focusOn(b.dataset.b); kick(); setTimeout(() => openCategory(b.dataset.b), reduceMotion ? 0 : 450); });
    },
    rebuild(){ renderHud(); kick(); },
    update(res){
      const m = {};
      for (const r of res) for (const c of r.cats) m[c] = (m[c]||0) + 1;
      for (const b of buildings) b.match = m[b.id] || 0;
      if (S.cat) focusOn(S.cat);
      renderHud(); kick(); if (reduceMotion) frame();
    },
    name: id => NAME[id] || CAT[id]?.name || id,
    snapshot(id, scale = 3){
      const b = buildings.find(x => x.id === id); if (!b) return null;
      const pad = 4, x0 = Math.max(0, b.box.x0 - pad), y0 = Math.max(0, b.box.y0 - pad), w = Math.min(WW, b.box.x1 + pad) - x0, h = Math.min(WH, b.box.y1 + pad) - y0;
      const c = document.createElement("canvas"); c.width = w*scale; c.height = h*scale; c.className = "snap";
      const cx = c.getContext("2d"); cx.imageSmoothingEnabled = false; cx.drawImage(sc, x0, y0, w, h, 0, 0, w*scale, h*scale);
      return c;
    }
  };
  function renderHud(){
    const lit = buildings.filter(b => b.match).length;
    const filtering = S.q || S.view !== "all" || S.fresh || S.lib;
    $("hudStats").textContent = filtering ? `${lit} of ${buildings.length} buildings have matches` : `${buildings.length} buildings · ${ALL.length.toLocaleString()} repos`;
    $("focusWrap").innerHTML = S.cat ? `<span class="focus-chip"><span style="width:8px;height:8px;background:${rgb(S.cat)}"></span>${esc(NAME[S.cat] || CAT[S.cat].name)}<button type="button" id="zoomOut">Leave</button></span>` : "";
    $("hint").textContent = small ? "Drag sideways to look around" : "Click a building to go inside · click a villager for a tip";
  }
})();

/* ---------- inside a building ---------- */
function openCategory(id){
  const c = CAT[id]; if (!c) return;
  if (!lastFocus) lastFocus = document.activeElement;
  current = null; currentCat = id;
  const list = ALL.filter(r => r.cats.includes(id));
  const picks = list.filter(r => r.k).sort((a, b) => (b.s||0) - (a.s||0));
  const top = list.filter(r => !r.k).sort((a, b) => (b.s||0) - (a.s||0)).slice(0, 30);
  const fresh = list.filter(r => r.p && Date.parse(r.p) > NOW - 14*864e5).length;
  const row = x => `<button type="button" data-rel="${esc(x.nameL)}">${tile(x)}<span class="t"><b>${esc(x.n)}</b><span>${esc(x.d || "")}</span></span><span class="s num">★ ${fmtStars(x.s)}</span></button>`;
  $("dCrumb").textContent = "Village · " + net.name(id);
  $("dBody").innerHTML = `
    <div class="b-hero"><div class="b-pic" id="bPic"></div><div style="min-width:0"><span class="b-cat" style="--h:${rgb(id)}"><i></i>${esc(c.name)}</span><h2 id="dTitle" class="pix">${esc(net.name(id))}</h2><p>${esc(c.desc)}</p></div></div>
    <div class="stats num"><div><small>Repos</small><b>${list.length}</b></div><div><small>Start here</small><b>${picks.length}</b></div><div><small>Active 14d</small><b>${fresh}</b></div><div><small>Top stars</small><b>${fmtStars(list.reduce((m, r) => Math.max(m, r.s||0), 0))}</b></div></div>
    <div class="d-actions"><button class="btn pri" type="button" data-allcat="${id}">Show all ${list.length} in the list</button></div>
    ${picks.length ? `<div class="d-sec"><h4>Start here</h4><div class="rel">${picks.map(row).join("")}</div></div>` : ""}
    <div class="d-sec"><h4>Most starred</h4><div class="rel">${top.map(row).join("")}</div></div>
  `;
  const pic = net.snapshot(id, 4); if (pic) $("bPic").appendChild(pic);
  $("drawer").hidden = false; $("scrim").hidden = false;
  $("dBody").scrollTop = 0;
  $("dClose").focus();
}
