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
REDUCED = HERE / "REDUCED_WEIGHT5_RESIDUAL.json"

EXPECTED_A0 = "41218*n^3+198849*n^2+320790*n+173057"
EXPECTED_C3 = "2*(n+3)^5*(2*n+5)*a0(n)"
EXPECTED_RANKS = [(198,199),(792,793),(1980,1981)]
EXPECTED_QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
EXPECTED_SOURCE_COMMITS = [
    "968477ed7e406df6542f8da6fbe1cd6ca7273c47",
    "790685b7ee4f642a8a88a1bd120636d1b8b39ea8",
]


def validate() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    result = json.loads(BASELINE.read_text(encoding="utf-8"))
    search = json.loads(SEARCH.read_text(encoding="utf-8"))
    qrow = json.loads(QROW.read_text(encoding="utf-8"))
    replay = json.loads(QROW_REPLAY.read_text(encoding="utf-8"))
    reduced = json.loads(REDUCED.read_text(encoding="utf-8"))

    if any(x["operation"] != "OZ-RT-BZ-T3-009" for x in (lock,result,search,qrow,replay,reduced)):
        raise AssertionError("operation drift")
    if any(x["route"] != "T3_SEQUENCE_RECURRENCE_EXTRACTION_001" for x in (lock,result,search,replay,reduced)):
        raise AssertionError("route drift")
    if lock["a0"] != EXPECTED_A0 or lock["coefficients"]["c3"] != EXPECTED_C3:
        raise AssertionError("locked forward recurrence coefficient drift")
    if lock["source"]["commit"] != EXPECTED_SOURCE_COMMITS[0]:
        raise AssertionError("upstream recurrence source drift")
    if lock["source"]["programme_lock"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_001/OZ_RT_BZ_T3_001.json":
        raise AssertionError("Programme recurrence authority drift")

    if result["execution_intake"]["protected_head"] != "fa283a283c4584c79af86fec632d50aa49e6d640":
        raise AssertionError("protected intake head drift")
    if result["execution_intake"]["protected_tree"] != "49f644c8ff4462015833d6477dfb6fde5b847970":
        raise AssertionError("protected intake tree drift")
    rows = result["finite_component_baseline"]
    if [x["n"] for x in rows] != list(range(7)):
        raise AssertionError("finite component range drift")
    if rows[1]["P5"] != [87,4] or rows[1]["W"] != [-87,2]:
        raise AssertionError("nonvacuity witness drift")
    if any(x["D"] != [0,1] for x in rows):
        raise AssertionError("finite target baseline drift")
    residuals = result["finite_residual_baseline"]
    if [x["n"] for x in residuals] != list(range(4)):
        raise AssertionError("finite recurrence range drift")
    if any(x[key] != [0,1] for x in residuals for key in ("L_P5","L_W","L_D")):
        raise AssertionError("finite recurrence residual drift")
    nv = result["nonvacuity"]
    if not nv["scalar_D_recurrence_fitting_forbidden"] or nv["finite_residuals_are_proof"]:
        raise AssertionError("vacuity/proof firewall drift")

    ms = result["moving_support"]
    if not ms["uniform_support_proof_complete"] or ms["shell_omission"]:
        raise AssertionError("moving-support zero-extension certificate drift")
    if search["common_support"]["square"] != ms["common_square"]:
        raise AssertionError("search/support square drift")
    if not search["common_support"]["uniform_zero_extension_lemma"] or search["common_support"]["shell_omission"]:
        raise AssertionError("search support firewall drift")
    if search["flux"]["basis_monomials"] != 198 or search["flux"]["basis_sha256"] != "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438":
        raise AssertionError("protected raw-jet basis drift")
    if search["flux"]["coefficient_total_degrees"] != [0,1,2]:
        raise AssertionError("bounded degree ladder drift")
    if search["denominator_condition"]["max_harmonic_argument_on_strongest_grid"] != 63:
        raise AssertionError("harmonic denominator-bound drift")
    if search["denominator_condition"]["max_flux_linear_factor"] != 43:
        raise AssertionError("flux denominator-bound drift")
    for kind in ("D","P5","W"):
        stages=search["target_results"][kind]["stages"]
        if [(x["coefficient_rank"],x["augmented_rank"]) for x in stages] != EXPECTED_RANKS:
            raise AssertionError(f"bounded recurrence-rank drift: {kind}")
        if any(x["classification"] != "EXACT_AFFINE_INCONSISTENCY" for x in stages):
            raise AssertionError(f"bounded recurrence classification drift: {kind}")
    if search["bounded_terminal"] != "LOCKED_LBZ_NPLUS3_SYMMETRIC_RAW_JET_DIVERGENCE_DEG_LE_2_EXHAUSTED_FOR_D_P5_W":
        raise AssertionError("bounded recurrence terminal drift")

    src=qrow["source_certificate"]
    if src["blob_sha1"] != EXPECTED_QROW_BLOB:
        raise AssertionError("Q-row source blob drift")
    if src["present_identically_at_commits"] != EXPECTED_SOURCE_COMMITS:
        raise AssertionError("Q-row source-head concordance drift")
    if src["programme_reverification_status"] != "EXACT_RATIONAL_REPLAY_COMPLETE_WITH_REGULARIZED_BOUNDARY_FLUX":
        raise AssertionError("Q-row replay status drift")
    if src["upstream_certified_label_is_programme_authority"]:
        raise AssertionError("Q-row upstream authority inflation")
    if not qrow["product_rule"]["kernel_identity_reverified"] or not qrow["product_rule"]["algebraic_reduction_proved"]:
        raise AssertionError("Q-row kernel/product-rule replay lost")
    if qrow["product_rule"]["delta_convention"] != "Delta_k F(n,k,l)=F(n,k+1,l)-F(n,k,l); analogously for l":
        raise AssertionError("Q-row delta convention drift")
    qm=qrow["moving_support"]
    if not qm["programme_uniform_zero_extension_already_proved"] or qm["qrow_boundary_recheck_required"] or not qm["qrow_boundary_recheck_complete"]:
        raise AssertionError("Q-row boundary status drift")
    if not qm["outer_flux_vanishes_for_K_ge_n_plus_3"]:
        raise AssertionError("Q-row outer boundary drift")
    if qrow["terminal"] != "QROW_KERNEL_CERTIFICATE_REVERIFIED_REDUCED_WEIGHT5_RESIDUAL_LOCKED":
        raise AssertionError("Q-row terminal drift")

    if replay["source_lock"]["blob_sha1"] != EXPECTED_QROW_BLOB:
        raise AssertionError("Q-row replay source drift")
    rp=replay["replay"]
    if rp["arithmetic"] != "EXACT_RATIONAL" or rp["risc_loaded"]:
        raise AssertionError("Q-row replay arithmetic/independence drift")
    if rp["kernel_ratio_reconstruction"] != "DIRECT_FROM_GAMMA_PRODUCT":
        raise AssertionError("Q-row ratio reconstruction drift")
    if not rp["cleared_numerator_identically_zero"] or rp["finite_sampling_used_as_proof"] or rp["syntactic_cancel_used_as_proof"]:
        raise AssertionError("Q-row exact zero-test firewall drift")
    bp=replay["boundary_and_poles"]
    if bp["rho_at_k_zero"] != "0" or bp["sigma_at_l_zero"] != "0":
        raise AssertionError("Q-row lower boundary drift")
    if bp["nonnegative_shell_offsets"] != [1,2,3] or bp["candidate_shell_pole_order"] != 2 or bp["kernel_reciprocal_gamma_zero_order"] != 2:
        raise AssertionError("Q-row shell order drift")
    if bp["kernel_zero_leading_coefficients_offsets_1_2_3"] != [1,1,4]:
        raise AssertionError("Q-row reciprocal-Gamma shell coefficient drift")
    if not all(bp["rho_shell_regularized_coefficients_finite"]) or not all(bp["sigma_shell_regularized_coefficients_finite"]):
        raise AssertionError("Q-row shell regularization drift")
    if not bp["joint_shell_intersections_finite"] or not bp["finite_box_telescoping_boundary_complete"]:
        raise AssertionError("Q-row boundary completion drift")
    if replay["classification"] != "EXACT_QROW_KERNEL_CERTIFICATE_REVERIFIED_WITH_REGULARIZED_BOUNDARY_FLUX":
        raise AssertionError("Q-row replay classification drift")

    if reduced["kernel_certificate"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_009/QROW_REPLAY_RESULT.json":
        raise AssertionError("reduced residual kernel binding drift")
    if reduced["general_residual"]["summation_identity_status"] != "EXACT_DISCRETE_PRODUCT_RULE_WITH_REVERIFIED_QROW_AND_ZERO_BOUNDARY_FLUX":
        raise AssertionError("reduced residual derivation drift")
    if reduced["protected_weight_instantiations"]["E_D"]["v"] != "W1+2*w5_sym":
        raise AssertionError("T3 reduced weight drift")
    if reduced["protected_weight_instantiations"]["E_D"]["linearity"] != "E_D=E_W+2*E_P5":
        raise AssertionError("reduced residual linearity drift")
    if reduced["residual_sum_zero_proved"]:
        raise AssertionError("reduced residual promoted without proof")
    if reduced["terminal"] != "QROW_REVERIFIED_REDUCED_WEIGHT5_RESIDUAL_INTERFACE_LOCKED":
        raise AssertionError("reduced residual terminal drift")

    if result["source_artifact_audit"]["RFD_ann.m"]["relevance"] != "NOT_A_T3_CERTIFICATE":
        raise AssertionError("middle-row checkpoint promoted into T3")
    if any(x["proof_effect"] != "NONE" or x["promotion_effect"] != "NONE" for x in (result,search,qrow,replay,reduced)):
        raise AssertionError("proof or promotion inflation")
    if any(x["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER" for x in (result,search,qrow,replay,reduced)):
        raise AssertionError("T3 status inflation")
    if result["terminal"] != "RECURRENCE_INTERFACE_LOCKED_NONVACUOUS_BASELINE_AND_MOVING_SUPPORT_CERTIFIED":
        raise AssertionError("baseline terminal drift")


def main() -> int:
    validate()
    print("OZ-RT-BZ-T3-009 recurrence, Q-row replay, regularized boundary, and reduced residual package is valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
