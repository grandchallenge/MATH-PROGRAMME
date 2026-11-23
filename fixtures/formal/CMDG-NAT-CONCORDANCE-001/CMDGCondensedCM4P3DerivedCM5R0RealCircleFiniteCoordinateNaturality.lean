import CMDGCondensedCM4P3DerivedCM5R0RealCircleDerivedTriangle

/-!
# CMDG CM5: naturality of actual condensed short exact real/circle sequence

Against protected-merged source PR#3643, reindexing sigma : J → I
acts contravariantly on the topological coefficient products.
Prove the actual continuous additive coordinate-pullback map,
both commuting algebraic squares, and composition of induced
CondensedAb morphisms. Construct all three real/integer/circle
coordinate maps IN CondensedAb, prove their naturality squares,
and form a morphism of the actual ShortComplex objects.

Finally use the standard derived localization and canonical
ShortExact.singleTriangle.map to give the induced morphism
between the REAL distinguished triangles, including its
connecting-morphism compatibility by construction.

This is not an identification of an internal derived Hom or
an equality with the canonical solidification unit.
-/

noncomputable section
universe u
attribute [local instance] HasDerivedCategory.standard
open CategoryTheory
namespace CMDG.CondensedCM5R0.RealCircleFiniteCoordinateNaturality

open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf

variable (I J : Type u)

def reindexTopHom (M : Type) [TopologicalSpace M]
    [AddCommGroup M] [IsTopologicalAddGroup M] (σ : J → I) :
    ULift.{u+1,u} (I → M) →+ ULift.{u+1,u} (J → M) where
  toFun x := ⟨fun j => x.down (σ j)⟩
  map_zero' := by
    ext j
    rfl
  map_add' x y := by
    ext j
    rfl

theorem reindexTopHom_continuous (M : Type) [TopologicalSpace M]
    [AddCommGroup M] [IsTopologicalAddGroup M] (σ : J → I) :
    Continuous (reindexTopHom I J M σ :
      ULift.{u+1,u} (I → M) → ULift.{u+1,u} (J → M)) := by
  apply continuous_uliftUp.comp
  apply continuous_pi
  intro j
  exact (continuous_apply (σ j)).comp continuous_uliftDown

theorem int_reindex_naturality (σ : J → I) :
    (reindexTopHom I J ℝ σ).comp (intProductTopHom I) =
      (intProductTopHom J).comp (reindexTopHom I J ℤ σ) := by
  apply AddMonoidHom.ext
  intro x
  apply ULift.ext
  funext j
  rfl

theorem circle_reindex_naturality (σ : J → I) :
    (reindexTopHom I J UnitAddCircle σ).comp (realProductTopHom I) =
      (realProductTopHom J).comp (reindexTopHom I J ℝ σ) := by
  apply AddMonoidHom.ext
  intro x
  apply ULift.ext
  funext j
  rfl

theorem condensedGroupMap_comp (M N K : Type (u+1))
    [TopologicalSpace M] [AddCommGroup M] [IsTopologicalAddGroup M]
    [TopologicalSpace N] [AddCommGroup N] [IsTopologicalAddGroup N]
    [TopologicalSpace K] [AddCommGroup K] [IsTopologicalAddGroup K]
    (f : M →+ N) (hf : Continuous (f : M → N))
    (g : N →+ K) (hg : Continuous (g : N → K)) :
    condensedGroupMap M f hf ≫ condensedGroupMap N g hg =
      condensedGroupMap M (g.comp f) (hg.comp hf) := by
  letI : CategoryTheory.Limits.HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    CategoryTheory.Limits.hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  change ((Condensed.StoneanCompHaus.equivalence
    (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor).map
      (stoneanSheafMap M f hf) ≫
    ((Condensed.StoneanCompHaus.equivalence
      (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor).map
      (stoneanSheafMap N g hg) =
    ((Condensed.StoneanCompHaus.equivalence
      (ModuleCat.{u+1} (ULift.{u+1} ℤ))).functor).map
      (stoneanSheafMap M (g.comp f) (hg.comp hf))
  rw [← Functor.map_comp]
  rfl

#print axioms condensedGroupMap_comp

local instance (X : Type u) :
    IsTopologicalAddGroup (ULift.{u+1,u} (X → UnitAddCircle)) := ⟨⟩

noncomputable def integerReindex (σ : J → I) :
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → ℤ)) ⟶
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (J → ℤ)) :=
  condensedGroupMap (ULift.{u+1,u} (I → ℤ))
    (reindexTopHom I J ℤ σ)
    (reindexTopHom_continuous I J ℤ σ)

noncomputable def realReindex (σ : J → I) :
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → ℝ)) ⟶
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (J → ℝ)) :=
  condensedGroupMap (ULift.{u+1,u} (I → ℝ))
    (reindexTopHom I J ℝ σ)
    (reindexTopHom_continuous I J ℝ σ)

noncomputable def circleReindex (σ : J → I) :
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → UnitAddCircle)) ⟶
    condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (J → UnitAddCircle)) :=
  condensedGroupMap (ULift.{u+1,u} (I → UnitAddCircle))
    (reindexTopHom I J UnitAddCircle σ)
    (reindexTopHom_continuous I J UnitAddCircle σ)

theorem condensed_integer_reindex_square (σ : J → I) :
    condensedIntegerToReal I ≫ realReindex I J σ =
    integerReindex I J σ ≫ condensedIntegerToReal J := by
  unfold condensedIntegerToReal realReindex integerReindex
  rw [condensedGroupMap_comp, condensedGroupMap_comp]
  congr 1

theorem condensed_circle_reindex_square (σ : J → I) :
    condensedRealToCircle I ≫ circleReindex I J σ =
    realReindex I J σ ≫ condensedRealToCircle J := by
  unfold condensedRealToCircle circleReindex realReindex
  rw [condensedGroupMap_comp, condensedGroupMap_comp]
  congr 1

noncomputable def realCircleSequenceReindex (σ : J → I) :
    (realCircleCondensedSequence I) ⟶ (realCircleCondensedSequence J) where
  τ₁ := integerReindex I J σ
  τ₂ := realReindex I J σ
  τ₃ := circleReindex I J σ
  comm₁₂ := (condensed_integer_reindex_square I J σ).symm
  comm₂₃ := (condensed_circle_reindex_square I J σ).symm

noncomputable def realCircleTriangleReindex (σ : J → I) :
    (CMDG.CondensedCM5R0.RealCircleSheafExact.realCircleCondensedSequence_shortExact I).singleTriangle ⟶
    (CMDG.CondensedCM5R0.RealCircleSheafExact.realCircleCondensedSequence_shortExact J).singleTriangle :=
  ShortComplex.ShortExact.singleTriangle.map
    (CMDG.CondensedCM5R0.RealCircleSheafExact.realCircleCondensedSequence_shortExact I)
    (CMDG.CondensedCM5R0.RealCircleSheafExact.realCircleCondensedSequence_shortExact J)
    (realCircleSequenceReindex I J σ)

#print axioms realCircleTriangleReindex

#print axioms realCircleSequenceReindex

#print axioms condensed_integer_reindex_square
#print axioms condensed_circle_reindex_square

#print axioms int_reindex_naturality
#print axioms circle_reindex_naturality
end CMDG.CondensedCM5R0.RealCircleFiniteCoordinateNaturality
