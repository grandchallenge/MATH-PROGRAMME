# ADR-0006: Integrate the Poincaré reconstruction archive

## Status

Accepted, 2026-07-24; filename consequence clarified 2026-07-26.

## Context

`PC-001` was developed as a solved-problem reconstruction campaign while the Birch–Swinnerton-Dyer campaign was integrated concurrently. The draft Poincaré stack initially used Domain 04 and `ADR-0005`. Before PC-001 reached `main`, BSD was canonically integrated as Domain 04 under `ADR-0005`.

Retaining both identifiers would make the programme registers ambiguous without changing any mathematical claim.

## Decision

1. Preserve Hodge as Domain 03 under `ADR-0004`.
2. Preserve BSD as Domain 04 under `ADR-0005`.
3. Integrate Poincaré as Domain 05 under `ADR-0006`.
4. Treat draft-branch references to Poincaré Domain 04 or Poincaré `ADR-0005` as historical pre-integration aliases superseded by this record.
5. Preserve all mathematical, source, certification, and claim-boundary content of `PC-WP00` through `PC-WP05` unchanged.
6. Enter `PC-001` into archival maintenance after qualified archival integration.
7. Remove the mislabelled root alias `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md` from the current tree while preserving it through version history.

## Consequences

- `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md` is the canonical domain entry.
- `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md` is retired from the current tree and remains recoverable only through version history; it must not be listed as a current or retained repository artifact.
- Poincaré artifact-ledger entries reference `ADR-0006`.
- No theorem-strengthening work package is opened.
- Citation correction, documentation preservation, CI maintenance, overclaim repair, and bounded pedagogy remain permitted.

## Claim boundary

This governance repair does not alter the Poincaré theorem, the Hamilton–Perelman reconstruction, the source-concordance disposition, the WP03 event certificate, the WP04 Lean certificate, or the qualified archive claim. It makes no novelty, priority, new-proof, or full-formalization claim.

## Supersession

This record supersedes only the draft-internal governance identifiers `Domain 04` and `ADR-0005` as applied to Poincaré. It does not supersede BSD `ADR-0005`.
