from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci/validate_cmdg_condensed_cm4_p3.py"
spec = importlib.util.spec_from_file_location("validate_cmdg_condensed_cm4_p3", MODULE_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class TestCMDGCondensedCM4P3(unittest.TestCase):
    def test_record_and_fixture(self):
        validator.validate()

    def test_adversarial_mutations(self):
        validator.mutation_tests()


if __name__ == "__main__":
    unittest.main()