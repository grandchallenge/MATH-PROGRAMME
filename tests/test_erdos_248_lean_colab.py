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

    def test_actual_lean_four_print_format(self):
        line = "'Erdos248.erdos_248' depends on axioms: [propext, Classical.choice]"
        self.assertEqual(w.validate_axiom_output(line), line)

    def test_lean_four_sorry_axiom_rejected(self):
        with self.assertRaisesRegex(ValueError, "forbidden"):
            w.validate_axiom_output(
                "'Erdos248.erdos_248' depends on axioms: [sorryAx]")

    def test_valid_lean_axiom_print_parses(self):
        self.assertEqual(w.validate_axiom_output(
            "Erdos248.erdos_248 : True\naxioms used: [propext, Classical.choice, Quot.sound]\n"),
            "axioms used: [propext, Classical.choice, Quot.sound]")

    def test_direct_provider_patches_do_not_regenerate_manifest(self):
        import inspect
        worker_source = inspect.getsource(w.perform)
        self.assertIn('"git", "apply", "--check"', worker_source)
        self.assertIn('"git", "apply", str(patch_file)', worker_source)
        self.assertNotIn('"lake", "update"', worker_source)
        self.assertIn('verify_provider_post_update(project)', worker_source)

    def test_bounded_cpu_budget_for_heavy_pinned_sieve_proof(self):
        self.assertEqual(w.TIMEOUTS["lean-build"], 10800)
        self.assertEqual(w.TIMEOUTS["mathlib-cache"], 1500)
        self.assertEqual(w.TIMEOUTS["axiom-audit"], 240)
        self.assertLessEqual(
            sum(w.TIMEOUTS.values()) + 80, 15000,
            "all conservative worker stage caps must fit protected CPU session")

    def test_provider_patch_plan_is_complete(self):
        self.assertEqual(len(w.COMPATIBILITY_PATCHES), 9)
        self.assertEqual(len(set(p[1] for p in w.COMPATIBILITY_PATCHES)), 9)
        self.assertEqual(w.PINNED_DEPENDENCIES["BoundedGaps"],
                         "ffbb65c21afc8a36ace67720f1b0df1c63d26bd1")
        self.assertIn(("BoundedGaps", "formalpantheon-v4.33.0.patch",
                       "ad5f8915e55205e15d4557958020d71314294d6e"),
                      w.COMPATIBILITY_PATCHES)

    def test_patch_provenance_and_missing_hook_fail_closed(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "patches").mkdir()
            declared = "\n".join(
                '(' + '"' + dep + '", "' + name + '")'
                for dep, name, blob in w.COMPATIBILITY_PATCHES)
            (project / "lakefile.lean").write_text("post_update pkg do\n" + declared)
            (project / "lake-manifest.json").write_text(json.dumps({
                "packages": [{"name": name, "rev": rev}
                             for name, rev in w.PINNED_DEPENDENCIES.items()]}))
            for _, filename, _ in w.COMPATIBILITY_PATCHES:
                (project / "patches" / filename).write_text("frozen patch")
            patch_digests = {
                str(project / "patches" / filename): sha
                for _, filename, sha in w.COMPATIBILITY_PATCHES}
            patch_digests[str(project / "lakefile.lean")] = w.LAKEFILE_BLOB
            with patch.object(w, "git_blob",
                              side_effect=lambda p: patch_digests[str(p)]):
                records = w.verify_provider_patch_locks(project)
                self.assertEqual(len(records), 9)
                patch_digests[str(project / "patches" /
                    "formalpantheon-v4.33.0.patch")] = "0" * 40
                with self.assertRaisesRegex(ValueError, "blob drift"):
                    w.verify_provider_patch_locks(project)
                patch_digests[str(project / "patches" /
                    "formalpantheon-v4.33.0.patch")] = w.COMPATIBILITY_PATCHES[0][2]
                (project / "lakefile.lean").write_text(declared)
                with self.assertRaisesRegex(ValueError, "post_update"):
                    w.verify_provider_patch_locks(project)

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
