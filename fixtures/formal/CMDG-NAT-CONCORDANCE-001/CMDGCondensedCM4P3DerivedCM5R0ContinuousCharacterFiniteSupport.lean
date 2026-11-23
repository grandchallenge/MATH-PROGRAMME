import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Connected.TotallyDisconnected
import Mathlib.Topology.Instances.Int
import Mathlib.Topology.ContinuousMap.Algebra
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

open Filter Topology
open scoped Topology

/-!
# CMDG CM5 continuous characters and integer products

For any index type I, every genuine continuous additive homomorphism
(I→ℝ)→ₜ+ℤ and (I→UnitAddCircle)→ₜ+ℤ is zero, by
path-connectedness of arbitrary products and discreteness of ℤ.

For the product of discrete integer factors (I→ℤ), continuity
of any additive hom f:(I→ℤ)→ₜ+ℤ at zero forces its kernel to
contain a basic product neighbourhood of zero, which restricts
only finitely many coordinates. The resulting rigorous finite
support/finite-coordinate statement yields the *explicit*
formula f x = ∑ i∈S, f (Pi.single i (x i)) for a finite S.

This is the fundamental H⁰ continuous-character information
needed for the prospective derived real/circle-to-integers
computation. It does not assert derived functor identification,
vanishing of higher Ext, all-degree Breen–Deligne pseudocoherence,
or equality of the bidual evaluation with canonical solidification.
-/
noncomputable section
universe u
namespace CMDG.CM5R0.DerivedDegreeZero

variable (I : Type u)

theorem continuous_realProduct_to_integer_zero
    (f : (I → ℝ) →ₜ+ ℤ) :
    f = 0 := by
  apply ContinuousAddMonoidHom.ext
  intro x
  calc
    f x = f 0 :=
      (PreconnectedSpace.constant (α := I → ℝ) (f := fun x => f x) inferInstance
        f.continuous)
    _ = 0 := map_zero f

theorem continuous_integer_product_has_finite_support
    (f : (I → ℤ) →ₜ+ ℤ) :
    ∃ s : Finset I, ∀ x : I → ℤ,
      (∀ i ∈ s, x i = 0) → f x = 0 := by
  classical
  have hzero : ({0} : Set ℤ) ∈ 𝓝 (0:ℤ) := by simp
  have hker : (f ⁻¹' {0}) ∈ 𝓝 (0 : I → ℤ) := by
    simpa using f.continuous.continuousAt.preimage_mem_nhds
      (by simpa [map_zero] using hzero)
  rw [nhds_pi, Filter.mem_pi'] at hker
  obtain ⟨s,t,ht,hs⟩ := hker
  refine ⟨s, fun x hx => ?_⟩
  have hx' : x ∈ Set.pi (↑s) t := by
    intro i hi
    rw [hx i (Finset.mem_coe.mp hi)]
    exact mem_of_mem_nhds (ht i)
  exact (hs hx' : f x ∈ ({0} : Set ℤ))

theorem continuous_integer_product_determined_by_finitely_many_coordinates
    (f : (I → ℤ) →ₜ+ ℤ) :
    ∃ s : Finset I, ∀ x y : I → ℤ,
      (∀ i ∈ s, x i = y i) → f x = f y := by
  classical
  obtain ⟨s, hs⟩ := continuous_integer_product_has_finite_support I f
  refine ⟨s, fun x y hxy => ?_⟩
  have hz : f (x - y) = 0 := by
    apply hs
    intro i hi
    simp [hxy i hi]
  have hsub : f x - f y = 0 := by
    simpa only [map_sub] using hz
  exact sub_eq_zero.mp hsub

theorem continuous_circleProduct_to_integer_zero
    (f : (I → UnitAddCircle) →ₜ+ ℤ) :
    f = 0 := by
  apply ContinuousAddMonoidHom.ext
  intro x
  calc
    f x = f 0 :=
      (PreconnectedSpace.constant (α := I → UnitAddCircle)
        (f := fun x => f x) inferInstance f.continuous)
    _ = 0 := map_zero f

#print axioms continuous_integer_product_determined_by_finitely_many_coordinates
#print axioms continuous_circleProduct_to_integer_zero

theorem continuous_integer_product_finite_character_formula
    [DecidableEq I] (f : (I → ℤ) →ₜ+ ℤ) :
    ∃ s : Finset I, ∀ x : I → ℤ,
      f x = ∑ i ∈ s, f (Pi.single i (x i)) := by
  classical
  obtain ⟨s, hs⟩ :=
    continuous_integer_product_determined_by_finitely_many_coordinates I f
  refine ⟨s, fun x => ?_⟩
  have heq :
      f x = f (∑ i ∈ s, Pi.single i (x i)) := by
    apply hs
    intro i hi
    simpa only [Finset.sum_apply, Finset.sum_pi_single, if_pos hi]
  simpa only [map_sum] using heq

#print axioms continuous_integer_product_finite_character_formula

#print axioms continuous_integer_product_has_finite_support

#print axioms continuous_realProduct_to_integer_zero
end CMDG.CM5R0.DerivedDegreeZero
