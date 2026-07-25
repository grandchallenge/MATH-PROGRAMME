# ADR-0002: Use Union-Closed WP01 as the first Agent Council campaign pilot

**Date:** 2026-07-17  
**Status:** Accepted  
**Owner:** The Amanuensis

## Context

The Agent Council had repository-level doctrine, review schemas, and promotion gates but had not yet been tested against a real mathematical campaign. The first pilot needed enough mathematical substance to expose governance failure while remaining bounded enough to distinguish useful discipline from bureaucratic duplication.

Union-Closed WP01 already contained a formal problem statement, literature status, exact bounded computation, a claim ledger, failure analysis, and a MATHCERT handoff. It therefore provided a meaningful test of foundations, dependency mapping, verification, adversarial review, formal boundaries, continuity, and referee acceptance.

## Decision

Govern `WP01_UNION_CLOSED_STATUS_SPINE.md` through one canonical Agent Council review record and one minimal dependency DAG.

The pilot must explicitly record:

- the Axiomatist foundational profile;
- the Cartographer dependency graph;
- Verifier obligations;
- Adversary failure modes;
- the Formalist boundary;
- the Amanuensis ledger and continuity state;
- Referee acceptance criteria.

The review record references existing proofs, certificates, claim ledgers, and source artifacts. It does not reproduce them.

## Anti-bureaucracy constraints

1. One authoritative review record per governed Work Package state.
2. One dependency DAG containing only promotion-relevant nodes.
3. Nonblocking obligations remain visible without halting useful work.
4. A new review version is required only when mathematical status, representation, dependencies, or promotion state materially changes.
5. Council review cannot upgrade mathematical claim status without the relevant proof or certificate route.

## Consequences

- `UC-WP01` becomes the first battle-tested council-governed mathematical artifact.
- CI validates all committed Agent Council review records, not only the blank template.
- Promotion semantics reject blocking unresolved obligations, incomplete continuity control, or unreviewed core campaign offices.
- The pilot yields a reusable pattern for later Union-Closed Work Packages without requiring a new governance document for routine changes.

## Unresolved obligations

- Literature-status claims require periodic freshness review.
- Any finite-range extension requires an independent replay and new ledger entry.
- Finite-set and lattice formulations require explicit correspondence lemmas before claims transfer between them.
- Any original theorem claim requires a fresh novelty and contribution-boundary review.

## Affected artifacts

- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `UC_WP01_AGENT_COUNCIL_AUDIT.md`
- `reviews/union_closed/UC-WP01.agent_review.yaml`
- `reviews/union_closed/UC-WP01.dependency_dag.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`

## Review provenance

- Governing instruction: apply the council to the Union-Closed campaign without bureaucratic overhead, 2026-07-17.
- Existing mathematical evidence: WP01 status spine, WP02 formal handoff, claim ledger, bounded exact audit, and MATHCERT replay route.

## Supersedes

No prior campaign-pilot decision record.
