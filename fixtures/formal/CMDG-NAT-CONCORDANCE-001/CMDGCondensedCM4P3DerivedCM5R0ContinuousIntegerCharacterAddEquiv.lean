import CMDGCondensedCM4P3DerivedCM5R0ContinuousIntegerCharacterEquiv


/-!
# CMDG CM5: additive classification of continuous integer-product characters

The previously proved all-index continuous character Finsupp equivalence
is an actual equivalence of additive groups, not merely a bijection:
(I→₀ℤ) ≃+ ((I→ℤ)→ₜ+ℤ). Prove the character on each unit
coordinate basis, the additivity of the finite-sum character map,
and construct the final AddEquiv. Only standard Lean axioms.

This compares the underlying groups of continuous additive
homomorphisms; it is not an internal CondensedAb derived Hom
comparison, nor a higher Ext or BD pseudocoherence proof.
-/

noncomputable section
universe u
namespace CMDG.CM5R0.DerivedDegreeZero

variable (I : Type u) [DecidableEq I]

theorem finitaryCharacter_basis (a : I →₀ ℤ) (i : I) :
    finitaryCharacter I a (Pi.single i 1) = a i := by
  have h := congrArg (fun z : I →₀ ℤ => z i)
    (coefficients_of_finitaryCharacter I a)
  rw [characterCoefficients_apply] at h
  exact h

theorem finitaryCharacter_add (a b : I →₀ ℤ) :
    finitaryCharacter I (a + b) =
      finitaryCharacter I a + finitaryCharacter I b := by
  apply continuous_integer_character_ext_on_basis I
  intro i
  rw [finitaryCharacter_basis, ContinuousAddMonoidHom.add_apply,
    finitaryCharacter_basis, finitaryCharacter_basis, Finsupp.add_apply]

noncomputable def continuousIntegerCharacterAddEquiv :
    (I →₀ ℤ) ≃+ ((I → ℤ) →ₜ+ ℤ) where
  toEquiv := continuousIntegerCharacterEquiv I
  map_add' := fun a b => finitaryCharacter_add I a b

#print axioms continuousIntegerCharacterAddEquiv
end CMDG.CM5R0.DerivedDegreeZero
