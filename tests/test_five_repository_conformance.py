from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "five_repository_conformance", ROOT / "ci" / "five_repository_conformance.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class FiveRepositoryConformanceTests(unittest.TestCase):
    def matrix(self):
        return json.loads(
            (ROOT / "governance" / "five_repository_conformance_matrix.json").read_text(
                encoding="utf-8"
            )
        )

    def test_matrix_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_identity_mismatch_must_remain_zero(self):
        matrix = self.matrix()
        matrix["identity_mismatch_count"] = 1
        self.assertTrue(any("must be zero" in error for error in module.validation_errors(matrix)))

    def test_programme_head_drift_fails(self):
        matrix = self.matrix()
        matrix["repositories"]["math_programme"]["state_commit"] = "0" * 40
        self.assertTrue(any("math_programme head drift" in error for error in module.validation_errors(matrix)))

    def test_cert_registry_drift_fails(self):
        matrix = self.matrix()
        matrix["repositories"]["mathcert"]["route_registry"]["digest"] = "0" * 40
        self.assertTrue(any("Cert registry blob drift" in error for error in module.validation_errors(matrix)))

    def test_intellect_provider_drift_fails(self):
        matrix = self.matrix()
        matrix["repositories"]["intellect"]["current_provider"]["digest"] = "0" * 40
        self.assertTrue(any("INTELLECT current-provider blob drift" in error for error in module.validation_errors(matrix)))

    def test_qualification_cannot_be_presented_as_proof(self):
        matrix = self.matrix()
        matrix["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(any("mathematical_target_proved" in error for error in module.validation_errors(matrix)))

    def test_release_trust_cannot_be_reopened(self):
        matrix = self.matrix()
        matrix["claim_boundaries"]["release_trust_issues_reopened"] = True
        self.assertTrue(any("release_trust_issues_reopened" in error for error in module.validation_errors(matrix)))

    def test_blocker_coverage_cannot_drop_campaign(self):
        matrix = self.matrix()
        del matrix["preserved_blockers"]["OZ-001"]
        self.assertTrue(any("blocker coverage" in error for error in module.validation_errors(matrix)))

    def test_retrospective_closure_set_is_exact(self):
        matrix = self.matrix()
        matrix["tracker_reconciliation"]["mathsolve_retrospective_closed_completed"] = [66, 67, 68]
        self.assertTrue(any("closure set drift" in error for error in module.validation_errors(matrix)))


if __name__ == "__main__":
    unittest.main()
