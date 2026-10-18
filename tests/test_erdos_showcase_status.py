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
        self.assertIn(f'{len(admitted):,} reviewed articles', rendered)
        self.assertIn(f'{EXPECTED_COUNT:,} listed problems', rendered)
        self.assertIn(f'Another {counts["drafts"]:,} articles have been written', rendered)
        self.assertIn(f'{counts["reference_only"]:,} problems have catalogue entries', rendered)
        self.assertIn("record of reviewed articles", rendered)
        self.assertIn("not how many mathematical questions have been solved", rendered)

    def test_showcase_marker_and_evidence_links(self):
        source = (ROOT / "docs/SHOWCASE.md").read_text(encoding="utf-8")
        self.assertEqual(source.count(ERDOS_SHOWCASE_MARKER), 1)
        for phrase in (
            "OPENAI_TEN_PROOFS_VERIFICATION.md", "LOG_GCD_PUBLICATION.md",
            "folding mechanisms", "Erdős Compendium",
            "issues/2690", "issues/2698", "pull/2701",
            "CURRENT_WORK.md#vgse-001--mechanical-semantics",
            'id="fixture-003-the-logarithmic-gcd-kernel"',
        ):
            self.assertIn(phrase, source)
        rendered = on_page_markdown(source, SimpleNamespace(
            file=SimpleNamespace(src_uri="SHOWCASE.md")), None, None)
        self.assertNotIn(ERDOS_SHOWCASE_MARKER, rendered)
        self.assertEqual(rendered.count('aria-label="Erdős Compendium progress"'), 1)

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
