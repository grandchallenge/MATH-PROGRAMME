import unittest
import sys
from pathlib import Path
from unittest.mock import patch
import hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ci'))
from paar_original_origin_forensics import EvidenceError, classify, DOSSIER_BLOB, SUBJECT

class OriginalOriginTests(unittest.TestCase):
    def setUp(self):
        self.raw={r:('synthetic-'+r).encode() for r in ('VERIFIER','ADVERSARY','REFEREE')}
        self.expected={r:(r.lower()+'.stderr',hashlib.sha256(v).hexdigest()) for r,v in self.raw.items()}
        self.outputs={self.expected[r][0]:v for r,v in self.raw.items()}
        self.dossier={'record_type':'GCL_AGENT_REVIEW_DOSSIER_V1','subject':{'head_sha':SUBJECT},'passes':[{'role':r,'checks':[{'exit_code':0,'receipt_sha256':x[1]}]} for r,x in self.expected.items()]}
        self.console={'entries_with_embedded_receipt':0}
        self.receipts={'command_bound_receipts':0}
    def inspect(self,reviews=None):
        with patch('paar_original_origin_forensics.EXPECTED',self.expected):
            return classify(self.dossier,self.outputs,DOSSIER_BLOB,self.console,self.receipts,reviews or [])
    def test_hash_match_is_not_execution_attestation(self):
        x=self.inspect()
        self.assertFalse(x['original_command_execution_authenticated'])
        self.assertFalse(x['independent_reviewer_system_authenticated'])
    def test_output_mutation_rejected(self):
        self.outputs['verifier.stderr']+=b'changed'
        with self.assertRaises(EvidenceError):self.inspect()
    def test_changed_role_rejected(self):
        self.dossier['passes'][0]['role']='REFEREE'
        with self.assertRaises(EvidenceError):self.inspect()
    def test_missing_output_rejected(self):
        self.outputs.pop('referee.stderr')
        with self.assertRaises(EvidenceError):self.inspect()
    def test_changed_claimed_hash_rejected(self):
        self.dossier['passes'][0]['checks'][0]['receipt_sha256']='0'*64
        with self.assertRaises(EvidenceError):self.inspect()
    def test_new_console_receipt_requires_reinspection(self):
        self.console['entries_with_embedded_receipt']=1
        with self.assertRaises(EvidenceError):self.inspect()
    def test_new_commander_record_requires_reinspection(self):
        self.receipts['command_bound_receipts']=1
        with self.assertRaises(EvidenceError):self.inspect()
    def test_native_review_does_not_prove_command_origin(self):
        x=self.inspect([{'state':'APPROVED'}])
        self.assertEqual(x['historical_native_source_approving_reviews'],1)
        self.assertFalse(x['original_command_execution_authenticated'])

if __name__=='__main__':unittest.main()
