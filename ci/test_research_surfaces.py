#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_research_surfaces", ROOT / "ci/validate_research_surfaces.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class ResearchSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "governance/research_surfaces.json").read_text())

    def test_current_registry_valid(self):
        self.assertEqual(MOD.validate(copy.deepcopy(self.data)), [])

    def test_duplicate_campaign_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["surfaces"].append(copy.deepcopy(bad["surfaces"][0]))
        self.assertTrue(any("duplicate campaign_id" in e or "schema:" in e for e in MOD.validate(bad)))

    def test_missing_authority_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["surfaces"][0]["authority"]["records"] = ["governance/DOES_NOT_EXIST.json"]
        self.assertTrue(any("authority record missing" in e for e in MOD.validate(bad)))

    def test_issue_cannot_confer_certification(self):
        bad = copy.deepcopy(self.data)
        bad["surfaces"][0]["claim_boundary"]["issue_confers_certification"] = True
        self.assertTrue(any("schema:" in e for e in MOD.validate(bad)))

    def test_active_governed_campaign_coverage_is_fail_closed(self):
        bad = copy.deepcopy(self.data)
        bad["surfaces"] = [row for row in bad["surfaces"] if row["campaign_id"] != "OZ-001"]
        self.assertTrue(any("active governed campaign missing research surface: OZ-001" in e for e in MOD.validate(bad)))

    def test_live_child_exposition_drift_rejected_for_present_guide(self):
        bad = copy.deepcopy(self.data)
        row = next(r for r in bad["surfaces"] if r["campaign_id"] == "OPENMATH-2026")
        row["live"]["active_children"] = ["https://github.com/grandchallenge/MATHSOLVE/issues/999999"]
        self.assertTrue(any("mature exposition missing active child tracker" in e for e in MOD.validate(bad)))

    def test_authority_exposition_drift_rejected_for_present_guide(self):
        bad = copy.deepcopy(self.data)
        row = next(r for r in bad["surfaces"] if r["campaign_id"] == "OPENMATH-2026")
        row["authority"]["records"].append("AGENTS.md")
        self.assertTrue(any("mature exposition missing registered authority record AGENTS.md" in e for e in MOD.validate(bad)))

    def test_terminal_lifecycle_conflict_detected(self):
        row = copy.deepcopy(next(r for r in self.data["surfaces"] if r["campaign_id"] == "OPENMATH-2026"))
        row["lifecycle"] = "TERMINAL"
        errors = MOD._mature_exposition_relation_errors(row, "**Programme state:** active research", "")
        self.assertTrue(any("terminal lifecycle conflicts" in e for e in errors))

    def test_exposition_cannot_confer_certification(self):
        row = copy.deepcopy(next(r for r in self.data["surfaces"] if r["campaign_id"] == "OPENMATH-2026"))
        errors = MOD._mature_exposition_relation_errors(row, "", "This guide certifies the result.")
        self.assertTrue(any("attempts to confer certification authority" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
