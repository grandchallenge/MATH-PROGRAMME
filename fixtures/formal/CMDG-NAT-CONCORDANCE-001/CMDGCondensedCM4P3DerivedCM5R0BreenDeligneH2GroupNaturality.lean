import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneH2PrimitiveOperator
import Mathlib.Topology.Algebra.ContinuousMonoidHom
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Abel


/-!
# CMDG CM5: natural bounded H² splitting in the compact group source

The protected-merged finite-degree compact real-cochain complex has a
global bounded continuous-linear primitive G and bounded idempotent
projection Π onto its degree-two cocycle subspace.

For arbitrary compact Hausdorff abelian groups A and B, compact S,
and any continuous additive homomorphism φ:A→B, define genuine
cochain pullbacks on the actual C(A^r×S,ℝ) through φ^r×id_S.

Prove functorial identities under identity and composition,
equivariance of the finite homotopy, coordinate doubling, genuine
Banach inverse (1−[2]*/2)⁻¹, degree-one differential, and finally
  φ* G_B = G_A φ*,
  φ* Π_B = Π_A φ*.
This is naturality in the source group A, complementing the
distinct naturality in the compact probe S established in
PR #3632. All theorems hold for infinite-dimensional products
of circles wherever the required compact Hausdorff group instances
are available; there is no finite-index restriction.

This is a *verified low-degree presheaf-level* compatibility, not the
all-degree Breen–Deligne resolution or a derived CondensedAb RHom
comparison. Neither canonical solidification-unit equality nor
public MATHCERT certification follows.
-/
noncomputable section
universe u v w
namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (B : Type v) (S : Type w)
variable [TopologicalSpace A] [CompactSpace A]
  [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace B] [CompactSpace B]
  [AddCommGroup B] [ContinuousAdd B]
variable [TopologicalSpace S] [CompactSpace S]

def groupC1 (φ : ContinuousAddMonoidHom A B) :
    C((A × A) × S, (B × B) × S) :=
  ⟨fun p => ((φ p.1.1,φ p.1.2),p.2),by fun_prop⟩

def groupC2a (φ : ContinuousAddMonoidHom A B) :
    C((A × (A × A)) × S, (B × (B × B)) × S) :=
  ⟨fun p => ((φ p.1.1,(φ p.1.2.1,φ p.1.2.2)),p.2),by fun_prop⟩

def groupReindex1 (φ : ContinuousAddMonoidHom A B) :
    C1 B S →L[ℝ] C1 A S :=
  ContinuousMap.compCLM ℝ ℝ (groupC1 A B S φ)

def groupReindex2 (φ : ContinuousAddMonoidHom A B) :
    C2 B S →L[ℝ] C2 A S :=
  ((ContinuousMap.compCLM ℝ ℝ (groupC2a A B S φ)).comp
    (ContinuousLinearMap.fst ℝ (C2a B S) (C1 B S))).prod
  ((groupReindex1 A B S φ).comp
    (ContinuousLinearMap.snd ℝ (C2a B S) (C1 B S)))

theorem groupReindex_hStar1
    (φ : ContinuousAddMonoidHom A B) (f : C2 B S) :
    groupReindex1 A B S φ (hStar1 B S f) =
      hStar1 A S (groupReindex2 A B S φ f) := by
  ext p
  simp [groupReindex1,groupReindex2,groupC1,groupC2a,
    hStar1,qAssoc1,qAssoc2,qAssoc3,qComm,φ.map_add]

theorem groupReindex_doubling
    (φ : ContinuousAddMonoidHom A B) (f : C2 B S) :
    groupReindex2 A B S φ (doubleStar2 B S f) =
      doubleStar2 A S (groupReindex2 A B S φ f) := by
  apply Prod.ext
  · ext p
    simp [groupReindex2,groupC2a,groupReindex1,groupC1,
      doubleStar2,doubleStar1,pDouble2a,pDouble1,φ.map_add]
  · ext p
    simp [groupReindex2,groupC2a,groupReindex1,groupC1,
      doubleStar2,doubleStar1,pDouble2a,pDouble1,φ.map_add]

/-- The analytic Banach inverse is natural in every continuous
homomorphism of compact abelian source groups. -/
theorem groupReindex_halfInverse
    (φ : ContinuousAddMonoidHom A B) (f : C2 B S) :
    groupReindex2 A B S φ (h2HalfInverse B S f) =
      h2HalfInverse A S (groupReindex2 A B S φ f) := by
  have hcomm (x : C2 B S) :
      groupReindex2 A B S φ (h2HalfDoubling B S x) =
      h2HalfDoubling A S (groupReindex2 A B S φ x) := by
    simp only [h2HalfDoubling,ContinuousLinearMap.smul_apply,map_smul]
    rw [groupReindex_doubling]
  have hinj : Function.Injective
      ((1 - h2HalfDoubling A S) : C2 A S →L[ℝ] C2 A S) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (h2HalfIsUnit A S)).1
  apply hinj
  have hL : (1 - h2HalfDoubling A S)
      (groupReindex2 A B S φ (h2HalfInverse B S f)) =
      groupReindex2 A B S φ f := by
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.one_apply]
    rw [←hcomm, ←map_sub, h2HalfInverse_equation]
  have hR : (1 - h2HalfDoubling A S)
      (h2HalfInverse A S (groupReindex2 A B S φ f)) =
      groupReindex2 A B S φ f := by
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply] using
      h2HalfInverse_equation A S (groupReindex2 A B S φ f)
  exact hL.trans hR.symm

/-- The bounded degree-two primitive is natural in source A,
not just in the external compact test parameter. -/
theorem groupReindex_h2Primitive
    (φ : ContinuousAddMonoidHom A B) (f : C2 B S) :
    groupReindex1 A B S φ (h2PrimitiveOperator B S f) =
      h2PrimitiveOperator A S (groupReindex2 A B S φ f) := by
  change groupReindex1 A B S φ
    ((1/2 : ℝ) • hStar1 B S (h2HalfInverse B S f)) =
    (1/2 : ℝ) • hStar1 A S
      (h2HalfInverse A S (groupReindex2 A B S φ f))
  rw [map_smul, groupReindex_hStar1, groupReindex_halfInverse]

theorem groupReindex_differential1
    (φ : ContinuousAddMonoidHom A B) (g : C1 B S) :
    groupReindex2 A B S φ (differential1 B S g) =
      differential1 A S (groupReindex1 A B S φ g) := by
  apply Prod.ext
  · ext p
    simp [groupReindex1,groupReindex2,groupC1,groupC2a,
      differential1,pBC,pAB_C,pA_BC,pAB,φ.map_add]
  · ext p
    simp [groupReindex1,groupReindex2,groupC1,groupC2a,
      differential1,pSwap]

/-- The actual bounded projection onto H²-cocycles is natural under
every continuous additive homomorphism between compact source groups. -/
theorem groupReindex_h2Projection
    (φ : ContinuousAddMonoidHom A B) (f : C2 B S) :
    groupReindex2 A B S φ (h2CocycleProjection B S f) =
      h2CocycleProjection A S (groupReindex2 A B S φ f) := by
  change groupReindex2 A B S φ
      (differential1 B S (h2PrimitiveOperator B S f)) =
    differential1 A S
      (h2PrimitiveOperator A S (groupReindex2 A B S φ f))
  rw [groupReindex_differential1,groupReindex_h2Primitive]

/-- Contravariant functoriality in the compact abelian source:
identity and composition for the actual degree-one and degree-two
compact real cochain pullbacks. -/
theorem groupReindex1_id (f : C1 A S) :
    groupReindex1 A A S (ContinuousAddMonoidHom.id A) f = f := by
  ext p
  rfl

theorem groupReindex2_id (f : C2 A S) :
    groupReindex2 A A S (ContinuousAddMonoidHom.id A) f = f := by
  apply Prod.ext
  · ext p
    rfl
  · ext p
    rfl

theorem groupReindex1_comp
    {C : Type*} [TopologicalSpace C] [CompactSpace C]
    [AddCommGroup C] [ContinuousAdd C]
    (φ : ContinuousAddMonoidHom A B)
    (ψ : ContinuousAddMonoidHom B C) (f : C1 C S) :
    groupReindex1 A C S (ψ.comp φ) f =
      groupReindex1 A B S φ (groupReindex1 B C S ψ f) := by
  ext p
  rfl

theorem groupReindex2_comp
    {C : Type*} [TopologicalSpace C] [CompactSpace C]
    [AddCommGroup C] [ContinuousAdd C]
    (φ : ContinuousAddMonoidHom A B)
    (ψ : ContinuousAddMonoidHom B C) (f : C2 C S) :
    groupReindex2 A C S (ψ.comp φ) f =
      groupReindex2 A B S φ (groupReindex2 B C S ψ f) := by
  apply Prod.ext
  · ext p
    rfl
  · ext p
    rfl

#print axioms groupReindex1_id
#print axioms groupReindex2_id
#print axioms groupReindex1_comp
#print axioms groupReindex2_comp

#print axioms groupReindex_halfInverse
#print axioms groupReindex_h2Primitive
#print axioms groupReindex_differential1
#print axioms groupReindex_h2Projection

#print axioms groupReindex_hStar1
#print axioms groupReindex_doubling
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
