import CMDGCondensedCM4P3DerivedCM5R0GSProductCompactSupport

/-!
# CMDG CM5: actual enriched coefficient-coordinate morphisms of G_S

This construction extracts each Nöbeling coordinate through the genuine
presheaf-category enriched internal Hom; it never replaces that internal
Hom by an ordinary algebraic dual or assumes the unproved infinite product
identification.

The underlying source map is the actual discrete-presheaf image of
Finsupp.lsingle. Contravariant precomposition in the closed monoidal
presheaf category, followed by the protected rank-one natural iso,
yields a *presheaf natural transformation* to the discrete coefficient
presheaf. It lifts to an actual CondensedMod morphism from G_S by
the protected CM4-P2-E comparison and CM5 basis transport.

This supplies every required component map. Joint universality,
a product cone, and the isomorphism G_S ≅ ∏ᶜ R_disc remain open.
-/

noncomputable section

universe u

open CategoryTheory Limits
open scoped CategoryTheory.MonoidalClosed

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

noncomputable local instance : MonoidalClosed
    CMDG.CondensedCM4P2D.PresheafModule.{u} :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- The actual coefficient inclusion into the Nöbeling basis source,
lifted by the discrete presheaf functor from Finsupp.lsingle. -/
noncomputable def gsBasisCoefficientInclusionPresheaf
    (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    CMDG.CondensedCM4P2D.coefficientPresheaf ⟶
      gsBasisDiscreteSourcePresheaf S :=
  (CondensedMod.LocallyConstant.functorToPresheaves R.{u}).map
    (ModuleCat.ofHom
      (Finsupp.lsingle i : R.{u} →ₗ[R.{u}]
        (LiftedSourceBasisIndex S →₀ R.{u})))

/-- Genuine natural enriched-Hom coordinate on compact-Hausdorff tests,
obtained by precomposition and the previously proved rank-one iso. -/
noncomputable def gsBasisEnrichedCoordinatePresheaf
    (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    gsBasisInternalHomPresheaf S ⟶
      CMDG.CondensedCM4P2D.coefficientPresheaf :=
  (MonoidalClosed.pre (gsBasisCoefficientInclusionPresheaf S i)).app
      CMDG.CondensedCM4P2D.coefficientPresheaf ≫
    CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom

/-- A genuine condensed-module coefficient coordinate of the actual
free-solid target, not a map merely on underlying module sections. -/
noncomputable def gsFreeSolidCoefficientCoordinate
    (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    (Condensed.profiniteSolid R.{u}).obj S ⟶ discreteIntegerCoeff.{u} :=
  (freeSolidToBasisInternalHomCondensedIso S).hom ≫
    ObjectProperty.homMk (gsBasisEnrichedCoordinatePresheaf S i)

/-- The canonical map from the actual G_S into the categorical product
of discrete coefficient sheaves, assembled from its genuine enriched
coordinate morphisms. No isomorphism is asserted by its construction. -/
noncomputable def gsFreeSolidToCoefficientProduct
    (S : Profinite.{u}) :
    (Condensed.profiniteSolid R.{u}).obj S ⟶
      (∏ᶜ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})) :=
  Pi.lift (fun i => gsFreeSolidCoefficientCoordinate S i)

@[simp]
theorem gsFreeSolidToCoefficientProduct_projection
    (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    gsFreeSolidToCoefficientProduct S ≫
      Pi.π (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u}) i =
        gsFreeSolidCoefficientCoordinate S i := by
  exact Pi.lift_π _ _

#check gsBasisCoefficientInclusionPresheaf
#check gsBasisEnrichedCoordinatePresheaf
#check gsFreeSolidCoefficientCoordinate
#check gsFreeSolidToCoefficientProduct
#check gsFreeSolidToCoefficientProduct_projection

#print axioms gsBasisCoefficientInclusionPresheaf
#print axioms gsBasisEnrichedCoordinatePresheaf
#print axioms gsFreeSolidCoefficientCoordinate
#print axioms gsFreeSolidToCoefficientProduct
#print axioms gsFreeSolidToCoefficientProduct_projection

end CMDG.CondensedCM5R0
