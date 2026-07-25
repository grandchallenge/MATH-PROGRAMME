# Agent Council Decision Records

## Status

Active programme index.

**Owner:** The Amanuensis.

Decision records preserve governance choices that affect how an artifact must be interpreted, reviewed, integrated, or superseded. They record why a choice was made and which alternatives were rejected. They do not replace mathematical proofs, claim ledgers, or source provenance.

## Canonical storage rule

Every decision record has one canonical file under `docs/decisions/`. This document is the index and contract description; it does not duplicate ADR bodies. Historical embedded copies remain recoverable through version control.

## Record contract

Each decision record contains:

- a stable decision ID;
- date and decision status;
- context and governing problem;
- the adopted decision;
- material alternatives considered;
- consequences and unresolved obligations, when applicable;
- affected artifact references;
- review-provenance references;
- supersession relationships, when applicable.

## Active index

| Decision | Date | Status | Scope | Canonical record |
|---|---|---|---|---|
| ADR-0001 | 2026-07-09 | Accepted | Establish the Amanuensis continuity office. | [`ADR-0001_AMANUENSIS_CONTINUITY_OFFICE.md`](decisions/ADR-0001_AMANUENSIS_CONTINUITY_OFFICE.md) |
| ADR-0002 | 2026-07-17 | Accepted | Use Union-Closed WP01 as the first Agent Council campaign pilot. | [`ADR-0002_UNION_CLOSED_AGENT_COUNCIL_PILOT.md`](decisions/ADR-0002_UNION_CLOSED_AGENT_COUNCIL_PILOT.md) |
| ADR-0003 | 2026-07-23 | Accepted for draft initialization | Initialize the Navier–Stokes critical-integrability campaign. | [`ADR-0003_NAVIER_STOKES_CRITICAL_INTEGRABILITY.md`](decisions/ADR-0003_NAVIER_STOKES_CRITICAL_INTEGRABILITY.md) |
| ADR-0004 | 2026-07-24 | Accepted for draft WP00 audit | Initialize the governed rational Hodge cycle-class campaign. | [`ADR-0004_HODGE_CONJECTURE_CAMPAIGN.md`](decisions/ADR-0004_HODGE_CONJECTURE_CAMPAIGN.md) |
| ADR-0005 | 2026-07-24 | Accepted and WP00 promoted | Initialize Birch–Swinnerton-Dyer under source-and-equivalence controls. | [`ADR-0005_BSD_SOURCE_EQUIVALENCE.md`](decisions/ADR-0005_BSD_SOURCE_EQUIVALENCE.md) |
| ADR-0006 | 2026-07-24 | Accepted | Integrate the Poincaré reconstruction archive and normalize domain identifiers. | [`ADR-0006_POINCARE_RECONSTRUCTION_ARCHIVE.md`](decisions/ADR-0006_POINCARE_RECONSTRUCTION_ARCHIVE.md) |
| ADR-0007 | 2026-07-24 | Accepted | Normalize Agent Council decision, review, lifecycle, and UC-WP01 temporal contracts. | [`ADR-0007_AGENT_COUNCIL_CONTRACT_NORMALIZATION.md`](decisions/ADR-0007_AGENT_COUNCIL_CONTRACT_NORMALIZATION.md) |

## Identifier rule

ADR identifiers are never reused. A later decision may supersede all or part of an earlier decision, but both records remain in the index with the supersession boundary stated in the later ADR.
