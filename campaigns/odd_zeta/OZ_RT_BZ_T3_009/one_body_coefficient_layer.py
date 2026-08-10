#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

import residual_canonical as rc
import one_body_structure as obs

HERE = Path(__file__).resolve().parent

NESTED_PREFIX = ("U_k_l_", "U_l_k_", "ES_k_", "ES_l_")
SHIFTS = {
    "n1": (1, 0, 0),
    "n2": (2, 0, 0),
    "n3": (3, 0, 0),
    "k1": (0, 1, 0),
    "l1": (0, 0, 1),
}

# The signs are part of the scalar definitions.  Thus every retained harmonic
# polynomial can be added with coefficient +1 in the sparse layer.
SCALARS = {
    "TN1": "c1(n)*T(n+1,k,l)",
    "TN2": "c2(n)*T(n+2,k,l)",
    "TN3": "c3(n)*T(n+3,k,l)",
    "SK": "-Rk_sym(n,k+1,l)",
    "SL": "-Rl_sym(n,k,l+1)",
    "AK": "-Jk_A(n,k+1,l)",
    "AL": "-Jl_A(n,k,l+1)",
    "LKK": "-Jk_Lk(n,k+1,l)",
    "LKL": "-Jl_Lk(n,k,l+1)",
    "LLK": "-Jk_Ll(n,k+1,l)",
    "LLL": "-Jl_Ll(n,k,l+1)",
}
SCALAR_ORDER = tuple(SCALARS)

DIRECT_SCALAR = {
    "n1": "TN1",
    "n2": "TN2",
    "n3": "TN3",
    "k1": "SK",
    "l1": "SL",
}

TRANSFER_TERMS = (
    ("AK", "N11", "k"),
    ("AL", "N11", "l"),
    ("LKK", "N12k", "k"),
    ("LKL", "N12k", "l"),
    ("LLK", "N12l", "k"),
    ("LLL", "N12l", "l"),
)


def is_nested(name: str) -> bool:
    return name.startswith(NESTED_PREFIX)


def one_body_projection(poly: rc.Poly) -> rc.Poly:
    return {
        mon: coeff
        for mon, coeff in poly.items()
        if not any(is_nested(atom) for atom in mon)
    }


def nested_projection(poly: rc.Poly) -> rc.Poly:
    return {
        mon: coeff
        for mon, coeff in poly.items()
        if any(is_nested(atom) for atom in mon)
    }


def shift_constant_coefficient_poly(poly: rc.Poly, shift: tuple[int, int, int]) -> rc.Poly:
    """Shift a polynomial whose coefficients are constants in Q.

    Lk, Ll, and A=Lk*Ll-C2 have constant coefficients in the protected atom
    algebra.  Restricting this helper to that case avoids silently inventing a
    shift action on the Laurent coefficient ring.
    """
    out: rc.Poly = {}
    for mon, coeff in poly.items():
        if any(sig for sig in coeff):
            # Constant rational coefficients use the empty Laurent signature.
            if set(coeff) != {()}:
                raise AssertionError("nonconstant coefficient passed to protected expression shifter")
        q: rc.Poly = {(): coeff}
        for atom in mon:
            q = rc.p_mul(q, rc.shift_atom(atom, shift))
        out = rc.p_add(out, q)
    return out


def delta_expr(poly: rc.Poly, shift: tuple[int, int, int]) -> rc.Poly:
    return rc.p_add(shift_constant_coefficient_poly(poly, shift), rc.p_scale(poly, -1))


def protected_auxiliary_polynomials() -> dict[str, rc.Poly]:
    lk = rc.p_scale(
        rc.p_add(rc.p_atom("A_k_1"), rc.p_atom("C_1"), rc.p_scale(rc.p_atom("B_k_1"), 2)),
        -1,
    )
    ll = rc.p_scale(
        rc.p_add(rc.p_atom("A_l_1"), rc.p_atom("C_1"), rc.p_scale(rc.p_atom("B_l_1"), 2)),
        -1,
    )
    a = rc.p_add(rc.p_mul(lk, ll), rc.p_scale(rc.p_atom("C_2"), -1))
    n11 = rc.p_add(rc.p_atom("U_k_l_1_2"), rc.p_atom("U_l_k_1_2"))
    n12k = rc.p_add(rc.p_scale(rc.p_atom("ES_l_1_3"), 2), rc.p_scale(rc.p_atom("U_k_l_2_2"), -1))
    n12l = rc.p_add(rc.p_scale(rc.p_atom("ES_k_1_3"), 2), rc.p_scale(rc.p_atom("U_l_k_2_2"), -1))
    return {"Lk": lk, "Ll": ll, "A": a, "N11": n11, "N12k": n12k, "N12l": n12l}


def verify_nested_skeleton(deltas: dict[str, rc.Poly]) -> dict[str, str]:
    aux = protected_auxiliary_polynomials()
    digests: dict[str, str] = {}
    for label, shift in SHIFTS.items():
        predicted = rc.p_add(
            rc.p_mul(delta_expr(aux["A"], shift), aux["N11"]),
            rc.p_mul(delta_expr(aux["Lk"], shift), aux["N12k"]),
            rc.p_mul(delta_expr(aux["Ll"], shift), aux["N12l"]),
        )
        actual = nested_projection(deltas[label])
        if predicted != actual:
            raise AssertionError(f"nested three-skeleton coefficient identity drift: {label}")
        digests[label] = rc.digest_poly(actual)
    return digests


# Sparse layer: harmonic monomial -> external scalar -> Laurent coefficient.
Layer = dict[tuple[str, ...], dict[str, rc.Rat]]


def add_scalar_poly(layer: Layer, scalar: str, poly: rc.Poly) -> None:
    if scalar not in SCALARS:
        raise AssertionError(f"unknown scalar {scalar}")
    for mon, coeff in poly.items():
        by_scalar = layer.setdefault(mon, {})
        merged = rc.r_add(by_scalar.get(scalar, {}), coeff)
        if merged:
            by_scalar[scalar] = merged
        elif scalar in by_scalar:
            del by_scalar[scalar]
        if not by_scalar:
            del layer[mon]


def scalar_projection(layer: Layer, scalar: str) -> rc.Poly:
    return {
        mon: by_scalar[scalar]
        for mon, by_scalar in layer.items()
        if scalar in by_scalar
    }


def layer_json(layer: Layer):
    rows = []
    for mon in sorted(layer):
        terms = []
        for scalar in SCALAR_ORDER:
            coeff = layer[mon].get(scalar)
            if coeff:
                terms.append([scalar, rc.rat_json(coeff)])
        rows.append([list(mon), terms])
    return rows


def layer_digest(layer: Layer) -> str:
    raw = json.dumps(layer_json(layer), separators=(",", ":"), sort_keys=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def atom_set_layer(layer: Layer) -> list[str]:
    return sorted({atom for mon in layer for atom in mon})


def build_layer() -> tuple[Layer, dict]:
    _, deltas = rc.build_all()
    skeleton_digests = verify_nested_skeleton(deltas)

    layer: Layer = {}
    direct_profiles = {}
    for label in ("n1", "n2", "n3", "k1", "l1"):
        poly = one_body_projection(deltas[label])
        add_scalar_poly(layer, DIRECT_SCALAR[label], poly)
        direct_profiles[label] = {
            "monomials": len(poly),
            "atoms": len(rc.atom_set(poly)),
            "max_atomic_arity": max((len(mon) for mon in poly), default=0),
            "sha256": rc.digest_poly(poly),
        }

    transfer_profiles = {}
    for scalar, basis, orient in TRANSFER_TERMS:
        shift = (0, 1, 0) if orient == "k" else (0, 0, 1)
        poly = obs.delta_combo(basis, shift)
        if any(is_nested(atom) for mon in poly for atom in mon):
            raise AssertionError(f"nested atom survived Abel transfer: {basis}/{orient}")
        add_scalar_poly(layer, scalar, poly)
        transfer_profiles[f"{scalar}:{basis}:{orient}"] = {
            "monomials": len(poly),
            "atoms": len(rc.atom_set(poly)),
            "max_atomic_arity": max((len(mon) for mon in poly), default=0),
            "sha256": rc.digest_poly(poly),
        }

    atoms = atom_set_layer(layer)
    if len(atoms) != 22:
        raise AssertionError(f"final one-body atom universe drift: {len(atoms)}")
    if any(is_nested(atom) for atom in atoms):
        raise AssertionError("nested atom survived final one-body layer")

    scalar_profiles = {}
    for scalar in SCALAR_ORDER:
        poly = scalar_projection(layer, scalar)
        scalar_profiles[scalar] = {
            "formula": SCALARS[scalar],
            "monomials": len(poly),
            "atoms": len(rc.atom_set(poly)),
            "max_atomic_arity": max((len(mon) for mon in poly), default=0),
            "sha256": rc.digest_poly(poly),
        }

    result = {
        "schema_version": "1.0.0",
        "operation": "OZ-RT-BZ-T3-009",
        "execution_boundary": "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001",
        "route": "DIRECT_T3_DISCRETE_RESIDUAL_CERT_001",
        "subroute": "STRUCTURED_ONE_BODY_LETTER_SPLIT_HOLONOMIC_001",
        "status": "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_CONSTRUCTED",
        "source_locks": {
            "residual_canonical_result_blob": "3bce6acbc601e2b6ba6f880b8a78854e242e2f88",
            "one_body_structure_result_blob": "9b94915d18016d3d903d04217eadb7b10e69c7dd",
            "nested_derivative_certificate_route_blob": "d0129e6a8245bf4846d18e1e3130fead2b963086",
            "qrow_symmetric_gauge_blob": "90ced05b422ef30186e6ead2abb4d1fd78614197",
        },
        "coefficient_ring": "finite Q-linear Laurent combinations of integer-affine factors, tensored with an 11-element exact regularized Q-row scalar basis",
        "scalar_basis": scalar_profiles,
        "regularized_scalar_definitions": {
            "Fk": "Reg[rho_sym(n,k,l)*T(n,k,l)]",
            "Fl": "Reg[sigma_sym(n,k,l)*T(n,k,l)]",
            "Rk_sym": "Fk",
            "Rl_sym": "Fl",
            "Jk_Lk": "-partial_k(Fk)-Fk*Lk_disc",
            "Jl_Lk": "-partial_k(Fl)-Fl*Lk_disc",
            "Jk_Ll": "-partial_l(Fk)-Fk*Ll_disc",
            "Jl_Ll": "-partial_l(Fl)-Fl*Ll_disc",
            "Jk_A": "partial_k partial_l(Fk)-Fk*A_disc",
            "Jl_A": "partial_k partial_l(Fl)-Fl*A_disc",
        },
        "direct_one_body_profiles": direct_profiles,
        "nested_skeleton_exact_digests": skeleton_digests,
        "abel_transfer_profiles": transfer_profiles,
        "final_layer": {
            "monomials": len(layer),
            "atoms": len(atoms),
            "atom_names": atoms,
            "max_atomic_arity": max((len(mon) for mon in layer), default=0),
            "scalar_basis_size": len(SCALAR_ORDER),
            "sha256": layer_digest(layer),
            "rows": layer_json(layer),
        },
        "sum_identity": {
            "direct_decomposition": "E_D=E_D_one+E[A]*N11+E[Lk]*N12k+E[Ll]*N12l",
            "abel_rule": "sum N*Delta_i(J_i)=-sum J_i(shifted)*Delta_i(N), with the already-proved zero regularized finite-box boundary",
            "result": "sum E_D=sum R_one, where R_one is exactly the retained final_layer",
            "difference_from_direct_cell_residual": "a sum of the three certified regularized divergences Delta_k(Jk_f*N_f)+Delta_l(Jl_f*N_f), f in {A,Lk,Ll}",
        },
        "pole_semantics": "All F/J objects denote the globally regularized products from NESTED_DERIVATIVE_CERTIFICATE_ROUTE. No generic-field T*partial(rho) shell simplification is permitted.",
        "finite_sampling_used_as_sum_proof": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_exact_obligation": "Independently replay the retained coefficient layer against the direct canonical E_D decomposition and the Abel-transfer identity; only then admit the symmetry-reduced shift-channel x harmonic-block certificate calculation.",
    }
    return layer, result


def main() -> int:
    _, result = build_layer()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
