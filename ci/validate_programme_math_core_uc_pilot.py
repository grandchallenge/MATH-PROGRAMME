#!/usr/bin/env python3
"""Validate the first real MATH-CORE-01 MATHSOLVE -> MATHCERT pilot."""
from __future__ import annotations

import sys

import validate_programme_math_core as core

PILOT_TRACE = core.ROOT / "governance/math_core_01/pilots/UC-001/blackboard.json"
HANDOFF_SNAPSHOT = core.ROOT / "governance/math_core_01/pilots/UC-001/artifacts/mathsolve_handoff_snapshot.json"
MATHCERT_SNAPSHOT = core.ROOT / "governance/math_core_01/pilots/UC-001/artifacts/mathcert_theorem_snapshot.json"
UNIVERSAL_SNAPSHOT = core.ROOT / "governance/math_core_01/pilots/UC-001/artifacts/universal_target_snapshot.json"

RESTRICTED_CLAIM = "MCORE-UC-C-RESTRICTED"
UNIVERSAL_CLAIM = "MCORE-UC-C-FRANKL"
ROUTE_OBLIGATION = "MCORE-UC-O-ROUTE"
UNIVERSAL_OBLIGATION = "MCORE-UC-O-UNIVERSAL"
LEAN_EQUIVALENCE = "MCORE-UC-Q-LEAN"
EXPECTED_BOUNDARY = "Restricted Lean theorems and finite replay through n <= 4 do not prove Frankl's conjecture."


def event_by_subject(trace: dict, subject_id: str) -> dict:
    matches = [e for e in trace["events"] if e["subject"]["id"] == subject_id]
    if not matches:
        raise core.ProtocolError(f"UC-001 pilot object is missing: {subject_id}")
    if subject_id not in {ROUTE_OBLIGATION, UNIVERSAL_OBLIGATION} and len(matches) != 1:
        raise core.ProtocolError(f"UC-001 pilot object is not unique: {subject_id}")
    return matches[0]


def validate_external_snapshots() -> None:
    handoff = core.load_json(HANDOFF_SNAPSHOT)
    mathcert = core.load_json(MATHCERT_SNAPSHOT)
    universal = core.load_json(UNIVERSAL_SNAPSHOT)

    expected_handoff = {
        "artifact_kind": "EXTERNAL_GOVERNED_HANDOFF_SNAPSHOT",
        "campaign_id": "UC-001",
        "source_repository": "grandchallenge/MATHSOLVE",
        "source_commit": "07814c1e28855ff0314737d3666642217da095a1",
        "source_path": "cert_handoffs/UC-001.json",
        "source_blob_sha1": "8369bc21e45be6af71d2a0cdb0c5ab3cb5313bfb",
        "handoff_id": "MC-HANDOFF-UC-001",
        "solve_work_package_id": "MS-UC-WP04",
    }
    for key, expected in expected_handoff.items():
        if handoff.get(key) != expected:
            raise core.ProtocolError(f"UC-001 MATHSOLVE handoff identity drift: {key}")
    selected = handoff.get("selected_claim", {})
    if selected.get("claim_id") != "UC-WP04-L001":
        raise core.ProtocolError("UC-001 pilot selected-claim identity drift")
    if selected.get("claim_type") != "CHECKED_RESTRICTED_THEOREM":
        raise core.ProtocolError("UC-001 pilot selected claim is no longer restricted")
    if selected.get("support_type") != "LEAN_FORMALIZATION":
        raise core.ProtocolError("UC-001 pilot selected-claim support drift")
    if handoff.get("claim_boundary") != EXPECTED_BOUNDARY:
        raise core.ProtocolError("UC-001 pilot MATHSOLVE claim boundary drift")
    if handoff.get("proof_obligation_dag", {}).get("open_terminal_obligation") != "UC-P04":
        raise core.ProtocolError("UC-001 pilot lost the open universal bridge obligation")

    expected_mathcert = {
        "artifact_kind": "EXTERNAL_FORMAL_REPRESENTATION_SNAPSHOT",
        "campaign_id": "UC-001",
        "claim_id": "UC-WP04-L001",
        "source_repository": "grandchallenge/MATHCERT",
        "source_commit": "d59173899dcd1a67dbe8f31de0b9f0917cd1459a",
        "source_path": "MathCert/Domains/UnionClosed/TwoElementCase.lean",
        "source_blob_sha1": "3caf5a7f2c0a2399970ed260f49daa01b3eb2ca4",
        "formal_identifier": "MathCert.UnionClosed.two_element_case",
        "representation_scope": "REPRESENTATION_EQUIVALENT",
        "promotion_effect": "NONE_DIRECT",
    }
    for key, expected in expected_mathcert.items():
        if mathcert.get(key) != expected:
            raise core.ProtocolError(f"UC-001 MATHCERT representation identity drift: {key}")
    lane = mathcert.get("programme_replay_lane", {})
    if lane.get("job_id") != "union-closed-mathcert":
        raise core.ProtocolError("UC-001 pilot Programme replay-lane drift")
    if lane.get("pinned_mathcert_commit") != expected_mathcert["source_commit"]:
        raise core.ProtocolError("UC-001 pilot MATHCERT replay pin drift")

    if universal.get("artifact_kind") != "EXTERNAL_OPEN_TARGET_SNAPSHOT":
        raise core.ProtocolError("UC-001 universal target snapshot kind drift")
    if universal.get("claim_id") != "UC-FRANKL":
        raise core.ProtocolError("UC-001 universal target claim identity drift")
    if universal.get("status") != "OPEN_PROBLEM":
        raise core.ProtocolError("UC-001 universal target is no longer explicitly open")
    if universal.get("open_terminal_obligation") != "UC-P04":
        raise core.ProtocolError("UC-001 universal bridge obligation drift")
    if universal.get("boundary") != EXPECTED_BOUNDARY:
        raise core.ProtocolError("UC-001 universal target boundary drift")


def validate_uc_pilot(trace: dict, registry: dict) -> None:
    blackboard_schema = core.load_json(core.BLACKBOARD_SCHEMA)
    core.validate_schema(trace, blackboard_schema, "UC-001 pilot blackboard")
    core.validate_trace(trace, registry)
    validate_external_snapshots()

    state = core.materialize(trace["events"])
    if state["resolved_obligations"].get(ROUTE_OBLIGATION) != "DISCHARGED":
        raise core.ProtocolError("UC-001 routing obligation is not explicitly discharged")
    if ROUTE_OBLIGATION in state["open_obligations"]:
        raise core.ProtocolError("UC-001 routing obligation remained open after discharge")
    if UNIVERSAL_OBLIGATION not in state["open_obligations"]:
        raise core.ProtocolError("UC-001 universal Frankl bridge must remain open")
    if UNIVERSAL_OBLIGATION in state["resolved_obligations"]:
        raise core.ProtocolError("UC-001 pilot may not resolve the universal Frankl bridge")

    if any(e["event_type"] == "CERTIFICATE" for e in trace["events"]):
        raise core.ProtocolError("UC-001 integration pilot may map existing evidence but may not manufacture a new certificate")

    universal_events = [e for e in trace["events"] if e["subject"]["id"] == UNIVERSAL_CLAIM]
    if len(universal_events) != 1 or universal_events[0]["event_type"] != "ASSERT":
        raise core.ProtocolError("UC-001 universal Frankl target may only enter the pilot as an external canonical reference")
    if universal_events[0]["payload"].get("working_class") != "EXTERNAL_CANONICAL_REFERENCE":
        raise core.ProtocolError("UC-001 universal Frankl target lost external-canonical-reference status")

    restricted = event_by_subject(trace, RESTRICTED_CLAIM)
    if restricted["event_type"] != "ASSERT" or restricted["payload"].get("working_class") != "EXTERNAL_CANONICAL_REFERENCE":
        raise core.ProtocolError("UC-001 restricted theorem must enter as an external canonical reference")

    equivalence = event_by_subject(trace, LEAN_EQUIVALENCE)
    if equivalence["event_type"] != "EQUIVALENCE":
        raise core.ProtocolError("UC-001 pinned Lean representation mapping is missing")
    if equivalence["payload"].get("relation_scope") != "REPRESENTATION_EQUIVALENT":
        raise core.ProtocolError("UC-001 pilot may not upgrade formal-representation mapping to mathematical equivalence")
    members = set(equivalence["payload"].get("members", []))
    expected_formal = "formal:MathCert.UnionClosed.two_element_case@d59173899dcd1a67dbe8f31de0b9f0917cd1459a"
    if members != {RESTRICTED_CLAIM, expected_formal}:
        raise core.ProtocolError("UC-001 pilot formal-representation members drift")

    for event in trace["events"]:
        if event["event_type"] == "PROPAGATE" and UNIVERSAL_CLAIM in event.get("dependencies", []):
            raise core.ProtocolError("UC-001 pilot may not propagate the universal Frankl target")


def main() -> int:
    try:
        registry = core.load_json(core.CAPABILITY_REGISTRY)
        trace = core.load_json(PILOT_TRACE)
        core.validate_capabilities(registry)
        validate_uc_pilot(trace, registry)
        print("MATH-CORE-01 UC-001 pilot: content-addressed context valid")
        print("MATH-CORE-01 UC-001 pilot: MATHSOLVE restricted claim mapped to pinned MATHCERT representation")
        print("MATH-CORE-01 UC-001 pilot: routing obligation discharged explicitly")
        print("MATH-CORE-01 UC-001 pilot: universal Frankl bridge remains OPEN_PROBLEM / open obligation")
        print("MATH-CORE-01 UC-001 pilot: no new certificate or canonical promotion created")
        return 0
    except (OSError, core.json.JSONDecodeError, core.jsonschema.SchemaError, core.ProtocolError) as exc:
        print(f"MATH-CORE-01 UC-001 pilot validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
