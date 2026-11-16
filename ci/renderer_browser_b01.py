#!/usr/bin/env python3
"""Non-production exact-head real-Chromium math and documentary parity audit."""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlsplit

SLUGS=('bsd','hodge','navier_stokes','p_vs_np','poincare','riemann','union_closed','yang_mills')
ROUTES=('index.html','erdos/catalogue/index.html','erdos/problems/0001/index.html','erdos/problems/1221/index.html','oai26/catalogue/index.html','oai26/families/001/index.html','oai26/families/377/index.html','CMDG_CM4/index.html')+tuple('documentaries/'+s+'/index.html' for s in SLUGS)
SIZES={'desktop':(1440,900),'mobile':(390,844)}
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,root,**kw):
  self.root=root;super().__init__(*a,directory=str(root),**kw)
 def translate_path(self,path):
  path=urlsplit(path).path;prefix='/MATH-PROGRAMME/'
  if not path.startswith(prefix):return str(self.root/'__not_found__')
  return super().translate_path('/'+path[len(prefix):])
 def log_message(self,*args):pass
@contextmanager
def serve(root):
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,root=root));thread=Thread(target=server.serve_forever,daemon=True);thread.start()
 try:yield 'http://127.0.0.1:'+str(server.server_port)+'/MATH-PROGRAMME/'
 finally:server.shutdown();server.server_close();thread.join(timeout=3)
def inspect(page):
 return page.evaluate('''() => {
 const visible=e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'};
 const math=[...document.querySelectorAll('mjx-container, .MathJax, .katex')].filter(visible);
 const main=document.querySelector('main,article,.md-content__inner');
 const clipped=math.filter(e=>{let r=e.getBoundingClientRect();return r.left < -12 || r.right > innerWidth+24}).slice(0,6).map(e=>[Math.round(e.getBoundingClientRect().left),Math.round(e.getBoundingClientRect().right)]);
 const images=[...document.querySelectorAll('main img,article img')];
 return {h1:(document.querySelector('h1')?.innerText||'').trim().slice(0,150),main:!!main,
 chars:(main?.innerText||'').length,raw_math:document.querySelectorAll('.arithmatex').length,
 rendered_math:math.length,clipped_math:clipped,broken_images:images.filter(e=>!e.complete||!e.naturalWidth).map(e=>e.getAttribute('src')).slice(0,8),
 images:images.length,overflow:Math.max(0,Math.round(document.documentElement.scrollWidth-innerWidth)),mathjax_present:!!window.MathJax};}''')
def compare(a,b,route,viewport,mode):
 reasons=[]
 if b['status']!=200 or not b['main'] or b['chars']<60:reasons.append('CANDIDATE_PAGE_UNREADABLE')
 if a['h1']!=b['h1']:reasons.append('HEADING_CHANGED')
 if b['broken_images'] and not a['broken_images']:reasons.append('CANDIDATE_BROKEN_IMAGES')
 if b['overflow']>32 and b['overflow']>a['overflow']+20:reasons.append('CANDIDATE_MOBILE_OVERFLOW')
 if b['clipped_math'] and not a['clipped_math']:reasons.append('CANDIDATE_CLIPPED_MATH')
 if mode=='default' and a['rendered_math']>0 and b['rendered_math']==0:reasons.append('MATHJAX_RENDERING_LOST')
 return [{'route':route,'viewport':viewport,'mode':mode,'code':r} for r in reasons]
def run(mk,zen,dest):
 from playwright.sync_api import sync_playwright
 for site,root in (('mkdocs',mk),('zensical',zen)):
  missing=[r for r in ROUTES if not (root/r).is_file()]
  if missing:raise RuntimeError(site+' missing '+str(missing))
 dest.mkdir(parents=True,exist_ok=True);shots=dest/'screenshots';shots.mkdir(exist_ok=True)
 results=[];fail=[]
 with serve(mk) as bm,serve(zen) as bz,sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  browser_version=browser.version
  for size,(width,height) in SIZES.items():
   for route in ROUTES:
    observations={}
    for label,base in (('mkdocs',bm),('zensical',bz)):
     cx=browser.new_context(viewport={'width':width,'height':height});p=cx.new_page();errors=[]
     p.on('pageerror',lambda e:errors.append(str(e)[:200]))
     url=base+route.removesuffix('index.html');res=p.goto(url,wait_until='domcontentloaded',timeout=20000)
     p.wait_for_timeout(1200);obs=inspect(p);obs['status']=res.status if res else None;obs['errors']=errors[:5]
     shot=shots/(label+'_'+size+'_'+route.replace('/','_')+'.png');p.screenshot(path=str(shot));obs['screenshot']=shot.name
     obs['sha256']=hashlib.sha256(shot.read_bytes()).hexdigest();observations[label]=obs;cx.close()
    fail+=compare(observations['mkdocs'],observations['zensical'],route,size,'default')
    results.append({'route':route,'viewport':size,'mode':'default',**observations})
  for route in ('erdos/problems/0001/index.html','oai26/families/001/index.html','CMDG_CM4/index.html'):
   for mode in ('no_js','mathjax_blocked'):
    observations={}
    for label,base in (('mkdocs',bm),('zensical',bz)):
     cx=browser.new_context(java_script_enabled=(mode!='no_js'),viewport={'width':390,'height':844});p=cx.new_page()
     if mode=='mathjax_blocked':p.route('**/*mathjax*',lambda r:r.abort())
     res=p.goto(base+route.removesuffix('index.html'),wait_until='domcontentloaded',timeout=20000)
     p.wait_for_timeout(500);obs=inspect(p);obs['status']=res.status if res else None;observations[label]=obs;cx.close()
    fail+=compare(observations['mkdocs'],observations['zensical'],route,'mobile',mode)
    results.append({'route':route,'viewport':'mobile','mode':mode,**observations})
  browser.close()
 head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 report={'record_type':'DOC_RENDER_G1_B01_CHROMIUM/1','head':head,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'chromium_version':browser_version,'routes':len(ROUTES),'observations':results,'critical_differences':fail,'screenshots':len(list(shots.glob('*.png'))),
 'limitations':['Chromium only; not screen-reader review','MathJax network availability is recorded, not assumed','Geometry cannot certify mathematical semantics','No production change']}
 (dest/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'head':head,'observations':len(results),'screenshots':report['screenshots'],'critical':len(fail),'examples':fail[:15]},indent=2))
 return bool(fail)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--mkdocs',type=Path,default=Path('.mkdocs-probe-site'));p.add_argument('--zensical',type=Path,default=Path('.zensical-probe-site'));p.add_argument('--out',type=Path,default=Path('renderer-b01-evidence'));a=p.parse_args()
 raise SystemExit(2 if run(a.mkdocs.resolve(),a.zensical.resolve(),a.out.resolve()) else 0)
