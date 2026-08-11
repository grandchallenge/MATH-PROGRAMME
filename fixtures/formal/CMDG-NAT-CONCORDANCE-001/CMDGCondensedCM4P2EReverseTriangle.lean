import CMDGCondensedCM4P2EPointProbeRecovery

/-!
# CMDG CM4-P2-E reverse rank-one triangle

This auxiliary fixture closes the reverse triangle for the rank-one internal-Hom comparison.
The proof transports the opaque `rankOneInternalHom` object through its canonical definitional
isomorphism to the native enriched end, then uses `Limits.end_.hom_ext` to reduce equality to every
slice projection. Each projection is discharged by the certified point-probe recovery theorem.

It establishes only the objectwise reverse triangle. It does not yet package the rank-one
presheaf isomorphism or the finite P2-E natural comparison.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Limits Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

lemma rankOneInternalHom_obj_eq_enrichedHom (X : CompHaus.{u}) :
    rankOneInternalHom.obj (op X) =
      enrichedHom
        (ModuleCat.{u + 1} R)
        (Under.forget (op X) ⋙ coefficientPresheaf)
        (Under.forget (op X) ⋙ coefficientPresheaf) := by
  rfl

noncomputable def rankOneInternalHomAtIso (X : CompHaus.{u}) :
    rankOneInternalHom.obj (op X) ≅
      enrichedHom
        (ModuleCat.{u + 1} R)
        (Under.forget (op X) ⋙ coefficientPresheaf)
        (Under.forget (op X) ⋙ coefficientPresheaf) :=
  eqToIso (rankOneInternalHom_obj_eq_enrichedHom X)

lemma rankOneInternalHomAtIso_hom_projection
    (X : CompHaus.{u}) (k : Under (op X)) :
    (rankOneInternalHomAtIso X).hom ≫
        enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          k =
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op X) ⋙ coefficientPresheaf)
        (Under.forget (op X) ⋙ coefficientPresheaf)
        k := by
  rfl

lemma rankOneEvaluation_multiplication (X : CompHaus.{u}) :
    rankOneEvaluationApp X ≫ rankOneMultiplicationApp X =
      𝟙 (rankOneInternalHom.obj (op X)) := by
  rw [← cancel_mono (rankOneInternalHomAtIso X).hom]
  apply end_.hom_ext
  intro k
  change
    ((rankOneEvaluationApp X ≫ rankOneMultiplicationApp X) ≫
        (rankOneInternalHomAtIso X).hom) ≫
        enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          k =
      ((𝟙 (rankOneInternalHom.obj (op X))) ≫
        (rankOneInternalHomAtIso X).hom) ≫
        enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          (Under.forget (op X) ⋙ coefficientPresheaf)
          k
  simp only [Category.assoc, Category.id_comp,
    rankOneInternalHomAtIso_hom_projection,
    rankOneMultiplicationApp_projection]
  apply ModuleCat.hom_injective
  ext φ
  change
    rankOneMultiplicationToEndomorphism X k (rankOneEvaluationApp X φ) =
      rankOneProjectionEndomorphism X k φ
  exact (rankOneProjection_recovery X k φ).symm

#check rankOneInternalHom_obj_eq_enrichedHom
#check rankOneInternalHomAtIso
#check rankOneInternalHomAtIso_hom_projection
#check rankOneEvaluation_multiplication
#check Limits.end_.hom_ext

#print axioms rankOneInternalHom_obj_eq_enrichedHom
#print axioms rankOneInternalHomAtIso_hom_projection
#print axioms rankOneEvaluation_multiplication

end CMDG.CondensedCM4P2E.InternalHom
