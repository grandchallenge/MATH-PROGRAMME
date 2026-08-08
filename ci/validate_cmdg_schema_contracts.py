#!/usr/bin/env python3
"""Validate the bounded CMDG-SCHEMA-001 contracts.

This checker intentionally enforces schema-local and cross-field admission rules only.
Graph traversal, transitive closure, whole-graph completeness, replay execution, and
production GRAPH_CERTIFIED adjudication remain reserved to CMDG-VALIDATOR-001.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
DEFAULT_FIXTURE_DIR = ROOT / "fixtures" / "cmdg" / "schema_001"


class ContractError(ValueError):
    pass


def fail(message: str) -> None:
    raise ContractError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path}: cannot load JSON: {exc}")


def build_registry() -> Registry:
    resources = []
    for path in sorted(SCHEMAS.glob("cmdg_*.schema.json")):
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validate_schema(instance: Any, schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, registry=build_registry())
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        fail(f"{label}: schema violation at {location}: {first.message}")


def validate_edge(edge: dict[str, Any], label: str = "edge") -> None:
    validate_schema(edge, SCHEMAS / "cmdg_edge.schema.json", label)

    layer = edge["layer"]
    relation = edge["relation"]
    authority = edge["authority_state"]

    if layer == "G_semantic" and authority == "REVIEWED_DIRECT":
        require(edge.get("evidence_refs"), f"{label}: reviewed direct semantic edge requires evidence_refs")
        require("review" in edge, f"{label}: reviewed direct semantic edge requires review")

    if authority == "DERIVED":
        require(
            layer != "G_semantic" or relation not in {"IMPLEMENTATION_IMPORT", "PROOF_USES_DECLARATION"},
            f"{label}: derived edge cannot launder proof/import semantics into G_semantic",
        )

    proposal = edge.get("proposal_origin")
    if proposal and proposal["origin"] in {"SEMANTIC_GRAPH_RECONCILER", "OTHER_TOOL"} and authority == "REVIEWED_DIRECT":
        review = edge.get("review", {})
        require(
            review.get("independent_of_proposal_origin") is True,
            f"{label}: tool-origin proposal requires independent review before REVIEWED_DIRECT admission",
        )

    if relation == "REALIZES_AS":
        realization = edge["realization"]
        claims = realization["automatic_claims"]
        require(not any(claims.values()), f"{label}: REALIZES_AS cannot carry automatic stronger claims")

    equivalence = edge.get("equivalence")
    if equivalence and equivalence["quotient_admissibility"] == "CERTIFIED_GENERATOR":
        require(relation == "EQUIVALENT_TO", f"{label}: quotient generator must be EQUIVALENT_TO")
        require(authority == "REVIEWED_DIRECT", f"{label}: quotient generator must be REVIEWED_DIRECT")
        require(bool(equivalence.get("certification_ref")), f"{label}: certified quotient generator requires certification_ref")


def validate_manifest(manifest: dict[str, Any], label: str = "manifest") -> None:
    validate_schema(manifest, SCHEMAS / "cmdg_graph_certification_manifest.schema.json", label)

    require(
        manifest["semantic_scope"]["global_completeness_claim"] is False,
        f"{label}: global completeness claim is prohibited",
    )
    require(
        manifest["claim_boundary"]["graph_certified_conferred"] is False,
        f"{label}: CMDG-SCHEMA-001 cannot confer GRAPH_CERTIFIED",
    )
    require(
        manifest["claim_boundary"]["schema_validation_only"] is True,
        f"{label}: schema package must remain schema-validation only",
    )

    if manifest["intent"] == "PRODUCTION_INTENT":
        root = manifest["root"]
        if root["root_kind"] in {"THEOREM", "CERTIFICATE"}:
            eligible = root["programme_level"] == 5
            if not eligible:
                eligible = (
                    root["replayable_certificate_equivalent"] is True
                    and bool(root.get("equivalence_admission_ref"))
                )
            require(
                eligible,
                f"{label}: production-intent theorem/certificate root requires Level 5 or an admitted replayable-certificate equivalent",
            )

        in_boundary = [
            obligation["obligation_id"]
            for obligation in manifest["unresolved_obligations"]
            if obligation["scope"] == "INSIDE_BOUNDARY"
        ]
        require(
            not in_boundary,
            f"{label}: production intent has unresolved in-boundary obligations: {', '.join(in_boundary)}",
        )

    for index, edge in enumerate(manifest["direct_semantic_edges"]):
        edge_label = f"{label}.direct_semantic_edges[{index}]"
        validate_edge(edge, edge_label)
        require(edge["layer"] == "G_semantic", f"{edge_label}: must be in G_semantic")
        require(edge["authority_state"] == "REVIEWED_DIRECT", f"{edge_label}: must be REVIEWED_DIRECT")
        require(
            "review" in edge and edge.get("evidence_refs"),
            f"{edge_label}: direct semantic authority requires reviewed evidence",
        )

    for index, edge in enumerate(manifest["realizations"]):
        edge_label = f"{label}.realizations[{index}]"
        validate_edge(edge, edge_label)
        require(edge["layer"] == "CROSS_LAYER", f"{edge_label}: realization must be CROSS_LAYER")
        require(edge["relation"] == "REALIZES_AS", f"{edge_label}: realization must use REALIZES_AS")

    proof_environment = manifest["proof_environment"]
    require(proof_environment["pins"], f"{label}: proof environment must be pinned")
    require(
        manifest["replay"]["exact_environment_ref"] == proof_environment["environment_id"],
        f"{label}: replay exact_environment_ref must bind the declared proof environment",
    )

    edge_by_id = {edge["edge_id"]: edge for edge in manifest["direct_semantic_edges"]}
    quotient = manifest["quotient_projection"]
    if quotient["enabled"]:
        require(quotient["generator_edge_ids"], f"{label}: enabled quotient projection requires generator_edge_ids")
        for edge_id in quotient["generator_edge_ids"]:
            require(edge_id in edge_by_id, f"{label}: quotient generator {edge_id} is not a direct semantic edge")
            edge = edge_by_id[edge_id]
            require(edge["relation"] == "EQUIVALENT_TO", f"{label}: quotient generator {edge_id} is not EQUIVALENT_TO")
            equivalence = edge.get("equivalence", {})
            require(
                equivalence.get("quotient_admissibility") == "CERTIFIED_GENERATOR",
                f"{label}: quotient generator {edge_id} is not certified admissible",
            )
            require(
                bool(equivalence.get("certification_ref")),
                f"{label}: quotient generator {edge_id} lacks certification_ref",
            )


def validate_fixture_dir(fixture_dir: Path) -> None:
    node = load_json(fixture_dir / "valid_node.json")
    edge = load_json(fixture_dir / "valid_edge.json")
    manifest = load_json(fixture_dir / "valid_manifest.json")

    validate_schema(node, SCHEMAS / "cmdg_node.schema.json", "valid_node")
    validate_edge(edge, "valid_edge")
    validate_manifest(manifest, "valid_manifest")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "fixture_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_FIXTURE_DIR,
        help="directory containing valid_node.json, valid_edge.json, and valid_manifest.json",
    )
    args = parser.parse_args()

    try:
        validate_fixture_dir(args.fixture_dir)
    except ContractError as exc:
        print(f"CMDG schema contract validation FAILED: {exc}")
        return 1

    print("CMDG schema contract validation PASS")
    print("scope: schema-local and cross-field admission only; no GRAPH_CERTIFIED status conferred")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
