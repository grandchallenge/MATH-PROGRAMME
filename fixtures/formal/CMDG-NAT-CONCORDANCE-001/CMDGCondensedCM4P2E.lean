import CMDGCondensedCM4P2D
import Mathlib.Condensed.Solid
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Functor.KanExtension.Basic
import Mathlib.CategoryTheory.Functor.KanExtension.Pointwise
import Mathlib.LinearAlgebra.Finsupp.Pi
import Mathlib.Algebra.BigOperators.Pi

/-!
# CMDG CM4-P2-E comparison reconstruction

This fixture freezes the exact P2-E theorem target after protected admission of P2-D and develops
the basis-free finite algebraic duality core needed for the finite comparison.

No natural equivalence with `Condensed.profiniteSolid` is asserted until the finite condensed
comparison and the measure-side right-Kan-extension property are both constructed.
-/

namespace CMDG.CondensedCM4P2E

universe u

open CategoryTheory
open scoped BigOperators

/-- The exact lifted integral coefficient ring inherited from protected P2-D. -/
abbrev R := CMDG.CondensedCM4P2D.R

/-- The protected P2-D canonical measure/dual functor. -/
noncomputable abbrev measureFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  CMDG.CondensedCM4P2D.measureFunctor

/-- The pinned solid functor to which P2-E must compare the protected P2-D functor. -/
noncomputable abbrev solidFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  Condensed.profiniteSolid R

/-- Restriction of the protected measure/dual functor to finite profinite sets. -/
noncomputable abbrev finiteMeasure : FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  FintypeCat.toProfinite ⋙ measureFunctor

/-- The exact finite-free functor used by `Condensed.profiniteSolid`. -/
noncomputable abbrev finiteFree : FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  Condensed.finFree R

/-- The finite comparison that P2-E must construct canonically and naturally. -/
abbrev FiniteComparisonTarget := finiteMeasure ≅ finiteFree

/-- The final P2-E theorem target. -/
abbrev ComparisonTarget := measureFunctor ≅ solidFunctor

/-!
## E1 algebraic core

For a finite type `X`, the dual of the finite function module `X → R` is canonically the same
finite function module. The forward map evaluates a functional on the canonical delta functions;
the inverse is the finite dot product. This uses only the elements of `X` themselves as canonical
coordinates and makes no arbitrary basis choice.
-/

/-- Canonical self-duality of a finite function module, by delta evaluation and finite summation. -/
noncomputable def finiteFunctionDualEquiv (X : Type u) [Fintype X] :
    ((X → R) →ₗ[R] R) ≃ₗ[R] (X → R) where
  toFun φ := by
    classical
    exact fun x => φ (Pi.single x (1 : R))
  invFun a :=
    { toFun := fun h => ∑ x, h x * a x
      map_add' := by
        intro f g
        simp [add_mul, Finset.sum_add_distrib]
      map_smul' := by
        intro c f
        simp [Finset.mul_sum, mul_assoc] }
  left_inv φ := by
    classical
    apply LinearMap.ext
    intro h
    change (∑ x, h x * φ (Pi.single x (1 : R))) = φ h
    calc
      (∑ x, h x * φ (Pi.single x (1 : R))) =
          ∑ x, φ (h x • (Pi.single x (1 : R) : X → R)) := by
            apply Finset.sum_congr rfl
            intro x _
            simpa using (φ.map_smul (h x) (Pi.single x (1 : R) : X → R)).symm
      _ = φ (∑ x, h x • (Pi.single x (1 : R) : X → R)) := by
            rw [map_sum]
      _ = φ h := by
            rw [← pi_eq_sum_univ' h]
  right_inv a := by
    classical
    funext x
    change (∑ y, (Pi.single x (1 : R) : X → R) y * a y) = a x
    rw [Fintype.sum_eq_single x (fun y hy => by simp [Pi.single, hy])]
    simp
  map_add' φ ψ := by
    classical
    funext x
    simp
  map_smul' c φ := by
    classical
    funext x
    simp

/-- Canonical finite-free form of the algebraic dual, using finite-support/function equivalence. -/
noncomputable def finiteFunctionDualFreeEquiv (X : Type u) [Fintype X] :
    ((X → R) →ₗ[R] R) ≃ₗ[R] (X →₀ R) :=
  (finiteFunctionDualEquiv X).trans (Finsupp.linearEquivFunOnFinite R R X).symm

#check CMDG.CondensedCM4P2D.measureFunctor
#check CMDG.CondensedCM4P2D.dualityHomEquiv
#check finiteFunctionDualEquiv
#check finiteFunctionDualFreeEquiv
#check Condensed.finFree
#check Condensed.profiniteSolid
#check Condensed.profiniteSolidCounit
#check Condensed.profiniteSolidIsPointwiseRightKanExtension
#check Functor.rightKanExtensionUniqueOfIso
#check Functor.rightKanExtensionUnique
#check Condensed.isColimitLocallyConstantPresheafDiagram
#check Condensed.lanPresheafNatIso

#print axioms finiteFunctionDualEquiv
#print axioms finiteFunctionDualFreeEquiv

end CMDG.CondensedCM4P2E
