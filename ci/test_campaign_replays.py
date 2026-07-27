#!/usr/bin/env python3
"""Adversarial rejection tests for governed campaign replay coverage."""
from __future__ import annotations

import copy

from validate_campaign_replays import ROOT, load_json, registry_errors


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

    print("campaign replay registry rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
