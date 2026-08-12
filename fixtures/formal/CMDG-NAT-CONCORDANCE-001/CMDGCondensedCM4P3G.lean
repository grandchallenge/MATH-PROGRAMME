import CMDGCondensedCM4P3D
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.AsLimit

/-!
# CMDG CM4-P3-G — coefficient finite-stage mapping-out attack

This fixture attacks the single coefficient-object residual left by protected P3-D.
It identifies lower Hom with locally constant coefficient functions, proves finite-quotient
factorization on the lower/free side, constructs the corresponding finite-stage extension on
the solid side, and proves surjectivity of coefficient solidification precomposition.

The sole deliberately unproved proposition introduced below is
`CoefficientFiniteStageMappingOut`: every morphism from `profiniteSolid X` to the discrete
coefficient object is already represented at one finite quotient stage. No coefficient solidity
or injectivity theorem is assumed.
-/

namespace CMDG.CondensedCM4P3G

universe u

open CategoryTheory Limits Opposite

abbrev R := CMDG.CondensedCM4P3D.R.{u}

noncomputable abbrev coefficientObject : CondensedMod.{u} R :=
  CMDG.CondensedCM4P3D.coefficientObject.{u}

abbrev LowerHom (X : Profinite.{u}) :=
  (Condensed.profiniteFree R).obj X ⟶ coefficientObject

abbrev CoefficientSections (X : Profinite.{u}) :=
  ((Condensed.forget R).obj coefficientObject).obj.obj
    (op ((profiniteToCompHaus).obj X))

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

noncomputable def lowerHomEquiv (X : Profinite.{u}) :
    LowerHom X ≃ LocallyConstant X R := by
  exact lowerHomSectionsEquiv X

/-- A transparent application formula for the composite adjunction/Yoneda equivalence. -/
theorem lowerHomSectionsEquiv_apply (X : Profinite.{u}) (g : LowerHom X) :
    lowerHomSectionsEquiv X g =
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction R).homEquiv
          ((profiniteToCondensed).obj X) coefficientObject g) := by
  rfl

/-- The categorical part of lower-Hom naturality, before unfolding the concrete
locally-constant coefficient presheaf. -/
theorem lowerHomSectionsEquiv_precomp {X Y : Profinite.{u}}
    (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomSectionsEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      ((Condensed.forget R).obj coefficientObject).obj.map
        ((profiniteToCompHaus).map q).op (lowerHomSectionsEquiv Y g) := by
  rw [lowerHomSectionsEquiv_apply X, lowerHomSectionsEquiv_apply Y]
  have hfree :
      (Condensed.profiniteFree R).map q =
        (Condensed.free R).map ((profiniteToCondensed).map q) := by
    rfl
  rw [hfree]
  rw [(Condensed.freeForgetAdjunction R).homEquiv_naturality_left]
  simpa [GrothendieckTopology.uliftYoneda, profiniteToCondensed,
    compHausToCondensed, compHausToCondensed', Condensed.ulift, Functor.comp_map] using
    ((coherentTopology CompHaus.{u}).uliftYonedaEquiv_naturality
      ((Condensed.freeForgetAdjunction R).homEquiv
        ((profiniteToCondensed).obj Y) coefficientObject g)
      ((profiniteToCompHaus).map q)).symm

/-- Naturality of G0: precomposition along a profinite map is exactly restriction of
locally constant functions. -/
theorem lowerHomEquiv_precomp {X Y : Profinite.{u}} (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      (lowerHomEquiv Y g).comap q.hom.hom := by
  change lowerHomSectionsEquiv X ((Condensed.profiniteFree R).map q ≫ g) = _
  rw [lowerHomSectionsEquiv_precomp]
  rfl

/-- The canonical projection from a profinite space to one of its finite discrete quotients. -/
noncomputable def finiteQuotientMap (X : Profinite.{u}) (j : DiscreteQuotient X) :
    X ⟶ X.diagram.obj j :=
  X.asLimitCone.π.app j

theorem finiteQuotientMap_surjective (X : Profinite.{u}) (j : DiscreteQuotient X) :
    Function.Surjective (finiteQuotientMap X j).hom.hom := by
  change Function.Surjective j.proj
  exact j.proj_surjective

/-- Every lower/free-side coefficient morphism already factors through one finite quotient. -/
theorem lowerHom_factors_finite (X : Profinite.{u}) (g : LowerHom X) :
    ∃ (j : DiscreteQuotient X) (gQ : LowerHom (X.diagram.obj j)),
      g = (Condensed.profiniteFree R).map (finiteQuotientMap X j) ≫ gQ := by
  obtain ⟨j, fQ, hf⟩ :=
    Profinite.exists_locallyConstant X.asLimitCone X.asLimit (lowerHomEquiv X g)
  refine ⟨j, (lowerHomEquiv (X.diagram.obj j)).symm fQ, ?_⟩
  apply (lowerHomEquiv X).injective
  rw [lowerHomEquiv_precomp]
  simpa [finiteQuotientMap] using hf

/-- Precomposition on lower Hom is injective along any surjective profinite map. -/
theorem lowerHom_precomp_injective_of_surjective {X Y : Profinite.{u}}
    (q : X ⟶ Y) (hq : Function.Surjective q.hom.hom) :
    Function.Injective
      (fun g : LowerHom Y => (Condensed.profiniteFree R).map q ≫ g) := by
  intro g₁ g₂ h
  apply (lowerHomEquiv Y).injective
  apply LocallyConstant.comap_injective q.hom.hom hq
  rw [← lowerHomEquiv_precomp q g₁, ← lowerHomEquiv_precomp q g₂]
  exact congrArg (lowerHomEquiv X) h

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

/-- Extend a lower morphism defined on one finite quotient stage to the right-Kan/solid object. -/
noncomputable def finiteStageExtension
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (gQ : LowerHom (X.diagram.obj j)) :
    (Condensed.profiniteSolid R).obj X ⟶ coefficientObject :=
  (Condensed.profiniteSolid R).map (finiteQuotientMap X j) ≫
    (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ gQ

/-- The finite-stage extension is a genuine lift of the corresponding lower/free-side morphism. -/
theorem finiteStageExtension_precomp
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (gQ : LowerHom (X.diagram.obj j)) :
    (Condensed.profiniteSolidification R).app X ≫ finiteStageExtension X j gQ =
      (Condensed.profiniteFree R).map (finiteQuotientMap X j) ≫ gQ := by
  unfold finiteStageExtension
  rw [← (Condensed.profiniteSolidification R).naturality_assoc]
  rw [finiteSolidification_counit_assoc]

/-- The coefficient precomposition map is already surjective; only injectivity remains. -/
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

/-- The exact remaining mathematical boundary: every solid-side coefficient morphism is already
visible at one finite discrete quotient stage. This proposition is deliberately not asserted. -/
def CoefficientFiniteStageMappingOut : Prop :=
  ∀ (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject),
    ∃ (j : DiscreteQuotient X) (gQ : LowerHom (X.diagram.obj j)),
      h = finiteStageExtension X j gQ

#check lowerHomSectionsEquiv
#check lowerHomEquiv
#check lowerHomEquiv_precomp
#check finiteQuotientMap_surjective
#check lowerHom_factors_finite
#check lowerHom_precomp_injective_of_surjective
#check finiteSolidification_counit
#check finiteStageExtension_precomp
#check coefficient_homPrecomp_surjective
#check CoefficientFiniteStageMappingOut

#print axioms lowerHomEquiv
#print axioms lowerHomEquiv_precomp
#print axioms finiteQuotientMap_surjective
#print axioms lowerHom_factors_finite
#print axioms lowerHom_precomp_injective_of_surjective
#print axioms finiteSolidification_counit
#print axioms finiteStageExtension_precomp
#print axioms coefficient_homPrecomp_surjective

end CMDG.CondensedCM4P3G
