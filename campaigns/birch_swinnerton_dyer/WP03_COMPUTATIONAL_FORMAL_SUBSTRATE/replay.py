#!/usr/bin/env python3
"""Replay the BSD-WP03 substrate contract using only the Python standard library."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
OPEN_BSD = {"BSD-RANK-Q", "BSD-SHA-Q", "BSD-LEAD-Q"}
WP02_PREFIX = "BSD-T-"


class ContractError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ContractError(f"{path.name}: top-level value must be an object")
    return value


def require_keys(obj: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise ContractError(f"{label}: missing required keys {missing}")


def validate_certificate(obj: dict[str, Any]) -> None:
    require_keys(
        obj,
        [
            "schema_version", "artifact_id", "trust_class", "status", "scope",
            "curve", "claims", "theorem_interfaces", "normalization",
            "computation", "proof_evidence", "claim_boundary",
        ],
        "certificate",
    )
    if obj["trust_class"] != "individual_curve_certificate":
        raise ContractError("certificate: wrong trust class")
    if obj["scope"] != "individual_curve":
        raise ContractError("certificate: scope must be individual_curve")
    if obj.get("universal_claim") is not False:
        raise ContractError("certificate: universal_claim must be false")
    curve = obj["curve"]
    require_keys(curve, ["canonical_id", "integral_weierstrass_coefficients"], "curve")
    coeffs = curve["integral_weierstrass_coefficients"]
    if not isinstance(coeffs, list) or len(coeffs) != 5 or not all(isinstance(x, int) for x in coeffs):
        raise ContractError("curve: integral Weierstrass model must contain five integers")
    a1, a2, a3, a4, a6 = coeffs
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    discriminant = -(b2 * b2 * b8) - 8 * (b4 ** 3) - 27 * (b6 ** 2) + 9 * b2 * b4 * b6
    if discriminant == 0:
        raise ContractError("curve: Weierstrass model is singular")
    claims = obj["claims"]
    if not isinstance(claims, list) or not claims:
        raise ContractError("certificate: claims must be a nonempty list")
    for claim in claims:
        require_keys(claim, ["claim_kind", "statement", "scope"], "claim")
        if claim["scope"] != "individual_curve":
            raise ContractError("claim: scope drift")
    interfaces = obj["theorem_interfaces"]
    if not isinstance(interfaces, list) or not all(
        isinstance(item, str) and item.startswith(WP02_PREFIX) for item in interfaces
    ):
        raise ContractError("certificate: theorem interfaces must be BSD-WP02 records")
    analytic_claim = any(
        claim["claim_kind"] in {"analytic_rank", "leading_term_p_part", "full_leading_term"}
        for claim in claims
    )
    if analytic_claim and obj["normalization"].get("complex_L") != "complete_complex_L":
        if not obj["normalization"].get("explicit_conversion_proof"):
            raise ContractError("certificate: analytic claim lacks complete-L normalization")
    if obj["status"] == "CERTIFIED":
        evidence = obj["proof_evidence"]
        if not isinstance(evidence, list) or not evidence:
            raise ContractError("certificate: CERTIFIED requires proof-producing evidence")
        allowed = {
            "exact_symbolic", "rigorous_interval", "theorem_application",
            "formal_certificate", "independently_replayed_certificate",
        }
        for item in evidence:
            if item.get("kind") not in allowed:
                raise ContractError("certificate: unsupported evidence kind")
        if any(claim["claim_kind"] == "full_leading_term" for claim in claims):
            required = {"global_sha_finiteness", "global_sha_order", "exact_arithmetic_factors"}
            if not required.issubset(obj):
                raise ContractError("certificate: full leading term lacks global arithmetic evidence")
    boundary = obj["claim_boundary"]
    if boundary.get("universal_BSD") is not False:
        raise ContractError("certificate: claim boundary permits universal BSD")


def validate_experiment(obj: dict[str, Any]) -> None:
    require_keys(
        obj,
        [
            "schema_version", "artifact_id", "trust_class", "status", "scope",
            "snapshot", "selection", "population_count", "software", "outputs",
            "claim_boundary",
        ],
        "experiment",
    )
    if obj["trust_class"] != "finite_database_experiment":
        raise ContractError("experiment: wrong trust class")
    if obj["scope"] != "finite_snapshot":
        raise ContractError("experiment: scope must be finite_snapshot")
    if obj.get("universal_claim") is not False:
        raise ContractError("experiment: universal_claim must be false")
    if not isinstance(obj["population_count"], int) or isinstance(obj["population_count"], bool) or obj["population_count"] <= 0:
        raise ContractError("experiment: population_count must be a positive integer")
    require_keys(obj["snapshot"], ["source", "immutable_id", "retrieval_date"], "snapshot")
    require_keys(obj["selection"], ["query", "inclusion_rule"], "selection")
    boundary = obj["claim_boundary"]
    if any(boundary.get(key) is True for key in ("universal_BSD", "density_theorem", "individual_certificate")):
        raise ContractError("experiment: prohibited promotion in claim boundary")


def validate_formal(obj: dict[str, Any], registry_ids: set[str]) -> None:
    require_keys(
        obj,
        [
            "schema_version", "artifact_id", "trust_class", "status",
            "interface_id", "imports", "axioms", "open_conjecture_axioms",
            "claim_boundary",
        ],
        "formal interface",
    )
    if obj["trust_class"] != "formal_interface":
        raise ContractError("formal interface: wrong trust class")
    if obj["interface_id"] not in registry_ids:
        raise ContractError("formal interface: unknown registry id")
    if set(obj["open_conjecture_axioms"]) & OPEN_BSD:
        raise ContractError("formal interface: open BSD proposition imported as axiom")
    if obj["claim_boundary"].get("proves_BSD") is not False:
        raise ContractError("formal interface: boundary claims BSD")


def validate_registry(registry: dict[str, Any]) -> set[str]:
    require_keys(registry, ["schema_version", "artifact_id", "interfaces"], "registry")
    ids: set[str] = set()
    for interface in registry["interfaces"]:
        require_keys(
            interface,
            [
                "id", "name", "statement", "imports", "forbidden_axioms",
                "formalization_state", "claim_scope",
            ],
            "registry interface",
        )
        if interface["id"] in ids:
            raise ContractError(f"registry: duplicate id {interface['id']}")
        ids.add(interface["id"])
        if not isinstance(interface["forbidden_axioms"], list):
            raise ContractError("registry: forbidden_axioms must be a list")
    return ids


def validate_policy(policy: dict[str, Any]) -> None:
    require_keys(
        policy,
        ["schema_version", "artifact_id", "trust_classes", "allowed_edges", "forbidden_edges", "gates"],
        "policy",
    )
    forbidden_targets = {edge["to"] for edge in policy["forbidden_edges"]}
    if not {"BSD-RANK-Q", "BSD-SHA-Q", "BSD-LEAD-Q"}.issubset(forbidden_targets):
        raise ContractError("policy: universal BSD targets are not all forbidden")
    for gate in ("mechanism_generation", "novelty_claims", "restricted_target_selection", "wp04"):
        if policy["gates"].get(gate) != "CLOSED":
            raise ContractError(f"policy: {gate} must remain CLOSED")


def expect_accept(label: str, function, obj: dict[str, Any], *args: Any) -> None:
    function(obj, *args)
    print(f"ACCEPT {label}")


def expect_reject(label: str, function, obj: dict[str, Any], *args: Any) -> None:
    try:
        function(obj, *args)
    except ContractError as error:
        print(f"REJECT {label}: {error}")
        return
    raise AssertionError(f"{label}: adversarial fixture was accepted")


def main() -> int:
    registry = load(ROOT / "04_FORMAL_INTERFACE_REGISTRY.json")
    registry_ids = validate_registry(registry)
    validate_policy(load(ROOT / "05_CLAIM_PROMOTION_POLICY.json"))

    expect_accept(
        "valid individual candidate",
        validate_certificate,
        load(FIXTURES / "valid_individual_candidate.json"),
    )
    expect_accept(
        "valid finite experiment",
        validate_experiment,
        load(FIXTURES / "valid_database_experiment.json"),
    )
    expect_accept(
        "valid formal interface",
        validate_formal,
        load(FIXTURES / "valid_formal_interface.json"),
        registry_ids,
    )

    expect_reject(
        "finite experiment promoted to universal",
        validate_experiment,
        load(FIXTURES / "invalid_universal_from_finite.json"),
    )
    expect_reject(
        "numerical-only certificate",
        validate_certificate,
        load(FIXTURES / "invalid_certificate_numerical_only.json"),
    )
    expect_reject(
        "open BSD axiom in formal interface",
        validate_formal,
        load(FIXTURES / "invalid_formal_open_axiom.json"),
        registry_ids,
    )

    print("BSD-WP03 substrate replay passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
