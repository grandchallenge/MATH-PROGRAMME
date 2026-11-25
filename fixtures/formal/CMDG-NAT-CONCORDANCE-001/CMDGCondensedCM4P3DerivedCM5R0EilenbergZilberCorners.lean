import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberComparison

/-! Exact mixed-corner involution on the ordinal-coordinate paths of the
signed shuffle. All claims are about the original Path type. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
namespace CMDG.CondensedCM5R0.EilenbergZilberCorners

abbrev Vertex (p q : ℕ) := Fin (p+q+1)

def X {p q : ℕ} (u : Path p q) (k : Vertex p q) : ℕ := (u.val.1 k).val
def Y {p q : ℕ} (u : Path p q) (k : Vertex p q) : ℕ := (u.val.2 k).val

theorem rank {p q} (u : Path p q) (k : Vertex p q) :
    X u k + Y u k = k.val := u.property k
theorem xbound {p q} (u : Path p q) (k : Vertex p q) : X u k ≤ p :=
  Nat.le_of_lt_succ (u.val.1 k).isLt
theorem ybound {p q} (u : Path p q) (k : Vertex p q) : Y u k ≤ q :=
  Nat.le_of_lt_succ (u.val.2 k).isLt

theorem xmono {p q} (u : Path p q) : Monotone (X u) :=
  fun _ _ h => u.val.1.monotone h
theorem ymono {p q} (u : Path p q) : Monotone (Y u) :=
  fun _ _ h => u.val.2.monotone h

theorem step {p q} (u : Path p q) (i : Fin (p+q)) :
    (X u i.succ = X u i.castSucc+1 ∧ Y u i.succ = Y u i.castSucc) ∨
    (X u i.succ = X u i.castSucc ∧ Y u i.succ = Y u i.castSucc+1) := by
  have hx := xmono u (show i.castSucc ≤ i.succ by exact Nat.le_succ _)
  have hy := ymono u (show i.castSucc ≤ i.succ by exact Nat.le_succ _)
  have h₁ := rank u i.castSucc
  have h₂ := rank u i.succ
  simp only [Fin.val_succ,Fin.val_castSucc] at h₁ h₂
  omega

abbrev Interior (p q : ℕ) := {k : Vertex p q // 0 < k.val ∧ k.val < p+q}

def prev {p q} (k : Interior p q) : Vertex p q :=
  ⟨k.val.val-1,by have := k.val.isLt; omega⟩
def next {p q} (k : Interior p q) : Vertex p q :=
  ⟨k.val.val+1,by have := k.property.2; omega⟩

def Mixed {p q} (u : Path p q) (k : Interior p q) : Prop :=
  X u (next k) = X u (prev k)+1 ∧ Y u (next k) = Y u (prev k)+1

def swappedX {p q} (u : Path p q) (k : Interior p q) (i : Vertex p q) : ℕ :=
  if i=k.val then X u (prev k) + X u (next k) - X u k.val else X u i
def swappedY {p q} (u : Path p q) (k : Interior p q) (i : Vertex p q) : ℕ :=
  if i=k.val then Y u (prev k) + Y u (next k) - Y u k.val else Y u i

theorem prev_le {p q} (k : Interior p q) : prev k ≤ k.val := by
  change k.val.val-1 ≤ k.val.val
  omega
theorem le_next {p q} (k : Interior p q) : k.val ≤ next k := by
  change k.val.val ≤ k.val.val+1
  omega

theorem swappedX_bounds {p q} (u : Path p q) (k : Interior p q) :
    X u (prev k) ≤ swappedX u k k.val ∧ swappedX u k k.val ≤ X u (next k) := by
  have h₁ := xmono u (prev_le k)
  have h₂ := xmono u (le_next k)
  simp [swappedX]
  omega

theorem swappedY_bounds {p q} (u : Path p q) (k : Interior p q) :
    Y u (prev k) ≤ swappedY u k k.val ∧ swappedY u k k.val ≤ Y u (next k) := by
  have h₁ := ymono u (prev_le k)
  have h₂ := ymono u (le_next k)
  simp [swappedY]
  omega

theorem swappedX_mono {p q} (u : Path p q) (k : Interior p q) :
    Monotone (swappedX u k) := by
  intro i j hij
  by_cases hi : i=k.val
  · subst i
    by_cases hj : j=k.val
    · subst j; rfl
    · rw [show swappedX u k j = X u j by unfold swappedX; rw [if_neg hj]]
      exact (swappedX_bounds u k).2.trans (xmono u (by
        have hlt : k.val < j := lt_of_le_of_ne hij (Ne.symm hj)
        change k.val.val+1 ≤ j.val
        exact hlt))
  · by_cases hj : j=k.val
    · subst j
      rw [swappedX,if_neg hi]
      exact (xmono u (by
        have hlt : i < k.val := lt_of_le_of_ne hij hi
        change i.val ≤ k.val.val-1
        change i.val < k.val.val at hlt
        omega)).trans (swappedX_bounds u k).1
    · rw [swappedX,if_neg hi,swappedX,if_neg hj]
      exact xmono u hij

theorem swappedY_mono {p q} (u : Path p q) (k : Interior p q) :
    Monotone (swappedY u k) := by
  intro i j hij
  by_cases hi : i=k.val
  · subst i
    by_cases hj : j=k.val
    · subst j; rfl
    · rw [show swappedY u k j = Y u j by unfold swappedY; rw [if_neg hj]]
      exact (swappedY_bounds u k).2.trans (ymono u (by
        have hlt : k.val < j := lt_of_le_of_ne hij (Ne.symm hj)
        change k.val.val+1 ≤ j.val
        exact hlt))
  · by_cases hj : j=k.val
    · subst j
      rw [swappedY,if_neg hi]
      exact (ymono u (by
        have hlt : i < k.val := lt_of_le_of_ne hij hi
        change i.val ≤ k.val.val-1
        change i.val < k.val.val at hlt
        omega)).trans (swappedY_bounds u k).1
    · rw [swappedY,if_neg hi,swappedY,if_neg hj]
      exact ymono u hij

def swap {p q} (u : Path p q) (k : Interior p q) : Path p q :=
  ⟨({toFun := fun i => ⟨swappedX u k i,by
      by_cases h : i=k.val
      · subst i; have := (swappedX_bounds u k).2; have := xbound u (next k); omega
      · rw [swappedX,if_neg h]; have := xbound u i; omega⟩,
      monotone' := swappedX_mono u k},
    {toFun := fun i => ⟨swappedY u k i,by
      by_cases h : i=k.val
      · subst i; have := (swappedY_bounds u k).2; have := ybound u (next k); omega
      · rw [swappedY,if_neg h]; have := ybound u i; omega⟩,
      monotone' := swappedY_mono u k}), by
    intro i
    change swappedX u k i + swappedY u k i = i.val
    by_cases hi : i=k.val
    · subst i
      have hx := xmono u (prev_le k)
      have hx' := xmono u (le_next k)
      have hy := ymono u (prev_le k)
      have hy' := ymono u (le_next k)
      have h₁ := rank u (prev k)
      have h₂ := rank u (next k)
      have h₃ := rank u k.val
      have h₄ := k.property.1
      simp only [swappedX,swappedY,if_true,prev,next] at *
      omega
    · rw [swappedX,if_neg hi,swappedY,if_neg hi]
      exact rank u i⟩

theorem swap_x {p q} (u : Path p q) (k : Interior p q) (i : Vertex p q) :
    X (swap u k) i = swappedX u k i := rfl
theorem swap_y {p q} (u : Path p q) (k : Interior p q) (i : Vertex p q) :
    Y (swap u k) i = swappedY u k i := rfl

theorem prev_ne {p q} (k : Interior p q) : prev k ≠ k.val := by
  intro h
  have hh := congrArg Fin.val h
  change k.val.val-1 = k.val.val at hh
  have := k.property.1
  omega

theorem next_ne {p q} (k : Interior p q) : next k ≠ k.val := by
  intro h
  have hh := congrArg Fin.val h
  change k.val.val+1 = k.val.val at hh
  omega

theorem swap_mixed {p q} (u : Path p q) (k : Interior p q) :
    Mixed (swap u k) k ↔ Mixed u k := by
  unfold Mixed
  simp only [swap_x,swap_y,swappedX,swappedY,if_neg (prev_ne k),if_neg (next_ne k)]

theorem swap_involution {p q} (u : Path p q) (k : Interior p q) :
    swap (swap u k) k = u := by
  apply Subtype.ext
  apply Prod.ext
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    change X (swap (swap u k) k) i = X u i
    by_cases hi : i=k.val
    · subst i
      rw [swap_x,swappedX,if_pos rfl,swap_x,swappedX,if_neg (prev_ne k),
        swap_x,swappedX,if_neg (next_ne k),swap_x,swappedX,if_pos rfl]
      have := xmono u (le_next k)
      omega
    · rw [swap_x,swappedX,if_neg hi,swap_x,swappedX,if_neg hi]
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    change Y (swap (swap u k) k) i = Y u i
    by_cases hi : i=k.val
    · subst i
      rw [swap_y,swappedY,if_pos rfl,swap_y,swappedY,if_neg (prev_ne k),
        swap_y,swappedY,if_neg (next_ne k),swap_y,swappedY,if_pos rfl]
      have := ymono u (le_next k)
      omega
    · rw [swap_y,swappedY,if_neg hi,swap_y,swappedY,if_neg hi]

def leftEdge {p q} (k : Interior p q) : Fin (p+q) :=
  ⟨k.val.val-1,by have := k.property.2; omega⟩
def rightEdge {p q} (k : Interior p q) : Fin (p+q) :=
  ⟨k.val.val,k.property.2⟩

theorem left_cast {p q} (k : Interior p q) : (leftEdge k).castSucc = prev k := rfl
theorem left_succ {p q} (k : Interior p q) : (leftEdge k).succ = k.val := by
  apply Fin.ext
  have := k.property.1
  change k.val.val-1+1=k.val.val
  omega
theorem right_cast {p q} (k : Interior p q) : (rightEdge k).castSucc = k.val := rfl
theorem right_succ {p q} (k : Interior p q) : (rightEdge k).succ = next k := rfl

theorem edges_ne {p q} (k : Interior p q) : leftEdge k ≠ rightEdge k := by
  intro h
  have hh := congrArg Fin.val h
  change k.val.val-1=k.val.val at hh
  have := k.property.1
  omega

def weight {p q} (u : Path p q) (i : Fin (p+q)) : ℕ :=
  if X u i.castSucc < X u i.succ then Y u i.castSucc else 0

def exponent {p q} (u : Path p q) : ℕ := ∑ i : Fin (p+q), weight u i

theorem sign_exponent {p q} (u : Path p q) : pathSign u = (-1 : ℤ)^(exponent u) := rfl

theorem weight_unchanged {p q} (u : Path p q) (k : Interior p q) (i : Fin (p+q))
    (hl : i ≠ leftEdge k) (hr : i ≠ rightEdge k) :
    weight (swap u k) i = weight u i := by
  have h₁ : i.castSucc ≠ k.val := by
    intro h
    apply hr
    exact Fin.ext (congrArg (fun t : Vertex p q => t.val) h)
  have h₂ : i.succ ≠ k.val := by
    intro h
    apply hl
    apply Fin.ext
    have hh := congrArg Fin.val h
    change i.val+1=k.val.val at hh
    change i.val=k.val.val-1
    omega
  simp only [weight,swap_x,swap_y,swappedX,swappedY,if_neg h₁,if_neg h₂]

theorem weight_left {p q} (u : Path p q) (k : Interior p q) :
    weight u (leftEdge k) =
      if X u (prev k) < X u k.val then Y u (prev k) else 0 := by
  rw [weight,left_cast,left_succ]

theorem weight_right {p q} (u : Path p q) (k : Interior p q) :
    weight u (rightEdge k) =
      if X u k.val < X u (next k) then Y u k.val else 0 := by
  rw [weight,right_cast,right_succ]

theorem local_weights {p q} (u : Path p q) (k : Interior p q) (hm : Mixed u k) :
    (weight (swap u k) (leftEdge k) + weight (swap u k) (rightEdge k) =
       weight u (leftEdge k) + weight u (rightEdge k) + 1) ∨
    (weight u (leftEdge k) + weight u (rightEdge k) =
       weight (swap u k) (leftEdge k) + weight (swap u k) (rightEdge k) + 1) := by
  have hstep := step u (leftEdge k)
  rw [left_cast,left_succ] at hstep
  obtain ⟨hx,hy⟩ := hm
  simp only [weight_left,weight_right,swap_x,swap_y,swappedX,swappedY,
    if_neg (prev_ne k),if_neg (next_ne k),if_true]
  rcases hstep with h | h
  · obtain ⟨h₁,h₂⟩ := h
    left
    rw [hx,hy,h₁,h₂]
    simp
  · obtain ⟨h₁,h₂⟩ := h
    right
    rw [hx,hy,h₁,h₂]
    simp

theorem exponent_decompose {p q} (u : Path p q) (k : Interior p q) :
    exponent u =
      (∑ i ∈ (Finset.univ.erase (leftEdge k)).erase (rightEdge k), weight u i) +
      weight u (rightEdge k) + weight u (leftEdge k) := by
  classical
  unfold exponent
  have hl : leftEdge k ∈ (Finset.univ : Finset (Fin (p+q))) := Finset.mem_univ _
  have hr : rightEdge k ∈ (Finset.univ : Finset (Fin (p+q))).erase (leftEdge k) :=
    Finset.mem_erase.mpr ⟨Ne.symm (edges_ne k), Finset.mem_univ _⟩
  rw [← Finset.sum_erase_add _ _ hl,← Finset.sum_erase_add _ _ hr]

theorem exponent_swap {p q} (u : Path p q) (k : Interior p q) (hm : Mixed u k) :
    exponent (swap u k) = exponent u + 1 ∨ exponent u = exponent (swap u k)+1 := by
  classical
  have he : (∑ i ∈ (Finset.univ.erase (leftEdge k)).erase (rightEdge k), weight (swap u k) i) =
    (∑ i ∈ (Finset.univ.erase (leftEdge k)).erase (rightEdge k), weight u i) := by
    apply Finset.sum_congr rfl
    intro i hi
    obtain ⟨hr,hl'⟩ := Finset.mem_erase.mp hi
    obtain ⟨hl,_⟩ := Finset.mem_erase.mp hl'
    exact weight_unchanged u k i hl hr
  rw [exponent_decompose (swap u k) k,exponent_decompose u k,he]
  have h := local_weights u k hm
  omega

theorem sign_swap {p q} (u : Path p q) (k : Interior p q) (hm : Mixed u k) :
    pathSign (swap u k) = - pathSign u := by
  rw [sign_exponent,sign_exponent]
  rcases exponent_swap u k hm with h | h
  · rw [h,pow_succ,mul_neg,mul_one]
  · rw [h,pow_succ,mul_neg,mul_one,neg_neg]

abbrev Deleted (p q : ℕ) :=
  (Fin (p+q) →o Fin (p+1)) × (Fin (p+q) →o Fin (q+1))

def deleted {p q} (u : Path p q) (k : Vertex p q) : Deleted p q :=
  (u.val.1.comp (Fin.succAboveOrderEmb k).toOrderHom,
    u.val.2.comp (Fin.succAboveOrderEmb k).toOrderHom)

theorem deleted_swap {p q} (u : Path p q) (k : Interior p q) :
    deleted (swap u k) k.val = deleted u k.val := by
  apply Prod.ext
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    change X (swap u k) (k.val.succAbove i) = X u (k.val.succAbove i)
    rw [swap_x,swappedX,if_neg (Fin.succAbove_ne _ _)]
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    change Y (swap u k) (k.val.succAbove i) = Y u (k.val.succAbove i)
    rw [swap_y,swappedY,if_neg (Fin.succAbove_ne _ _)]

theorem swap_ne {p q} (u : Path p q) (k : Interior p q) (hm : Mixed u k) :
    swap u k ≠ u := by
  intro h
  have he := exponent_swap u k hm
  rw [h] at he
  omega

abbrev MixedFace (p q : ℕ) := {z : Path p q × Interior p q // Mixed z.1 z.2}

noncomputable instance (p q : ℕ) : Fintype (MixedFace p q) := Fintype.ofFinite _

def swapFace {p q} (z : MixedFace p q) : MixedFace p q :=
  ⟨(swap z.val.1 z.val.2,z.val.2),(swap_mixed _ _).mpr z.property⟩

theorem swapFace_involution {p q} (z : MixedFace p q) :
    swapFace (swapFace z) = z := by
  apply Subtype.ext
  apply Prod.ext
  · exact swap_involution _ _
  · rfl

theorem swapFace_ne {p q} (z : MixedFace p q) : swapFace z ≠ z := by
  intro h
  exact swap_ne z.val.1 z.val.2 z.property (congrArg (fun t : MixedFace p q => t.val.1) h)

def mixedTerm {p q} {M : Type*} [AddCommGroup M]
    (F : Deleted p q → M) (z : MixedFace p q) : M :=
  ((-1 : ℤ)^z.val.2.val.val * pathSign z.val.1) • F (deleted z.val.1 z.val.2.val)

theorem mixedTerm_swap {p q} {M : Type*} [AddCommGroup M]
    (F : Deleted p q → M) (z : MixedFace p q) :
    mixedTerm F (swapFace z) = - mixedTerm F z := by
  unfold mixedTerm
  change ((-1 : ℤ)^z.val.2.val.val * pathSign (swap z.val.1 z.val.2)) •
    F (deleted (swap z.val.1 z.val.2) z.val.2.val) = _
  rw [sign_swap _ _ z.property,deleted_swap,mul_neg,neg_smul]

/-- The entire mixed-corner portion of the signed boundary cancels,
for any additive evaluation of the actual deleted coordinate pair. -/
theorem mixed_sum_zero {p q} {M : Type*} [AddCommGroup M] (F : Deleted p q → M) :
    ∑ z : MixedFace p q, mixedTerm F z = 0 := by
  classical
  apply Finset.sum_ninvolution swapFace
  · intro z
    rw [mixedTerm_swap,add_neg_cancel]
  · intro z _
    exact swapFace_ne z
  · intro z
    exact Finset.mem_univ _
  · exact swapFace_involution

#print axioms step
#print axioms swap
#print axioms swap_mixed
#print axioms swap_involution
#print axioms sign_swap
#print axioms mixed_sum_zero
end CMDG.CondensedCM5R0.EilenbergZilberCorners
