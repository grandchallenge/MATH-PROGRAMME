import CMDGCondensedCM4P3D
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Sites.Subcanonical

/-!
# CMDG CM4-P3-G — coefficient mapping-out attack

This fixture attacks the single coefficient-object residual left by protected P3-D.
It starts with the lower-Hom identification and the finite-stage right-Kan triangle.
No coefficient solidity or injectivity theorem is assumed.
-/

namespace CMDG.CondensedCM4P3G

universe u

open CategoryTheory Limits Opposite

/-- Exact lifted integral coefficient ring retained from protected CM4/P2/P3. -/
abbrev R := CMDG.CondensedCM4P3D.R.{u}

/-- The exact discrete coefficient object isolated by protected P3-D. -/
noncomputable abbrev coefficientObject : CondensedMod.{u} R :=
  CMDG.CondensedCM4P3D.coefficientObject.{u}

/-- The lower Hom set before applying the finite-quotient semantics of a discrete target. -/
abbrev LowerHom (X : Profinite.{u}) :=
  (Condensed.profiniteFree R).obj X ⟶ coefficientObject

/-- Sections of the underlying condensed set of the coefficient object at a profinite test object. -/
abbrev CoefficientSections (X : Profinite.{u}) :=
  ((Condensed.forget R).obj coefficientObject).obj.obj
    (op ((profiniteToCompHaus).obj X))

/-- Free-forget followed by represented sheaf evaluation. This is the exact categorical
interface behind the informal statement that maps from the free condensed module on `X`
to the discrete coefficient object are coefficient-valued locally constant functions on `X`. -/
noncomputable def lowerHomSectionsEquiv (X : Profinite.{u}) :
    LowerHom X ≃ CoefficientSections X := by
  change
    (((Condensed.free R).obj ((profiniteToCondensed).obj X) ⟶ coefficientObject) ≃
      CoefficientSections X)
  refine (Condensed.freeForgetAdjunction R).homEquiv.trans ?_
  change
    (((coherentTopology CompHaus.{u}).uliftYoneda.obj ((profiniteToCompHaus).obj X) ⟶
      (Condensed.forget R).obj coefficientObject) ≃ CoefficientSections X)
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv

/-- G0: the concrete lower-Hom equivalence. -/
noncomputable def lowerHomEquiv (X : Profinite.{u}) :
    LowerHom X ≃ LocallyConstant X R := by
  exact lowerHomSectionsEquiv X

/-- At a finite stage, solidification followed by the right-Kan counit is the identity.
This is the exact triangle needed to lift finite-quotient lower-Hom maps through
`profiniteSolidification`. -/
theorem finiteSolidification_counit (Q : FintypeCat.{u}) :
    (Condensed.profiniteSolidification R).app (FintypeCat.toProfinite.obj Q) ≫
        (Condensed.profiniteSolidCounit R).app Q =
      𝟙 ((Condensed.finFree R).obj Q) := by
  simpa [Condensed.profiniteSolidification] using
    (Functor.liftOfIsRightKanExtension_fac_app
      (Condensed.profiniteSolid R)
      (Condensed.profiniteSolidCounit R)
      (Condensed.profiniteFree R)
      (𝟙 (Condensed.finFree R)) Q)

#check lowerHomSectionsEquiv
#check lowerHomEquiv
#check finiteSolidification_counit
#check Profinite.exists_locallyConstant
#check Condensed.isColimitLocallyConstantPresheafDiagram
#check Functor.liftOfIsRightKanExtension_fac_app

#print axioms lowerHomSectionsEquiv
#print axioms lowerHomEquiv
#print axioms finiteSolidification_counit

end CMDG.CondensedCM4P3G
