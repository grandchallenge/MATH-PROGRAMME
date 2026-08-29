#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

import validate_programme_math_core as core
import validate_programme_math_core_uc_pilot as pilot


class MathCoreUC001PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = core.load_json(core.CAPABILITY_REGISTRY)
        cls.trace = core.load_json(pilot.PILOT_TRACE)

    def test_real_handoff_pilot_semantics(self) -> None:
        pilot.validate_uc_pilot(self.trace, self.registry)
        state = core.materialize(self.trace["events"])
        self.assertEqual(state["resolved_obligations"][pilot.ROUTE_OBLIGATION], "DISCHARGED")
        self.assertIn(pilot.UNIVERSAL_OBLIGATION, state["open_obligations"])

    def test_universal_bridge_cannot_be_resolved_by_restricted_mapping(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["events"].append(
            {
                "event_id": "MCORE-UC-E-9991",
                "event_type": "RESOLVE_OBLIGATION",
                "producer": {"id": "mathsolve-uc-pilot", "class": "MATHSOLVE", "execution_id": "uc-pilot-negative"},
                "base_checkpoint": copy.deepcopy(trace["base_checkpoint"]),
                "subject": {"kind": "OBLIGATION", "id": pilot.UNIVERSAL_OBLIGATION},
                "scope": {"programme": "MATH-PROGRAMME", "family": "UC-001", "work_package": "MS-UC-WP04", "campaign": "UC-001"},
                "dependencies": [pilot.UNIVERSAL_OBLIGATION, pilot.RESTRICTED_CLAIM, pilot.LEAN_EQUIVALENCE],
                "evidence_refs": ["repo:governance/math_core_01/pilots/UC-001/artifacts/mathcert_theorem_snapshot.json"],
                "payload": {"outcome": "DISCHARGED", "reason": "Negative regression fixture: restricted evidence must not discharge the universal target."},
                "created_at": "2026-08-29T12:31:00Z",
            }
        )
        with self.assertRaises(core.ProtocolError):
            pilot.validate_uc_pilot(trace, self.registry)

    def test_pilot_cannot_manufacture_new_certificate(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["events"].append(
            {
                "event_id": "MCORE-UC-E-9992",
                "event_type": "CERTIFICATE",
                "producer": {"id": "uc-pilot-checker", "class": "CHECKER", "execution_id": "uc-pilot-negative"},
                "base_checkpoint": copy.deepcopy(trace["base_checkpoint"]),
                "subject": {"kind": "CERTIFICATE", "id": "MCORE-UC-K-UNAUTHORIZED-PILOT"},
                "scope": {"programme": "MATH-PROGRAMME", "family": "UC-001", "work_package": "MS-UC-WP04", "campaign": "UC-001"},
                "dependencies": [pilot.RESTRICTED_CLAIM, pilot.LEAN_EQUIVALENCE],
                "evidence_refs": ["repo:governance/math_core_01/pilots/UC-001/artifacts/mathcert_theorem_snapshot.json"],
                "payload": {
                    "target_id": pilot.RESTRICTED_CLAIM,
                    "checker": "negative pilot fixture",
                    "certificate_kind": "INDEPENDENT_REPLAY",
                    "artifact_ref": "repo:governance/math_core_01/pilots/UC-001/artifacts/mathcert_theorem_snapshot.json",
                    "artifact_sha256": "e6ea063fc7f1c5e4be4a0a6aade4e2469db74a7c7498f7f67cde247ccba684e4",
                    "result": "PASS",
                    "ledger_effect": "NONE_DIRECT",
                },
                "created_at": "2026-08-29T12:31:01Z",
            }
        )
        core.validate_trace(trace, self.registry)
        with self.assertRaises(core.ProtocolError):
            pilot.validate_uc_pilot(trace, self.registry)

    def test_formal_mapping_cannot_upgrade_to_mathematical_equivalence(self) -> None:
        trace = copy.deepcopy(self.trace)
        equivalence = next(e for e in trace["events"] if e["subject"]["id"] == pilot.LEAN_EQUIVALENCE)
        equivalence["payload"]["relation_scope"] = "MATHEMATICALLY_EQUIVALENT"
        core.validate_trace(trace, self.registry)
        with self.assertRaises(core.ProtocolError):
            pilot.validate_uc_pilot(trace, self.registry)

    def test_universal_target_must_remain_external_open_reference(self) -> None:
        trace = copy.deepcopy(self.trace)
        universal = next(e for e in trace["events"] if e["subject"]["id"] == pilot.UNIVERSAL_CLAIM)
        universal["payload"]["working_class"] = "LEDGER_PROPOSAL"
        with self.assertRaises(core.ProtocolError):
            pilot.validate_uc_pilot(trace, self.registry)

    def test_external_snapshot_identities_are_pinned(self) -> None:
        pilot.validate_external_snapshots()


if __name__ == "__main__":
    unittest.main()
