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
EXPECTED_MANIFEST_BLOB = "99d43177d509c4ceb340c8b2e6330e9c75233169"
EXPECTED_LICENSE_BLOB = "0e259d42c996742e9e3cba14c677129b2c1b6311"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.33.0-rc1"
EXPECTED_MATHLIB = "v4.33.0-rc1"
EXPECTED_MATHLIB_COMMIT = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_CLAIMS = {f"LOG-GCD-001-C00{i}" for i in range(1, 5)}


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
    expected = {
        "schema_version": "1.0.0",
        "fixture_id": "LOG-GCD-001",
        "source_repository": "irregular-rhomboid/log-gcd-lean",
        "source_commit": EXPECTED_SOURCE_COMMIT,
        "source_formal_file": "Loggcd/Lean/loggcd.lean",
        "source_formal_file_git_blob_sha": EXPECTED_SOURCE_BLOB,
        "source_manifest_file": "lake-manifest.json",
        "source_manifest_git_blob_sha": EXPECTED_MANIFEST_BLOB,
        "ingestion_mode": "VENDORED_CC0_ADAPTATION",
        "lean_toolchain": EXPECTED_TOOLCHAIN,
        "mathlib_revision": EXPECTED_MATHLIB,
        "mathlib_commit": EXPECTED_MATHLIB_COMMIT,
    }
    for key, value in expected.items():
        require(lock.get(key) == value, f"source_lock: {key} drift")
    license_record = lock.get("source_license")
    require(isinstance(license_record, dict), "source_lock: missing license record")
    require(license_record.get("spdx") == "CC0-1.0", "source_lock: wrong license")
    require(license_record.get("git_blob_sha") == EXPECTED_LICENSE_BLOB, "source_lock: license blob drift")
    require(lock.get("theorem_names") == ["logGcd_posSemidef"], "source_lock: theorem set changed")


def check_lean_project(root: Path) -> None:
    lean = (root / "LogGcd.lean").read_text(encoding="utf-8")
    lake = (root / "lakefile.toml").read_text(encoding="utf-8")
    manifest = load_json(root / "lake-manifest.json")
    toolchain = (root / "lean-toolchain").read_text(encoding="utf-8").strip()

    require(re.search(r"\btheorem\s+logGcd_posSemidef\b", lean) is not None, "Lean theorem missing")
    require("Real.log (Nat.gcd" in lean, "Lean kernel statement changed")
    require("vonMangoldt_sum.symm" in lean, "Lean divisor-sum bridge missing")
    require("vonMangoldt_nonneg" in lean, "Lean nonnegative-weight step missing")
    require(re.search(r"\bsorry\b", lean) is None, "Lean sorry is forbidden")
    require(re.search(r"^\s*axiom\b", lean, re.MULTILINE) is None, "local Lean axioms are forbidden")
    require(toolchain == EXPECTED_TOOLCHAIN, "lean-toolchain drift")
    require('name = "loggcd-lean"' in lake, "lakefile package drift")
    require('name = "LogGcd"' in lake, "lakefile library missing")
    require(f'rev = "{EXPECTED_MATHLIB}"' in lake, "lakefile mathlib pin drift")
    require(manifest.get("name") == "«loggcd-lean»", "lake-manifest root package drift")
    packages = manifest.get("packages")
    require(isinstance(packages, list), "lake-manifest packages must be a list")
    mathlib = next((p for p in packages if isinstance(p, dict) and p.get("name") == "mathlib"), None)
    require(isinstance(mathlib, dict), "lake-manifest mathlib package missing")
    require(mathlib.get("inputRev") == EXPECTED_MATHLIB, "mathlib input revision drift")
    require(mathlib.get("rev") == EXPECTED_MATHLIB_COMMIT, "mathlib commit drift")


def check_claim_ledger(root: Path) -> None:
    ledger = load_json(root / "claim_ledger.json")
    require(ledger.get("fixture_id") == "LOG-GCD-001", "claim ledger fixture ID drift")
    claims = ledger.get("claims")
    require(isinstance(claims, list), "claim ledger claims must be a list")
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    require(len(by_id) == len(claims), "claim IDs must be unique")
    require(set(by_id) == EXPECTED_CLAIMS, "claim set changed")

    formal = by_id["LOG-GCD-001-C001"]
    require(
        (formal.get("claim_class"), formal.get("support_type"), formal.get("status"))
        == ("FORMALIZED", "LEAN_FORMALIZATION", "CERTIFIED"),
        "C001 must remain a certified Lean formalization",
    )
    require(formal.get("formal_theorem") == "logGcd_posSemidef", "C001 theorem drift")
    require("29984406250" in formal.get("certification_evidence", ""), "C001 CI evidence missing")

    require(by_id["LOG-GCD-001-C002"].get("depends_on") == ["LOG-GCD-001-C001"], "C002 dependency drift")
    require(by_id["LOG-GCD-001-C002"].get("status") == "AUDITED", "C002 status drift")
    require(
        by_id["LOG-GCD-001-C003"].get("status") == "AUDITED_NOT_FORMALIZED_AS_FEATURE_MAP",
        "C003 feature-map boundary drift",
    )
    strict = by_id["LOG-GCD-001-C004"]
    require(
        (strict.get("claim_class"), strict.get("support_type"), strict.get("status"))
        == ("REFUTED", "EXACT_COUNTEREXAMPLE", "AUDITED"),
        "C004 strict-PD boundary drift",
    )
    require(strict.get("counterexample", {}).get("point") == 1, "C004 counterexample drift")
    exclusions = ledger.get("claims_explicitly_not_made")
    require(isinstance(exclusions, list) and len(exclusions) >= 5, "claim exclusions incomplete")
    require(any("No novelty" in item for item in exclusions), "novelty boundary missing")
    require(any("No strict" in item for item in exclusions), "strict-PD boundary missing")


def check_agent_review(root: Path) -> None:
    review = load_yaml(root / "agent_review.yaml")
    schema = load_json(PROGRAMME_ROOT / "schemas" / "agent_review.schema.json")
    try:
        jsonschema.Draft202012Validator(schema).validate(review)
    except jsonschema.ValidationError as exc:
        raise FixtureError(f"agent_review.yaml: schema violation: {exc.message}") from exc

    require(review["artifact"] == {
        "id": "CERT-LOG-GCD-001",
        "type": "certificate",
        "title": "Positive semidefiniteness of the logarithmic GCD kernel",
        "pillar": "MATHCERT",
        "status": "certified",
    }, "agent review artifact record drift")
    require(
        review["amanuensis_control"]["artifact_ledger"]["entry_id"] == "CERT-LOG-GCD-001",
        "artifact-ledger entry mismatch",
    )
    obligations = {item["id"]: item for item in review["unresolved_obligations"]}
    require("LOG-GCD-001-O001" not in obligations, "resolved CI obligation remains open")
    require(set(obligations) == {"LOG-GCD-001-O002", "LOG-GCD-001-O003"}, "obligation set drift")
    require(not any(item["blocking"] for item in obligations.values()), "nonblocking debt became blocking")
    require(review["promotion"]["ready_for_next_stage"] is True, "certified fixture not promoted")
    require(review["promotion"]["blockers"] == [], "certified fixture has promotion blockers")
    require(review["promotion"]["certification_route"] == "LEAN_FORMALIZATION", "certification route drift")


def check_readme(root: Path) -> None:
    text = (root / "README.md").read_text(encoding="utf-8")
    for required in (
        "Result-status box", "Theorem spine", "Claim boundary", "Provenance",
        "Trust quartet", "Next executable step", "positive **semidefiniteness**", "CERTIFIED",
    ):
        require(required in text, f"README.md: missing {required!r}")


def validate(root: Path = DEFAULT_ROOT) -> None:
    require(root.is_dir(), f"{root}: fixture directory missing")
    for name in (
        "README.md", "LogGcd.lean", "lakefile.toml", "lake-manifest.json",
        "lean-toolchain", "source_lock.json", "claim_ledger.json", "agent_review.yaml",
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
