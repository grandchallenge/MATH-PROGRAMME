from __future__ import annotations

"""Ledger, mirror, and eligibility engine for generic protected receipts."""
from administrative_protected_receipt_model import *
from administrative_protected_receipt_adapters import *


# --- ledger_adapter.py ---
import copy
from dataclasses import dataclass
from typing import Any,Mapping
@dataclass(frozen=True)
class ReceiptBinding:
    occurrence:OccurrenceIdentity; record_path:str; reviewed_head:str; pull_request:int; disposition:str
@dataclass(frozen=True)
class LedgerValidation:
    state:LedgerState; candidate_digest:str; reason:str|None=None
class LedgerAdapter:
    def procedure(self,ledger:Mapping[str,Any],procedure_id:str)->Mapping[str,Any]:
        p=ledger.get("procedures",{}).get(procedure_id)
        if not isinstance(p,Mapping):raise KeyError(procedure_id)
        return p
    def _target_matches(self,r:Mapping[str,Any],o:OccurrenceIdentity)->bool:
        return r.get("procedure_id")==o.procedure_id and r.get("scheduled_due_at")==o.scheduled_due_at and r.get("merge_commit")==o.protected_record_merge
    def classify_predecessor(self,ledger:Mapping[str,Any],o:OccurrenceIdentity)->LedgerState:
        try:p=self.procedure(ledger,o.procedure_id)
        except KeyError:return LedgerState.UNKNOWN
        matches=[r for r in p.get("receipts",[]) if self._target_matches(r,o)]
        if len(matches)>1:return LedgerState.TARGET_DUPLICATED
        if len(matches)==1:return LedgerState.TARGET_PRESENT_EXACTLY_ONCE
        if int(p.get("receipt_count",-1))!=len(p.get("receipts",[])):return LedgerState.FRONTIER_DIVERGENT
        if str(p.get("completed_through_utc",''))>=o.scheduled_due_at:return LedgerState.FRONTIER_DIVERGENT
        return LedgerState.PREDECESSOR_EXACT
    def construct_candidate(self,predecessor:Mapping[str,Any],binding:ReceiptBinding)->dict[str,Any]:
        if self.classify_predecessor(predecessor,binding.occurrence)!=LedgerState.PREDECESSOR_EXACT:raise ValueError("predecessor not exact or target already present")
        out=copy.deepcopy(dict(predecessor)); p=out["procedures"][binding.occurrence.procedure_id]
        p["receipts"].append({"procedure_id":binding.occurrence.procedure_id,"scheduled_due_at":binding.occurrence.scheduled_due_at,"record_path":binding.record_path,"record_sha256":binding.occurrence.protected_record_digest,"merge_commit":binding.occurrence.protected_record_merge,"reviewed_head":binding.reviewed_head,"pull_request":binding.pull_request,"disposition":binding.disposition,"receipt_state":"PROTECTED_COMPLETE"})
        p["receipt_count"]=int(p["receipt_count"])+1; p["completed_through_utc"]=binding.occurrence.scheduled_due_at
        return out
    def validate_candidate(self,predecessor:Mapping[str,Any],candidate:Mapping[str,Any],binding:ReceiptBinding)->LedgerValidation:
        o=binding.occurrence
        try: pre=self.procedure(predecessor,o.procedure_id); cur=self.procedure(candidate,o.procedure_id)
        except KeyError:return LedgerValidation(LedgerState.UNKNOWN,sha256_json(candidate),"procedure missing")
        matches=[r for r in cur.get("receipts",[]) if self._target_matches(r,o)]
        if len(matches)>1:return LedgerValidation(LedgerState.TARGET_DUPLICATED,sha256_json(candidate),"target duplicated")
        if len(matches)!=1:return LedgerValidation(LedgerState.FRONTIER_DIVERGENT,sha256_json(candidate),"target absent")
        if int(cur.get("receipt_count",-1))!=int(pre.get("receipt_count",-1))+1 or cur.get("completed_through_utc")!=o.scheduled_due_at:return LedgerValidation(LedgerState.FRONTIER_DIVERGENT,sha256_json(candidate),"count/frontier mismatch")
        stripped=copy.deepcopy(dict(candidate)); sp=stripped["procedures"][o.procedure_id]; sp["receipts"]=[r for r in sp["receipts"] if not self._target_matches(r,o)]; sp["receipt_count"]=pre["receipt_count"]; sp["completed_through_utc"]=pre["completed_through_utc"]
        if stripped!=predecessor:return LedgerValidation(LedgerState.UNRELATED_MUTATION,sha256_json(candidate),"unrelated ledger mutation")
        return LedgerValidation(LedgerState.TARGET_PRESENT_EXACTLY_ONCE,sha256_json(candidate))


# --- mirror_adapter.py ---
from dataclasses import dataclass
@dataclass(frozen=True)
class AuthoritativeFrontier:
    procedure_id:str; completed_through_utc:str; receipt_count:int; source_digest:str; protected_head:str
@dataclass(frozen=True)
class DerivedFrontier:
    observed_through_utc:str|None; receipt_count:int|None=None; source_digest:str|None=None; available:bool=True
@dataclass(frozen=True)
class MirrorResult:
    state:MirrorState; receipt_chain_complete:bool; protected_completion_claim:bool; reason:str
class MirrorAdapter:
    def classify(self,a:AuthoritativeFrontier,d:DerivedFrontier)->MirrorResult:
        if not d.available:return MirrorResult(MirrorState.MIRROR_UNAVAILABLE,False,False,"mirror unavailable")
        if not d.observed_through_utc:return MirrorResult(MirrorState.MIRROR_UNKNOWN,False,False,"mirror frontier unknown")
        if d.observed_through_utc>a.completed_through_utc:return MirrorResult(MirrorState.MIRROR_CONFLICTED,False,False,"mirror ahead of protected ledger")
        if d.observed_through_utc<a.completed_through_utc:return MirrorResult(MirrorState.MIRROR_STALE,True,False,"mirror behind protected ledger")
        if d.receipt_count is not None and d.receipt_count!=a.receipt_count:return MirrorResult(MirrorState.MIRROR_CONFLICTED,False,False,"mirror count differs")
        if d.source_digest is not None and d.source_digest!=a.source_digest:return MirrorResult(MirrorState.MIRROR_CONFLICTED,False,False,"mirror source digest differs")
        return MirrorResult(MirrorState.MIRROR_CURRENT,True,False,"mirror agrees with protected source")


# --- engine.py ---
from dataclasses import dataclass
@dataclass(frozen=True)
class Eligibility:
    eligible:bool; blockers:frozenset[MergeBlocker]
class ProtocolEngine:
    def apply_role_separation(self,state:ProductState,candidate:CapabilitySet,referee:CapabilitySet,admin:CapabilitySet)->ProductState:
        failures=validate_role_separation(candidate,referee,admin)
        s=state.safety
        safety=SafetyState(s.direct_protected_push,s.bypass_exercised,s.human_steward_identity_asserted_by_agent,not any("candidate and referee" in x for x in failures),not any("administration" in x or "token roles" in x for x in failures),s.mutation_scope_valid)
        return state.with_updates(safety=safety)
    def evaluate_merge_eligibility(self,state:ProductState,*,review_required:bool,disposition_required:bool,protection_valid:bool=True)->Eligibility:
        b=set()
        if state.occurrence!=OccurrenceState.IDENTIFIED or state.record!=RecordState.PROTECTED or state.authority_objects!=AuthorityObjectState.VERIFIED:b.add(MergeBlocker.UNKNOWN)
        if state.branch!=BranchState.AT_CURRENT_BASE:b.add(MergeBlocker.FRESHNESS)
        if state.conflict!=ConflictState.CONFLICT_FREE:b.add(MergeBlocker.CONFLICT if state.conflict==ConflictState.CONFLICTED else MergeBlocker.UNKNOWN)
        if state.checks!=CheckState.PASSING:b.add(MergeBlocker.CHECKS)
        if review_required and state.review!=ReviewState.PRESENT_FOR_HEAD:b.add(MergeBlocker.REVIEW)
        if disposition_required and state.disposition not in {DispositionState.VALID_FOR_HEAD,DispositionState.NOT_REQUIRED_BY_CONTROL}:b.add(MergeBlocker.DISPOSITION)
        if state.config!=ConfigState.CONVERGED:b.add(MergeBlocker.CONFIGURATION)
        if not protection_valid:b.add(MergeBlocker.PROTECTION)
        if not state.safety.mutation_scope_valid:b.add(MergeBlocker.SCOPE)
        if state.safety.forbidden:b.add(MergeBlocker.IDENTITY if not state.safety.candidate_referee_identity_separated or not state.safety.candidate_admin_capability_separated else MergeBlocker.PROTECTION)
        return Eligibility(not b,frozenset(b))
