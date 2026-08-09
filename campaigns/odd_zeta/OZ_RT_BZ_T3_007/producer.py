#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import struct
import subprocess
import tempfile
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
ODD = HERE.parent
T3006 = ODD / "OZ_RT_BZ_T3_006" / "producer.py"
OUT = HERE / "SEARCH_RESULT.json"
P = 1000003

spec = importlib.util.spec_from_file_location("t3_006_producer_for_t3_007", T3006)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-006 producer")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

MONOMS = base.MONOMS
POLY = base.POLY
mon2 = base.mon2
mon3 = base.mon3


def digest(v) -> str:
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def grid(order: int, nmax: int):
    return [
        (n, k, l)
        for n in range(order + 1, nmax + 1)
        for k in range(n - order + 1)
        for l in range(n)
    ]


def normalization_lock() -> dict:
    mapping = base.jet_map.coefficient_map()
    multipliers = [int(x["raw_derivative_multiplier"]) for x in mapping["monomials"]]
    if len(multipliers) != 198:
        raise AssertionError("raw-derivative normalization cardinality drift")
    if not all(x != 0 for x in multipliers):
        raise AssertionError("zero raw-derivative multiplier")
    if not all(x % P != 0 for x in multipliers):
        raise AssertionError("raw-derivative multiplier rank-prime collision")
    return {
        "source": "OZ-RT-BZ-T3-005 raw_derivative_multiplier",
        "monomial_multiplier_count": 198,
        "all_nonzero_integers": True,
        "all_nonzero_mod_prime": True,
        "multiplier_vector_sha256": hashlib.sha256(
            json.dumps(multipliers, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "rank_effect": "INVERTIBLE_DIAGONAL_RESCALING_PRESERVES_RANK_OVER_Q_AND_MOD_P",
    }


def compile_rank(tmp: Path) -> Path:
    exe = tmp / "rank_mod"
    subprocess.run(
        [os.environ.get("CC", "cc"), "-O3", str(HERE / "rank_mod.c"), "-o", str(exe)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return exe


def rank_rows(rows: list[list[int]], exe: Path, tmp: Path, tag: str) -> int:
    nr, nc = len(rows), len(rows[0])
    path = tmp / f"{tag}.bin"
    with path.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for row in rows:
            if len(row) != nc:
                raise AssertionError("ragged rank matrix")
            a = array("I", (x % P for x in row))
            if a.itemsize != 4:
                raise AssertionError("unexpected unsigned-int width")
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(path)], text=True).strip())


def module_row(order: int, n: int, k: int, l: int, qdeg: int) -> list[int]:
    row: list[int] = []
    for shift in range(order + 1):
        f = base.Fm(n, k + shift, l)
        row.extend(f * pow(n, i, P) * pow(k, j, P) % P for i, j in mon2(2))
    tc, tn = base.Tm(n, k, l), base.Tm(n, k, l + 1)
    dc, dn = base.qden(k, l) % P, base.qden(k, l + 1) % P
    if dc == 0 or dn == 0:
        raise AssertionError("certificate denominator collision")
    idc, idn = pow(dc, -1, P), pow(dn, -1, P)
    for mon in MONOMS:
        vc = base.monomial_mod(mon, n, k, l)
        vn = base.monomial_mod(mon, n, k, l + 1)
        for i, j, h in mon3(qdeg):
            pc = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
            pn = pow(n, i, P) * pow(k, j, P) * pow(l + 1, h, P) % P
            row.append((tc * vc * pc * idc - tn * vn * pn * idn) % P)
    return row


def module_stage(order: int, qdeg: int, nmax: int, exe: Path, tmp: Path) -> dict:
    tel = (order + 1) * len(mon2(2))
    cert = len(MONOMS) * len(mon3(qdeg))
    unknowns = tel + cert
    g = grid(order, nmax)
    if len(g) < unknowns:
        raise AssertionError("insufficient rank-witness rows")
    rows = [module_row(order, n, k, l, qdeg) for n, k, l in g[:unknowns]]
    rank = rank_rows(rows, exe, tmp, f"o{order}_q{qdeg}")
    return {
        "order": order,
        "q_coefficient_degree": qdeg,
        "n_max": nmax,
        "full_grid_rows": len(g),
        "rank_witness_rows": unknowns,
        "telescoper_unknowns": tel,
        "certificate_unknowns": cert,
        "unknowns": unknowns,
        "rank": rank,
        "nullity": unknowns - rank,
    }


def main() -> int:
    basis = base.basis_lock()
    cross = base.exact_cross_lock()
    norm = normalization_lock()
    configs = {3: {0: 10, 1: 15, 2: 19}, 4: {0: 11, 1: 15, 2: 20}}
    with tempfile.TemporaryDirectory(prefix="t3_007_") as td:
        tmp = Path(td)
        exe = compile_rank(tmp)
        o3 = [module_stage(3, q, configs[3][q], exe, tmp) for q in (0, 1, 2)]
        o4 = [module_stage(4, q, configs[4][q], exe, tmp) for q in (0, 1, 2)]

    nullity = sum(x["nullity"] for x in o3 + o4)
    terminal = (
        "ORDER3_4_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED"
        if nullity == 0
        else "CANDIDATE_SPACE_REMAINS_REQUIRING_RATIONAL_RECONSTRUCTION"
    )
    result = {
        "schema_version": "1.0.0",
        "operation": "OZ-RT-BZ-T3-007",
        "route": "COUPLED_WEIGHT5_RAW_JET_ORDER3_4_SEARCH_001",
        "prime": P,
        "target": "sum_{k,l=0}^n T(n,k,l)*(W1(k,l)+2*w5_sym(n,k,l))=0",
        "predecessor": {
            "issue": 356,
            "pull_request": 357,
            "merge_commit": "d9b9ed1a3a4c7ab56d25091e724fa585fbcea071",
            "merge_tree": "2a7bd5d53af76b6705ebd526dae667a381860374",
        },
        "execution_intake": {
            "protected_head": "d9b9ed1a3a4c7ab56d25091e724fa585fbcea071",
            "protected_tree": "2a7bd5d53af76b6705ebd526dae667a381860374",
        },
        "basis": basis,
        "coordinate_normalization": norm,
        "exact_target_cross_checks": cross,
        "search_equation": "sum_{j=0}^r a_j(n,k) F(n,k+j,l) = Delta_l Q_r(n,k,l), r in {3,4}",
        "certificate_denominator": "(l+1)^3*(k+l+1)",
        "denominator_provenance": "exact undeformed T(n,k,l+1)/T(n,k,l) shift-ratio denominator",
        "search_class": {
            "a_degree": 2,
            "orders": [3, 4],
            "certificate_coefficient_degrees": [0, 1, 2],
            "certificate_basis": "all 198 locked weight-five monomials with independent polynomial coefficients",
        },
        "order3_full_weight5_module": {
            "classification": "EXACT_BOUNDED_EXHAUSTION",
            "stages": o3,
            "producer_witness_selection": "first unknowns rows of the order-aware lexicographic exact grid",
            "independent_verifier_witness_selection": "last unknowns rows of the same declared exact grid with reversed basis ordering and reversed elimination columns",
            "strongest_frontier": "COUPLED_WEIGHT5_RAW_JET_ORDER3_ADEG_LE_2_QCOEFFDEG_LE_2",
            "terminal": "NO_NONZERO_ORDER3_FIBRE_CERTIFICATE_IN_COMPLETE_WEIGHT5_MODULE_DECLARED_CLASS",
        },
        "order4_full_weight5_module": {
            "classification": "EXACT_BOUNDED_EXHAUSTION",
            "stages": o4,
            "producer_witness_selection": "first unknowns rows of the order-aware lexicographic exact grid",
            "independent_verifier_witness_selection": "last unknowns rows of the same declared exact grid with reversed basis ordering and reversed elimination columns",
            "strongest_frontier": "COUPLED_WEIGHT5_RAW_JET_ORDER4_ADEG_LE_2_QCOEFFDEG_LE_2",
            "terminal": "NO_NONZERO_ORDER4_FIBRE_CERTIFICATE_IN_COMPLETE_WEIGHT5_MODULE_DECLARED_CLASS",
        },
        "rank_certificate": "FULL_COLUMN_RANK_MOD_P_EXHIBITS_NONZERO_MAXIMAL_MINOR_AND_IMPLIES_FULL_COLUMN_RANK_OVER_Q",
        "denominator_condition": "all exact rational matrix-entry denominators are nonzero modulo p on every declared sample",
        "mirror_status": "EXACTLY_EQUIVALENT_BY_K_L_SWAP",
        "terminal": terminal,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_distinct_routes": [
            "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001",
            "T3_SEQUENCE_RECURRENCE_EXTRACTION_001",
        ],
        "nonclaims": [
            "T3 is not proved",
            "T3 is not refuted",
            "bounded order-3/4 exhaustion is not evidence that T3 is false",
            "T1-top is not substituted for T3",
            "DEPTH and Sharp-12 are unchanged",
            "MATHCERT and GRAPH_CERTIFIED are unchanged",
        ],
    }
    expected = json.loads(OUT.read_text(encoding="utf-8"))
    if result != expected:
        raise AssertionError(f"canonical result drift: computed={digest(result)} expected={digest(expected)}")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
