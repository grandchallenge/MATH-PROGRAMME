#!/usr/bin/env python3
"""Validate MCORE-DOMAIN-DIAG-001 as a deterministic read-only view."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from validate_math_core_domain_shadow import validate_document as validate_shadow

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/math_core_domain_diag.schema.json"
ARTIFACT = ROOT / "governance/math_core_domain_diag_condensed_001.json"
SHADOW = ROOT / "governance/math_core_domain_shadow_condensed_001.json"
SNAPSHOT = "03ca91bf486d38007799bee0b0552afbfb61245c"
SHADOW_BLOB = "c95e5dc79f1138b1066db42fefe4c56b0cc81c84"

LINEAGE = [
    "MCORE:CONDENSED:CM1",
    "MCORE:CONDENSED:CM2",
    "MCORE:CONDENSED:CM3",
    "MCORE:CONDENSED:C05",
    "MCORE:CONDENSED:CM4",
]
FRONTIER = ["CM4-P1", "CM4-P2", "CM4-P3", "CM4-P4", "CM4-P5", "CM4-P6"]
SUPPORTED_QUERIES = ["summary", "frontier", "node", "ancestry", "blockers", "evidence"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _node_map(shadow: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes = shadow["nodes"]
    result = {node["node_id"]: node for node in nodes}
    assert len(result) == len(nodes), "shadow node IDs must be unique"
    return result


def _frontier_blockers(shadow: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = shadow["current_frontier"]["blockers"]
    result = {row["id"]: row for row in rows}
    assert len(result) == len(rows), "shadow frontier blocker IDs must be unique"
    return result


def derive_document(shadow: dict[str, Any]) -> dict[str, Any]:
    nodes = _node_map(shadow)
    blockers = _frontier_blockers(shadow)

    lineage_view = [
        {
            "ordinal": ordinal,
            "node_id": node_id,
            "current_status": nodes[node_id]["current_status"],
            "authority_class": nodes[node_id]["authority_class"],
            "source_ref": nodes[node_id]["source_ref"],
        }
        for ordinal, node_id in enumerate(LINEAGE, start=1)
    ]

    frontier_view: list[dict[str, Any]] = []
    for item_id in FRONTIER:
        node_id = f"MCORE:CONDENSED:CM4:P{item_id[-1]}"
        node = nodes[node_id]
        if item_id == "CM4-P1":
            role = "AVAILABLE"
            depends_on: list[str] = []
            blocker_classes: list[str] = []
        elif item_id == "CM4-P2":
            role = "DISCHARGED"
            depends_on = []
            blocker_classes = []
        else:
            row = blockers[item_id]
            role = row["status"]
            depends_on = list(row["depends_on"])
            blocker_classes = list(row["blocker_classes"])
        frontier_view.append(
            {
                "id": item_id,
                "node_id": node_id,
                "current_status": node["current_status"],
                "frontier_role": role,
                "blocker_classes": blocker_classes,
                "depends_on": depends_on,
                "source_ref": node["source_ref"],
            }
        )

    return {
        "$schema": "../schemas/math_core_domain_diag.schema.json",
        "schema_version": "1.0.0",
        "operation_id": "MCORE-DOMAIN-DIAG-001",
        "mode": "READ_ONLY_DIAGNOSTIC",
        "domain_programme": "Condensed Mathematics",
        "source_checkpoint": {
            "kind": "GIT_COMMIT",
            "repository": "grandchallenge/MATH-PROGRAMME",
            "revision": SNAPSHOT,
        },
        "source_shadow": {
            "operation_id": "MCORE-DOMAIN-SHADOW-001",
            "path": "governance/math_core_domain_shadow_condensed_001.json",
            "git_blob_sha1": SHADOW_BLOB,
            "authority_effect": "NONE_DIRECT",
        },
        "invariants": {
            "retroactive_live_event_history": False,
            "autonomous_allocation": False,
            "autonomous_pruning": False,
            "canonical_promotion": False,
            "certificate_issuance": False,
            "source_mutation": False,
            "live_coordinator": False,
            "cross_domain_authority_transfer": False,
            "persistent_execution": False,
        },
        "supported_queries": list(SUPPORTED_QUERIES),
        "lineage_view": lineage_view,
        "frontier_view": frontier_view,
        "claim_boundary": {
            "proves_new_mathematics": False,
            "certifies_theorem": False,
            "promotes_claim": False,
            "upgrades_condensed_frontier": False,
            "graph_completeness_claim": False,
            "dependency_minimality_claim": False,
            "dependency_uniqueness_claim": False,
            "authorizes_live_allocation": False,
            "authorizes_live_pruning": False,
            "authorizes_persistent_coordinator": False,
        },
    }


def validate_document(doc: dict[str, Any], root: Path = ROOT) -> None:
    schema = load_json(root / "schemas/math_core_domain_diag.schema.json")
    jsonschema.Draft202012Validator(schema).validate(doc)

    shadow_path = root / "governance/math_core_domain_shadow_condensed_001.json"
    actual_shadow_blob = git_blob_sha1(shadow_path)
    assert actual_shadow_blob == SHADOW_BLOB, f"protected shadow bytes drifted: {actual_shadow_blob}"

    shadow = load_json(shadow_path)
    validate_shadow(shadow, root=root)
    expected = derive_document(shadow)
    assert doc == expected, "diagnostic artifact is not the deterministic projection of the protected shadow"

    nodes = _node_map(shadow)
    assert nodes["MCORE:CONDENSED:CM4:P2"]["current_status"] == "PROTECTED_CLOSED"
    assert nodes["MCORE:CONDENSED:CM4:P2"]["blocker_classes"] == []
    assert nodes["MCORE:CONDENSED:CM4:P3"]["current_status"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    frontier = {row["id"]: row for row in doc["frontier_view"]}
    assert frontier["CM4-P1"]["frontier_role"] == "AVAILABLE"
    assert frontier["CM4-P2"]["frontier_role"] == "DISCHARGED"
    assert frontier["CM4-P3"]["frontier_role"] == "BLOCKING"
    assert set(frontier["CM4-P3"]["blocker_classes"]) == {"MATHEMATICAL", "FORMALIZATION"}
    assert frontier["CM4-P4"]["depends_on"] == ["CM4-P5"]
    assert frontier["CM4-P6"]["depends_on"] == ["CM4-P3", "CM4-P4"]
    assert not any("EXECUTION_INFRASTRUCTURE" in row["blocker_classes"] for row in frontier.values())
    assert all(value is False for value in doc["invariants"].values())
    assert all(value is False for value in doc["claim_boundary"].values())


def main() -> int:
    validate_document(load_json(ARTIFACT))
    print("MCORE-DOMAIN-DIAG-001 validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
