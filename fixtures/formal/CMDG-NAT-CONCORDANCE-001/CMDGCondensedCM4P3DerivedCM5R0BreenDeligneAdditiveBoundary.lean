import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBottomAugmentation

/-! Bottom Hurewicz for the genuine reduced integral Eilenberg–MacLane
chain complex in positive degree. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology AlgebraicTopology.DoldKan
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
namespace CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary

set_option backward.isDefEq.respectTransparency false in
theorem generator_zero (A : AGrp) : reducedGenerator A 0 = 0 := by
  apply (AddCommGrpCat.mono_iff_injective (kernel.ι (augmentation A))).mp inferInstance
  have h := CategoryTheory.congr_fun (reducedProjectionApp_ι A) (FreeAbelianGroup.of (0 : A))
  change kernel.ι (augmentation A) (reducedProjectionApp A (FreeAbelianGroup.of (0 : A))) =
    (𝟙 (forgetFree.obj A) - augmentation A ≫ basepoint A) (FreeAbelianGroup.of (0 : A)) at h
  change kernel.ι (augmentation A) (reducedProjectionApp A (FreeAbelianGroup.of (0 : A))) =
    kernel.ι (augmentation A) 0
  rw [h]
  change FreeAbelianGroup.of (0 : A) - FreeAbelianGroup.of (0 : A) = _
  rw [sub_self]
  exact (map_zero (kernel.ι (augmentation A)).hom).symm

set_option backward.isDefEq.respectTransparency false in
theorem generator_natural {A B : AGrp} (f : A ⟶ B) (x : A) :
    reducedFree.map f (reducedGenerator A x) = reducedGenerator B (f x) := by
  have h := CategoryTheory.congr_fun (reducedProjection.naturality f) (FreeAbelianGroup.of x)
  change reducedProjectionApp B (FreeAbelianGroup.map (fun y : A => f y) (FreeAbelianGroup.of x)) =
    reducedFree.map f (reducedProjectionApp A (FreeAbelianGroup.of x)) at h
  rw [FreeAbelianGroup.map_of_apply] at h
  exact h.symm

section Faces
variable (X : SimplicialObject AGrp) (k : ℕ)
variable (hz : IsZero (X.obj (op (SimplexCategory.mk k))))

abbrev simplex (X : SimplicialObject AGrp) (n : ℕ) :=
  X.obj (op (SimplexCategory.mk n))

def witness (a b : simplex X (k+1)) : simplex X (k+2) :=
  X.σ (0 : Fin (k+2)) a + X.σ (1 : Fin (k+2)) b

include hz in
private theorem face_zero (i : Fin (k+2)) : X.δ i = 0 := hz.eq_of_tgt _ _

include hz in
set_option backward.isDefEq.respectTransparency false in
theorem face_witness_zero (a b : simplex X (k+1)) :
    X.δ (0 : Fin (k+3)) (witness X k a b) = a := by
  have h0 : X.σ (0 : Fin (k+2)) ≫ X.δ (0 : Fin (k+3)) = 𝟙 _ :=
    X.δ_comp_σ_self' (by ext; rfl)
  have h1 : X.σ (1 : Fin (k+2)) ≫ X.δ (0 : Fin (k+3)) = 0 := by
    have h := X.δ_comp_σ_of_le (n := k) (i := 0) (j := 0) (by simp)
    change X.σ (1 : Fin (k+2)) ≫ X.δ (0 : Fin (k+3)) = _ at h
    rw [face_zero X k hz, zero_comp] at h
    exact h
  have h0' := CategoryTheory.congr_fun h0 a
  have h1' := CategoryTheory.congr_fun h1 b
  change X.δ _ (X.σ _ a) = a at h0'
  change X.δ _ (X.σ _ b) = 0 at h1'
  unfold witness
  rw [map_add, h0', h1', add_zero]

set_option backward.isDefEq.respectTransparency false in
theorem face_witness_one (a b : simplex X (k+1)) :
    X.δ (1 : Fin (k+3)) (witness X k a b) = a + b := by
  have h0 : X.σ (0 : Fin (k+2)) ≫ X.δ (1 : Fin (k+3)) = 𝟙 _ :=
    X.δ_comp_σ_succ' (by ext; rfl)
  have h1 : X.σ (1 : Fin (k+2)) ≫ X.δ (1 : Fin (k+3)) = 𝟙 _ :=
    X.δ_comp_σ_self' (by ext; rfl)
  have h0' := CategoryTheory.congr_fun h0 a
  have h1' := CategoryTheory.congr_fun h1 b
  change X.δ _ (X.σ _ a) = a at h0'
  change X.δ _ (X.σ _ b) = b at h1'
  unfold witness
  rw [map_add, h0', h1']

include hz in
set_option backward.isDefEq.respectTransparency false in
theorem face_witness_two (a b : simplex X (k+1)) :
    X.δ (2 : Fin (k+3)) (witness X k a b) = b := by
  have h0 : X.σ (0 : Fin (k+2)) ≫ X.δ (2 : Fin (k+3)) = 0 := by
    rw [X.δ_comp_σ_of_gt' (by change 1 < 2 % (k+3); rw [Nat.mod_eq_of_lt (by omega)]; decide), face_zero X k hz, zero_comp]
  have h1 : X.σ (1 : Fin (k+2)) ≫ X.δ (2 : Fin (k+3)) = 𝟙 _ :=
    X.δ_comp_σ_succ' (by ext; rfl)
  have h0' := CategoryTheory.congr_fun h0 a
  have h1' := CategoryTheory.congr_fun h1 b
  change X.δ _ (X.σ _ a) = 0 at h0'
  change X.δ _ (X.σ _ b) = b at h1'
  unfold witness
  rw [map_add, h0', h1', zero_add]

include hz in
set_option backward.isDefEq.respectTransparency false in
theorem face_witness_tail (a b : simplex X (k+1)) (i : Fin k) :
    X.δ i.succ.succ.succ (witness X k a b) = 0 := by
  have h0 : X.σ (0 : Fin (k+2)) ≫ X.δ i.succ.succ.succ = 0 := by
    rw [X.δ_comp_σ_of_gt' (by simp [Fin.lt_def, Fin.val_succ]), face_zero X k hz, zero_comp]
  have h1 : X.σ (1 : Fin (k+2)) ≫ X.δ i.succ.succ.succ = 0 := by
    rw [X.δ_comp_σ_of_gt' (by change 2 % (k+3) < i.val + 3; rw [Nat.mod_eq_of_lt (by omega)]; omega), face_zero X k hz, zero_comp]
  have h0' := CategoryTheory.congr_fun h0 a
  have h1' := CategoryTheory.congr_fun h1 b
  change X.δ _ (X.σ _ a) = 0 at h0'
  change X.δ _ (X.σ _ b) = 0 at h1'
  unfold witness
  rw [map_add, h0', h1', zero_add]

def redComplex (X : SimplicialObject AGrp) : ChainComplex AGrp ℕ :=
  (alternatingFaceMapComplex AGrp).obj ((SimplicialObject.whiskering AGrp AGrp).obj reducedFree |>.obj X)

include hz in
set_option backward.isDefEq.respectTransparency false in
theorem witness_boundary (a b : simplex X (k+1)) :
    (redComplex X).d (k+2) (k+1) (reducedGenerator (simplex X (k+2)) (witness X k a b)) =
      reducedGenerator (simplex X (k+1)) a -
      reducedGenerator (simplex X (k+1)) (a+b) +
      reducedGenerator (simplex X (k+1)) b := by
  let Y := ((SimplicialObject.whiskering AGrp AGrp).obj reducedFree).obj X
  have hd := AlternatingFaceMapComplex.obj_d_eq Y (k+1)
  have h := CategoryTheory.congr_fun hd (reducedGenerator (simplex X (k+2)) (witness X k a b))
  change (redComplex X).d (k+2) (k+1) (reducedGenerator (simplex X (k+2)) (witness X k a b)) =
    (∑ i : Fin (k+3), (-1 : ℤ) ^ (i : ℕ) • reducedFree.map (X.δ i))
      (reducedGenerator (simplex X (k+2)) (witness X k a b)) at h
  rw [h]
  change (∑ i : Fin (k+3), (-1 : ℤ) ^ (i : ℕ) • reducedFree.map (X.δ i))
    (reducedGenerator (simplex X (k+2)) (witness X k a b)) = _
  change AddCommGrpCat.homAddEquiv
    (∑ i : Fin (k+3), (-1 : ℤ) ^ (i : ℕ) • reducedFree.map (X.δ i))
    (reducedGenerator (simplex X (k+2)) (witness X k a b)) = _
  rw [map_sum]
  change (AddMonoidHom.eval (reducedGenerator (simplex X (k+2)) (witness X k a b)))
    (∑ i : Fin (k+3), AddCommGrpCat.homAddEquiv ((-1 : ℤ) ^ (i : ℕ) • reducedFree.map (X.δ i))) = _
  rw [map_sum]
  simp only [map_zsmul]
  change (∑ i : Fin (k+3), (-1 : ℤ) ^ (i : ℕ) •
    reducedFree.map (X.δ i) (reducedGenerator (simplex X (k+2)) (witness X k a b))) = _
  have hg (i : Fin (k+3)) := generator_natural (X.δ i) (witness X k a b)
  simp_rw [hg]
  rw [Fin.sum_univ_succ, Fin.sum_univ_succ, Fin.sum_univ_succ]
  have h1 : (Fin.succ (0 : Fin (k+2))) = (1 : Fin (k+3)) := by ext; rfl
  have h2 : (Fin.succ (Fin.succ (0 : Fin (k+1)))) = (2 : Fin (k+3)) := by ext; rfl
  rw [h1, h2, face_witness_zero X k hz, face_witness_one X k, face_witness_two X k hz]
  have ht : (∑ i : Fin k, (-1 : ℤ) ^ (i.succ.succ.succ : ℕ) •
      reducedGenerator (simplex X (k+1)) (X.δ i.succ.succ.succ (witness X k a b))) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    rw [face_witness_tail X k hz, generator_zero, smul_zero]
  rw [ht]
  simp [sub_eq_add_neg, add_assoc, Nat.mod_eq_of_lt (show 2 < k+3 by omega)]

end Faces
#print axioms witness_boundary
end CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary
