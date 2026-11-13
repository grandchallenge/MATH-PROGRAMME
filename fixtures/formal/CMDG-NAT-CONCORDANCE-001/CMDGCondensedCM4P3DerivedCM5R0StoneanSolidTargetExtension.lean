import CMDGCondensedCM4P3DerivedCM5R0KernelHomExtension
import Mathlib.Algebra.Homology.ShortComplex.ShortExact

/-!
# CM5: explicit Stonean kernel extensions into actual solid coefficient targets

For any Stonean source P (possibly infinite), the canonical Stonean
presentation of its underlying profinite space admits a splitting,
since the actual free condensed module on P is projective.
A concrete retraction of the kernel inclusion extends *every* map
from that kernel into any condensed module A by composition.

In particular, the target may be the exact protected CM4 solid
coefficient object G_S = (Condensed.profiniteSolid Coeff).obj S
for arbitrary profinite S. This is an actual constructed extension,
not merely a derived Ext vanishing or a statement that extension
exists by an unidentified argument.

**Boundary:** the source T here is Stonean. For an arbitrary
non-Stonean profinite source the splitting cannot be assumed, and
this theorem does not imply the required universal extensions.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The exact Stonean presentation of an already Stonean profinite
source splits; the source of the short exact sequence is the kernel
of the actual free-condensed epi. -/
noncomputable def stoneanSourcePresentationSplitting
    (P : Stonean.{u}) :
    (stoneanPresentationShortComplex
      (Stonean.toProfinite.obj P)).Splitting := by
  let T : Profinite.{u} := Stonean.toProfinite.obj P
  letI : Projective ((Condensed.profiniteFree Coeff).obj T) :=
    freeStonean_projective P
  exact (stoneanPresentationShortExact T).splittingOfProjective

/-- An explicitly constructed extension of any kernel map f for an
already Stonean source, by the retraction of its kernel inclusion. -/
noncomputable def extendStoneanKernelHom
    (P : Stonean.{u}) (A : Ambient)
    (f : stoneanPresentationKernel (Stonean.toProfinite.obj P) ⟶ A) :
    ((Condensed.profiniteFree Coeff).obj
      (Stonean.toProfinite.obj
        (Stonean.toProfinite.obj P).presentation)) ⟶ A :=
  (stoneanSourcePresentationSplitting P).r ≫ f

/-- The construction is an actual lift of the original map in the
universe-lifted condensed-module category. -/
theorem extendStoneanKernelHom_restrict
    (P : Stonean.{u}) (A : Ambient)
    (f : stoneanPresentationKernel (Stonean.toProfinite.obj P) ⟶ A) :
    kernel.ι (freeStoneanPresentationMap (Stonean.toProfinite.obj P)) ≫
      extendStoneanKernelHom P A f = f := by
  change
    (stoneanPresentationShortComplex (Stonean.toProfinite.obj P)).f ≫
      ((stoneanSourcePresentationSplitting P).r ≫ f) = f
  rw [← Category.assoc, (stoneanSourcePresentationSplitting P).f_r]
  simp

/-- Explicit extension into the *actual* CM4 free solid target G_S
for arbitrary profinite S, when the source test P is Stonean. -/
theorem extendStoneanKernelHom_toSolidTarget
    (P : Stonean.{u}) (S : Profinite.{u})
    (f : stoneanPresentationKernel (Stonean.toProfinite.obj P) ⟶
      underivedObject S) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj
          (Stonean.toProfinite.obj P).presentation)) ⟶ underivedObject S,
      kernel.ι (freeStoneanPresentationMap (Stonean.toProfinite.obj P)) ≫ g = f := by
  exact ⟨extendStoneanKernelHom P (underivedObject S) f,
    extendStoneanKernelHom_restrict P (underivedObject S) f⟩

#print axioms stoneanSourcePresentationSplitting
#print axioms extendStoneanKernelHom_restrict
#print axioms extendStoneanKernelHom_toSolidTarget

end CMDG.CondensedCM5R0
