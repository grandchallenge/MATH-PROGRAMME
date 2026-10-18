from __future__ import annotations
import copy
import unittest
from unittest.mock import patch
from ci import programme_review_gate_migration as m

RULES = {
    "id": 17137629,
    "name": "Programme profile - main",
    "target": "branch",
    "enforcement": "active",
    "bypass_actors": [
        {"actor_id":4423678,"actor_type":"Integration","bypass_mode":"pull_request"}
    ],
    "conditions":{"ref_name":{"include":["~DEFAULT_BRANCH"],"exclude":[]}},
    "rules":[
        {"type":"pull_request","parameters":{
            "required_approving_review_count":1,
            "require_last_push_approval":True,
            "require_extra_approval_for_unattributed_changes":True,
            "required_review_thread_resolution":True
        }},
        {"type":"required_status_checks","parameters":{
            "required_status_checks":[{"context":x} for x in [
                "validate-json", "formal-validation / formal-validation",
                "policy / policy","security / action-policy"
            ]]
        }}
    ]
}
QUEUE={
    "id":21969152,"name":"GH-OS universal execution routing",
    "target":"branch","enforcement":"active","bypass_actors":[],
    "conditions":{"ref_name":{"include":["~DEFAULT_BRANCH"],"exclude":[]}},
    "rules":[
        {"type":"required_status_checks","parameters":{
            "required_status_checks":[{"context":"routing-enforcement"}]
        }},
        {"type":"merge_queue","parameters":{"merge_method":"MERGE"}}
    ],
}

class FakeClient:
    def __init__(self, bad_update=False):
        self.main=copy.deepcopy(RULES)
        self.queue=copy.deepcopy(QUEUE)
        self.puts=0
        self.bad_update=bad_update
    def request(self,method,path,data=None):
        if path.endswith("/21969152"):
            assert method=="GET"
            return copy.deepcopy(self.queue)
        if path.endswith("/17137629") and method=="PUT":
            self.puts+=1
            self.main.update(copy.deepcopy(data))
            if self.bad_update:
                self.main["rules"][1]["parameters"]["required_status_checks"]= [{"context":"wrong"}]
            return copy.deepcopy(self.main)
        if path.endswith("/17137629") and method=="GET":
            return copy.deepcopy(self.main)
        raise AssertionError((method,path))

class NarrowMigrationTests(unittest.TestCase):
    def test_contract_is_exact_and_target_zero(self):
        c=m.load_contract()
        self.assertEqual(c["to"],{
            "required_approving_review_count":0,
            "require_last_push_approval":False,
        })

    def test_only_two_live_pr_parameters_change(self):
        client=FakeClient()
        with patch.object(m,"branch_ruleset",side_effect=lambda _client,_repo:copy.deepcopy(client.main)):
            out=m.migrate(client,apply=True)
        self.assertEqual(client.puts,1)
        self.assertEqual(out["after_review"],m.load_contract()["to"])
        self.assertTrue(out["merge_queue_preserved"])
        self.assertTrue(client.main["rules"][0]["parameters"]["require_extra_approval_for_unattributed_changes"])
        self.assertTrue(client.main["rules"][0]["parameters"]["required_review_thread_resolution"])

    def test_idempotent_second_run(self):
        client=FakeClient()
        with patch.object(m,"branch_ruleset",side_effect=lambda _client,_repo:copy.deepcopy(client.main)):
            m.migrate(client,apply=True)
            out=m.migrate(client,apply=True)
        self.assertFalse(out["mutated"])
        self.assertEqual(client.puts,1)

    def test_fail_on_unexpected_source_policy(self):
        client=FakeClient()
        client.main["rules"][0]["parameters"]["required_approving_review_count"]=2
        with patch.object(m,"branch_ruleset",side_effect=lambda _client,_repo:copy.deepcopy(client.main)):
            with self.assertRaisesRegex(ValueError,"neither exact predecessor"):
                m.migrate(client,apply=True)
        self.assertEqual(client.puts,0)

    def test_protection_drift_after_mutation_is_detected(self):
        client=FakeClient(bad_update=True)
        with patch.object(m,"branch_ruleset",side_effect=lambda _client,_repo:copy.deepcopy(client.main)):
            with self.assertRaisesRegex(ValueError,"required checks drift"):
                m.migrate(client,apply=True)

    def test_ghos_queue_snapshot_preserves_without_pr_rule(self):
        self.assertEqual(m.projected(copy.deepcopy(QUEUE)),m.projected(copy.deepcopy(QUEUE)))


if __name__ == "__main__":
    unittest.main()
