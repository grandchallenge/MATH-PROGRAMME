from __future__ import annotations

"""Typed state, capabilities, and diagnostics for generic protected receipts."""


# --- model.py ---

from dataclasses import dataclass, field, replace
from enum import Enum
import re
from typing import FrozenSet

PROTOCOL_VERSION = "GCL-PROTECTED-RECEIPT/1.0"
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value

class OccurrenceState(StrEnum):
    UNRESOLVED="UNRESOLVED"; IDENTIFIED="IDENTIFIED"; DUPLICATE="DUPLICATE"; MISMATCHED_RECORD="MISMATCHED_RECORD"; UNKNOWN="UNKNOWN"
class RecordState(StrEnum):
    ABSENT="ABSENT"; CANDIDATE="CANDIDATE"; PROTECTED="PROTECTED"; INVALID="INVALID"; UNKNOWN="UNKNOWN"
class ReceiptState(StrEnum):
    ABSENT="ABSENT"; CANDIDATE="CANDIDATE"; SYNCHRONIZED="SYNCHRONIZED"; REVIEWABLE="REVIEWABLE"; PROTECTED="PROTECTED"; INVALID="INVALID"; UNKNOWN="UNKNOWN"
class LedgerState(StrEnum):
    PREDECESSOR_EXACT="PREDECESSOR_EXACT"; TARGET_PRESENT_EXACTLY_ONCE="TARGET_PRESENT_EXACTLY_ONCE"; TARGET_DUPLICATED="TARGET_DUPLICATED"; FRONTIER_DIVERGENT="FRONTIER_DIVERGENT"; UNRELATED_MUTATION="UNRELATED_MUTATION"; UNKNOWN="UNKNOWN"
class MirrorState(StrEnum):
    MIRROR_CURRENT="MIRROR_CURRENT"; MIRROR_STALE="MIRROR_STALE"; MIRROR_CONFLICTED="MIRROR_CONFLICTED"; MIRROR_UNAVAILABLE="MIRROR_UNAVAILABLE"; MIRROR_UNKNOWN="MIRROR_UNKNOWN"
class BranchState(StrEnum):
    AT_CURRENT_BASE="AT_CURRENT_BASE"; BEHIND_CURRENT_BASE="BEHIND_CURRENT_BASE"; DIVERGED_FROM_DECLARED_BASE="DIVERGED_FROM_DECLARED_BASE"; HEAD_MISSING="HEAD_MISSING"; BASE_MISSING="BASE_MISSING"; UNKNOWN="UNKNOWN"
class ConflictState(StrEnum):
    CONFLICT_FREE="CONFLICT_FREE"; CONFLICTED="CONFLICTED"; UNKNOWN="UNKNOWN"
class CheckState(StrEnum):
    NOT_STARTED="NOT_STARTED"; PENDING="PENDING"; PASSING="PASSING"; FAILING="FAILING"; STALE_FOR_HEAD="STALE_FOR_HEAD"; UNKNOWN="UNKNOWN"
class ReviewState(StrEnum):
    ABSENT="ABSENT"; PRESENT_FOR_HEAD="PRESENT_FOR_HEAD"; STALE_FOR_HEAD="STALE_FOR_HEAD"; INVALID="INVALID"; UNKNOWN="UNKNOWN"
class DispositionState(StrEnum):
    ABSENT="ABSENT"; VALID_FOR_HEAD="VALID_FOR_HEAD"; STALE_FOR_HEAD="STALE_FOR_HEAD"; INVALID="INVALID"; NOT_REQUIRED_BY_CONTROL="NOT_REQUIRED_BY_CONTROL"; UNKNOWN="UNKNOWN"
class ConfigState(StrEnum):
    CONVERGED="CONVERGED"; DRIFTED="DRIFTED"; UNKNOWN="UNKNOWN"
class AuthorityObjectState(StrEnum):
    VERIFIED="VERIFIED"; MISSING="MISSING"; DUPLICATED="DUPLICATED"; INVALID="INVALID"; STALE="STALE"; UNKNOWN="UNKNOWN"
class IssueNavigationState(StrEnum):
    OPEN="OPEN"; CLOSED="CLOSED"; MISSING="MISSING"; UNKNOWN="UNKNOWN"
class LaneState(StrEnum):
    SUSPENDED="SUSPENDED"; QUALIFICATION_ONLY="QUALIFICATION_ONLY"; ACTIVE="ACTIVE"; UNKNOWN="UNKNOWN"
class MergeBlocker(StrEnum):
    FRESHNESS="BLOCKED_BY_FRESHNESS"; CONFLICT="BLOCKED_BY_CONFLICT"; CHECKS="BLOCKED_BY_CHECKS"; REVIEW="BLOCKED_BY_REVIEW"; DISPOSITION="BLOCKED_BY_DISPOSITION"; CONFIGURATION="BLOCKED_BY_CONFIGURATION"; PROTECTION="BLOCKED_BY_PROTECTION"; SCOPE="BLOCKED_BY_SCOPE"; IDENTITY="BLOCKED_BY_IDENTITY"; UNKNOWN="BLOCKED_BY_UNKNOWN"

@dataclass(frozen=True)
class OccurrenceIdentity:
    procedure_id: str
    scheduled_due_at: str
    protected_record_merge: str
    protected_record_digest: str
    def __post_init__(self) -> None:
        if not self.procedure_id.strip(): raise ValueError("procedure_id must be nonempty")
        if not self.scheduled_due_at.endswith("Z"): raise ValueError("scheduled_due_at must be canonical UTC")
        if not _SHA40.fullmatch(self.protected_record_merge): raise ValueError("protected_record_merge must be 40 hex")
        if not _SHA256.fullmatch(self.protected_record_digest): raise ValueError("protected_record_digest must be sha256")
    @property
    def idempotency_key(self) -> tuple[str,str,str]:
        return (self.procedure_id,self.scheduled_due_at,self.protected_record_merge)

@dataclass(frozen=True)
class SafetyState:
    direct_protected_push: bool=False
    bypass_exercised: bool=False
    human_steward_identity_asserted_by_agent: bool=False
    candidate_referee_identity_separated: bool=True
    candidate_admin_capability_separated: bool=True
    mutation_scope_valid: bool=True
    @property
    def forbidden(self) -> bool:
        return self.direct_protected_push or self.bypass_exercised or self.human_steward_identity_asserted_by_agent or not self.candidate_referee_identity_separated or not self.candidate_admin_capability_separated or not self.mutation_scope_valid

@dataclass(frozen=True)
class ProductState:
    occurrence: OccurrenceState=OccurrenceState.UNRESOLVED
    record: RecordState=RecordState.UNKNOWN
    receipt: ReceiptState=ReceiptState.ABSENT
    ledger: LedgerState=LedgerState.UNKNOWN
    mirror: MirrorState=MirrorState.MIRROR_UNKNOWN
    branch: BranchState=BranchState.UNKNOWN
    conflict: ConflictState=ConflictState.UNKNOWN
    checks: CheckState=CheckState.NOT_STARTED
    review: ReviewState=ReviewState.ABSENT
    disposition: DispositionState=DispositionState.ABSENT
    config: ConfigState=ConfigState.UNKNOWN
    authority_objects: AuthorityObjectState=AuthorityObjectState.UNKNOWN
    issue_navigation: IssueNavigationState=IssueNavigationState.UNKNOWN
    lane: LaneState=LaneState.QUALIFICATION_ONLY
    safety: SafetyState=field(default_factory=SafetyState)
    blockers: FrozenSet[MergeBlocker]=field(default_factory=frozenset)
    def with_updates(self, **kwargs) -> "ProductState":
        return replace(self, **kwargs)
    def after_head_mutation(self) -> "ProductState":
        return replace(self, receipt=ReceiptState.SYNCHRONIZED,
            checks=CheckState.STALE_FOR_HEAD if self.checks != CheckState.NOT_STARTED else CheckState.NOT_STARTED,
            review=ReviewState.STALE_FOR_HEAD if self.review == ReviewState.PRESENT_FOR_HEAD else self.review,
            disposition=DispositionState.STALE_FOR_HEAD if self.disposition == DispositionState.VALID_FOR_HEAD else self.disposition)


# --- capabilities.py ---
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet

class StrEnum(str, Enum):
    def __str__(self): return self.value
class ActorRole(StrEnum):
    EVIDENCE="EVIDENCE"; CANDIDATE="CANDIDATE"; ADMINISTRATION="ADMINISTRATION"; REFEREE="REFEREE"; HUMAN_STEWARD="HUMAN_STEWARD"; MIRROR="MIRROR"; ARCHIVE="ARCHIVE"; MERGE_EXECUTOR="MERGE_EXECUTOR"
class Capability(StrEnum):
    READ_EVIDENCE="READ_EVIDENCE"; WRITE_CANDIDATE="WRITE_CANDIDATE"; UPDATE_CANDIDATE_BRANCH="UPDATE_CANDIDATE_BRANCH"; READ_CONFIGURATION="READ_CONFIGURATION"; WRITE_CONFIGURATION="WRITE_CONFIGURATION"; RECORD_REFEREE_DISPOSITION="RECORD_REFEREE_DISPOSITION"; VALIDATE_HUMAN_STEWARD_DISPOSITION="VALIDATE_HUMAN_STEWARD_DISPOSITION"; MERGE_PULL_REQUEST_EXACT_HEAD="MERGE_PULL_REQUEST_EXACT_HEAD"; WRITE_MIRROR="WRITE_MIRROR"; WRITE_ARCHIVE="WRITE_ARCHIVE"
@dataclass(frozen=True)
class ActorIdentity:
    login: str; app_id: int|None; token_role: str
    def __post_init__(self):
        if not self.login or not self.token_role: raise ValueError("identity fields must be nonempty")
        if self.app_id is not None and self.app_id <= 0: raise ValueError("app_id must be positive")
    @property
    def stable_key(self): return (self.login,self.app_id,self.token_role)
@dataclass(frozen=True)
class CapabilitySet:
    role: ActorRole; identity: ActorIdentity; capabilities: FrozenSet[Capability]
    def require(self,*caps: Capability):
        missing=[c.value for c in caps if c not in self.capabilities]
        if missing: raise PermissionError("missing capabilities: "+", ".join(sorted(missing)))
def validate_role_separation(candidate:CapabilitySet, referee:CapabilitySet, administration:CapabilitySet)->tuple[str,...]:
    f=[]
    if candidate.role != ActorRole.CANDIDATE: f.append("candidate role mislabeled")
    if referee.role != ActorRole.REFEREE: f.append("referee role mislabeled")
    if administration.role != ActorRole.ADMINISTRATION: f.append("administration role mislabeled")
    if candidate.identity.stable_key == referee.identity.stable_key: f.append("candidate and referee identities coincide")
    if candidate.identity.token_role == administration.identity.token_role: f.append("candidate and administration token roles coincide")
    if Capability.WRITE_CONFIGURATION in candidate.capabilities: f.append("candidate has administration capability")
    if Capability.WRITE_CANDIDATE in administration.capabilities: f.append("administration has candidate-content capability")
    if Capability.WRITE_CANDIDATE in referee.capabilities: f.append("referee has candidate-content capability")
    return tuple(f)
def assert_no_human_steward_synthesis(role:ActorRole)->None:
    if role != ActorRole.HUMAN_STEWARD: raise PermissionError("only Human Steward may originate Human Steward authority")
def require_runtime_modules(names:tuple[str,...])->None:
    import importlib
    missing=[]
    for n in names:
        try: importlib.import_module(n)
        except ModuleNotFoundError: missing.append(n)
    if missing: raise RuntimeError("ENVIRONMENT_DEPENDENCY_FAILURE: missing "+", ".join(sorted(missing)))


# --- diagnostics.py ---
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import hashlib, json
from typing import Any, Mapping, Sequence

def _jsonable(v:Any)->Any:
    if isinstance(v,Enum): return v.value
    if is_dataclass(v): return {k:_jsonable(x) for k,x in asdict(v).items()}
    if isinstance(v,Mapping): return {str(k):_jsonable(x) for k,x in v.items()}
    if isinstance(v,(list,tuple,set,frozenset)): return [_jsonable(x) for x in v]
    return v
def canonical_json(v:Any)->str:
    return json.dumps(_jsonable(v),sort_keys=True,separators=(",",":"),ensure_ascii=False)
def sha256_json(v:Any)->str:
    return hashlib.sha256(canonical_json(v).encode()).hexdigest()
@dataclass(frozen=True)
class MutationRecord:
    surface:str; operation:str; object_id:str; before:str|None=None; after:str|None=None
@dataclass(frozen=True)
class TransitionEnvelope:
    protocol_version:str; ordinal:int; transition_id:str; result:str; input_state:Any; output_state:Any; authoritative_input_ids:tuple[str,...]; planned_mutations:tuple[MutationRecord,...]=(); observed_mutations:tuple[MutationRecord,...]=(); failure_code:str|None=None
    @property
    def diagnostic_artifact_id(self)->str: return sha256_json(self)
    def as_dict(self): return _jsonable(self)
def failure_diagnostic(*,transition_id:str,state:Any,predicate:str,inputs:Sequence[str],code:str)->dict[str,Any]:
    body={"schema_version":"1.0.0","transition_id":transition_id,"typed_state":_jsonable(state),"failed_predicate":predicate,"authoritative_inputs":list(inputs),"failure_code":code,"authority_created":False}
    body["diagnostic_artifact_id"]=sha256_json(body)
    return body
