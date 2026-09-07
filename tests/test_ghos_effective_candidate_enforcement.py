from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ghos_execution_routing",
    ROOT / "ci" / "ghos_execution_routing.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ghos-routing-enforcement.yml"


class EffectiveCandidateRoutingTests(unittest.TestCase):
    def fixture(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / ".ghos-routing").mkdir()
        (root / "schemas").mkdir()
        shutil.copyfile(ROOT / MODULE.SCHEMA_PATH, root / MODULE.SCHEMA_PATH)
        return root

    def write_valid_bounded_fixture(self, root: Path) -> None:
        path = ".github/workflows/bounded.yml"
        (root / path).write_text(
            "on: workflow_dispatch\n"
            "jobs:\n"
            "  check:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps: []\n",
            encoding="utf-8",
        )
        registry = {
            "record_type": "GHOS_EXECUTION_ROUTING_REGISTRY",
            "schema_version": "1.0.0",
            "repository": "example/repository",
            "controllers": [dict(MODULE.ADMITTED_CONTROLLERS[0])],
            "workflows": [
                {
                    "path": path,
                    "observed_features": [],
                    "topology": "BOUNDED_ATOMIC",
                    "controller_id": None,
                }
            ],
            "claim_boundaries": MODULE.CLAIM_BOUNDARIES,
        }
        (root / MODULE.REGISTRY_PATH).write_text(
            json.dumps(registry),
            encoding="utf-8",
        )

    def test_relevant_protected_base_change_is_visible_only_in_effective_tree(self):
        head_only = self.fixture()
        self.write_valid_bounded_fixture(head_only)
        MODULE.validate(root=head_only, expected_repository="example/repository")

        effective = self.fixture()
        shutil.copytree(head_only, effective, dirs_exist_ok=True)
        (effective / ".github" / "workflows" / "protected-base-added.yml").write_text(
            "on: workflow_dispatch\n"
            "jobs:\n"
            "  check:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps: []\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(MODULE.RoutingError, "coverage mismatch"):
            MODULE.validate(root=effective, expected_repository="example/repository")

    def test_disjoint_protected_base_change_preserves_routing_result(self):
        effective = self.fixture()
        self.write_valid_bounded_fixture(effective)
        (effective / "docs").mkdir()
        (effective / "docs" / "unrelated.md").write_text(
            "Unrelated protected-base documentation movement.\n",
            encoding="utf-8",
        )
        MODULE.validate(root=effective, expected_repository="example/repository")


class EnforcementWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = MODULE._load_workflow(WORKFLOW_PATH)

    def test_workflow_has_pr_base_advance_and_manual_recovery_triggers(self):
        triggers = self.workflow.get("on", self.workflow.get(True, {}))
        self.assertIsInstance(triggers, dict)
        self.assertTrue(
            {"pull_request_target", "push", "workflow_dispatch"}.issubset(triggers)
        )

    def test_required_context_is_not_the_controller_job_name(self):
        self.assertNotIn("routing-enforcement", self.workflow["jobs"])
        self.assertIn('"context": "routing-enforcement"', self.text)

    def test_gate_runs_only_against_effective_candidate_tree(self):
        self.assertIn("refs/pull/${PR_NUMBER}/merge", self.text)
        self.assertIn('test "$PARENT_BASE" = "$CURRENT_BASE"', self.text)
        self.assertIn('test "$PARENT_HEAD" = "$HEAD_SHA"', self.text)
        self.assertIn("--root effective-candidate", self.text)
        self.assertNotIn("--root candidate", self.text)

    def test_enforcement_workflow_remains_self_protected(self):
        self.assertIn("Reject enforcement self-modification", self.text)
        self.assertIn(
            "protected-base/.github/workflows/ghos-routing-enforcement.yml",
            self.text,
        )
        self.assertIn(
            "effective-candidate/.github/workflows/ghos-routing-enforcement.yml",
            self.text,
        )

    def test_status_is_bound_to_effective_merge_sha(self):
        self.assertIn(
            '/statuses/{os.environ["MERGE_SHA"]}',
            self.text,
        )
        controller = self.workflow["jobs"]["routing-controller"]
        self.assertEqual(controller["permissions"]["statuses"], "write")
        self.assertEqual(controller["permissions"]["contents"], "read")

    def test_protected_base_push_dispatches_open_pr_revalidation(self):
        base_refresh = self.workflow["jobs"]["base-refresh"]
        self.assertEqual(base_refresh["permissions"]["actions"], "write")
        self.assertIn(
            "/actions/workflows/ghos-routing-enforcement.yml/dispatches",
            self.text,
        )
        self.assertIn('"ref": "main"', self.text)

    def test_registry_features_match_privileged_controller_surface(self):
        self.assertEqual(
            MODULE.observed_features(self.workflow),
            ["EXTERNAL_WAIT", "OPAQUE_EXECUTION", "SECRET_CREDENTIAL", "WRITE_CAPABLE"],
        )


if __name__ == "__main__":
    unittest.main()
