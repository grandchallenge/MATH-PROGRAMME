from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class T3010BCorrectionRankTests(unittest.TestCase):
    def test_exact_rank_classification_and_firewall(self):
        producer = load_module("t3_010_b", CAMPAIGN / "t3_010_b.py")
        verifier = load_module("verify_t3_010_b", CAMPAIGN / "verify_t3_010_b.py")
        contract = json.loads((CAMPAIGN / "T3_010_B_CONTRACT.json").read_text())

        # Exact-Q rank semantics: unique, affine, and inconsistent are distinct.
        c1 = {("S", ("H_k_1",), ()): Q(1)}
        c2 = {("S", ("H_l_1",), ()): Q(1)}
        self.assertEqual(producer.rank_sparse([c1, c2])[0], 2)
        self.assertEqual(producer.classify(2, 2, 2), "CONSISTENT_UNIQUE")
        self.assertEqual(producer.classify(1, 1, 2), "CONSISTENT_AFFINE")
        self.assertEqual(producer.classify(1, 2, 2), "EXACTLY_INCONSISTENT")

        # Protected moving-shell primitive increments retain pinv rather than Laurent continuation.
        d = producer.primitive_delta_atom("H_nmk_1", (0, 1, 0))
        rat = d[()]
        tagged = [f for sig in rat for f, _ in sig if len(f) == 5 and f[0] == producer.a.pcl.PINV_TAG]
        self.assertTrue(tagged)
        self.assertEqual(producer.specialize_poly(d, 0, None), {})

        # Ordinary oriented primitive increments remain exact rational functions.
        hk = producer.primitive_delta_atom("H_k_2", (0, 1, 0))
        self.assertTrue(hk)
        self.assertEqual(producer.primitive_delta_atom("H_l_2", (0, 1, 0)), {})

        result = producer.build()
        self.assertEqual(result["stage"], contract["stage"])
        self.assertEqual(result["t3_010_a_checkpoint"]["validated_head"], contract["t3_010_a_checkpoint"]["validated_head"])
        self.assertEqual(result["independent_cell_count"], 400)
        self.assertEqual(result["mirrored_l1_cell_count"], 100)
        self.assertEqual(result["exact_k1_l1_matrix_mirror_checks"], 100)
        self.assertEqual(result["active_cell_count"] + result["structural_zero_cell_count"], 400)
        self.assertEqual(result["viable_cell_count"] + result["inconsistent_cell_count"], result["active_cell_count"])
        self.assertTrue(all(x["solution_extraction_admitted"] is False for x in result["matrix_cells"]))
        self.assertFalse(result["solution_coefficients_extracted"])
        self.assertFalse(result["full_correction_layer_recombined"])
        self.assertFalse(result["final_n_holonomic_search_run"])
        self.assertFalse(result["finite_sampling_used_as_sum_proof"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        replay = verifier.verify(result)
        self.assertEqual(replay["status"], "INDEPENDENT_T3_010_B_EXACT_MATRIX_REPLAY_COMPLETE")
        self.assertEqual(replay["independent_cell_count"], 400)
        self.assertEqual(replay["active_cell_count"], result["active_cell_count"])
        self.assertEqual(replay["viable_cell_count"], result["viable_cell_count"])
        self.assertEqual(replay["inconsistent_cell_count"], result["inconsistent_cell_count"])
        self.assertFalse(replay["producer_matrix_imported_as_authority"])

        # Rank, mirror, and claim mutations fail closed.
        active = next(x for x in result["matrix_cells"] if x["classification"] != "STRUCTURAL_ZERO")
        bad_rank = copy.deepcopy(result)
        target = next(x for x in bad_rank["matrix_cells"] if x["id"] == active["id"])
        target["augmented_rank"] += 1
        with self.assertRaisesRegex(AssertionError, "independent B reconstruction drift"):
            verifier.verify(bad_rank)

        bad_mirror = copy.deepcopy(result)
        bad_mirror["exact_k1_l1_matrix_mirror_checks"] = 99
        with self.assertRaisesRegex(AssertionError, "mirror-check count"):
            verifier.verify(bad_mirror)

        inflated = copy.deepcopy(result)
        inflated["proof_effect"] = "PROOF"
        with self.assertRaisesRegex(AssertionError, "claim-boundary inflation"):
            verifier.verify(inflated)

        recurrence = copy.deepcopy(result)
        recurrence["final_n_holonomic_search_run"] = True
        with self.assertRaisesRegex(AssertionError, "illegal recurrence search"):
            verifier.verify(recurrence)

        self.assertEqual(contract["coefficient_envelope"]["degree"], 0)
        self.assertFalse(contract["bounded_correction_class"]["generic_198_raw_jet_reopened"])
        self.assertFalse(contract["execution_discipline"]["adaptive_post_result_basis_growth"])
        self.assertFalse(contract["positive_classification_boundary"]["solution_extraction"])
        self.assertFalse(contract["positive_classification_boundary"]["final_n_holonomic_search"])


if __name__ == "__main__":
    unittest.main()
