import CMDGCondensedCM4P3GPointFunctional

namespace CMDG.CondensedCM4P3M.KernelPointBridge

universe u

open CategoryTheory Limits Opposite
open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.PointFunctional
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3L.KernelFunctional
open CMDG.CondensedCM4P2E.RightKanReconstruction

theorem weightedFiniteBooleanMeasureLimitLift_allTrue_realizes_point
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    (freeHomSectionsEquiv (Profinite.of PUnit.{u + 1})
      (CMDG.CondensedCM4P2D.measureFunctor.obj X)).symm μ =
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
          (basisBooleanPointProbe X (fun _ => true)) ≫
        weightedFiniteBooleanMeasureLimitLift X
          (fun i => measurePointIntegralFunctional X μ (integralBasis X i)) := by
  let P := Profinite.of PUnit.{u + 1}
  let T := basisBooleanCube X
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj X
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let a : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  let μHom := (freeHomSectionsEquiv P A).symm μ
  change μHom =
    (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
      weightedFiniteBooleanMeasureLimitLift X a
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  let Aj := CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j)
  let qj := finiteQuotientMap X j
  let U := op ((profiniteToCompHaus).obj P)
  let ftrue := ((profiniteToCompHaus).map qtrue).op
  have hpost :
      ∀ {B C : CondensedMod.{u} CMDG.CondensedCM4P3G.R.{u}}
        (g : (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).obj P ⟶ B)
        (h : B ⟶ C),
        freeHomSectionsEquiv P C (g ≫ h) =
          (ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map h).hom.app U))
            (freeHomSectionsEquiv P B g) := by
    intro B C g h
    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
          ((profiniteToCondensed).obj P) C (g ≫ h)) = _
    rw [Adjunction.homEquiv_naturality_right]
    rfl
  have hfinite :
      μHom ≫ CMDG.CondensedCM4P2D.measureFunctor.map qj =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureHom X a j := by
    apply (freeHomSectionsEquiv P Aj).injective
    rw [hpost]
    have hmu : freeHomSectionsEquiv P A μHom = μ := by
      exact Equiv.apply_symm_apply _ _
    rw [hmu]
    rw [freeHomSectionsEquiv_precomp]
    have hsec :
        freeHomSectionsEquiv T Aj
          (weightedFiniteBooleanMeasureHom X a j) =
        weightedFiniteBooleanMeasureSection X a j := by
      exact Equiv.apply_symm_apply _ _
    rw [hsec]
    change
      ((CMDG.CondensedCM4P2D.measureFunctor.map qj).hom.app (op Point)) μ =
        (ConcreteCategory.hom
          ((measurePresheafObj (X.diagram.obj j)).map ftrue))
          (weightedFiniteBooleanMeasureSection X a j)
    symm
    simpa [qj, qtrue, a, ftrue] using
      weightedFiniteBooleanMeasureSection_allTrue_realizes_pushforward X μ j
  have hfac :=
    weightedFiniteBooleanMeasureLimitLift_fac X a j
  change
    μHom ≫ CMDG.CondensedCM4P2D.measureFunctor.map qj =
      ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
        weightedFiniteBooleanMeasureLimitLift X a) ≫
          CMDG.CondensedCM4P2D.measureFunctor.map qj
  rw [Category.assoc, hfac]
  exact hfinite

end CMDG.CondensedCM4P3M.KernelPointBridge
