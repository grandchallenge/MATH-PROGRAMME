#!/usr/bin/env python3
"""Construction-time integrity gate for governed agent work.

Authority-bearing inputs are expected to be read from protected main. Callers
may propose a commit and an operation, but may not supply their own predecessor,
path scope, lifecycle policy, or governed branch namespace.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

CONTROL_ID = "MP-CONSTRUCTION-INTEGRITY-001"
REPOSITORY = "grandchallenge/MATH-PROGRAMME"
PROTECTED_BRANCH = "main"
ALLOWED_OPERATIONS = {"CREATE_DEVELOPMENT", "UPDATE_DEVELOPMENT", "FREEZE_CANDIDATE"}
TERMINAL_STATES = {"FROZEN_CANDIDATE", "REVIEWED", "ADMITTED"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ConstructionIntegrityError(RuntimeError):
    pass


@dataclass(frozen=True)
class Decision:
    allowed: bool
    code: str
    reasons: tuple[str, ...]
    target_id: str
    operation: str
    observed_ref: str
    observed_head: str
    proposed_head: str
    authority_digest: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "control_id": CONTROL_ID,
            "allowed": self.allowed,
            "code": self.code,
            "reasons": list(self.reasons),
            "target_id": self.target_id,
            "operation": self.operation,
            "observed_ref": self.observed_ref,
            "observed_head": self.observed_head,
            "proposed_head": self.proposed_head,
            "authority_digest": self.authority_digest,
        }


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _sha(value: Any) -> bool:
    return isinstance(value, str) and SHA_RE.fullmatch(value) is not None


def validate_contract(contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "control_id": CONTROL_ID,
        "repository": REPOSITORY,
        "protected_branch": PROTECTED_BRANCH,
        "authority_source": "PROTECTED_MAIN_ONLY",
        "mutation_protocol": "ATOMIC_REF_COMPARE_AND_SWAP_V1",
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            errors.append(f"{key} drift")
    if contract.get("state") not in {"PROPOSED_NOT_ACTIVE", "ACTIVE"}:
        errors.append("invalid control state")
    namespaces = contract.get("namespaces", {})
    if namespaces.get("development") != "refs/heads/gcl/dev/":
        errors.append("development namespace drift")
    if namespaces.get("candidate") != "refs/heads/gcl/candidate/":
        errors.append("candidate namespace drift")
    if contract.get("frozen_candidate_updates_allowed") is not False:
        errors.append("frozen candidate updates must be prohibited")
    if contract.get("force_ref_updates_allowed") is not False:
        errors.append("force ref updates must be prohibited")
    if contract.get("operator_supplied_authority_allowed") is not False:
        errors.append("operator supplied authority must be prohibited")
    targets = contract.get("targets")
    if not isinstance(targets, list):
        errors.append("targets must be a list")
        return errors
    seen: set[str] = set()
    for index, target in enumerate(targets):
        prefix = f"targets/{index}"
        if not isinstance(target, Mapping):
            errors.append(f"{prefix}: target must be an object")
            continue
        target_id = target.get("target_id")
        if not isinstance(target_id, str) or not target_id:
            errors.append(f"{prefix}: target_id missing")
        elif target_id in seen:
            errors.append(f"{prefix}: duplicate target_id")
        else:
            seen.add(target_id)
        if not _sha(target.get("authorized_predecessor")):
            errors.append(f"{prefix}: authorized_predecessor must be a 40-char SHA")
        if target.get("lifecycle_state") not in {"DEVELOPMENT", *TERMINAL_STATES}:
            errors.append(f"{prefix}: invalid lifecycle_state")
        dev_ref = target.get("development_ref")
        cand_ref = target.get("candidate_ref")
        if not isinstance(dev_ref, str) or not dev_ref.startswith("refs/heads/gcl/dev/"):
            errors.append(f"{prefix}: invalid development_ref")
        if not isinstance(cand_ref, str) or not cand_ref.startswith("refs/heads/gcl/candidate/"):
            errors.append(f"{prefix}: invalid candidate_ref")
        allowed_paths = target.get("allowed_paths", [])
        allowed_prefixes = target.get("allowed_path_prefixes", [])
        if not isinstance(allowed_paths, list) or not all(isinstance(x, str) and x for x in allowed_paths):
            errors.append(f"{prefix}: invalid allowed_paths")
        if not isinstance(allowed_prefixes, list) or not all(isinstance(x, str) and x for x in allowed_prefixes):
            errors.append(f"{prefix}: invalid allowed_path_prefixes")
        if not allowed_paths and not allowed_prefixes:
            errors.append(f"{prefix}: empty path authority")
        patterns = target.get("forbidden_path_patterns", [])
        if not isinstance(patterns, list) or not all(isinstance(x, str) for x in patterns):
            errors.append(f"{prefix}: invalid forbidden_path_patterns")
        else:
            for pattern in patterns:
                try:
                    re.compile(pattern)
                except re.error:
                    errors.append(f"{prefix}: invalid forbidden regex {pattern!r}")
        if target.get("deny_update_when_exact_head_evidence_exists") is not True:
            errors.append(f"{prefix}: exact-head invalidation guard must be enabled")
    boundaries = contract.get("claim_boundaries")
    if not isinstance(boundaries, Mapping) or not boundaries or any(v is not False for v in boundaries.values()):
        errors.append("claim boundaries must all remain false")
    return errors


def target_by_id(contract: Mapping[str, Any], target_id: str) -> Mapping[str, Any] | None:
    for target in contract.get("targets", []):
        if isinstance(target, Mapping) and target.get("target_id") == target_id:
            return target
    return None


def path_allowed(path: str, target: Mapping[str, Any]) -> bool:
    if path in set(target.get("allowed_paths", [])):
        return True
    return any(path.startswith(prefix) for prefix in target.get("allowed_path_prefixes", []))


def forbidden_paths(paths: Iterable[str], target: Mapping[str, Any]) -> list[str]:
    patterns = [re.compile(pattern) for pattern in target.get("forbidden_path_patterns", [])]
    return sorted(path for path in paths if any(pattern.search(path) for pattern in patterns))


def _deny(reasons: Sequence[str], target_id: str, operation: str,
          observation: Mapping[str, Any], authority_digest: str,
          code: str = "DENIED") -> Decision:
    return Decision(False, code, tuple(sorted(set(reasons))), target_id, operation,
                    str(observation.get("ref") or ""),
                    str(observation.get("current_head") or ""),
                    str(observation.get("proposed_head") or ""), authority_digest)


def preflight(contract: Mapping[str, Any], target_id: str, operation: str,
              observation: Mapping[str, Any]) -> Decision:
    """Return an allow/deny decision from protected authority and observed Git facts."""
    contract_errors = validate_contract(contract)
    authority_digest = canonical_digest(contract)
    if contract_errors:
        return _deny([f"invalid protected contract: {item}" for item in contract_errors],
                     target_id, operation, observation, authority_digest,
                     "INVALID_PROTECTED_AUTHORITY")
    if contract.get("state") != "ACTIVE":
        return _deny(["construction integrity control is not active"], target_id,
                     operation, observation, authority_digest, "CONTROL_NOT_ACTIVE")
    if operation not in ALLOWED_OPERATIONS:
        return _deny(["unsupported operation"], target_id, operation,
                     observation, authority_digest)
    target = target_by_id(contract, target_id)
    if target is None:
        return _deny(["target has no protected authority row"], target_id,
                     operation, observation, authority_digest,
                     "MISSING_TARGET_AUTHORITY")

    reasons: list[str] = []
    if observation.get("repository") != REPOSITORY:
        reasons.append("repository mismatch")
    if observation.get("protected_branch") != PROTECTED_BRANCH:
        reasons.append("protected branch mismatch")

    predecessor = str(target["authorized_predecessor"])
    proposed_head = str(observation.get("proposed_head") or "")
    current_head = str(observation.get("current_head") or "")
    merge_base = str(observation.get("merge_base") or "")
    if not _sha(proposed_head):
        reasons.append("proposed head is not an exact commit SHA")
    if current_head and not _sha(current_head):
        reasons.append("current head is not an exact commit SHA")

    lifecycle = target["lifecycle_state"]
    dev_ref = str(target["development_ref"])
    cand_ref = str(target["candidate_ref"])
    observed_ref = str(observation.get("ref") or "")
    if lifecycle in TERMINAL_STATES and operation != "FREEZE_CANDIDATE":
        reasons.append(f"target lifecycle is immutable: {lifecycle}")

    if operation == "CREATE_DEVELOPMENT":
        if observed_ref != dev_ref:
            reasons.append("development ref mismatch")
        if observation.get("ref_exists") is not False:
            reasons.append("development ref already exists")
        if proposed_head != predecessor:
            reasons.append("new development ref must start at authorized predecessor")
        if observation.get("predecessor_exists") is not True:
            reasons.append("authorized predecessor does not exist")

    if operation == "UPDATE_DEVELOPMENT":
        if observed_ref != dev_ref:
            reasons.append("development ref mismatch")
        if observation.get("ref_exists") is not True:
            reasons.append("development ref does not exist")
        if lifecycle != "DEVELOPMENT":
            reasons.append("only DEVELOPMENT targets may be updated")
        if observation.get("candidate_ref_exists") is True:
            reasons.append("candidate ref already exists; development is frozen")
        if (target.get("deny_update_when_exact_head_evidence_exists") is True and
                observation.get("exact_head_evidence_exists") is True):
            reasons.append("update would invalidate exact-head evidence")
        if observation.get("predecessor_exists") is not True:
            reasons.append("authorized predecessor does not exist")
        if observation.get("predecessor_is_ancestor") is not True:
            reasons.append("authorized predecessor is not ancestor of proposed head")
        if merge_base != predecessor:
            reasons.append("merge base is not the authorized predecessor")
        changed = observation.get("changed_paths")
        if not isinstance(changed, list) or not all(isinstance(x, str) and x for x in changed):
            reasons.append("changed path inventory unavailable")
        else:
            widened = sorted(path for path in changed if not path_allowed(path, target))
            if widened:
                reasons.append(f"path scope widened: {widened}")
            contaminated = forbidden_paths(changed, target)
            if contaminated:
                reasons.append(f"forbidden governed paths present: {contaminated}")

    if operation == "FREEZE_CANDIDATE":
        if observed_ref != cand_ref:
            reasons.append("candidate ref mismatch")
        if lifecycle != "DEVELOPMENT":
            reasons.append("only DEVELOPMENT targets may be frozen")
        if observation.get("candidate_ref_exists") is not False:
            reasons.append("candidate ref already exists")
        dev_head = str(observation.get("development_head") or "")
        if not _sha(dev_head):
            reasons.append("development head unavailable")
        if proposed_head != dev_head:
            reasons.append("candidate must freeze the exact development head")
        if observation.get("predecessor_exists") is not True:
            reasons.append("authorized predecessor does not exist")
        if observation.get("predecessor_is_ancestor") is not True:
            reasons.append("authorized predecessor is not ancestor of candidate")
        if merge_base != predecessor:
            reasons.append("candidate merge base is not authorized predecessor")
        changed = observation.get("changed_paths")
        if not isinstance(changed, list) or not all(isinstance(x, str) and x for x in changed):
            reasons.append("changed path inventory unavailable")
        else:
            widened = sorted(path for path in changed if not path_allowed(path, target))
            if widened:
                reasons.append(f"path scope widened: {widened}")
            contaminated = forbidden_paths(changed, target)
            if contaminated:
                reasons.append(f"forbidden governed paths present: {contaminated}")

    if observation.get("force_requested") is True:
        reasons.append("force ref update prohibited")
    if reasons:
        return _deny(reasons, target_id, operation, observation, authority_digest)
    return Decision(True, "ALLOWED", (), target_id, operation, observed_ref,
                    current_head, proposed_head, authority_digest)


def transaction_spec(decision: Decision, observation: Mapping[str, Any]) -> dict[str, Any]:
    """Build the only permitted remote-ref transaction after a green preflight."""
    if not decision.allowed:
        raise ConstructionIntegrityError("cannot build transaction from denied preflight")
    repository_id = str(observation.get("repository_id") or "")
    if not repository_id:
        raise ConstructionIntegrityError("repository node id is required")
    if decision.operation == "UPDATE_DEVELOPMENT":
        before = str(observation.get("current_head") or "")
        if not _sha(before):
            raise ConstructionIntegrityError("compare-and-swap beforeOid is missing")
        before_oid = before
    elif decision.operation in {"CREATE_DEVELOPMENT", "FREEZE_CANDIDATE"}:
        before_oid = "0" * 40
    else:
        raise ConstructionIntegrityError("unsupported allowed operation")
    return {
        "protocol": "GRAPHQL_UPDATE_REFS_BEFORE_OID_V1",
        "repositoryId": repository_id,
        "refUpdates": [{
            "name": decision.observed_ref,
            "beforeOid": before_oid,
            "afterOid": decision.proposed_head,
            "force": False,
        }],
    }


def classify_legacy_pr(contract: Mapping[str, Any], target_id: str,
                       observation: Mapping[str, Any]) -> dict[str, Any]:
    """Read-only classification. It creates no merge or mutation authority."""
    target = target_by_id(contract, target_id)
    if target is None:
        return {"classification": "OUTSIDE_GOVERNED_SCOPE",
                "target_id": target_id, "reasons": []}
    synthetic = dict(observation)
    synthetic["ref"] = target["development_ref"]
    synthetic["ref_exists"] = True
    synthetic["candidate_ref_exists"] = False
    decision = preflight(contract, target_id, "UPDATE_DEVELOPMENT", synthetic)
    if decision.allowed:
        return {"classification": "LEGACY_CLEAN", "target_id": target_id,
                "reasons": []}
    return {"classification": "LEGACY_REQUIRES_RECONSTRUCTION",
            "target_id": target_id, "reasons": list(decision.reasons)}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ConstructionIntegrityError(f"{path}: expected JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--operation", choices=sorted(ALLOWED_OPERATIONS), required=True)
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    decision = preflight(load_json(args.contract), args.target, args.operation,
                         load_json(args.observation))
    rendered = json.dumps(decision.as_dict(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if decision.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
