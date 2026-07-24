# Agent Council Artifact Ledger

## Status

Active programme register.

**Owner:** The Amanuensis.

This ledger identifies the authoritative version of each Agent Council-governed artifact. It is a continuity register, not a claim ledger and not a certificate registry. Mathematical status remains governed by the relevant claim ledger and MATHCERT route.

## Required entry fields

Every governed artifact receives:

- a stable artifact ID;
- an artifact type and owning pillar;
- one authoritative integrated artifact reference;
- lifecycle status;
- references to relevant decision records;
- a terminology-registry reference when terms are introduced or changed;
- an Agent Council review-record reference;
- the most recent editorial-integration date;
- the current Amanuensis continuity state.

## Ledger

| Artifact ID | Type | Pillar | Authoritative integrated artifact | Status | Decision records | Terminology registry | Review record | Last integrated | Amanuensis state |
|---|---|---|---|---|---|---|---|---|---|
| GOV-AGENT-COUNCIL-001 | governance bundle | MATH-PROGRAMME | `docs/MATH_PROGRAMME_AGENT_COUNCIL.md` | active | `ADR-0001` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `templates/agent_review.yaml` | 2026-07-09 | reviewed |
| CERT-LOG-GCD-001 | formal certificate fixture | MATHCERT | `fixtures/formal/LOG-GCD-001/README.md` | certified | none | `docs/GLOSSARY.md` | `fixtures/formal/LOG-GCD-001/agent_review.yaml` | 2026-07-23 | reviewed |
| PUB-LOG-GCD-001 | public research note | MATH-PROGRAMME | `docs/LOG_GCD_PUBLICATION.md` | published | none | `docs/GLOSSARY.md` | `fixtures/formal/LOG-GCD-001/agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-WP00 | work package | MATHSOLVE | `campaigns/navier_stokes_critical_integrability/WP00_FOUNDATION_STATUS/00_README.md` | promoted | `ADR-0003` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/navier_stokes/NS-CI-WP00.agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-WP01 | work package | MATHFORGE | `campaigns/navier_stokes_critical_integrability/WP01_FALSE_PROOF_ATLAS/00_README.md` | referee_promoted | `ADR-0003` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/navier_stokes/NS-CI-WP01.agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-WP02 | work package | MATHSOLVE | `campaigns/navier_stokes_critical_integrability/WP02_CONDITIONAL_REGULARITY_LEDGER/00_README.md` | referee_promoted | `ADR-0003` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/navier_stokes/NS-CI-WP02.agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-WP04 | work package | MATH-PROGRAMME | `campaigns/navier_stokes_critical_integrability/WP04_RESTRICTED_TARGET_SCORECARD/00_README.md` | referee_selected_target | `ADR-0003`; `WP04/01`; `WP04/02` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/navier_stokes/NS-CI-WP04.agent_review.yaml` | 2026-07-23 | reviewed |
| NS-CI-R014-A2 | selected research target | MATHSOLVE | `campaigns/navier_stokes_critical_integrability/WP04_RESTRICTED_TARGET_SCORECARD/02_REFEREE_SELECTION.md` | selected_unproved | `WP04/02` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/navier_stokes/NS-CI-WP04.agent_review.yaml` | 2026-07-23 | active |
| HC-WP00 | work package | MATH-PROGRAMME | `campaigns/hodge_conjecture/WP00_FOUNDATION_STATUS/00_README.md` | promoted | `ADR-0004` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/hodge_conjecture/HC-WP00.agent_review.yaml` | 2026-07-24 | reviewed |
| BSD-WP00 | work package | MATHSOLVE | `campaigns/birch_swinnerton_dyer/WP00_FOUNDATION_STATUS/00_README.md` | promoted | `ADR-0005` | `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md` | `reviews/birch_swinnerton_dyer/BSD-WP00.agent_review.yaml` | 2026-07-24 | reviewed |

## Update rules

1. Artifact IDs are never reused.
2. The authoritative reference points to the integrated artifact, not a transient draft.
3. Superseded references remain recoverable through version control and decision records.
4. A ledger entry may not be marked reviewed while review provenance is incomplete.
5. A blocking cross-document conflict changes the Amanuensis state to `blocked`.
6. Mathematical promotion is never inferred from ledger status alone.
7. Publication status changes visibility and editorial readiness; it does not change the underlying claim status.
