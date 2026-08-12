import CMDGCondensedCM4P3D
import CMDGCondensedCM4P2ERankOneNaturalIso
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.CofilteredLimit

/-!
# CMDG CM4-P3-F — coefficient-object solidity

This successor isolates the single coefficient-object residual left by P3-E.
The first certified layer identifies the lower Hom set with locally constant
lifted-integer-valued functions on the profinite source. The second layer
factors every such lower-Hom morphism through a canonical finite quotient and
lifts it through the finite right-Kan counit. The third layer constructs the
canonical double-internal-dual evaluation whose surjectivity is the remaining
mapping-out theorem.
No coefficient solidity or P3 availability is asserted by this file unless
and until the terminal declarations are proved.
-/

namespace CMDG.CondensedCM4P3F

universe u

open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P3D.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule.{u}

noncomputable abbrev coefficientObject : CondensedMod.{u} R :=
  CMDG.CondensedCM4P3D.coefficientObject.{u}

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

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

/-- Naturality of the represented-set leg of `lowerHomEquiv`. -/
theorem lowerHomYonedaEquiv_naturality {X Y : Profinite.{u}} (q : X ⟶ Y)
    (h : Y.toCondensed ⟶ (Condensed.forget R).obj coefficientObject) :
    lowerHomYonedaEquiv X (profiniteToCondensed.map q ≫ h) =
      (lowerHomYonedaEquiv Y h).comap q.hom.hom := by
  have hy :=
    ((coherentTopology CompHaus.{u}).uliftYonedaEquiv_naturality
      h (profiniteToCompHaus.map q)).symm
  change
    (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((coherentTopology CompHaus.{u}).uliftYoneda.map
          (profiniteToCompHaus.map q) ≫ h) =
      (ConcreteCategory.hom
        (((Condensed.forget R).obj coefficientObject).obj.map
          (profiniteToCompHaus.map q).op))
        ((coherentTopology CompHaus.{u}).uliftYonedaEquiv h)
  exact hy

/-- The complete lower-Hom equivalence is contravariantly natural in the
profinite source. -/
theorem lowerHomEquiv_naturality {X Y : Profinite.{u}} (q : X ⟶ Y)
    (h : (Condensed.profiniteFree R).obj Y ⟶ coefficientObject) :
    lowerHomEquiv X ((Condensed.profiniteFree R).map q ≫ h) =
      (lowerHomEquiv Y h).comap q.hom.hom := by
  have hadj :
      lowerHomAdjunctionEquiv X ((Condensed.profiniteFree R).map q ≫ h) =
        profiniteToCondensed.map q ≫ lowerHomAdjunctionEquiv Y h := by
    simpa [lowerHomAdjunctionEquiv] using
      (Condensed.freeForgetAdjunction R).homEquiv_naturality_left
        (profiniteToCondensed.map q) h
  change
    lowerHomYonedaEquiv X
        (lowerHomAdjunctionEquiv X ((Condensed.profiniteFree R).map q ≫ h)) = _
  rw [hadj]
  exact lowerHomYonedaEquiv_naturality q (lowerHomAdjunctionEquiv Y h)

set_option backward.isDefEq.respectTransparency false in
/-- Every lower-Hom morphism factors through one of the canonical finite
quotients of the profinite source. -/
theorem lowerHom_factors_finite (X : Profinite.{u})
    (h : (Condensed.profiniteFree R).obj X ⟶ coefficientObject) :
    ∃ (j : DiscreteQuotient X)
      (hQ : (Condensed.profiniteFree R).obj (X.diagram.obj j) ⟶ coefficientObject),
      h = (Condensed.profiniteFree R).map (X.asLimitCone.π.app j) ≫ hQ := by
  obtain ⟨j, g, hg⟩ :=
    Profinite.exists_locallyConstant X.asLimitCone X.asLimit (lowerHomEquiv X h)
  let q : X ⟶ X.diagram.obj j := X.asLimitCone.π.app j
  refine ⟨j, (lowerHomEquiv (X.diagram.obj j)).symm g, ?_⟩
  change h = (Condensed.profiniteFree R).map q ≫
    (lowerHomEquiv (X.diagram.obj j)).symm g
  apply (lowerHomEquiv X).injective
  rw [lowerHomEquiv_naturality, Equiv.apply_symm_apply]
  simpa [q] using hg

set_option backward.isDefEq.respectTransparency false in
/-- On a finite profinite object, solidification followed by the right-Kan
counit is the identity on the finite free module. -/
@[reassoc (attr := simp)] theorem finiteSolidification_counit (Q : FintypeCat.{u}) :
    (Condensed.profiniteSolidification R).app (FintypeCat.toProfinite.obj Q) ≫
        (Condensed.profiniteSolidCounit R).app Q =
      𝟙 ((Condensed.finFree R).obj Q) := by
  simpa [Condensed.profiniteSolidification] using
    ((Condensed.profiniteSolid R).liftOfIsRightKanExtension_fac_app
      (Condensed.profiniteSolidCounit R)
      (Condensed.profiniteFree R)
      (𝟙 (Condensed.finFree R)) Q)

/-- Lift a lower-Hom morphism on a canonical finite quotient through the
solid finite value and pull it back along the solid functor. -/
noncomputable def finiteQuotientLift
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (hQ : (Condensed.profiniteFree R).obj (X.diagram.obj j) ⟶ coefficientObject) :
    (Condensed.profiniteSolid R).obj X ⟶ coefficientObject :=
  (Condensed.profiniteSolid R).map (X.asLimitCone.π.app j) ≫
    (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ hQ

set_option backward.isDefEq.respectTransparency false in
/-- The finite-quotient lift is a genuine preimage under coefficient
solidification. -/
theorem homPrecomp_finiteQuotientLift
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (hQ : (Condensed.profiniteFree R).obj (X.diagram.obj j) ⟶ coefficientObject) :
    CMDG.CondensedCM4P3D.homPrecomp coefficientObject X
        (finiteQuotientLift X j hQ) =
      (Condensed.profiniteFree R).map (X.asLimitCone.π.app j) ≫ hQ := by
  let q : X ⟶ X.diagram.obj j := X.asLimitCone.π.app j
  change
    (Condensed.profiniteSolidification R).app X ≫
        ((Condensed.profiniteSolid R).map q ≫
          (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ hQ) =
      (Condensed.profiniteFree R).map q ≫ hQ
  rw [← Category.assoc,
    ← (Condensed.profiniteSolidification R).naturality q]
  simp

/-- SECOND: every lower-Hom morphism has a finite-quotient lift through
`profiniteSolidification`. -/
theorem homPrecomp_surjective (X : Profinite.{u}) :
    Function.Surjective
      (CMDG.CondensedCM4P3D.homPrecomp coefficientObject X) := by
  intro h
  obtain ⟨j, hQ, hfac⟩ := lowerHom_factors_finite X h
  refine ⟨finiteQuotientLift X j hQ, ?_⟩
  rw [homPrecomp_finiteQuotientLift]
  exact hfac.symm

/-- A section `f ∈ C(X,R)` determines the rank-one map `R → C(X,R)`. -/
noncomputable def rankOneContinuousMap
    (X : Profinite.{u}) (f : LocallyConstant X R) :
    ModuleCat.of R R ⟶ CMDG.CondensedCM4P2D.continuousFunctions.obj (op X) :=
  ModuleCat.ofHom
    { toFun := fun r => r • f
      map_add' := by
        intro a b
        exact add_smul a b f
      map_smul' := by
        intro a b
        change (a * b) • f = a • b • f
        exact mul_smul a b f }

/-- Apply the protected locally-constant presheaf functor to the rank-one map. -/
noncomputable def rankOnePresheafMap
    (X : Profinite.{u}) (f : LocallyConstant X R) :
    CMDG.CondensedCM4P2D.coefficientPresheaf ⟶
      CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj (op X) := by
  change
    (CondensedMod.LocallyConstant.functorToPresheaves R).obj (ModuleCat.of R R) ⟶
      (CondensedMod.LocallyConstant.functorToPresheaves R).obj
        (CMDG.CondensedCM4P2D.continuousFunctions.obj (op X))
  exact (CondensedMod.LocallyConstant.functorToPresheaves R).map
    (rankOneContinuousMap X f)

/-- The canonical double-internal-dual evaluation attached to `f`, before
lifting from presheaves to condensed modules. -/
noncomputable def bidualEvaluationPresheaf
    (X : Profinite.{u}) (f : LocallyConstant X R) :
    CMDG.CondensedCM4P2D.measurePresheafObj X ⟶
      CMDG.CondensedCM4P2D.coefficientPresheaf :=
  (MonoidalClosed.pre (rankOnePresheafMap X f)).app
      CMDG.CondensedCM4P2D.coefficientPresheaf ≫
    CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom

/-- The same canonical evaluation as a morphism of condensed modules. -/
noncomputable def bidualEvaluationMeasureMap
    (X : Profinite.{u}) (f : LocallyConstant X R) :
    CMDG.CondensedCM4P2D.measureFunctor.obj X ⟶ coefficientObject :=
  ObjectProperty.homMk (bidualEvaluationPresheaf X f)

/-- Canonical global double-dual evaluation, transported from the protected
P2-D measure model to `profiniteSolid` by protected P2-E. -/
noncomputable def canonicalBidualEvaluation
    (X : Profinite.{u}) (f : LocallyConstant X R) :
    (Condensed.profiniteSolid R).obj X ⟶ coefficientObject :=
  (CMDG.CondensedCM4P3C.targetIso X).inv ≫ bidualEvaluationMeasureMap X f

/-- THIRD: the exact condensed finite-dependence / mapping-out residual.
Every global morphism from the double internal dual to the coefficient object
must be evaluation at a locally constant section. -/
def GlobalSectionsDoubleInternalDualSurjectivity (X : Profinite.{u}) : Prop :=
  Function.Surjective (canonicalBidualEvaluation X)

#check lowerHomAdjunctionEquiv
#check lowerHomYonedaEquiv
#check lowerHomEquiv
#check lowerHomYonedaEquiv_naturality
#check lowerHomEquiv_naturality
#check lowerHom_factors_finite
#check finiteSolidification_counit
#check finiteQuotientLift
#check homPrecomp_finiteQuotientLift
#check homPrecomp_surjective
#check rankOneContinuousMap
#check rankOnePresheafMap
#check bidualEvaluationPresheaf
#check bidualEvaluationMeasureMap
#check canonicalBidualEvaluation
#check GlobalSectionsDoubleInternalDualSurjectivity

#print axioms lowerHomEquiv
#print axioms lowerHom_factors_finite
#print axioms homPrecomp_surjective
#print axioms rankOneContinuousMap
#print axioms rankOnePresheafMap
#print axioms bidualEvaluationPresheaf
#print axioms bidualEvaluationMeasureMap
#print axioms canonicalBidualEvaluation
#print axioms GlobalSectionsDoubleInternalDualSurjectivity

end CMDG.CondensedCM4P3F
