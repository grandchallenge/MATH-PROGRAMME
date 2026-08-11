#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction as Q
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "OZ_RT_BZ_T3_002" / "target.py"
CANONICALIZER = HERE / "residual_canonical.py"
LOCK = HERE / "RECURRENCE_LOCK.json"
BASELINE = HERE / "BASELINE_RESULT.json"
CANONICAL_RESULT = HERE / "RESIDUAL_CANONICAL_RESULT.json"
SYMMETRIC_GAUGE = HERE / "QROW_SYMMETRIC_GAUGE.json"

spec = importlib.util.spec_from_file_location("t3_002_target_independent_for_t3_009", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected T3 target")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

cspec = importlib.util.spec_from_file_location("t3_009_residual_canonical_for_verify", CANONICALIZER)
if cspec is None or cspec.loader is None:
    raise RuntimeError("cannot load residual canonicalizer")
rc = importlib.util.module_from_spec(cspec)
cspec.loader.exec_module(rc)

EXPECTED_DIGESTS = {
    "n1": "ad46afea7d769dcba9d9c8a7b7842bcf72adfa1df0ae05f0734ec25432772655",
    "n2": "9c7a4849b95b1ab33670bbc8c2eb218df883cbf19add702f9228b4503b6b2b0e",
    "n3": "1e6f8e8ce6cf37b71dd741299c2ce5d1927225c5f08927b66c832a1687814a69",
    "k1": "ba7fa0176dc782b6c0747a71a9a0e13c3c5cf3d0c6077efe6f99c2a461c34780",
    "l1": "4fd7277655900f62a9f3676fd1d54614205cf8142cf26c04a4ef74eb8dfdc4c6",
}
EXPECTED_PROFILES = {
    "n1": (102,27,3), "n2": (102,27,3), "n3": (102,27,3),
    "k1": (134,28,3), "l1": (134,28,3),
}


def a0(n): return 41218*n**3 + 198849*n**2 + 320790*n + 173057

def B8(n):
    return (3874492*n**8 + 59373972*n**7 + 394148190*n**6 + 1481084196*n**5
            + 3447878810*n**4 + 5095855458*n**3 + 4673546679*n**2
            + 2433871008*n + 551502039)

def B9(n):
    return (48802112*n**9 + 967468896*n**8 + 8488000862*n**7 + 43246197636*n**6
            + 140983768422*n**5 + 304912330849*n**4 + 437406946975*n**3
            + 401272692378*n**2 + 213593890911*n + 50257929339)

def cs(n):
    return ((n+1)**5*(n+2)*a0(n+1), -2*(n+2)*B8(n), -2*B9(n), 2*(n+3)**5*(2*n+5)*a0(n))

def p5(n):
    return sum((Q(t.T(n,k,l))*t.w5sym(n,k,l) for k in range(n+1) for l in range(n+1)), Q(0))

def w(n):
    return sum((Q(t.T(n,k,l))*t.W1(n,k,l) for k in range(n+1) for l in range(n+1)), Q(0))

def d(n): return w(n) + 2*p5(n)

def R(f,n): return sum((Q(c)*f(n+j) for j,c in enumerate(cs(n))), Q(0))

def dweight(n,k,l): return t.W1(n,k,l) + 2*t.w5sym(n,k,l)


def atom_value(name: str, n: int, k: int, l: int) -> Q:
    p=name.split("_")
    r=int(p[-1])
    if name.startswith("H_k_"): return t.H(k,r)
    if name.startswith("H_l_"): return t.H(l,r)
    if name.startswith("H_kl_"): return t.H(k+l,r)
    if name.startswith("H_nk_"): return t.H(n+k,r)
    if name.startswith("H_nl_"): return t.H(n+l,r)
    if name.startswith("A_k_"): return t.A(n,k,r)
    if name.startswith("A_l_"): return t.A(n,l,r)
    if name.startswith("B_k_"): return t.B(n,k,r)
    if name.startswith("B_l_"): return t.B(n,l,r)
    if name.startswith("C_"): return t.C(n,k,l,r)
    if name.startswith("ES_k_"):
        rr,mm=map(int,p[-2:]); return t.ES(k,rr,mm)
    if name.startswith("ES_l_"):
        rr,mm=map(int,p[-2:]); return t.ES(l,rr,mm)
    if name.startswith("U_k_l_"):
        rr,mm=map(int,p[-2:]); return t.U(k,l,rr,mm)
    if name.startswith("U_l_k_"):
        rr,mm=map(int,p[-2:]); return t.U(l,k,rr,mm)
    raise ValueError(f"unknown independent atom {name}")


def coefficient_value(coeff, n: int, k: int, l: int) -> Q:
    out=Q(0)
    for sig,c in coeff.items():
        v=Q(c)
        for (a,b,cc,d0), exponent in sig:
            z=a*n+b*k+cc*l+d0
            if z == 0 and exponent < 0:
                raise ZeroDivisionError((a,b,cc,d0,exponent,n,k,l))
            v *= Q(z) ** exponent
        out += v
    return out


def independent_poly_value(poly, n: int, k: int, l: int) -> Q:
    out=Q(0)
    for mon,coeff in poly.items():
        v=coefficient_value(coeff,n,k,l)
        for name in mon:
            v *= atom_value(name,n,k,l)
        out += v
    return out


def verify_partial_fraction_table() -> None:
    # Independent combinatorial derivation of
    # 1/(x^r (x+d)^m) = sum_i A_i/x^i + sum_j B_j/(x+d)^j.
    for (r,m), rows in rc.PF.items():
        got={(family,s,dpow):Q(c) for c,dpow,family,s in rows}
        want={}
        for i in range(1,r+1):
            q=r-i
            want[("upper",i,m+q)] = Q((-1)**q * comb(m+q-1,q))
        for j in range(1,m+1):
            q=m-j
            want[("shifted",j,r+q)] = Q((-1)**r * comb(r+q-1,q))
        if got != want:
            raise AssertionError(f"independent U partial-fraction reconstruction drift: {(r,m)}")


def verify_canonical_maps() -> int:
    retained=json.loads(CANONICAL_RESULT.read_text(encoding="utf-8"))
    result,deltas=rc.build_all()
    if result["closure_only_atoms"] != []:
        raise AssertionError("canonical atom closure unexpectedly enlarged")
    if result["bundle_sha256"] != retained["producer_cross_checks"]["bundle_sha256"]:
        raise AssertionError("canonical bundle digest drift")
    shifts={"n1":(1,0,0),"n2":(2,0,0),"n3":(3,0,0),"k1":(0,1,0),"l1":(0,0,1)}
    for label,poly in deltas.items():
        row=result["shifts"][label]
        if rc.digest_poly(poly) != EXPECTED_DIGESTS[label]:
            raise AssertionError(f"canonical digest drift: {label}")
        if (row["canonical_monomials"],row["atom_count"],row["max_atomic_arity"]) != EXPECTED_PROFILES[label]:
            raise AssertionError(f"canonical profile drift: {label}")
    verify_partial_fraction_table()
    checks=0
    samples=[(6,1,2),(7,2,1),(8,3,2),(9,2,4),(10,4,3),(11,3,5)]
    protected_atoms=retained["protected_target"]["atom_count"]
    if protected_atoms != 41:
        raise AssertionError("protected atom-count drift")
    # Independent evaluation path: canonical coefficients are interpreted here,
    # while all harmonic/nested atoms and Dweight come from T3-002 target.py.
    for label,(dn,dk,dl) in shifts.items():
        for n,k,l in samples:
            got=independent_poly_value(deltas[label],n,k,l)
            want=dweight(n+dn,k+dk,l+dl)-dweight(n,k,l)
            if got != want:
                raise AssertionError(f"independent canonical D shift replay drift {label}@{(n,k,l)}")
            checks += 1
    return checks


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    gauge = json.loads(SYMMETRIC_GAUGE.read_text(encoding="utf-8"))
    if lock["order"] != 3 or lock["normalization_drift_allowed"]:
        raise AssertionError("operator lock drift")
    if lock["source"]["commit"] != "968477ed7e406df6542f8da6fbe1cd6ca7273c47":
        raise AssertionError("source pin drift")
    if not all(x > 0 for x in (41218,198849,320790,173057)):
        raise AssertionError("a0 coefficient positivity lost")
    for n in range(7):
        row = baseline["finite_component_baseline"][n]
        vals = (p5(n), w(n), d(n))
        exp = tuple(Q(*row[key]) for key in ("P5","W","D"))
        if vals != exp:
            raise AssertionError(f"source-normalized finite baseline drift at n={n}")
    if p5(1) != Q(87,4) or w(1) != Q(-87,2):
        raise AssertionError("nonvacuity witness drift")
    for n in range(4):
        if R(p5,n) != 0 or R(w,n) != 0 or R(d,n) != 0:
            raise AssertionError(f"finite operator residual drift at n={n}")
    for n in range(25):
        if cs(n)[3] <= 0:
            raise AssertionError("forward coefficient positivity failure")
    if baseline["proof_effect"] != "NONE" or baseline["promotion_effect"] != "NONE":
        raise AssertionError("finite evidence promoted")
    if not gauge["exact_replay"]["rho_sym_equals_swapped_sigma_sym"] or not gauge["exact_replay"]["cleared_kernel_identity_numerator_zero"]:
        raise AssertionError("symmetric Q-row gauge drift")
    checks=verify_canonical_maps()
    print(f"T3-009 independent locked-operator and canonical direct E_D replay: OK ({checks} independent full-shift checks)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
