import Mathlib.Data.Nat.Totient
import Mathlib.Analysis.SpecificLimits.Basic
import Lean.Elab.Tactic.Omega
import Mathlib.Tactic.NormNum

/-! Bounded formal witness tests for Erdős 249 (the open full totient series is NOT claimed). -/
namespace Erdos249Bounded

def exponent (m : ℕ) : ℕ := 2 ^ (m + 1) - m

theorem totient_two_succ (m : ℕ) :
    Nat.totient (2 ^ (m + 1)) = 2 ^ m := by
  simpa using Nat.totient_prime_pow_succ Nat.prime_two m

theorem two_pow_ge_succ (m : ℕ) : m + 1 ≤ 2 ^ m := by
  induction m with
  | zero => norm_num
  | succ m hm =>
    rw [pow_succ]
    omega

theorem exponent_succ (m : ℕ) :
    exponent (m + 1) = exponent m + (2 ^ (m + 1) - 1) := by
  unfold exponent
  rw [pow_succ]
  have h := two_pow_ge_succ (m + 1)
  omega

theorem exponent_strict (m : ℕ) :
    exponent m < exponent (m + 1) := by
  rw [exponent_succ]
  have h := two_pow_ge_succ (m + 1)
  omega

theorem exponent_gap (m : ℕ) :
    exponent (m + 1) - exponent m = 2 ^ (m + 1) - 1 := by
  rw [exponent_succ]
  omega

theorem exponent_ge_two (m : ℕ) : 2 ≤ exponent m := by
  induction m with
  | zero => norm_num [exponent]
  | succ m hm =>
    have h := exponent_strict m
    omega


theorem exponent_add_le (n k : ℕ) :
    exponent n + k ≤ exponent (n + k) := by
  induction k with
  | zero => simp
  | succ k ih =>
    have h := exponent_strict (n + k)
    have heq : n + (k + 1) = n + k + 1 := by omega
    rw [heq]
    omega

theorem exponent_ge_index (n : ℕ) : n ≤ exponent n := by
  induction n with
  | zero => simp [exponent]
  | succ n ih =>
    have hg := exponent_strict n
    omega

noncomputable def term (n : ℕ) : ℝ :=
  1 / (2 : ℝ) ^ exponent n

theorem summable_term : Summable term := by
  change Summable (fun i : ℕ => 1 / (2 : ℝ) ^ exponent i)
  exact (summable_one_div_pow_of_le (by norm_num : (1 : ℝ) < 2)
      exponent_ge_index)

noncomputable def partialSum (N : ℕ) : ℝ :=
  ∑ i ∈ Finset.range (N + 1), term i

theorem partialSum_succ (N : ℕ) :
    partialSum (N + 1) = partialSum N + term (N + 1) :=
  Finset.sum_range_succ _ _

noncomputable def remainder (N : ℕ) : ℝ :=
  ∑' i : ℕ, term (i + (N + 1))

theorem remainder_summable (N : ℕ) :
    Summable (fun i : ℕ => term (i + (N + 1))) :=
  (summable_nat_add_iff (N + 1)).2 summable_term

theorem remainder_pos (N : ℕ) : 0 < remainder N := by
  exact (remainder_summable N).tsum_pos (fun _ => by
    dsimp [term]; positivity) 0 (by dsimp [term]; positivity)

theorem partialSum_add_remainder (N : ℕ) :
    partialSum N + remainder N = ∑' i : ℕ, term i :=
  summable_term.sum_add_tsum_nat_add _


theorem remainder_le (N : ℕ) :
    remainder N ≤ 2 * (1 / (2 : ℝ) ^ exponent (N + 1)) := by
  have hgeo : Summable (fun i : ℕ => 1 / (2 : ℝ) ^ (exponent (N + 1) + i)) :=
    summable_one_div_pow_of_le (by norm_num) (fun i => by omega)
  calc
    remainder N ≤ ∑' i : ℕ, 1 / (2 : ℝ) ^ (exponent (N + 1) + i) := by
      dsimp [remainder]
      apply Summable.tsum_le_tsum
      · intro i
        dsimp [term]
        apply one_div_pow_le_one_div_pow_of_le (by norm_num : (1 : ℝ) ≤ 2)
        simpa only [Nat.add_comm] using (exponent_add_le (N + 1) i)
      · exact remainder_summable N
      · exact hgeo
    _ = ∑' i : ℕ, (1 / (2 : ℝ)) ^ i * (1 / (2 : ℝ) ^ exponent (N + 1)) := by
      congr 1
      funext i
      simp [pow_add, one_div, inv_pow, mul_comm]
    _ = (∑' i : ℕ, (1 / (2 : ℝ)) ^ i) *
        (1 / (2 : ℝ) ^ exponent (N + 1)) := by rw [tsum_mul_right]
    _ = 2 * (1 / (2 : ℝ) ^ exponent (N + 1)) := by
      rw [tsum_geometric_of_lt_one (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (1 : ℝ) / 2 < 1)]
      norm_num


theorem partialSum_eq_rat (N : ℕ) :
    ∃ A : ℕ, partialSum N = (A : ℝ) / (2 : ℝ) ^ exponent N := by
  induction N with
  | zero =>
    refine ⟨1, ?_⟩
    norm_num [partialSum, term, exponent]
  | succ N ih =>
    obtain ⟨A, hA⟩ := ih
    let δ : ℕ := exponent (N + 1) - exponent N
    have hgap : exponent N + δ = exponent (N + 1) := by
      dsimp [δ]
      have hh := exponent_strict N
      omega
    have hpow :
        (2 : ℝ) ^ exponent (N + 1) =
          (2 : ℝ) ^ exponent N * (2 : ℝ) ^ δ := by
      rw [← pow_add, hgap]
    refine ⟨A * 2 ^ δ + 1, ?_⟩
    rw [partialSum_succ, hA]
    dsimp [term]
    rw [hpow]
    push_cast
    field_simp


theorem gap_dominates_denominator (b : ℕ) :
    (b : ℝ) * 2 <
      (2 : ℝ) ^ (exponent (b + 2) - exponent (b + 1)) := by
  let N : ℕ := b + 1
  have hgap : N + 1 ≤ exponent (N + 1) - exponent N := by
    rw [exponent_gap]
    have h := two_pow_ge_succ (N + 1)
    omega
  have hbase := two_pow_ge_succ N
  have hlarge : 2 * b < 2 ^ (N + 1) := by
    rw [pow_succ]
    dsimp [N] at *
    omega
  have hmono : (2 : ℕ) ^ (N + 1) ≤
      (2 : ℕ) ^ (exponent (N + 1) - exponent N) := by
    gcongr
  have ht := lt_of_lt_of_le hlarge hmono
  change (b : ℝ) * 2 <
    (2 : ℝ) ^ (exponent (N + 1) - exponent N)
  have ht' : b * 2 < (2 : ℕ) ^ (exponent (N + 1) - exponent N) := by
    simpa only [Nat.mul_comm] using ht
  exact_mod_cast ht'


noncomputable def lacunary : ℝ :=
  ∑' i : ℕ, term i

theorem lacunary_not_rat :
    ¬ ∃ q : ℚ, (q : ℝ) = lacunary := by
  rintro ⟨q, hq⟩
  let b : ℕ := q.den
  let N : ℕ := b + 1
  have hb : 0 < b := q.den_pos
  have hbr : (0 : ℝ) < b := by exact_mod_cast hb
  obtain ⟨A, hA⟩ := partialSum_eq_rat N
  have hreal : (q : ℝ) = partialSum N + remainder N := by
    calc
      (q : ℝ) = lacunary := hq
      _ = partialSum N + remainder N := (partialSum_add_remainder N).symm
  have hcast : (q : ℝ) = (q.num : ℝ) / (b : ℝ) := by
    simpa only [b] using (Rat.cast_def (K := ℝ) q)
  have hrel :
      (q.num : ℝ) / (b : ℝ) =
        (A : ℝ) / (2 : ℝ) ^ exponent N + remainder N := by
    calc
      (q.num : ℝ) / (b : ℝ) = (q : ℝ) := hcast.symm
      _ = partialSum N + remainder N := hreal
      _ = _ := by rw [hA]
  let z : ℤ := q.num * (2 : ℤ) ^ exponent N - (b : ℤ) * (A : ℤ)
  have hz : (z : ℝ) = (b : ℝ) * (2 : ℝ) ^ exponent N * remainder N := by
    have hnum : (q.num : ℝ) =
      (b : ℝ) * ((A : ℝ) / (2 : ℝ) ^ exponent N + remainder N) := by
      calc
        (q.num : ℝ) =
            (q.num : ℝ) / (b : ℝ) * (b : ℝ) := by field_simp
        _ = _ := by rw [hrel]; ring
    dsimp [z]
    push_cast
    rw [hnum]
    field_simp
    ring
  have hgap : exponent N + (exponent (N + 1) - exponent N) =
      exponent (N + 1) := by
    have hh := exponent_strict N
    omega
  have hpow :
      (2 : ℝ) ^ exponent (N + 1) =
        (2 : ℝ) ^ exponent N *
          (2 : ℝ) ^ (exponent (N + 1) - exponent N) := by
    rw [← pow_add, hgap]
  have hden : (b : ℝ) * 2 <
      (2 : ℝ) ^ (exponent (N + 1) - exponent N) := by
    simpa only [N] using gap_dominates_denominator b
  have hsmall :
      (b : ℝ) * (2 : ℝ) ^ exponent N * remainder N < 1 := by
    have hupper := remainder_le N
    have hle :
        (b : ℝ) * (2 : ℝ) ^ exponent N * remainder N
          ≤ (b : ℝ) * 2 /
              (2 : ℝ) ^ (exponent (N + 1) - exponent N) := by
      calc
        (b : ℝ) * (2 : ℝ) ^ exponent N * remainder N
          ≤ (b : ℝ) * (2 : ℝ) ^ exponent N *
              (2 * (1 / (2 : ℝ) ^ exponent (N + 1))) :=
                mul_le_mul_of_nonneg_left hupper (by positivity)
        _ = _ := by rw [hpow]; field_simp
    have hpowpos : (0 : ℝ) <
      (2 : ℝ) ^ (exponent (N + 1) - exponent N) := by positivity
    exact hle.trans_lt ((div_lt_one hpowpos).mpr hden)
  have hpos : (0 : ℝ) < (z : ℝ) := by
    rw [hz]
    exact mul_pos (mul_pos hbr (by positivity)) (remainder_pos N)
  have hzi : 0 < z := by exact_mod_cast hpos
  have hge : (1 : ℝ) ≤ (z : ℝ) := by
    exact_mod_cast (show (1 : ℤ) ≤ z by omega)
  exact not_lt_of_ge hge (by simpa only [hz] using hsmall)


theorem term_eq_totient_fraction (m : ℕ) :
    term m = ((Nat.totient (2 ^ (m + 1)) : ℕ) : ℝ) /
      (2 : ℝ) ^ (2 ^ (m + 1)) := by
  have he : m + exponent m = 2 ^ (m + 1) := by
    unfold exponent
    have h := two_pow_ge_succ (m + 1)
    omega
  rw [totient_two_succ]
  dsimp [term]
  norm_cast
  rw [← he, pow_add]
  field_simp
  push_cast
  ring

theorem lacunary_eq_totient_subseries :
    lacunary =
      ∑' m : ℕ, ((Nat.totient (2 ^ (m + 1)) : ℕ) : ℝ) /
        (2 : ℝ) ^ (2 ^ (m + 1)) := by
  unfold lacunary
  congr 1
  funext m
  exact term_eq_totient_fraction m

theorem totient_subseries_not_rat :
    ¬ ∃ q : ℚ,
      (q : ℝ) =
        ∑' m : ℕ, ((Nat.totient (2 ^ (m + 1)) : ℕ) : ℝ) /
          (2 : ℝ) ^ (2 ^ (m + 1)) := by
  rw [← lacunary_eq_totient_subseries]
  exact lacunary_not_rat

theorem totient_subseries_irrational :
    (∑' m : ℕ, ((Nat.totient (2 ^ (m + 1)) : ℕ) : ℝ) /
        (2 : ℝ) ^ (2 ^ (m + 1))) ∉ Set.range ((↑) : ℚ → ℝ) := by
  rintro ⟨q, hq⟩
  exact totient_subseries_not_rat ⟨q, hq⟩

#check Erdos249Bounded.totient_subseries_irrational
#print axioms Erdos249Bounded.totient_subseries_irrational
#print axioms Erdos249Bounded.lacunary_not_rat
#print axioms Erdos249Bounded.totient_subseries_not_rat
#print axioms Erdos249Bounded.totient_two_succ
#print axioms Erdos249Bounded.exponent_succ
#print axioms Erdos249Bounded.exponent_strict
#print axioms Erdos249Bounded.exponent_gap
#print axioms Erdos249Bounded.exponent_ge_two

end Erdos249Bounded
