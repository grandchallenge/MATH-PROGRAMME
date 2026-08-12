import CMDGCondensedCM4P3D
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.CofilteredLimit

/-!
# CMDG CM4-P3-F — coefficient-object solidity

This successor isolates the single coefficient-object residual left by P3-E.
The first certified layer identifies the lower Hom set with locally constant
lifted-integer-valued functions on the profinite source. Later layers will
construct the finite-quotient lift and isolate the remaining mapping-out
injectivity theorem. No coefficient solidity or P3 availability is asserted
by this file unless and until those terminal declarations are proved.
-/

namespace CMDG.CondensedCM4P3F

universe u

open CategoryTheory Opposite

abbrev R := CMDG.CondensedCM4P3D.R.{u}

noncomputable abbrev coefficientObject : CondensedMod.{u} R :=
  CMDG.CondensedCM4P3D.coefficientObject.{u}

/-- The free-forgetful half of the lower-Hom identification. -/
noncomputable def lowerHomAdjunctionEquiv (X : Profinite.{u}) :
    (((Condensed.profiniteFree R).obj X ⟶ coefficientObject) ≃
      (X.toCondensed ⟶ (Condensed.forget R).obj coefficientObject)) :=
  (Condensed.freeForgetAdjunction R).homEquiv _ _

/-- The represented condensed-set Hom is exactly a section of the underlying
coefficient sheaf at `X`, hence a locally constant `R`-valued function. -/
noncomputable def lowerHomYonedaEquiv (X : Profinite.{u}) :
    ((X.toCondensed ⟶ (Condensed.forget R).obj coefficientObject) ≃
      LocallyConstant X R) := by
  change
    (((coherentTopology CompHaus.{u}).uliftYoneda.obj
          (profiniteToCompHaus.obj X) ⟶
        (Condensed.forget R).obj coefficientObject) ≃
      ((Condensed.forget R).obj coefficientObject).obj.obj
        (op (profiniteToCompHaus.obj X)))
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv

/-- FIRST: exact lower-Hom equivalence. -/
noncomputable def lowerHomEquiv (X : Profinite.{u}) :
    (((Condensed.profiniteFree R).obj X ⟶ coefficientObject) ≃
      LocallyConstant X R) :=
  (lowerHomAdjunctionEquiv X).trans (lowerHomYonedaEquiv X)

#check lowerHomAdjunctionEquiv
#check lowerHomYonedaEquiv
#check lowerHomEquiv

#print axioms lowerHomAdjunctionEquiv
#print axioms lowerHomYonedaEquiv
#print axioms lowerHomEquiv

end CMDG.CondensedCM4P3F
