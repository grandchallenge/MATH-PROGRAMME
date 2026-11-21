import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Tactic

/-!
# CMDG CM5: genuine circle-product real-lift and nonsplitting obstruction

For any compact Hausdorff abelian group A, every continuous additive
homomorphism A → ℝ is zero, by a compact-image bound on iterated sums.
For the actual circle T=ℝ/ℤ, the point [1/2] is proved nonzero and
2-torsion. Therefore even abstract additive sections of ℝ → T
cannot exist. More strongly, for any index set I and coordinate i,
there is no abstract additive lift T^I → ℝ of the i-th projection,
and when I is nonempty there is no additive section ℝ^I → T^I.
The corresponding continuous nonsplitting is also checked directly.

This is a genuine lower-class obstruction: it supports a nonzero
canonical circle-to-integer extension class ONCE the topological
0→ℤ→ℝ→T→0 sequence has been identified with an exact extension
in the true condensed abelian category. It does NOT itself construct
a Yoneda Ext class or prove the all-degree derived computation
RHom(T^I,ℤ) ≃ ⊕_I ℤ[-1], nor identify the solidification unit.
-/

noncomputable section
universe u
namespace CMDG.CondensedCM5R0.CircleRealObstruction

variable {A : Type u} [TopologicalSpace A] [CompactSpace A] [AddCommGroup A]

theorem compact_to_real_zero (f : A →+ ℝ)
    (hf : Continuous (f : A → ℝ)) : f = 0 := by
  let F : C(A, ℝ) := ⟨f,hf⟩
  apply AddMonoidHom.ext
  intro a
  by_contra hn
  have hpos : 0 < |f a| := abs_pos.mpr hn
  obtain ⟨n, hn'⟩ := exists_nat_gt (‖F‖ / |f a|)
  have hbound : |F (n • a)| ≤ ‖F‖ := by
    simpa only [Real.norm_eq_abs] using F.norm_coe_le_norm (n • a)
  change |f (n • a)| ≤ ‖F‖ at hbound
  have hmul : f (n • a) = (n:ℝ) * f a := by
    rw [map_nsmul, nsmul_eq_mul]
  rw [hmul, abs_mul, abs_of_nonneg (Nat.cast_nonneg n)] at hbound
  have hle : (n : ℝ) ≤ ‖F‖ / |f a| :=
    (le_div_iff₀ hpos).2 (by nlinarith [hbound])
  exact (not_lt_of_ge hle) hn'

theorem halfCircle_nonzero : ((1/2 : ℝ) : UnitAddCircle) ≠ 0 := by
  intro h
  obtain ⟨n, hn⟩ := (AddCircle.coe_eq_zero_iff (p := (1 : ℝ))).mp h
  have hn' : (n : ℝ) = 1/2 := by
    simpa [zsmul_eq_mul] using hn
  have heq : 2 * (n : ℝ) = 1 := by linarith
  have heq' : 2 * n = 1 := by exact_mod_cast heq
  omega

theorem circle_quotient_has_no_continuous_additive_section
    (s : UnitAddCircle →+ ℝ)
    (hs : Continuous (s : UnitAddCircle → ℝ))
    (hsec : ∀ x : UnitAddCircle, (s x : UnitAddCircle) = x) : False := by
  have hz : s = 0 := compact_to_real_zero s hs
  have h := hsec ((1/2 : ℝ) : UnitAddCircle)
  have hzero : ((1/2 : ℝ) : UnitAddCircle) = 0 := by
    simpa [hz] using h.symm
  exact halfCircle_nonzero hzero

theorem circleTorus_product_no_continuous_additive_section
    {I : Type u} [Nonempty I]
    (s : (I → UnitAddCircle) →+ (I → ℝ))
    (hs : Continuous (s : (I → UnitAddCircle) → (I → ℝ)))
    (hsec : ∀ x : I → UnitAddCircle,
      ∀ i : I, ((s x) i : UnitAddCircle) = x i) : False := by
  classical
  let i : I := Classical.choice ‹Nonempty I›
  let fi : (I → UnitAddCircle) →+ ℝ := {
    toFun := fun x => (s x) i
    map_zero' := by simp
    map_add' := by intros; simp }
  have hfi : Continuous (fi : (I → UnitAddCircle) → ℝ) := by
    change Continuous (fun x : I → UnitAddCircle => s x i)
    exact (continuous_apply i).comp hs
  have hz : fi = 0 := compact_to_real_zero fi hfi
  let x : I → UnitAddCircle := fun _ => ((1/2 : ℝ) : UnitAddCircle)
  have h := hsec x i
  have hzero : (s x) i = 0 := by
    have hx : fi x = 0 := by simp [hz]
    change (s x) i = 0 at hx
    exact hx
  rw [hzero] at h
  exact halfCircle_nonzero h.symm

#print axioms circleTorus_product_no_continuous_additive_section

/-- Stronger than topological non-splitting: torsion obstructs even
an *abstract group* section of the real-to-circle quotient. -/
theorem circle_quotient_no_additive_section
    (s : UnitAddCircle →+ ℝ)
    (hsec : ∀ x : UnitAddCircle, (s x : UnitAddCircle) = x) : False := by
  let x : UnitAddCircle := ((1/2 : ℝ) : UnitAddCircle)
  have h2 : (2:ℕ) • x = 0 := by
    dsimp [x]
    rw [← AddCircle.coe_nsmul]
    norm_num
  have hreal : (2:ℕ) • s x = 0 := by
    rw [← map_nsmul, h2, map_zero]
  have hzero : s x = 0 := by
    rw [two_nsmul] at hreal
    linarith
  have hx : x = 0 := by
    have h := hsec x
    simpa [hzero] using h.symm
  exact halfCircle_nonzero hx

#print axioms circle_quotient_no_additive_section

/-- For any nonempty index set, the product real-to-circle quotient
does not split even as an abstract additive-group homomorphism. -/
theorem circleTorus_product_no_additive_section
    {I : Type u} [Nonempty I]
    (s : (I → UnitAddCircle) →+ (I → ℝ))
    (hsec : ∀ x : I → UnitAddCircle,
      ∀ i : I, ((s x) i : UnitAddCircle) = x i) : False := by
  classical
  let i : I := Classical.choice ‹Nonempty I›
  let x : I → UnitAddCircle := fun _ => ((1/2 : ℝ) : UnitAddCircle)
  have h2 : (2:ℕ) • x = 0 := by
    funext j
    change (2:ℕ) • ((1/2:ℝ): UnitAddCircle) = 0
    rw [← AddCircle.coe_nsmul]
    norm_num
  have hreal : (2:ℕ) • (s x) = 0 := by
    rw [← map_nsmul, h2, map_zero]
  have hzero : (s x) i = 0 := by
    have hi := congrArg (fun y : I → ℝ => y i) hreal
    change (2:ℕ) • ((s x) i) = 0 at hi
    rw [two_nsmul] at hi
    linarith
  have h := hsec x i
  rw [hzero] at h
  exact halfCircle_nonzero h.symm

#print axioms circleTorus_product_no_additive_section

/-- Every individual coordinate projection from a product circle has no
abstract additive lift to ℝ. This is the precise nonsplitting obstruction
for the canonical degree-one class indexed by i. -/
theorem circleTorus_coordinate_no_additive_lift
    {I : Type u} (i : I)
    (s : (I → UnitAddCircle) →+ ℝ)
    (hsec : ∀ x : I → UnitAddCircle,
      ((s x : ℝ) : UnitAddCircle) = x i) : False := by
  classical
  let x : I → UnitAddCircle :=
    fun j => if j = i then ((1/2:ℝ):UnitAddCircle) else 0
  have h2 : (2:ℕ) • x = 0 := by
    funext j
    simp only [Pi.smul_apply, Pi.zero_apply]
    by_cases hij : j = i
    · subst j
      simp only [x, if_pos rfl]
      rw [← AddCircle.coe_nsmul]
      norm_num
    · simp [x, hij]
  have hreal : (2:ℕ) • s x = 0 := by
    rw [← map_nsmul,h2,map_zero]
  have hzero : s x = 0 := by
    rw [two_nsmul] at hreal
    linarith
  have h := hsec x
  have hh : ((1/2 : ℝ) : UnitAddCircle) = 0 := by
    rw [hzero] at h
    simpa only [x, if_pos rfl, AddCircle.coe_zero] using h.symm
  exact halfCircle_nonzero hh

#print axioms circleTorus_coordinate_no_additive_lift

#print axioms compact_to_real_zero
#print axioms circle_quotient_has_no_continuous_additive_section
end CMDG.CondensedCM5R0.CircleRealObstruction
