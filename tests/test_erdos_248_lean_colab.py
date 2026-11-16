"""Hostile, network-free tests of frozen external Lean/Mathlib replay semantics."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from colab import erdos_248_lean_worker as w

class Erdos248WorkerTests(unittest.TestCase):
    def test_pins_are_frozen(self):
        self.assertEqual(w.TOOLCHAIN, "leanprover/lean4:v4.33.0")
        self.assertEqual(w.COMMIT, "8822f7ddef30fadbd92e1c6ab4ed897af356af5e")
        self.assertEqual(w.MATHLIB, "db584cd6d46c92f209a44c0f1c829460d327499d")
        self.assertEqual(w.SOURCE_BLOB, "166659f39a435831d1a751718f9a385effcd7dfa")

    def test_missing_axiom_output_rejected(self):
        with self.assertRaisesRegex(ValueError, "no observed"):
            w.validate_axiom_output("Erdos248.erdos_248 : True")

    def test_untrusted_sorry_axiom_rejected(self):
        with self.assertRaisesRegex(ValueError, "forbidden"):
            w.validate_axiom_output("Erdos248.erdos_248\naxioms used: [sorryAx]")

    def test_green_report_requires_named_theorem(self):
        with self.assertRaisesRegex(ValueError, "named final theorem"):
            w.validate_axiom_output("axioms used: [propext]")

    def test_valid_lean_axiom_print_parses(self):
        self.assertEqual(w.validate_axiom_output(
            "Erdos248.erdos_248 : True\naxioms used: [propext, Classical.choice, Quot.sound]\n"),
            "axioms used: [propext, Classical.choice, Quot.sound]")

    def test_red_receipt_is_written_before_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            (p / "src.lean").write_text("theorem x : True := by trivial\n")
            (p / "worker.py").write_text("# worker\n")
            with patch.object(w, "run", side_effect=RuntimeError("isolated checkout error")):
                outcome = w.perform(p/"src.lean", p/"worker.py",
                                    p/"receipt.json", p/"out")
            self.assertEqual(outcome, 1)
            import json
            receipt = json.loads((p/"receipt.json").read_text())
            self.assertEqual(receipt["status"], "RED")
            self.assertFalse(receipt["full_kernel_replay"])
            self.assertIn("isolated checkout error", receipt["error"])

if __name__ == "__main__":
    unittest.main()
