#!/usr/bin/env python3
"""Deterministic artifact replay for VGSE-ENG-WP05."""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def load(name: str) -> Any:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def rank(matrix: list[list[int]]) -> int:
    a = [[Fraction(v) for v in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for i in range(rows):
            if i == r or not a[i][c]:
                continue
            factor = a[i][c]
            a[i] = [x - factor * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("determinant requires square matrix")
    a = [[int(v) for v in row] for row in matrix]
    sign = 1
    denom = 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k] != 0), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // denom
        denom = p
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[-1][-1]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def identity(n: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def monomial(point: list[Fraction], row: list[int]) -> Fraction:
    out = Fraction(1)
    for value, exponent in zip(point, row):
        if exponent >= 0:
            out *= value ** exponent
        else:
            out /= value ** (-exponent)
    return out


def validate() -> list[str]:
    errors: list[str] = []
    graph = load("GRAPH_INCIDENCE.json")
    gauge = load("GAUGE_ACTION.json")
    lattice = load("INVARIANT_LATTICE.json")
    chart = load("QUOTIENT_CHART.json")
    replay = load("BRANCH_REPLAY.json")
    results = load("RESULTS.json")
    claims = load("CLAIM_LEDGER.json")

    if graph["edge_count"] != 16 or graph["internal_vertex_count"] != 8 or graph["boundary_vertex_count"] != 6:
        errors.append("graph cardinality drift")
    if graph["total_vertex_count"] != 14 or not graph["connected"]:
        errors.append("full graph topology drift")

    G = gauge["matrix"]
    if rank(G) != 8 or gauge["rank"] != 8 or gauge["nullity"] != 8:
        errors.append("gauge rank/nullity mismatch")
    if gauge["full_graph_cycle_rank"] != 3 or 16 - 14 + 1 != 3:
        errors.append("closed-cycle rank mismatch")
    if gauge["boundary_flow_degrees"] != 5:
        errors.append("boundary-flow complement mismatch")

    edge_order = graph["edge_order"]
    basis = lattice["basis"]
    if len(basis) != 8:
        errors.append("invariant basis must contain eight rows")
    exponent_rows: list[list[int]] = []
    for item in basis:
        row = [int(item["exponents"].get(edge, 0)) for edge in edge_order]
        exponent_rows.append(row)
        for grow in G:
            if sum(a * b for a, b in zip(grow, row)) != 0:
                errors.append(f"{item['id']} is not gauge invariant")
    if rank(exponent_rows) != 8 or lattice["rank"] != 8:
        errors.append("natural invariant basis is not rank eight")
    if sum(item["kind"] == "closed_cycle" for item in basis) != 3:
        errors.append("expected exactly three closed-cycle basis rows")
    if sum(item["kind"] == "boundary_path" for item in basis) != 5:
        errors.append("expected exactly five boundary-path basis rows")

    A = chart["A"]
    Ainv = chart["A_inverse"]
    if determinant(A) != -1 or chart["A_determinant"] != -1:
        errors.append("quotient chart must be unimodular with determinant -1")
    if matmul(A, Ainv) != identity(8) or matmul(Ainv, A) != identity(8):
        errors.append("stored chart inverse is not exact")

    x = [Fraction(v) for v in chart["protected_point_x"]]
    y_expected = [Fraction(v) for v in chart["protected_point_y"]]
    y_actual = [monomial(x, row) for row in A]
    if y_actual != y_expected:
        errors.append(f"protected quotient point transform mismatch: {y_actual!r}")

    if replay["closed_cycle_replay"]["branch_count"] != 5:
        errors.append("cycle replay branch count drift")
    if replay["closed_cycle_replay"]["max_absolute_error"] >= 1e-10:
        errors.append("cycle replay exceeds tolerance")
    if replay["boundary_path_replay"]["max_absolute_error_after_boundary_normalization"] >= 1e-9:
        errors.append("boundary-normalized path replay exceeds tolerance")
    if replay["boundary_path_replay"]["raw_geometry_products_are_branch_invariant"]:
        errors.append("raw path products must remain branch dependent")
    if max(v["max_over_min"] for v in replay["boundary_path_replay"]["raw_magnitude_variation"].values()) <= 10:
        errors.append("retained replay no longer demonstrates material raw path variation")

    if results["exact_results"]["gauge_action_rank"] != 8:
        errors.append("results gauge rank drift")
    if results["exact_results"]["pure_closed_cycle_rank"] != 3:
        errors.append("results cycle rank drift")
    if results["geometry_only_result"]["independent_quotient_coordinates_recovered"] != 3:
        errors.append("geometry-only result must remain 3/8")
    if results["geometry_only_result"]["total_quotient_dimension"] != 8:
        errors.append("quotient dimension drift")
    if results["geometry_only_result"]["full_geometry_only_inverse_established"]:
        errors.append("full geometry-only inverse is not established")
    if results["calibrated_result"]["independent_quotient_coordinates_recovered"] != 8:
        errors.append("calibrated result must remain 8/8")
    if not results["calibrated_result"]["exact_chart_invertible"]:
        errors.append("calibrated chart must remain exactly invertible")
    if results["terminal_disposition"] != "CYCLE_INVARIANT_QUOTIENT_RECONSTRUCTION_PARTIAL":
        errors.append("terminal disposition drift")

    if any(results["claim_boundary"].values()):
        errors.append("forbidden claim boundary crossed")

    ids = {c["id"] for c in claims["claims"]}
    expected = {f"VGSE-ENG-WP05-C{i:02d}" for i in range(1, 10)}
    if ids != expected:
        errors.append("claim ledger ID set drift")

    return errors


def summary() -> dict[str, Any]:
    chart = load("QUOTIENT_CHART.json")
    replay = load("BRANCH_REPLAY.json")
    results = load("RESULTS.json")
    return {
        "work_package": "VGSE-ENG-WP05",
        "gauge_invariant_rank": results["exact_results"]["invariant_lattice_rank"],
        "geometry_only_rank": results["geometry_only_result"]["independent_quotient_coordinates_recovered"],
        "calibrated_rank": results["calibrated_result"]["independent_quotient_coordinates_recovered"],
        "chart_determinant": chart["A_determinant"],
        "max_cycle_replay_error": replay["closed_cycle_replay"]["max_absolute_error"],
        "max_calibrated_path_replay_error": replay["boundary_path_replay"]["max_absolute_error_after_boundary_normalization"],
        "terminal_disposition": results["terminal_disposition"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        return 1
    if args.check:
        print("VGSE-ENG-WP05 deterministic replay: PASS")
    else:
        print(json.dumps(summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
