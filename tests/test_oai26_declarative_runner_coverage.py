"""Adversarial assurance: a declared test owner must select an executing CI shard."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import policy_impact as impact


def component(*, shards, tests):
    return {
        "schema_version": "1.0.0",
        "component_id": "sandbox",
        "owner": "Synthetic test-only component",
        "shards": list(shards),
        "depends_on": [],
        "paths": {
            "exact": list(tests),
            "prefixes": ["governance/sandbox/"],
            "test_prefixes": [],
        },
    }


class RunnerCoverageAdversarialTest(unittest.TestCase):
    def check_manifest(self, row):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "sandbox.json").write_text(
                json.dumps(row), encoding="utf-8"
            )
            with patch.object(impact, "COMPONENT_DIR", directory):
                return impact.component_manifests()

    def test_reject_known_test_without_executing_shard(self):
        row = component(
            shards=["docs"],
            tests=["tests/test_sandbox_new_regression.py"],
        )
        with self.assertRaisesRegex(impact.ImpactError, "test route lacks executing shard"):
            self.check_manifest(row)

    def test_accept_same_test_once_runner_is_declared(self):
        row = component(
            shards=["docs", "repository-regression"],
            tests=["tests/test_sandbox_new_regression.py"],
        )
        registered = self.check_manifest(row)
        self.assertEqual(registered["sandbox"]["component_id"], "sandbox")

    def test_excluded_cmdg_test_requires_cmdg_runner(self):
        row = component(
            shards=["docs", "repository-regression"],
            tests=["tests/test_cmdg_sandbox_regression.py"],
        )
        with self.assertRaisesRegex(impact.ImpactError, "required=.*cmdg"):
            self.check_manifest(row)
        row["shards"].append("cmdg")
        self.assertIn("sandbox", self.check_manifest(row))

    def test_new_unregistered_test_still_rejected(self):
        with self.assertRaisesRegex(impact.ImpactError, "missing policy impact route"):
            impact.validate_new_test_routing(
                ["tests/test_unregistered_sandbox_regression.py"]
            )


if __name__ == "__main__":
    unittest.main()
