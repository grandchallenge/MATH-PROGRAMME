# CMDG-CONDENSED-CM4-001 — parent dependency reconciliation

## Candidate disposition

`CM4_DEPENDENCY_RECONCILIATION_READY__P3_NEXT_PENDING_PROTECTED_ADMISSION`

This package does **not** certify CM4. It reconciles the protected CM4-P2 closure into parent issue #355, removes the stale representation of P2 as a blocker, records the remaining dependency DAG, and selects the next bounded dependency lane. Protected CM4 authority is unchanged until this reconciliation itself is reviewed and admitted.

## Protected CM4-P2 receipt

CM4-P2 is no longer an open parent dependency.

- operation: `CMDG-CONDENSED-CM4-P2-001`
- issue: `#363` — closed / completed
- implementation/reconciliation PR: `#443`
- independently reviewed / Human-Steward-approved exact head: `36d29b4dea3b3049016e3a7277923cb37a7579f4`
- protected merge: `2abad244b57ab148184b3033524b7ec636cb7c7f`
- protected tree: `6c8c6ba86306571ed75294977842af8b3beeb245`
- protected CM4-P2 replay: `31549886295` — success
- protected P2-E replay: `31549886166` — success
- Programme policy: `31549886179` — success
- GCL conformance: `31549886679` — success

The admitted P2 interface is the canonical measure/dual representation plus the natural reconstruction equivalence. Its chosen-basis product presentation remains auxiliary, objectwise, noncanonical, and without naturality authority.

**CM4-P2 — protected-closed / available.**

## Frozen CM4 target

The module-level target remains unchanged:

```lean
∀ S : Profinite.{u},
  CondensedMod.IsSolid (ULift.{u + 1} ℤ)
    ((Condensed.profiniteSolid (ULift.{u + 1} ℤ)).obj S)
```

No theorem asserting this proposition is added by the reconciliation.

## Reconciled dependency graph

### CM4-P1 — available

Nöbeling/Specker freeness remains machine-replayable through `LocallyConstant.freeOfProfinite`.

### CM4-P2 — protected-closed / available

The former product/measure reconstruction blocker is discharged by protected P2-D/P2-E evidence. Parent CM4 must not continue to model P2 as blocking.

### CM4-P3 — selected next lane

Higher-cohomology / Ext vanishing for arbitrary profinite `S` with discrete integer coefficients remains unproved at the pinned CM4 boundary.

P3 has no unresolved dependency inside the currently characterized CM4 graph. It is therefore an independently closable remaining root prerequisite.

**Operational selection:** `CM4-P3`.

This is a bounded programme choice, not a claim that the dependency graph has a mathematically unique next operation or that global dependency minimality has been proved.

### CM4-P5 — remaining source-route root

The condensed `ℝ` / `ℝ/ℤ` exact-sequence and derived-Hom machinery used by the source proof remains unresolved. P5 is also a root blocker, but its immediate role is to support the source route into P4.

### CM4-P4 — downstream on the source route

The required equivalent of

`RHom(∏_J ℤ, ℤ) ≃ ⊕_J ℤ`

remains unresolved.

The source-route dependency is:

`P5 → P4`

P4 must not silently bypass P5. A direct alternative P4 proof is permitted only as a separately governed operation that explicitly records why P5 becomes unnecessary and how source-concordance accounting changes.

### CM4-P6 — final witness construction

The `CondensedMod.IsSolid` and solidification interfaces exist, and P2 is now discharged. P6 nevertheless remains partially blocking until P3 and P4 are closed and the exact `IsIso` witnesses can be constructed without assumptions or placeholders.

Remaining outstanding edge structure:

```text
P3 ───────────┐
              ├──> P6 ──> CM4 theorem attempt
P5 ──> P4 ────┘
```

P1 and P2 are already available.

## Why P3 is next

P3 and P5 are both unresolved roots. P4 is not an equivalent root because the source route reaches it through P5.

P3 is selected first because it closes an independent mandatory source ingredient without requiring the programme to commit yet to the larger condensed-real/circle reconstruction needed for the source P5 → P4 route. This sequencing leaves both later possibilities open:

1. reconstruct P5 and then certify P4 by the source route; or
2. separately govern a direct alternative P4 proof and record the resulting source-concordance change.

The selection therefore reduces the unresolved dependency set while preserving optionality. It does not assert uniqueness or global minimality.

## Exact pinned environment preserved

- Lean: `leanprover/lean4:v4.33.0-rc1`
- Lean commit: `62eed1db4d67327ec8120be05f1a1b0847d74561`
- mathlib commit: `79d0395a1825a6264ad5d269e35e60537518955e`
- mathlib tree: `d76f5e09b832a08949f6d8ad4fb80ce30527da64`

The historical exact-tree observations remain bounded observations. In particular, absence of dedicated `Mathlib/Condensed/Derived`, `Measure`, `Real`, or `Circle` loci is not a claim that relevant category theory is globally absent from mathlib.

## Admission boundary

Before protected admission of this reconciliation:

- `CM4-P3` is selected but a child lane is not yet authorized by the record;
- `CM4-P4`, `CM4-P5`, and `CM4-P6` remain unresolved;
- issue #355 remains open;
- the CM4 theorem remains uncertified.

After protected admission, the next separately governed mathematical operation should be a bounded CM4-P3 exact-tree interface audit and vanishing reconstruction/certification attempt.

## Preserved nonclaims

This package does not establish CM4, the derived/complex form of Proposition 0.5.7, arbitrary finite-type `ℤ`-algebra free-solid theorems, arbitrary commutative- or noncommutative-ring solidity, equivalence between pinned and reconstructed C05 predicates, an abelian category of solid modules, closure under limits/colimits/extensions/tensor/internal Hom, a solidification reflector, liquid mathematics, broader C04, C06, `GRAPH_CERTIFIED`, dependency minimality or uniqueness, CM5, or global CMDG completeness.
