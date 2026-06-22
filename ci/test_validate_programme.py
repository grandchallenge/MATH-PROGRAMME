#!/usr/bin/env python3
"""Regression tests for programme graph, mapping, and profile rejection paths."""
from __future__ import annotations

import copy

from validate_programme import load_json, validate_documents, ROOT


def fixtures():
    source_registry = load_json(ROOT / "classification" / "source_registry.json")
    graph = load_json(ROOT / "knowledge_graph" / "union_closed.json")
    mappings = load_json(ROOT / "classification" / "mappings" / "union_closed.json")
    import yaml

    domains = yaml.safe_load((ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    candidate = load_json(ROOT / "examples" / "candidate_problem_union_closed.json")
    return source_registry, graph, mappings, domains, [candidate]


def main() -> int:
    source_registry, graph, mappings, domains, candidates = fixtures()

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
            source_registry, dangling_graph, mappings, domains, candidates
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

    print("programme validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
