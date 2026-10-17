#!/usr/bin/env python3
"""One bounded rejected/unmerged PR and publishing transport check per repo."""
from __future__ import annotations
import datetime
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def call(url):
    p=subprocess.run(['gh','api',url],capture_output=True,text=True,timeout=30)
    if p.returncode:raise ValueError(p.stderr[:180])
    return json.loads(p.stdout)
def main():
    live=json.loads((ROOT/'ESTATE_LIFECYCLE_READBACK_20261017.json').read_text())
    negative=[]
    pages=[]
    for e in live['repositories']:
        repo=e['repository']
        pr=call(f'repos/{repo}/pulls?state=closed&per_page=100')
        unmerged=[x for x in pr if x.get('merged_at') is None and x.get('base',{}).get('ref')=='main']
        selected=max(unmerged,key=lambda x:x.get('closed_at') or '') if unmerged else None
        negative.append({'repository':repo,
          'status':'AUTHENTIC_CLOSED_NOT_MERGED_PR_OBSERVED' if selected else 'NO_CLOSED_UNMERGED_PR_IN_LATEST_100',
          'sample_pr_number':selected['number'] if selected else None,
          'sample_pr_url':selected['html_url'] if selected else None,
          'closed_at':selected['closed_at'] if selected else None,
          'pr_head_sha':selected['head']['sha'] if selected else None,
          'cause_of_nonmerge_authenticated':False,
          'failure_path_gate_rejection_certified':False})
        if repo=='grandchallenge/GCT-EXECUTIVE':
            for key in ('sample_pr_number','sample_pr_url','closed_at','pr_head_sha'):
                negative[-1][key]=None
            negative[-1]['private_metadata_redacted']=True
        target=e['publication']['url']
        if target:
            c=subprocess.run(['curl','-L','-sS','-o','/dev/null','--max-time','22',
               '-w','%{http_code}|%{url_effective}|%{content_type}',target],
               capture_output=True,text=True,timeout=27)
            segments=c.stdout.strip().split('|',2)
            success=(c.returncode==0 and len(segments)==3 and segments[0]=='200'
                     and segments[1].startswith('https://'))
            pages.append({'repository':repo,'configured_url':target,
                'http_status':int(segments[0]) if segments and segments[0].isdigit() else None,
                'final_url':segments[1] if len(segments)>1 else None,
                'content_type':segments[2] if len(segments)>2 else None,
                'https_transport_readback':'PASS' if success else 'FAIL_OR_UNAVAILABLE',
                'published_document_semantically_matches_source':'NOT_VERIFIED'})
        print(repo,negative[-1]['status'],flush=True)
    output={'record_type':'GCL_PAAR_001_REJECTED_STATE_AND_PUBLIC_HTTPS/1',
       'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'source_lifecycle_sha256':hashlib.sha256((ROOT/'ESTATE_LIFECYCLE_READBACK_20261017.json').read_bytes()).hexdigest(),
       'negative_samples':negative,'pages':pages,
       'closed_unmerged_samples':sum(x['status']=='AUTHENTIC_CLOSED_NOT_MERGED_PR_OBSERVED' for x in negative),
       'successful_https_pages':sum(x['https_transport_readback']=='PASS' for x in pages),
       'actual_negative_transition_causality_proven':False,
       'published_semantic_equivalence_proven':False,
       'global_assurance_certified':False}
    path=ROOT/'ESTATE_NEGATIVE_AND_PUBLIC_20261017.json'
    path.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'closed_unmerged':output['closed_unmerged_samples'],
       'page_http_ok':output['successful_https_pages'],'configured_pages':len(pages),
       'semantic_certification':False},sort_keys=True))
if __name__=='__main__':main()
