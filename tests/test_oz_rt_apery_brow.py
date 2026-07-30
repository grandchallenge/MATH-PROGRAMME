from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "campaigns/odd_zeta/OZ_RT_APERY_BROW_001/validate.py"
SPEC = importlib.util.spec_from_file_location("oz_rt_apery_brow_validate", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OZRTAperyBrowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for relative in (
            "campaigns/odd_zeta/OZ_RT_APERY_BROW_001",
            "campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER",
            "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE",
        ):
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def load(self, name: str) -> tuple[Path, dict]:
        path = self.root / "campaigns/odd_zeta/OZ_RT_APERY_BROW_001" / name
        return path, yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def write(path: Path, data: dict) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def assert_rejected(self, fragment: str) -> None:
        errors = MODULE.validate(self.root)
        self.assertTrue(errors, "mutated target package was accepted")
        self.assertIn(fragment, "\n".join(errors))

    def test_complete_package_passes(self) -> None:
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_modulus_inflation_is_rejected(self) -> None:
        path, data = self.load("DIRECT_PROOF_AUDIT.yaml")
        data["exact_target"]["modulus"] = "p3"
        self.write(path, data)
        self.assert_rejected("target modulus must remain p")

    def test_double_sum_formalization_inflation_is_rejected(self) -> None:
        path, data = self.load("SEMANTIC_CORRESPONDENCE.yaml")
        data["formalization_boundary"]["double_sum_equivalence_formalized"] = True
        self.write(path, data)
        self.assert_rejected("not kernel-checked")

    def test_missing_proof_step_is_rejected(self) -> None:
        path, data = self.load("DIRECT_PROOF_AUDIT.yaml")
        route = next(item for item in data["proof_routes"] if item["id"] == "OZ-AB-ROUTE-DIRECT")
        route["outline"].pop()
        self.write(path, data)
        self.assert_rejected("proof-step inventory drift")

    def test_source_hash_drift_is_rejected(self) -> None:
        path, data = self.load("LEAN_REPLAY.yaml")
        data["source_files"][0]["sha256"] = "0" * 64
        self.write(path, data)
        self.assert_rejected("Lean source identity mismatch")

    def test_novelty_promotion_is_rejected(self) -> None:
        path, data = self.load("REVIEW_REGISTER.yaml")
        data["disposition_on_success"]["novelty"] = "NEW_AFTER_AUDIT"
        self.write(path, data)
        self.assert_rejected("novelty status drift")

    def test_bridge_discharge_is_rejected(self) -> None:
        path = (
            self.root
            / "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE"
            / "03_IRRATIONALITY_BRIDGE_REGISTER.yaml"
        )
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["bridges"][0]["status"] = "DISCHARGED"
        self.write(path, data)
        self.assert_rejected("must remain open")


if __name__ == "__main__":
    unittest.main()
