import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct
import CMDGCondensedCM4P3DerivedCM5R0StoneanKernelDimension
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CMDG CM5: unconditional dimension shifting for higher Ext

The protected Stonean cover P(T) → F_T is epi with projective source,
and K_T denotes its actual kernel. The long exact contravariant Ext
sequence therefore makes the canonical connecting homomorphism

  Ext^(n+1)(K_T, A) → Ext^(n+2)(F_T, A)

an additive equivalence for every n ≥ 0 and every genuine condensed
coefficient target A. This is a structural equivalence, NOT proof of
higher Ext vanishing.

Specializing A to the actual protected free-solid G_S identifies
the next unproved degree-two obligation with Ext¹(K_T,G_S)=0.
Unlike the older conditional bound, no projectivity of K_T is assumed.

The module does not claim higher Ext vanishes, derived solidity,
independent MATHCERT certification or source-semantic review.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Actual canonical connecting map of the Stonean projective
presentation, in degree n+1 to n+2. -/
noncomputable def stoneanKernelHigherConnecting
    (T : Profinite.{u}) (A : Ambient) (n : ℕ) :
    Abelian.Ext (stoneanPresentationKernel T) A (n + 1) →+
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A (n + 2) :=
  ((stoneanPresentationShortExact T).extClass).precomp A (by omega)

/-- Surjectivity follows from exactness at Ext^(n+2)(F_T,A):
Ext^(n+2)(P(T),A) vanishes since P(T) is projective. -/
theorem stoneanKernelHigherConnecting_surjective
    (T : Profinite.{u}) (A : Ambient) (n : ℕ) :
    Function.Surjective (stoneanKernelHigherConnecting T A n) := by
  intro z
  letI : Projective
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) :=
    freeStoneanPresentation_source_projective T
  have hz :
      (Abelian.Ext.mk₀ (freeStoneanPresentationMap T)).comp
        z (zero_add (n + 2)) = 0 := by
    exact Abelian.Ext.eq_zero_of_projective _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanPresentationShortExact T) A z hz
      (by omega : 1 + (n + 1) = n + 2)
  exact ⟨x, hx⟩

/-- Injectivity follows from exactness at Ext^(n+1)(K_T,A):
Ext^(n+1)(P(T),A) vanishes. This does not assume K_T projective. -/
theorem stoneanKernelHigherConnecting_injective
    (T : Profinite.{u}) (A : Ambient) (n : ℕ) :
    Function.Injective (stoneanKernelHigherConnecting T A n) := by
  letI : Projective
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) :=
    freeStoneanPresentation_source_projective T
  intro x y hxy
  have hzero : stoneanKernelHigherConnecting T A n (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanPresentationShortExact T).extClass.comp (x - y)
        (by omega : 1 + (n + 1) = n + 2) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanPresentationShortExact T) A (x - y)
      (by omega : 1 + (n + 1) = n + 2) hcomp
  have hz0 : z = 0 := Abelian.Ext.eq_zero_of_projective z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

/-- An actual additive equivalence, not only equality of dimensions. -/
noncomputable def stoneanKernelHigherExtAddEquiv
    (T : Profinite.{u}) (A : Ambient) (n : ℕ) :
    Abelian.Ext (stoneanPresentationKernel T) A (n + 1) ≃+
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A (n + 2) :=
  AddEquiv.ofBijective
    (stoneanKernelHigherConnecting T A n)
    ⟨stoneanKernelHigherConnecting_injective T A n,
      stoneanKernelHigherConnecting_surjective T A n⟩

/-- For any target in the genuine condensed module category, all higher
vanishing is equivalent to one degree lower on the actual Stonean kernel. -/
theorem freeProfinite_extHigher_vanishes_iff_kernel_extLower_vanishes
    (T : Profinite.{u}) (A : Ambient) (n : ℕ) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A (n + 2),
       e = 0) ↔
      (∀ e : Abelian.Ext (stoneanPresentationKernel T) A (n + 1),
       e = 0) := by
  constructor
  · intro h e
    apply stoneanKernelHigherConnecting_injective T A n
    calc
      stoneanKernelHigherConnecting T A n e = 0 := h _
      _ = stoneanKernelHigherConnecting T A n 0 := (map_zero _).symm
  · intro h e
    obtain ⟨x, rfl⟩ := stoneanKernelHigherConnecting_surjective T A n e
    rw [h x]
    exact map_zero _

/-- Exact degree-two obstruction for the ACTUAL free-solid coefficient
object G_S. Ext² is not asserted to vanish here. -/
theorem freeSolid_extTwo_vanishes_iff_stoneanKernel_extOne_vanishes
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) 2,
       e = 0) ↔
      (∀ e : Abelian.Ext (stoneanPresentationKernel T)
        ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) 1,
        e = 0) := by
  exact freeProfinite_extHigher_vanishes_iff_kernel_extLower_vanishes T
    ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) 0

/-- The corresponding all-higher-degrees reduction, again with no
assertion of vanishing on either side. -/
theorem freeSolid_extHigher_vanishes_iff_stoneanKernel_extLower_vanishes
    (T S : Profinite.{u}) (n : ℕ) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) (n + 2),
       e = 0) ↔
      (∀ e : Abelian.Ext (stoneanPresentationKernel T)
        ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) (n + 1),
        e = 0) := by
  exact freeProfinite_extHigher_vanishes_iff_kernel_extLower_vanishes T
    ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) n

#check stoneanKernelHigherConnecting
#check stoneanKernelHigherConnecting_surjective
#check stoneanKernelHigherConnecting_injective
#check stoneanKernelHigherExtAddEquiv
#check freeProfinite_extHigher_vanishes_iff_kernel_extLower_vanishes
#check freeSolid_extTwo_vanishes_iff_stoneanKernel_extOne_vanishes
#check freeSolid_extHigher_vanishes_iff_stoneanKernel_extLower_vanishes

#print axioms stoneanKernelHigherConnecting_surjective
#print axioms stoneanKernelHigherConnecting_injective
#print axioms stoneanKernelHigherExtAddEquiv
#print axioms freeProfinite_extHigher_vanishes_iff_kernel_extLower_vanishes
#print axioms freeSolid_extTwo_vanishes_iff_stoneanKernel_extOne_vanishes
#print axioms freeSolid_extHigher_vanishes_iff_stoneanKernel_extLower_vanishes

end CMDG.CondensedCM5R0
