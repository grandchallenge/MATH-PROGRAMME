#!/usr/bin/env python3
"""Fail-closed critical publication parity with descriptive renderer differences.

Compares actual built HTML and referenced static assets. Does not infer theorem
certification, source provenance, or equivalent mathematics from HTML alone.
"""
from __future__ import annotations
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import re
from urllib.parse import urlsplit, unquote

_STATUS = re.compile(r'GCL_ERDOS_(?:HOME|SHOWCASE|LANDING)_STATUS')
_ALNUM = re.compile(r'\w+', re.UNICODE)
_MATH = re.compile(r'\\\(|\\\[|class=["\'][^"\']*(?:arithmatex|mathjax|katex)', re.I)
_CRITICAL = ('index.html', 'SHOWCASE/index.html', 'erdos/index.html',
             'erdos/catalogue/index.html','oai26/catalogue/index.html')

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings=[]; self.refs=[];self.visible=[];self.search_refs=[]
        self._skip=0;self._title=0;self._h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style','svg','noscript'):
            self._skip+=1
        if tag=='h1':self._h1+=1
        if tag=='title':self._title+=1
        for attr in ('src','href'):
            u=a.get(attr,'')
            if not u or not isinstance(u,str):continue
            if tag in ('script','link','img') and attr=='src' or (tag=='link' and attr=='href'):
                self.refs.append(u)
                if 'search' in u.lower():self.search_refs.append(u)
    def handle_endtag(self,tag):
        if tag in ('script','style','svg','noscript'):self._skip=max(0,self._skip-1)
        if tag=='h1':self._h1=max(0,self._h1-1)
        if tag=='title':self._title=max(0,self._title-1)
    def handle_data(self,data):
        if self._skip:return
        if self._h1:self.headings.append(data)
        if self._title:return
        self.visible.append(data)

def _local_asset(root:Path,html:Path,uri:str):
    parsed=urlsplit(uri)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith('data:'):
        return None
    if parsed.path.startswith('/'):
        # Do not claim a root-absolute path resolves without knowing site_url.
        return None
    target=(html.parent/unquote(parsed.path)).resolve()
    if not target.is_relative_to(root.resolve()):
        return 'ESCAPES_SITE_ROOT'
    return target

def inspect(root:Path,route:str):
    html=root/route
    markup=html.read_text(encoding='utf-8')
    parsed=Page();parsed.feed(markup)
    heading=' '.join(' '.join(parsed.headings).split()).casefold()
    words=Counter(_ALNUM.findall(' '.join(parsed.visible).casefold()))
    missing=[]
    for u in parsed.refs:
        asset=_local_asset(root,html,u)
        # MkDocs/Zensical use directory-style canonical links (`../foo/`).
        # A route with index.html is a valid local target, not a broken asset.
        if asset=='ESCAPES_SITE_ROOT' or (asset is not None
                and not asset.is_file()
                and not (asset.is_dir() and (asset/'index.html').is_file())):
            missing.append(u)
    return {'h1':heading,'word_count':sum(words.values()),'words':words,
            'math_markers':len(_MATH.findall(markup)),
            'missing_assets':missing[:20], 'search_asset_references':len(parsed.search_refs),
            'unexpanded_marker':bool(_STATUS.search(markup)),
            'html_sha256':hashlib.sha256(markup.encode()).hexdigest()}

def audit(baseline:Path,candidate:Path,routes:set[str]):
    issues=[];descriptive=[]; heading_drift=[]; math_loss=[];low_overlap=[]
    inherited_broken=[]
    for route in sorted(routes):
        b=inspect(baseline,route);c=inspect(candidate,route)
        if c['unexpanded_marker']:issues.append({'route':route,'code':'UNEXPANDED_SOURCE_MARKER'})
        if c['missing_assets']:
            # A defect shared by the production baseline is an independent
            # legacy defect; it is not evidence of *new* Zensical breakage.
            # Compare resolved target identities, not only href strings.
            baseline_broken = set(b['missing_assets'])
            new_broken = sorted(set(c['missing_assets']) - baseline_broken)
            if new_broken:
                issues.append({'route':route,'code':'NEW_BROKEN_LOCAL_ASSETS',
                               'examples':new_broken[:20],
                               'baseline_broken_examples':b['missing_assets']})
            if baseline_broken:
                inherited_broken.append({'route':route,
                                         'baseline_examples':b['missing_assets'],
                                         'candidate_examples':c['missing_assets']})
        if route in _CRITICAL and not c['h1']:
            issues.append({'route':route,'code':'MISSING_CRITICAL_HEADING'})
        if b['h1']!=c['h1']:
            heading_drift.append({'route':route,'baseline':b['h1'][:100], 'candidate':c['h1'][:100]})
        if b['math_markers'] and not c['math_markers']:
            math_loss.append(route)
        common=sum((b['words']&c['words']).values())
        denominator=max(1,sum(b['words'].values()))
        overlap=round(common/denominator,4)
        if overlap<0.80 and denominator>=100:
            low_overlap.append({'route':route,'baseline_tokens':denominator,
                                'candidate_tokens':sum(c['words'].values()),'overlap':overlap})
        if route in _CRITICAL:
            descriptive.append({'route':route,'baseline_sha256':b['html_sha256'],
                 'candidate_sha256':c['html_sha256'],'baseline_math_markers':b['math_markers'],
                 'candidate_math_markers':c['math_markers'],'baseline_search_refs':b['search_asset_references'],
                 'candidate_search_refs':c['search_asset_references'],'visible_token_overlap':overlap})
    # Some CSS/JS is intentionally renderer-specific; report counts rather than
    # require binary asset equality. Missing locally referenced files are fatal.
    return {'html_routes_audited':len(routes),'critical_issues':issues[:40],
            'critical_issue_count':len(issues),
            'baseline_broken_asset_route_count':len(inherited_broken),
            'baseline_broken_asset_route_examples':inherited_broken[:12],
            'heading_drift_count':len(heading_drift),
            'heading_drift_examples':heading_drift[:20], 'math_marker_loss_count':len(math_loss),
            'math_marker_loss_examples':math_loss[:20], 'low_visible_token_overlap_count':len(low_overlap),
            'low_overlap_examples':low_overlap[:20], 'critical_route_fingerprints':descriptive,
            'semantics_proven_equivalent':False,
            'limitations':['HTML math marker counts do not verify mathematical rendering.',
                           'Visible token overlap is a diagnostic, not proof of semantic equivalence.',
                           'Search index relevance or navigability requires a dedicated browser audit.',
                           'External and root-absolute asset URLs are not verified by local file checks.']}

# Governed source assets should be byte identical across renderers; theme
# bundles need not match because their implementation is renderer-dependent.
GOVERNED_ASSET_PREFIXES = ('assets/documentaries/', 'assets/visual_pedagogy/',
                           'stylesheets/', 'javascripts/')

def governed_asset_census(baseline:Path,candidate:Path):
    def file_map(root):
        result={}
        for prefix in GOVERNED_ASSET_PREFIXES:
            d=root/prefix
            if d.is_dir():
                for p in d.rglob('*'):
                    if p.is_file():
                        result[p.relative_to(root).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        return result
    before=file_map(baseline);after=file_map(candidate)
    missing=sorted(before.keys()-after.keys())
    changed=sorted(k for k in before.keys()&after.keys() if before[k]!=after[k])
    return {'baseline_governed_asset_files':len(before),
            'candidate_governed_asset_files':len(after),
            'missing_governed_asset_count':len(missing),'changed_governed_asset_count':len(changed),
            'missing_examples':missing[:20],'changed_examples':changed[:20],
            'byte_identical_on_shared_source_assets':not missing and not changed}

def search_census(root:Path):
    """Report actual built search-index form; never invent search compatibility."""
    candidates=sorted(p for p in root.rglob('*') if p.is_file()
                      and 'search' in p.parts and p.name.endswith('.json'))
    records=[]
    for p in candidates:
        record={'path':p.relative_to(root).as_posix(), 'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        try:
            import json
            j=json.loads(p.read_text(encoding='utf-8'))
            if isinstance(j,dict) and isinstance(j.get('docs'),list):
                docs=j['docs']
                record['indexed_documents']=len(docs)
                record['indexed_title_count']=sum(bool(x.get('title')) for x in docs if isinstance(x,dict))
                record['locations']=sorted({x.get('location') for x in docs
                                           if isinstance(x,dict) and isinstance(x.get('location'),str)})
                record['index_schema']='MKDOCS_SEARCH_DOCS'
            else:
                record['index_schema']='OTHER_JSON'
        except (ValueError,OSError,UnicodeError):
            record['index_schema']='UNREADABLE_JSON'
        records.append(record)
    return records

def search_parity(baseline:Path,candidate:Path):
    before=search_census(baseline);after=search_census(candidate)
    bypath_before={x['path']:x for x in before}
    bypath_after={x['path']:x for x in after}
    missing=sorted(bypath_before.keys()-bypath_after.keys())
    route_losses=[]
    for path in sorted(bypath_before.keys()&bypath_after.keys()):
        a,b=bypath_before[path],bypath_after[path]
        if a.get('index_schema')=='MKDOCS_SEARCH_DOCS' and b.get('index_schema')=='MKDOCS_SEARCH_DOCS':
            route_losses.extend(sorted(set(a['locations'])-set(b['locations'])))
    return {'baseline_search_files':len(before),'candidate_search_files':len(after),
            'baseline_indexes':[{k:v for k,v in x.items() if k!='locations'} for x in before],
            'candidate_indexes':[{k:v for k,v in x.items() if k!='locations'} for x in after],
            'missing_baseline_search_files':missing,
            'missing_indexed_locations_count':len(route_losses),
            'missing_indexed_locations_examples':route_losses[:20],
            'search_parity_proven':bool(before) and bool(after) and not missing and not route_losses
                and all(x.get('index_schema')=='MKDOCS_SEARCH_DOCS' for x in before+after),
            'limitations':['Matching search document locations does not prove search ranking, tokenization or browser interactions.',
                           'No search index file or an unknown schema is inconclusive, never proof of parity.']}
