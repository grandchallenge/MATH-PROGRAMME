"""Finite post-deployment coverage accounting for newly accepted/amended articles.

An article remains uncovered until a receipt is *protected merged* into the
coverage ledger; an Actions artifact or pending PR never counts as coverage.
"""
from __future__ import annotations
import hashlib
import json
import re

RECORD='ERDOS_ACCEPTED_RENDERED_COVERAGE/1'
SHA=re.compile(r'^[0-9a-f]{40}$')
DIGEST=re.compile(r'^[0-9a-f]{64}$')
MAX_PER_RECEIPT=25

def ensure(cond, reason):
    if not cond:raise ValueError('PARITY_COVERAGE_'+reason)

def verify_ledger(ledger):
    ensure(isinstance(ledger,dict) and set(ledger)=={'record_type','baseline_protected_sha','baseline_accepted','covered','bootstrap_ids'},'SCHEMA')
    ensure(ledger['record_type']==RECORD,'TYPE')
    ensure(isinstance(ledger['baseline_protected_sha'],str) and SHA.fullmatch(ledger['baseline_protected_sha']),'BASE_SHA')
    ensure(isinstance(ledger['baseline_accepted'],dict) and len(ledger['baseline_accepted'])>=1,'BASE_EMPTY')
    ensure(isinstance(ledger['covered'],dict),'COVERED_TYPE')
    ensure(isinstance(ledger['bootstrap_ids'],list) and len(set(ledger['bootstrap_ids']))==len(ledger['bootstrap_ids']),'BOOTSTRAP')
    for num,sha in ledger['baseline_accepted'].items():
        ensure(num.isdigit() and int(num)>0 and isinstance(sha,str) and DIGEST.fullmatch(sha),'BASE_ENTRY')
    for num,entry in ledger['covered'].items():
        ensure(num.isdigit() and int(num)>0 and isinstance(entry,dict),'COVER_ENTRY')
        ensure(set(entry)=={'source_sha256','public_html_sha256','verified_deployment_sha','run_id','receipt_sha256','editorial_sections','rendered_equations'},'COVER_FIELDS')
        ensure(all(isinstance(entry[k],str) and DIGEST.fullmatch(entry[k]) for k in ('source_sha256','public_html_sha256','receipt_sha256')),'COVER_HASH')
        ensure(isinstance(entry['verified_deployment_sha'],str) and SHA.fullmatch(entry['verified_deployment_sha']),'COVER_SHA')
        ensure(type(entry['run_id']) is int and entry['run_id']>0,'COVER_RUN')
        ensure(type(entry['editorial_sections']) is int and entry['editorial_sections']==6 and type(entry['rendered_equations']) is int and entry['rendered_equations']>=0,'COVER_QUANTITY')
    for value in ledger['bootstrap_ids']:
        ensure(type(value) is int and str(value) in ledger['baseline_accepted'],'BOOTSTRAP_ENTRY')
    return ledger

def plan(ledger,admissions,max_count=MAX_PER_RECEIPT):
    verify_ledger(ledger)
    ensure(isinstance(admissions,dict) and all(type(n) is int and n>0 and isinstance(e,dict) and isinstance(e.get('source_sha256'),str) and DIGEST.fullmatch(e['source_sha256']) for n,e in admissions.items()),'ADMISSIONS')
    ensure(type(max_count) is int and 1<=max_count<=MAX_PER_RECEIPT,'BATCH_SIZE')
    baseline=ledger['baseline_accepted'];covered=ledger['covered']
    # A claim whose accepted hash differs from the baseline or whose id was
    # explicitly seeded requires current protected proof for that exact hash.
    needed=[]
    for num,row in sorted(admissions.items()):
        key=str(num);digest=row['source_sha256']
        if (key not in baseline or baseline[key]!=digest or num in ledger['bootstrap_ids']):
            if key not in covered or covered[key]['source_sha256']!=digest:
                needed.append(num)
    return needed[:max_count],len(needed)-min(len(needed),max_count)

def apply_receipt(ledger,report):
    verify_ledger(ledger)
    ensure(isinstance(report,dict) and report.get('record_type')=='ERDOS_ACCEPTED_PARITY_BATCH_EVIDENCE/1','REPORT_SCHEMA')
    ensure(type(report.get('run_id')) is int and report['run_id']>0,'REPORT_RUN')
    sha=report.get('deployed_source_sha')
    ensure(isinstance(sha,str) and SHA.fullmatch(sha),'REPORT_SOURCE')
    records=report.get('articles')
    ensure(isinstance(records,list) and 1<=len(records)<=MAX_PER_RECEIPT,'REPORT_COUNT')
    keys=[];updated=json.loads(json.dumps(ledger))
    for item in records:
        ensure(isinstance(item,dict) and item.get('status')=='PASS_SOURCE_AND_RENDERED_HTML_PARITY','ARTICLE_NOT_PASS')
        num=item.get('problem_id')
        ensure(type(num) is int and num>0 and num not in keys,'DUPLICATE_ARTICLE')
        keys.append(num)
        ensure(item.get('source_commit')==sha and item.get('deployed_source_commit')==sha,'ART_DEPLOYMENT')
        ensure(item.get('visible_math_count')==item.get('verified_math_expressions') and item.get('verified_editorial_sections')==6 and item.get('mathjax_startup_complete') is True,'ART_RENDER')
        digest=item.get('source_sha256');html=item.get('public_html_sha256')
        ensure(isinstance(digest,str) and DIGEST.fullmatch(digest) and isinstance(html,str) and DIGEST.fullmatch(html),'ART_HASH')
        # The individual receipt digest is bound to the exact original
        # source and deployed HTML, even after 30-day Actions retention.
        material=json.dumps(item,sort_keys=True,separators=(',',':')).encode()
        updated['covered'][str(num)]={'source_sha256':digest,'public_html_sha256':html,
            'verified_deployment_sha':sha,'run_id':report['run_id'],
            'receipt_sha256':hashlib.sha256(material).hexdigest(),
            'editorial_sections':6,'rendered_equations':item['visible_math_count']}
    for num in keys:
        if num in updated['bootstrap_ids']:updated['bootstrap_ids'].remove(num)
    verify_ledger(updated)
    return updated
