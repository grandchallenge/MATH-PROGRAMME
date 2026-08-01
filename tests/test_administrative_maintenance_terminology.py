from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TERMS_PATH = ROOT / "docs" / "governance" / "ADMINISTRATIVE_MAINTENANCE_TERMINOLOGY.md"

REQUIRED_TERMS = {
    "Core Clarity",
    "Material change",
    "Nonmaterial change",
    "Event-triggered synchronization",
    "Accelerated maintenance time scale",
    "Accelerated pilot",
    "Workflow coverage",
    "Canonical tracker",
    "Issue mirror",
    "Tracker refresh clock",
    "Administrative waiver",
    "Emergency override",
    "Maintenance-burden circuit breaker",
    "Campaign-level fail closed",
    "Portfolio admission freeze",
    "INTELLECT Phase A buy-in",
    "INTELLECT Phase B protected adoption",
    "Protected-merge activation",
    "Final cross-repository closure",
}


class AdministrativeMaintenanceTerminologyTests(unittest.TestCase):
    def test_registry_extension_exists_and_is_decision_bound(self) -> None:
        text = TERMS_PATH.read_text(encoding="utf-8")
        self.assertIn("MP-ADMIN-TERMS-001", text)
        self.assertIn("ADR-0016", text)
        self.assertIn("docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md", text)

    def test_all_controlled_terms_are_registered(self) -> None:
        text = TERMS_PATH.read_text(encoding="utf-8")
        for term in REQUIRED_TERMS:
            self.assertIn(f"| {term} |", text)

    def test_accelerated_duration_and_authority_boundaries_are_explicit(self) -> None:
        text = TERMS_PATH.read_text(encoding="utf-8")
        self.assertIn("`0.1`", text)
        self.assertIn("`PT7H12M`", text)
        self.assertIn("cannot create protected state", text)
        self.assertIn("Final administrative closure is prohibited", text)


if __name__ == "__main__":
    unittest.main()
