from __future__ import annotations

import copy
import unittest

from ci.validate_administrative_cadence_reconciliation import (
    EXPECTED_INVENTORY,
    EXPECTED_SWEEPS,
    load_bundle,
    load_schemas,
    validate_bundle,
)


class AdministrativeCadenceReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = load_schemas()

    def fresh_bundle(self) -> dict:
        return load_bundle()

    def errors_for(self, bundle: dict) -> list[str]:
        return validate_bundle(bundle, self.schemas)

    def test_bundle_is_schema_and_semantically_valid(self) -> None:
        self.assertEqual(self.errors_for(self.fresh_bundle()), [])

    def test_four_missed_sweeps_remain_separate(self) -> None:
        bundle = self.fresh_bundle()
        self.assertEqual(len(bundle["sweeps"]), 4)
        self.assertEqual({item["sweep_id"] for item in bundle["sweeps"]}, set(EXPECTED_SWEEPS))
        self.assertEqual(len(bundle["reconciliation"]["structural_sweep_records"]), 4)

    def test_five_repository_inventory_is_exact(self) -> None:
        bundle = self.fresh_bundle()
        observed = {
            item["repository"]: (
                item["first_sweep_head"],
                item["reconciliation_head"],
                item["commits_since_first_sweep"],
            )
            for item in bundle["portfolio"]["repository_inventory"]
        }
        self.assertEqual(observed, EXPECTED_INVENTORY)

    def test_repeated_failure_escalates_without_p1_inflation(self) -> None:
        bundle = self.fresh_bundle()
        self.assertTrue(bundle["reconciliation"]["disposition"]["pilot_level_escalation_required"])
        self.assertTrue(bundle["portfolio"]["pilot_escalation"]["required"])
        self.assertFalse(bundle["portfolio"]["pilot_escalation"]["immediate_p1"])
        self.assertEqual(bundle["reconciliation"]["disposition"]["P1"], 0)
        self.assertEqual(bundle["reconciliation"]["disposition"]["P2"], 5)

    def test_mutation_rejects_deadline_rewrite(self) -> None:
        bundle = self.fresh_bundle()
        bundle["sweeps"][0]["scheduled_due_at"] = bundle["sweeps"][0]["reconstruction_started_at"]
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_false_lateness(self) -> None:
        bundle = self.fresh_bundle()
        bundle["sweeps"][1]["lateness_minutes_at_start"] = 0
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_contemporaneous_claim(self) -> None:
        bundle = self.fresh_bundle()
        bundle["sweeps"][2]["evidence_mode"] = "CONTEMPORANEOUS_EXECUTION"
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_consolidated_sweep(self) -> None:
        bundle = self.fresh_bundle()
        bundle["sweeps"].pop()
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_waiver_or_anchor_reset(self) -> None:
        bundle = self.fresh_bundle()
        bundle["sweeps"][0]["waiver_used"] = True
        bundle["reconciliation"]["disposition"]["cadence_anchor_reset"] = True
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_dispatch_authority_inflation(self) -> None:
        bundle = self.fresh_bundle()
        bundle["reconciliation"]["dispatcher_evidence"]["dispatch_is_not_authority"] = False
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_repository_head_drift(self) -> None:
        bundle = self.fresh_bundle()
        bundle["portfolio"]["repository_inventory"][0]["reconciliation_head"] = "0" * 40
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_p2_erasure(self) -> None:
        bundle = self.fresh_bundle()
        bundle["portfolio"]["findings"]["P2"].pop()
        bundle["reconciliation"]["disposition"]["P2"] = 4
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_pilot_escalation_erasure(self) -> None:
        bundle = self.fresh_bundle()
        bundle["portfolio"]["pilot_escalation"]["required"] = False
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_next_deadline_reset(self) -> None:
        bundle = self.fresh_bundle()
        bundle["reconciliation"]["next_deadlines"]["structural_sweep"] = "2026-08-05T15:57:00-07:00"
        self.assertTrue(self.errors_for(bundle))

    def test_mutation_rejects_claim_inflation(self) -> None:
        bundle = copy.deepcopy(self.fresh_bundle())
        bundle["portfolio"]["claim_boundaries"]["cert_output_issued"] = True
        self.assertTrue(self.errors_for(bundle))


if __name__ == "__main__":
    unittest.main()
