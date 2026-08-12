import unittest

import ci.validate_cmdg_condensed_cm4_p2 as p2


class TestCMDGCondensedCM4P2(unittest.TestCase):
    def test_package(self):
        record = p2.validate()
        self.assertEqual(record["operation_id"], "CMDG-CONDENSED-CM4-P2-001")
        self.assertEqual(
            record["disposition"],
            "P2_CLOSURE_READY_PENDING_PROTECTED_ADMISSION",
        )

    def test_mutations(self):
        p2.mutation_tests()

    def test_interface_boundary(self):
        matrix = {row["id"]: row for row in p2.validate()["interface_matrix"]}
        for key in ("CM4-P2-A", "CM4-P2-B", "CM4-P2-C", "CM4-P2-D", "CM4-P2-E"):
            self.assertEqual(matrix[key]["status"], "AVAILABLE")
            self.assertEqual(matrix[key]["closure_role"], "REQUIRED")
        self.assertEqual(matrix["CM4-P2-F"]["status"], "PARTIAL")
        self.assertEqual(
            matrix["CM4-P2-F"]["closure_role"],
            "NON_BLOCKING_AUXILIARY",
        )

    def test_reconciled_candidate_without_premature_protected_closure(self):
        record = p2.validate()
        stage = record["stage_result"]
        self.assertTrue(stage["p2_acceptance_reconciled"])
        self.assertTrue(stage["p2_closure_candidate"])
        self.assertFalse(stage["p2_protected_closed"])
        self.assertTrue(stage["canonical_measure_dual_functor_available"])
        self.assertTrue(stage["natural_equivalence_available"])
        self.assertFalse(stage["p2_f_blocks_closure"])

        claims = record["claim_boundary"]
        self.assertTrue(claims["p2_blocker_characterized"])
        self.assertFalse(claims["p2_closed"])
        self.assertFalse(claims["cm4_theorem_certified"])
        self.assertFalse(claims["p3_closed"])
        self.assertFalse(claims["graph_certified"])

    def test_basis_product_is_nonblocking_not_natural_bridge(self):
        record = p2.validate()
        role = record["target"]["objectwise_product_role"]
        self.assertIn("noncanonical", role)
        self.assertIn("not a substitute", role)
        self.assertIn("not an independent CM4-P2 closure requirement", role)

        p2f = {
            row["id"]: row for row in record["interface_matrix"]
        }["CM4-P2-F"]
        self.assertEqual(p2f["closure_role"], "NON_BLOCKING_AUXILIARY")
        self.assertIn("must not be promoted to naturality", p2f["reopen_condition"])


if __name__ == "__main__":
    unittest.main()
