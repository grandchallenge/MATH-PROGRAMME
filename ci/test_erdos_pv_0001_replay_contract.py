#!/usr/bin/env python3
"""Hostile tests for the source-locked Erdős #1 Lean replay contract."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import erdos_pv_0001_replay_contract as c

GREEN = (
    "'ErdosCounter.exists_binary_block_set' depends on axioms: [propext, Quot.sound, Classical.choice]\n"
    "'Erdos1.erdos_1.disproof' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
)

class Contracts(unittest.TestCase):
    def test_frozen_source_identity(self):
        self.assertEqual(c.PIN["commit"], "db6f9091dfaf9bac704e6b28fb3a094594869328")
        self.assertEqual(c.PIN["proof_git_blob"], "07d2f36647a2319e65c0c8c756527460925e9075")
        self.assertEqual(c.PIN["toolchain"], "leanprover/lean4:v4.28.0")
        self.assertEqual(c.PIN["mathlib_commit"], "8f9d9cff6bd728b17a24e163c9402775d9e6a365")

    def test_correct_theorem_scope(self):
        self.assertIn("hf : ErdosCounter.RelationFree a (2 ^ k)", c.READBACK)
        self.assertIn("A.card = d * k", c.READBACK)
        self.assertIn("Erdos1.erdos_1.disproof", c.READBACK)
        self.assertIn("Finset.Icc 1 (2 ^ (k - 1) * W)", c.READBACK)

    def test_negative_omits_the_required_relation_premise(self):
        self.assertNotIn("hf : ErdosCounter.RelationFree", c.NEGATIVE)
        self.assertIn("exact ErdosCounter.exists_binary_block_set", c.NEGATIVE)

    def test_axioms_approved(self):
        r=c.parse_axioms(GREEN)
        self.assertEqual(set(r),set(c.THEOREMS))
        self.assertEqual(set(r[c.THEOREMS[0]]),c.ALLOWED_AXIOMS)

    def test_no_axioms_accepted(self):
        s="\n".join(n+" does not depend on any axioms" for n in c.THEOREMS)
        self.assertEqual(c.parse_axioms(s),{n:[] for n in c.THEOREMS})

    def test_missing_theorem_axioms_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            c.parse_axioms("ErdosCounter.exists_binary_block_set does not depend on any axioms")

    def test_untrusted_axiom_rejected(self):
        with self.assertRaisesRegex(ValueError,"unexpected"):
            c.parse_axioms(GREEN.replace("propext", "InjectedAxiom"))

    def test_sorry_ax_rejected(self):
        with self.assertRaisesRegex(ValueError,"untrusted"):
            c.parse_axioms(GREEN+"sorryAx\n")

    def adjudicate(self, build=0, checked=0, negative=1, log=GREEN, bad="GCLNegative.lean:10:2: error: Type mismatch\\n  ErdosCounter.exists_binary_block_set d k W hd hk a ha hW\\nhas type ErdosCounter.RelationFree a (2 ^ k) → ..." ):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            logs=[p/x for x in ("build.log","check.log","bad.log")]
            for f,s in zip(logs,("BUILD SUCCESS\n",log,bad)):
                f.write_text(s)
            with patch.object(c,"verify_source",return_value={"result":"PINNED_SOURCE_MATCH",**c.PIN}):
                return c.adjudicate(p,*logs,build,checked,negative)

    def test_green_is_unadjudicated(self):
        r=self.adjudicate()
        self.assertEqual(r["result"],"LEAN_KERNEL_REPLAY_PASS_UNADJUDICATED")
        self.assertFalse(r["mathcert"])
        self.assertFalse(r["independent_referee"])
        self.assertEqual(len(r["log_sha256"]["readback"]),64)

    def test_build_timeout_stays_red(self):
        self.assertEqual(self.adjudicate(build=124)["result"],"REPLAY_FAILED_OR_UNVERIFIED")

    def test_type_failure_stays_red(self):
        self.assertEqual(self.adjudicate(checked=1)["result"],"REPLAY_FAILED_OR_UNVERIFIED")

    def test_false_negative_success_stays_red(self):
        self.assertEqual(self.adjudicate(negative=0)["result"],"REPLAY_FAILED_OR_UNVERIFIED")

    def test_fake_negative_error_stays_red(self):
        self.assertEqual(self.adjudicate(bad="not run")["result"],"REPLAY_FAILED_OR_UNVERIFIED")

    def test_unquoted_axiom_format_still_allowed(self):
        raw = GREEN.replace("'ErdosCounter.exists_binary_block_set'", "ErdosCounter.exists_binary_block_set").replace("'Erdos1.erdos_1.disproof'", "Erdos1.erdos_1.disproof")
        self.assertEqual(set(c.parse_axioms(raw)), set(c.THEOREMS))

    def test_unrelated_compiler_error_cannot_pass_negative_check(self):
        self.assertEqual(self.adjudicate(bad="bad.lean:1:1: error: Type mismatch")["result"], "REPLAY_FAILED_OR_UNVERIFIED")

    def test_axiom_injection_stays_red(self):
        self.assertEqual(self.adjudicate(log=GREEN.replace("Quot.sound","Injected"))["result"],
                         "REPLAY_FAILED_OR_UNVERIFIED")

if __name__=="__main__":
    unittest.main()
