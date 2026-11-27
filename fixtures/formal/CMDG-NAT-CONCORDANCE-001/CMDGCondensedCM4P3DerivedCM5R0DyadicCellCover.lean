import CMDGCondensedCM4P3DerivedCM5R0OrderedGridFinBridge
import CMDGCondensedCM4P3DerivedCM5R0CompactCoverFiniteCoordinates
import Mathlib.Analysis.Real.OfDigits

/-! Actual closed dyadic cells of the positional binary expansion cover.
Both binary expansions of a boundary point are retained. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic

abbrev Bits := ℕ → Fin 2
abbrev Interval := Set.Icc (0 : ℝ) 1

def prefixIndex : ℕ → Bits → ℕ
  | 0, _ => 0
  | m+1, a => 2 * prefixIndex m a + (a m).val

theorem prefix_lt (m : ℕ) (a : Bits) : prefixIndex m a < 2^m := by
  induction m with
  | zero => simp [prefixIndex]
  | succ m ih =>
    have h := (a m).isLt
    simp only [prefixIndex,pow_succ]
    omega

theorem prefix_congr (m : ℕ) (a b : Bits) (h : ∀ j < m, a j = b j) :
    prefixIndex m a = prefixIndex m b := by
  induction m with
  | zero => rfl
  | succ m ih =>
    simp only [prefixIndex,ih (fun j hj => h j (by omega)),h m (by omega)]

theorem prefix_injective_on_digits (m : ℕ) (a b : Bits) (h : prefixIndex m a = prefixIndex m b) :
    ∀ j < m, a j = b j := by
  induction m with
  | zero => omega
  | succ m ih =>
    have ha := (a m).isLt
    have hb := (b m).isLt
    simp only [prefixIndex] at h
    intro j hj
    by_cases he : j = m
    · subst j
      apply Fin.ext
      omega
    · exact ih (by omega) j (by omega)

theorem prefix_surj (m k : ℕ) (hk : k < 2^m) : ∃ a : Bits, prefixIndex m a = k := by
  induction m generalizing k with
  | zero =>
    refine ⟨fun _ => 0, ?_⟩
    simp only [prefixIndex]
    simp at hk
    omega
  | succ m ih =>
    have hq : k/2 < 2^m := by rw [pow_succ] at hk; omega
    obtain ⟨a,ha⟩ := ih (k/2) hq
    let b : Bits := fun j => if j=m then ⟨k%2,by omega⟩ else a j
    refine ⟨b,?_⟩
    have hpre : prefixIndex m b = prefixIndex m a := by
      apply prefix_congr
      intro j hj
      simp [b,show j ≠ m by omega]
    simp only [prefixIndex,hpre,ha,b,if_pos]
    omega

theorem prefix_continuous (m : ℕ) : Continuous (prefixIndex m) := by
  induction m with
  | zero => exact continuous_const
  | succ m ih =>
    exact (continuous_const.mul ih).add
      ((continuous_of_discreteTopology : Continuous (Fin.val : Fin 2 → ℕ)).comp (continuous_apply m))

def value (a : Bits) : Interval :=
  ⟨Real.ofDigits a, Real.ofDigits_nonneg a, Real.ofDigits_le_one a⟩

theorem value_continuous : Continuous value :=
  Continuous.subtype_mk Real.continuous_ofDigits _

theorem value_surj : Function.Surjective value := by
  intro x
  obtain ⟨a,_,ha⟩ := Real.ofDigits_SurjOn (b:=2) (by decide) x.property
  exact ⟨a,Subtype.ext ha⟩

theorem prefix_sum (m : ℕ) (a : Bits) :
    (∑ j ∈ Finset.range m, Real.ofDigitsTerm a j) =
      (prefixIndex m a : ℝ) / (2 : ℝ)^m := by
  induction m with
  | zero => simp [prefixIndex]
  | succ m ih =>
    rw [Finset.sum_range_succ,ih]
    simp only [Real.ofDigitsTerm,prefixIndex,Nat.cast_add,Nat.cast_mul,Nat.cast_ofNat,pow_succ]
    have h : (2 : ℝ)^m ≠ 0 := by positivity
    field_simp

theorem value_eq_prefix_tail (m : ℕ) (a : Bits) :
    (value a : ℝ) = ((prefixIndex m a : ℝ) + Real.ofDigits (fun j => a (j+m))) / (2 : ℝ)^m := by
  change Real.ofDigits a = _
  rw [Real.ofDigits_eq_sum_add_ofDigits a m,prefix_sum]
  ring

def cell (m k : ℕ) : Set ℝ :=
  Set.Icc ((k : ℝ)/(2 : ℝ)^m) (((k : ℝ)+1)/(2 : ℝ)^m)

theorem value_mem_cell (m : ℕ) (a : Bits) :
    (value a : ℝ) ∈ cell m (prefixIndex m a) := by
  rw [value_eq_prefix_tail]
  constructor
  · apply div_le_div_of_nonneg_right _ (by positivity)
    linarith [Real.ofDigits_nonneg (fun j => a (j+m))]
  · apply div_le_div_of_nonneg_right _ (by positivity)
    linarith [Real.ofDigits_le_one (fun j => a (j+m))]

/-- The image of a full binary cylinder is its entire CLOSED cell,
including both endpoints. -/
theorem cell_lift (m k : ℕ) (hk : k < 2^m) (x : ℝ) (hx : x ∈ cell m k) :
    ∃ a : Bits, prefixIndex m a = k ∧ (value a : ℝ) = x := by
  obtain ⟨b,hb⟩ := prefix_surj m k hk
  have hp : (0 : ℝ) < 2^m := by positivity
  let t : ℝ := x * 2^m - k
  have ht : t ∈ Set.Icc (0:ℝ) 1 := by
    constructor
    · have h := (div_le_iff₀ hp).mp hx.1
      dsimp [t]; linarith
    · have h := (le_div_iff₀ hp).mp hx.2
      dsimp [t]; linarith
  obtain ⟨a,_,ha⟩ := Real.ofDigits_SurjOn (b:=2) (by decide) ht
  let z : Bits := fun j => if j < m then b j else a (j-m)
  have hz : prefixIndex m z = k := (prefix_congr m z b (by intro j hj; simp [z,hj])).trans hb
  refine ⟨z,hz,?_⟩
  rw [value_eq_prefix_tail,hz]
  have htail : (fun j => z (j+m)) = a := by
    funext j
    simp [z,show ¬j+m<m by omega]
  rw [htail,ha]
  dsimp [t]
  field_simp
  ; ring

#print axioms prefix_injective_on_digits
#print axioms prefix_continuous
#print axioms cell_lift
end CMDG.CondensedCM5R0.CompactCover.Dyadic
