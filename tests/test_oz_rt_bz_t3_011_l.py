from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_L"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011LTests(unittest.TestCase):
    def test_scope_rejects_every_extra_widening(self) -> None:
        mutations = (
            {"reciprocal_spectator": False},
            {"reciprocal_left": True},
            {"reciprocal_right": True},
            {"multiple_reciprocal_axes": True},
            {"shifted_spectator": True},
            {"shifted_poles": True},
            {"arbitrary_rational_functions": True},
            {"support_or_harmonic_enlargement": True},
            {"candidate_bank_or_scalar_namespace_widening": True},
            {"recurrence_widening": True},
            {"correction_recombination": True},
            {"candidate_linear_combinations": True},
            {"third_finite_difference_operator": True},
            {"arbitrary_degree_cutoff": 1},
        )
        for kwargs in mutations:
            with self.assertRaises(AssertionError):
                producer.validate_scope(**kwargs)

    def test_exact_cancellation_ray_detector(self) -> None:
        self.assertEqual(
            producer.cancellation_ray((("n", 1),), (("k", 1),), (("k", 1),)),
            [0, 1, 1],
        )
        self.assertEqual(
            producer.cancellation_ray(
                (("a", 1),), (("b", 1),), (("a", 1), ("b", 1))
            ),
            [1, 1, 1],
        )
        self.assertIsNone(
            producer.cancellation_ray((("a", 1),), (("b", 1),), (("c", 1),))
        )

    def test_geometric_ray_requires_actual_positive_support_seed(self) -> None:
        left = (("a", 1),)
        right = (("b", 1),)
        spectator = (("b", 1),)
        self.assertEqual(producer.cancellation_ray(left, right, spectator), [0, 1, 1])

        # target-base = a admits (r,s,t)=(1,1,1), so the ray passes
        # through an actual positive integer support solution.
        seed = producer.feasible_seed((), (("a", 1),), left, right, spectator)
        self.assertIsNotNone(seed)
        r, s, t = seed
        self.assertGreaterEqual(min(r, s, t), 1)

        # target-base = b has the same homogeneous geometric ray but forces
        # r=0.  It is therefore outside the admitted r>=1 response class and
        # must not be reported as an unbounded admitted support family.
        self.assertIsNone(
            producer.feasible_seed((), (("b", 1),), left, right, spectator)
        )

    def test_producer_and_independent_verifier_stop_at_support_feasible_ray(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)

        self.assertEqual(result["terminal"], producer.BLOCKER_TERMINAL)
        self.assertEqual(replay["terminal"], producer.BLOCKER_TERMINAL)
        blocker = result["characterized_blocker"]
        self.assertEqual(
            blocker["kind"],
            "UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY",
        )
        ray = blocker["primitive_integer_ray"]
        seed = blocker["feasible_seed_tridegree"]
        self.assertGreater(ray[2], 0)
        self.assertGreater(ray[0] + ray[1], 0)
        self.assertGreaterEqual(min(seed), 1)
        self.assertIn("support_key", blocker)
        self.assertIn("base_signature", blocker)
        self.assertIn("target_signature", blocker)

        domain = result["domain_analysis"]
        self.assertTrue(domain["feasible_support_seed_required"])
        self.assertFalse(domain["arbitrary_degree_cutoff_used"])
        self.assertGreater(domain["candidate_records_inspected_for_support"], 0)
        self.assertGreater(domain["ray_bearing_support_signature_pairs_inspected"], 0)

        self.assertEqual(result["tested_record_count"], 0)
        self.assertEqual(result["tested_records"], [])
        self.assertIsNone(result["first_cokernel_breaking_direction"])
        self.assertIsNone(result["semantic_functional_ambiguity"])
        self.assertFalse(result["all_reciprocal_spectator_responses_cokernel_invisible"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        print(
            "T3_011_L_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "possible_record_count": result["possible_record_count"],
                    "tested_record_count": result["tested_record_count"],
                    "domain_analysis": domain,
                    "characterized_blocker": blocker,
                    "semantic_functional_ambiguity": result[
                        "semantic_functional_ambiguity"
                    ],
                    "first_cokernel_breaking_direction": result[
                        "first_cokernel_breaking_direction"
                    ],
                    "all_reciprocal_spectator_responses_cokernel_invisible": result[
                        "all_reciprocal_spectator_responses_cokernel_invisible"
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
