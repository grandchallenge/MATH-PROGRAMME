#!/usr/bin/env python3
"""GCL-PAAR-C V3 pilot: externally corroborate *a new* execution origin.

Requires independently reviewed, protected INTELLECT V3 source and separate
receipt, plus authenticated GitHub original Actions execution evidence.
Never upgrades historical CHAD V1 origin or creates GitHub approvals.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.parse
from pathlib import Path

from agent_role_receipt import demand_native_source_review
from paar_execution_origin import verify_witness, gh_api, OriginError
from specialist_receipt_adapter import protected_specialist_receipt,material_fingerprint

ORIGIN='grandchallenge/INTELLECT'
RUN=38988609732
SUBJECT='b380e583ca2c997c07a4b7f15cbf97728006a79e'
MATERIAL='b6b353decee67953b74c984a1c8856c3ea56debbae0599f759564f13bbe214b4'
SOURCE_PR=127
SOURCE_HEAD='a9dadf682be3d7a62870b00e005c087e06bc6165'
DOSSIER_PATH=f'governance/agent_execution/reviews_v3/MATH-PROGRAMME-{SUBJECT}.json'
DOSSIER_BLOB='3fcc621d55dd27afb58eb3a782c8e983fbd666bc'
WITNESS_PATH='governance/agent_execution/GCL-ARC-001/witness-38988609732.json'
WITNESS_BLOB='4f1114a841e1adc5039c518ab6a55eeec9e80509'
WITNESS_SHA='e9a6cc3f140a3ab1befdf5500c4779a10873b32886b7c69a785bb05b2d6198ab'
RECEIPT_PATH=f'governance/material_admission_receipts_v3/MATH-PROGRAMME-{SUBJECT}.json'
SHA40=re.compile('[a-f0-9]{40}\\Z')

class V3OriginError(ValueError):pass

def need(ok,reason):
    if not ok:raise V3OriginError(reason)

def read_intellect(api_get,path,sha):
    need(bool(SHA40.fullmatch(sha)) and path.endswith('.json')
         and not path.startswith('/') and '..' not in path.split('/'),
         'untrusted source ref or path')
    url=f'/repos/{ORIGIN}/contents/{urllib.parse.quote(path,safe="/")}?ref={sha}'
    item=api_get(url)
    need(isinstance(item,dict) and item.get('type')=='file'
         and item.get('encoding')=='base64'
         and isinstance(item.get('sha'),str)
         and SHA40.fullmatch(item['sha']), 'missing protected source file')
    try:
        raw=base64.b64decode(item['content'].replace('\n',''),validate=True)
        record=json.loads(raw)
    except (KeyError,ValueError,TypeError) as e:
        raise V3OriginError('invalid protected source bytes') from e
    need(isinstance(record,dict),'protected source must be JSON object')
    # Verify GitHub Contents API blob identity independently from supplied SHA.
    actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    need(actual==item['sha'],'GitHub content Git-blob identity mismatch')
    return record,raw,item['sha']

def authenticated_review(api_get,number,head):
    url=f'/repos/{ORIGIN}/pulls/{number}'
    pr=api_get(url)
    need(isinstance(pr,dict) and pr.get('merged_at')
         and (pr.get('head') or {}).get('sha')==head
         and (pr.get('base') or {}).get('ref')=='main'
         and (pr.get('head') or {}).get('repo',{}).get('full_name')==ORIGIN,
         'review source PR not merged at exact head')
    author=(pr.get('user') or {}).get('login')
    need(isinstance(author,str) and author,'missing authenticated source author')
    try:
        reviewers=demand_native_source_review(api_get,url=url,source_head=head,
                                             source_author=author)
    except ValueError as error:
        raise V3OriginError('missing genuine exact-head nonauthor source approval') from error
    return reviewers

def verify_v3(*,api_get,downloaded_artifact:bytes,receipt_pr_number:int)->dict:
    """Require source + receipt native independent reviews AND true platform run.

    The separately downloaded original GitHub artifact is mandatory. The
    protected source witness is not accepted merely because hashes agree.
    """
    need(type(receipt_pr_number) is int and receipt_pr_number>0,
         'missing separately governed receipt PR')
    main=api_get(f'/repos/{ORIGIN}/branches/main')
    protected=(main.get('commit') or {}).get('sha') if isinstance(main,dict) else None
    need(main.get('protected') is True and isinstance(protected,str)
         and SHA40.fullmatch(protected),'INTELLECT protected main unavailable')
    receipt,rraw,rblob=read_intellect(api_get,RECEIPT_PATH,protected)
    subject={'repository':'grandchallenge/MATH-PROGRAMME','head_sha':SUBJECT,
             'material_sha256':MATERIAL}
    need(receipt.get('record_type')=='GCL_PROTECTED_PLATFORM_ORIGIN_ADMISSION_EVIDENCE_V3'
         and receipt.get('schema_version')=='4.0.0'
         and receipt.get('subject')==subject
         and receipt.get('authority_domain')=='PROTECTION'
         and receipt.get('verdict')=='PLATFORM_EXECUTION_ORIGIN_CORROBORATED_NOT_HISTORICAL_CHAD',
         'V3 receipt identity/authority mismatch')
    anchor=receipt.get('source_review_anchor') or {}
    need(anchor.get('source_pr_number')==SOURCE_PR
         and anchor.get('source_pr_head_sha')==SOURCE_HEAD
         and anchor.get('dossier_blob_sha')==DOSSIER_BLOB,
         'V3 source PR anchor drift')
    rpr=api_get(f'/repos/{ORIGIN}/pulls/{receipt_pr_number}')
    need(isinstance(rpr,dict) and rpr.get('merged_at')
         and (rpr.get('base') or {}).get('ref')=='main'
         and (rpr.get('head') or {}).get('repo',{}).get('full_name')==ORIGIN,
         'V3 receipt not protected-admitted')
    rfiles=api_get(f'/repos/{ORIGIN}/pulls/{receipt_pr_number}/files?per_page=100')
    need(isinstance(rfiles,list) and len(rfiles)==rpr.get('changed_files')
         and any(f.get('filename')==RECEIPT_PATH and f.get('sha')==rblob
                 and f.get('status')=='added' for f in rfiles),
         'receipt blob not introduced by independently reviewed receipt PR')
    receipt_reviewers=authenticated_review(api_get,receipt_pr_number,rpr['head']['sha'])
    source_reviewers=authenticated_review(api_get,SOURCE_PR,SOURCE_HEAD)
    sfiles=api_get(f'/repos/{ORIGIN}/pulls/{SOURCE_PR}/files?per_page=100')
    need(isinstance(sfiles,list) and len(sfiles)==5
         and any(f.get('filename')==DOSSIER_PATH and f.get('sha')==DOSSIER_BLOB
                 and f.get('status')=='added' for f in sfiles)
         and any(f.get('filename')==WITNESS_PATH and f.get('sha')==WITNESS_BLOB
                 and f.get('status')=='added' for f in sfiles),
         'V3 independent source PR did not introduce exact original witness and dossier')
    dossier,_,dblob=read_intellect(api_get,DOSSIER_PATH,protected)
    witness,wraw,wblob=read_intellect(api_get,WITNESS_PATH,protected)
    need(dblob==DOSSIER_BLOB and wblob==WITNESS_BLOB
         and hashlib.sha256(wraw).hexdigest()==WITNESS_SHA,
         'V3 protected source blob or witness digest drift')
    need((receipt.get('protected_evidence') or {})=={'path':DOSSIER_PATH,'blob_sha':DOSSIER_BLOB}
         and (receipt.get('platform_witness') or {})=={'path':WITNESS_PATH,
             'blob_sha':WITNESS_BLOB,'sha256':WITNESS_SHA,
             'run_id':RUN,'run_attempt':1,'artifact_id':12084032389},
         'V3 receipt does not bind exact source witness and run')
    need(dossier.get('record_type')=='GCL_AGENT_PLATFORM_ORIGIN_DOSSIER_V3'
         and dossier.get('subject')==witness.get('source')
         and dossier.get('subject')==dict(subject,pr_number=2710)
         and (dossier.get('platform_execution') or {}).get('protected_witness')==
           {'path':WITNESS_PATH,'sha256':WITNESS_SHA,'git_blob_sha':WITNESS_BLOB},
         'V3 source subject or bytes not recognized')
    required_limits={'later_independent_platform_execution_verified':True,
                     'historical_2026_10_15_chad_execution_authenticated':False,
                     'independent_specialist_persons_certified':False,
                     'cryptographic_hardware_attestation':False,
                     'mathematical_certification':False,
                     'gcl_wide_assurance_certified':False}
    need(receipt.get('claims')==required_limits and dossier.get('claims')==required_limits,
         'V3 origin falsely promotes historical or scientific claims')
    need(isinstance(downloaded_artifact,bytes) and downloaded_artifact==wraw,
         'original independently downloaded Actions artifact differs from INTELLECT protected witness')
    need(witness.get('run_id')==RUN and witness.get('run_attempt')==1,
         'unexpected protected execution run')
    try:
        result=verify_witness(api_get=api_get,witness=witness,run_id=RUN)
    except (OriginError,ValueError,KeyError,TypeError) as error:
        raise V3OriginError('authenticated GitHub-hosted origin verification failed') from error
    need(result['artifact_id']==12084032389
         and result['trusted_workflow_head']=='80f3b83d94795dba2acceef05f66b386ac6f735d'
         and result['roles_verified']==['VERIFIER','ADVERSARY','REFEREE'],
         'authenticated runner artifact/workflow/role identity drift')
    again=api_get(f'/repos/{ORIGIN}/branches/main')
    need((again.get('commit') or {}).get('sha')==protected and again.get('protected') is True,
         'protected INTELLECT main drift during V3 verification')
    return {'status':'V3_PROTECTED_PLATFORM_EXECUTION_ORIGIN_CORROBORATED',
            'subject':subject,'source_reviewers':source_reviewers,
            'receipt_reviewers':receipt_reviewers,'protected_intellect_main':protected,
            'origin_run_id':RUN,'origin_artifact_id':12084032389,
            'original_chad_execution_attested':False,
            'separate_specialist_persons_certified':False,
            'mathematical_certification':False,'gcl_wide_assurance_certified':False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--receipt-pr',required=True,type=int,
        help='Actual separately merged, independently approved INTELLECT receipt PR')
    args=parser.parse_args()
    run=gh_api(f'/repos/grandchallenge/MATH-PROGRAMME/actions/runs/{RUN}')
    attempt=run.get('run_attempt')
    need(type(attempt) is int and attempt>0,'missing real platform run attempt')
    name=f'paar-c-origin-{RUN}-{attempt}'
    with tempfile.TemporaryDirectory(prefix='gcl-v3-origin-') as tmp:
        subprocess.run(['gh','run','download',str(RUN),
                        '-R','grandchallenge/MATH-PROGRAMME',
                        '-n',name,'-D',tmp],check=True,text=True,capture_output=True,timeout=90)
        path=Path(tmp)/'witness.json'
        need(path.is_file(),'GitHub artifact download missing witness.json')
        result=verify_v3(api_get=gh_api,downloaded_artifact=path.read_bytes(),
                         receipt_pr_number=args.receipt_pr)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
