#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T3_005 = HERE.parent / "OZ_RT_BZ_T3_005"
if str(T3_005) not in sys.path:
    sys.path.insert(0, str(T3_005))
import jet_map  # type: ignore
import t3_005_parent as parent  # type: ignore

# Coefficient ring: finite Q-linear combinations of Laurent monomials in
# integer-affine linear forms a*n+b*k+c*l+d.  This is sufficient for every
# exact shift increment of the protected weight-five atom system.
Factor = tuple[int, int, int, int]
Sig = tuple[tuple[Factor, int], ...]
Rat = dict[Sig, Q]
Mon = tuple[str, ...]
Poly = dict[Mon, Rat]

ZERO_FACTOR: Sig = ()


def _sig(items: dict[Factor, int]) -> Sig:
    return tuple(sorted((f, e) for f, e in items.items() if e))


def r_const(x=0) -> Rat:
    x = Q(x)
    return {ZERO_FACTOR: x} if x else {}


def r_factor(f: Factor, exponent: int = -1, scale=1) -> Rat:
    c = Q(scale)
    return {_sig({f: exponent}): c} if c else {}


def r_add(*xs: Rat) -> Rat:
    out: defaultdict[Sig, Q] = defaultdict(Q)
    for x in xs:
        for s, c in x.items():
            out[s] += c
    return {s: c for s, c in out.items() if c}


def r_scale(x: Rat, c) -> Rat:
    c = Q(c)
    return {s: c*v for s, v in x.items() if c*v}


def r_mul(a: Rat, b: Rat) -> Rat:
    out: defaultdict[Sig, Q] = defaultdict(Q)
    for sa, ca in a.items():
        da = dict(sa)
        for sb, cb in b.items():
            d = dict(da)
            for f, e in sb:
                d[f] = d.get(f, 0) + e
                if d[f] == 0:
                    del d[f]
            out[_sig(d)] += ca*cb
    return {s: c for s, c in out.items() if c}


def r_eval(x: Rat, n: int, k: int, l: int) -> Q:
    out = Q(0)
    for sig, c in x.items():
        v = c
        for (a,b,cc,d), e in sig:
            z = a*n+b*k+cc*l+d
            if z == 0 and e < 0:
                raise ZeroDivisionError((a,b,cc,d,e,n,k,l))
            v *= Q(z) ** e
        out += v
    return out


def p_const(c=0) -> Poly:
    r = r_const(c)
    return {(): r} if r else {}


def p_atom(name: str) -> Poly:
    return {(name,): r_const(1)}


def p_add(*xs: Poly) -> Poly:
    out: dict[Mon, Rat] = {}
    for x in xs:
        for m, c in x.items():
            z = r_add(out.get(m, {}), c)
            if z:
                out[m] = z
            elif m in out:
                del out[m]
    return out


def p_scale(x: Poly, c) -> Poly:
    if isinstance(c, dict):
        return {m: r_mul(v, c) for m, v in x.items() if r_mul(v, c)}
    return {m: r_scale(v, c) for m, v in x.items() if r_scale(v, c)}


def p_mul(a: Poly, b: Poly) -> Poly:
    out: dict[Mon, Rat] = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(sorted(ma+mb))
            z = r_add(out.get(m, {}), r_mul(ca, cb))
            if z:
                out[m] = z
            elif m in out:
                del out[m]
    return out


def inv(f: Factor, power: int = 1) -> Rat:
    return r_factor(f, -power)


def lin_nk(c: int) -> Factor: return (1,1,0,c)
def lin_nl(c: int) -> Factor: return (1,0,1,c)
def lin_nmink(c: int) -> Factor: return (1,-1,0,c)
def lin_nminl(c: int) -> Factor: return (1,0,-1,c)
def lin_nkl(c: int) -> Factor: return (1,1,1,c)
def lin_k(c: int) -> Factor: return (0,1,0,c)
def lin_l(c: int) -> Factor: return (0,0,1,c)
def lin_kl(c: int) -> Factor: return (0,1,1,c)


def sum_inv(forms: list[Factor], power: int) -> Rat:
    return r_add(*(inv(f, power) for f in forms))


def delta_atom(name: str, shift: tuple[int,int,int]) -> Poly:
    dn, dk, dl = shift
    if sum(int(x != 0) for x in shift) != 1 or dn not in (0,1,2,3) or dk not in (0,1) or dl not in (0,1):
        raise ValueError(f"unsupported shift {shift}")
    r = int(name.split("_")[-1])

    if name.startswith("H_nk_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nk(i) for i in range(1,dn+1)], r))
        if dk: return p_scale(p_const(1), inv(lin_nk(1), r))
        return {}
    if name.startswith("H_nl_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nl(i) for i in range(1,dn+1)], r))
        if dl: return p_scale(p_const(1), inv(lin_nl(1), r))
        return {}
    if name.startswith("H_kl_"):
        if dk or dl: return p_scale(p_const(1), inv(lin_kl(1), r))
        return {}
    if name.startswith("H_k_"):
        if dk: return p_scale(p_const(1), inv(lin_k(1), r))
        return {}
    if name.startswith("H_l_"):
        if dl: return p_scale(p_const(1), inv(lin_l(1), r))
        return {}

    if name.startswith("A_k_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nk(i) for i in range(1,dn+1)], r))
        if dk: return p_scale(p_const(1), r_add(inv(lin_nk(1),r), r_scale(inv(lin_k(1),r),-1)))
        return {}
    if name.startswith("A_l_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nl(i) for i in range(1,dn+1)], r))
        if dl: return p_scale(p_const(1), r_add(inv(lin_nl(1),r), r_scale(inv(lin_l(1),r),-1)))
        return {}
    if name.startswith("B_k_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nmink(i) for i in range(1,dn+1)], r))
        if dk: return p_scale(p_const(1), r_scale(r_add(inv(lin_nmink(0),r),inv(lin_k(1),r)),-1))
        return {}
    if name.startswith("B_l_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nminl(i) for i in range(1,dn+1)], r))
        if dl: return p_scale(p_const(1), r_scale(r_add(inv(lin_nminl(0),r),inv(lin_l(1),r)),-1))
        return {}
    if name.startswith("C_"):
        if dn: return p_scale(p_const(1), sum_inv([lin_nkl(i) for i in range(1,dn+1)], r))
        if dk or dl: return p_scale(p_const(1), r_add(inv(lin_nkl(1),r),r_scale(inv(lin_kl(1),r),-1)))
        return {}

    if name.startswith("ES_k_"):
        _,_,rr,mm = name.split("_"); rr=int(rr); mm=int(mm)
        if dk:
            return p_add(p_scale(p_atom(f"H_k_{mm}"), inv(lin_k(1),rr)),
                         p_scale(p_const(1), inv(lin_k(1),rr+mm)))
        return {}
    if name.startswith("ES_l_"):
        _,_,rr,mm = name.split("_"); rr=int(rr); mm=int(mm)
        if dl:
            return p_add(p_scale(p_atom(f"H_l_{mm}"), inv(lin_l(1),rr)),
                         p_scale(p_const(1), inv(lin_l(1),rr+mm)))
        return {}

    if name.startswith("U_k_l_"):
        *_, rr, mm = name.split("_"); rr=int(rr); mm=int(mm)
        if dk:
            return p_add(p_scale(p_atom(f"H_kl_{mm}"), inv(lin_k(1),rr)),
                         p_scale(p_const(1), r_mul(inv(lin_k(1),rr),inv(lin_kl(1),mm))))
        if dl:
            return secondary_increment("k","l",rr,mm)
        return {}
    if name.startswith("U_l_k_"):
        *_, rr, mm = name.split("_"); rr=int(rr); mm=int(mm)
        if dl:
            return p_add(p_scale(p_atom(f"H_kl_{mm}"), inv(lin_l(1),rr)),
                         p_scale(p_const(1), r_mul(inv(lin_l(1),rr),inv(lin_kl(1),mm))))
        if dk:
            return secondary_increment("l","k",rr,mm)
        return {}
    raise ValueError(f"unknown protected atom {name}")


PF = {
    (1,2): [(-1,1,"shifted",2),(-1,2,"shifted",1),(1,2,"upper",1)],
    (2,2): [(1,2,"shifted",2),(1,2,"upper",2),(2,3,"shifted",1),(-2,3,"upper",1)],
    (1,4): [(-1,1,"shifted",4),(-1,2,"shifted",3),(-1,3,"shifted",2),(-1,4,"shifted",1),(1,4,"upper",1)],
    (2,3): [(1,2,"shifted",3),(2,3,"shifted",2),(1,3,"upper",2),(3,4,"shifted",1),(-3,4,"upper",1)],
}


def secondary_increment(upper: str, offset: str, rr: int, mm: int) -> Poly:
    if (rr,mm) not in PF:
        raise ValueError(f"unlocked U partial-fraction type {(rr,mm)}")
    d = lin_l(1) if offset == "l" else lin_k(1)
    upper_h = (lambda s: f"H_k_{s}") if upper == "k" else (lambda s: f"H_l_{s}")
    offset_h = (lambda s: f"H_l_{s}") if offset == "l" else (lambda s: f"H_k_{s}")
    out: Poly = {}
    for c, dpow, family, s in PF[(rr,mm)]:
        pref = r_scale(inv(d,dpow),c)
        if family == "upper":
            out = p_add(out,p_scale(p_atom(upper_h(s)),pref))
        else:
            # Sum_{t=1}^upper (t+d)^(-s)
            # = H_{k+l+1}^{(s)}-H_{offset+1}^{(s)}
            # = H_{k+l}^{(s)}-H_offset^{(s)}+(k+l+1)^(-s)-(offset+1)^(-s).
            out = p_add(out,
                p_scale(p_atom(f"H_kl_{s}"),pref),
                p_scale(p_atom(offset_h(s)),r_scale(pref,-1)),
                p_scale(p_const(1),r_mul(pref,inv(lin_kl(1),s))),
                p_scale(p_const(1),r_scale(r_mul(pref,inv(d,s)),-1)))
    return out


def shift_atom(name: str, shift: tuple[int,int,int]) -> Poly:
    return p_add(p_atom(name),delta_atom(name,shift))


def target_poly() -> Poly:
    out: Poly = {}
    for mon,c in jet_map.target_polynomial().items():
        out = p_add(out,{tuple(mon):r_const(c)})
    return out


def shifted_target(shift: tuple[int,int,int]) -> Poly:
    out: Poly = {}
    for mon,c in jet_map.target_polynomial().items():
        q = p_const(c)
        for name in mon:
            q = p_mul(q,shift_atom(name,shift))
        out = p_add(out,q)
    return out


def delta_target(shift: tuple[int,int,int]) -> Poly:
    return p_add(shifted_target(shift),p_scale(target_poly(),-1))


def atom_value(name: str,n: int,k: int,l: int) -> Q:
    if name.startswith(("U_","ES_")):
        return parent.nested_atom_value(name,n,k,l)
    return parent.one_body_atom_value(name,n,k,l)


def eval_poly(poly: Poly,n: int,k: int,l: int) -> Q:
    out=Q(0)
    for mon,c in poly.items():
        v=r_eval(c,n,k,l)
        for name in mon:
            v*=atom_value(name,n,k,l)
        out+=v
    return out


def rat_json(x: Rat):
    rows=[]
    for sig,c in sorted(x.items()):
        rows.append([c.numerator,c.denominator,[[list(f),e] for f,e in sig]])
    return rows


def poly_json(x: Poly):
    return [[list(mon),rat_json(c)] for mon,c in sorted(x.items())]


def digest_poly(x: Poly) -> str:
    raw=json.dumps(poly_json(x),sort_keys=False,separators=(",",":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def atom_set(poly: Poly) -> set[str]:
    return {a for mon in poly for a in mon}


def verify_exact(deltas: dict[str,Poly]) -> int:
    checks=0
    shifts={"n1":(1,0,0),"n2":(2,0,0),"n3":(3,0,0),"k1":(0,1,0),"l1":(0,0,1)}
    protected_atoms=sorted({a for mon in jet_map.target_polynomial() for a in mon})
    samples=[(6,1,2),(7,2,1),(8,3,2),(9,2,4)]
    for label,shift in shifts.items():
        dn,dk,dl=shift
        for n,k,l in samples:
            # independent atom-shift replay against direct protected atom definitions
            for name in protected_atoms:
                got=eval_poly(delta_atom(name,shift),n,k,l)
                want=atom_value(name,n+dn,k+dk,l+dl)-atom_value(name,n,k,l)
                if got!=want:
                    raise AssertionError(f"atom shift drift {label}:{name}@{(n,k,l)}")
                checks+=1
            got=eval_poly(deltas[label],n,k,l)
            want=jet_map.direct_target(n+dn,k+dk,l+dl)-jet_map.direct_target(n,k,l)
            if got!=want:
                raise AssertionError(f"D shift canonicalization drift {label}@{(n,k,l)}")
            checks+=1
    return checks


def build_all():
    shifts={"n1":(1,0,0),"n2":(2,0,0),"n3":(3,0,0),"k1":(0,1,0),"l1":(0,0,1)}
    deltas={lab:delta_target(sh) for lab,sh in shifts.items()}
    protected=sorted({a for mon in jet_map.target_polynomial() for a in mon})
    closure=sorted(set().union(*(atom_set(p) for p in deltas.values()))-set(protected))
    checks=verify_exact(deltas)
    result={
        "schema_version":"1.0.0",
        "operation":"OZ-RT-BZ-T3-009",
        "subroute":"QROW_PRODUCT_RULE_REDUCTION_001",
        "object":"DIRECT_E_D_WEIGHT_DIFFERENCE_CANONICALIZATION",
        "protected_target_monomials":len(jet_map.target_polynomial()),
        "protected_atom_count":len(protected),
        "protected_atoms":protected,
        "closure_only_atoms":closure,
        "coefficient_ring":"Q-linear Laurent monomials in integer-affine forms a*n+b*k+c*l+d",
        "shifts":{},
        "exact_independent_checks":checks,
        "proof_effect":"NONE",
        "promotion_effect":"NONE",
        "t3_status":"OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
    for lab,p in deltas.items():
        result["shifts"][lab]={
            "canonical_monomials":len(p),
            "atom_count":len(atom_set(p)),
            "max_atomic_arity":max((len(m) for m in p),default=0),
            "sha256":digest_poly(p),
        }
    result["bundle_sha256"]=hashlib.sha256(json.dumps(result["shifts"],sort_keys=True,separators=(",",":" )).encode()).hexdigest()
    return result,deltas


def main() -> int:
    result,_=build_all()
    print(json.dumps(result,sort_keys=True,separators=(",",":")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
