#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("vgse_ms_m0",ROOT/"analyze_m0.py")
assert SPEC and SPEC.loader
m=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)

class VGSEMSM0Tests(unittest.TestCase):
    def test_graph_hypotheses(self) -> None:
        h=m.graph_hypotheses()
        self.assertEqual(h["matching_count"],31)
        self.assertEqual(h["kmin"],2)
        self.assertTrue(h["two_boundary_nondegenerate"])

    def test_baseline_full_t_embedding_replay(self) -> None:
        result=m.construct(m.BASELINE)
        self.assertEqual(result["selector_status"],"FOUND")
        self.assertTrue(result["valid_numerical_t_embedding"])
        metrics=result["metrics"]
        self.assertTrue(metrics["te2_all_convex"])
        self.assertTrue(metrics["te2_common_orientation"])
        self.assertEqual(metrics["nonadjacent_crossing_count"],0)
        self.assertLess(metrics["te3_max_relative_gauge_error"],m.TOL["te3"])
        self.assertLess(metrics["te4_max_angle_residual"],m.TOL["te4"])
        self.assertGreater(metrics["te5_min_angle_margin"],m.TOL["te5_margin"])

    def test_baseline_nonuniqueness_falsification(self) -> None:
        branches=m.multiple_baseline_branches()
        self.assertGreaterEqual(len(branches),5)
        self.assertTrue(all(row["valid_numerical_t_embedding"] for row in branches))
        signatures=[row["boundary_shape_signature"] for row in branches]
        self.assertGreater(
            min(
                max(abs(a-b) for a,b in zip(signatures[i],signatures[j]))
                for i in range(len(signatures)) for j in range(i+1,len(signatures))
            ),
            1e-4,
        )

    def test_retained_atlas_replay(self) -> None:
        generated=m.artifacts(m.build())
        m.validate_retained(generated)

if __name__=="__main__":
    unittest.main()
