"""Regression contract for EC-BULK-005 source-level mathematical typography.

Inspects only 20 non-admitted drafts. Does not change editorial admission,
mathematical status or any historical source-return record.
"""
from __future__ import annotations
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COHORT = ROOT / "governance/erdos_compendium/batches/EC-BULK-005.json"
MANUSCRIPTS = ROOT / "governance/erdos_compendium/editorial"
LEDGER = ROOT / "governance/erdos_compendium/EDITORIAL_ADMISSIONS.json"
TARGETS = frozenset({702, 714, 716, 718, 719, 722, 725, 730, 731, 732,
                     734, 743, 744, 747, 764, 814, 827, 831, 837, 840})
TEX_TOKENS = re.compile(r"(?s)\$\$.*?\$\$|\$[^\n$]*\$")
PLAIN_FORMULA = re.compile(r"\bbinom\(|\bex_r\(|\bex_3\(|\bΣ_[a-z]")

class EC005Typography(unittest.TestCase):
    def test_original_provenance_and_twenty_draft_hashes(self):
        manifest = json.loads(COHORT.read_text(encoding="utf-8"))
        items = {e["problem_id"]: e for e in manifest["items"]}
        admitted = json.loads(LEDGER.read_text(encoding="utf-8"))
        accepted = {e["problem_id"] for batch in admitted["batches"]
                    for e in batch["entries"]}
        self.assertEqual(len(TARGETS), 20)
        self.assertTrue(TARGETS <= set(items))
        self.assertFalse(TARGETS & accepted, "Amended an already-admitted article")
        self.assertTrue({765, 836} <= accepted)
        for n in TARGETS:
            with self.subTest(problem=n):
                e = items[n]
                self.assertEqual(e["audit_issue"] > 0, True)
                self.assertTrue(e["source_return"].startswith(
                    "https://github.com/grandchallenge/MATH-PROGRAMME/issues/"
                    + str(e["audit_issue"]) + "#issuecomment-"))
                source = (MANUSCRIPTS / f"{n:04d}.md").read_bytes()
                self.assertEqual(hashlib.sha256(source).hexdigest(), e["draft_sha256"])
                self.assertIn(e["source_return"].encode(), source)
                self.assertEqual(source.count(b"## "), 6)

    def test_math_syntax_and_no_unrendered_formula_prose(self):
        for n in TARGETS:
            with self.subTest(problem=n):
                text = (MANUSCRIPTS / f"{n:04d}.md").read_text(encoding="utf-8")
                matches = list(TEX_TOKENS.finditer(text))
                self.assertGreater(len(matches), 0, f"Missing math inputs #{n}")
                self.assertEqual(text.count("$") % 2, 0)
                self.assertFalse(any("$$" in line and line.strip() != "$$"
                                     for line in text.splitlines()))
                plain = TEX_TOKENS.sub("", text)
                plain = re.sub(r"\]\([^)]+\)", "](URL)", plain)
                self.assertIsNone(PLAIN_FORMULA.search(plain),
                                  f"Unformatted formula in #{n}")
