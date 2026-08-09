import unittest

import ci.validate_cmdg_condensed_cm4 as cm4


class TestCMDGCondensedCM4(unittest.TestCase):
    def test_package(self):
        record = cm4.validate()
        self.assertEqual(record["operation_id"], "CMDG-CONDENSED-CM4-001")
        self.assertEqual(record["disposition"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_mutations(self):
        cm4.mutation_tests()

    def test_only_nobeling_is_available(self):
        matrix = {row["id"]: row for row in cm4.validate()["prerequisite_matrix"]}
        self.assertEqual(matrix["CM4-P1"]["status"], "AVAILABLE")
        self.assertEqual(matrix["CM4-P2"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P3"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P4"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P5"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P6"]["status"], "PARTIAL_BLOCKING")

    def test_theorem_authority_remains_closed(self):
        claims = cm4.validate()["claim_boundary"]
        self.assertTrue(claims["blocker_characterized"])
        self.assertFalse(claims["cm4_theorem_certified"])
        self.assertFalse(claims["cm4_protected_closed"])
        self.assertFalse(claims["c06_discharged"])
        self.assertFalse(claims["graph_certified"])
        self.assertFalse(claims["global_cmdg_completeness_claim"])


if __name__ == "__main__":
    unittest.main()
