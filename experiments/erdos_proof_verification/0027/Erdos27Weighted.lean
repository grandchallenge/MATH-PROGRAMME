import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Tactic.NormNum
import Mathlib.Data.Finset.Card
import Mathlib.Algebra.Order.BigOperators.Group.Finset

namespace Erdos27Weighted

def ideal (p : ℕ → ℚ) : ℕ → ℚ
  | 0 => 1
  | n+1 => (1 - p n) * ideal p n

def weightedError (p e : ℕ → ℚ) : ℕ → ℚ
  | 0 => 0
  | n+1 => (1 - p n) * weightedError p e n + e n

def plainError (e : ℕ → ℚ) : ℕ → ℚ
  | 0 => 0
  | n+1 => plainError e n + e n

theorem weighted_recurrence (p e q : ℕ → ℚ)
    (h0 : q 0 = 1) (hp : ∀ j, p j ≤ 1)
    (hstep : ∀ j, (1-p j)*q j-e j ≤ q (j+1)) (n : ℕ) :
    ideal p n - weightedError p e n ≤ q n := by
  induction n with
  | zero => simp [ideal, weightedError, h0]
  | succ n ih =>
    simp only [ideal, weightedError]
    have h := mul_le_mul_of_nonneg_left ih (sub_nonneg.mpr (hp n))
    rw [sub_add_eq_sub_sub, ← mul_sub]
    exact (sub_le_sub_right h (e n)).trans (hstep n)

theorem weighted_nonneg (p e : ℕ → ℚ) (hp : ∀ j, p j ≤ 1)
    (he : ∀ j, 0 ≤ e j) (n : ℕ) : 0 ≤ weightedError p e n := by
  induction n with
  | zero => simp [weightedError]
  | succ n ih => exact add_nonneg (mul_nonneg (sub_nonneg.mpr (hp n)) ih) (he n)

theorem weighted_le_plain (p e : ℕ → ℚ)
    (hp0 : ∀ j, 0 ≤ p j) (hp1 : ∀ j, p j ≤ 1)
    (he : ∀ j, 0 ≤ e j) (n : ℕ) :
    weightedError p e n ≤ plainError e n := by
  induction n with
  | zero => simp [weightedError, plainError]
  | succ n ih =>
    simp only [weightedError, plainError]
    have h := mul_le_mul_of_nonneg_left (sub_le_self (1 : ℚ) (hp0 n))
      (weighted_nonneg p e hp1 he n)
    rw [mul_one, mul_comm (weightedError p e n) (1-p n)] at h
    exact add_le_add_left (h.trans ih) (e n)

theorem unweighted_bound (p e q : ℕ → ℚ)
    (h0 : q 0 = 1) (hp0 : ∀ j, 0 ≤ p j) (hp1 : ∀ j, p j ≤ 1)
    (he : ∀ j, 0 ≤ e j)
    (hstep : ∀ j, (1-p j)*q j-e j ≤ q (j+1)) (n : ℕ) :
    ideal p n - plainError e n ≤ q n := by
  exact (sub_le_sub_left (weighted_le_plain p e hp0 hp1 he n) (ideal p n)).trans
    (weighted_recurrence p e q h0 hp1 hstep n)

def mass {α : Type*} (T : ℕ) (S : Finset α) : ℚ := (S.card : ℚ) / T

theorem mass_mono {α : Type*} {T : ℕ} {S U : Finset α} (h : S ⊆ U) :
    mass T S ≤ mass T U := by
  unfold mass
  exact div_le_div_of_nonneg_right (by exact_mod_cast Finset.card_le_card h)
    (Nat.cast_nonneg T)

theorem mass_sdiff {α : Type*} [DecidableEq α] (T : ℕ) (S A : Finset α) :
    mass T (S \ A) = mass T S - mass T (A ∩ S) := by
  unfold mass
  rw [Finset.card_sdiff, Nat.cast_sub (Finset.card_le_card Finset.inter_subset_right), sub_div]

theorem mass_union_bound {α : Type*} [DecidableEq α] (T : ℕ) (S A : Finset α) :
    mass T (S ∪ A) ≤ mass T S + mass T A := by
  unfold mass
  rw [← add_div, ← Nat.cast_add]
  exact div_le_div_of_nonneg_right (by exact_mod_cast Finset.card_union_le S A) (Nat.cast_nonneg T)

theorem finite_step {α : Type*} [DecidableEq α] (T : ℕ)
    (I D A : Finset α) (p e : ℚ)
    (hp : 0 ≤ p) (he : mass T D ≤ e)
    (hind : mass T (A ∩ I) = p * mass T I) :
    (1-p)*mass T (I \ D)-p*e ≤ mass T ((I \ D) \ A) := by
  have hI : mass T I ≤ mass T (I \ D) + e := by
    have hcard := Finset.card_le_card_sdiff_add_card (s := I) (t := D)
    have hm : mass T I ≤ mass T (I \ D) + mass T D := by
      unfold mass
      rw [← add_div, ← Nat.cast_add]
      exact div_le_div_of_nonneg_right (by exact_mod_cast hcard) (Nat.cast_nonneg T)
    exact hm.trans (add_le_add_right he _)
  have hsub : A ∩ (I \ D) ⊆ A ∩ I := by
    intro x hx
    simp only [Finset.mem_inter, Finset.mem_sdiff] at hx ⊢
    exact ⟨hx.1, hx.2.1⟩
  have hcut : mass T (A ∩ (I \ D)) ≤ p*(mass T (I \ D)+e) :=
    (mass_mono hsub).trans (hind ▸ mul_le_mul_of_nonneg_left hI hp)
  rw [mass_sdiff T (I \ D) A]
  calc
    (1-p)*mass T (I \ D)-p*e = mass T (I \ D)-p*(mass T (I \ D)+e) := by
      rw [sub_mul, one_mul, mul_add, sub_add_eq_sub_sub]
    _ ≤ mass T (I \ D)-mass T (A ∩ (I \ D)) := sub_le_sub_left hcut _

def badUnion {α : Type*} [DecidableEq α] : List (Finset α) → Finset α
  | [] => ∅
  | A :: L => A ∪ badUnion L

def badMass {α : Type*} (T : ℕ) : List (Finset α) → ℚ
  | [] => 0
  | A :: L => mass T A + badMass T L

theorem bad_union_bound {α : Type*} [DecidableEq α] (T : ℕ) (L : List (Finset α)) :
    mass T (badUnion L) ≤ badMass T L := by
  induction L with
  | nil => simp [badUnion, badMass, mass]
  | cons A L ih =>
    exact (mass_union_bound T A (badUnion L)).trans (add_le_add_right ih _)

theorem finite_step_list {α : Type*} [DecidableEq α] (T : ℕ)
    (I A : Finset α) (L : List (Finset α)) (p : ℚ)
    (hp : 0 ≤ p) (hind : mass T (A ∩ I) = p * mass T I) :
    (1-p)*mass T (I \ badUnion L)-p*badMass T L ≤
      mass T ((I \ badUnion L) \ A) :=
  finite_step T I (badUnion L) A p (badMass T L) hp (bad_union_bound T L) hind

theorem finite_sequence {α : Type*} [DecidableEq α] (T : ℕ)
    (U I A : ℕ → Finset α) (L : ℕ → List (Finset α)) (p : ℕ → ℚ)
    (h0 : mass T (U 0) = 1) (hp0 : ∀ j, 0 ≤ p j) (hp1 : ∀ j, p j ≤ 1)
    (hU : ∀ j, U j = I j \ badUnion (L j))
    (hs : ∀ j, U (j+1) = U j \ A j)
    (hind : ∀ j, mass T (A j ∩ I j) = p j * mass T (I j)) (n : ℕ) :
    ideal p n - weightedError p (fun j => p j * badMass T (L j)) n ≤ mass T (U n) := by
  apply weighted_recurrence p (fun j => p j * badMass T (L j)) (fun j => mass T (U j)) h0 hp1
  intro j
  have h := finite_step_list T (I j) (A j) (L j) (p j) (hp0 j) (hind j)
  simpa only [← hU j, ← hs j] using h

theorem bad_mass_nonneg {α : Type*} (T : ℕ) (L : List (Finset α)) :
    0 ≤ badMass T L := by
  induction L with
  | nil => simp [badMass]
  | cons A L ih =>
    exact add_nonneg (div_nonneg (Nat.cast_nonneg A.card) (Nat.cast_nonneg T)) ih

theorem finite_sequence_unweighted {α : Type*} [DecidableEq α] (T : ℕ)
    (U I A : ℕ → Finset α) (L : ℕ → List (Finset α)) (p : ℕ → ℚ)
    (h0 : mass T (U 0) = 1) (hp0 : ∀ j, 0 ≤ p j) (hp1 : ∀ j, p j ≤ 1)
    (hU : ∀ j, U j = I j \ badUnion (L j))
    (hs : ∀ j, U (j+1) = U j \ A j)
    (hind : ∀ j, mass T (A j ∩ I j) = p j * mass T (I j)) (n : ℕ) :
    ideal p n - plainError (fun j => p j * badMass T (L j)) n ≤ mass T (U n) :=
  (sub_le_sub_left (weighted_le_plain p (fun j => p j * badMass T (L j)) hp0 hp1
    (fun j => mul_nonneg (hp0 j) (bad_mass_nonneg T (L j))) n) _).trans
      (finite_sequence T U I A L p h0 hp0 hp1 hU hs hind n)

#print axioms bad_mass_nonneg
#print axioms finite_sequence_unweighted
#print axioms bad_union_bound
#print axioms finite_step_list
#print axioms finite_sequence
#print axioms mass_mono
#print axioms mass_sdiff
#print axioms mass_union_bound
#print axioms finite_step
#print axioms weighted_recurrence
#print axioms weighted_nonneg
#print axioms weighted_le_plain
#print axioms unweighted_bound
#check finite_sequence
#check finite_sequence_unweighted
-- Concrete hostile controls: removing each indicated premise makes the assertion false.
theorem reject_independence_drop :
    ¬ ((1-(1/2:ℚ))*mass 4 ({0,1}:Finset ℕ) ≤ mass 4 (({0,1}:Finset ℕ) \ ({0,1}:Finset ℕ))) := by
  simp [mass]
  norm_num

theorem reject_correlation_drop :
    ¬ ((1-(1/4:ℚ))*mass 4 ({1,3}:Finset ℕ) ≤ mass 4 (({1,3}:Finset ℕ) \ ({1}:Finset ℕ))) := by
  have h : (({1,3}:Finset ℕ) \ ({1}:Finset ℕ)) = {3} := by decide
  rw [h]
  norm_num [mass]

theorem reject_weight_range_drop :
    ¬ (0 ≤ weightedError (fun _ => 2) (fun n => if n=0 then 1 else 0) 2) := by
  norm_num [weightedError]

#print axioms reject_independence_drop
#print axioms reject_correlation_drop
#print axioms reject_weight_range_drop
end Erdos27Weighted
