"""Evaluation engine for the OZ-WP01 false-proof atlas."""
from __future__ import annotations

from typing import Any

HYPOTHESES = {"H1", "H2", "H3", "H4", "H5"}


def evaluate(packet: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    claim_scope = packet.get("claim_scope")
    evidence_scope = packet.get("evidence_scope")

    if packet.get("normalization_pair") == "B/bMin" and packet.get("normalization_equivalence") != "bMin=6B":
        reasons.append("NORMALIZATION_EQUIVALENCE_MISSING")

    claim_modulus = packet.get("claim_modulus")
    evidence_modulus = packet.get("evidence_modulus")
    if claim_modulus and evidence_modulus and claim_modulus != evidence_modulus:
        reasons.append("MODULUS_MISMATCH")

    if evidence_scope == "finite" and claim_scope in {"unbounded", "uniform"}:
        reasons.append("FINITE_TO_UNBOUNDED")

    if claim_scope == "concrete_instance" and evidence_scope == "abstract_conditional":
        reasons.append("ABSTRACT_TO_INSTANCE")
        required = set(packet.get("required_hypotheses", []))
        discharged = set(packet.get("discharged_hypotheses", []))
        if required != HYPOTHESES or not HYPOTHESES <= discharged:
            reasons.append("HYPOTHESES_INCOMPLETE")

    if packet.get("operator_claim") == "annihilation" and packet.get("certificate_type") == "operator_definition":
        reasons.append("OPERATOR_DEFINITION_NOT_ANNIHILATION")

    if packet.get("target_identity") and packet.get("certificate_type") == "finite_match":
        reasons.append("FINITE_MATCH_NOT_IDENTITY")

    if packet.get("review_required") == "independent" and packet.get("review_origin") == "source_internal":
        reasons.append("SOURCE_INTERNAL_NOT_INDEPENDENT")

    if packet.get("formal_evidence") == "quarantined_declaration":
        reasons.append("SORRYAX_DEPENDENCY")

    if claim_scope == "uniform" and evidence_scope == "point":
        reasons.append("POINT_CERTIFICATE_NOT_UNIFORM")

    if packet.get("claim_prime_scope") == "all_primes" and packet.get("evidence_prime_scope") != "all_primes":
        reasons.append("PRIME_SCOPE_INFLATION")

    if packet.get("novelty_claim") == "NEW_AFTER_AUDIT" and packet.get("novelty_audit") != "exhaustive":
        reasons.append("NOVELTY_AUDIT_INCOMPLETE")

    if packet.get("irrationality_claim") is True and int(packet.get("bridges_open", 0)) > 0:
        reasons.append("IRRATIONALITY_BRIDGES_OPEN")

    if packet.get("sharp12_claim") is True:
        required = set(packet.get("required_dependencies", []))
        discharged = set(packet.get("discharged_dependencies", []))
        if not required or not required <= discharged:
            reasons.append("SHARP12_DEPENDENCIES_OPEN")

    if packet.get("operator_claim") == "reconstruction" and packet.get("source_inputs_complete") is not True:
        reasons.append("RECONSTRUCTION_INPUTS_MISSING")

    if claim_scope == "infinite_nonvanishing" and evidence_scope == "finite_nonzero":
        reasons.append("FINITE_NONVANISHING_NOT_INFINITE")

    return sorted(set(reasons))
