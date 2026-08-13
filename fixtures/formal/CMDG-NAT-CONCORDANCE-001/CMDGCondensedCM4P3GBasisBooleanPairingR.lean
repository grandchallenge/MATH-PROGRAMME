import CMDGCondensedCM4P3GBooleanCube

/-!
# CMDG CM4-P3-G lifted Nöbeling Boolean pairing

The integral Boolean pairing is transported through the exact coefficient-ring equivalence
`ℤ ≃+* R`. This yields the `R`-linear map needed to construct actual finite-stage measure
sections.
-/

namespace CMDG.CondensedCM4P3G.BasisBooleanPairingR

universe u

open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- Pointwise scalar descent from the lifted coefficient ring to integers. -/
noncomputable def locallyConstantIntegralDownEquiv (X : Profinite.{u}) :
    LocallyConstant X R ≃+* LocallyConstant X ℤ :=
  (CMDG.CondensedCM4P3G.locallyConstantIntegralLiftEquiv X).symm

/-- The already-certified Boolean pairing, bundled as an additive homomorphism. -/
noncomputable def basisBooleanPairingAddHom (X : Profinite.{u}) :
    LocallyConstant X ℤ →+ LocallyConstant (IntegralBasisIndex X → Bool) ℤ where
  toFun := basisBooleanPairing X
  map_zero' := basisBooleanPairing_zero X
  map_add' := basisBooleanPairing_add X

/-- The Boolean pairing as a canonical integral linear map. -/
noncomputable def basisBooleanPairingIntLinear (X : Profinite.{u}) :
    LocallyConstant X ℤ →ₗ[ℤ] LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
  (basisBooleanPairingAddHom X).toIntLinearMap

/-- The Nöbeling Boolean pairing, transported to the actual lifted coefficient ring. -/
noncomputable def basisBooleanPairingR (X : Profinite.{u}) :
    LocallyConstant X R →ₗ[R]
      LocallyConstant (IntegralBasisIndex X → Bool) R where
  toFun v :=
    CMDG.CondensedCM4P3G.locallyConstantIntegralLiftEquiv
      (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)
      (basisBooleanPairingIntLinear X (locallyConstantIntegralDownEquiv X v))
  map_add' v w := by
    rw [map_add, map_add, map_add]
  map_smul' r v := by
    ext t
    change
      ULift.up
          (basisBooleanPairingIntLinear X
            (locallyConstantIntegralDownEquiv X (r • v)) t) =
        r * ULift.up
          (basisBooleanPairingIntLinear X
            (locallyConstantIntegralDownEquiv X v) t)
    have hdown :
        locallyConstantIntegralDownEquiv X (r • v) =
          r.down • locallyConstantIntegralDownEquiv X v := by
      ext x
      rfl
    rw [hdown, map_smul]
    rfl

#print locallyConstantIntegralDownEquiv
#print basisBooleanPairingAddHom
#print basisBooleanPairingIntLinear
#print basisBooleanPairingR
#print axioms basisBooleanPairingR

end CMDG.CondensedCM4P3G.BasisBooleanPairingR
