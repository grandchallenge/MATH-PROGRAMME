from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECONCILIATION_PATH = ROOT / "governance" / "administrative_cadence_reconciliation.json"
PORTFOLIO_PATH = (
    ROOT
    / "governance"
    / "administrative_portfolio_reviews"
    / "MP-ADMIN-PORTFOLIO-REVIEW-2026-08-03-001.json"
)
SWEEP_PATHS = [
    ROOT / "governance" / "administrative_structural_sweeps" / name
    for name in (
        "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-02-002.json",
        "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-02-003.json",
        "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-03-004.json",
        "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-005.json",
    )
]
SCHEMA_PATHS = {
    "reconciliation": ROOT / "schemas" / "administrative_cadence_reconciliation.schema.json",
    "portfolio": ROOT / "schemas" / "administrative_portfolio_review.schema.json",
    "sweep": ROOT / "schemas" / "administrative_reconstructed_structural_sweep.schema.json",
}

EXPECTED_SWEEPS = {
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-02-002": (
        "2026-08-02T03:57:00-07:00",
        3645,
        "7e9e28ceac6b33442669b801350fe585939cb5a6",
    ),
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-02-003": (
        "2026-08-02T20:45:00-07:00",
        2637,
        "e828a19493c8547c2d0ffeede76038a51174990a",
    ),
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-03-004": (
        "2026-08-03T13:33:00-07:00",
        1629,
        "e828a19493c8547c2d0ffeede76038a51174990a",
    ),
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-005": (
        "2026-08-04T06:21:00-07:00",
        621,
        "42de075a3a3412042cac371870e863f17f0e248b",
    ),
}
EXPECTED_INVENTORY = {
    "grandchallenge/MATH-PROGRAMME": (
        "fb8e215d56714f595f328cb22b2b3f5e9410cc7b",
        "b98d5ba79439e7ef7ee6493604bcfc40f9422dd8",
        245,
    ),
    "grandchallenge/MATHFORGE": (
        "0ea98866de3066e6a44ea1ca2cf93ade8a9e1c15",
        "da79f89388099749d6a93e03c4364fc018a19197",
        5,
    ),
    "grandchallenge/MATHSOLVE": (
        "443daf537dc7e4ee34ab43aeb01508d9177816ab",
        "1ebc9ace360e453fbc3707f6b23032b1c3c561eb",
        37,
    ),
    "grandchallenge/MATHCERT": (
        "e8d1e34509e640d82902ad0195560740b52bec0e",
        "92e3e56fda50267a241e120eb337dbbc520e900f",
        232,
    ),
    "grandchallenge/INTELLECT": (
        "d26d673efffbe0874e1440450322869ff70be9d1",
        "c8629942e96ad52df5beede0b80a5909b2561b05",
        74,
    ),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_bundle() -> dict:
    return {
        "reconciliation": load_json(RECONCILIATION_PATH),
        "portfolio": load_json(PORTFOLIO_PATH),
        "sweeps": [load_json(path) for path in SWEEP_PATHS],
    }


def load_schemas() -> dict:
    return {name: load_json(path) for name, path in SCHEMA_PATHS.items()}


def schema_errors(document: dict, schema: dict) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(document)]


def validate_bundle(bundle: dict, schemas: dict | None = None) -> list[str]:
    schemas = schemas or load_schemas()
    errors: list[str] = []
    reconciliation = bundle["reconciliation"]
    portfolio = bundle["portfolio"]
    sweeps = bundle["sweeps"]

    errors.extend(f"reconciliation schema: {item}" for item in schema_errors(reconciliation, schemas["reconciliation"]))
    errors.extend(f"portfolio schema: {item}" for item in schema_errors(portfolio, schemas["portfolio"]))
    for sweep in sweeps:
        errors.extend(
            f"{sweep.get('sweep_id', 'unknown')} schema: {item}"
            for item in schema_errors(sweep, schemas["sweep"])
        )

    observed_sweeps = {sweep.get("sweep_id"): sweep for sweep in sweeps}
    if set(observed_sweeps) != set(EXPECTED_SWEEPS):
        errors.append("the four missed structural-sweep loci are not represented exactly once")

    for sweep_id, (due, lateness, head) in EXPECTED_SWEEPS.items():
        sweep = observed_sweeps.get(sweep_id)
        if not sweep:
            continue
        started = datetime.fromisoformat(sweep["reconstruction_started_at"])
        scheduled = datetime.fromisoformat(sweep["scheduled_due_at"])
        calculated = int((started - scheduled).total_seconds() // 60)
        if sweep["scheduled_due_at"] != due or sweep["lateness_minutes_at_start"] != lateness or calculated != lateness:
            errors.append(f"{sweep_id} does not preserve its original deadline and exact lateness")
        if sweep["programme_head_at_due"] != head:
            errors.append(f"{sweep_id} historical Programme head differs from reconstructed evidence")
        if sweep["waiver_used"] or sweep["cadence_anchor_reset"]:
            errors.append(f"{sweep_id} improperly waives or resets the cadence")
        if sweep["evidence_mode"] != "RETROSPECTIVE_RECONSTRUCTION":
            errors.append(f"{sweep_id} obscures retrospective evidence classification")
        if len(sweep["findings"]["P2"]) != 1:
            errors.append(f"{sweep_id} does not retain one independent P2 finding")
        if not all(value is False for value in sweep["claim_boundaries"].values()):
            errors.append(f"{sweep_id} inflates a prohibited claim")

    summary_paths = set(reconciliation["structural_sweep_records"])
    expected_paths = {str(path.relative_to(ROOT)).replace("\\", "/") for path in SWEEP_PATHS}
    if summary_paths != expected_paths:
        errors.append("reconciliation does not bind the four separate sweep records exactly")

    inventory = {
        item["repository"]: (
            item["first_sweep_head"],
            item["reconciliation_head"],
            item["commits_since_first_sweep"],
        )
        for item in reconciliation["repository_change_inventory"]
    }
    portfolio_inventory = {
        item["repository"]: (
            item["first_sweep_head"],
            item["reconciliation_head"],
            item["commits_since_first_sweep"],
        )
        for item in portfolio["repository_inventory"]
    }
    if inventory != EXPECTED_INVENTORY or portfolio_inventory != EXPECTED_INVENTORY:
        errors.append("five-repository exact-head material-change inventory differs from observed compare evidence")

    if reconciliation["disposition"]["P2"] != 5 or portfolio["portfolio_checks"]["unresolved_p2"] != 5:
        errors.append("the four missed sweeps and one missed review are not retained as five P2 loci")
    if not reconciliation["disposition"]["pilot_level_escalation_required"] or not portfolio["pilot_escalation"]["required"]:
        errors.append("repeated cadence failure is not escalated to the scheduled pilot review")
    if portfolio["pilot_escalation"]["immediate_p1"]:
        errors.append("pilot escalation is improperly represented as a present P1 authority breach")
    if reconciliation["next_deadlines"]["structural_sweep"] != "2026-08-04T23:09:00-07:00":
        errors.append("next structural deadline was reset")
    if reconciliation["next_deadlines"]["pilot_and_deep_conformance_review"] != "2026-08-09T18:21:00-07:00":
        errors.append("pilot or deep-conformance deadline was reset")
    if reconciliation["disposition"]["waiver_used"] or reconciliation["disposition"]["cadence_anchor_reset"]:
        errors.append("reconciliation silently waives or resets a missed obligation")
    if not all(value is False for value in reconciliation["claim_boundaries"].values()):
        errors.append("reconciliation inflates a prohibited claim")
    if not all(value is False for value in portfolio["claim_boundaries"].values()):
        errors.append("portfolio review inflates a prohibited claim")

    return errors


def main() -> int:
    errors = validate_bundle(load_bundle())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Administrative cadence reconciliation validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
