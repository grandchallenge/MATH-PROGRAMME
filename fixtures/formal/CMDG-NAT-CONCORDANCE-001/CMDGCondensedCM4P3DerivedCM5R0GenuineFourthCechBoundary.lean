import CMDGCondensedCM4P3DerivedCM5R0ThirdRelationExtCriterion

/-!
# CMDG CM5 — actual categorical fourfold Čech boundary and third relation

For arbitrary profinite T, construct the genuine categorical fourfold
Čech pullback (an iterated pullback of the pinned Stonean presentation)
with its four continuous face maps to the genuine categorical Čech triple.

These yield a morphism d₃:F_{P⁴_T}→F_{P³_T} of actual free
condensed modules. Prove the full chain identity d₃≫d₂=0 using
three repeated-face identities and the 12-term alternating boundary
cancellation in the actual categorical pullbacks. The composite with
the genuine triple-to-second-relation map F_{P³_T}→L_T also vanishes
by monicity of L_T→F_{P²_T}. Hence d₃ factors canonically through
M_T=kernel(F_{P³_T}→L_T), the genuine third relation object.

The map F_{P⁴_T}→M_T is NOT claimed to be an epimorphism.
Consequently no Ext³ vanishing, scalar H³ acyclicity, derived
solidity in all shifts or CM5 capstone closure is claimed.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Actual fourth level of the categorical Stonean Čech nerve. -/
noncomputable abbrev stoneanPresentationCechQuadruples
    (T : Profinite.{u}) : Profinite.{u} :=
  let p := Profinite.presentation.π T
  pullback
    (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p)
    p

private noncomputable def quadXYZ (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechTriples T :=
  pullback.fst
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

private noncomputable def quadW (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      Stonean.toProfinite.obj T.presentation :=
  pullback.snd
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

private theorem quad_base_condition (T : Profinite.{u}) :
    quadXYZ T ≫ (stoneanCechTripleXY T ≫
       pullback.fst (Profinite.presentation.π T)
         (Profinite.presentation.π T) ≫
       Profinite.presentation.π T) =
    quadW T ≫ Profinite.presentation.π T := by
  exact pullback.condition

/-- Remove z from the actual fourfold Čech object. -/
noncomputable def quadFaceXYW (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechTriples T := by
  let p := Profinite.presentation.π T
  exact pullback.lift
    (quadXYZ T ≫ stoneanCechTripleXY T) (quadW T)
    (by simpa only [Category.assoc] using quad_base_condition T)

theorem quadFaceXYW_xy (T : Profinite.{u}) :
    quadFaceXYW T ≫ stoneanCechTripleXY T =
    quadXYZ T ≫ stoneanCechTripleXY T := by
  exact pullback.lift_fst _ _ _

theorem quadFaceXYW_w (T : Profinite.{u}) :
    quadFaceXYW T ≫ stoneanCechTripleZ T = quadW T := by
  exact pullback.lift_snd _ _ _


/-- Remove y from the actual fourfold Čech object. -/
noncomputable def quadFaceXZW (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechTriples T := by
  let p := Profinite.presentation.π T
  refine pullback.lift
    (quadXYZ T ≫ stoneanCechTripleXZ T) (quadW T) ?_
  have hXZ : stoneanCechTripleXZ T ≫ pullback.fst p p =
      stoneanCechTripleXY T ≫ pullback.fst p p := by
    exact pullback.lift_fst _ _ _
  calc
    (quadXYZ T ≫ stoneanCechTripleXZ T) ≫ (pullback.fst p p ≫ p) =
      quadXYZ T ≫ ((stoneanCechTripleXZ T ≫ pullback.fst p p) ≫ p) := by
        simp only [Category.assoc]
    _ = quadXYZ T ≫ ((stoneanCechTripleXY T ≫ pullback.fst p p) ≫ p) := by
      rw [hXZ]
    _ = quadW T ≫ p := by
      simpa only [Category.assoc] using quad_base_condition T

/-- Remove x from the actual fourfold Čech object. -/
noncomputable def quadFaceYZW (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechTriples T := by
  let p := Profinite.presentation.π T
  refine pullback.lift
    (quadXYZ T ≫ stoneanCechTripleYZ T) (quadW T) ?_
  have hYZ : stoneanCechTripleYZ T ≫ pullback.fst p p =
      stoneanCechTripleXY T ≫ pullback.snd p p := by
    exact pullback.lift_fst _ _ _
  calc
    (quadXYZ T ≫ stoneanCechTripleYZ T) ≫ (pullback.fst p p ≫ p) =
      quadXYZ T ≫ ((stoneanCechTripleYZ T ≫ pullback.fst p p) ≫ p) := by
        simp only [Category.assoc]
    _ = quadXYZ T ≫ ((stoneanCechTripleXY T ≫ pullback.snd p p) ≫ p) := by
      rw [hYZ]
    _ = quadXYZ T ≫ ((stoneanCechTripleXY T ≫ pullback.fst p p) ≫ p) := by
      simpa only [Category.assoc] using
        congrArg (fun m : stoneanPresentationCechPairs T ⟶ T =>
          quadXYZ T ≫ (stoneanCechTripleXY T ≫ m))
          ((pullback.condition : pullback.fst p p ≫ p =
            pullback.snd p p ≫ p).symm)
    _ = quadW T ≫ p := by
      simpa only [Category.assoc] using quad_base_condition T

theorem quadFaceXZW_xz (T : Profinite.{u}) :
    quadFaceXZW T ≫ stoneanCechTripleXY T =
    quadXYZ T ≫ stoneanCechTripleXZ T := by
  exact pullback.lift_fst _ _ _

theorem quadFaceYZW_yz (T : Profinite.{u}) :
    quadFaceYZW T ≫ stoneanCechTripleXY T =
    quadXYZ T ≫ stoneanCechTripleYZ T := by
  exact pullback.lift_fst _ _ _

theorem quadFaceXZW_w (T : Profinite.{u}) :
    quadFaceXZW T ≫ stoneanCechTripleZ T = quadW T := by
  exact pullback.lift_snd _ _ _

theorem quadFaceYZW_w (T : Profinite.{u}) :
    quadFaceYZW T ≫ stoneanCechTripleZ T = quadW T := by
  exact pullback.lift_snd _ _ _


/-- The repeated x-w face of the nested categorical quadruple. -/
theorem quadFaceXZW_xw (T : Profinite.{u}) :
    quadFaceXZW T ≫ stoneanCechTripleXZ T =
      quadFaceXYW T ≫ stoneanCechTripleXZ T := by
  apply pullback.hom_ext
  · let p := Profinite.presentation.π T
    let fst := pullback.fst p p
    calc
      (quadFaceXZW T ≫ stoneanCechTripleXZ T) ≫ fst =
          (quadFaceXZW T ≫ stoneanCechTripleXY T) ≫ fst := by
            simpa only [Category.assoc] using
              congrArg (fun m : stoneanPresentationCechTriples T ⟶
                Stonean.toProfinite.obj T.presentation =>
                quadFaceXZW T ≫ m)
                (show stoneanCechTripleXZ T ≫ fst =
                  stoneanCechTripleXY T ≫ fst from
                  pullback.lift_fst _ _ _)
      _ = (quadXYZ T ≫ stoneanCechTripleXZ T) ≫ fst :=
        congrArg (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T => m ≫ fst)
          (quadFaceXZW_xz T)
      _ = (quadXYZ T ≫ stoneanCechTripleXY T) ≫ fst := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadXYZ T ≫ m)
            (show stoneanCechTripleXZ T ≫ fst =
              stoneanCechTripleXY T ≫ fst from
              pullback.lift_fst _ _ _)
      _ = (quadFaceXYW T ≫ stoneanCechTripleXY T) ≫ fst :=
        congrArg (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T => m ≫ fst)
          (quadFaceXYW_xy T).symm
      _ = (quadFaceXYW T ≫ stoneanCechTripleXZ T) ≫ fst := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadFaceXYW T ≫ m)
            (show stoneanCechTripleXZ T ≫ fst =
              stoneanCechTripleXY T ≫ fst from
              pullback.lift_fst _ _ _).symm
  · simp only [Category.assoc, stoneanCechTripleXZ,
      pullback.lift_snd, quadFaceXZW_w, quadFaceXYW_w]

/-- The repeated y-w face. -/
theorem quadFaceXYW_yw (T : Profinite.{u}) :
    quadFaceXYW T ≫ stoneanCechTripleYZ T =
      quadFaceYZW T ≫ stoneanCechTripleXZ T := by
  apply pullback.hom_ext
  · let p := Profinite.presentation.π T
    let fst := pullback.fst p p
    let snd := pullback.snd p p
    have hYZ : stoneanCechTripleYZ T ≫ fst =
        stoneanCechTripleXY T ≫ snd := pullback.lift_fst _ _ _
    have hXZ : stoneanCechTripleXZ T ≫ fst =
        stoneanCechTripleXY T ≫ fst := pullback.lift_fst _ _ _
    calc
      (quadFaceXYW T ≫ stoneanCechTripleYZ T) ≫ fst =
          (quadFaceXYW T ≫ stoneanCechTripleXY T) ≫ snd := by
            simpa only [Category.assoc] using
              congrArg (fun m : stoneanPresentationCechTriples T ⟶
                Stonean.toProfinite.obj T.presentation =>
                quadFaceXYW T ≫ m) hYZ
      _ = (quadXYZ T ≫ stoneanCechTripleXY T) ≫ snd :=
        congrArg (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T => m ≫ snd)
          (quadFaceXYW_xy T)
      _ = (quadXYZ T ≫ stoneanCechTripleYZ T) ≫ fst := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadXYZ T ≫ m) hYZ.symm
      _ = (quadFaceYZW T ≫ stoneanCechTripleXY T) ≫ fst :=
        congrArg (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T => m ≫ fst)
          (quadFaceYZW_yz T).symm
      _ = (quadFaceYZW T ≫ stoneanCechTripleXZ T) ≫ fst := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadFaceYZW T ≫ m) hXZ.symm
  · simp only [Category.assoc, stoneanCechTripleYZ,
      stoneanCechTripleXZ, pullback.lift_snd,
      quadFaceXYW_w, quadFaceYZW_w]

/-- The repeated z-w face. -/
theorem quadFaceXZW_zw (T : Profinite.{u}) :
    quadFaceXZW T ≫ stoneanCechTripleYZ T =
      quadFaceYZW T ≫ stoneanCechTripleYZ T := by
  apply pullback.hom_ext
  · let p := Profinite.presentation.π T
    let fst := pullback.fst p p
    let snd := pullback.snd p p
    have hYZ : stoneanCechTripleYZ T ≫ fst =
        stoneanCechTripleXY T ≫ snd := pullback.lift_fst _ _ _
    have hXZsnd : stoneanCechTripleXZ T ≫ snd =
        stoneanCechTripleZ T := pullback.lift_snd _ _ _
    have hYZsnd : stoneanCechTripleYZ T ≫ snd =
        stoneanCechTripleZ T := pullback.lift_snd _ _ _
    calc
      (quadFaceXZW T ≫ stoneanCechTripleYZ T) ≫ fst =
          (quadFaceXZW T ≫ stoneanCechTripleXY T) ≫ snd := by
            simpa only [Category.assoc] using
              congrArg (fun m : stoneanPresentationCechTriples T ⟶
                Stonean.toProfinite.obj T.presentation =>
                quadFaceXZW T ≫ m) hYZ
      _ = (quadXYZ T ≫ stoneanCechTripleXZ T) ≫ snd :=
        congrArg (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T => m ≫ snd)
          (quadFaceXZW_xz T)
      _ = quadXYZ T ≫ stoneanCechTripleZ T := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadXYZ T ≫ m) hXZsnd
      _ = (quadXYZ T ≫ stoneanCechTripleYZ T) ≫ snd := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadXYZ T ≫ m) hYZsnd.symm
      _ = (quadFaceYZW T ≫ stoneanCechTripleXY T) ≫ snd :=
        congrArg (fun m : stoneanPresentationCechQuadruples T ⟶
          stoneanPresentationCechPairs T => m ≫ snd)
          (quadFaceYZW_yz T).symm
      _ = (quadFaceYZW T ≫ stoneanCechTripleYZ T) ≫ fst := by
        simpa only [Category.assoc] using
          congrArg (fun m : stoneanPresentationCechTriples T ⟶
            Stonean.toProfinite.obj T.presentation =>
            quadFaceYZW T ≫ m) hYZ.symm
  · simp only [Category.assoc, stoneanCechTripleYZ,
      pullback.lift_snd, quadFaceXZW_w, quadFaceYZW_w]

/-- The genuine alternating fourfold Čech chain differential on
actual free profinite condensed modules. -/
noncomputable def stoneanCechFourthBoundary (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T) ⟶
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T) :=
  (Condensed.profiniteFree Coeff).map (quadFaceYZW T) -
    (Condensed.profiniteFree Coeff).map (quadFaceXZW T) +
    (Condensed.profiniteFree Coeff).map (quadFaceXYW T) -
    (Condensed.profiniteFree Coeff).map (quadXYZ T)

theorem stoneanCechFourthBoundary_comp_tripleBoundary_zero
    (T : Profinite.{u}) :
    stoneanCechFourthBoundary T ≫ stoneanCechTripleBoundary T = 0 := by
  unfold stoneanCechFourthBoundary stoneanCechTripleBoundary
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, ← Functor.map_comp]
  rw [quadFaceXZW_xw, quadFaceXYW_yw, quadFaceXZW_zw,
    quadFaceXZW_xz, quadFaceYZW_yz, quadFaceXYW_xy]
  abel


/-- The full categorical fourth Čech differential vanishes in the
genuine second-relation object, not merely after passing to points. -/
theorem stoneanCechFourthBoundary_comp_secondRelation_zero
    (T : Profinite.{u}) :
    stoneanCechFourthBoundary T ≫
      stoneanCechTripleToSecondRelation T = 0 := by
  apply (cancel_mono (kernel.ι (stoneanCechRelationToKernel T))).1
  rw [Category.assoc, stoneanCechTripleToSecondRelation_comp_ι,
    zero_comp]
  exact stoneanCechFourthBoundary_comp_tripleBoundary_zero T

/-- Genuine global continuous fourth-to-third relation morphism.
Its domain is the actual free condensed module on the categorical
fourfold Čech pullback, not a family of singleton point maps. -/
noncomputable def stoneanCechFourthToThirdRelation
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T) ⟶
      stoneanCechThirdRelationKernel T :=
  kernel.lift (stoneanCechTripleToSecondRelation T)
    (stoneanCechFourthBoundary T)
    (stoneanCechFourthBoundary_comp_secondRelation_zero T)

theorem stoneanCechFourthToThirdRelation_comp_inclusion
    (T : Profinite.{u}) :
    stoneanCechFourthToThirdRelation T ≫
      kernel.ι (stoneanCechTripleToSecondRelation T) =
        stoneanCechFourthBoundary T := by
  simp only [stoneanCechFourthToThirdRelation, kernel.lift_ι]

#print axioms stoneanCechFourthBoundary_comp_tripleBoundary_zero
#print axioms stoneanCechFourthBoundary_comp_secondRelation_zero
#print axioms stoneanCechFourthToThirdRelation_comp_inclusion

#print axioms quadFaceXYW_xy
#print axioms quadFaceXZW_xw
#print axioms quadFaceXYW_yw
#print axioms quadFaceXZW_zw
end CMDG.CondensedCM5R0
