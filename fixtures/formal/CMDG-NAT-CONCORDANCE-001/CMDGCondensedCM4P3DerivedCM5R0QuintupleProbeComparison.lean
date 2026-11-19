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

private theorem categoricalFifthFirst_fourth_atPoint
    (T : Profinite.{u}) (z : stoneanPresentationCechQuintuples T) :
    (pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z =
    (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)) := by
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let A4 := stoneanCechExplicitQuadrupleToAbstract T
  let B4 := stoneanCechCategoricalQuadrupleToExplicit T
  have hq : (quintupleFace4 T).hom.hom (B5.hom.hom z) =
      B4.hom.hom (F.hom.hom z) := by
    apply Subtype.ext
    rfl
  rw [hq]
  have h := congrArg (fun m :
    stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechQuadruples T =>
      m.hom.hom (F.hom.hom z))
    (stoneanCechCategoricalQuadruple_roundtrip T)
  exact h.symm

theorem stoneanCechCategoricalQuintuple_face3_xyz
    (T : Profinite.{u}) :
    pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ stoneanCechQuadFaceXYZ T =
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace3 T ≫ stoneanCechQuadFaceXYZ T := by
  apply ConcreteCategory.hom_ext
  intro z
  have h := categoricalFifthFirst_fourth_atPoint T z
  change (pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z =
    (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)) at h
  change (stoneanCechQuadFaceXYZ T).hom.hom
    ((pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z) =
    (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace3 T).hom.hom
          ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)))
  rw [h]
  let q5 := (stoneanCechCategoricalQuintupleToExplicit T).hom.hom z
  let q4 := (quintupleFace4 T).hom.hom q5
  let q3 := (quintupleFace3 T).hom.hom q5
  let X := stoneanCechExplicitQuadrupleToAbstract T
  have h4 := stoneanCechExplicitQuadruple_xyz_atPoint T q4
  have h3 := stoneanCechExplicitQuadruple_xyz_atPoint T q3
  change (stoneanCechQuadFaceXYZ T).hom.hom (X.hom.hom q4) =
    stoneanCechTripleOfRelated T
      q4.val.1 q4.val.2.1 q4.val.2.2.1
      q4.property.1 q4.property.2.1 at h4
  change (stoneanCechQuadFaceXYZ T).hom.hom (X.hom.hom q3) =
    stoneanCechTripleOfRelated T
      q3.val.1 q3.val.2.1 q3.val.2.2.1
      q3.property.1 q3.property.2.1 at h3
  have he :
      stoneanCechTripleOfRelated T
        q4.val.1 q4.val.2.1 q4.val.2.2.1
        q4.property.1 q4.property.2.1 =
      stoneanCechTripleOfRelated T
        q3.val.1 q3.val.2.1 q3.val.2.2.1
        q3.property.1 q3.property.2.1 := by rfl
  exact h4.trans (he.trans h3.symm)

theorem stoneanCechCategoricalQuintuple_face0_firstTriple
    (T : Profinite.{u}) :
    pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ quadFaceYZW T =
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace0 T ≫ stoneanCechQuadFaceXYZ T := by
  apply ConcreteCategory.hom_ext
  intro z
  have h := categoricalFifthFirst_fourth_atPoint T z
  change (pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z =
    (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)) at h
  change (quadFaceYZW T).hom.hom
    ((pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z) =
    (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace0 T).hom.hom
          ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)))
  rw [h]
  let q5 := (stoneanCechCategoricalQuintupleToExplicit T).hom.hom z
  let q4 := (quintupleFace4 T).hom.hom q5
  let q3 := (quintupleFace0 T).hom.hom q5
  let X := stoneanCechExplicitQuadrupleToAbstract T
  have h4 := stoneanCechExplicitQuadruple_yzw_atPoint T q4
  have h3 := stoneanCechExplicitQuadruple_xyz_atPoint T q3
  change (quadFaceYZW T).hom.hom (X.hom.hom q4) =
    stoneanCechTripleOfRelated T
      q4.val.2.1 q4.val.2.2.1 q4.val.2.2.2
      q4.property.2.1 q4.property.2.2 at h4
  change (stoneanCechQuadFaceXYZ T).hom.hom (X.hom.hom q3) =
    stoneanCechTripleOfRelated T
      q3.val.1 q3.val.2.1 q3.val.2.2.1
      q3.property.1 q3.property.2.1 at h3
  have he :
      stoneanCechTripleOfRelated T
      q4.val.2.1 q4.val.2.2.1 q4.val.2.2.2
      q4.property.2.1 q4.property.2.2 =
      stoneanCechTripleOfRelated T
        q3.val.1 q3.val.2.1 q3.val.2.2.1
        q3.property.1 q3.property.2.1 := by rfl
  exact h4.trans (he.trans h3.symm)

#print axioms stoneanCechCategoricalQuintuple_face0_firstTriple
theorem stoneanCechCategoricalQuintuple_face1_firstTriple
    (T : Profinite.{u}) :
    pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ quadFaceXZW T =
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace1 T ≫ stoneanCechQuadFaceXYZ T := by
  apply ConcreteCategory.hom_ext
  intro z
  have h := categoricalFifthFirst_fourth_atPoint T z
  change (pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z =
    (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)) at h
  change (quadFaceXZW T).hom.hom
    ((pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z) =
    (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace1 T).hom.hom
          ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)))
  rw [h]
  let q5 := (stoneanCechCategoricalQuintupleToExplicit T).hom.hom z
  let q4 := (quintupleFace4 T).hom.hom q5
  let q3 := (quintupleFace1 T).hom.hom q5
  let X := stoneanCechExplicitQuadrupleToAbstract T
  have h4 := stoneanCechExplicitQuadruple_xzw_atPoint T q4
  have h3 := stoneanCechExplicitQuadruple_xyz_atPoint T q3
  change (quadFaceXZW T).hom.hom (X.hom.hom q4) =
    stoneanCechTripleOfRelated T
      q4.val.1 q4.val.2.2.1 q4.val.2.2.2
      (q4.property.1.trans q4.property.2.1) q4.property.2.2 at h4
  change (stoneanCechQuadFaceXYZ T).hom.hom (X.hom.hom q3) =
    stoneanCechTripleOfRelated T
      q3.val.1 q3.val.2.1 q3.val.2.2.1
      q3.property.1 q3.property.2.1 at h3
  have he :
      stoneanCechTripleOfRelated T
      q4.val.1 q4.val.2.2.1 q4.val.2.2.2
      (q4.property.1.trans q4.property.2.1) q4.property.2.2 =
      stoneanCechTripleOfRelated T
        q3.val.1 q3.val.2.1 q3.val.2.2.1
        q3.property.1 q3.property.2.1 := by rfl
  exact h4.trans (he.trans h3.symm)

#print axioms stoneanCechCategoricalQuintuple_face1_firstTriple
theorem stoneanCechCategoricalQuintuple_face2_firstTriple
    (T : Profinite.{u}) :
    pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ quadFaceXYW T =
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace2 T ≫ stoneanCechQuadFaceXYZ T := by
  apply ConcreteCategory.hom_ext
  intro z
  have h := categoricalFifthFirst_fourth_atPoint T z
  change (pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z =
    (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom
        ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)) at h
  change (quadFaceXYW T).hom.hom
    ((pullback.fst
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z) =
    (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace2 T).hom.hom
          ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)))
  rw [h]
  let q5 := (stoneanCechCategoricalQuintupleToExplicit T).hom.hom z
  let q4 := (quintupleFace4 T).hom.hom q5
  let q3 := (quintupleFace2 T).hom.hom q5
  let X := stoneanCechExplicitQuadrupleToAbstract T
  have h4 := stoneanCechExplicitQuadruple_xyw_atPoint T q4
  have h3 := stoneanCechExplicitQuadruple_xyz_atPoint T q3
  change (quadFaceXYW T).hom.hom (X.hom.hom q4) =
    stoneanCechTripleOfRelated T
      q4.val.1 q4.val.2.1 q4.val.2.2.2
      q4.property.1 (q4.property.2.1.trans q4.property.2.2) at h4
  change (stoneanCechQuadFaceXYZ T).hom.hom (X.hom.hom q3) =
    stoneanCechTripleOfRelated T
      q3.val.1 q3.val.2.1 q3.val.2.2.1
      q3.property.1 q3.property.2.1 at h3
  have he :
      stoneanCechTripleOfRelated T
      q4.val.1 q4.val.2.1 q4.val.2.2.2
      q4.property.1 (q4.property.2.1.trans q4.property.2.2) =
      stoneanCechTripleOfRelated T
        q3.val.1 q3.val.2.1 q3.val.2.2.1
        q3.property.1 q3.property.2.1 := by rfl
  exact h4.trans (he.trans h3.symm)

#print axioms stoneanCechCategoricalQuintuple_face2_firstTriple


noncomputable def stoneanCechQuadrupleVertexLast (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      Stonean.toProfinite.obj T.presentation :=
  pullback.snd
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

theorem stoneanCechCategoricalQuintuple_last_atPoint (T : Profinite.{u})
    (z : stoneanPresentationCechQuintuples T) :
    (explicitQuintupleFifth T).hom.hom
      ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z) =
      (pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T)).hom.hom z := by rfl


theorem stoneanCechCategoricalQuintuple_face0_last
    (T : Profinite.{u}) :
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace0 T ≫ stoneanCechQuadrupleVertexLast T =
    pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (quintupleFace0 T).hom.hom
    ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)
  have hq := stoneanCechExplicitQuadruple_fourth_atPoint T q
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
      q.val.2.2.2 at hq
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [hq]
  exact stoneanCechCategoricalQuintuple_last_atPoint T z

#print axioms stoneanCechCategoricalQuintuple_face0_last

theorem stoneanCechCategoricalQuintuple_face1_last
    (T : Profinite.{u}) :
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace1 T ≫ stoneanCechQuadrupleVertexLast T =
    pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (quintupleFace1 T).hom.hom
    ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)
  have hq := stoneanCechExplicitQuadruple_fourth_atPoint T q
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
      q.val.2.2.2 at hq
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [hq]
  exact stoneanCechCategoricalQuintuple_last_atPoint T z

#print axioms stoneanCechCategoricalQuintuple_face1_last

theorem stoneanCechCategoricalQuintuple_face2_last
    (T : Profinite.{u}) :
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace2 T ≫ stoneanCechQuadrupleVertexLast T =
    pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (quintupleFace2 T).hom.hom
    ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)
  have hq := stoneanCechExplicitQuadruple_fourth_atPoint T q
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
      q.val.2.2.2 at hq
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [hq]
  exact stoneanCechCategoricalQuintuple_last_atPoint T z

#print axioms stoneanCechCategoricalQuintuple_face2_last

theorem stoneanCechCategoricalQuintuple_face3_last
    (T : Profinite.{u}) :
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace3 T ≫ stoneanCechQuadrupleVertexLast T =
    pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (quintupleFace3 T).hom.hom
    ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom z)
  have hq := stoneanCechExplicitQuadruple_fourth_atPoint T q
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
      q.val.2.2.2 at hq
  change (stoneanCechQuadrupleVertexLast T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [hq]
  exact stoneanCechCategoricalQuintuple_last_atPoint T z

#print axioms stoneanCechCategoricalQuintuple_face3_last


#print axioms stoneanCechCategoricalQuintuple_face3_xyz

theorem stoneanCompHausProbeCechQuadrupleUlift_last
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) :
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U z).val.2.2.2 =
    ULift.up (z.down ≫ profiniteToCompHaus.map
      (stoneanCechQuadrupleVertexLast T)) := by
  rfl

#print axioms stoneanCompHausProbeCechQuadrupleUlift_last
#print axioms stoneanCechCategoricalFifthFace4_eq_first
#print axioms stoneanCompHausProbeCechQuintupleUliftEquiv
#print axioms uliftCompatibleQuintupleEquiv
#print axioms compatibleNestedQuintupleEquiv
theorem stoneanCompHausProbeCechQuintupleUlift_face0
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :
    splitFreeCechQuintFace0 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuintupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuadrupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalQuintupleToExplicit T ≫
          stoneanCechFifthFace0 T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e4 := stoneanCompHausProbeCechQuadrupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalQuintupleToExplicit T ≫
    stoneanCechFifthFace0 T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have htriple :
      splitFreeCechQuadYZW p (e4 q0) =
      splitFreeCechQuadXYZ p (e4 q1) := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_yzw,
      stoneanCompHausProbeCechQuadrupleUlift_xyz]
    apply congrArg (stoneanCompHausProbeCechTripleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map (F ≫ quadFaceYZW T) =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadFaceXYZ T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        stoneanPresentationCechTriples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face0_firstTriple T)
  have hfourth :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e4 q1).val.2.2.2 := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_last]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadrupleVertexLast T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face0_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechTriple p => t.val.1) htriple
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.1) htriple
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.2) htriple
      · exact hfourth

#print axioms stoneanCompHausProbeCechQuintupleUlift_face0



theorem stoneanCompHausProbeCechQuintupleUlift_face1
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :
    splitFreeCechQuintFace1 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuintupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuadrupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalQuintupleToExplicit T ≫
          stoneanCechFifthFace1 T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e4 := stoneanCompHausProbeCechQuadrupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalQuintupleToExplicit T ≫
    stoneanCechFifthFace1 T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have htriple :
      splitFreeCechQuadXZW p (e4 q0) =
      splitFreeCechQuadXYZ p (e4 q1) := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_xzw,
      stoneanCompHausProbeCechQuadrupleUlift_xyz]
    apply congrArg (stoneanCompHausProbeCechTripleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map (F ≫ quadFaceXZW T) =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadFaceXYZ T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        stoneanPresentationCechTriples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face1_firstTriple T)
  have hfourth :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e4 q1).val.2.2.2 := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_last]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadrupleVertexLast T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face1_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechTriple p => t.val.1) htriple
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.1) htriple
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.2) htriple
      · exact hfourth

#print axioms stoneanCompHausProbeCechQuintupleUlift_face1

theorem stoneanCompHausProbeCechQuintupleUlift_face2
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :
    splitFreeCechQuintFace2 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuintupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuadrupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalQuintupleToExplicit T ≫
          stoneanCechFifthFace2 T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e4 := stoneanCompHausProbeCechQuadrupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalQuintupleToExplicit T ≫
    stoneanCechFifthFace2 T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have htriple :
      splitFreeCechQuadXYW p (e4 q0) =
      splitFreeCechQuadXYZ p (e4 q1) := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_xyw,
      stoneanCompHausProbeCechQuadrupleUlift_xyz]
    apply congrArg (stoneanCompHausProbeCechTripleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map (F ≫ quadFaceXYW T) =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadFaceXYZ T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        stoneanPresentationCechTriples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face2_firstTriple T)
  have hfourth :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e4 q1).val.2.2.2 := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_last]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadrupleVertexLast T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face2_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechTriple p => t.val.1) htriple
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.1) htriple
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.2) htriple
      · exact hfourth

#print axioms stoneanCompHausProbeCechQuintupleUlift_face2

theorem stoneanCompHausProbeCechQuintupleUlift_face3
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :
    splitFreeCechQuintFace3 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuintupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuadrupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalQuintupleToExplicit T ≫
          stoneanCechFifthFace3 T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e4 := stoneanCompHausProbeCechQuadrupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalQuintupleToExplicit T ≫
    stoneanCechFifthFace3 T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have htriple :
      splitFreeCechQuadXYZ p (e4 q0) =
      splitFreeCechQuadXYZ p (e4 q1) := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_xyz,
      stoneanCompHausProbeCechQuadrupleUlift_xyz]
    apply congrArg (stoneanCompHausProbeCechTripleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map (F ≫ stoneanCechQuadFaceXYZ T) =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadFaceXYZ T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        stoneanPresentationCechTriples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face3_xyz T)
  have hfourth :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e4 q1).val.2.2.2 := by
    rw [stoneanCompHausProbeCechQuadrupleUlift_last]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ stoneanCechQuadrupleVertexLast T)
    exact congrArg
      (fun m : stoneanPresentationCechQuintuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalQuintuple_face3_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechTriple p => t.val.1) htriple
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.1) htriple
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechTriple p => t.val.2.2) htriple
      · exact hfourth

#print axioms stoneanCompHausProbeCechQuintupleUlift_face3
end CMDG.CondensedCM5R0
