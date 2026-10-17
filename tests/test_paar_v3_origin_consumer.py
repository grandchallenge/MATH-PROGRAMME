"""Bounded V3 control tests; source/run positive is mocked, not live admission."""
from __future__ import annotations
import base64
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ci'))
import paar_v3_origin_consumer as v3

RUN_SHA='80f3b83d94795dba2acceef05f66b386ac6f735d'
MAIN_SHA='a'*40
RECEIPT_HEAD='c'*40

def gitblob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def pack(obj):
    raw=(json.dumps(obj,sort_keys=True,indent=2)+'\n').encode()
    return raw,{'type':'file','encoding':'base64','sha':gitblob(raw),
                'content':base64.b64encode(raw).decode()}

class V3OriginConsumerTests(unittest.TestCase):
    def setUp(self):
        subject={'repository':'grandchallenge/MATH-PROGRAMME','head_sha':v3.SUBJECT,
                 'material_sha256':v3.MATERIAL}
        self.witness={'source':dict(subject,pr_number=2710),'run_id':v3.RUN,
                      'run_attempt':1}
        self.wraw,self.wfile=pack(self.witness)
        self.dossier={'record_type':'GCL_AGENT_PLATFORM_ORIGIN_DOSSIER_V3',
            'subject':dict(subject,pr_number=2710),
            'platform_execution':{'protected_witness':{'path':v3.WITNESS_PATH,
                'sha256':hashlib.sha256(self.wraw).hexdigest(),
                'git_blob_sha':gitblob(self.wraw)}}}
        self.draw,self.dfile=pack(self.dossier)
        self.limits={
            'later_independent_platform_execution_verified':True,
            'historical_2026_10_15_chad_execution_authenticated':False,
            'independent_specialist_persons_certified':False,
            'cryptographic_hardware_attestation':False,
            'mathematical_certification':False,
            'gcl_wide_assurance_certified':False}
        self.dossier['claims']=self.limits.copy()
        self.draw,self.dfile=pack(self.dossier)
        self.receipt={'record_type':'GCL_PROTECTED_PLATFORM_ORIGIN_ADMISSION_EVIDENCE_V3',
            'schema_version':'4.0.0','subject':subject,'authority_domain':'PROTECTION',
            'verdict':'PLATFORM_EXECUTION_ORIGIN_CORROBORATED_NOT_HISTORICAL_CHAD',
            'source_review_anchor':{'source_pr_number':127,
                'source_pr_head_sha':v3.SOURCE_HEAD,'dossier_blob_sha':self.dfile['sha']},
            'protected_evidence':{'path':v3.DOSSIER_PATH,'blob_sha':self.dfile['sha']},
            'platform_witness':{'path':v3.WITNESS_PATH,'blob_sha':self.wfile['sha'],
                'sha256':hashlib.sha256(self.wraw).hexdigest(),
                'run_id':v3.RUN,'run_attempt':1,'artifact_id':12084032389},
            'claims':self.limits.copy()}
        self.rraw,self.rfile=pack(self.receipt)
        self.main={'protected':True,'commit':{'sha':MAIN_SHA}}
        self.source_pr={'merged_at':'2026-10-16T23:00:00Z',
            'head':{'sha':v3.SOURCE_HEAD,'repo':{'full_name':v3.ORIGIN}},
            'base':{'ref':'main'},'user':{'login':'fyremael'},'changed_files':5}
        self.receipt_pr={'merged_at':'2026-10-17T00:00:00Z',
            'head':{'sha':RECEIPT_HEAD,'repo':{'full_name':v3.ORIGIN}},
            'base':{'ref':'main'},'user':{'login':'fyremael'},'changed_files':1}
        self.source_files=[{'filename':v3.DOSSIER_PATH,'sha':self.dfile['sha'],'status':'added'},
                           {'filename':v3.WITNESS_PATH,'sha':self.wfile['sha'],'status':'added'}]
        self.source_files.extend({'filename':'governance/agent_execution/GCL-ARC-001/test'+str(i)+'.py',
                                  'sha':str(i+1)*40,'status':'added'} for i in range(3))
        self.receipt_files=[{'filename':v3.RECEIPT_PATH,
                             'sha':self.rfile['sha'],'status':'added'}]
        self.reviews={127:[{'user':{'login':'jimsteeg'},'state':'APPROVED',
                            'commit_id':v3.SOURCE_HEAD,'submitted_at':'2026-10-16T23:00:00Z','id':123}],
                      128:[{'user':{'login':'jimsteeg'},'state':'APPROVED',
                            'commit_id':RECEIPT_HEAD,'submitted_at':'2026-10-17T00:00:00Z','id':124}]}
        self.remote_result={'artifact_id':12084032389,'trusted_workflow_head':RUN_SHA,
                            'roles_verified':['VERIFIER','ADVERSARY','REFEREE']}
    def api(self,path):
        prefix=f'/repos/{v3.ORIGIN}'
        routes={
            prefix+'/branches/main':self.main,
            prefix+'/pulls/127':self.source_pr,
            prefix+'/pulls/128':self.receipt_pr,
            prefix+'/pulls/127/reviews?per_page=100':self.reviews[127],
            prefix+'/pulls/128/reviews?per_page=100':self.reviews[128],
            prefix+'/pulls/127/files?per_page=100':self.source_files,
            prefix+'/pulls/128/files?per_page=100':self.receipt_files,
            prefix+f'/contents/{v3.RECEIPT_PATH}?ref={MAIN_SHA}':self.rfile,
            prefix+f'/contents/{v3.DOSSIER_PATH}?ref={MAIN_SHA}':self.dfile,
            prefix+f'/contents/{v3.WITNESS_PATH}?ref={MAIN_SHA}':self.wfile,
        }
        if path not in routes:raise AssertionError('unexpected API '+path)
        return routes[path]

    def check(self):
        with (patch.object(v3,'DOSSIER_BLOB',self.dfile['sha']),
             patch.object(v3,'WITNESS_BLOB',self.wfile['sha']),
             patch.object(v3,'WITNESS_SHA',hashlib.sha256(self.wraw).hexdigest()),
             patch.object(v3,'verify_witness',return_value=self.remote_result)):
            return v3.verify_v3(api_get=self.api,downloaded_artifact=self.wraw,
                                receipt_pr_number=128)

    def reject(self):
        with self.assertRaises((v3.V3OriginError,ValueError)):
            self.check()

    def test_positive_full_mock_never_attests_chad(self):
        x=self.check()
        self.assertEqual(x['status'],'V3_PROTECTED_PLATFORM_EXECUTION_ORIGIN_CORROBORATED')
        self.assertFalse(x['original_chad_execution_attested'])
        self.assertEqual(x['source_reviewers'],['jimsteeg'])
        self.assertEqual(x['receipt_reviewers'],['jimsteeg'])

    def test_missing_native_source_review_rejected(self):
        self.reviews[127]=[];self.reject()
    def test_missing_native_receipt_review_rejected(self):
        self.reviews[128]=[];self.reject()
    def test_self_approved_receipt_rejected(self):
        self.reviews[128][0]['user']['login']='fyremael';self.reject()
    def test_stale_source_approval_rejected(self):
        self.reviews[127][0]['commit_id']='f'*40;self.reject()
    def test_stale_receipt_approval_rejected(self):
        self.reviews[128][0]['commit_id']='f'*40;self.reject()
    def test_source_not_merged_rejected(self):
        self.source_pr['merged_at']=None;self.reject()
    def test_receipt_not_merged_rejected(self):
        self.receipt_pr['merged_at']=None;self.reject()
    def test_witness_missing_in_original_source_rejected(self):
        self.source_files[1]['sha']='0'*40;self.reject()
    def test_receipt_not_introduced_by_pr_rejected(self):
        self.receipt_files[0]['sha']='0'*40;self.reject()
    def test_forged_downloaded_actions_artifact_rejected(self):
        with (patch.object(v3,'DOSSIER_BLOB',self.dfile['sha']),
             patch.object(v3,'WITNESS_BLOB',self.wfile['sha']),
             patch.object(v3,'WITNESS_SHA',hashlib.sha256(self.wraw).hexdigest()),
             patch.object(v3,'verify_witness',return_value=self.remote_result)):
            with self.assertRaises(v3.V3OriginError):
                v3.verify_v3(api_get=self.api,downloaded_artifact=self.wraw+b'forged',
                             receipt_pr_number=128)
    def test_unprotected_intellect_main_rejected(self):
        self.main['protected']=False;self.reject()
    def test_receipt_claims_original_chad_rejected(self):
        self.receipt['claims']['historical_2026_10_15_chad_execution_authenticated']=True
        self.rraw,self.rfile=pack(self.receipt)
        self.receipt_files[0]['sha']=self.rfile['sha'];self.reject()
    def test_forged_remote_authentication_result_rejected(self):
        self.remote_result['artifact_id']=999;self.reject()

if __name__=='__main__':unittest.main()
