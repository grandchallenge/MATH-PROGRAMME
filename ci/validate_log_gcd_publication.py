#!/usr/bin/env python3
"""Validate the publication-stage contract for LOG-GCD-001."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROGRAMME_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = PROGRAMME_ROOT / "fixtures" / "formal" / "LOG-GCD-001"

EXPECTED_SOURCE_COMMIT = "81e391ba26352b0291dd02495157fe313dddca46"
EXPECTED_STATUS = "CANDIDATE"
EXPECTED_PUBLICATION_DATE = None
EXPECTED_PUBLICATION_EVIDENCE = None
EXPECTED_PUBLISHED = {"LOG-GCD-001-C001", "LOG-GCD-001-C003"}
EXPECTED_BOUNDARIES = {"LOG-GCD-001-C004", "LOG-GCD-001-C005"}
EXPECTED_DESCRIPTION = (
    "A GCL-certified Lean formalization and explicit Finsupp realization of a "
    "classical GCD-matrix positivity criterion."
)
EXPECTED_PROHIBITED = {
    "new theorem",
    "novel kernel",
    "first proof",
    "first feature representation",
    "first Lean formalization",
    "strictly positive definite on all positive natural numbers",
}
EXPECTED_EVIDENCE = {
    "MATH-PROGRAMME workflow run 29984406250",
    "MATH-PROGRAMME workflow run 29993578051",
    "MATH-PROGRAMME workflow run 29994235171",
}


class PublicationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PublicationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationError(f"{path}: cannot load JSON: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level value must be an object")
    return value


def check_manifest(root: Path) -> dict[str, Any]:
    manifest = load_json(root / "publication_manifest.json")
    expected = {
        "schema_version": "1.0.0",
        "publication_id": "PUB-LOG-GCD-001",
        "fixture_id": "LOG-GCD-001",
        "source_artifact_id": "CERT-LOG-GCD-001",
        "stage": "PUBLICATION",
        "status": EXPECTED_STATUS,
        "title": "The logarithmic GCD kernel as certified divisor-feature geometry",
        "canonical_page": "docs/LOG_GCD_PUBLICATION.md",
        "showcase_page": "docs/SHOWCASE.md#fixture-003-the-logarithmic-gcd-kernel",
        "publication_date": EXPECTED_PUBLICATION_DATE,
        "source_commit": EXPECTED_SOURCE_COMMIT,
    }
    for key, value in expected.items():
        require(manifest.get(key) == value, f"publication manifest: {key} drift")

    if EXPECTED_PUBLICATION_EVIDENCE is None:
        require("publication_ci_evidence" not in manifest, "candidate publication has fabricated CI evidence")
    else:
        require(
            manifest.get("publication_ci_evidence") == EXPECTED_PUBLICATION_EVIDENCE,
            "publication CI evidence drift",
        )

    published = manifest.get("published_claims")
    require(isinstance(published, list), "published_claims must be a list")
    published_ids = {item.get("claim_id") for item in published if isinstance(item, dict)}
    require(len(published_ids) == len(published), "published claim IDs must be unique")
    require(published_ids == EXPECTED_PUBLISHED, "published claim set changed")
    for item in published:
        require(item.get("required_status") == "CERTIFIED", "publication includes an uncertified claim")
        statement = item.get("public_statement")
        require(isinstance(statement, str) and statement.strip(), "published claim lacks public statement")

    boundaries = manifest.get("boundary_claims")
    require(isinstance(boundaries, list), "boundary_claims must be a list")
    boundary_ids = {item.get("claim_id") for item in boundaries if isinstance(item, dict)}
    require(len(boundary_ids) == len(boundaries), "boundary claim IDs must be unique")
    require(boundary_ids == EXPECTED_BOUNDARIES, "publication boundary set changed")
    for item in boundaries:
        require(item.get("required_status") == "AUDITED", "publication boundary status drift")
        effect = item.get("public_effect")
        require(isinstance(effect, str) and effect.startswith("Do not"), "boundary lacks prohibitive effect")

    require(manifest.get("permitted_description") == EXPECTED_DESCRIPTION, "permitted description drift")
    prohibited = manifest.get("prohibited_descriptions")
    require(isinstance(prohibited, list), "prohibited_descriptions must be a list")
    require(set(prohibited) == EXPECTED_PROHIBITED, "publication prohibition set changed")
    evidence = manifest.get("certification_evidence")
    require(isinstance(evidence, list), "certification_evidence must be a list")
    require(set(evidence) == EXPECTED_EVIDENCE, "publication certification evidence drift")

    gate = manifest.get("publication_gate")
    require(isinstance(gate, dict), "publication gate missing")
    for key in (
        "claim_ledger_certified",
        "prior_art_audit_complete",
        "showcase_entry_required",
        "strict_docs_build_required",
        "adversarial_policy_required",
    ):
        require(gate.get(key) is True, f"publication gate disabled: {key}")
    promotion = gate.get("promotion_condition")
    require(isinstance(promotion, str) and "PUBLISHED" in promotion, "publication promotion condition missing")
    return manifest


def check_claim_support(root: Path, manifest: dict[str, Any]) -> None:
    ledger = load_json(root / "claim_ledger.json")
    claims = ledger.get("claims")
    require(isinstance(claims, list), "claim ledger claims must be a list")
    by_id = {item.get("claim_id"): item for item in claims if isinstance(item, dict)}

    for item in manifest["published_claims"]:
        claim_id = item["claim_id"]
        require(claim_id in by_id, f"published claim missing from ledger: {claim_id}")
        require(by_id[claim_id].get("status") == "CERTIFIED", f"published claim is not certified: {claim_id}")

    for item in manifest["boundary_claims"]:
        claim_id = item["claim_id"]
        require(claim_id in by_id, f"boundary claim missing from ledger: {claim_id}")
        require(by_id[claim_id].get("status") == "AUDITED", f"boundary claim is not audited: {claim_id}")

    audit = load_json(root / "prior_art_audit.json")
    require(audit.get("determinations") == {
        "mathematical_novelty": "NOT_SUPPORTED",
        "feature_factorization_novelty": "NOT_SUPPORTED",
        "lean_artifact_priority": "NOT_ESTABLISHED",
    }, "publication is detached from the negative prior-art determination")


def check_public_pages(manifest: dict[str, Any]) -> None:
    page = PROGRAMME_ROOT / manifest["canonical_page"]
    showcase_path = manifest["showcase_page"].split("#", 1)[0]
    showcase = PROGRAMME_ROOT / showcase_path
    nav = PROGRAMME_ROOT / "mkdocs.yml"
    ledger = PROGRAMME_ROOT / "docs" / "FIXTURE_LEDGER.md"
    artifact_ledger = PROGRAMME_ROOT / "docs" / "AGENT_COUNCIL_ARTIFACT_LEDGER.md"

    for path in (page, showcase, nav, ledger, artifact_ledger):
        require(path.is_file(), f"publication integration file missing: {path}")

    page_text = page.read_text(encoding="utf-8")
    required_page_fragments = (
        "Publication ID | `PUB-LOG-GCD-001`",
        f"Publication status | **{EXPECTED_STATUS}**",
        "Mathematical status | Classical result; mathematical novelty **not claimed**",
        "logGcd_posSemidef",
        "logGcd_eq_feature_inner",
        EXPECTED_DESCRIPTION,
        "Mathematical novelty is **not supported**",
        "first-public-Lean-formalization priority is established",
        "The publication does **not** claim any of the following",
        "workflow `29984406250`",
        "workflow `29993578051`",
        "workflow `29994235171`",
    )
    for fragment in required_page_fragments:
        require(fragment in page_text, f"publication page missing: {fragment!r}")
    require("Mathematical novelty is **supported**" not in page_text, "publication page promotes novelty")
    require("This is the first Lean formalization" not in page_text, "publication page promotes priority")

    showcase_text = showcase.read_text(encoding="utf-8")
    for fragment in (
        "## Fixture 003: The logarithmic GCD kernel",
        "PUB-LOG-GCD-001",
        "Classical mathematics · certified formal artifact",
        f"Publication {EXPECTED_STATUS.lower()}",
        "No novelty or priority claim",
    ):
        require(fragment in showcase_text, f"showcase entry missing: {fragment!r}")

    nav_text = nav.read_text(encoding="utf-8")
    require("Published Result: Logarithmic GCD Kernel: LOG_GCD_PUBLICATION.md" in nav_text,
            "publication page missing from site navigation")

    ledger_text = ledger.read_text(encoding="utf-8")
    require("Publication candidate" in ledger_text, "fixture ledger lacks publication-stage record")
    require("PUB-LOG-GCD-001" in ledger_text, "fixture ledger lacks publication ID")

    artifact_text = artifact_ledger.read_text(encoding="utf-8")
    require("PUB-LOG-GCD-001" in artifact_text, "artifact ledger lacks publication entry")
    require("publication candidate" in artifact_text, "artifact ledger publication status drift")


def validate(root: Path = DEFAULT_ROOT) -> None:
    require(root.is_dir(), f"{root}: fixture directory missing")
    require((root / "publication_manifest.json").is_file(), "publication manifest missing")
    manifest = check_manifest(root)
    check_claim_support(root, manifest)
    check_public_pages(manifest)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) == 2 else DEFAULT_ROOT
    try:
        validate(root)
    except PublicationError as exc:
        print(f"LOG-GCD publication rejected: {exc}", file=sys.stderr)
        return 1
    print(f"LOG-GCD publication checked: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
