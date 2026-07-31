from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "five_repository_conformance_third_pass_closure",
    ROOT / "ci" / "five_repository_conformance_third_pass_closure.py",
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class ThirdPassClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.closure = json.loads(module.CLOSURE_PATH.read_text(encoding="utf-8"))
        cls.staged = json.loads(module.STAGED_PATH.read_text(encoding="utf-8"))
        cls.runtime = json.loads(module.RUNTIME_PATH.read_text(encoding="utf-8"))
        cls.campaigns = json.loads(module.CAMPAIGN_PATH.read_text(encoding="utf-8"))
        cls.routing = json.loads(module.ROUTING_PATH.read_text(encoding="utf-8"))

    def errors(self, *, closure=None, staged=None, runtime=None, campaigns=None, routing=None):
        return module.validation_errors(
            closure=copy.deepcopy(self.closure if closure is None else closure),
            staged=copy.deepcopy(self.staged if staged is None else staged),
            runtime=copy.deepcopy(self.runtime if runtime is None else runtime),
            campaigns=copy.deepcopy(self.campaigns if campaigns is None else campaigns),
            routing=copy.deepcopy(self.routing if routing is None else routing),
        )

    def test_closure_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_programme_merge_drift_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["programme_stage"]["merge_commit"] = "0" * 40
        self.assertTrue(any("Programme merge_commit drift" in e for e in self.errors(closure=closure)))

    def test_intellect_provider_drift_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["intellect_stage"]["provider_module"]["digest"] = "0" * 40
        self.assertTrue(any("INTELLECT provider_module identity drift" in e for e in self.errors(closure=closure)))

    def test_staged_mismatch_evidence_is_required(self):
        staged = copy.deepcopy(self.staged)
        staged["reviewed_correction_unresolved_mismatch_count"] = 0
        self.assertTrue(any("staged mismatch evidence drift" in e for e in self.errors(staged=staged)))

    def test_runtime_consumer_independence_is_required(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["consumer_independence"]["pins_intellect_commit"] = True
        self.assertTrue(any("runtime consumer-independence drift" in e for e in self.errors(runtime=runtime)))

    def test_programme_tracker_substitution_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["programme_tracker_mirrors"]["RH-001"] = 89
        self.assertTrue(any("Programme tracker mirror drift" in e for e in self.errors(closure=closure)))

    def test_cert_tracker_omission_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        del closure["cert_tracker_mirrors"]["YM-001"]
        self.assertTrue(any("Cert tracker mirror drift" in e for e in self.errors(closure=closure)))

    def test_portfolio_inflation_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["portfolio"]["qualified_interface_only"].append("BSD-001")
        self.assertTrue(any("qualified_interface_only closure portfolio drift" in e for e in self.errors(closure=closure)))

    def test_blocker_loss_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        del closure["preserved_blockers"]["OZ-001"]
        self.assertTrue(any("mathematical blocker coverage drift" in e for e in self.errors(closure=closure)))

    def test_issue_authority_inflation_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["authority_model"]["github_issue_role"] = "state_authority"
        self.assertTrue(any("issue mirror boundary missing" in e for e in self.errors(closure=closure)))

    def test_mathematical_promotion_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(any("mathematical_target_proved" in e for e in self.errors(closure=closure)))

    def test_remaining_obligation_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["remaining_cross_repository_obligations"] = ["unexpected"]
        self.assertTrue(any("cross-repository obligation remains" in e for e in self.errors(closure=closure)))

    def test_self_inclusive_publication_is_rejected(self):
        closure = copy.deepcopy(self.closure)
        closure["publication_semantics"]["self_inclusive_head_claim"] = True
        self.assertTrue(any("publication semantics drift" in e for e in self.errors(closure=closure)))


if __name__ == "__main__":
    unittest.main()
