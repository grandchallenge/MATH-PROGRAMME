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

    def test_ownership_collapse(self):
        record = copy.deepcopy(self.record)
        record["ownership"]["programme"] = "certification_output_authority"
        self.assertTrue(self.errors(record=record))

    def test_current_root_drift(self):
        record = copy.deepcopy(self.record)
        record["formal_source_authority"]["current_root_for_unresolved_families"] = "0" * 40
        self.assertTrue(self.errors(record=record))

    def test_j1_qualification_removal(self):
        record = copy.deepcopy(self.record)
        record["cert_authority"]["qualified_restricted_surfaces"][1]["certificate_blob"] = "0" * 40
        self.assertTrue(self.errors(record=record))

    def test_j2_disposition_inflation(self):
        record = copy.deepcopy(self.record)
        record["cert_authority"]["qualified_restricted_surfaces"][2]["disposition"] = "qualified_unrestricted_theorem"
        self.assertTrue(self.errors(record=record))

    def test_aggregate_output_inflation(self):
        record = copy.deepcopy(self.record)
        record["cert_authority"]["aggregate_output_count"] = 1
        self.assertTrue(self.errors(record=record))

    def test_proof_promotion(self):
        record = copy.deepcopy(self.record)
        record["cert_authority"]["mathematical_targets_marked_proved"] = 1
        self.assertTrue(self.errors(record=record))

    def test_permanent_full_formula_route_inflation(self):
        record = copy.deepcopy(self.record)
        record["permanent_successor_surfaces"][0]["cert_route_state"] = "qualified"
        self.assertTrue(self.errors(record=record))

    def test_permanent_circuit_route_inflation(self):
        record = copy.deepcopy(self.record)
        record["permanent_successor_surfaces"][1]["cert_route_state"] = "submitted"
        self.assertTrue(self.errors(record=record))

    def test_gapcvp_removed_from_queue(self):
        record = copy.deepcopy(self.record)
        record["unresolved_family_queue"] = [x for x in record["unresolved_family_queue"] if x["family"] != "OTP-H-GAPCVP"]
        self.assertTrue(self.errors(record=record))

    def test_sphere_promoted_clear(self):
        record = copy.deepcopy(self.record)
        record["unresolved_family_queue"][0]["state"] = "semantic_and_nonvacuity_clear"
        self.assertTrue(self.errors(record=record))

    def test_execution_order_drift(self):
        record = copy.deepcopy(self.record)
        record["execution_order"][1], record["execution_order"][2] = record["execution_order"][2], record["execution_order"][1]
        self.assertTrue(self.errors(record=record))

    def test_whole_document_equivalence_inflation(self):
        record = copy.deepcopy(self.record)
        record["preserved_limitations"]["whole_document_semantic_equivalence"] = "established"
        self.assertTrue(self.errors(record=record))

    def test_open_schema(self):
        schema = copy.deepcopy(self.schema)
        schema["additionalProperties"] = True
        self.assertTrue(self.errors(schema=schema))

    def test_unexpected_authority_field(self):
        record = copy.deepcopy(self.record)
        record["aggregate_certification"] = True
        self.assertTrue(self.errors(record=record))


if __name__ == "__main__":
    unittest.main()
