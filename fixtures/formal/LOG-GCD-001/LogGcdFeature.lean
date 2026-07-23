import LogGcd

open Finset ArithmeticFunction

/-!
# A finitely supported feature map for the logarithmic GCD kernel

For a positive natural number `n`, the coordinate indexed by `d` is

`Real.sqrt (Λ d)` when `d ∣ n`, and zero otherwise.

The feature vector is represented by `ℕ →₀ ℝ`, so finite support is part of the
type rather than an external convergence obligation. Its canonical finite dot
product recovers `Real.log (Nat.gcd m n)` exactly.
-/

/-- The divisor feature vector for the logarithmic GCD kernel. -/
noncomputable def logGcdFeature (n : ℕ) : ℕ →₀ ℝ :=
  Finsupp.indicator n.divisors fun d _ => Real.sqrt (Λ d)

@[simp]
theorem logGcdFeature_apply (n d : ℕ) :
    logGcdFeature n d = if d ∈ n.divisors then Real.sqrt (Λ d) else 0 := by
  classical
  simp [logGcdFeature]

/-- The canonical finite dot product on real-valued finitely supported functions. -/
def finsuppDot (u v : ℕ →₀ ℝ) : ℝ :=
  ∑ d ∈ u.support, u d * v d

/-- A finitely supported vector has nonnegative squared dot norm. -/
theorem finsuppDot_self_nonneg (u : ℕ →₀ ℝ) : 0 ≤ finsuppDot u u := by
  classical
  unfold finsuppDot
  exact Finset.sum_nonneg fun d _ => mul_self_nonneg (u d)

/-- The logarithmic GCD kernel is exactly the Gram kernel of `logGcdFeature`. -/
theorem logGcd_eq_feature_inner
    (m n : ℕ) (hm : m ≠ 0) (hn : n ≠ 0) :
    finsuppDot (logGcdFeature m) (logGcdFeature n) =
      Real.log (Nat.gcd m n) := by
  classical
  have hg : Nat.gcd m n ≠ 0 := by
    rw [Ne, Nat.gcd_eq_zero_iff]
    rintro ⟨h, _⟩
    exact hm h
  have hsupp : (logGcdFeature m).support ⊆ m.divisors := by
    intro d hd
    by_contra hnot
    have hzero : logGcdFeature m d = 0 := by
      simp [logGcdFeature_apply, hnot]
    have hne : logGcdFeature m d ≠ 0 := by
      simpa using hd
    exact hne hzero
  have hsupp_zero : ∀ d ∈ m.divisors, d ∉ (logGcdFeature m).support →
      logGcdFeature m d * logGcdFeature n d = 0 := by
    intro d _ hd
    have hzero : logGcdFeature m d = 0 := by
      simpa using hd
    simp [hzero]
  have hsub : (Nat.gcd m n).divisors ⊆ m.divisors :=
    Nat.divisors_subset_of_dvd hm (Nat.gcd_dvd_left _ _)
  have h_on : ∀ d ∈ (Nat.gcd m n).divisors,
      Real.sqrt (Λ d) * logGcdFeature n d = Λ d := by
    intro d hd
    have hdivg : d ∣ Nat.gcd m n := (Nat.mem_divisors.mp hd).1
    have hdivn : d ∣ n := hdivg.trans (Nat.gcd_dvd_right _ _)
    have hdn : d ∈ n.divisors := Nat.mem_divisors.mpr ⟨hdivn, hn⟩
    rw [logGcdFeature_apply, if_pos hdn]
    simpa [pow_two] using (Real.sq_sqrt (vonMangoldt_nonneg : 0 ≤ Λ d))
  have h_off : ∀ d ∈ m.divisors, d ∉ (Nat.gcd m n).divisors →
      Real.sqrt (Λ d) * logGcdFeature n d = 0 := by
    intro d hdm hdg
    have hdivm : d ∣ m := (Nat.mem_divisors.mp hdm).1
    have hnotn : ¬ d ∣ n := by
      intro hdivn
      exact hdg (Nat.mem_divisors.mpr ⟨Nat.dvd_gcd hdivm hdivn, hg⟩)
    simp [logGcdFeature_apply, Nat.mem_divisors, hnotn]
  calc
    finsuppDot (logGcdFeature m) (logGcdFeature n)
        = ∑ d ∈ m.divisors, logGcdFeature m d * logGcdFeature n d := by
            unfold finsuppDot
            exact Finset.sum_subset hsupp hsupp_zero
    _ = ∑ d ∈ m.divisors, Real.sqrt (Λ d) * logGcdFeature n d := by
          exact Finset.sum_congr rfl fun d hd => by
            rw [logGcdFeature_apply, if_pos hd]
    _ = ∑ d ∈ (Nat.gcd m n).divisors, Λ d := by
          rw [← Finset.sum_subset hsub h_off]
          exact Finset.sum_congr rfl h_on
    _ = Real.log (Nat.gcd m n) := vonMangoldt_sum

/-- The squared feature norm is `log n`. -/
theorem logGcdFeature_self
    (n : ℕ) (hn : n ≠ 0) :
    finsuppDot (logGcdFeature n) (logGcdFeature n) = Real.log n := by
  simpa using logGcd_eq_feature_inner n n hn hn

/-- The original positive-semidefinite theorem remains available from the feature module. -/
theorem logGcd_posSemidef_feature_corollary
    {ι : Type*} [Fintype ι]
    (x : ι → ℕ) (hx : ∀ i, 1 ≤ x i) (c : ι → ℝ) :
    0 ≤ ∑ i, ∑ j, c i * c j * Real.log (Nat.gcd (x i) (x j)) :=
  logGcd_posSemidef x hx c
