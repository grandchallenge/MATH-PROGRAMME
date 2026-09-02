#!/usr/bin/env python3
"""Read-only query surface for MCORE-DOMAIN-DIAG-001."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "ci"
if str(CI) not in sys.path:
    sys.path.insert(0, str(CI))

from validate_math_core_domain_diag import (  # noqa: E402
    ARTIFACT,
    FRONTIER,
    LINEAGE,
    SHADOW,
    load_json,
    validate_document,
)

BLOCKER_CLASSES = [
    "MATHEMATICAL",
    "FORMALIZATION",
    "GOVERNANCE_EVIDENCE",
    "EXECUTION_INFRASTRUCTURE",
]


def emit(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def node_map(shadow: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {node["node_id"]: node for node in shadow["nodes"]}


def cmd_summary(diag: dict[str, Any]) -> None:
    emit(
        {
            "operation_id": diag["operation_id"],
            "mode": diag["mode"],
            "domain_programme": diag["domain_programme"],
            "source_checkpoint": diag["source_checkpoint"],
            "source_shadow": diag["source_shadow"],
            "lineage": [
                {"node_id": row["node_id"], "current_status": row["current_status"]}
                for row in diag["lineage_view"]
            ],
            "frontier": [
                {
                    "id": row["id"],
                    "current_status": row["current_status"],
                    "frontier_role": row["frontier_role"],
                }
                for row in diag["frontier_view"]
            ],
        }
    )


def cmd_frontier(diag: dict[str, Any]) -> None:
    emit(diag["frontier_view"])


def cmd_node(shadow: dict[str, Any], node_id: str) -> None:
    nodes = node_map(shadow)
    if node_id not in nodes:
        raise SystemExit(f"unknown node_id: {node_id}")
    emit(nodes[node_id])


def cmd_ancestry(shadow: dict[str, Any], node_id: str) -> None:
    nodes = node_map(shadow)
    if node_id not in nodes:
        raise SystemExit(f"unknown node_id: {node_id}")

    if node_id in LINEAGE:
        path = LINEAGE[: LINEAGE.index(node_id) + 1]
    elif node_id.startswith("MCORE:CONDENSED:CM4:P"):
        path = [*LINEAGE, node_id]
    else:
        raise SystemExit("ancestry is defined only for the protected lineage and CM4 frontier nodes")

    emit([{"node_id": item, "current_status": nodes[item]["current_status"]} for item in path])


def cmd_blockers(diag: dict[str, Any], blocker_class: str | None) -> None:
    rows = [
        row
        for row in diag["frontier_view"]
        if row["frontier_role"] in {"BLOCKING", "PARTIAL_BLOCKING"}
    ]
    if blocker_class is not None:
        rows = [row for row in rows if blocker_class in row["blocker_classes"]]
    emit(rows)


def cmd_evidence(shadow: dict[str, Any], node_id: str) -> None:
    nodes = node_map(shadow)
    if node_id not in nodes:
        raise SystemExit(f"unknown node_id: {node_id}")
    related_edges = [
        {
            "edge_id": edge["edge_id"],
            "relation": edge["relation"],
            "from": edge["from"],
            "to": edge["to"],
            "evidence_refs": edge["evidence_refs"],
            "authority_effect": edge["authority_effect"],
        }
        for edge in shadow["edges"]
        if edge["from"] == node_id or edge["to"] == node_id
    ]
    emit(
        {
            "node_id": node_id,
            "source_operation": nodes[node_id]["source_operation"],
            "source_ref": nodes[node_id]["source_ref"],
            "authority_class": nodes[node_id]["authority_class"],
            "related_edges": related_edges,
        }
    )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Query the protected Condensed Mathematics MATH-CORE diagnostic view."
    )
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("summary", help="show source identity, protected lineage, and frontier status")
    sub.add_parser("frontier", help="show the six CM4 frontier entries")

    node = sub.add_parser("node", help="show one exact shadow node")
    node.add_argument("node_id")

    ancestry = sub.add_parser("ancestry", help="show protected lineage ancestry for a node")
    ancestry.add_argument("node_id")

    blockers = sub.add_parser("blockers", help="show blocking and partial-blocking frontier entries")
    blockers.add_argument("--class", dest="blocker_class", choices=BLOCKER_CLASSES)

    evidence = sub.add_parser("evidence", help="show source/evidence references for a node")
    evidence.add_argument("node_id")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    diag = load_json(ARTIFACT)
    shadow = load_json(SHADOW)
    validate_document(diag)

    if args.command == "summary":
        cmd_summary(diag)
    elif args.command == "frontier":
        cmd_frontier(diag)
    elif args.command == "node":
        cmd_node(shadow, args.node_id)
    elif args.command == "ancestry":
        cmd_ancestry(shadow, args.node_id)
    elif args.command == "blockers":
        cmd_blockers(diag, args.blocker_class)
    elif args.command == "evidence":
        cmd_evidence(shadow, args.node_id)
    else:  # pragma: no cover
        raise AssertionError(args.command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
