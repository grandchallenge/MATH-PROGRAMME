#!/usr/bin/env python3
"""Independent positive/hostile tests for bounded Compendium direct returns."""
import unittest
import erdos_compendium_direct_return_projector as m

SHA="a"*40

def issue(n=2556, labels=None):
    assignment,p,source=m.DOCKETS[n]
    names=labels if labels is not None else [*m.ASSIGNMENT_LABELS,"gcl-state:available"]
    return {"number":n,"state":"open",
            "title":f"{assignment} — Erdős #{p} — exact editorial assignment",
            "body":f"Parent: https://github.com/{m.REPO}/issues/2552\n"
                   f"Source: https://github.com/{m.REPO}/issues/{source}",
            "labels":[{"name":x} for x in names]}

def fields(state="AVAILABLE"):
    d={"GCL State":state,"GCL Campaign":m.CAMPAIGN,"GCL Role":"CONSTRUCTIVE",
       "GCL Collaboration":"COOPERATIVE","GCL Phase":"SHARED",
       "GCL Cohort":"ERDOS-COMPENDIUM-EDITORIAL-TRANCHE-001"}
    return [{"issue_field_name":k,"single_select_option":{"name":v}}
            for k,v in d.items()]

def result(n=2556,actor="fyremael",disposition="DRAFT_PR"):
    assignment,p,source=m.DOCKETS[n]
    body="\n".join([
        "RESULT/1",f"ASSIGNMENT_ID: {assignment}",f"PROBLEM_ID: {p}",
        f"DISPOSITION: {disposition}",
        f"SOURCE_AUDIT: https://github.com/{m.REPO}/issues/{source}",
        "SOURCE_CLAIMS: source statement checked; critical review pending",
        "EXAMPLE_CHECK: tested finite congruence cover counterexample",
        f"PR_OR_REVIEW: https://github.com/{m.REPO}/pull/1 head {SHA}",
        "CRITICAL_PASS: pending independent role-reviewed pass",
        "GITHUB_RENDER: UNVERIFIED","MKDOCS_RENDER: UNVERIFIED",
        "PUBLIC_HTML: PENDING","BLOCKERS: source critical pass pending",
        f"GITHUB_ACTOR: {actor}",""
    ])
    return {"id":12345678,"body":body,"user":{"login":"fyremael"}}

class CompendiumReturnTests(unittest.TestCase):
    def test_real_bound_comment_is_evidence_only_without_lease(self):
        r=m.evaluate(issue(),fields(),[result()])
        self.assertTrue(r["project"])
        self.assertEqual(r["state_to_write"],"RETURNED")
        self.assertEqual(r["comment_id"],12345678)
        self.assertEqual(r["authenticated_actor"],"fyremael")
        self.assertFalse(r["requires_solve_reservation"])
        self.assertFalse(r["editorial_accepted"])
        self.assertFalse(r["publication_authorized"])

    def test_all_three_exact_dockets_are_supported(self):
        for n in m.DOCKETS:
            with self.subTest(n=n):
                r=m.evaluate(issue(n),fields(),[result(n)])
                self.assertTrue(r["project"])

    def test_wrong_assignment_source_and_problem_block(self):
        for old,new in [("ASSIGNMENT_ID: EC-ED02","ASSIGNMENT_ID: EC-ED04"),
                        ("PROBLEM_ID: 7","PROBLEM_ID: 8"),
                        ("issues/1276","issues/1277")]:
            c=result()
            c["body"]=c["body"].replace(old,new)
            self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])

    def test_authenticated_actor_mismatch_and_forged_bot_block(self):
        c=result(actor="somebodyelse")
        self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])
        c=result()
        c["user"]={"login":"github-actions[bot]"}
        self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])

    def test_malformed_or_duplicate_result_fields_block(self):
        c=result()
        c["body"]=c["body"].replace("PROBLEM_ID: 7\n","")
        self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])
        c=result()
        c["body"]+="ASSIGNMENT_ID: EC-ED02\n"
        self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])

    def test_dual_route_unknown_class_or_stale_fields_block(self):
        x=issue(labels=[*m.ASSIGNMENT_LABELS,
                        "gcl-state:available","gcl-pickup:reservation-controlled"])
        self.assertFalse(m.evaluate(x,fields(),[result()])["project"])
        x=issue(labels=[*m.ASSIGNMENT_LABELS,"gcl-state:blocked"])
        self.assertFalse(m.evaluate(x,fields(),[result()])["project"])
        stale=fields()
        stale[1]["single_select_option"]["name"]="WRONG"
        self.assertFalse(m.evaluate(issue(),stale,[result()])["project"])

    def test_returned_is_idempotent_and_partial_write_repairable(self):
        labels=[*m.ASSIGNMENT_LABELS,"gcl-state:returned"]
        self.assertEqual(m.evaluate(issue(labels=labels),fields("RETURNED"),[result()])["reason"],
                         "already_returned")
        labels=[*m.ASSIGNMENT_LABELS,"gcl-state:available"]
        r=m.evaluate(issue(labels=labels),fields("RETURNED"),[result()])
        self.assertTrue(r["project"])
        self.assertTrue(r["repair_incomplete_transition"])

    def test_return_label_write_interruption_is_idempotently_repairable(self):
        both=[*m.ASSIGNMENT_LABELS,"gcl-state:available","gcl-state:returned"]
        r=m.evaluate(issue(labels=both),fields("RETURNED"),[result()])
        self.assertTrue(r["project"])
        self.assertTrue(r["repair_incomplete_transition"])
        self.assertFalse(r["publication_authorized"])
        forged=[*m.ASSIGNMENT_LABELS,"gcl-state:unknown"]
        self.assertFalse(m.evaluate(issue(labels=forged),fields("RETURNED"),[result()])["project"])

    def test_worker_failure_return_is_allowed_without_fictional_pr(self):
        c=result(disposition="BLOCKED")
        c["body"]=c["body"].replace(f"https://github.com/{m.REPO}/pull/1 head {SHA}",
                                   "NONE: source unavailable")
        r=m.evaluate(issue(),fields(),[c])
        self.assertTrue(r["project"])
        self.assertEqual(r["self_reported_disposition"],"BLOCKED")

    def test_wrong_issue_and_duplicate_transport_ids_block(self):
        self.assertFalse(m.evaluate(issue(2556)|{"number":1234},fields(),[result()])["project"])
        c=result()
        self.assertFalse(m.evaluate(issue(),fields(),[c,c])["project"])
        c["id"]=None
        self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])

    def test_invalid_pr_head_not_published_as_draft_result(self):
        c=result()
        c["body"]=c["body"].replace(SHA,"HEAD_UNKNOWN")
        self.assertFalse(m.evaluate(issue(),fields(),[c])["project"])

if __name__=="__main__":
    unittest.main()
