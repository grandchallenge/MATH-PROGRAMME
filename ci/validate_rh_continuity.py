#!/usr/bin/env python3
"""Validate the RH-WP01/WP02 post-merge retained-blocker contract."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str, root: Path = ROOT) -> str:
    return (root / relative).read_text(encoding="utf-8")


def _review(relative: str, root: Path = ROOT) -> dict[str, Any]:
    return yaml.safe_load(_read(relative, root))


def rh_continuity_errors(
    root: Path = ROOT,
    texts: dict[str, str] | None = None,
    reviews: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    texts = {} if texts is None else texts
    reviews = {} if reviews is None else reviews

    def text(path: str) -> str:
        return texts.get(path, _read(path, root))

    def review(path: str) -> dict[str, Any]:
        return reviews.get(path, _review(path, root))

    errors: list[str] = []
    disposition_path = "campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md"
    disposition = text(disposition_path)
    for marker in (
        "implemented, merged through PR #90, and programme-policy CI passed",
        "NOT_PROMOTED / RETAINED_REVIEW_BLOCKERS",
        "promotion_recommended: false",
        "blocking Referee finding",
        "formal promotion remains withheld",
    ):
        if marker not in disposition:
            errors.append(f"{disposition_path}: missing retained-blocker marker {marker}")

    domain_path = "docs/domains/riemann_hypothesis.md"
    domain = text(domain_path)
    for marker in (
        "WP01 and WP02 implemented, merged, and CI-passed but not formally promoted",
        "promotion_recommended: false",
        "blocking Referee findings",
        "Post-merge retained-blocker disposition",
    ):
        if marker not in domain:
            errors.append(f"{domain_path}: missing current RH lifecycle marker {marker}")

    catalogue_path = "docs/domains/index.md"
    catalogue = text(catalogue_path)
    if "WP01/WP02 implemented, merged, and CI-passed, with formal promotion withheld" not in catalogue:
        errors.append(f"{catalogue_path}: RH catalogue posture does not preserve the promotion boundary")

    ledger_path = "docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md"
    ledger = text(ledger_path)
    for artifact in ("RH-WP01", "RH-WP02"):
        lines = [line for line in ledger.splitlines() if f"| {artifact} |" in line]
        if len(lines) != 1:
            errors.append(f"{ledger_path}: expected exactly one {artifact} row")
            continue
        row = lines[0]
        if "formal promotion withheld" not in row or not row.rstrip().endswith("| blocked |"):
            errors.append(f"{ledger_path}: {artifact} must remain withheld with blocked continuity state")

    register_path = "docs/CAMPAIGN_PROMOTION_REGISTER.md"
    register = text(register_path)
    for artifact in ("RH-WP01", "RH-WP02"):
        lines = [line for line in register.splitlines() if f"| `{artifact}` |" in line]
        if len(lines) != 1:
            errors.append(f"{register_path}: expected exactly one retained-blocker row for {artifact}")
            continue
        row = lines[0]
        if "not formally promoted" not in row or "promotion_recommended: false" not in row:
            errors.append(f"{register_path}: {artifact} row weakens the retained blocker")

    for artifact in ("RH-WP01", "RH-WP02"):
        review_path = f"reviews/riemann_hypothesis/{artifact}.agent_review.yaml"
        data = review(review_path)
        if data.get("promotion_recommended") is not False:
            errors.append(f"{review_path}: promotion_recommended must remain false")
        referee = data.get("offices", {}).get("Referee", {})
        if referee.get("blocking") is not True:
            errors.append(f"{review_path}: Referee blocking finding must remain true")

    return errors


def main() -> int:
    errors = rh_continuity_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"RH continuity validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("RH post-merge implementation and retained-promotion-blocker contracts are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
