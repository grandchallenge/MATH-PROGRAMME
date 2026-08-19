from __future__ import annotations

import hashlib
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci/validate_cmdg_condensed_cm4_p3.py"
P3E_PATH = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3E.lean"
P3E_BLOB = "596d601b6056f2f45b7780fc693f091549c2b316"
spec = importlib.util.spec_from_file_location("validate_cmdg_condensed_cm4_p3", MODULE_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


class TestCMDGCondensedCM4P3(unittest.TestCase):
    def test_record_and_fixture(self):
        validator.validate()

    def test_adversarial_mutations(self):
        validator.mutation_tests()

    def test_p3e_exact_source_boundary(self):
        data = P3E_PATH.read_bytes()
        self.assertEqual(git_blob_sha(data), P3E_BLOB)
        text = data.decode("utf-8")
        for snippet in (
            "finiteCoefficientFamilyConeIsLimit",
            "finiteMeasure_isSolid_of_coefficient",
            "measureFunctor_isSolid_of_coefficient",
            "profiniteSolid_isSolid_of_coefficient",
            "residualHomTheorem_of_coefficientResidual",
            "CoefficientResidualHomTheorem",
        ):
            self.assertIn(snippet, text)
        lowered = text.lower()
        for forbidden in ("sorry", "axiom ", "unsafe ", "implemented_by"):
            self.assertNotIn(forbidden, lowered)
        self.assertNotIn("instance ", lowered)


if __name__ == "__main__":
    unittest.main()
