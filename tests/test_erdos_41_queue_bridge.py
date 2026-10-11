import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/"ci"/"erdos_41_queue_bridge.py"
spec=importlib.util.spec_from_file_location("erdos_41_queue_bridge",SCRIPT)
bridge=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

class BridgeTests(unittest.TestCase):
    def sample(self):
        return {"schema":"GCL-ERDOS-041-DETERMINISTIC-REPLAY/1",
            "issue":2536,"problem_id":41,"status":"PASS_FINITE_SEMANTIC_DIFFERENCE_ONLY",
            "cohort":"ERDOS-ROLLING-024-001","roster_sha256":"a"*64,
            "source_provider_commit":bridge.PROVIDER_COMMIT,
            "source_provider_git_blob_sha1":bridge.SOURCE_BLOB,
            "worker_result_comment_id":6104193801,
            "finite_set":[1,2,3],"three_element_subsets":[[1,2,3]],
            "multisets_with_sum_five":[[1,1,3],[1,2,2]],
            "authority_effects":{k:False for k in bridge.AUTHORITY_KEYS}}
    def check(self,data):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"evidence.json";path.write_text(json.dumps(data))
            return bridge.validate(path)
    def test_valid_replay(self):
        digest,_=self.check(self.sample())
        self.assertEqual(len(digest),64)
    def test_authority_escalation_rejected(self):
        data=self.sample();data["authority_effects"]["publication"]=True
        with self.assertRaisesRegex(ValueError,"authority"):
            self.check(data)
    def test_source_drift_rejected(self):
        data=self.sample();data["source_provider_git_blob_sha1"]="f"*40
        with self.assertRaisesRegex(ValueError,"provenance"):
            self.check(data)
    def test_missing_witness_rejected(self):
        data=self.sample();data["multisets_with_sum_five"]=[]
        with self.assertRaisesRegex(ValueError,"witness"):
            self.check(data)
    def test_live_queue_field_mandatory(self):
        issue={"state":"open","labels":[{"name":x} for x in bridge.LABELS]}
        with patch.object(bridge,"github",side_effect=[issue,[],[]]):
            with self.assertRaisesRegex(RuntimeError,"Issue Field"):
                bridge.preflight()
    def test_prior_candidate_blocks_duplicate(self):
        issue={"state":"open","labels":[{"name":x} for x in bridge.LABELS]}
        fields=[{"issue_field_name":"GCL State","single_select_option":{"name":"AVAILABLE"}}]
        comments=[{"body":"GCL-FORGE-CRITIQUE-CANDIDATE/1\nSTATUS: UNADJUDICATED"}]
        with patch.object(bridge,"github",side_effect=[issue,fields,comments]):
            with self.assertRaisesRegex(RuntimeError,"already submitted"):
                bridge.preflight()
    def test_no_write_api(self):
        self.assertFalse(hasattr(bridge,"publish"))
        self.assertFalse(hasattr(bridge,"post"))

if __name__=="__main__":unittest.main()
