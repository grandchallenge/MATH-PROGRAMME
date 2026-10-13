"""Regression tests for the 200-item documentary-only cohort checkpoint."""
import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ec003", HERE / "validate_erdos_compendium_bulk_003.py")
ec003 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec003)


class Cohort003Tests(unittest.TestCase):
    def test_immutable_two_hundred_problem_scope_and_source_bytes(self):
        m = ec003.load(ec003.MANIFEST)
        self.assertEqual(m["source_registry_blob"], ec003.git_blob_sha(ec003.REGISTRY.read_bytes()))
        self.assertEqual({x["problem_id"] for x in m["items"]}, set(range(246, 447)) - {390})
        self.assertEqual(len(m["items"]), 200)

    def test_checkpoint_validates_every_record_and_real_article(self):
        result = ec003.verify()
        self.assertEqual(result["source_returns"] + result["missing_returns"], 200)
        self.assertEqual(result["articles"] + result["missing_articles"], 200)
        self.assertLessEqual(result["articles"], result["source_returns"])
        self.assertEqual(len(result["sample_problem_ids"]), 20)

    def test_bare_tex_commands_rejected_in_inline_and_display_math(self):
        for fragment in ('$mathbb{R}^2$', '$Nleq6$', '$sum_{i=1}^N$', '$$a,quad b$$'):
            with self.subTest(fragment=fragment):
                with self.assertRaisesRegex(AssertionError, 'Bare TeX command'):
                    ec003.check_math_commands(fragment, 999)

    def test_valid_tex_commands_accepted_in_inline_and_display_math(self):
        good = r'$\mathbb{R}^2$ and $$a,\quad b,\qquad c$$ and $N\leq6$'
        ec003.check_math_commands(good, 999)

    def test_strict_gate_requires_actual_complete_batch_and_qa(self):
        checkpoint = ec003.verify()
        if checkpoint["strict_ready"]:
            self.assertEqual(ec003.verify(strict=True)["articles"], 200)
        else:
            with self.assertRaises(AssertionError):
                ec003.verify(strict=True)


if __name__ == "__main__":
    unittest.main()
