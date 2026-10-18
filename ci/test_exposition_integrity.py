#!/usr/bin/env python3
"""Mutation checks for structural guide and semantic chronology guards."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from validate_accessible_research_guides import validate_text
from validate_exposition_integrity import errors as integrity_errors
from replay_accessible_guide_fixtures import OUTPUTS, replay

ROOT = Path(__file__).resolve().parents[1]
UC = "docs/domains/UC_001_RESEARCH_GUIDE.md"


class ExpositionMutationTests(unittest.TestCase):
    def test_baseline_guides(self):
        self.assertEqual(validate_text((ROOT / UC).read_text(), UC), [])

    def test_missing_worked_example_rejected(self):
        text = (ROOT / UC).read_text().replace("**Friendly example.**", "Example.")
        self.assertTrue(any("friendly worked" in x for x in validate_text(text, UC)))

    def test_missing_fixture_output_rejected(self):
        text = (ROOT / UC).read_text().replace("# Expected:", "# Omitted:", 1)
        self.assertTrue(any("expected output" in x for x in validate_text(text, UC)))

    def test_missing_guide_section_rejected(self):
        text = (ROOT / UC).read_text().replace("## Challenge ladder", "## Another section", 1)
        self.assertTrue(any("Challenge ladder" in x for x in validate_text(text, UC)))

    def test_wrong_fixture_result_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in OUTPUTS:
                dst = root / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, dst)
            p = root / UC
            source = p.read_text()
            self.assertIn("counts = {x: sum(x in a for a in F) for x in support}", source)
            p.write_text(source.replace(
                "counts = {x: sum(x in a for a in F) for x in support}",
                "counts = {x: 0 for x in support}", 1))
            self.assertTrue(any(UC in x and "mismatch" in x for x in replay(root)))

    def test_removed_empty_support_guard_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                "docs/documentaries/union_closed.md",
                "docs/documentaries/union_closed.edition.json",
                "docs/domains/union_closed.md",
                "docs/documentaries/DOCUMENTARY_CANDIDATES.json",
                "docs/documentaries/ARTIFACT_MANIFEST.json",
                "docs/EUCLID_GCD_E2E_001_PROOF_TRACE.md",
                "governance/euclid_gcd_e2e_001_closeout.json",
                "governance/research_surfaces.json",
            ]
            for name in paths:
                dst = root / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, dst)
            self.assertEqual(integrity_errors(root), [])
            p = root / "docs/documentaries/union_closed.md"
            p.write_text(p.read_text().replace("empty-only family", "unexplained edge case"))
            self.assertTrue(any("empty-support" in x for x in integrity_errors(root)))


if __name__ == "__main__":
    unittest.main()
