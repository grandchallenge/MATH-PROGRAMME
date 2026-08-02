from __future__ import annotations
import json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"ci"))
from disclose_evaluate import canonical,evaluate
from disclose_pr import validate

class DisclosureTests(unittest.TestCase):
    def copy(self)->Path:
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);dst=Path(tmp.name)
        for rel in ("disclosure","schemas","ci"):shutil.copytree(ROOT/rel,dst/rel)
        return dst
    @staticmethod
    def read(root:Path,rel:str)->dict:return json.loads((root/rel).read_text())
    @staticmethod
    def write(root:Path,rel:str,data:dict)->None:(root/rel).write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    def mutate(self,rel:str,fn)->list[str]:
        root=self.copy();data=self.read(root,rel);fn(data);self.write(root,rel,data);return validate(root)
    def finding(self,fid:str):return next(x for x in evaluate(ROOT/"disclosure/fixtures/GCL-DISCLOSE-PR-001")["findings"] if x["finding_id"]==fid)
    def test_valid(self):self.assertEqual([],validate())
    def test_deterministic(self):self.assertEqual(canonical(evaluate(ROOT/"disclosure/fixtures/GCL-DISCLOSE-PR-001")),canonical(evaluate(ROOT/"disclosure/fixtures/GCL-DISCLOSE-PR-001")))
    def test_product_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d.update(extra=True))))
    def test_manifest_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d.update(extra=True))))
    def test_review_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(extra=True))))
    def test_ledger_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("disclosure/disposition_ledger.json",lambda d:d.update(extra=True))))
    def test_activation_drift(self):self.assertTrue(any("too short" in e or "activation" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d["activation"].update(required_conditions=["protected_merge"]))))
    def test_external_release_prohibited(self):self.assertTrue(any("False was expected" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d["activation"].update(external_release_authorized=True))))
    def test_claim_promotion_prohibited(self):self.assertTrue(any("False was expected" in e or "claim-boundary" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d["claim_boundaries"].update(patentability_determined=True))))
    def test_aether_dependency_prohibited(self):self.assertTrue(any("False was expected" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d["core_contract"].update(aether_required=True))))
    def test_confidential_processing_prohibited(self):self.assertTrue(any("False was expected" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d["core_contract"].update(confidential_data_allowed=True))))
    def test_self_authentication_prohibited(self):self.assertTrue(any("False was expected" in e or "self-authenticating" in e for e in self.mutate("disclosure/product_contract.json",lambda d:d["review_packet"][0].update(may_self_authenticate=True))))
    def test_identity_drift(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(commit="0"*40))))
    def test_digest_drift(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(expected_sha256="0"*64))))
    def test_required_missing(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["artifacts"][2].update(required=True))))
    def test_optional_missing_abstains(self):self.assertEqual(("ABSTAIN","OPTIONAL_EVIDENCE_MISSING"),(self.finding("F-ART-MISSING")["disposition"],self.finding("F-ART-MISSING")["reason_code"]))
    def test_classification_absent_abstains(self):self.assertEqual(("ABSTAIN","CLASSIFICATION_ABSENT"),(self.finding("F-CLASS-MISSING")["disposition"],self.finding("F-CLASS-MISSING")["reason_code"]))
    def test_classification_head_mismatch(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["classification_cases"][0].update(subject_head="0"*40))))
    def test_classification_supersession(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["classification_cases"][0].update(superseded_by="CLASS-NEW"))))
    def test_active_hold_fails(self):self.assertEqual("ACTIVE_NO_RELEASE_HOLD",self.finding("F-HOLD-ACTIVE")["reason_code"])
    def test_stale_hold_fails(self):self.assertEqual("STALE_HOLD_USED_AS_AUTHORITY",self.finding("F-HOLD-STALE")["reason_code"])
    def test_hold_head_mismatch(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["hold_cases"][0].update(subject_head="0"*40))))
    def test_attribution_complete(self):self.assertEqual("ATTRIBUTION_COMPLETE",self.finding("F-ATTR-COMPLETE")["reason_code"])
    def test_attribution_missing(self):self.assertEqual("ATTRIBUTION_INCOMPLETE",self.finding("F-ATTR-MISSING")["reason_code"])
    def test_approved_claim(self):self.assertEqual("APPROVED_CLAIM_EXACT",self.finding("F-CLAIM-APPROVED")["reason_code"])
    def test_claim_inflation(self):self.assertEqual("CLAIM_EXCEEDS_APPROVED_LANGUAGE",self.finding("F-CLAIM-INFLATED")["reason_code"])
    def test_unsupported_ip_language(self):self.assertEqual("UNSUPPORTED_IP_LANGUAGE",self.finding("F-CLAIM-NOVELTY")["reason_code"])
    def test_professional_review_changes_novelty_case(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["claim_cases"][2].update(professional_review_present=True))))
    def test_public_export(self):self.assertEqual("SYNTHETIC_PUBLIC_EXPORT",self.finding("F-CONF-PUBLIC")["reason_code"])
    def test_confidential_leak(self):self.assertEqual("CONFIDENTIAL_EXPORT_LEAK",self.finding("F-CONF-LEAK")["reason_code"])
    def test_exact_review(self):self.assertEqual("EXACT_NON_AUTHOR_REVIEW",self.finding("F-REVIEW-EXACT")["reason_code"])
    def test_review_head_mismatch(self):self.assertEqual("REVIEW_HEAD_MISMATCH",self.finding("F-REVIEW-MISMATCH")["reason_code"])
    def test_author_only_authority(self):self.assertEqual("AUTHOR_ONLY_RELEASE_AUTHORITY",self.finding("F-RELEASE-AUTHOR")["reason_code"])
    def test_review_mutation(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(head_sha="0"*40))))
    def test_circular_authority(self):self.assertEqual("CIRCULAR_RELEASE_AUTHORITY",self.finding("F-AUTHORITY-GRAPH")["reason_code"])
    def test_break_cycle_changes_expectation(self):self.assertTrue(any("expectation ledger" in e or "too short" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d.update(authority_edges=d["authority_edges"][:1]))))
    def test_prior_disclosure_abstains(self):self.assertEqual(("ABSTAIN","PRIOR_DISCLOSURE_EVIDENCE_MISSING"),(self.finding("F-PRIOR-DISCLOSURE")["disposition"],self.finding("F-PRIOR-DISCLOSURE")["reason_code"]))
    def test_required_prior_disclosure_fails(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["prior_disclosure_evidence"].update(required=True))))
    def test_disposition_coverage(self):self.assertTrue(any("too short" in e or "exact nine" in e for e in self.mutate("disclosure/disposition_ledger.json",lambda d:d.update(supported_dispositions=d["supported_dispositions"][:-1]))))
    def test_ledger_release_authority(self):self.assertTrue(any("False was expected" in e or "cannot authorize" in e for e in self.mutate("disclosure/disposition_ledger.json",lambda d:d.update(external_release_authorized=True))))
    def test_measurement(self):self.assertTrue(any("measurement ledger" in e for e in self.mutate("disclosure/measurement_ledger.json",lambda d:d["bounded_classification"].update(false_positive_count=1))))
    def test_generated_json_drift(self):
        root=self.copy();(root/"disclosure/output/dossier.json").write_text("{}\n");self.assertTrue(any("generated output drift" in e for e in validate(root)))
    def test_generated_review_drift(self):
        root=self.copy();(root/"disclosure/output/review_packet.md").write_text("# stale\n");self.assertTrue(any("generated output drift" in e for e in validate(root)))
    def test_data_classification_closed(self):self.assertTrue(any("synthetic_public" in e for e in self.mutate("disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d.update(data_classification="confidential"))))
if __name__=="__main__":unittest.main()
