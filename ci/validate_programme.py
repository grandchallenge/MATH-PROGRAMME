#!/usr/bin/env python3
"""Validate programme classification, graph, mapping, review, and documentary contracts."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from validate_documentaries import documentary_contract_errors

ROOT = Path(__file__).resolve().parents[1]
MSC_CODE = re.compile(r"^\d{2}(?:-\d{2}|[A-Z](?:xx|\d{2}))$")
CORE_CAMPAIGN_AGENTS = (
    "Axiomatist",
    "Cartographer",
    "Verifier",
    "Adversary",
    "Formalist",
    "Amanuensis",
    "Referee",
)
# CI validates only the records explicitly registered here. Legacy campaign reviews
# use several pre-contract formats; add one only after complete migration to
# schemas/agent_review.schema.json.
SCHEMA_BOUND_AGENT_REVIEWS: tuple[str, ...] = (
    "reviews/union_closed/UC-WP01.agent_review.yaml",
    "reviews/navier_stokes/NS-CI-WP06.agent_review.yaml",
    "reviews/documentation/MKDOCS-COVERAGE.agent_review.yaml",
    "reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml",
    "reviews/governance/WORKFLOW-COVERAGE.agent_review.yaml",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema_name: str) -> list[str]:
    schema = load_json(ROOT / "schemas" / schema_name)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def foundational_profile_errors(instance: dict[str, Any], label: str) -> list[str]:
    if "foundational_profile" not in instance:
        return []
    return [
        f"{label}.foundational_profile: {error}"
        for error in schema_errors(instance["foundational_profile"], "foundational_profile.schema.json")
    ]


def agent_review_semantic_errors(instance: dict[str, Any], label: str) -> list[str]:
    """Enforce promotion semantics that are awkward to express in JSON Schema."""
    errors: list[str] = []
    promotion = instance.get("promotion", {})
    if not promotion.get("ready_for_next_stage", False):
        return errors

    council = instance.get("council_review", {})
    for agent in CORE_CAMPAIGN_AGENTS:
        status = council.get(agent, {}).get("status")
        if status != "reviewed":
            errors.append(
                f"{label}: promotion requires {agent} status reviewed, found {status!r}"
            )

    for agent, record in council.items():
        if record.get("status") == "blocked":
            errors.append(f"{label}: promotion cannot proceed while {agent} is blocked")

    for obligation in instance.get("unresolved_obligations", []):
        if obligation.get("blocking"):
            errors.append(
                f"{label}: promotion cannot proceed with blocking obligation "
                f"{obligation.get('id', '<unknown>')}"
            )

    return errors


def duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def schema_bound_review_registry_errors(review_paths: tuple[str, ...]) -> list[str]:
    """Validate the explicit CI binding registry without inferring legacy coverage."""
    errors: list[str] = []
    if not review_paths:
        return ["reviews: no schema-bound Agent Council review records registered"]
    for duplicate in sorted(duplicate_values(list(review_paths))):
        errors.append(f"reviews: duplicate schema-bound review registration {duplicate}")
    for relative in review_paths:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"reviews: schema-bound review path must be repository-relative: {relative}")
        if not relative.startswith("reviews/"):
            errors.append(f"reviews: schema-bound review must live under reviews/: {relative}")
        if path.suffix not in {".yaml", ".yml"}:
            errors.append(f"reviews: schema-bound review must be YAML: {relative}")
    return errors


def validate_documents(
    source_registry: dict[str, Any],
    graph: dict[str, Any],
    mappings: dict[str, Any],
    domain_registry: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    source_ids = {source["source_id"] for source in source_registry.get("sources", [])}
    if len(source_ids) != len(source_registry.get("sources", [])):
        errors.append("source registry contains duplicate source_id values")

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_ids = [node.get("node_id", "") for node in nodes]
    edge_ids = [edge.get("edge_id", "") for edge in edges]
    for duplicate in sorted(duplicate_values(node_ids)):
        errors.append(f"duplicate graph node_id: {duplicate}")
    for duplicate in sorted(duplicate_values(edge_ids)):
        errors.append(f"duplicate graph edge_id: {duplicate}")
    node_id_set = set(node_ids)
    for edge in edges:
        edge_id = edge.get("edge_id", "<unknown>")
        for endpoint in ("source", "target"):
            if edge.get(endpoint) not in node_id_set:
                errors.append(f"{edge_id}: dangling {endpoint} {edge.get(endpoint)!r}")
        for source_id in edge.get("provenance", {}).get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{edge_id}: unknown provenance source_id {source_id}")

    mapping_items = mappings.get("mappings", [])
    mapping_ids = [mapping.get("mapping_id", "") for mapping in mapping_items]
    for duplicate in sorted(duplicate_values(mapping_ids)):
        errors.append(f"duplicate mapping_id: {duplicate}")
    mapping_id_set = set(mapping_ids)
    primary_msc_by_ref: dict[str, list[str]] = {}
    for mapping in mapping_items:
        mapping_id = mapping.get("mapping_id", "<unknown>")
        if mapping.get("internal_ref") not in node_id_set:
            errors.append(f"{mapping_id}: unresolved internal_ref {mapping.get('internal_ref')!r}")
        source_id = mapping.get("provenance", {}).get("source_id")
        if source_id not in source_ids:
            errors.append(f"{mapping_id}: unknown provenance source_id {source_id}")
        if not mapping.get("scheme_version"):
            errors.append(f"{mapping_id}: unversioned mapping")
        if mapping.get("role") == "PRIMARY" and mapping.get("review_status") != "AUDITED":
            errors.append(f"{mapping_id}: primary mapping must be AUDITED")
        if mapping.get("scheme") == "MSC":
            if mapping.get("scheme_version") != "2020":
                errors.append(f"{mapping_id}: MSC mapping must use scheme version 2020")
            if not MSC_CODE.fullmatch(str(mapping.get("identifier", ""))):
                errors.append(f"{mapping_id}: invalid MSC code {mapping.get('identifier')!r}")
            if mapping.get("role") == "PRIMARY":
                primary_msc_by_ref.setdefault(mapping["internal_ref"], []).append(mapping_id)
    for internal_ref, primary_ids in primary_msc_by_ref.items():
        if len(primary_ids) > 1:
            errors.append(
                f"{internal_ref}: multiple primary MSC mappings: {', '.join(sorted(primary_ids))}"
            )

    domain_ids: set[str] = set()
    for domain in domain_registry.get("domains", []):
        domain_id = domain.get("domain_id", "<unknown>")
        if domain_id in domain_ids:
            errors.append(f"duplicate domain_id: {domain_id}")
        domain_ids.add(domain_id)
        for graph_ref in domain.get("knowledge_graph_refs", []):
            if graph_ref not in node_id_set:
                errors.append(f"{domain_id}: unresolved knowledge_graph_ref {graph_ref}")
        for mapping_ref in domain.get("classification_mapping_refs", []):
            if mapping_ref not in mapping_id_set:
                errors.append(f"{domain_id}: unresolved classification_mapping_ref {mapping_ref}")

    for candidate in candidates:
        problem_id = candidate.get("problem_id", "<unknown>")
        if candidate.get("domain_id") not in domain_ids:
            errors.append(f"{problem_id}: unresolved domain_id {candidate.get('domain_id')}")
        for graph_ref in candidate.get("knowledge_graph_refs", []):
            if graph_ref not in node_id_set:
                errors.append(f"{problem_id}: unresolved knowledge_graph_ref {graph_ref}")
        for mapping_ref in candidate.get("classification_mapping_refs", []):
            if mapping_ref not in mapping_id_set:
                errors.append(f"{problem_id}: unresolved classification_mapping_ref {mapping_ref}")
        for source_id in candidate.get("discovery_provenance", {}).get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{problem_id}: unknown discovery source_id {source_id}")
        errors.extend(foundational_profile_errors(candidate, problem_id))

    return errors


def main() -> int:
    documents = [
        ("classification/source_registry.json", "classification_source_registry.schema.json"),
        ("knowledge_graph/union_closed.json", "knowledge_graph.schema.json"),
        ("classification/mappings/union_closed.json", "external_mapping.schema.json"),
        ("examples/candidate_problem_union_closed.json", "candidate_problem.schema.json"),
    ]
    errors: list[str] = []
    loaded: dict[str, Any] = {}
    for relative_path, schema_name in documents:
        path = ROOT / relative_path
        instance = load_json(path)
        loaded[relative_path] = instance
        errors.extend(f"{relative_path}: {error}" for error in schema_errors(instance, schema_name))

    domain_registry = yaml.safe_load((ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    errors.extend(
        f"DOMAIN_REGISTRY.yaml: {error}"
        for error in schema_errors(domain_registry, "domain_registry.schema.json")
    )

    agent_review_template = yaml.safe_load(
        (ROOT / "templates" / "agent_review.yaml").read_text(encoding="utf-8")
    )
    errors.extend(
        f"templates/agent_review.yaml: {error}"
        for error in schema_errors(agent_review_template, "agent_review.schema.json")
    )

    errors.extend(schema_bound_review_registry_errors(SCHEMA_BOUND_AGENT_REVIEWS))
    for relative in SCHEMA_BOUND_AGENT_REVIEWS:
        review_path = ROOT / relative
        if not review_path.is_file():
            errors.append(f"{relative}: registered Agent Council review record is missing")
            continue
        review = yaml.safe_load(review_path.read_text(encoding="utf-8"))
        errors.extend(
            f"{relative}: {error}"
            for error in schema_errors(review, "agent_review.schema.json")
        )
        errors.extend(agent_review_semantic_errors(review, relative))

    ledger_paths = [
        ROOT / "templates" / "claim_ledger_template.yaml",
        ROOT / "templates" / "union_closed_claim_ledger_wp01.yaml",
    ]
    graph_ref_set = {
        node["node_id"]
        for node in loaded["knowledge_graph/union_closed.json"]["nodes"]
    }
    for ledger_path in ledger_paths:
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
        errors.extend(
            f"{ledger_path.relative_to(ROOT)}: {error}"
            for error in schema_errors(ledger, "claim_ledger.schema.json")
        )
        for claim in ledger.get("claims", []):
            for graph_ref in claim.get("knowledge_graph_refs", []):
                if graph_ref not in graph_ref_set:
                    errors.append(
                        f"{ledger_path.relative_to(ROOT)}: unresolved knowledge_graph_ref {graph_ref}"
                    )
            errors.extend(
                foundational_profile_errors(
                    claim,
                    f"{ledger_path.relative_to(ROOT)}:{claim.get('claim_id', '<unknown>')}",
                )
            )

    for schema_path in sorted((ROOT / "schemas").glob("*.json")):
        Draft202012Validator.check_schema(load_json(schema_path))

    errors.extend(
        validate_documents(
            loaded["classification/source_registry.json"],
            loaded["knowledge_graph/union_closed.json"],
            loaded["classification/mappings/union_closed.json"],
            domain_registry,
            [loaded["examples/candidate_problem_union_closed.json"]],
        )
    )
    errors.extend(documentary_contract_errors())

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"programme validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "programme classification, discovery, foundation, schema-bound review, and "
        "documentary contracts are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
