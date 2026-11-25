import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberInsert

/-! Inversion accounting for straight horizontal deletion. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCorners
open CMDG.CondensedCM5R0.EilenbergZilberStraight
open CMDG.CondensedCM5R0.EilenbergZilberInsert
namespace CMDG.CondensedCM5R0.EilenbergZilberStraightSign

def pivotEdge {p q} (v : Path p q) (a : Fin (p+2)) : Fin (p+1+q) :=
  ⟨min (cut v a) (p+q),by omega⟩

def liftEdge {p q} (v : Path p q) (a : Fin (p+2)) (i : Fin (p+q)) :
    Fin (p+1+q) :=
  ⟨if i.val<cut v a then i.val else i.val+1,by have := i.isLt; split_ifs <;> omega⟩

theorem liftEdge_ne {p q} (v : Path p q) (a : Fin (p+2)) (i : Fin (p+q)) :
    liftEdge v a i ≠ pivotEdge v a := by
  intro h
  have he := congrArg Fin.val h
  change (if i.val<cut v a then i.val else i.val+1) = min (cut v a) (p+q) at he
  have := i.isLt
  split_ifs at he <;> omega

theorem liftEdge_inj {p q} (v : Path p q) (a : Fin (p+2)) :
    Function.Injective (liftEdge v a) := by
  intro i j h
  have he := congrArg Fin.val h
  change (if i.val<cut v a then i.val else i.val+1) =
    (if j.val<cut v a then j.val else j.val+1) at he
  apply Fin.ext
  split_ifs at he <;> omega

theorem liftEdge_surj {p q} (v : Path p q) (a : Fin (p+2)) (j : Fin (p+1+q))
    (hj : j ≠ pivotEdge v a) : ∃ i : Fin (p+q), liftEdge v a i = j := by
  have hn : j.val ≠ min (cut v a) (p+q) := fun h => hj (Fin.ext h)
  have hb := j.isLt
  by_cases h : j.val<cut v a
  · have hl : j.val<p+q := by omega
    refine ⟨⟨j.val,hl⟩,Fin.ext ?_⟩
    change (if j.val<cut v a then j.val else j.val+1)=j.val
    rw [if_pos h]
  · have hl : j.val-1<p+q := by omega
    have hg : cut v a≤j.val-1 := by omega
    refine ⟨⟨j.val-1,hl⟩,Fin.ext ?_⟩
    change (if j.val-1<cut v a then j.val-1 else j.val-1+1)=j.val
    rw [if_neg (by omega)]
    omega

theorem oldVertex_val {p q} (v : Path p q) (a : Fin (p+2)) (i : Vertex p q) :
    (oldVertex (upperHorizontal v a) i).val =
      if i.val<cut v a then i.val else i.val+1 := by
  change ((cutVertex v a).succAbove (oldIndex i)).val = _
  by_cases h : i.val<cut v a
  · rw [Fin.succAbove_of_castSucc_lt _ _ (show (oldIndex i).castSucc < cutVertex v a from h),if_pos h]
    rfl
  · rw [Fin.succAbove_of_le_castSucc _ _ (show cutVertex v a ≤ (oldIndex i).castSucc from Nat.le_of_not_gt h),if_neg h]
    rfl

theorem upperX_old {p q} (v : Path p q) (a : Fin (p+2)) (i : Vertex p q) :
    (upperPath v a).val.1 (oldVertex (upperHorizontal v a) i) = a.succAbove (v.val.1 i) := by
  change insertX v a (oldVertex (upperHorizontal v a) i) = _
  have hn : oldVertex (upperHorizontal v a) i ≠ cutVertex v a := Fin.succAbove_ne _ _
  rw [insertX,dif_neg hn,lowerIndex_old]

theorem upperY_old {p q} (v : Path p q) (a : Fin (p+2)) (i : Vertex p q) :
    Y (upperPath v a) (oldVertex (upperHorizontal v a) i) = Y v i := by
  change (insertY v a (oldVertex (upperHorizontal v a) i)).val = _
  have hn : oldVertex (upperHorizontal v a) i ≠ cutVertex v a := Fin.succAbove_ne _ _
  rw [insertY,dif_neg hn,lowerIndex_old]
  rfl

theorem upperX_pivot {p q} (v : Path p q) (a : Fin (p+2)) :
    (upperPath v a).val.1 (cutVertex v a) = a := by
  change insertX v a (cutVertex v a)=a
  rw [insertX,dif_pos rfl]

theorem upperY_pivot {p q} (v : Path p q) (a : Fin (p+2)) :
    Y (upperPath v a) (cutVertex v a) = cut v a-a.val := by
  change (insertY v a (cutVertex v a)).val=_
  rw [insertY,dif_pos rfl]

theorem lift_cast {p q} (v : Path p q) (a : Fin (p+2)) (i : Fin (p+q)) :
    (liftEdge v a i).castSucc=oldVertex (upperHorizontal v a) i.castSucc := by
  apply Fin.ext
  rw [oldVertex_val]
  rfl

theorem lift_succ {p q} (v : Path p q) (a : Fin (p+2)) (i : Fin (p+q))
    (h : i.val+1≠cut v a) :
    (liftEdge v a i).succ=oldVertex (upperHorizontal v a) i.succ := by
  apply Fin.ext
  rw [oldVertex_val]
  change (if i.val<cut v a then i.val else i.val+1)+1 =
    if i.val+1<cut v a then i.val+1 else i.val+1+1
  split_ifs <;> omega

theorem lift_succ_cross {p q} (v : Path p q) (a : Fin (p+2)) (i : Fin (p+q))
    (h : i.val+1=cut v a) :
    (liftEdge v a i).succ=cutVertex v a := by
  apply Fin.ext
  change (if i.val<cut v a then i.val else i.val+1)+1=cut v a
  rw [if_pos (by omega)]
  exact h

theorem lift_weight {p q} (v : Path p q) (a : Fin (p+2)) (i : Fin (p+q)) :
    weight (upperPath v a) (liftEdge v a i) = weight v i := by
  rw [weight,weight,lift_cast,upperY_old]
  by_cases h : i.val+1=cut v a
  · rw [lift_succ_cross v a i h]
    have hlt : oldVertex (upperHorizontal v a) i.castSucc < cutVertex v a := by
      change (oldVertex (upperHorizontal v a) i.castSucc).val < cut v a
      rw [oldVertex_val]
      change (if i.val<cut v a then i.val else i.val+1)<cut v a
      rw [if_pos (by omega)]
      omega
    have hu := insertX_before v a _ hlt
    have h₀ : 0<cut v a := by omega
    have h₁ : cut v a<p+q+1 := by have := i.isLt; omega
    have hp : i.castSucc=prevCut v a h₀ := by apply Fin.ext; change i.val=cut v a-1; omega
    have hn : i.succ=nextCut v a h₁ := Fin.ext h
    have hx := cross_x v a h₀ h₁
    rw [← hp,← hn] at hx
    have hux : X (upperPath v a) (oldVertex (upperHorizontal v a) i.castSucc) <
        X (upperPath v a) (cutVertex v a) := by
      change (insertX v a _).val < (insertX v a (cutVertex v a)).val
      have he : insertX v a (cutVertex v a)=a := upperX_pivot v a
      rw [he]
      exact hu
    rw [if_pos hux,if_pos (by omega)]
  · rw [lift_succ v a i h]
    have hx : X (upperPath v a) (oldVertex (upperHorizontal v a) i.castSucc) <
        X (upperPath v a) (oldVertex (upperHorizontal v a) i.succ) ↔ X v i.castSucc < X v i.succ := by
      change (upperPath v a).val.1 _ < (upperPath v a).val.1 _ ↔ v.val.1 _ < v.val.1 _
      rw [upperX_old,upperX_old]
      exact (Fin.succAboveOrderEmb a).lt_iff_lt
    by_cases hh : X v i.castSucc < X v i.succ
    · rw [if_pos hh,if_pos (hx.mpr hh)]
    · rw [if_neg hh,if_neg (fun h => hh (hx.mp h))]

theorem pivot_weight {p q} (v : Path p q) (a : Fin (p+2)) :
    weight (upperPath v a) (pivotEdge v a) = cut v a-a.val := by
  unfold weight
  by_cases h : cut v a≤p+q
  · have hp : (pivotEdge v a).castSucc=cutVertex v a := by
      apply Fin.ext
      exact min_eq_left h
    rw [hp,upperY_pivot]
    have hl : cutVertex v a < (pivotEdge v a).succ := by
      rw [← hp]
      exact Nat.lt_succ_self _
    have hx := (afterX (upperPath v a) (cutVertex v a) (upperHorizontal v a).property _).mpr hl
    rw [if_pos hx]
  · have hc : cut v a=p+q+1 := by have := cut_le v a; omega
    have hs : (pivotEdge v a).succ=cutVertex v a := by
      apply Fin.ext
      change min (cut v a) (p+q)+1=cut v a
      omega
    have hl : (pivotEdge v a).castSucc < cutVertex v a := by
      rw [← hs]
      exact Nat.lt_succ_self _
    have hx := (beforeX (upperPath v a) (cutVertex v a) (upperHorizontal v a).property _).mpr hl
    rw [hs,if_pos hx]
    have hpos : 0<cut v a := by omega
    have hp : (pivotEdge v a).castSucc=oldVertex (upperHorizontal v a) (prevCut v a hpos) := by
      apply Fin.ext
      rw [oldVertex_val]
      change min (cut v a) (p+q) = if cut v a-1<cut v a then cut v a-1 else cut v a-1+1
      rw [if_pos (by omega)]
      omega
    rw [hp,upperY_old,prevCut_y]

theorem exponent_insert {p q} (v : Path p q) (a : Fin (p+2)) :
    exponent (upperPath v a) = exponent v + (cut v a-a.val) := by
  classical
  unfold exponent
  rw [← Finset.sum_erase_add _ _ (Finset.mem_univ (pivotEdge v a)),pivot_weight]
  congr 1
  symm
  apply Finset.sum_bij (fun i _ => liftEdge v a i)
  · intro i _
    exact Finset.mem_erase.mpr ⟨liftEdge_ne v a i,Finset.mem_univ _⟩
  · intro i _ j _ h
    exact liftEdge_inj v a h
  · intro j hj
    obtain ⟨i,hi⟩ := liftEdge_surj v a j (Finset.mem_erase.mp hj).1
    exact ⟨i,Finset.mem_univ _,hi⟩
  · intro i _
    exact (lift_weight v a i).symm

theorem exponent_remove {p q} (z : HFace p q) :
    exponent z.val.1 = exponent (lowerPath z) + Y z.val.1 z.val.2 := by
  let v := lowerPath z
  let a := (lowerHorizontal z).2
  have he := exponent_insert v a
  have hpath : upperPath v a = z.val.1 := congrArg (fun t : HFace p q => t.val.1) (upper_lower z)
  rw [hpath] at he
  have hk := cut_of_lower z
  change cut v a = z.val.2.val at hk
  have hr := rank z.val.1 z.val.2
  change a.val+Y z.val.1 z.val.2=z.val.2.val at hr
  change exponent z.val.1 = exponent v+Y z.val.1 z.val.2
  omega

theorem horizontal_sign {p q} (z : HFace p q) :
    (-1 : ℤ)^z.val.2.val * pathSign z.val.1 =
      (-1 : ℤ)^(lowerHorizontal z).2.val * pathSign (lowerPath z) := by
  rw [sign_exponent,sign_exponent,exponent_remove]
  have hr := rank z.val.1 z.val.2
  change (lowerHorizontal z).2.val + Y z.val.1 z.val.2 = z.val.2.val at hr
  rw [← hr,pow_add,pow_add]
  have hs : (-1 : ℤ)^Y z.val.1 z.val.2 * (-1 : ℤ)^Y z.val.1 z.val.2 = 1 := by
    rw [← pow_two,← pow_mul,mul_comm,pow_mul]
    norm_num
  calc
    _ = (-1 : ℤ)^(lowerHorizontal z).2.val * (-1 : ℤ)^exponent (lowerPath z) *
          ((-1 : ℤ)^Y z.val.1 z.val.2 * (-1 : ℤ)^Y z.val.1 z.val.2) := by ring
    _ = _ := by rw [hs,mul_one]

#print axioms liftEdge_surj
#print axioms lift_weight
#print axioms horizontal_sign
end CMDG.CondensedCM5R0.EilenbergZilberStraightSign
