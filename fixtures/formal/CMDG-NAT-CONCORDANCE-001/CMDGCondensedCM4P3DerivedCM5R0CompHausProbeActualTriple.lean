import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeUliftTriple

/-!
# CMDG CM5 — actual CompHaus Čech triple and the split free-set triple

Use the genuine CompHaus representable of Q=R×_T P, not a replacement
triple. Its pullback comparison is transported through the genuine
pair comparison and the necessary universe lift. The three Čech faces
are checked pointwise against the original profinite morphisms.

The remaining comparison of free-module presheaf complexes and
pointwise exactness is outside this module. No unproved Ext² or derived
solidity is inferred.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- A compatible pair represented by R, together with another point
over the same target, is equivalent to an actual compatible triple. -/
def compatibleNestedTripleEquiv {A B R : Type u}
    (f : A → B) (g : R → B)
    (e : R ≃ {xy : A × A // f xy.1 = f xy.2})
    (h : ∀ r, g r = f (e r).1.1) :
    {rz : R × A // g rz.1 = f rz.2} ≃
      {xyz : A × (A × A) //
        f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2} where
  toFun z :=
    ⟨((e z.1.1).1.1, ((e z.1.1).1.2, z.1.2)),
      ⟨(e z.1.1).2, (h z.1.1).symm.trans z.2⟩⟩
  invFun z := by
    let xy : {xy : A × A // f xy.1 = f xy.2} :=
      ⟨(z.1.1, z.1.2.1), z.2.1⟩
    refine ⟨(e.symm xy, z.1.2.2), ?_⟩
    have hr : g (e.symm xy) = f z.1.1 := by
      simpa [xy] using h (e.symm xy)
    exact hr.trans z.2.2
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
          (⟨(z.1.1, z.1.2.1), z.2.1⟩ :
            {xy : A × A // f xy.1 = f xy.2}))).1.1 = z.1.1
      simp only [Equiv.apply_symm_apply]
    · apply Prod.ext
      · change (e (e.symm
            (⟨(z.1.1, z.1.2.1), z.2.1⟩ :
              {xy : A × A // f xy.1 = f xy.2}))).1.2 = z.1.2.1
        simp only [Equiv.apply_symm_apply]
      · rfl

/-- The genuine universe-lifted Hom set of Q, at a Stonean test
object, is the exact compatible-triple type of the split Čech map. -/
noncomputable def stoneanCompHausProbeCechTripleUliftEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T)) ≃
      splitFreeCechTriple (stoneanCompHausProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  let A := U.compHaus ⟶ profiniteToCompHaus.obj
    (Stonean.toProfinite.obj T.presentation)
  let B := U.compHaus ⟶ profiniteToCompHaus.obj T
  let R := U.compHaus ⟶ profiniteToCompHaus.obj
    (stoneanPresentationCechPairs T)
  let f : A → B := fun x => x ≫ profiniteToCompHaus.map p
  let g : R → B := fun x =>
    x ≫ profiniteToCompHaus.map (pullback.fst p p ≫ p)
  let e : R ≃ {xy : A × A // f xy.1 = f xy.2} :=
    stoneanCompHausProbeCechPairEquiv T U
  let et := stoneanCompHausProbeCechTripleEquiv T U
  have h : ∀ r : R, g r = f (e r).1.1 := by
    intro r
    change r ≫ profiniteToCompHaus.map (pullback.fst p p ≫ p) =
      (r ≫ profiniteToCompHaus.map (pullback.fst p p)) ≫
        profiniteToCompHaus.map p
    simp only [Functor.map_comp, Category.assoc]
  exact (Equiv.ulift.trans
    (et.trans (compatibleNestedTripleEquiv f g e h))).trans
      (Equiv.ulift.symm.trans (uliftCompatibleTripleEquiv f))

/-- XY face of the genuine triple agrees with the split-Čech face. -/
theorem stoneanCompHausProbeCechTripleUlift_xy
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T))) :
    splitFreeCechTripleXY (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechTripleUliftEquiv T U z) =
      stoneanCompHausProbeCechPairUliftEquiv T U
        (ULift.up (z.down ≫ profiniteToCompHaus.map
          (stoneanCechTripleXY T))) := by
  rfl

/-- XZ face of the genuine triple agrees with the split-Čech face. -/
theorem stoneanCompHausProbeCechTripleUlift_xz
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T))) :
    splitFreeCechTripleXZ (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechTripleUliftEquiv T U z) =
      stoneanCompHausProbeCechPairUliftEquiv T U
        (ULift.up (z.down ≫ profiniteToCompHaus.map
          (stoneanCechTripleXZ T))) := by
  apply Subtype.ext
  apply Prod.ext
  · change ULift.up
        ((z.down ≫ profiniteToCompHaus.map (stoneanCechTripleXY T)) ≫
          profiniteToCompHaus.map
            (pullback.fst (Profinite.presentation.π T)
              (Profinite.presentation.π T))) =
        ULift.up
          ((z.down ≫ profiniteToCompHaus.map (stoneanCechTripleXZ T)) ≫
            profiniteToCompHaus.map
              (pullback.fst (Profinite.presentation.π T)
                (Profinite.presentation.π T)))
    exact congrArg ULift.up
      (stoneanCompHausProbeTripleXZ_fst T U z.down).symm
  · change ULift.up
        (z.down ≫ profiniteToCompHaus.map (stoneanCechTripleZ T)) =
      ULift.up
        ((z.down ≫ profiniteToCompHaus.map (stoneanCechTripleXZ T)) ≫
          profiniteToCompHaus.map
            (pullback.snd (Profinite.presentation.π T)
              (Profinite.presentation.π T)))
    exact congrArg ULift.up
      (stoneanCompHausProbeTripleXZ_snd T U z.down).symm

/-- YZ face of the genuine triple agrees with the split-Čech face. -/
theorem stoneanCompHausProbeCechTripleUlift_yz
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T))) :
    splitFreeCechTripleYZ (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechTripleUliftEquiv T U z) =
      stoneanCompHausProbeCechPairUliftEquiv T U
        (ULift.up (z.down ≫ profiniteToCompHaus.map
          (stoneanCechTripleYZ T))) := by
  apply Subtype.ext
  apply Prod.ext
  · change ULift.up
        ((z.down ≫ profiniteToCompHaus.map (stoneanCechTripleXY T)) ≫
          profiniteToCompHaus.map
            (pullback.snd (Profinite.presentation.π T)
              (Profinite.presentation.π T))) =
        ULift.up
          ((z.down ≫ profiniteToCompHaus.map (stoneanCechTripleYZ T)) ≫
            profiniteToCompHaus.map
              (pullback.fst (Profinite.presentation.π T)
                (Profinite.presentation.π T)))
    exact congrArg ULift.up
      (stoneanCompHausProbeTripleYZ_fst T U z.down).symm
  · change ULift.up
        (z.down ≫ profiniteToCompHaus.map (stoneanCechTripleZ T)) =
      ULift.up
        ((z.down ≫ profiniteToCompHaus.map (stoneanCechTripleYZ T)) ≫
          profiniteToCompHaus.map
            (pullback.snd (Profinite.presentation.π T)
              (Profinite.presentation.π T)))
    exact congrArg ULift.up
      (stoneanCompHausProbeTripleYZ_snd T U z.down).symm

/-- The genuine degree-two free coefficient module, on the actual
represented universe-lifted triple, is isomorphic to the contracted
split Čech degree-two free module. -/
noncomputable def stoneanCompHausProbeFreeTripleIso
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1}
        (U.compHaus ⟶ profiniteToCompHaus.obj
          (stoneanPresentationCechTriples T))) ≅
      (ModuleCat.free Coeff).obj
        (splitFreeCechTriple (stoneanCompHausProbePresentationMap T U)) :=
  (ModuleCat.free Coeff).mapIso
    (stoneanCompHausProbeCechTripleUliftEquiv T U).toIso

#print axioms compatibleNestedTripleEquiv
#print axioms stoneanCompHausProbeCechTripleUliftEquiv
#print axioms stoneanCompHausProbeCechTripleUlift_xy
#print axioms stoneanCompHausProbeCechTripleUlift_xz
#print axioms stoneanCompHausProbeCechTripleUlift_yz
#print axioms stoneanCompHausProbeFreeTripleIso

end CMDG.CondensedCM5R0
