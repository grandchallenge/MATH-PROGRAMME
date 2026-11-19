import CMDGCondensedCM4P3DerivedCM5R0ExplicitClosedProductH5HomBridge
import CMDGCondensedCM4P3DerivedCM5R0GenuineSixfoldCechFaces

/-!
# CMDG CM5 — actual sevenfold equal-image relation and d7*d6=0

All seven deletion maps are genuine continuous Profinite morphisms.
All 21 simplicial identities and full signed free-condensed-module
boundary-square zero are proved. No assumption of Ext5 vanishing.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

def profiniteCechSeptupleRelatedSet
    (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × (P × (P × (P × (P × (P × P)))))) :=
  {q | p.hom.hom q.1 = p.hom.hom q.2.1 ∧
    p.hom.hom q.2.1 = p.hom.hom q.2.2.1 ∧
    p.hom.hom q.2.2.1 = p.hom.hom q.2.2.2.1 ∧
    p.hom.hom q.2.2.2.1 = p.hom.hom q.2.2.2.2.1 ∧
    p.hom.hom q.2.2.2.2.1 = p.hom.hom q.2.2.2.2.2.1 ∧
    p.hom.hom q.2.2.2.2.2.1 = p.hom.hom q.2.2.2.2.2.2}

theorem profiniteCechSeptupleRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechSeptupleRelatedSet P T p) := by
  have c0 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.1) := by fun_prop
  have c1 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.2.1) := by fun_prop
  have c2 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.2.2.1) := by fun_prop
  have c3 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.2.2.2.1) := by fun_prop
  have c4 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.2.2.2.2.1) := by fun_prop
  have c5 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.2.2.2.2.2.1) := by fun_prop
  have c6 : Continuous (fun q : P × (P × (P × (P × (P × (P × P))))) => p.hom.hom q.2.2.2.2.2.2) := by fun_prop
  have h0 := isClosed_eq c0 c1
  have h1 := isClosed_eq c1 c2
  have h2 := isClosed_eq c2 c3
  have h3 := isClosed_eq c3 c4
  have h4 := isClosed_eq c4 c5
  have h5 := isClosed_eq c5 c6
  simpa only [profiniteCechSeptupleRelatedSet, Set.setOf_and] using
    h0.inter (h1.inter (h2.inter (h3.inter (h4.inter h5))))

noncomputable def stoneanCechExplicitSeptupleProfinite
    (T : Profinite.{u}) : Profinite.{u} := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  exact Profinite.of (↥(profiniteCechSeptupleRelatedSet P T p))

/-- Genuine Profinite septuple deletion face 0. -/
noncomputable def septupleFace0 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,(q.val.2.2.2.2.2.1,q.val.2.2.2.2.2.2))))), ⟨q.property.2.1,q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2.1,q.property.2.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine Profinite septuple deletion face 1. -/
noncomputable def septupleFace1 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,(q.val.2.2.2.2.2.1,q.val.2.2.2.2.2.2))))), ⟨(q.property.1.trans q.property.2.1),q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2.1,q.property.2.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine Profinite septuple deletion face 2. -/
noncomputable def septupleFace2 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,(q.val.2.2.2.2.2.1,q.val.2.2.2.2.2.2))))), ⟨q.property.1,(q.property.2.1.trans q.property.2.2.1),q.property.2.2.2.1,q.property.2.2.2.2.1,q.property.2.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine Profinite septuple deletion face 3. -/
noncomputable def septupleFace3 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.2.1,(q.val.2.2.2.2.2.1,q.val.2.2.2.2.2.2))))), ⟨q.property.1,q.property.2.1,(q.property.2.2.1.trans q.property.2.2.2.1),q.property.2.2.2.2.1,q.property.2.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine Profinite septuple deletion face 4. -/
noncomputable def septupleFace4 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.2.1,q.val.2.2.2.2.2.2))))), ⟨q.property.1,q.property.2.1,q.property.2.2.1,(q.property.2.2.2.1.trans q.property.2.2.2.2.1),q.property.2.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine Profinite septuple deletion face 5. -/
noncomputable def septupleFace5 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2.2))))), ⟨q.property.1,q.property.2.1,q.property.2.2.1,q.property.2.2.2.1,(q.property.2.2.2.2.1.trans q.property.2.2.2.2.2)⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine Profinite septuple deletion face 6. -/
noncomputable def septupleFace6 (T : Profinite.{u}) :
    stoneanCechExplicitSeptupleProfinite T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSeptupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSeptupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2.1))))), ⟨q.property.1,q.property.2.1,q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2.1⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSeptupleProfinite T,
        ↥(profiniteCechSextupleRelatedSet P T p)))

/-- Genuine signed seven-face condensed free-module boundary. -/
noncomputable def stoneanCechSeventhBoundary (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSeptupleProfinite T)) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) :=
    (Condensed.profiniteFree Coeff).map (septupleFace0 T)
    - (Condensed.profiniteFree Coeff).map (septupleFace1 T)
    + (Condensed.profiniteFree Coeff).map (septupleFace2 T)
    - (Condensed.profiniteFree Coeff).map (septupleFace3 T)
    + (Condensed.profiniteFree Coeff).map (septupleFace4 T)
    - (Condensed.profiniteFree Coeff).map (septupleFace5 T)
    + (Condensed.profiniteFree Coeff).map (septupleFace6 T)

/-- True sevenfold simplicial face-pair identity (0,1). -/
theorem septupleSimplicialFace01 (T : Profinite.{u}) :
    septupleFace0 T ≫ sextupleFace0 T =
    septupleFace1 T ≫ sextupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (0,2). -/
theorem septupleSimplicialFace02 (T : Profinite.{u}) :
    septupleFace0 T ≫ sextupleFace1 T =
    septupleFace2 T ≫ sextupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (0,3). -/
theorem septupleSimplicialFace03 (T : Profinite.{u}) :
    septupleFace0 T ≫ sextupleFace2 T =
    septupleFace3 T ≫ sextupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (0,4). -/
theorem septupleSimplicialFace04 (T : Profinite.{u}) :
    septupleFace0 T ≫ sextupleFace3 T =
    septupleFace4 T ≫ sextupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (0,5). -/
theorem septupleSimplicialFace05 (T : Profinite.{u}) :
    septupleFace0 T ≫ sextupleFace4 T =
    septupleFace5 T ≫ sextupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (0,6). -/
theorem septupleSimplicialFace06 (T : Profinite.{u}) :
    septupleFace0 T ≫ sextupleFace5 T =
    septupleFace6 T ≫ sextupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (1,2). -/
theorem septupleSimplicialFace12 (T : Profinite.{u}) :
    septupleFace1 T ≫ sextupleFace1 T =
    septupleFace2 T ≫ sextupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (1,3). -/
theorem septupleSimplicialFace13 (T : Profinite.{u}) :
    septupleFace1 T ≫ sextupleFace2 T =
    septupleFace3 T ≫ sextupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (1,4). -/
theorem septupleSimplicialFace14 (T : Profinite.{u}) :
    septupleFace1 T ≫ sextupleFace3 T =
    septupleFace4 T ≫ sextupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (1,5). -/
theorem septupleSimplicialFace15 (T : Profinite.{u}) :
    septupleFace1 T ≫ sextupleFace4 T =
    septupleFace5 T ≫ sextupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (1,6). -/
theorem septupleSimplicialFace16 (T : Profinite.{u}) :
    septupleFace1 T ≫ sextupleFace5 T =
    septupleFace6 T ≫ sextupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (2,3). -/
theorem septupleSimplicialFace23 (T : Profinite.{u}) :
    septupleFace2 T ≫ sextupleFace2 T =
    septupleFace3 T ≫ sextupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (2,4). -/
theorem septupleSimplicialFace24 (T : Profinite.{u}) :
    septupleFace2 T ≫ sextupleFace3 T =
    septupleFace4 T ≫ sextupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (2,5). -/
theorem septupleSimplicialFace25 (T : Profinite.{u}) :
    septupleFace2 T ≫ sextupleFace4 T =
    septupleFace5 T ≫ sextupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (2,6). -/
theorem septupleSimplicialFace26 (T : Profinite.{u}) :
    septupleFace2 T ≫ sextupleFace5 T =
    septupleFace6 T ≫ sextupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (3,4). -/
theorem septupleSimplicialFace34 (T : Profinite.{u}) :
    septupleFace3 T ≫ sextupleFace3 T =
    septupleFace4 T ≫ sextupleFace3 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (3,5). -/
theorem septupleSimplicialFace35 (T : Profinite.{u}) :
    septupleFace3 T ≫ sextupleFace4 T =
    septupleFace5 T ≫ sextupleFace3 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (3,6). -/
theorem septupleSimplicialFace36 (T : Profinite.{u}) :
    septupleFace3 T ≫ sextupleFace5 T =
    septupleFace6 T ≫ sextupleFace3 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (4,5). -/
theorem septupleSimplicialFace45 (T : Profinite.{u}) :
    septupleFace4 T ≫ sextupleFace4 T =
    septupleFace5 T ≫ sextupleFace4 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (4,6). -/
theorem septupleSimplicialFace46 (T : Profinite.{u}) :
    septupleFace4 T ≫ sextupleFace5 T =
    septupleFace6 T ≫ sextupleFace4 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- True sevenfold simplicial face-pair identity (5,6). -/
theorem septupleSimplicialFace56 (T : Profinite.{u}) :
    septupleFace5 T ≫ sextupleFace5 T =
    septupleFace6 T ≫ sextupleFace5 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

theorem stoneanCechSeventhBoundary_comp_sixthBoundary_zero
    (T : Profinite.{u}) :
    stoneanCechSeventhBoundary T ≫ stoneanCechSixthBoundary T = 0 := by
  unfold stoneanCechSeventhBoundary stoneanCechSixthBoundary
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub, ← Functor.map_comp]
  rw [septupleSimplicialFace01 T, septupleSimplicialFace02 T, septupleSimplicialFace03 T, septupleSimplicialFace04 T, septupleSimplicialFace05 T, septupleSimplicialFace06 T, septupleSimplicialFace12 T, septupleSimplicialFace13 T, septupleSimplicialFace14 T, septupleSimplicialFace15 T, septupleSimplicialFace16 T, septupleSimplicialFace23 T, septupleSimplicialFace24 T, septupleSimplicialFace25 T, septupleSimplicialFace26 T, septupleSimplicialFace34 T, septupleSimplicialFace35 T, septupleSimplicialFace36 T, septupleSimplicialFace45 T, septupleSimplicialFace46 T, septupleSimplicialFace56 T]
  simp only [sub_eq_add_neg]
  abel

#print axioms stoneanCechSeventhBoundary_comp_sixthBoundary_zero
end CMDG.CondensedCM5R0
