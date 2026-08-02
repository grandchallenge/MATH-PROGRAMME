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
    def test_deterministic(self):
        fixture=ROOT/"disclosure/fixtures/GCL-DISCLOSE-PR-001"
        self.assertEqual(canonical(evaluate(fixture)),canonical(evaluate(fixture)))
    def test_generated_json_drift(self):
        root=self.copy();(root/"disclosure/output/dossier.json").write_text("{}\n");self.assertTrue(any("generated output drift" in e for e in validate(root)))
    def test_generated_review_drift(self):
        root=self.copy();(root/"disclosure/output/review_packet.md").write_text("# stale\n");self.assertTrue(any("generated output drift" in e for e in validate(root)))

MUTATIONS=[
("product_schema_closed","disclosure/product_contract.json",lambda d:d.update(extra=True),("Additional properties",)),
("manifest_schema_closed","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d.update(extra=True),("Additional properties",)),
("review_schema_closed","disclosure/fixtures/GCL-DISCLOSE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(extra=True),("Additional properties",)),
("ledger_schema_closed","disclosure/disposition_ledger.json",lambda d:d.update(extra=True),("Additional properties",)),
("activation_drift","disclosure/product_contract.json",lambda d:d["activation"].update(required_conditions=["protected_merge"]),("too short","activation")),
("external_release_prohibited","disclosure/product_contract.json",lambda d:d["activation"].update(external_release_authorized=True),("False was expected",)),
("claim_promotion_prohibited","disclosure/product_contract.json",lambda d:d["claim_boundaries"].update(patentability_determined=True),("False was expected","claim-boundary")),
("aether_dependency_prohibited","disclosure/product_contract.json",lambda d:d["core_contract"].update(aether_required=True),("False was expected",)),
("confidential_processing_prohibited","disclosure/product_contract.json",lambda d:d["core_contract"].update(confidential_data_allowed=True),("False was expected",)),
("self_authentication_prohibited","disclosure/product_contract.json",lambda d:d["review_packet"][0].update(may_self_authenticate=True),("False was expected","self-authenticating")),
("identity_drift","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(commit="0"*40),("expectation ledger",)),
("digest_drift","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(expected_sha256="0"*64),("expectation ledger",)),
("required_missing","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:next(a for a in d["artifacts"] if a["artifact_id"]=="ART-MISSING").update(required=True),("expectation ledger",)),
("classification_head_mismatch","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["classification_cases"][0].update(subject_head="0"*40),("expectation ledger",)),
("classification_supersession","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["classification_cases"][0].update(superseded_by="CLASS-NEW"),("expectation ledger",)),
("hold_head_mismatch","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["hold_cases"][0].update(subject_head="0"*40),("expectation ledger",)),
("professional_review_changes_novelty","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["claim_cases"][2].update(professional_review_present=True),("expectation ledger",)),
("review_mutation","disclosure/fixtures/GCL-DISCLOSE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(head_sha="0"*40),("expectation ledger",)),
("break_cycle","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d.update(authority_edges=d["authority_edges"][:1]),("expectation ledger","too short")),
("required_prior_disclosure","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["prior_disclosure_evidence"].update(required=True),("expectation ledger",)),
("disposition_coverage","disclosure/disposition_ledger.json",lambda d:d.update(supported_dispositions=d["supported_dispositions"][:-1]),("too short","exact nine")),
("ledger_release_authority","disclosure/disposition_ledger.json",lambda d:d.update(external_release_authorized=True),("False was expected","cannot authorize")),
("measurement_drift","disclosure/measurement_ledger.json",lambda d:d["bounded_classification"].update(false_positive_count=1),("measurement ledger",)),
("data_classification_closed","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d.update(data_classification="confidential"),("synthetic_public",)),
("blob_drift","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(blob="0"*40),("expectation ledger",)),
("classification_expiry","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["classification_cases"][0].update(expires_at="2025-08-02"),("expectation ledger",)),
("active_hold_expiry_contradiction","disclosure/fixtures/GCL-DISCLOSE-PR-001/manifest.json",lambda d:d["hold_cases"][0].update(expires_at="2025-08-02"),("expectation ledger",)),
("review_expiry","disclosure/fixtures/GCL-DISCLOSE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(expires_at="2025-08-02"),("expectation ledger",)),
]

def mutation_test(rel,mutator,tokens):
    def test(self):
        errors=self.mutate(rel,mutator);self.assertTrue(any(any(token in error for token in tokens) for error in errors),errors)
    return test
for name,rel,mutator,tokens in MUTATIONS:setattr(DisclosureTests,"test_"+name,mutation_test(rel,mutator,tokens))

FINDINGS=[
("optional_missing_abstains","F-ART-MISSING","ABSTAIN","OPTIONAL_EVIDENCE_MISSING"),
("release_note_bound","F-ART-NOTE","PASS","EXACT_ARTIFACT_MATCH"),
("classification_absent_abstains","F-CLASS-MISSING","ABSTAIN","CLASSIFICATION_ABSENT"),
("active_hold_fails","F-HOLD-ACTIVE","FAIL","ACTIVE_NO_RELEASE_HOLD"),
("stale_hold_fails","F-HOLD-STALE","FAIL","STALE_HOLD_USED_AS_AUTHORITY"),
("attribution_complete","F-ATTR-COMPLETE","PASS","ATTRIBUTION_COMPLETE"),
("attribution_missing","F-ATTR-MISSING","FAIL","ATTRIBUTION_INCOMPLETE"),
("approved_claim","F-CLAIM-APPROVED","PASS","APPROVED_CLAIM_EXACT"),
("claim_inflation","F-CLAIM-INFLATED","FAIL","CLAIM_EXCEEDS_APPROVED_LANGUAGE"),
("unsupported_ip_language","F-CLAIM-NOVELTY","FAIL","UNSUPPORTED_IP_LANGUAGE"),
("public_export","F-CONF-PUBLIC","PASS","SYNTHETIC_PUBLIC_EXPORT"),
("confidential_leak","F-CONF-LEAK","FAIL","CONFIDENTIAL_EXPORT_LEAK"),
("exact_review","F-REVIEW-EXACT","PASS","EXACT_NON_AUTHOR_REVIEW"),
("review_head_mismatch","F-REVIEW-MISMATCH","FAIL","REVIEW_HEAD_MISMATCH"),
("author_only_authority","F-RELEASE-AUTHOR","FAIL","AUTHOR_ONLY_RELEASE_AUTHORITY"),
("circular_authority","F-AUTHORITY-GRAPH","FAIL","CIRCULAR_RELEASE_AUTHORITY"),
("prior_disclosure_abstains","F-PRIOR-DISCLOSURE","ABSTAIN","PRIOR_DISCLOSURE_EVIDENCE_MISSING"),
]
def finding_test(fid,disposition,reason):
    def test(self):
        item=self.finding(fid);self.assertEqual((disposition,reason),(item["disposition"],item["reason_code"]))
    return test
for name,fid,disposition,reason in FINDINGS:setattr(DisclosureTests,"test_"+name,finding_test(fid,disposition,reason))

if __name__=="__main__":unittest.main()
