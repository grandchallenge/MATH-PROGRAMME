"""Recent issue scans are leads, never formal proofs or editorial admissions."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from erdos_compendium_research_activity import read_activity

class ResearchActivityTests(unittest.TestCase):
    def setUp(self):
        self.registry={"issues":[{"issue_number":10000+n,"problem_id":n} for n in range(1,1222)]}
        self.sources={"MATH-PROGRAMME":{"total_count":1,"items":[{"number":10579,"title":"[GCL-ERDOS] task","updated_at":"2026-11-21T00:00:00Z","html_url":"https://github.com/grandchallenge/MATH-PROGRAMME/issues/10579"}]},"MATHSOLVE":{"total_count":1,"items":[{"number":22,"title":"Erdős #579 proof step","updated_at":"2026-11-21T01:00:00Z","html_url":"https://github.com/grandchallenge/MATHSOLVE/issues/22"}]},"MATHCERT":{"total_count":0,"items":[]}}
    def test_two_distinct_sources_index_without_claim(self):
        result=read_activity(self.registry,self.sources)
        self.assertEqual(2,result["matching_source_issues_observed"])
        self.assertFalse(result["automatic_status_promotion"])
        self.assertTrue(all(not x["mathematical_authority"] for x in result["activity_candidates"]))
    def test_truncated_source_explicit(self):
        self.sources["MATHSOLVE"]["total_count"]=500
        self.assertTrue(read_activity(self.registry,self.sources)["truncated_input"])
    def test_not_every_issue_is_an_erdos_result(self):
        self.sources["MATHSOLVE"]["items"][0]["title"]="Other mathematics issue"
        self.assertEqual(1,read_activity(self.registry,self.sources)["matching_source_issues_observed"])
    def test_fail_missing_pagination(self):
        self.sources["MATHCERT"].pop("total_count")
        with self.assertRaises(ValueError):
            read_activity(self.registry,self.sources)
if __name__=="__main__":unittest.main()
