from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_workflow_coverage import workflow_texts  # noqa: E402
from validate_workflow_coverage_v2 import workflow_coverage_errors  # noqa: E402


class PolicyRoutingWorkflowCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.texts = workflow_texts()
        cls.evidence = json.loads(
            (ROOT / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8")
        )
        cls.registry = json.loads(
            (ROOT / "governance/policy_shard_registry.json").read_text(encoding="utf-8")
        )

    def test_current_routed_full_suite_coverage_passes(self) -> None:
        self.assertEqual(
            workflow_coverage_errors(
                texts=self.texts,
                evidence=self.evidence,
                registry=self.registry,
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
