#!/usr/bin/env python3
from __future__ import annotations

import unittest

import analyze_wp05


class WP05ReplayTests(unittest.TestCase):
    def test_artifact_replay(self) -> None:
        self.assertEqual([], analyze_wp05.validate())

    def test_terminal_summary(self) -> None:
        summary = analyze_wp05.summary()
        self.assertEqual(8, summary["gauge_invariant_rank"])
        self.assertEqual(3, summary["geometry_only_rank"])
        self.assertEqual(8, summary["calibrated_rank"])
        self.assertEqual(-1, summary["chart_determinant"])
        self.assertEqual(
            "CYCLE_INVARIANT_QUOTIENT_RECONSTRUCTION_PARTIAL",
            summary["terminal_disposition"],
        )


if __name__ == "__main__":
    unittest.main()
