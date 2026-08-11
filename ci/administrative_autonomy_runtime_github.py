from __future__ import annotations

from datetime import datetime
from typing import Any

from administrative_autonomy_runtime_github_core import *  # noqa: F401,F403
from administrative_autonomy_runtime_github_core import (
    Client,
    eligible_candidates as _ordinary_eligible_candidates,
)

RECEIPT_BRANCH_SLUG_PREFIX = "receipt-"


def maintenance_branch_namespace(branch: str, branch_prefix: str) -> str:
    """Classify branches before candidate identity or manifest resolution."""
    if not branch.startswith(branch_prefix):
        return "outside"
    slug = branch.removeprefix(branch_prefix)
    if slug.startswith(RECEIPT_BRANCH_SLUG_PREFIX):
        return "receipt"
    return "candidate"


class _CandidateDiscoveryClient:
    """Filter receipt PRs from the candidate scanner's open-PR view only."""

    def __init__(self, delegate: Client, repo: str, branch_prefix: str):
        self._delegate = delegate
        self._repo = repo
        self._branch_prefix = branch_prefix

    def __getattr__(self, name: str) -> Any:
        return getattr(self._delegate, name)

    def get(self, path: str) -> Any:
        value = self._delegate.get(path)
        expected = f"/repos/{self._repo}/pulls?state=open&per_page=100"
        if path != expected or not isinstance(value, list):
            return value
        return [
            pull
            for pull in value
            if maintenance_branch_namespace(
                str(pull.get("head", {}).get("ref") or ""),
                self._branch_prefix,
            )
            != "receipt"
        ]


def eligible_candidates(
    candidate: Client,
    repo: str,
    runtime: dict[str, Any],
    now: datetime,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Run ordinary candidate validation after receipt namespace exclusion."""
    prefix = str(runtime["scope"]["branch_prefix"])
    return _ordinary_eligible_candidates(
        _CandidateDiscoveryClient(candidate, repo, prefix),
        repo,
        runtime,
        now,
    )
