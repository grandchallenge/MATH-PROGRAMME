import CMDGCondensedCM4P3D
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.AsLimit

/-!
# CMDG CM4-P3-G — coefficient mapping-out attack

This fixture attacks the single coefficient-object residual left by protected P3-D.
It identifies the lower Hom set with locally constant coefficient-valued functions,
uses finite quotients to construct extensions through profinite solidification, and
isolates the remaining mapping-out injectivity theorem exactly.
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
  refine ((Condensed.freeForgetAdjunction R).homEquiv
    ((profiniteToCondensed).obj X) coefficientObject).trans ?_
  change
    (((coherentTopology CompHaus.{u}).uliftYoneda.obj ((profiniteToCompHaus).obj X) ⟶
      (Condensed.forget R).obj coefficientObject) ≃ CoefficientSections X)
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv

/-- G0: the concrete lower-Hom equivalence. -/
noncomputable def lowerHomEquiv (X : Profinite.{u}) :
    LowerHom X ≃ LocallyConstant X R := by
  exact lowerHomSectionsEquiv X

/-- Naturality of G0: precomposition along a profinite map is exactly restriction of
locally constant functions. -/
theorem lowerHomEquiv_precomp {X Y : Profinite.{u}} (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      (lowerHomEquiv Y g).comap q.hom.hom := by
  change
    (coherentTopology CompHaus.{u}).uliftYonedaEquiv
      ((Condensed.freeForgetAdjunction R).homEquiv
        ((profiniteToCondensed).obj X) coefficientObject
        ((Condensed.free R).map ((profiniteToCondensed).map q) ≫ g)) = _
  rw [(Condensed.freeForgetAdjunction R).homEquiv_naturality_left]
  rw [← (coherentTopology CompHaus.{u}).uliftYonedaEquiv_naturality]
  rfl

/-- G1a: every lower-Hom map into the discrete coefficient object factors through a
finite quotient of the profinite source. -/
theorem lowerHom_factors_finite (X : Profinite.{u}) (g : LowerHom X) :
    ∃ (j : DiscreteQuotient X) (gQ : LowerHom (X.diagram.obj j)),
      g = (Condensed.profiniteFree R).map (X.asLimitCone.π.app j) ≫ gQ := by
  obtain ⟨j, fQ, hf⟩ :=
    Profinite.exists_locallyConstant X.asLimit (lowerHomEquiv X g)
  refine ⟨j, (lowerHomEquiv (X.diagram.obj j)).symm fQ, ?_⟩
  apply (lowerHomEquiv X).injective
  rw [lowerHomEquiv_precomp]
  simpa using hf

/-- At a finite stage, solidification followed by the right-Kan counit is the identity.
This is the exact triangle needed to lift finite-quotient lower-Hom maps through
`profiniteSolidification`. -/
@[reassoc]
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

/-- Explicit extension of a finite-stage lower-Hom map across solidification. -/
noncomputable def finiteStageExtension (X : Profinite.{u}) (j : DiscreteQuotient X)
    (gQ : LowerHom (X.diagram.obj j)) :
    (Condensed.profiniteSolid R).obj X ⟶ coefficientObject :=
  (Condensed.profiniteSolid R).map (X.asLimitCone.π.app j) ≫
    (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ gQ

/-- The explicit finite-stage extension restricts to the original finite-stage map. -/
theorem finiteStageExtension_precomp (X : Profinite.{u}) (j : DiscreteQuotient X)
    (gQ : LowerHom (X.diagram.obj j)) :
    (Condensed.profiniteSolidification R).app X ≫ finiteStageExtension X j gQ =
      (Condensed.profiniteFree R).map (X.asLimitCone.π.app j) ≫ gQ := by
  change
    (Condensed.profiniteSolidification R).app X ≫
          (Condensed.profiniteSolid R).map (X.asLimitCone.π.app j) ≫
          (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ gQ = _
  rw [← (Condensed.profiniteSolidification R).naturality_assoc,
    finiteSolidification_counit_assoc]

/-- G1b: every lower-Hom morphism into the discrete coefficient object extends across
`profiniteSolidification`. This certifies the surjective half of the residual Hom theorem. -/
theorem coefficient_homPrecomp_surjective (X : Profinite.{u}) :
    Function.Surjective
      (CMDG.CondensedCM4P3D.homPrecomp coefficientObject X) := by
  intro g
  obtain ⟨j, gQ, hg⟩ := lowerHom_factors_finite X g
  refine ⟨finiteStageExtension X j gQ, ?_⟩
  change
    (Condensed.profiniteSolidification R).app X ≫ finiteStageExtension X j gQ = g
  rw [finiteStageExtension_precomp]
  exact hg.symm

/-- The exact remaining theorem after G1: maps out of the solid/measure object into the
discrete coefficient object are determined by their restriction along solidification. -/
def CoefficientMappingOutInjectivity : Prop :=
  ∀ X : Profinite.{u}, Function.Injective
    (CMDG.CondensedCM4P3D.homPrecomp coefficientObject X)

/-- Once G1 is available, the protected coefficient residual is equivalent to the single
mapping-out injectivity statement. -/
theorem coefficientResidualHomTheorem_iff_injectivity :
    CMDG.CondensedCM4P3D.CoefficientResidualHomTheorem ↔
      CoefficientMappingOutInjectivity := by
  constructor
  · intro h X
    exact (h X).1
  · intro h X
    exact ⟨h X, coefficient_homPrecomp_surjective X⟩

/-- Consequently, protected coefficient solidity itself is now equivalent to the same
mapping-out injectivity statement. -/
theorem coefficientIsSolid_iff_injectivity :
    CondensedMod.IsSolid R coefficientObject ↔ CoefficientMappingOutInjectivity := by
  rw [← CMDG.CondensedCM4P3D.coefficientResidualHomTheorem_iff_isSolid]
  exact coefficientResidualHomTheorem_iff_injectivity

#check lowerHomSectionsEquiv
#check lowerHomEquiv
#check lowerHomEquiv_precomp
#check lowerHom_factors_finite
#check finiteSolidification_counit
#check finiteStageExtension
#check finiteStageExtension_precomp
#check coefficient_homPrecomp_surjective
#check coefficientResidualHomTheorem_iff_injectivity
#check coefficientIsSolid_iff_injectivity
#check Profinite.exists_locallyConstant
#check Condensed.isColimitLocallyConstantPresheafDiagram
#check Functor.liftOfIsRightKanExtension_fac_app

#print axioms lowerHomSectionsEquiv
#print axioms lowerHomEquiv
#print axioms lowerHomEquiv_precomp
#print axioms lowerHom_factors_finite
#print axioms finiteSolidification_counit
#print axioms finiteStageExtension_precomp
#print axioms coefficient_homPrecomp_surjective
#print axioms coefficientResidualHomTheorem_iff_injectivity
#print axioms coefficientIsSolid_iff_injectivity

end CMDG.CondensedCM4P3G
