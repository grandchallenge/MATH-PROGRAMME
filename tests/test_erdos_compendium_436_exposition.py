"""Admitted #436 recovered exposition: exact-hash positive/hostile regression.

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

PREVIOUS_SHA = "cbe761face26845a4c13c447b110a0f0bb693e4b0fe7f17530c272faf4125569"
REVISED_SHA = "ebdf77de6dc30bc3100000cce92e3fc217fddbf4a84ac951ccd4faaed0adc24a"


class RecoveredErdos436Admission(unittest.TestCase):
    def test_exact_historical_custody_and_accepted_revision(self):
        history = json.loads(ec.ACCEPTANCE.read_text(encoding="utf-8"))
        batch = next(b for b in history["batches"] if b["batch_id"] == "EC-BULK-003")
        original = next(e for e in batch["entries"] if e["problem_id"] == 436)
        self.assertEqual(original["source_sha256"], PREVIOUS_SHA)
        accepted = ec.load_batch_admissions()
        self.assertEqual(len(accepted), 650)
        self.assertEqual(accepted[436]["source_sha256"], REVISED_SHA)
        self.assertEqual(accepted[436]["exposition_amendment_id"], "EC-436-QRPAIR-20261022")
        self.assertEqual(
            hashlib.sha256(ec.manuscript(436).encode("utf-8")).hexdigest(),
            REVISED_SHA,
        )

    def test_unreviewed_manuscript_mutation_fails_closed(self):
        original = ec.manuscript

        def altered(problem_id, *args, **kwargs):
            body = original(problem_id, *args, **kwargs)
            return body + "\nUNREVIEWED_EDIT\n" if problem_id == 436 else body

        with mock.patch.object(ec, "manuscript", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "unreviewed #436"):
                ec.load_batch_admissions()

    def test_candidate_rewrites_protected_pr_identity_fails_closed(self):
        loads = json.loads

        def forged(data, *args, **kwargs):
            parsed = loads(data, *args, **kwargs)
            if isinstance(parsed, dict) and parsed.get("revision_id") == "EC-436-QRPAIR-20261022":
                parsed["protected_patch"] = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/99999"
            return parsed

        with mock.patch.object(ec.json, "loads", side_effect=forged):
            with self.assertRaisesRegex(ValueError, "Invalid #436 exposition amendment authority"):
                ec.load_batch_admissions()


if __name__ == "__main__":
    unittest.main()
