#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
WP01_MODEL = HERE.parent / "vgse-eng-wp01" / "model.json"
OUTPUT = HERE / "RESULTS.json"

REFERENCE = "124"
FEASIBLE_TOL = 1e-10
INCONSISTENT_TOL = 1e-7
PROBE_DELTA = 0.1
AMBIGUOUS_DELTA = 5e-9

FREE_IDS = [
    "F01|F02", "F07|F02", "F03|F04", "F03|F08",
    "F07|F04", "F05|F04", "F05|F06", "F07|F08",
]
EXTRACTOR_COORDS = ["134", "234", "145", "146", "345", "136", "156", "456"]
DEPENDENT_COORDS = ["125", "126", "135", "235", "236", "245", "246", "256", "346", "356"]
RESPONSE_ORDER = ["125","126","134","135","136","145","146","156","234","235","236","245","246","256","345","346","356","456"]

# Normalized positive measurement coordinates y_I = Delta_I / Delta_124.
# Each relation is denominator(y_extractors)*y_dep - numerator(y_extractors).
RELATION_TEXT = {
    "125": "y134*y146*y125 - y134*y156 - y136*y145",
    "126": "y134*y126 - y136",
    "135": "y146*y135 - y134*y156 - y136*y145",
    "235": "y134*y146*y235 - y234*(y134*y156 + y136*y145)",
    "236": "y134*y236 - y136*y234",
    "245": "y134*y245 - y145*y234 - y345",
    "246": "y134*y145*y246 - y134*y456 - y145*y146*y234 - y146*y345",
    "256": "y134*y145*y146*y256 - y134*y156*y456 - y136*y145*y456 - y145*y146*y156*y234 - y146*y156*y345",
    "346": "y145*y346 - y134*y456 - y146*y345",
    "356": "y145*y146*y356 - y134*y156*y456 - y136*y145*y456 - y146*y156*y345",
}
RELATION_DIAGONALS = {
    "125": "y134*y146",
    "126": "y134",
    "135": "y146",
    "235": "y134*y146",
    "236": "y134",
    "245": "y134",
    "246": "y134*y145",
    "256": "y134*y145*y146",
    "346": "y145",
    "356": "y145*y146",
}


def load_model() -> dict[str, Any]:
    return json.loads(WP01_MODEL.read_text(encoding="utf-8"))


def edge_records(model: dict[str, Any]) -> list[dict[str, Any]]:
    colors = {**model["object"]["internal_vertices"], **model["object"]["boundary_vertices"]}
    out = []
    for edge_id, left, right in model["object"]["edges"]:
        if colors[left] == colors[right]:
            raise AssertionError(f"non-bipartite edge {edge_id}")
        white, black = (left, right) if colors[left] == "white" else (right, left)
        out.append({"id": edge_id, "white": white, "black": black})
    return out


def enumerate_matchings(model: dict[str, Any], edges: list[dict[str, Any]]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    colors = {**model["object"]["internal_vertices"], **model["object"]["boundary_vertices"]}
    interior = sorted(model["object"]["internal_vertices"])
    incident = {
        vertex: [i for i, edge in enumerate(edges) if vertex in (edge["white"], edge["black"])]
        for vertex in colors
    }
    selected: list[tuple[int, ...]] = []

    def recurse(covered: set[str], chosen: list[int], used_boundary: set[str]) -> None:
        if len(covered) == len(interior):
            selected.append(tuple(chosen))
            return
        vertex = next(v for v in interior if v not in covered)
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
        boundary = []
        for index in range(1, 7):
            vertex = f"U{index}"
            if (colors[vertex] == "black" and vertex in used) or (
                colors[vertex] == "white" and vertex not in used
            ):
                boundary.append(index)
        records.append((tuple(boundary), matching))
    return records


def minor_polynomials(model: dict[str, Any]) -> tuple[dict[str, sp.Expr], list[tuple[tuple[int, ...], tuple[int, ...]]]]:
    edges = edge_records(model)
    records = enumerate_matchings(model, edges)
    x = sp.symbols("x1:9", positive=True)
    free_index = {edge_id: i for i, edge_id in enumerate(FREE_IDS)}
    polys: dict[str, sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for boundary, matching in records:
        monomial = sp.Integer(1)
        for edge_index in matching:
            edge_id = edges[edge_index]["id"]
            if edge_id in free_index:
                monomial *= x[free_index[edge_id]]
        name = "".join(map(str, boundary))
        polys[name] += monomial
    return {name: sp.expand(expr) for name, expr in polys.items()}, records


def symbols_y() -> dict[str, sp.Symbol]:
    names = [REFERENCE] + RESPONSE_ORDER
    syms = sp.symbols(" ".join(f"y{name}" for name in names), positive=True)
    return dict(zip(names, syms))


def extractor_from_y(y: dict[str, Any]) -> list[Any]:
    return [
        1 / y["134"],
        y["234"] / y["134"],
        y["134"] / y["145"],
        y["146"] / y["145"],
        y["345"] / y["145"],
        y["136"] / y["146"],
        y["156"] / y["146"],
        y["456"] / y["145"],
    ]


def relation_exprs(y: dict[str, sp.Symbol]) -> dict[str, sp.Expr]:
    local = {f"y{name}": y[name] for name in y}
    return {name: sp.expand(sp.sympify(text, locals=local)) for name, text in RELATION_TEXT.items()}


def relation_diagonals(y: dict[str, sp.Symbol]) -> dict[str, sp.Expr]:
    local = {f"y{name}": y[name] for name in y}
    return {name: sp.sympify(text, locals=local) for name, text in RELATION_DIAGONALS.items()}

