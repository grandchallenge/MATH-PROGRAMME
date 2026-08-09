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
WITNESS = HERE / "Q2_RANK_WITNESS.json"
P = 1000003

spec = importlib.util.spec_from_file_location("t3_006_producer_for_t3_008", T3006)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-006 producer")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

MONOMS = base.MONOMS
POLY = base.POLY
mon3 = base.mon3

BASIS_SHA = "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438"
NORMALIZATION_SHA = "69738508f28433f9090f93621c8da3bc6b18279fd70941a31d07fb96b607700b"
Q2_INDEX_SHA = "d0bb330deff059c2afdc4e1a994d7c544c42ce7ec497e1c6490ca9f2781dc57f"


def canonical_sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def boundary(n: int, x: int) -> int:
    return x * (n + 1 - x)


def d_k(k: int, l: int) -> int:
    return (k + 1) ** 3 * (k + l + 1)


def d_l(k: int, l: int) -> int:
    return (l + 1) ** 3 * (k + l + 1)


def grid(nmax: int):
    return [
        (n, k, l)
        for n in range(2, nmax + 1)
        for k in range(n + 1)
        for l in range(n + 1)
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
    digest = hashlib.sha256(
        json.dumps(multipliers, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if digest != NORMALIZATION_SHA:
        raise AssertionError("raw-derivative normalization digest drift")
    return {
        "source": "OZ-RT-BZ-T3-005 raw_derivative_multiplier",
        "monomial_multiplier_count": 198,
        "all_nonzero_integers": True,
        "all_nonzero_mod_prime": True,
        "multiplier_vector_sha256": digest,
        "rank_effect": "INVERTIBLE_DIAGONAL_RESCALING_PRESERVES_RANK_OVER_Q_AND_MOD_P",
    }


def symmetry_lock() -> dict:
    basis = base.basis_lock()
    if basis["basis_sha256"] != BASIS_SHA:
        raise AssertionError("protected weight-five basis drift")
    if base.jet_map.swap(POLY) != POLY:
        raise AssertionError("protected target lost k/l symmetry")
    for n in range(2, 7):
        for k in range(n + 1):
            for l in range(n + 1):
                if base.Fm(n, k, l) != base.Fm(n, l, k):
                    raise AssertionError("source-locked T3 cell lost k/l symmetry")
                if d_k(k, l) != d_l(l, k):
                    raise AssertionError("flux denominator family is not swap closed")
    for n in range(0, 21):
        if boundary(n, 0) != 0 or boundary(n, n + 1) != 0:
            raise AssertionError("finite-square boundary factor drift")
    if P % 2 == 0:
        raise AssertionError("rank prime must be odd for symmetrization")
    return {
        "target_swap_invariant": True,
        "basis_swap_closed": True,
        "denominator_swap_closed": True,
        "boundary_factor_swap_closed": True,
        "coefficient_envelope_swap_closed": True,
        "rank_prime_odd": True,
        "lemma": "ANY_UNRESTRICTED_SWAP_CLOSED_TWO_FLUX_SOLUTION_SYMMETRIZES_TO_Q_EQUALS_TAU_P",
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


def rank_rows(rows: list[list[int]], exe: Path, tmp: Path, tag: str, target: list[int] | None = None) -> int:
    if not rows:
        return 0
    if target is not None and len(target) != len(rows):
        raise AssertionError("target-row cardinality mismatch")
    nr = len(rows)
    nc0 = len(rows[0])
    nc = nc0 + (1 if target is not None else 0)
    path = tmp / f"{tag}.bin"
    with path.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for i, row in enumerate(rows):
            if len(row) != nc0:
                raise AssertionError("ragged rank matrix")
            a = array("I", (x % P for x in row))
            if target is not None:
                a.append(target[i] % P)
            if a.itemsize != 4:
                raise AssertionError("unexpected unsigned-int width")
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(path)], text=True).strip())


def matrix_row(n: int, k: int, l: int, qdeg: int) -> list[int]:
    exps = mon3(qdeg)
    dk0 = d_k(k, l) % P
    dk1 = d_k(k + 1, l) % P
    dl0 = d_l(k, l) % P
    dl1 = d_l(k, l + 1) % P
    if 0 in (dk0, dk1, dl0, dl1):
        raise AssertionError("flux denominator collision")
    tc = base.Tm(n, k, l)
    pk0 = tc * (boundary(n, k) % P) * pow(dk0, -1, P) % P
    pk1 = base.Tm(n, k + 1, l) * (boundary(n, k + 1) % P) * pow(dk1, -1, P) % P
    ql0 = tc * (boundary(n, l) % P) * pow(dl0, -1, P) % P
    ql1 = base.Tm(n, k, l + 1) * (boundary(n, l + 1) % P) * pow(dl1, -1, P) % P
    poly = []
    for i, j, h in exps:
        ni = pow(n, i, P)
        poly.append((
            ni * pow(k, j, P) % P * pow(l, h, P) % P,
            ni * pow(k + 1, j, P) % P * pow(l, h, P) % P,
            ni * pow(l, j, P) % P * pow(k, h, P) % P,
            ni * pow(l + 1, j, P) % P * pow(k, h, P) % P,
        ))
    row: list[int] = []
    for mon in MONOMS:
        a0 = pk0 * base.monomial_mod(mon, n, k, l) % P
        a1 = pk1 * base.monomial_mod(mon, n, k + 1, l) % P
        b0 = ql0 * base.monomial_mod(mon, n, l, k) % P
        b1 = ql1 * base.monomial_mod(mon, n, l + 1, k) % P
        for p0, p1, q0, q1 in poly:
            row.append((a0 * p0 - a1 * p1 + b0 * q0 - b1 * q1) % P)
    return row


def full_stage(qdeg: int, nmax: int, exe: Path, tmp: Path) -> dict:
    g = grid(nmax)
    unknowns = len(MONOMS) * len(mon3(qdeg))
    rows = [matrix_row(n, k, l, qdeg) for n, k, l in g]
    target = [base.Fm(n, k, l) for n, k, l in g]
    rc = rank_rows(rows, exe, tmp, f"q{qdeg}_coeff")
    ra = rank_rows(rows, exe, tmp, f"q{qdeg}_aug", target)
    if rc != unknowns or ra != unknowns + 1:
        raise AssertionError(f"degree-{qdeg} final affine rank drift: coefficient={rc}, augmented={ra}, unknowns={unknowns}")
    return {
        "q_coefficient_degree": qdeg,
        "n_max": nmax,
        "full_grid_rows": len(g),
        "unknowns": unknowns,
        "coefficient_rank": rc,
        "augmented_rank": ra,
        "classification": "EXACT_AFFINE_INCONSISTENCY",
        "rank_certificate": "FULL_COLUMN_RANK_COEFFICIENT_MATRIX_AND_ONE_HIGHER_AUGMENTED_RANK_MOD_P_IMPLIES_NO_RATIONAL_SOLUTION",
    }


def q2_stage(exe: Path, tmp: Path) -> dict:
    w = json.loads(WITNESS.read_text(encoding="utf-8"))
    ids = w["coefficient_row_indices"]
    if len(ids) != 1980 or len(set(ids)) != 1980:
        raise AssertionError("degree-2 coefficient witness cardinality drift")
    if canonical_sha(ids) != Q2_INDEX_SHA:
        raise AssertionError("degree-2 coefficient witness digest drift")
    g = grid(22)
    if len(g) != 4319:
        raise AssertionError("degree-2 full-grid cardinality drift")
    if any(i < 0 or i >= len(g) for i in ids):
        raise AssertionError("degree-2 witness index outside declared grid")
    extra = int(w["augmented_extra_row_index"])
    if g[extra] != tuple(w["augmented_extra_row_point"]):
        raise AssertionError("degree-2 augmented extra-row point drift")
    coeff_points = [g[i] for i in ids]
    coeff_rows = [matrix_row(n, k, l, 2) for n, k, l in coeff_points]
    rc = rank_rows(coeff_rows, exe, tmp, "q2_coeff_witness")
    if rc != 1980:
        raise AssertionError(f"degree-2 coefficient witness rank drift: {rc}")
    aug_points = coeff_points + [g[extra]]
    aug_rows = [matrix_row(n, k, l, 2) for n, k, l in aug_points]
    aug_target = [base.Fm(n, k, l) for n, k, l in aug_points]
    ra = rank_rows(aug_rows, exe, tmp, "q2_aug_witness", aug_target)
    if ra != 1981:
        raise AssertionError(f"degree-2 augmented witness rank drift: {ra}")
    return {
        "q_coefficient_degree": 2,
        "n_max": 22,
        "full_grid_rows": len(g),
        "unknowns": 1980,
        "coefficient_rank": rc,
        "augmented_rank": ra,
        "classification": "EXACT_AFFINE_INCONSISTENCY",
        "rank_certificate": "EXPLICIT_FULL_RANK_COEFFICIENT_MINOR_PLUS_ONE_EXTRA_AUGMENTED_ROW_MOD_P_IMPLIES_NO_RATIONAL_SOLUTION",
        "witness_file": "Q2_RANK_WITNESS.json",
        "coefficient_row_indices_sha256": Q2_INDEX_SHA,
        "augmented_extra_row_index": extra,
        "augmented_extra_row_point": list(g[extra]),
    }


def compute_result() -> dict:
    basis = base.basis_lock()
    norm = normalization_lock()
    symmetry = symmetry_lock()
    cross = base.exact_cross_lock()
    if cross != 135:
        raise AssertionError("exact target cross-lock count drift")
    with tempfile.TemporaryDirectory(prefix="t3_008_") as td:
        tmp = Path(td)
        exe = compile_rank(tmp)
        stages = [full_stage(0, 20, exe, tmp), full_stage(1, 20, exe, tmp), q2_stage(exe, tmp)]
    return {
        "schema_version": "1.0.0",
        "operation": "OZ-RT-BZ-T3-008",
        "route": "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001",
        "prime": P,
        "target": "sum_{k,l=0}^n T(n,k,l)*(W1(k,l)+2*w5_sym(n,k,l))=0",
        "predecessor": {"issue": 359, "pull_request": 360, "merge_commit": "5233b37506f28e80959139cbc0f89b7ad400b658", "merge_tree": "5f5fc435927888fbdf84c1ba15044c347506fbd0"},
        "execution_intake": {"protected_head": "5233b37506f28e80959139cbc0f89b7ad400b658", "protected_tree": "5f5fc435927888fbdf84c1ba15044c347506fbd0"},
        "basis": basis,
        "coordinate_normalization": norm,
        "exact_target_cross_checks": cross,
        "symmetry_completeness": symmetry,
        "search_equation": "F(n,k,l)=Delta_k P(n,k,l)+Delta_l tau(P)(n,k,l)",
        "difference_convention": {"Delta_k": "P(n,k,l)-P(n,k+1,l)", "Delta_l": "Q(n,k,l)-Q(n,k,l+1)"},
        "flux": {"P": "T(n,k,l)*k*(n+1-k)/((k+1)^3*(k+l+1))*sum_M p_M(n,k,l)M(n,k,l)", "Q": "tau(P)", "k_denominator": "(k+1)^3*(k+l+1)", "l_denominator": "(l+1)^3*(k+l+1)", "k_boundary_factor": "k*(n+1-k)", "l_boundary_factor": "l*(n+1-l)"},
        "search_class": {"certificate_basis": "all 198 locked weight-five monomials with independent polynomial coefficients", "coefficient_degrees": [0, 1, 2], "symmetric_subspace_complete_for_declared_swap_closed_two_flux_class": True},
        "preliminary_alias_grids": [
            {"q_coefficient_degree": 0, "n_max": 8, "rows": 280, "unknowns": 198, "coefficient_rank": 154, "augmented_rank": 154, "classification": "FINITE_GRID_ALIAS_ONLY"},
            {"q_coefficient_degree": 1, "n_max": 13, "rows": 1010, "unknowns": 792, "coefficient_rank": 544, "augmented_rank": 544, "classification": "FINITE_GRID_ALIAS_ONLY"},
            {"q_coefficient_degree": 2, "n_max": 18, "rows": 2465, "unknowns": 1980, "coefficient_rank": 1309, "augmented_rank": 1309, "classification": "FINITE_GRID_ALIAS_ONLY"}
        ],
        "stages": stages,
        "denominator_condition": "all declared finite-grid shift denominators and protected raw-derivative normalization multipliers are nonzero modulo p",
        "negative_certificate_logic": "a nonzero maximal coefficient minor together with a one-rank-higher augmented minor modulo p certifies affine inconsistency over Q",
        "terminal": "SYMMETRIC_2D_WEIGHT5_DIVERGENCE_BOUNDED_CLASS_EXHAUSTED",
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_distinct_route": "T3_SEQUENCE_RECURRENCE_EXTRACTION_001",
        "nonclaims": ["T3 is not proved", "T3 is not refuted", "bounded symmetric 2D divergence exhaustion is not evidence that T3 is false", "preliminary equal modular ranks on smaller grids are finite-grid aliasing and are not candidate evidence", "T1-top is not substituted for T3", "DEPTH and Sharp-12 are unchanged", "MATHCERT and GRAPH_CERTIFIED are unchanged"]
    }


def main() -> int:
    result = compute_result()
    expected = json.loads(OUT.read_text(encoding="utf-8"))
    if result != expected:
        raise AssertionError(f"canonical T3-008 result drift: computed={canonical_sha(result)} expected={canonical_sha(expected)}")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
