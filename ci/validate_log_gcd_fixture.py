#!/usr/bin/env python3
"""Validate the LOG-GCD-001 formal-result fixture."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml

DEFAULT_ROOT = Path("fixtures/formal/LOG-GCD-001")
PROGRAMME_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SOURCE_COMMIT = "d2038c7b09fe849f236d6428d7159b5a40f9aed7"
EXPECTED_SOURCE_BLOB = "fd5b136ed32c6d48f5f71381ccf4b69d1329088f"
EXPECTED_LICENSE_BLOB = "0e259d42c996742e9e3cba14c677129b2c1b6311"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.33.0-rc1"
EXPECTED_MATHLIB = "v4.33.0-rc1"
EXPECTED_CLAIMS = {
    "LOG-GCD-001-C001",
    "LOG-GCD-001-C002",
    "LOG-GCD-001-C003",
    "LOG-GCD-001-C004",
}


class FixtureError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FixtureError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FixtureError(f"{path}: cannot load JSON: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level value must be an object")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise FixtureError(f"{path}: cannot load YAML: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level value must be an object")
    return value


def check_source_lock(root: Path) -> None:
    lock = load_json(root / "source_lock.json")
    require(lock.get("schema_version") == "1.0.0", "source_lock: unsupported schema version")
    require(lock.get("fixture_id") == "LOG-GCD-001", "source_lock: wrong fixture ID")
    require(
        lock.get("source_repository") == "irregular-rhomboid/log-gcd-lean",
        "source_lock: wrong repository",
    )
    require(lock.get("source_commit") == EXPECTED_SOURCE_COMMIT, "source_lock: commit drift")
    require(
        lock.get("source_formal_file") == "Loggcd/Lean/loggcd.lean",
        "source_lock: wrong upstream formal file",
    )
    require(
        lock.get("source_formal_file_git_blob_sha") == EXPECTED_SOURCE_BLOB,
        "source_lock: theorem blob drift",
    )
    license_record = lock.get("source_license")
    require(isinstance(license_record, dict), "source_lock: missing license record")
    require(license_record.get("spdx") == "CC0-1.0", "source_lock: wrong license")
    require(
        license_record.get("git_blob_sha") == EXPECTED_LICENSE_BLOB,
        "source_lock: license blob drift",
    )
    require(
        lock.get("ingestion_mode") == "VENDORED_CC0_ADAPTATION",
        "source_lock: wrong ingestion mode",
    )
    require(lock.get("theorem_names") == ["logGcd_posSemidef"], "source_lock: theorem set changed")
    require(lock.get("lean_toolchain") == EXPECTED_TOOLCHAIN, "source_lock: toolchain drift")
    require(lock.get("mathlib_revision") == EXPECTED_MATHLIB, "source_lock: mathlib drift")


def check_lean_project(root: Path) -> None:
    lean_path = root / "LogGcd.lean"
    lake_path = root / "lakefile.toml"
    toolchain_path = root / "lean-toolchain"

    lean = lean_path.read_text(encoding="utf-8")
    lake = lake_path.read_text(encoding="utf-8")
    toolchain = toolchain_path.read_text(encoding="utf-8").strip()

    require(
        re.search(r"\btheorem\s+logGcd_posSemidef\b", lean) is not None,
        "LogGcd.lean: theorem declaration missing",
    )
    require("Real.log (Nat.gcd" in lean, "LogGcd.lean: kernel statement changed")
    require("vonMangoldt_sum.symm" in lean, "LogGcd.lean: divisor-sum bridge missing")
    require("vonMangoldt_nonneg" in lean, "LogGcd.lean: nonnegative-weight step missing")
    require(re.search(r"\bsorry\b", lean) is None, "LogGcd.lean: sorry is forbidden")
    require(re.search(r"^\s*axiom\b", lean, re.MULTILINE) is None, "LogGcd.lean: local axioms are forbidden")
    require(toolchain == EXPECTED_TOOLCHAIN, "lean-toolchain: unexpected toolchain")
    require('name = "log-gcd-gcl"' in lake, "lakefile: wrong package name")
    require('name = "LogGcd"' in lake, "lakefile: LogGcd library missing")
    require(f'rev = "{EXPECTED_MATHLIB}"' in lake, "lakefile: mathlib pin drift")


def check_claim_ledger(root: Path) -> None:
    ledger = load_json(root / "claim_ledger.json")
    require(ledger.get("fixture_id") == "LOG-GCD-001", "claim ledger: wrong fixture ID")
    claims = ledger.get("claims")
    require(isinstance(claims, list), "claim ledger: claims must be a list")
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    require(len(by_id) == len(claims), "claim ledger: claim IDs must be unique")
    require(set(by_id) == EXPECTED_CLAIMS, "claim ledger: claim set changed")

    formal = by_id["LOG-GCD-001-C001"]
    require(
        (formal.get("claim_class"), formal.get("support_type"), formal.get("status"))
        == ("FORMALIZED", "LEAN_FORMALIZATION", "PENDING_TARGET_CI"),
        "C001 must remain a Lean formalization pending target CI",
    )
    require(formal.get("formal_theorem") == "logGcd_posSemidef", "C001 theorem drift")

    interpretation = by_id["LOG-GCD-001-C002"]
    require(
        interpretation.get("depends_on") == ["LOG-GCD-001-C001"],
        "C002 must depend on the formal theorem",
    )
    require(interpretation.get("status") == "AUDITED", "C002 interpretation status drift")

    feature = by_id["LOG-GCD-001-C003"]
    require(
        feature.get("status") == "AUDITED_NOT_FORMALIZED_AS_FEATURE_MAP",
        "C003 must not be promoted to a formal feature map",
    )

    strict = by_id["LOG-GCD-001-C004"]
    require(
        (strict.get("claim_class"), strict.get("support_type"), strict.get("status"))
        == ("REFUTED", "EXACT_COUNTEREXAMPLE", "AUDITED"),
        "C004 strict-positive-definiteness boundary changed",
    )
    require(strict.get("counterexample", {}).get("point") == 1, "C004 counterexample changed")

    exclusions = ledger.get("claims_explicitly_not_made")
    require(isinstance(exclusions, list) and len(exclusions) >= 5, "claim ledger: exclusions incomplete")
    require(
        any("No novelty" in item for item in exclusions),
        "claim ledger: novelty boundary missing",
    )
    require(
        any("No strict" in item for item in exclusions),
        "claim ledger: strict-PD boundary missing",
    )


def check_agent_review(root: Path) -> None:
    review = load_yaml(root / "agent_review.yaml")
    schema_path = PROGRAMME_ROOT / "schemas" / "agent_review.schema.json"
    schema = load_json(schema_path)
    try:
        jsonschema.Draft202012Validator(schema).validate(review)
    except jsonschema.ValidationError as exc:
        raise FixtureError(f"agent_review.yaml: schema violation: {exc.message}") from exc

    require(review["artifact"]["id"] == "CERT-LOG-GCD-001", "agent review: wrong artifact ID")
    require(review["artifact"]["pillar"] == "MATHCERT", "agent review: wrong pillar")
    require(
        review["amanuensis_control"]["artifact_ledger"]["entry_id"] == "CERT-LOG-GCD-001",
        "agent review: artifact ledger entry mismatch",
    )
    obligations = {
        item["id"]: item
        for item in review["unresolved_obligations"]
        if isinstance(item, dict) and "id" in item
    }
    require("LOG-GCD-001-O001" in obligations, "agent review: CI obligation missing")
    require(obligations["LOG-GCD-001-O001"]["blocking"] is True, "agent review: CI must block promotion")
    require(review["promotion"]["ready_for_next_stage"] is False, "agent review: premature promotion")
    require(
        "LOG-GCD-001-O001" in review["promotion"]["blockers"],
        "agent review: CI blocker not linked",
    )


def check_readme(root: Path) -> None:
    text = (root / "README.md").read_text(encoding="utf-8")
    for required in (
        "Result-status box",
        "Theorem spine",
        "Claim boundary",
        "Provenance",
        "Trust quartet",
        "Next executable step",
        "positive **semidefiniteness**",
    ):
        require(required in text, f"README.md: missing {required!r}")


def validate(root: Path = DEFAULT_ROOT) -> None:
    require(root.is_dir(), f"{root}: fixture directory missing")
    for name in (
        "README.md",
        "LogGcd.lean",
        "lakefile.toml",
        "lean-toolchain",
        "source_lock.json",
        "claim_ledger.json",
        "agent_review.yaml",
    ):
        require((root / name).is_file(), f"{root / name}: required artifact missing")
    check_source_lock(root)
    check_lean_project(root)
    check_claim_ledger(root)
    check_agent_review(root)
    check_readme(root)


def main(argv: list[str]) -> int:
    fixture_root = Path(argv[1]) if len(argv) == 2 else DEFAULT_ROOT
    try:
        validate(fixture_root)
    except FixtureError as exc:
        print(f"LOG-GCD fixture rejected: {exc}", file=sys.stderr)
        return 1
    print(f"LOG-GCD fixture checked: {fixture_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
