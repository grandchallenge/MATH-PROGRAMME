import CMDGCondensedCM4P3DerivedCM5R0UniformExtLongExactShift
import Mathlib.CategoryTheory.Limits.Shapes.Kernels

noncomputable section
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Given any epic factor through a monomorphism, the kernel
of the composite is also the kernel of the epic factor. Thus
the evident sequence is genuinely short exact, without
assuming the source is projective. -/
theorem kernel_of_epi_factor_shortExact
    {X Y Z : Ambient} (q : X ⟶ Y) (m : Y ⟶ Z)
    [Epi q] [Mono m] :
    (ShortComplex.mk
       (kernel.ι (q ≫ m)) q (by
          apply (cancel_mono m).1
          simpa only [Category.assoc, zero_comp] using
            (kernel.condition (q ≫ m)))).ShortExact := by
  have hz : kernel.ι (q ≫ m) ≫ q = 0 := by
    apply (cancel_mono m).1
    simpa only [Category.assoc, zero_comp] using
      (kernel.condition (q ≫ m))
  let S := ShortComplex.mk (kernel.ι (q ≫ m)) q hz
  have hisLimit : IsLimit
      (KernelFork.ofι (kernel.ι (q ≫ m)) hz) :=
    isKernelOfComp (f := q) m (q ≫ m)
      (kernelIsKernel (q ≫ m)) hz rfl
  letI : Mono (kernel.ι (q ≫ m)) := inferInstance
  exact ShortComplex.ShortExact.mk
    (S.exact_of_f_is_kernel hisLimit)

#print axioms kernel_of_epi_factor_shortExact
end CMDG.CondensedCM5R0
