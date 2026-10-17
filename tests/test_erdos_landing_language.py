#!/usr/bin/env python3
"""Compendium landing page remains readable and grounded in reviewed article records."""
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
    ERDOS_LANDING_MARKER, protected_erdos_counts,
    erdos_landing_status, on_page_markdown
)


class CompendiumLandingTests(unittest.TestCase):
    def test_current_counts_from_reviewed_articles(self):
        admitted = load_batch_admissions()
        authored = {int(p.stem) for p in EDITORIAL.glob("[0-9][0-9][0-9][0-9].md")}
        counts = protected_erdos_counts()
        self.assertEqual(counts["registered"], EXPECTED_COUNT)
        self.assertEqual(counts["reviewed"], len(admitted))
        self.assertEqual(counts["drafts"], len(authored - admitted.keys()))
        self.assertEqual(counts["reference_only"], EXPECTED_COUNT - len(authored))
        paragraph = erdos_landing_status()
        for expected in (
            f'{len(admitted):,} reviewed articles',
            f'{counts["registered"]:,} listed problems',
            f'Another {counts["drafts"]:,} articles have been written',
            f'For {counts["reference_only"]:,} other problems',
            "They count articles, not mathematical problems solved",
            "reviewed-article records",
        ):
            self.assertIn(expected, paragraph)

    def test_reader_friendly_article_links_and_status_distinctions(self):
        text = (ROOT / "docs/erdos/index.md").read_text(encoding="utf-8")
        self.assertEqual(text.count(ERDOS_LANDING_MARKER), 1)
        for n in (1, 2, 3, 7, 665, 836):
            self.assertIn(
                f'https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/{n:04d}/',
                text
            )
        for phrase in (
            "A collection of mathematical questions",
            "Three problems worth exploring",
            "What you will find in an article",
            "How current is the information",
            "reviewed article means",
            "does **not** mean",
            "a status shown in a catalogue entry may reflect an earlier point in time",
        ):
            self.assertIn(phrase, text)
        for legacy in ("evidence level", "triage classes", "Forge → Solve → Cert",
                       "documentary reference annex", "frozen statuses",
                       "protected source snapshot", "MATHSOLVE campaign ledger"):
            self.assertNotIn(legacy, text)
        rendered = on_page_markdown(
            text, SimpleNamespace(file=SimpleNamespace(src_uri="erdos/index.md")),
            None, None
        )
        self.assertNotIn(ERDOS_LANDING_MARKER, rendered)
        self.assertEqual(rendered.count('aria-label="Erdős Compendium article progress"'), 1)

    def test_wrong_marker_rejected_without_affecting_other_pages(self):
        entry = SimpleNamespace(file=SimpleNamespace(src_uri="erdos/index.md"))
        for bad in ("no marker", ERDOS_LANDING_MARKER * 2):
            with self.assertRaisesRegex(RuntimeError, "requires exactly one"):
                on_page_markdown(bad, entry, None, None)
        other = SimpleNamespace(file=SimpleNamespace(src_uri="erdos/problems/0007.md"))
        self.assertEqual(on_page_markdown("untouched", other, None, None), "untouched")

    def test_invalid_reviewed_article_register_fails_closed(self):
        with patch("erdos_compendium_hook.load_batch_admissions",
                   return_value={9999: {"source_sha256": "0"*64}}):
            with self.assertRaisesRegex(RuntimeError, "protected catalogue"):
                erdos_landing_status()


if __name__ == "__main__":
    unittest.main()
