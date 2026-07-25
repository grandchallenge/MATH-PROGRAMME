#!/usr/bin/env python3
"""Replay BSD-WP04 target-selection and claim-boundary contracts."""

from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CAMPAIGN = ROOT.parent
WP01 = CAMPAIGN / "WP01_FALSE_PROOF_ATLAS" / "01_ATLAS.json"
WP02 = CAMPAIGN / "WP02_THEOREM_LEDGER" / "02_THEOREM_LEDGER.json"
DELTA = ROOT / "01_SOURCE_DELTA.json"
CANDIDATES = ROOT / "02_CANDIDATE_LEDGER.json"
DAG = ROOT / "04_PROOF_OBLIGATION_DAG.json"
GATES = ROOT / "05_CLAIM_AND_GATE.json"

COMPOSABLE = {
    "COMPOSABLE_STANDARD", "COMPOSABLE", "COMPOSABLE_OPERATIONAL_INTERFACE",
    "COMPOSABLE_RESTRICTED", "COMPOSABLE_RESTRICTED_P_PART", "INDIVIDUAL_ONLY",
}
REQUIRED_FIXTURES = {
    "BSD-FP-006", "BSD-FP-008", "BSD-FP-009", "BSD-FP-010",
    "BSD-FP-011", "BSD-FP-016", "BSD-FP-017", "BSD-FP-018",
}
HARD_GATES = {
    "exact_statement", "strictly_restricted", "audited_open_status",
    "non_circular", "normalization_fixed", "no_open_conjecture_axiom",
    "not_finite_data", "no_novelty_claim",
}
RECORD_FIELDS = {
    "id", "name", "status", "domain", "direction", "rank_range",
    "prime_profile", "reduction_profile", "residual_hypotheses",
    "selmer_structure", "normalization", "hypotheses", "conclusion",
    "source_ids", "source_locator", "composition_state",
}


class ContractError(ValueError):
    pass


def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ContractError(f"{path.name}: top level must be an object")
    return value


def require(obj, keys, label):
    missing = sorted(set(keys) - set(obj))
    if missing:
        raise ContractError(f"{label}: missing {missing}")


def validate_delta(delta):
    require(delta, {"sources", "records", "candidate_dispositions", "claim_boundary"}, "source delta")
    source_ids = set()
    for source in delta["sources"]:
        require(source, {"id", "citation", "kind", "locator", "audit_state", "url"}, "source")
        if source["id"] in source_ids:
            raise ContractError(f"duplicate source {source['id']}")
        source_ids.add(source["id"])
    for record in delta["records"]:
        require(record, RECORD_FIELDS, "delta theorem record")
        if not set(record["source_ids"]).issubset(source_ids):
            raise ContractError(f"{record['id']}: unknown delta source")
    boundary = delta["claim_boundary"]
    if boundary.get("new_theorem") is not False or boundary.get("novelty") is not False:
        raise ContractError("source delta overclaims theorem or novelty")


def theorem_records(base, delta):
    records = {}
    for record in list(base.get("records", [])) + list(delta.get("records", [])):
        require(record, RECORD_FIELDS, "theorem record")
        if record["id"] in records:
            raise ContractError(f"duplicate theorem record {record['id']}")
        records[record["id"]] = record
    return records


def adjusted(candidate):
    scores = candidate["scores"]
    return sum(value for key, value in scores.items() if key != "execution_cost") - scores["execution_cost"]


def validate_candidates(ledger, records, wp01_ids):
    require(ledger, {"selection_rule", "retired_before_scoring", "candidates", "selected_target_id", "claim_boundary"}, "candidate ledger")
    selected = [c for c in ledger["candidates"] if c["status"] == "SELECTED_RESEARCH_TARGET_UNPROVED"]
    if len(selected) != 1:
        raise ContractError("candidate ledger must select exactly one unproved target")
    target = selected[0]
    if target["id"] != ledger["selected_target_id"]:
        raise ContractError("selected target id mismatch")
    if adjusted(target) != target["adjusted_score"]:
        raise ContractError("selected score arithmetic mismatch")
    if target["adjusted_score"] < ledger["selection_rule"]["minimum_adjusted_score"]:
        raise ContractError("selected target below threshold")
    require(target["hard_gates"], HARD_GATES, "selected hard gates")
    if any(target["hard_gates"][gate] is not True for gate in HARD_GATES):
        raise ContractError("selected target fails a hard gate")
    fixtures = set(target["wp01_fixtures_to_bypass"])
    if not REQUIRED_FIXTURES.issubset(fixtures) or not fixtures.issubset(wp01_ids):
        raise ContractError("selected target has incomplete or unknown WP01 gates")
    for interface_id in target["imports"]:
        record = records.get(interface_id)
        if record is None:
            raise ContractError(f"unknown import {interface_id}")
        if record["composition_state"] not in COMPOSABLE:
            raise ContractError(f"noncomposable import {interface_id}")
    if any(source_id not in records for source_id in target["boundary_sources"]):
        raise ContractError("unknown boundary source")
    for token in ("ord_2", "ord_{s=1}L(E,s)=1", "semistable", "odd conductor"):
        if token not in target["statement"]:
            raise ContractError(f"selected statement lacks {token}")
    boundary = ledger["claim_boundary"]
    if boundary.get("universal_BSD") is not False or boundary.get("full_leading_term") is not False:
        raise ContractError("selection overclaims BSD")
    if boundary.get("novelty") is not False or boundary.get("mechanism_generation") != "CLOSED":
        raise ContractError("selection opens novelty or mechanism generation")
    return target["id"]


def validate_dag(dag, target_id):
    require(dag, {"target_id", "target_status", "nodes", "edges", "adversarial_gates", "mechanism_generation"}, "DAG")
    if dag["target_id"] != target_id or dag["target_status"] != "SELECTED_RESEARCH_TARGET_UNPROVED":
        raise ContractError("DAG target or truth status mismatch")
    node_ids = {node["id"] for node in dag["nodes"]}
    if len(node_ids) != len(dag["nodes"]):
        raise ContractError("duplicate DAG node")
    if any(source not in node_ids or target not in node_ids for source, target in dag["edges"]):
        raise ContractError("DAG edge references unknown node")
    if not REQUIRED_FIXTURES.issubset(set(dag["adversarial_gates"])):
        raise ContractError("DAG omits required adversarial gate")
    if dag["mechanism_generation"] != "CLOSED_PENDING_SEPARATE_AUTHORIZATION":
        raise ContractError("DAG opens mechanism generation")


def validate_gates(gates, target_id):
    require(gates, {"selected_target_id", "states", "prohibited_claims", "next_stage"}, "gate record")
    if gates["selected_target_id"] != target_id:
        raise ContractError("gate target mismatch")
    expected = {
        "target_selection": "PROVISIONAL_PENDING_REFEREE",
        "target_truth": "UNPROVED",
        "mechanism_generation": "CLOSED",
        "novelty_claims": "CLOSED",
        "universal_BSD": "OPEN_PROBLEM_UNCHANGED",
    }
    for key, value in expected.items():
        if gates["states"].get(key) != value:
            raise ContractError(f"gate {key} must be {value}")


def expect_reject(label, fn, *args):
    try:
        fn(*args)
    except ContractError as error:
        print(f"REJECT {label}: {error}")
        return
    raise AssertionError(f"{label}: mutation accepted")


def main():
    atlas = load(WP01)
    base = load(WP02)
    delta = load(DELTA)
    ledger = load(CANDIDATES)
    dag = load(DAG)
    gates = load(GATES)
    validate_delta(delta)
    records = theorem_records(base, delta)
    wp01_ids = {fixture["id"] for fixture in atlas["fixtures"]}
    target_id = validate_candidates(ledger, records, wp01_ids)
    validate_dag(dag, target_id)
    validate_gates(gates, target_id)
    print(f"ACCEPT selected target {target_id}")

    mutation = copy.deepcopy(ledger)
    mutation["claim_boundary"]["universal_BSD"] = True
    expect_reject("universal promotion", validate_candidates, mutation, records, wp01_ids)
    mutation = copy.deepcopy(ledger)
    mutation["candidates"][0]["status"] = "PROVED"
    expect_reject("truth promotion", validate_candidates, mutation, records, wp01_ids)
    mutation = copy.deepcopy(ledger)
    mutation["candidates"][0]["imports"].append("BSD-T-097")
    expect_reject("noncomposable source import", validate_candidates, mutation, records, wp01_ids)
    mutation = copy.deepcopy(ledger)
    mutation["claim_boundary"]["mechanism_generation"] = "OPEN"
    expect_reject("mechanism gate opened", validate_candidates, mutation, records, wp01_ids)
    mutation = copy.deepcopy(ledger)
    mutation["candidates"][0]["hard_gates"]["not_finite_data"] = False
    expect_reject("finite-data target", validate_candidates, mutation, records, wp01_ids)
    mutation = copy.deepcopy(dag)
    mutation["adversarial_gates"].pop("BSD-FP-006")
    expect_reject("one-prime firewall removed", validate_dag, mutation, target_id)

    print("BSD-WP04 target-selection replay passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
