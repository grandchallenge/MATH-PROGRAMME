import CMDGCondensedCM4P3LKernelFunctional

/-!
# CMDG CM4 P3-M — finite basis common discrete quotient discriminator

This file implements only the first discriminator authorized by
`CMDG-CM4-P3-M-FINITE-STAGE-RECOVERY-001`.

The protected P3-L theorem produces a finite set of chosen Nöbeling-basis coordinates on which
`kernelProductFunctional X h` depends.  The question here is strictly whether an arbitrary finite
set of those basis functions can be made to descend simultaneously through one
`DiscreteQuotient X`.

No lower-side morphism `gQ`, finite-stage recovery of `h`, mapping-out injectivity, solidity, or
P3 completion is asserted here.
-/

namespace CMDG.CondensedCM4P3M.FiniteQuotientBridge

universe u

open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation

/-- Package a finite family of chosen integral Nöbeling basis functions as one locally constant
map.  Finiteness of the subtype `I` is exactly what allows `LocallyConstant.unflip` to form the
joint observation. -/
noncomputable def finiteBasisFamily
    (X : Profinite.{u}) (I : Finset (IntegralBasisIndex X)) :
    LocallyConstant X (I → ℤ) :=
  LocallyConstant.unflip (fun i : I => integralBasis X i.1)

/-- Any finite family of chosen integral Nöbeling basis functions descends jointly through one
finite discrete quotient of `X`.

The proof deliberately uses only the existing cofiltered-limit factorization theorem already used
by protected P3-G: first package the family as one locally constant map, then factor that single
map through one stage. -/
theorem finiteBasisFamily_factors_common_discreteQuotient
    (X : Profinite.{u}) (I : Finset (IntegralBasisIndex X)) :
    ∃ (j : DiscreteQuotient X)
      (fQ : LocallyConstant (X.diagram.obj j) (I → ℤ)),
      finiteBasisFamily X I =
        fQ.comap (finiteQuotientMap X j).hom.hom := by
  exact
    Profinite.exists_locallyConstant X.asLimitCone X.asLimit
      (finiteBasisFamily X I)

/-- Coordinate form of `finiteBasisFamily_factors_common_discreteQuotient`: the same quotient
works simultaneously for every basis index in the finite set. -/
theorem integralBasis_factors_common_discreteQuotient
    (X : Profinite.{u}) (I : Finset (IntegralBasisIndex X)) :
    ∃ j : DiscreteQuotient X,
      ∀ i : I,
        ∃ fQ : LocallyConstant (X.diagram.obj j) ℤ,
          integralBasis X i.1 =
            fQ.comap (finiteQuotientMap X j).hom.hom := by
  obtain ⟨j, fQ, hf⟩ := finiteBasisFamily_factors_common_discreteQuotient X I
  refine ⟨j, ?_⟩
  intro i
  refine ⟨fQ.flip i, ?_⟩
  ext x
  simpa [finiteBasisFamily] using
    congrFun (LocallyConstant.congr_fun hf x) i

#check finiteBasisFamily_factors_common_discreteQuotient
#check integralBasis_factors_common_discreteQuotient
#print axioms finiteBasisFamily_factors_common_discreteQuotient
#print axioms integralBasis_factors_common_discreteQuotient

end CMDG.CondensedCM4P3M.FiniteQuotientBridge
