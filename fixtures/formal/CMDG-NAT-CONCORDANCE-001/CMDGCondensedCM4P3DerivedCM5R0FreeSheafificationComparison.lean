import CMDGCondensedCM4P3DerivedCM5R0StoneanProbeBarDescent
import Mathlib.Algebra.Homology.ShortComplex.ExactFunctor
import Mathlib.CategoryTheory.Sites.Abelian

/-!
# CMDG CM5 — genuine free-condensed-module sheafification comparison

This is the essential SHEAFIFICATION interface, not an identification
of a free abelian group on Hom(U,X) with F_X(U).

For any profinite X, the genuine free condensed Coeff-module F_X is
the associated sheaf of the presheaf of ordinary free Coeff-modules on
the (universe-lifted) representable condensed SET presheaf of X.

More strongly, this identification is NATURAL in X, with all module
maps given by the actual functor ModuleCat.free. The sheafification
functor is exact between the genuine abelian presheaf and sheaf module
categories: it preserves both finite limits (pinned left exact
sheafification) and finite colimits (pinned left adjoint).

CRITICAL: The preceding bar contraction is objectwise exact on
Stonean test objects, not necessarily on all CompHaus test objects.
One must still transport that exactness through the Stonean dense-site
comparison to infer an exact sheafified complex on CompHaus.
No global arbitrary-profinite second Cech relation epi is asserted
in this source, and no Ext² or derived solidity claim is made.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Presheaves of the *actual* universe-lifted coefficient modules on
CompHaus, rather than unsheafified integer functions. -/
private abbrev CompHausModulePresheaves :=
  CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff

/-- The true ordinary free module presheaf on the representable
condensed set of X, before sheafification. -/
noncomputable abbrev freeCompHausModulePresheaf
    (X : Profinite.{u}) : CompHausModulePresheaves :=
  (profiniteToCondensed.obj X).obj ⋙ ModuleCat.free Coeff

/-- Sheafification of module presheaves with the actual coherent
CompHaus topology, into the exact CondensedMod category. -/
noncomputable abbrev moduleSheafification :
    CompHausModulePresheaves ⥤ Ambient :=
  presheafToSheaf (coherentTopology CompHaus) (ModuleCat Coeff)

/-- The NATURAL presheaf of free modules on the representable
profinite-to-condensed set, with maps induced by profinite morphisms. -/
noncomputable abbrev freeCompHausModulePresheafFunctor :
    Profinite.{u} ⥤ CompHausModulePresheaves :=
  profiniteToCondensed ⋙
    sheafToPresheaf (coherentTopology CompHaus) (Type (u + 1)) ⋙
      (Functor.whiskeringRight _ _ _).obj (ModuleCat.free Coeff)

/-- The actual free condensed module F_X is precisely the
SHEAFIFICATION of the free module presheaf of X. This is the
sheafification comparison, not an incorrect objectwise equality. -/
theorem genuineFreeModule_eq_sheafification (X : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj X =
      moduleSheafification.obj (freeCompHausModulePresheaf X) := by
  rfl

/-- The comparison in the preceding theorem is NATURAL in all
profinite morphisms: it uses the genuine, preexisting free functor
on the site, not chosen local generators. -/
noncomputable def genuineFreeModuleSheafificationIso :
    freeCompHausModulePresheafFunctor ⋙ moduleSheafification ≅
      Condensed.profiniteFree Coeff :=
  Iso.refl _

/-- Left exactness of the actual sheafification on the abelian
presheaf category of Coeff-modules. -/
theorem moduleSheafification_preservesFiniteLimits :
    PreservesFiniteLimits moduleSheafification := by
  infer_instance

/-- Right exactness follows from the genuine sheafification adjunction:
the associated-sheaf functor is a LEFT adjoint. -/
theorem moduleSheafification_preservesFiniteColimits :
    PreservesFiniteColimits moduleSheafification := by
  infer_instance

/-- Sheafification is exact on the genuine abelian module presheaf
category, so it transports the exactness of ANY pre-sheaf short
complex, once source exactness is proved (at all test objects or,
after restriction, on a dense projective subsite). -/
theorem moduleSheafification_preservesExact
    (S : ShortComplex CompHausModulePresheaves) (h : S.Exact) :
    (S.map moduleSheafification).Exact := by
  haveI : PreservesFiniteLimits moduleSheafification :=
    moduleSheafification_preservesFiniteLimits
  haveI : PreservesFiniteColimits moduleSheafification :=
    moduleSheafification_preservesFiniteColimits
  have hExact :
      ∀ (R : ShortComplex CompHausModulePresheaves),
        R.Exact → (R.map moduleSheafification).Exact :=
    ((Functor.exact_tfae moduleSheafification).out 3 1).mp
      ⟨moduleSheafification_preservesFiniteLimits,
        moduleSheafification_preservesFiniteColimits⟩
  exact hExact S h

#print axioms genuineFreeModule_eq_sheafification
#print axioms genuineFreeModuleSheafificationIso
#print axioms moduleSheafification_preservesFiniteLimits
#print axioms moduleSheafification_preservesFiniteColimits
#print axioms moduleSheafification_preservesExact

end CMDG.CondensedCM5R0
