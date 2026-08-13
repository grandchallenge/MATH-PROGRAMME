from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "governance" / "agent_cadence_operating_plan_transform.json"
REQUIRED_NONCOMPRESSED = {
    "exact_head_review",
    "independent_review",
    "required_checks",
    "protected_merge",
    "protected_main_readback",
    "adverse_evidence_retention",
    "claim_boundaries",
    "reserved_human_authority",
}


def validate(path: Path = DEFAULT_MANIFEST) -> list[str]:
    errors: list[str] = []
    value: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    factor = Decimal(str(value.get("factor")))
    if factor != Decimal("0.1"):
        errors.append("factor must be exactly 0.1")

    source_total = int(value.get("source_total", {}).get("seconds", -1))
    target_total = int(value.get("target_total", {}).get("seconds", -1))
    if Decimal(source_total) * factor != Decimal(target_total):
        errors.append("total duration is not an exact 0.1 transform")

    phases = value.get("phase_durations", [])
    if not isinstance(phases, list) or len(phases) != 4:
        errors.append("exactly four phase durations are required")
        phases = []
    cumulative = 0
    source_phase_total = 0
    for phase in phases:
        source = int(phase.get("source_seconds", -1))
        target = int(phase.get("target_seconds", -1))
        cumulative += target
        source_phase_total += source
        if Decimal(source) * factor != Decimal(target):
            errors.append(f"phase {phase.get('phase')} is not an exact 0.1 transform")
        if int(phase.get("target_cumulative_seconds", -1)) != cumulative:
            errors.append(f"phase {phase.get('phase')} cumulative offset is incorrect")
    if source_phase_total != source_total or cumulative != target_total:
        errors.append("phase totals do not match plan totals")

    for collection_name in ("milestone_offsets", "cadence_offsets"):
        collection = value.get(collection_name, [])
        if not isinstance(collection, list) or not collection:
            errors.append(f"{collection_name} must be a non-empty array")
            continue
        for item in collection:
            source = int(item.get("source_seconds", -1))
            target = int(item.get("target_seconds", -1))
            if Decimal(source) * factor != Decimal(target):
                identity = item.get("gate", item.get("name", "unknown"))
                errors.append(f"{collection_name} {identity} is not an exact transform")

    noncompressed = set(value.get("noncompressed_requirements", []))
    missing = sorted(REQUIRED_NONCOMPRESSED - noncompressed)
    if missing:
        errors.append("missing noncompressed requirements: " + ", ".join(missing))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"agent cadence operating plan: {error}")
        return 1
    print("agent cadence operating plan deadline transform valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
