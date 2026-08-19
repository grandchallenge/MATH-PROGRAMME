from __future__ import annotations

"""Offline deterministic qualification replay. No production executor is present."""
from administrative_protected_receipt_model import *
from administrative_protected_receipt_adapters import *
from administrative_protected_receipt_engine import *


# --- replay.py ---
import copy,hashlib,json
from dataclasses import dataclass
from typing import Any,Mapping,MutableMapping,Sequence
class ReplayFailure(RuntimeError): pass
@dataclass(frozen=True)
class ReplayResult:
    protocol_version:str; fixture_manifest_digest:str; status:str; transition_log:tuple[TransitionEnvelope,...]; predecessor_digest:str; candidate_digest:str; protected_readback_digest:str; initial_candidate_head:str; synchronized_candidate_head:str; simulated_protected_merge:str; mirror_state:MirrorState; idempotent_reentry:str; forbidden_safety_events:tuple[str,...]
    def as_dict(self): return {"protocol_version":self.protocol_version,"fixture_manifest_digest":self.fixture_manifest_digest,"status":self.status,"transition_log":[x.as_dict() for x in self.transition_log],"predecessor_digest":self.predecessor_digest,"candidate_digest":self.candidate_digest,"protected_readback_digest":self.protected_readback_digest,"initial_candidate_head":self.initial_candidate_head,"synchronized_candidate_head":self.synchronized_candidate_head,"simulated_protected_merge":self.simulated_protected_merge,"mirror_state":self.mirror_state.value,"idempotent_reentry":self.idempotent_reentry,"forbidden_safety_events":list(self.forbidden_safety_events)}
    def digest(self): return sha256_json(self.as_dict())
class FixtureProvider:
    def __init__(self,f:Mapping[str,Any]):self.f=copy.deepcopy(dict(f));self.pr=copy.deepcopy(dict(f["pull_request"]));self.synced=False
    def pull_request(self,r,p):return copy.deepcopy(self.pr)
    def branch_sha(self,r,b):return str(self.f["current_base"])
    def is_ancestor(self,r,a,d):
        if a==d:return True
        if [a,d] in self.f.get("ancestry_true",[]):return True
        if [a,d] in self.f.get("ancestry_false",[]):return False
        return None
    def check_runs(self,r,h):return copy.deepcopy(self.f["check_runs_after_sync"] if self.synced else self.f["check_runs_before_sync"])
    def reviews(self,r,p):return copy.deepcopy(self.f.get("reviews",[]))
    def issue_comments(self,r,i):return copy.deepcopy(self.f.get("comments",[]))
    def update_branch(self,r,p,expected_head_sha):
        if self.f.get("update_branch_result")=="rejected":raise RuntimeError("fixture update-branch rejected")
        old=str(self.pr["head"]["sha"])
        if old!=expected_head_sha:raise RuntimeError("expected head mismatch")
        new=str(self.f["synchronized_head"]);self.pr["head"]["sha"]=new;self.synced=True;return {"head_sha":new}
def _sha40(*parts:str)->str:return hashlib.sha1("|".join(parts).encode()).hexdigest()
class ProtocolReplay:
    def __init__(self):self.engine=ProtocolEngine();self.ledger=LedgerAdapter();self.config=ConfigurationAdapter();self.mirror=MirrorAdapter()
    def _env(self,log,state,new,tid,ordinal,result="SUCCESS",planned=(),observed=(),failure=None):
        log.append(TransitionEnvelope(PROTOCOL_VERSION,ordinal,tid,result,state,new,(tid,),tuple(planned),tuple(observed),failure));return new
    def run(self,fixture:Mapping[str,Any])->ReplayResult:
        manifest=sha256_json(fixture);o=OccurrenceIdentity(**fixture["occurrence"]);provider=FixtureProvider(fixture["github"]);gh=GitHubStateAdapter(provider);log=[];n=1
        state=ProductState(issue_navigation=IssueNavigationState(fixture.get("issue_navigation_state","CLOSED")),lane=LaneState.QUALIFICATION_ONLY)
        rec=fixture["protected_record"]
        if rec["procedure_id"]!=o.procedure_id or rec["scheduled_due_at"]!=o.scheduled_due_at or rec["protected_record_merge"]!=o.protected_record_merge or rec["record_sha256"]!=o.protected_record_digest:raise ReplayFailure("protected record binding mismatch")
        new=state.with_updates(occurrence=OccurrenceState.IDENTIFIED,record=RecordState.PROTECTED);state=self._env(log,state,new,"T01_DISCOVER_PROTECTED_OCCURRENCE",n);n+=1
        auth=fixture["authority_objects"]
        if int(auth["review_id"])<=0 or int(auth["human_steward_comment_id"])<=0:raise ReplayFailure("authority object missing")
        new=state.with_updates(authority_objects=AuthorityObjectState.VERIFIED,review=ReviewState.PRESENT_FOR_HEAD,disposition=DispositionState.VALID_FOR_HEAD);state=self._env(log,state,new,"T02_RECONSTRUCT_AUTHORITY",n);n+=1
        dc=fixture["desired_configuration"];desired=DesiredConfiguration(dc["ruleset_id"],RulesetActor(dc["actor_id"],dc["actor_type"],dc["bypass_mode"]),False);raw=fixture["observed_configuration"];obs=self.config.observe(desired,raw)
        if obs.state!=ConfigState.CONVERGED:raise ReplayFailure("configuration not converged")
        new=state.with_updates(config=obs.state);state=self._env(log,state,new,"T03_VERIFY_CONFIGURATION",n);n+=1
        plan=self.config.plan(desired,raw);state=self._env(log,state,state,"T04_PLAN_CONFIGURATION_CONVERGENCE",n,"NO_OP" if plan.no_op else "SUCCESS");n+=1
        state=self._env(log,state,state,"T05_APPLY_CONFIGURATION_CONVERGENCE",n,"NO_OP");n+=1
        pre=copy.deepcopy(fixture["predecessor_ledger"])
        if self.ledger.classify_predecessor(pre,o)!=LedgerState.PREDECESSOR_EXACT:raise ReplayFailure("predecessor not exact")
        rb=fixture["receipt_binding"];binding=ReceiptBinding(o,rb["record_path"],rb["reviewed_head"],rb["record_pull_request"],rb["record_disposition"]);cand=self.ledger.construct_candidate(pre,binding);mut=MutationRecord("candidate","SIMULATE_CONSTRUCT_RECEIPT","completion_ledger")
        new=state.with_updates(receipt=ReceiptState.CANDIDATE,ledger=LedgerState.TARGET_PRESENT_EXACTLY_ONCE);state=self._env(log,state,new,"T06_CONSTRUCT_RECEIPT_CANDIDATE",n,planned=(mut,),observed=(mut,));n+=1
        val=self.ledger.validate_candidate(pre,cand,binding)
        if val.state!=LedgerState.TARGET_PRESENT_EXACTLY_ONCE:raise ReplayFailure(val.reason or "candidate invalid")
        state=self._env(log,state,state,"T07_VALIDATE_CANDIDATE",n);n+=1
        g=fixture["github"];facts=gh.classify_pr(fixture["repository"],g["pull_request"]["number"],g["declared_base_snapshot"],update_control_permitted=True)
        if facts.branch_state!=BranchState.BEHIND_CURRENT_BASE or facts.conflict_state!=ConflictState.CONFLICT_FREE or facts.raw_advisory.get("mergeable_state")!="blocked":raise ReplayFailure("historical stale-state fixture misclassified")
        new=state.with_updates(branch=facts.branch_state,conflict=facts.conflict_state,checks=facts.check_state);state=self._env(log,state,new,"T08_CLASSIFY_BRANCH_FRESHNESS",n);n+=1
        sync=gh.synchronize_candidate(fixture["repository"],g["pull_request"]["number"],g["initial_candidate_head"],g["current_base"])
        if sync.state!=UpdateBranchState.SUCCEEDED:raise ReplayFailure(sync.provider_detail or "sync failed")
        post=state.after_head_mutation().with_updates(branch=BranchState.AT_CURRENT_BASE,conflict=ConflictState.CONFLICT_FREE);mut=MutationRecord("candidate_branch","SIMULATE_UPDATE_BRANCH",str(g["pull_request"]["number"]),sync.old_head,sync.new_head);state=self._env(log,state,post,"T09_SYNCHRONIZE_CANDIDATE",n,planned=(mut,),observed=(mut,));n+=1
        checks=gh.classify_checks(fixture["repository"],sync.new_head or "",tuple(g["pull_request"]["required_checks"]));
        if checks!=CheckState.PASSING:raise ReplayFailure("fresh checks not passing")
        new=state.with_updates(checks=checks,receipt=ReceiptState.REVIEWABLE);state=self._env(log,state,new,"T10_WAIT_FOR_REQUIRED_CHECKS",n);n+=1
        new=state.with_updates(disposition=DispositionState.VALID_FOR_HEAD);state=self._env(log,state,new,"T11_OBTAIN_REFEREE_DISPOSITION",n);n+=1
        state=self._env(log,state,state,"T12_OBTAIN_HUMAN_STEWARD_DISPOSITION",n,"NO_OP");n+=1
        ids=fixture["identities"];candidate=CapabilitySet(ActorRole.CANDIDATE,ActorIdentity(ids["candidate"]["login"],ids["candidate"]["app_id"],"candidate"),frozenset({Capability.WRITE_CANDIDATE,Capability.UPDATE_CANDIDATE_BRANCH}));referee=CapabilitySet(ActorRole.REFEREE,ActorIdentity(ids["referee"]["login"],ids["referee"]["app_id"],"referee"),frozenset({Capability.RECORD_REFEREE_DISPOSITION}));admin=CapabilitySet(ActorRole.ADMINISTRATION,ActorIdentity(ids["administration"]["login"],ids["administration"]["app_id"],"administration"),frozenset({Capability.READ_CONFIGURATION,Capability.WRITE_CONFIGURATION}));state=self.engine.apply_role_separation(state,candidate,referee,admin)
        elig=self.engine.evaluate_merge_eligibility(state,review_required=False,disposition_required=True)
        if not elig.eligible:raise ReplayFailure("merge eligibility blocked: "+str(sorted(x.value for x in elig.blockers)))
        state=self._env(log,state,state.with_updates(blockers=elig.blockers),"T13_EVALUATE_MERGE_ELIGIBILITY",n);n+=1
        merge=_sha40("protected-merge",g["current_base"],sync.new_head or "",val.candidate_digest);mut=MutationRecord("protected_state","SIMULATE_EXPECTED_HEAD_PR_MERGE","main",g["current_base"],merge);state=self._env(log,state,state,"T14_MERGE_EXACT_HEAD",n,planned=(mut,),observed=(mut,));n+=1
        rbval=self.ledger.validate_candidate(pre,cand,binding)
        if rbval.state!=LedgerState.TARGET_PRESENT_EXACTLY_ONCE:raise ReplayFailure("readback invalid")
        new=state.with_updates(receipt=ReceiptState.PROTECTED,ledger=LedgerState.TARGET_PRESENT_EXACTLY_ONCE,branch=BranchState.AT_CURRENT_BASE);state=self._env(log,state,new,"T15_VERIFY_PROTECTED_READBACK",n);n+=1
        p=self.ledger.procedure(cand,o.procedure_id);a=AuthoritativeFrontier(o.procedure_id,p["completed_through_utc"],p["receipt_count"],rbval.candidate_digest,merge);d=DerivedFrontier(a.completed_through_utc,a.receipt_count,a.source_digest,True);mr=self.mirror.classify(a,d)
        if mr.state!=MirrorState.MIRROR_CURRENT:raise ReplayFailure("mirror convergence failed")
        new=state.with_updates(mirror=mr.state);state=self._env(log,state,new,"T16_CONVERGE_MIRRORS",n);n+=1
        state=self._env(log,state,state,"T17_ARCHIVE_TRANSITION_EVIDENCE",n);n+=1
        if self.ledger.classify_predecessor(cand,o)!=LedgerState.TARGET_PRESENT_EXACTLY_ONCE:raise ReplayFailure("idempotent reentry failed")
        state=self._env(log,state,state,"T18_IDEMPOTENT_REENTRY",n,"NO_OP")
        forbidden=[]
        if state.safety.forbidden:forbidden.append("SAFETY_STATE_FORBIDDEN")
        return ReplayResult(PROTOCOL_VERSION,manifest,"QUALIFICATION_REPLAY_COMPLETE",tuple(log),sha256_json(pre),val.candidate_digest,rbval.candidate_digest,g["initial_candidate_head"],sync.new_head or "",merge,mr.state,"NO_OP_ALREADY_PROTECTED",tuple(forbidden))
def load_fixture(path:str)->dict[str,Any]:
    with open(path,encoding="utf-8") as h:return json.load(h)
