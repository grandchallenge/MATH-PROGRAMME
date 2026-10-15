import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Arithmetic receipts for density-conditioned localized outer B3 differences.
Universal B3/Sidon injectivity and infinite density hypotheses are proved
or bounded in CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md and are NOT end-to-end
formalized in Lean here. -/
namespace GCLErdos41.LocalOuterDifferences

theorem interbin_ordered_pair_lower
    (m largest within : ℚ)
    (hm : 0 ≤ m)
    (hl : largest ≤ m/2)
    (hw : within ≤ m*largest) :
    m^2-within ≥ m^2/2 := by
  have h := mul_nonneg hm (sub_nonneg.mpr hl)
  nlinarith

theorem positive_difference_mass_coefficient (c jInv : ℚ) :
    ((c*jInv/2)^2)/4 = c^2*jInv^2/16 := by ring

theorem one_third_minus_five_eighteenths :
    (1:ℚ)/3-5/18=1/18 := by norm_num

theorem two_thirds_from_square :
    ((2:ℚ)/3)=2*(1/3) := by ring

end GCLErdos41.LocalOuterDifferences
