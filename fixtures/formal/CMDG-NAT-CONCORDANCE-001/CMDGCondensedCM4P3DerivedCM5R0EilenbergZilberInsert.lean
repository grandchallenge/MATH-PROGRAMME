import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberStraight

/-! The unique insertion cut of an omitted horizontal coordinate. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCorners
open CMDG.CondensedCM5R0.EilenbergZilberStraight
namespace CMDG.CondensedCM5R0.EilenbergZilberInsert

def cutPred {p q} (v : Path p q) (a : Fin (p+2)) (n : ℕ) : Prop :=
  n=p+q+1 ∨ ∃ j : Vertex p q, j.val=n ∧ a.val ≤ X v j

local instance {p q : ℕ} (v : Path p q) (a : Fin (p+2)) : DecidablePred (cutPred v a) := Classical.decPred _

def cut {p q} (v : Path p q) (a : Fin (p+2)) : ℕ :=
  Nat.find (show ∃ n, cutPred v a n from ⟨p+q+1,Or.inl rfl⟩)

theorem cut_spec {p q} (v : Path p q) (a : Fin (p+2)) :
    cutPred v a (cut v a) := Nat.find_spec _

theorem cut_le {p q} (v : Path p q) (a : Fin (p+2)) :
    cut v a ≤ p+q+1 := Nat.find_min' _ (Or.inl rfl)

theorem cut_before {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex p q) :
    j.val < cut v a ↔ X v j < a.val := by
  constructor
  · intro h
    by_contra! hh
    exact (Nat.not_le_of_lt h) (Nat.find_min' (show ∃ n, cutPred v a n from ⟨p+q+1,Or.inl rfl⟩) (Or.inr ⟨j,rfl,hh⟩))
  · intro h
    by_contra! hh
    rcases cut_spec v a with he | ⟨i,hi,ha⟩
    · have := j.isLt
      omega
    · exact (Nat.not_lt_of_ge (ha.trans (xmono v (by change i.val ≤ j.val; omega)))) h

theorem cut_lower {p q} (v : Path p q) (a : Fin (p+2)) :
    a.val ≤ cut v a := by
  rcases cut_spec v a with h | ⟨i,hi,ha⟩
  · have := a.isLt
    omega
  · have hr := rank v i
    omega

theorem cut_upper {p q} (v : Path p q) (a : Fin (p+2)) :
    cut v a ≤ a.val+q := by
  by_cases h : cut v a=0
  · omega
  · let j : Vertex p q := ⟨cut v a-1,by have := cut_le v a; omega⟩
    have hx := (cut_before v a j).mp (by change cut v a-1<cut v a; omega)
    have hr := rank v j
    have hy := ybound v j
    change X v j+Y v j=cut v a-1 at hr
    omega

def cutVertex {p q} (v : Path p q) (a : Fin (p+2)) : Vertex (p+1) q :=
  ⟨cut v a,by have := cut_le v a; omega⟩

def prevCut {p q} (v : Path p q) (a : Fin (p+2)) (h : 0<cut v a) : Vertex p q :=
  ⟨cut v a-1,by have := cut_le v a; omega⟩
def nextCut {p q} (v : Path p q) (a : Fin (p+2)) (h : cut v a<p+q+1) : Vertex p q :=
  ⟨cut v a,h⟩

theorem cross_x {p q} (v : Path p q) (a : Fin (p+2)) (h₀ : 0<cut v a)
    (h₁ : cut v a<p+q+1) :
    X v (prevCut v a h₀)+1=a.val ∧ X v (nextCut v a h₁)=a.val := by
  let i : Fin (p+q) := ⟨cut v a-1,by omega⟩
  have hp : i.castSucc=prevCut v a h₀ := rfl
  have hn : i.succ=nextCut v a h₁ := by
    apply Fin.ext
    change cut v a-1+1=cut v a
    omega
  have hs := step v i
  rw [hp,hn] at hs
  have hprev := (cut_before v a (prevCut v a h₀)).mp (by change cut v a-1<cut v a; omega)
  have hnext : a.val ≤ X v (nextCut v a h₁) := by
    by_contra! hn
    have hbad := (cut_before v a _).mpr hn
    exact (Nat.lt_irrefl _) hbad
  omega

theorem prevCut_y {p q} (v : Path p q) (a : Fin (p+2)) (h : 0<cut v a) :
    Y v (prevCut v a h) = cut v a-a.val := by
  have hx : X v (prevCut v a h)+1=a.val := by
    by_cases h₁ : cut v a<p+q+1
    · exact (cross_x v a h h₁).1
    · have hc : cut v a=p+q+1 := by have := cut_le v a; omega
      have hr := rank v (prevCut v a h)
      change X v (prevCut v a h)+Y v (prevCut v a h)=cut v a-1 at hr
      have hb := xbound v (prevCut v a h)
      have hy := ybound v (prevCut v a h)
      have hbefore := (cut_before v a (prevCut v a h)).mp (by change cut v a-1<cut v a; omega)
      have := a.isLt
      omega
  have hr := rank v (prevCut v a h)
  change X v (prevCut v a h)+Y v (prevCut v a h)=cut v a-1 at hr
  omega

theorem nextCut_y {p q} (v : Path p q) (a : Fin (p+2)) (h : cut v a<p+q+1) :
    Y v (nextCut v a h) = cut v a-a.val := by
  have hx : X v (nextCut v a h)=a.val := by
    by_cases h₀ : 0<cut v a
    · exact (cross_x v a h₀ h).2
    · have hr := rank v (nextCut v a h)
      change X v (nextCut v a h)+Y v (nextCut v a h)=cut v a at hr
      have := cut_lower v a
      omega
  have hr := rank v (nextCut v a h)
  change X v (nextCut v a h)+Y v (nextCut v a h)=cut v a at hr
  omega

def lowerIndex {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (hj : j≠cutVertex v a) : Vertex p q :=
  ⟨(drop (cutVertex v a) j hj).val,by have := (drop (cutVertex v a) j hj).isLt; omega⟩

theorem lowerIndex_lt {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (h : j<cutVertex v a) : (lowerIndex v a j (ne_of_lt h)).val=j.val :=
  drop_val_lt _ _ h

theorem lowerIndex_gt {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (h : cutVertex v a<j) : (lowerIndex v a j (ne_of_gt h)).val+1=j.val :=
  drop_val_gt _ _ h

def insertX {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q) : Fin (p+2) :=
  if h : j=cutVertex v a then a else a.succAbove (v.val.1 (lowerIndex v a j h))

def insertY {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q) : Fin (q+1) :=
  if h : j=cutVertex v a then ⟨cut v a-a.val,by have := cut_upper v a; omega⟩
  else v.val.2 (lowerIndex v a j h)

theorem insertX_before {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (h : j<cutVertex v a) : insertX v a j < a := by
  rw [insertX,dif_neg (ne_of_lt h)]
  apply (Fin.succAbove_lt_iff_castSucc_lt a _).mpr
  change X v (lowerIndex v a j (ne_of_lt h)) < a.val
  apply (cut_before v a _).mp
  rw [lowerIndex_lt v a j h]
  exact h

theorem insertX_after {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (h : cutVertex v a<j) : a < insertX v a j := by
  rw [insertX,dif_neg (ne_of_gt h)]
  apply (Fin.lt_succAbove_iff_le_castSucc a _).mpr
  change a.val ≤ X v (lowerIndex v a j (ne_of_gt h))
  by_contra! hn
  have he := (cut_before v a _).mpr hn
  have hj := lowerIndex_gt v a j h
  change cut v a<j.val at h
  omega

theorem insertY_before {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (h : j<cutVertex v a) : (insertY v a j).val ≤ cut v a-a.val := by
  rw [insertY,dif_neg (ne_of_lt h)]
  change Y v (lowerIndex v a j (ne_of_lt h)) ≤ _
  have hpos : 0<cut v a := by change j.val<cut v a at h; omega
  rw [← prevCut_y v a hpos]
  apply ymono v
  change (lowerIndex v a j (ne_of_lt h)).val ≤ cut v a-1
  rw [lowerIndex_lt v a j h]
  change j.val<cut v a at h
  omega

theorem insertY_after {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q)
    (h : cutVertex v a<j) : cut v a-a.val ≤ (insertY v a j).val := by
  rw [insertY,dif_neg (ne_of_gt h)]
  change _ ≤ Y v (lowerIndex v a j (ne_of_gt h))
  have hlt : cut v a<p+q+1 := by change cut v a<j.val at h; have := j.isLt; omega
  rw [← nextCut_y v a hlt]
  apply ymono v
  change cut v a ≤ (lowerIndex v a j (ne_of_gt h)).val
  have := lowerIndex_gt v a j h
  change cut v a<j.val at h
  omega

theorem lowerIndex_mono {p q} (v : Path p q) (a : Fin (p+2)) (i j : Vertex (p+1) q)
    (hi : i≠cutVertex v a) (hj : j≠cutVertex v a) (h : i≤j) :
    lowerIndex v a i hi ≤ lowerIndex v a j hj :=
  drop_mono _ _ _ hi hj h

theorem insertX_mono {p q} (v : Path p q) (a : Fin (p+2)) : Monotone (insertX v a) := by
  intro i j hij
  by_cases hi : i=cutVertex v a
  · subst i
    by_cases hj : j=cutVertex v a
    · subst j; rfl
    · rw [insertX,dif_pos rfl]
      exact le_of_lt (insertX_after v a j (lt_of_le_of_ne hij (Ne.symm hj)))
  · by_cases hj : j=cutVertex v a
    · subst j
      rw [show insertX v a (cutVertex v a)=a by rw [insertX,dif_pos rfl]]
      -- the new coordinate at the pivot is a
      exact le_of_lt (insertX_before v a i (lt_of_le_of_ne hij hi))
    · rw [insertX,dif_neg hi,insertX,dif_neg hj]
      exact (Fin.succAboveOrderEmb a).monotone (v.val.1.monotone (lowerIndex_mono v a i j hi hj hij))

theorem insertY_mono {p q} (v : Path p q) (a : Fin (p+2)) : Monotone (insertY v a) := by
  intro i j hij
  by_cases hi : i=cutVertex v a
  · subst i
    by_cases hj : j=cutVertex v a
    · subst j; rfl
    · rw [insertY,dif_pos rfl]
      exact insertY_after v a j (lt_of_le_of_ne hij (Ne.symm hj))
  · by_cases hj : j=cutVertex v a
    · subst j
      have he : insertY v a (cutVertex v a) = ⟨cut v a-a.val,by have := cut_upper v a; omega⟩ := by
        rw [insertY,dif_pos rfl]
      rw [he]
      exact insertY_before v a i (lt_of_le_of_ne hij hi)
    · rw [insertY,dif_neg hi,insertY,dif_neg hj]
      exact v.val.2.monotone (lowerIndex_mono v a i j hi hj hij)

theorem insert_rank {p q} (v : Path p q) (a : Fin (p+2)) (j : Vertex (p+1) q) :
    (insertX v a j).val+(insertY v a j).val=j.val := by
  by_cases hj : j=cutVertex v a
  · subst j
    rw [insertX,dif_pos rfl,insertY,dif_pos rfl]
    change a.val+(cut v a-a.val)=cut v a
    have := cut_lower v a
    omega
  · rw [insertX,dif_neg hj,insertY,dif_neg hj]
    rcases lt_or_gt_of_ne hj with h | h
    · have he := insertX_before v a j h
      rw [insertX,dif_neg hj] at he
      have hx := (Fin.succAbove_lt_iff_castSucc_lt a _).mp he
      rw [Fin.succAbove_of_castSucc_lt _ _ hx]
      exact (rank v (lowerIndex v a j hj)).trans (lowerIndex_lt v a j h)
    · have he := insertX_after v a j h
      rw [insertX,dif_neg hj] at he
      have hx := (Fin.lt_succAbove_iff_le_castSucc a _).mp he
      rw [Fin.succAbove_of_le_castSucc _ _ hx]
      have hr := rank v (lowerIndex v a j hj)
      have hl := lowerIndex_gt v a j h
      change X v (lowerIndex v a j hj)+1+Y v (lowerIndex v a j hj)=j.val
      omega

def upperPath {p q} (v : Path p q) (a : Fin (p+2)) : Path (p+1) q :=
  ⟨({toFun := insertX v a, monotone' := insertX_mono v a},
    {toFun := insertY v a, monotone' := insertY_mono v a}), insert_rank v a⟩

def upperHorizontal {p q} (v : Path p q) (a : Fin (p+2)) : HFace p q :=
  ⟨(upperPath v a,cutVertex v a),by
    intro j hj
    by_contra hn
    have he : (insertX v a j).val = a.val := by
      change (insertX v a j).val=(insertX v a (cutVertex v a)).val at hj
      have hv : insertX v a (cutVertex v a)=a := by rw [insertX,dif_pos rfl]
      rw [hv] at hj
      exact hj
    rw [insertX,dif_neg hn] at he
    exact Fin.succAbove_ne a _ (Fin.ext he)⟩

theorem cut_of_lower {p q} (z : HFace p q) :
    cut (lowerPath z) (lowerHorizontal z).2 = z.val.2.val := by
  let v := lowerPath z
  let a := (lowerHorizontal z).2
  let k := z.val.2
  have hpre (i : Vertex p q) : i.val < cut v a ↔ i.val < k.val := by
    rw [cut_before]
    change ((lowerPath z).val.1 i).val < a.val ↔ _
    change ((lowerPath z).val.1 i).castSucc < a ↔ _
    rw [← Fin.succAbove_lt_iff_castSucc_lt]
    change (lowerHorizontal z).2.succAbove ((lowerHorizontal z).1.val.1 i) < (lowerHorizontal z).2 ↔ _
    rw [lower_x]
    change X z.val.1 (oldVertex z i) < X z.val.1 k ↔ _
    rw [beforeX z.val.1 k z.property,oldVertex,Fin.succAbove_lt_iff_castSucc_lt]
    rfl
  have h₁ := cut_le v a
  have h₂ := k.isLt
  change k.val<p+1+q+1 at h₂
  change cut v a = k.val
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · let i : Vertex p q := ⟨cut v a,by omega⟩
    have he := (hpre i).mpr h
    exact (Nat.lt_irrefl _) he
  · let i : Vertex p q := ⟨k.val,by omega⟩
    have he := (hpre i).mp h
    exact (Nat.lt_irrefl _) he

theorem lowerIndex_old {p q} (v : Path p q) (a : Fin (p+2)) (i : Vertex p q) :
    lowerIndex v a (oldVertex (upperHorizontal v a) i) (Fin.succAbove_ne _ _) = i := by
  apply Fin.ext
  change (drop (cutVertex v a) ((cutVertex v a).succAbove (oldIndex i)) _).val = i.val
  rw [drop_succAbove]
  rfl

theorem lower_upper {p q} (v : Path p q) (a : Fin (p+2)) :
    lowerHorizontal (upperHorizontal v a) = (v,a) := by
  have ha : (lowerHorizontal (upperHorizontal v a)).2 = a := by
    change insertX v a (cutVertex v a)=a
    rw [insertX,dif_pos rfl]
  apply Prod.ext
  · apply Subtype.ext
    apply Prod.ext
    · apply OrderHom.ext
      funext i
      apply Fin.succAbove_right_injective (p:=a)
      have he := lower_x (upperHorizontal v a) i
      rw [ha] at he
      rw [he]
      change insertX v a (oldVertex (upperHorizontal v a) i) = _
      have hn : oldVertex (upperHorizontal v a) i ≠ cutVertex v a := Fin.succAbove_ne _ _
      rw [insertX,dif_neg hn,lowerIndex_old]
    · apply OrderHom.ext
      funext i
      change removeY (upperHorizontal v a) i = _
      change insertY v a (oldVertex (upperHorizontal v a) i) = _
      have hn : oldVertex (upperHorizontal v a) i ≠ cutVertex v a := Fin.succAbove_ne _ _
      rw [insertY,dif_neg hn,lowerIndex_old]
  · exact ha

theorem cutVertex_of_lower {p q} (z : HFace p q) :
    cutVertex (lowerPath z) (lowerHorizontal z).2 = z.val.2 :=
  Fin.ext (cut_of_lower z)

theorem old_lowerIndex {p q} (z : HFace p q) (j : Vertex (p+1) q)
    (h : j≠cutVertex (lowerPath z) (lowerHorizontal z).2) :
    oldVertex z (lowerIndex (lowerPath z) (lowerHorizontal z).2 j h) = j := by
  have he := drop_spec (cutVertex (lowerPath z) (lowerHorizontal z).2) j h
  have hi : oldIndex (lowerIndex (lowerPath z) (lowerHorizontal z).2 j h) =
      drop (cutVertex (lowerPath z) (lowerHorizontal z).2) j h := rfl
  unfold oldVertex
  rw [hi,← cutVertex_of_lower z]
  exact he

theorem upper_lower {p q} (z : HFace p q) :
    upperHorizontal (lowerHorizontal z).1 (lowerHorizontal z).2 = z := by
  let v := lowerPath z
  let a := (lowerHorizontal z).2
  let k := cutVertex v a
  have hk : k=z.val.2 := cutVertex_of_lower z
  apply Subtype.ext
  apply Prod.ext
  · apply Subtype.ext
    apply Prod.ext
    · apply OrderHom.ext
      funext j
      change insertX v a j = z.val.1.val.1 j
      by_cases h : j=k
      · subst j
        rw [insertX,dif_pos rfl]
        change z.val.1.val.1 z.val.2=z.val.1.val.1 k
        rw [hk]
      · rw [insertX,dif_neg h]
        have he := lower_x z (lowerIndex v a j h)
        change a.succAbove (v.val.1 (lowerIndex v a j h)) = _ at he
        rw [he,old_lowerIndex]
    · apply OrderHom.ext
      funext j
      change insertY v a j = z.val.1.val.2 j
      by_cases h : j=k
      · subst j
        rw [insertY,dif_pos rfl]
        apply Fin.ext
        change cut v a-a.val=Y z.val.1 k
        have hr := rank z.val.1 z.val.2
        rw [hk]
        have hc := cut_of_lower z
        change cut v a=z.val.2.val at hc
        change a.val+Y z.val.1 z.val.2=z.val.2.val at hr
        omega
      · rw [insertY,dif_neg h]
        have he := lower_y z (lowerIndex v a j h)
        change v.val.2 (lowerIndex v a j h) = _ at he
        rw [he,old_lowerIndex]
  · exact hk

/-- Straight/endpoint horizontal deletion and insertion are inverse,
including both endpoints. -/
def horizontalEquiv (p q : ℕ) : HFace p q ≃ Path p q × Fin (p+2) where
  toFun := lowerHorizontal
  invFun z := upperHorizontal z.1 z.2
  left_inv := upper_lower
  right_inv z := lower_upper z.1 z.2

#print axioms cut_before
#print axioms prevCut_y
#print axioms nextCut_y
#print axioms upperHorizontal
#print axioms horizontalEquiv
end CMDG.CondensedCM5R0.EilenbergZilberInsert
