#!/usr/bin/env python3
"""Validate the non-cyclic VGSE post-INTELLECT-repin closure record."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "vgse_post_repin_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "vgse_post_repin_closure.schema.json"
RUNTIME_PATH = ROOT / "governance" / "umbrella_runtime_contract_v5.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit_vgse.json"
ADMISSION_PATH = ROOT / "governance" / "campaign_admission_registry.json"
ACTIVE_PATH = ROOT / "governance" / "governed_campaign_registry.json"

EXPECTED_PROGRAMME_DIGESTS = {
    "routing": "6fb8dce8f1b4f11f8994798840e72b09ad862575",
    "runtime": "2f304cbf07f934e97cdd2fbac7a6ccece2ac4a5a",
    "admission_history": "c724d1174c2e1caa8a74297a21a46aa9d1910962",
    "active_registry": "4cabbd820097029d01430f9f8a0c02653321e5af",
}
FALSE_CLAIMS = {
    "mathematical_target_proved",
    "five_root_theorem_proved",
    "t_embedding_equivalence_proved",
    "certificate_issued",
    "mechanical_claim_authorized",
    "manufacturing_claim_authorized",
    "novelty_claim_authorized",
    "priority_claim_authorized",
    "patentability_claim_authorized",
    "product_claim_authorized",
    "commercial_claim_authorized",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(
        f"blob {len(payload)}\0".encode("ascii") + payload,
        usedforsecurity=False,
    ).hexdigest()


def validation_errors(record: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    record = load_json(RECORD_PATH) if record is None else record
    schema = load_json(SCHEMA_PATH)
    for error in Draft202012Validator(schema).iter_errors(record):
        errors.append(f"closure schema {error.json_path}: {error.message}")

    programme = record.get("programme_activation", {})
    path_map = {
        "routing": ROUTING_PATH,
        "runtime": RUNTIME_PATH,
        "admission_history": ADMISSION_PATH,
        "active_registry": ACTIVE_PATH,
    }
    for field, path in path_map.items():
        expected = EXPECTED_PROGRAMME_DIGESTS[field]
        if git_blob_sha1(path) != expected:
            errors.append(f"protected Programme {field} blob drift")
        if programme.get(field, {}).get("digest") != expected:
            errors.append(f"closure Programme {field} identity drift")

    runtime = load_json(RUNTIME_PATH)
    consumer_sync = runtime.get("consumer_sync", {})
    if consumer_sync.get("intellect_repin_required") is not True:
        errors.append("runtime v5 must preserve the original repin obligation")
    if consumer_sync.get("intellect_repin_complete") is not False:
        errors.append("runtime v5 must remain immutable rather than self-certify completion")
    if consumer_sync.get("completion_authority") != "separate_protected_INTELLECT_merge":
        errors.append("runtime v5 completion authority drift")

    routing = load_json(ROUTING_PATH)
    cert = routing.get("successor_campaign", {}).get("cert", {})
    if cert.get("route_state") != "registered_pending_evidence":
        errors.append("VGSE Cert route state inflated or rolled back")
    if cert.get("may_adjudicate") is not False or cert.get("cert_output") is not None:
        errors.append("VGSE adjudication or certificate output inflated")

    closure = record.get("closure_semantics", {})
    required_true = {
        "intellect_repin_obligation_satisfied",
        "runtime_v5_digest_stable",
        "cyclic_repin_avoided",
        "programme_activation_complete",
        "issue_may_close_only_after_this_record_protected",
        "issue_closure_is_navigation_only",
    }
    for field in required_true:
        if closure.get(field) is not True:
            errors.append(f"closure semantic must remain true: {field}")
    if closure.get("runtime_v5_mutated") is not False:
        errors.append("closure may not mutate runtime v5")

    route = record.get("retained_route_state", {})
    if route.get("route_state") != "registered_pending_evidence":
        errors.append("retained route state drift")
    if route.get("may_adjudicate") is not False or route.get("cert_output") is not None:
        errors.append("retained route state inflated")

    claims = record.get("claim_boundaries", {})
    for field in FALSE_CLAIMS:
        if claims.get(field) is not False:
            errors.append(f"claim boundary inflated: {field}")

    intellect = record.get("intellect_consumer_repin", {})
    if intellect.get("merge_commit") != "c8629942e96ad52df5beede0b80a5909b2561b05":
        errors.append("INTELLECT protected merge identity drift")
    if intellect.get("review", {}).get("state") != "APPROVED":
        errors.append("INTELLECT independent approval missing")
    if intellect.get("unchanged_direct_consumers", {}).get("repin_required") is not False:
        errors.append("unchanged direct consumers incorrectly require repin")

    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"VGSE post-repin closure validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("VGSE post-repin closure is exact, non-cyclic, bounded, and ready for protected review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
