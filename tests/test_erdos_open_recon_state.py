import copy
import json
import unittest

from ci.validate_erdos_open_recon_state import RECON, STATE, validate, validate_objects


class ErdosOpenReconStateTests(unittest.TestCase):
    def test_live_state_validates(self):
        self.assertEqual(validate(), [])

    def test_post_intake_automation_cannot_be_overstated(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        recon = json.loads(RECON.read_text(encoding="utf-8"))
        mutated = copy.deepcopy(state)
        mutated["automation"]["post_intake_cohort_lifecycle"] = "QUALIFIED_UNATTENDED"
        errors = validate_objects(mutated, recon)
        self.assertIn("post-intake lifecycle overstated", errors)

    def test_source_gate_cannot_be_fabricated(self):
        state = json.loads(STATE.read_text(encoding="utf-8"))
        recon = json.loads(RECON.read_text(encoding="utf-8"))
        mutated = copy.deepcopy(recon)
        mutated["source_gate"]["literature_dependent_promotion_allowed"] = True
        errors = validate_objects(state, mutated)
        self.assertIn("reconciliation literature promotion inflated", errors)


if __name__ == "__main__":
    unittest.main()
