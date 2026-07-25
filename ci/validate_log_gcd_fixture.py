#!/usr/bin/env python3
"""Validate the complete LOG-GCD-001 formal-result fixture."""

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
EXPECTED_CLAIMS = {f"LOG-GCD-001-C00{i}" for i in range(1, 6)}
BASE_REPLAY = "29984406250"
FEATURE_REPLAY = "29993578051"


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
    require(lock.get("theorem_names") == ["logGcd_posSemidef"], "source_lock: upstream theorem set changed")


def check_no_trust_escape(text: str, label: str) -> None:
    require(re.search(r"\bsorry\b", text) is None, f"{label}: sorry is forbidden")
    require(re.search(r"^\s*axiom\b", text, re.MULTILINE) is None, f"{label}: local axioms are forbidden")


def check_lean_project(root: Path) -> None:
    base = (root / "LogGcd.lean").read_text(encoding="utf-8")
    feature = (root / "LogGcdFeature.lean").read_text(encoding="utf-8")
    lake = (root / "lakefile.toml").read_text(encoding="utf-8")
    manifest = load_json(root / "lake-manifest.json")
    toolchain = (root / "lean-toolchain").read_text(encoding="utf-8").strip()

    require(re.search(r"\btheorem\s+logGcd_posSemidef\b", base) is not None, "base theorem missing")
    require("Real.log (Nat.gcd" in base, "base kernel statement changed")
    require("vonMangoldt_sum.symm" in base, "base divisor-sum bridge missing")
    require("vonMangoldt_nonneg" in base, "base nonnegative-weight step missing")
    check_no_trust_escape(base, "LogGcd.lean")

    for pattern, label in (
        (r"\bdef\s+logGcdFeature\b", "feature definition"),
        (r"\bdef\s+finsuppDot\b", "dot-product definition"),
        (r"\btheorem\s+logGcd_eq_feature_inner\b", "feature identity"),
        (r"\btheorem\s+logGcdFeature_self\b", "feature norm theorem"),
    ):
        require(re.search(pattern, feature) is not None, f"LogGcdFeature.lean: {label} missing")
    require("ℕ →₀ ℝ" in feature, "LogGcdFeature.lean: Finsupp codomain missing")
    require("Real.sqrt (Λ d)" in feature, "LogGcdFeature.lean: feature weight changed")
    require("Real.log (Nat.gcd m n)" in feature, "LogGcdFeature.lean: Gram target changed")
    check_no_trust_escape(feature, "LogGcdFeature.lean")

    require(toolchain == EXPECTED_TOOLCHAIN, "lean-toolchain drift")
    require('name = "loggcd-lean"' in lake, "lakefile package drift")
    require('defaultTargets = ["LogGcd", "LogGcdFeature"]' in lake, "lakefile targets drift")
    require(lake.count('name = "LogGcd"') == 1, "lakefile base library drift")
    require(lake.count('name = "LogGcdFeature"') == 1, "lakefile feature library missing")
    require(f'rev = "{EXPECTED_MATHLIB}"' in lake, "lakefile mathlib pin drift")

    require(manifest.get("name") == "«loggcd-lean»", "lake-manifest package drift")
    packages = manifest.get("packages")
    require(isinstance(packages, list), "lake-manifest packages must be a list")
    mathlib = next((item for item in packages if isinstance(item, dict) and item.get("name") == "mathlib"), None)
    require(isinstance(mathlib, dict), "lake-manifest mathlib package missing")
    require(mathlib.get("inputRev") == EXPECTED_MATHLIB, "mathlib input revision drift")
    require(mathlib.get("rev") == EXPECTED_MATHLIB_COMMIT, "mathlib commit drift")


def check_prior_art(root: Path) -> None:
    audit = load_json(root / "prior_art_audit.json")
    require(audit.get("schema_version") == "1.0.0", "prior-art schema drift")
    require(audit.get("fixture_id") == "LOG-GCD-001", "prior-art fixture drift")
    require(audit.get("audit_date") == "2026-07-23", "prior-art date drift")
    require(
        audit.get("determinations")
        == {
            "mathematical_novelty": "NOT_SUPPORTED",
            "feature_factorization_novelty": "NOT_SUPPORTED",
            "lean_artifact_priority": "NOT_ESTABLISHED",
        },
        "prior-art determination drift",
    )
    closest = audit.get("closest_prior_art")
    require(isinstance(closest, list) and len(closest) >= 5, "prior-art source set incomplete")
    keys = {item.get("citation_key") for item in closest if isinstance(item, dict)}
    required_keys = {
        "Smith1875",
        "BeslinLigh1989",
        "BourqueLigh1993",
        "MattilaHaukkanen2019",
        "KaarniojaEtAl2018",
    }
    require(required_keys <= keys, "governing prior-art sources changed")
    prohibited = audit.get("prohibited_descriptions")
    require(isinstance(prohibited, list), "prohibited-description list missing")
    require("new theorem" in prohibited, "theorem novelty was permitted")
    require("first Lean formalization" in prohibited, "unsupported Lean priority was permitted")
    search = audit.get("formalization_search")
    require(isinstance(search, dict), "formalization-search record missing")
    require(search.get("priority_inference") == "FORBIDDEN", "bounded search was promoted into priority")

    narrative = (root / "PRIOR_ART_AUDIT.md").read_text(encoding="utf-8")
    for required in (
        "Mathematical novelty | **NOT SUPPORTED**",
        "Feature-factorization novelty | **NOT SUPPORTED**",
        "Lean-artifact priority | **NOT ESTABLISHED**",
        "Mattila and Pentti Haukkanen",
        "No earlier public Lean formalization was located",
    ):
        require(required in narrative, f"PRIOR_ART_AUDIT.md: missing {required!r}")


def check_claim_ledger(root: Path) -> None:
    ledger = load_json(root / "claim_ledger.json")
    require(ledger.get("schema_version") == "1.1.0", "claim-ledger schema drift")
    require(ledger.get("fixture_id") == "LOG-GCD-001", "claim-ledger fixture drift")
    claims = ledger.get("claims")
    require(isinstance(claims, list), "claim ledger claims must be a list")
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    require(len(by_id) == len(claims), "claim IDs must be unique")
    require(set(by_id) == EXPECTED_CLAIMS, "claim set changed")

    base = by_id["LOG-GCD-001-C001"]
    require(
        (base.get("claim_class"), base.get("support_type"), base.get("status"))
        == ("FORMALIZED", "LEAN_FORMALIZATION", "CERTIFIED"),
        "C001 certification drift",
    )
    require(base.get("formal_theorem") == "logGcd_posSemidef", "C001 theorem drift")
    require(BASE_REPLAY in base.get("certification_evidence", ""), "C001 replay evidence missing")

    interpretation = by_id["LOG-GCD-001-C002"]
    require(interpretation.get("status") == "AUDITED", "C002 status drift")
    require(interpretation.get("depends_on") == ["LOG-GCD-001-C001"], "C002 dependency drift")

    feature = by_id["LOG-GCD-001-C003"]
    require(
        (feature.get("claim_class"), feature.get("support_type"), feature.get("status"))
        == ("FORMALIZED", "LEAN_FORMALIZATION", "CERTIFIED"),
        "C003 must remain a certified Lean formalization",
    )
    require(feature.get("formal_definition") == "logGcdFeature", "C003 definition drift")
    require(feature.get("formal_theorem") == "logGcd_eq_feature_inner", "C003 theorem drift")
    require(feature.get("artifact") == "LogGcdFeature.lean", "C003 artifact drift")
    require(FEATURE_REPLAY in feature.get("certification_evidence", ""), "C003 replay evidence missing")

    strict = by_id["LOG-GCD-001-C004"]
    require(
        (strict.get("claim_class"), strict.get("support_type"), strict.get("status"))
        == ("REFUTED", "EXACT_COUNTEREXAMPLE", "AUDITED"),
        "C004 strict-PD boundary drift",
    )
    require(strict.get("counterexample", {}).get("point") == 1, "C004 counterexample drift")

    novelty = by_id["LOG-GCD-001-C005"]
    require(
        (novelty.get("claim_class"), novelty.get("support_type"), novelty.get("status"))
        == ("LITERATURE_DERIVED", "PRIOR_ART_AUDIT", "AUDITED"),
        "C005 prior-art claim drift",
    )
    require("not supported" in novelty.get("claim_text", ""), "C005 novelty determination missing")

    exclusions = ledger.get("claims_explicitly_not_made")
    require(isinstance(exclusions, list) and len(exclusions) >= 6, "claim exclusions incomplete")
    require(any("novelty is not supported" in item for item in exclusions), "negative novelty determination missing")
    require(any("first-Lean-formalization" in item for item in exclusions), "formalization-priority boundary missing")
    require(any("No strict" in item for item in exclusions), "strict-PD boundary missing")


def check_agent_review(root: Path) -> None:
    review = load_yaml(root / "agent_review.yaml")
    schema = load_json(PROGRAMME_ROOT / "schemas" / "agent_review.schema.json")
    try:
        jsonschema.Draft202012Validator(schema).validate(review)
    except jsonschema.ValidationError as exc:
        raise FixtureError(f"agent_review.yaml: schema violation: {exc.message}") from exc

    artifact = review["artifact"]
    require(artifact.get("id") == "CERT-LOG-GCD-001", "agent-review artifact drift")
    require(artifact.get("pillar") == "MATHCERT", "agent-review pillar drift")
    require(artifact.get("status") == "certified", "completed artifact was demoted")
    require(
        review["amanuensis_control"]["artifact_ledger"]["entry_id"] == "CERT-LOG-GCD-001",
        "artifact-ledger entry mismatch",
    )
    evidence = review["amanuensis_control"]["review_provenance"]["evidence_refs"]
    for required in (
        "fixtures/formal/LOG-GCD-001/LogGcdFeature.lean",
        "fixtures/formal/LOG-GCD-001/PRIOR_ART_AUDIT.md",
        "fixtures/formal/LOG-GCD-001/prior_art_audit.json",
        f"MATH-PROGRAMME workflow run {FEATURE_REPLAY}",
    ):
        require(required in evidence, f"review evidence missing: {required}")
    require(review["unresolved_obligations"] == [], "resolved obligations were reintroduced")
    promotion = review["promotion"]
    require(promotion.get("ready_for_next_stage") is True, "completed artifact is not promoted")
    require(promotion.get("blockers") == [], "completed artifact retains blockers")
    require(promotion.get("certification_route") == "LEAN_FORMALIZATION", "certification route drift")


def check_readme(root: Path) -> None:
    text = (root / "README.md").read_text(encoding="utf-8")
    for required in (
        "Result-status box",
        "Theorem spine",
        "Feature realization",
        "Prior-art determination",
        "Claim boundary",
        "Trust quartet",
        "positive **semidefiniteness**",
        "logGcd_eq_feature_inner",
        "NOT SUPPORTED",
        FEATURE_REPLAY,
    ):
        require(required in text, f"README.md: missing {required!r}")


def validate(root: Path = DEFAULT_ROOT) -> None:
    require(root.is_dir(), f"{root}: fixture directory missing")
    for name in (
        "README.md",
        "LogGcd.lean",
        "LogGcdFeature.lean",
        "PRIOR_ART_AUDIT.md",
        "prior_art_audit.json",
        "lakefile.toml",
        "lake-manifest.json",
        "lean-toolchain",
        "source_lock.json",
        "claim_ledger.json",
        "agent_review.yaml",
    ):
        require((root / name).is_file(), f"{root / name}: required artifact missing")
    check_source_lock(root)
    check_lean_project(root)
    check_prior_art(root)
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
