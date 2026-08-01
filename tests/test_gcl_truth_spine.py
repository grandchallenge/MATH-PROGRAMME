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


def errors(registry: dict, matrix: dict) -> list[str]:
    return (
        V.schema_errors(registry, load(REGISTRY_SCHEMA), "registry")
        + V.schema_errors(matrix, load(MATRIX_SCHEMA), "matrix")
        + V.registry_semantic_errors(registry)
        + V.matrix_semantic_errors(matrix, registry)
    )


class TruthSpineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load(REGISTRY)
        self.matrix = load(MATRIX)

    def test_candidate_is_valid_and_nonbinding(self) -> None:
        self.assertEqual(errors(self.registry, self.matrix), [])
        self.assertFalse(self.registry["effective"])
        self.assertFalse(self.registry["promotion_gate"]["may_promote_now"])

    def test_cli_accepts_repository_files(self) -> None:
        self.assertEqual(V.validate(REGISTRY, REGISTRY_SCHEMA, MATRIX, MATRIX_SCHEMA), [])

    def test_exact_sets(self) -> None:
        self.assertEqual({x["record_class_id"] for x in self.registry["record_classes"]}, V.EXPECTED_RECORD_CLASSES)
        self.assertEqual({x["repository"] for x in self.matrix["repositories"]}, V.EXPECTED_REPOSITORIES)

    def assert_rejected(self, registry: dict | None = None, matrix: dict | None = None) -> None:
        self.assertTrue(errors(registry or self.registry, matrix or self.matrix))

    def test_rejects_issue_authority(self) -> None:
        value = copy.deepcopy(self.registry)
        value["authority_precedence"][-1]["may_define_current_state"] = True
        self.assert_rejected(registry=value)

    def test_rejects_precedence_reorder(self) -> None:
        value = copy.deepcopy(self.registry)
        value["authority_precedence"][0], value["authority_precedence"][1] = value["authority_precedence"][1], value["authority_precedence"][0]
        self.assert_rejected(registry=value)

    def test_rejects_missing_or_duplicate_class(self) -> None:
        missing = copy.deepcopy(self.registry)
        missing["record_classes"].pop()
        self.assert_rejected(registry=missing)
        duplicate = copy.deepcopy(self.registry)
        duplicate["record_classes"][-1]["record_class_id"] = duplicate["record_classes"][0]["record_class_id"]
        self.assert_rejected(registry=duplicate)

    def test_rejects_weak_record_semantics(self) -> None:
        value = copy.deepcopy(self.registry)
        value["record_classes"][0]["failure_disposition"] = "WARN"
        self.assert_rejected(registry=value)
        value = copy.deepcopy(self.registry)
        value["record_classes"][0]["supersession_rule"] = ""
        self.assert_rejected(registry=value)

    def test_rejects_aether_dependency_or_exclusive_facts(self) -> None:
        value = copy.deepcopy(self.registry)
        value["future_projection_boundary"]["aether_may_become_required_now"] = True
        self.assert_rejected(registry=value)
        matrix = copy.deepcopy(self.matrix)
        matrix["external_systems"][0]["exclusive_institutional_facts_allowed"] = True
        self.assert_rejected(matrix=matrix)

    def test_rejects_bridge_reactivation(self) -> None:
        value = copy.deepcopy(self.registry)
        value["future_projection_boundary"]["aether_bridge_status"] = "ACTIVE"
        self.assert_rejected(registry=value)

    def test_rejects_missing_repository(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["repositories"].pop()
        self.assert_rejected(matrix=matrix)

    def test_rejects_consumer_override(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["cross_repository_rules"]["consumer_projection_cannot_override_provider_authority"] = False
        self.assert_rejected(matrix=matrix)

    def test_rejects_unknown_class_reference(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["repositories"][0]["consumes_record_classes"].append("shadow_authority")
        self.assert_rejected(matrix=matrix)

    def test_rejects_premature_promotion(self) -> None:
        value = copy.deepcopy(self.registry)
        value["promotion_gate"]["may_promote_now"] = True
        self.assert_rejected(registry=value)

    def test_rejects_claim_inflation(self) -> None:
        value = copy.deepcopy(self.registry)
        value["claim_boundaries"]["commercial_claim_authorized"] = True
        self.assert_rejected(registry=value)


if __name__ == "__main__":
    unittest.main()
