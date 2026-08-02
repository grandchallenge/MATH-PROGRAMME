#!/usr/bin/env python3
"""Adversarial tests for the bounded GCL synthesis pilot."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "ci"
if str(CI) not in sys.path:
    sys.path.insert(0, str(CI))

from render_synthesis import render_report, render_review_packet  # noqa: E402
from validate_synthesis import validate  # noqa: E402


class SynthesisPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads((ROOT / "synthesis" / "pilot_registry.json").read_text(encoding="utf-8"))
        self.schema = json.loads((ROOT / "schemas" / "gcl_synthesis_registry.schema.json").read_text(encoding="utf-8"))

    def errors_for(self, registry: dict, *, report: str | None = None, review: str | None = None) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            registry_path = base / "registry.json"
            schema_path = base / "schema.json"
            report_path = base / "report.md"
            review_path = base / "review.md"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            schema_path.write_text(json.dumps(self.schema), encoding="utf-8")
            try:
                report_text = render_report(registry) if report is None else report
                review_text = render_review_packet(registry) if review is None else review
            except (KeyError, TypeError, ValueError):
                report_text = render_report(self.registry)
                review_text = render_review_packet(self.registry)
            report_path.write_text(report_text, encoding="utf-8")
            review_path.write_text(review_text, encoding="utf-8")
            return validate(registry_path, schema_path, report_path, review_path)

    def test_valid_registry(self) -> None:
        self.assertEqual([], validate())

    def test_schema_is_closed(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["analogy_confidence"] = 5
        self.assertTrue(any("Additional properties" in e for e in self.errors_for(mutated)))

    def test_source_membership_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["source_artifacts"].pop()
        self.assertTrue(any("too short" in e or "exact four" in e for e in self.errors_for(mutated)))

    def test_mutable_source_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["source_artifacts"][0]["authority_class"] = "mutable_issue_or_discussion_mirror"
        self.assertTrue(any("protected_normative_record" in e or "mutable" in e for e in self.errors_for(mutated)))

    def test_source_blob_drift_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["source_artifacts"][0]["git_blob_sha1"] = "a" * 40
        self.assertTrue(any("blob identity mismatch" in e for e in self.errors_for(mutated)))

    def test_assumption_loss_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["target_assumptions"] = []
        self.assertTrue(any("too short" in e or "assumptions" in e for e in self.errors_for(mutated)))

    def test_non_transferability_required(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][1]["non_transferable_component"] = ""
        self.assertTrue(any("too short" in e or "non-transferability" in e for e in self.errors_for(mutated)))

    def test_accepted_transfer_requires_consequence(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["bounded_executable_consequence"] = None
        self.assertTrue(any("accepted transfer requires" in e for e in self.errors_for(mutated)))

    def test_rejected_analogy_cannot_execute(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][3]["bounded_executable_consequence"] = "Open a new implementation route."
        self.assertTrue(any("cannot retain executable authority" in e for e in self.errors_for(mutated)))

    def test_rejected_analogy_requires_reason(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][3]["rejection_reason"] = None
        self.assertTrue(any("requires a rejection reason" in e for e in self.errors_for(mutated)))

    def test_analogy_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][3]["analysis_disposition"] = "accepted_bounded"
        mutated["transfer_records"][3]["bounded_executable_consequence"] = "Transfer the obstruction."
        mutated["transfer_records"][3]["rejection_reason"] = None
        self.assertTrue(any("membership or dispositions drifted" in e for e in self.errors_for(mutated)))

    def test_unknown_source_ref_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["source_ref"] = "SRC-UNKNOWN"
        self.assertTrue(any("unknown source_ref" in e for e in self.errors_for(mutated)))

    def test_source_must_appear_in_evidence_links(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["evidence_links"] = ["SRC-PORTFOLIO"]
        self.assertTrue(any("evidence_links must include source_ref" in e for e in self.errors_for(mutated)))

    def test_duplicate_relabeling_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][1]["target"] = copy.deepcopy(mutated["transfer_records"][0]["target"])
        self.assertTrue(any("duplicate relabeling" in e for e in self.errors_for(mutated)))

    def test_automated_disposition_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["governance"]["automated"] = True
        self.assertTrue(any("False was expected" in e or "automated" in e for e in self.errors_for(mutated)))

    def test_claim_widening_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["transfer_records"][0]["claim_boundaries"]["source_target_equivalence_established"] = True
        self.assertTrue(any("False was expected" in e or "claim-boundary" in e for e in self.errors_for(mutated)))

    def test_contradiction_erasure_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["contradiction_records"][0]["disposition"] = "distinct_responsibilities"
        self.assertTrue(any("membership or dispositions drifted" in e or "contradiction must remain preserved" in e for e in self.errors_for(mutated)))

    def test_duplication_must_reuse_or_separate(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["contradiction_records"][2]["kind"] = "contradiction"
        self.assertTrue(any("contradiction must remain preserved" in e for e in self.errors_for(mutated)))

    def test_review_packet_exact_offices(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["review_packet"][0]["office"] = "Referee"
        self.assertTrue(any("exact eight offices" in e for e in self.errors_for(mutated)))

    def test_review_packet_cannot_self_authenticate(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["review_packet"][0]["may_self_authenticate"] = True
        self.assertTrue(any("False was expected" in e or "cannot self-authenticate" in e for e in self.errors_for(mutated)))

    def test_generated_report_drift_rejected(self) -> None:
        self.assertTrue(any("generated synthesis report" in e for e in self.errors_for(self.registry, report="# stale\n")))

    def test_generated_review_drift_rejected(self) -> None:
        self.assertTrue(any("generated synthesis review packet" in e for e in self.errors_for(self.registry, review="# stale\n")))


if __name__ == "__main__":
    unittest.main()
