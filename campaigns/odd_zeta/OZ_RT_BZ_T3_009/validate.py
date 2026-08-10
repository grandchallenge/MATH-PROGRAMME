#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = HERE / "RECURRENCE_LOCK.json"
BASELINE = HERE / "BASELINE_RESULT.json"
SEARCH = HERE / "SEARCH_RESULT.json"
QROW = HERE / "QROW_PRODUCT_RULE.json"
QROW_REPLAY = HERE / "QROW_REPLAY_RESULT.json"
QROW_SYM = HERE / "QROW_SYMMETRIC_GAUGE.json"
REDUCED = HERE / "REDUCED_WEIGHT5_RESIDUAL.json"
CANON = HERE / "RESIDUAL_CANONICAL_RESULT.json"
NESTED = HERE / "NESTED_SKELETON_REDUCTION.json"
DERIV = HERE / "NESTED_DERIVATIVE_CERTIFICATE_ROUTE.json"

EXPECTED_A0 = "41218*n^3+198849*n^2+320790*n+173057"
EXPECTED_C3 = "2*(n+3)^5*(2*n+5)*a0(n)"
EXPECTED_RANKS = [(198,199),(792,793),(1980,1981)]
EXPECTED_QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
EXPECTED_SOURCE_COMMITS = [
    "968477ed7e406df6542f8da6fbe1cd6ca7273c47",
    "790685b7ee4f642a8a88a1bd120636d1b8b39ea8",
]
EXPECTED_CANONICAL = {
    "n1": (102,27,3,"ad46afea7d769dcba9d9c8a7b7842bcf72adfa1df0ae05f0734ec25432772655"),
    "n2": (102,27,3,"9c7a4849b95b1ab33670bbc8c2eb218df883cbf19add702f9228b4503b6b2b0e"),
    "n3": (102,27,3,"1e6f8e8ce6cf37b71dd741299c2ce5d1927225c5f08927b66c832a1687814a69"),
    "k1": (134,28,3,"ba7fa0176dc782b6c0747a71a9a0e13c3c5cf3d0c6077efe6f99c2a461c34780"),
    "l1": (134,28,3,"4fd7277655900f62a9f3676fd1d54614205cf8142cf26c04a4ef74eb8dfdc4c6"),
}
EXPECTED_CANON_BUNDLE = "a8b2bc4f905f58d03f0151e19e28e4ff0c1e217fbeb5721d38fe09bcd697b0e1"
EXPECTED_NESTED_ELIMINATED = [
    "U_k_l_1_4","U_l_k_1_4","U_k_l_2_3","U_l_k_2_3",
    "ES_k_1_4","ES_l_1_4","ES_k_2_3","ES_l_2_3",
]
EXPECTED_REDUCED_TERMINAL = "QROW_REVERIFIED_DIRECT_ED_CANONICALIZED_NESTED_GLOBALLY_REDUCED_ONE_BODY_RESIDUAL_NEXT"


def validate() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    result = json.loads(BASELINE.read_text(encoding="utf-8"))
    search = json.loads(SEARCH.read_text(encoding="utf-8"))
    qrow = json.loads(QROW.read_text(encoding="utf-8"))
    replay = json.loads(QROW_REPLAY.read_text(encoding="utf-8"))
    gauge = json.loads(QROW_SYM.read_text(encoding="utf-8"))
    reduced = json.loads(REDUCED.read_text(encoding="utf-8"))
    canon = json.loads(CANON.read_text(encoding="utf-8"))
    nested = json.loads(NESTED.read_text(encoding="utf-8"))
    deriv = json.loads(DERIV.read_text(encoding="utf-8"))

    objs=(lock,result,search,qrow,replay,gauge,reduced,canon,nested,deriv)
    if any(x["operation"] != "OZ-RT-BZ-T3-009" for x in objs):
        raise AssertionError("operation drift")
    if any(x.get("route","T3_SEQUENCE_RECURRENCE_EXTRACTION_001") != "T3_SEQUENCE_RECURRENCE_EXTRACTION_001" for x in objs):
        raise AssertionError("route drift")
    if lock["a0"] != EXPECTED_A0 or lock["coefficients"]["c3"] != EXPECTED_C3:
        raise AssertionError("locked forward recurrence coefficient drift")
    if lock["source"]["commit"] != EXPECTED_SOURCE_COMMITS[0]:
        raise AssertionError("upstream recurrence source drift")
    if lock["source"]["programme_lock"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_001/OZ_RT_BZ_T3_001.json":
        raise AssertionError("Programme recurrence authority drift")

    if result["execution_intake"]["protected_head"] != "fa283a283c4584c79af86fec632d50aa49e6d640" or result["execution_intake"]["protected_tree"] != "49f644c8ff4462015833d6477dfb6fde5b847970":
        raise AssertionError("protected intake drift")
    rows=result["finite_component_baseline"]
    if [x["n"] for x in rows] != list(range(7)) or rows[1]["P5"] != [87,4] or rows[1]["W"] != [-87,2] or any(x["D"] != [0,1] for x in rows):
        raise AssertionError("finite nonvacuity baseline drift")
    residuals=result["finite_residual_baseline"]
    if [x["n"] for x in residuals] != list(range(4)) or any(x[key] != [0,1] for x in residuals for key in ("L_P5","L_W","L_D")):
        raise AssertionError("finite recurrence residual drift")
    nv=result["nonvacuity"]
    if not nv["scalar_D_recurrence_fitting_forbidden"] or nv["finite_residuals_are_proof"]:
        raise AssertionError("vacuity/proof firewall drift")

    ms=result["moving_support"]
    if not ms["uniform_support_proof_complete"] or ms["shell_omission"] or search["common_support"]["square"] != ms["common_square"]:
        raise AssertionError("moving-support drift")
    if not search["common_support"]["uniform_zero_extension_lemma"] or search["common_support"]["shell_omission"]:
        raise AssertionError("search support firewall drift")
    if search["flux"]["basis_monomials"] != 198 or search["flux"]["basis_sha256"] != "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438":
        raise AssertionError("protected raw-jet basis drift")
    if search["flux"]["coefficient_total_degrees"] != [0,1,2] or search["denominator_condition"]["max_harmonic_argument_on_strongest_grid"] != 63 or search["denominator_condition"]["max_flux_linear_factor"] != 43:
        raise AssertionError("bounded generic search drift")
    for kind in ("D","P5","W"):
        stages=search["target_results"][kind]["stages"]
        if [(x["coefficient_rank"],x["augmented_rank"]) for x in stages] != EXPECTED_RANKS or any(x["classification"] != "EXACT_AFFINE_INCONSISTENCY" for x in stages):
            raise AssertionError(f"bounded recurrence-rank drift: {kind}")
    if search["bounded_terminal"] != "LOCKED_LBZ_NPLUS3_SYMMETRIC_RAW_JET_DIVERGENCE_DEG_LE_2_EXHAUSTED_FOR_D_P5_W":
        raise AssertionError("bounded recurrence terminal drift")

    src=qrow["source_certificate"]
    if src["blob_sha1"] != EXPECTED_QROW_BLOB or src["present_identically_at_commits"] != EXPECTED_SOURCE_COMMITS:
        raise AssertionError("Q-row source drift")
    if src["programme_reverification_status"] != "EXACT_RATIONAL_REPLAY_COMPLETE_WITH_REGULARIZED_BOUNDARY_FLUX" or src["upstream_certified_label_is_programme_authority"]:
        raise AssertionError("Q-row authority/replay drift")
    if not qrow["product_rule"]["kernel_identity_reverified"] or not qrow["product_rule"]["algebraic_reduction_proved"]:
        raise AssertionError("Q-row product-rule replay lost")
    if qrow["product_rule"]["delta_convention"] != "Delta_k F(n,k,l)=F(n,k+1,l)-F(n,k,l); analogously for l":
        raise AssertionError("Q-row delta convention drift")
    qm=qrow["moving_support"]
    if not qm["programme_uniform_zero_extension_already_proved"] or qm["qrow_boundary_recheck_required"] or not qm["qrow_boundary_recheck_complete"] or not qm["outer_flux_vanishes_for_K_ge_n_plus_3"]:
        raise AssertionError("Q-row boundary status drift")
    if qrow["terminal"] != "QROW_KERNEL_CERTIFICATE_REVERIFIED_REDUCED_WEIGHT5_RESIDUAL_LOCKED":
        raise AssertionError("Q-row terminal drift")

    if replay["source_lock"]["blob_sha1"] != EXPECTED_QROW_BLOB:
        raise AssertionError("Q-row replay source drift")
    rp=replay["replay"]
    if rp["arithmetic"] != "EXACT_RATIONAL" or rp["risc_loaded"] or rp["kernel_ratio_reconstruction"] != "DIRECT_FROM_GAMMA_PRODUCT":
        raise AssertionError("Q-row replay arithmetic/independence drift")
    if not rp["cleared_numerator_identically_zero"] or rp["finite_sampling_used_as_proof"] or rp["syntactic_cancel_used_as_proof"]:
        raise AssertionError("Q-row exact zero-test firewall drift")
    bp=replay["boundary_and_poles"]
    if bp["rho_at_k_zero"] != "0" or bp["sigma_at_l_zero"] != "0" or bp["nonnegative_shell_offsets"] != [1,2,3] or bp["candidate_shell_pole_order"] != 2 or bp["kernel_reciprocal_gamma_zero_order"] != 2:
        raise AssertionError("Q-row shell/lower-boundary drift")
    if bp["kernel_zero_leading_coefficients_offsets_1_2_3"] != [1,1,4] or not all(bp["rho_shell_regularized_coefficients_finite"]) or not all(bp["sigma_shell_regularized_coefficients_finite"]):
        raise AssertionError("Q-row shell regularization drift")
    if not bp["joint_shell_intersections_finite"] or not bp["finite_box_telescoping_boundary_complete"]:
        raise AssertionError("Q-row boundary completion drift")
    if replay["classification"] != "EXACT_QROW_KERNEL_CERTIFICATE_REVERIFIED_WITH_REGULARIZED_BOUNDARY_FLUX":
        raise AssertionError("Q-row replay classification drift")

    ge=gauge["exact_replay"]
    if not ge["rho_sym_equals_swapped_sigma_sym"] or not ge["rho_sym_at_k_zero"] or not ge["sigma_sym_at_l_zero"] or not ge["cleared_kernel_identity_numerator_zero"] or ge["finite_sampling_used_as_proof"]:
        raise AssertionError("symmetric Q-row gauge replay drift")
    if gauge["regularized_flux"]["relation"] != "Rl_sym(n,k,l)=Rk_sym(n,l,k)":
        raise AssertionError("symmetric regularized flux relation drift")
    if gauge["direct_D_reduction"]["status"] != "EXACT_SYMMETRY_REDUCTION_OF_THE_REVERIFIED_RESIDUAL_SUM" or gauge["residual_sum_zero_proved"]:
        raise AssertionError("symmetric residual reduction inflation/drift")

    if canon["producer"]["git_blob_sha1"] != "72c7ff8c24a119022cb41ebf65e7f1ecd136e6e8":
        raise AssertionError("canonical producer identity drift")
    pt=canon["protected_target"]
    if (pt["monomial_count"],pt["atom_count"],pt["max_atomic_arity"],pt["basis_sha256"]) != (198,41,4,"cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438"):
        raise AssertionError("canonical protected target drift")
    if canon["closure"]["closure_only_atoms"] != [] or not canon["closure"]["closed_inside_original_41_atom_system"] or canon["closure"]["max_atomic_arity_reduces_to"] != 3:
        raise AssertionError("canonical atom closure/arity drift")
    for label,expected in EXPECTED_CANONICAL.items():
        x=canon["shift_differences"][label]
        if (x["canonical_monomials"],x["atom_count"],x["max_atomic_arity"],x["sha256"]) != expected:
            raise AssertionError(f"canonical shift profile drift: {label}")
    pc=canon["producer_cross_checks"]
    if pc["exact_atom_shift_and_full_target_checks"] != 840 or pc["bundle_sha256"] != EXPECTED_CANON_BUNDLE or pc["finite_sampling_used_as_symbolic_proof"]:
        raise AssertionError("canonical producer cross-check/digest drift")
    if canon["classification"] != "DIRECT_ED_WEIGHT_DIFFERENCES_CANONICALIZED_IN_PROTECTED_ATOM_SYSTEM" or canon["residual_sum_zero_proved"]:
        raise AssertionError("canonical result classification/promotion drift")

    if nested["parent"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_009/RESIDUAL_CANONICAL_RESULT.json":
        raise AssertionError("nested skeleton parent drift")
    if nested["basis"] != {
        "N11":"U(k,l;1,2)+U(l,k;1,2)",
        "N12k":"2*ES(l;1,3)-U(k,l;2,2)",
        "N12l":"2*ES(k;1,3)-U(l,k;2,2)"}:
        raise AssertionError("nested skeleton basis drift")
    if not all(nested["coordinate_relations"].values()):
        raise AssertionError("nested coordinate relation drift")
    if nested["eliminated_nested_coordinates"] != EXPECTED_NESTED_ELIMINATED:
        raise AssertionError("nested eliminated-coordinate drift")
    if nested["terminal"] != "DIRECT_ED_NESTED_SECTOR_REDUCED_TO_THREE_PROTECTED_COMBINATIONS" or nested["residual_sum_zero_proved"]:
        raise AssertionError("nested skeleton terminal/promotion drift")

    if deriv["parent"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_009/NESTED_SKELETON_REDUCTION.json":
        raise AssertionError("differentiated certificate parent drift")
    if deriv["status"] != "GLOBAL_REGULARIZED_DERIVATIVE_CERTIFICATES_COMPLETE":
        raise AssertionError("differentiated certificate status drift")
    ie=deriv["interior_gamma_extension"]
    if ie["Lk_identity"] != "Lk=-partial_k log(T)" or ie["Ll_identity"] != "Ll=-partial_l log(T)":
        raise AssertionError("interior first-derivative identity drift")
    if ie["cross_log_identity"] != "partial_k partial_l log(T)=-C2" or ie["A_identity"] != "A:=Lk*Ll-C2=(partial_k partial_l T)/T":
        raise AssertionError("interior mixed-derivative identity drift")
    le=deriv["lattice_extension"]
    if le["T_times_Lk"] != "T*Lk_disc=-partial_k T on every integer point of 0<=k,l<=n+3":
        raise AssertionError("Lk lattice extension drift")
    if le["T_times_Ll"] != "T*Ll_disc=-partial_l T on every integer point of 0<=k,l<=n+3":
        raise AssertionError("Ll lattice extension drift")
    if le["T_times_A"] != "T*A_disc=partial_k partial_l T on every integer point of 0<=k,l<=n+3":
        raise AssertionError("A lattice extension drift")
    nd=deriv["nested_weight_decomposition"]
    if nd["nested_Dweight"] != "r22_nested + Lk*N12k + Ll*N12l + A*N11":
        raise AssertionError("nested differentiated decomposition drift")
    dc=deriv["regularized_derivative_certificates"]
    if dc["for_Lk"]["identity"] != "E[Lk]=Delta_k(Jk_Lk)+Delta_l(Jl_Lk)":
        raise AssertionError("Lk differentiated certificate drift")
    if dc["for_Ll"]["identity"] != "E[Ll]=Delta_k(Jk_Ll)+Delta_l(Jl_Ll)":
        raise AssertionError("Ll differentiated certificate drift")
    if dc["for_A"]["identity"] != "E[A]=Delta_k(Jk_A)+Delta_l(Jl_A)":
        raise AssertionError("A differentiated certificate drift")
    sr=deriv["shell_reconciliation"]
    lower=sr["lower_boundary"]
    if sr["base_certificate_pole_order"] != 2 or sr["kernel_zero_order"] != 2 or not sr["finite_box_boundary_complete"]:
        raise AssertionError("regularized differentiated shell/boundary drift")
    if not all(lower[x] for x in ("rho_sym_at_k_zero","partial_k_rho_sym_at_k_zero","sigma_sym_at_l_zero","partial_l_sigma_sym_at_l_zero")):
        raise AssertionError("regularized differentiated lower-boundary drift")
    witness=sr["historical_cubic_pole_witness"]
    if not witness["denominator_divisible_by_x_cubed"] or witness["denominator_divisible_by_x_fourth"] or not witness["numerator_nonzero_at_x_zero"]:
        raise AssertionError("historical generic-field pole witness drift")
    if not deriv["abel_transfer"]["nested_sector_reduced_to_one_body"] or not deriv["nested_sector_globally_reduced_to_one_body"]:
        raise AssertionError("global nested-to-one-body reduction lost")
    if deriv["residual_sum_zero_proved"] or deriv["terminal"] != "NESTED_GLOBAL_REGULARIZED_DERIVATIVE_CERTIFICATE_COMPLETE_ONE_BODY_REDUCTION_NEXT":
        raise AssertionError("differentiated certificate terminal/promotion drift")

    if reduced["kernel_certificate"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_009/QROW_REPLAY_RESULT.json" or reduced["general_residual"]["summation_identity_status"] != "EXACT_DISCRETE_PRODUCT_RULE_WITH_REVERIFIED_QROW_AND_ZERO_BOUNDARY_FLUX":
        raise AssertionError("reduced residual derivation drift")
    if reduced["protected_weight_instantiations"]["E_D"]["v"] != "W1+2*w5_sym" or reduced["protected_weight_instantiations"]["E_D"]["linearity"] != "E_D=E_W+2*E_P5":
        raise AssertionError("T3 reduced weight/linearity drift")
    cr=reduced["canonicalization"]
    if cr["closure_only_atoms"] != [] or cr["protected_atom_count"] != 41 or cr["difference_max_atomic_arity"] != 3:
        raise AssertionError("reduced canonicalization binding drift")
    sg=reduced["symmetric_gauge_reduction"]
    if sg["spatial_sum_orientations_after_index_swap"] != 1 or sg["four_channels"] != ["n1","n2","n3","k1"]:
        raise AssertionError("one-orientation residual reduction drift")
    ns=reduced["nested_skeleton"]
    if ns["dimension"] != 3 or ns["basis"] != ["N11","N12k","N12l"] or not ns["all_weight4_weight5_r22_nested_coordinates_eliminated_from_shift_differences"]:
        raise AssertionError("reduced nested skeleton binding drift")
    ndc=reduced["nested_derivative_certificates"]
    if ndc["artifact"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_009/NESTED_DERIVATIVE_CERTIFICATE_ROUTE.json":
        raise AssertionError("reduced differentiated certificate binding drift")
    if ndc["certificate_status"] != "GLOBAL_REGULARIZED_DERIVATIVE_CERTIFICATES_COMPLETE" or not ndc["nested_sector_globally_reduced_to_one_body"]:
        raise AssertionError("reduced global differentiated status drift")
    obr=reduced["one_body_reduction"]
    if obr["nested_atoms_remaining_after_transfer"] != 0 or obr["status"] != "MATHEMATICALLY_JUSTIFIED_CONSTRUCTION_NEXT":
        raise AssertionError("one-body reduction boundary drift")
    if reduced["residual_sum_zero_proved"] or reduced["terminal"] != EXPECTED_REDUCED_TERMINAL:
        raise AssertionError("reduced residual terminal/promotion drift")

    if result["source_artifact_audit"]["RFD_ann.m"]["relevance"] != "NOT_A_T3_CERTIFICATE":
        raise AssertionError("middle-row checkpoint promoted into T3")
    if any(x["proof_effect"] != "NONE" or x["promotion_effect"] != "NONE" for x in objs):
        raise AssertionError("proof or promotion inflation")
    if any(x["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER" for x in objs):
        raise AssertionError("T3 status inflation")
    if result["terminal"] != "RECURRENCE_INTERFACE_LOCKED_NONVACUOUS_BASELINE_AND_MOVING_SUPPORT_CERTIFIED":
        raise AssertionError("baseline terminal drift")


def main() -> int:
    validate()
    print("OZ-RT-BZ-T3-009 recurrence, Q-row, canonical direct E_D, globally reconciled nested certificates, and one-body reduction boundary is valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
