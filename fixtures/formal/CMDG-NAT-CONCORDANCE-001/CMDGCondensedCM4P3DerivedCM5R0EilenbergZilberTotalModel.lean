import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberSingleTotal

/-! Contract the actual total free model in both directions. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.EilenbergZilberHorizontalModel
open CMDG.CondensedCM5R0.EilenbergZilberSingleTotal
namespace CMDG.CondensedCM5R0.EilenbergZilberTotalModel

def simplexAug (b : ℕ) : SimplicialObject.Augmented Type :=
  (simplex b).augmentOfIsTerminal Types.isTerminalPUnit

def simplexExtra (b : ℕ) : SimplicialObject.Augmented.ExtraDegeneracy (simplexAug b) where
  s' := ↾fun _ => (SimplexCategory.const (SimplexCategory.mk 0) (SimplexCategory.mk b) 0).op
  s n := ↾fun x => (shift x.unop).op
  s'_comp_ε := by rfl
  s₀_comp_δ₁ := by
    apply ConcreteCategory.hom_ext
    intro x
    apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext i
    fin_cases i
    rfl
  s_comp_δ₀ n := by
    apply ConcreteCategory.hom_ext
    intro x
    apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext i
    rfl
  s_comp_δ n i := by
    apply ConcreteCategory.hom_ext
    intro x
    exact congrArg Quiver.Hom.op (shift_face x.unop i)
  s_comp_σ n i := by
    apply ConcreteCategory.hom_ext
    intro x
    exact congrArg Quiver.Hom.op (shift_degeneracy x.unop i)

def verticalModelEquiv (b : ℕ) :
    HomotopyEquiv (verticalModel b) ((ChainComplex.single₀ ZMod).obj (freeZ.obj PUnit)) :=
  ((simplexExtra b).map freeZ).homotopyEquiv

def totalizeEquiv {K L : BC} (e : HomotopyEquiv K L) :
    HomotopyEquiv (K.total c) (L.total c) where
  hom := HomologicalComplex₂.total.map e.hom c
  inv := HomologicalComplex₂.total.map e.inv c
  homotopyHomInvId := by
    rw [← HomologicalComplex₂.total.map_comp, ← HomologicalComplex₂.total.map_id K c]
    exact liftHomotopy e.homotopyHomInvId
  homotopyInvHomId := by
    rw [← HomologicalComplex₂.total.map_comp, ← HomologicalComplex₂.total.map_id L c]
    exact liftHomotopy e.homotopyInvHomId

def totalModelEquiv (a b : ℕ) :
    HomotopyEquiv (Tot.obj (model a b)) ((ChainComplex.single₀ ZMod).obj (freeZ.obj PUnit)) :=
  (totalizeEquiv (horizontalModelEquiv a b)).trans
    ((HomotopyEquiv.ofIso (singleTotalIso (verticalModel b)).symm).trans (verticalModelEquiv b))

def totalCone (a b n : ℕ) :
    (Tot.obj (model a b)).X n ⟶ (Tot.obj (model a b)).X (n+1) :=
  (totalModelEquiv a b).homotopyHomInvId.symm.hom n (n+1)

set_option backward.isDefEq.respectTransparency false in
theorem totalCone_fill (a b n : ℕ) (z : (Tot.obj (model a b)).X (n+1))
    (hz : (Tot.obj (model a b)).d (n+1) n z = 0) :
    (Tot.obj (model a b)).d (n+2) (n+1) (totalCone a b (n+1) z) = z := by
  let e := totalModelEquiv a b
  have h := e.homotopyHomInvId.symm.comm (n+1)
  rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex] at h
  have he : (e.hom ≫ e.inv).f (n+1) = 0 := by
    rw [HomologicalComplex.comp_f]
    have hzero := HomologicalComplex.isZero_single_obj_X c 0 (freeZ.obj PUnit) (n+1) (by omega)
    rw [hzero.eq_of_tgt (e.hom.f (n+1)) 0,zero_comp]
  rw [he,add_zero] at h
  have hh := CategoryTheory.congr_fun h z
  change z = totalCone a b n ((Tot.obj (model a b)).d (n+1) n z) +
    (Tot.obj (model a b)).d (n+2) (n+1) (totalCone a b (n+1) z) at hh
  rw [hz,map_zero,zero_add] at hh
  exact hh.symm

#print axioms totalModelEquiv
#print axioms totalCone_fill
end CMDG.CondensedCM5R0.EilenbergZilberTotalModel
