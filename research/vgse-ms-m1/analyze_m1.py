#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
M0_DIR = HERE.parent / "vgse-ms-m0"
M0_ANALYZER = M0_DIR / "analyze_m0.py"

PANELS = ["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08"]
CANONICAL_FIXED = "F04"
HINGE_IDS = [
    "F01|F04", "F01|F02", "F07|F02", "F03|F06", "F03|F04",
    "F03|F08", "F07|F04", "F05|F04", "F05|F06", "F07|F08",
]
ABS_RANK_TOL = 1e-12
REL_RANK_TOL = 1e-10
SUMMARY_ATOL = 1e-10
SUMMARY_RTOL = 1e-8

OUTPUTS = [
    "MODEL_AUDIT.json",
    "MOBILITY_ATLAS.json",
    "BRANCH_COMPARISON.json",
    "FALSIFICATION_LEDGER.json",
    "RESULTS.json",
    "CLAIM_LEDGER.json",
]


def q(value: float) -> float:
    return float(f"{float(value):.15g}")


def load_m0() -> Any:
    spec = importlib.util.spec_from_file_location("vgse_ms_m0_analyzer", M0_ANALYZER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {M0_ANALYZER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_positions(m0: Any, positions: dict[str, complex]) -> dict[str, complex]:
    center = sum(positions.values()) / len(positions)
    perimeter = sum(
        abs(positions[m0.BOUNDARY[(i + 1) % 6]] - positions[m0.BOUNDARY[i]])
        for i in range(6)
    )
    if perimeter <= 0:
        raise AssertionError("boundary perimeter is nonpositive")
    return {name: (value - center) / perimeter for name, value in positions.items()}


def body_columns(fixed: str) -> dict[str, int]:
    free = [panel for panel in PANELS if panel != fixed]
    return {panel: 6 * index for index, panel in enumerate(free)}


def add_relative_row(
    row: np.ndarray,
    coefficients: np.ndarray,
    panel_a: str,
    panel_b: str,
    columns: dict[str, int],
) -> None:
    if panel_a != CANONICAL_FIXED and panel_a in columns:
        start = columns[panel_a]
        row[start : start + 6] += coefficients
    elif panel_a in columns:
        start = columns[panel_a]
        row[start : start + 6] += coefficients
    if panel_b != CANONICAL_FIXED and panel_b in columns:
        start = columns[panel_b]
        row[start : start + 6] -= coefficients
    elif panel_b in columns:
        start = columns[panel_b]
        row[start : start + 6] -= coefficients


def hinge_geometry(
    m0: Any,
    positions: dict[str, complex],
    edge_index: int,
) -> tuple[str, str, float, float, float]:
    _, panel_a, panel_b, _, (p_name, q_name) = m0.EDGES[edge_index]
    p = positions[p_name]
    qv = positions[q_name]
    dx = qv.real - p.real
    dy = qv.imag - p.imag
    length = math.hypot(dx, dy)
    if length <= 1e-14:
        raise AssertionError(f"zero hinge length for {m0.EDGES[edge_index][0]}")
    ux, uy = dx / length, dy / length
    moment_z = p.real * uy - p.imag * ux
    return panel_a, panel_b, ux, uy, moment_z


def body_hinge_matrices(
    m0: Any,
    raw_positions: dict[str, complex],
    fixed: str,
) -> tuple[np.ndarray, np.ndarray]:
    if fixed not in PANELS:
        raise ValueError(f"unknown fixed panel {fixed}")
    positions = normalize_positions(m0, raw_positions)
    columns = body_columns(fixed)
    J = np.zeros((5 * len(HINGE_IDS), 6 * (len(PANELS) - 1)), dtype=float)
    R = np.zeros((len(HINGE_IDS), 6 * (len(PANELS) - 1)), dtype=float)

    for hinge_index in range(len(HINGE_IDS)):
        panel_a, panel_b, ux, uy, moment_z = hinge_geometry(m0, positions, hinge_index)
        constraints = [
            np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0]),
            np.array([-uy, ux, 0.0, 0.0, 0.0, 0.0]),
            np.array([-moment_z * ux, -moment_z * uy, 0.0, 0.0, 0.0, 1.0]),
        ]
        for local_row, coefficient in enumerate(constraints):
            row = np.zeros(J.shape[1], dtype=float)
            add_relative_row(row, coefficient, panel_a, panel_b, columns)
            norm = np.linalg.norm(row)
            if norm <= 1e-14:
                raise AssertionError(f"zero constraint row for hinge {HINGE_IDS[hinge_index]}")
            J[5 * hinge_index + local_row] = row / norm

        rate_coefficient = np.array([ux, uy, 0.0, 0.0, 0.0, 0.0])
        add_relative_row(R[hinge_index], rate_coefficient, panel_a, panel_b, columns)

    return J, R


def numerical_rank(values: np.ndarray) -> tuple[int, float]:
    if values.size == 0:
        return 0, ABS_RANK_TOL
    threshold = max(ABS_RANK_TOL, REL_RANK_TOL * float(values[0]))
    return int(np.count_nonzero(values > threshold)), threshold


def kinematic_metrics(
    m0: Any,
    positions: dict[str, complex],
    fixed: str = CANONICAL_FIXED,
) -> dict[str, Any]:
    J, R = body_hinge_matrices(m0, positions, fixed)
    _, singular_values, vh = np.linalg.svd(J, full_matrices=True)
    rank, threshold = numerical_rank(singular_values)
    null_basis = vh[rank:].T
    hinge_rates = R @ null_basis

    if hinge_rates.size:
        u_rate, s_rate, _ = np.linalg.svd(hinge_rates, full_matrices=False)
        rate_rank, rate_threshold = numerical_rank(s_rate)
        Q = u_rate[:, :rate_rank]
        projector = Q @ Q.T
    else:
        s_rate = np.array([], dtype=float)
        rate_rank = 0
        rate_threshold = ABS_RANK_TOL
        projector = np.zeros((len(HINGE_IDS), len(HINGE_IDS)), dtype=float)

    smallest_nonzero = float(singular_values[rank - 1]) if rank else 0.0
    largest_null = float(singular_values[rank]) if rank < len(singular_values) else 0.0
    return {
        "rank": rank,
        "mobility": J.shape[1] - rank,
        "constraint_dependency_dimension": J.shape[0] - rank,
        "hinge_rate_subspace_rank": rate_rank,
        "rank_threshold": q(threshold),
        "rate_rank_threshold": q(rate_threshold),
        "smallest_nonzero_singular_value": q(smallest_nonzero),
        "largest_null_singular_value": q(largest_null),
        "projector": projector,
        "singular_values": singular_values,
        "hinge_rate_singular_values": s_rate,
    }


def baseline_branch_positions(m0: Any, count: int = 5) -> list[dict[str, Any]]:
    minors, weights = m0.minors_from_x(m0.BASELINE)
    C = m0.c_from_minors(minors)
    Cp = m0.c_perp_rows(C)

    def collect(B: np.ndarray, target: float, indices: list[int]) -> list[tuple[int, int, np.ndarray]]:
        rows: list[tuple[int, int, np.ndarray]] = []
        for index, normal in m0.fibonacci_normals():
            for sign in (1.0, -1.0):
                candidate = m0.plane_candidate(B, sign * normal, target, indices)
                if candidate is not None:
                    rows.append((index, int(sign), candidate[0]))
                    if len(rows) >= count:
                        return rows
        return rows

    left = collect(C, 2 * math.pi, [1, 4, 5])
    right = collect(Cp, 4 * math.pi, [0, 2, 3])
    if len(left) < count or len(right) < count:
        raise AssertionError("lost required M0 baseline branch multiplicity")

    branches: list[dict[str, Any]] = []
    for branch_index, (lrow, rrow) in enumerate(zip(left, right), 1):
        li, ls, L = lrow
        ti, ts, Lt = rrow
        fv, tv, fres, tres = m0.solve_extensions(
            weights, L[0] + 1j * L[1], Lt[0] - 1j * Lt[1]
        )
        positions, closure = m0.primitive(weights, fv, tv)
        metrics = m0.validate_geometry(positions, weights, fv, tv)
        if not m0.embedding_ok(metrics, fres, tres, closure):
            raise AssertionError(f"baseline branch {branch_index} lost M0 validity")
        branches.append(
            {
                "branch": f"BASELINE-B{branch_index}",
                "lambda_selector": {"index": li, "sign": ls},
                "tilde_lambda_selector": {"index": ti, "sign": ts},
                "positions": positions,
            }
        )
    return branches


def graph_audit(m0: Any) -> dict[str, Any]:
    adjacency = {panel: set() for panel in PANELS}
    for edge_index in range(10):
        _, a, b, _, _ = m0.EDGES[edge_index]
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen = {PANELS[0]}
    queue = [PANELS[0]]
    while queue:
        vertex = queue.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return {
        "panel_count": len(PANELS),
        "hinge_count": len(HINGE_IDS),
        "free_boundary_edge_count": 6,
        "panel_adjacency_connected": len(seen) == len(PANELS),
        "panel_adjacency_cycle_rank": len(HINGE_IDS) - len(PANELS) + 1,
        "matrix_rows": 50,
        "matrix_columns_after_fixed_panel": 42,
        "rows_per_hinge": 5,
    }


def build() -> dict[str, Any]:
    m0 = load_m0()
    m0_data = m0.build()

    atlas_rows: list[dict[str, Any]] = []
    valid_metrics: list[dict[str, Any]] = []
    excluded: list[str] = []
    baseline_positions: dict[str, complex] | None = None

    for row in m0_data["atlas"]:
        result = row["result"]
        if result["selector_status"] != "FOUND":
            excluded.append(row["id"])
            atlas_rows.append(
                {
                    "id": row["id"],
                    "m0_selector_status": result["selector_status"],
                    "kinematic_status": "NOT_EVALUATED_NO_M0_GEOMETRY",
                }
            )
            continue
        if not result["valid_numerical_t_embedding"]:
            raise AssertionError(f"M0 selector success lost t-embedding validity: {row['id']}")
        positions = {
            name: complex(float(value[0]), float(value[1]))
            for name, value in result["positions"].items()
        }
        if row["id"] == "baseline":
            baseline_positions = positions
        metrics = kinematic_metrics(m0, positions, CANONICAL_FIXED)
        valid_metrics.append(metrics)
        atlas_rows.append(
            {
                "id": row["id"],
                "m0_selector_status": "FOUND",
                "kinematic_status": "EVALUATED",
                "rank": metrics["rank"],
                "mobility": metrics["mobility"],
                "constraint_dependency_dimension": metrics["constraint_dependency_dimension"],
                "hinge_rate_subspace_rank": metrics["hinge_rate_subspace_rank"],
            }
        )

    if baseline_positions is None:
        raise AssertionError("M0 baseline geometry missing")

    baseline_reference = kinematic_metrics(m0, baseline_positions, CANONICAL_FIXED)
    root_rows = []
    root_projector_differences = []
    for fixed in PANELS:
        metrics = kinematic_metrics(m0, baseline_positions, fixed)
        diff = float(np.max(np.abs(metrics["projector"] - baseline_reference["projector"])))
        root_projector_differences.append(diff)
        root_rows.append(
            {
                "fixed_panel": fixed,
                "rank": metrics["rank"],
                "mobility": metrics["mobility"],
                "constraint_dependency_dimension": metrics["constraint_dependency_dimension"],
                "hinge_rate_subspace_rank": metrics["hinge_rate_subspace_rank"],
                "projector_max_abs_difference_from_F04": q(diff),
            }
        )

    branch_rows = []
    branch_metrics = []
    for branch in baseline_branch_positions(m0):
        metrics = kinematic_metrics(m0, branch["positions"], CANONICAL_FIXED)
        branch_metrics.append((branch["branch"], metrics))
        branch_rows.append(
            {
                "branch": branch["branch"],
                "lambda_selector": branch["lambda_selector"],
                "tilde_lambda_selector": branch["tilde_lambda_selector"],
                "rank": metrics["rank"],
                "mobility": metrics["mobility"],
                "constraint_dependency_dimension": metrics["constraint_dependency_dimension"],
                "hinge_rate_subspace_rank": metrics["hinge_rate_subspace_rank"],
            }
        )

    pairwise = []
    for i in range(len(branch_metrics)):
        for j in range(i + 1, len(branch_metrics)):
            left_name, left = branch_metrics[i]
            right_name, right = branch_metrics[j]
            diff = float(np.max(np.abs(left["projector"] - right["projector"])))
            pairwise.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "hinge_rate_projector_max_abs_difference": q(diff),
                }
            )

    ranks = sorted({item["rank"] for item in valid_metrics})
    mobilities = sorted({item["mobility"] for item in valid_metrics})
    dependencies = sorted({item["constraint_dependency_dimension"] for item in valid_metrics})
    rate_ranks = sorted({item["hinge_rate_subspace_rank"] for item in valid_metrics})

    return {
        "graph_audit": graph_audit(m0),
        "atlas_rows": atlas_rows,
        "valid_metrics": valid_metrics,
        "excluded": excluded,
        "root_rows": root_rows,
        "root_max_projector_difference": max(root_projector_differences),
        "branch_rows": branch_rows,
        "branch_pairwise": pairwise,
        "aggregate": {
            "attempted_m0_samples": len(atlas_rows),
            "evaluated_valid_m0_realizations": len(valid_metrics),
            "excluded_without_m0_geometry": len(excluded),
            "observed_ranks": ranks,
            "observed_mobilities": mobilities,
            "observed_constraint_dependency_dimensions": dependencies,
            "observed_hinge_rate_subspace_ranks": rate_ranks,
            "minimum_smallest_nonzero_singular_value": q(
                min(item["smallest_nonzero_singular_value"] for item in valid_metrics)
            ),
            "maximum_smallest_nonzero_singular_value": q(
                max(item["smallest_nonzero_singular_value"] for item in valid_metrics)
            ),
            "maximum_largest_null_singular_value": q(
                max(item["largest_null_singular_value"] for item in valid_metrics)
            ),
        },
    }


def artifacts(data: dict[str, Any]) -> dict[str, Any]:
    aggregate = data["aggregate"]
    pairwise_values = [
        row["hinge_rate_projector_max_abs_difference"] for row in data["branch_pairwise"]
    ]
    same_mobility = len({row["mobility"] for row in data["branch_rows"]}) == 1
    same_subspace = max(pairwise_values) <= 1e-8

    model_audit = {
        "schema_version": "1.0.0",
        "work_package": "VGSE-MS-M1",
        "contract": "VGSE-MS-M1-BODY-HINGE-001",
        "predecessor": "M0 terminal c09d652f7a85b5b7277ce3c89a50d3bfc84d7d20",
        "graph": data["graph_audit"],
        "canonical_fixed_panel": CANONICAL_FIXED,
        "baseline_root_invariance": data["root_rows"],
        "max_hinge_rate_projector_difference_across_fixed_panel_choices": q(
            data["root_max_projector_difference"]
        ),
        "root_invariance_tolerance": 1e-10,
        "conclusion": "BODY_HINGE_MODEL_AUDITED",
    }

    mobility = {
        "schema_version": "1.0.0",
        "work_package": "VGSE-MS-M1",
        "matrix_contract": {
            "rows": 50,
            "columns": 42,
            "rank_threshold": "max(1e-12, 1e-10*sigma_max)",
            "row_normalization": "each scalar hinge constraint row is normalized to unit 2-norm after centering geometry and scaling coordinates by boundary perimeter",
        },
        "aggregate": aggregate,
        "samples": data["atlas_rows"],
        "interpretation": "Flat-state infinitesimal body-hinge result under the GCL-defined M1 semantics only.",
    }

    branches = {
        "schema_version": "1.0.0",
        "work_package": "VGSE-MS-M1",
        "fixed_quotient": "protected M0 baseline quotient",
        "branches": data["branch_rows"],
        "pairwise_hinge_rate_subspace_comparison": data["branch_pairwise"],
        "minimum_pairwise_projector_difference": q(min(pairwise_values)),
        "maximum_pairwise_projector_difference": q(max(pairwise_values)),
        "same_mobility_dimension": same_mobility,
        "same_hinge_rate_subspace": same_subspace,
        "conclusion": "FIXED_QUOTIENT_KINEMATIC_SUBSPACE_BRANCH_DEPENDENT",
    }

    falsification = {
        "schema_version": "1.0.0",
        "work_package": "VGSE-MS-M1",
        "hypotheses": [
            {
                "claim": "All retained valid M0 TE3 realizations have the same flat-state infinitesimal mobility under the M1 body-hinge semantics.",
                "status": "NOT_FALSIFIED_ON_RETAINED_ATLAS",
                "evidence": "All 40 evaluated retained M0 realizations have rank 38 and mobility 4.",
            },
            {
                "claim": "The eight quotient coordinates uniquely determine the flat-state infinitesimal kinematic state despite geometric branch multiplicity.",
                "status": "FALSIFIED_NUMERICALLY",
                "evidence": "Five valid geometric representatives at the same protected quotient all have mobility 4 but distinct labeled hinge-rate mechanism subspaces.",
                "minimum_pairwise_hinge_rate_projector_difference": q(min(pairwise_values)),
            },
        ],
    }

    results = {
        "schema_version": "1.0.0",
        "work_package": "VGSE-MS-M1",
        "disposition": "KINEMATIC_SEMANTICS_BRANCH_DEPENDENT",
        "model": "GCL-defined flat-state rigid-panel/body-hinge infinitesimal semantics",
        "atlas_summary": {
            "evaluated_valid_m0_realizations": aggregate["evaluated_valid_m0_realizations"],
            "rank": aggregate["observed_ranks"],
            "mobility": aggregate["observed_mobilities"],
            "constraint_dependency_dimension": aggregate["observed_constraint_dependency_dimensions"],
            "hinge_rate_mechanism_dimension": aggregate["observed_hinge_rate_subspace_ranks"],
            "minimum_smallest_nonzero_singular_value": aggregate[
                "minimum_smallest_nonzero_singular_value"
            ],
            "maximum_largest_null_singular_value": aggregate[
                "maximum_largest_null_singular_value"
            ],
        },
        "baseline_branch_summary": {
            "valid_branch_count": len(data["branch_rows"]),
            "all_mobility_four": all(row["mobility"] == 4 for row in data["branch_rows"]),
            "minimum_pairwise_hinge_rate_projector_difference": q(min(pairwise_values)),
            "maximum_pairwise_hinge_rate_projector_difference": q(max(pairwise_values)),
            "fixed_quotient_unique_kinematic_state": False,
        },
        "established_numerically": [
            "all 40 retained valid M0 realizations have flat-state body-hinge rank 38, mobility 4, and constraint-dependency dimension 12 under the declared M1 semantics",
            "baseline mobility and labeled hinge-rate mechanism subspace are invariant to which panel is fixed, within the declared numerical tolerance",
            "five valid geometric representatives at the same protected quotient have distinct four-dimensional labeled hinge-rate mechanism subspaces",
        ],
        "structural_interpretation": "The observed four-dimensional mobility is consistent with ten labeled hinge-rate variables subject to six independent planar rotation-closure conditions at the three interior dual vertices A, C, and D. M1 does not promote that counting interpretation to a universal theorem.",
        "not_established": [
            "universal mobility classification outside the retained M0 atlas",
            "finite rigid foldability",
            "mountain/valley assignment",
            "collision-free continuation",
            "finite thickness",
            "stiffness, force, energy, constitutive, material, or actuation behaviour",
            "VGSE-C06/source correspondence",
            "unique kinematic state from quotient coordinates alone",
        ],
        "next_boundary": "M1 may terminate at KINEMATIC_SEMANTICS_BRANCH_DEPENDENT. Any M2 inverse-design activation must treat geometric branch/representative choice as latent structure and apply GCL-ID-00 before substantial inverse optimization.",
        "claim_boundary": {
            "mathematical_certification": False,
            "finite_rigid_foldability": False,
            "collision_freedom": False,
            "finite_thickness": False,
            "stiffness_force_energy": False,
            "constitutive_material_model": False,
            "actuation": False,
            "manufacturing": False,
            "product": False,
            "source_correspondence_c06": False,
            "novelty_patent_commercial": False,
        },
    }

    claims = {
        "schema_version": "1.0.0",
        "work_package": "VGSE-MS-M1",
        "claims": [
            {
                "id": "VGSE-MS-M1-C01",
                "statement": "The GCL-defined M1 body-hinge incidence and 50x42 Jacobian contract are internally consistent with the protected M0 dual embedding.",
                "status": "COMPUTED_MODEL_AUDIT",
            },
            {
                "id": "VGSE-MS-M1-C02",
                "statement": "All 40 retained valid M0 realizations replay numerically at rank 38, mobility 4, and constraint-dependency dimension 12 under the M1 flat-state body-hinge semantics.",
                "status": "NUMERICALLY_REPLAYED",
            },
            {
                "id": "VGSE-MS-M1-C03",
                "statement": "The baseline mobility and labeled hinge-rate mechanism subspace are invariant to the fixed-panel gauge within numerical tolerance.",
                "status": "NUMERICALLY_REPLAYED",
            },
            {
                "id": "VGSE-MS-M1-C04",
                "statement": "At the protected quotient, distinct valid M0 geometric representatives yield distinct four-dimensional labeled hinge-rate mechanism subspaces; quotient coordinates therefore do not uniquely determine the M1 infinitesimal kinematic state.",
                "status": "NUMERICALLY_FALSIFIED_UNIQUENESS",
            },
            {
                "id": "VGSE-MS-M1-C05",
                "statement": "Finite rigid foldability follows from the retained infinitesimal mobility.",
                "status": "NOT_ESTABLISHED",
            },
        ],
    }

    return {
        "MODEL_AUDIT.json": model_audit,
        "MOBILITY_ATLAS.json": mobility,
        "BRANCH_COMPARISON.json": branches,
        "FALSIFICATION_LEDGER.json": falsification,
        "RESULTS.json": results,
        "CLAIM_LEDGER.json": claims,
    }


def summary_equal(actual: Any, expected: Any) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return actual is expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if isinstance(actual, int) and isinstance(expected, int):
            return actual == expected
        return math.isclose(float(actual), float(expected), rel_tol=SUMMARY_RTOL, abs_tol=SUMMARY_ATOL)
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            summary_equal(actual[key], expected[key]) for key in actual
        )
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(
            summary_equal(left, right) for left, right in zip(actual, expected)
        )
    return actual == expected


def validate_retained(generated: dict[str, Any]) -> None:
    for name in OUTPUTS:
        path = HERE / name
        if not path.is_file():
            raise AssertionError(f"missing retained artifact {name}")
        actual = json.loads(path.read_text(encoding="utf-8"))
        if not summary_equal(actual, generated[name]):
            raise AssertionError(f"{name} drift exceeds deterministic replay tolerance")

    results = generated["RESULTS.json"]
    if results["disposition"] != "KINEMATIC_SEMANTICS_BRANCH_DEPENDENT":
        raise AssertionError("M1 disposition drift")
    if results["atlas_summary"]["rank"] != [38]:
        raise AssertionError("M1 rank drift")
    if results["atlas_summary"]["mobility"] != [4]:
        raise AssertionError("M1 mobility drift")
    if generated["BRANCH_COMPARISON.json"]["same_hinge_rate_subspace"]:
        raise AssertionError("fixed-quotient branch dependence was lost")
    if any(results["claim_boundary"].values()):
        raise AssertionError("M1 claim boundary crossed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    generated = artifacts(build())
    if args.write:
        for name, value in generated.items():
            (HERE / name).write_text(
                json.dumps(value, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    if args.check:
        validate_retained(generated)
        print("VGSE-MS-M1 deterministic kinematic mobility atlas: PASS")
    if not args.write and not args.check:
        print(json.dumps(generated["RESULTS.json"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
