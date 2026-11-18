import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeTwo
import CMDGCondensedCM4P3DerivedCM5R0GenuineFourthCechBoundary
import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeActualTriple

/-!
# CMDG CM5 — represented fourfold Čech object at every Stonean probe

For every profinite T and Stonean U, build a universe-correct equivalence
from the *actual* represented CompHaus Hom set of the genuine categorical
fourfold Čech pullback to the compatible quadruple set used by the
split-free Čech degree-two contracting homotopy.

The equivalence is assembled via the preserved genuine CompHaus
pullback, actual triple-pullback comparison, one generic set-level
nested-quadruple equivalence, and the explicit ULift of compatible
quadruples. All four faces XYW, XZW, YZW, XYZ are proved compatible with the
genuine categorical CompHaus pullback face maps.

Free-module differential comparison and exactness at every
Stonean probe are proved in the adjacent separate module.
Sheafification into genuine CondensedMod and global epi remain OPEN. In
particular the map F_{P(T)^4_T}→M_T is NOT proved epimorphic and
no Ext³ vanishing is asserted.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- A nested relation over the base is equivalent to a right-associated
compatible quadruple; this is a genuine set equivalence. -/
def compatibleNestedQuadrupleEquiv {A B R : Type u}
    (f : A → B) (g : R → B)
    (e : R ≃ {xyz : A × (A × A) //
      f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2})
    (h : ∀ r, g r = f (e r).1.1) :
    {rw : R × A // g rw.1 = f rw.2} ≃
      {xyzw : A × (A × (A × A)) //
        f xyzw.1 = f xyzw.2.1 ∧
        f xyzw.1 = f xyzw.2.2.1 ∧
        f xyzw.1 = f xyzw.2.2.2} where
  toFun z :=
    ⟨((e z.1.1).1.1,
      ((e z.1.1).1.2.1, ((e z.1.1).1.2.2, z.1.2))),
      ⟨(e z.1.1).2.1, (e z.1.1).2.2,
        (h z.1.1).symm.trans z.2⟩⟩
  invFun z := by
    let xyz : {xyz : A × (A × A) //
      f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2} :=
      ⟨(z.1.1, (z.1.2.1, z.1.2.2.1)),
        ⟨z.2.1, z.2.2.1⟩⟩
    refine ⟨(e.symm xyz, z.1.2.2.2), ?_⟩
    have hr : g (e.symm xyz) = f z.1.1 := by
      simpa [xyz] using h (e.symm xyz)
    exact hr.trans z.2.2.2
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
        (⟨(z.1.1, (z.1.2.1, z.1.2.2.1)),
          ⟨z.2.1, z.2.2.1⟩⟩ :
          {xyz : A × (A × A) //
            f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2}))).1.1 =
        z.1.1
      simp only [Equiv.apply_symm_apply]
    · apply Prod.ext
      · change (e (e.symm
          (⟨(z.1.1, (z.1.2.1, z.1.2.2.1)),
            ⟨z.2.1, z.2.2.1⟩⟩ :
          {xyz : A × (A × A) //
            f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2}))).1.2.1 =
          z.1.2.1
        simp only [Equiv.apply_symm_apply]
      · apply Prod.ext
        · change (e (e.symm
            (⟨(z.1.1, (z.1.2.1, z.1.2.2.1)),
              ⟨z.2.1, z.2.2.1⟩⟩ :
            {xyz : A × (A × A) //
              f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2}))).1.2.2 =
            z.1.2.2.1
          simp only [Equiv.apply_symm_apply]
        · rfl

/-- The universe lift of a compatible quadruple is exactly the
split-free Čech quadruple on the universe-lifted presentation. -/
def uliftCompatibleQuadrupleEquiv {A B : Type u} (f : A → B) :
    ULift.{u + 1}
      {xyzw : A × (A × (A × A)) //
        f xyzw.1 = f xyzw.2.1 ∧
        f xyzw.1 = f xyzw.2.2.1 ∧
        f xyzw.1 = f xyzw.2.2.2} ≃
      splitFreeCechQuadruple (uliftFunction f) where
  toFun z :=
    ⟨(ULift.up z.down.1.1,
      (ULift.up z.down.1.2.1,
        (ULift.up z.down.1.2.2.1, ULift.up z.down.1.2.2.2))),
      ⟨congrArg ULift.up z.down.2.1,
        congrArg ULift.up z.down.2.2.1,
        congrArg ULift.up z.down.2.2.2⟩⟩
  invFun z := ULift.up
    ⟨(z.1.1.down, (z.1.2.1.down,
      (z.1.2.2.1.down, z.1.2.2.2.down))),
      ⟨congrArg ULift.down z.2.1,
        congrArg ULift.down z.2.2.1,
        congrArg ULift.down z.2.2.2⟩⟩
  left_inv := by
    rintro ⟨⟨⟨a, ⟨b, ⟨c,d⟩⟩⟩, h⟩⟩
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
        · exact ULift.up_down z.1.2.2.2


/-- The genuine universe-lifted CompHaus Hom set of the actual
categorical fourfold Stonean Čech pullback is equivalent to the
compatible-quadruple type of the split free Čech complex. -/
noncomputable def stoneanCompHausProbeCechQuadrupleUliftEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T)) ≃
      splitFreeCechQuadruple
        (stoneanCompHausProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  let A := U.compHaus ⟶ profiniteToCompHaus.obj
    (Stonean.toProfinite.obj T.presentation)
  let B := U.compHaus ⟶ profiniteToCompHaus.obj T
  let R₁ := U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechPairs T)
  let R₃ := U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)
  let f : A → B := fun x => x ≫ profiniteToCompHaus.map p
  let g₁ : R₁ → B := fun x =>
    x ≫ profiniteToCompHaus.map (pullback.fst p p ≫ p)
  let e₁ : R₁ ≃ {xy : A × A // f xy.1 = f xy.2} :=
    stoneanCompHausProbeCechPairEquiv T U
  have h₁ : ∀ r : R₁, g₁ r = f (e₁ r).1.1 := by
    intro r
    change r ≫ profiniteToCompHaus.map (pullback.fst p p ≫ p) =
      (r ≫ profiniteToCompHaus.map (pullback.fst p p)) ≫
        profiniteToCompHaus.map p
    simp only [Functor.map_comp, Category.assoc]
  let e₃ : R₃ ≃ {xyz : A × (A × A) //
      f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2} :=
    (stoneanCompHausProbeCechTripleEquiv T U).trans
      (compatibleNestedTripleEquiv f g₁ e₁ h₁)
  let g₃ : R₃ → B := fun x =>
    x ≫ profiniteToCompHaus.map
      (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p)
  have h₃ : ∀ r : R₃, g₃ r = f (e₃ r).1.1 := by
    intro r
    change r ≫ profiniteToCompHaus.map
        (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) =
      ((r ≫ profiniteToCompHaus.map (stoneanCechTripleXY T)) ≫
        profiniteToCompHaus.map (pullback.fst p p)) ≫
          profiniteToCompHaus.map p
    simp only [Functor.map_comp, Category.assoc]
  let et := compHausHomProfinitePullbackEquiv U.compHaus
    (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  exact (Equiv.ulift.trans
    (et.trans (compatibleNestedQuadrupleEquiv f g₃ e₃ h₃))).trans
      (Equiv.ulift.symm.trans (uliftCompatibleQuadrupleEquiv f))


private noncomputable abbrev quadProbeXYZ (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
    stoneanPresentationCechTriples T :=
  pullback.fst
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- Actual fourfold face omitted w is the split XYZ face in each
genuine represented CompHaus Stonean probe. -/
theorem stoneanCompHausProbeCechQuadrupleUlift_xyz
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) :
    splitFreeCechQuadXYZ (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuadrupleUliftEquiv T U z) =
    stoneanCompHausProbeCechTripleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T))) := by
  rfl


private noncomputable abbrev quadProbeW (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
    Stonean.toProfinite.obj T.presentation :=
  pullback.snd
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The genuine fourfold XYW face commutes with the same actual
universe-lifted CompHaus representation equivalence. -/
theorem stoneanCompHausProbeCechQuadrupleUlift_xyw
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) :
    splitFreeCechQuadXYW (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuadrupleUliftEquiv T U z) =
    stoneanCompHausProbeCechTripleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceXYW T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let eT := stoneanCompHausProbeCechTripleUliftEquiv T U
  let q0 : ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T))
  let q1 : ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceXYW T))
  have hMorph : quadProbeXYZ T ≫ stoneanCechTripleXY T =
      quadFaceXYW T ≫ stoneanCechTripleXY T := by
    unfold quadFaceXYW
    rw [pullback.lift_fst]
    rfl
  have hpair : splitFreeCechTripleXY p (eT q0) =
      splitFreeCechTripleXY p (eT q1) := by
    rw [stoneanCompHausProbeCechTripleUlift_xy,
      stoneanCompHausProbeCechTripleUlift_xy]
    apply congrArg (stoneanCompHausProbeCechPairUliftEquiv T U)
    apply congrArg ULift.up
    change
      z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T) ≫
        profiniteToCompHaus.map (stoneanCechTripleXY T) =
      z.down ≫ profiniteToCompHaus.map (quadFaceXYW T) ≫
        profiniteToCompHaus.map (stoneanCechTripleXY T)
    simpa only [Category.assoc, ← Functor.map_comp] using
      congrArg
        (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T =>
          z.down ≫ profiniteToCompHaus.map m) hMorph
  have h0 := stoneanCompHausProbeCechQuadrupleUlift_xyz T U z
  apply Subtype.ext
  apply Prod.ext
  · exact (congrArg (fun t : splitFreeCechTriple p => t.val.1) h0).trans
      (congrArg (fun xy : splitFreeCechPair p => xy.val.1) hpair)
  · apply Prod.ext
    · exact (congrArg (fun t : splitFreeCechTriple p => t.val.2.1) h0).trans
        (congrArg (fun xy : splitFreeCechPair p => xy.val.2) hpair)
    · change ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeW T)) =
        ULift.up ((z.down ≫ profiniteToCompHaus.map (quadFaceXYW T)) ≫
          profiniteToCompHaus.map (stoneanCechTripleZ T))
      apply congrArg ULift.up
      change z.down ≫ profiniteToCompHaus.map (quadProbeW T) =
        (z.down ≫ profiniteToCompHaus.map (quadFaceXYW T)) ≫
          profiniteToCompHaus.map (stoneanCechTripleZ T)
      have hw : quadProbeW T =
          quadFaceXYW T ≫ stoneanCechTripleZ T := by
        unfold quadFaceXYW
        rw [pullback.lift_snd]
        rfl
      simpa only [Category.assoc, ← Functor.map_comp] using
        congrArg
          (fun m : stoneanPresentationCechQuadruples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            z.down ≫ profiniteToCompHaus.map m) hw

theorem stoneanCompHausProbeCechQuadrupleUlift_xzw
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) :
    splitFreeCechQuadXZW (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuadrupleUliftEquiv T U z) =
    stoneanCompHausProbeCechTripleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceXZW T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let eT := stoneanCompHausProbeCechTripleUliftEquiv T U
  let q0 : ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T))
  let q1 : ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceXZW T))
  have hMorph : quadProbeXYZ T ≫ stoneanCechTripleXZ T =
      quadFaceXZW T ≫ stoneanCechTripleXY T := by
    unfold quadFaceXZW
    rw [pullback.lift_fst]
    rfl
  have hpair : splitFreeCechTripleXZ p (eT q0) =
      splitFreeCechTripleXY p (eT q1) := by
    rw [stoneanCompHausProbeCechTripleUlift_xz,
      stoneanCompHausProbeCechTripleUlift_xy]
    apply congrArg (stoneanCompHausProbeCechPairUliftEquiv T U)
    apply congrArg ULift.up
    change
      z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T) ≫
        profiniteToCompHaus.map (stoneanCechTripleXZ T) =
      z.down ≫ profiniteToCompHaus.map (quadFaceXZW T) ≫
        profiniteToCompHaus.map (stoneanCechTripleXY T)
    simpa only [Category.assoc, ← Functor.map_comp] using
      congrArg
        (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T =>
          z.down ≫ profiniteToCompHaus.map m) hMorph
  have h0 := stoneanCompHausProbeCechQuadrupleUlift_xyz T U z
  apply Subtype.ext
  apply Prod.ext
  · exact (congrArg (fun t : splitFreeCechTriple p => t.val.1) h0).trans
      (congrArg (fun xy : splitFreeCechPair p => xy.val.1) hpair)
  · apply Prod.ext
    · exact (congrArg (fun t : splitFreeCechTriple p => t.val.2.2) h0).trans
        (congrArg (fun xy : splitFreeCechPair p => xy.val.2) hpair)
    · change ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeW T)) =
        ULift.up ((z.down ≫ profiniteToCompHaus.map (quadFaceXZW T)) ≫
          profiniteToCompHaus.map (stoneanCechTripleZ T))
      apply congrArg ULift.up
      change z.down ≫ profiniteToCompHaus.map (quadProbeW T) =
        (z.down ≫ profiniteToCompHaus.map (quadFaceXZW T)) ≫
          profiniteToCompHaus.map (stoneanCechTripleZ T)
      have hw : quadProbeW T =
          quadFaceXZW T ≫ stoneanCechTripleZ T := by
        unfold quadFaceXZW
        rw [pullback.lift_snd]
        rfl
      simpa only [Category.assoc, ← Functor.map_comp] using
        congrArg
          (fun m : stoneanPresentationCechQuadruples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            z.down ≫ profiniteToCompHaus.map m) hw


theorem stoneanCompHausProbeCechQuadrupleUlift_yzw
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) :
    splitFreeCechQuadYZW (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechQuadrupleUliftEquiv T U z) =
    stoneanCompHausProbeCechTripleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceYZW T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let eT := stoneanCompHausProbeCechTripleUliftEquiv T U
  let q0 : ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T))
  let q1 : ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechTriples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceYZW T))
  have hMorph : quadProbeXYZ T ≫ stoneanCechTripleYZ T =
      quadFaceYZW T ≫ stoneanCechTripleXY T := by
    unfold quadFaceYZW
    rw [pullback.lift_fst]
    rfl
  have hpair : splitFreeCechTripleYZ p (eT q0) =
      splitFreeCechTripleXY p (eT q1) := by
    rw [stoneanCompHausProbeCechTripleUlift_yz,
      stoneanCompHausProbeCechTripleUlift_xy]
    apply congrArg (stoneanCompHausProbeCechPairUliftEquiv T U)
    apply congrArg ULift.up
    change
      z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T) ≫
        profiniteToCompHaus.map (stoneanCechTripleYZ T) =
      z.down ≫ profiniteToCompHaus.map (quadFaceYZW T) ≫
        profiniteToCompHaus.map (stoneanCechTripleXY T)
    simpa only [Category.assoc, ← Functor.map_comp] using
      congrArg
        (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T =>
          z.down ≫ profiniteToCompHaus.map m) hMorph
  have h0 := stoneanCompHausProbeCechQuadrupleUlift_xyz T U z
  apply Subtype.ext
  apply Prod.ext
  · exact (congrArg (fun t : splitFreeCechTriple p => t.val.2.1) h0).trans
      (congrArg (fun xy : splitFreeCechPair p => xy.val.1) hpair)
  · apply Prod.ext
    · exact (congrArg (fun t : splitFreeCechTriple p => t.val.2.2) h0).trans
        (congrArg (fun xy : splitFreeCechPair p => xy.val.2) hpair)
    · change ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeW T)) =
        ULift.up ((z.down ≫ profiniteToCompHaus.map (quadFaceYZW T)) ≫
          profiniteToCompHaus.map (stoneanCechTripleZ T))
      apply congrArg ULift.up
      change z.down ≫ profiniteToCompHaus.map (quadProbeW T) =
        (z.down ≫ profiniteToCompHaus.map (quadFaceYZW T)) ≫
          profiniteToCompHaus.map (stoneanCechTripleZ T)
      have hw : quadProbeW T =
          quadFaceYZW T ≫ stoneanCechTripleZ T := by
        unfold quadFaceYZW
        rw [pullback.lift_snd]
        rfl
      simpa only [Category.assoc, ← Functor.map_comp] using
        congrArg
          (fun m : stoneanPresentationCechQuadruples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            z.down ≫ profiniteToCompHaus.map m) hw



#print axioms compatibleNestedQuadrupleEquiv
#print axioms uliftCompatibleQuadrupleEquiv
#print axioms stoneanCompHausProbeCechQuadrupleUliftEquiv
#print axioms stoneanCompHausProbeCechQuadrupleUlift_xyz
#print axioms stoneanCompHausProbeCechQuadrupleUlift_xyw
#print axioms stoneanCompHausProbeCechQuadrupleUlift_xzw
#print axioms stoneanCompHausProbeCechQuadrupleUlift_yzw
end CMDG.CondensedCM5R0
