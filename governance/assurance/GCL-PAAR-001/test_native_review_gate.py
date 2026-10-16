#!/usr/bin/env python3
"""Negative controls for the observed INTELLECT constitutional review gate."""
from __future__ import annotations
import importlib.util
import pathlib
import unittest

MODULE = pathlib.Path(__file__).with_name("replay_baseline.py")
spec = importlib.util.spec_from_file_location("paar_replay_baseline", MODULE)
assert spec and spec.loader
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)

def review_rule(approvals):
    return [{"type": "pull_request",
             "parameters": {"required_approving_review_count": approvals}}]

class NativeReviewGateTests(unittest.TestCase):
    def test_accept_one(self):
        self.assertEqual(replay.enforce_native_review_requirement(review_rule(1)), 1)

    def test_accept_more_than_one(self):
        self.assertEqual(replay.enforce_native_review_requirement(review_rule(2)), 2)

    def test_reject_zero(self):
        with self.assertRaises(ValueError):
            replay.enforce_native_review_requirement(review_rule(0))

    def test_reject_missing_rule(self):
        with self.assertRaises(ValueError):
            replay.enforce_native_review_requirement([{"type": "required_status_checks"}])

    def test_reject_absent_or_invalid_count(self):
        for invalid in (None, True, "1", -1):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                replay.enforce_native_review_requirement(review_rule(invalid))

    def test_reject_untrusted_shape(self):
        with self.assertRaises(ValueError):
            replay.enforce_native_review_requirement({"type":"pull_request"})

if __name__ == "__main__":
    unittest.main()
