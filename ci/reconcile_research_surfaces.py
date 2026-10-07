#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_research_surfaces import ROOT, REGISTRY, validate


def build_report() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors = validate(data)
    surfaces = []
    for row in data["surfaces"]:
        surfaces.append({
            "campaign_id": row["campaign_id"],
            "lifecycle": row["lifecycle"],
            "canonical_tracker": row["live"]["canonical_tracker"],
            "authority_records": row["authority"]["records"],
            "primary_page": row["exposition"]["primary_page"],
            "research_guide": row["exposition"]["research_guide"],
            "status": "CONSISTENT" if not any(e.startswith(row["campaign_id"] + ":") for e in errors) else "RECONCILE",
        })
    return {
        "report_type": "GCL_RESEARCH_SURFACE_RECONCILIATION",
        "authority_effect": "NONE",
        "automatic_claim_promotion": False,
        "errors": errors,
        "surfaces": surfaces,
        "next_action": "repair listed surface relations through ordinary issue/protected-record/docs routes" if errors else "none",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    report = build_report()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        (ROOT / args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if args.check and report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
