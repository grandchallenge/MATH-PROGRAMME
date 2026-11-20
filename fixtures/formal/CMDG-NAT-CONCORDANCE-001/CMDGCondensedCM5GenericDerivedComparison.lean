import Mathlib.Algebra.Homology.DerivedCategory.Basic
import Mathlib.Algebra.Homology.Single
import Mathlib.Algebra.Homology.QuasiIso
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex

/-!
# Canonical derived comparison of a fully exact augmented chain complex

This general theorem works in any abelian category. It constructs the
actual augmentation chain map, proves that it is a quasi-isomorphism,
and proves that it becomes an isomorphism after localization.

It does not assert that the terms are projective, and it does not
identify an independent solidification unit as an isomorphism.
-/

noncomputable section
universe u v
open CategoryTheory Limits HomologicalComplex

namespace CMDG.DerivedComparison

variable {C : Type u} [Category.{v} C] [Abelian C]
variable (K : ChainComplex C ℕ) (X : C)
variable (ε : K.X 0 ⟶ X) (hε : K.d 1 0 ≫ ε = 0)

/-- The genuine augmented chain map, whose degree zero component is ε. -/
noncomputable def chainAugmentation :
    K ⟶ (ChainComplex.single₀ C).obj X :=
  (ChainComplex.toSingle₀Equiv K X).symm ⟨ε, hε⟩

@[simp] theorem chainAugmentation_f_zero :
    (chainAugmentation K X ε hε).f 0 = ε :=
  ChainComplex.toSingle₀Equiv_symm_apply_f_zero ε hε

/-- An exact augmented chain complex is quasi-isomorphic to the
object it resolves. This is a map-of-complexes theorem, not an Ext statement. -/
theorem chainAugmentation_quasiIso
    (hPositive : ∀ n : ℕ, K.ExactAt (n + 1))
    (hZero : (ShortComplex.mk (K.d 1 0) ε hε).Exact)
    [Epi ε] :
    QuasiIso (chainAugmentation K X ε hε) := by
  rw [HomologicalComplex.quasiIso_iff]
  intro n
  cases n with
  | zero =>
    rw [HomologicalComplex.quasiIsoAt_iff]
    let φ := (shortComplexFunctor C (ComplexShape.down ℕ) 0).map
      (chainAugmentation K X ε hε)
    have hgK : (K.sc 0).g = 0 := by
      change K.d 0 0 = 0
      exact K.shape 0 0 (by simp)
    have hfL :
        (((ChainComplex.single₀ C).obj X).sc 0).f = 0 := by
      simp [ChainComplex.single₀, HomologicalComplex.single]
    have hgL :
        (((ChainComplex.single₀ C).obj X).sc 0).g = 0 := by
      simp [ChainComplex.single₀, HomologicalComplex.single]
    change ShortComplex.QuasiIso φ
    apply (ShortComplex.quasiIso_iff_of_zeros' φ hgK hfL hgL).2
    constructor
    · simpa [φ, chainAugmentation, HomologicalComplex.sc,
        shortComplexFunctor, ChainComplex.single₀] using hZero
    · change Epi ε
      infer_instance
  | succ n =>
    have hL : ((ChainComplex.single₀ C).obj X).ExactAt (n + 1) :=
      HomologicalComplex.ExactAt.of_isZero
        (HomologicalComplex.isZero_single_obj_X
          (ComplexShape.down ℕ) 0 X (n + 1) (by omega))
    exact (HomologicalComplex.quasiIsoAt_iff_exactAt'
      (chainAugmentation K X ε hε) (n + 1) hL).2 (hPositive n)

/-- The canonical morphism in the localized category of chain complexes. -/
noncomputable def localizedDerivedComparison :
    (HomologicalComplexUpToQuasiIso.Q).obj K ⟶
      (HomologicalComplexUpToQuasiIso.Q).obj ((ChainComplex.single₀ C).obj X) :=
  (HomologicalComplexUpToQuasiIso.Q).map (chainAugmentation K X ε hε)

/-- The canonical comparison is invertible in the derived localization. -/
theorem localizedDerivedComparison_isIso
    (hPositive : ∀ n : ℕ, K.ExactAt (n + 1))
    (hZero : (ShortComplex.mk (K.d 1 0) ε hε).Exact)
    [Epi ε] :
    IsIso (localizedDerivedComparison K X ε hε) := by
  apply (HomologicalComplexUpToQuasiIso.isIso_Q_map_iff_mem_quasiIso
    (chainAugmentation K X ε hε)).2
  exact (HomologicalComplex.mem_quasiIso_iff
    (chainAugmentation K X ε hε)).2
    (chainAugmentation_quasiIso K X ε hε hPositive hZero)

#print axioms localizedDerivedComparison_isIso
end CMDG.DerivedComparison
