#!/usr/bin/env python3
from __future__ import annotations

import copy
import fnmatch
import json
import sys
import tempfile
import unittest
from pathlib import Path

import run_policy_shard
import run_unittest_modules

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/policy_shard_registry.json"
EXCLUDE_PATTERNS = [
    "test_oz*.py",
    "test_cmdg*.py",
    "test_*fixture*.py",
    "test_administrative*.py",
    "test_campaign*.py",
]
EXCLUDE_MANIFESTS = ["governance/contract_test_manifest.json"]


class PolicyShardRuntimeTests(unittest.TestCase):
    def registry(self) -> dict[str, object]:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_execution_policy_has_one_exact_long_running_override(self) -> None:
        default, overrides = run_policy_shard._execution_policy(self.registry())
        self.assertEqual(default, 900.0)
        self.assertEqual(set(overrides), {("oz", 1)})
        timeout, reason = overrides[("oz", 1)]
        self.assertEqual(timeout, 1680.0)
        self.assertIn("protected", reason.lower())

    def test_execution_policy_rejects_override_command_drift(self) -> None:
        data = copy.deepcopy(self.registry())
        override = data["execution"]["timeout_overrides"][0]
        override["command"] = list(override["command"]) + ["--drift"]
        with self.assertRaisesRegex(RuntimeError, "command drift"):
            run_policy_shard._execution_policy(data)

    def test_stream_command_enforces_timeout(self) -> None:
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as handle:
            returncode, timed_out = run_policy_shard._stream_command(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                log_handle=handle,
                timeout_seconds=0.05,
            )
        self.assertTrue(timed_out)
        self.assertEqual(returncode, run_policy_shard.TIMEOUT_EXIT)

    def test_repository_regression_exclusions_are_explicit_and_nonempty(self) -> None:
        discovered = run_unittest_modules._discover("tests", "test_*.py")
        selected, excluded = run_unittest_modules._apply_exclusions(
            discovered,
            exclude_patterns=EXCLUDE_PATTERNS,
            exclude_manifests=EXCLUDE_MANIFESTS,
        )
        self.assertTrue(selected)
        self.assertTrue(excluded)
        manifest_paths = set(
            run_unittest_modules._manifest_paths(
                ROOT / "governance/contract_test_manifest.json"
            )
        )
        for path in selected:
            self.assertNotIn(path, manifest_paths)
            self.assertFalse(
                any(fnmatch.fnmatchcase(path.name, pattern) for pattern in EXCLUDE_PATTERNS),
                path,
            )
        self.assertTrue(any(path.name.startswith("test_oz") for path, _ in excluded))


if __name__ == "__main__":
    unittest.main()
