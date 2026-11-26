#!/usr/bin/env python3
"""Deterministic, dependency-free exact and schematic SCC teaching plates."""
from pathlib import Path
from html import escape
from xml.etree import ElementTree as ET
from itertools import product
from math import comb

OUT = Path(__file__).resolve().parents[1] / "docs/assets/scc"
OUT.mkdir(parents=True, exist_ok=True)
PAPER="#faf7ee"; INK="#142941"; MUTED="#4d6072"; RULE="#c7c6b9"; TEAL="#276c70"; PALE="#d6e5df"; GOLD="#966a28"; WARM="#f1e4cc"; WHITE="#fffdf7"
def txt(x,y,s,size=20,fill=INK,anchor="start",weight="400",serif=False):
    return f'<text x="{x}" y="{y}" font-family="{ "Georgia, serif" if serif else "Arial, sans-serif"}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill=WHITE,stroke=RULE,rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def line(x,y,x2,y2,c=RULE,w=1,arrow=False,dash=False):
    return f'<path d="M{x} {y} L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="5 5"' if dash else '')+'/>'
def circle(x,y,r,fill=PALE,stroke=TEAL):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>'
def write(name,num,label,h,desc,parts):
    title=f"Plate {num} — {label}"
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {h}" role="img" aria-labelledby="title description"><title id="title">{escape(title)}</title><desc id="description">{escape(desc)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{TEAL}"/></marker></defs><rect width="760" height="{h}" fill="{PAPER}"/>'+txt(24,30,f"SCC  /  {num}     {label.upper()}",15,GOLD,weight="700")+line(24,44,736,44)+''.join(parts)+'</svg>\n'
    ET.fromstring(svg)
    (OUT/f"{name}.svg").write_text(svg,encoding="utf-8")
# I: literal coefficient matrices and exact costs, with sparse annotation.
p=[]
for x,title,sub,dense,cost in [(48,"Shared structure","All cross-pairings",True,1),(416,"Independent structure","Matched pairings only",False,8)]:
    p += [txt(x,82,title,27,serif=True),txt(x,108,sub,17,MUTED)]
    for i in range(8):
        p += [txt(x+45+i*29+13,140,f"y{i+1}",13,MUTED,"middle"),txt(x+30,164+i*29,f"x{i+1}",13,MUTED,"end")]
        for j in range(8):
            p += [rect(x+45+j*29,146+i*29,26,26,TEAL if dense or i==j else WHITE,TEAL if dense or i==j else RULE,2)]
    p += [txt(x+45,404,"64 nonzero entries" if dense else "8 nonzero entries",18,MUTED),txt(x+45,441,str(cost),36,INK,weight="700",serif=True),txt(x+83,439,"multiplication" if dense else "multiplications",19,INK)]
p += [line(380,65,380,449,RULE),line(24,459,736,459),txt(380,489,"Coefficient count grows; independent rank determines this cost.",19,INK,"middle",serif=True)]
write("01-compression","01","The cost of independent relations",510,"Two literal 8 by 8 coefficient matrices over F2. All 64 entries of the first are one; only 8 diagonal entries of the second are one. Their exact multiplicative complexities are one and eight.",p)
# II: exact 16 monomials grouped by factor choices; exact three-gate factorization.
p=[txt(32,77,"Four pairs, sixteen terms",26,serif=True),txt(32,101,"Choose one symbol from each pair.",17,MUTED)]
terms=[''.join(t) for t in product("ab","cd","ef","gh")]
for i,t in enumerate(terms):
    x=32+(i%4)*88;y=126+(i//4)*42
    p += [rect(x,y,76,32,WHITE,RULE,3),txt(x+38,y+22,t,18,INK,"middle",serif=True)]
p += [line(400,63,400,338),txt(420,77,"Three products",26,serif=True),txt(420,101,"Reuse the factors.",17,MUTED)]
for i,s in enumerate(["a+b","c+d","e+f","g+h"]):
    x=416+i*81;p += [rect(x,128,72,35,WHITE,RULE,3),txt(x+36,151,s,17,INK,"middle"),line(x+36,163,492+(i//2)*162,204,TEAL,1.6)]
for x in [492,654]:
    p += [circle(x,218,17),txt(x,224,"×",23,TEAL,"middle",weight="700"),line(x,235,573,265,TEAL,1.6)]
p += [circle(573,280,17),txt(573,286,"×",23,TEAL,"middle",weight="700"),line(573,298,573,322,TEAL,1.6,True),txt(573,345,"F",23,INK,"middle",serif=True),txt(32,323,"2⁴ terms",23,INK,serif=True),line(24,363,736,363),txt(380,393,"The expanded expression and the small circuit compute the same function.",18,INK,"middle",serif=True)]
write("02-factorization","02","Compression through composition",416,"All sixteen terms of (a+b)(c+d)(e+f)(g+h), and a binary multiplication tree using exactly three products.",p)
# III: literal degree histogram and promoted monomial list for four variables.
before=[comb(4,r) for r in range(5)]
R=[comb(2,r) if 0<=r<=2 else 0 for r in range(5)]
after=[before[r]+(R[r-1] if r>=1 else 0)-(R[r-2] if r>=2 else 0) for r in range(5)]
assert after==[1,5,7,3,0] and sum(before)==sum(after)==16
p=[txt(28,78,"Before: affine primitives",23,serif=True),txt(28,104,"After: one new primitive y = ab",19,TEAL,weight="700"),txt(45,142,"Degree",16,MUTED),txt(151,142,"Before",16,MUTED),txt(385,142,"After",16,TEAL)]
for r in range(5):
    y=158+r*45
    p += [txt(74,y+24,r,20,INK,"middle"),line(29,y+39,731,y+39,RULE)]
    for j in range(before[r]):p += [rect(153+j*27,y+3,22,27,WHITE,MUTED,2)]
    for j in range(after[r]):p += [rect(385+j*27,y+3,22,27,PALE,TEAL,2)]
    p += [txt(347,y+24,before[r],18,MUTED,"end"),txt(607,y+24,after[r],18,TEAL,"end")]
p += [txt(651,142,"Change",16,MUTED,"middle")]
for r in range(5):
    diff=after[r]-before[r];p += [txt(651,182+r*45,("+" if diff>0 else "")+str(diff),20,TEAL if diff>0 else INK,"middle")]
p += [line(24,388,736,388),txt(28,420,"The four promotions",23,serif=True)]
for i,(s,t) in enumerate([("ab","y"),("abc","yc"),("abd","yd"),("abcd","ycd")]):
    x=28+i*180;p += [txt(x,455,s,20,INK,serif=True),line(x+65,448,x+104,448,TEAL,2,True),txt(x+114,455,t,20,TEAL,serif=True)]
p += [txt(28,489,"Each named direction falls by exactly one degree; all share y.",19,MUTED)]
write("03-promotion","03","The graded promotion law",512,"Exact graded dimensions on four input bits before and after computing ab: before 1,4,6,4,1; after 1,5,7,3,0. The four directions ab, abc, abd, abcd drop one degree.",p)

# IV: exact four operand-value cells for g=ab, on n=4 inputs.
p=[txt(28,79,"Four possible joint values",27,serif=True),txt(28,104,"Each cell has four assignments of the remaining bits c,d.",18,MUTED)]
for i,(a,b) in enumerate(product(range(2),repeat=2)):
    x=30+i*179;fill=PALE if a*b else WHITE
    p += [rect(x,132,166,164,fill,TEAL if a*b else RULE,3),txt(x+83,160,f"a={a}    b={b}",20,INK,"middle",weight="700"),txt(x+83,184,f"g = {a*b}",18,TEAL if a*b else MUTED,"middle")]
    for j,(c,d) in enumerate(product(range(2),repeat=2)):
        dx=x+25+(j%2)*65;dy=199+(j//2)*40
        p += [rect(dx,dy,51,28,PAPER,RULE,3),txt(dx+25.5,dy+19,f"{a}{b}{c}{d}",15,INK,"middle")]
p += [line(24,317,736,317),txt(28,349,"Why the smallest cell controls the rank",22,serif=True),txt(28,378,"Complement either operand: the old degree-two symbol stays the same.",18,INK),txt(28,404,"Its rank is bounded by the support of each of the four indicators.",18,INK),txt(28,447,"Four cells  →  capacity at most 2ⁿ⁻²",25,TEAL,serif=True)]
write("04-cell-ceiling","04","A sharp one-gate ceiling",470,"Exact four-cell partition of the sixteen assignments of a,b,c,d. The indicator ab is one on four assignments. Complementing operands keeps the degree-two symbol unchanged, so the smallest cell bounds the graded rank.",p)
# V: literal equality of two evaluation paths and schematic successor construction.
p=[txt(28,78,"Two ways to compute the same product",26,serif=True),txt(28,104,"Work over the binary field. One old gate, one new gate.",18,MUTED)]
for x,s in [(172,"a"),(380,"b"),(588,"c")]:
    p += [circle(x,144,22,WHITE,MUTED),txt(x,152,s,25,INK,"middle",serif=True)]
for x,x1,x2,s,c in [(250,172,380,"y = ab",MUTED),(510,172,588,"t = ac",TEAL)]:
    p += [line(x1,166,x-45,207,c,1.6),line(x2,166,x+45,207,c,1.6),rect(x-67,207,134,45,PALE if x==510 else WHITE,c,4),txt(x,236,s,22,c,"middle",serif=True)]
p += [line(250,252,250,292,MUTED,2,True),line(510,252,510,292,TEAL,2,True),txt(250,321,"cy",30,INK,"middle",serif=True),txt(510,321,"bt",30,TEAL,"middle",serif=True),txt(380,321,"=",32,INK,"middle",serif=True),line(250,334,380,369,MUTED,1.8),line(510,334,380,369,TEAL,1.8),rect(296,369,168,51,WARM,GOLD,4),txt(380,401,"abc",27,INK,"middle",serif=True),txt(380,449,"A new symbol; an old dependency.",21,INK,"middle",serif=True)]
write("05-syzygy","05","The relation between relationships",475,"The exact Boolean products y=ab and t=ac obey cy=bt=abc. The geometry and edge placement are schematic, while the equations are literal.",p)
# VI: schematic algebra presentation with explicit relation text.
p=[txt(28,78,"A complete one-step presentation",26,serif=True),txt(28,104,"Three mathematical operations, not three computational gates.",18,MUTED)]
for i,(head,formula,caption) in enumerate([("I. Inherit","C = A/(q)","Forget the old grade-two symbol."),("II. Adjoin","C[t]/(t²)","Introduce its new grade-one symbol."),("III. Relate","ta = δ(a)","For each a in the residual module H.")]):
    y=132+i*97
    p += [rect(28,y,704,76,WHITE,RULE,3),txt(46,y+25,head,16,GOLD,weight="700"),txt(214,y+33,formula,27,INK,serif=True),txt(214,y+59,caption,17,MUTED)]
    if i<2:p += [line(380,y+76,380,y+94,TEAL,1.8,True)]
p += [line(24,427,736,427),txt(380,459,"A′ = C[t] / (t², ta + δ(a) : a ∈ H)",26,INK,"middle",serif=True),txt(380,486,"The inherited quotient alone does not determine the correction.",17,MUTED,"middle")]
write("06-quotient","06","Quotient, primitive, cross-relations",510,"Schematic dependency sequence for the exact presentation of the successor algebra: quotient A by q, adjoin the square-zero t, and impose ta=delta(a) for every residual relation a.",p)
# VII: literal 16 spectator monomials.
p=[txt(28,78,"One correction direction, many consequences",26,serif=True),txt(28,104,"Append four unused independent switches p,q,r,s.",18,MUTED)]
p += [rect(28,208,181,90,PALE,TEAL,4),txt(118.5,239,"One direction",16,TEAL,"middle",weight="700"),txt(118.5,274,"b → cy",29,INK,"middle",serif=True)]
vars_="pqrs"; monomials=[''.join(c for j,c in enumerate(vars_) if (m>>j)&1) or '1' for m in range(16)]
for i,m in enumerate(monomials):
    x=306+(i%4)*105;y=145+(i//4)*61
    p += [line(209,253,x,y+22,TEAL,0.9)]
for i,m in enumerate(monomials):
    x=306+(i%4)*105;y=145+(i//4)*61
    p += [rect(x,y,94,45,WHITE,TEAL,3),txt(x+47,y+28,m,20,INK,"middle",serif=True)]
p += [txt(518,407,"16 independent directions",21,TEAL,"middle",weight="700"),line(24,427,736,427),txt(380,456,"Still two gates in total: y = ab, then t = ac.",21,INK,"middle",serif=True)]
write("07-spectators","07","The spectator obstruction",479,"Four spectator coordinates yield sixteen square-free monomials, listed literally. Tensoring the one correction direction with these monomials amplifies its rank to sixteen without further multiplication gates.",p)
# VIII: literal assignment support, schematic split of cohomology without dimension claim.
p=[txt(28,78,"Complementary support regions",26,serif=True),txt(28,103,"Example: g = ac on three input bits.",18,MUTED)]
for i,g in enumerate([1,0]):
    x=28 if i==0 else 270;w=220 if i==0 else 462
    p += [rect(x,130,w,161,PALE if g else WHITE,TEAL if g else RULE,4),txt(x+20,160,f"g = {g}",23,TEAL if g else INK,weight="700")]
    vals=[f"{a}{b}{c}" for a,b,c in product(range(2),repeat=3) if a*c==g]
    for j,s in enumerate(vals):
        dx=x+20+(j%3)*77;dy=180+(j//3)*42
        p += [rect(dx,dy,66,32,PAPER,RULE,3),txt(dx+33,dy+22,s,17,INK,"middle")]
    p += [txt(x+20,272,f"{len(vals)} input assignments",17,MUTED)]
p += [line(138,291,138,325,TEAL,1.8,True),line(501,291,501,325,TEAL,1.8,True),txt(138,352,"im P",24,TEAL,"middle",serif=True),txt(501,352,"im (1+P)",24,INK,"middle",serif=True),txt(380,398,"L = im P  ⊕  im (1+P)",26,INK,"middle",serif=True),txt(380,425,"Cell sizes are literal; the cohomology dimensions are not depicted.",17,MUTED,"middle")]
write("08-projections","08","Complementary projections",450,"Exact assignment sets for ac=1 and ac=0 on three variables (two and six respectively). Arrows schematically indicate that the cohomology projections admit representatives supported in these sets; no equality of set size and dimension is claimed.",p)
