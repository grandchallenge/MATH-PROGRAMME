from __future__ import annotations

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


def emit(title: str, payload: dict) -> None:
    # GitHub Actions workflow-command annotation. Compact JSON is deliberate:
    # this diagnostic branch projects, but does not alter, the frozen C result.
    print(f"::error title={title}::{json.dumps(payload, sort_keys=True, separators=(',', ':'))}", flush=True)


class T3010CLedgerProbe(unittest.TestCase):
    def test_emit_exact_c_ledger_after_independent_verification(self):
        producer = load_module("t3_010_c", CAMPAIGN / "t3_010_c.py")
        verifier = load_module("verify_t3_010_c", CAMPAIGN / "verify_t3_010_c.py")

        result = producer.build()
        replay = verifier.verify(result)

        for rec in result["channel_systems"]:
            emit(
                f"T3-010-C {rec['channel']}",
                {
                    "channel": rec["channel"],
                    "unknown_count": rec["unknown_count"],
                    "active_cell_count": rec["active_cell_count"],
                    "structural_zero_cell_count": rec["structural_zero_cell_count"],
                    "local_classification_histogram": rec["local_classification_histogram"],
                    "coefficient_rank": rec["coefficient_rank"],
                    "augmented_rank": rec["augmented_rank"],
                    "nullity": rec["nullity"],
                    "classification": rec["classification"],
                    "global_target_coordinate_count": rec["global_target_coordinate_count"],
                    "global_matrix_coordinate_count": rec["global_matrix_coordinate_count"],
                    "zero_global_columns": rec["zero_global_columns"],
                    "exact_solution_extracted": rec["exact_solution_extracted"],
                    "exact_substitution_checks": rec["exact_substitution_checks"],
                    "canonical_solution_sha256": rec["canonical_solution_sha256"],
                },
            )

        emit("T3-010-C l1 mirror", result["mirrored_l1_system"])
        emit(
            "T3-010-C aggregate",
            {
                "globally_consistent_independent_channel_count": result["globally_consistent_independent_channel_count"],
                "globally_inconsistent_independent_channel_count": result["globally_inconsistent_independent_channel_count"],
                "exact_solution_extracted_channel_count": result["exact_solution_extracted_channel_count"],
                "all_independent_channels_globally_consistent": result["all_independent_channels_globally_consistent"],
                "terminal": result["terminal"],
                "residual_sum_zero_proved": result["residual_sum_zero_proved"],
                "proof_effect": result["proof_effect"],
                "promotion_effect": result["promotion_effect"],
                "t3_status": result["t3_status"],
                "verifier_status": replay["status"],
                "verifier_consistent_count": replay["globally_consistent_independent_channel_count"],
                "verifier_inconsistent_count": replay["globally_inconsistent_independent_channel_count"],
                "producer_matrix_imported_as_authority": replay["producer_matrix_imported_as_authority"],
            },
        )

        self.fail("T3_010_C_LEDGER_PROBE_COMPLETE")
