#!/usr/bin/env python3
"""Validate MCORE-DOMAIN-SHADOW-001 against its exact protected source snapshot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/math_core_domain_shadow.schema.json"
ARTIFACT = ROOT / "governance/math_core_domain_shadow_condensed_001.json"
SNAPSHOT = "a501eef7517ec9a3170ee8190a1d856c050da92c"

EXPECTED_SOURCES = {
    "governance/cmdg_condensed_cm1_001.json": "d85305fe900eeb10f3857f82635841a5f175b222",
    "governance/cmdg_condensed_cm2_001.json": "11ceaa9577add91a1fa231cab9f403b5d4df2db0",
    "governance/cmdg_condensed_cm3_001.json": "301bc288ef54288282fa7287696edba621e98327",
    "governance/cmdg_solid_c05_001.json": "76f1e0c34da6e5b3da39045c32043f2c7b766b0d",
    "governance/cmdg_condensed_cm4_001.json": "bde38326e72a7dba3fb65bcd8f7e096c967bd7cd",
    "governance/cmdg_condensed_cm4_p3_001.json": "949ea8cc3abd06dfe8da87f6baca0a200a35a300",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _node_map(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes = doc["nodes"]
    result = {node["node_id"]: node for node in nodes}
    assert len(result) == len(nodes), "shadow node IDs must be unique"
    return result


def _matrix(cm4: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = cm4["prerequisite_matrix"]
    result = {row["id"]: row for row in rows}
    assert len(result) == len(rows), "CM4 prerequisite IDs must be unique"
    return result


def validate_document(doc: dict[str, Any], root: Path = ROOT) -> None:
    schema = load_json(root / "schemas/math_core_domain_shadow.schema.json")
    jsonschema.Draft202012Validator(schema).validate(doc)

    assert doc["operation_id"] == "MCORE-DOMAIN-SHADOW-001"
    assert doc["mode"] == "READ_ONLY_SHADOW"
    assert doc["source_checkpoint"] == {
        "kind": "GIT_COMMIT",
        "repository": "grandchallenge/MATH-PROGRAMME",
        "revision": SNAPSHOT,
    }

    invariants = doc["invariants"]
    assert invariants == {
        "retroactive_live_event_history": False,
        "autonomous_allocation": False,
        "autonomous_pruning": False,
        "canonical_promotion": False,
        "certificate_issuance": False,
        "source_mutation": False,
    }

    supplied_sources = {row["path"]: row for row in doc["source_records"]}
    assert set(supplied_sources) == set(EXPECTED_SOURCES), "source set drifted"
    for rel, expected_blob in EXPECTED_SOURCES.items():
        row = supplied_sources[rel]
        assert row["git_blob_sha1"] == expected_blob, f"declared blob drift for {rel}"
        actual_blob = git_blob_sha1(root / rel)
        assert actual_blob == expected_blob, f"source bytes drifted for {rel}: {actual_blob}"

    cm1 = load_json(root / "governance/cmdg_condensed_cm1_001.json")
    cm2 = load_json(root / "governance/cmdg_condensed_cm2_001.json")
    cm3 = load_json(root / "governance/cmdg_condensed_cm3_001.json")
    c05 = load_json(root / "governance/cmdg_solid_c05_001.json")
    cm4 = load_json(root / "governance/cmdg_condensed_cm4_001.json")
    p3 = load_json(root / "governance/cmdg_condensed_cm4_p3_001.json")

    # Protected-close status is derived forward from later protected receipts;
    # historical source records are intentionally not rewritten.
    assert cm2["protected_cm1"]["operation"] == cm1["operation_id"]
    assert cm2["protected_cm1"]["record_blob_sha1"] == EXPECTED_SOURCES["governance/cmdg_condensed_cm1_001.json"]
    assert cm2["protected_cm1"]["terminal_disposition"] == "CMDG_CONDENSED_CM1_001_PROTECTED_CLOSED"

    assert cm3["protected_cm2"]["operation"] == cm2["operation_id"]
    assert cm3["protected_cm2"]["record_blob_sha1"] == EXPECTED_SOURCES["governance/cmdg_condensed_cm2_001.json"]
    assert cm3["protected_cm2"]["terminal_disposition"] == "CMDG_CONDENSED_CM2_001_PROTECTED_CLOSED"

    assert c05["protected_cm3"]["operation"] == cm3["operation_id"]
    assert c05["protected_cm3"]["terminal_disposition"] == "CMDG_CONDENSED_CM3_001_PROTECTED_CLOSED"

    assert cm4["protected_predecessor"]["operation"] == c05["operation_id"]
    assert cm4["protected_predecessor"]["terminal_disposition"] == "CMDG_SOLID_C05_001_PROTECTED_CLOSED"

    # Preserve the C05 semantic boundary: protected definition work is not a
    # theorem about unrestricted rings and is not a nontrivial solid-object result.
    assert c05["claim_boundary"]["pinned_general_ring_semantics_conferred"] is False
    assert c05["claim_boundary"]["nontrivial_solid_object_conferred"] is False
    assert c05["claim_boundary"]["cm4_conferred"] is False

    p2 = cm4["dependency_reconciliation"]["protected_p2_receipt"]
    assert p2["state"] == "PROTECTED_CLOSED"
    assert cm4["dependency_reconciliation"]["p2_effect"].startswith("CM4-P2 is discharged")

    matrix = _matrix(cm4)
    assert matrix["CM4-P1"]["status"] == "AVAILABLE"
    assert matrix["CM4-P2"]["status"] == "AVAILABLE"
    assert matrix["CM4-P2"]["route_role"] == "PROTECTED_CLOSED"
    assert matrix["CM4-P3"]["status"] == "BLOCKING"
    assert matrix["CM4-P4"]["status"] == "BLOCKING"
    assert matrix["CM4-P4"]["depends_on"] == ["CM4-P5"]
    assert matrix["CM4-P5"]["status"] == "BLOCKING"
    assert matrix["CM4-P6"]["status"] == "PARTIAL_BLOCKING"
    assert matrix["CM4-P6"]["depends_on"] == ["CM4-P3", "CM4-P4"]
    assert cm4["claim_boundary"]["cm4_theorem_certified"] is False
    assert cm4["claim_boundary"]["c06_discharged"] is False

    assert p3["operation_id"] == "CMDG-CONDENSED-CM4-P3-001"
    assert p3["exact_tree_audit"]["result"] == "BLOCKER_NARROWED_TO_PROFINITE_DISCRETE_ACYCLICITY_OR_CERTIFIED_UNDERIVED_REDUCTION"
    assert p3["stage_result"]["p3_state"] == "BLOCKING"
    assert p3["stage_result"]["audit_complete"] is True
    assert p3["stage_result"]["p3_theorem_certified"] is False
    assert p3["stage_result"]["p3_nonblocking_bypass_certified"] is False
    assert p3["disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    # Generic machinery is known to be present; the shadow must not encode the
    # P3 blocker as a generic infrastructure absence.
    observed_classes = {row["classification"] for row in p3["exact_tree_audit"]["observed_sources"]}
    assert "AVAILABLE_GENERIC_EXT" in observed_classes
    assert "AVAILABLE_SHEAF_COHOMOLOGY_AS_EXT" in observed_classes
    assert p3["route_assessment"]["absence_of_condensed_derived_directory_is_blocker"] is False

    nodes = _node_map(doc)
    required_status = {
        "MCORE:CONDENSED:CM1": "PROTECTED_CLOSED",
        "MCORE:CONDENSED:CM2": "PROTECTED_CLOSED",
        "MCORE:CONDENSED:CM3": "PROTECTED_CLOSED",
        "MCORE:CONDENSED:C05": "PROTECTED_CLOSED_DEFINITION_BOUNDARY",
        "MCORE:CONDENSED:CM4": "OPEN_UNCERTIFIED",
        "MCORE:CONDENSED:CM4:P1": "AVAILABLE",
        "MCORE:CONDENSED:CM4:P2": "PROTECTED_CLOSED",
        "MCORE:CONDENSED:CM4:P3": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "MCORE:CONDENSED:CM4:P4": "BLOCKING",
        "MCORE:CONDENSED:CM4:P5": "BLOCKING",
        "MCORE:CONDENSED:CM4:P6": "PARTIAL_BLOCKING",
    }
    for node_id, status in required_status.items():
        assert nodes[node_id]["current_status"] == status, f"shadow status drift for {node_id}"

    assert nodes["MCORE:CONDENSED:CM4:P2"]["blocker_classes"] == []
    assert set(nodes["MCORE:CONDENSED:CM4:P3"]["blocker_classes"]) == {"MATHEMATICAL", "FORMALIZATION"}
    assert all(node["live_event"] is False for node in doc["nodes"])
    assert all(node["canonical_claim_effect"] == "NONE" for node in doc["nodes"])

    node_ids = set(nodes)
    edge_ids: set[str] = set()
    for edge in doc["edges"]:
        assert edge["edge_id"] not in edge_ids, "shadow edge IDs must be unique"
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in node_ids and edge["to"] in node_ids, f"dangling edge {edge['edge_id']}"
        assert edge["authority_effect"] == "NONE_DIRECT"

    frontier = doc["current_frontier"]
    assert frontier["target_status"] == "OPEN_UNCERTIFIED"
    assert frontier["cm4_theorem_certified"] is False
    assert frontier["p1_status"] == "AVAILABLE"
    assert frontier["p2_status"] == "PROTECTED_CLOSED"
    assert frontier["c06_discharged"] is False
    blockers = {row["id"]: row for row in frontier["blockers"]}
    assert set(blockers) == {"CM4-P3", "CM4-P4", "CM4-P5", "CM4-P6"}
    assert blockers["CM4-P3"]["status"] == "BLOCKING"
    assert blockers["CM4-P4"]["depends_on"] == ["CM4-P5"]
    assert blockers["CM4-P6"]["depends_on"] == ["CM4-P3", "CM4-P4"]
    assert not any("EXECUTION_INFRASTRUCTURE" in row["blocker_classes"] for row in blockers.values())

    assert all(value is False for value in doc["claim_boundary"].values())


def main() -> int:
    validate_document(load_json(ARTIFACT))
    print("MCORE-DOMAIN-SHADOW-001 validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
