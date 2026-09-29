#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "governance" / "openmath_2026_campaign_state.json"
STATE_SCHEMA = ROOT / "schemas" / "openmath_2026_campaign_state.schema.json"
HUMAN = ROOT / "docs" / "campaigns" / "OPENMATH_2026_STATUS.md"
ADOPTION = ROOT / "governance" / "GCL-CC-00-ADOPTION.json"
SUPERSESSION = ROOT / "governance" / "openmath_2026_supersession_registry.json"

EXPECTED_HILLS = {
    "OM26-H1": ("Kobon triangles", "alejandrozu/kobon-triangles"),
    "OM26-H2": ("Busy Beaver 6 certificates", "alejandrozu/busy-beaver-6-certificates"),
    "OM26-H3": ("Clique-cluster Ramsey multiplicity", "alejandrozu/clique-cluster-ramsey-multiplicity"),
    "OM26-H4": ("Collatz modular descent", "alejandrozu/collatz-modular-descent"),
    "OM26-H5": ("Grothendieck constant witnesses", "alejandrozu/grothendieck-constant-witnesses"),
    "OM26-H6": ("3x3 matrix multiplication tensor", "alejandrozu/matrix-multiplication-tensor-3x3"),
    "OM26-H7": ("Erdős Problem 3", "ottogin/erdos-3"),
}
EXPECTED_LEGACY = {
    "governance/openmath_2026_external_state.json": "d355be89d5ed4c5f1a70dff9d20026451a17c8db",
    "governance/openmath_2026_campaign_binding.json": "36d89557ba5aab589cdf03b099df1d7778a74267",
}


class CoreClarityError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CoreClarityError(f"expected object: {path}")
    return value


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CoreClarityError(message)


def validate_local(root: Path = ROOT) -> dict[str, Any]:
    state = load(root / "governance" / "openmath_2026_campaign_state.json")
    schema = load(root / "schemas" / "openmath_2026_campaign_state.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        state,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    adoption = load(root / "governance" / "GCL-CC-00-ADOPTION.json")
    require(adoption["status"] == "effective", "GCL-CC-00 Programme adoption is not effective")
    require(
        adoption["enforcement"]["canonical_state"] == "governance/openmath_2026_campaign_state.json",
        "GCL-CC-00 canonical-state pointer drift",
    )
    require(
        adoption["enforcement"]["human_view"] == "docs/campaigns/OPENMATH_2026_STATUS.md",
        "GCL-CC-00 human-view pointer drift",
    )
    require(
        adoption["enforcement"]["on_drift"] == "BLOCK_DISCRETIONARY_SUBSTANTIVE_ADVANCEMENT",
        "GCL-CC-00 drift behavior weakened",
    )

    require(state["status"] == "ACTIVE__CONTROL_PLANE_COHERENT", "canonical state is not coherent")
    require(
        state["canonical_authority"]["path"] == "governance/openmath_2026_campaign_state.json",
        "canonical authority self-pointer drift",
    )
    require(state["summary"]["hill_count"] == 7, "hill-count summary must be seven")
    require(state["summary"]["source_locked_hills"] == 7, "all seven hills must be source locked")
    require(state["summary"]["solve_released_hills"] == 7, "all seven hills must be Solve released")

    hills = {row["hill_slot"]: row for row in state["hills"]}
    require(set(hills) == set(EXPECTED_HILLS), "canonical hill roster mismatch")
    for slot, (title, external_id) in EXPECTED_HILLS.items():
        row = hills[slot]
        require(row["title"] == title, f"{slot} title drift")
        require(row["external_hill_id"] == external_id, f"{slot} external identity drift")
        require(
            row["competition"]["official_submission"] == "NOT_SUBMITTED",
            f"{slot} must explicitly record NOT_SUBMITTED",
        )
        require(row["competition"]["official_acceptance"] == "NONE", f"{slot} acceptance state drift")

    h1 = hills["OM26-H1"]
    require(h1["solve"]["campaign_best_observed"] == 93, "H1 campaign best must remain 93")
    require(
        h1["solve"]["frontier"] == "Q_GE_6_OR_Q5_EXACT_NESTED_TRIANGLE_EQUALITY__SOURCE_CONDITIONAL",
        "H1 protected frontier drift",
    )
    require(h1["solve"]["frontier_changed_by_agent001"] is False, "unadjudicated Agent 001 result changed frontier")
    require(h1["external_agent"]["lifecycle"] == "CAPTURED", "H1 Agent 001 must be CAPTURED")
    require(h1["external_agent"]["capture_state"] == "CAPTURED_RECOVERED_UNADJUDICATED", "H1 capture state drift")
    require(h1["external_agent"]["adjudication"] == "PENDING", "H1 adjudication must remain PENDING")
    require(h1["cert"]["certification_effect"] is False, "H1 Cert intake cannot self-certify")
    require(h1["competition"]["lifecycle"] == "CERT_PENDING", "H1 competition lifecycle drift")
    require(h1["competition"]["public_evaluator_replay"] == "PASS__UNOFFICIAL_LOCAL_SCORE", "H1 evaluator boundary drift")

    for i in range(2, 8):
        row = hills[f"OM26-H{i}"]
        require(row["external_agent"]["lifecycle"] == "LEASED_NOT_LAUNCHED", f"OM26-H{i} lifecycle drift")
        require(row["external_agent"]["launch_evidence"] is None, f"OM26-H{i} has undeclared launch evidence")
        require(row["external_agent"]["return_evidence"] is None, f"OM26-H{i} has undeclared return evidence")
        require(row["external_agent"]["adjudication"] == "NOT_STARTED", f"OM26-H{i} adjudication drift")
        require(row["cert"]["state"] == "NOT_YET_ELIGIBLE", f"OM26-H{i} Cert state drift")
        require(row["competition"]["lifecycle"] == "NO_CANDIDATE", f"OM26-H{i} competition lifecycle drift")

    agents = state["summary"]["external_agents"]
    require(agents == {
        "captured_pending_adjudication": 1,
        "leased_not_launched": 6,
        "launched_without_return": 0,
        "accepted": 0,
    }, "agent summary does not equal hill projection")
    competition = state["summary"]["competition"]
    require(competition["submitted_hills"] == 0 and competition["accepted_hills"] == 0, "competition summary implies an external result")
    require(state["next_action"]["id"] == "adjudicate_agent001_recovered_result", "next action is not deterministic Agent 001 adjudication")

    supersession_registry = load(root / "governance" / "openmath_2026_supersession_registry.json")
    require(
        supersession_registry.get("current_state_authority") == "governance/openmath_2026_campaign_state.json",
        "supersession registry current-state authority drift",
    )
    registry_rows = {row["path"]: row for row in supersession_registry.get("records", [])}
    require(set(registry_rows) == set(EXPECTED_LEGACY), "supersession registry roster mismatch")

    superseded = {row["path"]: row for row in state["superseded_current_state_surfaces"]}
    require(set(superseded) == set(EXPECTED_LEGACY), "superseded Programme surface roster mismatch")
    for rel, expected_blob in EXPECTED_LEGACY.items():
        row = superseded[rel]
        require(row["status"] == "SUPERSEDED_FOR_CURRENT_STATE", f"{rel} is not marked superseded")
        require(row["historical_only"] is True, f"{rel} is not historical-only")
        require(row["git_blob_sha1"] == expected_blob, f"{rel} supersession blob mismatch")
        registry_row = registry_rows[rel]
        require(registry_row["git_blob_sha1"] == expected_blob, f"{rel} supersession registry blob mismatch")
        require(registry_row["status"] == "SUPERSEDED_FOR_CURRENT_STATE", f"{rel} registry status drift")
        require(registry_row["historical_only"] is True, f"{rel} registry historical-only drift")
        require(git_blob_sha1(root / rel) == expected_blob, f"{rel} local historical bytes drift")

    human = (root / "docs" / "campaigns" / "OPENMATH_2026_STATUS.md").read_text(encoding="utf-8")
    required_human = [
        "**Canonical machine authority:** `governance/openmath_2026_campaign_state.json`",
        "SUPERSEDED_FOR_CURRENT_STATE",
        "1 CAPTURED pending adjudication; 6 LEASED_NOT_LAUNCHED",
        "Official competition submissions: **0**",
        "Agent 001 result recovered; adjudication **PENDING**",
        "**CERT_PENDING; NOT_SUBMITTED**",
        "**Adjudicate the recovered Agent 001 H1 result.**",
        "control-plane drift",
    ]
    for marker in required_human:
        require(marker in human, f"human status view missing canonical marker: {marker}")
    for i in range(2, 8):
        require(f"| H{i} |" in human and f"Agent 00{i} / #{503+i}" in human, f"human status missing OM26-H{i}")
    require(human.count("LEASED_NOT_LAUNCHED") >= 7, "human status does not expose all lease lifecycle states")
    require(human.count("NOT_SUBMITTED") >= 8, "human status does not make competition state explicit")

    if any(bool(value) for value in state["claim_boundaries"].values()):
        raise CoreClarityError("canonical state widens prohibited claim authority")
    return state


def remote_blob(repository: str, path: str) -> str:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise CoreClarityError("GH_TOKEN is required for --verify-live")
    cmd = [
        "gh", "api", "-X", "GET",
        f"repos/{repository}/contents/{path}",
        "-f", "ref=main",
        "--jq", ".sha",
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise CoreClarityError(
            f"cannot resolve live protected artifact {repository}:{path}: {completed.stderr.strip()}"
        )
    value = completed.stdout.strip()
    if len(value) != 40:
        raise CoreClarityError(f"invalid live Git blob identity for {repository}:{path}")
    return value


def verify_live(state: dict[str, Any]) -> None:
    drift: list[str] = []
    for domain in ("forge", "solve", "cert"):
        binding = state["domain_bindings"][domain]
        repository = binding["repository"]
        for artifact in binding["artifacts"]:
            actual = remote_blob(repository, artifact["path"])
            if actual != artifact["git_blob_sha1"]:
                drift.append(
                    f"{repository}:{artifact['path']} canonical={artifact['git_blob_sha1']} live={actual}"
                )
    if drift:
        raise CoreClarityError(
            "CONTROL_PLANE_DRIFT__BLOCK_DISCRETIONARY_SUBSTANTIVE_ADVANCEMENT\n"
            + "\n".join(drift)
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-live", action="store_true")
    args = parser.parse_args()
    try:
        state = validate_local(ROOT)
        if args.verify_live:
            verify_live(state)
    except (CoreClarityError, OSError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
        print(f"OPENMATH_CORE_CLARITY_FAIL: {exc}", file=sys.stderr)
        return 2
    print("OPENMATH_CORE_CLARITY_PASS: canonical seven-hill state and human projection agree")
    if args.verify_live:
        print("OPENMATH_CORE_CLARITY_LIVE_PASS: Forge/Solve/Cert protected artifacts match canonical bindings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
