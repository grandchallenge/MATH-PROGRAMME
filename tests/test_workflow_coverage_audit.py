from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_workflow_coverage_audit import WorkflowCoverageAuditError, validate  # noqa: E402


class WorkflowCoverageAuditTests(unittest.TestCase):
    def make_root(self) -> tempfile.TemporaryDirectory:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        for relative in (
            "governance",
            "schemas",
            ".github/workflows",
            "ci",
        ):
            (root / relative).mkdir(parents=True, exist_ok=True)
        for relative in (
            "governance/workflow_coverage_audit.json",
            "governance/mathcert_cross_repository_conformance.json",
            "schemas/workflow_coverage_audit.schema.json",
            ".github/workflows/ci.yml",
            ".github/workflows/pages.yml",
            "ci/validate_workflow_semantics.py",
            "ci/validate_policy_reachability.py",
            "ci/validate_repository_execution.py",
            "ci/validate_symbolic_resource_budgets.py",
            "ci/validate_cross_pillar_lane_packages.py",
        ):
            shutil.copy2(ROOT / relative, root / relative)
        return directory

    def mutate(self, root: Path, mutator) -> None:
        path = root / "governance/workflow_coverage_audit.json"
        audit = json.loads(path.read_text(encoding="utf-8"))
        mutator(audit)
        path.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    def assert_rejected(self, mutator) -> None:
        directory = self.make_root()
        root = Path(directory.name)
        try:
            mutator(root)
            with self.assertRaises(WorkflowCoverageAuditError):
                validate(root)
        finally:
            directory.cleanup()

    def test_current_audit_passes(self) -> None:
        validate(ROOT)

    def test_missing_coverage_area_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate(root, lambda audit: audit["coverage_areas"].pop())
        )

    def test_blocker_cannot_be_silently_removed(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate(root, lambda audit: audit["remaining_blockers"].pop())
        )

    def test_umbrella_issue_cannot_close_while_blocked(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate(
                root, lambda audit: audit.update(umbrella_issue_disposition="CLOSE")
            )
        )

    def test_operational_release_cannot_be_true_with_incomplete_children(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate(
                root, lambda audit: audit.update(operational_release_complete=True)
            )
        )

    def test_technical_implementation_identity_drift_is_rejected(self) -> None:
        def mutate(audit: dict) -> None:
            child = next(item for item in audit["children"] if item["repository"] == "grandchallenge/MATHFORGE")
            child["implementation"]["merge_commit"] = "0" * 40

        self.assert_rejected(lambda root: self.mutate(root, mutate))

    def test_administrative_child_cannot_be_marked_complete_without_full_closure(self) -> None:
        def mutate(audit: dict) -> None:
            child = next(item for item in audit["children"] if item["issue"] == 7)
            child["state"] = "CLOSED"
            child["complete"] = True
            child["close_conditions"] = []

        self.assert_rejected(lambda root: self.mutate(root, mutate))

    def test_missing_child_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate(root, lambda audit: audit["children"].pop())
        )

    def test_missing_audited_control_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: (root / "ci/validate_policy_reachability.py").unlink()
        )


if __name__ == "__main__":
    unittest.main()
