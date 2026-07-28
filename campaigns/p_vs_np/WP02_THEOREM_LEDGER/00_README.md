# PNP-WP02 — Source-Normalized Algorithm and Lower-Bound Ledger

**Artifact ID:** `PNP-WP02`  
**Campaign:** `PNP-001`  
**Pillar:** MATHSOLVE  
**Status:** `INTERNAL REVIEW COMPLETE — REPOSITORY GATE PENDING`  
**Audit date:** 2026-07-28  
**Claim class:** `SOURCE-NORMALIZED THEOREM-INTERFACE LEDGER / NON-SOLUTION ARTIFACT`

## Purpose

This package records the theorem interfaces that a P-versus-NP route may legitimately use.

It contains:

- **36 source records**;
- **31 theorem, algorithm, lower-bound, transfer, barrier, or research-programme interfaces**;
- one open terminal target, `PNP-T-130`;
- an explicit dependency and proof-debt gate;
- cross-links to all 46 WP01 fixtures.

The ledger distinguishes:

- complete versus restricted SAT algorithms;
- exact polynomial-time claims versus exponential improvements;
- uniform versus nonuniform computation;
- explicit versus counting lower bounds;
- monotone, constant-depth, modular, threshold, and ACC circuit models;
- proof-system lower bounds and the stronger `NP != coNP` route;
- relativization, natural-proofs, and algebrization barriers;
- hardness-versus-randomness, algorithm-to-lower-bound, magnification, and self-improvement transfers;
- meta-complexity, algebraic complexity, and Geometric Complexity Theory;
- current 2025–2026 frontier results with preprint and model qualifiers preserved.

## Composition rule

A theorem record is an interface, not a free-standing premise. It composes only when its hypotheses, machine model, uniformity, source locator, quantitative threshold, and residual debts match the proposed route.

No present record supplies either terminal certificate:

- a deterministic polynomial-time algorithm for a locked NP-complete language; or
- a superpolynomial lower bound placing an explicit NP language outside deterministic polynomial time.

## Files

- `01_SOURCE_REGISTRY.json`
- `02_THEOREM_LEDGER.json`
- `03_COMPOSITION_RULES.md`
- `04_DEPENDENCY_DEBT_GATE.json`
- `05_NEXT_GATE.md`

## Current-frontier rule

The 2025–2026 records are retained as restricted frontier interfaces. Their presence does not imply progress on the unrestricted terminal target. Source status and theorem scope require refresh before any later promotion or novelty statement.
