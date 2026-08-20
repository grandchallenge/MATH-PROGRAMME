import CMDGCondensedCM4P3KKernelFiniteDependence

/-!
# CMDG CM4-P3-L — global weighted kernel-functional bridge

This successor starts the passage from the protected finite weighted Boolean measure algebra to
an additive global weighted family.  The present boundary is deliberately narrow: transport
weight additivity through the free/section equivalence and then through the protected profinite
measure limit.  No mapping-out injectivity, coefficient-object solidity, or P3 completion is
asserted here.
-/

namespace CMDG.CondensedCM4P3L.KernelFunctional

universe u

open CategoryTheory Limits Opposite

open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3K.KernelFiniteDependence
open CMDG.CondensedCM4P2E.RightKanReconstruction

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The generic free/section equivalence preserves addition in the morphism variable. -/
theorem freeHomSectionsEquiv_add
    (T : Profinite.{u}) (A : CondensedMod.{u} R)
    (f g : (Condensed.profiniteFree R).obj T ⟶ A) :
    (show A.obj.obj (op ((profiniteToCompHaus).obj T)) from
      freeHomSectionsEquiv T A (f + g)) =
      (show A.obj.obj (op ((profiniteToCompHaus).obj T)) from
        freeHomSectionsEquiv T A f) +
        (show A.obj.obj (op ((profiniteToCompHaus).obj T)) from
          freeHomSectionsEquiv T A g) := by
  rfl

/-- The finite weighted measure morphism is additive in its external weight vector. -/
theorem weightedFiniteBooleanMeasureHom_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    weightedFiniteBooleanMeasureHom X (a + b) j =
      weightedFiniteBooleanMeasureHom X a j +
        weightedFiniteBooleanMeasureHom X b j := by
  let T := basisBooleanCube X
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j)
  let S := op ((profiniteToCompHaus).obj T)
  have hab :
      (show A.obj.obj S from
        freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X (a + b) j)) =
        (show A.obj.obj S from
          weightedFiniteBooleanMeasureSection X (a + b) j) := by
    exact Equiv.apply_symm_apply _ _
  have ha :
      (show A.obj.obj S from
        freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X a j)) =
        (show A.obj.obj S from
          weightedFiniteBooleanMeasureSection X a j) := by
    exact Equiv.apply_symm_apply _ _
  have hb :
      (show A.obj.obj S from
        freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X b j)) =
        (show A.obj.obj S from
          weightedFiniteBooleanMeasureSection X b j) := by
    exact Equiv.apply_symm_apply _ _
  have hsections :
      (show A.obj.obj S from
        weightedFiniteBooleanMeasureSection X (a + b) j) =
        (show A.obj.obj S from
          weightedFiniteBooleanMeasureSection X a j) +
          (show A.obj.obj S from
            weightedFiniteBooleanMeasureSection X b j) := by
    exact weightedFiniteBooleanMeasureSection_add X a b j
  have hsum :
      (show A.obj.obj S from
        freeHomSectionsEquiv T A
          (weightedFiniteBooleanMeasureHom X a j +
            weightedFiniteBooleanMeasureHom X b j)) =
        (show A.obj.obj S from
          freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X a j)) +
          (show A.obj.obj S from
            freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X b j)) := by
    exact freeHomSectionsEquiv_add T A
      (weightedFiniteBooleanMeasureHom X a j)
      (weightedFiniteBooleanMeasureHom X b j)
  have hadd :
      (show A.obj.obj S from
        freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X a j)) +
        (show A.obj.obj S from
          freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X b j)) =
      (show A.obj.obj S from
        weightedFiniteBooleanMeasureSection X a j) +
        (show A.obj.obj S from
          weightedFiniteBooleanMeasureSection X b j) := by
    exact congrArg₂ (fun x y : A.obj.obj S => x + y) ha hb
  apply (freeHomSectionsEquiv T A).injective
  exact hab.trans (hsections.trans (hadd.symm.trans hsum.symm))

/-- The canonical global weighted Boolean measure family is additive in the weight vector. -/
theorem weightedFiniteBooleanMeasureLimitLift_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ) :
    weightedFiniteBooleanMeasureLimitLift X (a + b) =
      weightedFiniteBooleanMeasureLimitLift X a +
        weightedFiniteBooleanMeasureLimitLift X b := by
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  have hab := weightedFiniteBooleanMeasureLimitLift_fac X (a + b) j
  have ha := weightedFiniteBooleanMeasureLimitLift_fac X a j
  have hb := weightedFiniteBooleanMeasureLimitLift_fac X b j
  have hsum := weightedFiniteBooleanMeasureHom_add X a b j
  have hcomp :
      (weightedFiniteBooleanMeasureLimitLift X a +
          weightedFiniteBooleanMeasureLimitLift X b) ≫
          (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
        (weightedFiniteBooleanMeasureLimitLift X a ≫
          (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j) +
        (weightedFiniteBooleanMeasureLimitLift X b ≫
          (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j) := by
    exact Preadditive.add_comp _ _ _ _ _ _
  exact
    hab.trans
      (hsum.trans
        ((congrArg₂ (· + ·) ha.symm hb.symm).trans hcomp.symm))

/-- The coefficient section obtained by sending a global weighted measure family through the
protected measure/solid comparison and then through a chosen solid-side coefficient morphism. -/
noncomputable def kernelProductSection
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject)
    (a : IntegralBasisIndex X → ℤ) :
    LocallyConstant (basisBooleanCube X) R := by
  exact
    freeHomSectionsEquiv (basisBooleanCube X) coefficientObject
      (weightedFiniteBooleanMeasureLimitLift X a ≫
        CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X ≫
        h)

/-- The global coefficient section is additive in the external weight vector. -/
theorem kernelProductSection_add
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject)
    (a b : IntegralBasisIndex X → ℤ) :
    kernelProductSection X h (a + b) =
      kernelProductSection X h a + kernelProductSection X h b := by
  let T := basisBooleanCube X
  let e :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X
  have hsum := weightedFiniteBooleanMeasureLimitLift_add X a b
  have he :
      (weightedFiniteBooleanMeasureLimitLift X a +
          weightedFiniteBooleanMeasureLimitLift X b) ≫ e =
        (weightedFiniteBooleanMeasureLimitLift X a ≫ e) +
          (weightedFiniteBooleanMeasureLimitLift X b ≫ e) := by
    exact Preadditive.add_comp _ _ _ _ _ _
  have hh :
      ((weightedFiniteBooleanMeasureLimitLift X a ≫ e) +
          (weightedFiniteBooleanMeasureLimitLift X b ≫ e)) ≫ h =
        (weightedFiniteBooleanMeasureLimitLift X a ≫ e ≫ h) +
          (weightedFiniteBooleanMeasureLimitLift X b ≫ e ≫ h) := by
    exact Preadditive.add_comp _ _ _ _ _ _
  have hcomp :
      weightedFiniteBooleanMeasureLimitLift X (a + b) ≫ e ≫ h =
        (weightedFiniteBooleanMeasureLimitLift X a ≫ e ≫ h) +
          (weightedFiniteBooleanMeasureLimitLift X b ≫ e ≫ h) := by
    exact
      (congrArg (fun q => q ≫ e ≫ h) hsum).trans
        ((congrArg (fun q => q ≫ h) he).trans hh)
  change
    (show coefficientObject.obj.obj (op ((profiniteToCompHaus).obj T)) from
      freeHomSectionsEquiv T coefficientObject
        (weightedFiniteBooleanMeasureLimitLift X (a + b) ≫ e ≫ h)) =
      (show coefficientObject.obj.obj (op ((profiniteToCompHaus).obj T)) from
        freeHomSectionsEquiv T coefficientObject
          (weightedFiniteBooleanMeasureLimitLift X a ≫ e ≫ h)) +
        (show coefficientObject.obj.obj (op ((profiniteToCompHaus).obj T)) from
          freeHomSectionsEquiv T coefficientObject
            (weightedFiniteBooleanMeasureLimitLift X b ≫ e ≫ h))
  exact
    (congrArg
      (fun q =>
        (show coefficientObject.obj.obj (op ((profiniteToCompHaus).obj T)) from
          freeHomSectionsEquiv T coefficientObject q))
      hcomp).trans
        (freeHomSectionsEquiv_add T coefficientObject _ _)

/-- All-true evaluation of the global weighted coefficient section, lowered back to integers,
forms an additive functional on the full integer product of basis weights. -/
noncomputable def kernelProductFunctional
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject) :
    (IntegralBasisIndex X → ℤ) →+ ℤ where
  toFun := fun a => (kernelProductSection X h a (fun _ => true)).down
  map_zero' := by
    let z := (kernelProductSection X h (0 : IntegralBasisIndex X → ℤ)
      (fun _ => true)).down
    change z = 0
    have hz0 :
        (kernelProductSection X h
          ((0 : IntegralBasisIndex X → ℤ) + 0) (fun _ => true)).down =
          (kernelProductSection X h (0 : IntegralBasisIndex X → ℤ)
            (fun _ => true)).down +
            (kernelProductSection X h (0 : IntegralBasisIndex X → ℤ)
              (fun _ => true)).down := by
      rw [kernelProductSection_add]
      rfl
    have hz : z = z + z := by
      simpa [z] using hz0
    have hz' : z + z = z + 0 :=
      hz.symm.trans (add_zero z).symm
    exact add_left_cancel hz'
  map_add' := by
    intro a b
    change
      (kernelProductSection X h (a + b) (fun _ => true)).down =
        (kernelProductSection X h a (fun _ => true)).down +
          (kernelProductSection X h b (fun _ => true)).down
    rw [kernelProductSection_add]
    rfl

@[simp]
theorem kernelProductFunctional_apply
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject)
    (a : IntegralBasisIndex X → ℤ) :
    kernelProductFunctional X h a =
      (kernelProductSection X h a (fun _ => true)).down := by
  rfl

#check freeHomSectionsEquiv_add
#check weightedFiniteBooleanMeasureHom_add
#check weightedFiniteBooleanMeasureLimitLift_add
#check kernelProductSection
#check kernelProductSection_add
#check kernelProductFunctional
#check kernelProductFunctional_apply

#print axioms freeHomSectionsEquiv_add
#print axioms weightedFiniteBooleanMeasureHom_add
#print axioms weightedFiniteBooleanMeasureLimitLift_add
#print axioms kernelProductSection_add
#print axioms kernelProductFunctional

end CMDG.CondensedCM4P3L.KernelFunctional
