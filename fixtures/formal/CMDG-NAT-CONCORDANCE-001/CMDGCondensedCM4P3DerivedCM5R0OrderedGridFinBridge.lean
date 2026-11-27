import CMDGCondensedCM4P3DerivedCM5R0OrderedGridContraction

noncomputable section
universe u
namespace CMDG.CondensedCM5R0.CompactCover.OrderedGrid

theorem alt_ofFn {A : Type u} (c : A → ℤ) (n : ℕ) (x : Fin n → A) :
    alt c (List.ofFn x) = ∑ i : Fin n, (-1 : ℤ) ^ (i : ℕ) * c (x i) := by
  induction n with
  | zero => simp [alt]
  | succ n ih =>
    rw [List.ofFn_succ, alt, ih, Fin.sum_univ_succ]
    simp only [Fin.val_zero,pow_zero,one_mul,Fin.val_succ,pow_succ,mul_neg,mul_one,
      neg_mul,Finset.sum_neg_distrib,sub_eq_add_neg]

theorem faces_ofFn {A : Type u} (n : ℕ) (x : Fin (n+1) → A) :
    faces (List.ofFn x) = List.ofFn (fun i : Fin (n+1) => List.ofFn (x ∘ i.succAbove)) := by
  induction n with
  | zero => simp [List.ofFn_succ,faces]
  | succ n ih =>
    conv_lhs => rw [List.ofFn_succ, faces, ih]
    conv_rhs => rw [List.ofFn_succ]
    congr 1
    rw [← List.ofFn_comp']
    congr 1
    funext i
    conv_rhs => rw [List.ofFn_succ]
    congr 1
    apply congrArg List.ofFn
    funext j
    simp [Function.comp_apply,Fin.succ_succAbove_succ]

theorem D_ofFn {A : Type u} (c : List A → ℤ) (n : ℕ) (x : Fin (n+1) → A) :
    D c (List.ofFn x) =
      ∑ i : Fin (n+1), (-1 : ℤ) ^ (i : ℕ) * c (List.ofFn (x ∘ i.succAbove)) := by
  rw [D,faces_ofFn,alt_ofFn]

theorem valid_ofFn {I : Type u} (M n : ℕ) (x : Fin n → Vertex I) :
    valid M (List.ofFn x) ↔
      (∀ j i, x j i ≤ M) ∧ (∀ j k i, x j i ≤ x k i + 1) := by
  simp only [valid,List.mem_ofFn]
  constructor
  · rintro ⟨h₁,h₂⟩
    exact ⟨fun j i => h₁ _ ⟨j,rfl⟩ i,fun j k i => h₂ _ ⟨j,rfl⟩ _ ⟨k,rfl⟩ i⟩
  · rintro ⟨h₁,h₂⟩
    constructor
    · rintro _ ⟨j,rfl⟩; exact h₁ j
    · rintro _ ⟨j,rfl⟩ _ ⟨k,rfl⟩; exact h₂ j k

#print axioms D_ofFn
#print axioms valid_ofFn
end CMDG.CondensedCM5R0.CompactCover.OrderedGrid
