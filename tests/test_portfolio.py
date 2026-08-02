#!/usr/bin/env python3
"""Adversarial tests for the GCL portfolio pilot."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "ci"
if str(CI) not in sys.path:
    sys.path.insert(0, str(CI))

from render_portfolio import advisory_interval, render  # noqa: E402
from validate_portfolio import validate  # noqa: E402


class PortfolioPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads((ROOT / "portfolio" / "pilot_registry.json").read_text(encoding="utf-8"))
        self.schema = json.loads((ROOT / "schemas" / "gcl_portfolio_registry.schema.json").read_text(encoding="utf-8"))

    def errors_for(self, registry: dict, *, view: str | None = None) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            registry_path = base / "registry.json"
            schema_path = base / "schema.json"
            view_path = base / "view.md"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            schema_path.write_text(json.dumps(self.schema), encoding="utf-8")
            if view is None:
                try:
                    rendered = render(registry)
                except (KeyError, TypeError, ValueError):
                    rendered = render(self.registry)
            else:
                rendered = view
            view_path.write_text(rendered, encoding="utf-8")
            return validate(registry_path, schema_path, view_path)

    def test_valid_registry(self) -> None:
        self.assertEqual([], validate())

    def test_schema_is_closed(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["prestige_bonus"] = 5
        self.assertTrue(any("Additional properties" in error for error in self.errors_for(mutated)))

    def test_exact_cardinality_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"].pop()
        self.assertTrue(any("too short" in error or "exactly four" in error for error in self.errors_for(mutated)))

    def test_duplicate_work_identity_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][1]["work_package_id"] = mutated["records"][0]["work_package_id"]
        self.assertTrue(any("unique" in error or "exactly GCL work packages" in error for error in self.errors_for(mutated)))

    def test_issue_mapping_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["issue_number"] = 191
        mutated["records"][1]["issue_number"] = 190
        self.assertTrue(any("expected issue" in error for error in self.errors_for(mutated)))

    def test_negative_cost_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["cost"]["labour"] = -1
        self.assertTrue(any("minimum" in error or "not valid" in error for error in self.errors_for(mutated)))

    def test_hidden_cost_component_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        del mutated["records"][0]["cost"]["review"]
        self.assertTrue(any("required property" in error for error in self.errors_for(mutated)))

    def test_stale_evidence_without_refresh_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["evidence_freshness"]["status"] = "stale"
        self.assertTrue(any("requires a refresh obligation" in error for error in self.errors_for(mutated)))

    def test_current_evidence_with_refresh_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["evidence_freshness"]["refresh_obligation"] = "Unnecessary refresh"
        self.assertTrue(any("current evidence" in error for error in self.errors_for(mutated)))

    def test_score_weight_gaming_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["model"]["benefit_weights"]["scientific_importance"] = 5
        self.assertTrue(any("2 was expected" in error for error in self.errors_for(mutated)))

    def test_zero_readiness_zeroes_advisory(self) -> None:
        blocked = self.registry["records"][1]
        lower, upper = advisory_interval(blocked, self.registry["model"])
        self.assertEqual((0.0, 0.0), (lower, upper))

    def test_blocked_readiness_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][1]["execution_readiness"] = 5
        self.assertTrue(any("at most one" in error for error in self.errors_for(mutated)))

    def test_active_dependency_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["dependencies"] = ["GCL-SYNTHESIS-WP00"]
        self.assertTrue(any("active record must not retain" in error or "earlier umbrella" in error for error in self.errors_for(mutated)))

    def test_unknown_widens_interval(self) -> None:
        original = self.registry["records"][1]
        _, original_upper = advisory_interval(original, self.registry["model"])
        mutated = copy.deepcopy(original)
        mutated["execution_readiness"] = "unknown"
        _, unknown_upper = advisory_interval(mutated, self.registry["model"])
        self.assertGreater(unknown_upper, original_upper)

    def test_automated_disposition_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["disposition"]["automated"] = True
        self.assertTrue(any("False was expected" in error or "automated disposition" in error for error in self.errors_for(mutated)))

    def test_machine_action_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["disposition"]["machine_action"] = "allocate_compute"
        self.assertTrue(any("not of type 'null'" in error or "automated disposition" in error for error in self.errors_for(mutated)))

    def test_irreversible_lock_in_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["reversibility"]["irreversible_commitment"] = True
        self.assertTrue(any("False was expected" in error or "irreversible" in error for error in self.errors_for(mutated)))

    def test_dependency_cycle_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["dependencies"] = ["GCL-DISCLOSURE-WP00"]
        self.assertTrue(any("dependency cycle" in error or "earlier umbrella" in error for error in self.errors_for(mutated)))

    def test_generated_view_drift_rejected(self) -> None:
        self.assertTrue(any("generated portfolio view" in error for error in self.errors_for(self.registry, view="# stale\n")))

    def test_fabricated_fractional_precision_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["scientific_importance"] = 4.7
        self.assertTrue(any("not valid under any" in error or "not of type 'integer'" in error for error in self.errors_for(mutated)))

    def test_claim_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["records"][0]["claim_boundaries"]["allocates_resources"] = True
        self.assertTrue(any("False was expected" in error or "claim-boundary" in error for error in self.errors_for(mutated)))


if __name__ == "__main__":
    unittest.main()
