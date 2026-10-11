#!/usr/bin/env python3
"""Protected Compendium EDITOR queue activation: all-three preflight/hostile replay."""
import unittest
from unittest.mock import patch,call

import erdos_compendium_editorial_activate as a


def staged(n:int):
    problem,source,_=a.DOCKETS[n]
    return {"number":n,"state":"open",
            "title":f"EC-ED0{n-2554} — Erdős #{problem} — staged reader explanation",
            "labels":[{"name":x} for x in sorted(a.REQUIRED)]}


class EditorialActivationTests(unittest.TestCase):
    def test_exact_three_source_bounded_scope(self):
        self.assertEqual(set(a.DOCKETS),{2556,2557,2558})
        self.assertNotIn(2555,a.DOCKETS)
        self.assertEqual(set(a.OPTIONS),set(a.ISSUE_FIELDS))

    @patch.object(a,"source_return",return_value=610000001)
    @patch.object(a,"project_record",side_effect=lambda n:{"id":None,"queue_class":None})
    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue",side_effect=staged)
    def test_all_three_staged_are_checked_before_any_write(self,issue,fields,gh,member,source):
        rows=a.preflight()
        self.assertEqual([row["issue"] for row in rows],[2556,2557,2558])
        self.assertTrue(all(not row["was_available"] for row in rows))
        self.assertEqual(member.call_count,3)
        self.assertEqual(source.call_count,3)
        self.assertFalse(any("POST" in call.args for call in gh.call_args_list))

    @patch.object(a,"source_return",side_effect=ValueError("source unverified"))
    @patch.object(a,"project_record",return_value={"id":"PVTI_2556","queue_class":"Editorial"})
    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue",side_effect=staged)
    def test_missing_source_blocks_preflight(self,issue,fields,gh,member,source):
        with self.assertRaisesRegex(ValueError,"source unverified"):
            a.preflight()
        self.assertFalse(any("POST" in c.args for c in gh.call_args_list))

    @patch.object(a,"source_return",return_value=9)
    @patch.object(a,"project_record",return_value={"id":"PVTI_2556","queue_class":"Editorial"})
    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue")
    def test_spoofed_lifecycle_never_available(self,issue,fields,gh,member,source):
        d=staged(2556)
        d["labels"].append({"name":"gcl-state:blocked"})
        issue.return_value=d
        with self.assertRaisesRegex(ValueError,"lifecycle drift"):
            a.preflight()

    @patch.object(a,"editorial_option_id",return_value="deadbeef")
    @patch.object(a,"project_record")
    @patch.object(a,"gh")
    def test_bind_three_missing_project_items_then_verify_all(self,gh,record,option):
        created={}
        classified=set()
        def live(n):
            if n not in created:
                return {"id":None,"queue_class":None}
            return {"id":created[n],"queue_class":"Editorial" if n in classified else None}
        def mutate(*args,**kwargs):
            if args[:2]==("project","item-add"):
                n=int(args[args.index("--url")+1].split("/")[-1])
                created[n]=f"PVTI_{n}"
                return {"id":created[n]}
            if args[:2]==("project","item-edit"):
                n=int(args[args.index("--id")+1].split("_")[-1])
                classified.add(n)
                self.assertEqual(args[args.index("--field-id")+1],a.QUEUE_FIELD_ID)
                self.assertEqual(args[args.index("--single-select-option-id")+1],"deadbeef")
                return {}
            self.fail("unexpected GitHub call in Project binding")
        gh.side_effect=mutate
        record.side_effect=live
        rows=[{"issue":n,"project_item":None} for n in a.DOCKETS]
        a.bind_editorial_items(rows)
        self.assertEqual(set(created),set(a.DOCKETS))
        self.assertEqual(classified,set(a.DOCKETS))
        self.assertTrue(all(x["project_class"]=="Editorial" for x in rows))
        self.assertEqual(gh.call_count,6)

    @patch.object(a,"editorial_option_id",return_value="deadbeef")
    @patch.object(a,"project_record")
    @patch.object(a,"gh")
    def test_already_bound_editorial_is_replayed_without_mutation(self,gh,record,option):
        record.side_effect=lambda n:{"id":f"PVTI_{n}","queue_class":"Editorial"}
        rows=[{"issue":n,"project_item":f"PVTI_{n}"} for n in a.DOCKETS]
        a.bind_editorial_items(rows)
        gh.assert_not_called()

    @patch.object(a,"project_record",side_effect=ValueError("conflicting live Queue Class"))
    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue",side_effect=staged)
    def test_wrong_mathematics_class_never_rewritten(self,issue,fields,gh,record):
        with self.assertRaisesRegex(ValueError,"conflicting live Queue Class"):
            a.preflight()
        self.assertFalse(any("POST" in c.args for c in gh.call_args_list))

    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue")
    def test_second_pickup_mode_and_unknown_lifecycle_block_before_project(self,issue,fields,gh):
        for hostile in ("gcl-pickup:reservation-controlled","gcl-state:unknown"):
            row=staged(2556)
            row["labels"].append({"name":hostile})
            issue.return_value=row
            with patch.object(a,"project_record") as project:
                with self.assertRaisesRegex(ValueError,"lifecycle drift"):
                    a.preflight()
                project.assert_not_called()

    @patch.object(a,"gh")
    def test_editorial_option_identity_fails_closed(self,gh):
        gh.return_value={"fields":[{"id":a.QUEUE_FIELD_ID,"name":"Queue Class",
                                    "options":[{"name":"Mathematics","id":"12345678"}]}]}
        with self.assertRaisesRegex(ValueError,"Editorial Project option ID"):
            a.editorial_option_id()
        gh.return_value={"fields":[{"id":a.QUEUE_FIELD_ID,"name":"Queue Class",
                                    "options":[{"name":"Editorial","id":"deadbeef"}]}]}
        self.assertEqual(a.editorial_option_id(),"deadbeef")

    @patch.object(a,"project_record",return_value={"id":"PVTI_2556","queue_class":"Editorial"})
    @patch.object(a,"issue")
    @patch.object(a,"fields",return_value=a.OPTIONS)
    @patch.object(a,"gh",return_value=[])
    def test_verified_post_state_admitted_without_claim(self,gh,fields,issue,member):
        d=staged(2556)
        d["labels"].append({"name":"gcl-state:available"})
        issue.return_value=d
        row={"issue":2556,"project_item":"PVTI_2556","was_available":False}
        a.apply([row])
        self.assertEqual(gh.call_count,2)
        self.assertIn("issue-field-values",gh.call_args_list[0].args[1])
        self.assertEqual(gh.call_args_list[1].kwargs["payload"],{"labels":["gcl-state:available"]})
        self.assertTrue(all("/claim" not in str(c) for c in gh.call_args_list))

    @patch.object(a,"project_record",return_value={"id":"PVTI_2556","queue_class":"Editorial"})
    @patch.object(a,"issue",return_value=staged(2556))
    @patch.object(a,"fields",return_value=a.OPTIONS)
    @patch.object(a,"gh",return_value=[])
    def test_no_available_label_means_failure_even_with_fields(self,gh,fields,issue,member):
        with self.assertRaisesRegex(ValueError,"post-activation"):
            a.apply([{"issue":2556,"project_item":"PVTI_2556","was_available":True}])
        gh.assert_not_called()


if __name__ == "__main__":
    unittest.main()
