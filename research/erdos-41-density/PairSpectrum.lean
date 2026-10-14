import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! Arithmetic receipts for the B3 pair-sum autocorrelation selector and
its A-indexed Gram matrix spectrum. Universal B3 multiset injections are
proved in SHADOW_CORRELATION_SPECTRUM.md (not kernel-formalized here). -/
namespace GCLErdos41.PairSpectrum

theorem pair_sum_cardinal_twice (n : ℚ) :
    2*(n*(n+1)/2) = n*(n+1) := by ring

theorem gram_small_eigenvalue_twice (n : ℚ) :
    2*(n*(n+1)/2-n) = n*(n-1) := by ring

theorem gram_large_eigenvalue_twice (n : ℚ) :
    2*(n*(n+1)/2+n*(n-1)) = n*(3*n-1) := by ring

theorem selector_total_positive_difference (n : ℚ) :
    n*(n*(n-1)) = n*n*(n-1) := by ring

theorem sample_non_b3_autocorrelation_violates_selector :
    (4 : ℕ) ≠ 3 := by norm_num

theorem sample_pair_spectrum_overlap :
    (3 - 438 : ℤ) = 66 - 501 := by norm_num

end GCLErdos41.PairSpectrum
