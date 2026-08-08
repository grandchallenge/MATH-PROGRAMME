#!/usr/bin/env python3
"""Deterministic fail-closed runtime validator for CMDG-VALIDATOR-001.

The validator checks manifest-relative admission preconditions and emits a
machine-readable report. Its terminal vocabulary deliberately excludes
GRAPH_CERTIFIED. Derived reachability is diagnostic output only and never
becomes direct semantic authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from validate_cmdg_schema_contracts import (
    ContractError,
    SCHEMAS,
    load_json,
    validate_edge,
    validate_manifest,
    validate_schema,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE = ROOT / "fixtures" / "cmdg" / "validator_001" / "valid_package.json"
PACKAGE_SCHEMA = SCHEMAS / "cmdg_validation_package.schema.json"
REPORT_SCHEMA = SCHEMAS / "cmdg_validator_report.schema.json"
VALIDATOR_VERSION = "1.0.0"
EXPECTED_SCHEMA_VERSIONS = {
    "node": "1.0.0",
    "edge": "1.0.0",
    "manifest": "1.0.0",
    "package": "1.0.0",
    "report": "1.0.0",
}


class RuntimeValidationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def reject(code: str, message: str) -> None:
    raise RuntimeValidationError(code, message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _empty_report(package: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "validator_version": VALIDATOR_VERSION,
        "package_id": package.get("package_id") or "UNKNOWN_PACKAGE",
        "package_digest_sha256": sha256_json(package),
        "manifest_id": "",
        "manifest_version": "",
        "manifest_git_blob_sha1": "",
        "root_node_id": "",
        "authoritative_direct_semantic_edge_ids": [],
        "traversed_direct_semantic_edge_ids": [],
        "derived_reachable_node_ids": [],
        "boundary_exits": [],
        "realization_checks": [],
        "quotient_generator_checks": [],
        "pin_checks": {
            "manifest_identity": "NOT_CHECKED",
            "proof_environment": "NOT_CHECKED",
            "replay": "NOT_CHECKED",
            "implementation_dependencies": "NOT_CHECKED",
        },
        "footprint_summary": {
            "axiom_entries": 0,
            "classicality_entries": 0,
            "boundary_trust_entries": 0,
        },
        "unresolved_obligations": [],
        "rejection_codes": [],
        "terminal_state": "VALIDATOR_REJECTED",
        "claim_boundary": {
            "graph_certified_conferred": False,
            "global_completeness_claim": False,
            "derived_closure_authoritative": False,
        },
    }


def _schema_or_reject(instance: Any, schema_path: Path, label: str) -> None:
    try:
        validate_schema(instance, schema_path, label)
    except ContractError as exc:
        reject("SCHEMA_VIOLATION", str(exc))


def _cross_field_manifest_or_reject(manifest: dict[str, Any]) -> None:
    try:
        validate_manifest(manifest, "runtime_manifest")
    except ContractError as exc:
        reject("MANIFEST_CONTRACT_VIOLATION", str(exc))


def _precheck_versions(package: dict[str, Any], manifest: dict[str, Any]) -> None:
    if package.get("package_schema_version") != "1.0.0":
        reject("SCHEMA_VERSION_DRIFT", "package schema version drift")
    if package.get("required_schema_versions") != EXPECTED_SCHEMA_VERSIONS:
        reject("SCHEMA_VERSION_DRIFT", "required schema-version set drift")
    if manifest.get("schema_version") != "1.0.0" or manifest.get("schema_versions") != {
        "node": "1.0.0", "edge": "1.0.0", "manifest": "1.0.0"
    }:
        reject("SCHEMA_VERSION_DRIFT", "manifest schema-version binding drift")
    for node in package.get("nodes", []):
        if node.get("schema_version") != "1.0.0":
            reject("SCHEMA_VERSION_DRIFT", f"node schema drift: {node.get('node_id', '<unknown>')}")
    for edge in package.get("additional_edges", []):
        if edge.get("schema_version") != "1.0.0":
            reject("SCHEMA_VERSION_DRIFT", f"edge schema drift: {edge.get('edge_id', '<unknown>')}")
    for edge in manifest.get("direct_semantic_edges", []) + manifest.get("realizations", []):
        if edge.get("schema_version") != "1.0.0":
            reject("SCHEMA_VERSION_DRIFT", f"manifest edge schema drift: {edge.get('edge_id', '<unknown>')}")


def _precheck_claim_boundaries(package: dict[str, Any], manifest: dict[str, Any]) -> None:
    if package.get("requested_terminal_state") != "VALIDATOR_ACCEPTED_PRECONDITIONS":
        reject("PROHIBITED_TERMINAL_STATE", "runtime validator cannot request or emit GRAPH_CERTIFIED")
    p_claim = package.get("claim_boundary", {})
    if p_claim.get("graph_certified_conferred") is not False:
        reject("PROHIBITED_TERMINAL_STATE", "package attempts to confer GRAPH_CERTIFIED")
    if p_claim.get("global_completeness_claim") is not False:
        reject("GLOBAL_COMPLETENESS_PROHIBITED", "package attempts a global completeness claim")
    scope = manifest.get("semantic_scope", {})
    if scope.get("global_completeness_claim") is not False:
        reject("GLOBAL_COMPLETENESS_PROHIBITED", "manifest attempts a global completeness claim")
    m_claim = manifest.get("claim_boundary", {})
    if m_claim.get("graph_certified_conferred") is not False:
        reject("PROHIBITED_TERMINAL_STATE", "manifest attempts to confer GRAPH_CERTIFIED")
    if m_claim.get("global_completeness_claim") is not False:
        reject("GLOBAL_COMPLETENESS_PROHIBITED", "manifest claim boundary attempts global completeness")


def _precheck_direct_authority(manifest: dict[str, Any]) -> None:
    allowed = set(manifest.get("closure_policy", {}).get("traversable_semantic_relations", []))
    for edge in manifest.get("direct_semantic_edges", []):
        edge_id = edge.get("edge_id", "<unknown>")
        if edge.get("layer") != "G_semantic":
            reject("SEMANTIC_LAYER_LAUNDERING", f"direct semantic edge {edge_id} is not in G_semantic")
        relation = edge.get("relation")
        if relation in {"IMPLEMENTATION_IMPORT", "TOOLCHAIN_DEPENDENCY", "BUILD_DEPENDENCY", "PROOF_USES_DECLARATION", "PROOF_USES_AXIOM", "PROOF_USES_CLASSICALITY", "PROOF_USES_CERTIFICATE"}:
            reject("SEMANTIC_LAYER_LAUNDERING", f"proof/import relation {relation} presented as semantic authority")
        authority = edge.get("authority_state")
        if authority == "DERIVED":
            reject("DERIVED_DIRECT_AUTHORITY", f"derived edge {edge_id} injected as direct semantic authority")
        if authority != "REVIEWED_DIRECT":
            reject("DIRECT_SEMANTIC_NOT_REVIEWED", f"direct semantic edge {edge_id} lacks reviewed-direct authority")
        if not edge.get("evidence_refs") or not edge.get("review"):
            reject("DIRECT_SEMANTIC_EVIDENCE_MISSING", f"direct semantic edge {edge_id} lacks reviewed evidence")
        proposal = edge.get("proposal_origin", {})
        if proposal.get("origin") in {"SEMANTIC_GRAPH_RECONCILER", "OTHER_TOOL"}:
            if edge.get("review", {}).get("independent_of_proposal_origin") is not True:
                reject("TOOL_PROPOSAL_NOT_INDEPENDENT", f"tool-origin direct edge {edge_id} lacks independent review")
        if relation not in allowed:
            reject("DIRECT_EDGE_OUTSIDE_CLOSURE_POLICY", f"direct semantic relation {relation} is not traversable under the manifest")


def _precheck_realizations(manifest: dict[str, Any]) -> None:
    policy = manifest.get("closure_policy", {})
    realizations = manifest.get("realizations", [])
    if policy.get("realization_crossing") == "DISABLED" and realizations:
        reject("REALIZATION_POLICY_MISMATCH", "manifest disables realization crossing but supplies REALIZES_AS edges")
    for edge in realizations:
        edge_id = edge.get("edge_id", "<unknown>")
        if edge.get("layer") != "CROSS_LAYER" or edge.get("relation") != "REALIZES_AS":
            reject("REALIZATION_POLICY_MISMATCH", f"realization edge {edge_id} is not explicit CROSS_LAYER REALIZES_AS")
        realization = edge.get("realization") or {}
        if not realization.get("evidence_refs") or not realization.get("target_locator"):
            reject("REALIZATION_EVIDENCE_MISSING", f"realization {edge_id} lacks evidence or target locator")
        claims = realization.get("automatic_claims") or {}
        if any(claims.values()):
            reject("REALIZATION_OVERCLAIM", f"realization {edge_id} asserts an automatic stronger claim")
        if edge.get("authority_state") == "REVIEWED_DIRECT":
            proposal = edge.get("proposal_origin", {})
            if proposal.get("origin") in {"SEMANTIC_GRAPH_RECONCILER", "OTHER_TOOL"} and edge.get("review", {}).get("independent_of_proposal_origin") is not True:
                reject("TOOL_PROPOSAL_NOT_INDEPENDENT", f"tool-origin realization {edge_id} lacks independent review")


def _precheck_obligations(manifest: dict[str, Any]) -> None:
    if manifest.get("intent") != "PRODUCTION_INTENT":
        return
    inside = sorted(
        obligation.get("obligation_id", "<unknown>")
        for obligation in manifest.get("unresolved_obligations", [])
        if obligation.get("scope") == "INSIDE_BOUNDARY"
    )
    if inside:
        reject("UNRESOLVED_IN_BOUNDARY", "production intent has unresolved in-boundary obligations: " + ", ".join(inside))


def _all_edges(package: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return list(manifest.get("direct_semantic_edges", [])) + list(manifest.get("realizations", [])) + list(package.get("additional_edges", []))


def _validate_loaded(package: dict[str, Any], manifest: dict[str, Any], manifest_blob_sha: str, report: dict[str, Any]) -> None:
    report["manifest_id"] = str(manifest.get("manifest_id", ""))
    report["manifest_version"] = str(manifest.get("manifest_version", ""))
    report["manifest_git_blob_sha1"] = manifest_blob_sha
    report["root_node_id"] = str(manifest.get("root", {}).get("node_id", ""))

    _precheck_claim_boundaries(package, manifest)
    _precheck_versions(package, manifest)
    _schema_or_reject(package, PACKAGE_SCHEMA, "runtime_package")

    if package["manifest_git_blob_sha1"] != manifest_blob_sha:
        report["pin_checks"]["manifest_identity"] = "MISMATCH"
        reject("MANIFEST_IDENTITY_MISMATCH", "manifest Git blob identity does not match the package pin")
    report["pin_checks"]["manifest_identity"] = "MATCH"

    _precheck_direct_authority(manifest)
    _precheck_realizations(manifest)
    _precheck_obligations(manifest)
    _cross_field_manifest_or_reject(manifest)

    nodes = package["nodes"]
    node_ids = [node["node_id"] for node in nodes]
    duplicate_nodes = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    if duplicate_nodes:
        reject("DUPLICATE_NODE_ID", "duplicate node IDs: " + ", ".join(duplicate_nodes))
    node_by_id = {node["node_id"]: node for node in nodes}

    edges = _all_edges(package, manifest)
    edge_ids = [edge.get("edge_id", "") for edge in edges]
    duplicate_edges = sorted({edge_id for edge_id in edge_ids if edge_ids.count(edge_id) > 1})
    if duplicate_edges:
        reject("DUPLICATE_EDGE_ID", "duplicate edge IDs: " + ", ".join(duplicate_edges))

    for index, edge in enumerate(package["additional_edges"]):
        try:
            validate_edge(edge, f"runtime_package.additional_edges[{index}]")
        except ContractError as exc:
            reject("SCHEMA_VIOLATION", str(exc))
        if edge["layer"] == "G_semantic" and edge["authority_state"] == "REVIEWED_DIRECT":
            reject("UNDECLARED_DIRECT_SEMANTIC_EDGE", f"reviewed semantic edge {edge['edge_id']} is absent from manifest.direct_semantic_edges")

    root_id = manifest["root"]["node_id"]
    if root_id not in node_by_id:
        reject("ROOT_NODE_MISSING", f"root node {root_id} is absent from package nodes")

    included = set(manifest["semantic_scope"]["included_node_ids"])
    missing_scope_nodes = sorted(included - set(node_by_id))
    if missing_scope_nodes:
        reject("SEMANTIC_SCOPE_NODE_MISSING", "semantic-scope nodes absent from package: " + ", ".join(missing_scope_nodes))
    if root_id not in included:
        reject("ROOT_OUTSIDE_SEMANTIC_SCOPE", f"root {root_id} is not in semantic_scope.included_node_ids")

    boundaries = {boundary["node_id"]: boundary for boundary in manifest["boundaries"]}
    for boundary_id, boundary in boundaries.items():
        if boundary_id not in node_by_id or boundary_id not in included:
            reject("BOUNDARY_NODE_MISSING", f"declared boundary {boundary_id} is not a represented in-scope node")
        if not boundary.get("authority_refs") or not boundary.get("trust_class"):
            reject("BOUNDARY_TRUST_MALFORMED", f"boundary {boundary_id} lacks trust authority")

    for edge in edges:
        for side in ("source", "target"):
            endpoint = edge.get(side, {})
            if endpoint.get("kind") == "SEMANTIC_NODE":
                identity = endpoint.get("identity")
                if identity not in node_by_id:
                    reject("DANGLING_SEMANTIC_ENDPOINT", f"edge {edge.get('edge_id')} has dangling semantic endpoint {identity}")
                if edge in manifest["direct_semantic_edges"] and identity not in included:
                    reject("SEMANTIC_SCOPE_MISSING_ENDPOINT", f"direct semantic edge {edge.get('edge_id')} endpoint {identity} is outside semantic scope")

    authoritative = sorted(edge["edge_id"] for edge in manifest["direct_semantic_edges"])
    report["authoritative_direct_semantic_edge_ids"] = authoritative

    allowed_relations = set(manifest["closure_policy"]["traversable_semantic_relations"])
    by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in manifest["direct_semantic_edges"]:
        if edge["relation"] in allowed_relations:
            by_source[edge["source"]["identity"]].append(edge)
    for source in by_source:
        by_source[source].sort(key=lambda edge: edge["edge_id"])

    reached: set[str] = {root_id}
    traversed: set[str] = set()
    boundary_exits: dict[str, dict[str, Any]] = {}
    queue: deque[str] = deque([root_id])
    while queue:
        node_id = queue.popleft()
        if node_id in boundaries and node_id != root_id:
            boundary = boundaries[node_id]
            if "SEMANTIC" not in boundary["allowed_traversal_purposes"]:
                reject("BOUNDARY_PURPOSE_MISMATCH", f"reached boundary {node_id} does not permit SEMANTIC traversal purpose")
            boundary_exits[node_id] = {
                "node_id": node_id,
                "trust_class": boundary["trust_class"],
                "authority_refs": sorted(boundary["authority_refs"]),
                "allowed_traversal_purposes": sorted(boundary["allowed_traversal_purposes"]),
            }
            if manifest["closure_policy"]["boundary_behavior"] == "TERMINATE_AT_DECLARED_BOUNDARY":
                continue
        for edge in by_source.get(node_id, []):
            traversed.add(edge["edge_id"])
            target = edge["target"]["identity"]
            if target not in included:
                reject("SEMANTIC_SCOPE_MISSING_ENDPOINT", f"closure from {node_id} exits scope at {target}")
            if target not in reached:
                reached.add(target)
                queue.append(target)

    report["traversed_direct_semantic_edge_ids"] = sorted(traversed)
    report["derived_reachable_node_ids"] = sorted(reached)
    report["boundary_exits"] = [boundary_exits[key] for key in sorted(boundary_exits)]

    realization_checks = []
    proof_environment_id = manifest["proof_environment"]["environment_id"]
    for edge in sorted(manifest["realizations"], key=lambda item: item["edge_id"]):
        source_id = edge["source"]["identity"]
        if source_id not in node_by_id or source_id not in included:
            reject("REALIZATION_SOURCE_UNKNOWN", f"realization {edge['edge_id']} has unknown semantic source {source_id}")
        environment_ref = edge["realization"].get("proof_environment_ref")
        if environment_ref is not None and environment_ref != proof_environment_id:
            reject("REALIZATION_ENVIRONMENT_MISMATCH", f"realization {edge['edge_id']} proof environment drift")
        realization_checks.append({
            "edge_id": edge["edge_id"],
            "status": "ACCEPTED",
            "proof_environment_ref": environment_ref,
        })
    report["realization_checks"] = realization_checks

    direct_by_id = {edge["edge_id"]: edge for edge in manifest["direct_semantic_edges"]}
    quotient_checks = []
    quotient = manifest["quotient_projection"]
    if quotient["enabled"]:
        for edge_id in sorted(quotient["generator_edge_ids"]):
            edge = direct_by_id.get(edge_id)
            if edge is None:
                reject("QUOTIENT_GENERATOR_UNKNOWN", f"quotient generator {edge_id} is not a declared direct semantic edge")
            equivalence = edge.get("equivalence") or {}
            if edge.get("relation") != "EQUIVALENT_TO" or edge.get("authority_state") != "REVIEWED_DIRECT" or equivalence.get("quotient_admissibility") != "CERTIFIED_GENERATOR" or not equivalence.get("certification_ref"):
                reject("QUOTIENT_GENERATOR_NOT_CERTIFIED", f"quotient generator {edge_id} is not certified admissible")
            quotient_checks.append({
                "edge_id": edge_id,
                "status": "ACCEPTED",
                "certification_ref": equivalence["certification_ref"],
            })
    elif quotient["generator_edge_ids"]:
        reject("QUOTIENT_POLICY_MISMATCH", "disabled quotient projection carries generator IDs")
    report["quotient_generator_checks"] = quotient_checks

    retained = package["retained_evidence"]
    if retained["proof_environment"] != manifest["proof_environment"]:
        report["pin_checks"]["proof_environment"] = "MISMATCH"
        reject("STALE_PROOF_ENVIRONMENT_PIN", "retained proof environment differs from manifest proof_environment")
    report["pin_checks"]["proof_environment"] = "MATCH"

    replay_expected = {
        "route_id": manifest["replay"]["route_id"],
        "exact_environment_ref": manifest["replay"]["exact_environment_ref"],
        "command": manifest["replay"]["command"],
        "artifact_refs": manifest["replay"]["artifact_refs"],
    }
    if retained["replay"] != replay_expected:
        report["pin_checks"]["replay"] = "MISMATCH"
        reject("REPLAY_EVIDENCE_MISMATCH", "retained replay identity differs from manifest replay binding")
    report["pin_checks"]["replay"] = "MATCH"

    expected_impl = {dep["dependency_id"]: dep["pin"] for dep in manifest["implementation_dependencies"]}
    if retained["implementation_pins"] != expected_impl:
        report["pin_checks"]["implementation_dependencies"] = "MISMATCH"
        reject("IMPLEMENTATION_PIN_MISMATCH", "retained implementation pins differ from manifest dependencies")
    report["pin_checks"]["implementation_dependencies"] = "MATCH"

    boundary_ids = set(boundaries)
    for footprint_name in ("axiom_footprint", "classicality_footprint"):
        for boundary_id in manifest[footprint_name]["boundary_trust"]:
            if boundary_id not in boundary_ids:
                reject("FOOTPRINT_BOUNDARY_TRUST_UNKNOWN", f"{footprint_name} references undeclared boundary {boundary_id}")

    footprint_keys = ["operational_substrate", "imported_formal_declarations", "root_proof", "object_theory_assumptions", "boundary_trust"]
    report["footprint_summary"] = {
        "axiom_entries": sum(len(manifest["axiom_footprint"][key]) for key in footprint_keys),
        "classicality_entries": sum(len(manifest["classicality_footprint"][key]) for key in footprint_keys),
        "boundary_trust_entries": len(manifest["axiom_footprint"]["boundary_trust"]) + len(manifest["classicality_footprint"]["boundary_trust"]),
    }
    report["unresolved_obligations"] = sorted(obligation["obligation_id"] for obligation in manifest["unresolved_obligations"])
    report["terminal_state"] = "VALIDATOR_ACCEPTED_PRECONDITIONS"


def validate_loaded_package(package: dict[str, Any], manifest: dict[str, Any], manifest_blob_sha: str) -> dict[str, Any]:
    """Validate already-loaded objects; used by retained mutation tests."""
    package_copy = copy.deepcopy(package)
    manifest_copy = copy.deepcopy(manifest)
    report = _empty_report(package_copy)
    try:
        _validate_loaded(package_copy, manifest_copy, manifest_blob_sha, report)
    except RuntimeValidationError as exc:
        report["terminal_state"] = "VALIDATOR_REJECTED"
        report["rejection_codes"] = [exc.code]
    _schema_or_reject(report, REPORT_SCHEMA, "validator_report")
    return report


def load_package_and_manifest(package_path: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    package = load_json(package_path)
    manifest_path_value = package.get("manifest_path")
    if not isinstance(manifest_path_value, str) or not manifest_path_value:
        reject("MANIFEST_PATH_INVALID", "package has no valid manifest_path")
    manifest_path = (ROOT / manifest_path_value).resolve()
    try:
        manifest_path.relative_to(ROOT.resolve())
    except ValueError:
        reject("MANIFEST_PATH_INVALID", "manifest_path escapes repository root")
    try:
        raw = manifest_path.read_bytes()
        manifest = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        reject("MANIFEST_LOAD_FAILED", f"cannot load manifest: {exc}")
    return package, manifest, git_blob_sha1(raw)


def validate_package_path(package_path: Path) -> dict[str, Any]:
    try:
        package, manifest, manifest_blob_sha = load_package_and_manifest(package_path)
    except RuntimeValidationError as exc:
        package = {"package_id": "UNKNOWN_PACKAGE", "package_path": str(package_path)}
        report = _empty_report(package)
        report["rejection_codes"] = [exc.code]
        _schema_or_reject(report, REPORT_SCHEMA, "validator_report")
        return report
    return validate_loaded_package(package, manifest, manifest_blob_sha)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", nargs="?", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--report", type=Path, help="optional path for deterministic JSON report")
    args = parser.parse_args()

    report = validate_package_path(args.package)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["terminal_state"] == "VALIDATOR_ACCEPTED_PRECONDITIONS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
