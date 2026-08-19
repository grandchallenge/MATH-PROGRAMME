import CMDGCondensedCM4P3GFiniteBooleanCoefficientPushforward

/-!
# CMDG CM4-P3-H finite-stage Boolean measure morphisms

This fixture packages each concrete finite Boolean measure section through the generic
profinite-free/section equivalence and proves that the resulting condensed-module morphisms are
covariantly compatible under refinement of finite quotients.

This remains a finite-stage compatibility statement. No right-Kan cone, mapping-out injectivity,
coefficient-object solidity, or global CMDG completeness claim is asserted here.
-/

namespace CMDG.CondensedCM4P3G.FiniteBooleanMeasureHom

universe u

open CategoryTheory Opposite

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.FiniteBooleanCoefficientPushforward

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The finite-stage universal Boolean measure family as a condensed-module morphism. -/
noncomputable def finiteBooleanMeasureHom
    (X : Profinite.{u}) (j : DiscreteQuotient X) :
    (Condensed.profiniteFree R).obj (basisBooleanCube X) ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j) :=
  (freeHomSectionsEquiv
      (basisBooleanCube X)
      (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j))).symm
    (finiteBooleanMeasureSection X j)

/-- P3-H target theorem. The packaged finite Boolean measure morphisms commute with finite-quotient
refinement. -/
theorem finiteBooleanMeasureHom_pushforward
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) :
    finiteBooleanMeasureHom X j ≫
        CMDG.CondensedCM4P2D.measureFunctor.map (X.diagram.map f) =
      finiteBooleanMeasureHom X k := by
  let T := basisBooleanCube X
  let S := op ((profiniteToCompHaus).obj T)

  have hpost :
      ∀ {A B : CondensedMod.{u} R}
        (g : (Condensed.profiniteFree R).obj T ⟶ A)
        (h : A ⟶ B),
        freeHomSectionsEquiv T B (g ≫ h) =
          (ConcreteCategory.hom
            (((Condensed.forget R).map h).hom.app S))
            (freeHomSectionsEquiv T A g) := by

    intro A B g h

    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction R).homEquiv
          ((profiniteToCondensed).obj T)
          B
          (g ≫ h)) =
        _

    rw [Adjunction.homEquiv_naturality_right]

    rfl

  have hj :
      freeHomSectionsEquiv
          (basisBooleanCube X)
          (CMDG.CondensedCM4P2D.measureFunctor.obj
            (X.diagram.obj j))
          (finiteBooleanMeasureHom X j) =
        finiteBooleanMeasureSection X j := by
    exact Equiv.apply_symm_apply _ _

  have hk :
      freeHomSectionsEquiv
          (basisBooleanCube X)
          (CMDG.CondensedCM4P2D.measureFunctor.obj
            (X.diagram.obj k))
          (finiteBooleanMeasureHom X k) =
        finiteBooleanMeasureSection X k := by
    exact Equiv.apply_symm_apply _ _

  apply
    (freeHomSectionsEquiv
      (basisBooleanCube X)
      (CMDG.CondensedCM4P2D.measureFunctor.obj
        (X.diagram.obj k))).injective

  rw [
    hpost
      (g := finiteBooleanMeasureHom X j)
      (h :=
        CMDG.CondensedCM4P2D.measureFunctor.map
          (X.diagram.map f)),
    hj,
    hk
  ]

  have hforget :
      (ConcreteCategory.hom
        (((Condensed.forget R).map
          (CMDG.CondensedCM4P2D.measureFunctor.map
            (X.diagram.map f))).hom.app
          (op
            ((profiniteToCompHaus).obj
              (basisBooleanCube X)))))
        (finiteBooleanMeasureSection X j) =
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2D.measureFunctor.map
          (X.diagram.map f)).hom.app
          (op
            ((profiniteToCompHaus).obj
              (basisBooleanCube X)))))
        (finiteBooleanMeasureSection X j) := by
    rfl

  rw [hforget]

  exact finiteBooleanMeasureSection_pushforward X f


#print finiteBooleanMeasureHom
#print axioms finiteBooleanMeasureHom
#check finiteBooleanMeasureHom_pushforward
#print axioms finiteBooleanMeasureHom_pushforward

end CMDG.CondensedCM4P3G.FiniteBooleanMeasureHom
