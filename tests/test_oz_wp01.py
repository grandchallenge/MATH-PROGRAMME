from __future__ import annotations

import copy
import importlib
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "campaigns/odd_zeta/OZ_WP01_FALSE_PROOF_ATLAS"
sys.path.insert(0, str(PACKAGE))
REPLAY = importlib.import_module("replay")


class OZWP01Tests(unittest.TestCase):
    def load(self) -> dict:
        return yaml.safe_load((PACKAGE / "ATLAS.yaml").read_text(encoding="utf-8"))

    def run_mutation(self, data: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ATLAS.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            return REPLAY.replay(path)

    def test_complete_atlas_passes(self) -> None:
        self.assertEqual(REPLAY.replay(), [])

    def test_promotion_inflation_is_rejected(self) -> None:
        data = self.load()
        case = next(item for item in data["cases"] if item["id"] == "OZ-FPA-P005")
        case["packet"]["novelty_claim"] = "NEW_AFTER_AUDIT"
        errors = self.run_mutation(data)
        self.assertTrue(any("verdict REJECT" in error for error in errors))

    def test_missing_family_is_rejected(self) -> None:
        data = self.load()
        data["cases"] = [item for item in data["cases"] if item["family"] != "ZETA7_OPERATOR"]
        errors = self.run_mutation(data)
        self.assertTrue(any("missing controlled families" in error for error in errors))

    def test_duplicate_case_id_is_rejected(self) -> None:
        data = self.load()
        duplicate = copy.deepcopy(data["cases"][0])
        data["cases"].append(duplicate)
        errors = self.run_mutation(data)
        self.assertIn("duplicate case IDs", errors)

    def test_reason_code_omission_is_rejected(self) -> None:
        data = self.load()
        data["required_reason_codes"].remove("FINITE_TO_UNBOUNDED")
        errors = self.run_mutation(data)
        self.assertTrue(any("reason-code coverage mismatch" in error for error in errors))

    def test_finite_evidence_does_not_support_unbounded_claim(self) -> None:
        reasons = REPLAY.evaluate({"claim_scope": "unbounded", "evidence_scope": "finite"})
        self.assertIn("FINITE_TO_UNBOUNDED", reasons)


if __name__ == "__main__":
    unittest.main()
