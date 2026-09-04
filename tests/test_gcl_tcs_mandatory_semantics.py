from __future__ import annotations

import copy
import unittest
from pathlib import Path

from ci.gcl_tcs_mandatory_semantics import (
    CONTRACT_MANIFEST,
    COVERAGE,
    EXCEPTION_TEST,
    MATRIX_ROWS,
    coverage_contract_errors,
    declaration_semantic_errors,
    gate_review_semantic_errors,
    gate_satisfies_gate,
    schema_required_field_sets,
    validation_errors,
)
from ci.gcl_tcs_normative_agreement import (
    DECL_SCHEMA,
    POLICY,
    RECORD_SCHEMA,
    RECORD_TEMPLATE,
    _load_json,
    _load_yaml,
    load_matrix,
)


class GclTcsMandatorySemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = load_matrix()
        cls.policy = _load_yaml(POLICY)
        cls.coverage = _load_json(COVERAGE)
        cls.decl_schema = _load_json(DECL_SCHEMA)
        cls.record_schema = _load_json(RECORD_SCHEMA)
        cls.decl_template = _load_yaml(
            Path("docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.conformance.template.yaml")
        )
        cls.record_template = _load_yaml(RECORD_TEMPLATE)
        cls.contract_manifest = _load_json(CONTRACT_MANIFEST)

    def assertInvalid(self, instance: object, schema: dict) -> None:
        self.assertTrue(validation_errors(instance, schema))

    def assertValid(self, instance: object, schema: dict) -> None:
        self.assertEqual(validation_errors(instance, schema), [])

    def required_targets(self) -> dict[str, tuple[dict, dict]]:
        defs = self.decl_schema["$defs"]
        props = self.decl_schema["properties"]
        record_defs = self.record_schema["$defs"]
        targets: dict[str, tuple[dict, dict]] = {
            "declaration": (copy.deepcopy(self.decl_template), self.decl_schema),
            "declaration.standard": (copy.deepcopy(self.decl_template["standard"]), defs["standardIdentifier"]),
            "declaration.primary_profile": (copy.deepcopy(self.decl_template["primary_profile"]), defs["profile"]),
            "declaration.dependency": (
                {
                    "artifact_id": "DEP-001",
                    "version_or_revision": "abc123",
                    "authority_status": "authoritative",
                    "relation": "source",
                },
                defs["dependency"],
            ),
            "declaration.location_or_not_applicable": (
                {"status": "not_applicable", "reason": "No terminology registry applies."},
                defs["locationOrNotApplicable"],
            ),
            "declaration.location_or_explicit_empty": (
                {"status": "explicit_empty", "reason": "No consequential claims."},
                defs["locationOrExplicitEmpty"],
            ),
            "declaration.review_reference": (
                {
                    "review_id": "REV-001",
                    "gate_id": "G5",
                    "location": "reviews/REV-001.yaml",
                    "decision": "PASS",
                    "reviewed_revision": "abc123",
                },
                defs["reviewReference"],
            ),
            "declaration.exception_reference": (
                {
                    "exception_id": "EXC-001",
                    "location": "exceptions/EXC-001.yaml",
                    "status": "approved",
                },
                defs["exceptionReference"],
            ),
            "declaration.conformance_dimensions": (
                copy.deepcopy(self.decl_template["conformance_dimensions"]),
                props["conformance_dimensions"],
            ),
            "declaration.licence_and_access": (
                copy.deepcopy(self.decl_template["licence_and_access"]),
                props["licence_and_access"],
            ),
            "declaration.generated_content": (
                copy.deepcopy(self.decl_template["generated_content"]),
                props["generated_content"],
            ),
        }
        record_mapping = {
            "record.claimRecord": ("claim_record", "claimRecord"),
            "record.evidenceRecord": ("evidence_record", "evidenceRecord"),
            "record.reviewRecord": ("review_record", "reviewRecord"),
            "record.exceptionRecord": ("exception_record", "exceptionRecord"),
            "record.gateRecord": ("gate_record", "gateRecord"),
            "record.conformanceStatement": ("conformance_statement", "conformanceStatement"),
            "record.releaseRecord": ("release_record", "releaseRecord"),
        }
        for name, (template_key, schema_key) in record_mapping.items():
            targets[name] = (copy.deepcopy(self.record_template[template_key]), record_defs[schema_key])
        return targets

    def test_coverage_contract_is_exact_and_governed(self) -> None:
        self.assertEqual(
            coverage_contract_errors(
                coverage=self.coverage,
                matrix=self.matrix,
                declaration_schema=self.decl_schema,
                record_schema=self.record_schema,
                policy=self.policy,
                contract_manifest=self.contract_manifest,
            ),
            [],
        )
        self.assertEqual(
            self.coverage["required_field_sets"],
            schema_required_field_sets(self.decl_schema, self.record_schema),
        )

    def test_every_required_field_rejects_omission(self) -> None:
        targets = self.required_targets()
        self.assertEqual(set(targets), set(self.coverage["required_field_sets"]))
        for target_name, required_fields in self.coverage["required_field_sets"].items():
            baseline, schema = targets[target_name]
            self.assertValid(baseline, schema)
            for field in required_fields:
                with self.subTest(target=target_name, field=field):
                    broken = copy.deepcopy(baseline)
                    broken.pop(field, None)
                    self.assertInvalid(broken, schema)

    def test_matrix_bound_field_semantics_reject_invalid_values(self) -> None:
        cases: list[tuple[str, dict, dict]] = []

        def declaration_case(name: str, mutate) -> None:
            broken = copy.deepcopy(self.decl_template)
            mutate(broken)
            cases.append((name, broken, self.decl_schema))

        declaration_case("schema_version_const", lambda x: x.__setitem__("schema_version", "latest"))
        declaration_case("standard_id_const", lambda x: x["standard"].__setitem__("id", "GCL-TCS-99"))
        declaration_case("standard_version_const", lambda x: x["standard"].__setitem__("version", "latest"))
        declaration_case("profile_id_enum", lambda x: x["primary_profile"].__setitem__("id", "GCL-TCS-P99"))
        declaration_case("profile_version_const", lambda x: x["primary_profile"].__setitem__("version", "latest"))
        declaration_case("authority_status_enum", lambda x: x.__setitem__("authority_status", "displayed"))
        declaration_case("promotion_status_enum", lambda x: x.__setitem__("promotion_status", "approved"))
        declaration_case("impact_class_enum", lambda x: x.__setitem__("impact_class", "IC-4"))
        declaration_case("assessment_state_enum", lambda x: x["conformance_dimensions"].__setitem__("V", "COMPLETE"))
        declaration_case("date_format", lambda x: x.__setitem__("date", "2026-99-99"))
        declaration_case("artifact_id_pattern", lambda x: x.__setitem__("artifact_id", "bad id with spaces"))
        declaration_case("audience_min_items", lambda x: x.__setitem__("audience", []))
        declaration_case(
            "secondary_profiles_unique",
            lambda x: x.__setitem__("secondary_profiles", [copy.deepcopy(x["primary_profile"]), copy.deepcopy(x["primary_profile"])]),
        )
        declaration_case("additional_properties_closed", lambda x: x.__setitem__("display_authority", "promoted"))
        declaration_case(
            "not_applicable_requires_reason",
            lambda x: x.__setitem__("terminology_registry", {"status": "not_applicable"}),
        )
        declaration_case(
            "explicit_empty_requires_reason",
            lambda x: x.__setitem__("claim_register", {"status": "explicit_empty"}),
        )

        defs = self.decl_schema["$defs"]
        cases.extend(
            [
                (
                    "dependency_authority_enum",
                    {"artifact_id": "DEP-1", "version_or_revision": "abc", "authority_status": "working", "relation": "source"},
                    defs["dependency"],
                ),
                (
                    "review_reference_gate_pattern",
                    {"review_id": "R", "gate_id": "G10", "location": "r", "decision": "PASS", "reviewed_revision": "abc"},
                    defs["reviewReference"],
                ),
                (
                    "exception_reference_status_enum",
                    {"exception_id": "E", "location": "e", "status": "live"},
                    defs["exceptionReference"],
                ),
            ]
        )

        record_defs = self.record_schema["$defs"]
        record_mutations = [
            ("claim_type_enum", "claim_record", "claimRecord", lambda x: x.__setitem__("claim_type", "fact")),
            ("claim_status_enum", "claim_record", "claimRecord", lambda x: x.__setitem__("claim_status", "accepted")),
            ("claim_review_date_format", "claim_record", "claimRecord", lambda x: x.__setitem__("last_reviewed", "yesterday")),
            ("evidence_datetime_format", "evidence_record", "evidenceRecord", lambda x: x.__setitem__("created_at", "2026-09-03")),
            ("review_gate_pattern", "review_record", "reviewRecord", lambda x: x.__setitem__("gate_id", "gate-five")),
            ("review_decision_enum", "review_record", "reviewRecord", lambda x: x.__setitem__("decision", "APPROVED")),
            ("review_date_format", "review_record", "reviewRecord", lambda x: x.__setitem__("date", "03-09-2026")),
            ("exception_status_enum", "exception_record", "exceptionRecord", lambda x: x.__setitem__("status", "active")),
            ("exception_date_format", "exception_record", "exceptionRecord", lambda x: x.__setitem__("issued_date", "today")),
            ("exception_controls_min_items", "exception_record", "exceptionRecord", lambda x: x.__setitem__("compensating_controls", [])),
            ("gate_id_pattern", "gate_record", "gateRecord", lambda x: x.__setitem__("gate_id", "G99")),
            ("gate_decision_enum", "gate_record", "gateRecord", lambda x: x.__setitem__("decision", "APPROVED")),
            ("conformance_impact_enum", "conformance_statement", "conformanceStatement", lambda x: x.__setitem__("impact_class", "IC-9")),
            ("conformance_target_enum", "conformance_statement", "conformanceStatement", lambda x: x.__setitem__("target_state", "COMPLETE")),
            ("conformance_standard_versions_min_items", "conformance_statement", "conformanceStatement", lambda x: x.__setitem__("standard_versions", [])),
            ("release_nonempty_identifier", "release_record", "releaseRecord", lambda x: x.__setitem__("new_standard_identifier", "")),
        ]
        for name, template_key, schema_key, mutate in record_mutations:
            broken = copy.deepcopy(self.record_template[template_key])
            mutate(broken)
            cases.append((name, broken, record_defs[schema_key]))

        for name, instance, schema in cases:
            with self.subTest(case=name):
                self.assertInvalid(instance, schema)

    def test_claim_requires_exactly_one_statement_or_pointer(self) -> None:
        schema = self.record_schema["$defs"]["claimRecord"]
        baseline = copy.deepcopy(self.record_template["claim_record"])
        self.assertValid(baseline, schema)

        missing = copy.deepcopy(baseline)
        missing.pop("statement", None)
        self.assertInvalid(missing, schema)

        both = copy.deepcopy(baseline)
        both["statement_ref"] = "claims/CLAIM-EXAMPLE-001.md"
        self.assertInvalid(both, schema)

        pointer_only = copy.deepcopy(baseline)
        pointer_only.pop("statement", None)
        pointer_only["statement_ref"] = "claims/CLAIM-EXAMPLE-001.md"
        self.assertValid(pointer_only, schema)

    def test_assured_requires_linked_exact_revision_review(self) -> None:
        declaration = copy.deepcopy(self.decl_template)
        declaration["conformance_dimensions"]["V"] = "ASSURED"
        self.assertIn("declaration: ASSURED_requires_linked_review", declaration_semantic_errors(declaration))

        declaration["review_register"] = [
            {
                "review_id": "REV-ASSURED-001",
                "gate_id": "G5",
                "location": "reviews/REV-ASSURED-001.yaml",
                "decision": "PASS",
                "reviewed_revision": "wrong-revision",
            }
        ]
        self.assertIn("declaration: ASSURED_review_revision_mismatch", declaration_semantic_errors(declaration))

        declaration["review_register"][0]["reviewed_revision"] = declaration["source_revision"]
        self.assertEqual(declaration_semantic_errors(declaration), [])
        self.assertValid(declaration, self.decl_schema)

    def test_gate_review_semantics_fail_closed(self) -> None:
        gate = copy.deepcopy(self.record_template["gate_record"])
        review = copy.deepcopy(self.record_template["review_record"])
        self.assertEqual(gate_review_semantic_errors(gate, review), [])
        self.assertFalse(gate_satisfies_gate(gate, review))

        gate["decision"] = "NOT_APPLICABLE"
        gate["not_applicable_reason"] = "Not applicable for this exact artifact."
        self.assertIn(
            "gate_review: NOT_APPLICABLE_requires_reviewer_approval",
            gate_review_semantic_errors(gate, review),
        )

        review["decision"] = "NOT_APPLICABLE"
        self.assertEqual(gate_review_semantic_errors(gate, review), [])
        self.assertTrue(gate_satisfies_gate(gate, review))

        review["reviewed_revision"] = "different-revision"
        self.assertIn("gate_review: reviewed_revision_mismatch", gate_review_semantic_errors(gate, review))
        self.assertFalse(gate_satisfies_gate(gate, review))

        review["reviewed_revision"] = gate["reviewed_revision"]
        review["gate_id"] = "G3"
        self.assertIn("gate_review: gate_id_mismatch", gate_review_semantic_errors(gate, review))

    def test_dedicated_exception_semantics_are_reused_and_governed(self) -> None:
        paths = {item["path"] for item in self.contract_manifest["tests"]}
        self.assertIn(EXCEPTION_TEST, paths)
        reused = self.coverage["reused_dedicated_controls"]
        self.assertTrue(any(item["test"] == EXCEPTION_TEST for item in reused))

    def test_machine_completeness_does_not_absorb_review_only_rows(self) -> None:
        by_id = {row["id"]: row for row in self.matrix["rows"]}
        for row_id in MATRIX_ROWS:
            with self.subTest(row=row_id):
                self.assertNotEqual(by_id[row_id]["machine_checkability"], "review")


if __name__ == "__main__":
    unittest.main()
