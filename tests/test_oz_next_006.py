from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE"
    / "review/OZ_NEXT_006/validation.py"
)
SPEC = importlib.util.spec_from_file_location("oz_next_006_validation", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

BASE_REL = Path("campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE")


class OZNext006Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        target = self.root / BASE_REL
        target.parent.mkdir(parents=True)
        shutil.copytree(ROOT / BASE_REL, target)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def load(self, name: str) -> tuple[Path, dict]:
        path = self.root / BASE_REL / "review/OZ_NEXT_006" / name
        return path, yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def write(path: Path, data: dict) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def assert_rejected(self, fragment: str) -> None:
        errors = MODULE.validate_package(self.root)
        self.assertTrue(errors, "mutated package was accepted")
        self.assertIn(fragment, "\n".join(errors))

    def test_complete_package_passes(self) -> None:
        self.assertEqual(MODULE.validate_package(ROOT), [])

    def test_promotion_inflation_is_rejected(self) -> None:
        path, data = self.load("CLOSURE_REGISTER.yaml")
        data["closure_findings"]["promotion_ready"] = True
        self.write(path, data)
        self.assert_rejected("may not set promotion_ready")

    def test_missing_role_is_rejected(self) -> None:
        path, data = self.load("CLOSURE_REGISTER.yaml")
        data["roles"] = [item for item in data["roles"] if item["role"] != "Adversary"]
        self.write(path, data)
        self.assert_rejected("role set mismatch")

    def test_lane_reordering_is_rejected(self) -> None:
        path, data = self.load("LANE_AUTHORIZATION.yaml")
        data["execution_order"][0], data["execution_order"][1] = (
            data["execution_order"][1],
            data["execution_order"][0],
        )
        self.write(path, data)
        self.assert_rejected("ordered lane sequence drift")

    def test_literature_digest_drift_is_rejected(self) -> None:
        path, data = self.load("SUPPLEMENTAL_LITERATURE_ADMISSION.yaml")
        data["records"][0]["sha256"] = "0" * 64
        self.write(path, data)
        self.assert_rejected("SHA-256 drift")

    def test_bridge_promotion_is_rejected(self) -> None:
        path = self.root / BASE_REL / "03_IRRATIONALITY_BRIDGE_REGISTER.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["bridges"][0]["status"] = "DISCHARGED"
        self.write(path, data)
        self.assert_rejected("must remain OPEN")


if __name__ == "__main__":
    unittest.main()
