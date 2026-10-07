#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/research_surfaces.json"
SCHEMA = ROOT / "schemas/research_surface_registry.schema.json"
MKDOCS = ROOT / "mkdocs.yml"

CHAIDEZ_REFERENCE_MARKERS = (
    "## 1. Status",
    "## 2. Plain object",
    "## 3. Exact obstruction",
    "## 4. Working model",
    "## 5. Restricted claim",
    "## 6. Theorem-spine location",
    "## 7. Support route",
    "## 8. Debt audit and claim boundary",
    "## 9. First executable step",
)


def _nav_paths(node: Any) -> set[str]:
    out: set[str] = set()
    if isinstance(node, str):
        if node.endswith(".md"):
            out.add(node)
    elif isinstance(node, list):
        for item in node:
            out |= _nav_paths(item)
    elif isinstance(node, dict):
        for item in node.values():
            out |= _nav_paths(item)
    return out


def validate(registry: dict[str, Any] | None = None) -> list[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8")) if registry is None else registry
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [
        f"schema: {err.message}"
        for err in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    ]
    ids = [row.get("campaign_id") for row in data.get("surfaces", [])]
    if len(ids) != len(set(ids)):
        errors.append("registry: duplicate campaign_id")

    nav = _nav_paths(yaml.safe_load(MKDOCS.read_text(encoding="utf-8")).get("nav", []))

    for row in data.get("surfaces", []):
        cid = row.get("campaign_id", "<unknown>")
        authority = row.get("authority", {}).get("records", [])
        for ref in authority:
            if not (ROOT / ref).is_file():
                errors.append(f"{cid}: authority record missing: {ref}")

        expo = row.get("exposition", {})
        page = expo.get("primary_page")
        if page:
            p = ROOT / page
            if not p.is_file():
                errors.append(f"{cid}: exposition page missing: {page}")
                continue
            nav_ref = page.removeprefix("docs/")
            if nav_ref not in nav:
                errors.append(f"{cid}: exposition page missing from mkdocs nav: {nav_ref}")
            text = p.read_text(encoding="utf-8")
            if "Research surface authority" not in text:
                errors.append(f"{cid}: primary page missing Research surface authority box")
            canonical = row.get("live", {}).get("canonical_tracker", "")
            if canonical and canonical not in text:
                errors.append(f"{cid}: primary page missing canonical live tracker {canonical}")
            if authority and not any(ref in text for ref in authority):
                errors.append(f"{cid}: primary page does not cite a registered authority record")
            if "claim boundary" not in text.lower():
                errors.append(f"{cid}: primary page missing explicit claim boundary")
            if row.get("enforcement") == "REFERENCE":
                for marker in CHAIDEZ_REFERENCE_MARKERS:
                    if marker not in text:
                        errors.append(f"{cid}: reference page missing Chaidez marker {marker}")

        guide = expo.get("research_guide")
        if guide:
            gp = ROOT / guide
            if not gp.is_file():
                errors.append(f"{cid}: research guide missing: {guide}")
            elif guide.removeprefix("docs/") not in nav:
                errors.append(f"{cid}: research guide missing from mkdocs nav: {guide}")
            else:
                gtext = gp.read_text(encoding="utf-8")
                trackers = [row.get("live", {}).get("canonical_tracker", "")] + row.get("live", {}).get("active_children", [])
                if trackers and not any(t and t in gtext for t in trackers):
                    errors.append(f"{cid}: research guide missing live tracker link")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        print(f"research surface validation failed with {len(errors)} error(s)")
        return 1
    print("research surface LIVE / AUTHORITY / EXPOSITION contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
