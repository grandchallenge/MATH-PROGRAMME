#!/usr/bin/env python3
"""Protected specialist authority and conservative material-routing registry.

This registry is read only from the checked-out protected controller revision.
It cannot be supplied or widened by a candidate PR or inferred from a label.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parents[1] / "governance/specialist_admission_domains.json"
IDENTITY = "GCL-SPECIALIST-ADMISSION-DOMAINS-001"
REPOSITORY = "grandchallenge/MATH-PROGRAMME"

# Deliberately duplicate the authority contract in code: changes to the JSON
# alone cannot silently expand privileged App reviewer routing.
EXPECTED = {
    "MATHEMATICAL": ("grandchallenge/MATHCERT", "certificates/",
                     "INDEPENDENT_NON_AUTHOR", "MATHEMATICAL_PROOF_REVIEW",
                     "GCL_DOMAIN_INDEPENDENT_REVIEW_V1", ()),
    "SOURCE_SEMANTIC": ("grandchallenge/MATHFORGE", "governance/",
                        "ROLE_SCOPED_NON_AUTHOR_SPECIALIST", "SOURCE_SEMANTIC_REVIEW",
                        "GCL_DOMAIN_INDEPENDENT_REVIEW_V1", ("governance/source_",)),
    "SOLUTION_INTEGRITY": ("grandchallenge/MATHSOLVE", "contributions/",
                           "ROLE_SCOPED_NON_AUTHOR_SPECIALIST",
                           "SOLVE_EXECUTION_INTEGRITY_ONLY",
                           "GCL_DOMAIN_ROLE_SCOPED_REVIEW_V1",
                           ("governance/mathsolve_", "governance/solve_execution_",
                            "governance/solution_integrity_")),
    "PROTECTION": ("grandchallenge/INTELLECT", "governance/",
                   "ROLE_SCOPED_NON_AUTHOR_SPECIALIST", "SECURITY_AND_GOVERNANCE_REVIEW",
                   "GCL_DOMAIN_INDEPENDENT_REVIEW_V1", ()),
}
BOUNDARIES = {
    "unmapped_or_mixed": "REJECT",
    "candidate_claims_as_authority": False,
    "mathematical_certification_by_solve": False,
    "source_adjudication_by_solve": False,
    "constitutional_authority_by_solve": False,
    "external_claim_promotion_by_solve": False,
    "no_required_check_cutover": True,
}


class DomainRegistryError(ValueError):
    pass


def load_domains(path: Path = REGISTRY) -> dict[str, dict[str, Any]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if (doc.get("schema_version"), doc.get("registry_id"),
        doc.get("authority"), doc.get("target_repository"), doc.get("status")) != (
        "1.0.0", IDENTITY, "PROTECTED_REPOSITORY_ONLY", REPOSITORY,
        "SHADOW_PLUS_SCOPED_REVIEW_NOT_REQUIRED_CHECK",
    ):
        raise DomainRegistryError("specialist registry identity drift")
    if doc.get("boundaries") != BOUNDARIES:
        raise DomainRegistryError("specialist noncertification boundaries changed")
    entries = doc.get("domains")
    if not isinstance(entries, list) or len(entries) != len(EXPECTED):
        raise DomainRegistryError("unknown or missing specialist domain")
    result = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise DomainRegistryError("invalid specialist domain")
        domain = entry.get("id")
        expected = EXPECTED.get(domain)
        if expected is None or domain in result:
            raise DomainRegistryError("unrecognized or duplicated domain")
        repo, prefix, independence, scope, record_type, candidate_paths = expected
        if entry != {
            "id": domain, "repository": repo, "protected_ref": "main",
            "evidence_prefix": prefix, "independence": independence,
            "review_scope": scope, "review_record_type": record_type,
            "candidate_prefixes": list(candidate_paths),
        }:
            raise DomainRegistryError("specialist scope or authority drift")
        result[domain] = entry
    if set(result) != set(EXPECTED):
        raise DomainRegistryError("specialist registry incomplete")
    return result


def protected_path(path: str) -> bool:
    return path.startswith((
        ".github/workflows/", ".ghos-routing/", "governance/release_trust",
        "governance/constitutional", "schemas/release_trust", "ci/agent_",
        "ci/specialist_",
    )) or path in (
        "mkdocs.yml", "governance/specialist_admission_domains.json",
        # Protected-main operational custody, queue, and policy controller lanes.
        "ci/erdos_catalogue_queue_projection.py",
        "tests/test_erdos_catalogue_queue_projection.py",
        "ci/erdos_event_custody.py",
        "tests/test_erdos_event_custody.py",
        "ci/validate_workflow_coverage_v2.py",
        "tests/test_agent_routine_review.py",
    )


def domain_for_paths(paths: list[str], registry: dict | None = None) -> str | None:
    if not paths or len(paths) > 100 or any(
        not isinstance(p, str) or not p or
        p.startswith("/") or ".." in p.split("/") or "\x00" in p
        for p in paths
    ):
        return None
    authority = registry if registry is not None else load_domains()
    def one(path: str) -> str | None:
        if protected_path(path):
            return "PROTECTION"
        if path.endswith(".lean") or path.startswith(("fixtures/formal/", "fixtures/cmdg/")):
            return "MATHEMATICAL"
        for domain in ("SOURCE_SEMANTIC", "SOLUTION_INTEGRITY"):
            if any(path.startswith(prefix) for prefix in authority[domain]["candidate_prefixes"]):
                return domain
        return None
    routes = {one(path) for path in paths}
    return routes.pop() if len(routes) == 1 and None not in routes else None
