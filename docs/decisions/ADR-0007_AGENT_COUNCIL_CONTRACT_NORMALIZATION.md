# ADR-0007: Normalize Agent Council decision, review, and lifecycle contracts

**Date:** 2026-07-24  
**Status:** Accepted  
**Owner:** The Amanuensis with the Verifier, Grammarian, and Referee

## Context

The first Agent Council pilot was merged while later campaigns were adopting several legacy review formats. A cross-document audit then found four contract-level inconsistencies:

1. ADR-0002 claimed that CI validated every committed Agent Council review record, while the validator intentionally checked only explicitly schema-bound records.
2. The aggregate decision register embedded some ADRs but linked others, without identifying which representation was canonical.
3. The Work Package checklist limited review records to MATHSOLVE while governance doctrine described all governed Work Packages.
4. The review schema's pillar, artifact-type, and lifecycle vocabularies were narrower than the programme's governed artifact ledger.

The same audit found that the Union-Closed WP01 status spine still described its completed WP02 handoff as future work.

## Decision

1. Store every ADR as a dedicated file under `docs/decisions/`; use `docs/AGENT_COUNCIL_DECISION_RECORDS.md` only as the canonical index and contract description.
2. Define a **schema-bound Agent Council review record** as a record explicitly registered in `ci/validate_programme.py`. CI validates those records and does not imply that unmigrated legacy formats satisfy the current schema.
3. Require an Agent Council review record for every governed Work Package across MATHFORGE, MATHSOLVE, MATHCERT, and MATH-PROGRAMME. Existing legacy records remain visible migration debt rather than being silently treated as schema-conformant.
4. Separate canonical lifecycle status from detailed disposition. The review schema uses a bounded lifecycle vocabulary and permits a free-text `disposition`; the artifact ledger may retain campaign-specific disposition labels.
5. Extend the schema pillar vocabulary to include `MATH-PROGRAMME` and permit stable snake-case artifact types used by governed artifacts.
6. Treat WP01 as a completed baseline snapshot whose WP02/MATHCERT handoff has been discharged. Downstream theorem and certificate status remains authoritative in WP02, WP04, WP05, and the domain master plan.
7. Re-run the UC-WP01 Amanuensis consistency review against the ADR, ledger, audit, validator, schema, MkDocs navigation, and downstream Work Packages.

## Canonical lifecycle statuses

The review schema recognizes:

- `draft`
- `active`
- `blocked`
- `ready_for_next_stage`
- `ready_for_certification`
- `certified`
- `completed`
- `selected`
- `published`
- `archived`

Campaign-specific phrases such as `referee_promoted_conditional` belong in `artifact.disposition` or the artifact ledger, not in `artifact.status`.

## Alternatives considered

1. Glob every YAML file under `reviews/` and validate it against one schema. Rejected because several established campaigns use pre-contract formats with different field structures; pretending they conform would create false CI assurance.
2. Keep mixed embedded and file-based ADR storage. Rejected because it obscures canonical identity and complicates navigation, linking, and supersession.
3. Restrict the governance contract to MATHSOLVE. Rejected because MATHFORGE, MATHCERT, and programme-level Work Packages already carry review and continuity obligations.
4. Enumerate every campaign-specific ledger status in the review schema. Rejected because it would couple the stable schema to evolving campaign vocabulary.

## Consequences

- ADR-0001, ADR-0003, and ADR-0004 move into dedicated canonical files without semantic change beyond stale ADR-0002 references.
- The decision register becomes an index.
- The schema and its human-readable mirror distinguish lifecycle from disposition.
- Validator tests cover programme-level pillars, stable artifact types, lifecycle tokens, and the explicit schema-bound registry.
- UC-WP01's review date, evidence set, checked-against set, status, and integration notes are refreshed.
- Legacy review migration is explicit nonblocking governance debt; it is not represented as completed work.

## Affected artifacts

- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`
- `docs/decisions/ADR-0001_AMANUENSIS_CONTINUITY_OFFICE.md`
- `docs/decisions/ADR-0002_UNION_CLOSED_AGENT_COUNCIL_PILOT.md`
- `docs/decisions/ADR-0003_NAVIER_STOKES_CRITICAL_INTEGRABILITY.md`
- `docs/decisions/ADR-0004_HODGE_CONJECTURE_CAMPAIGN.md`
- `docs/AGENT_COUNCIL_GOVERNANCE.md`
- `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `UC_WP01_AGENT_COUNCIL_AUDIT.md`
- `reviews/union_closed/UC-WP01.agent_review.yaml`
- `schemas/agent_review.schema.json`
- `schemas/agent_review.schema.yaml`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`
- `mkdocs.yml`

## Review provenance

- Governing instruction: implement the complete documentation consistency repair, 2026-07-24.
- Source audit: cross-document review of the UC-WP01 ledger, ADRs, validator, schemas, review record, status spine, downstream handoff, and MkDocs navigation.
- Repository integration: pull request 85, branch `agent/documentation-consistency-repair`.

## Supersedes

This record supersedes only conflicting documentation about CI review scope, ADR storage, review-record scope, lifecycle vocabulary, and the temporal status of the UC-WP01 handoff. It does not alter any mathematical claim or certificate.
