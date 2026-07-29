from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_symbolic_resource_budgets import SymbolicBudgetError, validate  # noqa: E402


class SymbolicResourceBudgetTests(unittest.TestCase):
    def source_registry(self) -> dict:
        return json.loads(
            (ROOT / "governance/expensive_symbolic_lane_registry.json").read_text(
                encoding="utf-8"
            )
        )

    def source_manifest(self) -> dict:
        return json.loads(
            (ROOT / "applications/grobner_manifest.json").read_text(encoding="utf-8")
        )

    def build_root(self, registry: dict, manifest: dict) -> tempfile.TemporaryDirectory:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        for path in ("applications", "campaigns", "fixtures", "governance", "schemas"):
            (root / path).mkdir(parents=True, exist_ok=True)
        (root / "applications/grobner_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        (root / "governance/expensive_symbolic_lane_registry.json").write_text(
            json.dumps(registry, indent=2) + "\n", encoding="utf-8"
        )
        (root / "schemas/expensive_symbolic_lane_registry.schema.json").write_text(
            (ROOT / "schemas/expensive_symbolic_lane_registry.schema.json").read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )
        return directory

    def assert_rejected(self, registry: dict, manifest: dict) -> None:
        directory = self.build_root(registry, manifest)
        try:
            with self.assertRaises(SymbolicBudgetError):
                validate(Path(directory.name))
        finally:
            directory.cleanup()

    def test_current_repository_passes(self) -> None:
        validate(ROOT)

    def test_missing_budget_is_rejected(self) -> None:
        registry = self.source_registry()
        manifest = self.source_manifest()
        manifest["lanes"][0].pop("resource_budget")
        self.assert_rejected(registry, manifest)

    def test_unregistered_discovered_lane_is_rejected(self) -> None:
        registry = self.source_registry()
        manifest = self.source_manifest()
        added = copy.deepcopy(manifest["lanes"][0])
        added["lane_id"] = "APP-NEW-07"
        manifest["lanes"].append(added)
        self.assert_rejected(registry, manifest)

    def test_orphan_registry_entry_is_rejected(self) -> None:
        registry = self.source_registry()
        manifest = self.source_manifest()
        registry["entries"].append(
            {
                "lane_id": "APP-MISSING-99",
                "path": "applications/grobner_manifest.json",
                "owner": "MATH-PROGRAMME",
                "reviewed_at": "2026-07-28",
            }
        )
        self.assert_rejected(registry, manifest)

    def test_failed_run_without_failure_record_is_rejected(self) -> None:
        registry = self.source_registry()
        manifest = self.source_manifest()
        manifest["lanes"][1]["run_ledger"] = {
            "execution_status": "failed",
            "termination_status": "timeout",
            "failure_status": "timeout",
            "failure_record": None,
            "result_artifact": None,
            "recorded_at": "2026-07-28T00:00:00Z",
        }
        self.assert_rejected(registry, manifest)

    def test_completed_run_without_artifact_is_rejected(self) -> None:
        registry = self.source_registry()
        manifest = self.source_manifest()
        manifest["lanes"][2]["run_ledger"] = {
            "execution_status": "completed",
            "termination_status": "success",
            "failure_status": None,
            "failure_record": None,
            "result_artifact": None,
            "recorded_at": "2026-07-28T00:00:00Z",
        }
        self.assert_rejected(registry, manifest)


if __name__ == "__main__":
    unittest.main()
