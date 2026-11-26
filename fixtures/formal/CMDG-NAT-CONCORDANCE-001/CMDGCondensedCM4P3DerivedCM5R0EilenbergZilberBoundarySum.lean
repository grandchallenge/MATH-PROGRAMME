import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberPartition

/-! Complete signed boundary identity of the original ordinal paths,
before evaluation by a bisimplicial module. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCorners
open CMDG.CondensedCM5R0.EilenbergZilberStraight
open CMDG.CondensedCM5R0.EilenbergZilberInsert
open CMDG.CondensedCM5R0.EilenbergZilberStraightSign
open CMDG.CondensedCM5R0.EilenbergZilberTranspose
open CMDG.CondensedCM5R0.EilenbergZilberPartition
namespace CMDG.CondensedCM5R0.EilenbergZilberBoundarySum

def hIndex {p q} (i : Fin (p+1+q)) : Vertex p q :=
  ⟨i.val,by have := i.isLt; omega⟩

def hPair {p q} (v : Path p q) (a : Fin (p+2)) : Deleted (p+1) q :=
  ({toFun := fun i => a.succAbove (v.val.1 (hIndex i)),
    monotone' := fun _ _ h => (Fin.succAboveOrderEmb a).monotone (v.val.1.monotone h)},
   {toFun := fun i => v.val.2 (hIndex i), monotone' := fun _ _ h => v.val.2.monotone h})

def vPair {p q} (v : Path p q) (a : Fin (q+2)) : Deleted p (q+1) :=
  ({toFun := fun i => v.val.1 i, monotone' := v.val.1.monotone},
   {toFun := fun i => a.succAbove (v.val.2 i),
    monotone' := fun _ _ h => (Fin.succAboveOrderEmb a).monotone (v.val.2.monotone h)})

theorem deleted_horizontal {p q} (z : HFace p q) :
    deleted z.val.1 z.val.2 = hPair (lowerHorizontal z).1 (lowerHorizontal z).2 := by
  apply Prod.ext
  · apply OrderHom.ext
    funext i
    change z.val.1.val.1 (z.val.2.succAbove i) =
      (lowerHorizontal z).2.succAbove ((lowerHorizontal z).1.val.1 (hIndex i))
    exact (lower_x z (hIndex i)).symm
  · apply OrderHom.ext
    funext i
    exact (lower_y z (hIndex i)).symm

theorem succAbove_val {N : ℕ} (k : Fin (N+1)) (i : Fin N) :
    (k.succAbove i).val = if i.val<k.val then i.val else i.val+1 := by
  by_cases h : i.val<k.val
  · rw [Fin.succAbove_of_castSucc_lt _ _ h,if_pos h]
    rfl
  · rw [Fin.succAbove_of_le_castSucc _ _ (Nat.le_of_not_gt h),if_neg h]
    rfl

theorem flip_oldVertex {p q} (z : VFace p q) (i : Fin (p+(q+1))) :
    oldVertex (flipH z) (flipVertex i) = flipVertex (z.val.2.succAbove i) := by
  apply Fin.ext
  unfold oldVertex
  rw [succAbove_val]
  change (if i.val<z.val.2.val then i.val else i.val+1)=(z.val.2.succAbove i).val
  rw [succAbove_val]

theorem deleted_vertical {p q} (z : VFace p q) :
    deleted z.val.1 z.val.2 = vPair (lowerVertical z).1 (lowerVertical z).2 := by
  apply Prod.ext
  · apply OrderHom.ext
    funext i
    have h := lower_y (flipH z) (flipVertex i)
    rw [flip_oldVertex] at h
    exact h.symm
  · apply OrderHom.ext
    funext i
    have h := lower_x (flipH z) (flipVertex i)
    rw [flip_oldVertex] at h
    exact h.symm

def faceTerm {p q} {M : Type*} [AddCommGroup M] (F : Deleted p q → M)
    (z : Face p q) : M :=
  ((-1 : ℤ)^z.2.val * pathSign z.1) • F (deleted z.1 z.2)

def hTerm {p q} {M : Type*} [AddCommGroup M] (F : Deleted (p+1) q → M)
    (z : Path p q × Fin (p+2)) : M :=
  ((-1 : ℤ)^z.2.val * pathSign z.1) • F (hPair z.1 z.2)

def vTerm {p q} {M : Type*} [AddCommGroup M] (F : Deleted p (q+1) → M)
    (z : Path p q × Fin (q+2)) : M :=
  ((-1 : ℤ)^(p+z.2.val) * pathSign z.1) • F (vPair z.1 z.2)

theorem h_sum {p q} {M : Type*} [AddCommGroup M] (F : Deleted (p+1) q → M) :
    (∑ z : HFace p q, faceTerm F z.val) = ∑ z : Path p q × Fin (p+2), hTerm F z := by
  apply Fintype.sum_equiv (horizontalEquiv p q)
  intro z
  unfold faceTerm hTerm
  change _ = ((-1 : ℤ)^(lowerHorizontal z).2.val * pathSign (lowerPath z)) • _
  rw [horizontal_sign,deleted_horizontal]
  rfl

theorem v_sum {p q} {M : Type*} [AddCommGroup M] (F : Deleted p (q+1) → M) :
    (∑ z : VFace p q, faceTerm F z.val) = ∑ z : Path p q × Fin (q+2), vTerm F z := by
  apply Fintype.sum_equiv (verticalEquiv p q)
  intro z
  unfold faceTerm vTerm
  change _ = ((-1 : ℤ)^(p+(lowerVertical z).2.val) * pathSign (lowerVertical z).1) • _
  rw [vertical_sign,deleted_vertical]
  rfl

theorem boundary_sum {p q} {M : Type*} [AddCommGroup M] (F : Deleted (p+1) (q+1) → M) :
    (∑ u : Path (p+1) (q+1), ∑ k : Vertex (p+1) (q+1), faceTerm F (u,k)) =
      (∑ a : Fin (p+2), ∑ v : Path p (q+1), hTerm F (v,a)) +
      (∑ a : Fin (q+2), ∑ v : Path (p+1) q, vTerm F (v,a)) := by
  classical
  rw [← Fintype.sum_prod_type (faceTerm F)]
  have h := Equiv.sum_comp (facePartition p q).symm (faceTerm F)
  change (∑ z : Kinds p q, faceTerm F (forgetKind p q z)) =
    ∑ z : Face (p+1) (q+1), faceTerm F z at h
  rw [← h,Fintype.sum_sum_type,Fintype.sum_sum_type]
  change (∑ z : HFace p (q+1), faceTerm F z.val) +
    ((∑ z : VFace (p+1) q, faceTerm F z.val) + ∑ z : MixedFace (p+1) (q+1), mixedTerm F z) = _
  rw [mixed_sum_zero,add_zero,h_sum,v_sum,Fintype.sum_prod_type,Fintype.sum_prod_type]
  rw [Finset.sum_comm (f := fun v a => hTerm F (v,a)),
    Finset.sum_comm (f := fun v a => vTerm F (v,a))]

#print axioms deleted_horizontal
#print axioms deleted_vertical
#print axioms boundary_sum
end CMDG.CondensedCM5R0.EilenbergZilberBoundarySum
