#!/usr/bin/env python3
"""Adversarial tests for the clean/dirty/sentinel formal replay gate."""
from __future__ import annotations

import datetime as dt
import tempfile
from pathlib import Path

import formal_replay_gate as gate

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 8, 10, 12, 0, tzinfo=UTC)


def fake_policy() -> dict:
    return {
        "operation": "MP-FORMAL-REPLAY-CONTENT-ADDRESSING-001",
        "global": {"repository": "grandchallenge/MATH-PROGRAMME"},
        "sentinel": {
            "reuse_max_age_hours": 18,
            "required_full_replay_within_hours": 24,
        },
        "lanes": {
            "log-gcd": {
                "command": ["lake", "build"],
                "proof_semantic_tcb": {"runner": "ubuntu-24.04"},
            }
        },
    }


def receipt(*, event: str = "push", created: dt.datetime | None = None) -> dict:
    when = created or (NOW - dt.timedelta(hours=1))
    return {
        "schema_version": 1,
        "lane": "log-gcd",
        "status": gate.formal.RECEIPT_STATUS,
        "input_digest": "d" * 64,
        "repository": "grandchallenge/MATH-PROGRAMME",
        "origin_commit": "a" * 40,
        "origin_run_id": "123",
        "origin_run_attempt": "1",
        "origin_event": event,
        "origin_ref": "refs/heads/main",
        "policy_operation": "MP-FORMAL-REPLAY-CONTENT-ADDRESSING-001",
        "command": ["lake", "build"],
        "proof_semantic_tcb": {"runner": "ubuntu-24.04"},
        "result_digest": "e" * 64,
        "result_files": [],
        "created_at": when.isoformat().replace("+00:00", "Z"),
    }


def main() -> int:
    original_digest = gate.formal.compute_digest
    original_ancestor = gate.formal.is_ancestor
    original_now = gate.formal.now_utc
    gate.formal.compute_digest = lambda repo, policy, lane: ("d" * 64, {})
    gate.formal.is_ancestor = lambda repo, origin: True
    gate.formal.now_utc = lambda: NOW
    try:
        policy = fake_policy()
        ok, reason = gate.validate(Path("."), policy, "log-gcd", receipt(), 24)
        assert ok and reason == "protected_attestation_healthy"

        ok, _ = gate.validate(Path("."), policy, "log-gcd", receipt(event="schedule"), 24)
        assert ok

        ok, reason = gate.validate(Path("."), policy, "log-gcd", receipt(event="pull_request"), 24)
        assert not ok and reason == "receipt_origin_event_not_protected"

        ok, reason = gate.validate(
            Path("."),
            policy,
            "log-gcd",
            receipt(created=NOW - dt.timedelta(hours=24)),
            24,
        )
        assert not ok and reason == "protected_sentinel_stale"

        drift = receipt()
        drift["command"] = ["lake", "test"]
        ok, reason = gate.validate(Path("."), policy, "log-gcd", drift, 24)
        assert not ok and reason == "receipt_command_mismatch"

        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "receipt.json"
            assert gate.decide(Path("."), policy, "log-gcd", missing, "clean", None) == 3
            assert gate.decide(Path("."), policy, "log-gcd", missing, "dirty", None) == 0
            assert gate.decide(Path("."), policy, "log-gcd", missing, "sentinel", None) == 0

        print("formal replay gate rejection tests passed")
        return 0
    finally:
        gate.formal.compute_digest = original_digest
        gate.formal.is_ancestor = original_ancestor
        gate.formal.now_utc = original_now


if __name__ == "__main__":
    raise SystemExit(main())
