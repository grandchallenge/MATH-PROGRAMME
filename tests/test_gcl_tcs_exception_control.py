from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "gcl_tcs_exception_control.py"
SPEC = importlib.util.spec_from_file_location("gcl_tcs_exception_control", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
control = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = control
SPEC.loader.exec_module(control)

AS_OF = date(2026, 9, 3)
AUTHORIZED = {"GCL-TCS-test-steward"}


def valid_exception() -> dict:
    return {
        "exception_id": "GCL-TCS-EX-TEST-001",
        "rule_id": "profile_language_sentence_length",
        "artifact_scope": "fixture://GCL-TCS-CANDIDATE-HARDENING-001",
        "affected_content": "synthetic test sentence",
        "justification": "Strict application would change the technical meaning in this fixture.",
        "risk_assessment": "The deviation is local and does not change claim or authority status.",
        "compensating_controls": [
            "Preserve the exact technical term and require explicit reviewer inspection."
        ],
        "requested_by": "GCL-TCS-test-owner",
        "approved_by": "GCL-TCS-test-steward",
        "issued_date": "2026-09-03",
        "review_date": "2026-10-03",
        "status": "approved",
    }


class GclTcsExceptionControlTests(unittest.TestCase):
    def assert_has(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in item for item in errors),
            msg=f"expected {fragment!r} in {errors!r}",
        )

    def test_valid_narrow_approved_exception_passes(self) -> None:
        self.assertEqual(
            control.validate_exception_record(
                valid_exception(),
                authorized_approvers=AUTHORIZED,
                as_of=AS_OF,
            ),
            [],
        )

    def test_missing_approval_authority_fails_closed(self) -> None:
        record = valid_exception()
        record.pop("approved_by")
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "approved_by: missing")
        self.assert_has(errors, "approved_by: missing_or_invalid")

    def test_unresolved_approval_authority_fails_closed(self) -> None:
        errors = control.validate_exception_record(
            valid_exception(),
            authorized_approvers=None,
            as_of=AS_OF,
        )
        self.assert_has(errors, "approved_by: approval_authority_unresolved")

    def test_unauthorized_approver_fails_closed(self) -> None:
        record = valid_exception()
        record["approved_by"] = "GCL-TCS-unmapped-reviewer"
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "approved_by: unauthorized")

    def test_approved_exception_requires_review_or_expiry(self) -> None:
        record = valid_exception()
        record.pop("review_date")
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "approved_requires_review_or_expiry")

    def test_non_waivable_requirement_cannot_be_excepted(self) -> None:
        record = valid_exception()
        record["rule_id"] = "truthful_nonmisleading_communication"
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "non_waivable_requirement")

    def test_empty_compensating_controls_fail_closed(self) -> None:
        record = valid_exception()
        record["compensating_controls"] = []
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "compensating_controls: missing_or_insufficient")

    def test_placeholder_compensating_control_fails_closed(self) -> None:
        record = valid_exception()
        record["compensating_controls"] = ["TBD"]
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "compensating_controls: missing_or_insufficient")

    def test_malformed_exception_record_fails_closed(self) -> None:
        self.assertEqual(
            control.validate_exception_record(
                ["not", "a", "record"],
                authorized_approvers=AUTHORIZED,
                as_of=AS_OF,
            ),
            ["record: malformed_non_mapping"],
        )

    def test_malformed_date_fails_closed(self) -> None:
        record = valid_exception()
        record["issued_date"] = "03-09-2026"
        errors = control.validate_exception_record(
            record,
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "issued_date: invalid_iso_date")

    def test_missing_required_exception_blocks_promotion(self) -> None:
        errors = control.evaluate_required_exceptions_for_promotion(
            required_exception_ids={"GCL-TCS-EX-MISSING"},
            exception_records={},
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "required_exception_missing")

    def test_revoked_required_exception_blocks_promotion(self) -> None:
        record = valid_exception()
        record["status"] = "revoked"
        errors = control.evaluate_required_exceptions_for_promotion(
            required_exception_ids={record["exception_id"]},
            exception_records={record["exception_id"]: record},
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "required_exception_revoked")

    def test_expired_required_exception_blocks_promotion(self) -> None:
        record = valid_exception()
        record["status"] = "expired"
        errors = control.evaluate_required_exceptions_for_promotion(
            required_exception_ids={record["exception_id"]},
            exception_records={record["exception_id"]: record},
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "required_exception_expired")

    def test_approved_exception_past_expiry_blocks_promotion(self) -> None:
        record = valid_exception()
        record.pop("review_date")
        record["expiry_date"] = "2026-09-02"
        errors = control.evaluate_required_exceptions_for_promotion(
            required_exception_ids={record["exception_id"]},
            exception_records={record["exception_id"]: record},
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "lifecycle: exception_expired")

    def test_required_exception_must_be_approved(self) -> None:
        record = valid_exception()
        record["status"] = "requested"
        record["approved_by"] = ""
        errors = control.evaluate_required_exceptions_for_promotion(
            required_exception_ids={record["exception_id"]},
            exception_records={record["exception_id"]: record},
            authorized_approvers=AUTHORIZED,
            as_of=AS_OF,
        )
        self.assert_has(errors, "required_exception_not_approved")

    def test_policy_non_waivable_contract_remains_live(self) -> None:
        policy = control._load_policy(ROOT)
        non_waivable = set(policy["exception_model"]["non_waivable"])
        self.assertIn("truthful_nonmisleading_communication", non_waivable)
        self.assertIn("exception_registration", non_waivable)
        self.assertIn("fail_closed_missing_record_behaviour", non_waivable)
        self.assertIn("no_fabricated_evidence_reviews_or_authority", non_waivable)

    def test_normative_required_fields_remain_bound(self) -> None:
        normative = (
            ROOT
            / "council_submissions/GCL-TCS-00/parts/04-exceptions-promotion-gates.md"
        ).read_text(encoding="utf-8")
        for field in control.REQUIRED_FIELDS + control.DATE_FIELDS:
            with self.subTest(field=field):
                self.assertIn(f"`{field}`", normative)


if __name__ == "__main__":
    unittest.main()
