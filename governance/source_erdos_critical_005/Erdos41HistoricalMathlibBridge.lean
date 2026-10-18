/-
Copyright 2026 Grand Challenge GCL.
SPDX-License-Identifier: Apache-2.0

Historical Mathlib & Formal Conjectures Theorem-Type Bridge for Erdős Problem #41.
Pinned Compiler: leanprover/lean4:v4.33.0
Pinned Mathlib:  db584cd6d46c92f209a44c0f1c829460d327499d
Provider Refreshed Commit: 79eac378a26b46d30974cdb33962e0752591b79d
  (FormalConjectures/ErdosProblems/41.lean blob SHA1: 2a1bd1f521325e36aaaf50a3a3feffc9c426aaf6)
Provider Frozen Commit:    85f863718beeec7b58a3a1926ee92e3472bc2020
  (FormalConjectures/ErdosProblems/41.lean blob SHA1: 5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50)

Scope: SOURCE_SEMANTIC formal source specification and predicate separation only.
Does NOT prove or claim any solution to the open asymptotic Erdős #41 conjecture.
-/
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Max
import Mathlib.Data.Multiset.Basic
import Mathlib.Data.Set.Finite.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Order.Interval.Finset.Nat

open scoped BigOperators
open Set

namespace Erdos41HistoricalMathlibBridge

section GeneralPredicates

variable {α : Type*} [AddCommMonoid α]

/--
Exact refreshed Formal Conjectures predicate (`NtupleCondition` from commit
`79eac378a26b46d30974cdb33962e0752591b79d`, blob `2a1bd1f521325e36aaaf50a3a3feffc9c426aaf6`):
sums of `n`-element `Multiset`s drawn from `A` (permitting repeated summands) uniquely
determine the multiset up to permutation.
-/
def NtupleCondition (A : Set α) (n : ℕ) : Prop :=
  ∀ I J : Multiset α,
    (∀ i ∈ I, i ∈ A) →
    (∀ j ∈ J, j ∈ A) →
    I.card = n →
    J.card = n →
    I.sum = J.sum →
    I = J

/--
Exact frozen historical Formal Conjectures predicate (`NtupleCondition` from commit
`85f863718beeec7b58a3a1926ee92e3472bc2020`, blob `5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50`):
sums of `n`-element `Finset`s drawn from `A` (distinct summands of fixed cardinality `n`)
uniquely determine the finset.
-/
def FrozenFinsetNtupleCondition (A : Set α) (n : ℕ) : Prop :=
  ∀ (I : Finset α) (J : Finset α),
    ↑I ⊆ A ∧ ↑J ⊆ A ∧ I.card = n ∧ J.card = n ∧
    (∑ i ∈ I, i = ∑ j ∈ J, j) → I = J

/--
Primary historical 1980 survey predicate (`B_r`, Erdős 1980 pp. 98–99):
sums of nonempty `Finset`s of at most `r` distinct elements drawn from `A`
(Sidon 0/1 coefficients on distinct terms, `1 ≤ |I| ≤ r`) uniquely determine the subset.
-/
def HistoricalBrCondition (A : Set α) (r : ℕ) : Prop :=
  ∀ (I J : Finset α),
    ↑I ⊆ A → ↑J ⊆ A →
    I.Nonempty → J.Nonempty →
    I.card ≤ r → J.card ≤ r →
    (∑ i ∈ I, i = ∑ j ∈ J, j) → I = J

end GeneralPredicates

/-!
## Specialization to `ℕ` and `r = 3` (`HistoricalB3`, `ModernB3`, `WeakFixed3`)
-/

/-- `HistoricalB3 A`: nonempty `Finset ℕ` subsets of `A` of cardinality at most 3 have distinct sums. -/
def HistoricalB3 (A : Set ℕ) : Prop :=
  HistoricalBrCondition A 3

/-- `ModernB3 A`: 3-element `Multiset ℕ`s in `A` (allowing repeated elements) have distinct sums. -/
def ModernB3 (A : Set ℕ) : Prop :=
  NtupleCondition A 3

/-- `WeakFixed3 A`: 3-element `Finset ℕ` subsets of `A` (distinct elements, fixed size 3) have distinct sums. -/
def WeakFixed3 (A : Set ℕ) : Prop :=
  FrozenFinsetNtupleCondition A 3

/--
Kernel-proved one-way implication `HistoricalB3 → WeakFixed3`:
any set with unique sums over nonempty distinct subsets of size `≤ 3` has unique sums over
distinct subsets of exact size `3`.
-/
theorem historical_implies_fixed (A : Set ℕ) (h : HistoricalB3 A) : WeakFixed3 A := by
  intro I J ⟨hIA, hJA, hI3, hJ3, hsum⟩
  have hIne : I.Nonempty := Finset.card_pos.mp (by omega)
  have hJne : J.Nonempty := Finset.card_pos.mp (by omega)
  exact h I J hIA hJA hIne hJne (by omega) (by omega) hsum

/--
Kernel-proved one-way implication `ModernB3 → WeakFixed3`:
any set with unique sums over 3-term multisets (with repetition) has unique sums over
3-element finsets (without repetition), because `Finset.val` embeds `Finset ℕ` into `Multiset ℕ`.
-/
theorem modern_implies_fixed (A : Set ℕ) (h : ModernB3 A) : WeakFixed3 A := by
  intro I J ⟨hIA, hJA, hI3, hJ3, hsum⟩
  apply Finset.val_inj.mp
  apply h I.val J.val
  · intro i hi
    exact hIA (Finset.mem_coe.mpr hi)
  · intro j hj
    exact hJA (Finset.mem_coe.mpr hj)
  · exact hI3
  · exact hJ3
  · rw [Finset.sum_val, Finset.sum_val]
    exact hsum

/-!
## Boundary Conventions: Empty Set, Zero, Permutation, Diagonal, and Cross-Cardinality
-/

/-- The empty set vacuously satisfies all three predicates. -/
theorem empty_historicalB3 : HistoricalB3 (∅ : Set ℕ) := by
  intro I _ hIA _ ⟨x, hx⟩ _ _ _ _
  exact False.elim (hIA (Finset.mem_coe.mpr hx))

theorem empty_modernB3 : ModernB3 (∅ : Set ℕ) := by
  intro I _ hIA _ hI3 _ _
  obtain ⟨x, hx⟩ := Multiset.exists_mem_of_ne_zero (by intro (h0 : I = 0); rw [h0] at hI3; contradiction)
  exact False.elim (hIA x hx)

theorem empty_weakFixed3 : WeakFixed3 (∅ : Set ℕ) := by
  exact modern_implies_fixed ∅ empty_modernB3

/--
Zero-element convention: if `0 ∈ A` and `a ∈ A` with `a ≠ 0`, then `{a}` and `{0, a}` are
distinct nonempty subsets of size `≤ 2 ≤ 3` with identical sum `a`, violating `HistoricalB3 A`.
-/
theorem zero_and_nonzero_not_historicalB3 {A : Set ℕ} {a : ℕ}
    (h0 : 0 ∈ A) (ha : a ∈ A) (hne : a ≠ 0) : ¬ HistoricalB3 A := by
  intro h
  let I : Finset ℕ := {a}
  let J : Finset ℕ := insert 0 ({a} : Finset ℕ)
  have hIA : (↑I : Set ℕ) ⊆ A := by
    intro x hx
    rw [Finset.coe_singleton, Set.mem_singleton_iff] at hx
    exact hx ▸ ha
  have hJA : (↑J : Set ℕ) ⊆ A := by
    intro x hx
    simp only [J, Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact h0
    · exact ha
  have h0not : (0 : ℕ) ∉ ({a} : Finset ℕ) := by
    rw [Finset.mem_singleton]
    exact hne.symm
  have hIc : I.card ≤ 3 := by
    change ({a} : Finset ℕ).card ≤ 3
    rw [Finset.card_singleton]
    decide
  have hJc : J.card ≤ 3 := by
    have hle := Finset.card_insert_le 0 ({a} : Finset ℕ)
    rw [Finset.card_singleton] at hle
    exact Nat.le_trans hle (by decide)
  have hsum : ∑ i ∈ I, i = ∑ j ∈ J, j := by
    change ∑ i ∈ ({a} : Finset ℕ), i = ∑ j ∈ insert 0 ({a} : Finset ℕ), j
    rw [Finset.sum_insert h0not, Finset.sum_singleton, zero_add]
  have hIJ : I = J := h I J hIA hJA (Finset.singleton_nonempty a) ⟨0, Finset.mem_insert_self 0 {a}⟩ hIc hJc hsum
  have h0inI : (0 : ℕ) ∈ I := hIJ.symm ▸ Finset.mem_insert_self 0 {a}
  exact h0not h0inI

/--
Permutation convention: `Multiset ℕ` equality is quotient equality modulo `List.Perm`,
so reordering summands is automatically identified as a trivial coincidence in `ModernB3`.
-/
theorem multiset_perm_trivial_coincidence (xs ys : List ℕ) (h : xs.Perm ys) :
    (xs : Multiset ℕ) = (ys : Multiset ℕ) :=
  Multiset.coe_eq_coe.mpr h

/--
Diagonal convention: `Finset ℕ` deduplicates repeated elements (`{a, a, b} = {a, b}`),
whereas `Multiset ℕ` preserves multiplicity (`a ::ₘ a ::ₘ b ::ₘ 0` has cardinality 3).
-/
theorem diagonal_finset_dedup_vs_multiset_card (a : ℕ) :
    ({a, a, a} : Finset ℕ).card = 1 ∧ ((a ::ₘ a ::ₘ a ::ₘ 0 : Multiset ℕ).card = 3) := by
  simp

/--
Cross-cardinality convention: if `a, b ∈ A` with `a ≠ b`, `0 < a`, `0 < b`, and `a + b ∈ A`,
then `{a, b}` (size 2) and `{a + b}` (size 1) have identical sum `a + b` and distinct sizes,
violating `HistoricalB3 A`.
-/
theorem cross_cardinality_pair_eq_singleton_not_historicalB3 {A : Set ℕ} {a b : ℕ}
    (ha : a ∈ A) (hb : b ∈ A) (hab : a + b ∈ A)
    (hne : a ≠ b) (ha0 : 0 < a) (hb0 : 0 < b) : ¬ HistoricalB3 A := by
  intro h
  let I : Finset ℕ := insert a ({b} : Finset ℕ)
  let J : Finset ℕ := {a + b}
  have hIA : (↑I : Set ℕ) ⊆ A := by
    intro x hx
    simp only [I, Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact ha
    · exact hb
  have hJA : (↑J : Set ℕ) ⊆ A := by
    intro x hx
    rw [Finset.coe_singleton, Set.mem_singleton_iff] at hx
    exact hx ▸ hab
  have hanotb : a ∉ ({b} : Finset ℕ) := by
    rw [Finset.mem_singleton]
    exact hne
  have hIc : I.card ≤ 3 := by
    have hle := Finset.card_insert_le a ({b} : Finset ℕ)
    rw [Finset.card_singleton] at hle
    exact Nat.le_trans hle (by decide)
  have hJc : J.card ≤ 3 := by
    change ({a + b} : Finset ℕ).card ≤ 3
    rw [Finset.card_singleton]
    decide
  have hsum : ∑ i ∈ I, i = ∑ j ∈ J, j := by
    change ∑ i ∈ insert a ({b} : Finset ℕ), i = ∑ j ∈ ({a + b} : Finset ℕ), j
    rw [Finset.sum_insert hanotb, Finset.sum_singleton, Finset.sum_singleton]
  have hIJ : I = J := h I J hIA hJA ⟨a, Finset.mem_insert_self a {b}⟩ (Finset.singleton_nonempty (a + b)) hIc hJc hsum
  have hainJ : a ∈ J := hIJ ▸ Finset.mem_insert_self a {b}
  rw [Finset.mem_singleton] at hainJ
  omega

/-!
## Finite Witness `{1, 2, 3}`: `WeakFixed3` Does Not Imply `HistoricalB3` or `ModernB3`
-/

def finiteWeakWitness : Set ℕ := {x : ℕ | x = 1 ∨ x = 2 ∨ x = 3}

theorem finiteWeakWitness_weakFixed3 : WeakFixed3 finiteWeakWitness := by
  intro I J ⟨hIA, hJA, hI3, hJ3, _⟩
  let U : Finset ℕ := {1, 2, 3}
  have hIU : I ⊆ U := by
    intro x hx
    have hxA := hIA (Finset.mem_coe.mpr hx)
    simp only [U, Finset.mem_insert, Finset.mem_singleton]
    exact hxA
  have hJU : J ⊆ U := by
    intro x hx
    have hxA := hJA (Finset.mem_coe.mpr hx)
    simp only [U, Finset.mem_insert, Finset.mem_singleton]
    exact hxA
  have hU3 : U.card ≤ 3 := by decide
  have hIeq : I = U := Finset.eq_of_subset_of_card_le hIU (by omega)
  have hJeq : J = U := Finset.eq_of_subset_of_card_le hJU (by omega)
  exact hIeq.trans hJeq.symm

theorem finiteWeakWitness_not_historicalB3 : ¬ HistoricalB3 finiteWeakWitness := by
  intro h
  let I : Finset ℕ := {1, 2}
  let J : Finset ℕ := {3}
  have hIA : (↑I : Set ℕ) ⊆ finiteWeakWitness := by
    intro x hx
    simp only [I, Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact Or.inl rfl
    · exact Or.inr (Or.inl rfl)
  have hJA : (↑J : Set ℕ) ⊆ finiteWeakWitness := by
    intro x hx
    simp only [J, Finset.coe_singleton, Set.mem_singleton_iff] at hx
    subst hx
    exact Or.inr (Or.inr rfl)
  have hIJ : I = J := h I J hIA hJA (by decide) (by decide) (by decide) (by decide) (by decide)
  have hmem : (1 : ℕ) ∈ J := hIJ ▸ (by decide : (1 : ℕ) ∈ I)
  exact (by decide : (1 : ℕ) ∉ J) hmem

theorem finiteWeakWitness_not_modernB3 : ¬ ModernB3 finiteWeakWitness := by
  intro h
  let I : Multiset ℕ := (1 : ℕ) ::ₘ (1 : ℕ) ::ₘ (3 : ℕ) ::ₘ 0
  let J : Multiset ℕ := (1 : ℕ) ::ₘ (2 : ℕ) ::ₘ (2 : ℕ) ::ₘ 0
  have hI : ∀ i ∈ I, i ∈ finiteWeakWitness := by
    intro i hi
    simp only [I, Multiset.mem_cons] at hi
    rcases hi with rfl | rfl | rfl | h0
    · exact Or.inl rfl
    · exact Or.inl rfl
    · exact Or.inr (Or.inr rfl)
    · cases h0
  have hJ : ∀ j ∈ J, j ∈ finiteWeakWitness := by
    intro j hj
    simp only [J, Multiset.mem_cons] at hj
    rcases hj with rfl | rfl | rfl | h0
    · exact Or.inl rfl
    · exact Or.inr (Or.inl rfl)
    · exact Or.inr (Or.inl rfl)
    · cases h0
  have hIJ : I = J := h I J hI hJ rfl rfl rfl
  have hmem : (2 : ℕ) ∈ I := hIJ.symm ▸ (by decide : (2 : ℕ) ∈ J)
  exact (by decide : (2 : ℕ) ∉ I) hmem

theorem not_weakFixed3_implies_historicalB3 : ¬ (∀ A : Set ℕ, WeakFixed3 A → HistoricalB3 A) := by
  intro h
  exact finiteWeakWitness_not_historicalB3 (h finiteWeakWitness finiteWeakWitness_weakFixed3)

theorem not_weakFixed3_implies_modernB3 : ¬ (∀ A : Set ℕ, WeakFixed3 A → ModernB3 A) := by
  intro h
  exact finiteWeakWitness_not_modernB3 (h finiteWeakWitness finiteWeakWitness_weakFixed3)

/-!
## Infinite Separating Model 1: `infSuperincreasing = {1, 2, 4} ∪ {10^k : k ≥ 1}`
Satisfies `HistoricalB3` and `WeakFixed3`, is infinite, and violates `ModernB3` (`1+1+4 = 2+2+2`).
-/

def seqA : ℕ → ℕ
  | 0 => 1
  | 1 => 2
  | 2 => 4
  | k + 3 => 10 ^ (k + 1)

def infSuperincreasing : Set ℕ :=
  {x : ℕ | x = 1 ∨ x = 2 ∨ x = 4 ∨ ∃ k ≥ 1, x = 10 ^ k}

theorem infSuperincreasing_infinite : infSuperincreasing.Infinite := by
  apply Set.infinite_of_injective_forall_mem (f := fun k : ℕ => 10 ^ (k + 1))
  · intro a b hab
    have h := Nat.pow_right_injective (by decide : 2 ≤ 10) hab
    omega
  · intro k
    exact Or.inr (Or.inr (Or.inr ⟨k + 1, by omega, rfl⟩))

lemma seqA_mem (n : ℕ) : seqA n ∈ infSuperincreasing := by
  match n with
  | 0 => exact Or.inl rfl
  | 1 => exact Or.inr (Or.inl rfl)
  | 2 => exact Or.inr (Or.inr (Or.inl rfl))
  | k + 3 => exact Or.inr (Or.inr (Or.inr ⟨k + 1, by omega, rfl⟩))

lemma ten_pow_ge_ten : ∀ k : ℕ, 10 ≤ 10 ^ (k + 1)
  | 0 => by decide
  | k + 1 => by
    have := ten_pow_ge_ten k
    rw [Nat.pow_succ]
    omega

lemma seqA_strictMono : StrictMono seqA := by
  refine strictMono_nat_of_lt_succ (fun n => ?_)
  match n with
  | 0 => decide
  | 1 => decide
  | 2 => decide
  | k + 3 =>
    change 10 ^ (k + 1) < 10 ^ (k + 1 + 1)
    have := ten_pow_ge_ten k
    rw [Nat.pow_succ 10 (k + 1)]
    omega

lemma mem_infSuperincreasing_iff (x : ℕ) : x ∈ infSuperincreasing ↔ ∃ n, seqA n = x := by
  constructor
  · intro hx
    rcases hx with rfl | rfl | rfl | ⟨k, hk, rfl⟩
    · exact ⟨0, rfl⟩
    · exact ⟨1, rfl⟩
    · exact ⟨2, rfl⟩
    · refine ⟨k + 2, ?_⟩
      obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
      rfl
  · rintro ⟨n, rfl⟩
    exact seqA_mem n

lemma sum_range_seqA_lt : ∀ m : ℕ, ∑ i ∈ Finset.range m, seqA i < seqA m
  | 0 => by decide
  | 1 => by decide
  | 2 => by decide
  | 3 => by decide
  | k + 4 => by
    have ih : ∑ i ∈ Finset.range (k + 3), seqA i < seqA (k + 3) := sum_range_seqA_lt (k + 3)
    rw [Finset.sum_range_succ]
    change (∑ i ∈ Finset.range (k + 3), seqA i) + 10 ^ (k + 1) < 10 ^ (k + 1 + 1)
    change ∑ i ∈ Finset.range (k + 3), seqA i < 10 ^ (k + 1) at ih
    rw [Nat.pow_succ 10 (k + 1)]
    omega

lemma sum_subset_lt_of_lt {I : Finset ℕ} {y : ℕ}
    (hIA : (↑I : Set ℕ) ⊆ infSuperincreasing)
    (hyA : y ∈ infSuperincreasing)
    (hlt : ∀ x ∈ I, x < y) :
    ∑ x ∈ I, x < y := by
  obtain ⟨m, rfl⟩ := (mem_infSuperincreasing_iff y).mp hyA
  have hsub : I ⊆ (Finset.range m).image seqA := by
    intro x hx
    have hxA := hIA (Finset.mem_coe.mpr hx)
    obtain ⟨n, rfl⟩ := (mem_infSuperincreasing_iff x).mp hxA
    have hlt_n : n < m := seqA_strictMono.lt_iff_lt.mp (hlt (seqA n) hx)
    exact Finset.mem_image.mpr ⟨n, Finset.mem_range.mpr hlt_n, rfl⟩
  have hle : ∑ x ∈ I, x ≤ ∑ x ∈ (Finset.range m).image seqA, x :=
    Finset.sum_le_sum_of_subset hsub
  have hinj : Set.InjOn seqA (Finset.range m) := seqA_strictMono.injective.injOn
  have himg : ∑ x ∈ (Finset.range m).image seqA, x = ∑ i ∈ Finset.range m, seqA i :=
    Finset.sum_image hinj
  have hbound := sum_range_seqA_lt m
  omega

lemma superincreasing_sum_inj : ∀ (B : ℕ) (I J : Finset ℕ),
    (↑I : Set ℕ) ⊆ infSuperincreasing →
    (↑J : Set ℕ) ⊆ infSuperincreasing →
    (∀ x ∈ I, x < B) →
    (∀ y ∈ J, y < B) →
    (∑ x ∈ I, x = ∑ y ∈ J, y) → I = J
  | 0, I, J, _, _, hIB, hJB, _ => by
    ext x
    constructor
    · intro hx; have := hIB x hx; omega
    · intro hx; have := hJB x hx; omega
  | B + 1, I, J, hIA, hJA, hIB, hJB, hsum => by
    by_cases hBI : B ∈ I <;> by_cases hBJ : B ∈ J
    · have hIA' : (↑(I.erase B) : Set ℕ) ⊆ infSuperincreasing :=
        fun x hx => hIA (Finset.erase_subset B I hx)
      have hJA' : (↑(J.erase B) : Set ℕ) ⊆ infSuperincreasing :=
        fun y hy => hJA (Finset.erase_subset B J hy)
      have hIB' : ∀ x ∈ I.erase B, x < B := by
        intro x hx
        have hne : x ≠ B := (Finset.mem_erase.mp hx).1
        have hlt : x < B + 1 := hIB x (Finset.mem_erase.mp hx).2
        omega
      have hJB' : ∀ y ∈ J.erase B, y < B := by
        intro y hy
        have hne : y ≠ B := (Finset.mem_erase.mp hy).1
        have hlt : y < B + 1 := hJB y (Finset.mem_erase.mp hy).2
        omega
      have hsumI := Finset.add_sum_erase I id hBI
      have hsumJ := Finset.add_sum_erase J id hBJ
      have hsum' : ∑ x ∈ I.erase B, x = ∑ y ∈ J.erase B, y := by
        change B + ∑ x ∈ I.erase B, x = ∑ x ∈ I, x at hsumI
        change B + ∑ y ∈ J.erase B, y = ∑ y ∈ J, y at hsumJ
        omega
      have heq := superincreasing_sum_inj B (I.erase B) (J.erase B) hIA' hJA' hIB' hJB' hsum'
      rw [← Finset.insert_erase hBI, ← Finset.insert_erase hBJ, heq]
    · have hJB' : ∀ y ∈ J, y < B := by
        intro y hy
        have hne : y ≠ B := fun h => hBJ (h ▸ hy)
        have hlt : y < B + 1 := hJB y hy
        omega
      have hBA : B ∈ infSuperincreasing := hIA (Finset.mem_coe.mpr hBI)
      have hJlt : ∑ y ∈ J, y < B := sum_subset_lt_of_lt hJA hBA hJB'
      have hsumI := Finset.add_sum_erase I id hBI
      change B + ∑ x ∈ I.erase B, x = ∑ x ∈ I, x at hsumI
      omega
    · have hIB' : ∀ x ∈ I, x < B := by
        intro x hx
        have hne : x ≠ B := fun h => hBI (h ▸ hx)
        have hlt : x < B + 1 := hIB x hx
        omega
      have hBA : B ∈ infSuperincreasing := hJA (Finset.mem_coe.mpr hBJ)
      have hIlt : ∑ x ∈ I, x < B := sum_subset_lt_of_lt hIA hBA hIB'
      have hsumJ := Finset.add_sum_erase J id hBJ
      change B + ∑ y ∈ J.erase B, y = ∑ y ∈ J, y at hsumJ
      omega
    · have hIB' : ∀ x ∈ I, x < B := by
        intro x hx
        have hne : x ≠ B := fun h => hBI (h ▸ hx)
        have hlt : x < B + 1 := hIB x hx
        omega
      have hJB' : ∀ y ∈ J, y < B := by
        intro y hy
        have hne : y ≠ B := fun h => hBJ (h ▸ hy)
        have hlt : y < B + 1 := hJB y hy
        omega
      exact superincreasing_sum_inj B I J hIA hJA hIB' hJB' hsum

theorem infSuperincreasing_finset_sum_inj (I J : Finset ℕ)
    (hIA : (↑I : Set ℕ) ⊆ infSuperincreasing)
    (hJA : (↑J : Set ℕ) ⊆ infSuperincreasing)
    (hsum : ∑ i ∈ I, i = ∑ j ∈ J, j) : I = J := by
  apply superincreasing_sum_inj ((∑ i ∈ I, i) + (∑ j ∈ J, j) + 1) I J hIA hJA
  · intro x hx
    have hle : x ≤ ∑ i ∈ I, i := Finset.single_le_sum (f := fun i : ℕ => i) (fun _ _ => Nat.zero_le _) hx
    omega
  · intro y hy
    have hle : y ≤ ∑ j ∈ J, j := Finset.single_le_sum (f := fun j : ℕ => j) (fun _ _ => Nat.zero_le _) hy
    omega
  · exact hsum

theorem infSuperincreasing_historicalB3 : HistoricalB3 infSuperincreasing := by
  intro I J hIA hJA _ _ _ _ hsum
  exact infSuperincreasing_finset_sum_inj I J hIA hJA hsum

theorem infSuperincreasing_weakFixed3 : WeakFixed3 infSuperincreasing :=
  historical_implies_fixed infSuperincreasing infSuperincreasing_historicalB3

theorem infSuperincreasing_not_modernB3 : ¬ ModernB3 infSuperincreasing := by
  intro h
  let I : Multiset ℕ := (1 : ℕ) ::ₘ (1 : ℕ) ::ₘ (4 : ℕ) ::ₘ 0
  let J : Multiset ℕ := (2 : ℕ) ::ₘ (2 : ℕ) ::ₘ (2 : ℕ) ::ₘ 0
  have hI : ∀ i ∈ I, i ∈ infSuperincreasing := by
    intro i hi
    simp only [I, Multiset.mem_cons] at hi
    rcases hi with rfl | rfl | rfl | h0
    · exact Or.inl rfl
    · exact Or.inl rfl
    · exact Or.inr (Or.inr (Or.inl rfl))
    · cases h0
  have hJ : ∀ j ∈ J, j ∈ infSuperincreasing := by
    intro j hj
    simp only [J, Multiset.mem_cons] at hj
    rcases hj with rfl | rfl | rfl | h0
    · exact Or.inr (Or.inl rfl)
    · exact Or.inr (Or.inl rfl)
    · exact Or.inr (Or.inl rfl)
    · cases h0
  have hIJ : I = J := h I J hI hJ rfl rfl rfl
  have hmem : (1 : ℕ) ∈ J := hIJ ▸ (by decide : (1 : ℕ) ∈ I)
  exact (by decide : (1 : ℕ) ∉ J) hmem

/-!
## Infinite Separating Model 2: `infModernWitness = {1, 4, 5} ∪ {100^k : k ≥ 1}`
Satisfies `ModernB3` and `WeakFixed3`, is infinite, and violates `HistoricalB3` (`1+4 = 5`).
-/

def infModernWitness : Set ℕ :=
  {x : ℕ | x = 1 ∨ x = 4 ∨ x = 5 ∨ ∃ k ≥ 1, x = 100 ^ k}

theorem infModernWitness_infinite : infModernWitness.Infinite := by
  apply Set.infinite_of_injective_forall_mem (f := fun k : ℕ => 100 ^ (k + 1))
  · intro a b hab
    have h := Nat.pow_right_injective (by decide : 2 ≤ 100) hab
    omega
  · intro k
    exact Or.inr (Or.inr (Or.inr ⟨k + 1, by omega, rfl⟩))

lemma hundred_pow_ge_hundred : ∀ k : ℕ, 100 ≤ 100 ^ (k + 1)
  | 0 => by decide
  | k + 1 => by
    have := hundred_pow_ge_hundred k
    rw [Nat.pow_succ 100 (k + 1)]
    omega

lemma elem_bound_of_lt_tail {x k : ℕ} (hxA : x ∈ infModernWitness) (hlt : x < 100 ^ (k + 1)) :
    3 * x + 1 ≤ 100 ^ (k + 1) := by
  rcases hxA with rfl | rfl | rfl | ⟨m, hm, rfl⟩
  · have := hundred_pow_ge_hundred k; omega
  · have := hundred_pow_ge_hundred k; omega
  · have := hundred_pow_ge_hundred k; omega
  · have hmk : m < k + 1 := by
      by_contra hge
      have hpow : 100 ^ (k + 1) ≤ 100 ^ m := Nat.pow_le_pow_right (by decide) (by omega)
      omega
    have hpow : 100 ^ (m + 1) ≤ 100 ^ (k + 1) := Nat.pow_le_pow_right (by decide) hmk
    rw [Nat.pow_succ 100 m] at hpow
    omega

lemma multiset_sum_bound (I : Multiset ℕ) (k : ℕ)
    (hA : ∀ x ∈ I, x ∈ infModernWitness)
    (hlt : ∀ x ∈ I, x < 100 ^ (k + 1)) :
    3 * I.sum + I.card ≤ I.card * 100 ^ (k + 1) := by
  induction I using Multiset.induction_on with
  | empty => simp
  | @cons a s ih =>
    simp only [Multiset.sum_cons, Multiset.card_cons]
    have ha : 3 * a + 1 ≤ 100 ^ (k + 1) :=
      elem_bound_of_lt_tail (hA a (Multiset.mem_cons_self a s)) (hlt a (Multiset.mem_cons_self a s))
    have hs : 3 * s.sum + s.card ≤ s.card * 100 ^ (k + 1) :=
      ih (fun x hx => hA x (Multiset.mem_cons_of_mem hx))
         (fun x hx => hlt x (Multiset.mem_cons_of_mem hx))
    have hmul : (s.card + 1) * 100 ^ (k + 1) = s.card * 100 ^ (k + 1) + 100 ^ (k + 1) :=
      Nat.succ_mul s.card (100 ^ (k + 1))
    omega

lemma multiset_sum_lt_tail {I : Multiset ℕ} {k : ℕ}
    (hcard : I.card ≤ 3)
    (hA : ∀ x ∈ I, x ∈ infModernWitness)
    (hlt : ∀ x ∈ I, x < 100 ^ (k + 1)) :
    I.sum < 100 ^ (k + 1) := by
  have hb := multiset_sum_bound I k hA hlt
  have hk := hundred_pow_ge_hundred k
  rcases (by omega : I.card = 0 ∨ I.card = 1 ∨ I.card = 2 ∨ I.card = 3) with h0 | h1 | h2 | h3
  · rw [Multiset.card_eq_zero.mp h0]
    simp only [Multiset.sum_zero]
    omega
  · rw [h1] at hb; omega
  · rw [h2] at hb; omega
  · rw [h3] at hb; omega

lemma base_elem_cases {x : ℕ} (hxA : x ∈ infModernWitness) (hlt : x < 100) :
    x = 1 ∨ x = 4 ∨ x = 5 := by
  rcases hxA with rfl | rfl | rfl | ⟨k, hk, rfl⟩
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)
  · obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
    have := hundred_pow_ge_hundred m
    omega

lemma base_multiset_eq : ∀ (n : ℕ) (I J : Multiset ℕ),
    I.card = n → J.card = n → n ≤ 3 →
    (∀ x ∈ I, x = 1 ∨ x = 4 ∨ x = 5) →
    (∀ y ∈ J, y = 1 ∨ y = 4 ∨ y = 5) →
    I.sum = J.sum → I = J := by
  intro n I J hIc hJc hn3 hI hJ hsum
  obtain ⟨lI, rfl⟩ := Quotient.exists_rep I
  obtain ⟨lJ, rfl⟩ := Quotient.exists_rep J
  change lI.length = n at hIc
  change lJ.length = n at hJc
  change lI.sum = lJ.sum at hsum
  apply Multiset.coe_eq_coe.mpr
  match n, lI, lJ, hIc, hJc, hn3 with
  | 0, [], [], _, _, _ => exact List.Perm.nil
  | 1, [a], [b], _, _, _ =>
    simp only [List.sum_cons, List.sum_nil, add_zero] at hsum
    subst hsum
    exact List.Perm.refl [a]
  | 2, [a1, a2], [b1, b2], _, _, _ =>
    have ha1 := hI a1 (by simp)
    have ha2 := hI a2 (by simp)
    have hb1 := hJ b1 (by simp)
    have hb2 := hJ b2 (by simp)
    simp only [List.sum_cons, List.sum_nil, add_zero] at hsum
    rcases ha1 with rfl | rfl | rfl <;>
    rcases ha2 with rfl | rfl | rfl <;>
    rcases hb1 with rfl | rfl | rfl <;>
    rcases hb2 with rfl | rfl | rfl <;>
    first | omega | decide
  | 3, [a1, a2, a3], [b1, b2, b3], _, _, _ =>
    have ha1 := hI a1 (by simp)
    have ha2 := hI a2 (by simp)
    have ha3 := hI a3 (by simp)
    have hb1 := hJ b1 (by simp)
    have hb2 := hJ b2 (by simp)
    have hb3 := hJ b3 (by simp)
    simp only [List.sum_cons, List.sum_nil, add_zero] at hsum
    rcases ha1 with rfl | rfl | rfl <;>
    rcases ha2 with rfl | rfl | rfl <;>
    rcases ha3 with rfl | rfl | rfl <;>
    rcases hb1 with rfl | rfl | rfl <;>
    rcases hb2 with rfl | rfl | rfl <;>
    rcases hb3 with rfl | rfl | rfl <;>
    first | omega | decide

lemma modern_sum_inj : ∀ (n : ℕ) (B : ℕ) (I J : Multiset ℕ),
    I.card = n →
    J.card = n →
    n ≤ 3 →
    (∀ x ∈ I, x ∈ infModernWitness) →
    (∀ y ∈ J, y ∈ infModernWitness) →
    (∀ x ∈ I, x < B) →
    (∀ y ∈ J, y < B) →
    I.sum = J.sum → I = J
  | 0, _, I, J, hIc, hJc, _, _, _, _, _, _ => by
    rw [Multiset.card_eq_zero.mp hIc, Multiset.card_eq_zero.mp hJc]
  | n + 1, 0, I, _, hIc, _, _, _, _, hIB, _, _ => by
    obtain ⟨x, hx⟩ := Multiset.exists_mem_of_ne_zero (by intro (h0 : I = 0); rw [h0] at hIc; contradiction)
    have := hIB x hx
    omega
  | n + 1, B + 1, I, J, hIc, hJc, hn3, hIA, hJA, hIB, hJB, hsum => by
    by_cases hB100 : B < 100
    · apply base_multiset_eq (n + 1) I J hIc hJc hn3
      · intro x hx
        have hxlt : x < 100 := by
          have hle : x ≤ B := Nat.lt_succ_iff.mp (hIB x hx)
          rcases hIA x hx with rfl | rfl | rfl | ⟨k, hk, rfl⟩
          · omega
          · omega
          · omega
          · obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
            have := hundred_pow_ge_hundred m
            omega
        exact base_elem_cases (hIA x hx) hxlt
      · intro y hy
        have hylt : y < 100 := by
          have hle : y ≤ B := Nat.lt_succ_iff.mp (hJB y hy)
          rcases hJA y hy with rfl | rfl | rfl | ⟨k, hk, rfl⟩
          · omega
          · omega
          · omega
          · obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
            have := hundred_pow_ge_hundred m
            omega
        exact base_elem_cases (hJA y hy) hylt
      · exact hsum
    · by_cases hBI : B ∈ I <;> by_cases hBJ : B ∈ J
      · have hIc' : (I.erase B).card = n := by
          have hcons : (I.erase B).card + 1 = I.card := by
            rw [← Multiset.card_cons, Multiset.cons_erase hBI]
          omega
        have hJc' : (J.erase B).card = n := by
          have hcons : (J.erase B).card + 1 = J.card := by
            rw [← Multiset.card_cons, Multiset.cons_erase hBJ]
          omega
        have hIA' : ∀ x ∈ I.erase B, x ∈ infModernWitness :=
          fun x hx => hIA x (Multiset.mem_of_mem_erase hx)
        have hJA' : ∀ y ∈ J.erase B, y ∈ infModernWitness :=
          fun y hy => hJA y (Multiset.mem_of_mem_erase hy)
        have hIB' : ∀ x ∈ I.erase B, x < B + 1 :=
          fun x hx => hIB x (Multiset.mem_of_mem_erase hx)
        have hJB' : ∀ y ∈ J.erase B, y < B + 1 :=
          fun y hy => hJB y (Multiset.mem_of_mem_erase hy)
        have hsumI : B + (I.erase B).sum = I.sum := by
          rw [← Multiset.sum_cons, Multiset.cons_erase hBI]
        have hsumJ : B + (J.erase B).sum = J.sum := by
          rw [← Multiset.sum_cons, Multiset.cons_erase hBJ]
        have hsum' : (I.erase B).sum = (J.erase B).sum := by omega
        have heq := modern_sum_inj n (B + 1) (I.erase B) (J.erase B)
          hIc' hJc' (by omega) hIA' hJA' hIB' hJB' hsum'
        rw [← Multiset.cons_erase hBI, ← Multiset.cons_erase hBJ, heq]
      · have hBA : B ∈ infModernWitness := hIA B hBI
        obtain ⟨k, rfl⟩ : ∃ k, B = 100 ^ (k + 1) := by
          rcases hBA with rfl | rfl | rfl | ⟨m, hm, rfl⟩
          · omega
          · omega
          · omega
          · exact ⟨m - 1, by obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩; rfl⟩
        have hJB' : ∀ y ∈ J, y < 100 ^ (k + 1) := by
          intro y hy
          have hne : y ≠ 100 ^ (k + 1) := fun h => hBJ (h ▸ hy)
          have hlt := hJB y hy
          omega
        have hJlt : J.sum < 100 ^ (k + 1) :=
          multiset_sum_lt_tail (by omega) hJA hJB'
        have hsumI : 100 ^ (k + 1) + (I.erase (100 ^ (k + 1))).sum = I.sum := by
          rw [← Multiset.sum_cons, Multiset.cons_erase hBI]
        omega
      · have hBA : B ∈ infModernWitness := hJA B hBJ
        obtain ⟨k, rfl⟩ : ∃ k, B = 100 ^ (k + 1) := by
          rcases hBA with rfl | rfl | rfl | ⟨m, hm, rfl⟩
          · omega
          · omega
          · omega
          · exact ⟨m - 1, by obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩; rfl⟩
        have hIB' : ∀ x ∈ I, x < 100 ^ (k + 1) := by
          intro x hx
          have hne : x ≠ 100 ^ (k + 1) := fun h => hBI (h ▸ hx)
          have hlt := hIB x hx
          omega
        have hIlt : I.sum < 100 ^ (k + 1) :=
          multiset_sum_lt_tail (by omega) hIA hIB'
        have hsumJ : 100 ^ (k + 1) + (J.erase (100 ^ (k + 1))).sum = J.sum := by
          rw [← Multiset.sum_cons, Multiset.cons_erase hBJ]
        omega
      · have hIB' : ∀ x ∈ I, x < B := by
          intro x hx
          have hne : x ≠ B := fun h => hBI (h ▸ hx)
          have hlt := hIB x hx
          omega
        have hJB' : ∀ y ∈ J, y < B := by
          intro y hy
          have hne : y ≠ B := fun h => hBJ (h ▸ hy)
          have hlt := hJB y hy
          omega
        exact modern_sum_inj (n + 1) B I J hIc hJc hn3 hIA hJA hIB' hJB' hsum

theorem infModernWitness_modernB3 : ModernB3 infModernWitness := by
  intro I J hIA hJA hIc hJc hsum
  apply modern_sum_inj 3 (I.sum + J.sum + 1) I J hIc hJc (by decide) hIA hJA
  · intro x hx
    have hle : x ≤ I.sum := Multiset.le_sum_of_mem hx
    omega
  · intro y hy
    have hle : y ≤ J.sum := Multiset.le_sum_of_mem hy
    omega
  · exact hsum

theorem infModernWitness_weakFixed3 : WeakFixed3 infModernWitness :=
  modern_implies_fixed infModernWitness infModernWitness_modernB3

theorem infModernWitness_not_historicalB3 : ¬ HistoricalB3 infModernWitness := by
  intro h
  let I : Finset ℕ := {1, 4}
  let J : Finset ℕ := {5}
  have hIA : (↑I : Set ℕ) ⊆ infModernWitness := by
    intro x hx
    simp only [I, Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact Or.inl rfl
    · exact Or.inr (Or.inl rfl)
  have hJA : (↑J : Set ℕ) ⊆ infModernWitness := by
    intro x hx
    simp only [J, Finset.coe_singleton, Set.mem_singleton_iff] at hx
    subst hx
    exact Or.inr (Or.inr (Or.inl rfl))
  have hIJ : I = J := h I J hIA hJA (by decide) (by decide) (by decide) (by decide) (by decide)
  have hmem : (1 : ℕ) ∈ J := hIJ ▸ (by decide : (1 : ℕ) ∈ I)
  exact (by decide : (1 : ℕ) ∉ J) hmem

/-!
## Exported Infinite Incomparability Theorems and Historical Statement Specification
-/

/-- There exists an infinite set `A ⊆ ℕ` satisfying `HistoricalB3 A` and `WeakFixed3 A`, but not `ModernB3 A`. -/
theorem exists_infinite_historicalB3_not_modernB3 :
    ∃ A : Set ℕ, A.Infinite ∧ HistoricalB3 A ∧ WeakFixed3 A ∧ ¬ ModernB3 A :=
  ⟨infSuperincreasing, infSuperincreasing_infinite, infSuperincreasing_historicalB3,
   infSuperincreasing_weakFixed3, infSuperincreasing_not_modernB3⟩

/-- There exists an infinite set `A ⊆ ℕ` satisfying `ModernB3 A` and `WeakFixed3 A`, but not `HistoricalB3 A`. -/
theorem exists_infinite_modernB3_not_historicalB3 :
    ∃ A : Set ℕ, A.Infinite ∧ ModernB3 A ∧ WeakFixed3 A ∧ ¬ HistoricalB3 A :=
  ⟨infModernWitness, infModernWitness_infinite, infModernWitness_modernB3,
   infModernWitness_weakFixed3, infModernWitness_not_historicalB3⟩

/-- Neither `HistoricalB3` nor `ModernB3` implies the other on infinite subsets of `ℕ`. -/
theorem not_historicalB3_implies_modernB3_infinite :
    ¬ (∀ A : Set ℕ, A.Infinite → HistoricalB3 A → ModernB3 A) := by
  intro h
  exact infSuperincreasing_not_modernB3 (h infSuperincreasing infSuperincreasing_infinite infSuperincreasing_historicalB3)

theorem not_modernB3_implies_historicalB3_infinite :
    ¬ (∀ A : Set ℕ, A.Infinite → ModernB3 A → HistoricalB3 A) := by
  intro h
  exact infModernWitness_not_historicalB3 (h infModernWitness infModernWitness_infinite infModernWitness_modernB3)

/--
Parameterized Formal Conjectures statement shapes for Erdős #41 (`Q A` represents the
open asymptotic density conclusion `liminf_{N → ∞} |A ∩ [1, N]| / N^{1/3} = 0`, kept abstract
here as `Q : Set ℕ → Prop` so no unproved conjecture axiom is introduced):
- `Erdos41HistoricalStatement Q` (`erdos_41.variants.historical_b3`): hypothesis `HistoricalB3 A`
- `Erdos41ModernStatement Q` (`erdos_41`): hypothesis `ModernB3 A` (`NtupleCondition A 3`)
- `Erdos41FrozenFixed3Statement Q`: hypothesis `WeakFixed3 A`
-/
def Erdos41HistoricalStatement (Q : Set ℕ → Prop) : Prop :=
  ∀ A : Set ℕ, HistoricalB3 A → A.Infinite → Q A

def Erdos41ModernStatement (Q : Set ℕ → Prop) : Prop :=
  ∀ A : Set ℕ, ModernB3 A → A.Infinite → Q A

def Erdos41FrozenFixed3Statement (Q : Set ℕ → Prop) : Prop :=
  ∀ A : Set ℕ, WeakFixed3 A → A.Infinite → Q A

/--
The frozen fixed-triple statement implies both the historical statement and the modern statement,
because `HistoricalB3 A → WeakFixed3 A` and `ModernB3 A → WeakFixed3 A`.
-/
theorem frozen_statement_implies_historical_and_modern (Q : Set ℕ → Prop)
    (h : Erdos41FrozenFixed3Statement Q) :
    Erdos41HistoricalStatement Q ∧ Erdos41ModernStatement Q :=
  ⟨fun A hH hInf => h A (historical_implies_fixed A hH) hInf,
   fun A hM hInf => h A (modern_implies_fixed A hM) hInf⟩

/--
However, the historical statement does NOT generically imply the modern statement across
predicates `Q : Set ℕ → Prop` (witnessed by `Q := HistoricalB3` on `infModernWitness`),
and the modern statement does NOT generically imply the historical statement (witnessed by
`Q := ModernB3` on `infSuperincreasing`).
-/
theorem historical_statement_not_implies_modern_statement :
    ¬ (∀ Q : Set ℕ → Prop, Erdos41HistoricalStatement Q → Erdos41ModernStatement Q) := by
  intro h
  have hMod : Erdos41ModernStatement HistoricalB3 := h HistoricalB3 (fun _ hH _ => hH)
  exact infModernWitness_not_historicalB3
    (hMod infModernWitness infModernWitness_modernB3 infModernWitness_infinite)

theorem modern_statement_not_implies_historical_statement :
    ¬ (∀ Q : Set ℕ → Prop, Erdos41ModernStatement Q → Erdos41HistoricalStatement Q) := by
  intro h
  have hHist : Erdos41HistoricalStatement ModernB3 := h ModernB3 (fun _ hM _ => hM)
  exact infSuperincreasing_not_modernB3
    (hHist infSuperincreasing infSuperincreasing_historicalB3 infSuperincreasing_infinite)

#print axioms historical_implies_fixed
#print axioms modern_implies_fixed
#print axioms exists_infinite_historicalB3_not_modernB3
#print axioms exists_infinite_modernB3_not_historicalB3
#print axioms not_weakFixed3_implies_historicalB3
#print axioms not_weakFixed3_implies_modernB3
#print axioms historical_statement_not_implies_modern_statement
#print axioms modern_statement_not_implies_historical_statement

end Erdos41HistoricalMathlibBridge
