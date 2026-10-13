import unittest
from unittest.mock import patch
from ci import gcl_lean_colab_jobs as skill

class LeanColabSkillTests(unittest.TestCase):
    def test_frozen_cpu_job(self):
        job=skill.jobs()["ERDOS-041-FINITE-001"]
        self.assertEqual(job["accelerator"],"CPU")
        self.assertEqual(job["toolchain"],"leanprover/lean4:v4.29.1")
    def test_unknown_task_rejected(self):
        self.assertNotIn("ARBITRARY",skill.jobs())
    def test_live_checkout_requires_protected_main(self):
        with patch.object(skill.subprocess,"check_output",side_effect=[b"",b"wronghead\n",b"mainhead\n"]):
            with self.assertRaisesRegex(ValueError,"protected main"):
                skill.protected_main()
    def test_offline_registry(self):
        self.assertEqual(skill.main(["verify"]) if False else len(skill.jobs()),1)
