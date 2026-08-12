import CMDGCondensedCM4P3D
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.AsLimit

/-!
# CMDG CM4-P3-G — coefficient finite-stage mapping-out attack

This fixture attacks the single coefficient-object residual left by protected P3-D.
It retains the machine-certified lower-Hom naturality, identifies the canonical finite
quotient projections, and proves that every lower/free-side coefficient morphism factors
through one finite quotient. No coefficient solidity or solid-side mapping-out theorem is assumed.
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

theorem lowerHomSectionsEquiv_apply (X : Profinite.{u}) (g : LowerHom X) :
    lowerHomSectionsEquiv X g =
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction R).homEquiv
          ((profiniteToCondensed).obj X) coefficientObject g) := by
  rfl

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

theorem lowerHomEquiv_precomp {X Y : Profinite.{u}} (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      (lowerHomEquiv Y g).comap q.hom.hom := by
  change lowerHomSectionsEquiv X ((Condensed.profiniteFree R).map q ≫ g) = _
  rw [lowerHomSectionsEquiv_precomp]
  rfl

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

#check lowerHomEquiv_precomp
#check finiteQuotientMap
#check finiteQuotientMap_surjective
#check lowerHom_factors_finite
#check finiteSolidification_counit

#print axioms lowerHomEquiv_precomp
#print axioms finiteQuotientMap_surjective
#print axioms lowerHom_factors_finite
#print axioms finiteSolidification_counit

end CMDG.CondensedCM4P3G
