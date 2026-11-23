import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Tactic.NormNum


/-!
# CMDG CM5: the real–circle group extension is intrinsically non-split

On the actual additive circle ℝ/ℤ there is a nonzero order-two
class [1/2]. Any additive map into ℝ sends order-two elements
to zero, because ℝ is torsion-free. Therefore the standard
real→circle quotient cannot admit even a NONCONTINUOUS additive
section. The same obstruction persists in every nonempty
arbitrary product (ℝ/ℤ)^I→ℝ^I by choosing one coordinate.

These statements are verified in Lean with actual UnitAddCircle
and product group structures; no abstract Ext or non-splitting
axiom. In particular, do not infer nontrivial condensed Ext¹
without proving the bridge from categorical splitting to
componentwise ordinary-group splitting in the genuine CondensedAb
models. The complete derived comparison and canonical-unit
identity remain open.
-/
noncomputable section
namespace CMDG.CM5R0.NonSplit

theorem circle_half_ne_zero :
    (((1/2 : ℝ) : UnitAddCircle) ≠ 0) := by
  intro h
  have ha : (1/2 : ℝ) ∈ Set.Ico (0:ℝ) 1 := by norm_num
  have hz := (AddCircle.coe_eq_zero_iff_of_mem_Ico (p := (1:ℝ)) ha).mp h
  norm_num at hz

theorem circle_half_two_zero :
    (2:ℕ) • ((1/2 : ℝ) : UnitAddCircle) = 0 := by
  rw [← AddCircle.coe_nsmul]
  have hh : (2:ℕ) • (1/2:ℝ) = 1 := by norm_num [nsmul_eq_mul]
  rw [hh]
  rw [AddCircle.coe_eq_zero_iff]
  exact ⟨1, by simp⟩

theorem no_additive_circle_to_real_quotient_section
    (s : UnitAddCircle →+ ℝ)
    (hs : ∀ a : UnitAddCircle, ((s a : ℝ) : UnitAddCircle) = a) : False := by
  let a : UnitAddCircle := ((1/2:ℝ) : UnitAddCircle)
  have h2 : (2:ℕ) • s a = 0 := by
    rw [← map_nsmul, show (2:ℕ) • a = 0 from circle_half_two_zero]
    exact map_zero s
  have heq : s a + s a = 0 := by
    simpa [two_nsmul] using h2
  have hsa : s a = 0 := add_self_eq_zero.mp heq
  have ha : a = 0 := by
    rw [← hs a, hsa]
    simp
  exact circle_half_ne_zero ha

#print axioms no_additive_circle_to_real_quotient_section

universe u

theorem no_additive_product_realCircle_quotient_section
    (I : Type u) [Nonempty I]
    (s : (I → UnitAddCircle) →+ (I → ℝ))
    (hs : ∀ x : I → UnitAddCircle, ∀ i : I,
      ((s x i : ℝ) : UnitAddCircle) = x i) : False := by
  classical
  let i : I := Classical.choice ‹Nonempty I›
  let x : I → UnitAddCircle := Pi.single i ((1/2:ℝ):UnitAddCircle)
  have hx : (2:ℕ) • x = 0 := by
    ext j
    by_cases hj : j = i
    · subst j
      simpa [x, Pi.single_eq_same] using circle_half_two_zero
    · simp [x, hj, Pi.smul_apply]
  have h2 : (2:ℕ) • s x = 0 := by
    rw [← map_nsmul, hx, map_zero]
  have hi : (2:ℕ) • (s x i) = 0 := by
    have h := congrArg (fun y : I → ℝ => y i) h2
    simpa [Pi.smul_apply] using h
  have hz : s x i = 0 := add_self_eq_zero.mp (by simpa [two_nsmul] using hi)
  have hzero : x i = 0 := by rw [← hs x i, hz]; simp
  exact circle_half_ne_zero (by simpa [x, Pi.single_eq_same] using hzero)

#print axioms no_additive_product_realCircle_quotient_section

#print axioms circle_half_ne_zero
#print axioms circle_half_two_zero
end CMDG.CM5R0.NonSplit
