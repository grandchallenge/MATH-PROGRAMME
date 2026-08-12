from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import policy_impact  # noqa: E402
import validate_cmdg_workflow_impact_gating as gate  # noqa: E402


class CMDGWorkflowImpactGatingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = json.loads(gate.CONTROL.read_text(encoding="utf-8"))
        cls.schema = json.loads(gate.SCHEMA.read_text(encoding="utf-8"))
        cls.texts = gate.load_workflow_texts()
        cls.dispatcher = gate.load_dispatcher_text()

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

    def test_unrelated_docs_do_not_match_pr_gate(self):
        for sample in self.control["negative_examples"]:
            self.assertFalse(gate.path_matches(sample, self.control["pull_request_paths"]), sample)

    def test_each_declared_dependency_class_matches_pr_gate(self):
        for sample in self.control["positive_examples"]:
            self.assertTrue(gate.path_matches(sample, self.control["pull_request_paths"]), sample)

    def test_new_or_missing_cmdg_workflow_fails_closed(self):
        added = dict(self.texts)
        added["cmdg-unregistered-successor.yml"] = next(iter(added.values()))
        self.assertTrue(any("roster drift" in error for error in self.errors(texts=added)))
        missing = dict(self.texts)
        missing.pop(self.control["workflow_roster"][0])
        self.assertTrue(any("roster drift" in error for error in self.errors(texts=missing)))

    def test_pr_path_contract_drift_fails_closed(self):
        texts = dict(self.texts)
        name = self.control["workflow_roster"][0]
        texts[name] = texts[name].replace('      - ".github/workflows/**"\n', '      - "docs/**"\n', 1)
        self.assertTrue(any("pull_request paths" in error for error in self.errors(texts=texts)))

    def test_standalone_push_or_call_contract_drift_fails_closed(self):
        texts = dict(self.texts)
        name = self.control["workflow_roster"][0]
        texts[name] = texts[name].replace("  workflow_call:\n", "  push:\n    branches: [main]\n", 1)
        errors = self.errors(texts=texts)
        self.assertTrue(any("direct push" in error for error in errors), errors)
        self.assertTrue(any("workflow_call" in error for error in errors), errors)

    def test_native_main_push_filter_fails_closed(self):
        dispatcher = self.dispatcher.replace("  schedule:\n", "    paths:\n      - \"fixtures/cmdg/**\"\n  schedule:\n", 1)
        errors = self.errors(dispatcher=dispatcher)
        self.assertTrue(any("without native paths" in error for error in errors), errors)

    def test_unknown_main_push_selects_cmdg_full_family(self):
        result = policy_impact.classify_paths(["brand-new-policy-domain/data.bin"], event_name="push")
        self.assertIn("cmdg", result["policy_shards"])
        self.assertEqual(result["unknown_paths"], ["brand-new-policy-domain/data.bin"])

    def test_dispatcher_reusable_roster_drift_fails_closed(self):
        dispatcher = self.dispatcher.replace("    uses: ./.github/workflows/cmdg-condensed-cm1.yml\n", "", 1)
        errors = self.errors(dispatcher=dispatcher)
        self.assertTrue(any("reusable-workflow roster drift" in error for error in errors), errors)

    def test_dispatch_and_daily_current_head_sentinel_are_required(self):
        dispatcher = self.dispatcher.replace("  workflow_dispatch:\n", "", 1)
        self.assertTrue(any("workflow_dispatch" in error for error in self.errors(dispatcher=dispatcher)))
        dispatcher = self.dispatcher.replace('    - cron: "47 11 * * *"\n', '    - cron: "47 11 * * 0"\n', 1)
        self.assertTrue(any("current-head sentinel" in error for error in self.errors(dispatcher=dispatcher)))

    def test_authority_mutation_is_rejected(self):
        mutated = copy.deepcopy(self.control)
        mutated["authority_boundary"]["bypass_created"] = True
        errors = self.errors(control=mutated)
        self.assertTrue(any("control/schema invalid" in error or "authority" in error for error in errors), errors)

    def test_large_unrelated_pr_remains_allowed(self):
        paths = [f"docs/generated-{index:04d}.md" for index in range(301)]
        result = policy_impact.classify_paths(paths, event_name="pull_request")
        self.assertEqual(set(result["policy_shards"]), {"core", "docs"})

    def test_large_cmdg_relevant_pr_fails_protected_policy(self):
        paths = [f"docs/generated-{index:04d}.md" for index in range(300)] + ["fixtures/cmdg/condensed_cm1_001/nodes.json"]
        with self.assertRaises(policy_impact.ImpactError):
            policy_impact.classify_paths(paths, event_name="pull_request")


if __name__ == "__main__":
    unittest.main()
