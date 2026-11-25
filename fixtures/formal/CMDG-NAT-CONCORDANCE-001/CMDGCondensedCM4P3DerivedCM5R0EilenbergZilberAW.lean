import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberCut

/-! Assemble the local cut cancellation into the actual Alexander–Whitney
chain map. The total differential is Mathlib's signed total differential. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberCut
namespace CMDG.CondensedCM5R0.EilenbergZilberAW

def cutMap (B : Bi) (n p q : ℕ) (h : p+q=n) :
    (diagChains B).X n ⟶ B.obj (d p,d q) :=
  B.map ((interval 0 p n (by omega)).op ×ₘ (interval p q n (by omega)).op)

def cutTerm (B : Bi) (n p q : ℕ) (h : p+q=n) :
    (diagChains B).X n ⟶ (total B).X n :=
  cutMap B n p q h ≫ (double B).ιTotal c p q n h

def term (B : Bi) (n : ℕ) (i : Fin (n+1)) :
    (diagChains B).X n ⟶ (total B).X n :=
  cutTerm B n i.val (n-i.val) (by omega)

theorem term_split (B : Bi) (n p q : ℕ) (h : p+q=n) :
    term B n ⟨p,by omega⟩ = cutTerm B n p q h := by
  have hq : q = n-p := by omega
  subst q
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem term_eq (B : Bi) (n : ℕ) (i : Fin (n+1)) :
    term B n i = awTerm B n i := by
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem diag_d (B : Bi) (n : ℕ) :
    (diagChains B).d (n+1) n =
      ∑ i : Fin (n+2), (-1 : ℤ)^i.val •
        B.map ((SimplexCategory.δ i).op ×ₘ (SimplexCategory.δ i).op) := by
  unfold diagChains
  rw [alternatingFaceMapComplex_obj_d]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem hor_d (B : Bi) (p q : ℕ) :
    ((double B).d (p+1) p).f q =
      ∑ i : Fin (p+2), (-1 : ℤ)^i.val • B.map ((SimplexCategory.δ i).op ×ₘ 𝟙 (d q)) := by
  let F := HomologicalComplex.eval ZMod c q
  change F.map ((double B).d (p+1) p) = _
  unfold double
  rw [alternatingFaceMapComplex_obj_d]
  unfold AlternatingFaceMapComplex.objD
  rw [Functor.map_sum]
  simp only [Functor.map_zsmul]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem ver_d (B : Bi) (p q : ℕ) :
    ((double B).X p).d (q+1) q =
      ∑ i : Fin (q+2), (-1 : ℤ)^i.val • B.map (𝟙 (d p) ×ₘ (SimplexCategory.δ i).op) := by
  change ((alternatingFaceMapComplex ZMod).obj ((Functor.curry.obj B).obj (d p))).d (q+1) q = _
  rw [alternatingFaceMapComplex_obj_d]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem diag_cut (B : Bi) (p q : ℕ) :
    (diagChains B).d (p+q+1) (p+q) ≫ cutMap B (p+q) p q rfl =
      ∑ i : Fin (p+q+2), (-1 : ℤ)^i.val • dFace B p q i := by
  rw [diag_d,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.zsmul_comp]
  congr 1
  unfold cutMap dFace
  rw [← B.map_comp]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem hor_cut (B : Bi) (p q : ℕ) :
    cutMap B (p+q+1) (p+1) q (by omega) ≫ ((double B).d (p+1) p).f q =
      ∑ i : Fin (p+2), (-1 : ℤ)^i.val • hFace B p q i := by
  rw [hor_d,Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.comp_zsmul]
  congr 1
  unfold cutMap hFace
  rw [← B.map_comp]
  congr 1

set_option backward.isDefEq.respectTransparency false in
theorem ver_cut (B : Bi) (p q : ℕ) :
    (-1 : ℤ)^p • (cutMap B (p+q+1) p (q+1) (by omega) ≫ ((double B).X p).d (q+1) q) =
      ∑ i : Fin (q+2), (-1 : ℤ)^(p+i.val) • vFace B p q i := by
  rw [ver_d,Preadditive.comp_sum,Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.comp_zsmul,smul_smul,← pow_add]
  congr 1
  unfold cutMap vFace
  rw [← B.map_comp]
  congr 1

set_option backward.isDefEq.respectTransparency false in
theorem hor_term (B : Bi) (p q : ℕ) :
    cutTerm B (p+q+1) (p+1) q (by omega) ≫ (double B).D₁ c (p+q+1) (p+q) =
      (∑ i : Fin (p+2), (-1 : ℤ)^i.val • hFace B p q i) ≫
        (double B).ιTotal c p q (p+q) rfl := by
  unfold cutTerm
  rw [Category.assoc,HomologicalComplex₂.ι_D₁]
  have h := HomologicalComplex₂.d₁_eq (double B) c (i₁ := p+1) (i₁' := p)
    (by rfl) q (p+q) rfl
  rw [h]
  change cutMap B (p+q+1) (p+1) q _ ≫ ((1 : ℤˣ) •
    (((double B).d (p+1) p).f q ≫ (double B).ιTotal c p q (p+q) rfl)) = _
  rw [one_smul,← Category.assoc,hor_cut]

set_option backward.isDefEq.respectTransparency false in
theorem ver_term (B : Bi) (p q : ℕ) :
    cutTerm B (p+q+1) p (q+1) (by omega) ≫ (double B).D₂ c (p+q+1) (p+q) =
      (∑ i : Fin (q+2), (-1 : ℤ)^(p+i.val) • vFace B p q i) ≫
        (double B).ιTotal c p q (p+q) rfl := by
  unfold cutTerm
  rw [Category.assoc,HomologicalComplex₂.ι_D₂]
  have h := HomologicalComplex₂.d₂_eq (double B) c p (i₂ := q+1) (i₂' := q)
    (by rfl) (p+q) rfl
  rw [h]
  change cutMap B (p+q+1) p (q+1) _ ≫ (((-1 : ℤˣ)^p) •
    (((double B).X p).d (q+1) q ≫ (double B).ιTotal c p q (p+q) rfl)) = _
  rw [Linear.comp_units_smul,← Category.assoc,← Linear.units_smul_comp]
  change ((-1 : ℤ)^p • (cutMap B (p+q+1) p (q+1) _ ≫ ((double B).X p).d (q+1) q)) ≫ _ = _
  rw [ver_cut]

set_option backward.isDefEq.respectTransparency false in
theorem cut_term_comm (B : Bi) (p q : ℕ) :
    (diagChains B).d (p+q+1) (p+q) ≫ cutTerm B (p+q) p q rfl =
      cutTerm B (p+q+1) (p+1) q (by omega) ≫ (double B).D₁ c (p+q+1) (p+q) +
      cutTerm B (p+q+1) p (q+1) (by omega) ≫ (double B).D₂ c (p+q+1) (p+q) := by
  rw [hor_term,ver_term,← Preadditive.add_comp,← cutBoundary]
  unfold cutTerm
  rw [← Category.assoc,diag_cut]

set_option backward.isDefEq.respectTransparency false in
theorem term_comm (B : Bi) (n : ℕ) (i : Fin (n+1)) :
    (diagChains B).d (n+1) n ≫ term B n i =
      term B (n+1) i.succ ≫ (double B).D₁ c (n+1) n +
      term B (n+1) i.castSucc ≫ (double B).D₂ c (n+1) n := by
  obtain ⟨p,hp⟩ := i
  generalize hq : n-p = q
  have hn : p+q=n := by omega
  have hc := cut_term_comm B p q
  -- Work at the exact ambient degree, before rewriting the cut.
  have h (m : ℕ) (hm : p+q=m) :
      (diagChains B).d (m+1) m ≫ cutTerm B m p q hm =
      cutTerm B (m+1) (p+1) q (by omega) ≫ (double B).D₁ c (m+1) m +
      cutTerm B (m+1) p (q+1) (by omega) ≫ (double B).D₂ c (m+1) m := by
    subst m
    exact hc
  rw [term_split B n p q hn]
  change _ = term B (n+1) ⟨p+1,by omega⟩ ≫ _ +
    term B (n+1) ⟨p,by omega⟩ ≫ _
  rw [term_split B (n+1) (p+1) q (by omega),term_split B (n+1) p (q+1) (by omega)]
  exact h n hn

set_option backward.isDefEq.respectTransparency false in
theorem horizontal_zero (B : Bi) (n : ℕ) :
    term B (n+1) 0 ≫ (double B).D₁ c (n+1) n = 0 := by
  change term B (n+1) ⟨0,by omega⟩ ≫ _ = _
  rw [term_split B (n+1) 0 (n+1) (by omega)]
  unfold cutTerm
  rw [Category.assoc,HomologicalComplex₂.ι_D₁]
  have h := HomologicalComplex₂.d₁_eq_zero (double B) c 0 (n+1) n (by
    simp [c])
  rw [h,comp_zero]

set_option backward.isDefEq.respectTransparency false in
theorem vertical_zero (B : Bi) (n : ℕ) :
    term B (n+1) (Fin.last (n+1)) ≫ (double B).D₂ c (n+1) n = 0 := by
  rw [show Fin.last (n+1) = (⟨n+1,by omega⟩ : Fin (n+2)) from rfl]
  rw [term_split B (n+1) (n+1) 0 (by omega)]
  unfold cutTerm
  rw [Category.assoc,HomologicalComplex₂.ι_D₂]
  have h := HomologicalComplex₂.d₂_eq_zero (double B) c (n+1) 0 n (by
    simp [c])
  rw [h,comp_zero]

set_option backward.isDefEq.respectTransparency false in
theorem aw_comm (B : Bi) (n : ℕ) :
    (diagChains B).d (n+1) n ≫ awDegree B n =
      awDegree B (n+1) ≫ (total B).d (n+1) n := by
  simp only [awDegree,← term_eq]
  change _ ≫ (∑ i, term B n i) = (∑ i, term B (n+1) i) ≫
    ((double B).D₁ c (n+1) n + (double B).D₂ c (n+1) n)
  rw [Preadditive.comp_sum,Preadditive.comp_add,Preadditive.sum_comp,Preadditive.sum_comp]
  rw [Fin.sum_univ_succ (fun i : Fin (n+2) => term B (n+1) i ≫ (double B).D₁ c (n+1) n),
    Fin.sum_univ_castSucc (fun i : Fin (n+2) => term B (n+1) i ≫ (double B).D₂ c (n+1) n)]
  rw [horizontal_zero,vertical_zero,zero_add,add_zero,← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl (fun i _ => term_comm B n i)

/-- The actual Alexander–Whitney chain map, not just a graded family. -/
def aw (B : Bi) : diagChains B ⟶ total B :=
  ChainComplex.ofHom (awDegree B) (fun n => (aw_comm B n).symm)

#print axioms cut_term_comm
#print axioms aw
end CMDG.CondensedCM5R0.EilenbergZilberAW
