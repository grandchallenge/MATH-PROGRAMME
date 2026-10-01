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
STATE = ROOT / "governance/openmath_2026_campaign_state.json"
SCHEMA = ROOT / "schemas/openmath_2026_campaign_state.schema.json"
HUMAN = ROOT / "docs/campaigns/OPENMATH_2026_STATUS.md"
ADOPTION = ROOT / "governance/GCL-CC-00-ADOPTION.json"
SUPERSESSION = ROOT / "governance/openmath_2026_supersession_registry.json"
TOPOLOGY_POLICY = ROOT / "governance/openmath_2026_deprecated_topology_policy.json"
LIFECYCLE_CONTROLLER = ROOT / "governance/openmath_unattended_lifecycle_controller.json"
HILLS = [f"OM26-H{i}" for i in range(1, 8)]
EXPECTED = {
    "OM26-H1": ("Kobon triangles", "alejandrozu/kobon-triangles"),
    "OM26-H2": ("Busy Beaver 6 certificates", "alejandrozu/busy-beaver-6-certificates"),
    "OM26-H3": ("Clique-cluster Ramsey multiplicity", "alejandrozu/clique-cluster-ramsey-multiplicity"),
    "OM26-H4": ("Collatz modular descent", "alejandrozu/collatz-modular-descent"),
    "OM26-H5": ("Grothendieck constant witnesses", "alejandrozu/grothendieck-constant-witnesses"),
    "OM26-H6": ("3x3 matrix multiplication tensor", "alejandrozu/matrix-multiplication-tensor-3x3"),
    "OM26-H7": ("Erdős Problem 3", "ottogin/erdos-3"),
}
LEGACY = {
    "governance/openmath_2026_external_state.json": "d355be89d5ed4c5f1a70dff9d20026451a17c8db",
    "governance/openmath_2026_campaign_binding.json": "36d89557ba5aab589cdf03b099df1d7778a74267",
}
PIPELINE = ["READY","LAUNCHED","RETURNED","CAPTURED","REPLAYED","ADJUDICATED","ADVANCED"]


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
    state = load(root / "governance/openmath_2026_campaign_state.json")
    schema = load(root / "schemas/openmath_2026_campaign_state.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(state, schema, cls=jsonschema.Draft202012Validator)

    topology_policy = load(root / "governance/openmath_2026_deprecated_topology_policy.json")
    require(topology_policy.get("invariant_id") == "CURRENT_TOPOLOGY_NO_H2_H7_GROUPING", "topology policy drift")
    require(topology_policy.get("enforcement", {}).get("on_violation") == "BLOCK_DISCRETIONARY_SUBSTANTIVE_ADVANCEMENT", "topology enforcement weakened")

    adoption = load(root / "governance/GCL-CC-00-ADOPTION.json")
    require(adoption.get("status") == "effective", "GCL-CC-00 adoption not effective")
    require(adoption["enforcement"]["canonical_state"] == "governance/openmath_2026_campaign_state.json", "canonical state pointer drift")
    require(adoption["enforcement"]["human_view"] == "docs/campaigns/OPENMATH_2026_STATUS.md", "human view pointer drift")

    lifecycle = load(root / "governance/openmath_unattended_lifecycle_controller.json")
    require(lifecycle.get("status") == "ACTIVE", "OPENMATH lifecycle controller not active")
    require(lifecycle.get("lifecycle") == PIPELINE, "OPENMATH lifecycle contract drift")
    require(lifecycle.get("acceptance_test", {}).get("manual_transport_allowed") is False, "manual transport reintroduced")
    require(lifecycle.get("acceptance_test", {}).get("manual_controller_wake_allowed") is False, "manual controller wake reintroduced")

    require(state.get("status") == "ACTIVE__CONTROL_PLANE_COHERENT", "canonical state not coherent")
    topology = state.get("canonical_authority", {}).get("topology", {})
    require(topology.get("lane_model") == "SEVEN_FIRST_CLASS_HILLS", "lane model drift")
    require(topology.get("hills") == HILLS, "hill roster drift")
    require(topology.get("grouped_current_lanes") == [], "grouped current lanes reintroduced")
    require(state.get("summary", {}).get("hill_count") == 7, "hill count drift")
    require(state["summary"].get("source_locked_hills") == 7, "source lock count drift")
    require(state["summary"].get("solve_released_hills") == 7, "Solve release count drift")

    rows = {x["hill_slot"]: x for x in state.get("hills", [])}
    require(set(rows) == set(HILLS), "canonical hill rows drift")
    leased = 0
    for hill,(title,external_id) in EXPECTED.items():
        row = rows[hill]
        require(row.get("title") == title, f"{hill} title drift")
        require(row.get("external_hill_id") == external_id, f"{hill} external id drift")
        require(row.get("topology_role") == "FIRST_CLASS_HILL_LANE", f"{hill} topology role drift")
        competition = row.get("competition", {})
        require(competition.get("official_submission") == "NOT_SUBMITTED", f"{hill} official submission drift")
        require(competition.get("official_acceptance") == "NONE", f"{hill} official acceptance drift")
        agent = row.get("external_agent", {})
        lifecycle_state = agent.get("lifecycle")
        require(lifecycle_state in {"LEASED_NOT_LAUNCHED","ACCEPTED"}, f"{hill} unsupported current agent lifecycle")
        if lifecycle_state == "LEASED_NOT_LAUNCHED":
            leased += 1
            require(agent.get("launch_evidence") is None, f"{hill} unexpected launch evidence")
            require(agent.get("return_evidence") is None, f"{hill} unexpected return evidence")
            require(agent.get("adjudication") == "NOT_STARTED", f"{hill} unexpected current adjudication")
        pred = agent.get("predecessor")
        if pred:
            require(pred.get("lifecycle") == "ACCEPTED", f"{hill} predecessor not accepted")
            require(bool(pred.get("adjudication")), f"{hill} predecessor lacks adjudication")

    h1 = rows["OM26-H1"]
    require(h1.get("solve", {}).get("campaign_best_observed") == 93, "H1 campaign best drift")
    require(h1.get("solve", {}).get("frontier") == "Q_GE_6__SOURCE_CONDITIONAL", "H1 frontier drift")
    h1_agent = h1.get("external_agent", {})
    h1_history = h1_agent
    while h1_history.get("assignment_id") != "OM26-H1-H1-12" and isinstance(h1_history.get("predecessor"),dict):
        h1_history=h1_history["predecessor"]
    require(h1_history.get("lifecycle") == "ACCEPTED", "H1 accepted result lost")
    require(h1_history.get("assignment_id") == "OM26-H1-H1-12", "H1 accepted assignment history drift")
    require(h1_history.get("accepted_claim") == "OM26-H1-RED-023", "H1 source-conditional accepted claim lost")

    h2 = rows["OM26-H2"]
    require(str(h2.get("external_agent", {}).get("assignment_id","")).startswith("OM26-H2-WP"), "H2 current assignment syntax drift")

    agents = state["summary"]["external_agents"]
    require(agents.get("leased_not_launched") == leased, "leased-agent summary drift")
    require(isinstance(agents.get("accepted"), int) and agents["accepted"] >= 3, "accepted-agent summary regressed")
    require(agents.get("captured_pending_adjudication") == 0, "captured unadjudicated work left in canonical state")
    require(agents.get("launched_without_return") == 0, "unexpected launched-without-return summary")

    selected = [hill for hill,row in rows.items() if row.get("external_agent",{}).get("lifecycle") == "LEASED_NOT_LAUNCHED"]
    require(state.get("next_action", {}).get("currently_selected") == selected, "next-action selection differs from current leases")

    automation = state.get("automation", {}).get("openmath_lifecycle")
    if automation is not None:
        require(automation.get("manual_transport_required") is False, "canonical automation requires manual transport")
        require(automation.get("manual_controller_wake_required") is False, "canonical automation requires manual wake")
        require(automation.get("last_transition_result") == "ADVANCED", "recorded lifecycle transition did not reach ADVANCED")

    supersession = load(root / "governance/openmath_2026_supersession_registry.json")
    require(supersession.get("current_state_authority") == "governance/openmath_2026_campaign_state.json", "supersession authority drift")
    state_legacy = {x["path"]:x for x in state.get("superseded_current_state_surfaces", [])}
    for path,sha in LEGACY.items():
        require(path in state_legacy, f"missing superseded surface {path}")
        require(state_legacy[path].get("git_blob_sha1") == sha, f"{path} historical blob drift")
        require(git_blob_sha1(root/path) == sha, f"{path} historical bytes drift")

    human = (root / "docs/campaigns/OPENMATH_2026_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        "**Canonical machine authority:** `governance/openmath_2026_campaign_state.json`",
        "H1", "H2", "H3", "H4", "H5", "H6", "H7",
        "Official competition submissions: **0**",
        "GCL-RETURN-RELAY/1",
    ):
        require(marker in human, f"human status missing {marker}")
    if "READY → LAUNCHED → RETURNED → CAPTURED → REPLAYED → ADJUDICATED → ADVANCED" not in human:
        # Pre-controller current status is still permitted while this controller is being admitted.
        require(
            state.get("automation", {}).get("openmath_lifecycle") is None,
            "human status omits frozen lifecycle after automation activation",
        )

    active_surfaces = {
        "hills": state["hills"],
        "next_action": state["next_action"],
        "certification": state["summary"]["certification"],
        "external_agents": state["summary"]["external_agents"],
        "competition": state["summary"]["competition"],
    }
    require("H2-H7" not in json.dumps(active_surfaces, sort_keys=True), "deprecated aggregate leaked into operational state")

    boundaries = state.get("claim_boundaries", {})
    for key,value in boundaries.items():
        if key.endswith("_adjudicated"):
            continue
        require(not bool(value), f"prohibited claim authority widened: {key}")
    return state


def remote_blob(repository: str, path: str) -> str:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise CoreClarityError("GH_TOKEN is required for --verify-live")
    completed = subprocess.run(
        ["gh","api","-X","GET",f"repos/{repository}/contents/{path}","-f","ref=main","--jq",".sha"],
        cwd=ROOT,text=True,capture_output=True,check=False,
    )
    if completed.returncode:
        raise CoreClarityError(f"cannot resolve live artifact {repository}:{path}: {completed.stderr.strip()}")
    value=completed.stdout.strip()
    if len(value)!=40:
        raise CoreClarityError(f"invalid live blob identity {repository}:{path}")
    return value


def verify_live(state: dict[str, Any]) -> None:
    drift=[]
    for domain in ("forge","solve","cert"):
        binding=state["domain_bindings"][domain]
        for artifact in binding["artifacts"]:
            actual=remote_blob(binding["repository"],artifact["path"])
            if actual!=artifact["git_blob_sha1"]:
                drift.append(f"{binding['repository']}:{artifact['path']} canonical={artifact['git_blob_sha1']} live={actual}")
    if drift:
        raise CoreClarityError("CONTROL_PLANE_DRIFT__BLOCK_DISCRETIONARY_SUBSTANTIVE_ADVANCEMENT\n"+"\n".join(drift))


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify-live",action="store_true")
    args=parser.parse_args()
    try:
        state=validate_local(ROOT)
        if args.verify_live:
            verify_live(state)
    except (CoreClarityError,OSError,json.JSONDecodeError,jsonschema.ValidationError) as exc:
        print(f"OPENMATH_CORE_CLARITY_FAIL: {exc}",file=sys.stderr)
        return 2
    print("OPENMATH_CORE_CLARITY_PASS: seven-hill canonical state is coherent")
    if args.verify_live:
        print("OPENMATH_CORE_CLARITY_LIVE_PASS: Forge/Solve/Cert bindings match protected main")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
