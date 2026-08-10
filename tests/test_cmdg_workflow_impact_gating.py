from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "ci"))
import validate_cmdg_workflow_impact_gating as gate  # noqa: E402


class CMDGWorkflowImpactGatingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = json.loads(gate.CONTROL.read_text(encoding="utf-8"))
        cls.schema = json.loads(gate.SCHEMA.read_text(encoding="utf-8"))
        cls.texts = gate.load_workflow_texts()

    def test_control_schema_is_closed(self):
        jsonschema.validate(self.control, self.schema)
        mutated = copy.deepcopy(self.control)
        mutated["unexpected"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mutated, self.schema)

    def test_protected_roster_and_event_contract(self):
        self.assertEqual(gate.validation_errors(self.control, self.texts), [])

    def test_unrelated_docs_do_not_match(self):
        paths = self.control["pull_request_paths"]
        for sample in self.control["negative_examples"]:
            self.assertFalse(gate.path_matches(sample, paths), sample)

    def test_each_declared_dependency_class_matches(self):
        paths = self.control["pull_request_paths"]
        for sample in self.control["positive_examples"]:
            self.assertTrue(gate.path_matches(sample, paths), sample)

    def test_new_cmdg_workflow_fails_closed(self):
        texts = dict(self.texts)
        texts["cmdg-unregistered-successor.yml"] = next(iter(texts.values()))
        errors = gate.validation_errors(self.control, texts)
        self.assertTrue(any("roster drift" in error for error in errors), errors)

    def test_missing_cmdg_workflow_fails_closed(self):
        texts = dict(self.texts)
        texts.pop(self.control["workflow_roster"][0])
        errors = gate.validation_errors(self.control, texts)
        self.assertTrue(any("roster drift" in error for error in errors), errors)

    def test_path_contract_drift_fails_closed(self):
        texts = dict(self.texts)
        name = self.control["workflow_roster"][0]
        texts[name] = texts[name].replace(
            '      - ".github/workflows/**"\n',
            '      - "docs/**"\n',
            1,
        )
        errors = gate.validation_errors(self.control, texts)
        self.assertTrue(any("pull_request paths" in error for error in errors), errors)

    def test_push_or_dispatch_removal_fails_closed(self):
        texts = dict(self.texts)
        name = self.control["workflow_roster"][1]
        texts[name] = texts[name].replace("  workflow_dispatch:\n", "", 1)
        errors = gate.validation_errors(self.control, texts)
        self.assertTrue(any("workflow_dispatch" in error for error in errors), errors)

    def test_authority_mutation_is_rejected(self):
        mutated = copy.deepcopy(self.control)
        mutated["authority_boundary"]["bypass_created"] = True
        errors = gate.validation_errors(mutated, self.texts)
        self.assertTrue(any("control/schema invalid" in error or "authority" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
