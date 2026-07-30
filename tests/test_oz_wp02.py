from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER/validate.py"
SPEC = importlib.util.spec_from_file_location("oz_wp02_validate", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OZWP02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for relative in (
            "campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER",
            "campaigns/odd_zeta/OZ_WP01_FALSE_PROOF_ATLAS",
            "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/03_IRRATIONALITY_BRIDGE_REGISTER.yaml",
        ):
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def load(self, name: str) -> tuple[Path, dict]:
        path = self.root / "campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER" / name
        return path, yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def write(path: Path, data: dict) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def assert_rejected(self, fragment: str) -> None:
        errors = MODULE.validate(self.root)
        self.assertTrue(errors, "mutated ledger was accepted")
        self.assertIn(fragment, "\n".join(errors))

    def test_complete_ledger_passes(self) -> None:
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_finite_claim_inflation_is_rejected(self) -> None:
        path, data = self.load("THEOREM_LEDGER.yaml")
        theorem = next(item for item in data["theorems"] if item["id"] == "OZ-THM-T003")
        theorem["disposition"] = "SOURCE_PROOF_PRESENT_INDEPENDENT_REVIEW_OPEN"
        self.write(path, data)
        self.assert_rejected("multi-digit theorem must remain finite evidence")

    def test_factor_six_loss_is_rejected(self) -> None:
        path, data = self.load("NORMALIZATION_REGISTER.yaml")
        data["required_equivalence"] = "B_n = bMin_n"
        self.write(path, data)
        self.assert_rejected("factor-six equivalence missing")

    def test_dependency_cycle_is_rejected(self) -> None:
        path, data = self.load("PROOF_OBLIGATIONS.yaml")
        first = next(item for item in data["obligations"] if item["id"] == "OZ-OBL-AB-001")
        first["dependencies"] = ["OZ-OBL-AB-012"]
        self.write(path, data)
        self.assert_rejected("dependency cycle")

    def test_next_lane_inflation_is_rejected(self) -> None:
        path, data = self.load("THEOREM_LEDGER.yaml")
        data["next_executable_lane"] = "OZ-RT-LB-INSTANCE-001"
        self.write(path, data)
        self.assert_rejected("next lane must be Apéry B-row")

    def test_false_novelty_is_rejected(self) -> None:
        path, data = self.load("THEOREM_LEDGER.yaml")
        theorem = next(item for item in data["theorems"] if item["id"] == "OZ-THM-T002")
        theorem["novelty_status"] = "NEW_AFTER_AUDIT"
        self.write(path, data)
        self.assert_rejected("novelty inflation")

    def test_sharp12_blocker_discharge_is_rejected(self) -> None:
        path, data = self.load("PROOF_OBLIGATIONS.yaml")
        obligation = next(item for item in data["obligations"] if item["id"] == "OZ-OBL-SH-003")
        obligation["status"] = "SATISFIED"
        self.write(path, data)
        self.assert_rejected("premature discharge")


if __name__ == "__main__":
    unittest.main()
