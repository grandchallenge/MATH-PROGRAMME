import CMDGCondensedCM4P3DerivedCM5R0ExtFourFourthRelationCriterion
import CMDGCondensedCM4P3DerivedCM5R0GenuineQuadrupleRelationIso

/-!
# CM5: actual fifth Čech source, as a closed profinite fivefold relation.

The fifth Čech source is the genuine closed relation of all five
presentation points mapping to the same base point. Its five face
maps land in the already-proved actual fourth categorical pullback.
The signed fifth boundary and d4*d3=0 are proven below. The source is the closed five-point profinite relation; the explicit isomorphism to the iterated categorical fivefold pullback is proved below; global epimorphy remains separate.
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

noncomputable def quintupleFace0 (T : Profinite.{u}) :
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

noncomputable def quintupleFace1 (T : Profinite.{u}) :
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


noncomputable def quintupleFace2 (T : Profinite.{u}) :
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


noncomputable def quintupleFace3 (T : Profinite.{u}) :
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


noncomputable def quintupleFace4 (T : Profinite.{u}) :
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

/-- The first vertex of the genuine fourth categorical Čech pullback. -/
noncomputable def stoneanCechQuadrupleVertexFirst (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      Stonean.toProfinite.obj T.presentation :=
  stoneanCechQuadFaceXYZ T ≫ stoneanCechTripleXY T ≫
    pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T)

/-- The actual fifth iterated categorical Čech pullback object. -/
noncomputable def stoneanPresentationCechQuintuples (T : Profinite.{u}) :
    Profinite.{u} :=
  pullback (stoneanCechQuadrupleVertexFirst T ≫
    Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The closed quadruple's first vertex is respected by its proved
actual categorical fourth pullback isomorphism. -/
theorem stoneanCechQuadrupleVertexFirst_atClosed
    (T : Profinite.{u})
    (r : stoneanCechExplicitQuadrupleProfinite T) :
    (stoneanCechQuadrupleVertexFirst T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r) =
        r.val.1 := by
  change (pullback.fst (Profinite.presentation.π T)
    (Profinite.presentation.π T)).hom.hom
    ((stoneanCechTripleXY T).hom.hom
      ((stoneanCechQuadFaceXYZ T).hom.hom
        ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r))) =
    r.val.1
  have h := stoneanCechExplicitQuadruple_xyz_atPoint T r
  rw [show (stoneanCechQuadFaceXYZ T).hom.hom
    ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r) =
    stoneanCechTripleOfRelated T
      r.val.1 r.val.2.1 r.val.2.2.1
      r.property.1 r.property.2.1 from h]
  rw [stoneanCechTripleOfRelated_xy,
    stoneanCechPairOfRelated_fst]


noncomputable def explicitQuintupleFifth (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨fun q => q.val.2.2.2.2,
    by fun_prop⟩ : C(stoneanCechExplicitQuintupleProfinite T, P))

/-- Source normalization into the actual iterated fifth Profinite pullback. -/
noncomputable def stoneanCechExplicitQuintupleToAbstract (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuintuples T := by
  let p := Profinite.presentation.π T
  let a := quintupleFace4 T ≫ stoneanCechExplicitQuadrupleToAbstract T
  let b := explicitQuintupleFifth T
  have h : a ≫ (stoneanCechQuadrupleVertexFirst T ≫ p) = b ≫ p := by
    apply ConcreteCategory.hom_ext
    intro z
    change p.hom.hom ((stoneanCechQuadrupleVertexFirst T).hom.hom
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom
        ((quintupleFace4 T).hom.hom z))) =
      p.hom.hom ((explicitQuintupleFifth T).hom.hom z)
    rw [stoneanCechQuadrupleVertexFirst_atClosed]
    have hf : ((quintupleFace4 T).hom.hom z).val.1 = z.val.1 := rfl
    have hv : (explicitQuintupleFifth T).hom.hom z = z.val.2.2.2.2 := rfl
    rw [hf,hv]
    exact z.property.1.trans
      (z.property.2.1.trans
       (z.property.2.2.1.trans z.property.2.2.2))
  exact pullback.lift a b h

theorem stoneanCechExplicitQuintupleToAbstract_first (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleToAbstract T ≫
      pullback.fst
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
      quintupleFace4 T ≫ stoneanCechExplicitQuadrupleToAbstract T := by
  unfold stoneanCechExplicitQuintupleToAbstract
  exact pullback.lift_fst _ _ _

theorem stoneanCechExplicitQuintupleToAbstract_fifth (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleToAbstract T ≫
      pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) = explicitQuintupleFifth T := by
  unfold stoneanCechExplicitQuintupleToAbstract
  exact pullback.lift_snd _ _ _


/-- The reverse map from the fifth iterated *categorical* Profinite
pullback to its compact five-vertex closed relation. -/
noncomputable def stoneanCechCategoricalQuintupleToExplicit (T : Profinite.{u}) :
    stoneanPresentationCechQuintuples T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ p) p
  let W := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ p) p
  let B := stoneanCechCategoricalQuadrupleToExplicit T
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  have hlast (z : stoneanPresentationCechQuintuples T) :
      p.hom.hom ((B.hom.hom (F.hom.hom z)).val.2.2.2) =
      p.hom.hom (W.hom.hom z) := by
    have h := stoneanCechQuadrupleVertexFirst_atClosed T
      (B.hom.hom (F.hom.hom z))
    have hBA := congrArg (fun f :
        stoneanPresentationCechQuadruples T ⟶
        stoneanPresentationCechQuadruples T =>
        f.hom.hom (F.hom.hom z))
      (stoneanCechCategoricalQuadruple_roundtrip T)
    change (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      (B.hom.hom (F.hom.hom z)) = F.hom.hom z at hBA
    rw [hBA] at h
    have hf : (stoneanCechQuadrupleVertexFirst T ≫ p).hom.hom
        (F.hom.hom z) = p.hom.hom (W.hom.hom z) := by
      have ht := congrArg
        (fun k : stoneanPresentationCechQuintuples T ⟶ T =>
          k.hom.hom z)
        (pullback.condition :
          F ≫ (stoneanCechQuadrupleVertexFirst T ≫ p) = W ≫ p)
      exact ht
    change p.hom.hom
      ((stoneanCechQuadrupleVertexFirst T).hom.hom (F.hom.hom z)) =
      p.hom.hom (W.hom.hom z) at hf
    exact ((B.hom.hom (F.hom.hom z)).property.1.trans
      ((B.hom.hom (F.hom.hom z)).property.2.1.trans
      (B.hom.hom (F.hom.hom z)).property.2.2)).symm.trans
        ((congrArg p.hom.hom h).trans hf)
  let c : C(stoneanPresentationCechQuintuples T,
      ↥(profiniteCechQuintupleRelatedSet P T p)) := by
    refine ⟨fun z =>
      ⟨((B.hom.hom (F.hom.hom z)).val.1,
         ((B.hom.hom (F.hom.hom z)).val.2.1,
           ((B.hom.hom (F.hom.hom z)).val.2.2.1,
             ((B.hom.hom (F.hom.hom z)).val.2.2.2,
               W.hom.hom z)))),
        ⟨(B.hom.hom (F.hom.hom z)).property.1,
         (B.hom.hom (F.hom.hom z)).property.2.1,
         (B.hom.hom (F.hom.hom z)).property.2.2,
         hlast z⟩⟩, ?_⟩
    apply Continuous.subtype_mk
    let tr : stoneanPresentationCechQuintuples T ⟶
      stoneanCechExplicitQuadrupleProfinite T := F ≫ B
    have htr : Continuous (fun z : stoneanPresentationCechQuintuples T =>
      (B.hom.hom (F.hom.hom z)).val) :=
      continuous_subtype_val.comp tr.hom.hom.continuous
    exact (continuous_fst.comp htr).prodMk
      ((continuous_fst.comp (continuous_snd.comp htr)).prodMk
        ((continuous_fst.comp
          (continuous_snd.comp (continuous_snd.comp htr))).prodMk
          ((continuous_snd.comp
            (continuous_snd.comp (continuous_snd.comp htr))).prodMk
            W.hom.hom.continuous)))
  exact CompHausLike.ofHom _ c


theorem stoneanCechExplicitQuintuple_roundtrip (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleToAbstract T ≫
      stoneanCechCategoricalQuintupleToExplicit T =
        𝟙 (stoneanCechExplicitQuintupleProfinite T) := by
  apply ConcreteCategory.hom_ext
  intro z
  apply Subtype.ext
  change ((stoneanCechCategoricalQuintupleToExplicit T).hom.hom
    ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z)).val = z.val
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let A4 := stoneanCechExplicitQuadrupleToAbstract T
  let B4 := stoneanCechCategoricalQuadrupleToExplicit T
  have hf := congrArg (fun f :
      stoneanCechExplicitQuintupleProfinite T ⟶
        stoneanPresentationCechQuadruples T => f.hom.hom z)
      (stoneanCechExplicitQuintupleToAbstract_first T)
  change F.hom.hom ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z) =
    A4.hom.hom ((quintupleFace4 T).hom.hom z) at hf
  have hw := congrArg (fun f :
      stoneanCechExplicitQuintupleProfinite T ⟶
        Stonean.toProfinite.obj T.presentation => f.hom.hom z)
      (stoneanCechExplicitQuintupleToAbstract_fifth T)
  change W.hom.hom ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z) =
    (explicitQuintupleFifth T).hom.hom z at hw
  have hB4 := congrArg (fun f :
      stoneanCechExplicitQuadrupleProfinite T ⟶
        stoneanCechExplicitQuadrupleProfinite T =>
        f.hom.hom ((quintupleFace4 T).hom.hom z))
      (stoneanCechExplicitQuadruple_roundtrip T)
  change B4.hom.hom (A4.hom.hom ((quintupleFace4 T).hom.hom z)) =
    (quintupleFace4 T).hom.hom z at hB4
  change
      ((B4.hom.hom (F.hom.hom
        ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z))).val.1,
      ((B4.hom.hom (F.hom.hom
        ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z))).val.2.1,
       ((B4.hom.hom (F.hom.hom
        ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z))).val.2.2.1,
        ((B4.hom.hom (F.hom.hom
        ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z))).val.2.2.2,
          W.hom.hom ((stoneanCechExplicitQuintupleToAbstract T).hom.hom z))))) =
      z.val
  rw [hf,hB4,hw]
  have h4 : ((quintupleFace4 T).hom.hom z).val =
    (z.val.1,(z.val.2.1,(z.val.2.2.1,z.val.2.2.2.1))) := rfl
  have h5 : (explicitQuintupleFifth T).hom.hom z = z.val.2.2.2.2 := rfl
  rw [h4,h5]


theorem stoneanCechCategoricalQuintuple_roundtrip (T : Profinite.{u}) :
    stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechExplicitQuintupleToAbstract T =
        𝟙 (stoneanPresentationCechQuintuples T) := by
  let p := Profinite.presentation.π T
  let F := pullback.fst (stoneanCechQuadrupleVertexFirst T ≫ p) p
  let W := pullback.snd (stoneanCechQuadrupleVertexFirst T ≫ p) p
  let A := stoneanCechExplicitQuintupleToAbstract T
  let B := stoneanCechCategoricalQuintupleToExplicit T
  let A4 := stoneanCechExplicitQuadrupleToAbstract T
  let B4 := stoneanCechCategoricalQuadrupleToExplicit T
  let E := quintupleFace4 T
  let V := explicitQuintupleFifth T
  have hf : B ≫ E = F ≫ B4 := by
    apply ConcreteCategory.hom_ext
    intro z
    apply Subtype.ext
    change (E.hom.hom (B.hom.hom z)).val =
      (B4.hom.hom (F.hom.hom z)).val
    rfl
  have hw : B ≫ V = W := by
    apply ConcreteCategory.hom_ext
    intro z
    change V.hom.hom (B.hom.hom z) = W.hom.hom z
    rfl
  apply pullback.hom_ext
  · apply ConcreteCategory.hom_ext
    intro z
    change F.hom.hom (A.hom.hom (B.hom.hom z)) = F.hom.hom z
    have h := congrArg (fun m :
        stoneanCechExplicitQuintupleProfinite T ⟶
        stoneanPresentationCechQuadruples T =>
          m.hom.hom (B.hom.hom z))
       (stoneanCechExplicitQuintupleToAbstract_first T)
    change F.hom.hom (A.hom.hom (B.hom.hom z)) =
        A4.hom.hom (E.hom.hom (B.hom.hom z)) at h
    rw [h]
    have he := congrArg (fun m :
      stoneanPresentationCechQuintuples T ⟶
      stoneanCechExplicitQuadrupleProfinite T =>
        m.hom.hom z) hf
    change E.hom.hom (B.hom.hom z) =
      B4.hom.hom (F.hom.hom z) at he
    rw [he]
    have hr := congrArg (fun m :
      stoneanPresentationCechQuadruples T ⟶
      stoneanPresentationCechQuadruples T =>
        m.hom.hom (F.hom.hom z))
      (stoneanCechCategoricalQuadruple_roundtrip T)
    exact hr
  · apply ConcreteCategory.hom_ext
    intro z
    change W.hom.hom (A.hom.hom (B.hom.hom z)) = W.hom.hom z
    have h := congrArg (fun m :
        stoneanCechExplicitQuintupleProfinite T ⟶
        Stonean.toProfinite.obj T.presentation =>
          m.hom.hom (B.hom.hom z))
       (stoneanCechExplicitQuintupleToAbstract_fifth T)
    change W.hom.hom (A.hom.hom (B.hom.hom z)) =
      V.hom.hom (B.hom.hom z) at h
    rw [h]
    have he := congrArg (fun m :
      stoneanPresentationCechQuintuples T ⟶
      Stonean.toProfinite.obj T.presentation =>
        m.hom.hom z) hw
    exact he

noncomputable def stoneanCechExplicitQuintupleIso (T : Profinite.{u}) :
    stoneanCechExplicitQuintupleProfinite T ≅
      stoneanPresentationCechQuintuples T where
  hom := stoneanCechExplicitQuintupleToAbstract T
  inv := stoneanCechCategoricalQuintupleToExplicit T
  hom_inv_id := stoneanCechExplicitQuintuple_roundtrip T
  inv_hom_id := stoneanCechCategoricalQuintuple_roundtrip T

#print axioms stoneanCechCategoricalQuintuple_roundtrip
#print axioms stoneanCechExplicitQuintupleIso
#print axioms stoneanCechExplicitQuintuple_roundtrip
#print axioms stoneanCechCategoricalQuintupleToExplicit
#print axioms stoneanCechExplicitQuintupleToAbstract_first
#print axioms stoneanCechExplicitQuintupleToAbstract_fifth
#print axioms stoneanCechQuadrupleVertexFirst_atClosed

#print axioms stoneanCechFifthBoundary_comp_fourthBoundary_zero

#print axioms stoneanCechFifthFace01_commute
#print axioms profiniteCechQuintupleRelatedSet_isClosed
#print axioms quintupleFace0
#print axioms quintupleFace1
#print axioms quintupleFace2
#print axioms quintupleFace3
#print axioms quintupleFace4
end CMDG.CondensedCM5R0
