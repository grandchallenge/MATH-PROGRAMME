import copy
import json
import pathlib
import sys
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
from administrative_protected_receipt_model import *
from administrative_protected_receipt_adapters import *
from administrative_protected_receipt_engine import *
from administrative_protected_receipt_replay import *
FIXTURE = ROOT / "tests" / "protected_receipt" / "fixtures" / "aug13_incident.json"



# --- test_state_model.py ---
class StateModelTests(unittest.TestCase):
    def occurrence(self,**kw):
        d=dict(procedure_id="p",scheduled_due_at="2026-01-01T00:00:00Z",protected_record_merge="a"*40,protected_record_digest="b"*64);d.update(kw);return OccurrenceIdentity(**d)
    def test_key_omits_digest(self): self.assertEqual(self.occurrence().idempotency_key,("p","2026-01-01T00:00:00Z","a"*40))
    def test_bad_sha_rejected(self): self.assertRaises(ValueError,self.occurrence,protected_record_merge="x")
    def test_bad_time_rejected(self): self.assertRaises(ValueError,self.occurrence,scheduled_due_at="2026-01-01")
    def test_head_mutation_stales_authority(self):
        s=ProductState(receipt=ReceiptState.REVIEWABLE,checks=CheckState.PASSING,review=ReviewState.PRESENT_FOR_HEAD,disposition=DispositionState.VALID_FOR_HEAD).after_head_mutation();self.assertEqual(s.checks,CheckState.STALE_FOR_HEAD);self.assertEqual(s.review,ReviewState.STALE_FOR_HEAD);self.assertEqual(s.disposition,DispositionState.STALE_FOR_HEAD)
    def test_safety_forbidden_direct_push(self): self.assertTrue(SafetyState(direct_protected_push=True).forbidden)
    def test_safety_forbidden_bypass(self): self.assertTrue(SafetyState(bypass_exercised=True).forbidden)
    def test_default_lane_qualification_only(self): self.assertEqual(ProductState().lane,LaneState.QUALIFICATION_ONLY)


# --- test_capabilities.py ---
class CapabilityTests(unittest.TestCase):
    def cs(self,role,login,token,caps=()): return CapabilitySet(role,ActorIdentity(login,1,token),frozenset(caps))
    def test_separated(self): self.assertFalse(validate_role_separation(self.cs(ActorRole.CANDIDATE,"c[bot]","c"),self.cs(ActorRole.REFEREE,"r[bot]","r"),self.cs(ActorRole.ADMINISTRATION,"a[bot]","a")))
    def test_self_referee_rejected(self): self.assertTrue(validate_role_separation(self.cs(ActorRole.CANDIDATE,"x","same"),self.cs(ActorRole.REFEREE,"x","same"),self.cs(ActorRole.ADMINISTRATION,"a","a")))
    def test_candidate_admin_cap_rejected(self): self.assertTrue(validate_role_separation(self.cs(ActorRole.CANDIDATE,"c","c",[Capability.WRITE_CONFIGURATION]),self.cs(ActorRole.REFEREE,"r","r"),self.cs(ActorRole.ADMINISTRATION,"a","a")))
    def test_require(self): self.assertRaises(PermissionError,self.cs(ActorRole.CANDIDATE,"c","c").require,Capability.WRITE_CANDIDATE)
    def test_no_steward_synthesis(self): self.assertRaises(PermissionError,assert_no_human_steward_synthesis,ActorRole.REFEREE)
    def test_missing_dependency_fails_before_effects(self): self.assertRaisesRegex(RuntimeError,"ENVIRONMENT_DEPENDENCY_FAILURE",require_runtime_modules,("definitely_missing_gcl_module_123",))


# --- test_config_adapter.py ---
class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.d=DesiredConfiguration(1,RulesetActor(9,"Integration","pull_request"));self.raw={"id":1,"name":"r","target":"branch","enforcement":"active","conditions":{},"rules":[],"bypass_actors":[{"actor_id":8,"actor_type":"Integration","bypass_mode":"pull_request"}]}
    def test_missing_actor_drifted(self): self.assertEqual(ConfigurationAdapter().observe(self.d,self.raw).state,ConfigState.DRIFTED)
    def test_exact_actor_converged(self):
        r=copy.deepcopy(self.raw);r["bypass_actors"].append(self.d.actor.as_dict());self.assertEqual(ConfigurationAdapter().observe(self.d,r).state,ConfigState.CONVERGED)
    def test_plan_add_exact(self): self.assertEqual(ConfigurationAdapter().plan(self.d,self.raw).operation,"ADD_EXACT_TARGET")
    def test_preserves_non_target(self):
        a=ConfigurationAdapter();p=a.plan(self.d,self.raw);r=copy.deepcopy(self.raw);r["bypass_actors"].append(self.d.actor.as_dict());self.assertTrue(a.verify_preservation(p,r,self.d))
    def test_non_target_mutation_detected(self):
        a=ConfigurationAdapter();p=a.plan(self.d,self.raw);r=copy.deepcopy(self.raw);r["bypass_actors"]=[self.d.actor.as_dict()];self.assertFalse(a.verify_preservation(p,r,self.d))


# --- test_github_adapter.py ---
class P:
    def __init__(self): self.pr={"base":{"ref":"main"},"head":{"sha":"h"},"mergeable":True,"mergeable_state":"blocked","required_checks":["c"]};self.anc={};self.runs=[];self.revs=[];self.comments=[]
    def pull_request(self,r,p):return copy.deepcopy(self.pr)
    def branch_sha(self,r,b):return "b1"
    def is_ancestor(self,r,a,d):return self.anc.get((a,d))
    def check_runs(self,r,h):return self.runs
    def reviews(self,r,p):return self.revs
    def issue_comments(self,r,i):return self.comments
    def update_branch(self,r,p,e):self.pr["head"]["sha"]="h2";return {"head_sha":"h2"}
class GitHubTests(unittest.TestCase):
    def setUp(self): self.p=P();self.a=GitHubStateAdapter(self.p)
    def test_blocked_raw_but_behind_typed(self):
        self.p.anc={("b0","h"):True,("b0","b1"):True,("b1","h"):False};f=self.a.classify_pr("r",1,"b0",update_control_permitted=True);self.assertEqual(f.branch_state,BranchState.BEHIND_CURRENT_BASE);self.assertEqual(f.raw_advisory["mergeable_state"],"blocked")
    def test_current(self): self.p.pr["head"]["sha"]="b1";self.assertEqual(self.a.classify_branch("r","b0","b1","b1"),BranchState.AT_CURRENT_BASE)
    def test_unknown_ancestry(self): self.assertEqual(self.a.classify_branch("r","b0","h","b1"),BranchState.UNKNOWN)
    def test_checks_missing(self): self.assertEqual(self.a.classify_checks("r","h",("c",)),CheckState.NOT_STARTED)
    def test_checks_passing(self): self.p.runs=[{"name":"c","head_sha":"h","status":"completed","conclusion":"success"}];self.assertEqual(self.a.classify_checks("r","h",("c",)),CheckState.PASSING)
    def test_checks_failing(self): self.p.runs=[{"name":"c","head_sha":"h","status":"completed","conclusion":"failure"}];self.assertEqual(self.a.classify_checks("r","h",("c",)),CheckState.FAILING)
    def test_exact_review_ignores_author_association(self): self.p.revs=[{"id":7,"commit_id":"h","user":{"login":"r"},"author_association":"CONTRIBUTOR"}];self.assertEqual(self.a.lookup_exact_review("r",1,7,"h","r").authority_state,AuthorityObjectState.VERIFIED)
    def test_duplicate_review_fails(self): self.p.revs=[{"id":7},{"id":7}];self.assertEqual(self.a.lookup_exact_review("r",1,7,"h","r").authority_state,AuthorityObjectState.DUPLICATED)
    def test_comment_marker_required(self): self.p.comments=[{"id":9,"user":{"login":"s"},"body":"APPROVED"}];self.assertEqual(self.a.lookup_exact_comment("r",1,9,"s",("APPROVED",)).authority_state,AuthorityObjectState.VERIFIED)
    def test_sync_expected_head(self): self.assertEqual(self.a.synchronize_candidate("r",1,"h","b1").state,UpdateBranchState.SUCCEEDED)


# --- test_ledger_adapter.py ---
class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.o=OccurrenceIdentity("p","2026-01-02T00:00:00Z","a"*40,"b"*64);self.pre={"procedures":{"p":{"completed_through_utc":"2026-01-01T00:00:00Z","receipt_count":1,"receipts":[{"procedure_id":"p","scheduled_due_at":"2026-01-01T00:00:00Z","merge_commit":"c"*40}]}}};self.b=ReceiptBinding(self.o,"record.json","d"*40,5,"OK");self.a=LedgerAdapter()
    def test_predecessor_exact(self): self.assertEqual(self.a.classify_predecessor(self.pre,self.o),LedgerState.PREDECESSOR_EXACT)
    def test_construct_one_delta(self): c=self.a.construct_candidate(self.pre,self.b);self.assertEqual(c["procedures"]["p"]["receipt_count"],2)
    def test_validate_exact(self): c=self.a.construct_candidate(self.pre,self.b);self.assertEqual(self.a.validate_candidate(self.pre,c,self.b).state,LedgerState.TARGET_PRESENT_EXACTLY_ONCE)
    def test_duplicate_rejected(self): c=self.a.construct_candidate(self.pre,self.b);c["procedures"]["p"]["receipts"].append(copy.deepcopy(c["procedures"]["p"]["receipts"][-1]));self.assertEqual(self.a.validate_candidate(self.pre,c,self.b).state,LedgerState.TARGET_DUPLICATED)
    def test_unrelated_mutation_rejected(self): c=self.a.construct_candidate(self.pre,self.b);c["x"]=1;self.assertEqual(self.a.validate_candidate(self.pre,c,self.b).state,LedgerState.UNRELATED_MUTATION)
    def test_idempotent_predecessor_classification(self): c=self.a.construct_candidate(self.pre,self.b);self.assertEqual(self.a.classify_predecessor(c,self.o),LedgerState.TARGET_PRESENT_EXACTLY_ONCE)


# --- test_mirror_adapter.py ---
class MirrorTests(unittest.TestCase):
    def a(self):return AuthoritativeFrontier("p","2026-08-10T01:21:00Z",3,"d","h")
    def test_ahead_conflicted(self):self.assertEqual(MirrorAdapter().classify(self.a(),DerivedFrontier("2026-08-16T01:21:00Z")).state,MirrorState.MIRROR_CONFLICTED)
    def test_behind_stale(self):self.assertEqual(MirrorAdapter().classify(self.a(),DerivedFrontier("2026-08-07T01:21:00Z")).state,MirrorState.MIRROR_STALE)
    def test_current(self):self.assertEqual(MirrorAdapter().classify(self.a(),DerivedFrontier("2026-08-10T01:21:00Z",3,"d")).state,MirrorState.MIRROR_CURRENT)
    def test_count_conflict(self):self.assertEqual(MirrorAdapter().classify(self.a(),DerivedFrontier("2026-08-10T01:21:00Z",4,"d")).state,MirrorState.MIRROR_CONFLICTED)
    def test_unavailable(self):self.assertEqual(MirrorAdapter().classify(self.a(),DerivedFrontier(None,available=False)).state,MirrorState.MIRROR_UNAVAILABLE)


# --- test_engine.py ---
class EngineTests(unittest.TestCase):
    def good(self):return ProductState(occurrence=OccurrenceState.IDENTIFIED,record=RecordState.PROTECTED,receipt=ReceiptState.REVIEWABLE,ledger=LedgerState.TARGET_PRESENT_EXACTLY_ONCE,branch=BranchState.AT_CURRENT_BASE,conflict=ConflictState.CONFLICT_FREE,checks=CheckState.PASSING,review=ReviewState.PRESENT_FOR_HEAD,disposition=DispositionState.VALID_FOR_HEAD,config=ConfigState.CONVERGED,authority_objects=AuthorityObjectState.VERIFIED)
    def test_good_eligible(self):self.assertTrue(ProtocolEngine().evaluate_merge_eligibility(self.good(),review_required=True,disposition_required=True).eligible)
    def test_behind_blocks(self):self.assertIn(MergeBlocker.FRESHNESS,ProtocolEngine().evaluate_merge_eligibility(self.good().with_updates(branch=BranchState.BEHIND_CURRENT_BASE),review_required=False,disposition_required=True).blockers)
    def test_checks_block(self):self.assertIn(MergeBlocker.CHECKS,ProtocolEngine().evaluate_merge_eligibility(self.good().with_updates(checks=CheckState.FAILING),review_required=False,disposition_required=True).blockers)
    def test_config_blocks(self):self.assertIn(MergeBlocker.CONFIGURATION,ProtocolEngine().evaluate_merge_eligibility(self.good().with_updates(config=ConfigState.DRIFTED),review_required=False,disposition_required=True).blockers)
    def test_scope_blocks(self):self.assertIn(MergeBlocker.SCOPE,ProtocolEngine().evaluate_merge_eligibility(self.good().with_updates(safety=SafetyState(mutation_scope_valid=False)),review_required=False,disposition_required=True).blockers)
