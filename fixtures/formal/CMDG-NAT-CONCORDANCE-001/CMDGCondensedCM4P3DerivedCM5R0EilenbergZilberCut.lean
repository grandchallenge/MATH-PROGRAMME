import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberMaps

/-! The local Alexander–Whitney boundary calculation in every bidegree. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
namespace CMDG.CondensedCM5R0.EilenbergZilberCut

abbrev S := SimplexCategory.mk

def interval (a k n : ℕ) (h : a+k ≤ n) : S k ⟶ S n :=
  SimplexCategory.subinterval a k h

theorem interval_val (a k n : ℕ) (h : a+k ≤ n) (i : Fin (k+1)) :
    ((interval a k n h).toOrderHom i).val = i.val+a := rfl

theorem face_val {n : ℕ} (i : Fin (n+2)) (j : Fin (n+1)) :
    ((SimplexCategory.δ i).toOrderHom j).val =
      if j.val < i.val then j.val else j.val+1 := by
  change (i.succAbove j).val = _
  split_ifs with h
  · rw [Fin.succAbove_of_castSucc_lt _ _ (by exact h)]
    rfl
  · rw [Fin.succAbove_of_le_castSucc _ _ (by exact Nat.le_of_not_gt h)]
    rfl

def dFace (B : Bi) (p q : ℕ) (i : Fin (p+q+2)) :
    B.obj (d (p+q+1),d (p+q+1)) ⟶ B.obj (d p,d q) :=
  B.map (((interval 0 p (p+q) (by omega)) ≫ SimplexCategory.δ i).op ×ₘ
         ((interval p q (p+q) (by omega)) ≫ SimplexCategory.δ i).op)

def hFace (B : Bi) (p q : ℕ) (i : Fin (p+2)) :
    B.obj (d (p+q+1),d (p+q+1)) ⟶ B.obj (d p,d q) :=
  B.map (((SimplexCategory.δ i) ≫ interval 0 (p+1) (p+q+1) (by omega)).op ×ₘ
         (interval (p+1) q (p+q+1) (by omega)).op)

def vFace (B : Bi) (p q : ℕ) (i : Fin (q+2)) :
    B.obj (d (p+q+1),d (p+q+1)) ⟶ B.obj (d p,d q) :=
  B.map ((interval 0 p (p+q+1) (by omega)).op ×ₘ
         ((SimplexCategory.δ i) ≫ interval p (q+1) (p+q+1) (by omega)).op)

theorem dFace_hFace (B : Bi) (p q : ℕ) (i : Fin (p+1)) :
    dFace B p q ⟨i.val,by omega⟩ = hFace B p q i.castSucc := by
  unfold dFace hFace
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    simp only [SimplexCategory.comp_toOrderHom, OrderHom.comp, OrderHom.coe_mk, Function.comp_apply, interval_val,face_val,
      Fin.val_castSucc, Nat.add_zero]
    rfl
  · apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    simp only [SimplexCategory.comp_toOrderHom, OrderHom.comp, OrderHom.coe_mk, Function.comp_apply, interval_val,face_val]
    have hi : ¬ j.val+p < i.val := by omega
    simp [hi]
    omega

theorem dFace_vFace (B : Bi) (p q : ℕ) (i : Fin (q+1)) :
    dFace B p q ⟨p+1+i.val,by omega⟩ = vFace B p q i.succ := by
  unfold dFace vFace
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    simp only [SimplexCategory.comp_toOrderHom, OrderHom.comp, OrderHom.coe_mk, Function.comp_apply, interval_val,face_val,
      Nat.add_zero]
    have hj : j.val < p+1 := j.isLt
    have hi : j.val < p+1+i.val := by omega
    simp [hi]
  · apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    simp only [SimplexCategory.comp_toOrderHom, OrderHom.comp, OrderHom.coe_mk, Function.comp_apply, interval_val,face_val,
      Fin.val_succ]
    change (if j.val+p < p+1+i.val then j.val+p else j.val+p+1) =
      (if j.val < i.val+1 then j.val else j.val+1)+p
    by_cases h : j.val < i.val+1
    · rw [if_pos h,if_pos (show j.val+p < p+1+i.val by omega)]
    · rw [if_neg h,if_neg (show ¬ j.val+p < p+1+i.val by omega)]
      omega

theorem hFace_last_eq_vFace_zero (B : Bi) (p q : ℕ) :
    hFace B p q (Fin.last (p+1)) = vFace B p q 0 := by
  unfold hFace vFace
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    simp only [SimplexCategory.comp_toOrderHom, OrderHom.comp, OrderHom.coe_mk, Function.comp_apply, interval_val,face_val,
      Fin.val_last,Nat.add_zero]
    simp [show j.val < p+1 from j.isLt]
  · apply congrArg Quiver.Hom.op
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    simp only [SimplexCategory.comp_toOrderHom, OrderHom.comp, OrderHom.coe_mk, Function.comp_apply, interval_val,face_val,
      Fin.val_zero,Nat.not_lt_zero,if_false]
    omega

set_option backward.isDefEq.respectTransparency false in
theorem cutBoundary (B : Bi) (p q : ℕ) :
    (∑ i : Fin (p+q+2), (-1 : ℤ)^i.val • dFace B p q i) =
      (∑ i : Fin (p+2), (-1 : ℤ)^i.val • hFace B p q i) +
      (∑ i : Fin (q+2), (-1 : ℤ)^(p+i.val) • vFace B p q i) := by
  let f : Fin ((p+1)+(q+1)) → _ := fun i =>
    (-1 : ℤ)^i.val • dFace B p q ⟨i.val,by omega⟩
  have heq : (∑ i : Fin (p+q+2), (-1 : ℤ)^i.val • dFace B p q i) = ∑ i, f i := by
    apply Finset.sum_bij (fun i _ => (⟨i.val,by omega⟩ : Fin ((p+1)+(q+1))))
    · simp
    · intro a _ b _ h
      exact Fin.ext (congrArg (fun x : Fin ((p+1)+(q+1)) => x.val) h)
    · intro b _
      refine ⟨⟨b.val,by omega⟩,by simp,?_⟩
      rfl
    · intro i _
      rfl
  rw [heq,Fin.sum_univ_add]
  rw [Fin.sum_univ_castSucc (fun i : Fin (p+2) => (-1 : ℤ)^i.val • hFace B p q i)]
  rw [Fin.sum_univ_succ (fun i : Fin (q+2) => (-1 : ℤ)^(p+i.val) • vFace B p q i)]
  simp only [f,Fin.val_castAdd,Fin.val_natAdd,Fin.val_castSucc,Fin.val_succ,Fin.val_last,
    Fin.val_zero,Nat.add_zero]
  simp_rw [dFace_hFace, dFace_vFace]
  rw [hFace_last_eq_vFace_zero, pow_succ]
  simp only [mul_neg,mul_one,neg_smul]
  abel

#print axioms dFace_hFace
#print axioms dFace_vFace
#print axioms cutBoundary
end CMDG.CondensedCM5R0.EilenbergZilberCut
