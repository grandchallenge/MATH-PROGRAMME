import CMDGCondensedCM4P3MFiniteQuotientBridge

/-!
# CMDG CM4 P3-M — pointwise Nöbeling kernel vanishing

This successor is the bounded `CMDG-CM4-P3-M-KERNEL-POINT-002` theorem file. It starts from the
protected finite-stage evaluation-weight/Dirac machinery and develops only the point-mass
comparison needed to turn a solidification-kernel hypothesis into the pointwise Nöbeling
vanishing statement frozen in issue #664.

No coefficient-object solidity, finite-stage mapping-out theorem, P3 completion, or CM4 closure is
asserted here.
-/

namespace CMDG.CondensedCM4P3M.KernelPointVanishing

universe u

open CategoryTheory Limits Opposite
open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3L.KernelFunctional
open CMDG.CondensedCM4P3M.KernelPointBridge

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The one-point profinite probe selecting a chosen point of `X`. -/
noncomputable def profinitePointProbe (X : Profinite.{u}) (x : X) :
    Profinite.of PUnit.{u + 1} ⟶ X :=
  ConcreteCategory.ofHom
    { toFun := fun _ => x
      continuous_toFun := continuous_const }

/-- Passing a point probe through a finite quotient selects the represented quotient point. -/
theorem profinitePointProbe_comp_finiteQuotientMap
    (X : Profinite.{u}) (x : X) (j : DiscreteQuotient X) :
    profinitePointProbe X x ≫ finiteQuotientMap X j =
      profinitePointProbe (X.diagram.obj j) (j.proj x) := by
  ext z
  rfl

/-- The generic free/section equivalence is natural under postcomposition in the condensed-module
 target. This is the target-side companion to the protected source-side precomposition theorem. -/
theorem freeHomSectionsEquiv_postcomp
    (T : Profinite.{u}) {A B : CondensedMod.{u} R}
    (g : (Condensed.profiniteFree R).obj T ⟶ A) (h : A ⟶ B) :
    freeHomSectionsEquiv T B (g ≫ h) =
      (ConcreteCategory.hom
        (((Condensed.forget R).map h).hom.app
          (op ((profiniteToCompHaus).obj T))))
        (freeHomSectionsEquiv T A g) := by
  change
    (coherentTopology CompHaus.{u}).uliftYonedaEquiv
      ((Condensed.freeForgetAdjunction R).homEquiv
        ((profiniteToCondensed).obj T) B (g ≫ h)) = _
  rw [Adjunction.homEquiv_naturality_right]
  rfl

/-- The tail of the protected finite comparison, after the concrete finite measure/small-free
comparison has already been applied. -/
noncomputable def finiteComparisonTailNatIso :
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedFunctor ≅
      Condensed.finFree R :=
  CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso ≪≫
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso ≪≫
    CMDG.CondensedCM4P2E.finiteFreeDiscreteIso.symm

/-- The first comparison-tail square is just naturality of the protected locally-constant/discrete
comparison. This keeps the coordinate map outside the nontrivial section-level presentation. -/
theorem finiteSmallFreeCoordinate_condensedDiscrete
    (Q : FintypeCat.{u}) (q : Q.obj) :
    (CondensedMod.LocallyConstant.functor R).map
          (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateModuleMap Q q) ≫
        (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso.app Q).hom =
      (CondensedMod.LocallyConstant.functorIsoDiscrete R).hom.app (ModuleCat.of R R) ≫
        (Condensed.discrete (ModuleCat.{u + 1} R)).map
          (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateModuleMap Q q) := by
  exact (CondensedMod.LocallyConstant.functorIsoDiscrete R).hom.naturality
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateModuleMap Q q)

/-- The protected universe transport sends the concrete finite free coordinate value to its
ULifted coordinate value.  This is the element-level form actually consumed by the finite-stage
Dirac section, avoiding an unnecessary equality of bundled coordinate maps. -/
theorem finiteSmallFreeCoordinateValue_ulift
    (Q : FintypeCat.{u}) (q : Q.obj) :
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv Q
        (Finsupp.single q (1 : R)) =
      Finsupp.single (ULift.up q) (1 : R) := by
  exact
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv_single Q q 1

/-- The inverse unique-left-adjoint comparison carries the free-module unit back to the
free-condensed-set unit.  This is the universal generator law needed for the last finite
comparison-tail stage. -/
theorem discreteFreeIso_inv_unit (A : Type (u + 1)) :
    CMDG.CondensedCM4P2E.freeDiscreteModuleAdj.unit.app A ≫
        (Condensed.forget R ⋙ Condensed.underlying (Type (u + 1))).map
          (CMDG.CondensedCM4P2E.discreteFreeIso.inv.app A) =
      CMDG.CondensedCM4P2E.discreteSetFreeAdj.unit.app A := by
  change
    CMDG.CondensedCM4P2E.freeDiscreteModuleAdj.unit.app A ≫
        (Condensed.forget R ⋙ Condensed.underlying (Type (u + 1))).map
          ((Adjunction.leftAdjointUniq
            CMDG.CondensedCM4P2E.freeDiscreteModuleAdj
            CMDG.CondensedCM4P2E.discreteSetFreeAdj).hom.app A) =
      CMDG.CondensedCM4P2E.discreteSetFreeAdj.unit.app A
  exact
    Adjunction.unit_leftAdjointUniq_hom_app
      CMDG.CondensedCM4P2E.freeDiscreteModuleAdj
      CMDG.CondensedCM4P2E.discreteSetFreeAdj A

/-- Elementwise form of the inverse unique-left-adjoint generator law.  It stays in the Type-valued
right adjoint, so no additional concrete-category coercion is introduced. -/
theorem discreteFreeIso_inv_unit_apply (A : Type (u + 1)) (a : A) :
    (CMDG.CondensedCM4P2E.freeDiscreteModuleAdj.unit.app A ≫
      (Condensed.forget R ⋙ Condensed.underlying (Type (u + 1))).map
        (CMDG.CondensedCM4P2E.discreteFreeIso.inv.app A)) a =
      CMDG.CondensedCM4P2E.discreteSetFreeAdj.unit.app A a := by
  exact congrFun (discreteFreeIso_inv_unit A) a

#check profinitePointProbe
#check profinitePointProbe_comp_finiteQuotientMap
#check freeHomSectionsEquiv_postcomp
#check finiteComparisonTailNatIso
#check finiteSmallFreeCoordinate_condensedDiscrete
#check finiteSmallFreeCoordinateValue_ulift
#check discreteFreeIso_inv_unit
#check discreteFreeIso_inv_unit_apply
#print axioms profinitePointProbe_comp_finiteQuotientMap
#print axioms freeHomSectionsEquiv_postcomp
#print axioms finiteSmallFreeCoordinate_condensedDiscrete
#print axioms finiteSmallFreeCoordinateValue_ulift
#print axioms discreteFreeIso_inv_unit
#print axioms discreteFreeIso_inv_unit_apply

end CMDG.CondensedCM4P3M.KernelPointVanishing
