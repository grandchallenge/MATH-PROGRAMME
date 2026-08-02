from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "openai_ten_proofs_cert_state_sync",
    ROOT / "governance/validators/openai_ten_proofs_cert_state_sync.py",
)
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class OpenAITenProofsCertStateSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = M.load(M.RECORD)
        self.schema = M.load(M.SCHEMA)

    def errors(self, *, record=None, schema=None, historical_overlay_blob=None):
        return M.validation_errors(
            record=copy.deepcopy(self.record if record is None else record),
            schema=copy.deepcopy(self.schema if schema is None else schema),
            historical_overlay_blob=(
                M.EXPECTED_HISTORICAL_OVERLAY_BLOB
                if historical_overlay_blob is None
                else historical_overlay_blob
            ),
        )

    def test_baseline(self):
        self.assertEqual([], self.errors())

    def test_historical_overlay_drift(self):
        self.assertTrue(self.errors(historical_overlay_blob="0" * 40))

    def test_ownership_collapse(self):
        record = copy.deepcopy(self.record)
        record["ownership"]["forge"] = "route_adjudication_and_output"
        self.assertTrue(self.errors(record=record))

    def test_forge_semantic_blob_drift(self):
        record = copy.deepcopy(self.record)
        record["forge_authority"]["semantic_records"][0]["git_blob_sha1"] = "0" * 40
        self.assertTrue(self.errors(record=record))

    def test_solve_packet_blob_drift(self):
        record = copy.deepcopy(self.record)
        record["solve_authority"]["producer_packets"][1]["git_blob_sha1"] = "0" * 40
        self.assertTrue(self.errors(record=record))

    def test_cert_closure_merge_drift(self):
        record = copy.deepcopy(self.record)
        record["cert_authority"]["ehrhart_documentary_closure_merge"] = "0" * 40
        self.assertTrue(self.errors(record=record))

    def test_cert_certificate_blob_drift(self):
        record = copy.deepcopy(self.record)
        record["cert_authority"]["ehrhart_certificate_blob"] = "0" * 40
        self.assertTrue(self.errors(record=record))

    def test_compactness_qualification_inflation(self):
        record = copy.deepcopy(self.record)
        record["result_family_state"][1]["cert_route_state"] = "qualified"
        self.assertTrue(self.errors(record=record))

    def test_aggregate_output_inflation(self):
        record = copy.deepcopy(self.record)
        record["tranche_totals"]["aggregate_output_count"] = 1
        self.assertTrue(self.errors(record=record))

    def test_proof_promotion(self):
        record = copy.deepcopy(self.record)
        record["tranche_totals"]["mathematical_targets_marked_proved"] = 1
        self.assertTrue(self.errors(record=record))

    def test_blocker_removal(self):
        record = copy.deepcopy(self.record)
        record["remaining_state"]["blocked_repair_lanes"] = []
        self.assertTrue(self.errors(record=record))

    def test_next_obligation_drift(self):
        record = copy.deepcopy(self.record)
        record["next_controlled_obligation"] = "OTP-J2-TWO-DEGENERATE-CERT-EVIDENCE-REFRESH-001"
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
