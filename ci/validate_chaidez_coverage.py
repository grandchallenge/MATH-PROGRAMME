#!/usr/bin/env python3
"""Offline coverage inventory; protected bytes are checked by reconciliation."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "governance/chaidez_conformance_coverage.json"

def requirements(contract):
    ids = {"campaign_unit"}
    for key, value in contract.items():
        if isinstance(value, list):
            ids.update(f"{key}.{item}" for item in value)
        elif isinstance(value, dict):
            ids.update(f"{key}.{item}" for item in value)
    return ids

def errors(data=None, compatibility=None):
    data = json.loads(LEDGER.read_text()) if data is None else data
    contract = json.loads((ROOT / "pedagogy/chaidez_protocol_contract.json").read_text())
    compatibility = json.loads((ROOT / "pedagogy/chaidez_v1_v2_compatibility.json").read_text()) if compatibility is None else compatibility
    schema = json.loads((ROOT / "schemas/chaidez_conformance_coverage.schema.json").read_text())
    result = [e.message for e in Draft202012Validator(schema).iter_errors(data)]
    if result:
        return result
    rows = data["requirements"]
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != requirements(contract):
        result.append("coverage must account for every contract member exactly once")
    for row in rows:
        if row["coverage"] == "POLICY_ONLY":
            if not row["unresolved_obligation"]:
                result.append(f'{row["id"]}: policy-only requires an explicit obligation')
        else:
            if any(row[k] is None for k in ("validator", "positive_test", "negative_test")):
                result.append(f'{row["id"]}: enforcement requires pinned tests and validator')
        if row["coverage"] == "PRODUCTION_EXERCISED" and data["production_promotion_count"] == 0:
            result.append("test canary cannot establish production exercise")
    if data["phase"] == "CLOSED":
        if any(row["unresolved_obligation"] or row["coverage"] == "POLICY_ONLY" for row in rows):
            result.append("cannot close with unfinished coverage")
        if data["integration_receipt"] is None:
            result.append("closed coverage requires a pinned integration receipt")
    if compatibility.get("scope") != "CHAIDEZ_RESULT_STATUS_ONLY":
        result.append("migration must stay scoped to Chaidez result status")
    if compatibility.get("field_renames") != {"computation_class": "support_route_class"}:
        result.append("compatibility field mapping drift")
    if any(compatibility.get(k) is not False for k in ("historical_rewrite", "resource_ledger_rename", "claim_upgrade")):
        result.append("compatibility cannot rewrite history or upgrade claims")
    if set(compatibility.get("exposition_stage_mapping", {}).values()) | set(compatibility.get("added_exposition_stages", [])) != set(contract["exposition_sequence"]):
        result.append("compatibility must cover all v2 stages")
    return result

def main():
    failures = errors()
    if failures:
        raise SystemExit("\n".join(failures))
    data = json.loads(LEDGER.read_text())
    print(f'Chaidez coverage: {len(data["requirements"])} requirements, phase={data["phase"]}, production={data["production_promotion_count"]}')

if __name__ == "__main__":
    main()
