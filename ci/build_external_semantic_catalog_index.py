#!/usr/bin/env python3
"""Build the public metadata index and read-only MATH-CORE projection."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def entries(forge: Path) -> Iterator[dict[str, Any]]:
    manifest = load(forge / "catalog" / "manifest.json")
    for snapshot in manifest["provider_snapshots"]:
        provider = load(forge / "catalog" / "providers" / f"{snapshot}.json")
        for shard in provider["catalog_shards"]:
            with (forge / shard["path"]).open("r", encoding="utf-8") as handle:
                for line in handle:
                    yield json.loads(line)


def campaign_map(forge: Path) -> tuple[dict[str, list[str]], list[dict[str, str]]]:
    campaigns: dict[str, list[str]] = {}
    edges: list[dict[str, str]] = []
    for path in sorted((forge / "catalog" / "relations").glob("*.json")):
        for relation in load(path).get("relations", []):
            subject = relation["subject_id"]
            obj = relation["object_id"]
            campaign = subject if subject.startswith("GCL-CAMPAIGN:") else obj if obj.startswith("GCL-CAMPAIGN:") else None
            catalog = subject if subject.startswith("GCL-CAT-") else obj if obj.startswith("GCL-CAT-") else None
            if campaign and catalog:
                campaigns.setdefault(catalog, []).append(campaign.removeprefix("GCL-CAMPAIGN:"))
            edges.append({
                "relation_id": relation["relation_id"], "subject_id": subject,
                "predicate": relation["predicate"], "object_id": obj,
                "review_state": relation["review_state"],
            })
    return campaigns, edges


def status_labels(entry: dict[str, Any]) -> list[str]:
    labels = []
    for assertion in entry.get("status_assertions", []):
        value = str(assertion.get("value", ""))
        if value.startswith("open_status:") or value.startswith("category:"):
            labels.append(value.split(":", 1)[1])
    return sorted(set(labels))


def build(forge: Path, forge_commit: str, public_path: Path, projection_path: Path) -> None:
    manifest = load(forge / "catalog" / "manifest.json")
    campaigns, edges = campaign_map(forge)
    public_entries = []
    node_ranges = []
    for snapshot in manifest["provider_snapshots"]:
        provider = load(forge / "catalog" / "providers" / f"{snapshot}.json")
        for shard in provider["catalog_shards"]:
            node_ranges.append({
                "provider_id": provider["provider_id"], "snapshot_id": snapshot,
                "artifact_path": shard["path"], "artifact_sha256": shard["sha256"],
                "first_catalog_id": shard["first_catalog_id"], "last_catalog_id": shard["last_catalog_id"],
                "node_count": shard["entry_count"], "mode": "READ_ONLY_PROVENANCE_BOUND",
            })
    for entry in entries(forge):
        metadata_only = entry["licensing"]["redistribution_class"] != "full_text"
        if metadata_only:
            title = entry.get("formal_language", {}).get("declaration_name", entry["catalog_id"])
            warning = "Metadata only; source text is withheld under the entry's redistribution disposition."
        else:
            title = entry["representations"]["original"].splitlines()[0][:240]
            warning = "Source text is reproduced under the recorded license; status remains provider-attributed."
        public_entries.append({
            "id": entry["catalog_id"], "title": title, "provider": entry["provider_id"],
            "msc": entry["classification"]["msc2020_primary"], "status": status_labels(entry),
            "language": entry.get("formal_language", {}).get("language"),
            "assurance": entry["assurance"]["tier"], "campaign": sorted(campaigns.get(entry["catalog_id"], [])),
            "visibility": entry["licensing"]["redistribution_class"], "warning": warning,
        })
    public_entries.sort(key=lambda item: item["id"])
    write(public_path, {
        "schema_version": "2.0.0", "catalog_release_id": manifest["catalog_release_id"],
        "mathforge_commit": forge_commit, "entry_count": len(public_entries), "entries": public_entries,
        "authority_boundary": "This public index exposes provenance and assurance metadata only. It is not a status ledger, result registry, Claim Ledger, proof record, or certificate registry."
    })
    write(projection_path, {
        "schema_version": "2.0.0", "projection_id": "MATH-CORE-EXTERNAL-SEMANTIC-CATALOG-001",
        "catalog_release_id": manifest["catalog_release_id"], "mathforge_commit": forge_commit,
        "node_count": len(public_entries), "node_ranges": node_ranges, "typed_edges": edges,
        "projection_mode": "READ_ONLY_PROVENANCE_BOUND", "canonical_claim_ledger_mutation": False,
        "authority_boundary": "This projection exposes catalog nodes and reviewed or proposed typed relations to MATH-CORE domain subgraphs. It cannot create, amend, supersede, or certify a canonical Claim Ledger claim."
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mathforge", type=Path, required=True)
    parser.add_argument("--mathforge-commit", required=True)
    parser.add_argument("--public-output", type=Path, required=True)
    parser.add_argument("--projection-output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.mathforge_commit) != 40:
        raise SystemExit("mathforge commit must be a full 40-character identity")
    build(args.mathforge.resolve(), args.mathforge_commit, args.public_output, args.projection_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
