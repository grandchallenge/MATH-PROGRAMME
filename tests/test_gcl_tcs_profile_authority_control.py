from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from ci.gcl_tcs_profile_authority_control import MAP_PATH, ROOT, validate_profile_authority_map


class GclTcsProfileAuthorityControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = json.loads((ROOT / MAP_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))

    def validate(self, mapping):
        return validate_profile_authority_map(mapping, root=ROOT)

    def test_canonical_map_passes(self):
        self.assertEqual(self.validate(copy.deepcopy(self.canonical)), [])

    def test_missing_profile_fails_closed(self):
        candidate = copy.deepcopy(self.canonical)
        del candidate["profiles"]["GCL-TCS-P04"]
        self.assertIn("map: profile_set_mismatch", self.validate(candidate))

    def test_extra_profile_fails_closed(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P08"] = copy.deepcopy(candidate["profiles"]["GCL-TCS-P07"])
        self.assertIn("map: profile_set_mismatch", self.validate(candidate))

    def test_profile_version_drift_fails_closed(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P03"]["version"] = "1.0.0"
        self.assertIn("GCL-TCS-P03: version_drift", self.validate(candidate))

    def test_non_steward_lifecycle_owner_fails_closed(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P05"]["profile_lifecycle_owner_role"] = "Mechanist"
        self.assertIn("GCL-TCS-P05: lifecycle_owner_must_be_Steward", self.validate(candidate))

    def test_profile_must_not_preassign_artifact_owner(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["authority_semantics"]["artifact_owner_fixed_by_profile"] = True
        self.assertIn("authority_semantics: artifact_owner_must_not_be_fixed", self.validate(candidate))

    def test_profile_must_not_replace_artifact_owner(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P01"]["artifact_owner_binding"] = "Steward"
        self.assertIn("GCL-TCS-P01: artifact_owner_binding_invalid", self.validate(candidate))

    def test_mapping_cannot_become_authority_registry(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["authority_semantics"]["mapping_is_authority_registry"] = True
        self.assertIn("authority_semantics: mapping_is_authority_registry_must_be_false", self.validate(candidate))

    def test_mapping_cannot_confer_authority_by_role_name(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["authority_semantics"]["mapping_confers_authority_by_role_name"] = True
        self.assertIn("authority_semantics: mapping_confers_authority_by_role_name_must_be_false", self.validate(candidate))

    def test_mapping_cannot_activate_promotion_gate(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["authority_semantics"]["mapping_activates_promotion_gate"] = True
        self.assertIn("authority_semantics: mapping_activates_promotion_gate_must_be_false", self.validate(candidate))

    def test_unknown_review_role_fails_closed(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P02"]["gates"]["G5"]["review_roles"].append("NewConstitutionalOffice")
        self.assertIn("GCL-TCS-P02/G5: unknown_review_role:NewConstitutionalOffice", self.validate(candidate))

    def test_unknown_conditional_role_fails_closed(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P01"]["gates"]["G5"]["conditional_domain_roles"] = ["NewSpecialistOffice"]
        self.assertIn("GCL-TCS-P01/G5: unknown_conditional_role:NewSpecialistOffice", self.validate(candidate))

    def test_gate_mode_must_match_existing_policy_matrix(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P06"]["gates"]["G5"]["mode"] = "required"
        self.assertIn("GCL-TCS-P06/G5: mode_mismatch", self.validate(candidate))

    def test_g1_must_preserve_artifact_owner_requirement(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P07"]["gates"]["G1"]["artifact_owner_required"] = False
        self.assertIn("GCL-TCS-P07/G1: artifact_owner_must_remain_required", self.validate(candidate))

    def test_g8_referee_mapping_is_promotion_only(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["profiles"]["GCL-TCS-P04"]["gates"]["G8"]["promotion_only"] = False
        self.assertIn("GCL-TCS-P04/G8: promotion_only_required", self.validate(candidate))

    def test_boundary_cannot_claim_constitutional_authority(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["boundary"]["constitutional_authority_created"] = True
        self.assertIn("boundary: constitutional_authority_created_must_be_false", self.validate(candidate))

    def test_boundary_cannot_claim_standard_promotion(self):
        candidate = copy.deepcopy(self.canonical)
        candidate["boundary"]["promotion_requested"] = True
        self.assertIn("boundary: promotion_requested_must_be_false", self.validate(candidate))


if __name__ == "__main__":
    unittest.main()
