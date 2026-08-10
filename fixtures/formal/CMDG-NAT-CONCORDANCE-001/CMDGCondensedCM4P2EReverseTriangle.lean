import CMDGCondensedCM4P2EPointProbeRecovery

/-!
# CMDG CM4-P2-E reverse rank-one triangle

This auxiliary fixture closes the reverse triangle for the rank-one internal-Hom comparison.
The proof uses `Limits.end_.hom_ext` to reduce equality in the enriched end to equality after every
slice projection, then discharges each projection with the certified point-probe recovery theorem.

It establishes only the objectwise reverse triangle. It does not yet package the rank-one
presheaf isomorphism or the finite P2-E natural comparison.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Limits Opposite
open CategoryTheory.Enriched.FunctorCategory

lemma rankOneEvaluation_multiplication (X : CompHaus.{u}) :
    rankOneEvaluationApp X ≫ rankOneMultiplicationApp X =
      𝟙 (rankOneInternalHom.obj (op X)) := by
  rw [rankOneInternalHom_eq_functorEnrichedHom]
  apply end_.hom_ext
  intro k
  rw [Category.assoc, rankOneMultiplicationApp_projection, Category.id_comp]
  apply ModuleCat.hom_injective
  ext φ
  change
    rankOneMultiplicationToEndomorphism X k (rankOneEvaluationApp X φ) =
      rankOneProjectionEndomorphism X k φ
  exact (rankOneProjection_recovery X k φ).symm

#check rankOneEvaluation_multiplication
#check Limits.end_.hom_ext

#print axioms rankOneEvaluation_multiplication

end CMDG.CondensedCM4P2E.InternalHom
