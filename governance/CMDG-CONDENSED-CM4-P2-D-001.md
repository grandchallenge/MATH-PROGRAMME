# CMDG-CONDENSED-CM4-P2-D-001 — canonical measure/dual condensed-module reconstruction

Parent P2 operation: `CMDG-CONDENSED-CM4-P2-001` / issue #363  
Operation issue: #369  
Implementation PR: #371  
Protected predecessor merge: `baeee7329e12c73b422251edfb88a643108d7667`  
Implementation baseline: `fa283a283c4584c79af86fec632d50aa49e6d640`  
Implementation baseline tree: `49f644c8ff4462015833d6477dfb6fde5b847970`

## Purpose

This operation reconstructs **CM4-P2-D only**: the canonical, functorial condensed-module measure/dual model associated to locally constant integral functions on a profinite set.

The construction is basis-free. It does not identify the resulting functor with `Condensed.profiniteSolid`; that natural equivalence is the separately governed P2-E operation under issue #370 and remains dependency-blocked until P2-D is protected-admitted.

## Exact formal environment

- Lean image/toolchain: `leanprover/lean4:v4.33.0-rc1`
- Lean commit: `62eed1db4d67327ec8120be05f1a1b0847d74561`
- mathlib commit: `79d0395a1825a6264ad5d269e35e60537518955e`
- mathlib tree: `d76f5e09b832a08949f6d8ad4fb80ce30527da64`

The coefficient ring is exactly `R := ULift.{u + 1} ℤ`, matching the lifted integral coefficient realization required by the pinned condensed-module environment.

## Stage A — exact-tree duality audit

The P2 parent audit correctly established that no dedicated `Mathlib/Condensed/Measure` subtree is present. P2-D is nevertheless reconstructible from general closed-monoidal, enriched-Hom, sheaf, and locally-constant module interfaces already present in the exact pinned tree.

### A1. Locally constant/discrete module interface

`Mathlib/Condensed/Discrete/Module.lean`  
blob `b3ba358aa6b01b2de4cfedf6480ac22e863241d3`

Machine-usable declarations:

- `CondensedMod.LocallyConstant.functorToPresheaves`;
- `CondensedMod.LocallyConstant.functor`;
- `CondensedMod.LocallyConstant.functorIsoDiscrete`;
- `CondensedMod.LocallyConstant.adjunction`.

For `S : Profinite`, restriction along `profiniteToCompHaus.op` evaluates the coefficient presheaf on `S` and gives the lifted locally constant module `C(S,R)`. Composing again with `functorToPresheaves` gives its discrete condensed-module presheaf presentation.

### A2. Closed module category

`Mathlib/Algebra/Category/ModuleCat/Monoidal/Closed.lean`  
blob `119610224bb253a976b03764f4e24fd3f662dc6c`

Machine-usable declarations include the `MonoidalClosed (ModuleCat R)` instance and its Hom/internal-Hom adjunction. Thus module-valued internal Hom requires no new semantic axiom.

### A3. Enriched internal Hom of presheaves and sheaf closure

`Mathlib/CategoryTheory/Sites/Monoidal.lean`  
blob `64b111b39f9f44dcab88a7fbe60411ef5008532c`

Key declaration:

- `Presheaf.isSheaf_functorEnrichedHom`.

It proves that `functorEnrichedHom A F G` is a sheaf whenever the target `G` is a sheaf. Taking `G` to be the discrete lifted-integer coefficient sheaf therefore turns the internal dual into an actual condensed module without sheafification choices.

`Mathlib/CategoryTheory/Monoidal/Closed/FunctorCategory/Basic.lean`  
blob `6f3c9a844bc5f98ef1754263de2e2c54496356ea`

Key declarations:

- `MonoidalClosed.FunctorCategory.homEquiv`;
- `MonoidalClosed.FunctorCategory.monoidalClosed`.

These supply the closed structure and the defining natural Hom equivalence in the presheaf category.

`Mathlib/CategoryTheory/Monoidal/Closed/Basic.lean`  
blob `57dd533860e4be3957c13211f275b6f75441787c`

Key declarations:

- `MonoidalClosed.pre`;
- `MonoidalClosed.pre_id`;
- `MonoidalClosed.pre_map`;
- `MonoidalClosed.internalHom`.

These make the variance machine-explicit: a map `C(T,R) → C(S,R)` induces by precomposition a map from the dual of `C(S,R)` to the dual of `C(T,R)`.

## Stage B — canonical reconstruction

The formal fixture is:

`fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean`.

It constructs the following objects in order.

1. `coefficientPresheaf`: the discrete lifted-integer coefficient sheaf, presented by locally constant functions.
2. `continuousFunctions : Profiniteᵒᵖ ⥤ ModuleCat R`: `S ↦ C(S,R)` with pullback variance.
3. `discreteContinuousPresheaf`: the discrete condensed-module presheaf associated to `C(S,R)`.
4. `measurePresheafObj S := functorEnrichedHom (ModuleCat R) (C(S,R)_disc) R_disc`.
5. `measurePresheafObj_isSheaf`: the proof that this enriched internal Hom is already a sheaf.
6. `measurePresheafFunctor : Profinite ⥤ PresheafModule`: functoriality in `S`, induced by precomposition.
7. `measureFunctor : Profinite ⥤ CondensedMod R`: the canonical condensed-module lift.
8. `dualityHomEquiv`: the closed-monoidal universal property

   `(C(S,R)_disc ⊗ F ⟶ R_disc) ≃ (F ⟶ measurePresheafObj S)`.

No basis enters any definition or functor law.

## Variance audit

For `f : S ⟶ T` in `Profinite`:

1. pullback gives `C(T,R) ⟶ C(S,R)`;
2. the discrete locally-constant functor preserves that arrow;
3. internal Hom is contravariant in its first argument;
4. precomposition therefore gives `measure(S) ⟶ measure(T)`.

Hence `measureFunctor` is covariant `Profinite ⥤ CondensedMod R`, matching the variance required for the later P2-E comparison to `profiniteSolid`.

A variance-reversed substitute is explicitly rejected by the governed validator.

## Source concordance

Scholze's source construction defines the solid free object on a profinite set by the canonical internal dual

`ℤ[S]^□ = underline Hom(C(S,ℤ), ℤ)`,

and identifies its underlying group with the integer-valued measure group `Hom(C(S,ℤ),ℤ)`. The source obtains a product `∏_I ℤ` only after choosing a Nöbeling basis of `C(S,ℤ)`.

The P2-D fixture reconstructs exactly the basis-free internal-dual side of this description at the pinned lifted coefficient ring. It therefore supplies the canonical measure/dual model itself rather than the noncanonical product presentation.

This source-concordance statement does **not** identify the constructed functor with mathlib's right-Kan-extension `Condensed.profiniteSolid`; proving that natural identification is P2-E.

## Adversarial exclusions

The governed record and validator reject any candidate that:

- depends on a chosen Nöbeling basis;
- substitutes an objectwise product for the internal-dual functor;
- reverses the required `Profinite` variance;
- declares the P2-E equivalence available;
- claims P2 closure, CM4 certification, or any broader protected result;
- introduces `sorry`, local axioms, unsafe placeholders, or `implemented_by` in the P2-D fixture.

## Axiom/dependency reporting

The dedicated workflow builds and directly replays the P2-D fixture at the exact mathlib pin and emits declaration-level `#print axioms` output for the reconstruction and its Hom interface. P2-D admission is conditional on that replay and the repository policy/conformance checks.

## Candidate disposition

`P2_D_RECONSTRUCTED_PENDING_PROTECTED_ADMISSION`

This means the branch contains a candidate reconstruction of CM4-P2-D. It does not mean protected P2-D authority exists. Protected availability requires the exact-head review, Human Steward disposition when required, protected merge, and protected-main readback prescribed by issue #369.

## Nonclaims

This operation does not establish:

- CM4-P2-E natural equivalence with `profiniteSolid`;
- closure of `CMDG-CONDENSED-CM4-P2-001` / issue #363;
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
