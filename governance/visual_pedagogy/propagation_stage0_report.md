# MP-DOC-VISUAL-PROPAGATION-STAGE0-001 — exact migration manifest

Status: `AUTHORIZED_FOR_STAGE0_MANIFEST_CONSTRUCTION__NO_LIVE_VISUAL_SWITCH_AUTHORITY`

Parent authority: #416  
Implementation docket: #417  
Stage-0 base: `cc0e7a3a87ab298645f1be5e1d6744b0d6cdd7e7`

## Source of truth

`propagation_manifest.json` is derived from protected `governance/documentary_visual_pedagogy_pilot_audit.json` (blob `7ad220f07e2bb36ec6e5e332a222fb3f39b4f18c`). It binds all 45 audited asset paths and exact Git blob identities. The original audit classification remains 19 `KEEP`, 21 `REDRAW`, and 5 `REPLACE`.

The manifest intentionally uses compact record arrays. Their field order is declared by `asset_record_fields` and `migration_record_fields`; repository tests decode and validate those fields mechanically.

## Risk ordering

Migration candidates are ordered ascending by:

`(disposition_rank, domain_sensitivity, representation_risk, provenance_burden, accessibility_adaptation_proxy, live_reference_fanout, audit_uncertainty, canonical_path)`

This is a migration-planning heuristic only. It is not a ranking of mathematical importance, truth, difficulty, novelty, or proof status.

Fanout counts distinct published pages under `docs/documentaries/*.md` containing the unique asset reference suffix beginning at `assets/documentaries/`.

## Fixed tranches

### Batch 1 — REDRAW, 6
- `docs/assets/documentaries/union_closed/plate_garden.svg`
- `docs/assets/documentaries/union_closed/plate_entropy.svg`
- `docs/assets/documentaries/union_closed/plate_lattice.svg`
- `docs/assets/documentaries/union_closed/plate_frequency.svg`
- `docs/assets/documentaries/union_closed/plate_frontier.svg`
- `docs/assets/documentaries/bsd/plate_curve.svg`

### Batch 2 — REDRAW, 6
- `docs/assets/documentaries/bsd/plate_bridge.svg`
- `docs/assets/documentaries/bsd/plate_harmony.svg`
- `docs/assets/documentaries/bsd/plate_frontier.svg`
- `docs/assets/documentaries/bsd/plate_overture.svg`
- `docs/assets/documentaries/hodge/cycles.svg`
- `docs/assets/documentaries/hodge/diamond.svg`

### Batch 3 — REDRAW, 5
- `docs/assets/documentaries/navier_stokes/field.svg`
- `docs/assets/documentaries/navier_stokes/frontier.svg`
- `docs/assets/documentaries/poincare/plate_extinction.svg`
- `docs/assets/documentaries/riemann/euler.svg`
- `docs/assets/documentaries/riemann/evidence.svg`

### Batch 4 — REDRAW, 4
- `docs/assets/documentaries/riemann/explicit.svg`
- `docs/assets/documentaries/yang_mills/curvature.svg`
- `docs/assets/documentaries/hodge/frontier.svg`
- `docs/assets/documentaries/hodge/memory.svg`

### Batch 5 — REPLACE, 5
- `docs/assets/documentaries/navier_stokes/vorticity.svg`
- `docs/assets/documentaries/poincare/plate_geometry.svg`
- `docs/assets/documentaries/poincare/plate_surgery.svg`
- `docs/assets/documentaries/yang_mills/gauge.svg`
- `docs/assets/documentaries/riemann/strip.svg`

Each Batch-5 replacement remains subject to isolated-PR treatment.

## Fail-closed invariants

The Stage-0 test recomputes audit membership, current Git blob identity, counts, batch uniqueness, fixed tranche sizes, live-reference fanout, and the declared risk tuple. It rejects any `KEEP` asset in a batch, any missing rollback identity, any `visual_is_evidence: true`, or any Stage-0 live-switch/blanket-rewrite authority.

## Non-authority

Stage 0 does not change any live visual, does not make a successor authoritative, and does not authorize Batch 1 merge. Batch 1 can begin only after Stage 0 receives independent exact-head review, Human Steward exact-head protected-merge authorization, protected merge, and terminal post-merge readback.
