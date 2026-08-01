from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "gcl_truth_spine_registry.json"
REGISTRY_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_registry.schema.json"
MATRIX = ROOT / "governance" / "cross_repository_authority_matrix.json"
MATRIX_SCHEMA = ROOT / "schemas" / "cross_repository_authority_matrix.schema.json"
DESIGNATION = ROOT / "governance" / "gcl_delegated_referee_office.json"
DESIGNATION_SCHEMA = ROOT / "schemas" / "gcl_delegated_referee_office.schema.json"
STEWARD = ROOT / "governance" / "gcl_truth_spine_steward_release.json"
STEWARD_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_steward_release.schema.json"
REFEREE = ROOT / "governance" / "gcl_truth_spine_referee_review.json"
REFEREE_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_referee_review.schema.json"
PROMOTION = ROOT / "governance" / "gcl_truth_spine_promotion_record.json"
PROMOTION_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_promotion_record.schema.json"
VALIDATOR_PATH = ROOT / "ci" / "validate_gcl_truth_spine.py"


def load_module():
    spec = importlib.util.spec_from_file_location("truth_spine_validator", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = load_module()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def core_errors(registry: dict, matrix: dict) -> list[str]:
    return (
        V.schema_errors(registry, load(REGISTRY_SCHEMA), "registry")
        + V.schema_errors(matrix, load(MATRIX_SCHEMA), "matrix")
        + V.registry_semantic_errors(registry)
        + V.matrix_semantic_errors(matrix, registry)
    )


def envelope_errors(
    designation: dict,
    steward: dict,
    referee: dict,
    promotion: dict,
    registry: dict,
) -> list[str]:
    return (
        V.schema_errors(designation, load(DESIGNATION_SCHEMA), "designation")
        + V.schema_errors(steward, load(STEWARD_SCHEMA), "steward")
        + V.schema_errors(referee, load(REFEREE_SCHEMA), "referee")
        + V.schema_errors(promotion, load(PROMOTION_SCHEMA), "promotion")
        + V.designation_semantic_errors(designation)
        + V.steward_semantic_errors(steward)
        + V.referee_semantic_errors(referee, designation)
        + V.promotion_semantic_errors(
            promotion, registry, designation, steward, referee, ROOT
        )
    )


class TruthSpineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load(REGISTRY)
        self.matrix = load(MATRIX)
        self.designation = load(DESIGNATION)
        self.steward = load(STEWARD)
        self.referee = load(REFEREE)
        self.promotion = load(PROMOTION)

    def test_candidate_and_review_envelope_are_valid(self) -> None:
        self.assertEqual(core_errors(self.registry, self.matrix), [])
        self.assertEqual(
            envelope_errors(
                self.designation,
                self.steward,
                self.referee,
                self.promotion,
                self.registry,
            ),
            [],
        )
        self.assertFalse(self.registry["effective"])
        self.assertFalse(self.promotion["effective_before_protected_merge"])
        self.assertTrue(
            self.promotion["gate_disposition"][
                "may_merge_when_branch_protection_is_satisfied"
            ]
        )

    def test_cli_accepts_repository_files(self) -> None:
        self.assertEqual(V.validate(REGISTRY, REGISTRY_SCHEMA, MATRIX, MATRIX_SCHEMA), [])

    def test_exact_sets(self) -> None:
        self.assertEqual(
            {x["record_class_id"] for x in self.registry["record_classes"]},
            V.EXPECTED_RECORD_CLASSES,
        )
        self.assertEqual(
            {x["repository"] for x in self.matrix["repositories"]},
            V.EXPECTED_REPOSITORIES,
        )

    def assert_core_rejected(
        self, registry: dict | None = None, matrix: dict | None = None
    ) -> None:
        self.assertTrue(core_errors(registry or self.registry, matrix or self.matrix))

    def assert_envelope_rejected(
        self,
        designation: dict | None = None,
        steward: dict | None = None,
        referee: dict | None = None,
        promotion: dict | None = None,
    ) -> None:
        self.assertTrue(
            envelope_errors(
                designation or self.designation,
                steward or self.steward,
                referee or self.referee,
                promotion or self.promotion,
                self.registry,
            )
        )

    def test_rejects_issue_authority(self) -> None:
        value = copy.deepcopy(self.registry)
        value["authority_precedence"][-1]["may_define_current_state"] = True
        self.assert_core_rejected(registry=value)

    def test_rejects_precedence_reorder(self) -> None:
        value = copy.deepcopy(self.registry)
        value["authority_precedence"][0], value["authority_precedence"][1] = (
            value["authority_precedence"][1],
            value["authority_precedence"][0],
        )
        self.assert_core_rejected(registry=value)

    def test_rejects_missing_or_duplicate_class(self) -> None:
        missing = copy.deepcopy(self.registry)
        missing["record_classes"].pop()
        self.assert_core_rejected(registry=missing)
        duplicate = copy.deepcopy(self.registry)
        duplicate["record_classes"][-1]["record_class_id"] = duplicate[
            "record_classes"
        ][0]["record_class_id"]
        self.assert_core_rejected(registry=duplicate)

    def test_rejects_weak_record_semantics(self) -> None:
        value = copy.deepcopy(self.registry)
        value["record_classes"][0]["failure_disposition"] = "WARN"
        self.assert_core_rejected(registry=value)
        value = copy.deepcopy(self.registry)
        value["record_classes"][0]["supersession_rule"] = ""
        self.assert_core_rejected(registry=value)

    def test_rejects_aether_dependency_or_exclusive_facts(self) -> None:
        value = copy.deepcopy(self.registry)
        value["future_projection_boundary"]["aether_may_become_required_now"] = True
        self.assert_core_rejected(registry=value)
        matrix = copy.deepcopy(self.matrix)
        matrix["external_systems"][0]["exclusive_institutional_facts_allowed"] = True
        self.assert_core_rejected(matrix=matrix)

    def test_rejects_bridge_reactivation(self) -> None:
        value = copy.deepcopy(self.registry)
        value["future_projection_boundary"]["aether_bridge_status"] = "ACTIVE"
        self.assert_core_rejected(registry=value)

    def test_rejects_missing_repository(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["repositories"].pop()
        self.assert_core_rejected(matrix=matrix)

    def test_rejects_consumer_override(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["cross_repository_rules"][
            "consumer_projection_cannot_override_provider_authority"
        ] = False
        self.assert_core_rejected(matrix=matrix)

    def test_rejects_unknown_class_reference(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["repositories"][0]["consumes_record_classes"].append(
            "shadow_authority"
        )
        self.assert_core_rejected(matrix=matrix)

    def test_rejects_mutating_embedded_candidate_gate(self) -> None:
        value = copy.deepcopy(self.registry)
        value["promotion_gate"]["human_steward_release_complete"] = True
        self.assert_core_rejected(registry=value)

    def test_rejects_claim_inflation(self) -> None:
        value = copy.deepcopy(self.registry)
        value["claim_boundaries"]["commercial_claim_authorized"] = True
        self.assert_core_rejected(registry=value)

    def test_rejects_referee_blanket_or_fiat_authority(self) -> None:
        designation = copy.deepcopy(self.designation)
        designation["operating_rules"][
            "standing_designation_is_not_blanket_approval"
        ] = False
        self.assert_envelope_rejected(designation=designation)
        designation = copy.deepcopy(self.designation)
        designation["operating_rules"][
            "claim_promotion_by_referee_fiat_prohibited"
        ] = False
        self.assert_envelope_rejected(designation=designation)

    def test_rejects_steward_semantic_change_delegation(self) -> None:
        steward = copy.deepcopy(self.steward)
        steward["administrative_effectuation_authority"][
            "semantic_change_to_approved_subject_permitted"
        ] = True
        self.assert_envelope_rejected(steward=steward)

    def test_rejects_steward_subject_drift(self) -> None:
        steward = copy.deepcopy(self.steward)
        steward["subject_commit"] = "0" * 40
        self.assert_envelope_rejected(steward=steward)

    def test_rejects_inaccurate_referee_independence(self) -> None:
        referee = copy.deepcopy(self.referee)
        referee["independence_disclosure"][
            "model_or_provider_separate_from_authoring_assistant"
        ] = True
        self.assert_envelope_rejected(referee=referee)

    def test_rejects_referee_blocker_or_subject_edit(self) -> None:
        referee = copy.deepcopy(self.referee)
        referee["blocking_findings_remaining"] = True
        self.assert_envelope_rejected(referee=referee)
        referee = copy.deepcopy(self.referee)
        referee["independence_disclosure"][
            "reviewer_modified_reviewed_subject_after_assignment"
        ] = True
        self.assert_envelope_rejected(referee=referee)

    def test_rejects_comment_only_activation(self) -> None:
        promotion = copy.deepcopy(self.promotion)
        promotion["activation"]["issue_or_pr_comment_alone_can_activate"] = True
        self.assert_envelope_rejected(promotion=promotion)

    def test_rejects_disabled_final_head_or_protected_merge_gate(self) -> None:
        promotion = copy.deepcopy(self.promotion)
        promotion["gate_disposition"]["final_pr_head_required_checks_must_pass"] = False
        self.assert_envelope_rejected(promotion=promotion)
        promotion = copy.deepcopy(self.promotion)
        promotion["gate_disposition"]["protected_merge_required"] = False
        self.assert_envelope_rejected(promotion=promotion)

    def test_rejects_semantic_artifact_identity_drift(self) -> None:
        promotion = copy.deepcopy(self.promotion)
        promotion["preserved_semantic_artifacts"][0]["blob"] = "0" * 40
        self.assert_envelope_rejected(promotion=promotion)

    def test_rejects_promotion_claim_inflation(self) -> None:
        promotion = copy.deepcopy(self.promotion)
        promotion["claim_boundaries"]["commercial_claim_authorized"] = True
        self.assert_envelope_rejected(promotion=promotion)


if __name__ == "__main__":
    unittest.main()
