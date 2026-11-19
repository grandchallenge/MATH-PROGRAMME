# CMDG CM5-R0 — genuine profinite Čech relations in all degrees

**Status:** FORMAL SOURCE CANDIDATE. Lean 4.33.0-rc1 local source replay passed; **protected exact-head CI, native merge-group admission, external independent MATHCERT and derived-solid comparison remain separate gates**.

## Theorem actually formalized

For arbitrary profinite spaces `P,T`, morphism `p : P ⟶ T` (surjective or not), and every natural number `n`, let `R_(n+1)(P/T)` be the **actual closed subspace** of `P^(n+1)` consisting of tuples with equal `p`-images. The continuous deletion maps yield an honest, *unnormalized* Čech differential

`d_n : C(R_(n+1), ℤ) → C(R_(n+2), ℤ)`

where `C(-,ℤ)` denotes `LocallyConstant _ ℤ`. The new formal results establish:

1. `uniformProfiniteRelationDifferential_sq_zero`: `d_(n+1) ∘ d_n = 0` on true closed relations, uniformly in `n`.
2. `uniformProfiniteRelationAllPositive_cocycle_coboundary`: for each `n`, every cocycle in degree `n+1` is the differential of an actual degree-`n` locally constant cochain on `R_(n+1)`. In other words **all positive-degree scalar relation cohomology groups vanish**.
3. `uniformProfiniteRelationAllPositive_product_family`: any arbitrary collection of scalar relation cocycles admits a collection of primitives, chosen coordinatewise, **without a common finite clopen observation across coefficient coordinates**.

Tuple indices include all orders and repetitions. There is no assumed section of `p`, no finite hypothesis on `P,T`, and no degree-specific numeric surrogate.

## Mechanism and dependency closure

- Protected `CMDGCondensedCM4P3DerivedCM5R0AllArityClosedCechRelation.lean`: every finite-arity equal-image relation is closed and every scalar relation cochain extends to its full tuple product.
- `CMDGCondensedCM4P3DerivedCM5R0UniformBivariateFiniteObservation.lean`: heterogeneous compact-profinite finite clopen-rectangle decomposition.
- `CMDGCondensedCM4P3DerivedCM5R0UniformArityFiniteObservation.lean`: inductively extract **one** finite coordinate observation from an arbitrary-arity locally constant ambient cochain, including empty spaces.
- `CMDGCondensedCM4P3DerivedCM5R0UniformRelationFiniteObservation.lean`: form closed subsets `E_j=p(q^{-1}(j))` of `T`, descend cocycle identities by choosing lifts at each target point, invoke degree-uniform finite closed-family acyclicity and **continuously reassemble** the primitive on the true related tuples.
- `CMDGCondensedCM4P3DerivedCM5R0UniformProfiniteRelationComplex.lean`: actual continuous deletion maps and degree-uniform scalar relation exactness; arbitrary coordinatewise products.
- `CMDGCondensedCM4P3DerivedCM5R0UniformProfiniteRelationDsq.lean`: squared differential by ambient extension, true face naturality, and the all-tuple simplicial identity.

The finite closed-family all-positive theorem is sourced from the separately submitted `CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechAllPositive.lean`; exact-byte copies of still-unmerged prerequisite modules are staged on this candidate branch for independent compiler replay. Once upstream is protected-merged, only the newly proved relation modules constitute a material increment.

All locally compiled public theorems report `#print axioms` contained in `[propext, Classical.choice, Quot.sound]`; no new `axiom`, `sorry`, or `admit` is used.

## Outstanding obligations — not implied by these theorems

The scalar complex result does **not** itself identify the categorical `Hom(F_{R_k},A)` complex with these locally constant functions at every degree. Prove the **degree-uniform genuine free-condensed/free-solid Hom identifications**, all face-naturalities, compatibility with the actual product coefficient object, and exactness/epimorphism of the corresponding relation morphisms at every probe. Establish the necessary categorical Ext computation, dimension-shifting and source-compatible derived mapping comparison. Separately validate all source semantics and independent MATHCERT authority before any public mathematical certification.

**Disposition:** ALL_POSITIVE_GENUINE_SCALAR_RELATION_ACYCLICITY_LOCAL_LEAN_VERIFIED__PROTECTED_AND_CATEGORICAL_BRIDGES_PENDING.
