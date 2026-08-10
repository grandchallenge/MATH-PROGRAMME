from __future__ import annotations
from pathlib import Path
import hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/documentaries'
OUT.mkdir(parents=True, exist_ok=True)
W,H=1055,1491

PALETTE={
 'night':'#06152b','night2':'#102d4c','gold':'#c99b3c','gold2':'#f0cf73',
 'paper':'#f7efd9','paper2':'#dfcda8','ink':'#173b60','blue':'#2e719e',
 'blue2':'#79a6c8','red':'#b43b2e','green':'#46785b','muted':'#6e7781','white':'#fffaf0'
}

def esc(s:str)->str:
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def text(x,y,s,size=28,weight=400,anchor='start',fill=None,italic=False):
    fill=fill or PALETTE['ink']
    style='font-style:italic;' if italic else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-family="Georgia, Times New Roman, serif" font-size="{size}" font-weight="{weight}" style="{style}">{esc(s)}</text>'

def line(x1,y1,x2,y2,stroke=None,width=3,dash=None,opacity=1):
    stroke=stroke or PALETTE['ink']; d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{d}/>'

def rect(x,y,w,h,fill='none',stroke=None,width=2,rx=0,opacity=1):
    ss=f' stroke="{stroke}" stroke-width="{width}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" opacity="{opacity}"{ss}/>'

def circle(cx,cy,r,fill='none',stroke=None,width=2,opacity=1):
    ss=f' stroke="{stroke}" stroke-width="{width}"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{opacity}"{ss}/>'

def ellipse(cx,cy,rx,ry,fill='none',stroke=None,width=2,dash=None,opacity=1):
    ss=f' stroke="{stroke}" stroke-width="{width}"' if stroke else ''
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{opacity}"{ss}{dd}/>'

def path(d,fill='none',stroke=None,width=3,dash=None,opacity=1):
    stroke=stroke or PALETTE['ink']; dd=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"{dd}/>'

def arrow(x1,y1,x2,y2,stroke=None,width=3,label=None,label_dy=-12):
    stroke=stroke or PALETTE['red']
    ang=math.atan2(y2-y1,x2-x1); al=14
    a1=ang+2.6; a2=ang-2.6
    pts=f'{x2},{y2} {x2+al*math.cos(a1):.1f},{y2+al*math.sin(a1):.1f} {x2+al*math.cos(a2):.1f},{y2+al*math.sin(a2):.1f}'
    parts=[line(x1,y1,x2,y2,stroke,width), f'<polygon points="{pts}" fill="{stroke}"/>']
    if label: parts.append(text((x1+x2)/2,(y1+y2)/2+label_dy,label,22,600,'middle',stroke))
    return ''.join(parts)

def base(title, subtitle, desc):
    return [
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
      f'<title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>',
      '<defs><linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06152b"/><stop offset="1" stop-color="#102d4c"/></linearGradient><linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7efd9"/><stop offset="1" stop-color="#dfcda8"/></linearGradient><filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#000" flood-opacity=".32"/></filter></defs>',
      '<rect width="1055" height="1491" fill="url(#night)"/>', rect(26,26,1003,1439,'none',PALETTE['gold'],4,8), rect(42,42,971,1407,'none',PALETTE['gold2'],1,0),
      line(45,120,1010,120,PALETTE['gold'],2), line(45,1370,1010,1370,PALETTE['gold'],2),
      rect(78,140,899,1175,'url(#paper)',PALETTE['gold'],4,18),
      text(112,200,title,38,700), text(112,244,subtitle,22,400,fill=PALETTE['muted'],italic=True)
    ]

def finish(parts, footer='Pedagogical reconstruction · visual_is_evidence = false'):
    parts += [line(112,1252,943,1252,PALETTE['gold'],2), text(527,1292,footer,19,600,'middle',PALETTE['muted']), '</svg>']
    return ''.join(parts)

def write(rel, content):
    p=ROOT/rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding='utf-8', newline='\n')
    return hashlib.sha256(content.encode()).hexdigest()

# 1 Ricci flow
p=base('Plate II — Metric evolution under Ricci flow','Time-indexed geometry; qualitative curvature is encoded separately.','Three staged schematic surfaces under Ricci flow show metric evolution, smoothing, and qualitative curvature concentration without claiming a computed solution or singularity.')
p += [text(112,300,'ORIENTATION',18,700,fill=PALETTE['gold']), text(112,332,'∂g/∂t = −2 Ric(g)',31,700), text(943,332,'schematic — not a numerical flow',18,600,'end',PALETTE['red'])]
for i,(x,tlabel) in enumerate([(120,'t₀'),(390,'t₁'),(660,'t₂')]):
    p += [rect(x,380,235,505,'#fffaf0',PALETTE['gold'],2,14), text(x+22,422,tlabel,26,700), text(x+118,458,['initial metric','evolving metric','localized concentration'][i],18,400,'middle',PALETTE['muted'])]
    if i==0: d=f'M{x+28} 620 C{x+65} 520 {x+130} 540 {x+150} 585 C{x+175} 630 {x+190} 690 {x+205} 705 C{x+170} 755 {x+80} 760 {x+35} 700 Z'
    elif i==1: d=f'M{x+28} 620 C{x+70} 565 {x+130} 565 {x+157} 600 C{x+177} 627 {x+192} 675 {x+205} 700 C{x+170} 730 {x+80} 735 {x+35} 700 Z'
    else: d=f'M{x+28} 625 C{x+78} 585 {x+124} 585 {x+160} 615 C{x+178} 630 {x+188} 650 {x+205} 655 C{x+196} 676 {x+176} 690 {x+155} 703 C{x+110} 732 {x+60} 722 {x+35} 690 Z'
    p += [path(d,PALETTE['blue2'],PALETTE['ink'],4)]
    for yy in (620,660,700): p += [path(f'M{x+42} {yy} C{x+95} {yy-25+i*8} {x+152} {yy+20-i*5} {x+195} {yy-5}', 'none', PALETTE['white'],2,opacity=.85)]
    for xx in (x+70,x+115,x+160): p += [path(f'M{xx} 580 C{xx-20+i*5} 630 {xx+15} 680 {xx} 720','none',PALETTE['white'],2,opacity=.75)]
    p += [text(x+22,810,'qualitative |Rm|',17,600), rect(x+22,827,190,16,'#e7dfcf',None,0,8)]
    widths=[65,95,155]; p += [rect(x+22,827,widths[i],16,PALETTE['red'],None,0,8,opacity=.65)]
    if i==2: p += [circle(x+175,650,38,'none',PALETTE['red'],4), text(x+175,768,'region of interest',16,600,'middle',PALETTE['red'])]
p += [arrow(355,635,382,635,PALETTE['red'],3),arrow(625,635,652,635,PALETTE['red'],3)]
p += [rect(120,925,775,245,'#f3ead6',PALETTE['gold'],2,12), text(145,965,'RELATION / INVARIANT',18,700,fill=PALETTE['gold']), text(145,1005,'Geometry changes through g(t); curvature is a derived field.',23,600), text(145,1045,'Smoothing and concentration are distinct observable features.',22,400), text(145,1100,'BOUNDARY',18,700,fill=PALETTE['red']), text(145,1135,'No panel is a computed Ricci-flow solution or singularity certificate.',21,600,fill=PALETTE['red'])]
ricci=finish(p)
sha_ricci=write('docs/assets/documentaries/poincare/plate_geometry_successor.svg',ricci)

# 2 Surgery
p=base('Plate III — Controlled neck surgery','A three-stage S² × I reconstruction with explicit cutting spheres and caps.','A schematic three-dimensional neck is identified, cut along two sphere cross-sections, excised, and replaced by standard-cap models; topology bookkeeping and theorem boundaries are explicit.')
p += [text(112,300,'ORIENTATION',18,700,fill=PALETTE['gold']), text(112,334,'local model: S² × I',30,700), text(943,334,'theorem-bound schematic',18,600,'end',PALETTE['red'])]
for i,(x,lab) in enumerate([(115,'1 · identify neck'),(390,'2 · cut / remove'),(665,'3 · attach caps')]):
    p += [rect(x,390,245,520,'#fffaf0',PALETTE['gold'],2,14), text(x+122,430,lab,19,700,'middle')]
    cx=x+122
    if i<2:
        p += [path(f'M{x+35} 570 C{x+70} 545 {cx-25} 550 {cx} 565 C{cx+25} 550 {x+175} 545 {x+210} 570 L{x+210} 715 C{x+175} 740 {cx+25} 735 {cx} 720 C{cx-25} 735 {x+70} 740 {x+35} 715 Z',PALETTE['blue2'],PALETTE['ink'],4)]
        p += [ellipse(x+35,642,18,73,'none',PALETTE['ink'],3), ellipse(x+210,642,18,73,'none',PALETTE['ink'],3)]
        if i==1:
            p += [ellipse(cx-38,642,18,65,'none',PALETTE['red'],5,'10 7'),ellipse(cx+38,642,18,65,'none',PALETTE['red'],5,'10 7'), text(cx-38,750,'S²₋',18,700,'middle',PALETTE['red']),text(cx+38,750,'S²₊',18,700,'middle',PALETTE['red'])]
            p += [rect(cx-30,565,60,155,'#f7efd9',None,0,0,.82), text(cx,805,'excised neck',17,600,'middle',PALETTE['red'])]
        else:
            p += [ellipse(cx,642,14,60,'none',PALETTE['gold'],4,'8 6'), text(cx,790,'high-curvature neck',17,600,'middle',PALETTE['red'])]
    else:
        p += [path(f'M{x+35} 585 C{x+75} 555 {x+115} 565 {x+125} 610 C{x+138} 660 {x+115} 705 {x+70} 720 C{x+50} 710 {x+35} 690 {x+35} 665 Z',PALETTE['blue2'],PALETTE['ink'],4), path(f'M{x+210} 585 C{x+170} 555 {x+130} 565 {x+120} 610 C{x+107} 660 {x+130} 705 {x+175} 720 C{x+195} 710 {x+210} 690 {x+210} 665 Z',PALETTE['blue2'],PALETTE['ink'],4)]
        p += [path(f'M{x+115} 582 Q{x+140} 642 {x+115} 702','none',PALETTE['green'],5),path(f'M{x+130} 582 Q{x+105} 642 {x+130} 702','none',PALETTE['green'],5),text(cx,790,'standard-cap models',17,600,'middle',PALETTE['green'])]
p += [arrow(360,645,382,645),arrow(635,645,657,645)]
p += [rect(115,945,795,225,'#f3ead6',PALETTE['gold'],2,12), text(140,983,'TOPOLOGY BOOKKEEPING',18,700,fill=PALETTE['gold']), text(140,1020,'Cutting changes topology; the event must be recorded and later reversed.',21,600), text(140,1060,'Canonical-neighbourhood and surgery-scale claims are imported theorems.',20,400), text(140,1115,'BOUNDARY',18,700,fill=PALETTE['red']), text(140,1150,'The plate does not certify a valid surgery event.',21,700,fill=PALETTE['red'])]
surgery=finish(p)
sha_surgery=write('docs/assets/documentaries/poincare/plate_surgery_successor.svg',surgery)
sha_surgery_print=write('docs/assets/documentaries/poincare/plate_surgery_successor_print.svg',surgery)

# 3 Riemann
p=base('Plate II — The critical strip','Exact symbolic frame; no decorative nontrivial-zero coordinates.','An exact schematic complex-plane frame labels the critical strip, critical line, pole at one, negative-even trivial zeros, and zero symmetries while intentionally omitting numerical nontrivial-zero dots.')
p += [text(112,300,'ORIENTATION',18,700,fill=PALETTE['gold']), text(112,334,'s = σ + it',30,700), text(943,334,'no finite zero dataset plotted',18,600,'end',PALETTE['red'])]
x0,y0=170,410; pw,ph=715,560
def X(sig): return x0+(sig+0.2)/1.4*pw
def Y(t): return y0+ph-(t+20)/40*ph
p += [rect(x0,y0,pw,ph,'#fffaf0',PALETTE['ink'],2,4)]
p += [rect(X(0),y0,X(1)-X(0),ph,'#dce8ef',None,0,0,.8)]
for sig,label_s,style in [(0,'Re(s)=0','5 5'),(.5,'Re(s)=1/2',None),(1,'Re(s)=1','5 5')]:
    p += [line(X(sig),y0,X(sig),y0+ph, PALETTE['red'] if sig==.5 else PALETTE['ink'], 4 if sig==.5 else 2, style)]
p += [line(x0,Y(0),x0+pw,Y(0),PALETTE['ink'],3), arrow(x0+pw-15,Y(0),x0+pw+4,Y(0),PALETTE['ink'],3), arrow(X(0),y0+15,X(0),y0-6,PALETTE['ink'],3)]
p += [text(x0+pw+12,Y(0)+7,'Re(s)',20,700), text(X(0)-10,y0-18,'Im(s)',20,700,'middle')]
for sig,lab in [(0,'0'),(.5,'1/2'),(1,'1')]: p += [text(X(sig),Y(0)+30,lab,18,600,'middle')]
for sig,lab in [(0,'Re(s)=0'),(.5,'critical line'),(1,'Re(s)=1')]: p += [text(X(sig),y0+ph+66,lab,17,600,'middle', PALETTE['red'] if sig==.5 else PALETTE['ink'])]
p += [circle(X(1),Y(0),9,PALETTE['red'],PALETTE['red'],2), text(X(1)+18,Y(0)-16,'pole s=1',18,700,fill=PALETTE['red'])]
p += [text(x0+18,y0+42,'functional symmetry: ρ ↦ 1−ρ',18,600), text(x0+18,y0+72,'conjugation: ρ ↦ ρ̄',18,600), arrow(X(.28),Y(11),X(.72),Y(11),PALETTE['green'],2,'mirror about 1/2',-10), arrow(X(.72),Y(-11),X(.28),Y(-11),PALETTE['green'],2)]
p += [rect(140,1030,775,150,'#fffaf0',PALETTE['gold'],2,10), text(165,1062,'TRIVIAL ZEROS — separate real-axis context',17,700,fill=PALETTE['gold']), line(210,1122,850,1122,PALETTE['ink'],2)]
for j,n in enumerate([-6,-4,-2]):
    xx=310+j*210; p += [circle(xx,1122,7,PALETTE['ink'],PALETTE['ink'],1), text(xx,1150,str(n),17,600,'middle')]
p += [text(527,1208,'Nontrivial zeros lie in 0 < Re(s) < 1; RH asserts Re(s)=1/2 for all of them.',19,600,'middle',PALETTE['red'])]
rh=finish(p,'Exact symbolic frame · no completeness or RH claim · visual_is_evidence = false')
sha_rh=write('docs/assets/documentaries/riemann/critical_strip_successor.svg',rh)

# 4 Navier-Stokes
p=base('Plate II — Vorticity stretching in three dimensions','Geometry of a vortex tube is separated from the global energy identity.','Three schematic vortex-tube stages show lengthening, thinning, and qualitative vorticity amplification linked to the stretching term, while a separate panel states the global energy identity.')
p += [text(112,300,'ORIENTATION',18,700,fill=PALETTE['gold']), text(112,334,'∂tω + (u·∇)ω = (ω·∇)u + νΔω',27,700), text(943,334,'schematic — not a simulation',18,600,'end',PALETTE['red'])]
for i,(x,lab,L,R) in enumerate([(110,'t₀',155,48),(385,'t₁',180,35),(660,'t₂',205,24)]):
    p += [rect(x,390,245,475,'#fffaf0',PALETTE['gold'],2,14), text(x+122,430,lab,24,700,'middle')]
    cy=615; left=x+122-L/2; right=x+122+L/2
    p += [path(f'M{left} {cy-R} C{x+122} {cy-R*1.25} {x+122} {cy-R*1.25} {right} {cy-R} L{right} {cy+R} C{x+122} {cy+R*1.25} {x+122} {cy+R*1.25} {left} {cy+R} Z', '#9ec2d7',PALETTE['ink'],4), ellipse(left,cy,16,R,'none',PALETTE['ink'],3),ellipse(right,cy,16,R,'none',PALETTE['ink'],3)]
    p += [arrow(left+18,cy,right-18,cy,PALETTE['red'],3,'ω / stretch direction',-18)]
    p += [text(x+122,760,['baseline tube','longer + thinner','amplified |ω|'][i],17,600,'middle',PALETTE['muted'])]
    p += [rect(x+35,790,175,12,'#e7dfcf',None,0,6),rect(x+35,790,[65,110,155][i],12,PALETTE['red'],None,0,6,.7)]
p += [arrow(355,615,377,615),arrow(630,615,652,615)]
p += [rect(110,910,795,270,'#f3ead6',PALETTE['gold'],2,12), text(140,950,'RELATION',18,700,fill=PALETTE['gold']), text(140,987,'The stretching term (ω·∇)u can amplify vorticity in 3D.',22,600), text(140,1038,'GLOBAL ENERGY — analytically separate',18,700,fill=PALETTE['green']), text(140,1075,'½‖u(t)‖²₂ + ν∫₀ᵗ ‖∇u(s)‖²₂ ds = ½‖u(0)‖²₂',21,600), text(140,1125,'BOUNDARY',18,700,fill=PALETTE['red']), text(140,1160,'No numerical cascade, blow-up mechanism, or regularity result is depicted.',19,700,fill=PALETTE['red'])]
ns=finish(p)
sha_ns=write('docs/assets/documentaries/navier_stokes/vorticity_stretching_successor.svg',ns)

# 5 BSD exact/data-derived
p=base('Plate I — The congruent number 5','Exact curve E₅, one verified rational point, and its area-five triangle.','A deterministic plot of y squared equals x cubed minus 25x marks the verified rational point 25/4,75/8 and displays the corresponding rational right triangle with sides 3/2, 20/3, and 41/6.')
p += [text(112,300,'ORIENTATION',18,700,fill=PALETTE['gold']), text(112,334,'E₅ : y² = x³ − 25x',30,700), text(943,334,'exact object + deterministic sampling',18,600,'end',PALETTE['green'])]
px,py,pw,ph=115,390,560,610
p += [rect(px,py,pw,ph,'#fffaf0',PALETTE['ink'],2,4)]
xmin,xmax=-8,10; ymin,ymax=-24,24
def bx(x): return px+(x-xmin)/(xmax-xmin)*pw
def by(y): return py+ph-(y-ymin)/(ymax-ymin)*ph
p += [line(px,by(0),px+pw,by(0),PALETTE['ink'],2),line(bx(0),py,bx(0),py+ph,PALETTE['ink'],2),text(px+pw-5,by(0)-8,'x',18,700,'end'),text(bx(0)+10,py+20,'y',18,700)]
segments=[]
for a,b in [(-8,-5),(-5,0),(5,10)]:
    pts=[]
    for k in range(121):
        x=a+(b-a)*k/120; rhs=x**3-25*x
        if rhs>=0:
            y=math.sqrt(rhs); pts.append((bx(x),by(y)))
    if pts:
        d='M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts); segments.append(path(d,'none',PALETTE['blue'],4))
        d2='M'+' L'.join(f'{x:.2f} {by(-(ymin+(py+ph-y)/ph*(ymax-ymin))):.2f}' for x,y in pts)
for a,b in [(-8,-5),(-5,0),(5,10)]:
    up=[]; lo=[]
    for k in range(121):
        x=a+(b-a)*k/120; rhs=x**3-25*x
        if rhs>=0:
            y=math.sqrt(rhs); up.append((bx(x),by(y))); lo.append((bx(x),by(-y)))
    if up:
        p += [path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in up),'none',PALETTE['blue'],4),path('M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in lo),'none',PALETTE['blue'],4)]
qx,qy=25/4,75/8
p += [circle(bx(qx),by(qy),8,PALETTE['red'],PALETTE['red'],2),line(bx(qx)+8,by(qy)-8,650,470,PALETTE['red'],2),text(650,455,'P = (25/4, 75/8)',19,700,'end',PALETTE['red']),text(650,482,'verified exactly on E₅',16,600,'end',PALETTE['red'])]
p += [rect(700,390,240,610,'#fffaf0',PALETTE['gold'],2,12),text(820,430,'AREA-FIVE TRIANGLE',17,700,'middle',PALETTE['gold'])]
A=(745,820); B=(895,820); C=(745,610)
p += [path(f'M{A[0]} {A[1]} L{B[0]} {B[1]} L{C[0]} {C[1]} Z','#e8dfca',PALETTE['ink'],3),rect(745,790,30,30,'none',PALETTE['ink'],2),text(820,855,'20/3',18,700,'middle'),text(720,720,'3/2',18,700,'end'),text(835,700,'41/6',18,700,'middle')]
p += [text(820,900,'½ · (3/2) · (20/3) = 5',17,700,'middle',PALETTE['green']),text(820,940,'exact rational sides',16,600,'middle',PALETTE['muted'])]
p += [rect(115,1040,825,140,'#f3ead6',PALETTE['gold'],2,12),text(140,1080,'BOUNDARY',18,700,fill=PALETTE['red']),text(140,1118,'Finding a rational point is not a completeness proof for E₅(Q).',21,700,fill=PALETTE['red']),text(140,1154,'This finite rendering makes no rank or BSD claim.',19,600,fill=PALETTE['muted'])]
bsd=finish(p)
sha_bsd=write('docs/assets/documentaries/bsd/plate_curve_successor.svg',bsd)

# 6 Hodge
p=base('Plate III — The cycle-class map','Established algebraic-to-Hodge direction; conjectural rational converse isolated.','A conceptual vector diagram maps codimension-p algebraic cycles with rational coefficients through the cycle-class map into rational Hodge classes, showing possible information loss and a dashed conjectural converse.')
p += [text(112,300,'ORIENTATION',18,700,fill=PALETTE['gold']), text(112,334,'codimension p on a smooth projective X',26,700), text(943,334,'conceptual exact labels',18,600,'end',PALETTE['green'])]
p += [rect(120,430,315,430,'#fffaf0',PALETTE['gold'],3,16),text(277,475,'ALGEBRAIC SIDE',19,700,'middle',PALETTE['gold']),text(277,535,'Zᵖ(X) ⊗ Q',30,700,'middle')]
for j,(yy,w) in enumerate([(615,190),(675,155),(735,210)]):
    p += [ellipse(277,yy,w/2,28,'#dce8ef',PALETTE['ink'],2),text(277,yy+6,f'codim-p cycle {j+1}',16,600,'middle')]
p += [text(277,815,'formal Q-linear combinations',17,600,'middle',PALETTE['muted'])]
p += [arrow(450,645,605,645,PALETTE['red'],4,'clᵖ',-18),text(527,700,'cycle-class map',18,700,'middle',PALETTE['red'])]
p += [rect(620,430,315,430,'#fffaf0',PALETTE['gold'],3,16),text(777,475,'COHOMOLOGICAL SIDE',19,700,'middle',PALETTE['gold']),text(777,545,'H²ᵖ(X,Q) ∩ Hᵖ,ᵖ(X)',25,700,'middle'),text(777,625,'rational Hodge classes',18,600,'middle')]
p += [path('M665 705 C710 675 735 675 770 705','none',PALETTE['blue'],3),path('M665 740 C710 710 735 710 770 705','none',PALETTE['blue'],3),circle(800,705,26,'#dce8ef',PALETTE['ink'],2),text(800,711,'α',20,700,'middle'),text(777,790,'different cycles may share a class',16,600,'middle',PALETTE['muted'])]
p += [rect(120,930,815,250,'#f3ead6',PALETTE['gold'],2,12),text(145,970,'ESTABLISHED DIRECTION',18,700,fill=PALETTE['green']),text(145,1008,'algebraic cycles  →  rational (p,p) classes',22,700,fill=PALETTE['green']),line(145,1040,910,1040,PALETTE['gold'],1),text(145,1080,'OPEN CONVERSE',18,700,fill=PALETTE['red']),text(145,1118,'rational Hodge class  ⇢  Q-combination of algebraic cycles ?',21,700,fill=PALETTE['red']),text(145,1152,'No injectivity or general surjectivity is asserted by this diagram.',17,600,fill=PALETTE['muted'])]
hodge=finish(p)
sha_hodge=write('docs/assets/documentaries/hodge/cycle_class_successor.svg',hodge)

manifest={
  'schema_version':'1.0.0','operation_id':'MP-DOC-VISUAL-PILOT-SUCCESSORS-001',
  'protected_base_commit':'3b79b35fadc6805775246c03124deb3e1425ef86',
  'generator':'tools/render_visual_pedagogy_successors.py',
  'environment':'Python 3 standard library; deterministic SVG; no randomness; no external services',
  'outputs':[
   {'plate_id':'PC-RICCI-FLOW-PLATE-II','representation_class':'schematic','path':'docs/assets/documentaries/poincare/plate_geometry_successor.svg','sha256':sha_ricci,'source_reference':'docs/documentaries/poincare.md#geometry'},
   {'plate_id':'PC-SURGERY-PLATE-III','representation_class':'schematic','path':'docs/assets/documentaries/poincare/plate_surgery_successor.svg','sha256':sha_surgery,'print_path':'docs/assets/documentaries/poincare/plate_surgery_successor_print.svg','print_sha256':sha_surgery_print,'source_reference':'docs/documentaries/poincare.md#surgery'},
   {'plate_id':'RH-CRITICAL-STRIP-PLATE-II','representation_class':'exact','path':'docs/assets/documentaries/riemann/critical_strip_successor.svg','sha256':sha_rh,'source_reference':'docs/documentaries/riemann.md#zeros'},
   {'plate_id':'NS-VORTICITY-PLATE-II','representation_class':'schematic','path':'docs/assets/documentaries/navier_stokes/vorticity_stretching_successor.svg','sha256':sha_ns,'source_reference':'docs/documentaries/navier_stokes.md#vorticity'},
   {'plate_id':'BSD-CURVE-PLATE-I','representation_class':'data-derived','path':'docs/assets/documentaries/bsd/plate_curve_successor.svg','sha256':sha_bsd,'source_reference':'docs/documentaries/bsd.md#rational-points'},
   {'plate_id':'HC-CYCLE-CLASS-PLATE-III','representation_class':'schematic','path':'docs/assets/documentaries/hodge/cycle_class_successor.svg','sha256':sha_hodge,'source_reference':'docs/documentaries/hodge.md#cycles'},
  ],
  'positive_controls':[
   {'path':'docs/assets/documentaries/p_vs_np/reduction.svg','git_blob':'e351902a073e9fdb41d0953400992d1732fd0fd4'},
   {'path':'docs/assets/documentaries/euclid_book_vii/plate_anthyphairesis.svg','git_blob':'6bcddb97bcd31d99575cfbbe1f6698b9c6eb3cd1'}
  ],
  'authority_boundary':{'visual_is_evidence':False,'programme_wide_migration_authorized':False,'mathematical_claim_promoted':False},
  'publication_state':'review_candidates_only; canonical documentary page references remain on predecessor assets until independent visual-semantic review'
}
write('governance/visual_pedagogy/successor_render_manifest.json', json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(manifest, indent=2))
