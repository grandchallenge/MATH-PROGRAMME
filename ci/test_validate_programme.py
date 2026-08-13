#!/usr/bin/env python3
"""Regression tests for programme graph, review, ledger, and documentary rejection paths."""

from __future__ import annotations

import copy

import yaml

from test_validate_documentaries import run_rejection_tests as run_documentary_rejection_tests
from validate_programme import (
    ROOT,
    SCHEMA_BOUND_AGENT_REVIEWS,
    SCHEMA_BOUND_CLAIM_LEDGERS,
    agent_review_semantic_errors,
    claim_ledger_registry_errors,
    claim_ledger_semantic_errors,
    discovered_canonical_claim_ledgers,
    discovered_schema_bound_reviews,
    load_json,
    schema_bound_review_registry_errors,
    schema_errors,
    validate_documents,
)


def main() -> int:
    source_registry = load_json(ROOT / "classification/source_registry.json")
    graph = load_json(ROOT / "knowledge_graph/union_closed.json")
    mappings = load_json(ROOT / "classification/mappings/union_closed.json")
    domains = yaml.safe_load((ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    candidate = load_json(ROOT / "examples/candidate_problem_union_closed.json")
    agent_review = yaml.safe_load(
        (ROOT / "templates/agent_review.yaml").read_text(encoding="utf-8")
    )

    duplicate_graph = copy.deepcopy(graph)
    duplicate_graph["nodes"].append(copy.deepcopy(duplicate_graph["nodes"][0]))
    assert any(
        "duplicate graph node_id" in error
        for error in validate_documents(
            source_registry, duplicate_graph, mappings, domains, [candidate]
        )
    )

    dangling_graph = copy.deepcopy(graph)
    dangling_graph["edges"][0]["target"] = "UC-MISSING"
    assert any(
        "dangling target" in error
        for error in validate_documents(
            source_registry, dangling_graph, mappings, domains, [candidate]
        )
    )

    multiple_primary = copy.deepcopy(mappings)
    second_primary = copy.deepcopy(multiple_primary["mappings"][1])
    second_primary["mapping_id"] = "UC-MAP-MSC-06A12-PRIMARY"
    second_primary["role"] = "PRIMARY_SUBJECT"
    multiple_primary["mappings"].append(second_primary)
    multiple_primary_domains = copy.deepcopy(domains)
    multiple_primary_domains["domains"][0]["classification_mapping_refs"].append(
        second_primary["mapping_id"]
    )
    assert any(
        "requires exactly one primary MSC mapping" in error
        for error in validate_documents(
            source_registry, graph, multiple_primary, multiple_primary_domains, [candidate]
        )
    )

    unaudited_primary = copy.deepcopy(mappings)
    unaudited_primary["mappings"][0]["review_status"] = "PROPOSED"
    assert any(
        "qualified primary mapping must be AUDITED" in error
        for error in validate_documents(
            source_registry, graph, unaudited_primary, domains, [candidate]
        )
    )

    automated_audited = copy.deepcopy(mappings)
    automated_audited["mappings"][0]["provenance"]["assignment_method"] = "PROVIDER_AUTOMATED"
    assert any(
        "provider-automated mapping cannot be AUDITED" in error
        for error in validate_documents(
            source_registry, graph, automated_audited, domains, [candidate]
        )
    )

    unqualified_normative_source = copy.deepcopy(source_registry)
    for source in unqualified_normative_source["sources"]:
        if source["source_id"] == "msc2020_normative":
            source["qualification_status"] = "UNQUALIFIED_CANDIDATE"
    assert any(
        "must cite the qualified normative subject source" in error
        for error in validate_documents(
            unqualified_normative_source, graph, mappings, domains, [candidate]
        )
    )

    missing_primary = copy.deepcopy(mappings)
    missing_primary["mappings"][0]["role"] = "SECONDARY_SUBJECT"
    assert any(
        "requires exactly one primary MSC mapping" in error
        for error in validate_documents(
            source_registry, graph, missing_primary, domains, [candidate]
        )
    )

    waiver_conflict_domains = copy.deepcopy(domains)
    waiver_conflict_domains["domains"][0]["classification_waiver"] = {
        "waiver_id": "UC-MAP-WAIVER-001",
        "owner": "Human Steward",
        "rationale": "Synthetic waiver used to exercise the mutual-exclusion gate.",
        "compensating_control": "Retain visible unresolved state until a mapping is independently reviewed.",
        "expires_at": "2026-12-31",
        "next_review": "2026-10-01",
    }
    assert any(
        "cannot use mappings and a classification waiver together" in error
        for error in validate_documents(
            source_registry, graph, mappings, waiver_conflict_domains, [candidate]
        )
    )

    wrong_domain_mappings = copy.deepcopy(mappings)
    wrong_domain_mappings["mappings"][0]["target_type"] = "DOMAIN"
    wrong_domain_mappings["mappings"][0]["internal_ref"] = "RH"
    assert any(
        "does not match mapping-set domain" in error
        for error in validate_documents(
            source_registry, graph, wrong_domain_mappings, domains, [candidate]
        )
    )

    invalid_profile = copy.deepcopy(candidate)
    invalid_profile["foundational_profile"] = {"carrier_type": "bare_set"}
    assert any(
        "foundational_profile" in error
        for error in validate_documents(
            source_registry, graph, mappings, domains, [invalid_profile]
        )
    )

    assert not schema_errors(agent_review, "agent_review.schema.json")
    missing_verifier = copy.deepcopy(agent_review)
    missing_verifier["council_review"].pop("Verifier")
    assert any(
        "Verifier" in error and "required property" in error
        for error in schema_errors(missing_verifier, "agent_review.schema.json")
    )

    invalid_status = copy.deepcopy(agent_review)
    invalid_status["council_review"]["Verifier"]["status"] = "approved"
    assert any(
        "approved" in error
        for error in schema_errors(invalid_status, "agent_review.schema.json")
    )

    integrated_promotion = copy.deepcopy(agent_review)
    integrated_promotion["promotion"]["ready_for_next_stage"] = True
    integrated_promotion["amanuensis_control"]["artifact_ledger"] = {
        "ledger_ref": "docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md",
        "entry_id": "TEST-ARTIFACT",
    }
    integrated_promotion["amanuensis_control"]["review_provenance"]["complete"] = True
    integrated_promotion["amanuensis_control"]["cross_document_consistency"][
        "status"
    ] = "reviewed"
    integrated_promotion["amanuensis_control"]["final_editorial_integration"] = {
        "status": "reviewed",
        "integrated_artifact_ref": "tests/test_validate_programme.py",
        "integration_notes": [],
    }
    assert not schema_errors(integrated_promotion, "agent_review.schema.json")

    pending_referee = copy.deepcopy(integrated_promotion)
    pending_referee["council_review"]["Referee"]["status"] = "pending"
    assert any(
        "promotion requires Referee status reviewed" in error
        for error in agent_review_semantic_errors(pending_referee, "TEST-ARTIFACT")
    )

    blocking_obligation = copy.deepcopy(integrated_promotion)
    blocking_obligation["unresolved_obligations"].append(
        {
            "id": "TEST-BLOCKER",
            "owner": "Adversary",
            "description": "Synthetic blocking obligation.",
            "severity": "critical",
            "blocking": True,
        }
    )
    assert any(
        "blocking obligation TEST-BLOCKER" in error
        for error in agent_review_semantic_errors(blocking_obligation, "TEST-ARTIFACT")
    )

    assert SCHEMA_BOUND_AGENT_REVIEWS == (
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
    discovered_reviews = discovered_schema_bound_reviews()
    assert not schema_bound_review_registry_errors(SCHEMA_BOUND_AGENT_REVIEWS)
    omitted_review_registry = tuple(
        path
        for path in SCHEMA_BOUND_AGENT_REVIEWS
        if path != "reviews/yang_mills/YM-WP02.agent_review.yaml"
    )
    assert any(
        "discovered schema-bound review is unregistered" in error
        for error in schema_bound_review_registry_errors(
            omitted_review_registry,
            discovered_paths=discovered_reviews,
        )
    )
    synthetic_review_discovery = set(discovered_reviews)
    synthetic_review_discovery.add("reviews/union_closed/OMITTED.agent_review.yaml")
    assert any(
        "OMITTED.agent_review.yaml" in error
        for error in schema_bound_review_registry_errors(
            SCHEMA_BOUND_AGENT_REVIEWS,
            discovered_paths=synthetic_review_discovery,
        )
    )
    assert any(
        "duplicate schema-bound review registration" in error
        for error in schema_bound_review_registry_errors(
            (SCHEMA_BOUND_AGENT_REVIEWS[0], SCHEMA_BOUND_AGENT_REVIEWS[0]),
            discovered_paths={SCHEMA_BOUND_AGENT_REVIEWS[0]},
        )
    )

    for relative in SCHEMA_BOUND_AGENT_REVIEWS:
        review = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
        assert not schema_errors(review, "agent_review.schema.json"), relative
        assert not agent_review_semantic_errors(review, relative), relative

    assert SCHEMA_BOUND_CLAIM_LEDGERS == (
        "templates/claim_ledger_template.yaml",
        "templates/union_closed_claim_ledger_wp01.yaml",
        "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/10_CLAIM_LEDGER.yaml",
        "campaigns/yang_mills/WP01_FALSE_PROOF_ATLAS/10_CLAIM_LEDGER.yaml",
        "campaigns/yang_mills/WP02_THEOREM_LEDGER/10_CLAIM_LEDGER.yaml",
    )
    discovered_ledgers = discovered_canonical_claim_ledgers()
    assert not claim_ledger_registry_errors(SCHEMA_BOUND_CLAIM_LEDGERS)
    omitted_ledger_registry = tuple(
        path
        for path in SCHEMA_BOUND_CLAIM_LEDGERS
        if path != "campaigns/yang_mills/WP02_THEOREM_LEDGER/10_CLAIM_LEDGER.yaml"
    )
    assert any(
        "discovered canonical ledger is unregistered" in error
        for error in claim_ledger_registry_errors(
            omitted_ledger_registry,
            discovered_paths=discovered_ledgers,
        )
    )
    incomplete_ledger_discovery = set(discovered_ledgers)
    incomplete_ledger_discovery.remove("templates/claim_ledger_template.yaml")
    assert any(
        "registered canonical ledger is missing" in error
        for error in claim_ledger_registry_errors(
            SCHEMA_BOUND_CLAIM_LEDGERS,
            discovered_paths=incomplete_ledger_discovery,
        )
    )
    synthetic_ledger_discovery = set(discovered_ledgers)
    synthetic_ledger_discovery.add("campaigns/example/10_CLAIM_LEDGER.yaml")
    assert any(
        "campaigns/example/10_CLAIM_LEDGER.yaml" in error
        for error in claim_ledger_registry_errors(
            SCHEMA_BOUND_CLAIM_LEDGERS,
            discovered_paths=synthetic_ledger_discovery,
        )
    )

    ledgers = []
    for relative in SCHEMA_BOUND_CLAIM_LEDGERS:
        ledger = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
        assert not schema_errors(ledger, "claim_ledger.schema.json"), relative
        ledgers.append((relative, ledger))

    graph_refs = {node["node_id"] for node in graph["nodes"]}
    assert not claim_ledger_semantic_errors(ledgers, graph_refs)

    malformed_ledger = copy.deepcopy(ledgers[0][1])
    malformed_ledger["claims"][0].pop("support_summary")
    assert any(
        "support_summary" in error
        for error in schema_errors(malformed_ledger, "claim_ledger.schema.json")
    )

    duplicate_claim_ledger = copy.deepcopy(ledgers[2][1])
    duplicate_claim_ledger["claims"][1]["claim_id"] = duplicate_claim_ledger["claims"][
        0
    ]["claim_id"]
    assert any(
        "duplicate claim_id" in error
        for error in claim_ledger_semantic_errors(
            [(ledgers[2][0], duplicate_claim_ledger)],
            graph_refs,
        )
    )

    duplicate_ledger_id = copy.deepcopy(ledgers[1][1])
    duplicate_ledger_id["ledger_id"] = ledgers[0][1]["ledger_id"]
    assert any(
        "duplicate ledger_id" in error
        for error in claim_ledger_semantic_errors(
            [ledgers[0], (ledgers[1][0], duplicate_ledger_id)],
            graph_refs,
        )
    )

    run_documentary_rejection_tests()
    print("programme, review, claim-ledger, and documentary rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
