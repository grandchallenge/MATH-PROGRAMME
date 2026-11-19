import CMDGCondensedCM4P3DerivedCM5R0ExtFiveRelationReduction
import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthCechBoundary

/-!
# CM5: actual sixfold profinite fibre product and its six honest face maps

The source is the closed equal-image six-tuple over the actual Stonean
presentation. Every deletion face is a continuous Profinite morphism into
the true fivefold relation. No abstract cohomological exactness or Ext5
vanishing is asserted here.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

def profiniteCechSextupleRelatedSet
    (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × (P × (P × (P × (P × P))))) :=
  {q | p.hom.hom q.1 = p.hom.hom q.2.1 ∧
    p.hom.hom q.2.1 = p.hom.hom q.2.2.1 ∧
    p.hom.hom q.2.2.1 = p.hom.hom q.2.2.2.1 ∧
    p.hom.hom q.2.2.2.1 = p.hom.hom q.2.2.2.2.1 ∧
    p.hom.hom q.2.2.2.2.1 = p.hom.hom q.2.2.2.2.2}

theorem profiniteCechSextupleRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechSextupleRelatedSet P T p) := by
  have c0 : Continuous (fun q : P × (P × (P × (P × (P × P)))) => p.hom.hom q.1) := by fun_prop
  have c1 : Continuous (fun q : P × (P × (P × (P × (P × P)))) => p.hom.hom q.2.1) := by fun_prop
  have c2 : Continuous (fun q : P × (P × (P × (P × (P × P)))) => p.hom.hom q.2.2.1) := by fun_prop
  have c3 : Continuous (fun q : P × (P × (P × (P × (P × P)))) => p.hom.hom q.2.2.2.1) := by fun_prop
  have c4 : Continuous (fun q : P × (P × (P × (P × (P × P)))) => p.hom.hom q.2.2.2.2.1) := by fun_prop
  have c5 : Continuous (fun q : P × (P × (P × (P × (P × P)))) => p.hom.hom q.2.2.2.2.2) := by fun_prop
  have h0 := isClosed_eq c0 c1
  have h1 := isClosed_eq c1 c2
  have h2 := isClosed_eq c2 c3
  have h3 := isClosed_eq c3 c4
  have h4 := isClosed_eq c4 c5
  simpa only [profiniteCechSextupleRelatedSet, Set.setOf_and] using
    h0.inter (h1.inter (h2.inter (h3.inter h4)))

noncomputable def stoneanCechExplicitSextupleProfinite
    (T : Profinite.{u}) : Profinite.{u} := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact Profinite.of (↥(profiniteCechSextupleRelatedSet P T p))

/-- Delete vertex 0 from the genuine closed sixfold fibre relation. -/
noncomputable def sextupleFace0 (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))),
      ⟨q.property.2.1,q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSextupleProfinite T,
        ↥(profiniteCechQuintupleRelatedSet P T p)))

/-- Delete vertex 1 from the genuine closed sixfold fibre relation. -/
noncomputable def sextupleFace1 (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))),
      ⟨(q.property.1.trans q.property.2.1),q.property.2.2.1,q.property.2.2.2.1,q.property.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSextupleProfinite T,
        ↥(profiniteCechQuintupleRelatedSet P T p)))

/-- Delete vertex 2 from the genuine closed sixfold fibre relation. -/
noncomputable def sextupleFace2 (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))),
      ⟨q.property.1,(q.property.2.1.trans q.property.2.2.1),q.property.2.2.2.1,q.property.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSextupleProfinite T,
        ↥(profiniteCechQuintupleRelatedSet P T p)))

/-- Delete vertex 3 from the genuine closed sixfold fibre relation. -/
noncomputable def sextupleFace3 (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.2.1,q.val.2.2.2.2.2)))),
      ⟨q.property.1,q.property.2.1,(q.property.2.2.1.trans q.property.2.2.2.1),q.property.2.2.2.2⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSextupleProfinite T,
        ↥(profiniteCechQuintupleRelatedSet P T p)))

/-- Delete vertex 4 from the genuine closed sixfold fibre relation. -/
noncomputable def sextupleFace4 (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,q.val.2.2.2.2.2)))),
      ⟨q.property.1,q.property.2.1,q.property.2.2.1,(q.property.2.2.2.1.trans q.property.2.2.2.2)⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSextupleProfinite T,
        ↥(profiniteCechQuintupleRelatedSet P T p)))

/-- Delete vertex 5 from the genuine closed sixfold fibre relation. -/
noncomputable def sextupleFace5 (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanCechExplicitQuintupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  letI : CompactSpace
      (↥(profiniteCechQuintupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuintupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨
    fun q => ⟨(q.val.1,(q.val.2.1,(q.val.2.2.1,(q.val.2.2.2.1,q.val.2.2.2.2.1)))),
      ⟨q.property.1,q.property.2.1,q.property.2.2.1,q.property.2.2.2.1⟩⟩,
    by apply Continuous.subtype_mk; fun_prop⟩ :
      C(stoneanCechExplicitSextupleProfinite T,
        ↥(profiniteCechQuintupleRelatedSet P T p)))

/-- True six-face free-condensed-module alternating boundary.
The codomain is the actual fivefold Čech source, not a surrogate set. -/
noncomputable def stoneanCechSixthBoundary (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) :=
    (Condensed.profiniteFree Coeff).map (sextupleFace0 T)
    - (Condensed.profiniteFree Coeff).map (sextupleFace1 T)
    + (Condensed.profiniteFree Coeff).map (sextupleFace2 T)
    - (Condensed.profiniteFree Coeff).map (sextupleFace3 T)
    + (Condensed.profiniteFree Coeff).map (sextupleFace4 T)
    - (Condensed.profiniteFree Coeff).map (sextupleFace5 T)

/-- The (0,1) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace01 (T : Profinite.{u}) :
    sextupleFace0 T ≫ quintupleFace0 T =
    sextupleFace1 T ≫ quintupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (0,2) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace02 (T : Profinite.{u}) :
    sextupleFace0 T ≫ quintupleFace1 T =
    sextupleFace2 T ≫ quintupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (0,3) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace03 (T : Profinite.{u}) :
    sextupleFace0 T ≫ quintupleFace2 T =
    sextupleFace3 T ≫ quintupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (0,4) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace04 (T : Profinite.{u}) :
    sextupleFace0 T ≫ quintupleFace3 T =
    sextupleFace4 T ≫ quintupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (0,5) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace05 (T : Profinite.{u}) :
    sextupleFace0 T ≫ quintupleFace4 T =
    sextupleFace5 T ≫ quintupleFace0 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (1,2) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace12 (T : Profinite.{u}) :
    sextupleFace1 T ≫ quintupleFace1 T =
    sextupleFace2 T ≫ quintupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (1,3) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace13 (T : Profinite.{u}) :
    sextupleFace1 T ≫ quintupleFace2 T =
    sextupleFace3 T ≫ quintupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (1,4) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace14 (T : Profinite.{u}) :
    sextupleFace1 T ≫ quintupleFace3 T =
    sextupleFace4 T ≫ quintupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (1,5) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace15 (T : Profinite.{u}) :
    sextupleFace1 T ≫ quintupleFace4 T =
    sextupleFace5 T ≫ quintupleFace1 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (2,3) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace23 (T : Profinite.{u}) :
    sextupleFace2 T ≫ quintupleFace2 T =
    sextupleFace3 T ≫ quintupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (2,4) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace24 (T : Profinite.{u}) :
    sextupleFace2 T ≫ quintupleFace3 T =
    sextupleFace4 T ≫ quintupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (2,5) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace25 (T : Profinite.{u}) :
    sextupleFace2 T ≫ quintupleFace4 T =
    sextupleFace5 T ≫ quintupleFace2 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (3,4) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace34 (T : Profinite.{u}) :
    sextupleFace3 T ≫ quintupleFace3 T =
    sextupleFace4 T ≫ quintupleFace3 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (3,5) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace35 (T : Profinite.{u}) :
    sextupleFace3 T ≫ quintupleFace4 T =
    sextupleFace5 T ≫ quintupleFace3 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (4,5) simplicial face identity on the *actual*
profinite sixfold equal-image relation. -/
theorem sextupleSimplicialFace45 (T : Profinite.{u}) :
    sextupleFace4 T ≫ quintupleFace4 T =
    sextupleFace5 T ≫ quintupleFace4 T := by
  apply ConcreteCategory.hom_ext
  intro q
  rfl

/-- The (0,1) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace01 (T : Profinite.{u}) :
    sextupleFace0 T ≫ stoneanCechFifthFace0 T =
    sextupleFace1 T ≫ stoneanCechFifthFace0 T := by
  simp only [stoneanCechFifthFace0, stoneanCechFifthFace0]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace01 T]

/-- The (0,2) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace02 (T : Profinite.{u}) :
    sextupleFace0 T ≫ stoneanCechFifthFace1 T =
    sextupleFace2 T ≫ stoneanCechFifthFace0 T := by
  simp only [stoneanCechFifthFace1, stoneanCechFifthFace0]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace02 T]

/-- The (0,3) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace03 (T : Profinite.{u}) :
    sextupleFace0 T ≫ stoneanCechFifthFace2 T =
    sextupleFace3 T ≫ stoneanCechFifthFace0 T := by
  simp only [stoneanCechFifthFace2, stoneanCechFifthFace0]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace03 T]

/-- The (0,4) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace04 (T : Profinite.{u}) :
    sextupleFace0 T ≫ stoneanCechFifthFace3 T =
    sextupleFace4 T ≫ stoneanCechFifthFace0 T := by
  simp only [stoneanCechFifthFace3, stoneanCechFifthFace0]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace04 T]

/-- The (0,5) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace05 (T : Profinite.{u}) :
    sextupleFace0 T ≫ stoneanCechFifthFace4 T =
    sextupleFace5 T ≫ stoneanCechFifthFace0 T := by
  simp only [stoneanCechFifthFace4, stoneanCechFifthFace0]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace05 T]

/-- The (1,2) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace12 (T : Profinite.{u}) :
    sextupleFace1 T ≫ stoneanCechFifthFace1 T =
    sextupleFace2 T ≫ stoneanCechFifthFace1 T := by
  simp only [stoneanCechFifthFace1, stoneanCechFifthFace1]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace12 T]

/-- The (1,3) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace13 (T : Profinite.{u}) :
    sextupleFace1 T ≫ stoneanCechFifthFace2 T =
    sextupleFace3 T ≫ stoneanCechFifthFace1 T := by
  simp only [stoneanCechFifthFace2, stoneanCechFifthFace1]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace13 T]

/-- The (1,4) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace14 (T : Profinite.{u}) :
    sextupleFace1 T ≫ stoneanCechFifthFace3 T =
    sextupleFace4 T ≫ stoneanCechFifthFace1 T := by
  simp only [stoneanCechFifthFace3, stoneanCechFifthFace1]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace14 T]

/-- The (1,5) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace15 (T : Profinite.{u}) :
    sextupleFace1 T ≫ stoneanCechFifthFace4 T =
    sextupleFace5 T ≫ stoneanCechFifthFace1 T := by
  simp only [stoneanCechFifthFace4, stoneanCechFifthFace1]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace15 T]

/-- The (2,3) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace23 (T : Profinite.{u}) :
    sextupleFace2 T ≫ stoneanCechFifthFace2 T =
    sextupleFace3 T ≫ stoneanCechFifthFace2 T := by
  simp only [stoneanCechFifthFace2, stoneanCechFifthFace2]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace23 T]

/-- The (2,4) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace24 (T : Profinite.{u}) :
    sextupleFace2 T ≫ stoneanCechFifthFace3 T =
    sextupleFace4 T ≫ stoneanCechFifthFace2 T := by
  simp only [stoneanCechFifthFace3, stoneanCechFifthFace2]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace24 T]

/-- The (2,5) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace25 (T : Profinite.{u}) :
    sextupleFace2 T ≫ stoneanCechFifthFace4 T =
    sextupleFace5 T ≫ stoneanCechFifthFace2 T := by
  simp only [stoneanCechFifthFace4, stoneanCechFifthFace2]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace25 T]

/-- The (3,4) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace34 (T : Profinite.{u}) :
    sextupleFace3 T ≫ stoneanCechFifthFace3 T =
    sextupleFace4 T ≫ stoneanCechFifthFace3 T := by
  simp only [stoneanCechFifthFace3, stoneanCechFifthFace3]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace34 T]

/-- The (3,5) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace35 (T : Profinite.{u}) :
    sextupleFace3 T ≫ stoneanCechFifthFace4 T =
    sextupleFace5 T ≫ stoneanCechFifthFace3 T := by
  simp only [stoneanCechFifthFace4, stoneanCechFifthFace3]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace35 T]

/-- The (4,5) face-pair law after transport into the
genuine categorical fourth Čech source. -/
theorem sextupleCategoricalFace45 (T : Profinite.{u}) :
    sextupleFace4 T ≫ stoneanCechFifthFace4 T =
    sextupleFace5 T ≫ stoneanCechFifthFace4 T := by
  simp only [stoneanCechFifthFace4]
  rw [← Category.assoc, ← Category.assoc,
    sextupleSimplicialFace45 T]

/-- Actual simplicial chain law d₆·d₅=0 in the ambient
condensed-module category, without finite approximations. -/
theorem stoneanCechSixthBoundary_comp_fifthBoundary_zero
    (T : Profinite.{u}) :
    stoneanCechSixthBoundary T ≫ stoneanCechFifthBoundary T = 0 := by
  unfold stoneanCechSixthBoundary stoneanCechFifthBoundary
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub, ← Functor.map_comp]
  rw [sextupleCategoricalFace01 T, sextupleCategoricalFace02 T, sextupleCategoricalFace03 T, sextupleCategoricalFace04 T, sextupleCategoricalFace05 T, sextupleCategoricalFace12 T, sextupleCategoricalFace13 T, sextupleCategoricalFace14 T, sextupleCategoricalFace15 T, sextupleCategoricalFace23 T, sextupleCategoricalFace24 T, sextupleCategoricalFace25 T, sextupleCategoricalFace34 T, sextupleCategoricalFace35 T, sextupleCategoricalFace45 T]
  simp only [sub_eq_add_neg]
  abel


/-- The actual sixth chain boundary vanishes after mapping to the
genuine *fourth relation*. The proof cancels the true kernel mono. -/
theorem stoneanCechSixthBoundary_comp_fourthRelation_zero
    (T : Profinite.{u}) :
    stoneanCechSixthBoundary T ≫
      stoneanCechFifthToFourthRelation T = 0 := by
  apply (cancel_mono (kernel.ι
    (stoneanCechFourthToThirdRelation T))).1
  rw [Category.assoc, stoneanCechFifthToFourthRelation_comp_inclusion,
    zero_comp]
  exact stoneanCechSixthBoundary_comp_fifthBoundary_zero T

/-- Global genuine sixth-to-fifth relation morphism, into the
actual kernel of the fifth-to-fourth relation, not an abstract
or finite fibre set. -/
noncomputable def stoneanCechSixthToFifthRelation
    (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
    stoneanCechFifthRelationKernel T :=
  kernel.lift (stoneanCechFifthToFourthRelation T)
    (stoneanCechSixthBoundary T)
    (stoneanCechSixthBoundary_comp_fourthRelation_zero T)

/-- Its categorical kernel inclusion recovers the true signed
sixth free-module Čech boundary on all six faces. -/
theorem stoneanCechSixthToFifthRelation_comp_inclusion
    (T : Profinite.{u}) :
    stoneanCechSixthToFifthRelation T ≫
      kernel.ι (stoneanCechFifthToFourthRelation T) =
        stoneanCechSixthBoundary T := by
  simp only [stoneanCechSixthToFifthRelation, kernel.lift_ι]

#print axioms stoneanCechSixthToFifthRelation_comp_inclusion
#print axioms stoneanCechSixthBoundary_comp_fifthBoundary_zero

#print axioms profiniteCechSextupleRelatedSet_isClosed
end CMDG.CondensedCM5R0
