#!/usr/bin/env python3
"""Real browser cross-engine search test. All outcomes fail closed on required target."""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from ci.renderer_browser_b01 import serve
from ci.zensical_semantic_parity import canonical_search_route

# Every mandatory target is a previously verified generated canonical page.
CASES=(
 {'query':'Erdős Problem #1221','target':'erdos/problems/1221/index.html','kind':'number'},
 {'query':'Free Solid Abelian Groups on Profinite Spaces','target':'CMDG_CM4/index.html','kind':'heading'},
 {'query':'OAI26 catalogue','target':'oai26/catalogue/index.html','kind':'acronym'},
 {'query':'The Geometry of Hidden Harmony','target':'documentaries/hodge/index.html','kind':'source-title'},
 {'query':'The Music of the Primes','target':'documentaries/riemann/index.html','kind':'source-title'},
 {'query':'The Shape of Computational Truth','target':'documentaries/p_vs_np/index.html','kind':'source-title'},
)
EXPLORATORY=('Erdős Problem #1','ζ(3)','\\zeta','"profinite spaces"','nonexistent-zzzxxyy-123')
SIZES={'desktop':(1440,900),'mobile':(390,844)}
JS='''() => {
 const visible=e=>{let s=getComputedStyle(e),r=e.getBoundingClientRect();return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
 let inputs=[...document.querySelectorAll('input')].map(x=>({placeholder:x.placeholder,role:x.getAttribute('role'),aria:x.getAttribute('aria-label'),type:x.type,visible:visible(x),outer:x.outerHTML.slice(0,400)}));
 let buttons=[...document.querySelectorAll('button,[role="button"],label')].filter(visible).map(x=>({text:x.textContent.trim().slice(0,60),aria:x.getAttribute('aria-label'),title:x.getAttribute('title'),outer:x.outerHTML.slice(0,200)})).slice(0,22);
 let found=[...document.querySelectorAll('.md-search-result__link,.md-search-result a,[data-md-component="search-result"] a,[role="listbox"] a, .search-result a')];
 let searchArea=document.querySelector('[data-md-component="search"],.md-search,.search, [role="search"]');
 let resultLinks=(found.length?found:(searchArea?[...searchArea.querySelectorAll('a[href]')]:[]));
 return {inputs,buttons,searchAreaPresent:!!searchArea,searchAreaText:(searchArea?.innerText||'').slice(0,3500),resultLinks:resultLinks.map(x=>({href:x.href,text:(x.innerText||x.textContent||'').trim().slice(0,240),html:x.outerHTML.slice(0,260)})).slice(0,35),activeElement:document.activeElement?.outerHTML.slice(0,270),url:location.href};
}'''

def probe(page,query,viewport,kind):
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)[:300]))
 res=page.goto(page._gcl_base,wait_until='domcontentloaded',timeout=30000)
 page.wait_for_timeout(700)
 before=page.evaluate(JS)
 # Prefer keyboard activation of the real UI, not direct index search.
 page.keyboard.press('/')
 page.wait_for_timeout(350)
 slash=page.evaluate(JS)
 inputs=page.locator('input[type="search"], input[role="searchbox"], .md-search__input')
 selected=None
 for i in range(inputs.count()):
  item=inputs.nth(i)
  if item.is_visible():selected=item;break
 if selected is None:
  for selector in ('[data-md-component="search-query"]','input[placeholder*="Search"]','input[placeholder*="search"]'):
   match=page.locator(selector)
   if match.count() and match.first.is_visible():selected=match.first;break
 if selected is not None:
  selected.fill(query,timeout=8000)
  page.wait_for_timeout(1600)
 after=page.evaluate(JS)
 # Playwright pierces open Shadow DOM (Zensical search uses a custom overlay).
 # document.querySelectorAll alone misses those links and must not create false negatives.
 shadow_links=page.locator('a[href]').evaluate_all('''els => els.filter(e => e.getRootNode() instanceof ShadowRoot || e.closest('dialog,[role="dialog"],.md-search__output,.md-search-result,[class*="search-result"]')).map(e=>({href:e.href,text:(e.innerText||e.textContent||'').trim().slice(0,240),html:e.outerHTML.slice(0,260)})).slice(0,180)''')
 merged={x['href']:x for x in after['resultLinks']+shadow_links}
 after['resultLinks']=list(merged.values())
 return {'query':query,'kind':kind,'viewport':viewport,'status':res.status if res else None,
  'open_from_keyboard':any(x['visible'] and (x['type']=='search' or (x['role'] or '')=='searchbox') for x in slash['inputs']),
  'initial_inputs':before['inputs'],'slash_inputs':slash['inputs'],'inputs_after':after['inputs'],
  'buttons':after['buttons'][:10],'search_area_present':after['searchAreaPresent'],
  'search_area_excerpt':after['searchAreaText'][:2200], 'results':after['resultLinks'], 'shadow_result_count':len(shadow_links),
  'active_element':after['activeElement'],'errors':errors[:10],
  'input_selected':selected is not None}

def check(result,expected):
 if expected is None:return []
 failures=[]
 if not result['input_selected']:failures.append('NO_USABLE_SEARCH_INPUT')
 if result['errors']:failures.append('JAVASCRIPT_PAGEERROR')
 links=result['results']
 if not any(canonical_search_route(x['href'].split('/MATH-PROGRAMME/')[-1])==expected for x in links):
  failures.append('REQUIRED_TARGET_NOT_FOUND')
 return failures

def run(a):
 mk=a.mkdocs.resolve();zen=a.zensical.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
 for root in (mk,zen):
  if not root.is_dir():raise RuntimeError('missing build '+str(root))
 indexes={}
 for label,root,name in [('mkdocs',mk,'search/search_index.json'),('zensical',zen,'search.json')]:
  p=root/name
  if not p.is_file():raise RuntimeError('missing real search index '+str(p))
  indexes[label]={'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
 observations=[];critical=[]
 with serve(mk) as bm,serve(zen) as bz,sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);browser_ver=browser.version
  for viewport,(w,h) in SIZES.items():
   matrix=CASES if viewport=='desktop' else CASES[:4]
   for case in list(matrix)+([{'query':q,'kind':'exploratory','target':None} for q in EXPLORATORY] if viewport=='desktop' else []):
    for label,url in (('mkdocs',bm),('zensical',bz)):
     cx=browser.new_context(viewport={'width':w,'height':h});page=cx.new_page();page._gcl_base=url
     result=probe(page,case['query'],viewport,case['kind']);result['engine']=label
     failures=check(result,case['target']);result['critical_failures']=failures
     critical.extend([{'engine':label,'viewport':viewport,'query':case['query'],'expected':case['target'],'code':x} for x in failures])
     shot=out/(label+'-'+viewport+'-'+str(len(observations))+'.png');page.screenshot(path=str(shot));result['screenshot']=shot.name;result['screenshot_sha256']=hashlib.sha256(shot.read_bytes()).hexdigest()
     observations.append(result);cx.close()
  browser.close()
 head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 report={'record_type':'DOC_RENDER_G1_B02_BROWSER_SEARCH/1','source_head':head,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'browser_version':browser_ver,'indexes':indexes,'cases':CASES,'observations':observations,'critical_failures':critical,
         'limitations':['Search ranking is not assumed identical','Exploratory Unicode and typo queries are reported, not automatically accepted as equivalent','Canonical target must appear in real browser results for the mandatory matrix','No public renderer changes']}
 p=out/'report.json';p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'head':head,'cases':len(observations),'critical':len(critical),'first_critical':critical[:15],'example':observations[0] if observations else None},indent=2)[:16000])
 return bool(critical)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--mkdocs',type=Path,default=Path('.mkdocs-probe-site'));p.add_argument('--zensical',type=Path,default=Path('.zensical-probe-site'));p.add_argument('--out',type=Path,default=Path('renderer-b02-evidence'));args=p.parse_args()
 raise SystemExit(2 if run(args) else 0)
