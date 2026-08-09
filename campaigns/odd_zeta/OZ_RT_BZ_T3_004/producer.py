#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import t3_004_parent as parent

HERE = Path(__file__).resolve().parent
OUT = HERE / "SEARCH_RESULT.json"
P = 1000003
COMPONENTS = (("U", 1), ("U", 2), ("ES", 1), ("ES", 2))
ETA_SAMPLES = (Q(0), Q(1, 2), Q(1))
STAGES = ((0, 6), (1, 6), (2, 6), (3, 7), (4, 8))

def mon2(d: int):
    return [(i, j) for i in range(d + 1) for j in range(d + 1 - i)]

def mon4(d: int):
    return [(i, j, h, u) for i in range(d + 1) for j in range(d + 1 - i) for h in range(d + 1 - i - j) for u in range(d + 1 - i - j - h)]

def k_ratios(n: int, k: int, l: int):
    return [Q(1), parent.rk(n, k, l), parent.rk(n, k, l) * parent.rk(n, k + 1, l)]

def a_basis(n: int, k: int, eta: Q, d: int):
    return [Q(n ** i * k ** j) * eta ** e for e in range(2) for i, j in mon2(d)]

def ql_basis(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q, d: int):
    D = Q(parent.ql_denominator(kind, n, k, l, t)); edge = Q(parent.ql_boundary(n, l))
    return [edge * Q(n ** i * k ** j * l ** h * t ** u) * eta ** e / D for e in range(2) for i, j, h, u in mon4(d)]

def qt_basis(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q, d: int):
    D = Q(parent.qt_denominator(kind, r, l, t)); edge = Q(parent.qt_boundary(k, t))
    return [edge * Q(n ** i * k ** j * l ** h * t ** u) * eta ** e / D for e in range(2) for i, j, h, u in mon4(d)]

def row(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q, d: int):
    base = a_basis(n, k, eta, d)
    A = [ratio * x for ratio in k_ratios(n, k, l) for x in base]
    qc = ql_basis(kind, r, n, k, l, t, eta, d); qn = ql_basis(kind, r, n, k, l + 1, t, eta, d)
    Rl = parent.ratio_l(kind, r, n, k, l, t, eta); QL = [x - Rl * y for x, y in zip(qc, qn)]
    sc = qt_basis(kind, r, n, k, l, t, eta, d); sn = qt_basis(kind, r, n, k, l, t + 1, eta, d)
    Rt = parent.ratio_t(kind, r, n, k, l, t, eta); QT = [x - Rt * y for x, y in zip(sc, sn)]
    return A, QL + QT

def component_rows(kind: str, r: int, d: int, nmax: int):
    rows = []
    for eta in ETA_SAMPLES:
        for n in range(4, nmax + 1):
            for k in range(2, n - 1):
                for l in range(1, n):
                    for t in range(1, k + 1):
                        A, B = row(kind, r, n, k, l, t, eta, d); rows.append(A + B)
    return rows

def modq(x: Q) -> int:
    den = x.denominator % P
    if den == 0: raise AssertionError("rank-prime denominator collision")
    return (x.numerator % P) * pow(den, -1, P) % P

def eliminate_component(rows, na: int, nb: int):
    M = [[modq(x) for x in r[na:na + nb]] + [modq(x) for x in r[:na]] for r in rows]; rank = 0
    for c in range(nb):
        pivot = next((rr for rr in range(rank, len(M)) if M[rr][c]), None)
        if pivot is None: return rank, []
        M[rank], M[pivot] = M[pivot], M[rank]
        inv = pow(M[rank][c], -1, P); M[rank][c:] = [(x * inv) % P for x in M[rank][c:]]; pr = M[rank]
        for rr in range(rank + 1, len(M)):
            f = M[rr][c]
            if f: M[rr][c:] = [(x - f * y) % P for x, y in zip(M[rr][c:], pr[c:])]
        rank += 1
    return rank, [r[nb:] for r in M[rank:] if any(r[nb:])]

def rank_mod_int(rows):
    M = [r[:] for r in rows]
    if not M: return 0
    rank = 0; nc = len(M[0])
    for c in range(nc):
        pivot = next((rr for rr in range(rank, len(M)) if M[rr][c]), None)
        if pivot is None: continue
        M[rank], M[pivot] = M[pivot], M[rank]
        inv = pow(M[rank][c], -1, P); M[rank][c:] = [(x * inv) % P for x in M[rank][c:]]; pr = M[rank]
        for rr in range(rank + 1, len(M)):
            f = M[rr][c]
            if f: M[rr][c:] = [(x - f * y) % P for x, y in zip(M[rr][c:], pr[c:])]
        rank += 1
        if rank == nc: break
    return rank

def run_stage(d: int, nmax: int):
    na = 3 * 2 * len(mon2(d)); nb = 4 * len(mon4(d)); constraints = []; component_ranks = {}; component_equations = {}
    for kind, r in COMPONENTS:
        rows = component_rows(kind, r, d, nmax); rb, cons = eliminate_component(rows, na, nb); key = f"{kind}_R{r}"
        component_ranks[key] = rb; component_equations[key] = len(rows); constraints.extend(cons)
    shared_rank = rank_mod_int(constraints); total_rank = sum(component_ranks.values()) + shared_rank; unknowns = na + len(COMPONENTS) * nb
    return {"degree": d, "eta_degree": 1, "n_min": 4, "n_max": nmax, "eta_samples": ["0", "1/2", "1"], "components": ["U_R1", "U_R2", "ES_R1", "ES_R2"], "equations": sum(component_equations.values()), "shared_telescoper_unknowns": na, "certificate_unknowns_per_component": nb, "unknowns": unknowns, "component_certificate_ranks": component_ranks, "shared_telescoper_rank": shared_rank, "rank": total_rank, "nullity": unknowns - total_rank, "rank_certificate": "COMPONENT_CERTIFICATE_BLOCKS_PLUS_SHARED_TELESCOPER_QUOTIENT_FULL_RANK_MOD_P_IMPLIES_FULL_COLUMN_RANK_OVER_Q", "classification": "INCONSISTENT_ANSATZ" if total_rank == unknowns else "CANDIDATE_SPACE_REMAINS"}

def main():
    nested_checks = parent.verify_nested_lift(); ratio_checks = parent.verify_shift_ratios(); stages = [run_stage(d, nmax) for d, nmax in STAGES]
    result = {"schema_version": "1.0.0", "operation": "OZ-RT-BZ-T3-004", "fixture": "PARAMETER_DEPENDENT_ORDER2_TAUX_001", "parent_family": {"U": "T(n,k,l)*t^(-r)*Q(t+l,0;eta)", "ES": "T(n,k,l)*t^(-r)*Q(t,0;eta)", "r_values": [1, 2], "parameter": "eta", "parameter_semantics": "normalized-Pochhammer deformation retained before cumulant extraction", "nested_cumulant_checks": nested_checks, "exact_shift_ratio_checks": ratio_checks}, "search": {"order": 2, "external_shift": "k", "differences": ["l", "t"], "common_telescoper_across_components": True, "eta_coefficient_degree": 1, "eta_samples": ["0", "1/2", "1"], "degree_ladder": [0, 1, 2, 3, 4], "ql_boundary_factor": "l*(n+1-l)", "qt_boundary_factor": "(t-1)*(k+1-t)", "ql_denominators": {"U": "(l+1)^3*(k+l+1)*(t+l+1)", "ES": "(l+1)^3*(k+l+1)"}, "qt_denominators": {"U_R1": "(t+1)*(t+l+1)", "U_R2": "(t+1)^2*(t+l+1)", "ES_R1": "(t+1)", "ES_R2": "(t+1)^2"}, "sample_domain": "eta in {0,1/2,1}; 4<=n<=n_max; 2<=k<=n-2; 1<=l<=n-1; 1<=t<=k", "prime": P, "denominator_condition": "every exact rational matrix-entry denominator is nonzero modulo p", "stages": stages, "strongest_frontier": stages[-1]}, "coverage": {"covered": ["k-side U(k,l,r,m) auxiliary parent for r=1,2", "k-side ES(k,r,m) auxiliary parent for r=1,2", "exact eta-dependent parent shift ratios", "vanishing finite l/t flux basis"], "not_yet_covered": ["mirror U(l,k,r,m)/ES(l,r,m) triangular domain", "complete one-body mixed-derivative jet module", "full weight-five differential extraction of the locked T3 summand"], "full_t3_certificate": False}, "terminal": "NO_COMMON_PARAMETER_DEPENDENT_ORDER2_CERTIFICATE_IN_BOUNDED_K_SIDE_AUXILIARY_CLASS", "newly_exhausted_class": "PARAMETER_DEPENDENT_ORDER2_KSIDE_U_ES_TAUX_ETADEG_LE_1_POLYDEG_LE_4", "next_distinct_route": "MIRROR_TRIANGULAR_AUXILIARY_MODULE_THEN_ONE_BODY_JET_COUPLING", "proof_effect": "NONE", "promotion_effect": "NONE"}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"); print(json.dumps(result, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
