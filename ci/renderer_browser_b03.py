#!/usr/bin/env python3
"""B03 isolated Chromium and axe accessibility parity, never release authority."""
import argparse,hashlib,json,datetime,subprocess
from pathlib import Path
if __package__:
 from ci.renderer_browser_b01 import serve
else:
 from renderer_browser_b01 import serve
ROUTES=('index.html','erdos/problems/1221/index.html','oai26/catalogue/index.html','oai26/families/001/index.html','CMDG_CM4/index.html','documentaries/bsd/index.html','documentaries/hodge/index.html','documentaries/p_vs_np/index.html')
VIEWS={'desktop':(1440,900),'mobile':(390,844),'reflow200':(720,900)}
def new_severe(a,b):
 """Include increased node counts, even when the rule exists in baseline."""
 baseline={(x['id'],x['impact']):x.get('nodes',0) for x in a}
 return [{'rule':x['id'],'impact':x['impact'],'nodes':x.get('examples',[])[:3],
          'candidate_count':x.get('nodes',0),'baseline_count':baseline.get((x['id'],x['impact']),0)}
         for x in b if x['impact'] in ('serious','critical')
         and x.get('nodes',0)>baseline.get((x['id'],x['impact']),0)]

def inspect(page):
 return page.evaluate('''() => {let m=document.querySelector('main,article');let f=document.activeElement;let d=f;for(let n=0;n<5&&d?.shadowRoot?.activeElement;n++)d=d.shadowRoot.activeElement;return {heading:(document.querySelector('h1')?.innerText||'').trim().slice(0,150),main:!!m,chars:(m?.innerText||'').length,overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),lang:document.documentElement.lang,focus_tag:f?.tagName,focus_visible:!!f?.matches(':focus-visible'),focus_outer:f?.outerHTML.slice(0,250),deep_focus_tag:d?.tagName,deep_focus_outer:d?.outerHTML.slice(0,300),deep_focus_visible:!!d?.matches(':focus-visible'),skip_links:[...document.querySelectorAll('a[href^="#"]')].filter(x=>/skip/i.test(x.textContent)).map(x=>x.getAttribute('href')).slice(0,8),headings:[...document.querySelectorAll('h1,h2,h3')].slice(0,20).map(x=>[x.tagName,(x.innerText||'').trim().slice(0,70)])}}''')
def run(args):
 from playwright.sync_api import sync_playwright
 roots={'mkdocs':args.mkdocs.resolve(),'zensical':args.zensical.resolve()};out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
 axe=args.axe.resolve()
 if not axe.is_file():raise ValueError('pinned axe script absent')
 for name,root in roots.items():
  missing=[x for x in ROUTES if not (root/x).is_file()]
  if missing:raise ValueError(name+' missing '+str(missing))
 rows=[];critical=[]
 with serve(roots['mkdocs']) as ma,serve(roots['zensical']) as za,sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);version=browser.version
  for view,(w,h) in VIEWS.items():
   for route in ROUTES:
    pair={}
    for label,base in (('mkdocs',ma),('zensical',za)):
     cx=browser.new_context(viewport={'width':w,'height':h},reduced_motion='reduce',color_scheme='dark' if view=='reflow200' else 'light');page=cx.new_page();errors=[]
     page.on('pageerror',lambda e:errors.append(str(e)[:200]))
     resp=page.goto(base+route.removesuffix('index.html'),wait_until='domcontentloaded',timeout=25000)
     page.wait_for_timeout(550);before=inspect(page)
     page.keyboard.press('Tab');first=inspect(page)
     for _ in range(4):page.keyboard.press('Tab')
     fifth=inspect(page)
     # Expose actual browser-computed accessible names, not only HTML labels.
     aria_h1=page.locator('h1').first.aria_snapshot(timeout=6000)[:500] if page.locator('h1').count() else ''
     aria_nav=page.locator('nav').first.aria_snapshot(timeout=6000)[:1300] if page.locator('nav').count() else ''
     page.add_script_tag(path=str(axe))
     ax=page.evaluate('''async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})''')
     viol=[{'id':v['id'],'impact':v['impact'],'nodes':len(v['nodes']),'examples':[{'target':n['target'],'summary':(n.get('failureSummary') or '')[:180]} for n in v['nodes'][:3]]} for v in ax['violations']]
     search=None
     if route=='index.html':
      page.keyboard.press('Escape');page.keyboard.press('/');page.wait_for_timeout(330)
      search=inspect(page)
      page.keyboard.press('Escape')
     shot=out/(label+'_'+view+'_'+route.replace('/','_')+'.png');page.screenshot(path=str(shot))
     pair[label]={'status':resp.status if resp else None,'before':before,'first_tab':first,'fifth_tab':fifth,'search_shortcut':search,'aria_heading_snapshot':aria_h1,'aria_nav_snapshot':aria_nav,'color_scheme':'dark' if view=='reflow200' else 'light','axe_violations':viol,'axe_incomplete':len(ax['incomplete']),'axe_passes':len(ax['passes']),'js_errors':errors[:6],'screenshot':shot.name,'screenshot_sha256':hashlib.sha256(shot.read_bytes()).hexdigest()}
     cx.close()
    b=pair['mkdocs'];c=pair['zensical'];new=new_severe(b['axe_violations'],c['axe_violations'])
    if new:critical.append({'route':route,'view':view,'code':'NEW_SEVERE_AXE_RULE','rules':new})
    if c['status']!=200 or not c['before']['main'] or c['before']['chars']<50:critical.append({'route':route,'view':view,'code':'UNREADABLE_CANDIDATE'})
    if c['before']['overflow']>32 and c['before']['overflow']>b['before']['overflow']+20:critical.append({'route':route,'view':view,'code':'CANDIDATE_REFLOW_REGRESSION'})
    rows.append({'route':route,'view':view,**pair})
  browser.close()
 head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 report={'type':'GCL_B03_CHROMIUM_AXE/1','source_head':head,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'chromium':version,'axe_sha256':hashlib.sha256(axe.read_bytes()).hexdigest(),'paired_samples':rows,'new_critical_regressions':critical,'limitations':['Automated axe tests do not prove WCAG conformance','Manual screen-reader testing not performed by automation','Only sampled routes and Chromium with three viewports; reflow200 is a narrow viewport proxy, not actual browser zoom','Separate manual focus and semantic inspection needed before B03 closure','No production changes']}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'source_head':head,'paired':len(rows),'critical':len(critical),'examples':critical[:7],'screens':len(list(out.glob('*.png')))},indent=2)[:8000]);return bool(critical)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--mkdocs',type=Path,default=Path('.mkdocs-probe-site'));p.add_argument('--zensical',type=Path,default=Path('.zensical-probe-site'));p.add_argument('--axe',type=Path,default=Path('node_modules/axe-core/axe.min.js'));p.add_argument('--out',type=Path,default=Path('renderer-b03-evidence'))
 raise SystemExit(2 if run(p.parse_args()) else 0)
