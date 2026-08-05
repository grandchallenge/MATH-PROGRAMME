from __future__ import annotations

import copy
import json
import unittest

from euclid_gcd_closeout import PAGE, RECORD, SCHEMA, semantic_errors, validate


class EuclidGCDCloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.page = PAGE.read_text(encoding="utf-8")

    def errors_for(self, mutate_record=None, mutate_page=None) -> list[str]:
        data = copy.deepcopy(self.record)
        page = self.page
        if mutate_record:
            mutate_record(data)
        if mutate_page:
            page = mutate_page(page)
        return semantic_errors(data, page)

    def test_baseline(self) -> None:
        self.assertEqual(validate(), [])

    def test_forge_merge_substitution_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["forge"].update(merge_commit="0" * 40)))

    def test_solve_candidate_blob_substitution_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["solve"]["artifacts"]["candidate"].update(git_blob_sha1="0" * 40)))

    def test_cert_output_blob_substitution_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["cert"]["artifacts"]["certification_output"].update(git_blob_sha1="0" * 40)))

    def test_review_inflation_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["cert"]["independent_review"].update(state="COMMENTED")))

    def test_merge_parent_drift_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["solve"].update(merge_parents=list(reversed(d["solve"]["merge_parents"])))))

    def test_changed_quotient_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["canonical_instance"]["trace"][0].update(quotient=3)))

    def test_changed_remainder_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["canonical_instance"]["trace"][1].update(remainder=20)))

    def test_changed_bezout_coefficient_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["canonical_instance"]["bezout"].update(x=-1)))

    def test_zero_zero_widening_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["boundaries"].update(zero_zero_input_admitted=True)))

    def test_novelty_inflation_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["boundaries"].update(novelty=True)))

    def test_universal_correctness_inflation_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["boundaries"].update(universal_extended_euclid_program_correctness=True)))

    def test_historical_verbatim_inflation_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["boundaries"].update(historical_verbatim_equivalence=True)))

    def test_linear_diophantine_activation_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["boundaries"].update(linear_diophantine_stage_activated=True)))

    def test_book_vii_activation_rejected(self) -> None:
        self.assertTrue(self.errors_for(lambda d: d["boundaries"].update(book_vii_microcampaign_activated=True)))

    def test_page_equation_drift_rejected(self) -> None:
        self.assertTrue(self.errors_for(mutate_page=lambda p: p.replace("252 = 2 * 105 + 42", "252 = 2 * 105 + 41")))

    def test_page_authority_chain_omission_rejected(self) -> None:
        self.assertTrue(self.errors_for(mutate_page=lambda p: p.replace(self.record["cert"]["merge_commit"], "redacted")))

    def test_schema_is_closed(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertIs(schema["additionalProperties"], False)


if __name__ == "__main__":
    unittest.main()
