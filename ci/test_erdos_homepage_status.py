#!/usr/bin/env python3
"""Public homepage source/visual status must reflect protected editorial state."""
from __future__ import annotations
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from erdos_compendium import EDITORIAL, EXPECTED_COUNT, load_batch_admissions
from erdos_compendium_hook import (
    ERDOS_HOME_MARKER, erdos_home_status, on_page_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "docs/index.md"


class HomepageCompendiumTests(unittest.TestCase):
    def test_build_counters_match_current_protected_admissions(self):
        published = load_batch_admissions()
        drafted_ids = {int(x.stem) for x in
                       EDITORIAL.glob("[0-9][0-9][0-9][0-9].md")}
        rendered = erdos_home_status()
        self.assertEqual(EXPECTED_COUNT, 1221)
        self.assertEqual(len(published) + len(drafted_ids - published.keys())
                         + EXPECTED_COUNT - len(drafted_ids), 1221)
        self.assertEqual(rendered.count('class="home-erdos-stat"'), 4)
        for number in (
            EXPECTED_COUNT, len(published),
            len(drafted_ids - published.keys()),
            EXPECTED_COUNT - len(drafted_ids),
        ):
            self.assertRegex(rendered, rf"<strong>{number:,}</strong>")
        self.assertIn("not an independently certified theorem", rendered)
        for target in ("issues/2690", "issues/2698", "EDITORIAL_ADMISSIONS.json"):
            self.assertIn(target, rendered)

    def test_index_injects_one_panel_only_and_has_direct_navigation(self):
        source = HOME.read_text(encoding="utf-8")
        self.assertEqual(source.count(ERDOS_HOME_MARKER), 1)
        self.assertIn('href="erdos/"', source)
        rendered = on_page_markdown(source, SimpleNamespace(
            file=SimpleNamespace(src_uri="index.md")), None, None)
        self.assertNotIn(ERDOS_HOME_MARKER, rendered)
        self.assertEqual(rendered.count('class="home-erdos-status"'), 1)
        self.assertIn("Erdős Compendium — the public reference", rendered)
        self.assertIn("(erdos/catalogue/index.md)", rendered)
        self.assertEqual(
            on_page_markdown(source, SimpleNamespace(
                file=SimpleNamespace(src_uri="CURRENT_WORK.md")), None, None),
            source,
        )

    def test_marker_fail_closed(self):
        p = SimpleNamespace(file=SimpleNamespace(src_uri="index.md"))
        for raw in ("missing marker", ERDOS_HOME_MARKER * 2):
            with self.assertRaisesRegex(RuntimeError, "exactly one status marker"):
                on_page_markdown(raw, p, None, None)

    def test_invalid_source_authority_fails_closed(self):
        with patch("erdos_compendium_hook.load_batch_admissions",
                   return_value={9999: {"source_sha256": "0"*64}}):
            with self.assertRaisesRegex(RuntimeError, "count disagrees"):
                erdos_home_status()

    def test_responsive_style_is_present(self):
        css = (ROOT / "docs/stylesheets/home.css").read_text()
        for marker in (
            ".home-erdos-status__stats",
            ".home-erdos-stat__label",
            "@media (max-width: 980px)",
            "@media (max-width: 490px)",
        ):
            self.assertIn(marker, css)


if __name__ == "__main__":
    unittest.main()
