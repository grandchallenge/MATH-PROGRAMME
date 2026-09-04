from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "governance/gcl_tcs_pilots/TCM-C72-INTERFACE-001"
DECL = PKG / "TCM-C72-INTERFACE-001-TCS-PILOT-001.conformance.yaml"
MEAS = PKG / "P04_MEASUREMENT.json"
APPLICATION = PKG / "P04_APPLICATION.md"
SCHEMA = ROOT / "docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-conformance.schema.json"

EXPECTED_APPLICATION_BLOB = "82d7078ab2ada4c817b5dc03b8e4070dbf904cd4"
EXPECTED_SUBJECT_MERGE = "aa53dc3c0e99c39f766f4ccb0c0d0629cd9093db"
EXPECTED_REPORT_BLOB = "929fdf77bb5ea2557e86658d22a0ab9627ce7313"
EXPECTED_MANIFEST_BLOB = "2e0d4747ba055aae840567f38d4f05f8d6778388"
EXPECTED_WORKFLOW_BLOB = "1fcd5fda34a19169db81922abb1f8a12dec1848f"
EXPECTED_CORPUS = "23b49e39eafd70c9619f8837dfcb0046e13a1600cd7176d42a6018814f518050"


class TcmC72P04PilotContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.decl = yaml.safe_load(DECL.read_text(encoding="utf-8"))
        cls.meas = json.loads(MEAS.read_text(encoding="utf-8"))
        cls.application = APPLICATION.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_conformance_schema(self) -> None:
        validator = Draft202012Validator(self.schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(self.decl), key=lambda e: list(e.path))
        self.assertEqual([], [e.message for e in errors])

    def test_candidate_p04_only(self) -> None:
        self.assertEqual("candidate", self.decl["authority_status"])
        self.assertEqual("in_review", self.decl["promotion_status"])
        self.assertEqual("GCL-TCS-P04", self.decl["primary_profile"]["id"])
        self.assertEqual([], self.decl["secondary_profiles"])
        self.assertEqual({"DECLARED"}, set(self.decl["conformance_dimensions"].values()))

    def test_immutable_subject_bindings(self) -> None:
        serialized = json.dumps(self.decl, sort_keys=True) + self.application + json.dumps(self.meas, sort_keys=True)
        for token in [
            EXPECTED_APPLICATION_BLOB,
            EXPECTED_SUBJECT_MERGE,
            EXPECTED_REPORT_BLOB,
            EXPECTED_MANIFEST_BLOB,
            EXPECTED_WORKFLOW_BLOB,
            EXPECTED_CORPUS,
        ]:
            self.assertIn(token, serialized)

    def test_real_subject_not_manufactured(self) -> None:
        subject = self.meas["subject"]
        self.assertTrue(subject["preexisting_real_result"])
        self.assertFalse(subject["created_for_gcl_tcs"])
        self.assertEqual(0, self.meas["burden"]["incremental_scientific_compute"])
        self.assertEqual(0, self.meas["burden"]["scientific_subject_files_modified"])

    def test_finite_positive_and_negative_results_preserved(self) -> None:
        preserved = self.meas["result_preservation"]
        self.assertEqual(329, preserved["frozen_inputs"])
        self.assertEqual(4096, preserved["logical_classes_per_input"])
        self.assertEqual(64, preserved["source_shards"])
        self.assertEqual({"soft_tropical_base_2": 167, "sum_product_bsc_p_0_1": 166, "min_plus_hamming": 152}, preserved["oracle_success"])
        self.assertEqual({"soft_tropical_base_2": 162, "sum_product_bsc_p_0_1": 163, "min_plus_hamming": 177}, preserved["oracle_failure"])
        self.assertEqual(0, preserved["syndrome_inconsistent"])

    def test_p04_coverage_and_plot_boundary(self) -> None:
        coverage = self.meas["p04_coverage"]
        self.assertEqual(11, coverage["mandatory_emphasis_count"])
        self.assertEqual(11, coverage["explicitly_addressed"])
        self.assertEqual("NOT_APPLICABLE__NO_SOURCE_PLOT", coverage["plot_provenance"])
        for heading in [
            "Primary question and alternatives",
            "Target observables",
            "Intervention and controls",
            "Data and model versions",
            "Seeds and environment",
            "Stopping and exclusion rules",
            "Metrics, uncertainty, and sensitivity",
            "Negative and null evidence",
            "Exact execution path",
            "Plot provenance and interpretation limits",
        ]:
            self.assertIn(heading, self.application)

    def test_real_environment_defect_is_not_erased(self) -> None:
        defects = self.meas["defects"]
        self.assertEqual(1, len(defects))
        self.assertEqual("P04-D001", defects[0]["id"])
        self.assertFalse(defects[0]["repair_in_this_pilot"])
        self.assertIn("ubuntu-latest", defects[0]["finding"])
        self.assertIn("P04 defect `P04-D001`", self.application)

    def test_claim_boundary_fails_closed(self) -> None:
        boundary = self.meas["claim_boundary"]
        self.assertTrue(boundary["preserved"])
        for key, value in boundary.items():
            if key == "preserved":
                continue
            self.assertFalse(value, key)
        text = self.application.lower()
        for phrase in ["c90 execution is not authorized", "no family/asymptotic", "hardware-superiority", "qec-circuit-003", "qldpc-forge"]:
            self.assertIn(phrase, text)

    def test_no_promotion_authority(self) -> None:
        boundary = self.meas["authority_boundary"]
        self.assertTrue(all(value is False for value in boundary.values()))
        reviews = {r["gate_id"]: r for r in self.decl["review_register"]}
        self.assertEqual("DEFERRED", reviews["G8"]["decision"])
        self.assertEqual("DEFERRED", reviews["G9"]["decision"])


if __name__ == "__main__":
    unittest.main()
