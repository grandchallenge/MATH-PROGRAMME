from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "openai_ten_proofs_umbrella_sync",
    ROOT / "ci" / "openai_ten_proofs_umbrella_sync.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OpenAITenProofsUmbrellaSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(MODULE.RECORD_PATH.read_text(encoding="utf-8"))
        self.document = MODULE.DOCUMENT_PATH.read_text(encoding="utf-8")

    def errors(self, record=None, document=None):
        return MODULE.validation_errors(
            record=copy.deepcopy(self.record if record is None else record),
            document=self.document if document is None else document,
        )

    def test_current_sync_passes(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_official_root_cannot_revert_to_disconnected_root(self) -> None:
        record = copy.deepcopy(self.record)
        record["source_identity"]["current_official"]["commit"] = record["source_identity"]["historical_disconnected"]["commit"]
        self.assertTrue(self.errors(record))

    def test_each_forge_artifact_blob_is_pinned(self) -> None:
        for artifact in record_artifacts(self.record):
            with self.subTest(artifact=artifact):
                record = copy.deepcopy(self.record)
                record["authority"]["forge_artifacts"][artifact]["git_blob_sha1"] = "0" * 40
                self.assertTrue(self.errors(record))

    def test_replay_counts_cannot_be_inflated_or_rolled_back(self) -> None:
        for field, value in (
            ("kernel_clear_count", 11),
            ("comparator_pass_count", 11),
            ("required_nanoda_accept_count", 8),
            ("theorem_axiom_report_count", 40),
        ):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record["trusted_replay"][field] = value
                self.assertTrue(self.errors(record))

    def test_all_import_failure_cannot_reopen_kernel_gate(self) -> None:
        record = copy.deepcopy(self.record)
        record["aggregate_integration"]["reopens_kernel_gate"] = True
        self.assertTrue(self.errors(record))

    def test_semantic_zero_forbids_all_routes(self) -> None:
        for field in ("may_emit_result_family_handoff", "may_emit_aggregate_handoff", "may_adjudicate", "may_promote_result"):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record["route_state"][field] = True
                self.assertTrue(self.errors(record))

    def test_cert_output_must_remain_null(self) -> None:
        record = copy.deepcopy(self.record)
        record["route_state"]["cert_output"] = {"disposition": "certified"}
        self.assertTrue(self.errors(record))

    def test_review_remedy_identity_is_closed(self) -> None:
        record = copy.deepcopy(self.record)
        record["authority"]["review_remedy"]["merge_commit_sha"] = "0" * 40
        self.assertTrue(self.errors(record))

    def test_claim_boundary_cannot_be_weakened(self) -> None:
        record = copy.deepcopy(self.record)
        record["claim_boundary"] = "This record certifies all ten proofs." * 12
        self.assertTrue(self.errors(record))

    def test_document_tokens_are_preserved(self) -> None:
        for token in ("12/12", "0/12", "All.lean", "No aggregate certification"):
            with self.subTest(token=token):
                self.assertTrue(self.errors(document=self.document.replace(token, "REMOVED", 1)))


def record_artifacts(record):
    return tuple(record["authority"]["forge_artifacts"].keys())


if __name__ == "__main__":
    unittest.main()
