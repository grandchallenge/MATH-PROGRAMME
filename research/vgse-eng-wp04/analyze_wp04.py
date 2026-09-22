#!/usr/bin/env python3
"""Deterministic consistency replay for VGSE-ENG-WP04."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def load(name: str) -> Any:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def validate() -> list[str]:
    errors: list[str] = []
    geometry = load("GEOMETRY_MODEL.json")
    evidence = load("EVIDENCE_MATRIX.json")
    hypotheses = load("HYPOTHESIS_LEDGER.json")
    results = load("RESULTS.json")
    claims = load("CLAIM_LEDGER.json")

    counts = evidence["counts"]
    expected_counts = {
        "total_reconstructed_pairs": 5,
        "genuinely_independent_pairs": 0,
        "independently_varied_quotient_points": 0,
        "source_geometry_records": 5,
        "source_geometry_records_with_authorized_quotient_pair": 0,
    }
    if counts != expected_counts:
        errors.append(f"evidence counts mismatch: {counts!r}")

    pairs = evidence["candidate_pairs"]
    if len(pairs) != 5:
        errors.append("expected exactly five reconstructed candidate pairs")
    if any(pair["independent"] for pair in pairs):
        errors.append("no reconstructed pair may be classified as independent")
    quotients = {pair["quotient"] for pair in pairs}
    if quotients != {"Q_PINNED_C_CANONICAL"}:
        errors.append(f"candidate pairs must share one quotient fixture, found {sorted(quotients)}")

    q = geometry["quotient_space"]
    if q["domain"] != "(R_{>0})^8":
        errors.append("quotient domain drift")
    expected_point = ["1", "1", "2/7", "25/7", "6/7", "3/25", "2/25", "9/7"]
    if q["protected_point"] != expected_point:
        errors.append("protected quotient point drift")
    if results["exact_quotient_point"]["coordinates"] != expected_point:
        errors.append("RESULTS quotient point disagrees with geometry model")

    if geometry["geometry_space"]["branch_count"] != 5:
        errors.append("C05 branch count drift")
    if geometry["geometry_space"]["continuous_family_established"]:
        errors.append("WP04 must not promote the five isolated branches to a certified continuous family")

    h = {entry["id"]: entry for entry in hypotheses["hypotheses"]}
    expected_status = {
        "H0": "SUPPORTED_AS_CURRENT_EVIDENTIARY_DISPOSITION",
        "H1": "FALSIFIED_IN_PROTECTED_SOURCE_GEOMETRY_TEST",
        "H2": "NOT_IDENTIFIABLE_FROM_CURRENT_EVIDENCE",
        "H3": "JACOBIAN_NOT_IDENTIFIABLE",
        "H4": "NOT_WARRANTED",
    }
    for key, status in expected_status.items():
        if h.get(key, {}).get("status") != status:
            errors.append(f"{key} status drift")

    h1 = h["H1"]["evidence"]
    if h1["source_pattern_count"] != 5:
        errors.append("H1 source pattern count drift")
    if h1["boundary_relabelings_exhausted"] != 720:
        errors.append("H1 must retain exhaustive 6! relabeling count")
    if h1["global_color_complement_conventions_tested"] != 2:
        errors.append("H1 color/complement convention count drift")
    if not h1["certified_rounding_robust_lower_bound"] > h1["required_lower_threshold"]:
        errors.append("H1 protected negative separation no longer exceeds threshold")
    if h1["minimum_observed_best_projective_distortion_factor"] < h1["certified_rounding_robust_lower_bound"]:
        errors.append("H1 certified lower bound cannot exceed observed distortion")

    if h["H3"].get("observed_output_rank") != 0:
        errors.append("H3 observed quotient sample variation rank must remain zero")
    if "rank-zero" not in h["H3"]["prohibited_inference"]:
        errors.append("H3 must explicitly prohibit interpreting non-identifiability as a zero Jacobian")

    ident = results["identifiability"]
    for field in (
        "general_phi_identified",
        "subset_of_quotient_coordinates_identified",
        "jacobian_identified",
        "latent_metric_model_identified",
    ):
        if ident[field]:
            errors.append(f"{field} must remain false")

    if results["terminal_disposition"] != "GEOMETRY_QUOTIENT_NON_IDENTIFIABLE":
        errors.append("unexpected terminal disposition")

    if results["response_consistency"]["required"]:
        errors.append("downstream WP02/WP03 replay must not be used as substitute coupling evidence")

    boundary = geometry["claim_boundary"]
    if any(boundary.values()):
        errors.append("geometry model crossed a forbidden claim boundary")
    if any(results["claim_boundary"].values()):
        errors.append("results crossed a forbidden claim boundary")

    claim_ids = {claim["id"] for claim in claims["claims"]}
    expected_claim_ids = {f"VGSE-ENG-WP04-C0{i}" for i in range(1, 9)}
    if claim_ids != expected_claim_ids:
        errors.append(f"claim ledger IDs drift: {sorted(claim_ids)}")

    return errors


def summary() -> dict[str, Any]:
    evidence = load("EVIDENCE_MATRIX.json")
    results = load("RESULTS.json")
    hypotheses = load("HYPOTHESIS_LEDGER.json")
    return {
        "work_package": "VGSE-ENG-WP04",
        "independent_pair_count": evidence["counts"]["genuinely_independent_pairs"],
        "independently_varied_quotient_points": evidence["counts"]["independently_varied_quotient_points"],
        "h1_certified_distortion_lower_bound": hypotheses["hypotheses"][1]["evidence"]["certified_rounding_robust_lower_bound"],
        "terminal_disposition": results["terminal_disposition"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        return 1
    if args.check:
        print("VGSE-ENG-WP04 deterministic replay: PASS")
    else:
        print(json.dumps(summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
