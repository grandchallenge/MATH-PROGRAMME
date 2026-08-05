from __future__ import annotations

import os

import administrative_automation as automation
import administrative_receipts as receipts

automation.derive_completion_state = receipts.derive_completion_state

import prepare_administrative_candidate as implementation

_original_repository_state = implementation.repository_state


def split_repository_state(
    write_client: implementation.GitHubClient,
    repositories: list[str],
) -> list[dict]:
    primary = os.environ.get("GITHUB_REPOSITORY", "")
    if primary not in repositories:
        raise automation.AutomationError("primary repository missing from evidence scope")
    evidence_token = os.environ.get("EVIDENCE_GITHUB_TOKEN", "")
    if not evidence_token:
        raise automation.AutomationError("EVIDENCE_GITHUB_TOKEN is required in apply mode")
    evidence_client = implementation.GitHubClient(
        evidence_token,
        os.environ.get("GITHUB_API_URL", "https://api.github.com"),
    )
    result = _original_repository_state(write_client, [primary])
    result.extend(
        _original_repository_state(
            evidence_client,
            [repository for repository in repositories if repository != primary],
        )
    )
    return result


implementation.repository_state = split_repository_state


if __name__ == "__main__":
    raise SystemExit(implementation.main())
