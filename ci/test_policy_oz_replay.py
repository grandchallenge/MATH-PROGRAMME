#!/usr/bin/env python3
from __future__ import annotations

import unittest

import policy_oz_replay as oz


class OzReplayRoutingTests(unittest.TestCase):
    def test_measured_heavy_profile_is_exact(self) -> None:
        self.assertEqual(len(oz.HEAVY_MODULES), 12)
        self.assertEqual(len(set(oz.HEAVY_MODULES)), 12)
        self.assertEqual(
            oz.HEAVY_MODULES[-1],
            "tests/test_oz_rt_bz_t3_011_f.py",
        )

    def test_unrelated_change_selects_no_heavy_replay(self) -> None:
        self.assertEqual(oz.select_heavy(["docs/governance/example.md"]), [])
        self.assertEqual(oz.select_heavy(["campaigns/bsd/README.md"]), [])

    def test_full_sentinel_selects_all_measured_heavy_replays(self) -> None:
        self.assertEqual(oz.select_heavy(None), list(oz.HEAVY_MODULES))

    def test_stage_003_and_004_are_local(self) -> None:
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_003/verify.py"]),
            ["tests/test_oz_rt_bz_t3_003.py"],
        )
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_004/verify.py"]),
            ["tests/test_oz_rt_bz_t3_004.py"],
        )

    def test_rank_kernel_change_selects_search_replay(self) -> None:
        self.assertEqual(
            oz.select_heavy(["campaigns/odd_zeta/OZ_RT_BZ_T3_008/rank_mod.c"]),
            ["tests/test_oz_rt_bz_t3_009_search.py"],
        )

    def test_t3_009_computational_change_propagates_to_search_and_downstream(self) -> None:
        selected = oz.select_heavy([
            "campaigns/odd_zeta/OZ_RT_BZ_T3_009/one_body_coefficient_layer.py"
        ])
        self.assertIn("tests/test_oz_rt_bz_t3_009_search.py", selected)
        for stage in ("010_a", "010_b", "010_c", "011_a", "011_b", "011_c", "011_d", "011_e", "011_f"):
            self.assertIn(f"tests/test_oz_rt_bz_t3_{stage}.py", selected)
        self.assertNotIn("tests/test_oz_rt_bz_t3_003.py", selected)
        self.assertNotIn("tests/test_oz_rt_bz_t3_004.py", selected)

    def test_stage_dependencies_propagate_forward_only(self) -> None:
        selected_c = oz.select_heavy([
            "campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_010_c.py"
        ])
        self.assertNotIn("tests/test_oz_rt_bz_t3_010_a.py", selected_c)
        self.assertNotIn("tests/test_oz_rt_bz_t3_010_b.py", selected_c)
        self.assertIn("tests/test_oz_rt_bz_t3_010_c.py", selected_c)
        for stage in ("011_a", "011_b", "011_c", "011_d", "011_e", "011_f"):
            self.assertIn(f"tests/test_oz_rt_bz_t3_{stage}.py", selected_c)

        selected_e = oz.select_heavy([
            "campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_e.py"
        ])
        self.assertEqual(
            selected_e,
            [
                "tests/test_oz_rt_bz_t3_011_e.py",
                "tests/test_oz_rt_bz_t3_011_f.py",
            ],
        )

        selected_f = oz.select_heavy([
            "campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_f.py"
        ])
        self.assertEqual(selected_f, ["tests/test_oz_rt_bz_t3_011_f.py"])

    def test_documentary_change_does_not_trigger_computational_replay(self) -> None:
        self.assertEqual(
            oz.select_heavy([
                "campaigns/odd_zeta/OZ_RT_BZ_T3_010/README_011_F.md"
            ]),
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
