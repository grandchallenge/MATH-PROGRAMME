import CMDGCondensedCM4P2EE1
import Mathlib.Condensed.Discrete.Characterization
import Mathlib.CategoryTheory.Monoidal.Closed.Braided

/-!
# CMDG CM4-P2-E E2 — measure-side right Kan reconstruction

This fixture is separate from the certified E1 layer. It starts the E2 reconstruction by
identifying the P2-D continuous-function source as the filtered colimit of its finite quotients,
then prepares the objectwise nested locally-constant transport needed for the protected presheaf.

No E3 uniqueness statement or final comparison with `Condensed.profiniteSolid` is asserted here.
-/

namespace CMDG.CondensedCM4P2E.RightKanReconstruction

universe u

open CategoryTheory Limits Opposite

abbrev R := CMDG.CondensedCM4P2D.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule

/-- The coefficient condensed module whose underlying presheaf is the protected P2-D coefficient
presheaf. -/
noncomputable abbrev coefficientCondensed : CondensedMod.{u} R :=
  (CondensedMod.LocallyConstant.functor R).obj (ModuleCat.of R R)

lemma coefficientCondensed_mem_locallyConstant :
    (CondensedMod.LocallyConstant.functor R).essImage coefficientCondensed :=
  ⟨ModuleCat.of R R, ⟨Iso.refl _⟩⟩

/-- The protected continuous-function module on a profinite set is the filtered colimit of the
continuous-function modules on its canonical finite quotients. This is the module-valued form of
the pinned discrete-object characterization. -/
noncomputable def continuousFunctionsIsColimit (S : Profinite.{u}) :
    IsColimit
      (CMDG.CondensedCM4P2D.continuousFunctions.mapCocone S.asLimitCone.op) := by
  have h :=
    ((CondensedMod.isDiscrete_tfae R coefficientCondensed).out 3 6).mp
      coefficientCondensed_mem_locallyConstant
  change IsColimit
    ((profiniteToCompHaus.op ⋙ coefficientCondensed.obj).mapCocone S.asLimitCone.op)
  exact (h S).some

/-- The same finite-quotient colimit after applying the canonical locally-constant/discrete
condensed-module functor. The cocone is written as an explicit mapped cocone so no associativity
transport is hidden in the statement. -/
noncomputable def discreteContinuousCondensedMappedIsColimit (S : Profinite.{u}) :
    IsColimit
      ((CondensedMod.LocallyConstant.functor R).mapCocone
        (CMDG.CondensedCM4P2D.continuousFunctions.mapCocone S.asLimitCone.op)) := by
  letI : (CondensedMod.LocallyConstant.functor R).IsLeftAdjoint :=
    (CondensedMod.LocallyConstant.adjunction R).isLeftAdjoint
  exact isColimitOfPreserves
    (CondensedMod.LocallyConstant.functor R)
    (continuousFunctionsIsColimit S)

/-- Transpose two compact variables of a nested locally-constant function. Compactness of the
outer variable makes the range finite; after factoring through that finite range, the pinned
`LocallyConstant.unflip` construction performs the transpose without an infinite intersection of
open fibres. -/
noncomputable def locallyConstantSwap (T S : CompHaus.{u})
    (f : LocallyConstant T (LocallyConstant S R)) :
    LocallyConstant S (LocallyConstant T R) := by
  classical
  let A : Finset (LocallyConstant S R) := f.range_finite.toFinset
  let q : LocallyConstant T {g // g ∈ A} :=
    { toFun := fun t => ⟨f t, by simp [A]⟩
      isLocallyConstant := by
        apply IsLocallyConstant.desc
          (fun t => (⟨f t, by simp [A]⟩ : {g // g ∈ A}))
          (fun g => (g.1 : LocallyConstant S R))
        · simpa [Function.comp_def] using f.isLocallyConstant
        · exact Subtype.val_injective }
  let family : {g // g ∈ A} → LocallyConstant S R := fun g => g.1
  let transposedValues : LocallyConstant S ({g // g ∈ A} → R) :=
    LocallyConstant.unflip family
  exact transposedValues.map (fun values => q.map values)

@[simp]
lemma locallyConstantSwap_apply (T S : CompHaus.{u})
    (f : LocallyConstant T (LocallyConstant S R)) (s : S) (t : T) :
    locallyConstantSwap T S f s t = f t s := by
  classical
  rfl

/-- The transpose is linear in the coefficient module and involutive. -/
noncomputable def locallyConstantSwapLinearEquiv (T S : CompHaus.{u}) :
    LocallyConstant T (LocallyConstant S R) ≃ₗ[R]
      LocallyConstant S (LocallyConstant T R) where
  toFun := locallyConstantSwap T S
  invFun := locallyConstantSwap S T
  left_inv f := by
    ext t s
    rw [locallyConstantSwap_apply, locallyConstantSwap_apply]
  right_inv f := by
    ext s t
    rw [locallyConstantSwap_apply, locallyConstantSwap_apply]
  map_add' f g := by
    apply LocallyConstant.ext
    intro s
    apply LocallyConstant.ext
    intro t
    change f t s + g t s =
      locallyConstantSwap T S f s t + locallyConstantSwap T S g s t
    rw [locallyConstantSwap_apply, locallyConstantSwap_apply]
  map_smul' r f := by
    apply LocallyConstant.ext
    intro s
    apply LocallyConstant.ext
    intro t
    change r • f t s = r • locallyConstantSwap T S f s t
    rw [locallyConstantSwap_apply]

#check continuousFunctionsIsColimit
#check discreteContinuousCondensedMappedIsColimit
#check locallyConstantSwap
#check locallyConstantSwapLinearEquiv

#print axioms continuousFunctionsIsColimit
#print axioms discreteContinuousCondensedMappedIsColimit
#print axioms locallyConstantSwap
#print axioms locallyConstantSwapLinearEquiv

end CMDG.CondensedCM4P2E.RightKanReconstruction
