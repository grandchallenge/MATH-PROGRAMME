/-
GCL provenance note

This formalization is adapted from:
  irregular-rhomboid/log-gcd-lean
  commit d2038c7b09fe849f236d6428d7159b5a40f9aed7
  file Loggcd/Lean/loggcd.lean
  upstream Git blob fd5b136ed32c6d48f5f71381ccf4b69d1329088f

The upstream repository is dedicated under CC0-1.0. The mathematical proof and
Lean term structure are preserved; package/module naming and this provenance
header are GCL integration changes.

The theorem states positive semidefiniteness, not strict positive definiteness.
-/

import Mathlib

open Finset ArithmeticFunction

/-
  The kernel K(m, n) = log (gcd m n) is positive semidefinite
  (equivalently, a positive-definite kernel in the RKHS / Moore-Aronszajn
  convention: every finite Gram matrix is positive semidefinite).

  Proof (von Mangoldt / complete the square):
    log n = ∑_{d ∣ n} Λ d
    Λ d ≥ 0
  hence, for a, b ≥ 1,
    log gcd(a,b) = ∑_d Λ d · [d∣a] · [d∣b],
  and therefore
    ∑_{i,j} c_i c_j · log gcd(x_i, x_j)
      = ∑_d Λ d · (∑_i c_i · [d ∣ x_i])² ≥ 0.

  The GCL fixture replays this file in CI against the pinned Lean/mathlib
  toolchain recorded beside it.
-/

variable {ι : Type*} [Fintype ι]

theorem logGcd_posSemidef
    (x : ι → ℕ) (hx : ∀ i, 1 ≤ x i) (c : ι → ℝ) :
    0 ≤ ∑ i, ∑ j, c i * c j * Real.log (Nat.gcd (x i) (x j)) := by
  classical
  -- A common divisor pool: the divisors of the product of all the xᵢ.
  set P : ℕ := ∏ i, x i with hP
  have hPne : P ≠ 0 := by
    rw [hP, Finset.prod_ne_zero_iff]
    exact fun i _ => Nat.one_le_iff_ne_zero.mp (hx i)
  -- The 0/1 real indicator "does d divide xₖ".
  set f : ℕ → ι → ℝ := fun d k => if d ∣ x k then (1 : ℝ) else 0 with hf
  -- Step 1: rewrite each log-gcd as a von-Mangoldt-weighted product of features.
  have key : ∀ i j,
      Real.log (Nat.gcd (x i) (x j))
        = ∑ d ∈ P.divisors, Λ d * f d i * f d j := by
    intro i j
    have hg : Nat.gcd (x i) (x j) ≠ 0 := by
      rw [Ne, Nat.gcd_eq_zero_iff]
      rintro ⟨h, _⟩
      have hxi_ne : (x i) ≠ 0 := (Nat.one_le_iff_ne_zero.mp (hx i))
      have hxj_ne : (x j) ≠ 0 := (Nat.one_le_iff_ne_zero.mp (hx j))
      exact hxi_ne h
      --omega
    have hsub : (Nat.gcd (x i) (x j)).divisors ⊆ P.divisors :=
      Nat.divisors_subset_of_dvd hPne
        ((Nat.gcd_dvd_left _ _).trans (Finset.dvd_prod_of_mem x (Finset.mem_univ i)))
    -- On the divisors of the gcd, both indicators equal 1.
    have hgcd : ∀ d ∈ (Nat.gcd (x i) (x j)).divisors, Λ d = Λ d * f d i * f d j := by
      intro d hd
      rw [Nat.mem_divisors] at hd
      have hdi : d ∣ x i := hd.1.trans (Nat.gcd_dvd_left _ _)
      have hdj : d ∣ x j := hd.1.trans (Nat.gcd_dvd_right _ _)
      simp [hf, hdi, hdj]
    -- Off the divisors of the gcd, at least one indicator is 0.
    have hvanish : ∀ d ∈ P.divisors, d ∉ (Nat.gcd (x i) (x j)).divisors →
        Λ d * f d i * f d j = 0 := by
      intro d _ hd
      rw [Nat.mem_divisors, not_and] at hd
      have hnd : ¬ d ∣ Nat.gcd (x i) (x j) := fun h => hd h hg
      have hnab : ¬ (d ∣ x i ∧ d ∣ x j) := fun h => hnd (Nat.dvd_gcd h.1 h.2)
      rcases not_and_or.mp hnab with h | h <;> simp [hf, h]
    rw [show Real.log (Nat.gcd (x i) (x j))
            = ∑ d ∈ (Nat.gcd (x i) (x j)).divisors, Λ d from vonMangoldt_sum.symm,
        Finset.sum_congr rfl hgcd, Finset.sum_subset hsub hvanish]
  -- Step 2: substitute, interchange sums, and complete the square.
  have hswap :
      ∑ i, ∑ j, c i * c j * Real.log (Nat.gcd (x i) (x j))
        = ∑ d ∈ P.divisors, Λ d * (∑ i, c i * f d i) ^ 2 := by
    simp_rw [key]
    calc
      ∑ i, ∑ j, c i * c j * ∑ d ∈ P.divisors, Λ d * f d i * f d j
          = ∑ i, ∑ j, ∑ d ∈ P.divisors, c i * c j * (Λ d * f d i * f d j) := by
            simp_rw [Finset.mul_sum]
        _ = ∑ i, ∑ d ∈ P.divisors, ∑ j, c i * c j * (Λ d * f d i * f d j) :=
            Finset.sum_congr rfl (fun i _ => Finset.sum_comm)
        _ = ∑ d ∈ P.divisors, ∑ i, ∑ j, c i * c j * (Λ d * f d i * f d j) :=
            Finset.sum_comm
        _ = ∑ d ∈ P.divisors, Λ d * (∑ i, c i * f d i) ^ 2 := by
            refine Finset.sum_congr rfl (fun d _ => ?_)
            rw [sq, Finset.sum_mul_sum, Finset.mul_sum]
            refine Finset.sum_congr rfl (fun i _ => ?_)
            rw [Finset.mul_sum]
            exact Finset.sum_congr rfl (fun j _ => by ring)
  -- Step 3: Λ ≥ 0 and squares are ≥ 0.
  rw [hswap]
  exact Finset.sum_nonneg (fun d _ => mul_nonneg vonMangoldt_nonneg (sq_nonneg _))
