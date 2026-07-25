#!/usr/bin/env python3
"""Replay the BSD-WP03 substrate contract using only the Python standard library."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
WP02_LEDGER = ROOT.parent / "WP02_THEOREM_LEDGER" / "02_THEOREM_LEDGER.json"
OPEN_BSD = {"BSD-RANK-Q", "BSD-SHA-Q", "BSD-LEAD-Q"}
CERTIFICATE_STATES = {
    "COMPOSABLE_STANDARD",
    "COMPOSABLE",
    "COMPOSABLE_OPERATIONAL_INTERFACE",
    "COMPOSABLE_RESTRICTED",
    "COMPOSABLE_RESTRICTED_P_PART",
    "INDIVIDUAL_ONLY",
}


class ContractError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ContractError(f"{path.name}: top level must be an object")
    return value


def require(obj: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise ContractError(f"{label}: missing {missing}")


def wp02_records() -> dict[str, dict[str, Any]]:
    ledger = load(WP02_LEDGER)
    require(ledger, ["records"], "WP02 ledger")
    records: dict[str, dict[str, Any]] = {}
    for record in ledger["records"]:
        require(record, ["id", "composition_state"], "WP02 record")
        if record["id"] in records:
            raise ContractError(f"WP02 ledger: duplicate {record['id']}")
        records[record["id"]] = record
    return records


def validate_certificate(obj: dict[str, Any], records: dict[str, dict[str, Any]]) -> None:
    require(
        obj,
        [
            "schema_version", "artifact_id", "trust_class", "status", "scope",
            "curve", "claims", "theorem_interfaces", "theorem_applications",
            "normalization", "computation", "proof_evidence", "claim_boundary",
        ],
        "certificate",
    )
    if obj["trust_class"] != "individual_curve_certificate" or obj["scope"] != "individual_curve":
        raise ContractError("certificate: wrong trust class or scope")
    if obj.get("universal_claim") is not False:
        raise ContractError("certificate: universal_claim must be false")

    curve = obj["curve"]
    require(curve, ["canonical_id", "integral_weierstrass_coefficients"], "curve")
    coeffs = curve["integral_weierstrass_coefficients"]
    if not isinstance(coeffs, list) or len(coeffs) != 5 or not all(isinstance(x, int) for x in coeffs):
        raise ContractError("curve: expected five integral Weierstrass coefficients")
    a1, a2, a3, a4, a6 = coeffs
    b2 = a1 * a1 + 4 * a2
    b4 = a1 * a3 + 2 * a4
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    if -(b2 * b2 * b8) - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6 == 0:
        raise ContractError("curve: singular Weierstrass model")

    claims = obj["claims"]
    if not isinstance(claims, list) or not claims:
        raise ContractError("certificate: claims must be nonempty")
    for claim in claims:
        require(claim, ["claim_kind", "statement", "scope"], "claim")
        if claim["scope"] != "individual_curve":
            raise ContractError("claim: scope drift")

    interfaces = obj["theorem_interfaces"]
    if not isinstance(interfaces, list) or not interfaces:
        raise ContractError("certificate: theorem_interfaces must be nonempty")
    for interface_id in interfaces:
        record = records.get(interface_id)
        if record is None:
            raise ContractError(f"certificate: unknown WP02 interface {interface_id}")
        state = record["composition_state"]
        if state not in CERTIFICATE_STATES:
            raise ContractError(f"certificate: {interface_id} is not composable ({state})")

    applications = obj["theorem_applications"]
    if not isinstance(applications, list) or not applications:
        raise ContractError("certificate: theorem_applications must be nonempty")
    applied: set[str] = set()
    for application in applications:
        require(application, ["interface_id", "hypotheses_verified", "evidence_refs"], "application")
        interface_id = application["interface_id"]
        if interface_id not in interfaces or interface_id in applied:
            raise ContractError("certificate: undeclared or duplicate theorem application")
        if not application["hypotheses_verified"] or not application["evidence_refs"]:
            raise ContractError("certificate: theorem application lacks evidence")
        applied.add(interface_id)
    if applied != set(interfaces):
        raise ContractError("certificate: each interface needs one application record")

    analytic = {"analytic_rank", "leading_term_p_part", "full_leading_term"}
    if any(claim["claim_kind"] in analytic for claim in claims):
        if obj["normalization"].get("complex_L") != "complete_complex_L":
            if not obj["normalization"].get("explicit_conversion_proof"):
                raise ContractError("certificate: analytic claim lacks complete-L normalization")

    if obj["status"] == "CERTIFIED":
        evidence = obj["proof_evidence"]
        allowed = {
            "exact_symbolic", "rigorous_interval", "theorem_application",
            "formal_certificate", "independently_replayed_certificate",
        }
        if not evidence or any(item.get("kind") not in allowed for item in evidence):
            raise ContractError("certificate: CERTIFIED requires proof-producing evidence")
        if any(claim["claim_kind"] == "full_leading_term" for claim in claims):
            required = {"global_sha_finiteness", "global_sha_order", "exact_arithmetic_factors"}
            if not required.issubset(obj):
                raise ContractError("certificate: full leading term lacks global arithmetic evidence")

    if obj["claim_boundary"].get("universal_BSD") is not False:
        raise ContractError("certificate: boundary permits universal BSD")


def validate_experiment(obj: dict[str, Any]) -> None:
    require(
        obj,
        [
            "schema_version", "artifact_id", "trust_class", "status", "scope",
            "snapshot", "selection", "population_count", "software", "outputs",
            "claim_boundary",
        ],
        "experiment",
    )
    if obj["trust_class"] != "finite_database_experiment" or obj["scope"] != "finite_snapshot":
        raise ContractError("experiment: wrong trust class or scope")
    if obj.get("universal_claim") is not False:
        raise ContractError("experiment: universal_claim must be false")
    count = obj["population_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        raise ContractError("experiment: population_count must be a positive integer")
    require(obj["snapshot"], ["source", "immutable_id", "retrieval_date"], "snapshot")
    require(obj["selection"], ["query", "inclusion_rule"], "selection")
    if any(obj["claim_boundary"].get(key) is True for key in
           ("universal_BSD", "density_theorem", "individual_certificate")):
        raise ContractError("experiment: prohibited promotion")


def validate_formal(obj: dict[str, Any], registry_ids: set[str]) -> None:
    require(
        obj,
        [
            "schema_version", "artifact_id", "trust_class", "status",
            "interface_id", "imports", "axioms", "open_conjecture_axioms",
            "claim_boundary",
        ],
        "formal interface",
    )
    if obj["trust_class"] != "formal_interface" or obj["interface_id"] not in registry_ids:
        raise ContractError("formal interface: wrong class or unknown interface")
    if set(obj["open_conjecture_axioms"]) & OPEN_BSD:
        raise ContractError("formal interface: open BSD proposition imported as axiom")
    if obj["claim_boundary"].get("proves_BSD") is not False:
        raise ContractError("formal interface: boundary claims BSD")


def registry_ids() -> set[str]:
    registry = load(ROOT / "04_FORMAL_INTERFACE_REGISTRY.json")
    require(registry, ["interfaces"], "registry")
    ids: set[str] = set()
    for interface in registry["interfaces"]:
        require(interface, ["id", "forbidden_axioms"], "registry interface")
        if interface["id"] in ids:
            raise ContractError(f"registry: duplicate {interface['id']}")
        ids.add(interface["id"])
    return ids


def validate_policy() -> None:
    policy = load(ROOT / "05_CLAIM_PROMOTION_POLICY.json")
    require(policy, ["forbidden_edges", "gates"], "policy")
    targets = {edge["to"] for edge in policy["forbidden_edges"]}
    if not OPEN_BSD.issubset(targets):
        raise ContractError("policy: universal targets are not all forbidden")
    for gate in ("mechanism_generation", "novelty_claims", "restricted_target_selection", "wp04"):
        if policy["gates"].get(gate) != "CLOSED":
            raise ContractError(f"policy: {gate} must remain CLOSED")


def accept(label: str, validator: Callable[..., None], obj: dict[str, Any], *args: Any) -> None:
    validator(obj, *args)
    print(f"ACCEPT {label}")


def reject(label: str, validator: Callable[..., None], obj: dict[str, Any], *args: Any) -> None:
    try:
        validator(obj, *args)
    except ContractError as error:
        print(f"REJECT {label}: {error}")
        return
    raise AssertionError(f"{label}: adversarial fixture was accepted")


def main() -> int:
    records = wp02_records()
    interfaces = registry_ids()
    validate_policy()
    accept("valid individual candidate", validate_certificate,
           load(FIXTURES / "valid_individual_candidate.json"), records)
    accept("valid finite experiment", validate_experiment,
           load(FIXTURES / "valid_database_experiment.json"))
    accept("valid formal interface", validate_formal,
           load(FIXTURES / "valid_formal_interface.json"), interfaces)
    reject("finite experiment promoted to universal", validate_experiment,
           load(FIXTURES / "invalid_universal_from_finite.json"))
    reject("numerical-only certificate", validate_certificate,
           load(FIXTURES / "invalid_certificate_numerical_only.json"), records)
    reject("open BSD axiom in formal interface", validate_formal,
           load(FIXTURES / "invalid_formal_open_axiom.json"), interfaces)
    print("BSD-WP03 substrate replay passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
