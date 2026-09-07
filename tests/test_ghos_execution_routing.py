from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ghos_execution_routing", ROOT / "ci" / "ghos_execution_routing.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name] = MODULE; SPEC.loader.exec_module(MODULE)
ENFORCEMENT_WORKFLOW = ROOT / ".github" / "workflows" / "ghos-routing-enforcement.yml"


class UniversalRoutingTests(unittest.TestCase):
    def fixture(self) -> Path:
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / ".github/workflows").mkdir(parents=True); (root / ".ghos-routing").mkdir(); (root / "schemas").mkdir()
        (root / MODULE.SCHEMA_PATH).write_bytes((ROOT / MODULE.SCHEMA_PATH).read_bytes())
        return root

    def write_workflow(self, root: Path, name: str, text: str) -> str:
        relative = f".github/workflows/{name}"; (root / relative).write_text(text, encoding="utf-8"); return relative

    def controller(self) -> dict:
        return dict(MODULE.ADMITTED_CONTROLLERS[0])

    def write_registry(self, root: Path, entries: list[dict], *, controllers: list[dict] | None = None, repository: str = "example/repository") -> None:
        value = {"record_type": "GHOS_EXECUTION_ROUTING_REGISTRY", "schema_version": "1.0.0", "repository": repository,
            "controllers": controllers if controllers is not None else [self.controller()], "workflows": entries, "claim_boundaries": MODULE.CLAIM_BOUNDARIES}
        (root / MODULE.REGISTRY_PATH).write_text(json.dumps(value), encoding="utf-8")

    def entry(self, path: str, features: list[str] | None = None, controller_id: str | None = None) -> dict:
        features = features or []
        return {"path": path, "observed_features": features, "topology": MODULE.derive_topology(set(features)), "controller_id": controller_id}

    def write_valid_bounded_fixture(self, root: Path) -> str:
        path = self.write_workflow(root, "bounded.yml", "on: workflow_dispatch\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(root, [self.entry(path)])
        return path

    def test_repository_registry_is_valid(self):
        MODULE.validate(root=ROOT, expected_repository="grandchallenge/MATH-PROGRAMME")

    def test_undeclared_unattended_workflow_fails_closed(self):
        root = self.fixture(); bounded = self.write_workflow(root, "bounded.yml", "on: push\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_workflow(root, "hidden.yaml", "on:\n  schedule:\n    - cron: '0 0 * * *'\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(root, [self.entry(bounded)])
        with self.assertRaisesRegex(MODULE.RoutingError, "coverage mismatch"): MODULE.validate(root=root, expected_repository="example/repository")

    def test_persistent_workflow_without_allowlisted_controller_fails(self):
        root = self.fixture(); path = self.write_workflow(root, "scheduled.yml", "on:\n  schedule:\n    - cron: '0 0 * * *'\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(root, [self.entry(path, ["AUTONOMOUS_WAKE", "SCHEDULED"], "invented")])
        with self.assertRaisesRegex(MODULE.RoutingError, "lacks admitted controller"): MODULE.validate(root=root, expected_repository="example/repository")

    def test_registry_cannot_self_authorize_invented_controller(self):
        root = self.fixture(); path = self.write_workflow(root, "scheduled.yml", "on:\n  schedule:\n    - cron: '0 0 * * *'\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        invented = self.controller(); invented["controller_id"] = "INVENTED"; invented["provider"] = "x"
        self.write_registry(root, [self.entry(path, ["AUTONOMOUS_WAKE", "SCHEDULED"], "INVENTED")], controllers=[invented])
        with self.assertRaisesRegex(MODULE.RoutingError, "governed admitted-controller set"): MODULE.validate(root=root, expected_repository="example/repository")

    def test_declared_features_cannot_hide_autonomous_wake(self):
        root = self.fixture(); path = self.write_workflow(root, "scheduled.yml", "on:\n  schedule:\n    - cron: '0 0 * * *'\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(root, [self.entry(path)])
        with self.assertRaisesRegex(MODULE.RoutingError, "feature declaration drift"): MODULE.validate(root=root, expected_repository="example/repository")

    def test_write_permissions_and_opaque_script_are_derived(self):
        root = self.fixture(); path = self.write_workflow(root, "writer.yml", "on: push\npermissions:\n  contents: write\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps:\n      - run: python scripts/write.py\n")
        features = ["OPAQUE_EXECUTION", "WRITE_CAPABLE"]
        self.write_registry(root, [self.entry(path, features, "GITHUB_ACTIONS")])
        MODULE.validate(root=root, expected_repository="example/repository")

    def test_secret_api_mutation_is_not_bounded(self):
        root = self.fixture(); path = self.write_workflow(root, "api.yml", "on: push\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps:\n      - env:\n          TOKEN: ${{ secrets.APP_TOKEN }}\n        run: gh api -X POST repos/x/y/issues\n")
        features = ["OPAQUE_EXECUTION", "SECRET_CREDENTIAL", "WRITE_CAPABLE"]
        self.write_registry(root, [self.entry(path, features, "GITHUB_ACTIONS")])
        MODULE.validate(root=root, expected_repository="example/repository")

    def test_nested_external_action_is_opaque(self):
        root = self.fixture(); path = self.write_workflow(root, "action.yml", "on: push\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: attacker/action@0123456789012345678901234567890123456789\n")
        self.write_registry(root, [self.entry(path, ["OPAQUE_EXECUTION"], "GITHUB_ACTIONS")])
        MODULE.validate(root=root, expected_repository="example/repository")

    def test_repository_identity_is_bound(self):
        root = self.fixture(); path = self.write_workflow(root, "bounded.yml", "on: push\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(root, [self.entry(path)])
        with self.assertRaisesRegex(MODULE.RoutingError, "repository identity mismatch"): MODULE.validate(root=root, expected_repository="other/repository")

    def test_rewriting_persistent_workflow_to_bounded_is_valid_decomposition_outcome(self):
        root = self.fixture(); path = self.write_workflow(root, "bounded.yml", "on: workflow_dispatch\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(root, [self.entry(path)])
        MODULE.validate(root=root, expected_repository="example/repository")

    def test_relevant_protected_base_change_is_visible_only_in_effective_tree(self):
        head_only = self.fixture(); self.write_valid_bounded_fixture(head_only)
        MODULE.validate(root=head_only, expected_repository="example/repository")

        effective = self.fixture(); bounded = self.write_valid_bounded_fixture(effective)
        self.write_workflow(effective, "protected-base-added.yml", "on: workflow_dispatch\njobs:\n  run:\n    runs-on: ubuntu-latest\n    steps: []\n")
        self.write_registry(effective, [self.entry(bounded)])
        with self.assertRaisesRegex(MODULE.RoutingError, "coverage mismatch"):
            MODULE.validate(root=effective, expected_repository="example/repository")

    def test_disjoint_protected_base_change_preserves_routing_result(self):
        effective = self.fixture(); self.write_valid_bounded_fixture(effective)
        (effective / "docs").mkdir(); (effective / "docs" / "unrelated.md").write_text("unrelated\n", encoding="utf-8")
        MODULE.validate(root=effective, expected_repository="example/repository")

    def test_enforcement_workflow_has_pr_base_advance_and_recovery_triggers(self):
        workflow = MODULE._load_workflow(ENFORCEMENT_WORKFLOW)
        triggers = workflow.get("on", workflow.get(True, {}))
        self.assertIsInstance(triggers, dict)
        self.assertTrue({"pull_request_target", "push", "workflow_dispatch"}.issubset(triggers))

    def test_required_context_is_explicitly_bound_to_effective_merge_sha(self):
        workflow = MODULE._load_workflow(ENFORCEMENT_WORKFLOW)
        text = ENFORCEMENT_WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn("routing-enforcement", workflow["jobs"])
        self.assertIn('"context": "routing-enforcement"', text)
        self.assertIn('/statuses/{os.environ["MERGE_SHA"]}', text)
        controller = workflow["jobs"]["routing-controller"]
        self.assertEqual(controller["permissions"]["statuses"], "write")
        self.assertEqual(controller["permissions"]["contents"], "read")

    def test_gate_runs_only_against_verified_effective_candidate_tree(self):
        text = ENFORCEMENT_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("refs/pull/${PR_NUMBER}/merge", text)
        self.assertIn('test "$PARENT_BASE" = "$CURRENT_BASE"', text)
        self.assertIn('test "$PARENT_HEAD" = "$HEAD_SHA"', text)
        self.assertIn("--root effective-candidate", text)
        self.assertNotIn("--root candidate", text)

    def test_enforcement_workflow_remains_self_protected(self):
        text = ENFORCEMENT_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("Reject enforcement self-modification", text)
        self.assertIn("protected-base/.github/workflows/ghos-routing-enforcement.yml", text)
        self.assertIn("effective-candidate/.github/workflows/ghos-routing-enforcement.yml", text)

    def test_protected_base_is_rechecked_after_gate_before_success_publication(self):
        text = ENFORCEMENT_WORKFLOW.read_text(encoding="utf-8")
        gate = text.index("Verify and execute external gate against effective candidate")
        post_gate = text.index("Verify protected base remained current through evaluation")
        publish = text.index("Publish required effective-candidate status")
        self.assertLess(gate, post_gate)
        self.assertLess(post_gate, publish)

    def test_protected_base_push_dispatches_open_pr_revalidation(self):
        workflow = MODULE._load_workflow(ENFORCEMENT_WORKFLOW)
        text = ENFORCEMENT_WORKFLOW.read_text(encoding="utf-8")
        base_refresh = workflow["jobs"]["base-refresh"]
        self.assertEqual(base_refresh["permissions"]["actions"], "write")
        self.assertIn("/actions/workflows/ghos-routing-enforcement.yml/dispatches", text)
        self.assertIn('"ref": "main"', text)

    def test_registry_features_match_privileged_controller_surface(self):
        workflow = MODULE._load_workflow(ENFORCEMENT_WORKFLOW)
        self.assertEqual(MODULE.observed_features(workflow), ["EXTERNAL_WAIT", "OPAQUE_EXECUTION", "SECRET_CREDENTIAL", "WRITE_CAPABLE"])


if __name__ == "__main__": unittest.main()
