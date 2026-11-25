import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberStraightSign

/-! Transposition of the original paths complements the inversion count. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCorners
open CMDG.CondensedCM5R0.EilenbergZilberStraight
open CMDG.CondensedCM5R0.EilenbergZilberInsert
open CMDG.CondensedCM5R0.EilenbergZilberStraightSign
namespace CMDG.CondensedCM5R0.EilenbergZilberTranspose

def flipVertex {p q : ℕ} (i : Vertex p q) : Vertex q p :=
  ⟨i.val,by have := i.isLt; omega⟩
def flipEdge {p q : ℕ} (i : Fin (p+q)) : Fin (q+p) :=
  ⟨i.val,by have := i.isLt; omega⟩

theorem flipVertex_flip {p q} (i : Vertex p q) : flipVertex (flipVertex i)=i := rfl
theorem flipEdge_flip {p q} (i : Fin (p+q)) : flipEdge (flipEdge i)=i := rfl

def transpose {p q} (u : Path p q) : Path q p :=
  ⟨({toFun := fun i => u.val.2 (flipVertex i), monotone' := fun _ _ h => u.val.2.monotone h},
    {toFun := fun i => u.val.1 (flipVertex i), monotone' := fun _ _ h => u.val.1.monotone h}),by
      intro i
      have h := rank u (flipVertex i)
      change Y u (flipVertex i)+X u (flipVertex i)=i.val
      exact (Nat.add_comm _ _).trans h⟩

theorem transpose_x {p q} (u : Path p q) (i : Vertex p q) :
    X (transpose u) (flipVertex i)=Y u i := rfl
theorem transpose_y {p q} (u : Path p q) (i : Vertex p q) :
    Y (transpose u) (flipVertex i)=X u i := rfl

theorem transpose_involution {p q} (u : Path p q) : transpose (transpose u)=u := by
  apply Subtype.ext
  apply Prod.ext <;> apply OrderHom.ext <;> funext i <;> rfl

theorem transpose_uniqueX {p q} (u : Path p q) (k : Vertex p q) :
    UniqueX (transpose u) (flipVertex k) ↔ UniqueY u k := by
  constructor
  · intro h j hj
    have he := h (flipVertex j) hj
    exact Fin.ext (congrArg (fun i : Vertex q p => i.val) he)
  · intro h j hj
    have he := h (flipVertex j) hj
    exact Fin.ext (congrArg (fun i : Vertex p q => i.val) he)

def area {p q} (u : Path p q) (i : Vertex p q) : ℕ := X u i * Y u i

theorem area_step {p q} (u : Path p q) (i : Fin (p+q)) :
    area u i.succ = area u i.castSucc + (weight u i + weight (transpose u) (flipEdge i)) := by
  have hs := step u i
  unfold area weight
  change X u i.succ * Y u i.succ = X u i.castSucc * Y u i.castSucc +
    ((if X u i.castSucc < X u i.succ then Y u i.castSucc else 0) +
     (if Y u i.castSucc < Y u i.succ then X u i.castSucc else 0))
  rcases hs with ⟨hx,hy⟩ | ⟨hx,hy⟩
  · rw [hx,hy,if_pos (by omega),if_neg (by omega)]
    ring
  · rw [hx,hy,if_neg (by omega),if_pos (by omega)]
    ring

theorem area_zero {p q} (u : Path p q) : area u 0=0 := by
  have h := rank u 0
  change X u 0 + Y u 0=0 at h
  have hx : X u 0=0 := by omega
  simp [area,hx]

theorem area_last {p q} (u : Path p q) : area u (Fin.last (p+q))=p*q := by
  have h := rank u (Fin.last (p+q))
  have hx := xbound u (Fin.last (p+q))
  have hy := ybound u (Fin.last (p+q))
  change X u (Fin.last (p+q))+Y u (Fin.last (p+q))=p+q at h
  have hx' : X u (Fin.last (p+q))=p := by omega
  have hy' : Y u (Fin.last (p+q))=q := by omega
  simp [area,hx',hy']

theorem sum_flip {p q} (u : Path p q) :
    (∑ i : Fin (p+q), weight (transpose u) (flipEdge i)) = exponent (transpose u) := by
  unfold exponent
  apply Finset.sum_bij (fun i _ => flipEdge i)
  · simp
  · intro i _ j _ h
    exact Fin.ext (congrArg (fun i : Fin (q+p) => i.val) h)
  · intro j _
    exact ⟨flipEdge j,by simp,flipEdge_flip j⟩
  · intros
    rfl

theorem exponent_complement {p q} (u : Path p q) :
    exponent u + exponent (transpose u)=p*q := by
  -- use two expansions without rewriting the shorter sum
  have h : (∑ i : Fin (p+q+1), area u i) =
    (∑ i : Fin (p+q), area u i.castSucc) + area u (Fin.last (p+q)) :=
    Fin.sum_univ_castSucc _
  have h' : (∑ i : Fin (p+q+1), area u i) =
    area u 0 + ∑ i : Fin (p+q), area u i.succ := Fin.sum_univ_succ _
  rw [area_zero,zero_add] at h'
  have ht : (∑ i : Fin (p+q), area u i.succ) =
    (∑ i : Fin (p+q), area u i.castSucc) + (exponent u+exponent (transpose u)) := by
    simp only [area_step,Finset.sum_add_distrib,exponent,sum_flip]
  rw [ht] at h'
  rw [area_last] at h
  omega

abbrev VFace (p q : ℕ) := {z : Path p (q+1) × Vertex p (q+1) // UniqueY z.1 z.2}

def flipH {p q} (z : VFace p q) : HFace q p :=
  ⟨(transpose z.val.1,flipVertex z.val.2),(transpose_uniqueX _ _).mpr z.property⟩

def flipV {p q} (z : HFace q p) : VFace p q :=
  ⟨(transpose z.val.1,flipVertex z.val.2),by
    apply (transpose_uniqueX _ _).mp
    rw [transpose_involution,flipVertex_flip]
    exact z.property⟩

def flipFaceEquiv (p q : ℕ) : VFace p q ≃ HFace q p where
  toFun := flipH
  invFun := flipV
  left_inv z := by apply Subtype.ext; apply Prod.ext; exact transpose_involution _; rfl
  right_inv z := by apply Subtype.ext; apply Prod.ext; exact transpose_involution _; rfl

def lowerVertical {p q} (z : VFace p q) : Path p q × Fin (q+2) :=
  (transpose (lowerPath (flipH z)),(lowerHorizontal (flipH z)).2)

def transposeEquiv (p q : ℕ) : Path p q ≃ Path q p where
  toFun := transpose
  invFun := transpose
  left_inv := transpose_involution
  right_inv := transpose_involution

def verticalEquiv (p q : ℕ) : VFace p q ≃ Path p q × Fin (q+2) :=
  (flipFaceEquiv p q).trans ((horizontalEquiv q p).trans
    (Equiv.prodCongr (transposeEquiv q p) (Equiv.refl _)))

theorem vertical_sign {p q} (z : VFace p q) :
    (-1 : ℤ)^z.val.2.val * pathSign z.val.1 =
      (-1 : ℤ)^(p+(lowerVertical z).2.val) * pathSign (lowerVertical z).1 := by
  let t := flipH z
  have h₁ := exponent_complement z.val.1
  have h₂ := exponent_complement (lowerPath t)
  have h₃ := exponent_remove t
  change exponent (transpose z.val.1) =
    exponent (lowerPath t) + X z.val.1 z.val.2 at h₃
  have h₄ := rank z.val.1 z.val.2
  change X z.val.1 z.val.2 + (lowerVertical z).2.val=z.val.2.val at h₄
  rw [Nat.mul_succ] at h₁
  rw [Nat.mul_comm q p] at h₂
  rw [sign_exponent,sign_exponent,← pow_add,← pow_add]
  change (-1 : ℤ)^(z.val.2.val+exponent z.val.1) =
    (-1 : ℤ)^(p+(lowerVertical z).2.val+exponent (transpose (lowerPath t)))
  congr 1
  omega

#print axioms transpose_involution
#print axioms exponent_complement
#print axioms verticalEquiv
#print axioms vertical_sign
end CMDG.CondensedCM5R0.EilenbergZilberTranspose
