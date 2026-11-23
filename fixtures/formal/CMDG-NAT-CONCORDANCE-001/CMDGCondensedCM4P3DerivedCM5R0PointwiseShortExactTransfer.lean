import Mathlib.CategoryTheory.Abelian.ShortExact
import Mathlib.CategoryTheory.Abelian.FunctorCategory
import Mathlib.CategoryTheory.Limits.FunctorCategory.EpiMono
import Mathlib.CategoryTheory.Abelian.Exact

noncomputable section
universe u v w z
open CategoryTheory CategoryTheory.Limits
namespace CMDG.CondensedCM5R0.CategoryExactness

variable {C : Type u} [Category.{v} C]
  {D : Type w} [Category.{z} D] [Abelian D]
variable (S : ShortComplex (C ⥤ D))

theorem shortExact_of_pointwise
    (h : ∀ x : C, (S.map ((evaluation C D).obj x)).ShortExact) :
    S.ShortExact := by
  have hm : Mono S.f := by
    apply (NatTrans.mono_iff_mono_app S.f).2
    intro x
    change Mono ((S.map ((evaluation C D).obj x)).f)
    exact (h x).mono_f
  have he : Epi S.g := by
    apply (NatTrans.epi_iff_epi_app S.g).2
    intro x
    change Epi ((S.map ((evaluation C D).obj x)).g)
    exact (h x).epi_g
  apply ShortComplex.ShortExact.mk' ?_ hm he
  rw [ShortComplex.exact_iff_kernel_ι_comp_cokernel_π_zero]
  ext x
  let F : (C ⥤ D) ⥤ D := (evaluation C D).obj x
  have hS := (h x).exact
  rw [ShortComplex.exact_iff_kernel_ι_comp_cokernel_π_zero] at hS
  change F.map (kernel.ι S.g ≫ cokernel.π S.f) = 0
  obtain ⟨k, hk⟩ :=
    kernel.lift' (F.map S.g) (F.map (kernel.ι S.g))
      (by simp only [← F.map_comp, kernel.condition, Functor.map_zero])
  obtain ⟨l, hl⟩ :=
    cokernel.desc' (F.map S.f) (F.map (cokernel.π S.f))
      (by simp only [← F.map_comp, cokernel.condition, Functor.map_zero])
  change kernel.ι (F.map S.g) ≫ cokernel.π (F.map S.f) = 0 at hS
  rw [F.map_comp, ← hl, ← hk]
  calc
    (k ≫ kernel.ι (F.map S.g)) ≫
        (cokernel.π (F.map S.f) ≫ l) =
      k ≫ ((kernel.ι (F.map S.g) ≫ cokernel.π (F.map S.f)) ≫ l) := by
        simp only [Category.assoc]
    _ = 0 := by rw [hS]; simp

#print axioms shortExact_of_pointwise
end CMDG.CondensedCM5R0.CategoryExactness
