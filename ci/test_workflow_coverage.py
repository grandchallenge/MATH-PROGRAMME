#!/usr/bin/env python3
"""Adversarial rejection tests for workflow and cross-repository coverage."""
from __future__ import annotations

import copy
import json

from test_rh_continuity import main as run_rh_continuity_tests
from validate_workflow_coverage import ROOT, workflow_coverage_errors, workflow_texts


def main() -> int:
    texts = workflow_texts()
    evidence = json.loads(
        (ROOT / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8")
    )
    assert not workflow_coverage_errors(texts=texts, evidence=evidence)

    missing_policy = dict(texts)
    missing_policy.pop("ci.yml")
    assert any(
        "missing governed workflow ci.yml" in error
        for error in workflow_coverage_errors(texts=missing_policy, evidence=evidence)
    )

    direct_pages_push = dict(texts)
    direct_pages_push["pages.yml"] = direct_pages_push["pages.yml"].replace(
        "  workflow_run:\n", "  push:\n    branches: [main]\n  workflow_run:\n", 1
    )
    assert any(
        "triggered only by workflow_run" in error
        for error in workflow_coverage_errors(texts=direct_pages_push, evidence=evidence)
    )

    bypass_success = dict(texts)
    bypass_success["pages.yml"] = bypass_success["pages.yml"].replace(
        "github.event.workflow_run.conclusion == 'success'", "true", 1
    )
    assert any(
        "missing publication gate" in error
        for error in workflow_coverage_errors(texts=bypass_success, evidence=evidence)
    )

    missing_replay = dict(texts)
    missing_replay["ci.yml"] = missing_replay["ci.yml"].replace(
        "python3 ci/validate_campaign_replays.py", "python3 -c 'print(\"skipped\")'", 1
    )
    assert any(
        "validate_campaign_replays.py" in error
        for error in workflow_coverage_errors(texts=missing_replay, evidence=evidence)
    )

    unpinned_evidence = copy.deepcopy(evidence)
    unpinned_evidence["commit"] = "main"
    assert any(
        "does not match" in error
        for error in workflow_coverage_errors(texts=texts, evidence=unpinned_evidence)
    )

    incomplete_evidence = copy.deepcopy(evidence)
    incomplete_evidence["paths"].remove("ci/replay_certificates.py")
    assert any(
        "required formal and bounded replay paths are incomplete" in error
        for error in workflow_coverage_errors(texts=texts, evidence=incomplete_evidence)
    )

    assert run_rh_continuity_tests() == 0

    print("workflow and RH continuity rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
