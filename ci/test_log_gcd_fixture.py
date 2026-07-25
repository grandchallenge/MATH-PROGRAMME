#!/usr/bin/env python3
"""Adversarial rejection tests for LOG-GCD-001."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import yaml

from validate_log_gcd_fixture import FixtureError, validate

SOURCE = Path(__file__).resolve().parents[1] / "fixtures" / "formal" / "LOG-GCD-001"


def materialize() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory()
    target = Path(temporary.name) / "LOG-GCD-001"
    shutil.copytree(SOURCE, target)
    return temporary, target


def rejected(mutator) -> None:
    temporary, target = materialize()
    try:
        mutator(target)
        try:
            validate(target)
        except FixtureError:
            return
        raise AssertionError("invalid LOG-GCD fixture was accepted")
    finally:
        temporary.cleanup()


def update_json(path: Path, mutator) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutator(value)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_yaml(path: Path, mutator) -> None:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutator(value)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> int:
    validate(SOURCE)

    rejected(
        lambda root: update_json(
            root / "source_lock.json",
            lambda value: value.update(source_commit="0" * 40),
        )
    )
    rejected(
        lambda root: (root / "LogGcd.lean").write_text(
            (root / "LogGcd.lean").read_text(encoding="utf-8").replace(
                "theorem logGcd_posSemidef", "theorem removed_result"
            ),
            encoding="utf-8",
        )
    )
    rejected(
        lambda root: (root / "LogGcdFeature.lean").write_text(
            (root / "LogGcdFeature.lean").read_text(encoding="utf-8").replace(
                "theorem logGcd_eq_feature_inner", "theorem removed_feature_identity"
            ),
            encoding="utf-8",
        )
    )
    rejected(lambda root: (root / "LogGcdFeature.lean").unlink())
    rejected(
        lambda root: update_json(
            root / "claim_ledger.json",
            lambda value: value["claims"][2].update(status="PENDING_TARGET_CI"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "claim_ledger.json",
            lambda value: value["claims"].pop(),
        )
    )
    rejected(
        lambda root: update_json(
            root / "prior_art_audit.json",
            lambda value: value["determinations"].update(mathematical_novelty="SUPPORTED"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "prior_art_audit.json",
            lambda value: value["formalization_search"].update(priority_inference="FIRST_FORMALIZATION"),
        )
    )
    rejected(
        lambda root: update_yaml(
            root / "agent_review.yaml",
            lambda value: value["unresolved_obligations"].append(
                {
                    "id": "LOG-GCD-001-O999",
                    "owner": "Formalist",
                    "description": "Fabricated residual obligation.",
                    "severity": "high",
                    "blocking": True,
                }
            ),
        )
    )
    rejected(
        lambda root: update_yaml(
            root / "agent_review.yaml",
            lambda value: value["promotion"].update(
                ready_for_next_stage=False,
                blockers=["LOG-GCD-001-O999"],
            ),
        )
    )
    rejected(
        lambda root: update_yaml(
            root / "agent_review.yaml",
            lambda value: value["artifact"].update(status="ready_for_certification"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "source_lock.json",
            lambda value: value["source_license"].update(spdx="MIT"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "lake-manifest.json",
            lambda value: value["packages"][0].update(rev="0" * 40),
        )
    )

    print("adversarial LOG-GCD fixture tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
