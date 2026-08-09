import unittest

import ci.validate_cmdg_condensed_cm4_p2_d as p2d


class TestCMDGCondensedCM4P2D(unittest.TestCase):
    def test_package(self):
        record = p2d.validate()
        self.assertEqual(record["operation_id"], "CMDG-CONDENSED-CM4-P2-D-001")
        self.assertEqual(record["disposition"], "P2_D_RECONSTRUCTED_PENDING_PROTECTED_ADMISSION")

    def test_mutations(self):
        p2d.mutation_tests()

    def test_canonical_functor_candidate(self):
        record = p2d.validate()
        construction = record["construction"]
        self.assertFalse(construction["basis_dependency"])
        self.assertFalse(construction["objectwise_product_definition"])
        self.assertEqual(
            construction["variance"],
            "COVARIANT_PROFINITE_BY_PULLBACK_THEN_INTERNAL_HOM_PRECOMPOSITION",
        )
        self.assertIn("measureFunctor", construction["condensed_functor"])
        self.assertIn("dualityHomEquiv", construction["duality_interface"])

    def test_p2_e_remains_unavailable(self):
        record = p2d.validate()
        self.assertTrue(record["stage_result"]["p2_d_candidate_reconstructed"])
        self.assertFalse(record["stage_result"]["p2_d_protected_available"])
        self.assertFalse(record["stage_result"]["p2_e_available"])
        self.assertFalse(record["claim_boundary"]["p2_e_natural_equivalence_established"])
        self.assertFalse(record["claim_boundary"]["p2_closed"])

    def test_source_concordance_preserves_canonicality(self):
        source = p2d.validate()["source_concordance"]
        self.assertTrue(source["product_after_basis_only"])
        self.assertIn("basis-free", source["interpretation"])
        self.assertIn("noncanonical", source["interpretation"])


if __name__ == "__main__":
    unittest.main()
