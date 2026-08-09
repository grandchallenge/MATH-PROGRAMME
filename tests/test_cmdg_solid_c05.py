import unittest

import ci.validate_cmdg_solid_c05 as c05

class TestCMDGSolidC05(unittest.TestCase):
    def test_package(self):
        self.assertEqual(c05.validate()["operation_id"], "CMDG-SOLID-C05-001")

    def test_mutations(self):
        c05.mutation_tests()

    def test_general_equivalence_is_not_claimed(self):
        record = c05.validate()
        self.assertFalse(record["claim_boundary"]["pinned_reconstructed_equivalence_conferred"])
        self.assertTrue(any(row["relationship"] == "UNPROVED_EQUIVALENCE" for row in record["concordance_matrix"]))

    def test_noncommutative_general_ring_out_of_scope(self):
        record = c05.validate()
        self.assertFalse(record["claim_boundary"]["noncommutative_general_ring_reconstruction_conferred"])
        self.assertTrue(any(row["layer"] == "NONCOMMUTATIVE_GENERAL_RING" and row["relationship"] == "OUT_OF_SCOPE" for row in record["concordance_matrix"]))

if __name__ == "__main__":
    unittest.main()
