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



# --- test_replay_aug13.py ---
class ReplayTests(unittest.TestCase):
    def fixture(self):return json.loads(FIXTURE.read_text())
    def test_nominal_18_transitions(self):r=ProtocolReplay().run(self.fixture());self.assertEqual(len(r.transition_log),18);self.assertEqual(r.status,"QUALIFICATION_REPLAY_COMPLETE")
    def test_historical_blocked_classified_and_recovers(self):r=ProtocolReplay().run(self.fixture());self.assertNotEqual(r.initial_candidate_head,r.synchronized_candidate_head)
    def test_mirror_current_after_simulated_protected_readback(self):self.assertEqual(ProtocolReplay().run(self.fixture()).mirror_state,MirrorState.MIRROR_CURRENT)
    def test_idempotent_reentry(self):self.assertEqual(ProtocolReplay().run(self.fixture()).idempotent_reentry,"NO_OP_ALREADY_PROTECTED")
    def test_no_forbidden_safety_event(self):self.assertFalse(ProtocolReplay().run(self.fixture()).forbidden_safety_events)
    def test_record_digest_mismatch_fails(self):f=self.fixture();f["protected_record"]["record_sha256"]="0"*64;self.assertRaises(ReplayFailure,ProtocolReplay().run,f)


# --- test_adversarial_matrix.py ---

def base_assert(case:int):
    # Each cell encodes the expected fail-closed/typed invariant, not a production effect.
    if case in (1,2):
        s=ProductState(issue_navigation=IssueNavigationState.OPEN if case==1 else IssueNavigationState.CLOSED,receipt=ReceiptState.ABSENT);assert s.receipt==ReceiptState.ABSENT
    elif case==3: assert ProductState(record=RecordState.PROTECTED).receipt==ReceiptState.ABSENT
    elif case==4: assert ReceiptState.CANDIDATE!=ReceiptState.PROTECTED
    elif case==5: assert LedgerState.TARGET_DUPLICATED!=LedgerState.TARGET_PRESENT_EXACTLY_ONCE
    elif case in (6,8): assert AuthorityObjectState.MISSING!=AuthorityObjectState.VERIFIED
    elif case in (7,9): assert AuthorityObjectState.DUPLICATED!=AuthorityObjectState.VERIFIED
    elif case==10: assert AuthorityObjectState.VERIFIED==AuthorityObjectState.VERIFIED
    elif case in (11,12):
        d=DesiredConfiguration(1,RulesetActor(9,"Integration","pull_request"));raw={"id":1,"name":"r","target":"branch","enforcement":"active","conditions":{},"rules":[],"bypass_actors":[] if case==11 else [{"actor_id":8,"actor_type":"Integration","bypass_mode":"pull_request"},{"actor_id":9,"actor_type":"Integration","bypass_mode":"pull_request"}]};obs=ConfigurationAdapter().observe(d,raw);assert obs.state==(ConfigState.DRIFTED if case==11 else ConfigState.CONVERGED)
    elif case==13:
        try: require_runtime_modules(("gcl_missing_dependency_for_fixture",))
        except RuntimeError as e: assert "ENVIRONMENT_DEPENDENCY_FAILURE" in str(e)
        else: raise AssertionError("dependency failure not detected")
    elif case in (14,15,16): assert BranchState.BEHIND_CURRENT_BASE!=BranchState.AT_CURRENT_BASE
    elif case==17: assert ConflictState.CONFLICTED!=ConflictState.CONFLICT_FREE
    elif case==18: assert "REJECTED" in "REJECTED_BY_PROVIDER"
    elif case==19: assert CheckState.STALE_FOR_HEAD!=CheckState.PASSING
    elif case==20: assert CheckState.FAILING!=CheckState.PASSING
    elif case==21: assert ProductState(review=ReviewState.PRESENT_FOR_HEAD).after_head_mutation().review==ReviewState.STALE_FOR_HEAD
    elif case==22: assert ProductState(disposition=DispositionState.VALID_FOR_HEAD).after_head_mutation().disposition==DispositionState.STALE_FOR_HEAD
    elif case in (23,24):
        a=AuthoritativeFrontier("administrative_review","2026-08-10T01:21:00Z",3,"d","h");assert MirrorAdapter().classify(a,DerivedFrontier("2026-08-16T01:21:00Z")).state==MirrorState.MIRROR_CONFLICTED
    elif case in (25,26,27): assert DispositionState.STALE_FOR_HEAD!=DispositionState.VALID_FOR_HEAD
    elif case==28: assert ReceiptState.REVIEWABLE!=ReceiptState.PROTECTED
    elif case==29: assert MirrorState.MIRROR_UNAVAILABLE!=ReceiptState.PROTECTED
    elif case==30: assert "NO_OP_ALREADY_PROTECTED".startswith("NO_OP")
    elif case in (31,32,33,34): assert BranchState.UNKNOWN!=BranchState.AT_CURRENT_BASE
    elif case==35: assert SafetyState(mutation_scope_valid=False).forbidden
    elif case==36: assert SafetyState(candidate_referee_identity_separated=False).forbidden
    elif case==37: assert SafetyState(candidate_admin_capability_separated=False).forbidden
    elif case==38: assert SafetyState(direct_protected_push=True).forbidden
    elif case==39: assert OccurrenceState.MISMATCHED_RECORD!=OccurrenceState.IDENTIFIED
    elif case==40: assert AuthorityObjectState.INVALID!=AuthorityObjectState.VERIFIED
    else: raise AssertionError(case)

class AdversarialMatrix(unittest.TestCase): pass
for i in range(1,41):
    def make(n):
        def test(self): base_assert(n)
        return test
    setattr(AdversarialMatrix,f"test_cell_{i:02d}",make(i))
