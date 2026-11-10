import CMDGCondensedCM4P3DerivedCM5R0Interface

/-!
# CMDG CM5-R0: derived Hom comparison candidate

This module constructs the exact degree-zero solidification map and its
precomposition maps on morphisms in the standard derived category.

The candidate predicate quantifies over every profinite test object and integer
shift. This is an interface **proposal**, not a certified source-to-formal
definition of derived solidity. In particular, there is no proof that these
comparison functions are bijective.

No sorry, axiom, derived-locality proof, Ext vanishing, or global theorem.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

/-- Ordinary free condensed module, embedded in cohomological degree zero. -/
def freeAtZero (T : Profinite.{u}) : DerivedCategory Ambient :=
  (DerivedCategory.singleFunctor Ambient 0).obj
    ((Condensed.profiniteFree Coeff).obj T)

/-- The derived-category image of the *underived* solidification morphism.
It is not asserted to be an isomorphism. -/
def solidificationAtZero (T : Profinite.{u}) :
    freeAtZero T ⟶ degreeZeroObject T :=
  (DerivedCategory.singleFunctor Ambient 0).map
    ((Condensed.profiniteSolidification Coeff).app T)

/-- Precomposition with solidification on morphisms at a specified shift.
No bijectivity assertion is made. -/
def comparisonAtShift (S T : Profinite.{u}) (n : ℤ) :
    (((shiftFunctor (DerivedCategory Ambient) n).obj (degreeZeroObject T)) ⟶
      degreeZeroObject S) →
    (((shiftFunctor (DerivedCategory Ambient) n).obj (freeAtZero T)) ⟶
      degreeZeroObject S) :=
  fun f => (shiftFunctor (DerivedCategory Ambient) n).map (solidificationAtZero T) ≫ f

/-- Candidate condition for all profinite probes and integer shifts.
Source-semantic equivalence with derived solidity remains to be established. -/
def ShiftedComparisonBijectiveCandidate (S : Profinite.{u}) : Prop :=
  ∀ (T : Profinite.{u}) (n : ℤ),
    Function.Bijective (comparisonAtShift S T n)

#check freeAtZero
#check solidificationAtZero
#check comparisonAtShift
#check ShiftedComparisonBijectiveCandidate

end CMDG.CondensedCM5R0
