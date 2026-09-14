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
        self.assertEqual(len(oz.HEAVY_MODULES), 34)
        self.assertEqual(len(set(oz.HEAVY_MODULES)), 34)
        self.assertEqual(
            oz.HEAVY_MODULES[-1],
            "tests/test_oz_rt_bz_t3_016_a_minimal_kernel_basis.py",
        )
        self.assertEqual(
            oz.HEAVY_MODULE_TIMEOUT_OVERRIDES,
            {"tests/test_oz_rt_bz_t3_011_g.py": 600.0},
        )

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
                with self.assertRaisesRegex(
                    RuntimeError, "transition base/head unavailable"
                ):
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

    def test_upstream_computational_change_propagates_to_all_downstream(self) -> None:
        for path in (
            "campaigns/odd_zeta/OZ_RT_BZ_T3_006/producer.py",
            "campaigns/odd_zeta/OZ_RT_BZ_T3_009/one_body_coefficient_layer.py",
        ):
            selected = oz.select_heavy([path])
            self.assertIn("tests/test_oz_rt_bz_t3_009_search.py", selected)
            self.assertEqual(
                selected,
                [
                    oz.SEARCH_MODULE,
                    *oz.EARLY_CHAIN_MODULES,
                    *oz.LATE_MODULES,
                ],
            )
            self.assertNotIn("tests/test_oz_rt_bz_t3_003.py", selected)
            self.assertNotIn("tests/test_oz_rt_bz_t3_004.py", selected)

    def test_early_stage_dependencies_propagate_forward_only(self) -> None:
        selected_c = oz.select_heavy(
            ["campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_010_c.py"]
        )
        self.assertNotIn("tests/test_oz_rt_bz_t3_010_a.py", selected_c)
        self.assertNotIn("tests/test_oz_rt_bz_t3_010_b.py", selected_c)
        self.assertEqual(
            selected_c,
            [
                *oz.EARLY_CHAIN_MODULES[2:],
                *oz.LATE_MODULES,
            ],
        )

        selected_e = oz.select_heavy(
            ["campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_e.py"]
        )
        self.assertEqual(
            selected_e,
            [
                *oz.EARLY_CHAIN_MODULES[7:],
                *oz.LATE_MODULES,
            ],
        )

        selected_g = oz.select_heavy(
            ["campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_g.py"]
        )
        self.assertEqual(
            selected_g,
            [
                "tests/test_oz_rt_bz_t3_011_g.py",
                *oz.LATE_MODULES,
            ],
        )

    def test_late_stage_dependencies_propagate_forward_only(self) -> None:
        selected_k = oz.select_heavy(
            ["campaigns/odd_zeta/OZ_RT_BZ_T3_011_K/producer.py"]
        )
        self.assertNotIn("tests/test_oz_rt_bz_t3_011_h.py", selected_k)
        self.assertNotIn("tests/test_oz_rt_bz_t3_011_i.py", selected_k)
        self.assertNotIn("tests/test_oz_rt_bz_t3_011_j.py", selected_k)
        self.assertEqual(
            selected_k[0],
            "tests/test_oz_rt_bz_t3_011_k.py",
        )
        self.assertEqual(
            selected_k[-1],
            "tests/test_oz_rt_bz_t3_016_a_minimal_kernel_basis.py",
        )

        selected_015c = oz.select_heavy(
            ["campaigns/odd_zeta/OZ_RT_BZ_T3_015_C/producer_impl.py.inc"]
        )
        self.assertEqual(
            selected_015c,
            [
                "tests/test_oz_rt_bz_t3_015_c.py",
                "tests/test_oz_rt_bz_t3_016_a.py",
                "tests/test_oz_rt_bz_t3_016_a_gauge_domain.py",
                "tests/test_oz_rt_bz_t3_016_a_minimal_kernel_basis.py",
            ],
        )

    def test_t3_016_computational_change_replays_local_group(self) -> None:
        self.assertEqual(
            oz.select_heavy(
                ["campaigns/odd_zeta/OZ_RT_BZ_T3_016_A/minimal_kernel_basis.py"]
            ),
            [
                "tests/test_oz_rt_bz_t3_016_a.py",
                "tests/test_oz_rt_bz_t3_016_a_gauge_domain.py",
                "tests/test_oz_rt_bz_t3_016_a_minimal_kernel_basis.py",
            ],
        )

    def test_shared_early_helper_fails_closed_to_every_successor_replay(self) -> None:
        selected = oz.select_heavy(
            ["campaigns/odd_zeta/OZ_RT_BZ_T3_010/shared_exact_helper.py"]
        )
        self.assertEqual(
            selected,
            [
                *oz.EARLY_CHAIN_MODULES,
                *oz.LATE_MODULES,
            ],
        )

    def test_documentary_change_does_not_trigger_computational_replay(self) -> None:
        self.assertEqual(
            oz.select_heavy(
                ["campaigns/odd_zeta/OZ_RT_BZ_T3_016_A/README.md"]
            ),
            [],
        )

    def test_inc_files_are_computational_inputs(self) -> None:
        self.assertTrue(
            oz._computational(
                "campaigns/odd_zeta/OZ_RT_BZ_T3_015_C/producer_impl.py.inc"
            )
        )

    def test_direct_heavy_test_change_selects_that_test_only(self) -> None:
        target = "tests/test_oz_rt_bz_t3_012_b.py"
        self.assertEqual(oz.select_heavy([target]), [target])

    def test_unsafe_changed_paths_fail_closed(self) -> None:
        for value in ("../escape", "/absolute", "a/../escape", "..", "a/b/.."):
            with self.assertRaises(RuntimeError):
                oz._normalize([value])


if __name__ == "__main__":
    unittest.main()
