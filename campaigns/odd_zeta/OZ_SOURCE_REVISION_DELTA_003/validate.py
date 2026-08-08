#!/usr/bin/env python3
"""Fail-closed validator for OZ-SOURCE-REVISION-DELTA-003."""
from __future__ import annotations
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "OZ_SOURCE_REVISION_DELTA_003.json"
EXPECTED_HEAD = "6cc0bf07137815ceeef0d9f340559f85352391e5"
EXPECTED_TREE = "be780558454b704bdd016a3070d698c2e106e2b8"
EXPECTED_SHARP12 = "6a347e2a483ec781afac98016635ce1d73b3c38e"
EXPECTED_REOPEN = {f"REOPEN-0{i}" for i in range(1, 8)}
FORBIDDEN_PREFIXES = ("papers_out/sharp12/", "work/z5la/", "lean/")

class ValidationError(RuntimeError):
    pass

def reject(message: str) -> None:
    raise ValidationError(message)

def load(path: Path = RECORD) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate(data: dict) -> None:
    if data.get("$schema") != "OZ_SOURCE_REVISION_DELTA_003.schema.json": reject("schema identity drift")
    if data.get("record_id") != "OZ-SOURCE-REVISION-DELTA-003": reject("record identity drift")
    if data.get("campaign_id") != "OZ-001" or data.get("programme_issue") != 305 or data.get("umbrella_issue") != 113: reject("governance identity drift")
    a = data.get("authority", {})
    for key in ("programme_base_commit","governed_source_head","governed_source_tree","candidate_source_head","candidate_tree","sharp12_blob"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(a.get(key, ""))): reject(f"malformed {key}")
    if a.get("candidate_source_head") != EXPECTED_HEAD: reject("candidate source head drift")
    if a.get("candidate_tree") != EXPECTED_TREE: reject("candidate tree drift")
    if a.get("governed_source_head") != "790685b7ee4f642a8a88a1bd120636d1b8b39ea8": reject("governed source head drift")
    if a.get("governed_source_tree") != "646ee73dd9066e059b043fad64fb20959f111cbf": reject("governed source tree drift")
    if a.get("ahead_by") != 20 or a.get("changed_file_count") != 44: reject("delta cardinality drift")
    if a.get("sharp12_blob") != EXPECTED_SHARP12 or a.get("sharp12_changed") is not False: reject("Sharp-12 drift incorrectly asserted")
    files = data.get("changed_files", [])
    if len(files) != 44 or len(set(files)) != 44: reject("changed-file manifest must contain exactly 44 unique paths")
    if any(p.startswith(FORBIDDEN_PREFIXES) for p in files): reject("changed-file manifest contradicts locked Sharp-12/z5la/Lean non-delta")
    ds = data.get("delta_scope", {})
    if ds.get("sharp12_files_changed") != [] or ds.get("z5la_files_changed") != [] or ds.get("lean_files_changed") != []: reject("scope drift")
    reopen = data.get("depth_reopening_audit", [])
    ids = {x.get("id") for x in reopen}
    if ids != EXPECTED_REOPEN or len(reopen) != 7: reject("incomplete DEPTH reopening audit")
    if any(x.get("state") != "ABSENT" for x in reopen): reject("DEPTH reopening may not be asserted without a new canonical artifact")
    if data.get("candidate_disposition") != "SOURCE_REVISION_PARTIALLY_ADMITTED_WITH_BLOCKERS": reject("unexpected candidate disposition")
    if data.get("promotion_effect") != "NONE": reject("source intake may not promote claims")
    if data.get("lean_replay", {}).get("state") != "NO_LEAN_DELTA": reject("Lean delta falsely asserted")
    if data.get("executable_replay", {}).get("state") != "PENDING_INDEPENDENT_REPLAY": reject("unreplayed source scripts promoted")
    claims = data.get("claim_register", [])
    if len(claims) < 10: reject("claim register incomplete")
    if not any(c.get("id") == "OZ-DELTA3-C001" and c.get("programme_effect") == "NO_SHARP12_STATUS_CHANGE" for c in claims): reject("missing Sharp-12 no-drift claim")
    nc = data.get("nonclaims", {})
    required_false = ["depth_certified","depth_reopened","t1_top_proved","sharp12_proved","t3_proved","t3_refuted","prime_2_covered","prime_3_covered","new_irrationality_theorem","new_infinitude_theorem","mathcert_adjudicated","novelty_assessed","priority_assessed"]
    if any(nc.get(k) is not False for k in required_false): reject("nonclaim firewall violated")

def main() -> int:
    validate(load())
    print("OZ-SOURCE-REVISION-DELTA-003 validation: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
