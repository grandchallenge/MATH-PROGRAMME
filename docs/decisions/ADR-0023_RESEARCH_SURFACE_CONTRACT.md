# ADR-0023 — GCL Research Surface Contract

**Date:** 2026-10-07  
**Status:** Human Steward directed full implementation; candidate protected admission in progress  
**Operation:** GCL-RESEARCH-SURFACE-CONTRACT-001  
**Tracker:** MATH-PROGRAMME #1224

## Context

GCL research state has historically been distributed among GitHub issues, protected repository records, and MkDocs pages. Each is useful, but ambiguity arises when a mutable tracker, a certified claim record, and a reader-facing explanation are treated as interchangeable.

The CM4 closeout demonstrated a cleaner architecture:

```text
GitHub issue = live research state
protected record = certified claim authority
MkDocs = Chaidez-compliant human model
```

## Decision

Adopt the three-surface architecture programme-wide for material research campaigns.

The three roles are named `LIVE`, `AUTHORITY`, and `EXPOSITION`.

No surface may silently acquire the authority class of another.

The normative operational contract is
`docs/RESEARCH_SURFACE_CONTRACT.md`.

## Machine implementation

- registry: `governance/research_surfaces.json`;
- schema: `schemas/research_surface_registry.schema.json`;
- validator: `ci/validate_research_surfaces.py`;
- reconciliation diagnostic: `ci/reconcile_research_surfaces.py`;
- policy enforcement: routed through existing policy shards; no new autonomous workflow is created.

## Rollout rule

CM4 is the reference exemplar. RH-001, OPENMATH-2026, YM-001, EUCLID-GCD-E2E-001 and PC-WP01 form the initial varied pilot cohort.

After pilot validation, active campaigns are migrated before inactive history. Historical artifacts are not rewritten merely to satisfy the new convention.

## Automation boundary

Automation may detect missing/stale surface relations and emit deterministic reconciliation actions. It may not infer theorem truth, certify a claim, close a mathematical issue, or rewrite protected authority based solely on mutable issue state.

## Supersession

This ADR extends ADR-0008/0009 documentation coverage, the Chaidez Pedagogical Protocol, and existing protected-record doctrine. It does not weaken any prior claim-boundary, review, certification, or documentary-integrity requirement.
