import CMDGCondensedCM4P3MFiniteQuotientBridge

/-!
# CMDG CM4 P3-M — pointwise Nöbeling kernel vanishing

This successor is the bounded `CMDG-CM4-P3-M-KERNEL-POINT-002` theorem file.  It starts from the
protected finite-stage evaluation-weight/Dirac machinery and develops only the point-mass
comparison needed to turn a solidification-kernel hypothesis into the pointwise Nöbeling
vanishing statement frozen in issue #664.

No coefficient-object solidity, finite-stage mapping-out theorem, P3 completion, or CM4 closure is
asserted here.
-/

namespace CMDG.CondensedCM4P3M.KernelPointVanishing

universe u

open CategoryTheory Limits Opposite
open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3L.KernelFunctional
open CMDG.CondensedCM4P3M.KernelPointBridge

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The one-point profinite probe selecting a chosen point of `X`. -/
noncomputable def profinitePointProbe (X : Profinite.{u}) (x : X) :
    Profinite.of PUnit.{u + 1} ⟶ X :=
  ConcreteCategory.ofHom
    { toFun := fun _ => x
      continuous_toFun := continuous_const }

/-- Passing a point probe through a finite quotient selects the represented quotient point. -/
theorem profinitePointProbe_comp_finiteQuotientMap
    (X : Profinite.{u}) (x : X) (j : DiscreteQuotient X) :
    profinitePointProbe X x ≫ finiteQuotientMap X j =
      profinitePointProbe (X.diagram.obj j) (j.proj x) := by
  ext z
  rfl

#check profinitePointProbe
#check profinitePointProbe_comp_finiteQuotientMap
#print axioms profinitePointProbe_comp_finiteQuotientMap

end CMDG.CondensedCM4P3M.KernelPointVanishing
