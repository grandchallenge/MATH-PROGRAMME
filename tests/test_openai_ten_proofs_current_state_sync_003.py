from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "governance/validators/openai_ten_proofs_current_state_sync_003.py"
RECORD_PATH = ROOT / "governance/openai_ten_proofs_current_state_sync_003.json"
SCHEMA_PATH = ROOT / "schemas/openai_ten_proofs_current_state_sync_003.schema.json"

spec = importlib.util.spec_from_file_location("otp_sync003", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestOTPSync003(unittest.TestCase):
    def setUp(self):
        self.record = load(RECORD_PATH)
        self.schema = load(SCHEMA_PATH)
        self.historical = dict(validator.EXPECTED_BLOBS)

    def errors(self, record=None, schema=None, historical=None):
        return validator.validation_errors(
            record=self.record if record is None else record,
            schema=self.schema if schema is None else schema,
            historical_blobs=self.historical if historical is None else historical,
        )

    def test_baseline_clear(self):
        self.assertEqual([], self.errors())

    def test_reject_predecessor_rewrite(self):
        hist = dict(self.historical)
        hist["sync002"] = "0" * 40
        self.assertTrue(self.errors(historical=hist))

    def test_reject_programme_activation(self):
        r = copy.deepcopy(self.record)
        r["active_campaign_member"] = True
        self.assertTrue(self.errors(record=r))

    def test_reject_repository_ownership_collapse(self):
        r = copy.deepcopy(self.record)
        r["ownership"]["programme"] = "route_adjudication_disposition_and_output"
        self.assertTrue(self.errors(record=r))

    def test_reject_qualified_surface_inflation(self):
        r = copy.deepcopy(self.record)
        r["cert_authority"]["restricted_qualified_surfaces"].append(copy.deepcopy(r["cert_authority"]["restricted_qualified_surfaces"][0]))
        self.assertTrue(self.errors(record=r))

    def test_reject_mathematical_proof_promotion(self):
        r = copy.deepcopy(self.record)
        r["cert_authority"]["mathematical_targets_marked_proved"] = 1
        self.assertTrue(self.errors(record=r))

    def test_reject_a_output_insertion(self):
        r = copy.deepcopy(self.record)
        r["a_sphere_packing_frontier"]["cert_output"] = {"certificate": "invented"}
        r["a_sphere_packing_frontier"]["may_issue_output"] = True
        self.assertTrue(self.errors(record=r))

    def test_reject_a_route_transition(self):
        r = copy.deepcopy(self.record)
        r["a_sphere_packing_frontier"]["route_state"] = "qualified"
        self.assertTrue(self.errors(record=r))

    def test_reject_h_route_proposal_inference(self):
        r = copy.deepcopy(self.record)
        r["cert_replay_frontier"][0]["next_boundary"] = "route_proposal"
        self.assertTrue(self.errors(record=r))

    def test_reject_b1_work_package_substitution(self):
        r = copy.deepcopy(self.record)
        r["cert_replay_frontier"][1]["work_package_blob"] = "0" * 40
        self.assertTrue(self.errors(record=r))

    def test_reject_b2_family_reordering(self):
        r = copy.deepcopy(self.record)
        r["cert_replay_frontier"][1], r["cert_replay_frontier"][2] = r["cert_replay_frontier"][2], r["cert_replay_frontier"][1]
        self.assertTrue(self.errors(record=r))

    def test_reject_i_solve_authority_inference(self):
        r = copy.deepcopy(self.record)
        r["forge_clear_downstream_pending"][0]["next_boundary"] = "solve_handoff_authorized"
        self.assertTrue(self.errors(record=r))

    def test_reject_forge_audit_substitution(self):
        r = copy.deepcopy(self.record)
        r["forge_clear_downstream_pending"][3]["audit_record_blob"] = "f" * 40
        self.assertTrue(self.errors(record=r))

    def test_reject_aggregate_authority(self):
        r = copy.deepcopy(self.record)
        r["preserved_limitations"]["aggregate_ten_proofs_authority"] = True
        self.assertTrue(self.errors(record=r))

    def test_reject_cross_family_authority_transfer(self):
        r = copy.deepcopy(self.record)
        r["preserved_limitations"]["cross_family_authority_transfer"] = True
        self.assertTrue(self.errors(record=r))

    def test_reject_open_schema(self):
        s = copy.deepcopy(self.schema)
        s["additionalProperties"] = True
        self.assertTrue(self.errors(schema=s))


if __name__ == "__main__":
    unittest.main()
