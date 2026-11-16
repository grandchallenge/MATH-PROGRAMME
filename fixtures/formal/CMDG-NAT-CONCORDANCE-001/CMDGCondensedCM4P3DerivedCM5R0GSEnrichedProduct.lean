import CMDGCondensedCM4P3DerivedCM5R0GSPresheafCoproduct
import CMDGCondensedCM4P3DerivedCM5R0GSEnrichedCoordinates
import Mathlib.CategoryTheory.Monoidal.Closed.Braided
import Mathlib.CategoryTheory.Limits.Shapes.Opposites.Products

/-!
# CMDG CM5: enriched internal Hom of the actual source is a product

The exact Nöbeling source PRESHEAF coproduct was admitted in PR #3389.
In the braided monoidal closed presheaf category, the contravariant
first-variable internal-Hom functor at the fixed coefficient target
preserves limits of the opposite category. Applying this theorem to
the opposite of the real rank-one inclusion cocone produces a limit
fan whose legs are the precomposition maps used by the protected
canonical G_S coordinates.

Transport the rank-one internal-Hom presheaf natural isomorphism
to the coefficient-presheaf family, prove the resulting cone is
limiting, and exhibit its unique product comparison isomorphism.

This file does not yet identify the *CondensedMod* product map for
the actual free-solid target or assert its Ext¹ consequence.
-/

noncomputable section

universe u

open CategoryTheory Limits Opposite
open scoped CategoryTheory.MonoidalClosed

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

noncomputable local instance : MonoidalClosed
    CMDG.CondensedCM4P2D.PresheafModule.{u} :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- The cone of genuine first-variable enriched-Hom precomposition maps
along the exact coefficient-to-basis inclusion presheaf morphisms. -/
noncomputable def gsBasisEnrichedRankOneFan
    (S : Profinite.{u}) :
    Fan (fun _ : LiftedSourceBasisIndex S =>
      CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.{u}) :=
  Fan.mk (gsBasisInternalHomPresheaf S)
    (fun i => (MonoidalClosed.pre
      (gsBasisCoefficientInclusionPresheaf S i)).app
        CMDG.CondensedCM4P2D.coefficientPresheaf.{u})

/-- The actual enriched-Hom cone is limiting, rather than merely
jointly injective: internal Hom in its first variable sends the
protected source-presheaf coproduct cocone to a product fan. -/
noncomputable def gsBasisEnrichedRankOneFanIsLimit
    (S : Profinite.{u}) :
    IsLimit (gsBasisEnrichedRankOneFan S) := by
  let F : (CMDG.CondensedCM4P2D.PresheafModule.{u})ᵒᵖ ⥤
      CMDG.CondensedCM4P2D.PresheafModule.{u} :=
    MonoidalClosed.internalHom.flip.obj
      CMDG.CondensedCM4P2D.coefficientPresheaf.{u}
  let e :
      Discrete.functor
        (fun _ : LiftedSourceBasisIndex S =>
          op CMDG.CondensedCM4P2D.coefficientPresheaf.{u}) ⋙ F ≅
      Discrete.functor
        (fun _ : LiftedSourceBasisIndex S =>
          CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.{u}) :=
    Discrete.natIso (fun _ => Iso.refl _)
  have h : IsLimit (F.mapCone
      (gsBasisDiscreteSourcePresheafCofan S).op) :=
    isLimitOfPreserves F
      (Cofan.IsColimit.op
        (gsBasisDiscreteSourcePresheafCofanIsColimit S))
  have h' : IsLimit
      ((Cone.postcompose e.hom).obj
        (F.mapCone (gsBasisDiscreteSourcePresheafCofan S).op)) :=
    (IsLimit.postcomposeHomEquiv e
      (F.mapCone (gsBasisDiscreteSourcePresheafCofan S).op)).symm h
  exact IsLimit.ofIsoLimit h'
    (Cone.ext (Iso.refl _) (fun ⟨i⟩ => by
      rfl))

/-- Canonical product identification for the genuine enriched source
with the unconverted rank-one internal-Hom presheaves. -/
noncomputable instance gsBasisEnrichedRankOneHasProduct
    (S : Profinite.{u}) :
    HasProduct (fun _ : LiftedSourceBasisIndex S =>
      CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.{u}) :=
  HasLimit.mk ⟨gsBasisEnrichedRankOneFan S,
    gsBasisEnrichedRankOneFanIsLimit S⟩

noncomputable def gsBasisEnrichedToRankOneProductIso
    (S : Profinite.{u}) :
    gsBasisInternalHomPresheaf S ≅
      (∏ᶜ (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.{u})) :=
  (gsBasisEnrichedRankOneFanIsLimit S).conePointUniqueUpToIso
    (limit.isLimit (Discrete.functor
      (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.{u})))

/-- The target of the already protected coordinate maps is the
actual coefficient presheaf, through the previously proved rank-one
enriched-Hom natural isomorphism. -/
noncomputable def gsBasisEnrichedCoefficientFan
    (S : Profinite.{u}) :
    Fan (fun _ : LiftedSourceBasisIndex S =>
      CMDG.CondensedCM4P2D.coefficientPresheaf.{u}) :=
  Fan.mk (gsBasisInternalHomPresheaf S)
    (gsBasisEnrichedCoordinatePresheaf S)

/-- The coefficient coordinate fan is limiting in the presheaf
category, including the full presheaf-level universal property.
No passage to ordinary algebraic duals is used. -/
noncomputable def gsBasisEnrichedCoefficientFanIsLimit
    (S : Profinite.{u}) :
    IsLimit (gsBasisEnrichedCoefficientFan S) := by
  let e : Discrete.functor
      (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.{u}) ≅
      Discrete.functor
      (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf.{u}) :=
    Discrete.natIso
      (fun _ => CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso)
  have h :
      IsLimit ((Cone.postcompose e.hom).obj
        (gsBasisEnrichedRankOneFan S)) :=
    (IsLimit.postcomposeHomEquiv e
      (gsBasisEnrichedRankOneFan S)).symm
        (gsBasisEnrichedRankOneFanIsLimit S)
  exact IsLimit.ofIsoLimit h
    (Cone.ext (Iso.refl _) (fun ⟨i⟩ => rfl))

/-- Real enriched-Hom-to-product comparison on the exact underlying
presheaves used to construct G_S. -/
noncomputable def gsBasisEnrichedToCoefficientProductPresheafIso
    (S : Profinite.{u}) :
    gsBasisInternalHomPresheaf S ≅
      (∏ᶜ (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf.{u})) :=
  (gsBasisEnrichedCoefficientFanIsLimit S).conePointUniqueUpToIso
    (limit.isLimit (Discrete.functor
      (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf.{u})))

/-- Each projection of the genuine product is the exact existing
enriched coordinate of the actual basis-internal-Hom presheaf. -/
@[simp]
theorem gsBasisEnrichedToCoefficientProductPresheafIso_projection
    (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    (gsBasisEnrichedToCoefficientProductPresheafIso S).hom ≫
      Pi.π (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf.{u}) i =
      gsBasisEnrichedCoordinatePresheaf S i := by
  exact (gsBasisEnrichedCoefficientFanIsLimit S).conePointUniqueUpToIso_hom_comp
    (limit.isLimit (Discrete.functor
      (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf.{u}))) (Discrete.mk i)

#check gsBasisEnrichedRankOneFan
#check gsBasisEnrichedRankOneFanIsLimit
#check gsBasisEnrichedRankOneHasProduct
#check gsBasisEnrichedToRankOneProductIso
#check gsBasisEnrichedCoefficientFan
#check gsBasisEnrichedCoefficientFanIsLimit
#check gsBasisEnrichedToCoefficientProductPresheafIso
#check gsBasisEnrichedToCoefficientProductPresheafIso_projection

#print axioms gsBasisEnrichedRankOneFanIsLimit
#print axioms gsBasisEnrichedToRankOneProductIso
#print axioms gsBasisEnrichedCoefficientFanIsLimit
#print axioms gsBasisEnrichedToCoefficientProductPresheafIso
#print axioms gsBasisEnrichedToCoefficientProductPresheafIso_projection

end CMDG.CondensedCM5R0
