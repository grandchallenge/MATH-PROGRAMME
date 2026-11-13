import CMDGCondensedCM4P3DerivedCM5R0ExtOneEquivalence
import Mathlib.Condensed.Functors
import Mathlib.Condensed.Module

/-!
# CM5: canonical degree-zero free/Yoneda evaluation interface

For each arbitrary (including infinite) profinite test T and each
ambient condensed module A, identify the **actual** free condensed
module on T with the left side of the free/forgetful adjunction.

The resulting equivalence of Hom sets is natural in the target A,
and uses the precisely pinned universe-lifted coefficient ring.

This is an underived Hom/sections interface; it does not claim
derived adjunction, higher Ext acyclicity, or derived solidity.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- Canonical free-forgetful Hom equivalence for the actual CM5
free condensed module, for arbitrary profinite T. -/
noncomputable def freeProfiniteHomEquiv (T : Profinite.{u}) (A : Ambient) :
    (((Condensed.profiniteFree Coeff).obj T) ⟶ A) ≃
      (T.toCondensed ⟶ (Condensed.forget Coeff).obj A) :=
  (Condensed.freeForgetAdjunction Coeff).homEquiv T.toCondensed A

/-- The equivalence intertwines postcomposition in the actual condensed
category with postcomposition after forgetting the module structure. -/
theorem freeProfiniteHomEquiv_naturality_target
    (T : Profinite.{u}) {A B : Ambient}
    (g : ((Condensed.profiniteFree Coeff).obj T) ⟶ A) (f : A ⟶ B) :
    freeProfiniteHomEquiv T B (g ≫ f) =
      freeProfiniteHomEquiv T A g ≫ (Condensed.forget Coeff).map f :=
  (Condensed.freeForgetAdjunction Coeff).homEquiv_naturality_right g f

#print axioms freeProfiniteHomEquiv
#print axioms freeProfiniteHomEquiv_naturality_target

end CMDG.CondensedCM5R0
