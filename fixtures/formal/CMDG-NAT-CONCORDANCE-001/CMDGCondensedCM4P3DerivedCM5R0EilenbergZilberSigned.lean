import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberBoundarySum

/-! Evaluate the complete signed ordinal-path boundary identity on the
actual alternating diagonal and total complexes. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.EilenbergZilberAxes
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.EilenbergZilberCorners
open CMDG.CondensedCM5R0.EilenbergZilberBoundarySum
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberHomotopy
open CMDG.CondensedCM5R0.EilenbergZilberShuffle
open CMDG.CondensedCM5R0.EilenbergZilberTotalSide
open CMDG.CondensedCM5R0.EilenbergZilberZero
namespace CMDG.CondensedCM5R0.EilenbergZilberSigned

def indexAt {p q n : ℕ} (h : p+q=n) (i : Fin (n+1)) : Vertex p q :=
  ⟨i.val,by have := i.isLt; omega⟩

def deletedIndex {p q n : ℕ} (h : p+q=n+1) (i : Fin (n+1)) : Fin (p+q) :=
  ⟨i.val,by have := i.isLt; omega⟩

def pathAt {p q : ℕ} (B : Bi) (u : Path p q) (n : ℕ) (h : p+q=n) :
    B.obj (d p,d q) ⟶ (diagChains B).X n :=
  B.map ((SimplexCategory.mkHom
    {toFun := fun i => u.val.1 (indexAt h i), monotone' := fun _ _ h => u.val.1.monotone h}).op ×ₘ
    (SimplexCategory.mkHom
    {toFun := fun i => u.val.2 (indexAt h i), monotone' := fun _ _ h => u.val.2.monotone h}).op)

def evalDeleted (B : Bi) (p q n : ℕ) (h : p+q=n+1) (t : Deleted p q) :
    B.obj (d p,d q) ⟶ (diagChains B).X n :=
  B.map ((SimplexCategory.mkHom
    {toFun := fun i => t.1 (deletedIndex h i), monotone' := fun _ _ h => t.1.monotone h}).op ×ₘ
    (SimplexCategory.mkHom
    {toFun := fun i => t.2 (deletedIndex h i), monotone' := fun _ _ h => t.2.monotone h}).op)

set_option backward.isDefEq.respectTransparency false in
theorem shuffleAt_sum (B : Bi) (p q n : ℕ) (h : p+q=n) :
    (double B).ιTotal c p q n h ≫ shuffleDegree B n =
      ∑ u : Path p q, pathSign u • pathAt B u n h := by
  subst n
  rw [shuffleDegree_summand]
  rfl

theorem index_face {p q n} (h : p+q=n+1) (i : Fin (n+2)) (j : Fin (n+1)) :
    indexAt h (i.succAbove j) = (indexAt h i).succAbove (deletedIndex h j) := by
  apply Fin.ext
  change (i.succAbove j).val = ((indexAt h i).succAbove (deletedIndex h j)).val
  rw [succAbove_val,succAbove_val]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem diag_eval (B : Bi) {p q n : ℕ} (h : p+q=n+1) (u : Path p q) (i : Fin (n+2)) :
    pathAt B u (n+1) h ≫ B.map ((SimplexCategory.δ i).op ×ₘ (SimplexCategory.δ i).op) =
      evalDeleted B p q n h (deleted u (indexAt h i)) := by
  unfold pathAt evalDeleted
  rw [← B.map_comp]
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · apply Quiver.Hom.unop_inj
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    change u.val.1 (indexAt h (i.succAbove j)) =
      u.val.1 ((indexAt h i).succAbove (deletedIndex h j))
    rw [index_face]
  · apply Quiver.Hom.unop_inj
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    change u.val.2 (indexAt h (i.succAbove j)) =
      u.val.2 ((indexAt h i).succAbove (deletedIndex h j))
    rw [index_face]

set_option backward.isDefEq.respectTransparency false in
theorem hor_eval (B : Bi) {p q n : ℕ} (h : p+1+q=n+1) (v : Path p q) (a : Fin (p+2)) :
    B.map ((SimplexCategory.δ a).op ×ₘ 𝟙 (d q)) ≫ pathAt B v n (by omega) =
      evalDeleted B (p+1) q n h (hPair v a) := by
  unfold pathAt evalDeleted
  rw [← B.map_comp]
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · rfl
  · apply Quiver.Hom.unop_inj
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    rfl

set_option backward.isDefEq.respectTransparency false in
theorem ver_eval (B : Bi) {p q n : ℕ} (h : p+(q+1)=n+1) (v : Path p q) (a : Fin (q+2)) :
    B.map (𝟙 (d p) ×ₘ (SimplexCategory.δ a).op) ≫ pathAt B v n (by omega) =
      evalDeleted B p (q+1) n h (vPair v a) := by
  unfold pathAt evalDeleted
  rw [← B.map_comp]
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · apply Quiver.Hom.unop_inj
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    rfl
  · rfl

set_option backward.isDefEq.respectTransparency false in
theorem diag_boundary_sum (B : Bi) (p q n : ℕ) (h : p+q=n+1) :
    (double B).ιTotal c p q (n+1) h ≫ shuffleDegree B (n+1) ≫ (diagChains B).d (n+1) n =
      ∑ u : Path p q, ∑ k : Vertex p q, faceTerm (evalDeleted B p q n h) (u,k) := by
  rw [← Category.assoc,shuffleAt_sum,diag_d,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro u _
  rw [Preadditive.zsmul_comp,Preadditive.comp_sum,Finset.smul_sum]
  apply Fintype.sum_equiv (finCongr (show n+2=p+q+1 by omega))
  intro i
  rw [Preadditive.comp_zsmul,smul_smul,diag_eval]
  unfold faceTerm
  rw [mul_comm (pathSign u)]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem hor_boundary_sum (B : Bi) (p q n : ℕ) (h : p+1+q=n+1) :
    ((double B).d (p+1) p).f q ≫ (double B).ιTotal c p q n (by change p+q=n; omega) ≫ shuffleDegree B n =
      ∑ a : Fin (p+2), ∑ v : Path p q, hTerm (evalDeleted B (p+1) q n h) (v,a) := by
  rw [shuffleAt_sum,hor_d,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro a _
  rw [Preadditive.zsmul_comp,Preadditive.comp_sum,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro v _
  rw [Preadditive.comp_zsmul,smul_smul,hor_eval]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem ver_boundary_sum (B : Bi) (p q n : ℕ) (h : p+(q+1)=n+1) :
    (-1 : ℤ)^p • (((double B).X p).d (q+1) q ≫
      (double B).ιTotal c p q n (by change p+q=n; omega) ≫ shuffleDegree B n) =
      ∑ a : Fin (q+2), ∑ v : Path p q, vTerm (evalDeleted B p (q+1) n h) (v,a) := by
  rw [shuffleAt_sum,ver_d,Preadditive.sum_comp,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro a _
  rw [Preadditive.zsmul_comp,Preadditive.comp_sum,Finset.smul_sum,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro v _
  rw [Preadditive.comp_zsmul,smul_smul,smul_smul,ver_eval]
  unfold vTerm
  rw [pow_add,mul_assoc]

set_option backward.isDefEq.respectTransparency false in
theorem mixed_chain (B : Bi) (p q n : ℕ) (h : p+1+(q+1)=n+1) :
    (double B).ιTotal c (p+1) (q+1) (n+1) h ≫
      shuffleDegree B (n+1) ≫ (diagChains B).d (n+1) n =
    (double B).ιTotal c (p+1) (q+1) (n+1) h ≫
      (total B).d (n+1) n ≫ shuffleDegree B n := by
  rw [diag_boundary_sum,boundary_sum]
  change _ = (double B).ιTotal c (p+1) (q+1) (n+1) h ≫
    ((double B).D₁ c (n+1) n + (double B).D₂ c (n+1) n) ≫ shuffleDegree B n
  rw [← Category.assoc ( (double B).ιTotal c (p+1) (q+1) (n+1) h),
    Preadditive.comp_add,horizontal_succ (double B) p (q+1) (n+1) n h (by omega),
    vertical_succ (double B) (p+1) q (n+1) n h (by omega),
    Preadditive.add_comp,Category.assoc,Preadditive.zsmul_comp,Category.assoc,
    hor_boundary_sum,ver_boundary_sum]

set_option backward.isDefEq.respectTransparency false in
theorem signed_shuffle_comm (B : Bi) (n : ℕ) :
    shuffleDegree B (n+1) ≫ (diagChains B).d (n+1) n =
    (total B).d (n+1) n ≫ shuffleDegree B n := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=n+1 at h
  cases p with
  | zero =>
    have hq : q=n+1 := by omega
    subst q
    exact vertical_chain B n
  | succ p =>
    cases q with
    | zero =>
      have hp : p=n := by omega
      subst p
      exact horizontal_chain B n
    | succ q => exact mixed_chain B p q n h

/-- The explicit signed path sum is a natural chain map in every degree. -/
def signedShuffle : Tot ⟶ D where
  app B := ChainComplex.ofHom (shuffleDegree B) (signed_shuffle_comm B)
  naturality {_B _C} f := by
    apply HomologicalComplex.Hom.ext
    funext n
    exact shuffleDegree_natural f n

/-- Eilenberg–Zilber equivalence with the original signed shuffle as inverse,
with both chain homotopies constructed on the actual complexes. -/
def signedEquiv (B : Bi) : HomotopyEquiv (D.obj B) (Tot.obj B) where
  hom := awNat.app B
  inv := signedShuffle.app B
  homotopyHomInvId := diagonalHomotopy (awNat ≫ signedShuffle) (𝟙 D) (by
    apply NatTrans.ext
    funext C
    exact aw_shuffle_zero C) B
  homotopyInvHomId := totalHomotopy (signedShuffle ≫ awNat) (𝟙 Tot) (by
    apply NatTrans.ext
    funext C
    exact shuffle_aw_zero C) B

#print axioms signedShuffle
#print axioms signedEquiv
#print axioms shuffleAt_sum
#print axioms diag_eval
#print axioms hor_eval
#print axioms ver_eval
#print axioms signed_shuffle_comm
end CMDG.CondensedCM5R0.EilenbergZilberSigned
