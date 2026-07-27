from __future__ import annotations

import math
import unittest

from experiments.ns_wp06_undec.halting_gate_fixture import Instruction, run_fixture


class HaltingGateFixtureTests(unittest.TestCase):
    def test_immediate_halt_activates_growth_gate(self) -> None:
        result = run_fixture(
            [Instruction("halt")],
            machine_steps=20,
            dt=1e-3,
            nu=0.25,
            threshold=100.0,
            substeps_per_machine_step=100,
        )
        self.assertTrue(result.halted)
        self.assertEqual(result.halt_step, 0)
        self.assertTrue(result.gate_crossed)

    def test_nonhalting_loop_only_decays(self) -> None:
        result = run_fixture(
            [Instruction("inc", register=0, target=0)],
            machine_steps=20,
            dt=1e-3,
            nu=0.25,
            threshold=100.0,
            substeps_per_machine_step=100,
        )
        self.assertFalse(result.halted)
        self.assertFalse(result.gate_crossed)
        self.assertGreater(result.final_y, 0.0)
        self.assertLess(result.final_y, 2.0)

    def test_delayed_halt_is_distinguished_from_immediate_halt(self) -> None:
        program = [
            Instruction("inc", register=0, target=1),
            Instruction("dec_jump", register=0, target=2, zero_target=2),
            Instruction("halt"),
        ]
        result = run_fixture(
            program,
            machine_steps=20,
            dt=1e-3,
            nu=0.25,
            threshold=100.0,
            substeps_per_machine_step=100,
        )
        self.assertTrue(result.halted)
        self.assertEqual(result.halt_step, 2)
        self.assertTrue(result.gate_crossed)

    def test_counter_machine_rejects_noninteger_state(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative integers"):
            run_fixture([Instruction("halt")], initial_counters=(0.5, 0))
        with self.assertRaisesRegex(ValueError, "register must be integer"):
            run_fixture([Instruction("halt", register=True)])

    def test_numerical_contract_rejects_nonfinite_or_unstable_inputs(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be finite"):
            run_fixture([Instruction("halt")], dt=math.inf)
        with self.assertRaisesRegex(ValueError, "threshold must exceed"):
            run_fixture([Instruction("halt")], threshold=2.0)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            run_fixture([Instruction("halt")], substeps_per_machine_step=0)


if __name__ == "__main__":
    unittest.main()
