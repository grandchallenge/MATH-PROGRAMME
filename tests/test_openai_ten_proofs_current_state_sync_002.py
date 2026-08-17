from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "openai_ten_proofs_current_state_sync_002",
    ROOT / "governance/validators/openai_ten_proofs_current_state_sync_002.py",
)
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class OpenAITenProofsCurrentStateSync002Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = M.load(M.RECORD)
        self.schema = M.load(M.SCHEMA)

    def errors(self, *, record=None, schema=None, predecessor_blob=None, umbrella_blob=None):
        return M.validation_errors(
            record=copy.deepcopy(self.record if record is None else record),
            schema=copy.deepcopy(self.schema if schema is None else schema),
            predecessor_blob=M.EXPECTED_PREDECESSOR_BLOB if predecessor_blob is None else predecessor_blob,
            umbrella_blob=M.EXPECTED_UMBRELLA_BLOB if umbrella_blob is None else umbrella_blob,
        )

    def test_baseline(self):
        self.assertEqual([], self.errors())

    def test_predecessor_record_drift(self):
        self.assertTrue(self.errors(predecessor_blob="0" * 40))

    def test_historical_umbrella_drift(self):
        self.assertTrue(self.errors(umbrella_blob="0" * 40))

    def test_forge_main_drift(self):
        r = copy.deepcopy(self.record)
        r["protected_heads"]["forge_main"] = "0" * 40
        self.assertTrue(self.errors(record=r))

    def test_source_successor_cannot_collapse_into_current_forge_main(self):
        r = copy.deepcopy(self.record)
        r["formal_source_authority"]["protected_successor_merge"] = r["protected_heads"]["forge_main"]
        self.assertTrue(self.errors(record=r))

    def test_current_root_drift(self):
        r = copy.deepcopy(self.record)
        r["formal_source_authority"]["current_root_for_unresolved_families"] = "0" * 40
        self.assertTrue(self.errors(record=r))

    def test_unresolved_count_inflation(self):
        r = copy.deepcopy(self.record)
        r["formal_source_authority"]["unresolved_family_count"] = 8
        self.assertTrue(self.errors(record=r))

    def test_sphere_completion_merge_drift(self):
        r = copy.deepcopy(self.record)
        r["current_root_completed_families"][0]["forge_merge"] = "0" * 40
        self.assertTrue(self.errors(record=r))

    def test_gap_completion_blob_drift(self):
        r = copy.deepcopy(self.record)
        r["current_root_completed_families"][1]["audit_record_blob"] = "0" * 40
        self.assertTrue(self.errors(record=r))

    def test_completion_cannot_authorize_solve(self):
        r = copy.deepcopy(self.record)
        r["current_root_completed_families"][0]["solve_handoff_authorized"] = True
        self.assertTrue(self.errors(record=r))

    def test_completion_cannot_authorize_cert(self):
        r = copy.deepcopy(self.record)
        r["current_root_completed_families"][1]["mathcert_route_authorized"] = True
        self.assertTrue(self.errors(record=r))

    def test_completed_sphere_cannot_reenter_queue(self):
        r = copy.deepcopy(self.record)
        r["unresolved_family_queue"][0] = {
            "family": "OTP-A-SPHERE-PACKING",
            "state": "queued_current_root_semantic_audit",
        }
        self.assertTrue(self.errors(record=r))

    def test_binary_codes_frontier_cannot_be_reordered(self):
        r = copy.deepcopy(self.record)
        r["execution_order"][0], r["execution_order"][1] = r["execution_order"][1], r["execution_order"][0]
        self.assertTrue(self.errors(record=r))

    def test_b2_drift_cannot_be_erased(self):
        r = copy.deepcopy(self.record)
        r["unresolved_family_queue"][1]["state"] = "queued_current_root_semantic_audit"
        self.assertTrue(self.errors(record=r))

    def test_connes_identity_drift_cannot_be_erased(self):
        r = copy.deepcopy(self.record)
        r["unresolved_family_queue"][-1]["state"] = "queued_current_root_semantic_audit"
        self.assertTrue(self.errors(record=r))

    def test_j2_disposition_inflation(self):
        r = copy.deepcopy(self.record)
        r["cert_authority"]["qualified_restricted_surfaces"][2]["disposition"] = "qualified_unrestricted_theorem"
        self.assertTrue(self.errors(record=r))

    def test_aggregate_output_inflation(self):
        r = copy.deepcopy(self.record)
        r["cert_authority"]["aggregate_output_count"] = 1
        self.assertTrue(self.errors(record=r))

    def test_proof_promotion(self):
        r = copy.deepcopy(self.record)
        r["cert_authority"]["mathematical_targets_marked_proved"] = 1
        self.assertTrue(self.errors(record=r))

    def test_permanent_route_inflation(self):
        r = copy.deepcopy(self.record)
        r["permanent_successor_surfaces"][0]["cert_route_state"] = "qualified"
        self.assertTrue(self.errors(record=r))

    def test_whole_document_equivalence_inflation(self):
        r = copy.deepcopy(self.record)
        r["preserved_limitations"]["whole_document_semantic_equivalence"] = "established"
        self.assertTrue(self.errors(record=r))

    def test_open_schema(self):
        s = copy.deepcopy(self.schema)
        s["additionalProperties"] = True
        self.assertTrue(self.errors(schema=s))

    def test_unexpected_authority_field(self):
        r = copy.deepcopy(self.record)
        r["aggregate_certification"] = True
        self.assertTrue(self.errors(record=r))


if __name__ == "__main__":
    unittest.main()
