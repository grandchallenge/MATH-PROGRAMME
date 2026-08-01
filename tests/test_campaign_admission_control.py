from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "campaign_admission_control", ROOT / "ci" / "campaign_admission_control.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class CampaignAdmissionControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admission = json.loads(module.ADMISSION_PATH.read_text(encoding="utf-8"))
        cls.runtime = json.loads(module.RUNTIME_PATH.read_text(encoding="utf-8"))
        cls.active = json.loads(module.ACTIVE_PATH.read_text(encoding="utf-8"))
        cls.routing = json.loads(module.ROUTING_PATH.read_text(encoding="utf-8"))

    def errors(self, *, admission=None, runtime=None, active=None, routing=None):
        return module.validation_errors(
            admission=copy.deepcopy(self.admission if admission is None else admission),
            runtime=copy.deepcopy(self.runtime if runtime is None else runtime),
            active=copy.deepcopy(self.active if active is None else active),
            routing=copy.deepcopy(self.routing if routing is None else routing),
        )

    @staticmethod
    def candidate(admission, campaign_id):
        return next(item for item in admission["candidates"] if item["campaign_id"] == campaign_id)

    def test_current_candidate_control_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_nsof_cannot_enter_active_registry(self):
        active = copy.deepcopy(self.active)
        active["campaigns"].append({"campaign_id": "NSOF-001"})
        self.assertTrue(any("active campaign portfolio drift" in e or "leaked" in e for e in self.errors(active=active)))

    def test_nsof_cannot_enter_routing_registry(self):
        routing = copy.deepcopy(self.routing)
        routing["campaigns"].append({"campaign_id": "NSOF-001"})
        self.assertTrue(any("active routing portfolio drift" in e or "leaked" in e for e in self.errors(routing=routing)))

    def test_issue_edit_cannot_admit_campaign(self):
        admission = copy.deepcopy(self.admission)
        admission["authority"]["candidate_issue_mutation_can_admit_campaign"] = True
        self.assertTrue(any("issue mutation" in e for e in self.errors(admission=admission)))

    def test_nsof_source_cannot_be_verified_without_manifest(self):
        admission = copy.deepcopy(self.admission)
        self.candidate(admission, "NSOF-001")["source_provenance"]["state"] = "provider_verified"
        self.assertTrue(any("source provenance inflated" in e for e in self.errors(admission=admission)))

    def test_screenshot_digest_cannot_become_manuscript_identity(self):
        admission = copy.deepcopy(self.admission)
        source = self.candidate(admission, "NSOF-001")["source_provenance"]
        source["candidate_source"] = {
            "author": "OPENAI", "title": "NONSOFIC GROUPS EXIST",
            "printed_date": "2026-08-01",
            "candidate_sha256": module.EXPECTED_SCREENSHOT_DIGEST,
            "candidate_byte_length": 408154,
            "target_scope": "Complete claimed manuscript",
        }
        self.assertTrue(any("manuscript source identity fabricated" in e for e in self.errors(admission=admission)))

    def test_screenshot_evidence_digest_is_pinned(self):
        admission = copy.deepcopy(self.admission)
        evidence = self.candidate(admission, "NSOF-001")["source_provenance"]["intake_evidence"]
        evidence["sha256"] = "0" * 64
        self.assertTrue(any("screenshot evidence identity" in e for e in self.errors(admission=admission)))

    def test_intake_cannot_claim_manuscript_bytes(self):
        admission = copy.deepcopy(self.admission)
        evidence = self.candidate(admission, "NSOF-001")["source_provenance"]["intake_evidence"]
        evidence["manuscript_bytes_acquired"] = True
        self.assertTrue(any("screenshot evidence identity" in e for e in self.errors(admission=admission)))

    def test_nsof_cannot_fabricate_solve_merge(self):
        admission = copy.deepcopy(self.admission)
        solve = self.candidate(admission, "NSOF-001")["solve_candidate"]
        solve["merge_commit"] = "0" * 40
        self.assertTrue(any("fabricated Solve execution evidence" in e for e in self.errors(admission=admission)))

    def test_nsof_cannot_create_campaign_manifest(self):
        admission = copy.deepcopy(self.admission)
        solve = self.candidate(admission, "NSOF-001")["solve_candidate"]
        solve["may_create_campaign_manifest"] = True
        self.assertTrue(any("prohibited intake authority" in e for e in self.errors(admission=admission)))

    def test_nsof_pre_route_candidate_cannot_adjudicate(self):
        admission = copy.deepcopy(self.admission)
        cert = self.candidate(admission, "NSOF-001")["certification_candidate"]
        cert["may_adjudicate"] = True
        self.assertTrue(any("Cert pre-route boundary drift" in e for e in self.errors(admission=admission)))

    def test_nsof_review_gate_cannot_close_early(self):
        admission = copy.deepcopy(self.admission)
        gates = self.candidate(admission, "NSOF-001")["admission_gates"]
        gates["solve_candidate_package_reviewed"] = True
        self.assertTrue(any("admission gate inflated" in e for e in self.errors(admission=admission)))

    def test_vgse_reviewed_state_is_preserved(self):
        admission = copy.deepcopy(self.admission)
        self.candidate(admission, "VGSE-001")["candidate_phase"] = "intake_only"
        self.assertTrue(any("reviewed candidate phase drift" in e for e in self.errors(admission=admission)))

    def test_vgse_solve_evidence_identities_are_pinned(self):
        mutations = {
            "base_commit": "0" * 40,
            "reviewed_head": "0" * 40,
            "merge_commit": "0" * 40,
            "merged_at": "2026-01-01T00:00:00Z",
            "workflow_runs": {
                "solve_checks": 1,
                "gcl_conformance": 1,
                "candidate_replay": 1,
            },
            "required_admission_record_path": "work_packages/VGSE_WP00/wrong.json",
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                admission = copy.deepcopy(self.admission)
                solve = self.candidate(admission, "VGSE-001")["solve_candidate"]
                solve[field] = value
                expected = f"merged Solve evidence drift in {field}"
                self.assertTrue(any(expected in e for e in self.errors(admission=admission)))

    def test_runtime_must_pin_two_candidate_ids(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["candidate_admission_contract"]["candidate_ids"] = ["VGSE-001"]
        self.assertTrue(any("candidate portfolio identity drift" in e for e in self.errors(runtime=runtime)))

    def test_runtime_must_expose_nsof_as_intake_only(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["candidate_portfolio"]["intake_only"] = []
        self.assertTrue(any("candidate phase projection drift" in e for e in self.errors(runtime=runtime)))

    def test_candidate_work_cannot_self_admit(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["authority_model"]["candidate_work_can_self_admit"] = True
        self.assertTrue(any("may not self-admit" in e for e in self.errors(runtime=runtime)))

    def test_mathematical_claim_inflation_is_rejected(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(any("mathematical proof inflation" in e for e in self.errors(runtime=runtime)))


if __name__ == "__main__":
    unittest.main()
