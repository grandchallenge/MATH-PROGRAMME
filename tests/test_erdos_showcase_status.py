#!/usr/bin/env python3
"""The protected Showcase must describe the actual admitted Compendium."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
from erdos_compendium import EDITORIAL, EXPECTED_COUNT, load_batch_admissions
from erdos_compendium_hook import (
    ERDOS_SHOWCASE_MARKER, erdos_showcase_status,
    protected_erdos_counts, on_page_markdown,
)


class ShowcasePublicationTests(unittest.TestCase):
    def test_compendium_partition_exact_and_dynamic(self):
        admitted = load_batch_admissions()
        authored = {int(p.stem) for p in EDITORIAL.glob("[0-9][0-9][0-9][0-9].md")}
        counts = protected_erdos_counts()
        self.assertEqual(counts, {
            "registered": EXPECTED_COUNT, "reviewed": len(admitted),
            "drafts": len(authored - admitted.keys()),
            "reference_only": EXPECTED_COUNT - len(authored),
        })
        rendered = erdos_showcase_status()
        self.assertIn(f'{len(admitted):,} reviewed explainers', rendered)
        self.assertIn(f'{EXPECTED_COUNT:,} registered problems', rendered)
        self.assertIn(f'{counts["drafts"]:,} written drafts', rendered)
        self.assertIn(f'{counts["reference_only"]:,} catalogue-only references', rendered)
        self.assertIn("protected admissions ledger", rendered)
        self.assertIn("not mathematical proof outcomes", rendered)

    def test_showcase_marker_and_evidence_links(self):
        source = (ROOT / "docs/SHOWCASE.md").read_text(encoding="utf-8")
        self.assertEqual(source.count(ERDOS_SHOWCASE_MARKER), 1)
        for phrase in (
            "OpenAI Ten Proofs", "Logarithmic GCD kernel",
            "VGSE-001", "Erdős Compendium",
            "issues/2690", "issues/2698", "pull/2701",
            "CURRENT_WORK.md#vgse-001--mechanical-semantics",
        ):
            self.assertIn(phrase, source)
        rendered = on_page_markdown(source, SimpleNamespace(
            file=SimpleNamespace(src_uri="SHOWCASE.md")), None, None)
        self.assertNotIn(ERDOS_SHOWCASE_MARKER, rendered)
        self.assertEqual(rendered.count('aria-label="Erdős protected publication snapshot"'), 1)

    def test_showcase_marker_fail_closed_and_other_pages_preserved(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri="SHOWCASE.md"))
        for corrupt in ("", ERDOS_SHOWCASE_MARKER * 2):
            with self.assertRaisesRegex(RuntimeError, "requires exactly one"):
                on_page_markdown(corrupt, page, None, None)
        other = SimpleNamespace(file=SimpleNamespace(src_uri="CURRENT_WORK.md"))
        self.assertEqual(on_page_markdown("untouched", other, None, None), "untouched")

    def test_invalid_catalogue_rejected(self):
        with patch("erdos_compendium_hook.load_batch_admissions",
                   return_value={9999: {"source_sha256": "0"*64}}):
            with self.assertRaisesRegex(RuntimeError, "protected catalogue"):
                erdos_showcase_status()


if __name__ == "__main__":
    unittest.main()
