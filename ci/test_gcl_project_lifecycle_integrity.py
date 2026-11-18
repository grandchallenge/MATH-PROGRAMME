import unittest
from unittest.mock import patch
import json
from types import SimpleNamespace
import ci.gcl_project_lifecycle_integrity as integrity
from ci.gcl_project_lifecycle_integrity import validate, EXPECTED_STATUS, AVAILABLE_FILTER

FIELDS = [{"name":"Status","options":[{"name":s} for s in EXPECTED_STATUS]},
          {"name":"GCL State","options":[]}]
VIEWS = [{"name":"AVAILABLE","filter":AVAILABLE_FILTER}]

def row(number=1, state="OPEN", status="Todo", labels=(), duplicate=None):
    return {"id":str(number), "content":{"number":number,"state":state,
        "repository":{"nameWithOwner":"grandchallenge/MATHSOLVE"},
        "labels":{"totalCount":len(labels),"nodes":[{"name":x} for x in labels]}},
        "fieldValueByName":{"name":status}, "duplicate":duplicate}

class IntegrityTests(unittest.TestCase):
    def test_metadata_once_across_paginated_graphql(self):
        def response(args, **kwargs):
            cursor = "after=" in " ".join(args)
            project = {"id":integrity.PROJECT,"items":{"nodes":[row(number=2 if cursor else 1)],
                "pageInfo":{"hasNextPage":not cursor,"endCursor":"cursor-1" if not cursor else None}}}
            if not cursor:
                project.update(fields={"nodes":FIELDS},views={"nodes":VIEWS})
            return SimpleNamespace(stdout=json.dumps({"data":{"organization":{"projectV2":project}}}))
        with patch.object(integrity.subprocess,"run",side_effect=response) as run:
            with patch("builtins.print") as output:
                self.assertEqual(integrity.main(),0)
        self.assertEqual(run.call_count,2)
        first,second=[x.args[0] for x in run.call_args_list]
        self.assertIn("includeMetadata=true",first)
        self.assertIn("includeMetadata=false",second)
        self.assertIn("after=cursor-1",second)

    def test_healthy_available(self):
        r=validate(FIELDS,VIEWS,[row(labels=["gcl-state:available"])])
        self.assertEqual(r["status"],"PASS")
        self.assertEqual(r["counts"]["available"],1)
    def test_duplicate_project_field_options_rejected(self):
        f=[FIELDS[0],{"name":"GCL State","options":[{"name":"AVAILABLE"}]}]
        self.assertIn("PROJECT_GCL_STATE_DUPLICATE_CONFIGURED",validate(f,VIEWS,[])["errors"])
    def test_closed_active_rejected(self):
        self.assertTrue(any("CLOSED_ACTIVE_STATUS" in x for x in
            validate(FIELDS,VIEWS,[row(state="CLOSED")])["errors"]))
    def test_closed_available_rejected(self):
        self.assertTrue(any("CLOSED_AVAILABLE" in x for x in
            validate(FIELDS,VIEWS,[row(state="CLOSED",labels=["gcl-state:available"])])["errors"]))
    def test_open_done_notice_not_auto_repair(self):
        r=validate(FIELDS,VIEWS,[row(status="Done")])
        self.assertFalse(r["errors"])
        self.assertTrue(any("OPEN_DONE" in x for x in r["notices"]))
    def test_open_done_returned_is_valid_custody(self):
        r=validate(FIELDS,VIEWS,[row(status="Done",labels=["gcl-state:returned"])])
        self.assertEqual(r["status"],"PASS")
        self.assertEqual(r["counts"]["returned"],1)
    def test_closed_active_returned_still_rejected(self):
        r=validate(FIELDS,VIEWS,[row(state="CLOSED",status="In Progress",labels=["gcl-state:returned"])])
        self.assertTrue(any("CLOSED_ACTIVE_STATUS" in x for x in r["errors"]))
    def test_conflicting_labels(self):
        self.assertTrue(any("CONFLICTING" in x for x in validate(FIELDS,VIEWS,
            [row(labels=["gcl-state:available","gcl-state:returned"])])["errors"]))
    def test_view_drift(self):
        self.assertIn("AVAILABLE_VIEW_DRIFT",validate(FIELDS,[],[])["errors"])
    def test_status_schema_drift(self):
        self.assertIn("STATUS_SCHEMA_DRIFT",validate([],VIEWS,[])["errors"])
    def test_duplicate_field_populated(self):
        self.assertTrue(any("DUPLICATE_POPULATED" in x for x in validate(FIELDS,VIEWS,
            [row(duplicate={"name":"AVAILABLE"})])["errors"]))
    def test_label_truncation(self):
        r=row()
        r["content"]["labels"]["totalCount"]=101
        self.assertTrue(any("LABELS_TRUNCATED" in x for x in validate(FIELDS,VIEWS,[r])["errors"]))

if __name__=="__main__":
    unittest.main()
