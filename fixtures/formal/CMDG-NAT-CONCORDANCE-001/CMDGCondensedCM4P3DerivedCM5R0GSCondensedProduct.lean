import CMDGCondensedCM4P3DerivedCM5R0GSEnrichedProduct
import CMDGCondensedCM4P3DerivedCM5R0DiscreteExtOneClosure
import Mathlib.CategoryTheory.Sites.Limits
import Mathlib.CategoryTheory.Limits.Preserves.Shapes.Products

/-!
# CMDG CM5: the actual free-solid target is a condensed coefficient product

The protected presheaf fan in CMDGCondensedCM4P3DerivedCM5R0GSEnrichedProduct
is limiting and has precisely the existing enriched coefficient coordinates.
Mathlib's sheaf inclusion creates limits, so the same cone is limiting
in CondensedMod. Its unique product comparison is then the exact existing
canonical map out of G_S, not an arbitrary unrelated isomorphism.

This gives the genuine degree-one Ext vanishing for G_S via the protected
discrete-product extension theorem. It does not prove higher Ext,
unrestricted derived solidity or external source-semantic certification.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

/-- The condensed-module fan of the real Nöbeling coefficient maps. -/
noncomputable def gsBasisCondensedCoefficientFan (S : Profinite.{u}) :
    Fan (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u}) :=
  Fan.mk (gsBasisInternalHomCondensed S)
    (fun i => ObjectProperty.homMk (gsBasisEnrichedCoordinatePresheaf S i))

/-- The presheaf product universal property lifts to CondensedMod
because the inclusion of sheaves creates limits. -/
noncomputable def gsBasisCondensedCoefficientFanIsLimit (S : Profinite.{u}) :
    IsLimit (gsBasisCondensedCoefficientFan S) := by
  unfold gsBasisCondensedCoefficientFan
  apply (isLimitOfIsLimitFanMkObj
    (sheafToPresheaf (coherentTopology CompHaus.{u})
      (ModuleCat.{u + 1} R.{u}))
    (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})
    (fun i => ObjectProperty.homMk (gsBasisEnrichedCoordinatePresheaf S i)))
  change IsLimit (gsBasisEnrichedCoefficientFan S)
  exact gsBasisEnrichedCoefficientFanIsLimit S

/-- An actual categorical isomorphism in CondensedMod, not merely
one in a presheaf or an equivalence of groups of sections. -/
noncomputable def gsBasisCondensedToCoefficientProductIso
    (S : Profinite.{u}) :
    gsBasisInternalHomCondensed S ≅
      (∏ᶜ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})) :=
  (gsBasisCondensedCoefficientFanIsLimit S).conePointUniqueUpToIso
    (limit.isLimit (Discrete.functor
      (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})))

@[simp]
theorem gsBasisCondensedToCoefficientProductIso_projection
    (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    (gsBasisCondensedToCoefficientProductIso S).hom ≫
      Pi.π (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u}) i =
        ObjectProperty.homMk (gsBasisEnrichedCoordinatePresheaf S i) := by
  exact (gsBasisCondensedCoefficientFanIsLimit S).conePointUniqueUpToIso_hom_comp
    (limit.isLimit (Discrete.functor
      (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})))
    (Discrete.mk i)

/-- The existing canonical G_S map is the composite of the protected
free-solid basis-dual isomorphism and the newly proved product isomorphism. -/
theorem gsFreeSolidToCoefficientProduct_eq_iso_hom
    (S : Profinite.{u}) :
    gsFreeSolidToCoefficientProduct S =
      ((freeSolidToBasisInternalHomCondensedIso S) ≪≫
        gsBasisCondensedToCoefficientProductIso S).hom := by
  apply Pi.hom_ext
  intro i
  rw [gsFreeSolidToCoefficientProduct_projection]
  change gsFreeSolidCoefficientCoordinate S i =
    (freeSolidToBasisInternalHomCondensedIso S).hom ≫
      (gsBasisCondensedToCoefficientProductIso S).hom ≫
        Pi.π (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u}) i
  rw [gsBasisCondensedToCoefficientProductIso_projection]
  rfl

/-- The preexisting canonical comparison is a genuine isomorphism. -/
theorem gsFreeSolidToCoefficientProduct_isIso (S : Profinite.{u}) :
    IsIso (gsFreeSolidToCoefficientProduct S) := by
  rw [gsFreeSolidToCoefficientProduct_eq_iso_hom]
  infer_instance

/-- The new isomorphism has exactly the old, canonically constructed
coefficient comparison map as its forward morphism. -/
noncomputable def gsFreeSolidToCoefficientProductIso (S : Profinite.{u}) :
    (Condensed.profiniteSolid R.{u}).obj S ≅
      (∏ᶜ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})) := by
  letI := gsFreeSolidToCoefficientProduct_isIso S
  exact asIso (gsFreeSolidToCoefficientProduct S)

/-- Genuine CM5 degree-one Ext vanishing into the actual free-solid
coefficient object, for arbitrary profinite source and target. -/
theorem freeProfinite_extOne_genuineSolid_vanishes
    (T S : Profinite.{u}) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      ((Condensed.profiniteSolid R.{u}).obj S) 1, e = 0 := by
  exact freeProfinite_extOne_solid_vanishes_of_discreteProductModel
    T S (gsFreeSolidToCoefficientProductIso S)

#check gsBasisCondensedCoefficientFan
#check gsBasisCondensedCoefficientFanIsLimit
#check gsBasisCondensedToCoefficientProductIso
#check gsBasisCondensedToCoefficientProductIso_projection
#check gsFreeSolidToCoefficientProduct_eq_iso_hom
#check gsFreeSolidToCoefficientProduct_isIso
#check gsFreeSolidToCoefficientProductIso
#check freeProfinite_extOne_genuineSolid_vanishes

#print axioms gsBasisCondensedCoefficientFanIsLimit
#print axioms gsBasisCondensedToCoefficientProductIso
#print axioms gsBasisCondensedToCoefficientProductIso_projection
#print axioms gsFreeSolidToCoefficientProduct_eq_iso_hom
#print axioms gsFreeSolidToCoefficientProduct_isIso
#print axioms gsFreeSolidToCoefficientProductIso
#print axioms freeProfinite_extOne_genuineSolid_vanishes

end CMDG.CondensedCM5R0
