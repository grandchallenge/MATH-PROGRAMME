import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAdditiveBarTotal

/-! The ordinary diagonal bar of K(A,n) has the actual additive
chain-homotopy type of A concentrated in degree n+1. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBarTotal
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.BreenDeligneAdditiveBarShift

abbrev K (A : ZMod) (n : ℕ) : BC := singleRows ((singleZ n).obj A)

def survivingIso (A : ZMod) (n : ℕ) : ((K A n).X n).X 1 ≅ A :=
  HomologicalComplex.singleObjXSelf c 1 (((singleZ n).obj A).X n) ≪≫
    HomologicalComplex.singleObjXSelf c n A

theorem offZero (A : ZMod) (n p q : ℕ) (h : p≠n ∨ q≠1) :
    IsZero (((K A n).X p).X q) := by
  rcases h with hp | hq
  · exact (S1 ⋙ HomologicalComplex.eval ZMod c q).map_isZero
      (HomologicalComplex.isZero_single_obj_X c n A p hp)
  · exact HomologicalComplex.isZero_single_obj_X c 1 (((singleZ n).obj A).X p) q hq

theorem totalOffZero (A : ZMod) (n j : ℕ) (h : j≠n+1) :
    IsZero (((K A n).total c).X j) := by
  apply (IsZero.iff_id_eq_zero _).mpr
  apply HomologicalComplex₂.total.hom_ext
  intro p q hpq
  change p+q=j at hpq
  apply (offZero A n p q _).eq_of_src
  by_contra! hn
  omega

def atDegreeProj (A : ZMod) (n : ℕ) : ((K A n).total c).X (n+1) ⟶ A :=
  (K A n).totalDesc (fun p q h => if hp : p=n then
    eqToHom (by
      change p+q=n+1 at h
      have hq : q=1 := by omega
      subst p
      subst q
      rfl) ≫ (survivingIso A n).hom else 0)

def atDegreeIncl (A : ZMod) (n : ℕ) : A ⟶ ((K A n).total c).X (n+1) :=
  (survivingIso A n).inv ≫ (K A n).ιTotal c n 1 (n+1) rfl

set_option backward.isDefEq.respectTransparency false in
def atDegreeIso (A : ZMod) (n : ℕ) : ((K A n).total c).X (n+1) ≅ A where
  hom := atDegreeProj A n
  inv := atDegreeIncl A n
  hom_inv_id := by
    apply HomologicalComplex₂.total.hom_ext
    intro p q h
    change p+q=n+1 at h
    by_cases hp : p=n
    · subst p
      have hq : q=1 := by omega
      subst q
      unfold atDegreeProj atDegreeIncl
      rw [← Category.assoc,HomologicalComplex₂.ι_totalDesc,dif_pos rfl]
      simp
    · exact (offZero A n p q (Or.inl hp)).eq_of_src _ _
  inv_hom_id := by
    unfold atDegreeIncl atDegreeProj
    rw [Category.assoc,HomologicalComplex₂.ι_totalDesc,dif_pos rfl]
    simp

def doubleSingleComponent (A : ZMod) (n j : ℕ) :
    ((K A n).total c).X j ≅ ((singleZ (n+1)).obj A).X j := by
  by_cases h : j=n+1
  · subst j
    exact atDegreeIso A n ≪≫ (HomologicalComplex.singleObjXSelf c (n+1) A).symm
  · exact (totalOffZero A n j h).iso (HomologicalComplex.isZero_single_obj_X c (n+1) A j h)

def doubleSingleIso (A : ZMod) (n : ℕ) :
    (K A n).total c ≅ (singleZ (n+1)).obj A :=
  HomologicalComplex.Hom.isoOfComponents (doubleSingleComponent A n) (by
    intro i j h
    change j+1=i at h
    by_cases hi : i=n+1
    · exact (HomologicalComplex.isZero_single_obj_X c (n+1) A j (by omega)).eq_of_tgt _ _
    · exact (totalOffZero A n i hi).eq_of_src _ _)

def additiveBarShiftEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv (additiveChains (barDiagonal ((em n).obj A)))
      ((singleZ (n+1)).obj (toZModule.obj A)) :=
  (additiveBarDoubleSingleEquiv A n).trans (HomotopyEquiv.ofIso (doubleSingleIso _ n))

def additiveNextEquiv (A : AGrp) (n : ℕ) :
    HomotopyEquiv (additiveChains (barDiagonal ((em n).obj A)))
      (additiveChains ((EilenbergMacLaneModel.em (n+1)).obj A)) :=
  (additiveBarShiftEquiv A n).trans (additiveEMEquiv A (n+1)).symm

#print axioms doubleSingleIso
#print axioms additiveBarShiftEquiv
#print axioms additiveNextEquiv
end CMDG.CondensedCM5R0.BreenDeligneAdditiveBarShift
