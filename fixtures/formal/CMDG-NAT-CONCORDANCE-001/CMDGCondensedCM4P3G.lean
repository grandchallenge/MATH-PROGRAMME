import CMDGCondensedCM4P3D
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.AsLimit

/-!
# CMDG CM4-P3-G — coefficient mapping-out attack

This fixture attacks the single coefficient-object residual left by protected P3-D.
It starts from the machine-certified lower-Hom identification, then certifies the
naturality needed for finite-quotient factorization. No coefficient solidity or
injectivity theorem is assumed.

The present head separates categorical section-level naturality from the final
`LocallyConstant.comap` definitional reduction.
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

/-- The categorical part of lower-Hom naturality, before unfolding the concrete
locally-constant coefficient presheaf. -/
theorem lowerHomSectionsEquiv_precomp {X Y : Profinite.{u}}
    (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomSectionsEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      ((Condensed.forget R).obj coefficientObject).obj.map
        ((profiniteToCompHaus).map q).op (lowerHomSectionsEquiv Y g) := by
  change
    (coherentTopology CompHaus.{u}).uliftYonedaEquiv
      ((Condensed.freeForgetAdjunction R).homEquiv
        ((profiniteToCondensed).obj X) coefficientObject
        ((Condensed.free R).map ((profiniteToCondensed).map q) ≫ g)) = _
  rw [(Condensed.freeForgetAdjunction R).homEquiv_naturality_left]
  simpa [lowerHomSectionsEquiv, GrothendieckTopology.uliftYoneda,
    profiniteToCondensed, compHausToCondensed, compHausToCondensed',
    Condensed.ulift, Functor.comp_map] using
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

#check lowerHomSectionsEquiv
#check lowerHomEquiv
#check lowerHomSectionsEquiv_precomp
#check lowerHomEquiv_precomp
#check finiteSolidification_counit

#print axioms lowerHomSectionsEquiv
#print axioms lowerHomEquiv
#print axioms lowerHomSectionsEquiv_precomp
#print axioms lowerHomEquiv_precomp
#print axioms finiteSolidification_counit

end CMDG.CondensedCM4P3G
