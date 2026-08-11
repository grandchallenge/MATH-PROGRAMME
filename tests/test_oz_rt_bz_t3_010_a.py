from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

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


def test_t3_010_a_exact_shell_channel_block_gate():
    producer = load_module("t3_010_a", CAMPAIGN / "t3_010_a.py")
    verifier = load_module("verify_t3_010_a", CAMPAIGN / "verify_t3_010_a.py")
    contract = json.loads((CAMPAIGN / "T3_010_A_CONTRACT.json").read_text())

    assert producer.coordinate_activation(None) == (True, True, True, True)
    assert producer.coordinate_activation(0) == (False, True, True, True)
    assert producer.coordinate_activation(1) == (False, False, True, True)
    assert producer.coordinate_activation(2) == (False, False, False, True)
    assert producer.coordinate_activation(3) == (False, False, False, False)

    result = producer.build()
    assert result["mathematical_predecessor"]["coefficient_layer_sha256"] == contract["mathematical_predecessor"]["coefficient_layer_sha256"]
    assert result["shell_stratum_count"] == 25
    assert result["interior_stratum_count"] == 1
    assert result["moving_boundary_or_shell_stratum_count"] == 24
    assert result["harmonic_block_sizes"] == [5, 4, 2, 2]
    assert result["independent_probe_cell_count"] == 1300
    assert result["mirrored_l1_cell_count"] == 100
    assert result["shell_recombination"]["status"] == "EXACT_PIECEWISE_PARTITION_COMPLETE"
    assert result["shell_recombination"]["full_correction_layer_recombined"] is False
    assert all(p["correction_candidate_admitted"] is False for p in result["forcing_support_rank_probes"])

    replay = verifier.verify(result)
    assert replay["status"] == "INDEPENDENT_T3_010_A_REPLAY_COMPLETE"
    assert replay["forcing_support_rank_cells_verified"] == 1300
    assert replay["l1_policy_verified"] == "mirror_only"

    assert result["finite_sampling_used_as_sum_proof"] is False
    assert result["residual_sum_zero_proved"] is False
    assert result["proof_effect"] == "NONE"
    assert result["promotion_effect"] == "NONE"
    assert result["t3_status"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"
    assert result["terminal"] == "T3_010_A_COMPLETE__CORRECTION_FLUX_MATRIX_RANK_GATE_PENDING"

    inflated = copy.deepcopy(result)
    inflated["proof_effect"] = "PROOF"
    with pytest.raises(AssertionError, match="claim-boundary inflation"):
        verifier.verify(inflated)

    bad_status = copy.deepcopy(result)
    bad_status["t3_status"] = "PROVED"
    with pytest.raises(AssertionError, match="T3 status inflation"):
        verifier.verify(bad_status)

    assert contract["execution_discipline"]["blind_or_unbounded_creative_telescoping"] is False
    assert contract["execution_discipline"]["recurrence_fitting_to_zero_Dn"] is False
    assert contract["execution_discipline"]["generic_198_raw_jet_reopen"] is False
    assert contract["execution_discipline"]["final_n_holonomic_search"] is False
