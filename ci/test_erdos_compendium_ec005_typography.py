"""Regression contract for EC-BULK-005 source-level mathematical typography.

Inspects 20 typography-corrected source articles. Protected R6 admitted #814,
while R7 proposes #718, #722 and #747. Historical typography evidence persists.
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
    def test_original_provenance_and_twenty_source_hashes(self):
        manifest = json.loads(COHORT.read_text(encoding="utf-8"))
        items = {e["problem_id"]: e for e in manifest["items"]}
        admitted = json.loads(LEDGER.read_text(encoding="utf-8"))
        accepted = {e["problem_id"] for batch in admitted["batches"]
                    for e in batch["entries"]}
        self.assertEqual(len(TARGETS), 20)
        self.assertTrue(TARGETS <= set(items))
        self.assertEqual(TARGETS & accepted, {814, 718, 722, 747, 744} | {827, 837, 743, 840, 714, 716, 719, 731, 764, 734, 831}, "Only exact R6/R7/R8 entries admitted among typography targets")
        r6=next(b for b in admitted["batches"] if b["batch_id"]=="EC-BULK-005-R6")
        self.assertEqual([e["problem_id"] for e in r6["entries"] if e["problem_id"] in TARGETS],[814])
        r7=next(b for b in admitted["batches"] if b["batch_id"]=="EC-BULK-005-R7")
        self.assertEqual([e["problem_id"] for e in r7["entries"] if e["problem_id"] in TARGETS],[718,722,747])
        r8=next(b for b in admitted["batches"] if b["batch_id"]=="EC-BULK-005-R8")
        self.assertEqual([e["problem_id"] for e in r8["entries"] if e["problem_id"] in TARGETS],[744])
        r9=next(b for b in admitted["batches"] if b["batch_id"]=="EC-BULK-005-R9-80")
        self.assertEqual([e["problem_id"] for e in r9["entries"] if e["problem_id"] in TARGETS],[714, 716, 719, 731, 734, 743, 764, 827, 831, 837, 840])
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
                # GitHub math rendering fails when empty lines separate a
                # display delimiter from its actual mathematical content.
                lines = text.splitlines()
                block_open = False
                for i, line in enumerate(lines):
                    if line.strip() == "$$":
                        if not block_open:
                            self.assertLess(i + 1, len(lines))
                            self.assertTrue(lines[i + 1].strip(),
                                            f"Blank after display opener #{n}")
                        else:
                            self.assertTrue(lines[i - 1].strip(),
                                            f"Blank before display closer #{n}")
                        block_open = not block_open
                self.assertFalse(block_open)
                # GitHub math rendering fails when empty lines separate a
                # display delimiter from its actual mathematical content.
                lines = text.splitlines()
                block_open = False
                for i, line in enumerate(lines):
                    if line.strip() == "$$":
                        if not block_open:
                            self.assertLess(i + 1, len(lines))
                            self.assertTrue(lines[i + 1].strip(),
                                            f"Blank after display opener #{n}")
                        else:
                            self.assertTrue(lines[i - 1].strip(),
                                            f"Blank before display closer #{n}")
                        block_open = not block_open
                self.assertFalse(block_open)
                plain = TEX_TOKENS.sub("", text)
                plain = re.sub(r"\]\([^)]+\)", "](URL)", plain)
                self.assertIsNone(PLAIN_FORMULA.search(plain),
                                  f"Unformatted formula in #{n}")
