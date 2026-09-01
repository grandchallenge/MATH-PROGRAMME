import CMDGCondensedCM4P3GBooleanCube

/-!
# CMDG CM4-P3-G lifted Nöbeling Boolean pairing

The integral Boolean pairing is transported through the exact coefficient-ring equivalence
`ℤ ≃+* R`. This yields the `R`-linear map needed to construct actual finite-stage measure
sections. The same transport applies to every integer-weighted Boolean pairing.
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

/-- Pointwise scalar extension on the literal Boolean product type. Keeping this transport on
that exact topology avoids identifying the product topology with the packaged `basisBooleanCube`
topology by definitional equality. -/
noncomputable def basisBooleanIntegralLiftEquiv (X : Profinite.{u}) :
    LocallyConstant (IntegralBasisIndex X → Bool) ℤ ≃+*
      LocallyConstant (IntegralBasisIndex X → Bool) R :=
  LocallyConstant.congrRightRingEquiv (X := IntegralBasisIndex X → Bool)
    (ULift.ringEquiv.symm : ℤ ≃+* R)

/-- The Nöbeling Boolean pairing, transported to the actual lifted coefficient ring. -/
noncomputable def basisBooleanPairingR (X : Profinite.{u}) :
    LocallyConstant X R →ₗ[R]
      LocallyConstant (IntegralBasisIndex X → Bool) R where
  toFun v :=
    basisBooleanIntegralLiftEquiv X
      (basisBooleanPairing X (locallyConstantIntegralDownEquiv X v))
  map_add' v w := by
    rw [map_add, map_add, map_add]
  map_smul' r v := by
    have hdown :
        locallyConstantIntegralDownEquiv X (r • v) =
          r.down • locallyConstantIntegralDownEquiv X v := by
      ext x
      rfl
    rw [hdown, map_smul]
    ext t
    rfl

/-- The arbitrary integer-weighted Nöbeling Boolean pairing, transported to the lifted
coefficient ring. -/
noncomputable def weightedBasisBooleanPairingR (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ) :
    LocallyConstant X R →ₗ[R]
      LocallyConstant (IntegralBasisIndex X → Bool) R where
  toFun v :=
    basisBooleanIntegralLiftEquiv X
      (weightedBasisBooleanPairing X a (locallyConstantIntegralDownEquiv X v))
  map_add' v w := by
    rw [map_add, map_add, map_add]
  map_smul' r v := by
    have hdown :
        locallyConstantIntegralDownEquiv X (r • v) =
          r.down • locallyConstantIntegralDownEquiv X v := by
      ext x
      rfl
    rw [hdown, map_smul]
    ext t
    rfl

#print locallyConstantIntegralDownEquiv
#print basisBooleanIntegralLiftEquiv
#print basisBooleanPairingR
#print weightedBasisBooleanPairingR
#print axioms basisBooleanPairingR
#print axioms weightedBasisBooleanPairingR

end CMDG.CondensedCM4P3G.BasisBooleanPairingR
