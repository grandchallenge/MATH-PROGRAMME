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


if __name__ == "__main__":
    unittest.main()
