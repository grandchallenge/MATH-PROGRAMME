from __future__ import annotations

import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
RC=HERE/"residual_canonical.py"
spec=importlib.util.spec_from_file_location("t3_009_residual_canonical_for_onebody",RC)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load residual canonicalizer")
rc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

NESTED_PREFIX=("U_k_l_","U_l_k_","ES_k_","ES_l_")


def is_nested(name:str)->bool:
    return name.startswith(NESTED_PREFIX)


def one_body_projection(poly):
    return {m:c for m,c in poly.items() if not any(is_nested(a) for a in m)}


def atom_set(poly):
    return sorted({a for m in poly for a in m})


def profile(poly):
    return {
        "monomials":len(poly),
        "atoms":len(atom_set(poly)),
        "atom_names":atom_set(poly),
        "max_atomic_arity":max((len(m) for m in poly),default=0),
        "sha256":rc.digest_poly(poly),
    }


def scaled(poly,c):
    return rc.p_scale(poly,c)


def delta_combo(name:str,shift):
    if name=="N11":
        return rc.p_add(rc.delta_atom("U_k_l_1_2",shift),rc.delta_atom("U_l_k_1_2",shift))
    if name=="N12k":
        return rc.p_add(scaled(rc.delta_atom("ES_l_1_3",shift),2),scaled(rc.delta_atom("U_k_l_2_2",shift),-1))
    if name=="N12l":
        return rc.p_add(scaled(rc.delta_atom("ES_k_1_3",shift),2),scaled(rc.delta_atom("U_l_k_2_2",shift),-1))
    raise ValueError(name)


def build():
    _,deltas=rc.build_all()
    one={lab:one_body_projection(poly) for lab,poly in deltas.items()}
    transfer={}
    for name in ("N11","N12k","N12l"):
        for orient,shift in (("k",(0,1,0)),("l",(0,0,1))):
            p=delta_combo(name,shift)
            if any(is_nested(a) for m in p for a in m):
                raise AssertionError(f"nested atom survived Abel transfer difference {name}:{orient}")
            transfer[f"Delta_{orient}_{name}"]=p
    union_atoms=sorted(set().union(*(set(atom_set(p)) for p in one.values()),*(set(atom_set(p)) for p in transfer.values())))
    return {
        "schema_version":"1.0.0",
        "operation":"OZ-RT-BZ-T3-009",
        "route":"T3_SEQUENCE_RECURRENCE_EXTRACTION_001",
        "subroute":"QROW_PRODUCT_RULE_REDUCTION_001",
        "object":"ONE_BODY_RESIDUAL_HARMONIC_MODULE",
        "canonical_weight_difference_one_body":{lab:profile(p) for lab,p in one.items()},
        "abel_transfer_differences":{lab:profile(p) for lab,p in transfer.items()},
        "union_one_body_atoms":union_atoms,
        "union_one_body_atom_count":len(union_atoms),
        "nested_atoms_remaining":0,
        "coefficient_layer":"Exact Q-row regularized differentiated fluxes remain external scalar/hypergeometric coefficient functions; this builder canonicalizes only the harmonic/nested algebra and never expands the Q-row certificate into it.",
        "sum_reduction":"sum E_D equals the sum of the canonical one-body projection plus the six Abel-transfer terms -J_orientation(f)(shifted)*Delta_orientation(N), with f=A,Lk,Ll paired to N11,N12k,N12l; all six Delta(N) objects retained here contain no U/ES atom.",
        "residual_sum_zero_proved":False,
        "proof_effect":"NONE",
        "promotion_effect":"NONE",
        "t3_status":"OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
