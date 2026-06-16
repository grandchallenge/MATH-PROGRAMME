#!/usr/bin/env python3
"""Adversarial tests for the Chaidez pedagogy contract validator."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from validate_chaidez_pedagogy import DEFAULT_CONTRACT, validate


def write_case(directory: Path, name: str, data: dict) -> Path:
    path = directory / f"{name}.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def require_rejected(directory: Path, name: str, data: dict) -> None:
    errors = validate(write_case(directory, name, data))
    if not errors:
        raise AssertionError(f"adversarial case was accepted: {name}")


def main() -> int:
    canonical = json.loads(DEFAULT_CONTRACT.read_text(encoding="utf-8"))
    if validate(DEFAULT_CONTRACT):
        raise AssertionError("canonical contract is invalid")

    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)

        case = copy.deepcopy(canonical)
        case["campaign_unit"] = "WORK_PACKAGE_LIST"
        require_rejected(directory, "wrong_campaign_unit", case)

        case = copy.deepcopy(canonical)
        case["trust_quartet"].pop()
        require_rejected(directory, "missing_trust_question", case)

        case = copy.deepcopy(canonical)
        case["computation_classes"][2] = "NUMERICAL_EVIDENCE"
        require_rejected(directory, "blurred_computation_class", case)

        case = copy.deepcopy(canonical)
        case["proof_debt_categories"].remove("SEMANTIC_CORRESPONDENCE")
        require_rejected(directory, "missing_semantic_debt", case)

        case = copy.deepcopy(canonical)
        case["spine_node_fields"].remove("dependencies")
        require_rejected(directory, "missing_dependencies", case)

        case = copy.deepcopy(canonical)
        case["escalation_gate"]["proof_debt_register_current"] = False
        require_rejected(directory, "disabled_debt_gate", case)

        case = copy.deepcopy(canonical)
        case["required_work_package_artifacts"].remove("NEXT_EXECUTABLE_STEP")
        require_rejected(directory, "missing_next_step", case)

    print("all adversarial Chaidez pedagogy tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
