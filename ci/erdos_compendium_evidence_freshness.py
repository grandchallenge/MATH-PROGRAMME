#!/usr/bin/env python3
"""Read-only Erdős Compendium evidence-to-editorial drift detector.

Mathematical claims and editorial publication require separate governance.
This detector generates review *candidates*, never assertions of public truth.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

def audit(registry: dict, admissions: dict, routes: dict, editorial_paths: set[str]) -> dict:
    rows = registry.get("issues")
    if not isinstance(rows, list):
        raise ValueError("invalid catalogue registry")
    ids = {x["problem_id"] for x in rows}
    if len(ids) != 1221 or len(rows) != 1221:
        raise ValueError("not the source-locked 1221-entry catalogue")
    admitted: set[int] = set()
    for row in admissions.get("admissions", []):
        admitted.add(row["problem_id"])
    for batch in admissions.get("batches", []):
        for row in batch.get("entries", []):
            admitted.add(row["problem_id"])
    problems = []
    seen = set()
    for route in routes.get("routes", []):
        if not isinstance(route, dict):
            raise ValueError("invalid route record")
        campaign = route.get("campaign_id", "")
        match = re.fullmatch(r"ERDOS-(\d{1,4})-[A-Z0-9-]+", campaign)
        if not match:
            continue
        n = int(match.group(1))
        if n not in ids:
            raise ValueError(f"cert route not in locked catalogue: {n}")
        status = route.get("intake_status")
        output = route.get("cert_output")
        if status != "certified":
            continue
        if not isinstance(output, dict) or output.get("repository") != "grandchallenge/MATHCERT":
            raise ValueError(f"certified route missing MATHCERT identity: {campaign}")
        key = (n, campaign)
        if key in seen:
            raise ValueError(f"duplicate certified campaign: {campaign}")
        seen.add(key)
        manuscript = f"{n:04d}.md"
        has_manuscript = manuscript in editorial_paths
        is_admitted = n in admitted
        if not (has_manuscript and is_admitted):
            problems.append({
                "problem_id": n,
                "campaign_id": campaign,
                "route_id": route.get("route_id"),
                "certificate_path": output.get("path"),
                "certificate_digest": output.get("digest"),
                "manuscript_exists": has_manuscript,
                "editorial_admitted": is_admitted,
                "disposition": "CERTIFIED_RESULT_EDITORIAL_RECONCILIATION_REQUIRED",
                "publication_authorized_by_this_record": False,
            })
    return {
        "record_type": "ERDOS_COMPENDIUM_EVIDENCE_FRESHNESS/1",
        "authority": "READ_ONLY_TRIAGE_NOT_CLAIM_ADMISSION",
        "registered": len(rows),
        "certified_routes_scanned": len(seen),
        "unreconciled_certified_results": len(problems),
        "review_candidates": sorted(problems, key=lambda x: (x["problem_id"], x["campaign_id"])),
        "automatic_publication": False,
        "historical_snapshot_mutated": False,
    }

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--registry", type=Path, required=True)
    p.add_argument("--admissions", type=Path, required=True)
    p.add_argument("--routes", type=Path, required=True)
    p.add_argument("--editorial-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    for f in (args.registry, args.admissions, args.routes):
        if not f.is_file():
            p.error(f"missing evidence source: {f}")
    result = audit(
        json.loads(args.registry.read_text(encoding="utf-8")),
        json.loads(args.admissions.read_text(encoding="utf-8")),
        json.loads(args.routes.read_text(encoding="utf-8")),
        {x.name for x in args.editorial_dir.glob("[0-9][0-9][0-9][0-9].md")},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Certified routes requiring editorial reconciliation: {result['unreconciled_certified_results']}")
    for x in result["review_candidates"]:
        print(f"::warning title=Erdos {x['problem_id']} editorial drift::{x['campaign_id']} certified but manuscript/admission not complete")
    return None

if __name__ == "__main__":
    main()
