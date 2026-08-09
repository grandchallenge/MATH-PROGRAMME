#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import struct
import subprocess
import tempfile
from array import array
from fractions import Fraction as Q
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


def grid(nmax: int, nmin: int = 2):
    return [
        (n, k, l)
        for n in range(nmin, nmax + 1)
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
            a = array("I", (x % P for x in row))
            if target is not None:
                a.append(target[rix] % P)
            if a.itemsize != 4:
                raise AssertionError("unexpected unsigned-int width")
            a.tofile(f)
    return int(subprocess.check_output([str(exe), str(path)], text=True).strip())


def matrix_row(n: int, k: int, l: int, qdeg: int, reverse_basis: bool = False) -> list[int]:
    mons = list(reversed(MONOMS)) if reverse_basis else MONOMS
    exps = list(reversed(mon3(qdeg))) if reverse_basis else mon3(qdeg)

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
    for mon in mons:
        a0 = pk0 * base.monomial_mod(mon, n, k, l) % P
        a1 = pk1 * base.monomial_mod(mon, n, k + 1, l) % P
        b0 = ql0 * base.monomial_mod(mon, n, l, k) % P
        b1 = ql1 * base.monomial_mod(mon, n, l + 1, k) % P
        for p0, p1, q0, q1 in poly:
            row.append((a0 * p0 - a1 * p1 + b0 * q0 - b1 * q1) % P)
    return row


def classify_affine(rank_coeff: int, rank_aug: int, unknowns: int) -> tuple[str, str]:
    if rank_coeff == unknowns and rank_aug == unknowns + 1:
        return (
            "EXACT_AFFINE_INCONSISTENCY",
            "FULL_COLUMN_RANK_COEFFICIENT_MATRIX_AND_ONE_HIGHER_AUGMENTED_RANK_MOD_P_IMPLIES_NO_RATIONAL_SOLUTION",
        )
    if rank_aug == rank_coeff:
        return (
            "MODULAR_CANDIDATE_SPACE_REMAINS",
            "EQUAL_MODULAR_RANKS_ARE_DISCOVERY_ONLY_AND_DO_NOT_ESTABLISH_RATIONAL_CONSISTENCY",
        )
    return (
        "INCONCLUSIVE_MODULAR_RANK_RELATION",
        "MODULAR_RANK_GAP_WITHOUT_FULL_COLUMN_RANK_DOES_NOT_CERTIFY_RATIONAL_INCONSISTENCY",
    )


def stage(qdeg: int, nmax: int, exe: Path, tmp: Path) -> dict:
    unknowns = len(MONOMS) * len(mon3(qdeg))
    g = grid(nmax)
    need = unknowns + 1
    if len(g) < need:
        raise AssertionError("insufficient affine inconsistency witness rows")

    rows = [matrix_row(n, k, l, qdeg) for n, k, l in g]
    target = [base.Fm(n, k, l) for n, k, l in g]

    witness_rows = rows[:need]
    witness_target = target[:need]
    witness_coeff = rank_rows(witness_rows, exe, tmp, f"q{qdeg}_witness_coeff")
    witness_aug = rank_rows(witness_rows, exe, tmp, f"q{qdeg}_witness_aug", witness_target)

    full_coeff = rank_rows(rows, exe, tmp, f"q{qdeg}_full_coeff")
    full_aug = rank_rows(rows, exe, tmp, f"q{qdeg}_full_aug", target)
    classification, certificate = classify_affine(full_coeff, full_aug, unknowns)

    return {
        "q_coefficient_degree": qdeg,
        "n_max": nmax,
        "full_grid_rows": len(g),
        "rank_witness_rows": need,
        "unknowns": unknowns,
        "witness_coefficient_rank": witness_coeff,
        "witness_augmented_rank": witness_aug,
        "full_grid_coefficient_rank": full_coeff,
        "full_grid_augmented_rank": full_aug,
        "classification": classification,
        "rank_certificate": certificate,
    }


def solve_mod(rows: list[list[int]], target: list[int]) -> tuple[list[int], int, list[int]]:
    if not rows or len(rows) != len(target):
        raise AssertionError("invalid modular solve system")
    nc = len(rows[0])
    a = [[x % P for x in row] + [target[i] % P] for i, row in enumerate(rows)]
    nr = len(a)
    pivots: list[int] = []
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, P)
        a[r][c:] = [(v * inv) % P for v in a[r][c:]]
        for i in range(r + 1, nr):
            f = a[i][c]
            if not f:
                continue
            rowi = a[i]
            rowr = a[r]
            rowi[c] = 0
            for j in range(c + 1, nc + 1):
                rowi[j] = (rowi[j] - f * rowr[j]) % P
        pivots.append(c)
        r += 1
        if r == nr:
            break
    for i in range(r, nr):
        if all(a[i][j] == 0 for j in range(nc)) and a[i][nc] != 0:
            raise AssertionError("modular system became inconsistent")
    x = [0] * nc
    for i in range(r - 1, -1, -1):
        c = pivots[i]
        rhs = a[i][nc]
        for j in range(c + 1, nc):
            rhs = (rhs - a[i][j] * x[j]) % P
        x[c] = rhs
    for row, rhs in zip(rows, target):
        if sum((v * z for v, z in zip(row, x)), 0) % P != rhs % P:
            raise AssertionError("canonical modular particular solution failed reconstruction grid")
    return x, r, pivots


def rational_reconstruct(x: int) -> Q | None:
    x %= P
    if x == 0:
        return Q(0)
    bound = math.isqrt((P - 1) // 2)
    r0, r1 = P, x
    s0, s1 = 0, 1
    while abs(r1) > bound and r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0:
        return None
    num, den = r1, s1
    if den < 0:
        num, den = -num, -den
    g = math.gcd(abs(num), den)
    num //= g
    den //= g
    if abs(num) > bound or den > bound or (num - x * den) % P != 0:
        return None
    return Q(num, den)


def atom_exact(name: str, n: int, k: int, l: int) -> Q:
    p = name.split("_")
    t = base.target002
    if name.startswith("H_k_"):
        return t.H(k, int(p[-1]))
    if name.startswith("H_l_"):
        return t.H(l, int(p[-1]))
    if name.startswith("H_kl_"):
        return t.H(k + l, int(p[-1]))
    if name.startswith("H_nk_"):
        return t.H(n + k, int(p[-1]))
    if name.startswith("H_nl_"):
        return t.H(n + l, int(p[-1]))
    if name.startswith("A_k_"):
        return t.A(n, k, int(p[-1]))
    if name.startswith("A_l_"):
        return t.A(n, l, int(p[-1]))
    if name.startswith("B_k_"):
        return t.B(n, k, int(p[-1]))
    if name.startswith("B_l_"):
        return t.B(n, l, int(p[-1]))
    if name.startswith("C_"):
        return t.C(n, k, l, int(p[-1]))
    if name.startswith("U_k_l_"):
        r, m = map(int, p[-2:]); return t.U(k, l, r, m)
    if name.startswith("U_l_k_"):
        r, m = map(int, p[-2:]); return t.U(l, k, r, m)
    if name.startswith("ES_k_"):
        r, m = map(int, p[-2:]); return t.ES(k, r, m)
    if name.startswith("ES_l_"):
        r, m = map(int, p[-2:]); return t.ES(l, r, m)
    raise ValueError(name)


def monomial_exact(mon: tuple[str, ...], n: int, k: int, l: int) -> Q:
    out = Q(1)
    for name in mon:
        out *= atom_exact(name, n, k, l)
    return out


def exact_degree0_value(coeffs: list[Q], n: int, k: int, l: int) -> Q:
    t = base.target002
    pk0 = Q(t.T(n, k, l) * boundary(n, k), d_k(k, l))
    pk1 = Q(t.T(n, k + 1, l) * boundary(n, k + 1), d_k(k + 1, l))
    ql0 = Q(t.T(n, k, l) * boundary(n, l), d_l(k, l))
    ql1 = Q(t.T(n, k, l + 1) * boundary(n, l + 1), d_l(k, l + 1))
    value = Q(0)
    for coeff, mon in zip(coeffs, MONOMS):
        if coeff == 0:
            continue
        value += coeff * (
            pk0 * monomial_exact(mon, n, k, l)
            - pk1 * monomial_exact(mon, n, k + 1, l)
            + ql0 * monomial_exact(mon, n, l, k)
            - ql1 * monomial_exact(mon, n, l + 1, k)
        )
    return value


def degree0_reconstruction_probe(exe: Path, tmp: Path) -> dict:
    extended_nmax = 20
    g = grid(extended_nmax)
    rows = [matrix_row(n, k, l, 0) for n, k, l in g]
    target = [base.Fm(n, k, l) for n, k, l in g]
    rank_coeff = rank_rows(rows, exe, tmp, "q0_extended_coeff")
    rank_aug = rank_rows(rows, exe, tmp, "q0_extended_aug", target)
    out = {
        "extended_n_max": extended_nmax,
        "extended_grid_rows": len(g),
        "coefficient_rank": rank_coeff,
        "augmented_rank": rank_aug,
        "modular_candidate_survives": rank_coeff == rank_aug,
    }
    if rank_coeff != rank_aug:
        return out

    coeffs_mod, solve_rank, pivots = solve_mod(rows, target)
    holdout = grid(24, 21)
    holdout_failures = []
    for n, k, l in holdout:
        row = matrix_row(n, k, l, 0)
        lhs = sum((v * z for v, z in zip(row, coeffs_mod)), 0) % P
        rhs = base.Fm(n, k, l)
        if lhs != rhs:
            holdout_failures.append([n, k, l])
            if len(holdout_failures) >= 5:
                break

    reconstructed = [rational_reconstruct(x) for x in coeffs_mod]
    rr_complete = all(x is not None for x in reconstructed)
    exact_checks = 0
    exact_failure = None
    if rr_complete:
        coeffs_q = [x if x is not None else Q(0) for x in reconstructed]
        for n in range(2, 10):
            for k in range(n + 1):
                for l in range(n + 1):
                    if exact_degree0_value(coeffs_q, n, k, l) != base.target002.cell(n, k, l):
                        exact_failure = [n, k, l]
                        break
                    exact_checks += 1
                if exact_failure is not None:
                    break
            if exact_failure is not None:
                break

    centered = [x if x <= P // 2 else x - P for x in coeffs_mod]
    nonzero = [x for x in centered if x]
    out.update({
        "canonical_particular_solution_rank": solve_rank,
        "pivot_count": len(pivots),
        "free_variable_count": len(MONOMS) - len(pivots),
        "candidate_vector_sha256": hashlib.sha256(
            json.dumps(coeffs_mod, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "nonzero_coefficient_count": len(nonzero),
        "max_abs_centered_residue": max((abs(x) for x in nonzero), default=0),
        "holdout_n_range": [21, 24],
        "holdout_cell_count": len(holdout),
        "holdout_failures": holdout_failures,
        "rational_reconstruction_bound": math.isqrt((P - 1) // 2),
        "rational_reconstruction_complete": rr_complete,
        "rational_reconstruction_exact_checks": exact_checks,
        "rational_reconstruction_first_exact_failure": exact_failure,
    })
    return out


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
        reconstruction = degree0_reconstruction_probe(exe, tmp)

    if reconstruction.get("rational_reconstruction_complete") and not reconstruction.get("rational_reconstruction_first_exact_failure"):
        terminal = "EXACT_DEGREE0_DIVERGENCE_CANDIDATE_RECONSTRUCTED_REQUIRING_INDEPENDENT_PROOF_REPLAY"
        next_route = "EXACT_SYMMETRIC_2D_DIVERGENCE_CERTIFICATE_VERIFICATION_001"
    elif reconstruction.get("modular_candidate_survives"):
        terminal = "CANDIDATE_SPACE_REMAINS_REQUIRING_RATIONAL_RECONSTRUCTION"
        next_route = "RATIONAL_RECONSTRUCTION_OF_SYMMETRIC_2D_DIVERGENCE_CANDIDATE"
    elif all(x["classification"] == "EXACT_AFFINE_INCONSISTENCY" for x in stages):
        terminal = "SYMMETRIC_2D_WEIGHT5_DIVERGENCE_BOUNDED_CLASS_EXHAUSTED"
        next_route = "T3_SEQUENCE_RECURRENCE_EXTRACTION_001"
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
        "degree0_reconstruction_probe": reconstruction,
        "producer_witness_selection": "first unknowns+1 rows of the lexicographic finite-square grid",
        "candidate_survival_rule": "only full-grid coefficient/augmented rank equality retains a modular candidate space; this remains discovery only",
        "negative_certificate_condition": "full-grid coefficient rank equals unknown count and full-grid augmented rank equals unknown count plus one modulo p",
        "terminal": terminal,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_distinct_route": next_route,
        "alternative_route_retained": "T3_SEQUENCE_RECURRENCE_EXTRACTION_001",
        "nonclaims": [
            "T3 is not proved unless an exact rational divergence certificate is independently reconstructed, symbolically verified, and boundary telescoping is proved",
            "T3 is not refuted",
            "modular candidate survival does not establish rational consistency",
            "finite exact sample verification does not establish the symbolic divergence identity",
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
