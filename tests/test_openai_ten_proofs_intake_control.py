from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "openai_ten_proofs_intake_control",
    ROOT / "ci" / "openai_ten_proofs_intake_control.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OpenAITenProofsIntakeControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(MODULE.RECORD_PATH.read_text(encoding="utf-8"))
        self.document = MODULE.DOCUMENT_PATH.read_text(encoding="utf-8")

    def errors(self, record=None, document=None):
        return MODULE.validation_errors(
            record=copy.deepcopy(self.record if record is None else record),
            document=self.document if document is None else document,
        )

    def test_current_intake_control_passes(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_each_external_subject_identity_is_pinned(self) -> None:
        mutations = {
            "repository": "example/ten-proofs",
            "commit": "0" * 40,
            "tree": "1" * 40,
            "archive_sha256": "2" * 64,
            "root_commit": False,
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record["external_subject"][field] = value
                self.assertTrue(any("external subject identity drift" in e for e in self.errors(record)))

    def test_forge_reviewed_head_and_merge_are_pinned(self) -> None:
        for field in ("reviewed_head_commit", "merge_commit"):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record["forge_provider_authority"][field] = "0" * 40
                expected = f"Forge authority drift in {field}"
                self.assertTrue(any(expected in e for e in self.errors(record)))

    def test_every_forge_artifact_path_and_blob_is_pinned(self) -> None:
        for artifact_id in MODULE.EXPECTED_FORGE_ARTIFACTS:
            for field, value in (("path", "wrong/path.json"), ("git_blob_sha1", "0" * 40)):
                with self.subTest(artifact_id=artifact_id, field=field):
                    record = copy.deepcopy(self.record)
                    record["forge_provider_authority"]["artifacts"][artifact_id][field] = value
                    expected = f"Forge artifact identity drift in {artifact_id}"
                    self.assertTrue(any(expected in e for e in self.errors(record)))

    def test_result_family_identity_and_order_are_closed(self) -> None:
        record = copy.deepcopy(self.record)
        record["result_families"].reverse()
        self.assertTrue(any("result-family identity or order drift" in e for e in self.errors(record)))

    def test_no_gate_can_be_inflated_or_rolled_back(self) -> None:
        mutations = {
            "source_identity": ("not_verified", False),
            "kernel_correctness": ("provider_verified", True),
            "statement_fidelity": ("provider_verified", True),
            "independent_adjudication": ("performed", True),
        }
        for gate_id, (state, satisfied) in mutations.items():
            with self.subTest(gate_id=gate_id):
                record = copy.deepcopy(self.record)
                gate = record["gate_matrix"][gate_id]
                gate["state"] = state
                gate["satisfied_for_admission"] = satisfied
                expected = f"gate disposition drift in {gate_id}"
                self.assertTrue(any(expected in e for e in self.errors(record)))

    def test_route_prohibitions_and_granularity_are_closed(self) -> None:
        mutations = {
            "may_emit_solve_handoff": True,
            "may_adjudicate": True,
            "may_promote_result": True,
            "aggregate_admission_prohibited": False,
            "admission_granularity": "aggregate",
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record["route_state"][field] = value
                self.assertTrue(any("route prohibition or granularity drift" in e for e in self.errors(record)))

    def test_candidate_cannot_enter_active_portfolio(self) -> None:
        record = copy.deepcopy(self.record)
        record["active_campaign_member"] = True
        self.assertTrue(any("candidate entered active portfolio" in e for e in self.errors(record)))

    def test_candidate_lifecycle_is_pinned(self) -> None:
        record = copy.deepcopy(self.record)
        record["lifecycle_state"] = "admitted_active"
        self.assertTrue(any("candidate lifecycle drift" in e for e in self.errors(record)))

    def test_linked_trackers_are_pinned(self) -> None:
        record = copy.deepcopy(self.record)
        record["linked_trackers"]["mathsolve"] = "https://github.com/grandchallenge/MATHSOLVE/issues/1"
        self.assertTrue(any("linked tracker identity drift" in e for e in self.errors(record)))

    def test_claim_boundary_cannot_be_weakened(self) -> None:
        record = copy.deepcopy(self.record)
        record["claim_boundary"] = "This record admits and certifies the candidate." * 3
        self.assertTrue(any("claim boundary weakened" in e for e in self.errors(record)))

    def test_companion_document_preserves_evidence_tokens(self) -> None:
        for token in MODULE.DOCUMENT_REQUIRED_TOKENS:
            with self.subTest(token=token):
                document = self.document.replace(token, "REMOVED", 1)
                expected = f"missing preserved token {token}"
                self.assertTrue(any(expected in e for e in self.errors(document=document)))

    def test_schema_rejects_unexpected_nested_fields(self) -> None:
        record = copy.deepcopy(self.record)
        record["forge_provider_authority"]["artifacts"]["source_lock"]["mutable_ref"] = "main"
        self.assertTrue(any("Additional properties are not allowed" in e for e in self.errors(record)))


if __name__ == "__main__":
    unittest.main()
