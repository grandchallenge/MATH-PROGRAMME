#!/usr/bin/env python3
"""Adversarial rejection tests for governed campaign replay coverage and routing."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from validate_campaign_replays import (
    REGISTRY_RELATIVE,
    ROOT,
    ReplayRoutingError,
    affected_replay_ids,
    changed_registry_entry_ids,
    load_json,
    registry_errors,
    transition_refs_from_event,
)


def main() -> int:
    registry = load_json(ROOT / "ci/campaign_replay_registry.json")
    assert not registry_errors(registry)

    missing_rh = copy.deepcopy(registry)
    missing_rh["entries"] = [
        entry for entry in missing_rh["entries"] if entry["id"] != "RH-WP01-REPLAY"
    ]
    assert any(
        "unregistered executable" in error
        and "campaigns/riemann_hypothesis/WP01_FALSE_PROOF_ATLAS/replay.py" in error
        for error in registry_errors(missing_rh)
    )

    duplicate_id = copy.deepcopy(registry)
    duplicate_id["entries"][1]["id"] = duplicate_id["entries"][0]["id"]
    assert any("duplicate id" in error for error in registry_errors(duplicate_id))

    duplicate_command = copy.deepcopy(registry)
    duplicate_command["entries"][1]["command"] = duplicate_command["entries"][0]["command"][:]
    assert any("duplicate command path" in error for error in registry_errors(duplicate_command))

    missing_script = copy.deepcopy(registry)
    missing_script["entries"][0]["command"][1] = "campaigns/missing/replay.py"
    assert any("registered replay script is missing" in error for error in registry_errors(missing_script))

    shell_command = copy.deepcopy(registry)
    shell_command["entries"][0]["command"] = ["bash", "-lc", "true"]
    assert any("must invoke Python directly" in error for error in registry_errors(shell_command))

    narrowed_registry = copy.deepcopy(registry)
    narrowed_registry["discovery_globs"] = ["campaigns/riemann_hypothesis/**/replay.py"]
    assert any("additional properties" in error.lower() for error in registry_errors(narrowed_registry))

    # Unrelated full-fanout controls must not execute historical campaign replays.
    assert affected_replay_ids(
        registry,
        ["governance/policy_shard_registry.json"],
    ) == set()

    # A campaign-family transition selects that family and no others.
    oz_ids = affected_replay_ids(
        registry,
        ["campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/README.md"],
    )
    assert oz_ids
    assert all(
        str(next(entry for entry in registry["entries"] if entry["id"] == label)["command"][1]).startswith(
            "campaigns/odd_zeta/"
        )
        for label in oz_ids
    )
    assert not any(label.startswith("BSD-") for label in oz_ids)

    # A changed registry entry is replayed even when its campaign files are unchanged.
    base_registry = copy.deepcopy(registry)
    changed_registry = copy.deepcopy(registry)
    changed_label = str(changed_registry["entries"][0]["id"])
    changed_registry["entries"][0]["timeout_seconds"] += 1
    assert changed_registry_entry_ids(base_registry, changed_registry) == {changed_label}
    assert affected_replay_ids(
        changed_registry,
        [REGISTRY_RELATIVE],
        base_registry=base_registry,
    ) == {changed_label}

    # Registry deltas may not be routed without the exact predecessor registry.
    try:
        affected_replay_ids(changed_registry, [REGISTRY_RELATIVE])
    except ReplayRoutingError as exc:
        assert "predecessor registry is unavailable" in str(exc)
    else:
        raise AssertionError("registry delta without predecessor must fail closed")

    # Unknown campaign roots fail closed instead of silently skipping execution.
    try:
        affected_replay_ids(registry, ["campaigns/unregistered_family/helper.py"])
    except ReplayRoutingError as exc:
        assert "no registered replay entries" in str(exc)
    else:
        raise AssertionError("unregistered campaign root must fail closed")

    # GitHub event parsing must preserve exact PR and push transition identities.
    with tempfile.TemporaryDirectory() as temporary:
        event_path = Path(temporary) / "event.json"
        event_path.write_text(
            json.dumps(
                {
                    "pull_request": {
                        "base": {"sha": "a" * 40},
                        "head": {"sha": "b" * 40},
                    }
                }
            ),
            encoding="utf-8",
        )
        assert transition_refs_from_event("pull_request", str(event_path)) == (
            "a" * 40,
            "b" * 40,
        )
        event_path.write_text(
            json.dumps({"before": "c" * 40, "after": "d" * 40}),
            encoding="utf-8",
        )
        assert transition_refs_from_event("push", str(event_path)) == (
            "c" * 40,
            "d" * 40,
        )
        assert transition_refs_from_event("schedule", str(event_path)) is None

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "schemas").mkdir()
        (root / "ci").mkdir()
        (root / "campaigns" / "synthetic").mkdir(parents=True)
        (root / "schemas" / "campaign_replay_registry.schema.json").write_text(
            (ROOT / "schemas" / "campaign_replay_registry.schema.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        synthetic = root / "campaigns" / "synthetic" / "custom_runner.py"
        synthetic.write_text(
            "#!/usr/bin/env python3\nif __name__ == '__main__':\n    print('synthetic')\n",
            encoding="utf-8",
        )
        synthetic_registry = copy.deepcopy(registry)
        synthetic_registry["entries"] = []
        synthetic_registry["exemptions"] = []
        assert any(
            "campaigns/synthetic/custom_runner.py" in error
            and "unregistered executable" in error
            for error in registry_errors(synthetic_registry, root=root)
        )

        exempted = copy.deepcopy(synthetic_registry)
        exempted["exemptions"] = [
            {
                "path": "campaigns/synthetic/custom_runner.py",
                "rationale": "Synthetic executable is intentionally excluded from execution for this test.",
            }
        ]
        assert not [
            error for error in registry_errors(exempted, root=root)
            if "custom_runner.py" in error
        ]

        overlap = copy.deepcopy(exempted)
        overlap["entries"] = [
            {
                "id": "SYNTHETIC-RUNNER",
                "command": ["python3", "campaigns/synthetic/custom_runner.py"],
                "timeout_seconds": 10,
                "scope": "Execute the synthetic campaign runner for overlap rejection testing.",
            }
        ]
        assert any("both registered and exempt" in error for error in registry_errors(overlap, root=root))

    print("campaign replay registry and routing rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
