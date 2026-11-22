import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneH2PrimitiveOperator
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Abel


/-!
# CMDG CM5: natural bounded H² splittings under compact test reindexing

The protected-merged degree-two compact-real exactness/projection proofs
already construct a single continuous-linear primitive G and projection
Π=d₁G. This module proves an additional structural requirement for
sheaf-level comparison: G and Π commute with every continuous map of
compact test parameters φ:T→S.

Define genuine cochain maps induced by id_{A^r}×φ on the actual compact
continuous-function spaces C(A^r×S,ℝ). Prove functoriality, composition
with the true finite-degree-one homotopy, parameter-invariance of
the doubling operator, and commutation with the exact Banach inverse
1−[2]*/2. Consequently
  φ* (G_S f) = G_T (φ* f)
and
  φ* (Π_S f) = Π_T (φ* f),
uniformly for arbitrary compact Hausdorff abelian source A, compact
S and T, and every continuous φ:T→S. These are naturality identities
between genuine continuous-linear maps, not merely a pointwise
existence claim.

This advances the presheaf-functoriality input for derived condensed
cochain comparison. It does NOT prove full finite-type Breen–Deligne
resolution exactness, derived sheaf Hom comparison, circle-to-integers
derived equivalence, or equality with the canonical solidification unit.
-/
noncomputable section
universe u v w
namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (S : Type v) (T : Type w)
variable [TopologicalSpace A] [CompactSpace A]
  [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]
variable [TopologicalSpace T] [CompactSpace T]

def paramC1 (φ : C(T,S)) : C((A × A) × T,(A × A) × S) :=
  ⟨fun p => (p.1,φ p.2),by fun_prop⟩

def paramC2a (φ : C(T,S)) :
    C((A × (A × A)) × T,(A × (A × A)) × S) :=
  ⟨fun p => (p.1,φ p.2),by fun_prop⟩

def paramReindex1 (φ : C(T,S)) : C1 A S →L[ℝ] C1 A T :=
  ContinuousMap.compCLM ℝ ℝ (paramC1 A S T φ)

def paramReindex2 (φ : C(T,S)) : C2 A S →L[ℝ] C2 A T :=
  ((ContinuousMap.compCLM ℝ ℝ (paramC2a A S T φ)).comp
    (ContinuousLinearMap.fst ℝ (C2a A S) (C1 A S))).prod
  ((paramReindex1 A S T φ).comp
    (ContinuousLinearMap.snd ℝ (C2a A S) (C1 A S)))

theorem paramReindex_hStar1 (φ : C(T,S)) (f : C2 A S) :
    paramReindex1 A S T φ (hStar1 A S f) =
    hStar1 A T (paramReindex2 A S T φ f) := by
  ext p
  simp [paramReindex1,paramReindex2,paramC1,paramC2a,
    hStar1,qAssoc1,qAssoc2,qAssoc3,qComm]

theorem paramReindex_doubling (φ : C(T,S)) (f : C2 A S) :
    paramReindex2 A S T φ (doubleStar2 A S f) =
    doubleStar2 A T (paramReindex2 A S T φ f) := by
  apply Prod.ext
  · ext p
    simp [paramReindex2,paramC2a,paramReindex1,paramC1,
      doubleStar2,doubleStar1,pDouble2a,pDouble1]
  · ext p
    simp [paramReindex2,paramC2a,paramReindex1,paramC1,
      doubleStar2,doubleStar1,pDouble2a,pDouble1]

/-- Parameter pullback commutes with the genuine inverse of the
half-doubling operator, by uniqueness for the invertible Banach
endomorphism on the reindexed compact cochain space. -/
theorem paramReindex_halfInverse (φ : C(T,S)) (f : C2 A S) :
    paramReindex2 A S T φ (h2HalfInverse A S f) =
    h2HalfInverse A T (paramReindex2 A S T φ f) := by
  have hcomm (x : C2 A S) :
      paramReindex2 A S T φ (h2HalfDoubling A S x) =
      h2HalfDoubling A T (paramReindex2 A S T φ x) := by
    simp only [h2HalfDoubling,ContinuousLinearMap.smul_apply,map_smul]
    rw [paramReindex_doubling]
  have hinj : Function.Injective
      ((1 - h2HalfDoubling A T) : C2 A T →L[ℝ] C2 A T) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (h2HalfIsUnit A T)).1
  apply hinj
  have hL : (1 - h2HalfDoubling A T)
      (paramReindex2 A S T φ (h2HalfInverse A S f)) =
      paramReindex2 A S T φ f := by
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.one_apply]
    rw [←hcomm, ←map_sub, h2HalfInverse_equation]
  have hR : (1 - h2HalfDoubling A T)
      (h2HalfInverse A T (paramReindex2 A S T φ f)) =
      paramReindex2 A S T φ f := by
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply] using
      h2HalfInverse_equation A T (paramReindex2 A S T φ f)
  exact hL.trans hR.symm

/-- Naturality of the *global* analytic degree-two primitive in every
continuous change of the compact test parameter, not merely
pointwise elementwise construction. -/
theorem paramReindex_h2Primitive (φ : C(T,S)) (f : C2 A S) :
    paramReindex1 A S T φ (h2PrimitiveOperator A S f) =
    h2PrimitiveOperator A T (paramReindex2 A S T φ f) := by
  change paramReindex1 A S T φ
    ((1/2 : ℝ) • hStar1 A S (h2HalfInverse A S f)) =
    (1/2 : ℝ) • hStar1 A T
      (h2HalfInverse A T (paramReindex2 A S T φ f))
  rw [map_smul, paramReindex_hStar1, paramReindex_halfInverse]

theorem paramReindex_differential1 (φ : C(T,S)) (g : C1 A S) :
    paramReindex2 A S T φ (differential1 A S g) =
    differential1 A T (paramReindex1 A S T φ g) := by
  apply Prod.ext
  · ext p
    simp [paramReindex1,paramReindex2,paramC1,paramC2a,
      differential1,pBC,pAB_C,pA_BC,pAB]
  · ext p
    simp [paramReindex1,paramReindex2,paramC1,paramC2a,
      differential1,pSwap]

theorem paramReindex_h2Projection (φ : C(T,S)) (f : C2 A S) :
    paramReindex2 A S T φ (h2CocycleProjection A S f) =
    h2CocycleProjection A T (paramReindex2 A S T φ f) := by
  change paramReindex2 A S T φ
      (differential1 A S (h2PrimitiveOperator A S f)) =
    differential1 A T
      (h2PrimitiveOperator A T (paramReindex2 A S T φ f))
  rw [paramReindex_differential1,paramReindex_h2Primitive]

/-- Functoriality of degree-one compact-parameter cochain pullback. -/
theorem paramReindex1_id (f : C1 A S) :
    paramReindex1 A S S (ContinuousMap.id S) f = f := by
  ext p
  rfl

theorem paramReindex2_id (f : C2 A S) :
    paramReindex2 A S S (ContinuousMap.id S) f = f := by
  apply Prod.ext
  · ext p
    rfl
  · ext p
    rfl

theorem paramReindex1_comp
    {U : Type*} [TopologicalSpace U] [CompactSpace U]
    (φ : C(T,S)) (ψ : C(U,T)) (f : C1 A S) :
    paramReindex1 A S U (φ.comp ψ) f =
      paramReindex1 A T U ψ (paramReindex1 A S T φ f) := by
  ext p
  rfl

theorem paramReindex2_comp
    {U : Type*} [TopologicalSpace U] [CompactSpace U]
    (φ : C(T,S)) (ψ : C(U,T)) (f : C2 A S) :
    paramReindex2 A S U (φ.comp ψ) f =
      paramReindex2 A T U ψ (paramReindex2 A S T φ f) := by
  apply Prod.ext
  · ext p
    rfl
  · ext p
    rfl

#print axioms paramReindex1_id
#print axioms paramReindex2_id
#print axioms paramReindex1_comp
#print axioms paramReindex2_comp

#print axioms paramReindex_halfInverse
#print axioms paramReindex_h2Primitive
#print axioms paramReindex_differential1
#print axioms paramReindex_h2Projection

#print axioms paramReindex_hStar1
#print axioms paramReindex_doubling
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
