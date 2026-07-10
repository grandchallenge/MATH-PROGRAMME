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
