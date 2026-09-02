#!/usr/bin/env python3
from __future__ import annotations

import copy
import fnmatch
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_policy_shard
import run_unittest_modules

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/policy_shard_registry.json"


class PolicyShardRuntimeTests(unittest.TestCase):
    def registry(self) -> dict[str, object]:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_execution_policy_has_exact_long_running_overrides(self) -> None:
        default, overrides = run_policy_shard._execution_policy(self.registry())
        self.assertEqual(default, 900.0)
        self.assertEqual(set(overrides), {("oz", 1), ("campaigns", 5)})
        for key in (("oz", 1), ("campaigns", 5)):
            timeout, reason = overrides[key]
            self.assertEqual(timeout, 1680.0)
            self.assertGreaterEqual(len(reason), 20)

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

    def test_repository_regression_exclusions_are_governed_and_nonempty(self) -> None:
        data = self.registry()
        expected = data["execution"]["repository_regression_exclusions"]
        with patch.dict(os.environ, {"GCL_POLICY_SHARD": "repository-regression"}, clear=False):
            patterns, manifests = run_unittest_modules._governed_exclusions()
        self.assertEqual(patterns, expected["patterns"])
        self.assertEqual(manifests, expected["manifests"])

        discovered = run_unittest_modules._discover("tests", "test_*.py")
        selected, excluded = run_unittest_modules._apply_exclusions(
            discovered,
            exclude_patterns=patterns,
            exclude_manifests=manifests,
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
                any(fnmatch.fnmatchcase(path.name, pattern) for pattern in patterns),
                path,
            )
        self.assertTrue(any(path.name.startswith("test_oz") for path, _ in excluded))

    def test_non_regression_shards_do_not_inherit_repository_exclusions(self) -> None:
        with patch.dict(os.environ, {"GCL_POLICY_SHARD": "contracts"}, clear=False):
            patterns, manifests = run_unittest_modules._governed_exclusions()
        self.assertEqual(patterns, [])
        self.assertEqual(manifests, [])


if __name__ == "__main__":
    unittest.main()
