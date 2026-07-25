#!/usr/bin/env python3
"""Regression tests for programme graph, mapping, profile, and Agent Council rejection paths."""
from __future__ import annotations

import copy

from validate_programme import (
    ROOT,
    agent_review_semantic_errors,
    load_json,
    schema_errors,
    validate_documents,
)


def fixtures():
    source_registry = load_json(ROOT / "classification" / "source_registry.json")
    graph = load_json(ROOT / "knowledge_graph" / "union_closed.json")
    mappings = load_json(ROOT / "classification" / "mappings" / "union_closed.json")
    import yaml

    domains = yaml.safe_load((ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    candidate = load_json(ROOT / "examples" / "candidate_problem_union_closed.json")
    agent_review = yaml.safe_load((ROOT / "templates" / "agent_review.yaml").read_text(encoding="utf-8"))
    governed_review = yaml.safe_load(
        (ROOT / "reviews" / "union_closed" / "UC-WP01.agent_review.yaml").read_text(
            encoding="utf-8"
        )
    )
    return source_registry, graph, mappings, domains, [candidate], agent_review, governed_review


def main() -> int:
    (
        source_registry,
        graph,
        mappings,
        domains,
        candidates,
        agent_review,
        governed_review,
    ) = fixtures()

    duplicate_graph = copy.deepcopy(graph)
    duplicate_graph["nodes"].append(copy.deepcopy(duplicate_graph["nodes"][0]))
    assert any(
        "duplicate graph node_id" in error
        for error in validate_documents(
            source_registry, duplicate_graph, mappings, domains, candidates
        )
    )

    dangling_graph = copy.deepcopy(graph)
    dangling_graph["edges"][0]["target"] = "UC-MISSING"
    assert any(
        "dangling target" in error
        for error in validate_documents(
            source_registry,
            graph=dangling_graph,
            mappings=mappings,
            domain_registry=domains,
            candidates=candidates,
        )
    )

    multiple_primary = copy.deepcopy(mappings)
    second_primary = copy.deepcopy(multiple_primary["mappings"][1])
    second_primary["mapping_id"] = "UC-MAP-MSC-06A12-PRIMARY"
    second_primary["role"] = "PRIMARY"
    multiple_primary["mappings"].append(second_primary)
    assert any(
        "multiple primary MSC mappings" in error
        for error in validate_documents(
            source_registry, graph, multiple_primary, domains, candidates
        )
    )

    unaudited_primary = copy.deepcopy(mappings)
    unaudited_primary["mappings"][0]["review_status"] = "PROPOSED"
    assert any(
        "primary mapping must be AUDITED" in error
        for error in validate_documents(
            source_registry, graph, unaudited_primary, domains, candidates
        )
    )

    invalid_profile_candidates = copy.deepcopy(candidates)
    invalid_profile_candidates[0]["foundational_profile"] = {"carrier_type": "bare_set"}
    assert any(
        "foundational_profile" in error
        for error in validate_documents(
            source_registry, graph, mappings, domains, invalid_profile_candidates
        )
    )

    assert not schema_errors(agent_review, "agent_review.schema.json")

    missing_agent_review = copy.deepcopy(agent_review)
    missing_agent_review["council_review"].pop("Verifier")
    assert any(
        "Verifier" in error and "required property" in error
        for error in schema_errors(missing_agent_review, "agent_review.schema.json")
    )

    missing_amanuensis_review = copy.deepcopy(agent_review)
    missing_amanuensis_review["council_review"].pop("Amanuensis")
    assert any(
        "Amanuensis" in error and "required property" in error
        for error in schema_errors(missing_amanuensis_review, "agent_review.schema.json")
    )

    missing_amanuensis_control = copy.deepcopy(agent_review)
    missing_amanuensis_control.pop("amanuensis_control")
    assert any(
        "amanuensis_control" in error and "required property" in error
        for error in schema_errors(missing_amanuensis_control, "agent_review.schema.json")
    )

    invalid_status_review = copy.deepcopy(agent_review)
    invalid_status_review["council_review"]["Verifier"]["status"] = "approved"
    assert any(
        "approved" in error
        for error in schema_errors(invalid_status_review, "agent_review.schema.json")
    )

    premature_promotion = copy.deepcopy(agent_review)
    premature_promotion["promotion"]["ready_for_next_stage"] = True
    assert any(
        "amanuensis_control" in error
        for error in schema_errors(premature_promotion, "agent_review.schema.json")
    )

    integrated_promotion = copy.deepcopy(agent_review)
    integrated_promotion["promotion"]["ready_for_next_stage"] = True
    integrated_promotion["amanuensis_control"]["artifact_ledger"] = {
        "ledger_ref": "docs/ARTIFACT_LEDGER.md",
        "entry_id": "WPXX_DOMAIN_000X",
    }
    integrated_promotion["amanuensis_control"]["review_provenance"]["complete"] = True
    integrated_promotion["amanuensis_control"]["cross_document_consistency"]["status"] = "reviewed"
    integrated_promotion["amanuensis_control"]["final_editorial_integration"] = {
        "status": "reviewed",
        "integrated_artifact_ref": "work_packages/WPXX_DOMAIN_000X.md",
        "integration_notes": [],
    }
    assert not schema_errors(integrated_promotion, "agent_review.schema.json")

    assert not schema_errors(governed_review, "agent_review.schema.json")
    assert not agent_review_semantic_errors(governed_review, "UC-WP01")

    pending_verifier = copy.deepcopy(governed_review)
    pending_verifier["council_review"]["Verifier"]["status"] = "pending"
    assert any(
        "promotion requires Verifier status reviewed" in error
        for error in agent_review_semantic_errors(pending_verifier, "UC-WP01")
    )

    blocking_obligation = copy.deepcopy(governed_review)
    blocking_obligation["unresolved_obligations"].append(
        {
            "id": "UC-WP01-TEST-BLOCKER",
            "owner": "Adversary",
            "description": "Synthetic blocking obligation for rejection testing.",
            "severity": "critical",
            "blocking": True,
        }
    )
    assert any(
        "blocking obligation UC-WP01-TEST-BLOCKER" in error
        for error in agent_review_semantic_errors(blocking_obligation, "UC-WP01")
    )

    blocked_agent = copy.deepcopy(governed_review)
    blocked_agent["council_review"]["Experimentalist"]["status"] = "blocked"
    assert any(
        "Experimentalist is blocked" in error
        for error in agent_review_semantic_errors(blocked_agent, "UC-WP01")
    )

    print("programme validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
