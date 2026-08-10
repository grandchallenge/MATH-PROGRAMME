#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import residual_canonical as rc

HERE = Path(__file__).resolve().parent
RESULT = HERE / "ONE_BODY_COEFFICIENT_LAYER.json"

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


def add(layer: Layer, scalar: str, poly: rc.Poly) -> None:
    for mon, coeff in poly.items():
        d = layer.setdefault(mon, {})
        z = rc.r_add(d.get(scalar, {}), coeff)
        if z:
            d[scalar] = z
        elif scalar in d:
            del d[scalar]
        if not d:
            del layer[mon]


def explicit_transfer_polynomials() -> dict[str, rc.Poly]:
    # This deliberately does not import one_body_structure.py.  It rebuilds the
    # six finite differences directly from the protected atom shift rules.
    return {
        "AK": rc.p_add(rc.delta_atom("U_k_l_1_2", (0,1,0)), rc.delta_atom("U_l_k_1_2", (0,1,0))),
        "AL": rc.p_add(rc.delta_atom("U_k_l_1_2", (0,0,1)), rc.delta_atom("U_l_k_1_2", (0,0,1))),
        "LKK": rc.p_add(rc.p_scale(rc.delta_atom("ES_l_1_3", (0,1,0)), 2), rc.p_scale(rc.delta_atom("U_k_l_2_2", (0,1,0)), -1)),
        "LKL": rc.p_add(rc.p_scale(rc.delta_atom("ES_l_1_3", (0,0,1)), 2), rc.p_scale(rc.delta_atom("U_k_l_2_2", (0,0,1)), -1)),
        "LLK": rc.p_add(rc.p_scale(rc.delta_atom("ES_k_1_3", (0,1,0)), 2), rc.p_scale(rc.delta_atom("U_l_k_2_2", (0,1,0)), -1)),
        "LLL": rc.p_add(rc.p_scale(rc.delta_atom("ES_k_1_3", (0,0,1)), 2), rc.p_scale(rc.delta_atom("U_l_k_2_2", (0,0,1)), -1)),
    }


def shift_const(poly: rc.Poly, shift: tuple[int,int,int]) -> rc.Poly:
    out: rc.Poly = {}
    for mon, coeff in poly.items():
        if set(coeff) != {()}:
            raise AssertionError("independent skeleton shifter received nonconstant coefficient")
        q: rc.Poly = {(): coeff}
        for atom in mon:
            q = rc.p_mul(q, rc.shift_atom(atom, shift))
        out = rc.p_add(out, q)
    return out


def delta(poly: rc.Poly, shift: tuple[int,int,int]) -> rc.Poly:
    return rc.p_add(shift_const(poly, shift), rc.p_scale(poly, -1))


def aux() -> dict[str, rc.Poly]:
    lk = rc.p_scale(rc.p_add(rc.p_atom("A_k_1"), rc.p_atom("C_1"), rc.p_scale(rc.p_atom("B_k_1"),2)), -1)
    ll = rc.p_scale(rc.p_add(rc.p_atom("A_l_1"), rc.p_atom("C_1"), rc.p_scale(rc.p_atom("B_l_1"),2)), -1)
    aa = rc.p_add(rc.p_mul(lk,ll), rc.p_scale(rc.p_atom("C_2"),-1))
    n11 = rc.p_add(rc.p_atom("U_k_l_1_2"),rc.p_atom("U_l_k_1_2"))
    n12k = rc.p_add(rc.p_scale(rc.p_atom("ES_l_1_3"),2),rc.p_scale(rc.p_atom("U_k_l_2_2"),-1))
    n12l = rc.p_add(rc.p_scale(rc.p_atom("ES_k_1_3"),2),rc.p_scale(rc.p_atom("U_l_k_2_2"),-1))
    return {"Lk":lk,"Ll":ll,"A":aa,"N11":n11,"N12k":n12k,"N12l":n12l}


def independent_expected_layer() -> tuple[Layer, dict[str,str]]:
    _, deltas = rc.build_all()
    a = aux()
    skeleton_digests = {}
    for label, sh in SHIFTS.items():
        predicted = rc.p_add(
            rc.p_mul(delta(a["A"],sh),a["N11"]),
            rc.p_mul(delta(a["Lk"],sh),a["N12k"]),
            rc.p_mul(delta(a["Ll"],sh),a["N12l"]),
        )
        actual = nested(deltas[label])
        if predicted != actual:
            raise AssertionError(f"independent nested skeleton replay failed: {label}")
        skeleton_digests[label] = rc.digest_poly(actual)

    layer: Layer = {}
    for label, scalar in DIRECT.items():
        add(layer, scalar, one_body(deltas[label]))
    for scalar, poly in explicit_transfer_polynomials().items():
        if any(is_nested(a) for m in poly for a in m):
            raise AssertionError(f"nested transfer residue in {scalar}")
        add(layer, scalar, poly)
    return layer, skeleton_digests


def decode_rat(rows) -> rc.Rat:
    out: rc.Rat = {}
    for num, den, sig_rows in rows:
        sig = tuple((tuple(f), int(exp)) for f, exp in sig_rows)
        out[sig] = Q(int(num), int(den))
    return out


def decode_layer(rows) -> Layer:
    out: Layer = {}
    for mon_rows, terms in rows:
        mon = tuple(mon_rows)
        by_scalar = {}
        for scalar, rat_rows in terms:
            if scalar not in SCALARS:
                raise AssertionError(f"unknown retained scalar {scalar}")
            by_scalar[scalar] = decode_rat(rat_rows)
        if not by_scalar:
            raise AssertionError("empty retained coefficient row")
        out[mon] = by_scalar
    return out


def git_blob_sha1(path: Path) -> str:
    raw = path.read_bytes()
    prefix = f"blob {len(raw)}\0".encode()
    return hashlib.sha1(prefix + raw).hexdigest()


def nested_value(which: str, k: int, l: int) -> Q:
    p = rc.parent
    if which == "N11":
        return p.nested_atom_value("U_k_l_1_2", 0, k, l) + p.nested_atom_value("U_l_k_1_2", 0, k, l)
    if which == "N12k":
        return 2*p.nested_atom_value("ES_l_1_3", 0, k, l) - p.nested_atom_value("U_k_l_2_2", 0, k, l)
    if which == "N12l":
        return 2*p.nested_atom_value("ES_k_1_3", 0, k, l) - p.nested_atom_value("U_l_k_2_2", 0, k, l)
    raise ValueError(which)


def verify_abel_sign_and_shift() -> int:
    checks = 0
    for K in (3,4,5):
        def jk(k,l): return Q(k*(K+1-k)*(l+1), 7)
        def jl(k,l): return Q(l*(K+1-l)*(k+2), 11)
        for which in ("N11","N12k","N12l"):
            lhs = Q(0)
            rhs = Q(0)
            for k in range(K+1):
                for l in range(K+1):
                    nv = nested_value(which,k,l)
                    lhs += nv*((jk(k+1,l)-jk(k,l))+(jl(k,l+1)-jl(k,l)))
                    rhs -= jk(k+1,l)*(nested_value(which,k+1,l)-nv)
                    rhs -= jl(k,l+1)*(nested_value(which,k,l+1)-nv)
            if lhs != rhs:
                raise AssertionError(f"Abel sign/shift convention failed: K={K} {which}")
            checks += 1
    return checks


def verify() -> dict:
    retained = json.loads(RESULT.read_text(encoding="utf-8"))
    if retained["execution_boundary"] != "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001":
        raise AssertionError("execution boundary drift")
    if retained["proof_effect"] != "NONE" or retained["promotion_effect"] != "NONE" or retained["residual_sum_zero_proved"]:
        raise AssertionError("claim inflation")

    lock_map = {
        "RESIDUAL_CANONICAL_RESULT.json": retained["source_locks"]["residual_canonical_result_blob"],
        "ONE_BODY_STRUCTURE_RESULT.json": retained["source_locks"]["one_body_structure_result_blob"],
        "NESTED_DERIVATIVE_CERTIFICATE_ROUTE.json": retained["source_locks"]["nested_derivative_certificate_route_blob"],
        "QROW_SYMMETRIC_GAUGE.json": retained["source_locks"]["qrow_symmetric_gauge_blob"],
    }
    if lock_map != SOURCE_BLOBS:
        raise AssertionError("source lock declaration drift")
    for name, expected in SOURCE_BLOBS.items():
        got = git_blob_sha1(HERE/name)
        if got != expected:
            raise AssertionError(f"source blob drift {name}: {got}")

    expected, skeleton = independent_expected_layer()
    got = decode_layer(retained["final_layer"]["rows"])
    if got != expected:
        raise AssertionError("retained one-body coefficient layer differs from independent reconstruction")
    if retained["nested_skeleton_exact_digests"] != skeleton:
        raise AssertionError("nested skeleton digest drift")

    atoms = sorted({a for mon in got for a in mon})
    if len(atoms) != 22 or any(is_nested(a) for a in atoms):
        raise AssertionError("final atom universe is not the exact 22-atom one-body module")
    if retained["final_layer"]["monomials"] != len(got):
        raise AssertionError("retained monomial count drift")

    abel_checks = verify_abel_sign_and_shift()
    return {
        "status": "INDEPENDENT_FULL_POLE_FREE_ONE_BODY_COEFFICIENT_REPLAY_COMPLETE",
        "monomials": len(got),
        "atoms": len(atoms),
        "scalar_basis_size": len(SCALARS),
        "nested_skeleton_channels_verified": len(skeleton),
        "abel_exact_checks": abel_checks,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
