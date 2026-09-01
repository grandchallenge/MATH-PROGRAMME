from __future__ import annotations

"""Typed external-state adapters for generic protected receipts."""
from administrative_protected_receipt_model import *

from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class RulesetActor:
    actor_id:int; actor_type:str; bypass_mode:str
    def as_dict(self): return {"actor_id":self.actor_id,"actor_type":self.actor_type,"bypass_mode":self.bypass_mode}
@dataclass(frozen=True)
class DesiredConfiguration:
    ruleset_id:int; actor:RulesetActor; direct_protected_push:bool=False
@dataclass(frozen=True)
class ConfigObservation:
    state:ConfigState; observed_digest:str|None; target_present:bool; non_target_digest:str|None; body_digest:str|None; reason:str|None=None
@dataclass(frozen=True)
class ConfigPlan:
    operation:str; before_digest:str; target:RulesetActor; non_target_digest:str; body_digest:str
    @property
    def no_op(self): return self.operation=="NO_OP"
class ConfigurationAdapter:
    BODY_KEYS=("name","target","enforcement","conditions","rules")
    def _actors(self,raw:Mapping[str,Any])->list[dict[str,Any]]:
        out=[]
        for x in raw.get("bypass_actors",[]):
            if not all(k in x for k in ("actor_id","actor_type","bypass_mode")): raise ValueError("incomplete bypass actor")
            out.append({"actor_id":int(x["actor_id"]),"actor_type":str(x["actor_type"]),"bypass_mode":str(x["bypass_mode"])})
        return sorted(out,key=lambda x:(x["actor_type"],x["actor_id"],x["bypass_mode"]))
    def observe(self,desired:DesiredConfiguration, raw:Mapping[str,Any]|None)->ConfigObservation:
        if not raw or int(raw.get("id",-1))!=desired.ruleset_id: return ConfigObservation(ConfigState.UNKNOWN,None,False,None,None,"ruleset unavailable or wrong id")
        try: actors=self._actors(raw)
        except (TypeError,ValueError): return ConfigObservation(ConfigState.UNKNOWN,None,False,None,None,"provider schema incomplete")
        target=desired.actor.as_dict(); present=target in actors
        non=[a for a in actors if a!=target]
        body={k:raw.get(k) for k in self.BODY_KEYS}
        return ConfigObservation(ConfigState.CONVERGED if present and not desired.direct_protected_push else ConfigState.DRIFTED,sha256_json(raw),present,sha256_json(non),sha256_json(body),None if present else "target actor missing")
    def plan(self,desired:DesiredConfiguration, raw:Mapping[str,Any])->ConfigPlan:
        obs=self.observe(desired,raw)
        if obs.state==ConfigState.UNKNOWN: raise ValueError("cannot plan from unknown configuration")
        return ConfigPlan("NO_OP" if obs.target_present else "ADD_EXACT_TARGET",obs.observed_digest or "",desired.actor,obs.non_target_digest or "",obs.body_digest or "")
    def verify_preservation(self,plan:ConfigPlan, after:Mapping[str,Any], desired:DesiredConfiguration)->bool:
        obs=self.observe(desired,after)
        return obs.state==ConfigState.CONVERGED and obs.non_target_digest==plan.non_target_digest and obs.body_digest==plan.body_digest

from enum import Enum
from typing import Protocol, Sequence
class UpdateBranchState(str,Enum):
    PERMITTED_TO_ATTEMPT="PERMITTED_TO_ATTEMPT"; NOT_NEEDED="NOT_NEEDED"; NOT_PERMITTED_BY_POLICY="NOT_PERMITTED_BY_POLICY"; REJECTED_BY_PROVIDER="REJECTED_BY_PROVIDER"; SUCCEEDED="SUCCEEDED"; UNKNOWN="UNKNOWN"
class Provider(Protocol):
    def pull_request(self,repository:str,pr_number:int)->Mapping[str,Any]:...
    def branch_sha(self,repository:str,branch:str)->str:...
    def is_ancestor(self,repository:str,ancestor:str,descendant:str)->bool|None:...
    def check_runs(self,repository:str,head_sha:str)->Sequence[Mapping[str,Any]]:...
    def reviews(self,repository:str,pr_number:int)->Sequence[Mapping[str,Any]]:...
    def issue_comments(self,repository:str,issue_number:int)->Sequence[Mapping[str,Any]]:...
    def update_branch(self,repository:str,pr_number:int,expected_head_sha:str)->Mapping[str,Any]:...
@dataclass(frozen=True)
class GitHubFacts:
    current_base_sha:str; candidate_head_sha:str; candidate_recorded_base_sha:str; branch_state:BranchState; conflict_state:ConflictState; check_state:CheckState; update_branch_state:UpdateBranchState; raw_advisory:dict[str,Any]
@dataclass(frozen=True)
class AuthorityLookup:
    authority_state:AuthorityObjectState; review_state:ReviewState|None=None; disposition_state:DispositionState|None=None; object_id:int|None=None
@dataclass(frozen=True)
class SyncResult:
    state:UpdateBranchState; old_head:str; new_head:str|None; provider_detail:str|None=None
class GitHubStateAdapter:
    def __init__(self,provider:Provider): self.provider=provider
    @staticmethod
    def _head(pr:Mapping[str,Any])->str:
        h=pr.get("head"); return str(h.get("sha")) if isinstance(h,Mapping) else str(pr.get("head_sha") or "")
    def classify_branch(self,repository:str,b0:str,h:str,b1:str)->BranchState:
        if not h:return BranchState.HEAD_MISSING
        if not b0 or not b1:return BranchState.BASE_MISSING
        a_b1_h=self.provider.is_ancestor(repository,b1,h)
        if b1==h or a_b1_h is True:return BranchState.AT_CURRENT_BASE
        a_b0_h=self.provider.is_ancestor(repository,b0,h); a_b0_b1=self.provider.is_ancestor(repository,b0,b1)
        if a_b0_h is True and a_b0_b1 is True and a_b1_h is False:return BranchState.BEHIND_CURRENT_BASE
        if None in (a_b0_h,a_b0_b1,a_b1_h):return BranchState.UNKNOWN
        return BranchState.DIVERGED_FROM_DECLARED_BASE
    def classify_checks(self,repository:str,head:str,required:tuple[str,...])->CheckState:
        if not required:return CheckState.PASSING
        runs=list(self.provider.check_runs(repository,head)); by={str(x.get("name")):x for x in runs if str(x.get("head_sha") or head)==head}
        if any(n not in by for n in required):return CheckState.NOT_STARTED
        if any(by[n].get("status")!="completed" for n in required):return CheckState.PENDING
        if any(by[n].get("conclusion") not in {"success","neutral","skipped"} for n in required):return CheckState.FAILING
        return CheckState.PASSING
    def classify_pr(self,repository:str,pr_number:int,declared_base_snapshot:str,*,update_control_permitted:bool)->GitHubFacts:
        pr=self.provider.pull_request(repository,pr_number); head=self._head(pr); base_ref=str(pr.get("base",{}).get("ref") if isinstance(pr.get("base"),Mapping) else pr.get("base_ref") or "main"); current=self.provider.branch_sha(repository,base_ref)
        branch=self.classify_branch(repository,declared_base_snapshot,head,current)
        mergeable=pr.get("mergeable")
        conflict=(ConflictState.CONFLICT_FREE if mergeable is True else ConflictState.CONFLICTED if mergeable is False else ConflictState.UNKNOWN)
        checks=self.classify_checks(repository,head,tuple(pr.get("required_checks",())))
        update=UpdateBranchState.NOT_NEEDED if branch==BranchState.AT_CURRENT_BASE else (UpdateBranchState.PERMITTED_TO_ATTEMPT if branch==BranchState.BEHIND_CURRENT_BASE and conflict==ConflictState.CONFLICT_FREE and update_control_permitted else UpdateBranchState.NOT_PERMITTED_BY_POLICY)
        return GitHubFacts(current,head,declared_base_snapshot,branch,conflict,checks,update,{"mergeable":mergeable,"mergeable_state":pr.get("mergeable_state")})
    def lookup_exact_review(self,repository:str,pr:int,review_id:int,head:str,login:str)->AuthorityLookup:
        matches=[x for x in self.provider.reviews(repository,pr) if int(x.get("id",-1))==review_id]
        if not matches:return AuthorityLookup(AuthorityObjectState.MISSING,ReviewState.ABSENT)
        if len(matches)!=1:return AuthorityLookup(AuthorityObjectState.DUPLICATED,ReviewState.INVALID)
        x=matches[0]
        if str(x.get("user",{}).get("login"))!=login:return AuthorityLookup(AuthorityObjectState.INVALID,ReviewState.INVALID,object_id=review_id)
        if str(x.get("commit_id") or x.get("head_sha"))!=head:return AuthorityLookup(AuthorityObjectState.STALE,ReviewState.STALE_FOR_HEAD,object_id=review_id)
        return AuthorityLookup(AuthorityObjectState.VERIFIED,ReviewState.PRESENT_FOR_HEAD,object_id=review_id)
    def lookup_exact_comment(self,repository:str,issue:int,comment_id:int,login:str,required_markers:tuple[str,...])->AuthorityLookup:
        matches=[x for x in self.provider.issue_comments(repository,issue) if int(x.get("id",-1))==comment_id]
        if not matches:return AuthorityLookup(AuthorityObjectState.MISSING,disposition_state=DispositionState.ABSENT)
        if len(matches)!=1:return AuthorityLookup(AuthorityObjectState.DUPLICATED,disposition_state=DispositionState.INVALID)
        x=matches[0]; body=str(x.get("body") or "")
        if str(x.get("user",{}).get("login"))!=login or any(m not in body for m in required_markers):return AuthorityLookup(AuthorityObjectState.INVALID,disposition_state=DispositionState.INVALID,object_id=comment_id)
        return AuthorityLookup(AuthorityObjectState.VERIFIED,disposition_state=DispositionState.VALID_FOR_HEAD,object_id=comment_id)
    def synchronize_candidate(self,repository:str,pr:int,expected_head:str,current_base:str)->SyncResult:
        observed=self.provider.pull_request(repository,pr); old=self._head(observed)
        if old!=expected_head:return SyncResult(UpdateBranchState.REJECTED_BY_PROVIDER,old,None,"expected head mismatch")
        try: value=self.provider.update_branch(repository,pr,expected_head)
        except Exception as exc:return SyncResult(UpdateBranchState.REJECTED_BY_PROVIDER,old,None,str(exc))
        new=str(value.get("head_sha") or "")
        return SyncResult(UpdateBranchState.SUCCEEDED if new and new!=old else UpdateBranchState.UNKNOWN,old,new or None,None)
