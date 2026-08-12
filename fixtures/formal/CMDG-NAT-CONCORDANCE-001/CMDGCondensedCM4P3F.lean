import CMDGCondensedCM4P3D
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.CofilteredLimit

/-!
# CMDG CM4-P3-F — coefficient-object solidity

This successor isolates the single coefficient-object residual left by P3-E.
The first certified layer identifies the lower Hom set with locally constant
lifted-integer-valued functions on the profinite source. The second layer
factors every such lower-Hom morphism through a canonical finite quotient.
No coefficient solidity or P3 availability is asserted by this file unless
and until the terminal declarations are proved.
-/

namespace CMDG.CondensedCM4P3F

universe u

open CategoryTheory Opposite

abbrev R := CMDG.CondensedCM4P3D.R.{u}

noncomputable abbrev coefficientObject : CondensedMod.{u} R :=
  CMDG.CondensedCM4P3D.coefficientObject.{u}

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

#check lowerHomAdjunctionEquiv
#check lowerHomYonedaEquiv
#check lowerHomEquiv
#check lowerHomYonedaEquiv_naturality
#check lowerHomEquiv_naturality
#check lowerHom_factors_finite

#print axioms lowerHomAdjunctionEquiv
#print axioms lowerHomYonedaEquiv
#print axioms lowerHomEquiv
#print axioms lowerHomYonedaEquiv_naturality
#print axioms lowerHomEquiv_naturality
#print axioms lowerHom_factors_finite

end CMDG.CondensedCM4P3F
