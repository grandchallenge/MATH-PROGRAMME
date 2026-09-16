"""Deterministic static compositor for BSD Wolfram-backed plates.

Mathematical constants and finite-field fixtures are independently checked by
tools/bsd_wolfram_semantic_master.wl. This script only composes the static
web-delivery SVGs; it does not create mathematical authority.
"""
from pathlib import Path
import math, json, hashlib
ROOT = Path(__file__).resolve().parents[1] if 'tools' in Path(__file__).parts else Path('/mnt/data')
OUT = ROOT / 'docs/assets/documentaries/bsd/wolfram'
OUT.mkdir(parents=True, exist_ok=True)
PAPER='#f3ead5'; NAVY='#081a2e'; GOLD='#c29a48'; PALE='#e8edf0'; GREEN='#e7ecd6'; RED='#f4ddd7'; GRID='#b7bec3'

def head(title):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1536" role="img"><rect width="1024" height="1536" fill="{PAPER}"/><g fill="{NAVY}" font-family="Georgia,Times New Roman,serif"><path d="M34 58H990M34 178H990" stroke="{GOLD}" stroke-width="2"/><text x="512" y="130" text-anchor="middle" font-size="45">{title}</text>'''
def foot(text):
 return f'''<path d="M34 1425H990M34 1505H990" stroke="{GOLD}" stroke-width="2"/><text x="512" y="1470" text-anchor="middle" font-size="17">{text}</text></g></svg>'''
def box(x,y,w,h,title,fs=24):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{NAVY}" stroke-width="1.5"/><path d="M{x} {y+70}H{x+w}" stroke="{NAVY}"/><text x="{x+20}" y="{y+46}" font-size="{fs}">{title}</text>'
def poly(points): return ' '.join(f'{x:.1f},{y:.1f}' for x,y in points)

def mappt(x,y,x0,y0,w,h,xmin,xmax,ymin,ymax):
 return x0+(x-xmin)/(xmax-xmin)*w, y0+h-(y-ymin)/(ymax-ymin)*h

# I
s=head('PLATE I · Rational point to rational triangle')
s+=box(35,215,570,815,'The elliptic curve   E5: y^2 = x^3 - 25x',22)
s+='<defs><clipPath id="plot1"><rect x="80" y="315" width="485" height="650"/></clipPath></defs>'
px,py,pw,ph=80,315,485,650
xmin,xmax,ymin,ymax=-8,15,-18,22
# axes
xzero,yzero=mappt(0,0,px,py,pw,ph,xmin,xmax,ymin,ymax)
s+=f'<path d="M{px} {yzero:.1f}H{px+pw}M{xzero:.1f} {py}V{py+ph}" stroke="{NAVY}" stroke-width="1.2"/>'
# curves components exact sample
comps=[]
for lo,hi in [(-5,0),(5,30)]:
 for sign in [1,-1]:
  pts=[]
  for i in range(81):
   x=lo+(hi-lo)*i/80
   r=x**3-25*x
   if r>=-1e-9:
    y=sign*math.sqrt(max(0,r)); pts.append(mappt(x,y,px,py,pw,ph,xmin,xmax,ymin,ymax))
  comps.append(pts)
for pts in comps: s+=f'<polyline points="{poly(pts)}" fill="none" stroke="{NAVY}" stroke-width="3" clip-path="url(#plot1)"/>'
P=mappt(25/4,75/8,px,py,pw,ph,xmin,xmax,ymin,ymax)
s+=f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="7" fill="{GOLD}" stroke="{NAVY}"/><text x="{P[0]+30:.1f}" y="{P[1]-20:.1f}" font-size="20">P = (25/4, 75/8)</text>'
for xv in [-5,0,5,10,15]:
 x,_=mappt(xv,0,px,py,pw,ph,xmin,xmax,ymin,ymax); s+=f'<text x="{x:.1f}" y="{yzero+28:.1f}" text-anchor="middle" font-size="14">{xv}</text>'
for yv in [-10,0,10,20]:
 _,y=mappt(0,yv,px,py,pw,ph,xmin,xmax,ymin,ymax); s+=f'<text x="{px-10}" y="{y+5:.1f}" text-anchor="end" font-size="14">{yv}</text>'
s+=box(620,215,369,815,'Exact rational right triangle',20)
# triangle geometry
A=(735,835); B=(885,835); C=(735,380)
s+=f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="{PALE}" stroke="{NAVY}" stroke-width="4"/><rect x="735" y="805" width="30" height="30" fill="none" stroke="{NAVY}"/><g fill="{GOLD}" stroke="{NAVY}"><circle cx="735" cy="835" r="7"/><circle cx="885" cy="835" r="7"/><circle cx="735" cy="380" r="7"/></g><text x="810" y="875" text-anchor="middle" font-size="28">3/2</text><text x="690" y="620" font-size="28">20/3</text><text x="815" y="590" font-size="28">41/6</text><text x="810" y="930" text-anchor="middle" font-size="28">area = 5</text>'
s+=box(35,1065,954,270,'Corresponding exact data',23)
s+='<text x="75" y="1190" font-size="28">E5: y^2 = x^3 - 25x</text><text x="75" y="1260" font-size="28">P = (25/4, 75/8)</text><path d="M465 1145V1305" stroke="'+GOLD+'"/><text x="520" y="1190" font-size="26">a = 3/2     b = 20/3     c = 41/6</text><text x="660" y="1260" font-size="26">ab/2 = 5</text>'
s+=foot('Exact arithmetic correspondence. The finite real plot does not determine rank and does not prove BSD.')
(OUT/'plate_01_rational_point_triangle.svg').write_text(s)

# II
s=head('PLATE II · The chord–tangent group law')
s+=box(35,215,570,1040,'The elliptic curve   E: y^2 = x^3 - x + 1',22)
px,py,pw,ph=80,330,485,800
xmin,xmax,ymin,ymax=-2.4,2.4,-3.2,3.4
xzero,yzero=mappt(0,0,px,py,pw,ph,xmin,xmax,ymin,ymax)
s+=f'<path d="M{px} {yzero:.1f}H{px+pw}M{xzero:.1f} {py}V{py+ph}" stroke="{NAVY}" stroke-width="1.2"/>'
for sign in [1,-1]:
 pts=[]; openp=False
 for i in range(181):
  x=xmin+(xmax-xmin)*i/180; r=x**3-x+1
  if r>=0: pts.append(mappt(x,sign*math.sqrt(r),px,py,pw,ph,xmin,xmax,ymin,ymax))
 if pts: s+=f'<polyline points="{poly(pts)}" fill="none" stroke="{NAVY}" stroke-width="3"/>'
# y=1 line
_,yy=mappt(0,1,px,py,pw,ph,xmin,xmax,ymin,ymax); s+=f'<path d="M{px} {yy:.1f}H{px+pw}" stroke="{GOLD}" stroke-width="2" stroke-dasharray="10 8"/>'
labels=[('R',-1,1,-95,-20),('P',0,1,15,-20),('Q',1,1,20,-20),('P + Q',-1,-1,-115,45)]
for lab,x,y,dx,dy in labels:
 X,Y=mappt(x,y,px,py,pw,ph,xmin,xmax,ymin,ymax); s+=f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="7" fill="{GOLD}" stroke="{NAVY}"/><text x="{X+dx:.1f}" y="{Y+dy:.1f}" font-size="19">{lab} = ({x}, {y})</text>'
X1,Y1=mappt(-1,1,px,py,pw,ph,xmin,xmax,ymin,ymax); X2,Y2=mappt(-1,-1,px,py,pw,ph,xmin,xmax,ymin,ymax); s+=f'<path d="M{X1:.1f} {Y1+8:.1f}V{Y2-12:.1f}" stroke="{GOLD}" stroke-width="2" marker-end="url(#a)"/>'
s+=box(620,215,369,1040,'Chord–tangent construction',20)
lines=[('E: y^2 = x^3 - x + 1',365),('P = (0, 1)',470),('Q = (1, 1)',545),('R = (-1, 1)',620),('Chord through P and Q',735),('meets E again at R = (-1, 1)',795),('Reflect across the x-axis',920),('P + Q = -R = (-1, -1)',1010)]
for t,y in lines: s+=f'<text x="650" y="{y}" font-size="24">{t}</text>'
s+=foot('Exact rational example of the geometric addition law. It is not a picture of the full Mordell–Weil group.')
# inject marker defs
s=s.replace('<rect width="1024"', '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="'+GOLD+'"/></marker></defs><rect width="1024"',1)
(OUT/'plate_02_group_law.svg').write_text(s)

# III
s=head('PLATE III · Counting at a good prime')
s+=box(35,215,625,610,'Finite-field point set for E5: y^2 = x^3 - 25x  (mod 13)',19)
# grid
x0,y0,w,h=85,330,525,430
for i in range(13):
 x=x0+i*w/12; y=y0+i*h/12; s+=f'<path d="M{x:.1f} {y0}V{y0+h} M{x0} {y:.1f}H{x0+w}" stroke="{GRID}" stroke-width="0.8"/><text x="{x:.1f}" y="{y0+h+25}" text-anchor="middle" font-size="13">{i}</text><text x="{x0-10}" y="{y0+h-i*h/12+5:.1f}" text-anchor="end" font-size="13">{i}</text>'
pts=[(0,0),(2,6),(2,7),(3,2),(3,11),(4,4),(4,9),(5,0),(6,1),(6,12),(7,5),(7,8),(8,0),(9,6),(9,7),(10,3),(10,10),(11,4),(11,9)]
for x,y in pts:
 X=x0+x*w/12; Y=y0+h-y*h/12; s+=f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="6" fill="{GOLD}" stroke="{NAVY}"/>'
s+='<text x="350" y="800" text-anchor="middle" font-size="18">x mod 13</text><text x="55" y="550" transform="rotate(-90 55 550)" text-anchor="middle" font-size="18">y mod 13</text>'
s+=box(675,215,314,610,'Facts at p = 13',22)
facts=[('E5: y^2 = x^3 - 25x',360),('Affine solutions = 19',455),('#E5(F_13) = 20',550),('a_13 = 13 + 1 - 20 = -6',645),('L_13(E,s) =',720),('(1 + 6*13^(-s) + 13^(1-2s))^(-1)',775)]
for t,y in facts: s+=f'<text x="705" y="{y}" font-size="21">{t}</text>'
s+=box(35,865,954,410,'Finite sample of a_p values at good primes',22)
pr=[3,7,11,13,17,19,23,29,31]; av=[0,0,0,-6,-2,0,0,-10,0]
base=1035; left=105; right=945; sx=(right-left)/(len(pr)-1); scale=18
s+=f'<path d="M{left} {base}H{right}" stroke="{NAVY}" stroke-width="1.5"/>'
for i,(p,v) in enumerate(zip(pr,av)):
 x=left+i*sx; s+=f'<text x="{x:.1f}" y="1215" text-anchor="middle" font-size="15">{p}</text>'
 if v<0:
  hh=-v*scale; s+=f'<rect x="{x-15:.1f}" y="{base}" width="30" height="{hh}" fill="{GOLD}" stroke="{NAVY}"/><text x="{x:.1f}" y="{base+hh+22}" text-anchor="middle" font-size="15">{v}</text>'
 else: s+=f'<circle cx="{x:.1f}" cy="{base}" r="5" fill="{GOLD}" stroke="{NAVY}"/><text x="{x:.1f}" y="{base-14}" text-anchor="middle" font-size="14">0</text>'
s+='<text x="65" y="1040" font-size="18">a_p</text><text x="525" y="1245" font-size="18">p</text>'
s+=foot('Each good prime contributes a local factor. No single prime, and no finite sample of primes, determines rank.')
(OUT/'plate_03_good_prime.svg').write_text(s)

# IV
s=head('PLATE IV · The strong BSD leading-term ledger')
s+=box(35,215,954,250,'The BSD leading-term formula',22)
s+='<text x="175" y="345" font-size="28">L^(r)(E,1)/r! =</text><text x="650" y="325" text-anchor="middle" font-size="24">Omega_E * Reg(E/Q) * #Sha(E/Q) * product_p c_p</text><path d="M380 345H920" stroke="'+NAVY+'" stroke-width="1.5"/><text x="650" y="390" text-anchor="middle" font-size="24">#E(Q)_tors^2</text>'
s+=box(35,505,954,570,'Dependency ledger',22)
xs=[75,305,535,765]; tops=[('Omega_E','Real period'),('Reg(E/Q)','Neron-Tate regulator'),('#Sha(E/Q)','Tate-Shafarevich group'),('product_p c_p','Local Tamagawa product')]
for x,(a,b) in zip(xs,tops):
 s+=f'<rect x="{x}" y="620" width="190" height="150" fill="none" stroke="{NAVY}"/><text x="{x+95}" y="680" text-anchor="middle" font-size="23">{a}</text><text x="{x+95}" y="730" text-anchor="middle" font-size="13">{b}</text><path d="M{x+95} 770L512 835" stroke="{NAVY}" stroke-width="1.7"/>'
s+=f'<rect x="380" y="825" width="264" height="105" fill="#f2dfaa" stroke="{NAVY}"/><text x="512" y="890" text-anchor="middle" font-size="30">L^(r)(E,1)/r!</text><path d="M512 930V960" stroke="{NAVY}"/><rect x="355" y="960" width="314" height="80" fill="none" stroke="{NAVY}"/><text x="512" y="1010" text-anchor="middle" font-size="26">#E(Q)_tors^2</text>'
s+=box(35,1115,954,230,'The BSD obligations',22)
obs=[('1.','Rank equality: rank E(Q) = ord_(s=1) L(E,s)',1205),('2.','Sha finiteness: #Sha(E/Q) must be finite',1260),('3.','Leading term: normalized coefficient = arithmetic factor ledger',1315)]
for n,t,y in obs: s+=f'<text x="80" y="{y}" font-size="21" fill="{GOLD}">{n}</text><text x="145" y="{y}" font-size="20">{t}</text>'
s+=foot('These are separate obligations. A theorem about one does not silently establish the others.')
(OUT/'plate_04_strong_bsd_ledger.svg').write_text(s)

# V
s=head('PLATE V · The exact BSD theorem frontier')
# table
x0=35; y0=230; widths=[430,290,234]; rh=125
headers=['Statement','Scope','Status']; x=x0
for w,t in zip(widths,headers): s+=f'<rect x="{x}" y="{y0}" width="{w}" height="90" fill="none" stroke="{NAVY}"/><text x="{x+w/2}" y="{y0+58}" text-anchor="middle" font-size="27">{t}</text>'; x+=w
rows=[('Mordell–Weil finite generation','all E/Q','ESTABLISHED',GREEN),('Modularity','all E/Q','ESTABLISHED',GREEN),('rank equality + finite Sha','analytic rank 0 or 1','ESTABLISHED',GREEN),('rank E(Q) = ord at s = 1','all E/Q','OPEN',RED),('Sha(E/Q) finite','all E/Q','OPEN',RED),('complete normalized leading term','all E/Q','OPEN',RED)]
for i,row in enumerate(rows):
 y=y0+90+i*rh; x=x0
 for j,(w,t) in enumerate(zip(widths,row[:3])):
  fill='none' if j<2 else row[3]; s+=f'<rect x="{x}" y="{y}" width="{w}" height="{rh}" fill="{fill}" stroke="{NAVY}"/>'
  color=NAVY if j<2 else ('#4f4b1d' if row[2]=='ESTABLISHED' else '#8b1e1e'); anchor='start' if j==0 else 'middle'; tx=x+20 if j==0 else x+w/2; fs=20 if j==0 else 21
  s+=f'<text x="{tx}" y="{y+72}" text-anchor="{anchor}" font-size="{fs}" fill="{color}">{t}</text>'; x+=w
s+='<rect x="35" y="1110" width="954" height="235" fill="none" stroke="'+NAVY+'"/><text x="512" y="1190" text-anchor="middle" font-size="30">Established low-rank terrain is not the universal conjecture.</text><path d="M70 1225H954" stroke="'+GOLD+'"/><text x="512" y="1280" text-anchor="middle" font-size="20">Finite computation, parity, Selmer bounds, family averages, p-adic formulas,</text><text x="512" y="1320" text-anchor="middle" font-size="20">and one-prime results do not remove the universal quantifier.</text>'
s+=foot('Scope is part of theorem status. Established special cases do not erase the universal quantifier.')
(OUT/'plate_05_theorem_frontier.svg').write_text(s)

for p in sorted(OUT.glob('*.svg')):
 b=p.read_bytes(); print(p.name,len(b),hashlib.sha256(b).hexdigest())
