# Agent Council Artifact Ledger

## Status

Active programme register.

**Owner:** The Amanuensis.

This ledger identifies the authoritative version of each Agent Council-governed artifact. It is a continuity register, not a claim ledger and not a certificate registry. Mathematical status remains governed by the relevant claim ledger and MATHCERT route.

## Ledger

| Artifact ID | Type | Pillar | Authoritative integrated artifact | Status | Decision records | Review record | Last integrated | Amanuensis state |
|---|---|---|---|---|---|---|---|---|
| GOV-AGENT-COUNCIL-001 | governance bundle | MATH-PROGRAMME | `docs/MATH_PROGRAMME_AGENT_COUNCIL.md` | active | `ADR-0001` | `templates/agent_review.yaml` | 2026-07-09 | reviewed |
| CERT-LOG-GCD-001 | formal certificate fixture | MATHCERT | `fixtures/formal/LOG-GCD-001/README.md` | certified | none | `fixtures/formal/LOG-GCD-001/agent_review.yaml` | 2026-07-23 | reviewed |
| PUB-LOG-GCD-001 | public research note | MATH-PROGRAMME | `docs/LOG_GCD_PUBLICATION.md` | published | none | `fixtures/formal/LOG-GCD-001/agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-WP00 | work package | MATHSOLVE | `campaigns/navier_stokes_critical_integrability/WP00_FOUNDATION_STATUS/00_README.md` | promoted | `ADR-0003` | `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-WP01 | work package | MATHFORGE | `campaigns/navier_stokes_critical_integrability/WP01_FALSE_PROOF_ATLAS/00_README.md` | referee_promoted | `ADR-0003` | `reviews/navier_stokes/NS-CI-WP01.agent_review.yaml` | 2026-07-23 | reviewed |

## Integration order

Merge this WP01 governance change before the WP02 governance change. The WP02 branch carries the combined WP01/WP02 ledger state.

## Update rules

1. Artifact IDs are never reused.
2. The authoritative reference points to the integrated artifact, not a transient draft.
3. Superseded references remain recoverable through version control and decision records.
4. A ledger entry may not be marked reviewed while review provenance is incomplete.
5. A blocking cross-document conflict changes the Amanuensis state to `blocked`.
6. Mathematical promotion is never inferred from ledger status alone.
