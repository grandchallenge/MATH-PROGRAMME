# CMDG-CONDENSED-CM4-P2-001 — `profiniteSolid` product/measure bridge audit

Parent operation: `CMDG-CONDENSED-CM4-001` / issue #355  
Dependency operation: issue #363  
Protected baseline: `5aa885344835be0c462542ab6dce8e17a0b75401`  
Protected baseline tree: `cf86f3b98631a4cf3ede24b068ffb0ae092c9a05`

## Purpose

This operation isolates **CM4-P2**. It asks whether the exact pinned formal closure contains, or permits us to construct without new semantic assumptions, a source-concordant bridge from the canonical `Condensed.profiniteSolid` right-Kan-extension object to the canonical measure/dual description needed by the source proof of Scholze Proposition 0.5.7.

This package does **not** certify CM4 and does not close CM4-P2.

## Exact environment

- Lean image/toolchain: `leanprover/lean4:v4.33.0-rc1`
- Lean commit: `62eed1db4d67327ec8120be05f1a1b0847d74561`
- mathlib commit: `79d0395a1825a6264ad5d269e35e60537518955e`
- mathlib tree: `d76f5e09b832a08949f6d8ad4fb80ce30527da64`
- `Mathlib/Condensed/Solid.lean`: `f5214433f91ee87fc8fbe7e2746e0bd227faed2a`
- `Mathlib/Topology/Category/Profinite/Nobeling/Induction.lean`: `2989eac53e537e47fd9ac93cba92d50856573173`
- `Mathlib/Condensed/Discrete/Module.lean`: `b3ba358aa6b01b2de4cfedf6480ac22e863241d3`

## Exact-tree audit result

### P2-A — canonical right-Kan presentation: `AVAILABLE`

Pinned `Solid.lean` defines:

- `Condensed.finFree`;
- `Condensed.profiniteSolid`;
- `Condensed.profiniteSolidCounit`;
- `Condensed.profiniteSolidIsPointwiseRightKanExtension`;
- `Condensed.profiniteSolidification`.

Thus `(Condensed.profiniteSolid R).obj S` already has a canonical machine-level pointwise right-Kan/limit presentation from finite free condensed modules. This is formal reachability. It is **not by itself** the missing source-concordance theorem.

### P2-B — Nöbeling/Specker freeness: `AVAILABLE`

`LocallyConstant.freeOfProfinite` supplies `Module.Free ℤ (LocallyConstant S ℤ)` for profinite `S`.

### P2-C — locally-constant/discrete condensed-module interface: `AVAILABLE`

Pinned `Mathlib/Condensed/Discrete/Module.lean` supplies:

- `CondensedMod.LocallyConstant.functor`;
- `CondensedMod.LocallyConstant.functorIsoDiscrete`;
- the associated discrete/underlying adjunction interfaces.

This makes the locally constant side formally accessible inside condensed modules. It still does not identify its relevant dual/measure object with `profiniteSolid`.

### P2-D — canonical measure/dual functor: `BLOCKING`

The exact pinned tree does not expose a dedicated `Mathlib/Condensed/Measure` layer, and this audit has not located a machine-usable canonical condensed-module functor realizing the measure/dual model associated to the locally constant integer-valued functions on `S` in the form required for source concordance.

Reopening requirement: construct or identify, at the pinned universes and without axioms, a functorial condensed-module realization of the canonical measure/dual model associated to `C(S,ℤ)`, with the Hom/duality interface required downstream.

### P2-E — natural equivalence to `profiniteSolid`: `BLOCKING`

No pinned declaration has been located that composes P2-A/P2-C into a natural equivalence between `Condensed.profiniteSolid (ULift ℤ)` and the canonical measure/dual model required by the source proof.

Reopening requirement: prove a machine-replayable natural isomorphism/equivalence, with explicit universe and source-concordance accounting, from the pinned `profiniteSolid` functor to the canonical measure/dual functor supplied by P2-D.

## Product decomposition is not the canonical bridge

Nöbeling freeness makes the source's objectwise product description mathematically reachable after a basis is chosen. That chosen-basis product decomposition is noncanonical and is therefore **not** accepted as a substitute for the functorial P2-D/P2-E bridge.

A later proof may use such an objectwise product decomposition where only objectwise structure is required, but it must not manufacture naturality from a basis choice.

## Bounded absence statement

The exact pinned tree contains no `Mathlib/Condensed/Measure` subtree. This says only that no dedicated source locus of that name is present. It does not claim that relevant category theory, Hom machinery, limits, or a possible alternative construction are globally absent.

## Terminal state

`OPEN_WITH_CHARACTERIZED_BLOCKER`

CM4-P2 remains open, but its blocker is now narrowed to two compositional edges:

1. P2-D — construct/identify the canonical measure/dual condensed-module functor;
2. P2-E — prove the natural equivalence from `profiniteSolid` to that functor.

Only after both edges close may CM4-P2 be marked satisfied in parent issue #355.

## Nonclaims

This operation does not establish:

- the CM4 theorem;
- CM4-P3, P4, P5, or P6;
- the derived/complex form of Proposition 0.5.7;
- arbitrary-ring generalizations;
- broader C04;
- C06;
- `GRAPH_CERTIFIED`;
- dependency minimality or uniqueness;
- CM5;
- global CMDG completeness.
