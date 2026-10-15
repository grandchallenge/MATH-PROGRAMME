#!/usr/bin/env python3
"""Immutable source checks and finite falsifiers. No open conjecture proof."""
import hashlib
import itertools
import json
import unittest
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[2]
LEDGER=ROOT/"governance/source_erdos_critical_005/CRITICAL_SOURCE_CORRECTIONS_005.json"
SNAP=ROOT/"governance/source_erdos_critical_005/SOURCE_SNAPSHOTS.json"
IDS={11:2520,12:2521,14:2522,15:2523,41:2536}
OLD={11:"f0d8fa230850d0e0b7b8e7fa037e6f9ef47c0440",
     12:"29ce2d40361aba4e4a498f314f5dd60c62ded7d7",
     14:"0993d4a8e8f6eddd3ca7818bdc1c9c942cda2797",
     15:"20e1006e8c22aa73a3516592a6a7ff32f5a577a6",
     41:"5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50"}

def weak_p(a):
    return all(not(x<b and x<c and b!=c and (b+c)%x==0)
               for x in a for b in a for c in a)
def strict_p(a):
    return all(not(x<b and x<c and (b+c)%x==0)
               for x in a for b in a for c in a)
def weak_b3(a):
    sums=[sum(t) for t in itertools.combinations(a,3)]
    return len(sums)==len(set(sums))
def strong_b3(a):
    sums=[sum(t) for t in itertools.combinations_with_replacement(a,3)]
    return len(sums)==len(set(sums))
def r(a,n):
    return sum(x+y==n for x,y in itertools.combinations_with_replacement(a,2))
def c(a,n):
    return sum(x+y==n for x in a for y in a)
def diag(a,n):
    return int(n%2==0 and n//2 in a)

class FiveSourceFidelityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger=json.loads(LEDGER.read_text())
        cls.snaps=json.loads(SNAP.read_text())
        cls.rows={i["problem_id"]:i for i in cls.ledger["source_corrections"]}
        cls.sources={i["problem_id"]:(i,(ROOT/i["source_snapshot"]).read_bytes())
                     for i in cls.snaps["items"]}

    def test_exact_five_bindings(self):
        self.assertEqual(set(self.rows),set(IDS))
        self.assertEqual({n:v["review_issue"] for n,v in self.rows.items()},IDS)
        self.assertEqual(set(self.sources),set(IDS))
        for n,row in self.rows.items():
            self.assertEqual(row["catalogue_issue"],1269+n)

    def test_original_source_locks_preserved_and_git_blob_fidelity(self):
        self.assertIs(self.ledger["original_protected_source_locks_mutated"],False)
        for n,(p,src) in self.sources.items():
            blob=hashlib.sha1(f"blob {len(src)}\0".encode()+src).hexdigest()
            self.assertEqual(blob,p["refreshed_blob_sha1"])
            self.assertEqual(hashlib.sha256(src).hexdigest(),p["refreshed_file_sha256"])
            self.assertEqual(p["original_blob_sha1"],OLD[n])
            self.assertEqual(self.rows[n]["frozen_blob"],OLD[n])
            self.assertEqual(self.rows[n]["refreshed_blob"],blob)
            self.assertIn(b"Copyright",src)

    def test_no_solve_certification_or_revision_clearance(self):
        effects=self.ledger["governance_effects"]
        self.assertEqual(effects["proposed_correction_count"],5)
        self.assertEqual(effects["source_statement_fix_verified"],3)
        self.assertEqual(effects["partial_or_external_exception_count"],2)
        for key in ("old_source_mutation","mathematical_certification","solve_dispatch",
                    "research_claim_acceptance","clear_revision_labels","change_issue_fields"):
            self.assertIs(effects[key],False,key)
        self.assertTrue(all(x["claimable"] is False for x in self.rows.values()))

    def test_11_eventual_distinct_from_all_odd_and_polarity(self):
        s=self.sources[11][1].decode()
        for frag in ("∀ᶠ n : ℕ in atTop, Odd n",
                     "theorem erdos_11.variants.all_odd",
                     "theorem eventually_of_all_odd","¬ 2 ^ p ≡ 2 [MOD p ^ 2]"):
            self.assertIn(frag,s)
        self.assertNotEqual(pow(2,3,9),2%9)
        self.assertEqual(pow(2,1093,1093**2),2)

    def test_12_partial_repair_and_explicit_uncertainty(self):
        s=self.sources[12][1].decode()
        self.assertIn("a < c → b = c",s)
        self.assertIn("theorem erdos_12.variants.schoen",s)
        self.assertIn("theorem erdos_12.variants.baier",s)
        self.assertIn("∃ C >",s)
        self.assertIn("PREDICATE_ADJUDICATION_REQUIRED",self.rows[12]["source_fidelity_status"])

    def test_12_repetition_is_real_predicate_difference(self):
        self.assertTrue(weak_p((3,6)))
        self.assertFalse(strict_p((3,6)))
        for mask in range(1<<7):
            a=tuple(i for i in range(1,8) if mask&(1<<(i-1)))
            if strict_p(a):
                self.assertTrue(weak_p(a))
    def test_14_verified_external_claim_not_local_certification(self):
        s=self.sources[14][1].decode()
        for frag in ("nonUniqueSumCount","allUniqueSums A","almostSquareRoot","IsLittleO"):
            self.assertIn(frag,s)
        row=self.rows[14]
        self.assertEqual(row["research_status"],"EXTERNAL_CLAIM_REVIEW_PENDING")
        self.assertEqual({x["part"] for x in row["external_results"]},{"i","ii"})
        self.assertEqual({x["credited_solver"] for x in row["external_results"]},{"JenW1N"})
        self.assertTrue(all(len(x["task_bundle_sha256"])==64 for x in row["external_results"]))
        self.assertEqual({x["downloaded_source_sha256"] for x in row["external_results"]},
                         {"496840684dd5dc4f0747bf4732ee4fe246340353f8a11aae00bde325fa100ca5",
                          "188ebf8bdf3a04694155ddf3e2d87c64f53d545781cfda7b63e21d6b1434cd74"})
        self.assertTrue(all(x["published_proof_sha256"]==x["downloaded_source_sha256"]
                            and x["kernel_replayed_by_gcl"] is False
                            for x in row["external_results"]))

    def test_14_pair_symmetry_diagonal_and_zero(self):
        for mask in range(1<<7):
            a=tuple(i for i in range(7) if mask&(1<<i))
            for n in range(15):
                self.assertEqual(2*r(a,n),c(a,n)+diag(a,n))
                self.assertEqual(r(a,n)==1,c(a,n)+diag(a,n)==2)
        self.assertEqual(sum(r((0,1),n)!=1 for n in (1,2)),0)
        self.assertEqual(sum(r((1,),n)!=1 for n in (1,2)),1)

    def test_15_correct_ordered_real_limit_not_rational_summable(self):
        s=self.sources[15][1].decode()
        for frag in ("∃ l : ℝ, Tendsto","Finset.range N","atTop (𝓝 l)"):
            self.assertIn(frag,s)
        self.assertNotIn("theorem erdos_15 : Summable",s)
        self.assertEqual(Fraction(-1,2)+Fraction(2,3),Fraction(1,6))
        self.assertIn("CORRECTED_PROVIDER_PINNED",self.rows[15]["source_fidelity_status"])

    def test_41_fresh_multiset_repeated_summands(self):
        s=self.sources[41][1].decode()
        for frag in ("∀ I J : Multiset α","I.card = n","I.sum = J.sum","I = J"):
            self.assertIn(frag,s)
        self.assertNotIn("∀ (I : Finset α)",s)
        self.assertIn("HISTORICAL_AUDIT_PENDING",self.rows[41]["source_fidelity_status"])

    def test_41_weak_finset_not_strong_multiset(self):
        self.assertTrue(weak_b3((1,2,3)))
        self.assertFalse(strong_b3((1,2,3)))
        self.assertEqual(sum((1,1,3)),sum((1,2,2)))
        for mask in range(1<<7):
            a=tuple(i for i in range(1,8) if mask&(1<<(i-1)))
            if strong_b3(a):
                self.assertTrue(weak_b3(a))

    def test_all_five_revision_flags_retained(self):
        self.assertIn("Leave all five gcl-review:revise",self.ledger["correction_issue_states"])
        self.assertIn("RETURNED",self.ledger["correction_issue_states"])

    def test_12_1970_primary_example_disambiguates_later_stronger_usage(self):
        import importlib.util
        path=ROOT/"governance/source_erdos_critical_005/property_p_1970_primary_regression.py"
        spec=importlib.util.spec_from_file_location("erdos12_1970_primary",path)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        output=mod.audit()
        self.assertEqual(output["checked_m"],200)
        self.assertTrue(output["all_weak"])
        self.assertIs(output["all_strong"],False)
        self.assertFalse(output["historical_statement_solved"])
        info=json.loads((ROOT/"governance/source_erdos_critical_005/PRIMARY_1970_PROPERTY_P_ADJUDICATION.json").read_text())
        self.assertTrue(info["original_1970_source_semantics_adjudicated"])
        self.assertEqual(info["review_issue"],2521)
        self.assertEqual(info["primary_pdf_sha256"],
                         "4adba03f04de19ebb6ac9bddc6eaf43567619ca96c6cbe574e4c04be3595d0f3")
        self.assertFalse(info["external_formal_i_ii_kernel_replayed"])
        self.assertFalse(info["gcl_review_label_clearance_authorized"])

    def test_14_immutable_historical_task_parity_and_remaining_kernel_gate(self):
        path=ROOT/"governance/source_erdos_critical_005/ERDOS_014_EXTERNAL_TASK_PARITY.json"
        obj=json.loads(path.read_text())
        self.assertEqual(obj["result"],"PASS_HASHED_TASK_FILES_AND_PUBLISHED_REPORT_PARITY")
        self.assertEqual(len(obj["provenance"]),2)
        self.assertEqual({e["part"] for e in obj["provenance"]},{"i","ii"})
        self.assertTrue(all(e["trusted_files_byte_verified"]==5 for e in obj["provenance"]))
        self.assertTrue(all(e["historical_task_component_bytes_verified"] for e in obj["provenance"]))
        self.assertTrue(all(e["original_formal_provider_git_checkout_parity"] is False for e in obj["provenance"]))
        self.assertTrue(all(e["independent_gcl_kernel_replay"] is False for e in obj["provenance"]))
        self.assertFalse(obj["claim_effects"]["gcl_math_certification"])

    def test_41_historical_and_modern_B3_are_not_equivalent(self):
        import importlib.util
        f=ROOT/"governance/source_erdos_critical_005/erdos41_conventions.py"
        spec=importlib.util.spec_from_file_location("erdos41_conventions",f)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.validate(),793)
        self.assertTrue(module.historical((1,2,4)))
        self.assertFalse(module.new_multiset((1,2,4)))
        self.assertFalse(module.historical((1,4,5)))
        self.assertTrue(module.new_multiset((1,4,5)))
        self.assertTrue(module.old_finset((1,2,3)))
        self.assertFalse(module.new_multiset((1,2,3)))
        receipt=json.loads((ROOT/"governance/source_erdos_critical_005/ERDOS_041_014_SOURCE_BOUNDARY.json").read_text())
        self.assertFalse(receipt["erdos_41"]["source_correction_complete"])
        self.assertFalse(receipt["erdos_41"]["revision_label_clearance"])
        self.assertFalse(receipt["erdos_14"]["separate_gcl_kernel_replay"])
        self.assertFalse(receipt["mathematical_certification"])

    def test_41_infinite_historical_and_modern_incomparability_witnesses(self):
        import importlib.util
        f=ROOT/"governance/source_erdos_critical_005/erdos41_infinite_models.py"
        spec=importlib.util.spec_from_file_location("erdos41_infinite_models",f)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        proof=module.run()
        self.assertEqual(proof["family_check_tail_sizes"],list(range(8)))
        self.assertIs(proof["original_problem_41_settled"],False)
        self.assertIn("SUPERINCREASING",proof["proven_for_all_finite_subsets"])
        doc=ROOT/"governance/source_erdos_critical_005/ERDOS_041_INFINITE_SEMANTIC_SEPARATION.md"
        self.assertIn("logically incomparable even among infinite",doc.read_text())

    def test_exact_admitted_active_research_source_locks(self):
        import importlib.util
        p=ROOT/'governance/source_erdos_critical_005/active_source_lock.py'
        spec=importlib.util.spec_from_file_location('admitted_erdos_sources',p)
        m=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        registry=json.loads(m.LEDGER.read_text())
        roster=json.loads(m.ROSTER.read_text())
        rows=m.verify(registry,roster)
        self.assertEqual([x['problem_id'] for x in rows],[11,12,15])
        self.assertEqual(m.get(11)['review_issue'],2520)
        self.assertEqual(m.get(12)['review_issue'],2521)
        self.assertEqual(m.get(15)['review_issue'],2523)
        self.assertIsNone(m.get(14))
        self.assertIsNone(m.get(41))
        with self.assertRaises(m.SourceLockError):m.get(11,purpose='solve')
        with self.assertRaises(m.SourceLockError):m.get(15,purpose='certification')
        bad=json.loads(json.dumps(registry))
        bad['active_sources'][0]['source_sha256']='f'*64
        with self.assertRaises(m.SourceLockError):m.verify(bad,roster)
        bad=json.loads(json.dumps(registry))
        bad['active_sources'][2]['review_issue']=2522
        with self.assertRaises(m.SourceLockError):m.verify(bad,roster)
        bad=json.loads(json.dumps(registry))
        bad['authority_effects']['solve_dispatch']=True
        with self.assertRaises(m.SourceLockError):m.verify(bad,roster)
        bad=json.loads(json.dumps(registry))
        bad['excluded_until_replay'].pop('14')
        with self.assertRaises(m.SourceLockError):m.verify(bad,roster)

if __name__=="__main__":
    unittest.main(verbosity=2)
