import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneDoubleDescent
import CMDGCondensedCM4P3DerivedCM5R0UniformSplitCechAugmentation

/-! Actual module-valued Čech relation objects and their face maps.
The set-level relations are the same tuples as the established split
Čech bar, not an abstract resolution. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe
local instance (A : Mod.{u}) : Module Coeff.{u} A := A.isModule
local instance (A : Mod.{u}) : SMul Coeff.{u} A := A.isModule.toDistribMulAction.toDistribSMul.toSMul
variable {M N : Mod.{u}} (p : M ⟶ N)

def relSub (n : ℕ) : Submodule Coeff.{u} (Fin (n+1) → M) where
  carrier := {x | ∀ i, p (x i) = p (x 0)}
  zero_mem' := by intro i; rfl
  add_mem' := by
    intro x y hx hy i
    change p (x i + y i) = p (x 0 + y 0)
    rw [map_add,map_add,hx i,hy i]
  smul_mem' := by
    intro r x hx i
    obtain ⟨r⟩ := r
    change p (((r : Coeff.{u}) • x) i) = p (((r : Coeff.{u}) • x) 0)
    rw [Int.cast_smul_eq_zsmul]
    change p (r • x i) = p (r • x 0)
    rw [map_zsmul,map_zsmul,hx i]

abbrev rel (n : ℕ) : Mod.{u} := ModuleCat.of Coeff.{u} (relSub p n)

def relFace (n : ℕ) (k : Fin (n+2)) : rel p (n+1) ⟶ rel p n :=
  ModuleCat.ofHom {
    toFun := splitCechFace M N p n k
    map_add' := by intros; rfl
    map_smul' := by intros; rfl }

def relAug : rel p 0 ⟶ N :=
  ModuleCat.ofHom {
    toFun := fun x => p (x.val 0)
    map_add' := fun _ _ => map_add p.hom _ _
    map_smul' := by
      intro r x
      obtain ⟨r⟩ := r
      change p (((r : Coeff.{u}) • x).val 0) = (r : Coeff.{u}) • p (x.val 0)
      rw [Int.cast_smul_eq_zsmul,Int.cast_smul_eq_zsmul]
      change p (r • x.val 0) = r • p (x.val 0)
      exact map_zsmul p.hom _ _ }

def relD (n : ℕ) : rel p (n+1) ⟶ rel p n :=
  ∑ k : Fin (n+2), (-1 : ℤ)^k.val • relFace p n k

def evaluation (A : Mod.{u}) : freeM A ⟶ A :=
  ModuleCat.freeDesc (↾fun x : A => x)

theorem evaluation_surj (A : Mod.{u}) : Function.Surjective (evaluation A) := by
  intro x
  exact ⟨ModuleCat.freeMk x,ModuleCat.freeDesc_apply _ _⟩

theorem evaluation_natural {A B : Mod.{u}} (f : A ⟶ B) :
    (ModuleCat.free Coeff.{u}).map (↾fun x : A => f x) ≫ evaluation B =
      evaluation A ≫ f := by
  apply ModuleCat.free_hom_ext
  intro x
  change evaluation B ((ModuleCat.free Coeff.{u}).map (↾fun x : A => f x) (ModuleCat.freeMk x)) =
    f (evaluation A (ModuleCat.freeMk x))
  rw [ModuleCat.free_map_apply,evaluation,ModuleCat.freeDesc_apply,evaluation,ModuleCat.freeDesc_apply]
  rfl

theorem evaluation_d (n : ℕ) :
    splitBarD M N p n ≫ evaluation (rel p n) =
      evaluation (rel p (n+1)) ≫ relD p n := by
  unfold splitBarD relD
  rw [Preadditive.sum_comp,Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [Preadditive.zsmul_comp,Preadditive.comp_zsmul]
  congr 1
  exact evaluation_natural (relFace p n k)

theorem evaluation_aug :
    splitBarBaseMap M N p ≫ evaluation N = evaluation (rel p 0) ≫ relAug p :=
  by
    unfold splitBarBaseMap
    exact evaluation_natural (relAug p)

theorem relD_sq (n : ℕ) : relD p (n+1) ≫ relD p n = 0 := by
  letI : Epi (evaluation (rel p (n+2))) :=
    (ModuleCat.epi_iff_surjective _).2 (evaluation_surj _)
  apply (cancel_epi (evaluation (rel p (n+2)))).1
  rw [← Category.assoc,← evaluation_d,Category.assoc,← evaluation_d,
    ← Category.assoc,splitBarD_comp_D_zero,zero_comp,comp_zero]

theorem relD_aug : relD p 0 ≫ relAug p = 0 := by
  letI : Epi (evaluation (rel p 1)) :=
    (ModuleCat.epi_iff_surjective _).2 (evaluation_surj _)
  apply (cancel_epi (evaluation (rel p 1))).1
  rw [← Category.assoc,← evaluation_d,Category.assoc,← evaluation_aug,
    ← Category.assoc,splitBarZeroBoundary_comp_augmentation,zero_comp,comp_zero]

theorem relAug_surj (hp : Function.Surjective p) : Function.Surjective (relAug p) := by
  intro y
  obtain ⟨x,hx⟩ := hp y
  refine ⟨⟨fun _ => x,fun _ => rfl⟩,?_⟩
  change p x = y
  exact hx

theorem rel_zero_exact (x : rel p 0) (hx : relAug p x = 0) :
    ∃ y : rel p 1, relD p 0 y = x := by
  let y : rel p 1 := ⟨Fin.cons 0 x.val,by
    intro i
    refine Fin.cases rfl (fun j => ?_) i
    change p (x.val j) = p 0
    rw [x.property j,map_zero]
    exact (show p (x.val 0) = 0 from hx)⟩
  refine ⟨y,?_⟩
  apply Subtype.ext
  funext i
  have hi : i = 0 := Fin.eq_zero i
  subst i
  change ((relD p 0).hom y).val 0 = _
  simp only [relD,ModuleCat.hom_sum,LinearMap.sum_apply,ModuleCat.hom_zsmul,
    LinearMap.smul_apply]
  rw [Fin.sum_univ_two]
  change (((-1 : ℤ) ^ (0 : Fin 2).val) • y.val 1 +
    ((-1 : ℤ) ^ (1 : Fin 2).val) • y.val 0) = x.val 0
  simp [y]

def relAt (n : ℕ) (i : Fin (n+1)) : rel p n →+ M where
  toFun x := x.val i
  map_zero' := rfl
  map_add' _ _ := rfl

theorem relD_val (n : ℕ) (x : rel p (n+1)) (i : Fin (n+1)) :
    (relD p n x).val i = ∑ k : Fin (n+2), (-1 : ℤ)^k.val • x.val (k.succAbove i) := by
  change relAt p n i ((relD p n).hom x) = _
  simp only [relD,ModuleCat.hom_sum,LinearMap.sum_apply,ModuleCat.hom_zsmul,
    LinearMap.smul_apply,map_sum,map_zsmul]
  rfl

theorem relD_image (n : ℕ) (x : rel p (n+1)) (i : Fin (n+1)) :
    p ((relD p n x).val i) = (∑ k : Fin (n+2), (-1 : ℤ)^k.val) • p (x.val 0) := by
  rw [relD_val]
  change p.hom (∑ k : Fin (n+2), (-1 : ℤ)^k.val • x.val (k.succAbove i)) = _
  rw [map_sum,Finset.sum_smul]
  apply Finset.sum_congr rfl
  intro k _
  rw [map_zsmul]
  congr 1
  exact x.property _

theorem rel_exact (n : ℕ) (x : rel p (n+1)) (hx : relD p n x = 0) :
    ∃ y : rel p (n+2), relD p (n+1) y = x := by
  classical
  let b : M := if Even (n+2) then x.val 0 else 0
  have hb : p b = p (x.val 0) := by
    by_cases he : Even (n+2)
    · simp [b,he]
    · have h := relD_image p n x 0
      rw [hx,Fin.sum_neg_one_pow,if_neg he,one_zsmul] at h
      change p 0 = p (x.val 0) at h
      simpa [b,he] using h
  let y : rel p (n+2) := ⟨Fin.cons b x.val,by
    intro i
    refine Fin.cases rfl (fun j => ?_) i
    change p (x.val j) = p b
    rw [hb]
    exact x.property j⟩
  refine ⟨y,?_⟩
  apply Subtype.ext
  funext i
  rw [relD_val,Fin.sum_univ_succ]
  simp only [Fin.val_zero,pow_zero,one_zsmul,Fin.val_succ,pow_succ,mul_neg,mul_one,neg_smul,
    Finset.sum_neg_distrib]
  rw [Fin.zero_succAbove]
  change x.val i + -(∑ k : Fin (n+2), (-1 : ℤ)^k.val • y.val (k.succ.succAbove i)) = x.val i
  rw [← sub_eq_add_neg]
  change x.val i - (∑ k : Fin (n+2), (-1 : ℤ)^k.val •
    y.val (k.succ.succAbove i)) = x.val i
  have hz : (∑ k : Fin (n+2), (-1 : ℤ)^k.val • y.val (k.succ.succAbove i)) = 0 := by
    refine Fin.cases ?_ (fun j => ?_) i
    · change (∑ k : Fin (n+2), (-1 : ℤ)^k.val • b) = 0
      rw [← Finset.sum_smul,Fin.sum_neg_one_pow]
      by_cases he : Even (n+2) <;> simp [b,he]
    · have hd := relD_val p n x j
      rw [hx] at hd
      change (0 : M) = _ at hd
      refine Eq.trans ?_ hd.symm
      apply Finset.sum_congr rfl
      intro k _
      rw [Fin.succ_succAbove_succ]
      rfl
  rw [hz,sub_zero]

#print axioms rel_exact
#print axioms relD_sq
#print axioms rel_zero_exact
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
