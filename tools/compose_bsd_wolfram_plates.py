# Deterministic compositor for BSD exact-object editorial landscape plates.
# Mathematical fixtures are governed by tools/bsd_wolfram_semantic_master.wl.
from pathlib import Path
import hashlib, math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/assets/visual_pedagogy/bsd_exact"
OUT.mkdir(parents=True, exist_ok=True)

W,H=1536,1024
PAPER="#f3ead5"; NAVY="#081a2e"; GOLD="#c29a48"; PALE="#e8edf0"
GREEN="#e7ecd6"; RED="#f4ddd7"; GRID="#b7bec3"; MUTED="#6e6250"

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def head(title, subtitle=""):
    sub = f'<text x="768" y="132" text-anchor="middle" font-size="15" fill="{MUTED}">{esc(subtitle)}</text>' if subtitle else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<g fill="{NAVY}" font-family="Georgia,Times New Roman,serif">
<path d="M48 46H1488M48 142H1488" stroke="{GOLD}" stroke-width="2"/>
<text x="768" y="105" text-anchor="middle" font-size="42">{esc(title)}</text>{sub}'''

def foot(text):
    return f'''<path d="M48 946H1488M48 985H1488" stroke="{GOLD}" stroke-width="2"/>
<text x="768" y="972" text-anchor="middle" font-size="16">{esc(text)}</text>
</g></svg>'''

def box(x,y,w,h,title,fs=23,fill="none"):
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{fill}" stroke="{NAVY}" stroke-width="1.5"/>
<path d="M{x} {y+58}H{x+w}" stroke="{NAVY}" stroke-width="1"/>
<text x="{x+20}" y="{y+39}" font-size="{fs}">{esc(title)}</text>'''

def mappt(x,y,x0,y0,w,h,xmin,xmax,ymin,ymax):
    return x0+(x-xmin)/(xmax-xmin)*w, y0+h-(y-ymin)/(ymax-ymin)*h

def poly(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x,y in points)

def plate1():
    s=head("PLATE I · Rational point to rational triangle","Exact object correspondence · E5 and the congruent-number triangle")
    s+=box(55,180,865,610,"The elliptic curve   E5: y^2 = x^3 - 25x",25)
    px,py,pw,ph=105,265,770,440
    s+=f'<defs><clipPath id="plot1"><rect x="{px}" y="{py}" width="{pw}" height="{ph}"/></clipPath></defs>'
    xmin,xmax,ymin,ymax=-8,15,-18,22
    xzero,yzero=mappt(0,0,px,py,pw,ph,xmin,xmax,ymin,ymax)
    s+=f'<path d="M{px} {yzero:.1f}H{px+pw}M{xzero:.1f} {py}V{py+ph}" stroke="{NAVY}" stroke-width="1.2"/>'
    for lo,hi in [(-5,0),(5,30)]:
        for sign in [1,-1]:
            pts=[]
            for i in range(60):
                x=lo+(hi-lo)*i/59
                r=x**3-25*x
                if r>=-1e-9:
                    pts.append(mappt(x,sign*math.sqrt(max(0,r)),px,py,pw,ph,xmin,xmax,ymin,ymax))
            s+=f'<polyline points="{poly(pts)}" fill="none" stroke="{NAVY}" stroke-width="3" clip-path="url(#plot1)"/>'
    P=mappt(25/4,75/8,px,py,pw,ph,xmin,xmax,ymin,ymax)
    s+=f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="8" fill="{GOLD}" stroke="{NAVY}"/><text x="{P[0]+26:.1f}" y="{P[1]-18:.1f}" font-size="22">P = (25/4, 75/8)</text>'
    for xv in [-5,0,5,10,15]:
        x,_=mappt(xv,0,px,py,pw,ph,xmin,xmax,ymin,ymax)
        s+=f'<text x="{x:.1f}" y="{yzero+25:.1f}" text-anchor="middle" font-size="14">{xv}</text>'
    for yv in [-10,0,10,20]:
        _,y=mappt(0,yv,px,py,pw,ph,xmin,xmax,ymin,ymax)
        s+=f'<text x="{px-10}" y="{y+5:.1f}" text-anchor="end" font-size="14">{yv}</text>'
    s+=box(950,180,530,610,"Exact rational right triangle",24)
    A=(1070,680); B=(1360,680); C=(1070,315)
    s+=f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="{PALE}" stroke="{NAVY}" stroke-width="4"/><rect x="1070" y="650" width="30" height="30" fill="none" stroke="{NAVY}"/><g fill="{GOLD}" stroke="{NAVY}"><circle cx="1070" cy="680" r="7"/><circle cx="1360" cy="680" r="7"/><circle cx="1070" cy="315" r="7"/></g><text x="1215" y="720" text-anchor="middle" font-size="29">3/2</text><text x="1010" y="505" font-size="29">20/3</text><text x="1220" y="500" font-size="29">41/6</text><text x="1215" y="760" text-anchor="middle" font-size="28">area = 5</text>'
    s+=box(55,818,1425,100,"Corresponding exact data",21,fill="#f7f0df")
    s+='<text x="95" y="910" font-size="22">E5: y^2 = x^3 - 25x     ·     P = (25/4, 75/8)</text><path d="M780 885V920" stroke="'+GOLD+'"/><text x="825" y="910" font-size="21">a = 3/2     b = 20/3     c = 41/6     ·     ab/2 = 5</text>'
    s+=foot("Exact arithmetic correspondence. The finite real plot does not determine rank and does not prove BSD.")
    return s

def plate2():
    s=head("PLATE II · The chord–tangent group law","Exact rational addition on E: y^2 = x^3 - x + 1")
    s+=box(55,180,930,650,"The elliptic curve and the chord y = 1",25)
    px,py,pw,ph=105,270,830,470
    xmin,xmax,ymin,ymax=-2.4,2.4,-3.2,3.4
    xzero,yzero=mappt(0,0,px,py,pw,ph,xmin,xmax,ymin,ymax)
    s+=f'<path d="M{px} {yzero:.1f}H{px+pw}M{xzero:.1f} {py}V{py+ph}" stroke="{NAVY}" stroke-width="1.2"/>'
    for sign in [1,-1]:
        pts=[]
        for i in range(90):
            x=xmin+(xmax-xmin)*i/89
            r=x**3-x+1
            if r>=0: pts.append(mappt(x,sign*math.sqrt(r),px,py,pw,ph,xmin,xmax,ymin,ymax))
        s+=f'<polyline points="{poly(pts)}" fill="none" stroke="{NAVY}" stroke-width="3"/>'
    _,yy=mappt(0,1,px,py,pw,ph,xmin,xmax,ymin,ymax)
    s+=f'<path d="M{px} {yy:.1f}H{px+pw}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="12 9"/>'
    for lab,x,y,dx,dy in [('R',-1,1,-95,-18),('P',0,1,20,-18),('Q',1,1,20,-18),('P + Q',-1,-1,-125,42)]:
        X,Y=mappt(x,y,px,py,pw,ph,xmin,xmax,ymin,ymax)
        s+=f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="8" fill="{GOLD}" stroke="{NAVY}"/><text x="{X+dx:.1f}" y="{Y+dy:.1f}" font-size="21">{lab} = ({x}, {y})</text>'
    X1,Y1=mappt(-1,1,px,py,pw,ph,xmin,xmax,ymin,ymax); X2,Y2=mappt(-1,-1,px,py,pw,ph,xmin,xmax,ymin,ymax)
    s+=f'<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{GOLD}"/></marker></defs><path d="M{X1:.1f} {Y1+10:.1f}V{Y2-15:.1f}" stroke="{GOLD}" stroke-width="2.5" marker-end="url(#a)"/>'
    s+=box(1015,180,465,650,"Construction",24)
    for n,t,y in [('1','P=(0,1), Q=(1,1)',300),('2','Their chord is y=1',390),('3','Third intersection: R=(-1,1)',480),('4','Reflect R across the x-axis',570),('5','P + Q = -R = (-1,-1)',660)]:
        s+=f'<circle cx="1065" cy="{y-8}" r="18" fill="{PALE}" stroke="{NAVY}"/><text x="1065" y="{y-2}" text-anchor="middle" font-size="17">{n}</text><text x="1100" y="{y}" font-size="22">{esc(t)}</text>'
    s+=f'<rect x="55" y="845" width="1425" height="80" rx="2" fill="#f7f0df" stroke="{NAVY}" stroke-width="1.5"/><text x="80" y="878" font-size="20">Visual claim boundary</text><text x="80" y="910" font-size="18">The displayed rational points satisfy the exact group-law construction; the plate does not encode the full Mordell–Weil group.</text>'
    s+=foot("Exact rational example of geometric addition. The construction illustrates the operation, not the global group structure.")
    return s

def plate3():
    s=head("PLATE III · Counting at a good prime","Exact finite computation for E5 modulo 13")
    s+=box(55,180,835,585,"Finite-field point set for E5: y^2 = x^3 - 25x  (mod 13)",23)
    x0,y0,w,h=115,280,690,405
    gx=w/12; gy=h/12
    s+=f'<defs><pattern id="g13" width="{gx:.3f}" height="{gy:.3f}" patternUnits="userSpaceOnUse"><path d="M{gx:.3f} 0H0V{gy:.3f}" fill="none" stroke="{GRID}" stroke-width="0.8"/></pattern></defs><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#g13)" stroke="{GRID}"/>'
    for i in range(13):
        x=x0+i*w/12
        s+=f'<text x="{x:.1f}" y="{y0+h+24}" text-anchor="middle" font-size="13">{i}</text><text x="{x0-10}" y="{y0+h-i*h/12+5:.1f}" text-anchor="end" font-size="13">{i}</text>'
    pts=[(0,0),(2,6),(2,7),(3,2),(3,11),(4,4),(4,9),(5,0),(6,1),(6,12),(7,5),(7,8),(8,0),(9,6),(9,7),(10,3),(10,10),(11,4),(11,9)]
    for x,y in pts:
        X=x0+x*w/12; Y=y0+h-y*h/12
        s+=f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="6.5" fill="{GOLD}" stroke="{NAVY}"/>'
    s+=f'<text x="{x0+w/2}" y="742" text-anchor="middle" font-size="18">x mod 13</text><text x="78" y="{y0+h/2}" transform="rotate(-90 78 {y0+h/2})" text-anchor="middle" font-size="18">y mod 13</text>'
    s+=box(925,180,555,585,"Exact local data at p = 13",24)
    facts=[('Affine solutions','19'),('#E5(F_13)','20'),('a_13 = 13 + 1 - #E5(F_13)','-6'),('Local factor','(1 + 6·13^(-s) + 13^(1-2s))^(-1)')]
    yy=315
    for label,val in facts:
        s+=f'<text x="975" y="{yy}" font-size="18" fill="{MUTED}">{esc(label)}</text><text x="975" y="{yy+36}" font-size="25">{esc(val)}</text>'
        yy += 100 if label!="Local factor" else 135
    s+=box(55,795,1425,130,"Exact finite sample of a_p at selected good primes",21)
    pr=[3,7,11,13,17,19,23,29,31]; av=[0,0,0,-6,-2,0,0,-10,0]
    base=850; left=120; right=1410; sx=(right-left)/(len(pr)-1); scale=5.8
    s+=f'<path d="M{left} {base}H{right}" stroke="{NAVY}" stroke-width="1.5"/>'
    for i,(p,v) in enumerate(zip(pr,av)):
        x=left+i*sx
        if v<0:
            hh=-v*scale
            s+=f'<rect x="{x-18:.1f}" y="{base}" width="36" height="{hh}" fill="{GOLD}" stroke="{NAVY}"/><text x="{x:.1f}" y="{base+hh+19:.1f}" text-anchor="middle" font-size="14">{v}</text>'
        else:
            s+=f'<circle cx="{x:.1f}" cy="{base}" r="5" fill="{GOLD}" stroke="{NAVY}"/><text x="{x:.1f}" y="{base-12}" text-anchor="middle" font-size="13">0</text>'
        s+=f'<text x="{x:.1f}" y="915" text-anchor="middle" font-size="13">{p}</text>'
    s+=foot("Each good prime contributes a local Euler factor. No single prime, and no finite sample, determines rank.")
    return s

def plate4():
    s=head("PLATE IV · The strong BSD leading-term ledger","Quantified dependency structure · three logically distinct obligations")
    s+=box(55,180,1425,175,"The leading-term identity",24,fill="#f7f0df")
    s+='<text x="180" y="285" font-size="31">L^(r)(E,1)/r!  =</text><text x="890" y="260" text-anchor="middle" font-size="25">Omega_E · Reg(E/Q) · #Sha(E/Q) · product_p c_p</text><path d="M500 282H1320" stroke="'+NAVY+'" stroke-width="1.5"/><text x="910" y="322" text-anchor="middle" font-size="25">#E(Q)_tors^2</text>'
    s+=box(55,390,1425,285,"Arithmetic factor ledger",24)
    cards=[('Omega_E','archimedean period'),('Reg(E/Q)','Mordell–Weil lattice'),('#Sha(E/Q)','local-global obstruction'),('product_p c_p','bad-prime components'),('#E(Q)_tors^2','torsion denominator')]
    x=85
    for a,b in cards:
        s+=f'<rect x="{x}" y="485" width="252" height="125" fill="{PALE}" stroke="{NAVY}"/><text x="{x+126}" y="535" text-anchor="middle" font-size="24">{esc(a)}</text><text x="{x+126}" y="575" text-anchor="middle" font-size="15" fill="{MUTED}">{esc(b)}</text>'
        x+=277
    s+=box(55,710,1425,215,"Three obligations, not one slogan",24)
    y=790
    for n,a,b in [('1','Rank equality','rank E(Q) = ord_(s=1) L(E,s)'),('2','Sha finiteness','#Sha(E/Q) is finite'),('3','Leading term','normalized coefficient equals the arithmetic ledger')]:
        s+=f'<circle cx="95" cy="{y-8}" r="18" fill="{GOLD}"/><text x="95" y="{y-2}" text-anchor="middle" font-size="16" fill="{NAVY}">{n}</text><text x="130" y="{y}" font-size="22">{esc(a)}</text><text x="380" y="{y}" font-size="20" fill="{MUTED}">{esc(b)}</text>'
        y+=55
    s+=foot("Rank equality, Sha finiteness, and the normalized leading-term identity are separate obligations.")
    return s

def plate5():
    s=head("PLATE V · The exact BSD theorem frontier","Scope is part of theorem status")
    s+=box(55,180,1425,650,"Established terrain and universal open frontier",24)
    x0,y0=85,275; widths=[680,380,300]; header_h=70; rh=82
    x=x0
    for w,t in zip(widths,['Statement','Scope','Status']):
        s+=f'<rect x="{x}" y="{y0}" width="{w}" height="{header_h}" fill="{PALE}" stroke="{NAVY}"/><text x="{x+w/2}" y="{y0+45}" text-anchor="middle" font-size="24">{t}</text>'
        x+=w
    rows=[('Mordell–Weil finite generation','all E/Q','ESTABLISHED',GREEN),('Modularity','all E/Q','ESTABLISHED',GREEN),('rank equality + finite Sha','analytic rank 0 or 1','ESTABLISHED',GREEN),('rank E(Q) = ord at s = 1','all E/Q','OPEN',RED),('Sha(E/Q) finite','all E/Q','OPEN',RED),('complete normalized leading term','all E/Q','OPEN',RED)]
    for i,row in enumerate(rows):
        y=y0+header_h+i*rh; x=x0
        for j,(w,t) in enumerate(zip(widths,row[:3])):
            fill='none' if j<2 else row[3]
            tx=x+20 if j==0 else x+w/2
            anchor='start' if j==0 else 'middle'
            col=NAVY if j<2 else ('#4f4b1d' if row[2]=='ESTABLISHED' else '#8b1e1e')
            s+=f'<rect x="{x}" y="{y}" width="{w}" height="{rh}" fill="{fill}" stroke="{NAVY}"/><text x="{tx}" y="{y+51}" text-anchor="{anchor}" font-size="21" fill="{col}">{esc(t)}</text>'
            x+=w
    s+=f'<rect x="55" y="845" width="1425" height="80" rx="2" fill="#f7f0df" stroke="{NAVY}" stroke-width="1.5"/><text x="80" y="878" font-size="20">Quantifier guardrail</text><text x="80" y="910" font-size="18">Finite computation, parity, Selmer bounds, family averages, p-adic formulas, and one-prime results do not remove the universal quantifier.</text>'
    s+=foot("Established special cases do not erase the universal conjecture.")
    return s

PLATES={
    "plate_01_rational_point_triangle.svg":plate1,
    "plate_02_group_law.svg":plate2,
    "plate_03_good_prime.svg":plate3,
    "plate_04_strong_bsd_ledger.svg":plate4,
    "plate_05_theorem_frontier.svg":plate5,
}
for name,fn in PLATES.items():
    path=OUT/name
    path.write_text(fn(), encoding="utf-8")
    data=path.read_bytes()
    print(name, len(data), hashlib.sha256(data).hexdigest())
