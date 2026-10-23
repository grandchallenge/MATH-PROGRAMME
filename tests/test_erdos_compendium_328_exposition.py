"""Admitted #328 recovered exposition: exact-hash positive/hostile regression.

These tests verify custody and renderer admission, not mathematical certification.
"""
from __future__ import annotations

import json
import hashlib
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import erdos_compendium as ec

PREVIOUS_SHA = "7ad120af1caf9020990a709e8d4bdb0cdee51682a53991011cf8ca215241c28c"
REVISED_SHA = "f870262c3507edcc30075a524847b75b77241ebc2f0675c382615c7e53717c7e"


class RecoveredErdos328Admission(unittest.TestCase):
    def test_exact_historical_custody_and_accepted_revision(self):
        history = json.loads(ec.ACCEPTANCE.read_text(encoding="utf-8"))
        batch = next(b for b in history["batches"] if b["batch_id"] == "EC-BULK-003")
        original = next(e for e in batch["entries"] if e["problem_id"] == 328)
        self.assertEqual(original["source_sha256"], PREVIOUS_SHA)
        accepted = ec.load_batch_admissions()
        self.assertEqual(len(accepted), 650)
        self.assertEqual(accepted[328]["source_sha256"], REVISED_SHA)
        self.assertEqual(accepted[328]["exposition_amendment_id"], "EC-328-ORDERED-C2-20261022")
        self.assertEqual(
            hashlib.sha256(ec.manuscript(328).encode("utf-8")).hexdigest(),
            REVISED_SHA,
        )

    def test_unreviewed_manuscript_mutation_fails_closed(self):
        original = ec.manuscript

        def altered(problem_id, *args, **kwargs):
            body = original(problem_id, *args, **kwargs)
            return body + "\nUNREVIEWED_EDIT\n" if problem_id == 328 else body

        with mock.patch.object(ec, "manuscript", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "unreviewed #328"):
                ec.load_batch_admissions()

    def test_candidate_rewrites_protected_pr_identity_fails_closed(self):
        loads = json.loads

        def forged(data, *args, **kwargs):
            parsed = loads(data, *args, **kwargs)
            if isinstance(parsed, dict) and parsed.get("revision_id") == "EC-328-ORDERED-C2-20261022":
                parsed["protected_patch"] = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/99999"
            return parsed

        with mock.patch.object(ec.json, "loads", side_effect=forged):
            with self.assertRaisesRegex(ValueError, "Invalid #328 exposition amendment authority"):
                ec.load_batch_admissions()


    def test_ordered_binary_representations_finite_smoke(self):
        from collections import Counter
        from itertools import product
        for m in range(1, 13):
            a = [1 << j for j in range(m)]
            counts = Counter(x + y for x in a for y in a)
            self.assertLessEqual(max(counts.values()), 2)
        # In every 2-coloring of 5 elements, and every 3-coloring
        # of 6 elements, a color class has two different members.
        for m, colors in ((5, 2), (6, 3)):
            a = [1 << j for j in range(m)]
            for assignment in product(range(colors), repeat=m):
                self.assertTrue(any(
                    sum(assignment[j] == k for j in range(m)) >= 2
                    for k in range(colors)
                ))
        # These computations corroborate, but cannot prove, infinitude.



if __name__ == "__main__":
    unittest.main()
