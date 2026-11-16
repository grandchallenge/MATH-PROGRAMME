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

/-- The exact coefficient-ring transport of locally constant functions.
It is semilinear over the *ring isomorphism*, not an incorrectly
assumed Z-linear map into an R-module. -/
noncomputable def integralToLiftedLocallyConstantSemilinearEquiv
    (S : Profinite.{u}) :
    LocallyConstant S ℤ ≃ₛₗ[
      (ULift.ringEquiv.symm : ℤ ≃+* LiftedR).toRingHom]
        LocallyConstant S LiftedR := by
  let h : ℤ ≃+* LiftedR := ULift.ringEquiv.symm
  letI : RingHomInvPair (h : ℤ →+* LiftedR)
      (h.symm : LiftedR →+* ℤ) := RingHomInvPair.of_ringEquiv h
  letI : RingHomInvPair (h.symm : LiftedR →+* ℤ)
      (h : ℤ →+* LiftedR) := RingHomInvPair.of_ringEquiv h.symm
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
    Module.Free LiftedR (LocallyConstant S LiftedR) := by
  let h : ℤ ≃+* LiftedR := ULift.ringEquiv.symm
  letI : RingHomInvPair (h : ℤ →+* LiftedR)
      (h.symm : LiftedR →+* ℤ) := RingHomInvPair.of_ringEquiv h
  letI : RingHomInvPair (h.symm : LiftedR →+* ℤ)
      (h : ℤ →+* LiftedR) := RingHomInvPair.of_ringEquiv h.symm
  exact Module.Free.of_equiv (integralToLiftedLocallyConstantSemilinearEquiv S)

/-- The chosen R-basis index for the actual C(S,R) source module. -/
abbrev LiftedSourceBasisIndex (S : Profinite.{u}) :=
  Module.Free.ChooseBasisIndex LiftedR (LocallyConstant S LiftedR)

/-- Exact R-linear basis of the CM4 measure source. -/
noncomputable def liftedSourceBasis (S : Profinite.{u}) :
    Module.Basis (LiftedSourceBasisIndex S) LiftedR
      (LocallyConstant S LiftedR) :=
  Module.Free.chooseBasis LiftedR (LocallyConstant S LiftedR)

/-- Genuine module-category isomorphism, rather than a bare group
bijection, from C(S,R) to its direct-sum coefficient presentation. -/
noncomputable def liftedSourceModuleIso (S : Profinite.{u}) :
    ModuleCat.of LiftedR (LocallyConstant S LiftedR) ≅
      ModuleCat.of LiftedR (LiftedSourceBasisIndex S →₀ LiftedR) where
  hom := ModuleCat.ofHom (liftedSourceBasis S).repr.toLinearMap
  inv := ModuleCat.ofHom (liftedSourceBasis S).repr.symm.toLinearMap
  hom_inv_id := by
    apply ModuleCat.hom_injective
    ext f
    exact (liftedSourceBasis S).repr.symm_apply_apply f
  inv_hom_id := by
    apply ModuleCat.hom_injective
    ext f
    exact (liftedSourceBasis S).repr.apply_symm_apply f

/-- The actual presheaf in the protected CM4-P2-D enriched-Hom model
is the discrete presheaf of the basis-sum module. -/
noncomputable def liftedSourcePresheafIso (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj (op S) ≅
      (CondensedMod.LocallyConstant.functorToPresheaves LiftedR).obj
        (ModuleCat.of LiftedR (LiftedSourceBasisIndex S →₀ LiftedR)) := by
  exact (CondensedMod.LocallyConstant.functorToPresheaves LiftedR).mapIso
    (liftedSourceModuleIso S)

#check integralToLiftedLocallyConstantSemilinearEquiv
#check liftedLocallyConstantFree
#check liftedSourceBasis
#check liftedSourceModuleIso
#check liftedSourcePresheafIso

#print axioms integralToLiftedLocallyConstantSemilinearEquiv
#print axioms liftedLocallyConstantFree
#print axioms liftedSourceModuleIso
#print axioms liftedSourcePresheafIso

end CMDG.CondensedCM5R0
