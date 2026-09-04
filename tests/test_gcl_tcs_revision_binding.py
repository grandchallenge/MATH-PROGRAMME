from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from ci.gcl_tcs_revision_binding import (
    DECL_SCHEMA,
    RECORD_SCHEMA,
    binding_errors,
    governed_revision_errors,
    is_immutable_revision,
    schema_binding_errors,
)

ROOT = Path(__file__).resolve().parents[1]
DECL_TEMPLATE = ROOT / "docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.conformance.template.yaml"
RECORD_TEMPLATE = ROOT / "docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.records.template.yaml"
GOOD = "sha256:" + "a" * 64
ALT = "git-commit:" + "b" * 40


class GclTcsRevisionBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.decl_schema = json.loads((ROOT / DECL_SCHEMA).read_text(encoding="utf-8"))
        cls.record_schema = json.loads((ROOT / RECORD_SCHEMA).read_text(encoding="utf-8"))
        cls.declaration = yaml.safe_load(DECL_TEMPLATE.read_text(encoding="utf-8"))
        cls.records = yaml.safe_load(RECORD_TEMPLATE.read_text(encoding="utf-8"))

    def test_schema_binds_machine_revision_fields(self) -> None:
        self.assertEqual(schema_binding_errors(self.decl_schema, self.record_schema), [])

    def test_canonical_immutable_revision_forms_are_accepted(self) -> None:
        for value in (
            GOOD,
            ALT,
            "git-blob:" + "c" * 40,
            "git-tree:" + "d" * 40,
            "e" * 40,
        ):
            with self.subTest(value=value):
                self.assertTrue(is_immutable_revision(value))

    def test_mutable_symbolic_revisions_are_rejected(self) -> None:
        for value in ("main", "latest", "refs/heads/main", "HEAD", "release-current", "abc123", ""):
            with self.subTest(value=value):
                self.assertFalse(is_immutable_revision(value))

    def test_declaration_schema_rejects_mutable_source_revision(self) -> None:
        validator = Draft202012Validator(self.decl_schema, format_checker=FormatChecker())
        good = copy.deepcopy(self.declaration)
        self.assertEqual(list(validator.iter_errors(good)), [])
        for value in ("main", "latest", "refs/heads/main"):
            broken = copy.deepcopy(good)
            broken["source_revision"] = value
            self.assertTrue(list(validator.iter_errors(broken)))

    def test_gate_schema_rejects_mutable_revision(self) -> None:
        schema = self.record_schema["$defs"]["gateRecord"]
        validator = Draft202012Validator(schema)
        good = copy.deepcopy(self.records["gate_record"])
        self.assertEqual(list(validator.iter_errors(good)), [])
        good["reviewed_revision"] = "main"
        self.assertTrue(list(validator.iter_errors(good)))

    def test_review_schema_rejects_mutable_revision(self) -> None:
        schema = self.record_schema["$defs"]["reviewRecord"]
        validator = Draft202012Validator(schema)
        good = copy.deepcopy(self.records["review_record"])
        self.assertEqual(list(validator.iter_errors(good)), [])
        good["reviewed_revision"] = "latest"
        self.assertTrue(list(validator.iter_errors(good)))

    def exact_triplet(self):
        declaration = copy.deepcopy(self.declaration)
        declaration["artifact_id"] = "EXAMPLE-ARTIFACT-001"
        declaration["source_revision"] = GOOD
        gate = copy.deepcopy(self.records["gate_record"])
        gate["artifact_id"] = declaration["artifact_id"]
        gate["reviewed_revision"] = GOOD
        review = copy.deepcopy(self.records["review_record"])
        review["gate_id"] = gate["gate_id"]
        review["reviewed_revision"] = GOOD
        return declaration, gate, review

    def test_exact_artifact_revision_binding_passes(self) -> None:
        declaration, gate, review = self.exact_triplet()
        self.assertEqual(binding_errors(declaration, gate, review), [])

    def test_revision_mismatch_fails_closed(self) -> None:
        declaration, gate, review = self.exact_triplet()
        review["reviewed_revision"] = ALT
        self.assertIn("binding: revision_mismatch", binding_errors(declaration, gate, review))

    def test_artifact_mismatch_fails_closed(self) -> None:
        declaration, gate, review = self.exact_triplet()
        gate["artifact_id"] = "OTHER-ARTIFACT"
        self.assertIn("binding: artifact_id_mismatch", binding_errors(declaration, gate, review))

    def test_gate_mismatch_fails_closed(self) -> None:
        declaration, gate, review = self.exact_triplet()
        review["gate_id"] = "G7"
        self.assertIn("binding: gate_id_mismatch", binding_errors(declaration, gate, review))

    def test_governed_tcs_revision_values_are_immutable(self) -> None:
        self.assertEqual(governed_revision_errors(), [])


if __name__ == "__main__":
    unittest.main()
