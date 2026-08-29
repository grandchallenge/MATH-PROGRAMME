#!/usr/bin/env python3
"""Validate the MATH-CORE-01 reference protocol and semantic invariants."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_VERSION = "MATH-CORE-01/0.1.0"
BLACKBOARD_SCHEMA = ROOT / "schemas/math_core_blackboard.schema.json"
AGENT_SCHEMA = ROOT / "schemas/math_core_theory_agent.schema.json"
CAPABILITY_SCHEMA = ROOT / "schemas/math_core_capability_registry.schema.json"
CAPABILITY_REGISTRY = ROOT / "governance/math_core_01/capability_registry.json"
REFERENCE_TRACE = ROOT / "governance/math_core_01/reference_blackboard.json"
REFERENCE_EXCHANGE = ROOT / "governance/math_core_01/reference_agent_exchange.json"


class ProtocolError(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProtocolError(f"expected JSON object: {path.relative_to(ROOT)}")
    return value


def validate_schema(instance: dict, schema: dict, label: str) -> None:
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    if errors:
        rendered = "; ".join(f"{list(e.absolute_path)}: {e.message}" for e in errors[:8])
        raise ProtocolError(f"{label} schema validation failed: {rendered}")


def checkpoint_key(value: dict) -> tuple[str, str, str]:
    return (str(value["kind"]), str(value["locator"]), str(value["revision"]))


def materialize(events: list[dict]) -> dict:
    views: dict[str, list[str] | dict[str, str]] = {
        "claims": [],
        "obligations": [],
        "conflicts": [],
        "constraints": [],
        "equivalences": [],
        "witnesses": [],
        "certificates": [],
        "superseded": {},
    }
    kind_to_view = {
        "CLAIM": "claims",
        "OBLIGATION": "obligations",
        "CONFLICT": "conflicts",
        "CONSTRAINT": "constraints",
        "EQUIVALENCE": "equivalences",
        "WITNESS": "witnesses",
        "CERTIFICATE": "certificates",
    }
    for event in events:
        if event["event_type"] == "SUPERSEDE":
            superseded = views["superseded"]
            assert isinstance(superseded, dict)
            superseded[event["payload"]["target_id"]] = event["payload"]["replacement_id"]
            continue
        view = views[kind_to_view[event["subject"]["kind"]]]
        assert isinstance(view, list)
        view.append(event["subject"]["id"])
    return views


def validate_capabilities(registry: dict) -> None:
    if registry.get("protocol_version") != PROTOCOL_VERSION:
        raise ProtocolError("capability registry protocol version drift")
    invariants = registry["authority_invariants"]
    forbidden_true = (
        "canonical_claim_promotion_by_protocol_event",
        "human_steward_authority_may_be_inferred",
        "producer_self_authorization_allowed",
    )
    if any(invariants.get(key) is not False for key in forbidden_true):
        raise ProtocolError("capability registry authority boundary weakened")
    for name, row in registry["producer_classes"].items():
        if row.get("canonical_claim_promotion") is not False:
            raise ProtocolError(f"producer class {name} may not acquire canonical promotion authority")


def validate_trace(trace: dict, registry: dict) -> None:
    if trace.get("protocol_version") != PROTOCOL_VERSION:
        raise ProtocolError("reference trace protocol version drift")
    base = checkpoint_key(trace["base_checkpoint"])
    allowed = registry["producer_classes"]
    seen_event_ids: set[str] = set()
    seen_objects: dict[str, str] = {}
    conflicts: set[str] = set()

    for index, event in enumerate(trace["events"]):
        event_id = event["event_id"]
        event_type = event["event_type"]
        subject_id = event["subject"]["id"]
        producer_class = event["producer"]["class"]

        if event_id in seen_event_ids:
            raise ProtocolError(f"duplicate event id: {event_id}")
        seen_event_ids.add(event_id)

        if checkpoint_key(event["base_checkpoint"]) != base:
            raise ProtocolError(f"reference event {event_id} is not bound to the trace checkpoint")

        if event_type not in allowed[producer_class]["blackboard_event_types"]:
            raise ProtocolError(f"producer class {producer_class} is not authorized for {event_type}")

        unresolved = [dep for dep in event["dependencies"] if dep not in seen_objects]
        if unresolved:
            raise ProtocolError(f"event {event_id} has unresolved or forward dependencies: {unresolved}")

        if event_type == "LEARN":
            source = event["payload"]["source_conflict_id"]
            if source not in conflicts:
                raise ProtocolError(f"learn event {event_id} does not reference an earlier conflict")
            if source not in event["dependencies"]:
                raise ProtocolError(f"learn event {event_id} must depend on its source conflict")
            if event["payload"]["effect"] != "SEARCH_ONLY":
                raise ProtocolError(f"learn event {event_id} escaped SEARCH_ONLY scope")

        if event_type == "EQUIVALENCE" and event["payload"]["relation_scope"] == "MATHEMATICALLY_EQUIVALENT":
            if not event["evidence_refs"]:
                raise ProtocolError(f"mathematical equivalence {event_id} lacks evidence")

        if event_type == "WITNESS":
            target = event["payload"]["target_id"]
            if target not in seen_objects:
                raise ProtocolError(f"witness {event_id} targets an unresolved object: {target}")

        if event_type == "CERTIFICATE":
            if producer_class not in {"MATHCERT", "CHECKER"}:
                raise ProtocolError(f"certificate {event_id} has non-certifying producer class {producer_class}")
            target = event["payload"]["target_id"]
            if target not in seen_objects:
                raise ProtocolError(f"certificate {event_id} targets an unresolved object: {target}")
            if event["payload"]["ledger_effect"] != "NONE_DIRECT":
                raise ProtocolError(f"certificate {event_id} attempts direct ledger mutation")

        if event_type == "SUPERSEDE":
            target = event["payload"]["target_id"]
            replacement = event["payload"]["replacement_id"]
            if target == replacement:
                raise ProtocolError(f"supersede event {event_id} is self-referential")
            if target not in seen_objects or replacement not in seen_objects:
                raise ProtocolError(f"supersede event {event_id} references unresolved objects")
            if subject_id != replacement:
                raise ProtocolError(f"supersede event {event_id} subject must be the replacement object")
        else:
            if subject_id in seen_objects:
                raise ProtocolError(f"working object {subject_id} is recreated instead of superseded")
            seen_objects[subject_id] = event["subject"]["kind"]
            if event_type == "CONFLICT":
                conflicts.add(subject_id)

        if event_type == "PROPAGATE" and not event["dependencies"]:
            raise ProtocolError(f"propagation {event_id} lacks dependencies")
        if event_type == "CONFLICT" and not event["dependencies"]:
            raise ProtocolError(f"conflict {event_id} lacks an explanation dependency set")

    first = json.dumps(materialize(trace["events"]), sort_keys=True, separators=(",", ":"))
    second = json.dumps(materialize(trace["events"]), sort_keys=True, separators=(",", ":"))
    if first != second:
        raise ProtocolError("reference replay is not deterministic")


def validate_exchange(exchange: dict, trace: dict, registry: dict) -> None:
    if exchange.get("protocol_version") != PROTOCOL_VERSION:
        raise ProtocolError("reference exchange protocol version drift")
    allowed = registry["producer_classes"]
    trace_objects = {e["subject"]["id"] for e in trace["events"] if e["event_type"] != "SUPERSEDE"}
    requests: dict[str, dict] = {}
    seen_messages: set[str] = set()

    for message in exchange["messages"]:
        message_id = message["message_id"]
        if message_id in seen_messages:
            raise ProtocolError(f"duplicate theory-agent message id: {message_id}")
        seen_messages.add(message_id)

        if message["message_type"] == "REQUEST":
            request_id = message["request_id"]
            if request_id in requests:
                raise ProtocolError(f"duplicate request id: {request_id}")
            if message["obligation_id"] not in trace_objects:
                raise ProtocolError(f"request {request_id} targets an unknown obligation")
            unknown_refs = [ref for ref in message["context_refs"] + message["assumptions"] if ref not in trace_objects]
            if unknown_refs:
                raise ProtocolError(f"request {request_id} contains unresolved context: {unknown_refs}")
            requests[request_id] = message
            continue

        request_id = message["request_id"]
        if request_id not in requests:
            raise ProtocolError(f"response {message_id} has no earlier request")
        request = requests[request_id]
        if checkpoint_key(message["base_checkpoint"]) != checkpoint_key(request["base_checkpoint"]):
            raise ProtocolError(f"response {message_id} is stale relative to its request")
        producer_class = message["producer"]["class"]
        proposal_types = set(allowed[producer_class]["theory_proposal_types"])
        for proposal in message["proposals"]:
            if proposal["proposal_type"] not in proposal_types:
                raise ProtocolError(
                    f"producer class {producer_class} is not authorized to propose {proposal['proposal_type']}"
                )
            unresolved = [dep for dep in proposal["dependencies"] if dep not in trace_objects]
            if unresolved:
                raise ProtocolError(f"response {message_id} proposes from unresolved dependencies: {unresolved}")


def main() -> int:
    try:
        blackboard_schema = load_json(BLACKBOARD_SCHEMA)
        agent_schema = load_json(AGENT_SCHEMA)
        capability_schema = load_json(CAPABILITY_SCHEMA)
        registry = load_json(CAPABILITY_REGISTRY)
        trace = load_json(REFERENCE_TRACE)
        exchange = load_json(REFERENCE_EXCHANGE)

        validate_schema(registry, capability_schema, "capability registry")
        validate_schema(trace, blackboard_schema, "reference blackboard")
        validate_schema(exchange, agent_schema, "reference theory-agent exchange")
        validate_capabilities(registry)
        validate_trace(trace, registry)
        validate_exchange(exchange, trace, registry)
        print("MATH-CORE-01: wire schemas valid")
        print("MATH-CORE-01: capability boundary valid")
        print("MATH-CORE-01: reference replay deterministic")
        print("MATH-CORE-01: theory-agent exchange proposal-only and checkpoint-bound")
        return 0
    except (OSError, json.JSONDecodeError, jsonschema.SchemaError, ProtocolError) as exc:
        print(f"MATH-CORE-01 validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
