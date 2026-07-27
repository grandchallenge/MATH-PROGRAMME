#!/usr/bin/env python3
"""Adversarial rejection tests for governed campaign replay coverage."""
from __future__ import annotations

import copy
import tempfile
from pathlib import Path

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

    narrowed_registry = copy.deepcopy(registry)
    narrowed_registry["discovery_globs"] = ["campaigns/riemann_hypothesis/**/replay.py"]
    assert any("additional properties" in error.lower() for error in registry_errors(narrowed_registry))

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

    print("campaign replay registry rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
