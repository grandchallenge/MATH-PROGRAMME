import CMDGCondensedCM4P2D
import CMDGCondensedCM4P3GBasisSeparation
import Mathlib.LinearAlgebra.FreeModule.Basic
import Mathlib.Algebra.Module.ULift

/-!
# CMDG CM5: Nöbeling basis for the actual lifted discrete source

For every (possibly infinite) profinite S, Nöbeling supplies a basis of
LocallyConstant S ℤ. The protected CM4 measure/internal-Hom construction
uses the lifted integer ring R := ULift ℤ. This file transports Nöbeling
freeness across the exact ring equivalence ℤ ≃+* R and then applies the
chosen R-basis to the *actual* source presheaf of the protected measure.

This is a genuine categorical source comparison, not an assertion that
the free solid target G_S is already a categorical product. The latter
requires a separate internal-Hom/coproduct-to-product isomorphism.
-/

noncomputable section

universe u

open CategoryTheory Opposite

namespace CMDG.CondensedCM5R0

private abbrev LiftedR : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}
 
/-- The inverse ring homomorphisms are registered at declaration scope
so that the semilinear-equivalence type itself elaborates. -/
private instance liftedRingHomInvPair :
    RingHomInvPair
      ((ULift.ringEquiv.symm : ℤ ≃+* LiftedR.{u}).toRingHom)
      ((ULift.ringEquiv : LiftedR.{u} ≃+* ℤ).toRingHom) :=
  RingHomInvPair.of_ringEquiv
    (ULift.ringEquiv.symm : ℤ ≃+* LiftedR.{u})

private instance liftedRingHomInvPairSymm :
    RingHomInvPair
      ((ULift.ringEquiv : LiftedR.{u} ≃+* ℤ).toRingHom)
      ((ULift.ringEquiv.symm : ℤ ≃+* LiftedR.{u}).toRingHom) :=
  RingHomInvPair.of_ringEquiv
    (ULift.ringEquiv : LiftedR.{u} ≃+* ℤ)

/-- The exact coefficient-ring transport of locally constant functions.
It is semilinear over the *ring isomorphism*, not an incorrectly
assumed Z-linear map into an R-module. -/
noncomputable def integralToLiftedLocallyConstantSemilinearEquiv
    (S : Profinite.{u}) :
    LocallyConstant S ℤ ≃ₛₗ[
      (ULift.ringEquiv.symm : ℤ ≃+* LiftedR.{u}).toRingHom]
        LocallyConstant S LiftedR.{u} := by
  let h : ℤ ≃+* LiftedR.{u} := ULift.ringEquiv.symm
  exact
    { __ := (LocallyConstant.congrRightRingEquiv (X := S) h).toAddEquiv
      map_smul' := by
        intro a f
        ext s
        rfl }

/-- Nöbeling freeness for the *exact lifted coefficient ring* used by
the free solid condensed module. No restriction to finite S. -/
noncomputable instance liftedLocallyConstantFree
    (S : Profinite.{u}) :
    Module.Free LiftedR.{u} (LocallyConstant S LiftedR.{u}) := by
  let h : ℤ ≃+* LiftedR.{u} := ULift.ringEquiv.symm
  exact Module.Free.of_equiv (integralToLiftedLocallyConstantSemilinearEquiv S)

/-- The chosen R-basis index for the actual C(S,R) source module. -/
abbrev LiftedSourceBasisIndex (S : Profinite.{u}) :=
  Module.Free.ChooseBasisIndex LiftedR.{u} (LocallyConstant S LiftedR.{u})

/-- Exact R-linear basis of the CM4 measure source. -/
noncomputable def liftedSourceBasis (S : Profinite.{u}) :
    Module.Basis (LiftedSourceBasisIndex S) LiftedR.{u}
      (LocallyConstant S LiftedR.{u}) :=
  Module.Free.chooseBasis LiftedR.{u} (LocallyConstant S LiftedR.{u})

/-- Genuine module-category isomorphism, rather than a bare group
bijection, from C(S,R) to its direct-sum coefficient presentation. -/
noncomputable def liftedSourceModuleIso (S : Profinite.{u}) :
    ModuleCat.of LiftedR.{u} (LocallyConstant S LiftedR.{u}) ≅
      ModuleCat.of LiftedR.{u} (LiftedSourceBasisIndex S →₀ LiftedR.{u}) :=
  (liftedSourceBasis S).repr.toModuleIso

/-- The actual presheaf in the protected CM4-P2-D enriched-Hom model
is the discrete presheaf of the basis-sum module. -/
noncomputable def liftedSourcePresheafIso (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj (op S) ≅
      (CondensedMod.LocallyConstant.functorToPresheaves LiftedR.{u}).obj
        (ModuleCat.of LiftedR.{u} (LiftedSourceBasisIndex S →₀ LiftedR.{u})) := by
  exact (CondensedMod.LocallyConstant.functorToPresheaves LiftedR.{u}).mapIso
    (liftedSourceModuleIso S)

/-- Nöbeling coordinates of the ordinary R-linear dual, with arbitrary
test compact Hausdorff X. This is a genuine linear equivalence:
Hom_R(C(S,R), C(X,R)) ≃ (basis(S) → C(X,R)).
The internal-Hom/end-to-ordinary-linear-Hom comparison remains a
separate categorical obligation. -/
noncomputable def liftedSourceLinearDualCoordinates
    (S : Profinite.{u}) (X : CompHaus.{u}) :
    ((LocallyConstant S LiftedR.{u}) →ₗ[LiftedR.{u}]
      LocallyConstant X LiftedR.{u}) ≃ₗ[LiftedR.{u}]
      (LiftedSourceBasisIndex S → LocallyConstant X LiftedR.{u}) :=
  ((liftedSourceBasis S).constr LiftedR.{u}).symm

@[simp]
theorem liftedSourceLinearDualCoordinates_apply
    (S : Profinite.{u}) (X : CompHaus.{u})
    (f : LocallyConstant S LiftedR.{u} →ₗ[LiftedR.{u}]
      LocallyConstant X LiftedR.{u})
    (i : LiftedSourceBasisIndex S) :
    liftedSourceLinearDualCoordinates S X f i =
      f (liftedSourceBasis S i) := by
  rfl

#check integralToLiftedLocallyConstantSemilinearEquiv
#check liftedLocallyConstantFree
#check liftedSourceBasis
#check liftedSourceModuleIso
#check liftedSourcePresheafIso
#check liftedSourceLinearDualCoordinates
#check liftedSourceLinearDualCoordinates_apply

#print axioms integralToLiftedLocallyConstantSemilinearEquiv
#print axioms liftedLocallyConstantFree
#print axioms liftedSourceModuleIso
#print axioms liftedSourcePresheafIso
#print axioms liftedSourceLinearDualCoordinates
#print axioms liftedSourceLinearDualCoordinates_apply

end CMDG.CondensedCM5R0
