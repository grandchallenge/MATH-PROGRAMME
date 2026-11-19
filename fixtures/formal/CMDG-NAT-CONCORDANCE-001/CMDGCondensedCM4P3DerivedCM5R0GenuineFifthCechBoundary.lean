import CMDGCondensedCM4P3DerivedCM5R0ExtFourFourthRelationCriterion
import CMDGCondensedCM4P3DerivedCM5R0GenuineQuadrupleRelationIso

/-!
# CM5: actual fifth Čech source, as a closed profinite fivefold relation.

The fifth Čech source is the genuine closed relation of all five
presentation points mapping to the same base point. Its five face
maps land in the already-proved actual fourth categorical pullback.
The signed fifth boundary and d4*d3=0 are proven below. The source is the closed five-point profinite relation; an explicit isomorphism to the iterated categorical fivefold pullback and global epimorphy remain separate obligations.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

def profiniteCechQuintupleRelatedSet
    (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × (P × (P × (P × P)))) :=
  {xyzwv | p.hom.hom xyzwv.1 = p.hom.hom xyzwv.2.1 ∧
    p.hom.hom xyzwv.2.1 = p.hom.hom xyzwv.2.2.1 ∧
    p.hom.hom xyzwv.2.2.1 = p.hom.hom xyzwv.2.2.2.1 ∧
    p.hom.hom xyzwv.2.2.2.1 = p.hom.hom xyzwv.2.2.2.2}

theorem profiniteCechQuintupleRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechQuintupleRelatedSet P T p) := by
  have h1 : Continuous
    (fun q : P × (P × (P × (P × P))) => p.hom.hom q.1) := by fun_prop
  have h2 : Continuous
    (fun q : P × (P × (P × (P × P))) => p.hom.hom q.2.1) := by fun_prop
  have h3 : Continuous
    (fun q : P × (P × (P × (P × P))) => p.hom.hom q.2.2.1) := by fun_prop
  have h4 : Continuous
    (fun q : P × (P × (P × (P × P))) => p.hom.hom q.2.2.2.1) := by fun_prop
  have h5 : Continuous
    (fun q : P × (P × (P × (P × P))) => p.hom.hom q.2.2.2.2) := by fun_prop
  have h12 := isClosed_eq h1 h2
  have h23 := isClosed_eq h2 h3
  have h34 := isClosed_eq h3 h4
  have h45 := isClosed_eq h4 h5
  simpa only [profiniteCechQuintupleRelatedSet, Set.setOf_and] using
    h12.inter (h23.inter (h34.inter h45))

noncomputable def stoneanCechExplicitQuintupleProfinite
    (T : Profinite.{u}) : Profinite.{u} := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact Profinite.of (↥(profiniteCechQuintupleRelatedSet P T p))

private noncomputable def quintupleFace0 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanCechExplicitQuadrupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.2.1,(q.val.2.2.1,
      (q.val.2.2.2.1,q.val.2.2.2.2))),
      ⟨q.property.2.1,q.property.2.2.1,q.property.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitQuintupleProfinite T,
        ↥(profiniteCechQuadrupleRelatedSet P T p)))

private noncomputable def quintupleFace1 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanCechExplicitQuadrupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.2.1,
      (q.val.2.2.2.1,q.val.2.2.2.2))),
      ⟨q.property.1.trans q.property.2.1,
        q.property.2.2.1,q.property.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitQuintupleProfinite T,
        ↥(profiniteCechQuadrupleRelatedSet P T p)))


private noncomputable def quintupleFace2 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanCechExplicitQuadrupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,
      (q.val.2.2.2.1,q.val.2.2.2.2))),
      ⟨q.property.1,
        q.property.2.1.trans q.property.2.2.1,q.property.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitQuintupleProfinite T,
        ↥(profiniteCechQuadrupleRelatedSet P T p)))


private noncomputable def quintupleFace3 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanCechExplicitQuadrupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,
      (q.val.2.2.1,q.val.2.2.2.2))),
      ⟨q.property.1,
        q.property.2.1,q.property.2.2.1.trans q.property.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitQuintupleProfinite T,
        ↥(profiniteCechQuadrupleRelatedSet P T p)))


private noncomputable def quintupleFace4 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanCechExplicitQuadrupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,
      (q.val.2.2.1,q.val.2.2.2.1))),
      ⟨q.property.1,q.property.2.1,q.property.2.2.1⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitQuintupleProfinite T,
        ↥(profiniteCechQuadrupleRelatedSet P T p)))



/-- Fifth face deleting one vertex, targeting the *actual* fourth
Profinite Čech pullback, via the protected categorical isomorphism. -/
noncomputable def stoneanCechFifthFace0 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuadruples T :=
  quintupleFace0 T ≫ stoneanCechExplicitQuadrupleToAbstract T

noncomputable def stoneanCechFifthFace1 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuadruples T :=
  quintupleFace1 T ≫ stoneanCechExplicitQuadrupleToAbstract T

noncomputable def stoneanCechFifthFace2 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuadruples T :=
  quintupleFace2 T ≫ stoneanCechExplicitQuadrupleToAbstract T

noncomputable def stoneanCechFifthFace3 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuadruples T :=
  quintupleFace3 T ≫ stoneanCechExplicitQuadrupleToAbstract T

noncomputable def stoneanCechFifthFace4 (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuadruples T :=
  quintupleFace4 T ≫ stoneanCechExplicitQuadrupleToAbstract T

/-- The genuine free-condensed-module alternating fifth boundary,
with all five categorical face maps on a compact profinite source. -/
noncomputable def stoneanCechFifthBoundary (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) :=
    (Condensed.profiniteFree Coeff).map (stoneanCechFifthFace0 T) -
    (Condensed.profiniteFree Coeff).map (stoneanCechFifthFace1 T) +
    (Condensed.profiniteFree Coeff).map (stoneanCechFifthFace2 T) -
    (Condensed.profiniteFree Coeff).map (stoneanCechFifthFace3 T) +
    (Condensed.profiniteFree Coeff).map (stoneanCechFifthFace4 T)

/-- First simplicial face-pair identity, on the true categorical
target: deleting x and then y equals deleting y and then x. -/
theorem stoneanCechFifthFace01_commute (T : Profinite.{u}) :
    stoneanCechFifthFace0 T ≫ quadFaceYZW T =
    stoneanCechFifthFace1 T ≫ quadFaceYZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (quadFaceYZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace0 T).hom.hom q)) =
    (quadFaceYZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace1 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_yzw_atPoint,
    stoneanCechExplicitQuadruple_yzw_atPoint]
  rfl

/-- Named genuine categorical fourth face deleting the final vertex. -/
noncomputable def stoneanCechQuadFaceXYZ (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechTriples T :=
  pullback.fst
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

theorem stoneanCechFifthFace02_commute (T : Profinite.{u}) :
    stoneanCechFifthFace0 T ≫ quadFaceXZW T =
    stoneanCechFifthFace2 T ≫ quadFaceYZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (quadFaceXZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace0 T).hom.hom q)) =
    (quadFaceYZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace2 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xzw_atPoint,
    stoneanCechExplicitQuadruple_yzw_atPoint]
  rfl

#print axioms stoneanCechFifthFace02_commute
theorem stoneanCechFifthFace04_commute (T : Profinite.{u}) :
    stoneanCechFifthFace0 T ≫ stoneanCechQuadFaceXYZ T =
    stoneanCechFifthFace4 T ≫ quadFaceYZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace0 T).hom.hom q)) =
    (quadFaceYZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace4 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_yzw_atPoint]
  exact (stoneanCechExplicitQuadruple_xyz_atPoint T
    ((quintupleFace0 T).hom.hom q)).trans (by rfl)

#print axioms stoneanCechFifthFace04_commute
theorem stoneanCechFifthFace03_commute (T : Profinite.{u}) :
    stoneanCechFifthFace0 T ≫ quadFaceXYW T =
    stoneanCechFifthFace3 T ≫ quadFaceYZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (quadFaceXYW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace0 T).hom.hom q)) =
    (quadFaceYZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace3 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xyw_atPoint, stoneanCechExplicitQuadruple_yzw_atPoint]
  rfl

#print axioms stoneanCechFifthFace03_commute

theorem stoneanCechFifthFace12_commute (T : Profinite.{u}) :
    stoneanCechFifthFace1 T ≫ quadFaceXZW T =
    stoneanCechFifthFace2 T ≫ quadFaceXZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (quadFaceXZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace1 T).hom.hom q)) =
    (quadFaceXZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace2 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xzw_atPoint, stoneanCechExplicitQuadruple_xzw_atPoint]
  rfl

#print axioms stoneanCechFifthFace12_commute

theorem stoneanCechFifthFace13_commute (T : Profinite.{u}) :
    stoneanCechFifthFace1 T ≫ quadFaceXYW T =
    stoneanCechFifthFace3 T ≫ quadFaceXZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (quadFaceXYW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace1 T).hom.hom q)) =
    (quadFaceXZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace3 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xyw_atPoint, stoneanCechExplicitQuadruple_xzw_atPoint]
  rfl

#print axioms stoneanCechFifthFace13_commute

theorem stoneanCechFifthFace14_commute (T : Profinite.{u}) :
    stoneanCechFifthFace1 T ≫ stoneanCechQuadFaceXYZ T =
    stoneanCechFifthFace4 T ≫ quadFaceXZW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace1 T).hom.hom q)) =
    (quadFaceXZW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace4 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xzw_atPoint]
  exact (stoneanCechExplicitQuadruple_xyz_atPoint T
    ((quintupleFace1 T).hom.hom q)).trans (by rfl)

#print axioms stoneanCechFifthFace14_commute

theorem stoneanCechFifthFace23_commute (T : Profinite.{u}) :
    stoneanCechFifthFace2 T ≫ quadFaceXYW T =
    stoneanCechFifthFace3 T ≫ quadFaceXYW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (quadFaceXYW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace2 T).hom.hom q)) =
    (quadFaceXYW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace3 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xyw_atPoint, stoneanCechExplicitQuadruple_xyw_atPoint]
  rfl

#print axioms stoneanCechFifthFace23_commute

theorem stoneanCechFifthFace24_commute (T : Profinite.{u}) :
    stoneanCechFifthFace2 T ≫ stoneanCechQuadFaceXYZ T =
    stoneanCechFifthFace4 T ≫ quadFaceXYW T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace2 T).hom.hom q)) =
    (quadFaceXYW T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace4 T).hom.hom q))
  rw [stoneanCechExplicitQuadruple_xyw_atPoint]
  exact (stoneanCechExplicitQuadruple_xyz_atPoint T
    ((quintupleFace2 T).hom.hom q)).trans (by rfl)

#print axioms stoneanCechFifthFace24_commute

theorem stoneanCechFifthFace34_commute (T : Profinite.{u}) :
    stoneanCechFifthFace3 T ≫ stoneanCechQuadFaceXYZ T =
    stoneanCechFifthFace4 T ≫ stoneanCechQuadFaceXYZ T := by
  apply ConcreteCategory.hom_ext
  intro q
  change (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace3 T).hom.hom q)) =
    (stoneanCechQuadFaceXYZ T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace4 T).hom.hom q))
  exact (stoneanCechExplicitQuadruple_xyz_atPoint T
    ((quintupleFace3 T).hom.hom q)).trans
    (stoneanCechExplicitQuadruple_xyz_atPoint T
      ((quintupleFace4 T).hom.hom q)).symm

#print axioms stoneanCechFifthFace34_commute


/-- The full genuine fifth/fourth Čech differential squares to zero
as an equality of free condensed-module morphisms, not merely
after evaluating integer-valued functions. -/
theorem stoneanCechFifthBoundary_comp_fourthBoundary_zero
    (T : Profinite.{u}) :
    stoneanCechFifthBoundary T ≫ stoneanCechFourthBoundary T = 0 := by
  change stoneanCechFifthBoundary T ≫
    ((Condensed.profiniteFree Coeff).map (quadFaceYZW T) -
      (Condensed.profiniteFree Coeff).map (quadFaceXZW T) +
      (Condensed.profiniteFree Coeff).map (quadFaceXYW T) -
      (Condensed.profiniteFree Coeff).map (stoneanCechQuadFaceXYZ T)) = 0
  unfold stoneanCechFifthBoundary
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub,
    ← Functor.map_comp]
  rw [stoneanCechFifthFace01_commute,
    stoneanCechFifthFace02_commute,
    stoneanCechFifthFace03_commute,
    stoneanCechFifthFace04_commute,
    stoneanCechFifthFace12_commute,
    stoneanCechFifthFace13_commute,
    stoneanCechFifthFace14_commute,
    stoneanCechFifthFace23_commute,
    stoneanCechFifthFace24_commute,
    stoneanCechFifthFace34_commute]
  abel


/-- The exact signed fifth boundary lands in the actual fourth Čech
relation, not merely in the kernel of a pointwise surrogate. -/
theorem stoneanCechFifthBoundary_comp_thirdRelation_zero
    (T : Profinite.{u}) :
    stoneanCechFifthBoundary T ≫
      stoneanCechFourthToThirdRelation T = 0 := by
  apply (cancel_mono
    (kernel.ι (stoneanCechTripleToSecondRelation T))).1
  rw [Category.assoc, stoneanCechFourthToThirdRelation_comp_inclusion,
    zero_comp]
  exact stoneanCechFifthBoundary_comp_fourthBoundary_zero T

/-- Actual fifth-to-fourth relation global morphism. The missing
research assertion is its epimorphy, not its existence or chain law. -/
noncomputable def stoneanCechFifthToFourthRelation
    (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
      stoneanCechFourthRelationKernel T :=
  kernel.lift (stoneanCechFourthToThirdRelation T)
    (stoneanCechFifthBoundary T)
    (stoneanCechFifthBoundary_comp_thirdRelation_zero T)

theorem stoneanCechFifthToFourthRelation_comp_inclusion
    (T : Profinite.{u}) :
    stoneanCechFifthToFourthRelation T ≫
      kernel.ι (stoneanCechFourthToThirdRelation T) =
        stoneanCechFifthBoundary T := by
  simp only [stoneanCechFifthToFourthRelation, kernel.lift_ι]

#print axioms stoneanCechFifthBoundary_comp_thirdRelation_zero
#print axioms stoneanCechFifthToFourthRelation_comp_inclusion
#print axioms stoneanCechFifthBoundary_comp_fourthBoundary_zero

#print axioms stoneanCechFifthFace01_commute
#print axioms profiniteCechQuintupleRelatedSet_isClosed
#print axioms quintupleFace0
#print axioms quintupleFace1
#print axioms quintupleFace2
#print axioms quintupleFace3
#print axioms quintupleFace4
end CMDG.CondensedCM5R0
