import CMDGCondensedCM4P3DerivedCM5R0GSDiscreteCoproduct
import CMDGCondensedCM4P2ERankOneNaturalIso
import Mathlib.Topology.LocallyConstant.Algebra

/-!
# CMDG CM5: compact test-space support and the actual rank-one enriched dual

This successor isolates two substantive inputs for the unproved comparison
between the enriched internal Hom of the Nöbeling discrete sum and a
categorical product of discrete coefficient sheaves.

A locally constant function from any compact Hausdorff X into an arbitrary
Finsupp module has a uniform finite set of nonzero basis coordinates:
compactness gives a finite image, and each image has finite support.
The conclusion is uniform in x, but not uniform in X. It therefore does
not incorrectly identify the categorical product with a discrete product.

The already protected rank-one internal-Hom *presheaf* natural isomorphism
is lifted into the actual condensed-module category, preserving its genuine
enriched-end semantics.

Neither lemma asserts the presheaf coproduct universal property for the
infinite Nöbeling sum or the full enriched-Hom-to-product isomorphism.
-/

noncomputable section

universe u

open CategoryTheory Limits
open CategoryTheory.Enriched.FunctorCategory

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

/-- Every locally constant map from a compact Hausdorff test X into an
arbitrary (possibly infinitely indexed) algebraic direct sum has one
finite support that works simultaneously at every point of X. -/
theorem gsLocallyConstantFinsupp_uniformSupport
    (X : CompHaus.{u}) (I : Type (u + 1))
    (f : LocallyConstant X (I →₀ R.{u})) :
    ∃ s : Finset I, ∀ (x : X) (i : I), i ∉ s → f x i = 0 := by
  classical
  refine ⟨(f.range_finite.toFinset).biUnion (fun v => v.support), ?_⟩
  intro x i hi
  have hx : f x ∈ f.range_finite.toFinset := by
    simp only [Set.Finite.mem_toFinset, Set.mem_range]
    exact ⟨x, rfl⟩
  have hnot : i ∉ (f x).support := by
    intro hmem
    exact hi (Finset.mem_biUnion.mpr ⟨f x, hx, hmem⟩)
  exact Finsupp.notMem_support_iff.mp hnot

/-- A section of the discrete direct sum has finitely many nonzero
locally-constant coordinate sections on each compact Hausdorff test.
The finite set may depend on the test and the section. -/
theorem gsLocallyConstantFinsupp_coordinatesFinite
    (X : CompHaus.{u}) (I : Type (u + 1))
    (f : LocallyConstant X (I →₀ R.{u})) :
    ∃ s : Finset I, ∀ i ∉ s,
      LocallyConstant.map (fun a : I →₀ R.{u} => a i) f = 0 := by
  obtain ⟨s, hs⟩ := gsLocallyConstantFinsupp_uniformSupport X I f
  refine ⟨s, ?_⟩
  intro i hi
  ext x
  change f x i = (0 : R.{u})
  exact hs x i hi

/-- Package the coordinate sections into an *actual* finitely supported
family. The finite-support witness comes from compactness and is not
assumed from the start. -/
noncomputable def gsLocallyConstantFinsupp_coordinateFamily
    (X : CompHaus.{u}) (I : Type (u + 1))
    (f : LocallyConstant X (I →₀ R.{u})) :
    I →₀ LocallyConstant X R.{u} := by
  classical
  obtain ⟨s, hs⟩ := gsLocallyConstantFinsupp_coordinatesFinite X I f
  exact Finsupp.onFinset s
    (fun i => LocallyConstant.map (fun a : I →₀ R.{u} => a i) f)
    (by
      intro i hne
      by_contra hi
      exact hne (hs i hi))

@[simp]
theorem gsLocallyConstantFinsupp_coordinateFamily_apply
    (X : CompHaus.{u}) (I : Type (u + 1))
    (f : LocallyConstant X (I →₀ R.{u}))
    (i : I) (x : X) :
    gsLocallyConstantFinsupp_coordinateFamily X I f i x = f x i := by
  simp [gsLocallyConstantFinsupp_coordinateFamily, LocallyConstant.map_apply]

/-- The coordinate extraction is genuinely R-linear, for arbitrary
infinite basis index sets. -/
noncomputable def gsLocallyConstantFinsupp_coordinateLinear
    (X : CompHaus.{u}) (I : Type (u + 1)) :
    LocallyConstant X (I →₀ R.{u}) →ₗ[R.{u}]
      (I →₀ LocallyConstant X R.{u}) where
  toFun := gsLocallyConstantFinsupp_coordinateFamily X I
  map_add' := by
    intro f g
    ext i x
    simp only [gsLocallyConstantFinsupp_coordinateFamily_apply]
    rfl
  map_smul' := by
    intro a f
    ext i x
    simp only [gsLocallyConstantFinsupp_coordinateFamily_apply]
    rfl

/-- No information is lost when passing to all compact-test coordinate
sections of the algebraic discrete sum. -/
theorem gsLocallyConstantFinsupp_coordinateLinear_injective
    (X : CompHaus.{u}) (I : Type (u + 1)) :
    Function.Injective (gsLocallyConstantFinsupp_coordinateLinear X I) := by
  intro f g h
  ext x i
  have hi := congrArg (fun k : I →₀ LocallyConstant X R.{u} => k i x) h
  simpa only [gsLocallyConstantFinsupp_coordinateLinear,
    gsLocallyConstantFinsupp_coordinateFamily_apply] using hi

/-- The coefficient sheaf's actual enriched rank-one internal Hom. -/
noncomputable def gsRankOneInternalHomCondensed :
    CondensedMod.{u} R.{u} :=
  ⟨CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom,
    by
      change Presheaf.IsSheaf (coherentTopology CompHaus.{u})
        (functorEnrichedHom (ModuleCat.{u + 1} R.{u})
          CMDG.CondensedCM4P2D.coefficientPresheaf
          CMDG.CondensedCM4P2D.coefficientPresheaf)
      apply Presheaf.isSheaf_functorEnrichedHom
      exact ((CondensedMod.LocallyConstant.functor R.{u}).obj
        (ModuleCat.of R.{u} R.{u})).2⟩

/-- The already certified rank-one natural isomorphism is lifted from
the exact presheaf category into CondensedMod, with no objectwise
substitute for enriched internal Hom. -/
noncomputable def gsRankOneInternalHomCondensedIso :
    gsRankOneInternalHomCondensed.{u} ≅ discreteIntegerCoeff.{u} :=
  ObjectProperty.isoMk
    (Presheaf.IsSheaf (coherentTopology CompHaus.{u}))
    CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso

#check gsLocallyConstantFinsupp_uniformSupport
#check gsLocallyConstantFinsupp_coordinatesFinite
#check gsLocallyConstantFinsupp_coordinateFamily
#check gsLocallyConstantFinsupp_coordinateLinear
#check gsLocallyConstantFinsupp_coordinateLinear_injective
#check gsRankOneInternalHomCondensed
#check gsRankOneInternalHomCondensedIso

#print axioms gsLocallyConstantFinsupp_uniformSupport
#print axioms gsLocallyConstantFinsupp_coordinatesFinite
#print axioms gsLocallyConstantFinsupp_coordinateFamily
#print axioms gsLocallyConstantFinsupp_coordinateLinear
#print axioms gsLocallyConstantFinsupp_coordinateLinear_injective
#print axioms gsRankOneInternalHomCondensed
#print axioms gsRankOneInternalHomCondensedIso

end CMDG.CondensedCM5R0
