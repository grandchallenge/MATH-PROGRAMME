import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "ci" / "erdos_41_queue_bridge.py"
spec=importlib.util.spec_from_file_location("erdos_41_queue_bridge",SCRIPT)
bridge=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

class BridgeTests(unittest.TestCase):
    def sample(self):
        return {"schema":"GCL-ERDOS-041-DETERMINISTIC-REPLAY/1",
                "issue":2536,"problem_id":41,"status":"PASS_FINITE_SEMANTIC_DIFFERENCE_ONLY",
                "multisets_with_sum_five":[[1,1,3],[1,2,2]],
                "authority_effects":dict.fromkeys(("source_acceptance","solve_dispatch","mathcert_certification","publication"),False)}
    def test_valid_replay(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"evidence.json";path.write_text(json.dumps(self.sample()))
            digest,data=bridge.validate(path)
            self.assertEqual(len(digest),64)
    def test_authority_escalation_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"evidence.json"
            data=self.sample();data["authority_effects"]["publication"]=True
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError): bridge.validate(path)
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

if __name__=="__main__":unittest.main()
