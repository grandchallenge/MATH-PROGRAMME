"""Live regression: new OAI26 modules are discovered without classifier edits."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import policy_impact as impact


class DeclarativeOAI26RegistrationTest(unittest.TestCase):
    def test_new_module_is_owned_and_routed(self):
        path = "tests/test_oai26_declarative_auto_registration.py"
        result = impact.classify_paths([path])
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(
            result["policy_shards"], ["core", "docs", "repository-regression"]
        )
        impact.validate_new_test_routing([path])

    def test_documentary_dependency_closure(self):
        result = impact.classify_paths([
            "governance/oai26_documentary/editorial/092.md",
            "tests/test_oai26_declarative_auto_registration.py",
        ])
        self.assertEqual(result["unknown_paths"], [])
        self.assertEqual(
            result["policy_shards"],
            ["core", "contracts", "docs", "repository-regression"],
        )

    def test_unregistered_module_still_fails_new_test_gate(self):
        with self.assertRaisesRegex(impact.ImpactError, "missing policy impact route"):
            impact.validate_new_test_routing([
                "tests/test_unregistered_research_autorouting_probe.py",
            ])


if __name__ == "__main__":
    unittest.main()
