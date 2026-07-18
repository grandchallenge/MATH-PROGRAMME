# Agent Council Decision Records

## Status

Active programme register.

**Owner:** The Amanuensis.

Decision records preserve governance choices that affect how an artifact must be interpreted, reviewed, integrated, or superseded. They record why a choice was made and which alternatives were rejected. They do not replace mathematical proofs, claim ledgers, or source provenance.

## Record contract

Each decision record contains:

- a stable decision ID;
- date and decision status;
- context and governing problem;
- the adopted decision;
- material alternatives considered;
- consequences and unresolved obligations;
- affected artifact references;
- review-provenance references;
- supersession relationships, when applicable.

## ADR-0001: Establish the Amanuensis continuity office

**Date:** 2026-07-09  
**Status:** Accepted  
**Owner:** The Amanuensis

### Context

The Agent Council assigned specialist responsibilities for foundations, discovery, verification, exposition, implementation, provenance, and external review. No office was responsible for preserving the programme's internal reasoning across revisions or for integrating specialist reviews into one authoritative artifact.

### Decision

Establish the Amanuensis as the council office responsible for:

- the artifact ledger;
- decision records;
- the terminology registry;
- review provenance;
- cross-document consistency;
- final editorial integration.

Every governed artifact carries an `amanuensis_control` record. Promotion is blocked when the artifact-ledger identity is absent, review provenance is incomplete, cross-document consistency is not reviewed, final integration is not reviewed, or no authoritative integrated artifact is identified.

### Alternatives considered

1. Assign these duties to the Archivist. Rejected because external literature provenance and internal editorial continuity are distinct responsibilities.
2. Leave continuity implicit in pull-request history. Rejected because commit history does not express semantic decisions, unresolved obligations, or the authoritative integrated version.
3. Treat final integration as a Composer duty. Rejected because composition governs artifact structure, not continuity across versions and review states.

### Consequences

- The Exposition Kernel expands from four writing offices to an Exposition and Continuity Kernel of five offices.
- Agent-review schemas require the Amanuensis and an `amanuensis_control` record.
- Work Package promotion now includes continuity and integration gates.
- The repository maintains canonical artifact, decision, and terminology registers.

### Affected artifacts

- `docs/MATH_PROGRAMME_AGENT_COUNCIL.md`
- `docs/AGENT_COUNCIL_GOVERNANCE.md`
- `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- `templates/agent_review.yaml`
- `schemas/agent_review.schema.json`
- `schemas/agent_review.schema.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`

### Review provenance

- Governing instruction: Grand Challenge MATH-PROGRAMME council deliberation, 2026-07-09.
- Repository integration: pull request 50, branch `agent-council-governance`.

### Supersedes

No prior decision record.

## ADR-0002: Use Union-Closed WP01 as the first Agent Council campaign pilot

**Date:** 2026-07-17  
**Status:** Accepted  
**Owner:** The Amanuensis

### Context

The Agent Council had repository-level doctrine, review schemas, and promotion gates but had not yet been tested against a real mathematical campaign. The first pilot needed enough mathematical substance to expose governance failure while remaining bounded enough to distinguish useful discipline from bureaucratic duplication.

Union-Closed WP01 already contained a formal problem statement, literature status, exact bounded computation, a claim ledger, failure analysis, and a MATHCERT handoff. It therefore provided a meaningful test of foundations, dependency mapping, verification, adversarial review, formal boundaries, continuity, and referee acceptance.

### Decision

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

### Anti-bureaucracy constraints

1. One authoritative review record per governed Work Package state.
2. One dependency DAG containing only promotion-relevant nodes.
3. Nonblocking obligations remain visible without halting useful work.
4. A new review version is required only when mathematical status, representation, dependencies, or promotion state materially changes.
5. Council review cannot upgrade mathematical claim status without the relevant proof or certificate route.

### Consequences

- `UC-WP01` becomes the first battle-tested council-governed mathematical artifact.
- CI validates all committed Agent Council review records, not only the blank template.
- Promotion semantics reject blocking unresolved obligations, incomplete continuity control, or unreviewed core campaign offices.
- The pilot yields a reusable pattern for later Union-Closed Work Packages without requiring a new governance document for routine changes.

### Unresolved obligations

- Literature-status claims require periodic freshness review.
- Any finite-range extension requires an independent replay and new ledger entry.
- Finite-set and lattice formulations require explicit correspondence lemmas before claims transfer between them.
- Any original theorem claim requires a fresh novelty and contribution-boundary review.

### Affected artifacts

- `WP01_UNION_CLOSED_STATUS_SPINE.md`
- `UC_WP01_AGENT_COUNCIL_AUDIT.md`
- `reviews/union_closed/UC-WP01.agent_review.yaml`
- `reviews/union_closed/UC-WP01.dependency_dag.yaml`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- `ci/validate_programme.py`
- `ci/test_validate_programme.py`

### Review provenance

- Governing instruction: apply the council to the Union-Closed campaign without bureaucratic overhead, 2026-07-17.
- Existing mathematical evidence: WP01 status spine, WP02 formal handoff, claim ledger, bounded exact audit, and MATHCERT replay route.

### Supersedes

No prior campaign-pilot decision record.
