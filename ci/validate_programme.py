#!/usr/bin/env python3
"""Validate programme classification, graph, review, ledger, and documentary contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from validate_documentary_library import documentary_contract_errors
from openai_ten_proofs_intake_control import validation_errors as openai_ten_proofs_intake_errors

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
SCHEMA_BOUND_AGENT_REVIEWS: tuple[str, ...] = (
    "reviews/union_closed/UC-WP01.agent_review.yaml",
    "reviews/union_closed/UC-DOC-WP00.agent_review.yaml",
    "reviews/union_closed/UC-DOC-WP01.agent_review.yaml",
    "reviews/navier_stokes/NS-CI-WP06.agent_review.yaml",
    "reviews/documentation/MKDOCS-COVERAGE.agent_review.yaml",
    "reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml",
    "reviews/governance/WORKFLOW-COVERAGE.agent_review.yaml",
    "reviews/yang_mills/YM-WP01.agent_review.yaml",
    "reviews/yang_mills/YM-WP02.agent_review.yaml",
)
SCHEMA_BOUND_REVIEW_DISCOVERY_ROOTS: tuple[str, ...] = (
    "reviews/union_closed",
    "reviews/documentation",
    "reviews/governance",
    "reviews/yang_mills",
    "reviews/navier_stokes/NS-CI-WP06.agent_review.yaml",
)
SCHEMA_BOUND_CLAIM_LEDGERS: tuple[str, ...] = (
    "templates/claim_ledger_template.yaml",
    "templates/union_closed_claim_ledger_wp01.yaml",
    "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/10_CLAIM_LEDGER.yaml",
    "campaigns/yang_mills/WP01_FALSE_PROOF_ATLAS/10_CLAIM_LEDGER.yaml",
    "campaigns/yang_mills/WP02_THEOREM_LEDGER/10_CLAIM_LEDGER.yaml",
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
        for error in schema_errors(
            instance["foundational_profile"], "foundational_profile.schema.json"
        )
    ]


def agent_review_semantic_errors(instance: dict[str, Any], label: str) -> list[str]:
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


def duplicate_values(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def discovered_schema_bound_reviews(root: Path = ROOT) -> set[str]:
    discovered: set[str] = set()
    for relative in SCHEMA_BOUND_REVIEW_DISCOVERY_ROOTS:
        path = root / relative
        if path.is_file():
            paths = [path]
        elif path.is_dir():
            paths = sorted(path.rglob("*.agent_review.yaml"))
        else:
            paths = []
        for review_path in paths:
            try:
                review = yaml.safe_load(review_path.read_text(encoding="utf-8"))
            except yaml.YAMLError:
                continue
            if isinstance(review, dict) and not schema_errors(
                review, "agent_review.schema.json"
            ):
                discovered.add(review_path.relative_to(root).as_posix())
    return discovered


def schema_bound_review_registry_errors(
    review_paths: tuple[str, ...],
    root: Path = ROOT,
    *,
    discovered_paths: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not review_paths:
        return ["reviews: no schema-bound Agent Council review records registered"]
    for duplicate in sorted(duplicate_values(review_paths)):
        errors.append(f"reviews: duplicate schema-bound review registration {duplicate}")
    registered = set(review_paths)
    discovered = (
        discovered_paths
        if discovered_paths is not None
        else discovered_schema_bound_reviews(root)
    )
    for relative in sorted(discovered - registered):
        errors.append(f"reviews: discovered schema-bound review is unregistered: {relative}")
    for relative in review_paths:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            errors.append(
                f"reviews: schema-bound review path must be repository-relative: {relative}"
            )
        if not relative.startswith("reviews/"):
            errors.append(f"reviews: schema-bound review must live under reviews/: {relative}")
        if path.suffix not in {".yaml", ".yml"}:
            errors.append(f"reviews: schema-bound review must be YAML: {relative}")
        if not (root / relative).is_file():
            errors.append(f"reviews: registered schema-bound review is missing: {relative}")
    return errors


def discovered_canonical_claim_ledgers(root: Path = ROOT) -> set[str]:
    discovered: set[str] = set()
    for pattern in ("*.yaml", "*.yml"):
        for path in root.rglob(pattern):
            try:
                instance = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, yaml.YAMLError):
                continue
            if (
                isinstance(instance, dict)
                and instance.get("ledger_contract") == "canonical_claim_ledger"
            ):
                discovered.add(path.relative_to(root).as_posix())
    return discovered


def claim_ledger_registry_errors(
    ledger_paths: tuple[str, ...],
    root: Path = ROOT,
    *,
    discovered_paths: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not ledger_paths:
        return ["claim ledgers: no canonical ledgers registered"]
    for duplicate in sorted(duplicate_values(ledger_paths)):
        errors.append(f"claim ledgers: duplicate registration {duplicate}")
    registered = set(ledger_paths)
    discovered = (
        discovered_paths
        if discovered_paths is not None
        else discovered_canonical_claim_ledgers(root)
    )
    for relative in sorted(discovered - registered):
        errors.append(f"claim ledgers: discovered canonical ledger is unregistered: {relative}")
    for relative in sorted(registered - discovered):
        errors.append(
            "claim ledgers: registered canonical ledger is missing or lacks its "
            f"contract marker: {relative}"
        )
    for relative in ledger_paths:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"claim ledgers: path must be repository-relative: {relative}")
        if path.suffix not in {".yaml", ".yml"}:
            errors.append(f"claim ledgers: canonical ledger must be YAML: {relative}")
    return errors


def claim_ledger_semantic_errors(
    ledgers: list[tuple[str, dict[str, Any]]], graph_ref_set: set[str]
) -> list[str]:
    errors: list[str] = []
    ledger_ids = [str(instance.get("ledger_id", "")) for _, instance in ledgers]
    for duplicate in sorted(duplicate_values(ledger_ids)):
        errors.append(f"claim ledgers: duplicate ledger_id {duplicate}")
    global_claim_ids: list[str] = []
    for relative, ledger in ledgers:
        claim_ids = [str(claim.get("claim_id", "")) for claim in ledger.get("claims", [])]
        global_claim_ids.extend(claim_ids)
        for duplicate in sorted(duplicate_values(claim_ids)):
            errors.append(f"{relative}: duplicate claim_id {duplicate}")
        for claim in ledger.get("claims", []):
            for graph_ref in claim.get("knowledge_graph_refs", []):
                if graph_ref not in graph_ref_set:
                    errors.append(f"{relative}: unresolved knowledge_graph_ref {graph_ref}")
            errors.extend(
                foundational_profile_errors(
                    claim, f"{relative}:{claim.get('claim_id', '<unknown>')}"
                )
            )
    for duplicate in sorted(duplicate_values(global_claim_ids)):
        errors.append(f"claim ledgers: duplicate global claim_id {duplicate}")
    return errors


def validate_documents(
    source_registry: dict[str, Any],
    graph: dict[str, Any] | list[dict[str, Any]],
    mappings: dict[str, Any] | list[dict[str, Any]],
    domain_registry: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    sources = source_registry.get("sources", [])
    source_ids = {source["source_id"] for source in sources}
    source_by_id = {source["source_id"]: source for source in sources}
    if len(source_ids) != len(sources):
        errors.append("source registry contains duplicate source_id values")
    normative_sources = [
        source for source in sources if source.get("role") == "NORMATIVE_SUBJECT_SPINE"
    ]
    if len(normative_sources) != 1:
        errors.append(
            f"source registry requires exactly one normative subject spine; found {len(normative_sources)}"
        )
    for source in sources:
        if (
            source.get("role") == "MACHINE_SERIALIZATION_CANDIDATE"
            and source.get("runtime_authority") is not False
        ):
            errors.append(
                f"{source.get('source_id')}: unqualified machine serialization candidate cannot have runtime authority"
            )

    graphs = graph if isinstance(graph, list) else [graph]
    mapping_sets = mappings if isinstance(mappings, list) else [mappings]
    nodes = [node for graph_doc in graphs for node in graph_doc.get("nodes", [])]
    edges = [edge for graph_doc in graphs for edge in graph_doc.get("edges", [])]
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

    mapping_set_ids = [item.get("mapping_set_id", "") for item in mapping_sets]
    for duplicate in sorted(duplicate_values(mapping_set_ids)):
        errors.append(f"duplicate mapping_set_id: {duplicate}")
    mapping_set_domains = [item.get("domain_id", "") for item in mapping_sets]
    for duplicate in sorted(duplicate_values(mapping_set_domains)):
        errors.append(f"multiple mapping sets registered for domain_id: {duplicate}")

    mapping_items = [
        mapping
        for mapping_set in mapping_sets
        for mapping in mapping_set.get("mappings", [])
    ]
    mapping_ids = [mapping.get("mapping_id", "") for mapping in mapping_items]
    for duplicate in sorted(duplicate_values(mapping_ids)):
        errors.append(f"duplicate mapping_id: {duplicate}")
    mapping_id_set = set(mapping_ids)
    mapping_by_id = {mapping.get("mapping_id", ""): mapping for mapping in mapping_items}
    mapping_set_by_mapping_id = {
        mapping.get("mapping_id", ""): mapping_set
        for mapping_set in mapping_sets
        for mapping in mapping_set.get("mappings", [])
    }
    for mapping in mapping_items:
        mapping_id = mapping.get("mapping_id", "<unknown>")
        target_type = mapping.get("target_type")
        internal_ref = mapping.get("internal_ref")
        mapping_domain_id = mapping_set_by_mapping_id.get(mapping_id, {}).get("domain_id")
        if target_type == "GRAPH_NODE" and internal_ref not in node_id_set:
            errors.append(f"{mapping_id}: unresolved graph-node internal_ref {internal_ref!r}")
        if target_type == "DOMAIN" and internal_ref != mapping_domain_id:
            errors.append(
                f"{mapping_id}: domain target {internal_ref!r} does not match mapping-set domain {mapping_domain_id!r}"
            )
        source_id = mapping.get("provenance", {}).get("source_id")
        if source_id not in source_ids:
            errors.append(f"{mapping_id}: unknown provenance source_id {source_id}")
        source = source_by_id.get(source_id, {})
        source_artifact_id = mapping.get("provenance", {}).get("source_artifact_id")
        if source.get("artifact_id") and source_artifact_id != source.get("artifact_id"):
            errors.append(
                f"{mapping_id}: source_artifact_id {source_artifact_id!r} does not match registered artifact {source.get('artifact_id')!r}"
            )
        if not mapping.get("scheme_version"):
            errors.append(f"{mapping_id}: unversioned mapping")
        if (
            mapping.get("provenance", {}).get("assignment_method") == "PROVIDER_AUTOMATED"
            and mapping.get("review_status") == "AUDITED"
        ):
            errors.append(f"{mapping_id}: provider-automated mapping cannot be AUDITED")
        if mapping.get("scheme") == "MSC":
            if (
                source.get("role") != "NORMATIVE_SUBJECT_SPINE"
                or source.get("qualification_status") != "QUALIFIED_NORMATIVE_REFERENCE"
                or source.get("runtime_authority") is not True
            ):
                errors.append(
                    f"{mapping_id}: MSC mapping must cite the qualified normative subject source"
                )
            if mapping.get("scheme_version") != "2020":
                errors.append(f"{mapping_id}: MSC mapping must use scheme version 2020")
            if not MSC_CODE.fullmatch(str(mapping.get("identifier", ""))):
                errors.append(f"{mapping_id}: invalid MSC code {mapping.get('identifier')!r}")

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
            elif mapping_set_by_mapping_id[mapping_ref].get("domain_id") != domain_id:
                errors.append(
                    f"{domain_id}: classification_mapping_ref {mapping_ref} belongs to "
                    f"{mapping_set_by_mapping_id[mapping_ref].get('domain_id')}"
                )
        domain_mapping_items = [
            mapping_by_id[ref]
            for ref in domain.get("classification_mapping_refs", [])
            if ref in mapping_by_id
        ]
        primary_msc = [
            mapping
            for mapping in domain_mapping_items
            if mapping.get("scheme") == "MSC"
            and mapping.get("role") == "PRIMARY_SUBJECT"
            and mapping.get("review_status") not in {"REJECTED", "SUPERSEDED"}
        ]
        waiver = domain.get("classification_waiver")
        if domain.get("status") == "ACTIVE":
            if waiver and domain_mapping_items:
                errors.append(f"{domain_id}: active domain cannot use mappings and a classification waiver together")
            if not waiver and len(primary_msc) != 1:
                errors.append(
                    f"{domain_id}: active domain requires exactly one primary MSC mapping or waiver; found {len(primary_msc)}"
                )
            if waiver:
                if waiver.get("next_review", "") > waiver.get("expires_at", ""):
                    errors.append(f"{domain_id}: classification waiver review occurs after expiry")
            for mapping in primary_msc:
                mapping_set = mapping_set_by_mapping_id[mapping["mapping_id"]]
                if (
                    mapping_set.get("mapping_set_status") == "QUALIFIED"
                    and mapping.get("review_status") != "AUDITED"
                ):
                    errors.append(
                        f"{mapping['mapping_id']}: qualified primary mapping must be AUDITED"
                    )
                if (
                    mapping_set.get("mapping_set_status") == "CANDIDATE"
                    and mapping.get("review_status") != "PROPOSED"
                ):
                    errors.append(
                        f"{mapping['mapping_id']}: candidate primary mapping must remain PROPOSED pending independent review"
                    )

    for mapping_set in mapping_sets:
        if mapping_set.get("domain_id") not in domain_ids:
            errors.append(
                f"{mapping_set.get('mapping_set_id', '<unknown>')}: unresolved domain_id "
                f"{mapping_set.get('domain_id')!r}"
            )

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
        ("examples/candidate_problem_union_closed.json", "candidate_problem.schema.json"),
    ]
    errors: list[str] = []
    loaded: dict[str, Any] = {}
    for relative_path, schema_name in documents:
        instance = load_json(ROOT / relative_path)
        loaded[relative_path] = instance
        errors.extend(
            f"{relative_path}: {error}"
            for error in schema_errors(instance, schema_name)
        )

    graph_documents: list[dict[str, Any]] = []
    for graph_path in sorted((ROOT / "knowledge_graph").glob("*.json")):
        relative_path = graph_path.relative_to(ROOT).as_posix()
        instance = load_json(graph_path)
        graph_documents.append(instance)
        errors.extend(
            f"{relative_path}: {error}"
            for error in schema_errors(instance, "knowledge_graph.schema.json")
        )

    mapping_documents: list[dict[str, Any]] = []
    for mapping_path in sorted((ROOT / "classification" / "mappings").glob("*.json")):
        relative_path = mapping_path.relative_to(ROOT).as_posix()
        instance = load_json(mapping_path)
        mapping_documents.append(instance)
        errors.extend(
            f"{relative_path}: {error}"
            for error in schema_errors(instance, "external_mapping.schema.json")
        )

    domain_registry = yaml.safe_load(
        (ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8")
    )
    errors.extend(
        f"DOMAIN_REGISTRY.yaml: {error}"
        for error in schema_errors(domain_registry, "domain_registry.schema.json")
    )

    agent_review_template = yaml.safe_load(
        (ROOT / "templates/agent_review.yaml").read_text(encoding="utf-8")
    )
    errors.extend(
        f"templates/agent_review.yaml: {error}"
        for error in schema_errors(agent_review_template, "agent_review.schema.json")
    )

    errors.extend(schema_bound_review_registry_errors(SCHEMA_BOUND_AGENT_REVIEWS))
    for relative in SCHEMA_BOUND_AGENT_REVIEWS:
        review_path = ROOT / relative
        if not review_path.is_file():
            continue
        review = yaml.safe_load(review_path.read_text(encoding="utf-8"))
        errors.extend(
            f"{relative}: {error}"
            for error in schema_errors(review, "agent_review.schema.json")
        )
        errors.extend(agent_review_semantic_errors(review, relative))

    errors.extend(claim_ledger_registry_errors(SCHEMA_BOUND_CLAIM_LEDGERS))
    graph_ref_set = {
        node["node_id"] for graph_doc in graph_documents for node in graph_doc["nodes"]
    }
    ledgers: list[tuple[str, dict[str, Any]]] = []
    for relative in SCHEMA_BOUND_CLAIM_LEDGERS:
        ledger_path = ROOT / relative
        if not ledger_path.is_file():
            continue
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
        ledgers.append((relative, ledger))
        errors.extend(
            f"{relative}: {error}"
            for error in schema_errors(ledger, "claim_ledger.schema.json")
        )
    errors.extend(claim_ledger_semantic_errors(ledgers, graph_ref_set))

    for schema_path in sorted((ROOT / "schemas").glob("*.json")):
        Draft202012Validator.check_schema(load_json(schema_path))

    errors.extend(
        validate_documents(
            loaded["classification/source_registry.json"],
            graph_documents,
            mapping_documents,
            domain_registry,
            [loaded["examples/candidate_problem_union_closed.json"]],
        )
    )
    errors.extend(documentary_contract_errors())
    errors.extend(openai_ten_proofs_intake_errors())

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"programme validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "programme classification, discovery, foundation, schema-bound review, "
        "claim-ledger, and documentary contracts are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
