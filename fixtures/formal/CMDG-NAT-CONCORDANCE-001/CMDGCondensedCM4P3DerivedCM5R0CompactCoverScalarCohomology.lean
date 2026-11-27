import CMDGCondensedCM4P3DerivedCM5R0CompactCoverExtClasses
import Mathlib.GroupTheory.QuotientGroup.Basic

/-! The genuine scalar Čech cohomology quotient computes actual Ext.
This does not assume that the scalar cohomology vanishes. -/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover

variable (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)

abbrev scalarTerm (n : ℕ) := LocallyConstant (compactRelationProfinite P T p n) ℤ

def scalarAddEquiv (n : ℕ) :
    (term P T p n ⟶ discreteIntegerCoeff) ≃+ scalarTerm P T p n :=
  AddEquiv.ofBijective (uniformFreeRelationHomScalarAddHom
    (compactRelationProfinite P T p n))
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (compactRelationProfinite P T p n)).bijective

def scalarD (n : ℕ) : scalarTerm P T p n →+ scalarTerm P T p (n+1) :=
  (scalarAddEquiv P T p (n+1)).toAddMonoidHom.comp
    ((Preadditive.leftComp discreteIntegerCoeff (d P T p n)).comp
      (scalarAddEquiv P T p n).symm.toAddMonoidHom)

theorem scalarD_eq (n : ℕ) (c : scalarTerm P T p n) :
    scalarD P T p n c = compactCategoricalRelationScalarDifferential P T p n c := by
  let e := scalarAddEquiv P T p n
  change freeProfiniteDiscreteIntegerHomScalarEquiv _
    (d P T p n ≫ e.symm c) = _
  rw [compactFreeRelationBoundary_integerHom_scalar]
  exact congrArg (compactCategoricalRelationScalarDifferential P T p n)
    (e.apply_symm_apply c)

theorem scalarD_on_hom (n : ℕ) (f : term P T p n ⟶ discreteIntegerCoeff) :
    scalarD P T p n (scalarAddEquiv P T p n f) =
      scalarAddEquiv P T p (n+1) (d P T p n ≫ f) := by
  change scalarAddEquiv P T p (n+1) (d P T p n ≫
    (scalarAddEquiv P T p n).symm (scalarAddEquiv P T p n f)) = _
  rw [AddEquiv.symm_apply_apply]

theorem scalarD_sq (n : ℕ) (c : scalarTerm P T p n) :
    scalarD P T p (n+1) (scalarD P T p n c) = 0 := by
  obtain ⟨f,rfl⟩ := (scalarAddEquiv P T p n).surjective c
  rw [scalarD_on_hom, scalarD_on_hom, ← Category.assoc,
    compactFreeRelationBoundary_sq_zero, zero_comp, map_zero]

def scalarCocycles (n : ℕ) : AddSubgroup (scalarTerm P T p (n+1)) :=
  (scalarD P T p (n+1)).ker

def scalarCoboundary (n : ℕ) : scalarTerm P T p n →+ scalarCocycles P T p n :=
  (scalarD P T p n).codRestrict _ (scalarD_sq P T p n)

variable [Epi p]

omit [Epi p] in
theorem cover_closed (n : ℕ) :
    d P T p (n+1) ≫ syzygyCover P T p n = 0 := by
  letI := syzygyι_mono P T p n
  apply (cancel_mono (syzygyι P T p n)).1
  rw [Category.assoc, cover_comp_ι, zero_comp]
  exact compactFreeRelationBoundary_sq_zero P T p n

def scalarFromSyzygy (n : ℕ) :
    (syzygy P T p n ⟶ discreteIntegerCoeff) →+ scalarCocycles P T p n :=
  ((scalarAddEquiv P T p (n+1)).toAddMonoidHom.comp
    (Preadditive.leftComp discreteIntegerCoeff (syzygyCover P T p n))).codRestrict _ (by
      intro f
      change scalarD P T p (n+1)
        (scalarAddEquiv P T p (n+1) (syzygyCover P T p n ≫ f)) = 0
      rw [scalarD_on_hom, ← Category.assoc, cover_closed, zero_comp, map_zero])

theorem scalarFromSyzygy_bijective (n : ℕ) :
    Function.Bijective (scalarFromSyzygy P T p n) := by
  letI := cover_epi P T p n
  constructor
  · intro f g h
    apply (cancel_epi (syzygyCover P T p n)).1
    apply (scalarAddEquiv P T p (n+1)).injective
    exact congrArg Subtype.val h
  · intro c
    obtain ⟨f,hf⟩ := (scalarAddEquiv P T p (n+1)).surjective c.val
    have hc : scalarD P T p (n+1) c.val = 0 := c.property
    rw [← hf, scalarD_on_hom] at hc
    have hz : d P T p (n+1) ≫ f = 0 :=
      (map_eq_zero_iff (scalarAddEquiv P T p (n+2))
        (scalarAddEquiv P T p (n+2)).injective).mp hc
    obtain ⟨g,hg,_⟩ := cocycle_factors_unique P T p n f hz
    refine ⟨g,Subtype.ext ?_⟩
    change scalarAddEquiv P T p (n+1) (syzygyCover P T p n ≫ g) = c.val
    rw [hg,hf]

def scalarSyzygyEquiv (n : ℕ) :
    (syzygy P T p n ⟶ discreteIntegerCoeff) ≃+ scalarCocycles P T p n :=
  AddEquiv.ofBijective (scalarFromSyzygy P T p n) (scalarFromSyzygy_bijective P T p n)

def scalarClass (n : ℕ) : scalarCocycles P T p n →+
    Abelian.Ext (compactFreeFunctor.obj T) discreteIntegerCoeff (n+1) :=
  (classOfSyzygyHom P T p n).comp (scalarSyzygyEquiv P T p n).symm.toAddMonoidHom

theorem scalarClass_surj (n : ℕ) : Function.Surjective (scalarClass P T p n) :=
  (classOfSyzygyHom_surj P T p n).comp (scalarSyzygyEquiv P T p n).symm.surjective

theorem scalarClass_zero_iff (n : ℕ) (c : scalarCocycles P T p n) :
    scalarClass P T p n c = 0 ↔ c ∈ (scalarCoboundary P T p n).range := by
  let E := scalarSyzygyEquiv P T p n
  let f := E.symm c
  have hf : scalarAddEquiv P T p (n+1) (syzygyCover P T p n ≫ f) = c.val :=
    congrArg Subtype.val (E.apply_symm_apply c)
  change classOfSyzygyHom P T p n f = 0 ↔ _
  rw [classOfSyzygyHom_zero_iff]
  constructor
  · rintro ⟨g,hg⟩
    refine ⟨scalarAddEquiv P T p n g, Subtype.ext ?_⟩
    change scalarD P T p n (scalarAddEquiv P T p n g) = c.val
    rw [scalarD_on_hom, ← cover_comp_ι, Category.assoc, hg, hf]
  · rintro ⟨b,hb⟩
    obtain ⟨g,hg⟩ := (scalarAddEquiv P T p n).surjective b
    refine ⟨g,?_⟩
    letI := cover_epi P T p n
    apply (cancel_epi (syzygyCover P T p n)).1
    apply (scalarAddEquiv P T p (n+1)).injective
    rw [← Category.assoc, cover_comp_ι, hf]
    have h := congrArg Subtype.val hb
    change scalarD P T p n b = c.val at h
    rw [← hg, scalarD_on_hom] at h
    exact h

theorem scalarClass_ker (n : ℕ) :
    (scalarClass P T p n).ker = (scalarCoboundary P T p n).range := by
  ext c
  exact scalarClass_zero_iff P T p n c

def scalarCohomologyExtEquiv (n : ℕ) :
    (scalarCocycles P T p n ⧸ (scalarCoboundary P T p n).range) ≃+
      Abelian.Ext (compactFreeFunctor.obj T) discreteIntegerCoeff (n+1) :=
  (QuotientAddGroup.quotientAddEquivOfEq (scalarClass_ker P T p n).symm).trans
    (QuotientAddGroup.quotientKerEquivOfSurjective _
      (scalarClass_surj P T p n))

theorem scalarCohomologyExtEquiv_mk (n : ℕ) (c : scalarCocycles P T p n) :
    scalarCohomologyExtEquiv P T p n (QuotientAddGroup.mk c) =
      scalarClass P T p n c := by
  unfold scalarCohomologyExtEquiv
  rw [AddEquiv.trans_apply, QuotientAddGroup.quotientAddEquivOfEq_mk]
  rfl

#print axioms scalarCohomologyExtEquiv_mk
#print axioms scalarD_eq
#print axioms scalarClass_ker
#print axioms scalarCohomologyExtEquiv
end CMDG.CondensedCM5R0.CompactCover
