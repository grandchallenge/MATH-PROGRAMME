import CMDGCondensedCM4P3DerivedCM5R0ContinuousIntegerCharacterAddEquiv
import Mathlib.Data.Finsupp.Basic


/-!
# CMDG CM5 canonical coordinate naturality of integer-product characters

Under the genuine topological-product continuous-character AddEquiv,
the pullback of a continuous character along ANY reindexing
u:J→I corresponds to the algebraic pushforward
Finsupp.mapDomain u : (J→₀ℤ)→(I→₀ℤ).
No injectivity/surjectivity restriction on u: noninjective
indices correctly sum colliding finite-support coefficients.

The statements and naturality proof are true in the actual
ContinuousAddMonoidHom API for arbitrary products. All arguments
are independent of finite I. This is an ordinary continuous-group
duality input for eventual evaluation-unit identification; it
is NOT an all-degree derived/internal-Hom comparison.
-/
noncomputable section
universe u v
namespace CMDG.CM5R0.DerivedDegreeZero

variable (I : Type u) (J : Type v)

def coordinatePullback (u : J → I) : (I → ℤ) →ₜ+ (J → ℤ) where
  toFun x := fun j => x (u j)
  map_zero' := rfl
  map_add' x y := rfl
  continuous_toFun := continuous_pi (fun j => continuous_apply (u j))

theorem finitaryCharacter_mapDomain (u : J → I)
    (a : J →₀ ℤ) (x : I → ℤ) :
    finitaryCharacter I (a.mapDomain u) x =
      finitaryCharacter J a (coordinatePullback I J u x) := by
  change (a.mapDomain u).sum (fun i c => c * x i) =
    a.sum (fun j c => c * x (u j))
  apply Finsupp.sum_mapDomain_index
  · intro i
    simp
  · intro i c d
    simp [add_mul]

def characterPullback (u : J → I) :
    ((J → ℤ) →ₜ+ ℤ) →+ ((I → ℤ) →ₜ+ ℤ) where
  toFun f := f.comp (coordinatePullback I J u)
  map_zero' := by
    apply ContinuousAddMonoidHom.ext
    intro x
    rfl
  map_add' f g := by
    apply ContinuousAddMonoidHom.ext
    intro x
    rfl

theorem continuousIntegerCharacterAddEquiv_naturality
    [DecidableEq I] [DecidableEq J] (u : J → I) (a : J →₀ ℤ) :
    (continuousIntegerCharacterAddEquiv I) (a.mapDomain u) =
      characterPullback I J u ((continuousIntegerCharacterAddEquiv J) a) := by
  apply ContinuousAddMonoidHom.ext
  intro x
  exact finitaryCharacter_mapDomain I J u a x

theorem characterCoefficients_mapDomain
    [DecidableEq I] [DecidableEq J]
    (u : J → I) (f : (J → ℤ) →ₜ+ ℤ) :
    characterCoefficients I (characterPullback I J u f) =
      (characterCoefficients J f).mapDomain u := by
  apply (continuousIntegerCharacterAddEquiv I).injective
  calc
    (continuousIntegerCharacterAddEquiv I)
      (characterCoefficients I (characterPullback I J u f)) =
      characterPullback I J u f := by
        exact (continuousIntegerCharacterAddEquiv I).apply_symm_apply _
    _ = characterPullback I J u
      ((continuousIntegerCharacterAddEquiv J) (characterCoefficients J f)) := by
      exact congrArg (characterPullback I J u)
        (finitaryCharacter_of_coefficients J f).symm
    _ = (continuousIntegerCharacterAddEquiv I)
      ((characterCoefficients J f).mapDomain u) := by
      exact (continuousIntegerCharacterAddEquiv_naturality I J u
        (characterCoefficients J f)).symm

#print axioms continuousIntegerCharacterAddEquiv_naturality
#print axioms characterCoefficients_mapDomain

#print axioms finitaryCharacter_mapDomain
end CMDG.CM5R0.DerivedDegreeZero
