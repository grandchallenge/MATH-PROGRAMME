import json
import tempfile
import unittest
from pathlib import Path
from ci.erdos_41_colab_handoff import write_handoff

class ColabHandoffTests(unittest.TestCase):
    def make(self,folder):
        (folder/"task.json").write_text(json.dumps({"problem_id":41,"review_issue":2536,"source_comment_sha256":"a"*64}))
        (folder/"job.json").write_text("{}")
        (folder/"erdos_review_result.json").write_text(json.dumps({"review_issue":2536,"source_comment_sha256":"a"*64}))
        (folder/"erdos_review_receipt.json").write_text("{}")
        return {"state":"GREEN_ENGINEERING_UNADJUDICATED","subject":"ERDOS-024-41",
                "backend":"witness_only","role_pass_count":0,"result_sha256":"b"*64,
                "authority_effects":{"publication":False,"certification":False}}
    def test_handoff_is_write_once_and_source_bound(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp); verified=self.make(folder)
            result=write_handoff(folder,verified)
            self.assertEqual(len(result["handoff_sha256"]),64)
            self.assertEqual(json.loads(Path(result["handoff"]).read_text())["issue"],2536)
            with self.assertRaises(FileExistsError):
                write_handoff(folder,verified)
    def test_no_claim_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp); verified=self.make(folder)
            verified["authority_effects"]["publication"]=True
            with self.assertRaises(ValueError): write_handoff(folder,verified)
    def test_no_model_review_impersonation(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp); verified=self.make(folder)
            verified["role_pass_count"]=2
            with self.assertRaises(ValueError): write_handoff(folder,verified)
    def test_source_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp); verified=self.make(folder)
            (folder/"erdos_review_result.json").write_text(json.dumps({"review_issue":2536,"source_comment_sha256":"c"*64}))
            with self.assertRaises(ValueError): write_handoff(folder,verified)
if __name__=="__main__": unittest.main()
