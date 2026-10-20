import math, sys
exec(open(__file__.replace('favicon.py','logo.py')).read().split("R_OUT,R_IN=200,150")[0])  # reutiliza helpers (pt, arc_band, hexagon, f)
ring=arc_band(256,256,236,150,-30,250)
silver=arc_band(256,256,236,150,258,304)
tail="M330 318L392 292L508 480L432 500Z"
core=hexagon(256,256,74)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="ring" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#1450a8"/><stop offset=".55" stop-color="#1f6fd1"/><stop offset="1" stop-color="#22c3e6"/></linearGradient>
    <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f8fb"/><stop offset="1" stop-color="#8299ae"/></linearGradient>
    <linearGradient id="cyan" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fe3f7"/><stop offset="1" stop-color="#22c3e6"/></linearGradient>
  </defs>
  <path d="{ring}" fill="url(#ring)"/>
  <path d="{silver}" fill="url(#silver)"/>
  <path d="{tail}" fill="url(#cyan)"/>
  <path d="{core}" fill="url(#cyan)"/>
</svg>
'''
open(sys.argv[1],'w').write(svg)
