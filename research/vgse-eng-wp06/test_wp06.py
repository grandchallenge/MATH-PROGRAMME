#!/usr/bin/env python3
import unittest
import analyze_wp06

class WP06Tests(unittest.TestCase):
    def test_replay(self):
        self.assertEqual([], analyze_wp06.validate())

    def test_rank(self):
        a=analyze_wp06.load("QUOTIENT_ACTION.json")
        self.assertEqual(5, analyze_wp06.rank(a["matrix"]))
        self.assertEqual(1, a["kernel_dimension"])

    def test_terminal_candidate(self):
        r=analyze_wp06.load("RESULTS.json")
        self.assertEqual("BOUNDARY_CALIBRATION_FIVE_DIMENSIONAL_OBSTRUCTION",r["terminal_candidate"])
        self.assertEqual(8,r["source_defined_t_embedding"]["recovered_rank"])
        self.assertEqual(3,r["broader_algebraic_realization_class"]["geometry_only_identifiable_rank"])

if __name__=="__main__":
    unittest.main()
