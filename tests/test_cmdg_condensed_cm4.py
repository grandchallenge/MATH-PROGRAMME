import unittest

import ci.validate_cmdg_condensed_cm4 as cm4


class TestCMDGCondensedCM4(unittest.TestCase):
    def test_package(self):
        record = cm4.validate()
        self.assertEqual(record["operation_id"], "CMDG-CONDENSED-CM4-001")
        self.assertEqual(
            record["disposition"],
            "CM4_DEPENDENCY_RECONCILIATION_READY__P3_NEXT_PENDING_PROTECTED_ADMISSION",
        )

    def test_mutations(self):
        cm4.mutation_tests()

    def test_reconciled_dependency_graph(self):
        record = cm4.validate()
        matrix = {row["id"]: row for row in record["prerequisite_matrix"]}
        self.assertEqual(matrix["CM4-P1"]["status"], "AVAILABLE")
        self.assertEqual(matrix["CM4-P2"]["status"], "AVAILABLE")
        self.assertEqual(matrix["CM4-P2"]["route_role"], "PROTECTED_CLOSED")
        self.assertEqual(matrix["CM4-P3"]["status"], "BLOCKING")
        self.assertEqual(matrix["CM4-P3"]["route_role"], "READY_NEXT")
        self.assertEqual(matrix["CM4-P4"]["depends_on"], ["CM4-P5"])
        self.assertEqual(
            matrix["CM4-P5"]["route_role"],
            "SOURCE_ROUTE_PREREQUISITE_FOR_P4",
        )
        self.assertEqual(matrix["CM4-P6"]["depends_on"], ["CM4-P3", "CM4-P4"])

    def test_p3_selected_without_uniqueness_claim(self):
        record = cm4.validate()
        reconciliation = record["dependency_reconciliation"]
        self.assertEqual(reconciliation["selected_next_lane"], "CM4-P3")
        self.assertEqual(
            set(reconciliation["remaining_root_blockers"]),
            {"CM4-P3", "CM4-P5"},
        )
        claims = record["claim_boundary"]
        self.assertFalse(claims["dependency_minimality_claim"])
        self.assertFalse(claims["dependency_uniqueness_claim"])

    def test_theorem_authority_remains_closed(self):
        record = cm4.validate()
        stage = record["stage_a_result"]
        claims = record["claim_boundary"]
        self.assertFalse(stage["theorem_attempt_authorized"])
        self.assertFalse(stage["next_lane_opening_authorized"])
        self.assertFalse(claims["cm4_theorem_certified"])
        self.assertFalse(claims["cm4_protected_closed"])
        self.assertFalse(claims["c06_discharged"])
        self.assertFalse(claims["graph_certified"])
        self.assertFalse(claims["global_cmdg_completeness_claim"])


if __name__ == "__main__":
    unittest.main()
