import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeThree
import CMDGCondensedCM4P3DerivedCM5R0QuadrupleProbeComparison

/-!
# CM5: compatible nested five-point set comparison

Construct the universe-correct combinatorial equivalences required
for genuine represented fifth Čech probe comparison. This file does
not claim sheafified epi or Ext⁴ vanishing.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- The fivefold compatible tuple is canonically the next nested
pullback after the compatible fourfold tuple. -/
def compatibleNestedQuintupleEquiv {A B R : Type u}
    (f : A → B) (g : R → B)
    (e : R ≃ {q : A × (A × (A × A)) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧ f q.1 = f q.2.2.2})
    (h : ∀ r, g r = f (e r).1.1) :
    {rv : R × A // g rv.1 = f rv.2} ≃
    {q : A × (A × (A × (A × A))) //
      f q.1 = f q.2.1 ∧
      f q.1 = f q.2.2.1 ∧
      f q.1 = f q.2.2.2.1 ∧
      f q.1 = f q.2.2.2.2} where
  toFun z :=
    ⟨((e z.1.1).1.1,
      ((e z.1.1).1.2.1,
        ((e z.1.1).1.2.2.1, ((e z.1.1).1.2.2.2, z.1.2)))),
      ⟨(e z.1.1).2.1, (e z.1.1).2.2.1,
        (e z.1.1).2.2.2, (h z.1.1).symm.trans z.2⟩⟩
  invFun z := by
    let q4 : {q : A × (A × (A × A)) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
        f q.1 = f q.2.2.2} :=
      ⟨(z.1.1,(z.1.2.1,(z.1.2.2.1,z.1.2.2.2.1))),
        ⟨z.2.1,z.2.2.1,z.2.2.2.1⟩⟩
    refine ⟨(e.symm q4,z.1.2.2.2.2), ?_⟩
    have hr : g (e.symm q4) = f z.1.1 := by
      simpa [q4] using h (e.symm q4)
    exact hr.trans z.2.2.2.2
  left_inv := by
    intro z
    apply Subtype.ext
    apply Prod.ext
    · change e.symm (e z.1.1) = z.1.1
      exact e.symm_apply_apply _
    · rfl
  right_inv := by
    intro z
    apply Subtype.ext
    apply Prod.ext
    · change (e (e.symm
        (⟨(z.1.1,(z.1.2.1,(z.1.2.2.1,z.1.2.2.2.1))),
          ⟨z.2.1,z.2.2.1,z.2.2.2.1⟩⟩ :
          {q : A × (A × (A × A)) //
            f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
              f q.1 = f q.2.2.2}))).1.1 = z.1.1
      simp only [Equiv.apply_symm_apply]
    · apply Prod.ext
      · change (e (e.symm
          (⟨(z.1.1,(z.1.2.1,(z.1.2.2.1,z.1.2.2.2.1))),
            ⟨z.2.1,z.2.2.1,z.2.2.2.1⟩⟩ :
            {q : A × (A × (A × A)) //
              f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
                f q.1 = f q.2.2.2}))).1.2.1 = z.1.2.1
        simp only [Equiv.apply_symm_apply]
      · apply Prod.ext
        · change (e (e.symm
            (⟨(z.1.1,(z.1.2.1,(z.1.2.2.1,z.1.2.2.2.1))),
              ⟨z.2.1,z.2.2.1,z.2.2.2.1⟩⟩ :
              {q : A × (A × (A × A)) //
                f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
                  f q.1 = f q.2.2.2}))).1.2.2.1 = z.1.2.2.1
          simp only [Equiv.apply_symm_apply]
        · apply Prod.ext
          · change (e (e.symm
              (⟨(z.1.1,(z.1.2.1,(z.1.2.2.1,z.1.2.2.2.1))),
                ⟨z.2.1,z.2.2.1,z.2.2.2.1⟩⟩ :
                {q : A × (A × (A × A)) //
                  f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
                    f q.1 = f q.2.2.2}))).1.2.2.2 = z.1.2.2.2.1
            simp only [Equiv.apply_symm_apply]
          · rfl


def uliftCompatibleQuintupleEquiv {A B : Type u} (f : A → B) :
    ULift.{u + 1} {q : A × (A × (A × (A × A))) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
      f q.1 = f q.2.2.2.1 ∧ f q.1 = f q.2.2.2.2} ≃
      splitFreeCechQuintuple (uliftFunction f) where
  toFun z :=
    ⟨(ULift.up z.down.1.1,
      (ULift.up z.down.1.2.1,
        (ULift.up z.down.1.2.2.1,
          (ULift.up z.down.1.2.2.2.1,
            ULift.up z.down.1.2.2.2.2)))),
      ⟨congrArg ULift.up z.down.2.1,
        congrArg ULift.up z.down.2.2.1,
        congrArg ULift.up z.down.2.2.2.1,
        congrArg ULift.up z.down.2.2.2.2⟩⟩
  invFun z := ULift.up
    ⟨(z.1.1.down,
      (z.1.2.1.down,
        (z.1.2.2.1.down,
          (z.1.2.2.2.1.down,z.1.2.2.2.2.down)))),
      ⟨congrArg ULift.down z.2.1,
        congrArg ULift.down z.2.2.1,
        congrArg ULift.down z.2.2.2.1,
        congrArg ULift.down z.2.2.2.2⟩⟩
  left_inv := by
    rintro ⟨⟨⟨a, ⟨b, ⟨c, ⟨d,e⟩⟩⟩⟩, h⟩⟩
    rfl
  right_inv := by
    intro z
    apply Subtype.ext
    apply Prod.ext
    · exact ULift.up_down z.1.1
    · apply Prod.ext
      · exact ULift.up_down z.1.2.1
      · apply Prod.ext
        · exact ULift.up_down z.1.2.2.1
        · apply Prod.ext
          · exact ULift.up_down z.1.2.2.2.1
          · exact ULift.up_down z.1.2.2.2.2


/-- Genuine quintuple CompHaus representable versus compatible split
fivefold points for every Stonean test object. -/
noncomputable def stoneanCompHausProbeCechQuintupleUliftEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T)) ≃
      splitFreeCechQuintuple
        (stoneanCompHausProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  let A := U.compHaus ⟶ profiniteToCompHaus.obj
    (Stonean.toProfinite.obj T.presentation)
  let B := U.compHaus ⟶ profiniteToCompHaus.obj T
  let R4 := U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechQuadruples T)
  let f : A → B := fun x => x ≫ profiniteToCompHaus.map p
  let e4 : R4 ≃ {q : A × (A × (A × A)) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
        f q.1 = f q.2.2.2} :=
    (Equiv.ulift.symm.trans
      (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)).trans
        ((uliftCompatibleQuadrupleEquiv f).symm.trans Equiv.ulift)
  let g4 : R4 → B := fun x =>
    x ≫ profiniteToCompHaus.map
      (stoneanCechQuadrupleVertexFirst T ≫ p)
  have h4 : ∀ r : R4, g4 r = f (e4 r).1.1 := by
    intro r
    rfl
  let et := compHausHomProfinitePullbackEquiv U.compHaus
    (stoneanCechQuadrupleVertexFirst T ≫ p) p
  exact (Equiv.ulift.trans
    (et.trans (compatibleNestedQuintupleEquiv f g4 e4 h4))).trans
      (Equiv.ulift.symm.trans (uliftCompatibleQuintupleEquiv f))


/-- The fifth face deleting the last vertex, transported to the actual
categorical fifth pullback, is exactly its pullback-first projection. -/
theorem stoneanCechCategoricalFifthFace4_eq_first (T : Profinite.{u}) :
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace4 T =
    pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  change (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)) =
    (pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  have he :
      (quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z) =
      (stoneanCechCategoricalQuadrupleToExplicit T).hom.hom
        ((pullback.fst
          (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T)).hom.hom z) := by
    apply Subtype.ext
    rfl
  rw [he]
  have h4 := congrArg
    (fun m : stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechQuadruples T =>
      m.hom.hom
        ((pullback.fst
          (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T)).hom.hom z))
    (stoneanCechCategoricalQuadruple_roundtrip T)
  exact h4


/-- The actual categorical fifth-to-fourth last face agrees at every
Stonean probe with the split-set fifth deletion, under the exact
fivefold and fourfold representable equivalences. -/
theorem stoneanCompHausProbeCechQuintupleUlift_face4
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :
    splitFreeCechQuintFace4 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuintupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuadrupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalQuintupleToExplicit T ≫
          stoneanCechFifthFace4 T))) := by
  rw [stoneanCechCategoricalFifthFace4_eq_first]
  rfl


#print axioms stoneanCompHausProbeCechQuintupleUlift_face4
#print axioms stoneanCechCategoricalFifthFace4_eq_first
#print axioms stoneanCompHausProbeCechQuintupleUliftEquiv
#print axioms uliftCompatibleQuintupleEquiv
#print axioms compatibleNestedQuintupleEquiv
end CMDG.CondensedCM5R0
