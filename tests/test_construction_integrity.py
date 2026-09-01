from __future__ import annotations

import copy
import unittest

from ci.construction_integrity import (
    ConstructionIntegrityError,
    classify_legacy_pr,
    preflight,
    transaction_spec,
    validate_contract,
)

PRED = "1" * 40
OLD = "2" * 40
NEW = "3" * 40
OTHER = "4" * 40

TARGET = {
    "target_id": "TEST-STAGE-001",
    "authorized_predecessor": PRED,
    "lifecycle_state": "DEVELOPMENT",
    "development_ref": "refs/heads/gcl/dev/test-stage-001",
    "candidate_ref": "refs/heads/gcl/candidate/test-stage-001",
    "allowed_paths": ["campaigns/test/contract.json", "campaigns/test/impl.py"],
    "allowed_path_prefixes": ["tests/test_stage_"],
    "forbidden_path_patterns": [r"/SUCCESSOR_", r"T3_999_"],
    "deny_update_when_exact_head_evidence_exists": True,
}

CONTRACT = {
    "schema_version": "1.0.0",
    "control_id": "MP-CONSTRUCTION-INTEGRITY-001",
    "issue": 634,
    "state": "ACTIVE",
    "repository": "grandchallenge/MATH-PROGRAMME",
    "protected_branch": "main",
    "authority_source": "PROTECTED_MAIN_ONLY",
    "mutation_protocol": "ATOMIC_REF_COMPARE_AND_SWAP_V1",
    "namespaces": {
        "development": "refs/heads/gcl/dev/",
        "candidate": "refs/heads/gcl/candidate/",
    },
    "frozen_candidate_updates_allowed": False,
    "force_ref_updates_allowed": False,
    "operator_supplied_authority_allowed": False,
    "activation_requirements": {},
    "targets": [TARGET],
    "estate_classification": {},
    "claim_boundaries": {"mathematical_target_proved": False},
}


def update_observation():
    return {
        "repository": "grandchallenge/MATH-PROGRAMME",
        "repository_id": "R_123",
        "protected_branch": "main",
        "ref": TARGET["development_ref"],
        "ref_exists": True,
        "candidate_ref_exists": False,
        "current_head": OLD,
        "proposed_head": NEW,
        "predecessor_exists": True,
        "predecessor_is_ancestor": True,
        "merge_base": PRED,
        "changed_paths": ["campaigns/test/contract.json", "tests/test_stage_gate.py"],
        "exact_head_evidence_exists": False,
        "force_requested": False,
    }


class ConstructionIntegrityTests(unittest.TestCase):
    def test_contract_is_valid(self):
        self.assertEqual(validate_contract(CONTRACT), [])

    def test_control_must_be_active(self):
        contract = copy.deepcopy(CONTRACT)
        contract["state"] = "PROPOSED_NOT_ACTIVE"
        decision = preflight(contract, TARGET["target_id"], "UPDATE_DEVELOPMENT", update_observation())
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.code, "CONTROL_NOT_ACTIVE")

    def test_unknown_target_denied(self):
        decision = preflight(CONTRACT, "NOPE", "UPDATE_DEVELOPMENT", update_observation())
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.code, "MISSING_TARGET_AUTHORITY")

    def test_clean_update_allowed(self):
        self.assertTrue(preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", update_observation()).allowed)

    def test_wrong_predecessor_denied(self):
        observation = update_observation()
        observation["merge_base"] = OTHER
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        self.assertFalse(decision.allowed)
        self.assertIn("merge base is not the authorized predecessor", decision.reasons)

    def test_non_ancestor_denied(self):
        observation = update_observation()
        observation["predecessor_is_ancestor"] = False
        self.assertFalse(preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation).allowed)

    def test_missing_predecessor_denied_without_crash(self):
        observation = update_observation()
        observation["predecessor_exists"] = False
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        self.assertFalse(decision.allowed)
        self.assertIn("authorized predecessor does not exist", decision.reasons)

    def test_path_widening_denied(self):
        observation = update_observation()
        observation["changed_paths"].append("governance/unrelated.json")
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        self.assertFalse(decision.allowed)
        self.assertTrue(any("path scope widened" in reason for reason in decision.reasons))

    def test_successor_contamination_denied_even_if_prefix_allowed(self):
        contract = copy.deepcopy(CONTRACT)
        contract["targets"][0]["allowed_path_prefixes"].append("campaigns/test/")
        observation = update_observation()
        observation["changed_paths"].append("campaigns/test/SUCCESSOR_D.py")
        decision = preflight(contract, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        self.assertFalse(decision.allowed)
        self.assertTrue(any("forbidden governed paths" in reason for reason in decision.reasons))

    def test_exact_head_invalidation_denied(self):
        observation = update_observation()
        observation["exact_head_evidence_exists"] = True
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        self.assertFalse(decision.allowed)
        self.assertIn("update would invalidate exact-head evidence", decision.reasons)

    def test_candidate_ref_presence_freezes_development(self):
        observation = update_observation()
        observation["candidate_ref_exists"] = True
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        self.assertFalse(decision.allowed)
        self.assertIn("candidate ref already exists; development is frozen", decision.reasons)

    def test_frozen_lifecycle_is_immutable(self):
        contract = copy.deepcopy(CONTRACT)
        contract["targets"][0]["lifecycle_state"] = "FROZEN_CANDIDATE"
        self.assertFalse(preflight(contract, TARGET["target_id"], "UPDATE_DEVELOPMENT", update_observation()).allowed)

    def test_force_update_denied(self):
        observation = update_observation()
        observation["force_requested"] = True
        self.assertFalse(preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation).allowed)

    def test_create_development_must_start_at_predecessor(self):
        observation = {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "repository_id": "R_123",
            "protected_branch": "main",
            "ref": TARGET["development_ref"],
            "ref_exists": False,
            "current_head": "",
            "proposed_head": PRED,
            "predecessor_exists": True,
            "force_requested": False,
        }
        self.assertTrue(preflight(CONTRACT, TARGET["target_id"], "CREATE_DEVELOPMENT", observation).allowed)
        observation["proposed_head"] = NEW
        self.assertFalse(preflight(CONTRACT, TARGET["target_id"], "CREATE_DEVELOPMENT", observation).allowed)

    def test_freeze_is_exact_snapshot(self):
        observation = update_observation()
        observation.update({
            "ref": TARGET["candidate_ref"],
            "candidate_ref_exists": False,
            "development_head": NEW,
            "proposed_head": NEW,
        })
        self.assertTrue(preflight(CONTRACT, TARGET["target_id"], "FREEZE_CANDIDATE", observation).allowed)
        observation["proposed_head"] = OTHER
        self.assertFalse(preflight(CONTRACT, TARGET["target_id"], "FREEZE_CANDIDATE", observation).allowed)

    def test_second_freeze_denied(self):
        observation = update_observation()
        observation.update({
            "ref": TARGET["candidate_ref"],
            "candidate_ref_exists": True,
            "development_head": NEW,
            "proposed_head": NEW,
        })
        self.assertFalse(preflight(CONTRACT, TARGET["target_id"], "FREEZE_CANDIDATE", observation).allowed)

    def test_update_transaction_has_before_oid_and_no_force(self):
        observation = update_observation()
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        update = transaction_spec(decision, observation)["refUpdates"][0]
        self.assertEqual(update["name"], TARGET["development_ref"])
        self.assertEqual(update["beforeOid"], OLD)
        self.assertEqual(update["afterOid"], NEW)
        self.assertFalse(update["force"])

    def test_denied_transaction_cannot_be_built(self):
        observation = update_observation()
        observation["exact_head_evidence_exists"] = True
        decision = preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation)
        with self.assertRaises(ConstructionIntegrityError):
            transaction_spec(decision, observation)

    def test_create_transaction_is_atomic_create_if_absent(self):
        observation = {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "repository_id": "R_123",
            "protected_branch": "main",
            "ref": TARGET["development_ref"],
            "ref_exists": False,
            "current_head": "",
            "proposed_head": PRED,
            "predecessor_exists": True,
            "force_requested": False,
        }
        decision = preflight(CONTRACT, TARGET["target_id"], "CREATE_DEVELOPMENT", observation)
        update = transaction_spec(decision, observation)["refUpdates"][0]
        self.assertEqual(update["name"], TARGET["development_ref"])
        self.assertEqual(update["beforeOid"], "0" * 40)
        self.assertEqual(update["afterOid"], PRED)
        self.assertFalse(update["force"])

    def test_unrelated_protected_main_movement_is_not_a_sync_requirement(self):
        observation = update_observation()
        observation["protected_head"] = OTHER
        self.assertTrue(preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation).allowed)

    def test_operator_cannot_override_protected_authority(self):
        observation = update_observation()
        observation["authorized_predecessor"] = OTHER
        observation["allowed_paths"] = ["governance/unrelated.json"]
        self.assertTrue(preflight(CONTRACT, TARGET["target_id"], "UPDATE_DEVELOPMENT", observation).allowed)

    def test_legacy_clean(self):
        self.assertEqual(classify_legacy_pr(CONTRACT, TARGET["target_id"], update_observation())["classification"], "LEGACY_CLEAN")

    def test_legacy_reconstruction_required(self):
        observation = update_observation()
        observation["changed_paths"].append("governance/unrelated.json")
        self.assertEqual(classify_legacy_pr(CONTRACT, TARGET["target_id"], observation)["classification"], "LEGACY_REQUIRES_RECONSTRUCTION")

    def test_legacy_outside_scope(self):
        self.assertEqual(classify_legacy_pr(CONTRACT, "NOPE", update_observation())["classification"], "OUTSIDE_GOVERNED_SCOPE")


if __name__ == "__main__":
    unittest.main()
