#!/usr/bin/env python3
"""Check that manuscript presence and GitHub merges cannot self-authorize coverage."""
from __future__ import annotations
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from erdos_compendium import EDITORIAL, build, load_admissions, manuscript

REPO = "https://github.com/grandchallenge/MATH-PROGRAMME"

class EditorialGateTests(unittest.TestCase):
    def _build(self, admissions):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            manifest = root / "admissions.json"
            manifest.write_text(json.dumps({
                "record_type": "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/1",
                "admissions": admissions,
            }), encoding="utf-8")
            site = root / "erdos"
            counts = build(output=site, admissions_path=manifest)
            pages = {n: (site / "problems" / f"{n:04d}.md").read_text(encoding="utf-8")
                     for n in (1, 4, 7)}
            index = (site / "catalogue" / "index.md").read_text(encoding="utf-8")
            return counts, pages, index

    def _admission(self, n, sha):
        return {
            "problem_id": n,
            "source_sha256": sha,
            "source_check": REPO + "/issues/2556#issuecomment-6108695648",
            "critical_review": REPO + "/pull/2577#issuecomment-6108689695",
            "protected_admission": REPO + "/pull/2577",
            "mkdocs_run": REPO + "/actions/runs/38137356772",
            "public_html_readback": REPO + "/issues/2552#issuecomment-6109065121",
        }

    def test_merged_drafts_do_not_auto_promote(self):
        counts, pages, index = self._build([])
        self.assertEqual(counts["problems"], 1221)
        self.assertEqual(counts["reviewed"], 0)
        self.assertEqual(counts["legacy"], 3)
        self.assertEqual(counts["editorial"], 5)
        self.assertEqual(counts["pending"], 2)
        self.assertIn("Legacy authored exemplar", pages[1])
        for n in (4, 7):
            self.assertIn("UNACCEPTED DRAFT", pages[n])
            self.assertIn("NOT editorially accepted", pages[n])
            self.assertIn("## The question in plain language", pages[n])
            self.assertIn("## A small example", pages[n])
        self.assertIn("0 separately admitted explanations", index)
        self.assertIn("2 manuscripts pending acceptance", index)

    def test_exact_source_and_evidence_can_admit_only_bounded_article(self):
        text = manuscript(7)
        good_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        counts, pages, _ = self._build([self._admission(7, good_sha)])
        self.assertEqual((counts["reviewed"], counts["editorial"], counts["pending"]), (1, 5, 1))
        self.assertIn("## What is known", pages[7])
        self.assertIn("A **covering system**", pages[7])
        self.assertIn("UNACCEPTED DRAFT", pages[4])
        self.assertNotIn("UNACCEPTED DRAFT", pages[7])

    def test_new_manuscript_rejects_nonportable_github_math_fences(self):
        # Legacy authored sources have a documented, bounded exception;
        # new articles must render correctly on GitHub *and* on MkDocs.
        source = manuscript(7)
        self.assertNotIn(r"\(", source)
        self.assertNotIn(r"\[", source)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "0009.md"
            path.write_text(source + chr(10) + r"\(x\)" + chr(10), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "nonportable GitHub mathematical delimiters"):
                manuscript(9, base=Path(temp))
            path.write_text(source, encoding="utf-8")
            self.assertEqual(manuscript(9, base=Path(temp)), source)

    def test_stale_evidence_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "changed without re-review"):
            self._build([self._admission(7, "0"*64)])

    def test_invalid_evidence_and_duplicate_or_legacy_fail(self):
        sha = hashlib.sha256(manuscript(7).encode("utf-8")).hexdigest()
        bad = self._admission(7, sha)
        bad["public_html_readback"] = "https://example.com/unverified"
        with self.assertRaisesRegex(ValueError, "Invalid public_html_readback"):
            self._build([bad])
        with self.assertRaisesRegex(ValueError, "duplicated"):
            self._build([self._admission(7, sha)] * 2)
        with self.assertRaisesRegex(ValueError, "legacy"):
            self._build([self._admission(1, "a"*64)])

if __name__ == "__main__":
    unittest.main()
