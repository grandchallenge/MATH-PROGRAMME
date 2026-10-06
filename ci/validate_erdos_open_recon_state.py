#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "governance" / "erdos_open_recon_state.json"
RECON = ROOT / "governance" / "erdos_open_recon_reconciliations" / "ERDOS-241-RA-ADJUDICATION-001.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def readj(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_objects(state: dict[str, Any], recon: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("schema_version") != "1.0.0":
        errors.append("state schema drift")
    if state.get("record_type") != "ERDOS_OPEN_RECON_PROGRAMME_STATE":
        errors.append("state record type drift")
    if state.get("campaign") != "ERDOS-OPEN-RECON":
        errors.append("state campaign drift")
    if state.get("last_reconciliation") != "ERDOS-241-RA-ADJUDICATION-001":
        errors.append("last reconciliation drift")

    row = state.get("reconciled_advancements", {}).get("241")
    if not isinstance(row, dict):
        errors.append("241 advancement missing")
    else:
        if row.get("status") != "ADVANCED_NATIVE_SUCCESSOR_READY":
            errors.append("241 advancement status drift")
        if row.get("successor") != "ERDOS-241-N1-LOCAL-DIFFERENCE-POWER":
            errors.append("241 successor drift")
        if row.get("source_gate") != "OPEN__S1_NOT_PROTECTED":
            errors.append("241 source gate drift")
        if row.get("parent_problem_effect") != "NONE":
            errors.append("241 parent-problem effect inflated")
        if not SHA40.fullmatch(str(row.get("solve_merge", ""))):
            errors.append("241 Solve merge malformed")

    automation = state.get("automation")
    if not isinstance(automation, dict):
        errors.append("automation state missing")
    else:
        if automation.get("intake_preservation") != "QUALIFIED_UNATTENDED":
            errors.append("intake preservation qualification drift")
        if automation.get("post_intake_cohort_lifecycle") != "NOT_YET_UNATTENDED":
            errors.append("post-intake lifecycle overstated")

    for key in ("certification", "publication", "parent_problem", "literature_currentness"):
        if state.get("authority_boundaries", {}).get(key) is not False:
            errors.append(f"state authority inflation: {key}")

    if recon.get("schema_version") != "1.0.0":
        errors.append("reconciliation schema drift")
    if recon.get("record_type") != "ERDOS_OPEN_RECON_PROGRAMME_RECONCILIATION":
        errors.append("reconciliation record type drift")
    if recon.get("reconciliation_id") != "ERDOS-241-RA-ADJUDICATION-001":
        errors.append("reconciliation id drift")
    if recon.get("campaign") != "ERDOS-OPEN-RECON" or recon.get("problem_id") != 241:
        errors.append("reconciliation campaign/problem drift")
    if recon.get("solve_protected_merge") != "91c4a7879ad5b51077fdba9cb1f5e9367bc4a7e0":
        errors.append("protected Solve merge drift")
    if recon.get("solve_pull_request") != 936:
        errors.append("protected Solve PR drift")
    if recon.get("lifecycle") != [
        "RETURNED","CAPTURED","PROTECTED","BLIND_COHORT_CLOSED","REPLAYED","ADJUDICATED","ADVANCED"
    ]:
        errors.append("lifecycle trace drift")

    artifacts = recon.get("protected_artifacts")
    required = {
        "closure": ("contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/closures/ERDOS-241-BLIND-COHORT-001.json", "5b5d492bb63cf654f495fd1989c4d5e18a2bb8f5"),
        "replay": ("contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/replays/ERDOS-241-RA-REPLAY-001.json", "e4e1e6746eec93863bbb9afcbf71f482cf45a25a"),
        "synthesis": ("contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/synthesis/ERDOS-241-RA-SYNTHESIS-001.md", "bdd66ea573d9fc2b252881a349a1f32ad31651f3"),
        "adjudication": ("contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/adjudications/ERDOS-241-RA-ADJUDICATION-001.json", "bb16bcb2074bd59fa38b25a7f3f615c91844a630"),
        "successor": ("work_packages/ERDOS_OPEN/ERDOS_241_N1_LOCAL_DIFFERENCE_POWER.md", "d10d4ce51a9295afcf71f196e310d308911b1f67"),
    }
    if not isinstance(artifacts, dict):
        errors.append("protected artifact map missing")
    else:
        for key, (path, blob) in required.items():
            item = artifacts.get(key)
            if not isinstance(item, dict) or item.get("path") != path or item.get("git_blob_sha1") != blob:
                errors.append(f"protected artifact binding drift: {key}")

    source = recon.get("source_gate")
    if not isinstance(source, dict):
        errors.append("reconciliation source gate missing")
    else:
        if source.get("dispatch_id") != "ERDOS-241-S1-IA-001":
            errors.append("reconciliation source identity drift")
        if source.get("protected_at_adjudication") is not False:
            errors.append("reconciliation source protected flag inflated")
        if source.get("literature_dependent_promotion_allowed") is not False:
            errors.append("reconciliation literature promotion inflated")

    effects = recon.get("effects", {})
    if effects.get("solve_internal_claims") is not True:
        errors.append("Solve internal claim effect missing")
    for key in ("parent_erdos_problem", "literature_status", "certification", "publication", "prize"):
        if effects.get(key) is not False:
            errors.append(f"reconciliation authority inflation: {key}")

    return errors


def validate() -> list[str]:
    missing = [str(p.relative_to(ROOT)) for p in (STATE, RECON) if not p.is_file()]
    if missing:
        return [f"missing ERDOS Programme state: {x}" for x in missing]
    return validate_objects(readj(STATE), readj(RECON))


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("PASS: ERDOS-OPEN Programme reconciliation state valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
