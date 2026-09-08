#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

import policy_oz_replay as oz


class OzReplayRoutingTests(unittest.TestCase):
    def test_measured_heavy_profile_is_exact(self) -> None:
        self.assertEqual(len(oz.HEAVY_MODULES), 12)
        self.assertEqual(len(set(oz.HEAVY_MODULES)), 12)
        self.assertEqual(oz.HEAVY_MODULES[-1], "tests/test_oz_rt_bz_t3_011_f.py")

    def test_unrelated_change_selects_no_heavy_replay(self) -> None:
        self.assertEqual(oz.select_heavy(["docs/governance/example.md"]), [])
        self.assertEqual(oz.select_heavy(["campaigns/bsd/README.md"]), [])

    def test_full_sentinel_selects_all_measured_heavy_replays(self) -> None:
        self.assertEqual(oz.select_heavy(None), list(oz.HEAVY_MODULES))

    def test_merge_group_routes_exact_payload_transition(self) -> None:
        base = "a" * 40
        head = "b" * 40
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
            json.dump({"merge_group": {"base_sha": base, "head_sha": head}}, handle)
            event_path = handle.name
        try:
            diff_result = SimpleNamespace(
                returncode=0,
                stdout="docs/governance/example.md\n",
                stderr="",
            )
            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "GITHUB_EVENT_NAME": "merge_group",
                        "GITHUB_EVENT_PATH": event_path,
                    },
                    clear=False,
                ),
                mock.patch.object(oz, "_fetch_commit") as fetch_commit,
                mock.patch.object(oz.subprocess, "run", return_value=diff_result) as run,
            ):
                event, changed = oz._changed_paths()

            self.assertEqual(event, "merge_group")
            self.assertEqual(changed, ["docs/governance/example.md"])
            fetch_commit.assert_has_calls([mock.call(base), mock.call(head)])
            self.assertEqual(
                run.call_args.args[0],
                ["git", "diff", "--name-only", base, head, "--"],
            )
        finally:
            os.unlink(event_path)

    def test_merge_group_missing_identity_fails_closed(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
            json.dump({"merge_group": {"base_sha": "a" * 40}}, handle)
            event_path = handle.name
        try:
            with mock.patch.dict(
                os.environ,
                {
                    "GITHUB_EVENT_NAME": "merge_group",
                    "GITHUB_EVENT_PATH": event_path,
                },
                clear=False,
            ):
                with self.assertRaisesRegex(RuntimeError, "transition base/head unavailable"):
                    oz._changed_paths()
        finally:
            os.unlink(event_path)

    def test_stage_003_and_004_are_local(self) -> None:
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_003/verify.py"]),
            ["tests/test_oz_rt_bz_t3_003.py"],
        )
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_004/verify.py"]),
            ["tests/test_oz_rt_bz_t3_004.py"],
        )

    def test_rank_kernel_change_selects_search_replay_only(self) -> None:
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_008/rank_mod.c"]),
            ["tests/test_oz_rt_bz_t3_009_search.py"],
        )

    def test_upstream_computational_change_propagates_to_search_and_downstream(self) -> None:
        for path in (
            "campaigns/odd_zeta/OZ_RT_BZ_T3_006/producer.py",
            "campaigns/odd_zeta/OZ_RT_BZ_T3_009/one_body_coefficient_layer.py",
        ):
            selected = oz.select_heavy([path])
            self.assertIn("tests/test_oz_rt_bz_t3_009_search.py", selected)
            for stage in ("010_a", "010_b", "010_c", "011_a", "011_b", "011_c", "011_d", "011_e", "011_f"):
                self.assertIn(f"tests/test_oz_rt_bz_t3_{stage}.py", selected)
            self.assertNotIn("tests/test_oz_rt_bz_t3_003.py", selected)
            self.assertNotIn("tests/test_oz_rt_bz_t3_004.py", selected)

    def test_stage_dependencies_propagate_forward_only(self) -> None:
        selected_c = oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_010_c.py"])
        self.assertNotIn("tests/test_oz_rt_bz_t3_010_a.py", selected_c)
        self.assertNotIn("tests/test_oz_rt_bz_t3_010_b.py", selected_c)
        self.assertIn("tests/test_oz_rt_bz_t3_010_c.py", selected_c)
        for stage in ("011_a", "011_b", "011_c", "011_d", "011_e", "011_f"):
            self.assertIn(f"tests/test_oz_rt_bz_t3_{stage}.py", selected_c)

        selected_e = oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_e.py"])
        self.assertEqual(
            selected_e,
            ["tests/test_oz_rt_bz_t3_011_e.py", "tests/test_oz_rt_bz_t3_011_f.py"],
        )

        selected_f = oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_f.py"])
        self.assertEqual(selected_f, ["tests/test_oz_rt_bz_t3_011_f.py"])

    def test_shared_computational_helper_fails_closed_to_all_downstream_replays(self) -> None:
        selected = oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_010/shared_exact_helper.py"])
        expected = [module for module in oz.HEAVY_MODULES if module in oz.MODULE_STAGE]
        self.assertEqual(selected, expected)

    def test_documentary_change_does_not_trigger_computational_replay(self) -> None:
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_010/README_011_F.md"]),
            [],
        )

    def test_direct_heavy_test_change_selects_that_test(self) -> None:
        target = "tests/test_oz_rt_bz_t3_011_f.py"
        self.assertEqual(oz.select_heavy([target]), [target])

    def test_unsafe_changed_paths_fail_closed(self) -> None:
        for value in ("../escape", "/absolute", "a/../escape", ".."):
            with self.assertRaises(RuntimeError):
                oz._normalize([value])


if __name__ == "__main__":
    unittest.main()
