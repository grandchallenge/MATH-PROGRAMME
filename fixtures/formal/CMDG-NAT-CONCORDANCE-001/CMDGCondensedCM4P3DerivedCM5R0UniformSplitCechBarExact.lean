import CMDGCondensedCM4P3DerivedCM5R0UniformSplitCechTuple
import CMDGCondensedCM4P3DerivedCM5R0UniformCategoricalCechHom
import Mathlib.Algebra.Homology.ShortComplex.Exact
import CMDGCondensedCM4P3DerivedCM5R0UniformShortExactFromHomotopy

noncomputable section
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

universe u

private abbrev bar (A B : Type (u + 1)) (p : A → B) (n : ℕ) :=
  (ModuleCat.free Coeff).obj (splitCechTuple A B p n)

def splitBarD (A B : Type (u + 1)) (p : A → B) (n : ℕ) :
    bar A B p (n + 1) ⟶ bar A B p n :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    (ModuleCat.free Coeff).map (↾splitCechFace A B p n k)

def splitBarH (A B : Type (u + 1)) (p : A → B)
    (s : B → A) (hs : ∀ b, p (s b) = b) (n : ℕ) :
    bar A B p n ⟶ bar A B p (n + 1) :=
  (ModuleCat.free Coeff).map (↾splitCechExtra A B p s hs n)

theorem splitBarD_comp_H_identity
    (A B : Type (u + 1)) (p : A → B)
    (s : B → A) (hs : ∀ b, p (s b) = b)
    (n : ℕ) :
    splitBarH A B p s hs (n + 1) ≫ splitBarD A B p (n + 1) +
      splitBarD A B p n ≫ splitBarH A B p s hs n =
        𝟙 (bar A B p (n + 1)) := by
  unfold splitBarH splitBarD
  simp only [Preadditive.comp_sum, Preadditive.sum_comp,
    Preadditive.comp_zsmul, Preadditive.zsmul_comp]
  rw [Fin.sum_univ_succ]
  simp only [Fin.val_zero, pow_zero, one_smul,
    Fin.val_succ, pow_succ, mul_neg, mul_one, neg_smul,
    ← Finset.sum_neg_distrib]
  have h0 : (ModuleCat.free Coeff).map
       (↾splitCechExtra A B p s hs (n + 1)) ≫
      (ModuleCat.free Coeff).map
        (↾splitCechFace A B p (n + 1) 0) =
      𝟙 (bar A B p (n + 1)) := by
    rw [← Functor.map_comp]
    have he : (↾splitCechExtra A B p s hs (n + 1)) ≫
        (↾splitCechFace A B p (n + 1) 0) =
        𝟙 (splitCechTuple A B p (n + 1)) := by
      ext xs
      exact splitCechFace_zero_extra A B p s hs (n + 1) xs
    rw [he]
    simp
  rw [h0]
  have hs (k : Fin (n + 2)) :
      (ModuleCat.free Coeff).map
          (↾splitCechExtra A B p s hs (n + 1)) ≫
        (ModuleCat.free Coeff).map
          (↾splitCechFace A B p (n + 1) k.succ) =
      (ModuleCat.free Coeff).map
          (↾splitCechFace A B p n k) ≫
        (ModuleCat.free Coeff).map
          (↾splitCechExtra A B p s hs n) := by
    have he : (↾splitCechExtra A B p s hs (n + 1)) ≫
        (↾splitCechFace A B p (n + 1) k.succ) =
        (↾splitCechFace A B p n k) ≫
        (↾splitCechExtra A B p s hs n) := by
      ext x
      exact splitCechFace_succ_extra A B p s hs n k x
    calc
      _ = (ModuleCat.free Coeff).map
          ((↾splitCechExtra A B p s hs (n + 1)) ≫
            (↾splitCechFace A B p (n + 1) k.succ)) := by
              rw [Functor.map_comp]
      _ = (ModuleCat.free Coeff).map
          ((↾splitCechFace A B p n k) ≫
            (↾splitCechExtra A B p s hs n)) := by rw [he]
      _ = _ := by rw [Functor.map_comp]
  simp only [hs]
  rw [Finset.sum_neg_distrib]
  abel

theorem splitCechFace_comp_swap (A : Type (u + 1)) (B : Type (u + 1))
    (p : A → B) (n : ℕ)
    (i : Fin (n + 2)) (j : Fin (n + 3)) :
    (↾splitCechFace A B p (n + 1) j) ≫
      (↾splitCechFace A B p n i) =
    (↾splitCechFace A B p (n + 1) (j.succAbove i)) ≫
      (↾splitCechFace A B p n (i.predAbove j)) := by
  ext xs
  apply Subtype.ext
  change i.removeNth (j.removeNth xs.val) =
    (i.predAbove j).removeNth ((j.succAbove i).removeNth xs.val)
  exact Fin.removeNth_removeNth_eq_swap xs.val i j

theorem splitBarD_comp_D_zero (A B : Type (u + 1)) (p : A → B)
    (n : ℕ) :
    splitBarD A B p (n + 1) ≫ splitBarD A B p n = 0 := by
  dsimp [splitBarD]
  simp only [Preadditive.comp_sum, Preadditive.sum_comp,
    ← Finset.sum_product']
  let IJ := Fin (n + 2) × Fin (n + 3)
  let S : Finset IJ := {ij : IJ | (ij.2 : ℕ) ≤ (ij.1 : ℕ)}
  rw [Finset.univ_product_univ, ← Finset.sum_add_sum_compl S,
    ← eq_neg_iff_add_eq_zero, ← Finset.sum_neg_distrib]
  let φ : ∀ ij : IJ, ij ∈ S → IJ := fun ij hij =>
    (Fin.castLT ij.2
      (lt_of_le_of_lt (Finset.mem_filter.mp hij).right (Fin.is_lt ij.1)),
      ij.1.succ)
  apply Finset.sum_bij φ
  · intro ij hij
    simp_rw [S, φ, Finset.compl_filter, Finset.mem_filter_univ,
      Fin.val_succ, Fin.val_castLT] at hij ⊢
    lia
  · rintro ⟨i,j⟩ hij ⟨i',j'⟩ hij' h
    rw [Prod.mk_inj]
    exact ⟨by simpa [φ] using! congr_arg Prod.snd h,
      by simpa [φ, Fin.castSucc_castLT] using!
        congr_arg Fin.castSucc (congr_arg Prod.fst h)⟩
  · rintro ⟨i',j'⟩ hij'
    simp_rw [S, Finset.compl_filter, Finset.mem_filter_univ, not_le] at hij'
    refine ⟨(j'.pred <| ?_,Fin.castSucc i'), ?_, ?_⟩
    · rintro rfl
      simp only [Fin.val_zero, not_lt_zero] at hij'
    · simpa [S] using! Nat.le_sub_one_of_lt hij'
    · simp only [φ, Fin.castLT_castSucc, Fin.succ_pred]
  · rintro ⟨i,j⟩ hij
    dsimp
    simp only [Preadditive.zsmul_comp, Preadditive.comp_zsmul,
      smul_smul, ← neg_smul]
    congr 1
    · simp only [φ, Fin.val_succ, pow_add, pow_one, mul_neg,
        neg_neg, mul_one]
      apply mul_comm
    · have hface := splitCechFace_comp_swap A B p n i j
      simp only [φ]
      have hjval : (j : ℕ) ≤ (i : ℕ) :=
        (Finset.mem_filter.mp hij).2
      have hjle : j ≤ i.castSucc := Fin.le_iff_val_le_val.mpr hjval
      have hidx : i.predAbove j =
          Fin.castLT j (lt_of_le_of_lt hjval (Fin.is_lt i)) := by
        rw [Fin.predAbove_of_le_castSucc i j hjle]
        apply Fin.ext
        rfl
      have hidx' : j.succAbove i = i.succ :=
        Fin.succAbove_of_le_castSucc j i hjle
      rw [hidx, hidx'] at hface
      have hmap := congrArg
        (fun m => (ModuleCat.free Coeff).map m) hface
      change (ModuleCat.free Coeff).map
          (↾splitCechFace A B p (n + 1) j) ≫
            (ModuleCat.free Coeff).map
              (↾splitCechFace A B p n i) =
        (ModuleCat.free Coeff).map
          (↾splitCechFace A B p (n + 1) i.succ) ≫
            (ModuleCat.free Coeff).map
              (↾splitCechFace A B p n
                (Fin.castLT j (lt_of_le_of_lt hjval (Fin.is_lt i))))
      simpa only [Functor.map_comp] using hmap

def splitBarShortComplex (A B : Type (u + 1)) (p : A → B)
    (n : ℕ) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (splitBarD A B p (n + 1))
    (splitBarD A B p n)
    (splitBarD_comp_D_zero A B p n)

theorem splitBarShortComplex_exact
    (A B : Type (u + 1)) (p : A → B)
    (s : B → A) (hs : ∀ b, p (s b) = b)
    (n : ℕ) :
    (splitBarShortComplex A B p n).Exact := by
  apply shortComplex_exact_of_middle_homotopy
    (splitBarShortComplex A B p n)
    (splitBarH A B p s hs (n + 1))
    (splitBarH A B p s hs n)
  exact splitBarD_comp_H_identity A B p s hs n

#print axioms splitBarShortComplex_exact
#print axioms splitBarD_comp_D_zero
#print axioms splitBarD_comp_H_identity
end CMDG.CondensedCM5R0
