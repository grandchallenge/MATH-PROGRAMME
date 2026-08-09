# CMDG-CONDENSED-CM4-001 — Stage-A characterized blocker

## Disposition

`OPEN_WITH_CHARACTERIZED_BLOCKER`

This package does **not** certify CM4. It records the exact-tree prerequisite audit required by issue #355 and freezes the theorem statement so that later dependency reconstruction cannot silently change scope.

## Protected predecessor

CM4 inherits only the protected C05 restricted `ℤ` authority:

- operation: `CMDG-SOLID-C05-001`
- issue: `#348`
- implementation PR: `#350`
- protected merge: `a480fcecf8137ac7bd29534043623d09afab0a12`
- disposition: `CMDG_SOLID_C05_001_PROTECTED_CLOSED`

The current CM4 branch is based on protected `main` commit `d9b9ed1a3a4c7ab56d25091e724fa585fbcea071`, tree `2a7bd5d53af76b6705ebd526dae667a381860374`. Intervening protected operations do not broaden C05 mathematical authority.

## Exact formal environment

- Lean: `leanprover/lean4:v4.33.0-rc1`
- Lean commit: `62eed1db4d67327ec8120be05f1a1b0847d74561`
- mathlib commit: `79d0395a1825a6264ad5d269e35e60537518955e`
- mathlib tree: `d76f5e09b832a08949f6d8ad4fb80ce30527da64`

The frozen module-level target is:

```lean
∀ S : Profinite.{u},
  CondensedMod.IsSolid (ULift.{u + 1} ℤ)
    ((Condensed.profiniteSolid (ULift.{u + 1} ℤ)).obj S)
```

`CMDGCondensedCM4Blocker.lean` type-checks this proposition and separately replays only the already available Nöbeling prerequisite. It does not assert the target.

## Exact-tree audit

### Available

1. **Nöbeling/Specker freeness.** `Mathlib/Topology/Category/Profinite/Nobeling/Induction.lean`, blob `2989eac53e537e47fd9ac93cba92d50856573173`, exposes `LocallyConstant.freeOfProfinite` for arbitrary profinite `S`.
2. **Formal solidness interface.** `Mathlib/Condensed/Solid.lean`, blob `f5214433f91ee87fc8fbe7e2746e0bd227faed2a`, exposes `Condensed.profiniteSolid`, `Condensed.profiniteSolidification`, and `CondensedMod.IsSolid`. The same file explicitly leaves the target theorem as `TODO (hard)`.
3. **Ambient condensed module category.** `Mathlib/Condensed/Module.lean`, blob `f5834efa0d5bf1289187abe3319536186d67a405`.
4. **Adjacent projectivity infrastructure.** `Mathlib/Condensed/Light/InternallyProjective.lean`, blob `91b0b495e708368b0d5f58bb2865490d18d90657`, is relevant but only analogous to the missing proof chain.

The exact pinned tree contains no dedicated `Mathlib/Condensed/Derived`, `Mathlib/Condensed/Measure`, `Mathlib/Condensed/Real`, or `Mathlib/Condensed/Circle` locus. This is a bounded subtree observation, not a claim that all relevant category theory is absent from mathlib.

## Characterized blockers and reopening requirements

### CM4-P2 — `profiniteSolid` product/measure identification

**Status:** blocking.

Reopen when a universe-correct, replayable theorem identifies `(Condensed.profiniteSolid (ULift ℤ)).obj S` with the product/measure model required by the source proof, with naturality sufficient for the `IsSolid` argument.

### CM4-P3 — profinite higher-cohomology / Ext vanishing

**Status:** blocking.

Reopen when machine-checked vanishing results for arbitrary profinite `S` with discrete integer coefficients are available in a form composable with the CM4 derived-Hom calculation.

### CM4-P4 — derived product/Hom calculation

**Status:** blocking.

Reopen when a replayable formal result establishes the required equivalent of
`RHom(∏_J ℤ, ℤ) ≃ ⊕_J ℤ`, together with the categorical bridge to the CM4 object.

### CM4-P5 — condensed `ℝ` / `ℝ/ℤ` proof machinery

**Status:** blocking.

Reopen when the source-equivalent exact-sequence / derived-Hom machinery is formalized, or when a separately certified alternative proof closes CM4-P4 and explicitly records the changed proof concordance.

### CM4-P6 — final `CondensedMod.IsSolid` witnesses

**Status:** partial blocking.

The class and solidification maps exist, but the required `IsIso` witnesses are not derivable from the current closed dependency set. Reopen after CM4-P2 through CM4-P5 close and the witnesses can be constructed without assumptions or placeholders.

## Preserved nonclaims

This package does not establish CM4, the derived/complex form of Proposition 0.5.7, arbitrary finite-type `ℤ`-algebra free-solid theorems, arbitrary commutative- or noncommutative-ring solidity, equivalence between pinned and reconstructed C05 predicates, an abelian category of solid modules, closure under limits/colimits/extensions/tensor/internal Hom, a solidification reflector, liquid mathematics, broader C04, C06, `GRAPH_CERTIFIED`, dependency minimality or uniqueness, or global CMDG completeness.

## Reopening rule

CM4 theorem certification may resume only after every blocking or partially blocking prerequisite has machine-replayable evidence, or after a separately governed alternative proof path closes the same theorem while preserving explicit source-concordance accounting.
