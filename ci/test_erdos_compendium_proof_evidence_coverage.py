"""Hostile coverage tests: 1221 immutable identities, no theorem promotion."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from erdos_compendium_proof_evidence_coverage import reconcile

class EvidenceCoverageTests(unittest.TestCase):
    def setUp(self):
        self.registry={"issues":[{"problem_id":n} for n in range(1,1222)]}
        self.pv={"population":{"count":1221},"cohorts":[]}
        self.packets=[]
        for first in range(1,1222,100):
            last=min(first+99,1221)
            cid=f"PV-{first:04d}-{last:04d}"
            self.pv["cohorts"].append({"cohort_id":cid,"first":first,"last":last})
            self.packets.append({"cohort_id":cid,"range":{"first":first,"last":last},
                "items":[{"problem_id":n,"stage_work_items":{
                    x:{"work_status":"UNEXECUTED"} for x in "ABCD"}} for n in range(first,last+1)]})
        self.admissions={"admissions":[],"batches":[]}
        self.files={"governance/erdos_proof_verification/evidence/0561/B_REVIEW.md"}
        self.activity={"record_type":"ERDOS_COMPENDIUM_RECENT_RESEARCH_ACTIVITY/1",
            "activity_candidates":[{"problem_id":561,"source_url":"https://github.com/grandchallenge/MATH-PROGRAMME/issues/3490",
                "mathematical_authority":False}],"truncated_input":False}
    def go(self):
        return reconcile(self.registry,self.pv,self.packets,self.admissions,self.files,self.activity)
    def test_full_coverage_and_stale_snapshot(self):
        x=self.go()
        self.assertEqual((x["catalogue_id_count"],x["cohort_packet_count"],x["stage_slots_count"]),(1221,13,4884))
        self.assertEqual(x["retained_pv_evidence_problem_count"],1)
        self.assertEqual(x["retained_evidence_vs_unexecuted_snapshot_count"],1)
        self.assertEqual(x["active_editorial_delta_candidates"][0]["problem_id"],561)
        self.assertFalse(x["automatic_publication"])
        self.assertFalse(x["actual_pv_receipt_efficacy_assessed"])
    def test_active_lead_never_authorizes_claim(self):
        self.admissions["batches"]=[{"entries":[{"problem_id":561}]}]
        x=self.go()
        self.assertTrue(x["active_editorial_delta_candidates"][0]["editorial_admitted"])
        self.assertFalse(x["active_editorial_delta_candidates"][0]["public_mathematical_status_inferred"])
    def test_missing_packet_fails_closed(self):
        self.packets.pop()
        with self.assertRaises(ValueError):self.go()
    def test_duplicate_problem_fails_closed(self):
        self.packets[0]["items"][1]["problem_id"]=1
        with self.assertRaises(ValueError):self.go()
    def test_unrecognized_phase_fails_closed(self):
        self.packets[0]["items"][0]["stage_work_items"].pop("D")
        with self.assertRaises(ValueError):self.go()
    def test_bounded_leads_not_exhaustive(self):
        self.activity["truncated_input"]=True
        self.assertTrue(self.go()["recent_activity_sample_truncated"])
    def test_out_of_population_editorial_admission_fails(self):
        self.admissions["admissions"]=[{"problem_id":1222}]
        with self.assertRaises(ValueError):self.go()

if __name__ == "__main__":
    unittest.main()
