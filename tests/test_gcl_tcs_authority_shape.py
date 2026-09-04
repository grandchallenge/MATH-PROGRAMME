from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from ci.gcl_tcs_authority_shape import (
    ALL_STATUSES,
    AUTHORITATIVE_SOURCE_STATUSES,
    CANDIDATE_STATUSES,
    TERMINAL_SOURCE_STATUSES,
    authority_shape_errors,
    status_shape,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-conformance.schema.json"
TEMPLATE_PATH = ROOT / "docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.conformance.template.yaml"


class GclTcsAuthorityShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.template = yaml.safe_load(TEMPLATE_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_canonical_schema_has_disjoint_complete_authority_shapes(self) -> None:
        self.assertEqual(authority_shape_errors(self.schema), [])

    def test_candidate_template_validates(self) -> None:
        self.assertEqual(list(self.validator.iter_errors(copy.deepcopy(self.template))), [])

    def test_each_governed_authority_status_validates_exactly_one_top_level_shape(self) -> None:
        for status in sorted(ALL_STATUSES):
            record = copy.deepcopy(self.template)
            record["authority_status"] = status
            with self.subTest(status=status):
                self.assertEqual(list(self.validator.iter_errors(record)), [])
                self.assertIsNotNone(status_shape(status))

    def test_candidate_is_not_an_authoritative_source_shape(self) -> None:
        candidate_shape = self.schema["$defs"]["candidateRecordShape"]
        source_shape = self.schema["$defs"]["authoritativeSourceRecordShape"]
        record = {"authority_status": "candidate"}
        self.assertEqual(list(Draft202012Validator(candidate_shape).iter_errors(record)), [])
        self.assertTrue(list(Draft202012Validator(source_shape).iter_errors(record)))

    def test_admitted_is_source_not_candidate(self) -> None:
        candidate_shape = self.schema["$defs"]["candidateRecordShape"]
        source_shape = self.schema["$defs"]["authoritativeSourceRecordShape"]
        record = {"authority_status": "admitted"}
        self.assertTrue(list(Draft202012Validator(candidate_shape).iter_errors(record)))
        self.assertEqual(list(Draft202012Validator(source_shape).iter_errors(record)), [])

    def test_authoritative_is_source_not_candidate(self) -> None:
        candidate_shape = self.schema["$defs"]["candidateRecordShape"]
        source_shape = self.schema["$defs"]["authoritativeSourceRecordShape"]
        record = {"authority_status": "authoritative"}
        self.assertTrue(list(Draft202012Validator(candidate_shape).iter_errors(record)))
        self.assertEqual(list(Draft202012Validator(source_shape).iter_errors(record)), [])

    def test_terminal_statuses_are_neither_candidate_nor_active_source(self) -> None:
        candidate_shape = self.schema["$defs"]["candidateRecordShape"]
        source_shape = self.schema["$defs"]["authoritativeSourceRecordShape"]
        terminal_shape = self.schema["$defs"]["terminalSourceRecordShape"]
        for status in sorted(TERMINAL_SOURCE_STATUSES):
            record = {"authority_status": status}
            with self.subTest(status=status):
                self.assertTrue(list(Draft202012Validator(candidate_shape).iter_errors(record)))
                self.assertTrue(list(Draft202012Validator(source_shape).iter_errors(record)))
                self.assertEqual(list(Draft202012Validator(terminal_shape).iter_errors(record)), [])

    def test_unknown_authority_status_fails_closed(self) -> None:
        record = copy.deepcopy(self.template)
        record["authority_status"] = "source"
        self.assertTrue(list(self.validator.iter_errors(record)))
        self.assertIsNone(status_shape("source"))

    def test_status_domains_are_explicit_and_nonoverlapping(self) -> None:
        self.assertEqual(CANDIDATE_STATUSES, {"candidate"})
        self.assertEqual(AUTHORITATIVE_SOURCE_STATUSES, {"admitted", "authoritative"})
        self.assertEqual(TERMINAL_SOURCE_STATUSES, {"superseded", "withdrawn"})
        self.assertFalse(CANDIDATE_STATUSES & AUTHORITATIVE_SOURCE_STATUSES)
        self.assertFalse(CANDIDATE_STATUSES & TERMINAL_SOURCE_STATUSES)
        self.assertFalse(AUTHORITATIVE_SOURCE_STATUSES & TERMINAL_SOURCE_STATUSES)


if __name__ == "__main__":
    unittest.main()
