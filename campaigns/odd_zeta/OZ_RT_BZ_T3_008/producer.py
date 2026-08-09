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

spec = importlib.util.spec_from_file_location("t3_006_producer_for_t3_008", T3006)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3-006 producer")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

MONOMS = base.MONOMS
POLY = base.POLY
mon3 = base.mon3


def digest(v) -> str:
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def symmetry_and_boundary_lock() -> dict:
    if base.jet_map.swap(POLY) != POLY:
        raise AssertionError("protected target polynomial lost k/l symmetry")
    if base.basis_lock()["k_l_swap_invariant"] is not True:
        raise AssertionError("protected raw-jet basis lost swap closure")
    symmetry_checks = 0
    for n in range(2, 7):
        for k in range(n + 1):
            for l in range(n + 1):
                if base.Fm(n, k, l) != base.Fm(n, l, k):
                    raise AssertionError("source-locked T3 cell lost k/l symmetry")
                if d_k(k, l) != d_l(l, k):
                    raise AssertionError("flux denominator family is not swap closed")
                symmetry_checks += 1
    boundary_checks = 0
    for n in range(0, 21):
        for x in (0, n + 1):
            if boundary(n, x) != 0:
                raise AssertionError("finite-square flux boundary factor drift")
            boundary_checks += 2
    if P % 2 == 0:
        raise AssertionError("rank prime must support division by two for symmetrization")
    return {
        "target_swap_invariant": True,
        "basis_swap_closed": True,
        "denominator_swap_closed": True,
        "coefficient_envelope_swap_closed": True,
        "rank_prime_odd": True,
        "source_cell_symmetry_checks": symmetry_checks,
        "boundary_zero_checks": boundary_checks,
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


def rank_rows(
    rows: list[list[int]],
    exe: Path,
    tmp: Path,
    tag: str,
    target: list[int] | None = None,
) -> int:
    if not rows:
        return 0
    if target is not None and len(target) != len(rows):
        raise AssertionError("target-row cardinality mismatch")
    nr = len(rows)
    nc = len(rows[0]) + (1 if target is not None else 0)
    path = tmp / f"{tag}.bin"
    with path.open("wb") as f:
        f.write(struct.pack("<II", nr, nc))
        for rix, row in enumerate(rows):
            if len(row) != nc - (1 if target is not None else 0):
                raise AssertionError("ragged rank matrix")
            values = (x % P for x in row)
            a = array("I", values)
            if target is not None:
                a.append(target[rix] % P)
            if a.itemsize != 4:
                raise AssertionError("unexpected unsigned-int width")
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(path)], text=True).strip())


def flux_column_value(mon: tuple[str, ...], ex: tuple[int, int, int], n: int, k: int, l: int) -> int:
    i, j, h = ex
    tc = base.Tm(n, k, l)

    dk0 = d_k(k, l) % P
    dk1 = d_k(k + 1, l) % P
    dl0 = d_l(k, l) % P
    dl1 = d_l(k, l + 1) % P
    if 0 in (dk0, dk1, dl0, dl1):
        raise AssertionError("flux denominator collision")

    p0 = pow(n, i, P) * pow(k, j, P) * pow(l, h, P) % P
    p1 = pow(n, i, P) * pow(k + 1, j, P) * pow(l, h, P) % P
    q0 = pow(n, i, P) * pow(l, j, P) * pow(k, h, P) % P
    q1 = pow(n, i, P) * pow(l + 1, j, P) * pow(k, h, P) % P

    pk0 = tc * (boundary(n, k) % P) * pow(dk0, -1, P) % P
    pk1 = base.Tm(n, k + 1, l) * (boundary(n, k + 1) % P) * pow(dk1, -1, P) % P
    ql0 = tc * (boundary(n, l) % P) * pow(dl0, -1, P) % P
    ql1 = base.Tm(n, k, l + 1) * (boundary(n, l + 1) % P) * pow(dl1, -1, P) % P

    vpk0 = base.monomial_mod(mon, n, k, l)
    vpk1 = base.monomial_mod(mon, n, k + 1, l)
    vql0 = base.monomial_mod(mon, n, l, k)
    vql1 = base.monomial_mod(mon, n, l + 1, k)

    return (
        pk0 * vpk0 % P * p0
        - pk1 * vpk1 % P * p1
        + ql0 * vql0 % P * q0
        - ql1 * vql1 % P * q1
    ) % P


def matrix_row(n: int, k: int, l: int, qdeg: int, reverse_basis: bool = False) -> list[int]:
    mons = list(reversed(MONOMS)) if reverse_basis else MONOMS
    exps = list(reversed(mon3(qdeg))) if reverse_basis else mon3(qdeg)
    return [flux_column_value(mon, ex, n, k, l) for mon in mons for ex in exps]


def stage(qdeg: int, nmax: int, exe: Path, tmp: Path) -> dict:
    unknowns = len(MONOMS) * len(mon3(qdeg))
    g = grid(nmax)
    need = unknowns + 1
    if len(g) < need:
        raise AssertionError("insufficient affine inconsistency witness rows")
    witness = g[:need]
    rows = [matrix_row(n, k, l, qdeg) for n, k, l in witness]
    target = [base.Fm(n, k, l) for n, k, l in witness]
    rank_coeff = rank_rows(rows, exe, tmp, f"q{qdeg}_coeff")
    rank_aug = rank_rows(rows, exe, tmp, f"q{qdeg}_aug", target)
    if rank_coeff == unknowns and rank_aug == unknowns + 1:
        classification = "EXACT_AFFINE_INCONSISTENCY"
        certificate = "FULL_COLUMN_RANK_COEFFICIENT_MATRIX_AND_ONE_HIGHER_AUGMENTED_RANK_MOD_P_IMPLIES_NO_RATIONAL_SOLUTION"
    elif rank_aug == rank_coeff:
        classification = "MODULAR_CANDIDATE_SPACE_REMAINS"
        certificate = "NO_NEGATIVE_CERTIFICATE"
    else:
        classification = "INCONCLUSIVE_MODULAR_RANK_RELATION"
        certificate = "NO_RATIONAL_CONCLUSION_WITHOUT_ADDITIONAL_WITNESS"
    return {
        "q_coefficient_degree": qdeg,
        "n_max": nmax,
        "full_grid_rows": len(g),
        "rank_witness_rows": need,
        "unknowns": unknowns,
        "coefficient_rank": rank_coeff,
        "augmented_rank": rank_aug,
        "classification": classification,
        "rank_certificate": certificate,
    }


def compute_result() -> dict:
    basis = base.basis_lock()
    norm = normalization_lock()
    symmetry = symmetry_and_boundary_lock()
    cross = base.exact_cross_lock()
    configs = {0: 8, 1: 13, 2: 18}
    with tempfile.TemporaryDirectory(prefix="t3_008_") as td:
        tmp = Path(td)
        exe = compile_rank(tmp)
        stages = [stage(q, configs[q], exe, tmp) for q in (0, 1, 2)]

    if all(x["classification"] == "EXACT_AFFINE_INCONSISTENCY" for x in stages):
        terminal = "SYMMETRIC_2D_WEIGHT5_DIVERGENCE_BOUNDED_CLASS_EXHAUSTED"
        next_route = "T3_SEQUENCE_RECURRENCE_EXTRACTION_001"
    elif any(x["classification"] == "MODULAR_CANDIDATE_SPACE_REMAINS" for x in stages):
        terminal = "CANDIDATE_SPACE_REMAINS_REQUIRING_RATIONAL_RECONSTRUCTION"
        next_route = "RATIONAL_RECONSTRUCTION_OF_SYMMETRIC_2D_DIVERGENCE_CANDIDATE"
    else:
        terminal = "OPEN_WITH_CHARACTERIZED_BLOCKER"
        next_route = "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001"

    return {
        "schema_version": "1.0.0",
        "operation": "OZ-RT-BZ-T3-008",
        "route": "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001",
        "prime": P,
        "target": "sum_{k,l=0}^n T(n,k,l)*(W1(k,l)+2*w5_sym(n,k,l))=0",
        "predecessor": {
            "issue": 359,
            "pull_request": 360,
            "merge_commit": "5233b37506f28e80959139cbc0f89b7ad400b658",
            "merge_tree": "5f5fc435927888fbdf84c1ba15044c347506fbd0",
        },
        "execution_intake": {
            "protected_head": "5233b37506f28e80959139cbc0f89b7ad400b658",
            "protected_tree": "5f5fc435927888fbdf84c1ba15044c347506fbd0",
        },
        "basis": basis,
        "coordinate_normalization": norm,
        "exact_target_cross_checks": cross,
        "symmetry_completeness": symmetry,
        "search_equation": "F(n,k,l)=Delta_k P(n,k,l)+Delta_l tau(P)(n,k,l)",
        "difference_convention": {
            "Delta_k": "P(n,k,l)-P(n,k+1,l)",
            "Delta_l": "Q(n,k,l)-Q(n,k,l+1)",
        },
        "flux": {
            "P": "T(n,k,l)*k*(n+1-k)/((k+1)^3*(k+l+1))*sum_M p_M(n,k,l)M(n,k,l)",
            "Q": "tau(P)",
            "k_denominator": "(k+1)^3*(k+l+1)",
            "l_denominator": "(l+1)^3*(k+l+1)",
            "k_boundary_factor": "k*(n+1-k)",
            "l_boundary_factor": "l*(n+1-l)",
        },
        "search_class": {
            "certificate_basis": "all 198 locked weight-five monomials with independent polynomial coefficients",
            "coefficient_degrees": [0, 1, 2],
            "symmetric_subspace_complete_for_declared_swap_closed_two_flux_class": True,
        },
        "stages": stages,
        "producer_witness_selection": "first unknowns+1 rows of the lexicographic finite-square grid",
        "negative_certificate_condition": "coefficient rank equals unknown count and augmented rank equals unknown count plus one modulo p",
        "terminal": terminal,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_distinct_route": next_route,
        "alternative_route_retained": "T3_SEQUENCE_RECURRENCE_EXTRACTION_001",
        "nonclaims": [
            "T3 is not proved unless an exact rational divergence certificate is reconstructed and boundary telescoping is verified",
            "T3 is not refuted",
            "bounded symmetric 2D divergence exhaustion is not evidence that T3 is false",
            "T1-top is not substituted for T3",
            "DEPTH and Sharp-12 are unchanged",
            "MATHCERT and GRAPH_CERTIFIED are unchanged",
        ],
    }


def main() -> int:
    result = compute_result()
    if OUT.exists():
        expected = json.loads(OUT.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError(f"canonical result drift: computed={digest(result)} expected={digest(expected)}")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
