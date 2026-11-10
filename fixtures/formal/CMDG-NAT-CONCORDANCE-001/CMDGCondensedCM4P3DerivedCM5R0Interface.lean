import CMDGCondensedCM4Blocker
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic

/-!
# CMDG CM5-R0: exact degree-zero derived-category interface

This is a bounded interface test for the next CM5 research gate, compiled in the
already registered CMDG CM4-P3 formal lane for pinned environment continuity.

* R0-A: the exact universe-lifted integer condensed-module category is abelian.
* R0-B: the protected CM4 object embeds as an object of the derived category in
  cohomological degree zero.
* R0-C/R0-D/R0-E remain open: no derived-solid predicate, source-semantics
  comparison, or derived locality/Ext vanishing theorem is asserted here.

No new axioms, sorry, local postulates, or claimed derived solidities.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- Coefficients are precisely the lifted integers used by protected CM4. -/
abbrev Coeff : Type (u + 1) := CMDG.CondensedCM4.ZLift.{u}

/-- Exact abelian category in which the CM4 object lives. -/
abbrev Ambient := CondensedMod.{u} Coeff

#synth CategoryTheory.Abelian Ambient
#check CategoryTheory.HasExt
#check CategoryTheory.DerivedCategory.singleFunctor

/-- The protected underived CM4 profinite-solid object. -/
def underivedObject (S : Profinite.{u}) : Ambient :=
  (Condensed.profiniteSolid Coeff).obj S

/-- Reuse of the already protected *underived* theorem only. -/
theorem underivedObject_isSolid (S : Profinite.{u}) :
    CondensedMod.IsSolid Coeff (underivedObject S) :=
  CMDG.CondensedCM4.cm4Target_via_pointFunctional S

/-- Degree-zero image under the ordinary derived-category embedding.
This construction does not imply derived solidity. -/
def degreeZeroObject (S : Profinite.{u}) :
    CategoryTheory.DerivedCategory Ambient :=
  (CategoryTheory.DerivedCategory.singleFunctor Ambient 0).obj (underivedObject S)

#check underivedObject
#check underivedObject_isSolid
#check degreeZeroObject

end CMDG.CondensedCM5R0
