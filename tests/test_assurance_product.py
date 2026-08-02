from __future__ import annotations
import json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"ci"))
from assure_evaluate import canonical,evaluate
from assure_pr import validate

class AssuranceTests(unittest.TestCase):
    def copy(self)->Path:
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);dst=Path(tmp.name)
        for rel in ("assurance","schemas","ci"):shutil.copytree(ROOT/rel,dst/rel)
        return dst
    @staticmethod
    def read(root:Path,rel:str)->dict:return json.loads((root/rel).read_text())
    @staticmethod
    def write(root:Path,rel:str,data:dict)->None:(root/rel).write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    def mutate(self,rel:str,fn)->list[str]:
        root=self.copy();data=self.read(root,rel);fn(data);self.write(root,rel,data);return validate(root)
    def test_valid(self):self.assertEqual([],validate())
    def test_deterministic(self):self.assertEqual(canonical(evaluate(ROOT/"assurance/fixtures/GCL-ASSURE-PR-001")),canonical(evaluate(ROOT/"assurance/fixtures/GCL-ASSURE-PR-001")))
    def test_product_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("assurance/product_contract.json",lambda d:d.update(extra=True))))
    def test_manifest_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d.update(extra=True))))
    def test_head_drift(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(subject_head="0"*40))))
    def test_digest_drift(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["artifacts"][0].update(expected_sha256="0"*64))))
    def test_required_missing(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["artifacts"][2].update(required=True))))
    def test_optional_missing_abstains(self):
        f=next(x for x in evaluate(ROOT/"assurance/fixtures/GCL-ASSURE-PR-001")["findings"] if x["finding_id"]=="F-ART-MISSING");self.assertEqual(("ABSTAIN","OPTIONAL_EVIDENCE_MISSING"),(f["disposition"],f["reason_code"]))
    def test_fabricated_workflow(self):
        f=next(x for x in evaluate(ROOT/"assurance/fixtures/GCL-ASSURE-PR-001")["findings"] if x["finding_id"]=="F-WF-FABRICATED");self.assertEqual("FABRICATED_WORKFLOW_SUCCESS",f["reason_code"])
    def test_workflow_head_mismatch(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/evidence/workflows.json",lambda d:d["runs"][0].update(head_sha="0"*40))))
    def test_review_head_mismatch(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(head_sha="0"*40))))
    def test_review_contradiction(self):
        f=next(x for x in evaluate(ROOT/"assurance/fixtures/GCL-ASSURE-PR-001")["findings"] if x["finding_id"]=="F-REVIEW-STATE");self.assertEqual("UNRESOLVED_CHANGES_REQUESTED",f["reason_code"])
    def test_circular_authority(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["authority_edges"].append({"source":"claim:C-IDENTITY","target":"candidate:head"}))))
    def test_policy_leakage(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["policy_profile"]["rules"].__setitem__(0,"MATHFORGE private rule"))))
    def test_private_policy_schema(self):self.assertTrue(any("False was expected" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["policy_profile"].update(embedded_private_policy=True))))
    def test_confidential_data(self):self.assertTrue(any("False was expected" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["privacy"].update(contains_customer_secrets=True))))
    def test_unsupported_claim(self):self.assertTrue(any("expected claim disposition" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["claims"][3].update(expected_disposition="PASS"))))
    def test_unknown_evidence(self):self.assertTrue(any("expectation ledger" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/manifest.json",lambda d:d["claims"][0].update(evidence_refs=["F-UNKNOWN"]))))
    def test_claim_promotion(self):self.assertTrue(any("False was expected" in e or "claim-boundary" in e for e in self.mutate("assurance/product_contract.json",lambda d:d["claim_boundaries"].update(certificate_issued=True))))
    def test_external_use(self):self.assertTrue(any("False was expected" in e for e in self.mutate("assurance/product_contract.json",lambda d:d["activation"].update(external_use_authorized=True))))
    def test_aether_dependency(self):self.assertTrue(any("False was expected" in e for e in self.mutate("assurance/product_contract.json",lambda d:d["core_contract"].update(aether_required=True))))
    def test_self_authentication(self):self.assertTrue(any("False was expected" in e or "self-authenticating" in e for e in self.mutate("assurance/product_contract.json",lambda d:d["review_packet"][0].update(may_self_authenticate=True))))
    def test_component_coverage(self):self.assertTrue(any("component ledger" in e for e in self.mutate("assurance/component_disposition_ledger.json",lambda d:d.update(components=[x for x in d["components"] if x["disposition"]!="no_release"]))))
    def test_release_authority(self):self.assertTrue(any("cannot authorize" in e for e in self.mutate("assurance/component_disposition_ledger.json",lambda d:d.update(external_release_authorized=True))))
    def test_measurement(self):self.assertTrue(any("measurement ledger" in e for e in self.mutate("assurance/measurement_ledger.json",lambda d:d["bounded_classification"].update(false_positive_count=1))))
    def test_generated_json_drift(self):
        root=self.copy();(root/"assurance/output/dossier.json").write_text("{}\n");self.assertTrue(any("generated output drift" in e for e in validate(root)))
    def test_generated_review_drift(self):
        root=self.copy();(root/"assurance/output/review_packet.md").write_text("# stale\n");self.assertTrue(any("generated output drift" in e for e in validate(root)))
    def test_workflow_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/evidence/workflows.json",lambda d:d["runs"][0].update(extra=True))))
    def test_review_schema_closed(self):self.assertTrue(any("Additional properties" in e for e in self.mutate("assurance/fixtures/GCL-ASSURE-PR-001/evidence/reviews.json",lambda d:d["reviews"][0].update(extra=True))))
if __name__=="__main__":unittest.main()
