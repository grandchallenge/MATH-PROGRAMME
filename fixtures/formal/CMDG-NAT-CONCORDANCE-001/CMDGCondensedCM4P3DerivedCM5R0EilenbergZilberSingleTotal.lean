import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberHorizontalModel

/-! Totalization of a horizontal single-zero complex is the vertical complex. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.EilenbergZilberSingleTotal

abbrev single (V : Ch) : BC := (ChainComplex.single₀ Ch).obj V

def selfIso (V : Ch) : (single V).X 0 ≅ V :=
  HomologicalComplex.singleObjXSelf c 0 V

theorem otherZero (V : Ch) (p q : ℕ) (hp : p ≠ 0) :
    IsZero (((single V).X p).X q) :=
  (HomologicalComplex.eval ZMod c q).map_isZero
    (HomologicalComplex.isZero_single_obj_X c 0 V p hp)

def incl (V : Ch) (n : ℕ) : V.X n ⟶ ((single V).total c).X n :=
  (selfIso V).inv.f n ≫ (single V).ιTotal c 0 n n (by change 0+n=n; omega)

def proj (V : Ch) (n : ℕ) : ((single V).total c).X n ⟶ V.X n :=
  (single V).totalDesc (fun p q h => if hp : p=0 then
    eqToHom (by subst p; rfl) ≫ (selfIso V).hom.f q ≫ eqToHom (by
      change p+q=n at h; rw [hp,zero_add] at h; rw [h])
    else 0)

set_option backward.isDefEq.respectTransparency false in
theorem incl_proj (V : Ch) (n : ℕ) : incl V n ≫ proj V n = 𝟙 _ := by
  unfold incl proj
  rw [Category.assoc,HomologicalComplex₂.ι_totalDesc,dif_pos rfl]
  simp only [eqToHom_refl,Category.id_comp,Category.comp_id]
  exact congrArg (fun k => k.f n) (selfIso V).inv_hom_id

set_option backward.isDefEq.respectTransparency false in
theorem proj_incl (V : Ch) (n : ℕ) : proj V n ≫ incl V n = 𝟙 _ := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  by_cases hp : p=0
  · subst p
    change 0+q=n at h
    have hq : q=n := by omega
    subst q
    unfold proj incl
    rw [← Category.assoc,HomologicalComplex₂.ι_totalDesc,dif_pos rfl]
    simp only [eqToHom_refl,Category.id_comp,Category.comp_id,Category.assoc]
    rw [← Category.assoc]
    have he := congrArg (fun k => k.f n) (selfIso V).hom_inv_id
    change (selfIso V).hom.f n ≫ (selfIso V).inv.f n = 𝟙 _ at he
    rw [he,Category.id_comp]
  · exact (otherZero V p q hp).eq_of_src _ _

def componentIso (V : Ch) (n : ℕ) : V.X n ≅ ((single V).total c).X n where
  hom := incl V n
  inv := proj V n
  hom_inv_id := incl_proj V n
  inv_hom_id := proj_incl V n

set_option backward.isDefEq.respectTransparency false in
theorem incl_comm (V : Ch) (n : ℕ) :
    incl V (n+1) ≫ ((single V).total c).d (n+1) n = V.d (n+1) n ≫ incl V n := by
  unfold incl
  rw [Category.assoc]
  change _ ≫ (single V).ιTotal c 0 (n+1) (n+1) _ ≫
    ((single V).D₁ c (n+1) n + (single V).D₂ c (n+1) n) = _
  rw [Preadditive.comp_add,horizontal_axis,vertical_succ _ 0 n _ _ _ (by change 0+n=n; omega),
    zero_add,pow_zero,one_smul,← Category.assoc, (selfIso V).inv.comm,Category.assoc]

set_option backward.isDefEq.respectTransparency false in
def singleTotalIso (V : Ch) : V ≅ (single V).total c :=
  HomologicalComplex.Hom.isoOfComponents (componentIso V) (by
    intro i j h
    change j+1=i at h
    subst i
    exact incl_comm V j)

#print axioms singleTotalIso
end CMDG.CondensedCM5R0.EilenbergZilberSingleTotal
