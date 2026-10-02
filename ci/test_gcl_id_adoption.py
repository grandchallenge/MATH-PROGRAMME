#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "gcl_id_adoption",
    ROOT / "ci" / "validate_gcl_id_adoption.py",
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def lite_record() -> dict:
    return {
        "$schema": "../../schemas/identifiability_preflight.schema.json",
        "schema_version": "1.0.0",
        "record_type": "GCL_IDENTIFIABILITY_PREFLIGHT",
        "identifier": "TEST-ID-001",
        "work_package": "TEST-WP01",
        "status": "OPEN",
        "standard": "GCL-ID-00",
        "standard_version": "0.1.0",
        "programme_adoption": "governance/GCL-ID-00-ADOPTION.json",
        "level": "ID-PREFLIGHT-LITE",
        "recovery_target": {
            "description": "latent parameter representative",
            "representative_level_claim": True,
        },
        "observation_contract": {
            "solver_observations": ["declared observable y"],
            "side_information": [],
            "training_or_fixture_information_not_available_to_solver": [],
        },
        "observational_equivalence": {
            "known_transformations": [],
            "status": "UNRESOLVED",
        },
        "recoverable_object": {
            "strongest_justified_object": "unresolved pending preflight",
            "classification": "UNRESOLVED",
        },
        "symmetry_breaking": {
            "extra_information_or_normalization_for_stronger_recovery": [],
        },
        "solver_gate": {
            "target_after_preflight": "exploratory inverse probe only",
            "full_representative_recovery_claim_permitted": False,
            "reason": "identifiability unresolved",
        },
        "failure_classification": ["UNRESOLVED"],
        "evidence_refs": [],
        "unresolved_assumptions": ["injectivity not established"],
        "claim_boundaries": {
            "mathematical_certification": False,
            "scientific_claim_promotion": False,
            "publication": False,
            "production_activation": False,
            "commercial_claim": False,
        },
    }


class GCLIDAdoptionTests(unittest.TestCase):
    def test_adoption_and_current_repository_are_valid(self) -> None:
        mod.validate()

    def test_unresolved_lite_preflight_is_valid(self) -> None:
        record = lite_record()
        mod.validate_preflight_object(record)

    def test_absence_of_known_symmetry_cannot_be_used_as_full_identifiability(self) -> None:
        record = lite_record()
        record["observational_equivalence"]["status"] = "NONE_KNOWN_NOT_PROOF_OF_INJECTIVITY"
        record["recoverable_object"]["classification"] = "FULL_IDENTIFIABILITY"
        record["recoverable_object"]["strongest_justified_object"] = "full representative"
        record["solver_gate"]["full_representative_recovery_claim_permitted"] = True
        record["solver_gate"]["reason"] = "no symmetry found"
        record["evidence_refs"] = ["search found no symmetry"]
        with self.assertRaisesRegex(mod.GCLIDAdoptionError, "established injectivity"):
            mod.validate_preflight_object(record)

    def test_structural_ambiguity_cannot_authorize_full_representative_recovery(self) -> None:
        record = lite_record()
        record["observational_equivalence"]["status"] = "NONTRIVIAL_EQUIVALENCE_FOUND"
        record["observational_equivalence"]["known_transformations"] = ["x -> g.x preserves y"]
        record["recoverable_object"]["classification"] = "STRUCTURAL_NON_IDENTIFIABILITY"
        record["recoverable_object"]["strongest_justified_object"] = "equivalence class"
        record["solver_gate"]["full_representative_recovery_claim_permitted"] = True
        record["solver_gate"]["reason"] = "try a stronger optimizer"
        with self.assertRaisesRegex(mod.GCLIDAdoptionError, "full representative recovery"):
            mod.validate_preflight_object(record)

    def test_declared_normalization_can_select_representative(self) -> None:
        record = lite_record()
        record["observational_equivalence"]["status"] = "NONTRIVIAL_EQUIVALENCE_FOUND"
        record["observational_equivalence"]["known_transformations"] = ["scale symmetry"]
        record["recoverable_object"]["classification"] = "IDENTIFIABLE_WITH_DECLARED_NORMALIZATION"
        record["recoverable_object"]["strongest_justified_object"] = "normalized representative"
        record["symmetry_breaking"]["extra_information_or_normalization_for_stronger_recovery"] = ["fix gauge coordinate to 1"]
        record["solver_gate"]["full_representative_recovery_claim_permitted"] = True
        record["solver_gate"]["reason"] = "declared gauge fix selects the representative"
        record["failure_classification"] = ["IDENTIFIABLE_WITH_DECLARED_NORMALIZATION"]
        mod.validate_preflight_object(record)

    def test_full_identifiability_needs_no_failure_label(self) -> None:
        record = lite_record()
        record["observational_equivalence"]["status"] = "INJECTIVITY_ESTABLISHED"
        record["recoverable_object"]["classification"] = "FULL_IDENTIFIABILITY"
        record["recoverable_object"]["strongest_justified_object"] = "full representative"
        record["solver_gate"]["full_representative_recovery_claim_permitted"] = True
        record["solver_gate"]["reason"] = "injectivity established under the declared observation contract"
        record["evidence_refs"] = ["theorem:injectivity"]
        record["failure_classification"] = []
        record["unresolved_assumptions"] = []
        mod.validate_preflight_object(record)

    def test_completed_certified_level_requires_mathcert_reference(self) -> None:
        record = lite_record()
        record["level"] = "ID-CERTIFIED"
        record["status"] = "COMPLETE"
        with self.assertRaisesRegex(mod.GCLIDAdoptionError, "MATHCERT"):
            mod.validate_preflight_object(record)

    def test_review_required_at_twelve_completed_records(self) -> None:
        records = []
        for index in range(12):
            record = lite_record()
            record["identifier"] = f"TEST-ID-{index:03d}"
            record["status"] = "COMPLETE"
            records.append(copy.deepcopy(record))
        with self.assertRaisesRegex(mod.GCLIDAdoptionError, "required no later than 12"):
            mod.validate_review_requirement(records, None)


if __name__ == "__main__":
    unittest.main()
