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

/-- The protected finite-comparison tail sends the canonical small-free coordinate section at a
finite point to the section represented by the corresponding profinite point map. -/
theorem finiteComparisonTail_coordinateSection
    (Q : FintypeCat.{u}) (q : Q.obj) :
    let P := Profinite.of PUnit.{u + 1}
    let U := op ((profiniteToCompHaus).obj P)
    (ConcreteCategory.hom
      (((Condensed.forget R).map
        ((finiteComparisonTailNatIso.app Q).hom)).hom.app U))
      ((ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateInclusion Q q).app U))
        (1 : LocallyConstant P R)) =
      freeHomSectionsEquiv P ((Condensed.finFree R).obj Q)
        ((Condensed.profiniteFree R).map
          (profinitePointProbe (FintypeCat.toProfinite.obj Q) q)) := by
  simp [finiteComparisonTailNatIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso,
    CMDG.CondensedCM4P2E.finiteFreeDiscreteIso,
    CMDG.CondensedCM4P2E.discreteFreeIso,
    profinitePointProbe]

/-- After the complete protected finite comparison, the all-true pullback of the evaluation-weight
finite measure morphism is the free generator represented by the quotient point `j.proj x`. -/
theorem weightedFiniteBooleanMeasureHom_finiteComparison_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X) (j : DiscreteQuotient X) :
    (Condensed.profiniteFree R).map
          (basisBooleanPointProbe X (fun _ => true)) ≫
        weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j ≫
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom.app
          (FiniteQuotientObject X j) =
      (Condensed.profiniteFree R).map
        (profinitePointProbe (X.diagram.obj j) (j.proj x)) := by
  let P := Profinite.of PUnit.{u + 1}
  let T := basisBooleanCube X
  let Q := FiniteQuotientObject X j
  let U := op ((profiniteToCompHaus).obj P)
  let S := op ((profiniteToCompHaus).obj T)
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let w := weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j)
  let A0 := CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedFunctor.obj Q
  let B := (Condensed.finFree R).obj Q
  let i0 :=
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreeCondensedNatIso.app Q
  let it := finiteComparisonTailNatIso.app Q
  have hw : freeHomSectionsEquiv T A w =
      weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j := by
    exact Equiv.apply_symm_apply _ _
  have hnat := ConcreteCategory.congr_hom
    ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreePresheafNatIso
      (FiniteQuotientObject X j)).hom.naturality
      ((profiniteToCompHaus).map qtrue).op)
    (weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j)
  simp only [ConcreteCategory.comp_apply] at hnat
  have hdelta :=
    weightedFiniteBooleanMeasureSection_smallFree_evaluationWeight_allTrue X x j
  have htailNat := congrArg
    (fun t =>
      (ConcreteCategory.hom
        (((Condensed.forget R).map it.hom).hom.app U)) t)
    hnat
  have htailDelta := congrArg
    (fun t =>
      (ConcreteCategory.hom
        (((Condensed.forget R).map it.hom).hom.app U)) t)
    hdelta
  have hcoord := finiteComparisonTail_coordinateSection Q (j.proj x)
  apply (freeHomSectionsEquiv P B).injective
  change
    freeHomSectionsEquiv P B
      ((((Condensed.profiniteFree R).map qtrue ≫ w) ≫ i0.hom) ≫ it.hom) =
      freeHomSectionsEquiv P B
        ((Condensed.profiniteFree R).map
          (profinitePointProbe (FintypeCat.toProfinite.obj Q) (j.proj x)))
  rw [freeHomSectionsEquiv_postcomp P
      (((Condensed.profiniteFree R).map qtrue ≫ w) ≫ i0.hom) it.hom]
  rw [freeHomSectionsEquiv_postcomp P
      ((Condensed.profiniteFree R).map qtrue ≫ w) i0.hom]
  rw [freeHomSectionsEquiv_precomp qtrue A w, hw]
  exact htailNat.trans (htailDelta.trans hcoord)

#check profinitePointProbe
#check profinitePointProbe_comp_finiteQuotientMap
#check freeHomSectionsEquiv_postcomp
#check finiteComparisonTailNatIso
#check finiteComparisonTail_coordinateSection
#check weightedFiniteBooleanMeasureHom_finiteComparison_evaluationWeight_allTrue
#print axioms profinitePointProbe_comp_finiteQuotientMap
#print axioms freeHomSectionsEquiv_postcomp
#print axioms finiteComparisonTail_coordinateSection
#print axioms weightedFiniteBooleanMeasureHom_finiteComparison_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointVanishing
