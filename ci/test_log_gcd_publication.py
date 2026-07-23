#!/usr/bin/env python3
"""Adversarial rejection tests for the LOG-GCD publication contract."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from validate_log_gcd_publication import PublicationError, validate

SOURCE = Path(__file__).resolve().parents[1] / "fixtures" / "formal" / "LOG-GCD-001"


def materialize() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory()
    target = Path(temporary.name) / "LOG-GCD-001"
    shutil.copytree(SOURCE, target)
    return temporary, target


def update_json(path: Path, mutator) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutator(value)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rejected(mutator) -> None:
    temporary, target = materialize()
    try:
        mutator(target)
        try:
            validate(target)
        except PublicationError:
            return
        raise AssertionError("invalid LOG-GCD publication was accepted")
    finally:
        temporary.cleanup()


def main() -> int:
    validate(SOURCE)

    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(status="CANDIDATE"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(source_commit="0" * 40),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["published_claims"][1].update(required_status="AUDITED"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["published_claims"].pop(),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["boundary_claims"].pop(),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(permitted_description="A novel logarithmic GCD kernel."),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["prohibited_descriptions"].remove("first Lean formalization"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["certification_evidence"].pop(),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(canonical_page="docs/UNREVIEWED_CLAIM.md"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["publication_gate"].update(prior_art_audit_complete=False),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(publication_date=None),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(publication_date="2026-07-22"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.pop("publication_ci_evidence"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value.update(publication_ci_evidence="fabricated"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "publication_manifest.json",
            lambda value: value["publication_gate"].update(
                promotion_condition="Publication pending."
            ),
        )
    )
    rejected(
        lambda root: update_json(
            root / "claim_ledger.json",
            lambda value: value["claims"][2].update(status="AUDITED"),
        )
    )
    rejected(
        lambda root: update_json(
            root / "prior_art_audit.json",
            lambda value: value["determinations"].update(mathematical_novelty="SUPPORTED"),
        )
    )

    print("adversarial LOG-GCD publication tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
