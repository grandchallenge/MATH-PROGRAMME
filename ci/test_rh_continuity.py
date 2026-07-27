#!/usr/bin/env python3
"""Adversarial rejection tests for RH retained-blocker continuity."""
from __future__ import annotations

import copy

from validate_rh_continuity import ROOT, _read, _review, rh_continuity_errors


def main() -> int:
    assert not rh_continuity_errors()

    domain_path = "docs/domains/riemann_hypothesis.md"
    promoted_domain = _read(domain_path).replace(
        "but not formally promoted", "and formally promoted", 1
    )
    assert any(
        "missing current RH lifecycle marker" in error
        for error in rh_continuity_errors(texts={domain_path: promoted_domain})
    )

    disposition_path = "campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md"
    weakened_disposition = _read(disposition_path).replace(
        "NOT_PROMOTED / RETAINED_REVIEW_BLOCKERS", "PROMOTED", 1
    )
    assert any(
        "missing retained-blocker marker" in error
        for error in rh_continuity_errors(texts={disposition_path: weakened_disposition})
    )

    ledger_path = "docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md"
    unblocked_ledger = _read(ledger_path).replace(
        "| 2026-07-26 | blocked |", "| 2026-07-26 | reviewed |", 1
    )
    assert any(
        "must remain withheld with blocked continuity state" in error
        for error in rh_continuity_errors(texts={ledger_path: unblocked_ledger})
    )

    review_path = "reviews/riemann_hypothesis/RH-WP01.agent_review.yaml"
    promoted_review = copy.deepcopy(_review(review_path))
    promoted_review["promotion_recommended"] = True
    assert any(
        "promotion_recommended must remain false" in error
        for error in rh_continuity_errors(reviews={review_path: promoted_review})
    )

    referee_cleared = copy.deepcopy(_review(review_path))
    referee_cleared["offices"]["Referee"]["blocking"] = False
    assert any(
        "Referee blocking finding must remain true" in error
        for error in rh_continuity_errors(reviews={review_path: referee_cleared})
    )

    print("RH continuity rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
