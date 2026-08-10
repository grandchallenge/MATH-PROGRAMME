#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q

import residual_canonical as rc
import one_body_structure as obs

NESTED_PREFIX = ("U_k_l_", "U_l_k_", "ES_k_", "ES_l_")
PINV_TAG = 991337
SHIFTS = {
    "n1": (1, 0, 0),
    "n2": (2, 0, 0),
    "n3": (3, 0, 0),
    "k1": (0, 1, 0),
    "l1": (0, 0, 1),
}

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
DIRECT_SCALAR = {"n1": "TN1", "n2": "TN2", "n3": "TN3", "k1": "SK", "l1": "SL"}
TRANSFER_TERMS = (
    ("AK", "N11", "k"), ("AL", "N11", "l"),
    ("LKK", "N12k", "k"), ("LKL", "N12k", "l"),
    ("LLK", "N12l", "k"), ("LLL", "N12l", "l"),
)


def is_nested(name: str) -> bool:
    return name.startswith(NESTED_PREFIX)


def one_body_projection(poly: rc.Poly) -> rc.Poly:
    return {mon: coeff for mon, coeff in poly.items() if not any(is_nested(a) for a in mon)}


def nested_projection(poly: rc.Poly) -> rc.Poly:
    return {mon: coeff for mon, coeff in poly.items() if any(is_nested(a) for a in mon)}


def pinv_factor(f: tuple[int, int, int, int], power: int = 1) -> rc.Rat:
    """Protected positive reciprocal: x^-power for x>0, and 0 for x<=0.

    The tagged factor is intentionally distinct from an ordinary Laurent
    factor.  It implements exactly the Programme convention H_m^(r)=0 for
    m<=0 at moving-support shells.
    """
    tagged = (PINV_TAG, *f)
    return rc.r_factor(tagged, -power)


def sum_pinv(forms: list[tuple[int, int, int, int]], power: int) -> rc.Rat:
    return rc.r_add(*(pinv_factor(f, power) for f in forms))


def delta_atom_polefree(name: str, shift: tuple[int, int, int]) -> rc.Poly:
    dn, dk, dl = shift
    r = int(name.split("_")[-1])
    if name.startswith("B_k_"):
        if dn:
            return rc.p_scale(rc.p_const(1), sum_pinv([rc.lin_nmink(i) for i in range(1, dn + 1)], r))
        if dk:
            return rc.p_scale(
                rc.p_const(1),
                rc.r_scale(rc.r_add(pinv_factor(rc.lin_nmink(0), r), rc.inv(rc.lin_k(1), r)), -1),
            )
        return {}
    if name.startswith("B_l_"):
        if dn:
            return rc.p_scale(rc.p_const(1), sum_pinv([rc.lin_nminl(i) for i in range(1, dn + 1)], r))
        if dl:
            return rc.p_scale(
                rc.p_const(1),
                rc.r_scale(rc.r_add(pinv_factor(rc.lin_nminl(0), r), rc.inv(rc.lin_l(1), r)), -1),
            )
        return {}
    return rc.delta_atom(name, shift)


def shift_atom_polefree(name: str, shift: tuple[int, int, int]) -> rc.Poly:
    return rc.p_add(rc.p_atom(name), delta_atom_polefree(name, shift))


def shifted_target_polefree(shift: tuple[int, int, int]) -> rc.Poly:
    out: rc.Poly = {}
    for mon, coeff in rc.jet_map.target_polynomial().items():
        q = rc.p_const(coeff)
        for name in mon:
            q = rc.p_mul(q, shift_atom_polefree(name, shift))
        out = rc.p_add(out, q)
    return out


def delta_target_polefree(shift: tuple[int, int, int]) -> rc.Poly:
    return rc.p_add(shifted_target_polefree(shift), rc.p_scale(rc.target_poly(), -1))


def rat_eval_polefree(x: rc.Rat, n: int, k: int, l: int) -> Q:
    total = Q(0)
    for sig, coeff in x.items():
        value = coeff
        zero = False
        for factor, exponent in sig:
            if len(factor) == 5 and factor[0] == PINV_TAG:
                _, a, b, c, d = factor
                z = a*n + b*k + c*l + d
                if z <= 0:
                    zero = True
                    break
                value *= Q(z) ** exponent
            else:
                a, b, c, d = factor
                z = a*n + b*k + c*l + d
                if z == 0 and exponent < 0:
                    raise ZeroDivisionError((factor, exponent, n, k, l))
                value *= Q(z) ** exponent
        if not zero:
            total += value
    return total


def eval_poly_polefree(poly: rc.Poly, n: int, k: int, l: int) -> Q:
    total = Q(0)
    for mon, coeff in poly.items():
        value = rat_eval_polefree(coeff, n, k, l)
        for atom in mon:
            value *= rc.atom_value(atom, n, k, l)
        total += value
    return total


def build_polefree_deltas() -> dict[str, rc.Poly]:
    return {label: delta_target_polefree(shift) for label, shift in SHIFTS.items()}


def verify_protected_shift_lemma(deltas: dict[str, rc.Poly]) -> dict:
    """Adversarial replay across every moving shell for small n.

    The global justification is the finite-sum identity
      H(m+j,r)-H(m,r)=sum_{s=1}^j pinv_r(m+s)
      H(m-1,r)-H(m,r)=-pinv_r(m),
    where H(m,r)=0 for m<=0 and pinv_r(x)=x^-r for x>0 else 0.
    The exhaustive shell probes below guard the implementation of that lemma.
    """
    protected_atoms = sorted({a for mon in rc.jet_map.target_polynomial() for a in mon})
    atom_checks = 0
    target_checks = 0
    shell_checks = 0
    for n in range(5):
        K = n + 3
        for k in range(K + 1):
            for l in range(K + 1):
                for label, shift in SHIFTS.items():
                    dn, dk, dl = shift
                    for name in protected_atoms:
                        got = eval_poly_polefree(delta_atom_polefree(name, shift), n, k, l)
                        want = rc.atom_value(name, n+dn, k+dk, l+dl) - rc.atom_value(name, n, k, l)
                        if got != want:
                            raise AssertionError(f"pole-free atom shift drift {label}:{name}@{(n,k,l)}")
                        atom_checks += 1
                    got = eval_poly_polefree(deltas[label], n, k, l)
                    want = rc.jet_map.direct_target(n+dn, k+dk, l+dl) - rc.jet_map.direct_target(n, k, l)
                    if got != want:
                        raise AssertionError(f"pole-free D shift drift {label}@{(n,k,l)}")
                    target_checks += 1
                    if k >= n or l >= n:
                        shell_checks += 1
    return {
        "global_lemma": "For H(m,r)=0 at m<=0, H(m+j,r)-H(m,r)=sum_{s=1}^j pinv_r(m+s) and H(m-1,r)-H(m,r)=-pinv_r(m).",
        "pinv_definition": "pinv_r(x)=x^(-r) for integer x>0; 0 for integer x<=0",
        "only_modified_letter_families": ["B_k_r", "B_l_r"],
        "exact_atom_shift_checks": atom_checks,
        "exact_full_target_shift_checks": target_checks,
        "checks_touching_moving_shell": shell_checks,
        "finite_sampling_used_as_global_proof": False,
    }


def shift_constant_poly_polefree(poly: rc.Poly, shift: tuple[int, int, int]) -> rc.Poly:
    out: rc.Poly = {}
    for mon, coeff in poly.items():
        if set(coeff) != {()}:
            raise AssertionError("nonconstant coefficient passed to protected expression shifter")
        q: rc.Poly = {(): coeff}
        for atom in mon:
            q = rc.p_mul(q, shift_atom_polefree(atom, shift))
        out = rc.p_add(out, q)
    return out


def delta_expr_polefree(poly: rc.Poly, shift: tuple[int, int, int]) -> rc.Poly:
    return rc.p_add(shift_constant_poly_polefree(poly, shift), rc.p_scale(poly, -1))


def protected_auxiliary_polynomials() -> dict[str, rc.Poly]:
    lk = rc.p_scale(rc.p_add(rc.p_atom("A_k_1"), rc.p_atom("C_1"), rc.p_scale(rc.p_atom("B_k_1"), 2)), -1)
    ll = rc.p_scale(rc.p_add(rc.p_atom("A_l_1"), rc.p_atom("C_1"), rc.p_scale(rc.p_atom("B_l_1"), 2)), -1)
    aa = rc.p_add(rc.p_mul(lk, ll), rc.p_scale(rc.p_atom("C_2"), -1))
    n11 = rc.p_add(rc.p_atom("U_k_l_1_2"), rc.p_atom("U_l_k_1_2"))
    n12k = rc.p_add(rc.p_scale(rc.p_atom("ES_l_1_3"), 2), rc.p_scale(rc.p_atom("U_k_l_2_2"), -1))
    n12l = rc.p_add(rc.p_scale(rc.p_atom("ES_k_1_3"), 2), rc.p_scale(rc.p_atom("U_l_k_2_2"), -1))
    return {"Lk": lk, "Ll": ll, "A": aa, "N11": n11, "N12k": n12k, "N12l": n12l}


def verify_nested_skeleton(deltas: dict[str, rc.Poly]) -> dict[str, str]:
    aux = protected_auxiliary_polynomials()
    digests: dict[str, str] = {}
    for label, shift in SHIFTS.items():
        predicted = rc.p_add(
            rc.p_mul(delta_expr_polefree(aux["A"], shift), aux["N11"]),
            rc.p_mul(delta_expr_polefree(aux["Lk"], shift), aux["N12k"]),
            rc.p_mul(delta_expr_polefree(aux["Ll"], shift), aux["N12l"]),
        )
        actual = nested_projection(deltas[label])
        if predicted != actual:
            raise AssertionError(f"pole-free nested three-skeleton drift: {label}")
        digests[label] = rc.digest_poly(actual)
    return digests


Layer = dict[tuple[str, ...], dict[str, rc.Rat]]


def add_scalar_poly(layer: Layer, scalar: str, poly: rc.Poly) -> None:
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
    return {mon: terms[scalar] for mon, terms in layer.items() if scalar in terms}


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


def factor_profile(layer: Layer) -> dict:
    ordinary = set()
    protected = set()
    for by_scalar in layer.values():
        for rat in by_scalar.values():
            for sig in rat:
                for factor, _ in sig:
                    if len(factor) == 5 and factor[0] == PINV_TAG:
                        protected.add(factor[1:])
                    else:
                        ordinary.add(factor)
    return {
        "ordinary_affine_factors": [list(x) for x in sorted(ordinary)],
        "protected_positive_reciprocal_factors": [list(x) for x in sorted(protected)],
        "protected_factor_count": len(protected),
    }


def build_layer() -> tuple[Layer, dict]:
    deltas = build_polefree_deltas()
    shell_replay = verify_protected_shift_lemma(deltas)
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
        if any(is_nested(a) for mon in poly for a in mon):
            raise AssertionError(f"nested atom survived Abel transfer: {basis}/{orient}")
        add_scalar_poly(layer, scalar, poly)
        transfer_profiles[f"{scalar}:{basis}:{orient}"] = {
            "monomials": len(poly),
            "atoms": len(rc.atom_set(poly)),
            "max_atomic_arity": max((len(mon) for mon in poly), default=0),
            "sha256": rc.digest_poly(poly),
        }

    atoms = atom_set_layer(layer)
    if len(atoms) != 22 or any(is_nested(a) for a in atoms):
        raise AssertionError("final pole-free layer is not the exact 22-atom one-body module")

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
        "schema_version": "1.1.0",
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
        "coefficient_ring": "finite Q-linear combinations of ordinary affine Laurent factors and protected positive reciprocals, tensored with an 11-element exact regularized Q-row scalar basis",
        "protected_harmonic_shift_lemma": shell_replay,
        "factor_profile": factor_profile(layer),
        "scalar_basis": scalar_profiles,
        "regularized_scalar_definitions": {
            "Fk": "Reg[rho_sym(n,k,l)*T(n,k,l)]",
            "Fl": "Reg[sigma_sym(n,k,l)*T(n,k,l)]",
            "Rk_sym": "Fk", "Rl_sym": "Fl",
            "Jk_Lk": "-partial_k(Fk)-Fk*Lk_disc", "Jl_Lk": "-partial_k(Fl)-Fl*Lk_disc",
            "Jk_Ll": "-partial_l(Fk)-Fk*Ll_disc", "Jl_Ll": "-partial_l(Fl)-Fl*Ll_disc",
            "Jk_A": "partial_k partial_l(Fk)-Fk*A_disc", "Jl_A": "partial_k partial_l(Fl)-Fl*A_disc",
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
            "result": "sum E_D=sum R_one, where R_one is exactly the final_layer",
            "difference_from_direct_cell_residual": "the sum of three already-certified regularized divergences Delta_k(Jk_f*N_f)+Delta_l(Jl_f*N_f), f in {A,Lk,Ll}",
        },
        "pole_semantics": "Q-row F/J scalars are regularized before lattice specialization; B_k/B_l harmonic shifts use protected positive reciprocals, so no coefficient evaluates infinity on the common n+3 finite box.",
        "finite_sampling_used_as_sum_proof": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE", "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "next_exact_obligation": "Independently reconstruct and replay this pole-free coefficient layer; only after exact agreement admit the symmetry-reduced shift-channel x harmonic-block certificate calculation.",
    }
    return layer, result


def main() -> int:
    _, result = build_layer()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
