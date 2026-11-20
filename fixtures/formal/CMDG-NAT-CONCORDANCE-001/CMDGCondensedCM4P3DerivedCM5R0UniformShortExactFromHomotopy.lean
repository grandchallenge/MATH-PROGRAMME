import Mathlib.Algebra.Homology.ShortComplex.Exact

noncomputable section
open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The homotopy identity id_Y = h∘f + g∘k
certifies categorical short-complex exactness without
assuming projective middle terms. -/
theorem shortComplex_exact_of_middle_homotopy
    {C : Type*} [Category C] [Abelian C]
    (S : ShortComplex C)
    (h : S.X₂ ⟶ S.X₁) (k : S.X₃ ⟶ S.X₂)
    (hh : h ≫ S.f + S.g ≫ k = 𝟙 S.X₂) :
    S.Exact := by
  apply (S.exact_iff_kernel_ι_comp_cokernel_π_zero).2
  have hzero : kernel.ι S.g ≫ S.g = 0 := kernel.condition S.g
  have hzero' : S.f ≫ cokernel.π S.f = 0 :=
    cokernel.condition S.f
  calc
    kernel.ι S.g ≫ cokernel.π S.f =
        (kernel.ι S.g ≫ (h ≫ S.f + S.g ≫ k)) ≫ cokernel.π S.f := by
      rw [hh]
      simp
    _ = 0 := by
      simp only [Preadditive.comp_add, Preadditive.add_comp,
        Category.assoc, hzero', comp_zero, zero_add]
      simpa only [← Category.assoc, hzero, zero_comp, comp_zero]

#print axioms shortComplex_exact_of_middle_homotopy
end CMDG.CondensedCM5R0
