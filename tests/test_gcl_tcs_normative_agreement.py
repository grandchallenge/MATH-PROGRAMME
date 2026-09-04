from __future__ import annotations

import copy
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from ci.gcl_tcs_normative_agreement import (
    DECL_SCHEMA,
    EXPECTED_SOURCE_SHA256,
    HISTORICAL_MANIFEST,
    POLICY,
    RECORD_SCHEMA,
    RECORD_TEMPLATE,
    _load_json,
    _load_yaml,
    historical_manifest_errors,
    load_matrix,
    policy_contract_errors,
    repository_agreement_errors,
    schema_contract_errors,
    source_coverage_errors,
    source_digest,
    template_contract_errors,
)


class GclTcsNormativeAgreementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = load_matrix()
        cls.policy = _load_yaml(POLICY)
        cls.decl_schema = _load_json(DECL_SCHEMA)
        cls.record_schema = _load_json(RECORD_SCHEMA)
        cls.decl_template = _load_yaml(Path("docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.conformance.template.yaml"))
        cls.record_template = _load_yaml(RECORD_TEMPLATE)
        cls.historical = _load_yaml(HISTORICAL_MANIFEST)

    def test_live_repository_agreement_is_clean(self) -> None:
        self.assertEqual(repository_agreement_errors(), [])

    def test_normative_source_digest_is_fixed(self) -> None:
        self.assertEqual(source_digest(), EXPECTED_SOURCE_SHA256)

    def test_matrix_is_clause_level_and_has_no_open_gap(self) -> None:
        rows = self.matrix["rows"]
        self.assertEqual(self.matrix["row_count"], 119)
        self.assertGreaterEqual(len(rows), 100)
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        self.assertTrue(all(row["gap"] in {"CLOSED", "NOT_MACHINE_CHECKABLE"} for row in rows))

    def test_every_hard_and_strong_source_paragraph_is_covered(self) -> None:
        self.assertEqual(source_coverage_errors(self.matrix), [])

    def test_missing_source_row_fails_coverage(self) -> None:
        broken = copy.deepcopy(self.matrix)
        source = "council_submissions/GCL-TCS-00/parts/00-frontmatter-purpose-principles.md"
        broken["rows"] = [r for r in broken["rows"] if r["source"] != source]
        self.assertTrue(any("source_uncovered" in err or "uncovered_normative_clause" in err for err in source_coverage_errors(broken)))

    def test_policy_candidate_identity_and_source_binding(self) -> None:
        self.assertEqual(policy_contract_errors(self.policy), [])
        self.assertEqual(self.policy["standard"]["status"], "candidate")
        self.assertTrue(self.policy["normative_source_contract"]["source_controls_meaning"])
        self.assertTrue(self.policy["normative_source_contract"]["machine_surfaces_are_derivative"])

    def test_policy_missing_normative_review_field_fails(self) -> None:
        broken = copy.deepcopy(self.policy)
        broken["record_contracts"]["review"]["required_fields"].remove("reviewed_revision")
        self.assertIn("policy: record_contract_fields:review", policy_contract_errors(broken))

    def test_declaration_schema_locks_standard_and_profile_versions(self) -> None:
        self.assertEqual(schema_contract_errors(self.decl_schema, self.record_schema), [])
        defs = self.decl_schema["$defs"]
        self.assertEqual(defs["standardIdentifier"]["properties"]["id"]["const"], "GCL-TCS-00")
        self.assertEqual(defs["standardIdentifier"]["properties"]["version"]["const"], "0.1.0")
        self.assertEqual(defs["profile"]["properties"]["version"]["const"], "0.1.0")

    def test_wrong_standard_version_is_rejected(self) -> None:
        broken = copy.deepcopy(self.decl_template)
        broken["standard"]["version"] = "latest"
        errors = list(Draft202012Validator(self.decl_schema).iter_errors(broken))
        self.assertTrue(errors)

    def test_record_schema_defines_all_normative_record_bodies(self) -> None:
        self.assertTrue({"claimRecord","evidenceRecord","reviewRecord","exceptionRecord","gateRecord","conformanceStatement","releaseRecord"}.issubset(self.record_schema["$defs"]))

    def test_exception_record_requires_review_or_expiry(self) -> None:
        instance = copy.deepcopy(self.record_template["exception_record"])
        instance.pop("expiry_date", None)
        instance.pop("review_date", None)
        errors = list(Draft202012Validator(self.record_schema["$defs"]["exceptionRecord"]).iter_errors(instance))
        self.assertTrue(errors)

    def test_not_applicable_gate_requires_reason(self) -> None:
        instance = copy.deepcopy(self.record_template["gate_record"])
        instance["decision"] = "NOT_APPLICABLE"
        instance.pop("not_applicable_reason", None)
        errors = list(Draft202012Validator(self.record_schema["$defs"]["gateRecord"]).iter_errors(instance))
        self.assertTrue(errors)

    def test_machine_templates_validate(self) -> None:
        self.assertEqual(template_contract_errors(self.decl_schema, self.record_schema, self.decl_template, self.record_template), [])

    def test_record_template_cannot_claim_promoted_authority(self) -> None:
        broken = copy.deepcopy(self.record_template)
        broken["template_contract"]["authority"] = "promoted"
        errors = template_contract_errors(self.decl_schema, self.record_schema, self.decl_template, broken)
        self.assertIn("record_template: authority_boundary_missing", errors)

    def test_historical_issued_manifest_is_not_rewritten(self) -> None:
        self.assertEqual(historical_manifest_errors(self.historical), [])

    def test_historical_policy_hash_rewrite_is_detected(self) -> None:
        broken = copy.deepcopy(self.historical)
        tcs = next(x for x in broken["artifacts"] if x["artifact_id"] == "GCL-TCS-00")
        tcs["machine_policy"]["sha256"] = "0" * 64
        self.assertIn("historical_manifest: issued_policy_hash_rewritten", historical_manifest_errors(broken))

    def test_policy_preserves_no_v1_promotion_boundary(self) -> None:
        self.assertEqual(self.policy["standard"]["version"], "0.1.0")
        self.assertEqual(self.policy["standard"]["status"], "candidate")
        self.assertEqual(self.matrix["authority_boundary"], "DERIVATIVE_RECONCILIATION_ONLY__NO_V1_PROMOTION")


if __name__ == "__main__":
    unittest.main()
