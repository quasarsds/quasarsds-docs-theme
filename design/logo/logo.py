import math, sys
C=(256,256)
def f(v): return f"{v:.1f}".rstrip('0').rstrip('.')
def pt(cx,cy,r,deg):
    a=math.radians(deg); return (cx+r*math.cos(a), cy+r*math.sin(a))
def arc_band(cx,cy,r_out,r_in,a0,a1):
    # banda anular de a0 a a1 (grados, sentido horario SVG)
    large=1 if (a1-a0)%360>180 else 0
    p0=pt(cx,cy,r_out,a0); p1=pt(cx,cy,r_out,a1); q1=pt(cx,cy,r_in,a1); q0=pt(cx,cy,r_in,a0)
    return (f"M{f(p0[0])} {f(p0[1])}A{r_out} {r_out} 0 {large} 1 {f(p1[0])} {f(p1[1])}"
            f"L{f(q1[0])} {f(q1[1])}A{r_in} {r_in} 0 {large} 0 {f(q0[0])} {f(q0[1])}Z")
def hexagon(cx,cy,r,rot=-90):
    pts=[pt(cx,cy,r,rot+60*i) for i in range(6)]
    return "M"+"L".join(f"{f(x)} {f(y)}" for x,y in pts)+"Z"
def swoosh(cx,cy,rx,ry,rot,t0,t1,wmax,n=80):
    # banda elíptica afilada en ambos extremos
    cr,sr=math.cos(math.radians(rot)),math.sin(math.radians(rot))
    def E(t,k):
        x=(rx+k)*math.cos(t); y=(ry+k)*math.sin(t)
        return (cx+x*cr-y*sr, cy+x*sr+y*cr)
    outer=[];inner=[]
    for i in range(n+1):
        u=i/n; t=t0+(t1-t0)*u
        w=wmax*math.sin(math.pi*u)**0.7*(1-0.5*u)  # más grueso a la izquierda, se afila hacia la punta
        outer.append(E(t,w/2)); inner.append(E(t,-w/2))
    pts=outer+inner[::-1]
    return "M"+"L".join(f"{f(x)} {f(y)}" for x,y in pts)+"Z"

R_OUT,R_IN=200,150
ring=arc_band(256,256,R_OUT,R_IN,-28,252)         # cuerpo azul de la Q
silver=arc_band(256,256,R_OUT,R_IN,258,300)       # pieza plateada superior
tail="M316 322L366 300L478 470L420 452Z"          # pata de la Q
# panal central (7 hexágonos)
s=30; d=s*math.sqrt(3)
cells=[(0,0)]+[(d*math.cos(math.radians(30+60*i)), d*math.sin(math.radians(30+60*i))) for i in range(6)]
fills=['url(#hexA)','url(#hexB)','url(#hexA)','url(#hexC)','url(#hexB)','url(#hexC)','url(#hexA)']
cx0,cy0=252,240
hexes="".join(f'<path d="{hexagon(cx0+x,cy0+y,s*0.86)}" fill="{fills[i]}"/>' for i,(x,y) in enumerate(cells))
sw=swoosh(262,250,250,84,-32,math.radians(196),math.radians(6),34)
# hexágonos lanzados por la estela: a lo largo de la tangente en su punta
def ell(t,cx=262,cy=250,rx=250,ry=84,rot=-32):
    cr,sr=math.cos(math.radians(rot)),math.sin(math.radians(rot))
    x,y=rx*math.cos(t),ry*math.sin(t); return (cx+x*cr-y*sr, cy+x*sr+y*cr)
T1=math.radians(6)
tip=ell(T1); prev=ell(T1+0.02)
dx,dy=tip[0]-prev[0],tip[1]-prev[1]; n=math.hypot(dx,dy); dx,dy=dx/n,dy/n
nx,ny=-dy,dx  # normal
def along(dist,off): return (tip[0]+dx*dist+nx*off, tip[1]+dy*dist+ny*off)
h1=along(30,-6); h2=along(68,-26); h3=along(62,16); h4=along(40,-40)
pass
trail=(f'<path d="{hexagon(*h1,17)}" fill="url(#hexB)"/>'
       f'<path d="{hexagon(*h2,13)}" fill="url(#hexA)"/>'
       f'<path d="{hexagon(*h3,9)}" fill="url(#hexB)"/>'
       f'<path d="{hexagon(*h4,6)}" fill="url(#silver)"/>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="QuasarSDS">
  <defs>
    <linearGradient id="ring" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="#1450a8"/>
      <stop offset=".55" stop-color="#1f6fd1"/>
      <stop offset="1" stop-color="#22c3e6"/>
    </linearGradient>
    <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f4f8fb"/>
      <stop offset="1" stop-color="#8299ae"/>
    </linearGradient>
    <linearGradient id="tail" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#22c3e6"/>
      <stop offset="1" stop-color="#1f6fd1"/>
    </linearGradient>
    <linearGradient id="swoosh" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="#1f6fd1"/>
      <stop offset=".6" stop-color="#22c3e6"/>
      <stop offset="1" stop-color="#9eeefc"/>
    </linearGradient>
    <linearGradient id="hexA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fe3f7"/><stop offset="1" stop-color="#22c3e6"/></linearGradient>
    <linearGradient id="hexB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22c3e6"/><stop offset="1" stop-color="#1f6fd1"/></linearGradient>
    <linearGradient id="hexC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2b8af0"/><stop offset="1" stop-color="#1450a8"/></linearGradient>
  </defs>
  <path d="{ring}" fill="url(#ring)"/>
  <path d="{silver}" fill="url(#silver)"/>
  <path d="{tail}" fill="url(#tail)"/>
  {hexes}
  <path d="{sw}" fill="url(#swoosh)"/>
  {trail}
</svg>
'''
open(sys.argv[1],'w').write(svg)
