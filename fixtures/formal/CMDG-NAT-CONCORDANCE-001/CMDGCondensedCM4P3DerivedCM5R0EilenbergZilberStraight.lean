import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberCorners

/-! Straight horizontal faces: deletion of a vertex whose horizontal
coordinate occurs exactly once, with the precise lower-dimensional path. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCorners
namespace CMDG.CondensedCM5R0.EilenbergZilberStraight

def UniqueX {p q} (u : Path p q) (k : Vertex p q) : Prop :=
  ∀ j, X u j = X u k → j=k
def UniqueY {p q} (u : Path p q) (k : Vertex p q) : Prop :=
  ∀ j, Y u j = Y u k → j=k

theorem beforeX {p q} (u : Path p q) (k : Vertex p q) (h : UniqueX u k)
    (j : Vertex p q) : X u j < X u k ↔ j<k := by
  constructor
  · intro hj
    by_contra! hn
    exact (Nat.not_lt_of_ge (xmono u hn)) hj
  · intro hj
    exact lt_of_le_of_ne (xmono u (le_of_lt hj)) (fun he => (ne_of_lt hj) (h j he))

theorem afterX {p q} (u : Path p q) (k : Vertex p q) (h : UniqueX u k)
    (j : Vertex p q) : X u k < X u j ↔ k<j := by
  constructor
  · intro hj
    by_contra! hn
    exact (Nat.not_lt_of_ge (xmono u hn)) hj
  · intro hj
    exact lt_of_le_of_ne (xmono u (le_of_lt hj)) (fun he => (ne_of_gt hj) (h j he.symm))

def drop {n : ℕ} (a x : Fin (n+1)) (h : x≠a) : Fin n :=
  Classical.choose (Fin.exists_succAbove_eq h)

theorem drop_spec {n} (a x : Fin (n+1)) (h : x≠a) :
    a.succAbove (drop a x h) = x := Classical.choose_spec (Fin.exists_succAbove_eq h)

theorem drop_succAbove {n} (a : Fin (n+1)) (i : Fin n) :
    drop a (a.succAbove i) (Fin.succAbove_ne _ _) = i := by
  apply Fin.succAbove_right_injective (p:=a)
  exact drop_spec _ _ _

theorem drop_mono {n} (a x y : Fin (n+1)) (hx : x≠a) (hy : y≠a) (h : x≤y) :
    drop a x hx ≤ drop a y hy := by
  apply (Fin.succAboveOrderEmb a).le_iff_le.mp
  change a.succAbove (drop a x hx) ≤ a.succAbove (drop a y hy)
  rw [drop_spec,drop_spec]
  exact h

theorem drop_val_lt {n} (a x : Fin (n+1)) (h : x<a) :
    (drop a x (ne_of_lt h)).val = x.val := by
  have he := drop_spec a x (ne_of_lt h)
  have hlt : (drop a x (ne_of_lt h)).castSucc < a := by
    apply (Fin.succAbove_lt_iff_castSucc_lt a _).mp
    rw [he]; exact h
  rw [Fin.succAbove_of_castSucc_lt _ _ hlt] at he
  exact congrArg Fin.val he

theorem drop_val_gt {n} (a x : Fin (n+1)) (h : a<x) :
    (drop a x (ne_of_gt h)).val+1 = x.val := by
  have he := drop_spec a x (ne_of_gt h)
  have hlt : a ≤ (drop a x (ne_of_gt h)).castSucc := by
    apply (Fin.lt_succAbove_iff_le_castSucc a _).mp
    rw [he]; exact h
  rw [Fin.succAbove_of_le_castSucc _ _ hlt] at he
  exact congrArg Fin.val he

abbrev HFace (p q : ℕ) := {z : Path (p+1) q × Vertex (p+1) q // UniqueX z.1 z.2}

def oldIndex {p q} (i : Vertex p q) : Fin (p+1+q) :=
  ⟨i.val,by have := i.isLt; omega⟩

def oldVertex {p q} (z : HFace p q) (i : Vertex p q) : Vertex (p+1) q :=
  z.val.2.succAbove (oldIndex i)

theorem removed_ne {p q} (z : HFace p q) (i : Vertex p q) :
    z.val.1.val.1 (oldVertex z i) ≠ z.val.1.val.1 z.val.2 := by
  intro h
  exact Fin.succAbove_ne _ _ (z.property _ (congrArg Fin.val h))

def removeX {p q} (z : HFace p q) (i : Vertex p q) : Fin (p+1) :=
  drop (z.val.1.val.1 z.val.2) (z.val.1.val.1 (oldVertex z i)) (removed_ne z i)
def removeY {p q} (z : HFace p q) (i : Vertex p q) : Fin (q+1) :=
  z.val.1.val.2 (oldVertex z i)

theorem oldVertex_mono {p q} (z : HFace p q) : Monotone (oldVertex z) :=
  fun _ _ h => (Fin.succAboveOrderEmb z.val.2).monotone (show oldIndex _ ≤ oldIndex _ from h)

theorem remove_rank {p q} (z : HFace p q) (i : Vertex p q) :
    (removeX z i).val + (removeY z i).val = i.val := by
  let k := z.val.2
  let a := z.val.1.val.1 k
  let j := oldVertex z i
  have hr := rank z.val.1 j
  have hn : j≠k := Fin.succAbove_ne _ _
  rcases lt_or_gt_of_ne hn with h | h
  · have ha : z.val.1.val.1 j < a := (beforeX z.val.1 k z.property j).mpr h
    have hd := drop_val_lt a (z.val.1.val.1 j) ha
    have hk := (Fin.succAbove_lt_iff_castSucc_lt k (oldIndex i)).mp h
    have hj : j.val=i.val := congrArg Fin.val (Fin.succAbove_of_castSucc_lt k _ hk)
    change (removeX z i).val = X z.val.1 j at hd
    change (removeX z i).val + Y z.val.1 j = i.val
    omega
  · have ha : a < z.val.1.val.1 j := (afterX z.val.1 k z.property j).mpr h
    have hd := drop_val_gt a (z.val.1.val.1 j) ha
    have hk := (Fin.lt_succAbove_iff_le_castSucc k (oldIndex i)).mp h
    have hj : j.val=i.val+1 := congrArg Fin.val (Fin.succAbove_of_le_castSucc k _ hk)
    change (removeX z i).val+1 = X z.val.1 j at hd
    change (removeX z i).val + Y z.val.1 j = i.val
    omega

def lowerPath {p q} (z : HFace p q) : Path p q :=
  ⟨({toFun := removeX z, monotone' := fun _i _j h =>
      drop_mono _ _ _ _ _ (z.val.1.val.1.monotone (oldVertex_mono z h))},
    {toFun := removeY z, monotone' := fun _i _j h =>
      z.val.1.val.2.monotone (oldVertex_mono z h)}), remove_rank z⟩

def lowerHorizontal {p q} (z : HFace p q) : Path p q × Fin (p+2) :=
  (lowerPath z,z.val.1.val.1 z.val.2)

theorem lower_x {p q} (z : HFace p q) (i : Vertex p q) :
    (lowerHorizontal z).2.succAbove ((lowerHorizontal z).1.val.1 i) =
      z.val.1.val.1 (oldVertex z i)  := drop_spec _ _ (removed_ne z i)
theorem lower_y {p q} (z : HFace p q) (i : Vertex p q) :
    (lowerHorizontal z).1.val.2 i = z.val.1.val.2 (oldVertex z i) := rfl

#print axioms lowerPath
#print axioms lower_x
#print axioms lower_y
end CMDG.CondensedCM5R0.EilenbergZilberStraight
