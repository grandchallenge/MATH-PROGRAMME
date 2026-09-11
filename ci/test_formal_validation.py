#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import formal_validation as formal

ROOT = Path(__file__).resolve().parents[1]


def expect(paths: list[str], lanes: list[str]) -> None:
    registry = formal.load_registry(ROOT)
    got = formal.classify_paths(paths, registry)
    assert got["lanes"] == lanes, (paths, got["lanes"], lanes)
    assert got["unknown_paths"] == []


def main() -> int:
    registry = formal.load_registry(ROOT)
    lane_ids = [lane["id"] for lane in registry["lanes"]]
    assert len(lane_ids) == 15
    assert len(lane_ids) == len(set(lane_ids))

    # The live reproduction from PR #919 must instantiate exactly one substantive
    # formal lane. Unrelated historical CMDG stages and other campaigns are absent.
    p3_point = (
        "fixtures/formal/CMDG-NAT-CONCORDANCE-001/"
        "CMDGCondensedCM4P3GPointFunctional.lean"
    )
    expect([p3_point], ["cmdg-cm4-p3"])

    expect(
        ["fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM1.lean"],
        ["cmdg-cm1"],
    )
    expect(
        ["fixtures/formal/LOG-GCD-001/LogGcd.lean"],
        ["log-gcd"],
    )
    expect(
        ["fixtures/formal/PC-WP04/PCWP04.lean"],
        ["pc-wp04"],
    )
    expect(["evidence/UC-WP02-MATHCERT.json"], ["union-closed-mathcert"])
    expect(["docs/WORKFLOW_COVERAGE.md"], [])
    expect(["README.md"], [])

    # Shared CMDG environment changes conservatively select all CMDG lanes, but do
    # not wake unrelated LOG-GCD, PC-WP04, or Union-Closed formal campaigns.
    cmdg_ids = [
        lane["id"] for lane in registry["lanes"] if lane["family"] == "CMDG"
    ]
    expect(
        ["fixtures/formal/CMDG-NAT-CONCORDANCE-001/lakefile.toml"],
        cmdg_ids,
    )

    # Router/control changes are the deliberate conservative full-fanout case.
    control = formal.classify_paths(["ci/formal_validation.py"], registry)
    assert control["lanes"] == lane_ids
    assert control["reason"] == "control_plane_full_fanout"

    # An unknown formal source cannot silently evade validation.
    try:
        formal.classify_paths(
            ["fixtures/formal/CMDG-NAT-CONCORDANCE-001/UnknownFutureProbe.lean"],
            registry,
        )
    except formal.FormalValidationError as exc:
        assert "unclassified executable/formal path" in str(exc)
    else:
        raise AssertionError("unknown managed formal source was accepted")

    # Unsafe transition paths are rejected before classification.
    for unsafe in ("../escape.lean", "/absolute.lean", "a/../escape.lean"):
        try:
            formal.normalize_paths([unsafe])
        except formal.FormalValidationError:
            pass
        else:
            raise AssertionError(f"unsafe path accepted: {unsafe}")

    # Development compilation is the changed leaf plus its actual local import
    # closure, not a chronological replay roster.
    package = ROOT / registry["cmdg_environment"]["package_dir"]
    closure = formal.dependency_order([ROOT / p3_point], package)
    names = [path.name for path in closure]
    assert names[-1] == "CMDGCondensedCM4P3GPointFunctional.lean"
    assert "CMDGCondensedCM4P3GFiniteBooleanMeasureHom.lean" in names
    assert "CMDGCondensedCM4P3G.lean" in names
    assert "CMDGCondensedCM1.lean" not in names

    # All standalone CMDG workflows are explicit promotion surfaces only.
    wrappers = {
        "cmdg-nat-concordance.yml": "cmdg-nat",
        "cmdg-euclid-bridge.yml": "cmdg-euclid-bridge",
        "cmdg-vertical-spine-v0.yml": "cmdg-vertical-spine-v0",
        "cmdg-condensed-cm1.yml": "cmdg-cm1",
        "cmdg-condensed-cm2.yml": "cmdg-cm2",
        "cmdg-condensed-cm3.yml": "cmdg-cm3",
        "cmdg-solid-c05.yml": "cmdg-solid-c05",
        "cmdg-condensed-cm4.yml": "cmdg-cm4",
        "cmdg-condensed-cm4-p2.yml": "cmdg-cm4-p2",
        "cmdg-condensed-cm4-p2-d.yml": "cmdg-cm4-p2-d",
        "cmdg-condensed-cm4-p2-e.yml": "cmdg-cm4-p2-e",
        "cmdg-condensed-cm4-p3.yml": "cmdg-cm4-p3",
    }
    workflow_dir = ROOT / ".github/workflows"
    for filename, lane in wrappers.items():
        text = (workflow_dir / filename).read_text(encoding="utf-8")
        assert "workflow_call:" in text
        assert "workflow_dispatch:" in text
        assert "pull_request:" not in text
        assert "push:" not in text
        assert "schedule:" not in text
        assert "uses: ./.github/workflows/cmdg-formal-lane-replay.yml" in text
        assert f"lane: {lane}" in text

    promotion_executor = (workflow_dir / "cmdg-formal-lane-replay.yml").read_text(encoding="utf-8")
    assert 'run: test "$GITHUB_REF" = "refs/heads/main"' in promotion_executor
    assert promotion_executor.index("Require protected-main promotion source") < promotion_executor.index("actions/setup-python@")
    assert promotion_executor.index("Require protected-main promotion source") < promotion_executor.index("grandchallenge/lean-action@")

    pc_promotion = (workflow_dir / "pc-wp04.yml").read_text(encoding="utf-8")
    assert 'run: test "$GITHUB_REF" = "refs/heads/main"' in pc_promotion
    assert pc_promotion.index("Require protected-main promotion source") < pc_promotion.index("actions/setup-python@")
    assert pc_promotion.index("Require protected-main promotion source") < pc_promotion.index("grandchallenge/lean-action@")

    generic = (workflow_dir / "formal-validation.yml").read_text(encoding="utf-8")
    assert "matrix: ${{ fromJSON(needs.impact.outputs.formal_matrix) }}" in generic
    assert "name: formal-validation" in generic
    assert "ci/formal_validation.py run" in generic
    assert "timeout-minutes: 75" in generic

    # Candidate execution is deliberately unprivileged. Exact candidate SHA
    # checkout is allowed because no secret/write authority or persistent GitHub
    # Actions cache is available to the PR code. The Mathlib artifact path is
    # retrieval-only (`lake exe cache get`) and is needed to materialize the exact
    # committed Lake manifest without compiling all historical formal libraries.
    # External authority is a fixed audited repository+commit, never matrix data.
    candidate_ref = (
        "ref: ${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || "
        "github.event_name == 'merge_group' && github.event.merge_group.head_sha || github.sha }}"
    )
    assert generic.count(candidate_ref) == 2
    assert "permissions:\n  contents: read" in generic
    assert "${{ secrets." not in generic
    assert "github.token" not in generic
    assert "matrix.external_repository" not in generic
    assert "matrix.external_ref" not in generic
    assert "if: matrix.lane == 'union-closed-mathcert'" in generic
    assert "repository: grandchallenge/MATHCERT" in generic
    assert "ref: d59173899dcd1a67dbe8f31de0b9f0917cd1459a" in generic
    assert "use-github-cache: false" in generic
    assert "use-mathlib-cache: true" in generic

    print("formal validation routing and security acceptance matrix passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
