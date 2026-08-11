from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
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


class T3010AContractTests(unittest.TestCase):
    def test_exact_shell_channel_block_gate(self):
        producer = load_module("t3_010_a", CAMPAIGN / "t3_010_a.py")
        verifier = load_module("verify_t3_010_a", CAMPAIGN / "verify_t3_010_a.py")
        contract = json.loads((CAMPAIGN / "T3_010_A_CONTRACT.json").read_text())

        self.assertEqual(producer.coordinate_activation(None), (True, True, True, True))
        self.assertEqual(producer.coordinate_activation(0), (False, True, True, True))
        self.assertEqual(producer.coordinate_activation(1), (False, False, True, True))
        self.assertEqual(producer.coordinate_activation(2), (False, False, False, True))
        self.assertEqual(producer.coordinate_activation(3), (False, False, False, False))

        result = producer.build()
        self.assertEqual(
            result["mathematical_predecessor"]["coefficient_layer_sha256"],
            contract["mathematical_predecessor"]["coefficient_layer_sha256"],
        )
        self.assertEqual(result["shell_stratum_count"], 25)
        self.assertEqual(result["interior_stratum_count"], 1)
        self.assertEqual(result["moving_boundary_or_shell_stratum_count"], 24)
        self.assertEqual(result["harmonic_block_sizes"], [5, 4, 2, 2])
        self.assertEqual(result["independent_probe_cell_count"], 400)
        self.assertEqual(result["mirrored_l1_cell_count"], 100)
        self.assertEqual(result["shell_recombination"]["status"], "EXACT_PIECEWISE_PARTITION_COMPLETE")
        self.assertFalse(result["shell_recombination"]["full_correction_layer_recombined"])
        self.assertTrue(all(not p["correction_candidate_admitted"] for p in result["forcing_support_rank_probes"]))

        replay = verifier.verify(result)
        self.assertEqual(replay["status"], "INDEPENDENT_T3_010_A_REPLAY_COMPLETE")
        self.assertEqual(replay["forcing_support_rank_cells_verified"], 400)
        self.assertEqual(replay["l1_policy_verified"], "mirror_only")

        self.assertFalse(result["finite_sampling_used_as_sum_proof"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")
        self.assertEqual(result["terminal"], "T3_010_A_COMPLETE__CORRECTION_FLUX_MATRIX_RANK_GATE_PENDING")

        inflated = copy.deepcopy(result)
        inflated["proof_effect"] = "PROOF"
        with self.assertRaisesRegex(AssertionError, "claim-boundary inflation"):
            verifier.verify(inflated)

        bad_status = copy.deepcopy(result)
        bad_status["t3_status"] = "PROVED"
        with self.assertRaisesRegex(AssertionError, "T3 status inflation"):
            verifier.verify(bad_status)

        self.assertFalse(contract["execution_discipline"]["blind_or_unbounded_creative_telescoping"])
        self.assertFalse(contract["execution_discipline"]["recurrence_fitting_to_zero_Dn"])
        self.assertFalse(contract["execution_discipline"]["generic_198_raw_jet_reopen"])
        self.assertFalse(contract["execution_discipline"]["final_n_holonomic_search"])


if __name__ == "__main__":
    unittest.main()
