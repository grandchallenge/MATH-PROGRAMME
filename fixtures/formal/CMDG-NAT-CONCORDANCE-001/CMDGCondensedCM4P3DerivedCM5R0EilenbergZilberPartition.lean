import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberTranspose

/-! Exhaustive disjoint partition of all deleted path vertices. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCorners
open CMDG.CondensedCM5R0.EilenbergZilberStraight
open CMDG.CondensedCM5R0.EilenbergZilberTranspose
namespace CMDG.CondensedCM5R0.EilenbergZilberPartition

theorem unique_of_adjacent {N : ℕ} (f : Fin (N+1) → ℕ) (hf : Monotone f)
    (k : Fin (N+1))
    (hl : ∀ i : Fin N, i.succ=k → f i.castSucc < f k)
    (hr : ∀ i : Fin N, i.castSucc=k → f k < f i.succ) :
    ∀ j, f j=f k → j=k := by
  intro j hj
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · let i : Fin N := ⟨k.val-1,by have := k.isLt; change j.val<k.val at h; omega⟩
    have he : i.succ=k := by apply Fin.ext; change k.val-1+1=k.val; change j.val<k.val at h; omega
    have hle : j ≤ i.castSucc := by change j.val≤k.val-1; change j.val<k.val at h; omega
    have hh := (hf hle).trans_lt (hl i he)
    omega
  · let i : Fin N := ⟨k.val,by have := j.isLt; change k.val<j.val at h; omega⟩
    have he : i.castSucc=k := rfl
    have hle : i.succ ≤ j := by change k.val+1≤j.val; exact h
    have hh := (hr i he).trans_le (hf hle)
    omega

theorem uniqueX_not_uniqueY {p q} (u : Path p q) (k : Vertex p q) (hp : 0<p+q)
    (hx : UniqueX u k) : ¬ UniqueY u k := by
  intro hy
  by_cases h : k.val<p+q
  · let i : Fin (p+q) := ⟨k.val,h⟩
    have he : i.castSucc=k := rfl
    have hn : i.succ≠k := by intro he; have hh := congrArg Fin.val he; change k.val+1=k.val at hh; omega
    have hs := step u i
    rw [he] at hs
    rcases hs with h | h
    · exact hn (hy i.succ h.2)
    · exact hn (hx i.succ h.1)
  · have hk : k.val=p+q := by have := k.isLt; omega
    let i : Fin (p+q) := ⟨k.val-1,by omega⟩
    have he : i.succ=k := by apply Fin.ext; change k.val-1+1=k.val; omega
    have hn : i.castSucc≠k := by intro he; have hh := congrArg Fin.val he; change k.val-1=k.val at hh; omega
    have hs := step u i
    rw [he] at hs
    rcases hs with h | h
    · exact hn (hy i.castSucc h.2.symm)
    · exact hn (hx i.castSucc h.1.symm)

theorem mixed_not_uniqueX {p q} (u : Path p q) (k : Interior p q)
    (hm : Mixed u k) : ¬ UniqueX u k.val := by
  intro hx
  have h₁ := xmono u (prev_le k)
  have h₂ := xmono u (le_next k)
  have hn₁ : X u (prev k) ≠ X u k.val := fun h => prev_ne k (hx _ h)
  have hn₂ : X u (next k) ≠ X u k.val := fun h => next_ne k (hx _ h)
  exact (by obtain ⟨h,_⟩ := hm; omega)

theorem mixed_not_uniqueY {p q} (u : Path p q) (k : Interior p q)
    (hm : Mixed u k) : ¬ UniqueY u k.val := by
  intro hy
  have h₁ := ymono u (prev_le k)
  have h₂ := ymono u (le_next k)
  have hn₁ : Y u (prev k) ≠ Y u k.val := fun h => prev_ne k (hy _ h)
  have hn₂ : Y u (next k) ≠ Y u k.val := fun h => next_ne k (hy _ h)
  exact (by obtain ⟨_,h⟩ := hm; omega)

theorem endpoint_zero {p q} (u : Path p q) (k : Vertex p q) (hp : 0<p+q)
    (hk : k.val=0) : UniqueX u k ∨ UniqueY u k := by
  let i : Fin (p+q) := ⟨0,hp⟩
  have he : i.castSucc=k := Fin.ext hk.symm
  have hs := step u i
  rw [he] at hs
  rcases hs with h | h
  · left
    apply unique_of_adjacent (X u) (xmono u) k
    · intro j hj
      have hh := congrArg Fin.val hj
      change j.val+1=k.val at hh
      omega
    · intro j hj
      have hji : j=i := Fin.ext ((congrArg Fin.val hj).trans hk)
      subst j
      omega
  · right
    apply unique_of_adjacent (Y u) (ymono u) k
    · intro j hj
      have hh := congrArg Fin.val hj
      change j.val+1=k.val at hh
      omega
    · intro j hj
      have hji : j=i := Fin.ext ((congrArg Fin.val hj).trans hk)
      subst j
      omega

theorem endpoint_last {p q} (u : Path p q) (k : Vertex p q) (hp : 0<p+q)
    (hk : k.val=p+q) : UniqueX u k ∨ UniqueY u k := by
  let i : Fin (p+q) := ⟨k.val-1,by omega⟩
  have he : i.succ=k := by apply Fin.ext; change k.val-1+1=k.val; omega
  have hs := step u i
  rw [he] at hs
  rcases hs with h | h
  · left
    apply unique_of_adjacent (X u) (xmono u) k
    · intro j hj
      have hh := congrArg Fin.val hj
      change j.val+1=k.val at hh
      have hji : j=i := Fin.ext (by change j.val=k.val-1; omega)
      subst j
      omega
    · intro j hj
      have hh := congrArg Fin.val hj
      change j.val=k.val at hh
      have := j.isLt
      omega
  · right
    apply unique_of_adjacent (Y u) (ymono u) k
    · intro j hj
      have hh := congrArg Fin.val hj
      change j.val+1=k.val at hh
      have hji : j=i := Fin.ext (by change j.val=k.val-1; omega)
      subst j
      omega
    · intro j hj
      have hh := congrArg Fin.val hj
      change j.val=k.val at hh
      have := j.isLt
      omega

theorem interior_classify {p q} (u : Path p q) (k : Interior p q) :
    UniqueX u k.val ∨ UniqueY u k.val ∨ Mixed u k := by
  have hl := step u (leftEdge k)
  have hr := step u (rightEdge k)
  rw [left_cast,left_succ] at hl
  rw [right_cast,right_succ] at hr
  rcases hl with hl | hl <;> rcases hr with hr | hr
  · left
    apply unique_of_adjacent (X u) (xmono u) k.val
    · intro j hj
      have he : j=leftEdge k := Fin.ext (by
        have hh := congrArg Fin.val hj
        change j.val+1=k.val.val at hh
        change j.val=k.val.val-1
        omega)
      subst j
      rw [left_cast]
      omega
    · intro j hj
      have he : j=rightEdge k := Fin.ext (congrArg (fun t : Vertex p q => t.val) hj)
      subst j
      rw [right_succ]
      omega
  · right; right; unfold Mixed; omega
  · right; right; unfold Mixed; omega
  · right; left
    apply unique_of_adjacent (Y u) (ymono u) k.val
    · intro j hj
      have he : j=leftEdge k := Fin.ext (by
        have hh := congrArg Fin.val hj
        change j.val+1=k.val.val at hh
        change j.val=k.val.val-1
        omega)
      subst j
      rw [left_cast]
      omega
    · intro j hj
      have he : j=rightEdge k := Fin.ext (congrArg (fun t : Vertex p q => t.val) hj)
      subst j
      rw [right_succ]
      omega

theorem mixed_of_not_unique {p q} (u : Path p q) (k : Vertex p q) (hp : 0<p+q)
    (hx : ¬ UniqueX u k) (hy : ¬ UniqueY u k) :
    ∃ j : Interior p q, j.val=k ∧ Mixed u j := by
  have h₀ : 0<k.val := by
    by_contra! h
    exact (endpoint_zero u k hp (by omega)).elim hx hy
  have h₁ : k.val<p+q := by
    by_contra! h
    have := k.isLt
    exact (endpoint_last u k hp (by omega)).elim hx hy
  let j : Interior p q := ⟨k,h₀,h₁⟩
  exact ⟨j,rfl,(interior_classify u j).resolve_left hx |>.resolve_left hy⟩

abbrev Face (p q : ℕ) := Path p q × Vertex p q
abbrev Kinds (p q : ℕ) := HFace p (q+1) ⊕ (VFace (p+1) q ⊕ MixedFace (p+1) (q+1))

noncomputable instance (p q : ℕ) : Fintype (HFace p q) := Fintype.ofFinite _
noncomputable instance (p q : ℕ) : Fintype (VFace p q) := Fintype.ofFinite _

def chosenMixed (p q : ℕ) (z : Face (p+1) (q+1))
    (hx : ¬ UniqueX z.1 z.2) (hy : ¬ UniqueY z.1 z.2) : MixedFace (p+1) (q+1) :=
  let h := mixed_of_not_unique z.1 z.2 (by omega) hx hy
  ⟨(z.1,Classical.choose h),(Classical.choose_spec h).2⟩

theorem chosenMixed_vertex (p q : ℕ) (z : Face (p+1) (q+1))
    (hx : ¬ UniqueX z.1 z.2) (hy : ¬ UniqueY z.1 z.2) :
    (chosenMixed p q z hx hy).val.2.val=z.2 :=
  (Classical.choose_spec (mixed_of_not_unique z.1 z.2 (by omega) hx hy)).1

local instance {p q : ℕ} (u : Path p q) (k : Vertex p q) : Decidable (UniqueX u k) := Classical.propDecidable _
local instance {p q : ℕ} (u : Path p q) (k : Vertex p q) : Decidable (UniqueY u k) := Classical.propDecidable _

def classify (p q : ℕ) (z : Face (p+1) (q+1)) : Kinds p q :=
  if hx : UniqueX z.1 z.2 then Sum.inl ⟨z,hx⟩
  else if hy : UniqueY z.1 z.2 then Sum.inr (Sum.inl ⟨z,hy⟩)
  else Sum.inr (Sum.inr (chosenMixed p q z hx hy))

def forgetKind (p q : ℕ) : Kinds p q → Face (p+1) (q+1)
  | Sum.inl z => z.val
  | Sum.inr (Sum.inl z) => z.val
  | Sum.inr (Sum.inr z) => (z.val.1,z.val.2.val)

theorem forget_classify (p q : ℕ) (z : Face (p+1) (q+1)) :
    forgetKind p q (classify p q z)=z := by
  unfold classify
  split_ifs with hx hy
  · rfl
  · rfl
  · apply Prod.ext
    · rfl
    · exact chosenMixed_vertex p q z hx hy

theorem classify_forget (p q : ℕ) (z : Kinds p q) :
    classify p q (forgetKind p q z)=z := by
  rcases z with z | (z | z)
  · change classify p q z.val=_
    unfold classify
    rw [dif_pos z.property]
  · change classify p q z.val=_
    unfold classify
    have hx : ¬ UniqueX z.val.1 z.val.2 := fun h =>
      uniqueX_not_uniqueY _ _ (by omega) h z.property
    rw [dif_neg hx,dif_pos z.property]
  · let t : Face (p+1) (q+1) := (z.val.1,z.val.2.val)
    change classify p q t=_
    unfold classify
    have hx : ¬ UniqueX t.1 t.2 := mixed_not_uniqueX _ _ z.property
    have hy : ¬ UniqueY t.1 t.2 := mixed_not_uniqueY _ _ z.property
    rw [dif_neg hx,dif_neg hy]
    congr 2
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · apply Subtype.ext
      exact chosenMixed_vertex p q t hx hy

def facePartition (p q : ℕ) : Face (p+1) (q+1) ≃ Kinds p q where
  toFun := classify p q
  invFun := forgetKind p q
  left_inv := forget_classify p q
  right_inv := classify_forget p q

#print axioms mixed_of_not_unique
#print axioms interior_classify
#print axioms facePartition
end CMDG.CondensedCM5R0.EilenbergZilberPartition
