from __future__ import annotations

import producer
import verifier

NEGATIVE_TERMINAL = "SUPPORT_LOCKED_DEGREE0_COUPLED_CORRECTION_RECOMBINATION_INCOMPATIBLE"


def build() -> dict:
    """Bind the governed negative terminal from two independent exact replays.

    The source-functional calculation is a restriction of the protected global
    one-orientation identity to two regular strict-interior lattice points.  A
    global correction in the unchanged shared-coefficient class must satisfy
    every such specialization.  Therefore exact inconsistency of this
    restriction is sufficient for nonexistence in the declared class.  This is
    a negative witness only; it is not a finite-grid proof of a positive
    identity and it does not reconstruct every shell row of the global map.
    """
    evidence = producer.build()
    replay = verifier.verify(evidence)

    row = evidence["producer_source_functional_interior_probe"]
    independent = replay["source_functional_interior"]

    if row["source"]["git_blob_sha1"] != "61f12f412726887f506e1d423b7ee183a22116e5":
        raise AssertionError("T3-012-B Q-row source lock drift at terminalization")
    if row["source"]["byte_count"] != 44980:
        raise AssertionError("T3-012-B Q-row source byte-count drift at terminalization")
    if row["samples"] != [[8, 1, 2], [9, 2, 1]]:
        raise AssertionError("T3-012-B strict-interior witness drift")
    if not row["strict_interior_only"] or row["shell_regularization_enters_witness"]:
        raise AssertionError("T3-012-B negative witness left the regular strict interior")
    if not row["qrow_point_replay"]:
        raise AssertionError("T3-012-B protected Q-row identity was not replayed")
    if row["unknown_count"] != 506:
        raise AssertionError("T3-012-B correction-class identity drift")
    if (row["coefficient_rank"], row["augmented_rank"], row["consistent"]) != (84, 85, False):
        raise AssertionError("T3-012-B exact source-functional obstruction drift")

    for field in (
        "samples",
        "strict_interior_only",
        "shell_regularization_enters_witness",
        "qrow_point_replay",
        "one_orientation_spatial_multiplier",
        "unknown_count",
        "nonzero_column_count",
        "target_coordinate_count",
        "coefficient_rank",
        "augmented_rank",
        "consistent",
        "nullity",
    ):
        if independent[field] != row[field]:
            raise AssertionError(f"T3-012-B terminal independent replay drift: {field}")
    if not replay["independent_source_functional_replay_complete"]:
        raise AssertionError("T3-012-B independent source-functional replay incomplete")

    return {
        "schema_version": "1.2.0",
        "issue": 927,
        "stage": "T3_012_B_COUPLED_CORRECTION_RECOMBINATION_GATE",
        "protected_base": evidence["protected_base"],
        "terminal": NEGATIVE_TERMINAL,
        "terminal_basis": "EXACT_SOURCE_LOCKED_STRICT_INTERIOR_NECESSARY_SUBSYSTEM_INCONSISTENCY",
        "source_locked_recombination_restriction_reconstructed": True,
        "actual_source_locked_global_recombination_map_fully_reconstructed": False,
        "global_solution_implies_subsystem_solution": True,
        "finite_specialization_used_as_nonexistence_witness": True,
        "finite_sampling_used_as_identity_proof": False,
        "source_functional_interior": {
            "source": row["source"],
            "samples": row["samples"],
            "strict_interior_only": row["strict_interior_only"],
            "shell_regularization_enters_witness": row["shell_regularization_enters_witness"],
            "qrow_point_replay": row["qrow_point_replay"],
            "one_orientation_spatial_multiplier": row["one_orientation_spatial_multiplier"],
            "unknown_count": row["unknown_count"],
            "nonzero_column_count": row["nonzero_column_count"],
            "target_coordinate_count": row["target_coordinate_count"],
            "coefficient_rank": row["coefficient_rank"],
            "augmented_rank": row["augmented_rank"],
            "consistent": row["consistent"],
            "nullity": row["nullity"],
        },
        "independent_source_functional_replay_complete": True,
        "producer_source_jets_imported_by_verifier_as_authority": False,
        "producer_projected_matrices_imported_by_verifier_as_authority": False,
        "class_excluded": "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001",
        "scope_exclusion_only": True,
        "broader_correction_classes_excluded": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
