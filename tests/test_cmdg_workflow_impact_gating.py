from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import formal_validation  # noqa: E402
import validate_cmdg_workflow_impact_gating as gate  # noqa: E402


class CMDGWorkflowImpactGatingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = json.loads(gate.CONTROL.read_text(encoding="utf-8"))
        cls.schema = json.loads(gate.SCHEMA.read_text(encoding="utf-8"))
        cls.texts = gate.load_workflow_texts(cls.control)
        cls.dispatcher = gate.load_dispatcher_text()
        cls.registry = formal_validation.load_registry(ROOT)

    def errors(self, control=None, texts=None, dispatcher=None):
        return gate.validation_errors(
            self.control if control is None else control,
            self.texts if texts is None else texts,
            self.dispatcher if dispatcher is None else dispatcher,
        )

    def test_control_schema_is_closed(self):
        jsonschema.validate(self.control, self.schema)
        mutated = copy.deepcopy(self.control)
        mutated["unexpected"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mutated, self.schema)

    def test_protected_roster_and_event_contract(self):
        self.assertEqual(self.errors(), [])

    def test_p3_only_change_selects_only_p3(self):
        sample = self.control["acceptance_examples"]["p3_only"]
        result = formal_validation.classify_paths(sample["paths"], self.registry)
        self.assertEqual(result["lanes"], ["cmdg-cm4-p3"])
        self.assertNotIn("cmdg-cm1", result["lanes"])
        self.assertNotIn("log-gcd", result["lanes"])

    def test_unrelated_change_has_no_formal_lane(self):
        sample = self.control["acceptance_examples"]["unrelated"]
        result = formal_validation.classify_paths(sample["paths"], self.registry)
        self.assertEqual(result["lanes"], [])

    def test_new_or_missing_cmdg_wrapper_fails_closed(self):
        missing = dict(self.texts)
        missing.pop(next(iter(missing)))
        errors = self.errors(texts=missing)
        self.assertTrue(any("text roster drift" in error for error in errors), errors)

    def test_wrapper_lane_binding_drift_fails_closed(self):
        texts = dict(self.texts)
        name = "cmdg-condensed-cm1.yml"
        texts[name] = texts[name].replace("lane: cmdg-cm1", "lane: cmdg-cm2")
        errors = self.errors(texts=texts)
        self.assertTrue(any("lane binding drift" in error for error in errors), errors)

    def test_wrapper_pr_trigger_fails_closed(self):
        texts = dict(self.texts)
        name = "cmdg-condensed-cm1.yml"
        texts[name] = texts[name].replace("  workflow_call:\n", "  workflow_call:\n  pull_request:\n")
        errors = self.errors(texts=texts)
        self.assertTrue(any("triggers must be exactly" in error or "forbidden" in error for error in errors), errors)

    def test_current_head_sentinel_contract_is_exact(self):
        dispatcher = self.dispatcher.replace('    - cron: "47 11 * * *"', '    - cron: "47 11 * * 0"')
        errors = self.errors(dispatcher=dispatcher)
        self.assertTrue(any("sentinel cron drift" in error for error in errors), errors)

    def test_authority_mutation_is_rejected(self):
        mutated = copy.deepcopy(self.control)
        mutated["authority_boundary"]["bypass_created"] = True
        errors = self.errors(control=mutated)
        self.assertTrue(any("invalid" in error or "authority" in error for error in errors), errors)

    def test_unknown_formal_source_fails_closed(self):
        with self.assertRaises(formal_validation.FormalValidationError):
            formal_validation.classify_paths(
                ["fixtures/formal/CMDG-NAT-CONCORDANCE-001/UnknownFutureProbe.lean"],
                self.registry,
            )

    def test_large_p3_pr_is_not_rejected_by_native_path_limit(self):
        paths = [f"docs/generated-{index:04d}.md" for index in range(400)]
        paths.append(
            "fixtures/formal/CMDG-NAT-CONCORDANCE-001/"
            "CMDGCondensedCM4P3GPointFunctional.lean"
        )
        result = formal_validation.classify_paths(paths, self.registry)
        self.assertEqual(result["lanes"], ["cmdg-cm4-p3"])


if __name__ == "__main__":
    unittest.main()
