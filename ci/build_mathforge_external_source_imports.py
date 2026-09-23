#!/usr/bin/env python3
"""Build the sole Programme import authority from an exact MATHFORGE checkout."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def artifact(forge: Path, path: str, kind: str) -> dict[str, str]:
    data = (forge / path).read_bytes()
    return {"kind": kind, "path": path, "git_blob_sha1": blob_sha1(data), "sha256": hashlib.sha256(data).hexdigest()}


def build(forge: Path, verified_at: str) -> dict[str, Any]:
    commit = subprocess.run(["git", "-C", str(forge), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    registry = load(forge / "governance" / "external_sources.json")
    catalog = load(forge / "catalog" / "manifest.json")
    providers = []
    by_id = {entry["provider_id"]: entry for entry in registry["providers"]}
    for snapshot_id in catalog["provider_snapshots"]:
        manifest_path = f"catalog/providers/{snapshot_id}.json"
        composition_path = f"catalog/providers/{snapshot_id}-composition.json"
        manifest = load(forge / manifest_path)
        provider = by_id[manifest["provider_id"]]
        providers.append({
            "provider_id": manifest["provider_id"], "legacy_source_ids": provider["legacy_source_ids"],
            "snapshot_id": snapshot_id, "upstream_revision": manifest["revision"], "visibility": provider["visibility"],
            "inventory_count": manifest["inventory_count"], "manifest_artifact": artifact(forge, manifest_path, "snapshot_manifest"),
            "composition_artifact": artifact(forge, composition_path, "composition_summary"),
            "catalog_shards": [artifact(forge, shard["path"], "catalog_shard") for shard in manifest["catalog_shards"]],
            "programme_disposition": "READ_ONLY_SEMANTIC_CATALOG",
            "claim_boundary": "Programme imports this exact MATHFORGE snapshot as read-only provenance and tiered catalog metadata. It does not adopt provider status as Programme status, create a Solve result, mutate the canonical Claim Ledger, prove a mathematical claim, or issue or imply a MATHCERT certificate."
        })
    relation_paths = sorted(path.relative_to(forge).as_posix() for path in (forge / "catalog" / "relations").glob("*.json"))
    return {
        "schema_version": "2.0.0", "registry_id": "MATHFORGE-EXTERNAL-SOURCE-IMPORTS",
        "source_foundry": {"repository": "grandchallenge/MATHFORGE", "commit": commit, "registry_artifact": artifact(forge, "governance/external_sources.json", "external_provider_registry")},
        "verified_at": verified_at,
        "catalog_release": {"catalog_release_id": catalog["catalog_release_id"], "entry_count": catalog["total_entries"], "manifest_artifact": artifact(forge, "catalog/manifest.json", "semantic_catalog_manifest"), "relation_artifacts": [artifact(forge, path, "typed_relation_set") for path in relation_paths]},
        "providers": providers,
        "legacy_registry": {"path": "governance/mathforge_provider_imports.json", "disposition": "HISTORICAL_COMPATIBILITY_ONLY", "authority": False},
        "math_core_projection": {"path": "governance/math_core_semantic_catalog_projection.json", "mode": "READ_ONLY_PROVENANCE_BOUND", "canonical_claim_ledger_mutation": False},
        "routing_boundaries": {"mathsolve_minimum_proposal_tier": "SEMANTICALLY_REVIEWED", "exact_campaign_target_tier": "CAMPAIGN_CONCORDANT", "catalog_creates_result": False, "catalog_creates_claim": False, "catalog_creates_certificate": False}
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mathforge", type=Path, required=True)
    parser.add_argument("--verified-at", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = build(args.mathforge.resolve(), args.verified_at)
    args.output.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
