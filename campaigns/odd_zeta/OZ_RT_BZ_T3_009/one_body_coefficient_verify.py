#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import residual_canonical as rc

HERE = Path(__file__).resolve().parent
RESULT = HERE / "ONE_BODY_COEFFICIENT_LAYER.json"
PINV_TAG = 991337
NESTED_PREFIX = ("U_k_l_", "U_l_k_", "ES_k_", "ES_l_")
SCALARS = ("TN1", "TN2", "TN3", "SK", "SL", "AK", "AL", "LKK", "LKL", "LLK", "LLL")
DIRECT = {"n1": "TN1", "n2": "TN2", "n3": "TN3", "k1": "SK", "l1": "SL"}
SHIFTS = {"n1": (1,0,0), "n2": (2,0,0), "n3": (3,0,0), "k1": (0,1,0), "l1": (0,0,1)}
SOURCE_BLOBS = {
    "RESIDUAL_CANONICAL_RESULT.json": "3bce6acbc601e2b6ba6f880b8a78854e242e2f88",
    "ONE_BODY_STRUCTURE_RESULT.json": "9b94915d18016d3d903d04217eadb7b10e69c7dd",
    "NESTED_DERIVATIVE_CERTIFICATE_ROUTE.json": "d0129e6a8245bf4846d18e1e3130fead2b963086",
    "QROW_SYMMETRIC_GAUGE.json": "90ced05b422ef30186e6ead2abb4d1fd78614197",
}
Layer = dict[tuple[str, ...], dict[str, rc.Rat]]


def is_nested(name: str) -> bool:
    return name.startswith(NESTED_PREFIX)


def one_body(poly: rc.Poly) -> rc.Poly:
    return {m:c for m,c in poly.items() if not any(is_nested(a) for a in m)}


def nested(poly: rc.Poly) -> rc.Poly:
    return {m:c for m,c in poly.items() if any(is_nested(a) for a in m)}


def pinv(f: tuple[int,int,int,int], power: int) -> rc.Rat:
    return rc.r_factor((PINV_TAG, *f), -power)


def sum_pinv(forms: list[tuple[int,int,int,int]], power: int) -> rc.Rat:
    return rc.r_add(*(pinv(f, power) for f in forms))


def delta_atom(name: str, shift: tuple[int,int,int]) -> rc.Poly:
    dn, dk, dl = shift
    order = int(name.split("_")[-1])
    if name.startswith("B_k_"):
        if dn:
            return rc.p_scale(rc.p_const(1), sum_pinv([rc.lin_nmink(i) for i in range(1,dn+1)], order))
        if dk:
            return rc.p_scale(rc.p_const(1), rc.r_scale(rc.r_add(pinv(rc.lin_nmink(0),order), rc.inv(rc.lin_k(1),order)), -1))
        return {}
    if name.startswith("B_l_"):
        if dn:
            return rc.p_scale(rc.p_const(1), sum_pinv([rc.lin_nminl(i) for i in range(1,dn+1)], order))
        if dl:
            return rc.p_scale(rc.p_const(1), rc.r_scale(rc.r_add(pinv(rc.lin_nminl(0),order), rc.inv(rc.lin_l(1),order)), -1))
        return {}
    return rc.delta_atom(name, shift)


def shift_atom(name: str, shift: tuple[int,int,int]) -> rc.Poly:
    return rc.p_add(rc.p_atom(name), delta_atom(name, shift))


def delta_target(shift: tuple[int,int,int]) -> rc.Poly:
    shifted: rc.Poly = {}
    for mon, coeff in rc.jet_map.target_polynomial().items():
        q = rc.p_const(coeff)
        for atom in mon:
            q = rc.p_mul(q, shift_atom(atom, shift))
        shifted = rc.p_add(shifted, q)
    return rc.p_add(shifted, rc.p_scale(rc.target_poly(), -1))


def eval_rat(x: rc.Rat, n: int, k: int, l: int) -> Q:
    out = Q(0)
    for sig, coeff in x.items():
        v = coeff
        suppressed = False
        for factor, exponent in sig:
            if len(factor) == 5 and factor[0] == PINV_TAG:
                _, a,b,c,d = factor
                z = a*n+b*k+c*l+d
                if z <= 0:
                    suppressed = True
                    break
                v *= Q(z) ** exponent
            else:
                a,b,c,d = factor
                z = a*n+b*k+c*l+d
                if z == 0 and exponent < 0:
                    raise ZeroDivisionError((factor,exponent,n,k,l))
                v *= Q(z) ** exponent
        if not suppressed:
            out += v
    return out


def eval_poly(poly: rc.Poly, n: int, k: int, l: int) -> Q:
    out = Q(0)
    for mon, coeff in poly.items():
        v = eval_rat(coeff,n,k,l)
        for atom in mon:
            v *= rc.atom_value(atom,n,k,l)
        out += v
    return out


def shell_replay(deltas: dict[str,rc.Poly]) -> dict:
    atoms = sorted({a for mon in rc.jet_map.target_polynomial() for a in mon})
    atom_checks = target_checks = shell_checks = 0
    for n in range(5):
        K=n+3
        for k in range(K+1):
            for l in range(K+1):
                for label,shift in SHIFTS.items():
                    dn,dk,dl=shift
                    for atom in atoms:
                        if eval_poly(delta_atom(atom,shift),n,k,l) != rc.atom_value(atom,n+dn,k+dk,l+dl)-rc.atom_value(atom,n,k,l):
                            raise AssertionError(f"independent shell atom drift {label}:{atom}@{(n,k,l)}")
                        atom_checks += 1
                    if eval_poly(deltas[label],n,k,l) != rc.jet_map.direct_target(n+dn,k+dk,l+dl)-rc.jet_map.direct_target(n,k,l):
                        raise AssertionError(f"independent shell target drift {label}@{(n,k,l)}")
                    target_checks += 1
                    if k>=n or l>=n:
                        shell_checks += 1
    return {"atom_checks":atom_checks,"target_checks":target_checks,"shell_checks":shell_checks}


def shift_const(poly: rc.Poly, shift: tuple[int,int,int]) -> rc.Poly:
    out: rc.Poly={}
    for mon,coeff in poly.items():
        if set(coeff)!={()}:
            raise AssertionError("nonconstant auxiliary coefficient")
        q: rc.Poly={():coeff}
        for atom in mon:
            q=rc.p_mul(q,shift_atom(atom,shift))
        out=rc.p_add(out,q)
    return out


def delta_expr(poly: rc.Poly, shift: tuple[int,int,int]) -> rc.Poly:
    return rc.p_add(shift_const(poly,shift),rc.p_scale(poly,-1))


def auxiliaries() -> dict[str,rc.Poly]:
    lk=rc.p_scale(rc.p_add(rc.p_atom("A_k_1"),rc.p_atom("C_1"),rc.p_scale(rc.p_atom("B_k_1"),2)),-1)
    ll=rc.p_scale(rc.p_add(rc.p_atom("A_l_1"),rc.p_atom("C_1"),rc.p_scale(rc.p_atom("B_l_1"),2)),-1)
    aa=rc.p_add(rc.p_mul(lk,ll),rc.p_scale(rc.p_atom("C_2"),-1))
    n11=rc.p_add(rc.p_atom("U_k_l_1_2"),rc.p_atom("U_l_k_1_2"))
    n12k=rc.p_add(rc.p_scale(rc.p_atom("ES_l_1_3"),2),rc.p_scale(rc.p_atom("U_k_l_2_2"),-1))
    n12l=rc.p_add(rc.p_scale(rc.p_atom("ES_k_1_3"),2),rc.p_scale(rc.p_atom("U_l_k_2_2"),-1))
    return {"Lk":lk,"Ll":ll,"A":aa,"N11":n11,"N12k":n12k,"N12l":n12l}


def explicit_transfers() -> dict[str,rc.Poly]:
    return {
        "AK":rc.p_add(rc.delta_atom("U_k_l_1_2",(0,1,0)),rc.delta_atom("U_l_k_1_2",(0,1,0))),
        "AL":rc.p_add(rc.delta_atom("U_k_l_1_2",(0,0,1)),rc.delta_atom("U_l_k_1_2",(0,0,1))),
        "LKK":rc.p_add(rc.p_scale(rc.delta_atom("ES_l_1_3",(0,1,0)),2),rc.p_scale(rc.delta_atom("U_k_l_2_2",(0,1,0)),-1)),
        "LKL":rc.p_add(rc.p_scale(rc.delta_atom("ES_l_1_3",(0,0,1)),2),rc.p_scale(rc.delta_atom("U_k_l_2_2",(0,0,1)),-1)),
        "LLK":rc.p_add(rc.p_scale(rc.delta_atom("ES_k_1_3",(0,1,0)),2),rc.p_scale(rc.delta_atom("U_l_k_2_2",(0,1,0)),-1)),
        "LLL":rc.p_add(rc.p_scale(rc.delta_atom("ES_k_1_3",(0,0,1)),2),rc.p_scale(rc.delta_atom("U_l_k_2_2",(0,0,1)),-1)),
    }


def add(layer: Layer, scalar: str, poly: rc.Poly) -> None:
    for mon,coeff in poly.items():
        d=layer.setdefault(mon,{})
        z=rc.r_add(d.get(scalar,{}),coeff)
        if z: d[scalar]=z
        elif scalar in d: del d[scalar]
        if not d: del layer[mon]


def reconstruct() -> tuple[Layer,dict[str,str],dict]:
    deltas={label:delta_target(shift) for label,shift in SHIFTS.items()}
    replay=shell_replay(deltas)
    a=auxiliaries()
    digests={}
    for label,shift in SHIFTS.items():
        predicted=rc.p_add(
            rc.p_mul(delta_expr(a["A"],shift),a["N11"]),
            rc.p_mul(delta_expr(a["Lk"],shift),a["N12k"]),
            rc.p_mul(delta_expr(a["Ll"],shift),a["N12l"]),
        )
        actual=nested(deltas[label])
        if predicted!=actual:
            raise AssertionError(f"independent nested skeleton drift: {label}")
        digests[label]=rc.digest_poly(actual)
    layer:Layer={}
    for label,scalar in DIRECT.items(): add(layer,scalar,one_body(deltas[label]))
    for scalar,poly in explicit_transfers().items():
        if any(is_nested(a) for mon in poly for a in mon): raise AssertionError(f"nested transfer residue {scalar}")
        add(layer,scalar,poly)
    return layer,digests,replay


def canonical_rows(layer: Layer):
    rows=[]
    for mon in sorted(layer):
        terms=[]
        for scalar in SCALARS:
            coeff=layer[mon].get(scalar)
            if coeff: terms.append([scalar,rc.rat_json(coeff)])
        rows.append([list(mon),terms])
    return rows


def digest(layer: Layer) -> str:
    return hashlib.sha256(json.dumps(canonical_rows(layer),separators=(",",":"),sort_keys=False).encode()).hexdigest()


def factor_profile(layer:Layer)->dict:
    ordinary=set(); protected=set()
    for terms in layer.values():
        for rat in terms.values():
            for sig in rat:
                for factor,_ in sig:
                    if len(factor)==5 and factor[0]==PINV_TAG: protected.add(factor[1:])
                    else: ordinary.add(factor)
    return {
        "ordinary_affine_factors":[list(x) for x in sorted(ordinary)],
        "protected_positive_reciprocal_factors":[list(x) for x in sorted(protected)],
        "protected_factor_count":len(protected),
    }


def git_blob_sha1(path:Path)->str:
    raw=path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()


def nested_value(which:str,k:int,l:int)->Q:
    p=rc.parent
    if which=="N11": return p.nested_atom_value("U_k_l_1_2",0,k,l)+p.nested_atom_value("U_l_k_1_2",0,k,l)
    if which=="N12k": return 2*p.nested_atom_value("ES_l_1_3",0,k,l)-p.nested_atom_value("U_k_l_2_2",0,k,l)
    if which=="N12l": return 2*p.nested_atom_value("ES_k_1_3",0,k,l)-p.nested_atom_value("U_l_k_2_2",0,k,l)
    raise ValueError(which)


def verify_abel()->int:
    checks=0
    for K in (3,4,5):
        def jk(k,l): return Q(k*(K+1-k)*(l+1),7)
        def jl(k,l): return Q(l*(K+1-l)*(k+2),11)
        for which in ("N11","N12k","N12l"):
            lhs=rhs=Q(0)
            for k in range(K+1):
                for l in range(K+1):
                    nv=nested_value(which,k,l)
                    lhs+=nv*((jk(k+1,l)-jk(k,l))+(jl(k,l+1)-jl(k,l)))
                    rhs-=jk(k+1,l)*(nested_value(which,k+1,l)-nv)
                    rhs-=jl(k,l+1)*(nested_value(which,k,l+1)-nv)
            if lhs!=rhs: raise AssertionError(f"Abel sign/shift drift K={K} {which}")
            checks+=1
    return checks


def verify()->dict:
    retained=json.loads(RESULT.read_text(encoding="utf-8"))
    if retained["execution_boundary"]!="FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001": raise AssertionError("boundary drift")
    if retained["proof_effect"]!="NONE" or retained["promotion_effect"]!="NONE" or retained["residual_sum_zero_proved"]: raise AssertionError("claim inflation")
    lock_map={
        "RESIDUAL_CANONICAL_RESULT.json":retained["source_locks"]["residual_canonical_result_blob"],
        "ONE_BODY_STRUCTURE_RESULT.json":retained["source_locks"]["one_body_structure_result_blob"],
        "NESTED_DERIVATIVE_CERTIFICATE_ROUTE.json":retained["source_locks"]["nested_derivative_certificate_route_blob"],
        "QROW_SYMMETRIC_GAUGE.json":retained["source_locks"]["qrow_symmetric_gauge_blob"],
    }
    if lock_map!=SOURCE_BLOBS: raise AssertionError("source lock declaration drift")
    for name,expected in SOURCE_BLOBS.items():
        if git_blob_sha1(HERE/name)!=expected: raise AssertionError(f"source blob drift: {name}")
    layer,skeleton,replay=reconstruct()
    atoms=sorted({a for mon in layer for a in mon})
    final=retained["final_layer"]
    if (len(layer),len(atoms),max(map(len,layer)),len(SCALARS),digest(layer))!=(122,22,3,11,"90d067ae59790fab8648d006635c14950359b66eb8b57361e61d5b47b2b3af40"):
        raise AssertionError("independent canonical coefficient profile drift")
    if final["monomials"]!=len(layer) or final["atom_names"]!=atoms or final["max_atomic_arity"]!=3 or final["scalar_basis_size"]!=11 or final["sha256"]!=digest(layer):
        raise AssertionError("retained final-layer binding drift")
    if retained["nested_skeleton_exact_digests"]!=skeleton: raise AssertionError("nested skeleton digest drift")
    if retained["factor_profile"]!=factor_profile(layer): raise AssertionError("factor profile drift")
    if replay!={"atom_checks":38950,"target_checks":950,"shell_checks":800}: raise AssertionError("shell replay count drift")
    if retained["protected_harmonic_shift_lemma"]["finite_sampling_used_as_global_proof"]: raise AssertionError("finite-to-global inflation")
    abel=verify_abel()
    return {
        "status":"INDEPENDENT_FULL_POLE_FREE_ONE_BODY_COEFFICIENT_REPLAY_COMPLETE",
        "monomials":122,"atoms":22,"max_atomic_arity":3,"scalar_basis_size":11,
        "sha256":digest(layer),"protected_factor_count":8,
        "exact_atom_shift_checks":replay["atom_checks"],"exact_full_target_shift_checks":replay["target_checks"],
        "checks_touching_moving_shell":replay["shell_checks"],"nested_skeleton_channels_verified":5,
        "abel_exact_checks":abel,"full_rows_reconstructed_independently":True,
        "finite_sampling_used_as_sum_proof":False,"proof_effect":"NONE","promotion_effect":"NONE",
        "t3_status":"OPEN_WITH_CHARACTERIZED_BLOCKER"
    }


def main()->int:
    print(json.dumps(verify(),sort_keys=True,separators=(",",":")))
    return 0

if __name__=="__main__": raise SystemExit(main())
