import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberNatural

/-! Cycle filling in the actual free diagonal models. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
namespace CMDG.CondensedCM5R0.EilenbergZilberFilling

def cone (p q n : ℕ) :
    (D.obj (model p q)).X n ⟶ (D.obj (model p q)).X (n+1) :=
  (diagonalModelHomotopy p q).homotopyHomInvId.symm.hom n (n+1)

set_option backward.isDefEq.respectTransparency false in
theorem cone_fill (p q n : ℕ) (z : (D.obj (model p q)).X (n+1))
    (hz : (D.obj (model p q)).d (n+1) n z = 0) :
    (D.obj (model p q)).d (n+2) (n+1) (cone p q (n+1) z) = z := by
  let e := diagonalModelHomotopy p q
  have h := e.homotopyHomInvId.symm.comm (n+1)
  rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex] at h
  have he : (e.hom ≫ e.inv).f (n+1) = 0 := by
    rw [HomologicalComplex.comp_f]
    have hzero := HomologicalComplex.isZero_single_obj_X c 0 (freeZ.obj PUnit) (n+1) (by omega)
    rw [hzero.eq_of_tgt (e.hom.f (n+1)) 0,zero_comp]
  rw [he,add_zero] at h
  have hh := CategoryTheory.congr_fun h z
  change z = cone p q n ((D.obj (model p q)).d (n+1) n z) +
    (D.obj (model p q)).d (n+2) (n+1) (cone p q (n+1) z) at hh
  rw [hz,map_zero,zero_add] at hh
  exact hh.symm

#print axioms cone_fill
end CMDG.CondensedCM5R0.EilenbergZilberFilling
