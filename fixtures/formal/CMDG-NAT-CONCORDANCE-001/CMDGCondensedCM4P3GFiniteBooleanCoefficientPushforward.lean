import CMDGCondensedCM4P3GKernelWeightedLocalConstancy
import CMDGCondensedCM4P2EFiniteDualPushforward

/-!
# CMDG CM4-P3-G stage 22: finite Boolean coefficient-family pushforward

This successor fixture transports the certified stage-21 Boolean coefficient fiber identity through
the already-certified P2-E canonical finite coefficient-family pushforward. It stops before finite
measure transport, right-Kan cone assembly, kernel local constancy, mapping-out injectivity, or any
solidity claim.
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

/-- The finite-set map used by the profinite quotient diagram is definitionally the certified
quotient transition from stage 21. -/
theorem fintypeDiagram_map_eq_finiteQuotientTransition
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (p : j) :
    (ConcreteCategory.hom (X.fintypeDiagram.map f)) p = finiteQuotientTransition X f p := by
  rfl

/-- Explicit pointwise fiber-sum pushforward on finite coefficient families. This is used only as a
normal form for the already-certified P2-E canonical pushforward. -/
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
      (∑ x : A.obj,
        if (ConcreteCategory.hom g) x = y then
          (ModuleCat.Hom.hom (CMDG.CondensedCM4P2D.coefficientPresheaf.map h)) (a x)
        else 0) =
      (ModuleCat.Hom.hom (CMDG.CondensedCM4P2D.coefficientPresheaf.map h))
        (∑ x : A.obj,
          if (ConcreteCategory.hom g) x = y then a x else 0)
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro x _
    by_cases hxy : (ConcreteCategory.hom g) x = y <;> simp [hxy]

/-- The explicit fiber-sum map carries a canonical coordinate inclusion to the coordinate inclusion
at its image. -/
theorem finiteCoordinateInclusion_fiberPushforward
    {A B : FintypeCat.{u}} (g : A ⟶ B) (x : A.obj) :
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion A x ≫
        finiteCoefficientFamilyFiberPushforward g =
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion B
        ((ConcreteCategory.hom g) x) := by
  classical
  ext S h
  funext y
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

/-- The already-certified P2-E canonical pushforward is extensionally equal to the explicit
fiber-sum normal form. -/
theorem finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward
    {A B : FintypeCat.{u}} (g : A ⟶ B) :
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g =
      finiteCoefficientFamilyFiberPushforward g := by
  apply CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamily_hom_ext
  intro x
  rw [CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion_pushforwardMap]
  rw [finiteCoordinateInclusion_fiberPushforward]

/-- Coordinate/fiber normalization for the existing P2-E canonical coefficient-family pushforward. -/
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

/-- Stage-22 terminal theorem. The Boolean coefficient family is covariantly compatible with a
refinement of finite quotients under the already-certified P2-E pushforward map. -/
theorem finiteBooleanCoefficientFamily_pushforward
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap
        (X.fintypeDiagram.map f)).app
        (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
      (finiteBooleanCoefficientFamily X j) =
      finiteBooleanCoefficientFamily X k := by
  classical
  rw [finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward
    (X.fintypeDiagram.map f)]
  funext q
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
            rfl
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
