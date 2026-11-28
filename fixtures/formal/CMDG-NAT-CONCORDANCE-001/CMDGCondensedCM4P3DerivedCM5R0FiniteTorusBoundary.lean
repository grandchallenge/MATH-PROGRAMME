import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCircleGroup
import CMDGCondensedCM4P3DerivedCM5R0RealCircleExtDimensionShift
import CMDGCondensedCM4P3DerivedCM5R0IntegerProductBridge
import Mathlib.CategoryTheory.Preadditive.Biproducts

/-! Scalar Ext of the genuine circle and integer products.
Only the universal finite-type resolution input remains explicit. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.FiniteTorusBoundary
open RealCircleStoneanPresheaf RealCircleSheafExact RealCircleExtDimensionShift
open RealCircleFiniteCoordinateNaturality BreenDeligneProbe IntegerProductBridge
open AcyclicResolution

theorem scalarProjective : Projective discreteIntegerCoeff.{u} := by
  letI : (Condensed.underlying (ModuleCat.{u+1} Coeff.{u})).PreservesEpimorphisms :=
    ⟨fun f => by
      intro hf
      apply (ModuleCat.epi_iff_surjective _).2
      exact (CondensedMod.epi_iff_surjective_on_stonean Coeff f).mp inferInstance
        (Stonean.of PUnit.{u+1})⟩
  have hP : Projective (ModuleCat.of Coeff.{u} Coeff.{u}) := by
    constructor
    intro E X g e he
    obtain ⟨x,hx⟩ := (ModuleCat.epi_iff_surjective e).1 he (g 1)
    let l : Coeff.{u} →ₗ[Coeff.{u}] E := LinearMap.toSpanSingleton Coeff E x
    refine ⟨ModuleCat.ofHom l,?_⟩
    apply ModuleCat.hom_ext
    apply LinearMap.ext_ring
    change e.hom (l 1) = g.hom 1
    rw [show l 1 = x from LinearMap.toSpanSingleton_apply_one Coeff E x]
    exact hx
  exact (CondensedMod.LocallyConstant.adjunction Coeff).map_projective
    (ModuleCat.of Coeff Coeff) hP

abbrev integers (I : Type u) := (realCircleCondensedSequence I).X₁

def finiteBicone (I : Type u) : Bicone (fun _ : I => discreteIntegerCoeff.{u}) :=
  Bicone.ofLimitCone (integerFanIsLimit I)

def finiteBilimit (I : Type u) [Fintype I] : (finiteBicone I).IsBilimit :=
  biconeIsBilimitOfLimitConeOfIsLimit (integerFanIsLimit I)

def finiteIntegerExt (I : Type u) [Fintype I] (q : ℕ) :
    Abelian.Ext (integers I) discreteIntegerCoeff q ≃+
      (I → Abelian.Ext discreteIntegerCoeff discreteIntegerCoeff q) :=
  Abelian.Ext.biproductAddEquiv (finiteBilimit I) discreteIntegerCoeff q

theorem finiteInteger_extPositive_zero (I : Type u) [Fintype I] (q : ℕ)
    (e : Abelian.Ext (integers I) discreteIntegerCoeff (q+1)) : e = 0 := by
  letI := scalarProjective.{u}
  apply (finiteIntegerExt I (q+1)).injective
  rw [map_zero]
  funext i
  exact Abelian.Ext.eq_zero_of_projective _

def boundaryEquiv (I : Type u) (B : UniversalBD.{u}) (q : ℕ) :
    Abelian.Ext (integers I) discreteIntegerCoeff q ≃+
      Abelian.Ext (circleProductCondensed I) discreteIntegerCoeff (q+1) :=
  AddEquiv.ofBijective (connecting I discreteIntegerCoeff q)
    (connecting_bijective_of_real_vanishes I discreteIntegerCoeff q
      (realGroup_extZero I B q) (realGroup_extZero I B (q+1)))

theorem boundary_natural (I J : Type u) (σ : J → I) (q : ℕ)
    (e : Abelian.Ext (integers J) discreteIntegerCoeff q) :
    pb discreteIntegerCoeff (circleReindex I J σ) (q+1) (connecting J discreteIntegerCoeff q e) =
      connecting I discreteIntegerCoeff q (pb discreteIntegerCoeff (integerReindex I J σ) q e) := by
  have h := ShortComplex.ShortExact.extClass_naturality
    (realCircleCondensedSequence_shortExact I) (realCircleCondensedSequence_shortExact J)
      (realCircleSequenceReindex I J σ)
  change (realCircleCondensedSequence_shortExact I).extClass.comp
      (Abelian.Ext.mk₀ (integerReindex I J σ)) (add_zero 1) =
    (Abelian.Ext.mk₀ (circleReindex I J σ)).comp
      (realCircleCondensedSequence_shortExact J).extClass (zero_add 1) at h
  change (Abelian.Ext.mk₀ (circleReindex I J σ)).comp
      ((realCircleCondensedSequence_shortExact J).extClass.comp e (by omega : 1+q=q+1)) (zero_add (q+1)) =
    (realCircleCondensedSequence_shortExact I).extClass.comp
      ((Abelian.Ext.mk₀ (integerReindex I J σ)).comp e (zero_add q)) (by omega : 1+q=q+1)
  calc
    _ = ((Abelian.Ext.mk₀ (circleReindex I J σ)).comp
      (realCircleCondensedSequence_shortExact J).extClass (zero_add 1)).comp e (by omega : 1+q=q+1) :=
      (Abelian.Ext.comp_assoc _ _ _ (zero_add 1) (by omega : 1+q=q+1) (by omega : 0+1+q=q+1)).symm
    _ = _ := by rw [← h,Abelian.Ext.comp_assoc_of_second_deg_zero]

theorem finiteCircle_extHigh_zero (I : Type u) [Fintype I] (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (circleProductCondensed I) discreteIntegerCoeff (q+2)) : e = 0 := by
  obtain ⟨a,ha⟩ := (boundaryEquiv I B (q+1)).surjective e
  rw [← ha,finiteInteger_extPositive_zero I q a,map_zero]

theorem circle_extHigh_zero (I : Type u) (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (circleProductCondensed I) discreteIntegerCoeff (q+2)) : e=0 := by
  obtain ⟨F,b,hb⟩ := circleGroup_ext_finiteSupport I B (q+2) e
  rw [← hb,finiteCircle_extHigh_zero (↥F) B q b,map_zero]

theorem integer_extPositive_zero (I : Type u) (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (integers I) discreteIntegerCoeff (q+1)) : e=0 := by
  apply (boundaryEquiv I B (q+1)).injective
  rw [map_zero]
  exact circle_extHigh_zero I B q _

theorem integerHom_finiteSupport (I : Type u) (B : UniversalBD.{u})
    (g : integers I ⟶ discreteIntegerCoeff) :
    ∃ F : Finset I, ∃ b : integers (↥F) ⟶ discreteIntegerCoeff,
      integerReindex I (↥F) Subtype.val ≫ b = g := by
  let e := connecting I discreteIntegerCoeff 0 (Abelian.Ext.mk₀ g)
  obtain ⟨F,c,hc⟩ := circleGroup_ext_finiteSupport I B 1 e
  obtain ⟨a,ha⟩ := (boundaryEquiv (↥F) B 0).surjective c
  refine ⟨F,Abelian.Ext.addEquiv₀ a,?_⟩
  apply Abelian.Ext.addEquiv₀.symm.injective
  change Abelian.Ext.mk₀ (integerReindex I (↥F) Subtype.val ≫ Abelian.Ext.addEquiv₀ a) =
    Abelian.Ext.mk₀ g
  rw [← Abelian.Ext.mk₀_comp_mk₀,Abelian.Ext.mk₀_addEquiv₀_apply]
  apply (boundaryEquiv I B 0).injective
  change connecting I discreteIntegerCoeff 0
    (pb discreteIntegerCoeff (integerReindex I (↥F) Subtype.val) 0 a) = e
  rw [← boundary_natural,show connecting (↥F) discreteIntegerCoeff 0 a = c from ha]
  exact hc

/-- The actual finite-torus degree-one group, using the genuine
boundary and the finite integer product bicone. -/
def finiteCircleExtOne (I : Type u) [Fintype I] (B : UniversalBD.{u}) :
    (I → Abelian.Ext discreteIntegerCoeff discreteIntegerCoeff 0) ≃+
      Abelian.Ext (circleProductCondensed I) discreteIntegerCoeff 1 :=
  (finiteIntegerExt I 0).symm.trans (boundaryEquiv I B 0)

theorem finiteCircleExtOne_eq_sum (I : Type u) [Fintype I] (B : UniversalBD.{u})
    (a : I → Abelian.Ext discreteIntegerCoeff discreteIntegerCoeff 0) :
    finiteCircleExtOne I B a =
      ∑ i : I, connecting I discreteIntegerCoeff 0
        ((Abelian.Ext.mk₀ ((integerFan I).proj i)).comp (a i) (zero_add 0)) := by
  classical
  change connecting I discreteIntegerCoeff 0
    (∑ i : I, (Abelian.Ext.mk₀ ((integerFan I).proj i)).comp (a i) (zero_add 0)) = _
  rw [map_sum]

#print axioms finiteCircleExtOne_eq_sum
#print axioms scalarProjective
#print axioms boundary_natural
#print axioms integer_extPositive_zero
#print axioms integerHom_finiteSupport
end CMDG.CondensedCM5R0.FiniteTorusBoundary
