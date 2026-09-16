#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
DEFAULT_MODEL = HERE / "model.json"
DEFAULT_OUTPUT = HERE / "RESULTS.json"
REFERENCE = (1, 2, 4)
ROBUSTNESS_SEED = 20260916
ROBUSTNESS_SAMPLES = 256
ROBUSTNESS_EDGE_FRACTION = 0.05
RANK_TOL = 1e-10


def parse_fraction(value: str | int | float) -> Fraction:
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, float):
        return Fraction(str(value))
    return Fraction(value)


def load_model(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def edge_records(model: dict[str, Any]) -> list[dict[str, Any]]:
    colors = {
        **model["object"]["internal_vertices"],
        **model["object"]["boundary_vertices"],
    }
    records = []
    for edge_id, left, right in model["object"]["edges"]:
        if colors[left] == colors[right]:
            raise AssertionError(f"Non-bipartite edge {edge_id}")
        white, black = (left, right) if colors[left] == "white" else (right, left)
        records.append({
            "id": edge_id,
            "white": white,
            "black": black,
            "boundary": edge_id.startswith("B"),
        })
    return records


def enumerate_matchings(model: dict[str, Any], edges: list[dict[str, Any]]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    colors = {
        **model["object"]["internal_vertices"],
        **model["object"]["boundary_vertices"],
    }
    interior = sorted(model["object"]["internal_vertices"])
    incident = {
        vertex: [index for index, edge in enumerate(edges) if vertex in (edge["white"], edge["black"])]
        for vertex in colors
    }
    selected: list[tuple[int, ...]] = []

    def recurse(covered: set[str], chosen: list[int], used_boundary: set[str]) -> None:
        if len(covered) == len(interior):
            selected.append(tuple(chosen))
            return
        vertex = next(item for item in interior if item not in covered)
        for edge_index in incident[vertex]:
            edge = edges[edge_index]
            other = edge["black"] if vertex == edge["white"] else edge["white"]
            if other in interior and other in covered:
                continue
            if other.startswith("U") and other in used_boundary:
                continue
            next_covered = set(covered)
            next_covered.add(vertex)
            next_boundary = set(used_boundary)
            if other in interior:
                next_covered.add(other)
            else:
                next_boundary.add(other)
            recurse(next_covered, chosen + [edge_index], next_boundary)

    recurse(set(), [], set())
    records = []
    for matching in selected:
        used = {
            vertex
            for edge_index in matching
            for vertex in (edges[edge_index]["white"], edges[edge_index]["black"])
            if vertex.startswith("U")
        }
        boundary_set = []
        for index in range(1, 7):
            vertex = f"U{index}"
            if (colors[vertex] == "black" and vertex in used) or (
                colors[vertex] == "white" and vertex not in used
            ):
                boundary_set.append(index)
        records.append((tuple(boundary_set), matching))
    return records


def exact_boundary_measurement(
    records: list[tuple[tuple[int, ...], tuple[int, ...]]],
    weights: list[Fraction],
) -> dict[tuple[int, ...], Fraction]:
    minors: dict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    for boundary_set, matching in records:
        product = Fraction(1, 1)
        for edge_index in matching:
            product *= weights[edge_index]
        minors[boundary_set] += product
    return dict(minors)


def float_response_and_jacobian(
    records: list[tuple[tuple[int, ...], tuple[int, ...]]],
    log_weights: np.ndarray,
) -> tuple[dict[tuple[int, ...], float], np.ndarray, np.ndarray, list[tuple[int, ...]]]:
    weights = np.exp(log_weights)
    by_boundary: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for boundary_set, matching in records:
        by_boundary[boundary_set].append(matching)

    minors: dict[tuple[int, ...], float] = {}
    edge_expectations: dict[tuple[int, ...], np.ndarray] = {}
    for boundary_set, matchings in by_boundary.items():
        monomials = np.array([
            float(np.prod(weights[list(matching)])) for matching in matchings
        ])
        total = float(monomials.sum())
        minors[boundary_set] = total
        expectation = np.zeros(len(weights), dtype=float)
        for monomial, matching in zip(monomials, matchings):
            for edge_index in matching:
                expectation[edge_index] += monomial
        edge_expectations[boundary_set] = expectation / total

    supported = sorted(minors)
    outputs = [key for key in supported if key != REFERENCE]
    response = np.array([
        math.log(minors[key] / minors[REFERENCE]) for key in outputs
    ])
    jacobian = np.vstack([
        edge_expectations[key] - edge_expectations[REFERENCE] for key in outputs
    ])
    return minors, response, jacobian, outputs


def matrix_rank(matrix: np.ndarray, tol: float = RANK_TOL) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=tol))


def gauge_matrix(model: dict[str, Any], edges: list[dict[str, Any]]) -> tuple[list[str], np.ndarray]:
    vertices = sorted(model["object"]["internal_vertices"])
    matrix = np.zeros((len(edges), len(vertices)), dtype=float)
    for column, vertex in enumerate(vertices):
        for row, edge in enumerate(edges):
            if vertex in (edge["white"], edge["black"]):
                matrix[row, column] = 1.0
    return vertices, matrix


def canonicalize_weights(
    model: dict[str, Any],
    edges: list[dict[str, Any]],
    weights: dict[str, float],
) -> tuple[dict[str, float], dict[str, float]]:
    edge_by_id = {edge["id"]: edge for edge in edges}
    factors = {vertex: 1.0 for vertex in model["object"]["internal_vertices"]}
    boundary_owner = {
        "B1": "F07",
        "B2": "F02",
        "B3": "F01",
        "B4": "F05",
        "B5": "F06",
        "B6": "F08",
    }
    # Gauge transformation is w'_e = w_e * prod(g_v) over internal endpoints.
    for edge_id, owner in boundary_owner.items():
        factors[owner] = 1.0 / weights[edge_id]

    def transformed(edge_id: str) -> float:
        edge = edge_by_id[edge_id]
        value = weights[edge_id]
        for vertex in (edge["white"], edge["black"]):
            if vertex in factors:
                value *= factors[vertex]
        return value

    factors["F04"] = 1.0 / transformed("F01|F04")
    factors["F03"] = 1.0 / transformed("F03|F06")

    canonical = {}
    for edge in edges:
        value = weights[edge["id"]]
        for vertex in (edge["white"], edge["black"]):
            if vertex in factors:
                value *= factors[vertex]
        canonical[edge["id"]] = value
    return canonical, factors


def results(model: dict[str, Any]) -> dict[str, Any]:
    edges = edge_records(model)
    edge_ids = [edge["id"] for edge in edges]
    edge_index = {edge_id: index for index, edge_id in enumerate(edge_ids)}
    records = enumerate_matchings(model, edges)

    exact_source = model["qualified_exact_representative"]["weights"]
    exact_weights = [parse_fraction(exact_source[edge_id]) for edge_id in edge_ids]
    exact_minors = exact_boundary_measurement(records, exact_weights)
    target = {
        tuple(int(char) for char in key): Fraction(value, 1)
        for key, value in model["qualified_exact_representative"]["target_plucker"].items()
    }
    expected_scale = parse_fraction(model["qualified_exact_representative"]["common_scale"])
    exact_match = all(exact_minors[key] == expected_scale * target[key] for key in target)
    exact_support = sorted("".join(map(str, key)) for key in exact_minors if exact_minors[key] != 0)

    baseline = np.array([float(value) for value in exact_weights], dtype=float)
    minors, _, jacobian, outputs = float_response_and_jacobian(records, np.log(baseline))
    vertices, gauge = gauge_matrix(model, edges)
    full_rank = matrix_rank(jacobian)
    gauge_rank = matrix_rank(gauge)
    gauge_annihilation = float(np.max(np.abs(jacobian @ gauge)))

    fixed_ids = ["B1", "B2", "B3", "B4", "B5", "B6", "F01|F04", "F03|F06"]
    free_ids = model["layers"]["metric_response"]["canonical_variables"]
    free_indices = [edge_index[edge_id] for edge_id in free_ids]
    canonical_jacobian = jacobian[:, free_indices]
    singular_values = np.linalg.svd(canonical_jacobian, compute_uv=False)
    canonical_rank = matrix_rank(canonical_jacobian)
    condition_number = float(singular_values[0] / singular_values[-1])
    sensitivity_by_parameter = {}
    for column, edge_id in enumerate(free_ids):
        vector = canonical_jacobian[:, column]
        largest_index = int(np.argmax(np.abs(vector)))
        sensitivity_by_parameter[edge_id] = {
            "l2_log_sensitivity": float(np.linalg.norm(vector)),
            "max_abs_log_sensitivity": float(abs(vector[largest_index])),
            "most_sensitive_output_minor": "".join(map(str, outputs[largest_index])),
            "signed_sensitivity_at_that_output": float(vector[largest_index]),
        }

    # Deliberate falsification: relax strict positivity by setting one edge to zero.
    zero_edge = "F07|F04"
    zero_weights = list(exact_weights)
    zero_weights[edge_index[zero_edge]] = Fraction(0, 1)
    zero_minors = exact_boundary_measurement(records, zero_weights)
    lost_support = sorted(
        "".join(map(str, key)) for key in exact_minors
        if exact_minors[key] != 0 and zero_minors.get(key, Fraction(0, 1)) == 0
    )

    # Inverse-design non-identifiability: the older solve representative must
    # canonicalize to the protected exact representative if it differs only by
    # internal-vertex gauge.
    solve_weights = {
        key: float(value) for key, value in model["solve_numerical_representative"]["weights"].items()
    }
    canonical_solve, solve_factors = canonicalize_weights(model, edges, solve_weights)
    canonical_exact = {key: float(parse_fraction(value)) for key, value in exact_source.items()}
    max_canonical_discrepancy = max(
        abs(canonical_solve[key] - canonical_exact[key]) for key in edge_ids
    )

    # Directly exercise one nontrivial gauge move from the exact representative.
    gauge_lambda = np.array([0.19, -0.11, 0.07, 0.13, -0.17, 0.05, 0.09, -0.03])
    moved_log = np.log(baseline) + gauge @ gauge_lambda
    moved_minors, moved_response, _, _ = float_response_and_jacobian(records, moved_log)
    _, base_response, _, _ = float_response_and_jacobian(records, np.log(baseline))
    gauge_response_error = float(np.max(np.abs(moved_response - base_response)))
    moved_weights = {edge_id: float(np.exp(moved_log[index])) for index, edge_id in enumerate(edge_ids)}
    baseline_target_ratios = {
        "".join(map(str, key)): str(target[key] / target[REFERENCE])
        for key in outputs
    }

    # Robustness in the nonredundant canonical coordinates. Each sample is
    # scaled so no raw edge changes by more than +/-5% multiplicatively.
    rng = np.random.default_rng(ROBUSTNESS_SEED)
    robust_ranks: list[int] = []
    robust_conditions: list[float] = []
    robust_min_singular: list[float] = []
    robust_support_counts: list[int] = []
    max_edge_change = 0.0
    for _ in range(ROBUSTNESS_SAMPLES):
        direction = np.zeros(len(edges), dtype=float)
        random_free = rng.normal(size=len(free_indices))
        for index, edge_index_value in enumerate(free_indices):
            direction[edge_index_value] = random_free[index]
        largest = float(np.max(np.abs(direction)))
        target_log_radius = float(rng.uniform(0.0, math.log(1.0 + ROBUSTNESS_EDGE_FRACTION)))
        if largest > 0.0:
            direction *= target_log_radius / largest
        sample_log = np.log(baseline) + direction
        sample_minors, _, sample_jacobian, _ = float_response_and_jacobian(records, sample_log)
        sample_reduced = sample_jacobian[:, free_indices]
        sample_sv = np.linalg.svd(sample_reduced, compute_uv=False)
        robust_ranks.append(matrix_rank(sample_reduced))
        robust_conditions.append(float(sample_sv[0] / sample_sv[-1]))
        robust_min_singular.append(float(sample_sv[-1]))
        robust_support_counts.append(sum(value > 0.0 for value in sample_minors.values()))
        max_edge_change = max(max_edge_change, float(np.max(np.abs(np.exp(direction) - 1.0))))

    return {
        "schema_version": "1.0.0",
        "work_package": "VGSE-ENG-WP01",
        "evidence_binding": {
            "mathcert_head": "2f27aed33b32b4caf6ff8622c87cfd6d40e97607",
            "mathsolve_head": "b0854bb7770296b610b655753bc62b27365b27bb",
            "math_programme_start_head": "4624294cd09b81145b8fe174447ba15d392f241b"
        },
        "canonical_object": {
            "internal_vertex_count": 8,
            "boundary_vertex_count": 6,
            "edge_count": 16,
            "almost_perfect_matching_count": len(records),
            "supported_projective_minor_count": len(exact_support),
            "supported_projective_minors": exact_support,
            "absent_minor": "123"
        },
        "forward_map": {
            "definition": "F(theta)=log(Delta_I/Delta_124) over the 18 supported I != 124, theta=log(w) with w>0",
            "raw_parameter_dimension": len(edges),
            "output_dimension": len(outputs),
            "exact_baseline_matches_target": exact_match,
            "exact_common_scale": str(expected_scale),
            "raw_jacobian_rank": full_rank,
            "raw_jacobian_nullity": len(edges) - full_rank,
            "gauge_generator_rank": gauge_rank,
            "max_abs_J_times_gauge": gauge_annihilation
        },
        "canonical_gauge": {
            "fixed_edge_ids": fixed_ids,
            "free_edge_ids": free_ids,
            "free_parameter_dimension": len(free_ids),
            "jacobian_rank": canonical_rank,
            "singular_values": [float(value) for value in singular_values],
            "condition_number": condition_number,
            "sensitivity_by_parameter": sensitivity_by_parameter
        },
        "candidate_invariant_screen": {
            "candidate": "positroid support of the projective boundary measurement",
            "admissible_class": "all sixteen edge weights remain strictly positive on the fixed topology",
            "result": "verified for the fixed graph by positive almost-perfect-matching sums; support is exactly the 19 recorded minors",
            "falsification_attempt": {
                "relaxed_assumption": f"set {zero_edge}=0",
                "lost_supported_minors": lost_support,
                "conclusion": "strict positivity is material; the invariant fails when zero weights are admitted"
            }
        },
        "inverse_design": {
            "problem": "given y*=F(theta_baseline), recover all sixteen raw positive edge weights",
            "target_response_exact_projective_ratios_to_124": baseline_target_ratios,
            "result": "non_identifiable",
            "reason": "eight independent internal-vertex gauge rescalings leave F exactly unchanged",
            "local_kernel_exhausted_at_baseline": full_rank == 8 and gauge_rank == 8 and gauge_annihilation < 1e-12,
            "solve_to_cert_representative_gauge_equivalence": {
                "max_abs_canonical_weight_discrepancy": max_canonical_discrepancy,
                "gauge_factors_applied_to_solve_representative": solve_factors
            },
            "explicit_gauge_move": {
                "internal_vertex_log_gauge": {vertex: float(value) for vertex, value in zip(vertices, gauge_lambda)},
                "second_solution_weights": moved_weights,
                "max_abs_response_error": gauge_response_error
            }
        },
        "robustness": {
            "seed": ROBUSTNESS_SEED,
            "samples": ROBUSTNESS_SAMPLES,
            "max_requested_edge_fraction": ROBUSTNESS_EDGE_FRACTION,
            "max_observed_edge_fraction": max_edge_change,
            "support_count_range": [min(robust_support_counts), max(robust_support_counts)],
            "canonical_rank_range": [min(robust_ranks), max(robust_ranks)],
            "minimum_singular_value_range": [min(robust_min_singular), max(robust_min_singular)],
            "condition_number_range": [min(robust_conditions), max(robust_conditions)]
        },
        "recoverability": {
            "recoverable_from_projective_response_locally": "eight canonical gauge-fixed weight coordinates near the protected baseline, because the canonical Jacobian has full column rank eight",
            "not_recoverable": "the sixteen raw edge weights individually; an eight-dimensional gauge family is response-equivalent",
            "visible_geometry_boundary": "the existing source-vector geometry does not determine the pinned-C weight class by Euclidean edge length; C06 remains excluded"
        },
        "claim_boundary": {
            "source_geometry_recovered": False,
            "physical_stiffness_interpretation": False,
            "rigid_foldability": False,
            "collision_freedom": False,
            "finite_thickness": False,
            "manufacturability": False,
            "commercial_claim": False
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = results(load_model(args.model))
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            print("VGSE-ENG-WP01 results do not match replay.")
            return 1
        print("VGSE-ENG-WP01 replay matches RESULTS.json")
        return 0
    args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
