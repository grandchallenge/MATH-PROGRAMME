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
  let ftrue := ((profiniteToCompHaus).map qtrue).op
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
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      simpa [qj, qtrue, a, ftrue] using
        weightedFiniteBooleanMeasureSection_allTrue_realizes_pushforward X μ j
  have hfac :=
    weightedFiniteBooleanMeasureLimitLift_fac X a j
  have hleft := congrArg
    (fun g =>
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫ g)
    hfac
  have hfiniteCone :
      μHom ≫ (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureHom X a j := by
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      simpa [qj, finiteQuotientMap] using hfinite
  calc
    μHom ≫ (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureHom X a j := hfiniteCone
    _ =
        ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureLimitLift X a) ≫
            (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j := by
              set_option backward.defeqAttrib.useBackward true in
              set_option backward.isDefEq.respectTransparency false in
                simpa only [Category.assoc] using hleft.symm

/-- Evaluating an arbitrary Point measure section through the solid comparison and a coefficient
morphism is exactly the product functional of its Nöbeling coordinate vector. -/
theorem applied_d_point_kernelProductFunctional
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (μ : (measurePresheafObj X).obj (op Point)) :
    ((show LocallyConstant (Profinite.of PUnit.{u + 1}) CMDG.CondensedCM4P3G.R.{u} from
        (ConcreteCategory.hom
          (d.hom.app
            (op ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1})))))
          ((ConcreteCategory.hom
            ((CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X).hom.app
              (op ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1}))))) μ))
        PUnit.unit).down =
      kernelProductFunctional X d
        (fun i => measurePointIntegralFunctional X μ (integralBasis X i)) := by
  let P := Profinite.of PUnit.{u + 1}
  let T := basisBooleanCube X
  let U := op ((profiniteToCompHaus).obj P)
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj X
  let E :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let ftrue := ((profiniteToCompHaus).map qtrue).op
  let a : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  let μHom := (freeHomSectionsEquiv P A).symm μ
  have hglobal :=
    weightedFiniteBooleanMeasureLimitLift_allTrue_realizes_point X μ
  have hmor := congrArg
    (fun g => g ≫ E ≫ d) hglobal
  have hmor' :
      μHom ≫ E ≫ d =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          (weightedFiniteBooleanMeasureLimitLift X a ≫ E ≫ d) := by
    simpa [P, A, E, qtrue, a, μHom, Category.assoc] using hmor
  have hs := congrArg
    (fun g => freeHomSectionsEquiv P coefficientObject g) hmor'
  have hleft :
      freeHomSectionsEquiv P coefficientObject (μHom ≫ E ≫ d) =
        (d.hom.app U) ((E.hom.app U) μ) := by
    change
      freeHomSectionsEquiv P coefficientObject (μHom ≫ (E ≫ d)) =
        (d.hom.app U) ((E.hom.app U) μ)
    have hpost :
        freeHomSectionsEquiv P coefficientObject (μHom ≫ (E ≫ d)) =
          (ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map (E ≫ d)).hom.app U))
            (freeHomSectionsEquiv P A μHom) := by
      change
        (coherentTopology CompHaus.{u}).uliftYonedaEquiv
          ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
            ((profiniteToCondensed).obj P) coefficientObject (μHom ≫ (E ≫ d))) = _
      rw [Adjunction.homEquiv_naturality_right]
      rfl
    rw [hpost]
    have hmu :
        freeHomSectionsEquiv P A μHom =
          (show A.obj.obj U from μ) := by
      dsimp [μHom]
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        simpa [P, A, U] using (Equiv.apply_symm_apply (freeHomSectionsEquiv P A) μ)
    rw [hmu]
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      rfl
  rw [hleft] at hs
  have hpre :=
    freeHomSectionsEquiv_precomp qtrue coefficientObject
      (weightedFiniteBooleanMeasureLimitLift X a ≫ E ≫ d)
  rw [hpre] at hs
  have hkernel :
      freeHomSectionsEquiv T coefficientObject
          (weightedFiniteBooleanMeasureLimitLift X a ≫ E ≫ d) =
        kernelProductSection X d a := by
    rfl
  rw [hkernel] at hs
  have hsPoint := congrArg
    (fun f : LocallyConstant P CMDG.CondensedCM4P3G.R.{u} => f PUnit.unit) hs
  have hpull :
      ((show LocallyConstant P CMDG.CondensedCM4P3G.R.{u} from
        (ConcreteCategory.hom
          (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).obj coefficientObject).obj.map ftrue))
          (kernelProductSection X d a)) PUnit.unit) =
        kernelProductSection X d a (fun _ => true) := by
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      rfl
  rw [kernelProductFunctional_apply]
  have hsDown := congrArg ULift.down hsPoint
  rw [hpull] at hsDown
  set_option backward.defeqAttrib.useBackward true in
  set_option backward.isDefEq.respectTransparency false in
    simpa [P, U, E, qtrue, ftrue, a] using hsDown

/-- Zero product-functional data forces the coefficient morphism to vanish at the canonical
one-point profinite test object. -/
theorem canonicalPointComponent_eq_zero_of_kernelProductFunctional_eq_zero
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hk : kernelProductFunctional X d = 0) :
    d.hom.app
      (op ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1}))) = 0 := by
  let P := Profinite.of PUnit.{u + 1}
  let U := op ((profiniteToCompHaus).obj P)
  let e :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.app X
  let eU :
      (CMDG.CondensedCM4P2D.measureFunctor.obj X).obj.obj U ≅
        ((Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X).obj.obj U := {
    hom := e.hom.hom.app U
    inv := e.inv.hom.app U
    hom_inv_id := by
      exact congrArg (fun k => k.hom.app U) e.hom_inv_id
    inv_hom_id := by
      exact congrArg (fun k => k.hom.app U) e.inv_hom_id }
  let dU :
      ((Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X).obj.obj U ⟶
        ModuleCat.of CMDG.CondensedCM4P3G.R.{u}
          (LocallyConstant U.unop CMDG.CondensedCM4P3G.R.{u}) := by
    exact d.hom.app U
  apply ModuleCat.hom_injective
  apply LinearMap.ext
  intro s
  set_option backward.defeqAttrib.useBackward true in
  set_option backward.isDefEq.respectTransparency false in
    change
      dU s = (0 : LocallyConstant U.unop CMDG.CondensedCM4P3G.R.{u})
  apply LocallyConstant.ext
  intro z
  let z0 : U.unop := by
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      exact PUnit.unit
  have hz : z = z0 := by
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      change (show PUnit.{u + 1} from z) = (show PUnit.{u + 1} from z0)
    exact Subsingleton.elim _ _
  rw [hz]
  let μ : (measurePresheafObj X).obj U :=
    (ConcreteCategory.hom eU.inv) s
  let aμ : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  have heval' :
      (ConcreteCategory.hom eU.hom) μ = s := by
    have h := ConcreteCategory.congr_hom eU.inv_hom_id s
    simpa [μ, ConcreteCategory.comp_apply] using h
  have hcompat := applied_d_point_kernelProductFunctional X d μ
  have hk0raw := congrArg
    (fun F : (IntegralBasisIndex X → ℤ) →+ ℤ => F aμ) hk
  have hk0 : kernelProductFunctional X d aμ = 0 := by
    simpa using hk0raw
  apply ULift.ext
  change
    ((dU s) z0).down = 0
  rw [← heval']
  set_option backward.defeqAttrib.useBackward true in
  set_option backward.isDefEq.respectTransparency false in
    change
      ((show LocallyConstant P CMDG.CondensedCM4P3G.R.{u} from
        (ConcreteCategory.hom (d.hom.app U))
          ((ConcreteCategory.hom (e.hom.hom.app U)) μ)) PUnit.unit).down = 0
  exact hcompat.trans hk0

/-- The product-functional representation reflects zero on solid-side coefficient morphisms. -/
theorem eq_zero_of_kernelProductFunctional_eq_zero
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hk : kernelProductFunctional X d = 0) :
    d = 0 := by
  apply CMDG.CondensedCM4P3G.coefficient_hom_ext_point
  have hc :=
    canonicalPointComponent_eq_zero_of_kernelProductFunctional_eq_zero X d hk
  set_option backward.defeqAttrib.useBackward true in
  set_option backward.isDefEq.respectTransparency false in
    simpa [CMDG.CondensedCM4P3G.Point] using hc

/-- A coefficient morphism in the kernel of profinite solidification is zero. -/
theorem eq_zero_of_solidification_kernel
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hd :
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ d = 0) :
    d = 0 := by
  apply eq_zero_of_kernelProductFunctional_eq_zero X d
  exact kernelProductFunctional_eq_zero_of_solidification_kernel X d hd

end CMDG.CondensedCM4P3M.KernelPointBridge
