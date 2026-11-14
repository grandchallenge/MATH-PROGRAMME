#!/usr/bin/env python3
"""Guard the exceptional, source-hash-bound editorial promotion of Erdős #1.

This does not certify the mathematics or promote other legacy exemplars.
"""
import json
import tempfile
import unittest
from pathlib import Path

from erdos_compendium import LEGACY_EXEMPLARS, LEGACY_PROMOTION_SHA256, load_admissions

PIN = "64026cab37a6ba0bbe18d154ad64b38fe311d933dd0804e2c1a3414a9802cf78"

def row(n, digest=PIN):
    return {
        "problem_id": n,
        "source_sha256": digest,
        "source_check": "https://github.com/grandchallenge/MATH-PROGRAMME/issues/1270#issuecomment-6249309294",
        "critical_review": "https://github.com/grandchallenge/MATH-PROGRAMME/issues/3251#issuecomment-6877698802",
        "protected_admission": "https://github.com/grandchallenge/MATH-PROGRAMME/pull/3327",
        "mkdocs_run": "https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43591663103",
        "public_html_readback": "https://github.com/grandchallenge/MATH-PROGRAMME/issues/3251#issuecomment-6877705279",
    }

def accept(rows):
    with tempfile.TemporaryDirectory() as t:
        p = Path(t)/"admissions.json"
        p.write_text(json.dumps({"record_type": "ERDOS_COMPENDIUM_EDITORIAL_ADMISSIONS/1",
                                 "admissions": rows}))
        return load_admissions(p)

class LegacyPromotionTests(unittest.TestCase):
    def test_only_one_legacy_promotion_whitelisted(self):
        self.assertEqual(LEGACY_EXEMPLARS, frozenset({1,2,3}))
        self.assertEqual(LEGACY_PROMOTION_SHA256, {1: PIN})

    def test_correctly_reviewed_exact_manuscript_is_eligible(self):
        self.assertEqual(accept([row(1)])[1]["source_sha256"], PIN)

    def test_change_one_byte_or_hash_must_reject(self):
        with self.assertRaises(ValueError):
            accept([row(1, "f"*64)])

    def test_legacy_two_and_three_remain_excluded(self):
        for n in (2,3):
            with self.subTest(problem=n), self.assertRaises(ValueError):
                accept([row(n)])

    def test_duplicate_one_fails_closed(self):
        with self.assertRaises(ValueError):
            accept([row(1),row(1)])

    def test_missing_critical_review_fails_closed(self):
        x = row(1)
        x.pop("critical_review")
        with self.assertRaises(ValueError):
            accept([x])

    def test_missing_public_readback_fails_closed(self):
        x = row(1)
        x.pop("public_html_readback")
        with self.assertRaises(ValueError):
            accept([x])

    def test_invalid_source_review_url_fails_closed(self):
        x = row(1)
        x["source_check"] = "https://not-your-source.example"
        with self.assertRaises(ValueError):
            accept([x])

    def test_disallow_unsigned_review_token(self):
        x = row(1)
        x["critical_review"] = "UNREVIEWED"
        with self.assertRaises(ValueError):
            accept([x])

if __name__=="__main__":
    unittest.main()
