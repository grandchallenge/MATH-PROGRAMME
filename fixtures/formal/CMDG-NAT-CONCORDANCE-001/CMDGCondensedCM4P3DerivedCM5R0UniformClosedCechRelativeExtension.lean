import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechH0
import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechCochains

/-!
# Uniform closed-family relative extension

A locally constant integer function on a closed set U that vanishes on
another closed set V extends to the whole profinite space while retaining
that vanishing. Apply this coordinatewise to all unrestricted tuple
cochains in every degree. No clopen refinement is assumed.

The theorem is a prerequisite for closed-family cocycle gluing; it does
not establish positive-degree Čech acyclicity or derived solidity.
-/

noncomputable section
universe u v w
open Set
namespace CMDG.CondensedCM5R0

/-- Extend integer-valued locally constant data on closed U while forcing
zero on a second closed set V, assuming vanishing on U ∩ V.
No clopen assumption. -/
theorem locallyConstant_extend_closed_relative_zero
    (X : Profinite.{u}) (U V : Set X)
    (hU : IsClosed U) (hV : IsClosed V)
    (f : LocallyConstant U ℤ)
    (hzero : ∀ (x : U), x.val ∈ V → f x = 0) :
    ∃ g : LocallyConstant X ℤ,
      (∀ (x : U), g x.val = f x) ∧
      (∀ (x : V), g x.val = 0) := by
  let E : Bool → Set X := fun b => match b with
    | false => V
    | true => U
  let c : (b : Bool) → LocallyConstant (E b) ℤ := fun b => match b with
    | false => LocallyConstant.const V 0
    | true => f
  have hclosed : ∀ b, IsClosed (E b) := by
    intro b
    cases b
    · exact hV
    · exact hU
  have hagree :
      ∀ (i j : Bool) (x : X) (hi : x ∈ E i) (hj : x ∈ E j),
      c i ⟨x, hi⟩ = c j ⟨x, hj⟩ := by
    intro i j x hi hj
    cases i <;> cases j
    · rfl
    · change (0 : ℤ) = f ⟨x, hj⟩
      exact (hzero ⟨x,hj⟩ hi).symm
    · change f ⟨x, hi⟩ = (0 : ℤ)
      exact hzero ⟨x,hi⟩ hj
    · rfl
  obtain ⟨g, hg⟩ :=
    uniformFiniteClosedFamily_glue_ambient X E hclosed c hagree
  refine ⟨g, ?_, ?_⟩
  · intro x
    exact hg true x.val x.property
  · intro x
    exact hg false x.val x.property

/-- Any tuple-indexed local cochain which vanishes on a closed set F
admits ambient representatives vanishing identically on F, in *every*
cochain degree. This gives the relative extension operation needed
for closed-family inductive correction. -/
theorem uniformClosedCechRelativeAmbientExtension
    (X : Profinite.{u}) {I : Type v}
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (F : Set X) (hF : IsClosed F) (n : ℕ)
    (c : uniformClosedCechLocalCochain X E n)
    (hzero : ∀ (σ : Fin (n + 1) → I)
      (x : uniformClosedCechIntersection X E n σ),
      x.val ∈ F → c σ x = 0) :
    ∃ C : uniformClosedCechAmbientCochain X I n,
      uniformClosedCechRestrict X E n C = c ∧
      (∀ (σ : Fin (n + 1) → I) (x : X),
        x ∈ F → C σ x = 0) := by
  classical
  have hex (σ : Fin (n + 1) → I) :
      ∃ C : LocallyConstant X ℤ,
        (∀ x : uniformClosedCechIntersection X E n σ,
          C x.val = c σ x) ∧
        (∀ x : F, C x.val = 0) :=
    locallyConstant_extend_closed_relative_zero X
      (uniformClosedCechIntersection X E n σ) F
      (uniformClosedCechIntersection_isClosed X E hclosed n σ)
      hF (c σ) (hzero σ)
  choose C hC using hex
  refine ⟨C, ?_, ?_⟩
  · funext σ
    apply DFunLike.ext
    intro x
    exact (hC σ).1 x
  · intro σ x hx
    exact (hC σ).2 ⟨x,hx⟩

#print axioms uniformClosedCechRelativeAmbientExtension

#print axioms locallyConstant_extend_closed_relative_zero
end CMDG.CondensedCM5R0
