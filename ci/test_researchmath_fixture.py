#!/usr/bin/env python3
"""Adversarial tests for ResearchMath intake fixture RM-DIO-004."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from validate_researchmath_fixture import ResearchMathFixtureError, check_fixture

SOURCE = Path("fixtures/researchmath/RM-DIO-004")


def mutate_file(root: Path, relative: str, mutator) -> None:
    path = root / relative
    data = json.loads(path.read_text(encoding="utf-8"))
    mutator(data)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rejected(mutator) -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "RM-DIO-004"
        shutil.copytree(SOURCE, root)
        mutator(root)
        try:
            check_fixture(root)
        except ResearchMathFixtureError:
            return
    raise AssertionError("invalid ResearchMath intake fixture was accepted")


def main() -> int:
    check_fixture()
    rejected(lambda root: mutate_file(root, "source_row.json", lambda data: data.update(open_status="solved")))
    rejected(lambda root: mutate_file(root, "source_row.json", lambda data: data.pop("question_link")))
    rejected(lambda root: mutate_file(root, "problem_card.json", lambda data: data.update(source_row_sha256="0" * 64)))
    rejected(lambda root: mutate_file(root, "problem_card.json", lambda data: data["status_audit"].update(promotion_allowed=True)))
    rejected(lambda root: mutate_file(root, "problem_card.json", lambda data: data["algebraic_extraction"]["equations"][0]["canonical_polynomial"][2].update(coefficient=[1, 1])))
    rejected(lambda root: mutate_file(root, "problem_card.json", lambda data: data["semantic_boundary"].update(excluded_inference="")))
    rejected(lambda root: mutate_file(root, "mathsolve_handoff.json", lambda data: data.update(handoff_status="SOLVED")))
    rejected(lambda root: mutate_file(root, "mathsolve_handoff.json", lambda data: data["work_package_seed"].pop("first_executable_step")))
    rejected(lambda root: mutate_file(root, "claim_ledger.json", lambda data: data["claims"][2].update(status="CERTIFIED")))
    rejected(lambda root: mutate_file(root, "claim_ledger.json", lambda data: data["forbidden_promotions"].remove("SOLVED")))
    print("adversarial ResearchMath intake tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
