import CMDGCondensedCM4P3DerivedCM5R0ContinuousCharacterFiniteSupport
import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Topology.Algebra.Monoid


/-!
# CMDG CM5: finite-support classification of continuous integer-product characters

Starting from parent all-index finite-support theorem, construct
finitaryCharacter : (I→₀ℤ) → ((I→ℤ)→ₜ+ℤ)
by an actual finite sum with a continuous additive-hom proof.

Construct its inverse characterCoefficients from the kernel's
finite-coordinate annihilation neighbourhood via Classical.choose
and Finsupp.onFinset. Prove both inverse laws, the underlying
coordinate formulas, and unique character determination by
basis values; conclude a genuine Equiv for arbitrary I.

This is an equivalence of the underlying **sets** of
continuous additive characters and finitely supported integer
families. It is NOT yet an AddEquiv or derived/internal Hom
identification. The equivalence is not substituted for an
all-degree Breen–Deligne resolution or Ext vanishing theorem.
-/
noncomputable section
universe u
open Filter Topology
namespace CMDG.CM5R0.DerivedDegreeZero

variable (I : Type u)

def finitaryCharacter (a : I →₀ ℤ) : (I → ℤ) →ₜ+ ℤ where
  toFun x := ∑ i ∈ a.support, a i * x i
  map_zero' := by
    simp
  map_add' x y := by
    simp only [Pi.add_apply, mul_add, Finset.sum_add_distrib]
  continuous_toFun := by
    apply continuous_finsetSum
    intro i hi
    exact continuous_const.mul (continuous_apply i)

noncomputable def characterCoefficients (f : (I→ℤ)→ₜ+ℤ) : I →₀ ℤ := by
  classical
  let s := Classical.choose (continuous_integer_product_has_finite_support I f)
  have hs := Classical.choose_spec (continuous_integer_product_has_finite_support I f)
  refine Finsupp.onFinset s (fun i => f (Pi.single i 1)) ?_
  intro i hi
  by_contra hn
  apply hi
  apply hs
  intro j hj
  have hne : j ≠ i := by
    intro h
    subst i
    exact hn hj
  simp [hne]

theorem characterCoefficients_apply (f : (I→ℤ)→ₜ+ℤ) (i : I)
    [DecidableEq I] :
    characterCoefficients I f i = f (Pi.single i 1) := by
  unfold characterCoefficients
  simp only [Finsupp.onFinset_apply]
  congr 1
  funext j
  simp [Pi.single_apply]

#print axioms characterCoefficients_apply

theorem coefficients_of_finitaryCharacter (a : I →₀ ℤ)
    [DecidableEq I] :
    characterCoefficients I (finitaryCharacter I a) = a := by
  classical
  ext i
  rw [characterCoefficients_apply]
  change (∑ j ∈ a.support, a j * ((Pi.single i (1:ℤ) : I → ℤ) j)) = a i
  simp only [Pi.single_apply]
  simp [mul_ite, mul_one, mul_zero, Finset.sum_ite_eq',
    Finsupp.mem_support_iff]
  exact fun h => h.symm

#print axioms coefficients_of_finitaryCharacter

private theorem integer_single_as_smul [DecidableEq I] (i : I) (z : ℤ) :
    (Pi.single i z : I → ℤ) = z • (Pi.single i (1:ℤ) : I → ℤ) := by
  ext j
  simp [Pi.single_apply, Pi.smul_apply, mul_ite]

private theorem integer_character_single (f : (I → ℤ)→ₜ+ℤ)
    [DecidableEq I] (i : I) (z : ℤ) :
    f (Pi.single i z) = z * f (Pi.single i 1) := by
  rw [integer_single_as_smul I i z, map_zsmul]
  simp

#print axioms integer_character_single

private theorem integer_character_sum_on_support [DecidableEq I]
    (f : (I→ℤ)→ₜ+ℤ) (s : Finset I)
    (hs : ∀ x : I→ℤ, (∀ i ∈ s, x i = 0) → f x = 0)
    (x : I→ℤ) :
    f x = ∑ i ∈ s, f (Pi.single i (x i)) := by
  have hrest :
      f (x - ∑ i ∈ s, Pi.single i (x i)) = 0 := by
    apply hs
    intro i hi
    simp [Finset.sum_apply, Finset.sum_pi_single, hi]
  have heq : f x = f (∑ i ∈ s, Pi.single i (x i)) := by
    apply sub_eq_zero.mp
    simpa only [map_sub] using hrest
  simpa only [map_sum] using heq

theorem continuous_integer_character_ext_on_basis [DecidableEq I]
    (f g : (I→ℤ)→ₜ+ℤ)
    (heq : ∀ i : I, f (Pi.single i 1) = g (Pi.single i 1)) :
    f = g := by
  classical
  obtain ⟨sf, hsf⟩ := continuous_integer_product_has_finite_support I f
  obtain ⟨sg, hsg⟩ := continuous_integer_product_has_finite_support I g
  let s : Finset I := sf ∪ sg
  have hf (x : I→ℤ) (hx : ∀ i ∈ s, x i=0) : f x=0 := by
    apply hsf x
    intro i hi
    exact hx i (Finset.mem_union_left sg hi)
  have hg (x : I→ℤ) (hx : ∀ i ∈ s, x i=0) : g x=0 := by
    apply hsg x
    intro i hi
    exact hx i (Finset.mem_union_right sf hi)
  apply ContinuousAddMonoidHom.ext
  intro x
  calc
    f x = ∑ i ∈ s, f (Pi.single i (x i)) :=
      integer_character_sum_on_support I f s hf x
    _ = ∑ i ∈ s, g (Pi.single i (x i)) := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [integer_character_single I f i (x i),
        integer_character_single I g i (x i), heq i]
    _ = g x := (integer_character_sum_on_support I g s hg x).symm

theorem finitaryCharacter_of_coefficients [DecidableEq I]
    (f : (I→ℤ)→ₜ+ℤ) :
    finitaryCharacter I (characterCoefficients I f) = f := by
  apply continuous_integer_character_ext_on_basis I
  intro i
  have hc := congrArg (fun a : I→₀ℤ => a i)
    (coefficients_of_finitaryCharacter I (characterCoefficients I f))
  rw [characterCoefficients_apply] at hc
  exact hc.trans (characterCoefficients_apply I f i)

noncomputable def continuousIntegerCharacterEquiv [DecidableEq I] :
    (I →₀ ℤ) ≃ ((I → ℤ) →ₜ+ ℤ) where
  toFun := finitaryCharacter I
  invFun := characterCoefficients I
  left_inv := fun a => coefficients_of_finitaryCharacter I a
  right_inv := fun f => finitaryCharacter_of_coefficients I f

#print axioms continuous_integer_character_ext_on_basis
#print axioms finitaryCharacter_of_coefficients
#print axioms continuousIntegerCharacterEquiv

#print axioms finitaryCharacter
end CMDG.CM5R0.DerivedDegreeZero
