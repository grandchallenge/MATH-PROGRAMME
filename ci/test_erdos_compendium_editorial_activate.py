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
    @patch.object(a,"project_membership",side_effect=lambda n:f"PVTI_{n}")
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
    @patch.object(a,"project_membership",return_value="PVTI_2556")
    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue",side_effect=staged)
    def test_missing_source_blocks_preflight(self,issue,fields,gh,member,source):
        with self.assertRaisesRegex(ValueError,"source unverified"):
            a.preflight()
        self.assertFalse(any("POST" in c.args for c in gh.call_args_list))

    @patch.object(a,"source_return",return_value=9)
    @patch.object(a,"project_membership",return_value="PVTI_2556")
    @patch.object(a,"gh",return_value=[])
    @patch.object(a,"fields",return_value={})
    @patch.object(a,"issue")
    def test_spoofed_lifecycle_never_available(self,issue,fields,gh,member,source):
        d=staged(2556)
        d["labels"].append({"name":"gcl-state:blocked"})
        issue.return_value=d
        with self.assertRaisesRegex(ValueError,"lifecycle drift"):
            a.preflight()

    @patch.object(a,"project_membership",return_value="PVTI_2556")
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

    @patch.object(a,"project_membership",return_value="PVTI_2556")
    @patch.object(a,"issue",return_value=staged(2556))
    @patch.object(a,"fields",return_value=a.OPTIONS)
    @patch.object(a,"gh",return_value=[])
    def test_no_available_label_means_failure_even_with_fields(self,gh,fields,issue,member):
        with self.assertRaisesRegex(ValueError,"post-activation"):
            a.apply([{"issue":2556,"project_item":"PVTI_2556","was_available":True}])
        gh.assert_not_called()


if __name__ == "__main__":
    unittest.main()
