from __future__ import annotations
import copy, json, unittest
from euclid_diophantine_closeout import PAGE, RECORD, SCHEMA, semantic_errors, validate

class EuclidDiophantineCloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record=json.loads(RECORD.read_text(encoding="utf-8")); cls.page=PAGE.read_text(encoding="utf-8")
    def errors_for(self,mutate_record=None,mutate_page=None):
        d=copy.deepcopy(self.record); p=self.page
        if mutate_record: mutate_record(d)
        if mutate_page: p=mutate_page(p)
        return semantic_errors(d,p)
    def test_baseline(self): self.assertEqual(validate(),[])
    def test_stage1_output_substitution_rejected(self): self.assertTrue(self.errors_for(lambda d:d["protected_stage1"]["certification_output"].update(git_blob_sha1="0"*40)))
    def test_competing_gcd_boundary_rejected(self): self.assertTrue(self.errors_for(lambda d:d["protected_stage1"].update(reuse_only_no_competing_gcd_definition=False)))
    def test_forge_merge_substitution_rejected(self): self.assertTrue(self.errors_for(lambda d:d["forge"].update(merge_commit="0"*40)))
    def test_solve_merge_parent_drift_rejected(self): self.assertTrue(self.errors_for(lambda d:d["solve"].update(merge_parents=list(reversed(d["solve"]["merge_parents"])))))
    def test_cert_merge_parent_drift_rejected(self): self.assertTrue(self.errors_for(lambda d:d["cert"].update(merge_parents=list(reversed(d["cert"]["merge_parents"])))))
    def test_candidate_blob_substitution_rejected(self): self.assertTrue(self.errors_for(lambda d:d["solve"]["artifacts"]["candidate"].update(git_blob_sha1="0"*40)))
    def test_cert_output_blob_substitution_rejected(self): self.assertTrue(self.errors_for(lambda d:d["cert"]["artifacts"]["certification_output"].update(git_blob_sha1="0"*40)))
    def test_review_inflation_rejected(self): self.assertTrue(self.errors_for(lambda d:d["cert"]["independent_review"].update(state="COMMENTED")))
    def test_false_scale_rejected(self): self.assertTrue(self.errors_for(lambda d:d["canonical_instances"]["positive"].update(scale=3)))
    def test_altered_witness_rejected(self): self.assertTrue(self.errors_for(lambda d:d["canonical_instances"]["positive"]["witness"].update(x=-7)))
    def test_wrong_positive_target_rejected(self): self.assertTrue(self.errors_for(lambda d:d["canonical_instances"]["positive"].update(c=85)))
    def test_zero_obstruction_remainder_rejected(self): self.assertTrue(self.errors_for(lambda d:d["canonical_instances"]["negative"]["division"].update(remainder=0)))
    def test_out_of_range_obstruction_rejected(self): self.assertTrue(self.errors_for(lambda d:d["canonical_instances"]["negative"]["division"].update(remainder=21)))
    def test_wrong_obstruction_quotient_rejected(self): self.assertTrue(self.errors_for(lambda d:d["canonical_instances"]["negative"]["division"].update(quotient=1)))
    def test_timeout_as_unsat_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(timeout_as_unsatisfiability=True)))
    def test_arbitrary_completeness_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(arbitrary_diophantine_completeness=True)))
    def test_historical_verbatim_inflation_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(historical_verbatim_equivalence=True)))
    def test_novelty_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(novelty=True)))
    def test_first_formalization_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(first_formalization=True)))
    def test_stage3_activation_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(stage3_activated=True)))
    def test_source_lock_inflation_rejected(self): self.assertTrue(self.errors_for(lambda d:d["boundaries"].update(book_vii_source_locked=True)))
    def test_page_witness_drift_rejected(self): self.assertTrue(self.errors_for(mutate_page=lambda p:p.replace("84 = -8 * 252 + 20 * 105","84 = -7 * 252 + 20 * 105")))
    def test_page_obstruction_omission_rejected(self): self.assertTrue(self.errors_for(mutate_page=lambda p:p.replace("0 < 20 < 21","omitted")))
    def test_page_authority_chain_omission_rejected(self): self.assertTrue(self.errors_for(mutate_page=lambda p:p.replace(self.record["cert"]["merge_commit"],"redacted")))
    def test_schema_is_closed(self): self.assertIs(json.loads(SCHEMA.read_text(encoding="utf-8"))["additionalProperties"],False)
if __name__=="__main__": unittest.main()
