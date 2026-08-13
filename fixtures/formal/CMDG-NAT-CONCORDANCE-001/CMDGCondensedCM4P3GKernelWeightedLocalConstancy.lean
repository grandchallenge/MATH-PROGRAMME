import CMDGCondensedCM4P3GFiniteBooleanMeasure
import CMDGCondensedCM4P2EFiniteDualPushforward

/-!
# CMDG CM4-P3-G finite quotient coefficient compatibility

This successor fixture isolates the finite quotient-refinement calculation required before any
right-Kan assembly or kernel-local-constancy argument. It proves that a delta pulled back from a
coarser finite quotient is the fiberwise sum of the deltas from a finer quotient, then transports
that identity through the already-certified lifted Nöbeling Boolean pairing.

No finite-measure cone, right-Kan assembly, injectivity, coefficient-solidity, or broader P3 closure
claim is asserted here.
-/

namespace CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy

universe u

open CategoryTheory
open scoped BigOperators

open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.BasisBooleanPairingR

abbrev R := CMDG.CondensedCM4P3G.R.{u}

noncomputable local instance discreteQuotientFintype
    (X : Profinite.{u}) (j : DiscreteQuotient X) : Fintype j :=
  Fintype.ofFinite j

noncomputable local instance discreteQuotientDecidableEq
    (X : Profinite.{u}) (j : DiscreteQuotient X) : DecidableEq j :=
  Classical.decEq j

noncomputable def finiteQuotientTransition
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) : j → k :=
  DiscreteQuotient.ofLE f.le

theorem finiteQuotientTransition_proj
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (x : X) :
    finiteQuotientTransition X f (j.proj x) = k.proj x := by
  change DiscreteQuotient.ofLE f.le (j.proj x) = k.proj x
  exact DiscreteQuotient.ofLE_proj f.le x

theorem finiteDeltaFiberScalar_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) (x : X) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        if j.proj x = p then (1 : R.{u}) else 0
      else 0) =
      if k.proj x = q then (1 : R.{u}) else 0 := by
  by_cases hx : k.proj x = q
  · have hpx : finiteQuotientTransition X f (j.proj x) = q := by
      calc
        finiteQuotientTransition X f (j.proj x) = k.proj x :=
          finiteQuotientTransition_proj X f x
        _ = q := hx
    rw [Finset.sum_eq_single (j.proj x)]
    · simp [hpx, hx]
    · intro p _ hp
      have hjp : j.proj x ≠ p := fun h => hp h.symm
      by_cases hpq : finiteQuotientTransition X f p = q
      · simp [hpq, hjp]
      · simp [hpq]
    · simp
  · rw [if_neg hx]
    apply Finset.sum_eq_zero
    intro p _
    by_cases hpq : finiteQuotientTransition X f p = q
    · have hjp : j.proj x ≠ p := by
        intro h
        apply hx
        calc
          k.proj x = finiteQuotientTransition X f (j.proj x) :=
            (finiteQuotientTransition_proj X f x).symm
          _ = finiteQuotientTransition X f p := congrArg (finiteQuotientTransition X f) h
          _ = q := hpq
      simp [hpq, hjp]
    · simp [hpq]

theorem finiteDeltaPullbackR_fiber_sum_apply
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) (x : X) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) x =
      finiteDeltaPullbackR X k q x := by
  change
    (LocallyConstant.evalRingHom x)
        (∑ p : j,
          if finiteQuotientTransition X f p = q then
            finiteDeltaPullbackR X j p
          else 0) =
      (LocallyConstant.evalRingHom x) (finiteDeltaPullbackR X k q)
  calc
    (LocallyConstant.evalRingHom x)
        (∑ p : j,
          if finiteQuotientTransition X f p = q then
            finiteDeltaPullbackR X j p
          else 0) =
        ∑ p : j,
          (LocallyConstant.evalRingHom x)
            (if finiteQuotientTransition X f p = q then
              finiteDeltaPullbackR X j p
            else 0) := by
              rw [map_sum]
    _ = ∑ p : j,
          if finiteQuotientTransition X f p = q then
            if j.proj x = p then (1 : R.{u}) else 0
          else 0 := by
            apply Finset.sum_congr rfl
            intro p _
            by_cases hpq : finiteQuotientTransition X f p = q
            · simp [hpq, finiteDeltaPullbackR]
            · simp [hpq]
    _ = if k.proj x = q then (1 : R.{u}) else 0 :=
      finiteDeltaFiberScalar_sum X f q x
    _ = (LocallyConstant.evalRingHom x) (finiteDeltaPullbackR X k q) := by
      simp [finiteDeltaPullbackR]

theorem finiteDeltaPullbackR_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) =
      finiteDeltaPullbackR X k q := by
  apply LocallyConstant.ext
  intro x
  exact finiteDeltaPullbackR_fiber_sum_apply X f q x

theorem basisBooleanPairingR_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X j p)
      else 0) =
      basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X k q) := by
  calc
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X j p)
      else 0) =
        basisBooleanPairingR.{u, u, u, u} X
          (∑ p : j,
            if finiteQuotientTransition X f p = q then
              finiteDeltaPullbackR X j p
            else 0) := by
              rw [map_sum]
              apply Finset.sum_congr rfl
              intro p _
              by_cases hpq : finiteQuotientTransition X f p = q
              · rw [if_pos hpq, if_pos hpq]
              · rw [if_neg hpq, if_neg hpq, map_zero]
    _ = basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X k q) := by
      rw [finiteDeltaPullbackR_fiber_sum X f q]

theorem finiteBooleanCoefficient_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        finiteBooleanCoefficient X j p
      else 0) =
      finiteBooleanCoefficient X k q := by
  change
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X j p)
      else 0) =
      basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X k q)
  exact basisBooleanPairingR_fiber_sum X f q

#check finiteQuotientTransition
#check finiteQuotientTransition_proj
#check finiteDeltaFiberScalar_sum
#check finiteDeltaPullbackR_fiber_sum_apply
#check finiteDeltaPullbackR_fiber_sum
#check basisBooleanPairingR_fiber_sum
#check finiteBooleanCoefficient_fiber_sum

#print axioms finiteQuotientTransition_proj
#print axioms finiteDeltaFiberScalar_sum
#print axioms finiteDeltaPullbackR_fiber_sum_apply
#print axioms finiteDeltaPullbackR_fiber_sum
#print axioms basisBooleanPairingR_fiber_sum
#print axioms finiteBooleanCoefficient_fiber_sum

end CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy

/-!
## Stage 22 — finite Boolean coefficient-family pushforward

The stage-21 coefficient theorem above is transported through the already-certified P2-E canonical
finite-family pushforward. The proof introduces only an explicit fiber-sum normal form and proves it
equal to the canonical pushforward by the existing coordinate-generator extensionality theorem.
-/

namespace CMDG.CondensedCM4P3G.FiniteBooleanCoefficientPushforward

universe u

open CategoryTheory Opposite
open scoped BigOperators

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy

abbrev R := CMDG.CondensedCM4P2D.R.{u}

attribute [local instance] FintypeCat.fintype

noncomputable local instance fintypeCatObjDecidableEq
    (A : FintypeCat.{u}) : DecidableEq A.obj :=
  Classical.decEq A.obj

noncomputable local instance stage22DiscreteQuotientFintype
    (X : Profinite.{u}) (j : DiscreteQuotient X) : Fintype j :=
  Fintype.ofFinite j

noncomputable local instance stage22DiscreteQuotientDecidableEq
    (X : Profinite.{u}) (j : DiscreteQuotient X) : DecidableEq j :=
  Classical.decEq j

theorem fintypeDiagram_map_eq_finiteQuotientTransition
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (p : j) :
    (ConcreteCategory.hom (X.fintypeDiagram.map f)) p = finiteQuotientTransition X f p := by
  rfl

noncomputable def finiteCoefficientFamilyFiberPushforward
    {A B : FintypeCat.{u}} (g : A ⟶ B) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf A ⟶
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf B := by
  classical
  refine
    { app := fun S => ModuleCat.ofHom
        { toFun := fun a y =>
            ∑ x : A.obj, if (ConcreteCategory.hom g) x = y then a x else 0
          map_add' := ?_
          map_smul' := ?_ }
      naturality := ?_ }
  · intro a b
    funext y
    change
      (∑ x : A.obj,
        if (ConcreteCategory.hom g) x = y then a x + b x else 0) =
      (∑ x : A.obj,
        if (ConcreteCategory.hom g) x = y then a x else 0) +
      ∑ x : A.obj,
        if (ConcreteCategory.hom g) x = y then b x else 0
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro x _
    by_cases hxy : (ConcreteCategory.hom g) x = y <;> simp [hxy]
  · intro c a
    funext y
    change
      (∑ x : A.obj,
        if (ConcreteCategory.hom g) x = y then c • a x else 0) =
      c • ∑ x : A.obj,
        if (ConcreteCategory.hom g) x = y then a x else 0
    rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro x _
    by_cases hxy : (ConcreteCategory.hom g) x = y <;> simp [hxy]
  · intro S T h
    apply ModuleCat.hom_injective
    apply LinearMap.ext
    intro a
    funext y
    change
      (ModuleCat.Hom.hom (CMDG.CondensedCM4P2D.coefficientPresheaf.map h))
          (∑ x : A.obj,
            if (ConcreteCategory.hom g) x = y then a x else 0) =
        ∑ x : A.obj,
          if (ConcreteCategory.hom g) x = y then
            (ModuleCat.Hom.hom (CMDG.CondensedCM4P2D.coefficientPresheaf.map h)) (a x)
          else 0
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro x _
    by_cases hxy : (ConcreteCategory.hom g) x = y <;> simp [hxy]

theorem finiteCoordinateInclusion_fiberPushforward
    {A B : FintypeCat.{u}} (g : A ⟶ B) (x : A.obj) :
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion A x ≫
        finiteCoefficientFamilyFiberPushforward g =
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion B
        ((ConcreteCategory.hom g) x) := by
  classical
  ext S h y
  change
    (∑ z : A.obj,
      if (ConcreteCategory.hom g) z = y then
        if z = x then h else 0
      else 0) =
      if y = (ConcreteCategory.hom g) x then h else 0
  by_cases hy : y = (ConcreteCategory.hom g) x
  · rw [Finset.sum_eq_single x]
    · simp [hy]
    · intro z _ hzx
      have hzx' : z ≠ x := hzx
      simp [hzx']
    · simp
  · rw [if_neg hy]
    apply Finset.sum_eq_zero
    intro z _
    by_cases hzx : z = x
    · subst z
      have hgxy : (ConcreteCategory.hom g) x ≠ y := fun h => hy h.symm
      simp [hgxy]
    · simp [hzx]

theorem finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward
    {A B : FintypeCat.{u}} (g : A ⟶ B) :
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g =
      finiteCoefficientFamilyFiberPushforward g := by
  apply CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamily_hom_ext
  intro x
  rw [CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion_pushforwardMap]
  rw [finiteCoordinateInclusion_fiberPushforward]

theorem finiteCoefficientFamilyPushforwardMap_apply
    {A B : FintypeCat.{u}} (g : A ⟶ B) (S : CompHaus.{u}ᵒᵖ)
    (a :
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf A).obj S)
    (y : B.obj) :
    ((ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g).app S))
      a) y =
      ∑ x : A.obj, if (ConcreteCategory.hom g) x = y then a x else 0 := by
  rw [finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward g]
  rfl

theorem finiteBooleanCoefficientFamily_pushforward
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap
        (X.fintypeDiagram.map f)).app
        (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
      (finiteBooleanCoefficientFamily X j) =
      finiteBooleanCoefficientFamily X k := by
  funext q
  rw [finiteCoefficientFamilyPushforwardMap_apply]
  change
    (∑ p : j,
      if (ConcreteCategory.hom (X.fintypeDiagram.map f)) p = q then
        finiteBooleanCoefficient X j p
      else 0) =
      finiteBooleanCoefficient X k q
  calc
    (∑ p : j,
      if (ConcreteCategory.hom (X.fintypeDiagram.map f)) p = q then
        finiteBooleanCoefficient X j p
      else 0) =
        ∑ p : j,
          if finiteQuotientTransition X f p = q then
            finiteBooleanCoefficient X j p
          else 0 := by
            apply Finset.sum_congr rfl
            intro p _
            rw [fintypeDiagram_map_eq_finiteQuotientTransition X f p]
    _ = finiteBooleanCoefficient X k q :=
      finiteBooleanCoefficient_fiber_sum X f q

#check fintypeDiagram_map_eq_finiteQuotientTransition
#check finiteCoefficientFamilyFiberPushforward
#check finiteCoordinateInclusion_fiberPushforward
#check finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward
#check finiteCoefficientFamilyPushforwardMap_apply
#check finiteBooleanCoefficientFamily_pushforward

#print axioms fintypeDiagram_map_eq_finiteQuotientTransition
#print axioms finiteCoefficientFamilyFiberPushforward
#print axioms finiteCoordinateInclusion_fiberPushforward
#print axioms finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward
#print axioms finiteCoefficientFamilyPushforwardMap_apply
#print axioms finiteBooleanCoefficientFamily_pushforward

end CMDG.CondensedCM4P3G.FiniteBooleanCoefficientPushforward
