# CMDG-CM4 — External Mathematical Review Packet

## Purpose

This packet asks for independent mathematical review of a Lean-checked theorem closing the current mathlib TODO

```lean
((Condensed.profiniteSolid ℤ).obj S).IsSolid
```

for arbitrary profinite `S`, in the universe-correct lifted-integer formulation used by the current GCL fixture.

The request is deliberately narrower than a code review. The primary question is whether the mathematical argument embodied by the formal proof is sound, non-circular, and correctly identified with the standard solidity statement for the free solid abelian group on a profinite set.

## Exact protected result

Protected terminal merge:

`28aa80edc08833b9945380a848552cd5fb1da363`

Governed theorem:

```lean
CMDG.CondensedCM4.cm4Target_via_pointFunctional :
  CMDG.CondensedCM4.CM4Target
```

where

```lean
def CMDG.CondensedCM4.CM4Target : Prop :=
  ∀ S : Profinite.{u},
    CondensedMod.IsSolid (ULift.{u + 1} ℤ)
      ((Condensed.profiniteSolid (ULift.{u + 1} ℤ)).obj S)
```

The terminal axiom readback is:

```text
[propext, Classical.choice, Quot.sound]
```

with no `sorryAx`.

Primary proof file:

`fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3GPointFunctional.lean`

Terminal wrapper:

`fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean`

## Current mathlib comparison

Current mathlib master still contains the explicit TODO:

```text
TODO (hard): prove that ((profiniteSolid ℤ).obj S).IsSolid for S : Profinite.
```

The current `Mathlib/Condensed/Solid.lean` blob observed for this audit is:

`7700f3cba847c9a0030f5bc37bbe1dc2b6497955`.

Thus the mathematical target of this review is not merely a GCL-local milestone; it matches a currently advertised missing theorem in mathlib, modulo the standard universe lift used by the GCL fixture.

## Proof architecture

The proof does not reproduce the historical derived/cohomological source route. Instead it uses an underived Point-functional route.

The core chain is:

```text
finite Boolean / Nöbeling data
        ↓
weighted Point-measure reconstruction
        ↓
kernel product functional on integral-basis coefficients
        ↓
vanishing under solidification forces product functional = 0
        ↓
Point-functional faithfulness
        ↓
coefficient morphism = 0
        ↓
coefficient mapping-out injectivity
        ↓
coefficient object is solid
        ↓
profiniteSolid value is solid for every profinite S
```

The terminal propagation theorem is:

```lean
theorem profiniteSolid_isSolid_via_pointFunctional
    (S : Profinite.{u}) :
    CondensedMod.IsSolid R ((Condensed.profiniteSolid R).obj S)
```

for `R := ULift.{u + 1} ℤ`.

## Critical lemmas to review

The review should focus on these mathematical interfaces rather than every implementation helper.

### A. Point-measure faithfulness

```lean
measurePointProjection_zero_reflects
measurePointFunctional_zero_reflects
measurePointIntegralFunctional_zero_reflects
```

Question: does the passage from the enriched internal-Hom Point component to an ordinary integral linear functional genuinely lose no information?

### B. Weighted reconstruction

```lean
weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue
```

Question: does the weighted finite-Boolean limit reconstruct an arbitrary Point-measure section with no hidden compactness, finiteness, or choice assumption beyond those visible in the formal environment?

### C. Solidification-kernel annihilation

```lean
kernelProductFunctional_evaluationWeight_eq_zero_of_solidification_kernel
basisCombination_kernelProductFunctional_eq_zero_of_solidification_kernel
kernelProductFunctional_eq_zero_of_solidification_kernel
```

Question: is the transition from vanishing after solidification to vanishing of the full product functional mathematically legitimate and non-circular?

### D. Return from the scalar functional to the original morphism

```lean
applied_d_point_kernelProductFunctional
coefficient_eq_zero_of_solidification_kernel
coefficientMappingOutInjectivity_of_pointFunctional
```

Question: does Point-level vanishing suffice for the stated coefficient-object extensionality, and is that extensionality independent of the final solidity theorem?

### E. Final solidity propagation

```lean
coefficientObject_isSolid_via_pointFunctional
profiniteSolid_isSolid_via_pointFunctional
```

Question: do the previously established equivalences used here exactly match mathlib's current `CondensedMod.IsSolid` predicate, without smuggling in the target as an assumption?

## Explicit circularity check

A reviewer should verify that none of the following are imported or assumed upstream of the terminal theorem:

- `profiniteSolid_isSolid_via_pointFunctional`;
- `CM4Target`;
- the current mathlib TODO as an axiom or local postulate;
- a general theorem asserting solidity of `profiniteSolid ℤ`;
- any equivalent statement whose proof already uses the terminal theorem.

The GCL terminal validator and axiom readback found no such cycle, but this should be checked independently at the mathematical-architecture level.

## Scope

This review is only for the module-level integer-coefficient statement.

It does **not** claim:

- the full derived/complex form of the corresponding Clausen–Scholze source result;
- arbitrary finite-type `ℤ`-algebras;
- arbitrary commutative rings;
- the corrected general-ring notion of solid module alluded to in current mathlib's TODO note;
- C06, CM5, or global CMDG completeness.

## Requested reviewer disposition

Please return one of:

- `MATHEMATICALLY_SOUND__UPSTREAM_PORT_JUSTIFIED`
- `SOUND_WITH_REQUIRED_CLARIFICATIONS`
- `GAP_FOUND`
- `TARGET_MISIDENTIFIED`
- `REVIEW_INCONCLUSIVE`

For any disposition other than the first, identify the smallest exact lemma or interface requiring correction or explanation.

## Reviewer independence

The preferred reviewer is a condensed/solid-mathematics specialist who did not author the GCL proof and is not asked to accept any GCL governance premise. The proof should be judged as mathematics plus Lean evidence, not on programme authority.
