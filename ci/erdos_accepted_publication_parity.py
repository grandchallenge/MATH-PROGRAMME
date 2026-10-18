"""Fail-closed, full-body protected manuscript versus actually deployed HTML check.

This verifies editorial/source identity and displayed mathematics, not theorem truth.
Caller MUST separately authenticate the protected deployment commit and admission.
"""
from __future__ import annotations
import hashlib
import json
import re
from bs4 import BeautifulSoup, NavigableString
import markdown

HEADINGS=('The question in plain language','A small example','What is known',
          "GCL's current state",'What remains','Sources and claim boundaries')

def _fail(msg): raise ValueError('ACCEPTED_PUBLICATION_PARITY_'+msg)
def _math(tex):
    tex=tex.strip()
    tex=re.sub(r'^\\+\(', '',tex)
    tex=re.sub(r'\\+\)$','',tex)
    tex=re.sub(r'^\\+\[','',tex)
    tex=re.sub(r'\\+\]$','',tex)
    return re.sub(r'\s+','',tex)

def _sections(soup):
    headings=soup.find_all('h2')
    found=[h.get_text(' ',strip=True) for h in headings]
    # A site contains a preceding heading, so seek the exactly delimited editorial six.
    # The main article is authored as exactly six canonical editorial sections.
    # Extra headings are not silently ignored in acceptance-critical comparison.
    if tuple(found[:6])!=HEADINGS or found[6:] not in ([],['Catalogue and evidence provenance']):_fail('HEADING_SEQUENCE')
    chosen=headings[:6]
    result=[];maths=[]
    for h in chosen:
        blocks=[]
        for node in h.next_siblings:
            if getattr(node,'name',None)=='h2':break
            if getattr(node,'name',None) not in ('p','ul','ol','pre','blockquote','table'):continue
            frag=BeautifulSoup(str(node),'html.parser')
            for elem in frag.select('.arithmatex'):
                script=elem.find('script',attrs={'type':re.compile('^math/tex')})
                tex=script.get_text() if script else elem.get_text(' ',strip=True)
                canonical=_math(tex)
                if not canonical:_fail('EMPTY_MATH')
                maths.append(canonical)
                elem.replace_with(NavigableString(f' MATH_{len(maths)} '))
            content=' '.join(frag.get_text(' ',strip=True).split())
            if content: blocks.append(content)
        if not blocks:_fail('EMPTY_SECTION')
        result.append({'heading':h.get_text(' ',strip=True),'blocks':blocks})
    return result,maths

def compare_accepted_article(*,problem_id:int,source:str,admission:dict,
                             public_html:bytes,public_url:str,
                             source_commit:str,deploy_commit:str)->dict:
    if type(problem_id) is not int or problem_id<1 or problem_id>1221:_fail('PROBLEM_ID')
    if not isinstance(source,str) or not source.strip():_fail('SOURCE')
    if not isinstance(admission,dict) or admission.get('source_sha256')!=hashlib.sha256(source.strip().encode()).hexdigest():_fail('SOURCE_HASH')
    if not all(isinstance(x,str) and re.fullmatch('[0-9a-f]{40}',x) for x in (source_commit,deploy_commit)):_fail('GIT_COMMIT')
    if source_commit!=deploy_commit:_fail('STALE_DEPLOYMENT')
    expected=f'https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/{problem_id:04d}/'
    if public_url!=expected:_fail('PUBLIC_URL')
    if not isinstance(public_html,bytes) or len(public_html)<100:_fail('PUBLIC_HTML')
    actual=BeautifulSoup(public_html,'html.parser')
    main=actual.select_one('main')
    if main is None:_fail('MAIN_MISSING')
    title=main.find('h1')
    if title is None or title.get_text(' ',strip=True)!=f'Erdős Problem #{problem_id}':_fail('PAGE_IDENTITY')
    status=main.get_text(' ',strip=True)
    if ('Reviewed explanatory article — evidence qualified' not in status
            or 'UNACCEPTED DRAFT' in status
            or 'NOT received separate GCL editorial acceptance' in status):_fail('ACCEPTED_STATUS')
    expected_html=markdown.markdown(source,extensions=['pymdownx.arithmatex','extra'])
    expected_sections,expected_math=_sections(BeautifulSoup(expected_html,'html.parser'))
    rendered_sections,rendered_math=_sections(main)
    if expected_sections!=rendered_sections:_fail('SUBSTANTIVE_TEXT_CHANGED')
    if expected_math!=rendered_math:_fail('MATH_CHANGED_OR_NOT_RENDERED')
    return {'record_type':'ERDOS_ACCEPTED_PUBLICATION_SOURCE_PARITY/1',
            'problem_id':problem_id,'public_url':public_url,
            'source_sha256':admission['source_sha256'],
            'source_commit':source_commit,'deployed_source_commit':deploy_commit,
            'public_html_sha256':hashlib.sha256(public_html).hexdigest(),
            'verified_editorial_sections':len(expected_sections),
            'verified_math_expressions':len(expected_math),
            'status':'PASS_SOURCE_AND_RENDERED_HTML_PARITY',
            'mathematical_theorem_certification':False}

# The production wrapper calls this only with an authenticated protected-source
# checkout and an independently authenticated successful Pages deployment.
def assert_rendered_math(browser, url: str, expected_count: int) -> dict:
    if expected_count<0 or url not in (f'https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/{n:04d}/' for n in range(1,1222)):
        _fail('BROWSER_ARGUMENTS')
    page=browser.new_page(viewport={'width':1280,'height':850})
    errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)[:200]))
    try:
        response=page.goto(url,wait_until='domcontentloaded',timeout=45000)
        if response is None or response.status!=200:_fail('HTTP_RESPONSE')
        page.wait_for_function('''expected => window.MathJax && window.MathJax.startup &&
          document.querySelectorAll('main .arithmatex mjx-container').length === expected''',
          arg=expected_count,timeout=45000)
        page.evaluate('async () => { await window.MathJax.startup.promise; }')
        output=page.evaluate('''() => ({inputs:document.querySelectorAll('main .arithmatex').length,
          rendered:document.querySelectorAll('main .arithmatex mjx-container').length})''')
        if output['rendered']!=expected_count or output['inputs']!=expected_count or errors:
            _fail('MATH_RENDERING')
        return {'visible_math_count':output['rendered'],'mathjax_startup_complete':True,'page_script_errors':errors}
    except Exception as err:
        raise ValueError('ACCEPTED_PUBLICATION_PARITY_RENDER_FAILURE') from err
    finally:page.close()
