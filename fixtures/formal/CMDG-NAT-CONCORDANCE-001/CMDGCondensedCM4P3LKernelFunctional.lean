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
open CMDG.CondensedCM4P3G.FiniteSupport
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
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

/-- The free/section equivalence is natural under precomposition in the profinite source. -/
theorem freeHomSectionsEquiv_precomp
    {T U : Profinite.{u}}
    (q : T ⟶ U) (A : CondensedMod.{u} R)
    (g : (Condensed.profiniteFree R).obj U ⟶ A) :
    freeHomSectionsEquiv T A ((Condensed.profiniteFree R).map q ≫ g) =
      ((Condensed.forget R).obj A).obj.map
        ((profiniteToCompHaus).map q).op (freeHomSectionsEquiv U A g) := by
  change
    (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction R).homEquiv
          ((profiniteToCondensed).obj T) A
          ((Condensed.profiniteFree R).map q ≫ g)) = _
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
        ((profiniteToCondensed).obj U) A g)
      ((profiniteToCompHaus).map q)).symm

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

/-- The one-point profinite probe selecting a Boolean basis-coordinate vector. -/
noncomputable def basisBooleanPointProbe
    (X : Profinite.{u}) (t : IntegralBasisIndex X → Bool) :
    Profinite.of PUnit.{u} ⟶ basisBooleanCube X :=
  ConcreteCategory.ofHom
    { toFun := fun _ => t
      continuous_toFun := continuous_const }

/-- Pulling a finite weighted coefficient family to the selected one-point probe is the same as
pulling the selector-reweighted family to the all-true probe. -/
theorem weightedFiniteBooleanCoefficientFamily_point_reweight
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X)
    (t : IntegralBasisIndex X → Bool) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf
        (FiniteQuotientObject X j)).map
        ((profiniteToCompHaus).map (basisBooleanPointProbe X t)).op))
      (weightedFiniteBooleanCoefficientFamily X a j) =
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf
        (FiniteQuotientObject X j)).map
        ((profiniteToCompHaus).map
          (basisBooleanPointProbe X (fun _ => true))).op))
      (weightedFiniteBooleanCoefficientFamily X (weightedBoolToInt a t) j) := by
  funext q
  apply LocallyConstant.ext
  intro z
  change
    weightedFiniteBooleanCoefficient X a j q t =
      weightedFiniteBooleanCoefficient X (weightedBoolToInt a t) j q
        (fun _ => true)
  exact weightedFiniteBooleanCoefficient_reweight_eval X a j q t

/-- Selector reweighting survives the two protected finite coefficient-to-measure transports. -/
theorem weightedFiniteBooleanMeasureSection_point_reweight
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X)
    (t : IntegralBasisIndex X → Bool) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2D.measurePresheafObj (X.diagram.obj j)).map
        ((profiniteToCompHaus).map (basisBooleanPointProbe X t)).op))
      (weightedFiniteBooleanMeasureSection X a j) =
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2D.measurePresheafObj (X.diagram.obj j)).map
        ((profiniteToCompHaus).map
          (basisBooleanPointProbe X (fun _ => true))).op))
      (weightedFiniteBooleanMeasureSection X (weightedBoolToInt a t) j) := by
  let Q := FiniteQuotientObject X j
  let S := op ((profiniteToCompHaus).obj (basisBooleanCube X))
  let P := Profinite.of PUnit.{u}
  let U := op ((profiniteToCompHaus).obj P)
  let qt := basisBooleanPointProbe X t
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let ft := ((profiniteToCompHaus).map qt).op
  let ftrue := ((profiniteToCompHaus).map qtrue).op
  let F := CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf Q
  let G := CMDG.CondensedCM4P2D.measurePresheafObj (X.diagram.obj j)
  let T :=
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso Q).inv ≫
      (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso Q).inv
  have hSection (w : IntegralBasisIndex X → ℤ) :
      (ConcreteCategory.hom (T.app S))
          (weightedFiniteBooleanCoefficientFamily X w j) =
        weightedFiniteBooleanMeasureSection X w j := by
    rfl
  have ht := ConcreteCategory.congr_hom
    (T.naturality ft) (weightedFiniteBooleanCoefficientFamily X a j)
  have htrue := ConcreteCategory.congr_hom
    (T.naturality ftrue)
      (weightedFiniteBooleanCoefficientFamily X (weightedBoolToInt a t) j)
  rw [hSection a] at ht
  rw [hSection (weightedBoolToInt a t)] at htrue
  have hcoeff := weightedFiniteBooleanCoefficientFamily_point_reweight X a j t
  have hmid := congrArg
    (fun c => (ConcreteCategory.hom (T.app U)) c) hcoeff
  exact ht.symm.trans (hmid.trans htrue)

/-- At every finite quotient, precomposing the weighted measure morphism with a selected Boolean
point agrees with precomposing the selector-reweighted morphism with the all-true point. -/
theorem weightedFiniteBooleanMeasureHom_point_reweight
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X)
    (t : IntegralBasisIndex X → Bool) :
    (Condensed.profiniteFree R).map (basisBooleanPointProbe X t) ≫
        weightedFiniteBooleanMeasureHom X a j =
      (Condensed.profiniteFree R).map
          (basisBooleanPointProbe X (fun _ => true)) ≫
        weightedFiniteBooleanMeasureHom X (weightedBoolToInt a t) j := by
  let P := Profinite.of PUnit.{u}
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j)
  apply (freeHomSectionsEquiv P A).injective
  rw [freeHomSectionsEquiv_precomp, freeHomSectionsEquiv_precomp]
  have ha :
      freeHomSectionsEquiv (basisBooleanCube X) A
          (weightedFiniteBooleanMeasureHom X a j) =
        weightedFiniteBooleanMeasureSection X a j := by
    exact Equiv.apply_symm_apply _ _
  have hb :
      freeHomSectionsEquiv (basisBooleanCube X) A
          (weightedFiniteBooleanMeasureHom X (weightedBoolToInt a t) j) =
        weightedFiniteBooleanMeasureSection X (weightedBoolToInt a t) j := by
    exact Equiv.apply_symm_apply _ _
  rw [ha, hb]
  exact weightedFiniteBooleanMeasureSection_point_reweight X a j t

/-- The selector identity lifts uniquely through the protected finite-quotient measure limit. -/
theorem weightedFiniteBooleanMeasureLimitLift_point_reweight
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (t : IntegralBasisIndex X → Bool) :
    (Condensed.profiniteFree R).map (basisBooleanPointProbe X t) ≫
        weightedFiniteBooleanMeasureLimitLift X a =
      (Condensed.profiniteFree R).map
          (basisBooleanPointProbe X (fun _ => true)) ≫
        weightedFiniteBooleanMeasureLimitLift X (weightedBoolToInt a t) := by
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  simp only [Category.assoc]
  rw [weightedFiniteBooleanMeasureLimitLift_fac,
    weightedFiniteBooleanMeasureLimitLift_fac]
  exact weightedFiniteBooleanMeasureHom_point_reweight X a j t

/-- Global selector reweighting for the coefficient section. -/
theorem kernelProductSection_reweight_eval_R
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject)
    (a : IntegralBasisIndex X → ℤ)
    (t : IntegralBasisIndex X → Bool) :
    kernelProductSection X h a t =
      kernelProductSection X h (weightedBoolToInt a t) (fun _ => true) := by
  let P := Profinite.of PUnit.{u}
  let qt := basisBooleanPointProbe X t
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let e :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X
  have hlimit := weightedFiniteBooleanMeasureLimitLift_point_reweight X a t
  have hcomp :
      (Condensed.profiniteFree R).map qt ≫
          (weightedFiniteBooleanMeasureLimitLift X a ≫ e ≫ h) =
        (Condensed.profiniteFree R).map qtrue ≫
          (weightedFiniteBooleanMeasureLimitLift X (weightedBoolToInt a t) ≫ e ≫ h) := by
    simpa only [Category.assoc] using congrArg (fun q => q ≫ e ≫ h) hlimit
  have hs := congrArg
    (fun q => freeHomSectionsEquiv P coefficientObject q) hcomp
  rw [freeHomSectionsEquiv_precomp, freeHomSectionsEquiv_precomp] at hs
  have hs' := congrArg
    (fun f : LocallyConstant P R => f PUnit.unit) hs
  change
    kernelProductSection X h a t =
      kernelProductSection X h (weightedBoolToInt a t) (fun _ => true) at hs'
  exact hs'

/-- Integer-valued selector reweighting for the product functional. -/
theorem kernelProductSection_reweight_eval
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject)
    (a : IntegralBasisIndex X → ℤ)
    (t : IntegralBasisIndex X → Bool) :
    (kernelProductSection X h a t).down =
      kernelProductFunctional X h (weightedBoolToInt a t) := by
  rw [kernelProductFunctional_apply]
  exact congrArg ULift.down (kernelProductSection_reweight_eval_R X h a t)

/-- The protected weighted Boolean compactness theorem supplies one finite coordinate kernel for
the global product functional. -/
theorem kernelProductFunctional_finite_coordinate_kernel
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject) :
    ∃ I : Finset (IntegralBasisIndex X),
      ∀ a : IntegralBasisIndex X → ℤ,
        (∀ i ∈ I, a i = 0) →
        kernelProductFunctional X h a = 0 := by
  apply finite_coordinate_dependence_of_weighted_bool_locallyConstant
  intro a
  let s : LocallyConstant (IntegralBasisIndex X → Bool) R := kernelProductSection X h a
  let f : LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
    (basisBooleanIntegralLiftEquiv X).symm s
  refine ⟨f, ?_⟩
  intro t
  change
    (kernelProductSection X h a t).down =
      kernelProductFunctional X h (weightedBoolToInt a t)
  exact kernelProductSection_reweight_eval X h a t

/-- Consequently the product functional depends on only finitely many basis coordinates. -/
theorem kernelProductFunctional_finite_coordinate_dependence
    (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject) :
    ∃ I : Finset (IntegralBasisIndex X),
      ∀ a b : IntegralBasisIndex X → ℤ,
        (∀ i ∈ I, a i = b i) →
        kernelProductFunctional X h a = kernelProductFunctional X h b := by
  obtain ⟨I, hI⟩ := kernelProductFunctional_finite_coordinate_kernel X h
  refine ⟨I, ?_⟩
  intro a b hab
  have hzero : kernelProductFunctional X h (a - b) = 0 := by
    apply hI
    intro i hi
    simp [hab i hi]
  rw [map_sub] at hzero
  exact sub_eq_zero.mp hzero

#check freeHomSectionsEquiv_add
#check freeHomSectionsEquiv_precomp
#check weightedFiniteBooleanMeasureHom_add
#check weightedFiniteBooleanMeasureLimitLift_add
#check kernelProductSection
#check kernelProductSection_add
#check kernelProductFunctional
#check kernelProductFunctional_apply
#check basisBooleanPointProbe
#check weightedFiniteBooleanCoefficientFamily_point_reweight
#check weightedFiniteBooleanMeasureSection_point_reweight
#check weightedFiniteBooleanMeasureHom_point_reweight
#check weightedFiniteBooleanMeasureLimitLift_point_reweight
#check kernelProductSection_reweight_eval_R
#check kernelProductSection_reweight_eval
#check kernelProductFunctional_finite_coordinate_kernel
#check kernelProductFunctional_finite_coordinate_dependence

#print axioms freeHomSectionsEquiv_add
#print axioms freeHomSectionsEquiv_precomp
#print axioms weightedFiniteBooleanMeasureHom_add
#print axioms weightedFiniteBooleanMeasureLimitLift_add
#print axioms kernelProductSection_add
#print axioms kernelProductFunctional
#print axioms weightedFiniteBooleanMeasureLimitLift_point_reweight
#print axioms kernelProductSection_reweight_eval
#print axioms kernelProductFunctional_finite_coordinate_kernel
#print axioms kernelProductFunctional_finite_coordinate_dependence

end CMDG.CondensedCM4P3L.KernelFunctional
