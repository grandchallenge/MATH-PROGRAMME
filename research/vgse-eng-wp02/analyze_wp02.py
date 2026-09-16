#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
WP01_DIR = HERE.parent / "vgse-eng-wp01"
WP01_ANALYZER = WP01_DIR / "analyze_wp01.py"
WP01_MODEL = WP01_DIR / "model.json"
OUTPUT = HERE / "RESULTS.json"

SCREEN_SEED = 20260916
SCREEN_SAMPLES = 4096
SCREEN_LOG_RADIUS = 8.0
INFEASIBLE_DELTA = 0.1
REFERENCE_NAME = "124"

INVERSE_LAWS = {
    "F01|F02": ("124", "134"),
    "F07|F02": ("234", "134"),
    "F03|F04": ("134", "145"),
    "F03|F08": ("146", "145"),
    "F07|F04": ("345", "145"),
    "F05|F04": ("136", "146"),
    "F05|F06": ("156", "146"),
    "F07|F08": ("456", "145"),
}

EXPECTED_MONOMIALS = {
    "124": (1, 0, 1, 0, 0, 0, 0, 0),
    "134": (0, 0, 1, 0, 0, 0, 0, 0),
    "234": (0, 1, 1, 0, 0, 0, 0, 0),
    "145": (0, 0, 0, 0, 0, 0, 0, 0),
    "146": (0, 0, 0, 1, 0, 0, 0, 0),
    "345": (0, 0, 0, 0, 1, 0, 0, 0),
    "136": (0, 0, 0, 1, 0, 1, 0, 0),
    "156": (0, 0, 0, 1, 0, 0, 1, 0),
    "456": (0, 0, 0, 0, 0, 0, 0, 1),
}


def load_wp01() -> Any:
    spec = importlib.util.spec_from_file_location("vgse_wp01_analyzer", WP01_ANALYZER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {WP01_ANALYZER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minor_tuple(name: str) -> tuple[int, ...]:
    return tuple(int(char) for char in name)


def monomial_certificate(
    records: list[tuple[tuple[int, ...], tuple[int, ...]]],
    edge_ids: list[str],
    free_ids: list[str],
) -> dict[str, dict[tuple[int, ...], int]]:
    free_index = {edge_id: i for i, edge_id in enumerate(free_ids)}
    selected = {minor_tuple(name) for name in EXPECTED_MONOMIALS}
    result: dict[str, Counter[tuple[int, ...]]] = {
        name: Counter() for name in EXPECTED_MONOMIALS
    }
    for boundary, matching in records:
        if boundary not in selected:
            continue
        exponent = [0] * len(free_ids)
        for edge_index in matching:
            edge_id = edge_ids[edge_index]
            if edge_id in free_index:
                exponent[free_index[edge_id]] += 1
        result["".join(map(str, boundary))][tuple(exponent)] += 1
    return {name: dict(counter) for name, counter in result.items()}


def build_extractor(
    output_names: list[str],
    free_ids: list[str],
) -> np.ndarray:
    matrix = np.zeros((len(free_ids), len(output_names)), dtype=float)
    output_index = {name: i for i, name in enumerate(output_names)}
    for row, edge_id in enumerate(free_ids):
        numerator, denominator = INVERSE_LAWS[edge_id]
        if numerator != REFERENCE_NAME:
            matrix[row, output_index[numerator]] += 1.0
        if denominator != REFERENCE_NAME:
            matrix[row, output_index[denominator]] -= 1.0
    return matrix


def evaluate(
    wp01: Any,
    records: list[tuple[tuple[int, ...], tuple[int, ...]]],
    base_log_weights: np.ndarray,
    free_indices: list[int],
    theta: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    log_weights = base_log_weights.copy()
    log_weights[free_indices] = theta
    _, response, jacobian, outputs = wp01.float_response_and_jacobian(records, log_weights)
    output_names = ["".join(map(str, item)) for item in outputs]
    return response, jacobian[:, free_indices], output_names


def build_results() -> dict[str, Any]:
    wp01 = load_wp01()
    model = wp01.load_model(WP01_MODEL)
    edges = wp01.edge_records(model)
    records = wp01.enumerate_matchings(model, edges)
    edge_ids = [edge["id"] for edge in edges]
    edge_index = {edge_id: i for i, edge_id in enumerate(edge_ids)}
    free_ids = list(model["layers"]["metric_response"]["canonical_variables"])
    free_indices = [edge_index[edge_id] for edge_id in free_ids]

    certificate = monomial_certificate(records, edge_ids, free_ids)
    for name, expected in EXPECTED_MONOMIALS.items():
        observed = certificate[name]
        if observed != {expected: 1}:
            raise AssertionError(
                f"Minor {name} lost exact monomial certificate: {observed!r}"
            )

    exact_source = model["qualified_exact_representative"]["weights"]
    baseline = np.array(
        [float(wp01.parse_fraction(exact_source[edge_id])) for edge_id in edge_ids],
        dtype=float,
    )
    base_log_weights = np.log(baseline)
    baseline_theta = base_log_weights[free_indices].copy()
    baseline_response, baseline_jacobian, output_names = evaluate(
        wp01, records, base_log_weights, free_indices, baseline_theta
    )
    extractor = build_extractor(output_names, free_ids)

    inverse_error = float(np.max(np.abs(extractor @ baseline_response - baseline_theta)))
    identity_error = float(
        np.max(np.abs(extractor @ baseline_jacobian - np.eye(len(free_ids))))
    )
    if inverse_error > 1e-12 or identity_error > 1e-12:
        raise AssertionError("Baseline global-inverse identities failed")

    extractor_norm = float(np.linalg.svd(extractor, compute_uv=False)[0])
    global_smin_lower = 1.0 / extractor_norm

    # Every entry of the reduced Jacobian is a difference between two
    # edge-occupancy probabilities, hence belongs to [-1, 1].
    global_smax_upper = math.sqrt(len(output_names) * len(free_ids))
    global_condition_upper = global_smax_upper * extractor_norm

    rng = np.random.default_rng(SCREEN_SEED)
    perturbations = rng.uniform(
        -SCREEN_LOG_RADIUS,
        SCREEN_LOG_RADIUS,
        size=(SCREEN_SAMPLES, len(free_ids)),
    )
    ranks: list[int] = []
    smins: list[float] = []
    conditions: list[float] = []
    max_identity_error = 0.0
    max_inverse_error = 0.0
    for perturbation in perturbations:
        theta = baseline_theta + perturbation
        response, jacobian, names = evaluate(
            wp01, records, base_log_weights, free_indices, theta
        )
        if names != output_names:
            raise AssertionError("Response coordinate order changed")
        singular_values = np.linalg.svd(jacobian, compute_uv=False)
        ranks.append(int(np.linalg.matrix_rank(jacobian, tol=1e-10)))
        smins.append(float(singular_values[-1]))
        conditions.append(float(singular_values[0] / singular_values[-1]))
        max_identity_error = max(
            max_identity_error,
            float(np.max(np.abs(extractor @ jacobian - np.eye(len(free_ids))))),
        )
        max_inverse_error = max(
            max_inverse_error,
            float(np.max(np.abs(extractor @ response - theta))),
        )

    feasible_delta = np.array(
        [0.35, -0.22, 0.18, -0.41, 0.27, -0.16, 0.31, -0.29],
        dtype=float,
    )
    feasible_theta = baseline_theta + feasible_delta
    feasible_response, _, _ = evaluate(
        wp01, records, base_log_weights, free_indices, feasible_theta
    )
    recovered_theta = extractor @ feasible_response
    replay_response, _, _ = evaluate(
        wp01, records, base_log_weights, free_indices, recovered_theta
    )

    infeasible_target = baseline_response.copy()
    infeasible_index = output_names.index("125")
    infeasible_target[infeasible_index] += INFEASIBLE_DELTA
    infeasible_theta = extractor @ infeasible_target
    infeasible_replay, _, _ = evaluate(
        wp01, records, base_log_weights, free_indices, infeasible_theta
    )
    infeasible_residual = infeasible_target - infeasible_replay
    largest_residual_index = int(np.argmax(np.abs(infeasible_residual)))

    serialized_certificate = {
        name: list(EXPECTED_MONOMIALS[name]) for name in EXPECTED_MONOMIALS
    }
    serialized_inverse_laws = {
        edge_id: {
            "numerator_minor": numerator,
            "denominator_minor": denominator,
        }
        for edge_id, (numerator, denominator) in INVERSE_LAWS.items()
    }

    return {
        "schema_version": "1.0.0",
        "work_package": "VGSE-ENG-WP02",
        "evidence_binding": {
            "protected_wp01_merge": "8f43a8211c0236595eecee1cc5c195905bf5d27b",
            "reviewed_wp01_head": "e302494b683832626be95c8f4af104078cb87cf7",
            "mathcert_head": "2f27aed33b32b4caf6ff8622c87cfd6d40e97607",
        },
        "global_quotient_inverse": {
            "free_parameter_ids": free_ids,
            "minor_monomial_exponent_certificates": serialized_certificate,
            "inverse_laws": serialized_inverse_laws,
            "response_coordinate_order": output_names,
            "baseline_max_abs_inverse_reconstruction_error": inverse_error,
            "baseline_max_abs_extractor_jacobian_identity_error": identity_error,
            "extractor_operator_norm_2": extractor_norm,
            "global_smallest_singular_value_lower_bound": global_smin_lower,
            "global_largest_singular_value_upper_bound": global_smax_upper,
            "global_condition_number_upper_bound": global_condition_upper,
            "consequence": (
                "No rank-loss locus or conditioning blow-up exists anywhere in the "
                "strictly positive eight-coordinate quotient domain for the WP01 "
                "log-projective response map."
            ),
        },
        "wide_numerical_screen": {
            "seed": SCREEN_SEED,
            "samples": SCREEN_SAMPLES,
            "log_coordinate_box_radius": SCREEN_LOG_RADIUS,
            "minimum_rank": min(ranks),
            "minimum_smallest_singular_value": min(smins),
            "maximum_smallest_singular_value": max(smins),
            "minimum_condition_number": min(conditions),
            "maximum_condition_number": max(conditions),
            "maximum_abs_extractor_jacobian_identity_error": max_identity_error,
            "maximum_abs_inverse_reconstruction_error": max_inverse_error,
        },
        "inverse_design": {
            "feasible_log_coordinate_delta": [float(value) for value in feasible_delta],
            "feasible_max_abs_parameter_recovery_error": float(
                np.max(np.abs(recovered_theta - feasible_theta))
            ),
            "feasible_max_abs_response_replay_error": float(
                np.max(np.abs(replay_response - feasible_response))
            ),
            "infeasible_probe": {
                "perturbed_response_minor": "125",
                "log_response_delta": INFEASIBLE_DELTA,
                "recovered_parameter_max_abs_change": float(
                    np.max(np.abs(infeasible_theta - baseline_theta))
                ),
                "forward_consistency_max_abs_residual": float(
                    np.max(np.abs(infeasible_residual))
                ),
                "largest_residual_minor": output_names[largest_residual_index],
            },
        },
        "claim_boundary": {
            "source_correspondence_c06": "not established",
            "physical_stiffness_interpretation": "not established",
            "rigid_foldability": "not established",
            "collision_freedom": "not established",
            "finite_thickness": "not established",
            "manufacturability": "not established",
            "durability_fatigue": "not established",
            "product_performance": "not established",
            "novelty_priority_patentability_commercial_value": "not established",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    generated = build_results()
    if args.check:
        retained = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if retained != generated:
            raise AssertionError("RESULTS.json does not match deterministic replay")
        print("VGSE-ENG-WP02 deterministic replay: PASS")
        return 0

    OUTPUT.write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(generated, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
