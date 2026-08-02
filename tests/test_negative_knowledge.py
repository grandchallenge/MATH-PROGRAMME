#!/usr/bin/env python3
"""Adversarial tests for the GCL negative-knowledge registry."""
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

from validate_negative_knowledge import canonical_digest, validate  # noqa: E402


class NegativeKnowledgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(
            (ROOT / "negative_knowledge" / "pilot_registry.json").read_text(
                encoding="utf-8"
            )
        )
        self.schema = json.loads(
            (ROOT / "schemas" / "negative_knowledge_registry.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def write_fixture(
        self,
        registry: dict,
        schema: dict | None = None,
    ) -> tuple[Path, Path, tempfile.TemporaryDirectory]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        registry_path = root / "registry.json"
        schema_path = root / "schema.json"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        schema_path.write_text(json.dumps(schema or self.schema), encoding="utf-8")
        return registry_path, schema_path, temporary

    def errors_for(self, registry: dict) -> list[str]:
        registry_path, schema_path, temporary = self.write_fixture(registry)
        try:
            return validate(registry_path, schema_path)
        finally:
            temporary.cleanup()

    def redigest(self, record: dict) -> None:
        record["scope_digest"] = canonical_digest(record["scope"])
        record["evidence_digest"] = canonical_digest(record["evidence"])

    def test_valid_registry(self) -> None:
        self.assertEqual([], validate())

    def test_schema_is_closed(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["unexpected"] = True
        errors = self.errors_for(mutated)
        self.assertTrue(any("Additional properties" in error for error in errors))

    def test_scope_digest_drift_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["scope"]["assumptions"].append("Unrecorded premise")
        errors = self.errors_for(mutated)
        self.assertTrue(any("scope_digest" in error for error in errors))

    def test_evidence_digest_drift_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["evidence"][0]["commit_sha"] = "0" * 40
        errors = self.errors_for(mutated)
        self.assertTrue(any("evidence_digest" in error for error in errors))

    def test_missing_evidence_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["evidence"] = []
        mutated["records"][0]["evidence_digest"] = canonical_digest([])
        errors = self.errors_for(mutated)
        self.assertTrue(
            any(
                "should be non-empty" in error or "[] is too short" in error
                for error in errors
            )
        )

    def test_scope_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][1]["scope"]["conclusion_strength"] = "exact_scope_only"
        self.redigest(mutated["records"][1])
        errors = self.errors_for(mutated)
        self.assertTrue(any("finite_search_only" in error for error in errors))

    def test_silent_route_resurrection_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["disposition"]["route_state"] = "active"
        errors = self.errors_for(mutated)
        self.assertTrue(any("inactive" in error or "not one of" in error for error in errors))

    def test_missing_reopening_trigger_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["reopening"] = None
        errors = self.errors_for(mutated)
        self.assertTrue(any("structured reopening trigger" in error for error in errors))

    def test_invalid_supersession_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][2]["lineage"]["superseded_by"] = None
        errors = self.errors_for(mutated)
        self.assertTrue(any("superseded_by" in error for error in errors))

    def test_unknown_predecessor_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["lineage"]["predecessor_record_ids"] = [
            "NK-UNKNOWN-001"
        ]
        errors = self.errors_for(mutated)
        self.assertTrue(any("unknown predecessor" in error for error in errors))

    def test_claim_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["claim_boundaries"]["mathematical_target_proved"] = True
        errors = self.errors_for(mutated)
        self.assertTrue(
            any(
                "False was expected" in error or "claim boundary" in error
                for error in errors
            )
        )

    def test_exact_pilot_cardinality_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"].append(copy.deepcopy(mutated["records"][0]))
        mutated["records"][-1]["negative_record_id"] = "NK-EXTRA-001"
        mutated["records"][-1]["scope"]["work_package_id"] = "EXTRA"
        self.redigest(mutated["records"][-1])
        errors = self.errors_for(mutated)
        self.assertTrue(any("too long" in error or "exactly three" in error for error in errors))

    def test_reopening_status_trigger_mismatch_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["reopening"]["trigger_type"] = "new_evidence"
        errors = self.errors_for(mutated)
        self.assertTrue(any("requires new_theorem trigger" in error for error in errors))

    def test_lineage_cycle_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        first = mutated["records"][0]["negative_record_id"]
        second = mutated["records"][1]["negative_record_id"]
        mutated["records"][0]["lineage"]["predecessor_record_ids"] = [second]
        mutated["records"][1]["lineage"]["predecessor_record_ids"] = [first]
        errors = self.errors_for(mutated)
        self.assertTrue(any("lineage cycle detected" in error for error in errors))

    def test_refuted_status_mismatch_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["status"] = "refuted"
        mutated["records"][0]["reopening"] = None
        errors = self.errors_for(mutated)
        self.assertTrue(any("refuted status requires theorem_refutation" in error for error in errors))

    def test_computational_exhaustion_kind_mismatch_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["status"] = "computationally_exhausted"
        mutated["records"][0]["reopening"]["trigger_type"] = "new_evidence"
        errors = self.errors_for(mutated)
        self.assertTrue(
            any("computationally_exhausted requires" in error for error in errors)
        )

    def test_review_self_attestation_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["review"]["satisfaction_mode"] = "embedded_disposition"
        errors = self.errors_for(mutated)
        self.assertTrue(
            any(
                "external_exact_head_review" in error
                or "review satisfaction must remain external" in error
                for error in errors
            )
        )

    def test_pilot_type_coverage_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][2]["record_type"] = "mathematical"
        errors = self.errors_for(mutated)
        self.assertTrue(
            any(
                "exactly the mathematical, computational, and systems" in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()
