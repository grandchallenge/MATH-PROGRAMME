import CMDGCondensedCM4P3DerivedCM5R0GenuineSextupleRelationIso
import CMDGCondensedCM4P3DerivedCM5R0QuintupleProbeComparison

/-!
# CM5: true represented sixfold Čech probe versus split-set sixfold fibres

This is the actual categorical sixth iterated Profinite pullback, not
a substitute pointwise relation. Universe-correct type equivalence
preserves all six fibre coordinates for arbitrary Stonean test object.
-/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCompHausProbeCechSextupleUliftEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T)) ≃
      splitFreeCechSextuple
        (stoneanCompHausProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  let A := U.compHaus ⟶ profiniteToCompHaus.obj
    (Stonean.toProfinite.obj T.presentation)
  let B := U.compHaus ⟶ profiniteToCompHaus.obj T
  let R5 := U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechQuintuples T)
  let f : A → B := fun x => x ≫ profiniteToCompHaus.map p
  let e5 : R5 ≃ {q : A × (A × (A × (A × A))) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
        f q.1 = f q.2.2.2.1 ∧ f q.1 = f q.2.2.2.2} :=
    (Equiv.ulift.symm.trans
      (stoneanCompHausProbeCechQuintupleUliftEquiv T U)).trans
        ((uliftCompatibleQuintupleEquiv f).symm.trans Equiv.ulift)
  let g5 : R5 → B := fun x =>
    x ≫ profiniteToCompHaus.map
      (stoneanCechQuintupleVertexFirst T ≫ p)
  have h5 : ∀ r : R5, g5 r = f (e5 r).1.1 := by
    intro r
    rfl
  let et := compHausHomProfinitePullbackEquiv U.compHaus
    (stoneanCechQuintupleVertexFirst T ≫ p) p
  exact (Equiv.ulift.trans
    (et.trans (compatibleNestedSextupleEquiv f g5 e5 h5))).trans
      (Equiv.ulift.symm.trans (uliftCompatibleSextupleEquiv f))

#print axioms stoneanCompHausProbeCechSextupleUliftEquiv
end CMDG.CondensedCM5R0
