# CMDG-CONDENSED-CM4-P2-E-001 — comparison reconstruction audit

## Purpose

This operation is restricted to **CM4-P2-E**: construct a machine-replayable natural equivalence between the protected P2-D canonical measure/dual functor and the pinned `Condensed.profiniteSolid` functor.

The P2-D predecessor is protected authority. P2-E begins from that exact protected representation and must separately establish reconstruction.

## Programme semantic boundary — representation versus reconstruction

**P2-D — `REPRESENTATION`.** The protected predecessor constructs the canonical, basis-free, functorial measure/dual condensed-module model and its Hom/duality interface. It does not identify that model with `profiniteSolid`.

**P2-E — `RECONSTRUCTION/EQUIVALENCE`.** P2-E constructs the finite comparison, proves the protected measure functor has the required right-Kan universal property, and uses canonical right-Kan uniqueness to obtain

```lean
measureFunctor ≅ Condensed.profiniteSolid R
```

The governing rule remains: **duality does not imply reconstruction**.

The completed mathematical proof architecture is

```text
P2-D representation / duality
  → E1 finite natural comparison
  → E2 measure-side right-Kan reconstruction
  → E3 canonical right-Kan uniqueness
  → P2-E natural equivalence
```

## Protected predecessor and exact environment

- P2-D reviewed head: `358466932fde181c927cd428613f4578f38bfc1c`
- protected tree: `ac1e21d2746ad951a9aa3c747895b28f56092bf8`
- protected merge / P2-E baseline: `839e04e1b862ffddfe5ce1d4d733ba954cd45d96`
- protected P2-D replay: `31342558880` — success
- Lean: `v4.33.0-rc1`, commit `62eed1db4d67327ec8120be05f1a1b0847d74561`
- mathlib: `79d0395a1825a6264ad5d269e35e60537518955e`, tree `d76f5e09b832a08949f6d8ad4fb80ce30527da64`
- coefficient ring: `ULift.{u + 1} ℤ`

The historical Stage-A exact-tree result remains `FORMAL_ROUTE_REACHABLE_WITH_TWO_CONSTRUCTION_OBLIGATIONS`. It records the route as audited before E1/E2/E3 construction; it is not the current completion state.

## E1 — canonical finite comparison

State: `CERTIFIED`.

The terminal declaration is

```lean
finiteComparisonNatIso :
  FintypeCat.toProfinite ⋙ CMDG.CondensedCM4P2D.measureFunctor ≅
    Condensed.finFree R
```

The construction is canonical and basis-free. Exact synchronized E1 head `a7ab8c2fc26bc1c8e9d62f184d7779c8a48e14f8` replayed successfully in dedicated run `31457490712`. Declaration-level axiom dependencies are `[propext, Classical.choice, Quot.sound]`.

E1 remains frozen through E2 and E3.

## E2 — measure functor as right Kan extension

State: `CLOSED_MACHINE_CERTIFIED`.

The certified construction is complete:

```text
canonical finite-quotient colimit of the nested locally-constant source
  → opposite-category limit
  → internal-Hom limit preservation
  → explicit identification with measurePresheafFunctor
  → fully faithful sheaf/CondensedMod lift
  → Profinite.Extend.isLimitCone
  → pointwise right Kan extension
  → ordinary right Kan extension
```

The core finite-quotient/internal-Hom layer is isolated in `CMDGCondensedCM4P2EE2Core.lean`. The sheaf lift and RKE certificate are isolated in `CMDGCondensedCM4P2EE2.lean`.

Material declarations include:

- `discreteContinuousPresheafIsColimit`;
- `measurePresheafInternalHomNatIso`;
- `finiteQuotientMeasureConeIso`;
- `measurePresheafFunctorMapConeIsLimit`;
- `measureFunctorMapConeIsLimit`;
- `measureFunctorStructuredArrowIsLimit`;
- `measureRightExtensionIsPointwise`;
- `measureFunctorIsRightKanExtension`.

Exact synchronized E2 proof head:

`eefb8f3495018038047361c2cac2924a083f354a`

Dedicated P2-E run:

`31493933246` — **SUCCESS**

The E2 declarations retain the standard admitted axiom footprint `[propext, Classical.choice, Quot.sound]`; no `sorry`, local axiom, Nöbeling basis, or objectwise-only substitute is admitted.

E2 certifies the protected `measureFunctor` as a right Kan extension of `Condensed.finFree R` along `FintypeCat.toProfinite`, using the certified E1 comparison as counit.

## E3 — canonical uniqueness

State: `CLOSED_MACHINE_CERTIFIED`.

E3 is isolated in `CMDGCondensedCM4P2EE3.lean`. It performs the exact terminal comparison rather than deriving equivalence from the P2-D duality statement.

The certified route is:

```text
Condensed.profiniteSolidIsPointwiseRightKanExtension
  → IsPointwiseRightKanExtension.isRightKanExtension
  → pinned profiniteSolid right-Kan certificate over Condensed.finFree R

certified E1 finiteComparisonNatIso.hom
  + certified E2 measureFunctorIsRightKanExtension
  → measureFunctor right-Kan certificate over the same Condensed.finFree R

same finite source after E1 alignment
  → rightKanExtensionUniqueOfIso with Iso.refl (Condensed.finFree R)
  → rightKanExtensionUnique
  → measureFunctor ≅ Condensed.profiniteSolid R
```

The identity source isomorphism in `rightKanExtensionUniqueOfIso` is legitimate precisely because E2 already uses the certified E1 map

```lean
finiteComparisonNatIso.hom :
  FintypeCat.toProfinite ⋙ measureFunctor ⟶ Condensed.finFree R
```

as its right-extension counit. The identity therefore occurs **after** E1 alignment; it is not a substitute for that alignment.

Terminal declarations:

```lean
measureProfiniteSolidNatIsoOfIso :
  CMDG.CondensedCM4P2D.measureFunctor ≅ Condensed.profiniteSolid R

measureProfiniteSolidNatIso :
  CMDG.CondensedCM4P2D.measureFunctor ≅ Condensed.profiniteSolid R
```

Exact synchronized E3 proof head:

`58e4aaf77e9965dbb2552376a7433ba4ccfc8657`

Dedicated P2-E run:

`31542402818` — **SUCCESS**

Both the governed-state job and the formal replay job succeeded. The formal job pinned the exact Lean/mathlib environment, verified the Kan-extension declarations, rejected `sorry`, local axioms, and chosen-basis substitution, and replayed `CMDGCondensedCM4P2EE3.lean`.

All E3 terminal declarations report only `[propext, Classical.choice, Quot.sound]` under `#print axioms`.

E3 therefore establishes the mathematical P2-E natural equivalence target.

## Current disposition

`P2_E_NATURAL_EQUIVALENCE_ESTABLISHED_PENDING_PROTECTED_ADMISSION`

E1, E2, and E3 are machine-certified, and the terminal natural equivalence is established. This changes the mathematical candidate state but does **not** establish protected P2-E availability. Protected admission remains a separate governance transition.

## Explicit nonclaims

This stage does **not** establish protected P2-E availability or any of the following broader claims:

- closure of parent P2 issue #363;
- CM4 theorem certification (#355);
- P3, P4, P5, or P6;
- the derived/complex form of Proposition 0.5.7;
- arbitrary-ring generalization;
- broader C04 or discharge of C06;
- `GRAPH_CERTIFIED`;
- dependency minimality or uniqueness;
- CM5;
- global CMDG completeness.

The next distinct boundary is protected admission of the now-certified P2-E candidate. No parent-P2 or broader CM4 authority is created by E3 itself.
