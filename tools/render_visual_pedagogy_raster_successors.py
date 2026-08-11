#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, mpmath as mp
from PIL import Image, ImageDraw
from matplotlib.patches import FancyBboxPatch, Polygon

DPI=100; NAVY='#07182f'; GOLD='#c7a24b'; PAPER='#f3ead7'; INK='#15253a'; TEAL='#3d7d8b'; RED='#aa5147'; CREAM='#fffaf0'
OUT={
'PC-RICCI-FLOW-PLATE-II':'governance/visual_pedagogy/review_candidates/poincare/plate_geometry_successor.png',
'PC-SURGERY-PLATE-III':'governance/visual_pedagogy/review_candidates/poincare/plate_surgery_successor.png',
'PC-SURGERY-PLATE-III-PRINT':'governance/visual_pedagogy/review_candidates/poincare/plate_surgery_successor_print.png',
'RH-CRITICAL-STRIP-PLATE-II':'governance/visual_pedagogy/review_candidates/riemann/critical_strip_successor.png',
'NS-VORTICITY-PLATE-II':'governance/visual_pedagogy/review_candidates/navier_stokes/vorticity_stretching_successor.png',
'BSD-CURVE-PLATE-I':'governance/visual_pedagogy/review_candidates/bsd/plate_curve_successor.png',
'HC-CYCLE-CLASS-PLATE-III':'governance/visual_pedagogy/review_candidates/hodge/cycle_class_successor.png'}
GALLERY='governance/visual_pedagogy/review_candidates/contact_sheet.png'
plt.rcParams.update({'font.family':'DejaVu Sans','figure.facecolor':NAVY,'savefig.facecolor':NAVY})

def plate(title,sub,kicker):
 f=plt.figure(figsize=(14,18),dpi=DPI); a=f.add_axes([0,0,1,1]); a.axis('off'); a.add_patch(FancyBboxPatch((.025,.02),.95,.96,boxstyle='round,pad=.006,rounding_size=.012',transform=a.transAxes,fc=PAPER,ec=GOLD,lw=3));
 for y,t,fs,c,w in [(.955,'GRAND CHALLENGE LABS',14,NAVY,'bold'),(.925,kicker,12,GOLD,'bold'),(.885,title,34,NAVY,'bold'),(.846,sub,15,'#665f54','normal')]: a.text(.5,y,t,ha='center',va='top',fontsize=fs,color=c,weight=w,style='italic' if y==.846 else 'normal')
 return f,a

def save(f,p): p.parent.mkdir(parents=True,exist_ok=True); f.savefig(p,dpi=DPI,pad_inches=0,metadata={'Software':'GCL visual-pedagogy renderer v4'}); plt.close(f)
def foot(a,text): a.text(.5,.105,text,ha='center',fontsize=11.5,color=RED); a.text(.5,.07,'REVIEW CANDIDATE · NOT PROOF AUTHORITY',ha='center',fontsize=11,color='#6d665d',weight='bold')

def ricci(p):
 f,a=plate('When Geometry Becomes an Engine','Metric evolution and curvature concentration are shown as different visual layers.','POINCARÉ · RICCI FLOW · PLATE II'); x=np.linspace(-3,3,80); X,Y=np.meshgrid(x,x)
 Zs=[1.1*np.exp(-.7*((X+s)**2+Y**2))+.45*np.exp(-1.5*((X-1)**2+(Y+.5)**2)) for s in (.9,.5,.15)]
 for i,(z,l) in enumerate(zip(Zs,(.07,.37,.67))): q=f.add_axes([l,.49,.25,.27],projection='3d'); q.plot_surface(X,Y,z,cmap='viridis',lw=0); q.view_init(26,-58); q.set_axis_off(); q.set_title(f'$t_{i}$',color=INK)
 h=f.add_axes([.1,.23,.8,.17]); z=Zs[-1]; d=x[1]-x[0]; lap=np.gradient(np.gradient(z,d,axis=1),d,axis=1)+np.gradient(np.gradient(z,d,axis=0),d,axis=0); h.imshow(abs(lap),origin='lower',extent=[-3,3,-3,3],cmap='magma',aspect='auto'); h.contour(X,Y,z,8,colors='white',linewidths=.5,alpha=.4); h.set_yticks([]); h.set_title('QUALITATIVE CURVATURE-CONCENTRATION MAP — separate encoding',loc='left',fontsize=11,weight='bold')
 a.text(.5,.805,r'$\partial_t g=-2\,\mathrm{Ric}(g)$',ha='center',fontsize=24,color=INK); foot(a,'Synthetic 3D teaching surfaces and a curvature proxy; not a numerical Ricci-flow solution or singularity certificate.'); save(f,p)

def dumb(U,V):
 r=.55+.45*(np.tanh((abs(U)-1.1)*2.8)+1)/2-.32*np.exp(-(U/.8)**2); return U,r*np.cos(V),r*np.sin(V)
def surgery(p,prt=False):
 f,a=plate('The Craft of Controlled Surgery','Recognize the neck, cut on two-spheres, cap, and keep the topology ledger.','POINCARÉ · CONTROLLED SURGERY · PLATE III'); u=np.linspace(-2.4,2.4,90); v=np.linspace(0,2*np.pi,55); U,V=np.meshgrid(u,v); X,Y,Z=dumb(U,V)
 for k,l in enumerate((.05,.36,.67)):
  q=f.add_axes([l,.49,.27,.27],projection='3d');
  if k==0: q.plot_surface(X,Y,Z,cmap='cividis',lw=0); [q.plot(np.full(120,xc),.38*np.cos(np.linspace(0,2*np.pi,120)),.38*np.sin(np.linspace(0,2*np.pi,120)),color=RED,lw=3) for xc in (-.55,.55)]
  else:
   for m in ((U<=-.55),(U>=.55)): q.plot_surface(np.where(m,X,np.nan),np.where(m,Y,np.nan),np.where(m,Z,np.nan),cmap='cividis',lw=0)
  q.view_init(20,-60); q.set_axis_off(); q.set_box_aspect((2,1,1)); q.set_title(('1 · RECOGNIZE','2 · CUT / REMOVE','3 · CAP / CONTINUE')[k],fontsize=12,weight='bold')
 l=f.add_axes([.1,.22,.8,.16]); l.axis('off'); l.add_patch(FancyBboxPatch((0,0),1,1,boxstyle='round,pad=.02',fc=CREAM,ec=GOLD,lw=2)); l.text(.03,.8,'SURGERY EVENT LEDGER',color=GOLD,weight='bold'); rows=['local model: S² × I neck','cut locus: two spherical cross-sections','removed: middle neck segment','continue: capped components','record: topology/component transition']; [l.text(.05,.62-i*.12,t,fontsize=11,color=INK) for i,t in enumerate(rows)]
 a.text(.5,.805,'Surgery is controlled simplification — never arbitrary cutting.',ha='center',fontsize=18,color=NAVY,weight='bold');
 if prt: a.text(.92,.945,'PRINT',ha='center',fontsize=9,color=GOLD,weight='bold')
 foot(a,'Procedural 3D teaching geometry; it does not certify canonical-neighbourhood hypotheses, surgery scales, or topology preservation.'); save(f,p)

def riemann(p):
 f,a=plate('The Critical Strip','Exact analytic geography over a finite numerical texture of |ζ(σ+it)|.','RIEMANN · CRITICAL STRIP · PLATE II'); mp.mp.dps=20; s=np.linspace(-.2,1.2,60); t=np.linspace(-30,30,110); A=np.array([[float(mp.log10(1+min(abs(mp.zeta(mp.mpc(float(x),float(y)))),1e6))) for x in s] for y in t]); q=f.add_axes([.11,.29,.78,.46]); im=q.imshow(A,origin='lower',extent=[s[0],s[-1],t[0],t[-1]],aspect='auto',cmap='magma');
 for x,lab in ((0,'Re(s)=0'),(.5,'critical line'),(1,'Re(s)=1')): q.axvline(x,color=GOLD if x==.5 else 'white',ls='-' if x==.5 else '--',lw=2); q.text(x,29,lab,rotation=90,va='top',ha='right',fontsize=8,color=GOLD if x==.5 else 'white')
 q.scatter([1],[0],s=70,c=RED,edgecolors='white'); q.set_xlabel('σ = Re(s)'); q.set_ylabel('t = Im(s)'); q.set_title('FINITE NUMERICAL FIELD: log10(1+|ζ(σ+it)|)',loc='left',fontsize=11,weight='bold'); f.colorbar(im,ax=q,fraction=.025,pad=.01)
 a.text(.5,.805,r'$s=\sigma+it$    ·    $s\leftrightarrow1-s$    ·    $s\leftrightarrow\bar{s}$',ha='center',fontsize=19,color=NAVY); foot(a,'Finite numerical magnitude texture only. No nontrivial zero is certified, located, or inferred from the image.'); save(f,p)

def ns(p):
 f,a=plate('Energy Guards; Vorticity Stretches','Local three-dimensional stretching is separated from global energy control.','NAVIER–STOKES · VORTICITY · PLATE II'); q=f.add_axes([.12,.36,.76,.43],projection='3d'); z=np.linspace(-3,3,350); th=np.linspace(0,6*np.pi,350); r=np.linspace(.58,.22,350); q.plot(r*np.cos(th),r*np.sin(th),z,color=GOLD,lw=8)
 for k in range(10): ph=2*np.pi*k/10; tt=np.linspace(0,5*np.pi,200); zz=np.linspace(-3,3,200); rr=.9+.07*np.sin(tt+ph); q.plot(rr*np.cos(tt+ph),rr*np.sin(tt+ph),zz,color=TEAL,lw=1,alpha=.5)
 q.quiver(0,0,-2.7,0,0,5.3,color=RED,lw=3); q.view_init(20,-55); q.set_axis_off(); q.set_box_aspect((1,1,1.6)); a.text(.5,.805,'shorter/thicker  →  longer/thinner',ha='center',fontsize=18,weight='bold',color=NAVY); a.text(.25,.23,r'$\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega$',ha='center',fontsize=11,color=INK); a.text(.75,.23,r'$\frac{1}{2}\|u(t)\|_2^2+\nu\int_0^t\|\nabla u\|_2^2ds=\frac{1}{2}\|u_0\|_2^2$',ha='center',fontsize=10,color=INK); foot(a,'Synthetic tube and streamlines; no Navier–Stokes solution, turbulence cascade, or finite-time blow-up is simulated.'); save(f,p)

def bsd(p):
 f,a=plate('A Rational Point Opens a Door','One exact witness joins an elliptic curve to an area-five rational triangle.','BIRCH–SWINNERTON-DYER · PLATE I'); q=f.add_axes([.09,.34,.54,.45]); x=np.linspace(-6,8,1600); g=x**3-25*x; y=np.where(g>=0,np.sqrt(np.maximum(g,0)),np.nan); q.plot(x,y,color=GOLD,lw=2.5); q.plot(x,-y,color=TEAL,lw=2); px,py=25/4,75/8; q.scatter([px,px],[py,-py],c=RED,s=[85,45]); q.annotate('P=(25/4,75/8)',(px,py),xytext=(4,15),arrowprops={'arrowstyle':'->','color':RED}); q.set(xlim=(-6,8),ylim=(-18,18)); q.grid(alpha=.18); q.set_title('EXACT REAL LOCUS OF E₅: y²=x³−25x',loc='left',fontsize=11,weight='bold')
 t=f.add_axes([.68,.42,.22,.28]); t.axis('off'); t.set(xlim=(0,1),ylim=(0,1)); t.add_patch(Polygon([[.12,.16],[.88,.16],[.12,.86]],fc='#dbe8eb',ec=TEAL,lw=3)); t.text(.5,.07,'3/2',ha='center'); t.text(.03,.5,'20/3',rotation=90); t.text(.58,.57,'41/6',rotation=43); t.text(.5,.94,'EXACT TRIANGLE',ha='center',color=GOLD,weight='bold'); t.text(.5,-.03,'Area = 5',ha='center',color='#587d68',weight='bold'); a.text(.5,.805,r'$E_5:y^2=x^3-25x$  ↔  $P=(25/4,75/8)$  ↔  area $=5$',ha='center',fontsize=18,color=NAVY); foot(a,'The point and triangle are exact; the plotted window is finite. No rank, completeness, or BSD claim is made.'); save(f,p)

def hodge(p):
 f,a=plate('From Subvarieties to Classes','Geometry casts a cohomological shadow; the established direction is not the open converse.','HODGE · CYCLE CLASS · PLATE III'); q=f.add_axes([.07,.4,.4,.36],projection='3d'); u=np.linspace(0,2*np.pi,80); v=np.linspace(0,2*np.pi,45); U,V=np.meshgrid(u,v); X=(1.7+.55*np.cos(V))*np.cos(U); Y=(1.7+.55*np.cos(V))*np.sin(U); Z=.4*np.sin(V); q.plot_surface(X,Y,Z,cmap='viridis',lw=0,alpha=.8); q.set_axis_off(); q.view_init(28,-55); q.set_box_aspect((1,1,.5))
 c=f.add_axes([.57,.43,.33,.27]); c.axis('off'); [c.add_patch(FancyBboxPatch((.1+i*.08,.12+i*.18),.8-i*.16,.16,boxstyle='round,pad=.015',fc=TEAL,alpha=.18+.08*i,ec=GOLD)) for i in range(3)]; c.text(.5,.86,r'$H^{2p}(X,Q)\cap H^{p,p}(X)$',ha='center',fontsize=15,weight='bold'); a.annotate('',xy=(.58,.58),xytext=(.46,.58),xycoords='axes fraction',arrowprops={'arrowstyle':'-|>','lw':3,'color':GOLD}); a.text(.52,.605,r'$\mathrm{cl}^p$',ha='center',fontsize=18,weight='bold'); a.text(.25,.23,'ESTABLISHED: algebraic cycle with Q-coefficients → rational Hodge class',ha='center',fontsize=10,color='#587d68'); a.text(.73,.23,'OPEN CONVERSE: does every rational Hodge class arise this way?',ha='center',fontsize=10,color=RED); foot(a,'Generic 3D teaching geometry; no injectivity, kernel, general surjectivity, or proof of the Hodge conjecture is asserted.'); save(f,p)

def gallery(root):
 keys=['BSD-CURVE-PLATE-I','HC-CYCLE-CLASS-PLATE-III','NS-VORTICITY-PLATE-II','PC-RICCI-FLOW-PLATE-II','PC-SURGERY-PLATE-III','RH-CRITICAL-STRIP-PLATE-II']; c=Image.new('RGB',(1290,1120),(236,232,222)); d=ImageDraw.Draw(c)
 for i,k in enumerate(keys): im=Image.open(root/OUT[k]).convert('RGB'); im.thumbnail((400,500),Image.Resampling.LANCZOS); x=(i%3)*430+(430-im.width)//2; y=(i//3)*560+10; c.paste(im,(x,y)); d.text(((i%3)*430+12,(i//3)*560+520),k,fill=(15,30,50))
 p=root/GALLERY; p.parent.mkdir(parents=True,exist_ok=True); c.save(p,'PNG',compress_level=6)
def render(root): ricci(root/OUT['PC-RICCI-FLOW-PLATE-II']); surgery(root/OUT['PC-SURGERY-PLATE-III']); surgery(root/OUT['PC-SURGERY-PLATE-III-PRINT'],True); riemann(root/OUT['RH-CRITICAL-STRIP-PLATE-II']); ns(root/OUT['NS-VORTICITY-PLATE-II']); bsd(root/OUT['BSD-CURVE-PLATE-I']); hodge(root/OUT['HC-CYCLE-CLASS-PLATE-III']); gallery(root)
def hashes(root): return {**{k:hashlib.sha256((root/v).read_bytes()).hexdigest() for k,v in OUT.items()},'REVIEW-CONTACT-SHEET':hashlib.sha256((root/GALLERY).read_bytes()).hexdigest()}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--hashes',action='store_true'); x=ap.parse_args(); r=Path(x.root); render(r); print(json.dumps(hashes(r),indent=2,sort_keys=True)) if x.hashes else None
if __name__=='__main__': main()
