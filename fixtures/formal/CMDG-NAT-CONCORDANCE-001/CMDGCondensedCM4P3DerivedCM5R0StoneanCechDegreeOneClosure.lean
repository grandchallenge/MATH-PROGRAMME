import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeTrueDegreeOneExact
import CMDGCondensedCM4P3DerivedCM5R0DenseExactnessTransfer
import Mathlib.CategoryTheory.Abelian.FunctorCategory

/-!
# CMDG CM5 — unconditional second Čech relation epimorphism

For ANY profinite T, the genuine free Coeff-module presheaf short complex
associated to P(T) → T is exact after restriction to Stonean test objects.

1. Each Stonean U sees exactly the genuine represented ULift Čech pair and
   triple free-module complex, definitionally identified with the existing
   short complex. The protected Stonean splitting makes it exact.
2. An abelian functor category reflects short-complex exactness under
   all its evaluations; this is established here via its kernel/cokernel
   comparison and pointwise componentwise equality.
3. The existing protected dense-site theorem transports Stonean presheaf
   exactness through exact sheafification to the REAL condensed-module
   Čech short complex, not an invented surrogate.
4. The protected second-syzygy criterion identifies this exactness with
   Epi(F_Q → L_T), the genuine triple boundary onto the second relation.

This proves the previously OPEN global second-relation epimorphism, but not
by itself arbitrary-profinite Ext² vanishing, a splitting of the second
syzygy, higher derived solidity, source-semantic equivalence, or a MATHCERT
certificate. Those remain distinct research and authority obligations.
-/

noncomputable section
universe u v w z
open CategoryTheory Limits
variable {C : Type w} [Category.{z} C]
variable {D : Type u} [Category.{v} D] [Abelian D]
namespace CMDG.CondensedCM5R0

theorem functorShortComplex_exact_of_pointwise
    (S : ShortComplex (C ⥤ D))
    (h : ∀ x : C, (S.map ((evaluation C D).obj x)).Exact) :
    S.Exact := by
  rw [ShortComplex.exact_iff_kernel_ι_comp_cokernel_π_zero]
  apply NatTrans.ext
  funext x
  let F := (evaluation C D).obj x
  have hS := h x
  rw [ShortComplex.exact_iff_kernel_ι_comp_cokernel_π_zero] at hS
  change kernel.ι (F.map S.g) ≫ cokernel.π (F.map S.f) = 0 at hS
  have hMap : F.map (kernel.ι S.g ≫ cokernel.π S.f) = 0 := by
    obtain ⟨k, hk⟩ :=
      kernel.lift' (F.map S.g) (F.map (kernel.ι S.g))
        (by simp only [← F.map_comp, kernel.condition, CategoryTheory.Functor.map_zero])
    obtain ⟨l, hl⟩ :=
      cokernel.desc' (F.map S.f) (F.map (cokernel.π S.f))
        (by simp only [← F.map_comp, cokernel.condition, CategoryTheory.Functor.map_zero])
    rw [F.map_comp, ← hl, ← hk, Category.assoc, reassoc_of% hS, zero_comp, comp_zero]
  exact hMap

/-- Exactness of the genuine restricted presheaf complex, proved at every Stonean test. -/
theorem stoneanRestrictedCechDegreeOne_exact
    (T : Profinite.{u}) :
    (stoneanRestrictedCechDegreeOneComplex T).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  change (trueProbeDegreeOneComplex T U.unop).Exact
  exact trueProbeDegreeOne_exact T U.unop

/-- Global exactness of the genuine condensed-module Čech short complex. -/
theorem stoneanCechDegreeOne_exact_unconditional
    (T : Profinite.{u}) :
    (stoneanCechDegreeOneComplex T).Exact :=
  stoneanCechDegreeOneExact_of_stoneanPresheafExact T
    (stoneanRestrictedCechDegreeOne_exact T)

/-- Global second Čech relation epimorphism for any profinite T. -/
theorem stoneanCechTripleToSecondRelation_epi_unconditional
    (T : Profinite.{u}) :
    Epi (stoneanCechTripleToSecondRelation T) :=
  stoneanCechTripleToSecondRelation_epi_of_stoneanPresheafExact T
    (stoneanRestrictedCechDegreeOne_exact T)

#print axioms functorShortComplex_exact_of_pointwise
#print axioms stoneanRestrictedCechDegreeOne_exact
#print axioms stoneanCechDegreeOne_exact_unconditional
#print axioms stoneanCechTripleToSecondRelation_epi_unconditional

end CMDG.CondensedCM5R0
