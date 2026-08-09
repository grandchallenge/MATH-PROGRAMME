import unittest

import ci.validate_cmdg_condensed_cm4_p2 as p2


class TestCMDGCondensedCM4P2(unittest.TestCase):
    def test_package(self):
        record = p2.validate()
        self.assertEqual(record["operation_id"], "CMDG-CONDENSED-CM4-P2-001")
        self.assertEqual(record["disposition"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_mutations(self):
        p2.mutation_tests()

    def test_interface_boundary(self):
        matrix = {row["id"]: row for row in p2.validate()["interface_matrix"]}
        self.assertEqual(matrix["CM4-P2-A"]["status"], "AVAILABLE")
        self.assertEqual(matrix["CM4-P2-B"]["status"], "AVAILABLE")
        self.assertEqual(matrix["CM4-P2-C"]["status"], "AVAILABLE")
        self.assertEqual(matrix["CM4-P2-D"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P2-E"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P2-F"]["status"], "PARTIAL")

    def test_authority_remains_closed(self):
        record = p2.validate()
        self.assertFalse(record["stage_result"]["p2_bridge_closed"])
        claims = record["claim_boundary"]
        self.assertTrue(claims["p2_blocker_characterized"])
        self.assertFalse(claims["p2_closed"])
        self.assertFalse(claims["cm4_theorem_certified"])
        self.assertFalse(claims["p3_closed"])
        self.assertFalse(claims["graph_certified"])

    def test_basis_product_is_not_natural_bridge(self):
        role = p2.validate()["target"]["objectwise_product_role"]
        self.assertIn("noncanonical", role)
        self.assertIn("not a substitute", role)


if __name__ == "__main__":
    unittest.main()
