# Agent Council Artifact Ledger

## Status

Active programme register. Owner: Amanuensis.

This is a continuity register, not a claim ledger or certificate registry.

| Artifact ID | Type | Pillar | Authoritative artifact | Status | Review record | Amanuensis state |
|---|---|---|---|---|---|---|
| GOV-AGENT-COUNCIL-001 | governance bundle | MATH-PROGRAMME | `docs/MATH_PROGRAMME_AGENT_COUNCIL.md` | active | `templates/agent_review.yaml` | reviewed |
| CERT-LOG-GCD-001 | formal certificate fixture | MATHCERT | `fixtures/formal/LOG-GCD-001/README.md` | certified | `fixtures/formal/LOG-GCD-001/agent_review.yaml` | reviewed |
| PUB-LOG-GCD-001 | public research note | MATH-PROGRAMME | `docs/LOG_GCD_PUBLICATION.md` | published | `fixtures/formal/LOG-GCD-001/agent_review.yaml` | reviewed |
| NS-CI-WP00 | work package | MATHSOLVE | `campaigns/navier_stokes_critical_integrability/WP00_FOUNDATION_STATUS/00_README.md` | promoted | `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml` | reviewed |
| NS-CI-WP01 | work package | MATHFORGE | `campaigns/navier_stokes_critical_integrability/WP01_FALSE_PROOF_ATLAS/00_README.md` | referee_promoted | `reviews/navier_stokes/NS-CI-WP01.agent_review.yaml` | reviewed |

## Integration order

Merge this WP01 governance change before WP02. The WP02 branch carries the combined WP01/WP02 ledger state.

## Rules

Artifact IDs are never reused. Authoritative references identify integrated artifacts. Promotion is never inferred from ledger status alone. Blocking cross-document conflicts set Amanuensis state to `blocked`.
