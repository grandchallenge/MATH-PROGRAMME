import CMDGCondensedCM4P3DerivedCM5R0KernelHomExtension
import Mathlib.Condensed.Limits
import Mathlib.CategoryTheory.Limits.Shapes.Products

/-!
# CM5: explicit assembly of Stonean kernel extensions into products

Let T be *any* profinite test object, K_T the actual Stonean
presentation kernel in CondensedMod ZLift, and A_i arbitrary
condensed coefficient targets. Given extensions of each coordinate
of f:K_T→∏ A_i to the Stonean projective source, construct
the extension to the product by a categorical product lift.

Consequently if Ext¹(F_T,A_i)=0 for each i, then
Ext¹(F_T,∏ A_i)=0. The proof does not assume or require a
derived-Hom-to-product comparison: it directly constructs the
necessary kernel extension into the categorical product.

This supplies a rigorous *target-product assembly* gate. It does
not assert an isomorphism G_S ≅ ∏ Z in the pinned CM5 category,
nor prove the essential Ext¹(F_T,ZLift)=0 for infinite T.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Construct an extension of any actual Stonean-kernel morphism to
a categorical product target from extensions of each component. -/
theorem extendKernelHom_toProduct
    (T : Profinite.{u}) {ι : Type u} (A : ι → Ambient)
    (f : stoneanPresentationKernel T ⟶ ∏ᶜ i, A i)
    (h : ∀ i : ι,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
            (Stonean.toProfinite.obj T.presentation)) ⟶ A i,
        kernel.ι (freeStoneanPresentationMap T) ≫ g =
          f ≫ Pi.π A i) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
          (Stonean.toProfinite.obj T.presentation)) ⟶ ∏ᶜ i, A i,
      kernel.ι (freeStoneanPresentationMap T) ≫ g = f := by
  classical
  choose g hg using h
  refine ⟨Pi.lift g, ?_⟩
  apply Pi.hom_ext
  intro i
  calc
    (kernel.ι (freeStoneanPresentationMap T) ≫ Pi.lift g) ≫ Pi.π A i =
      kernel.ι (freeStoneanPresentationMap T) ≫
        (Pi.lift g ≫ Pi.π A i) := Category.assoc _ _ _
    _ = kernel.ι (freeStoneanPresentationMap T) ≫ g i := by
      rw [Pi.lift_π]
    _ = f ≫ Pi.π A i := hg i

/-- Exact degree-one coefficient transport: componentwise Ext¹
vanishing implies Ext¹ vanishing into their categorical product
for arbitrary profinite T, by *constructing* the required
kernel extension. -/
theorem freeProfinite_extOne_product_vanishes_of_components
    (T : Profinite.{u}) {ι : Type u} (A : ι → Ambient)
    (h : ∀ i : ι,
      ∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) (A i) 1,
        e = 0) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T) (∏ᶜ i, A i) 1, e = 0 := by
  apply (freeProfinite_extOne_vanishes_iff_kernel_hom_extends
    T (∏ᶜ i, A i)).2
  intro f
  apply extendKernelHom_toProduct T A f
  intro i
  exact (freeProfinite_extOne_vanishes_iff_kernel_hom_extends
    T (A i)).1 (h i) (f ≫ Pi.π A i)

#print axioms extendKernelHom_toProduct
#print axioms freeProfinite_extOne_product_vanishes_of_components

end CMDG.CondensedCM5R0
