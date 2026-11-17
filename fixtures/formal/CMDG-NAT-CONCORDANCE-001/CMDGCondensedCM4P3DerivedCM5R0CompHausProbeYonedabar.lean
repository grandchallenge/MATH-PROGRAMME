import CMDGCondensedCM4P3DerivedCM5R0StoneanProbeBarDescent
import CMDGCondensedCM4P3DerivedCM5R0StoneanEffectiveDescent
import Mathlib.Condensed.Epi
import Mathlib.AlgebraicTopology.ExtraDegeneracy

/-!
# CMDG CM5 — the TRUE CompHaus-site Stonean probe Čech contraction

The earlier Stonean-probe bar contraction was built on the
*Profinite* Hom sets Hom_Profinite(U,P(T)) → Hom_Profinite(U,T).
But the genuine free condensed-module presheaf is built on
the represented CompHaus-site Hom sets. This module constructs
the split epi for the EXACT universe-lifted CompHaus Hom map
appearing in that true representable presheaf, using
Stonean projectivity and the genuine profinite presentation.

It identifies the map with the actual morphism of represented
condensed SET presheaves, not merely a surrogate set function,
and constructs the all-degree free-module Čech homotopy
equivalence for this exact CompHaus-site map.

The remaining step is the natural degree-one/two face comparison
with the genuine *profinite* pair and triple fiber-product
representables, to infer exactness of the restricted presheaf.
No unconditional global F_triples → L_T epi, Ext² vanishing, or
derived solidity is claimed in this file.
-/

noncomputable section

universe u

open CategoryTheory Limits Opposite

namespace CMDG.CondensedCM5R0

/-- The genuine (not replacement) CompHaus representable Hom-set
map induced by the canonical profinite Stonean cover P(T) → T.
The universe lift is the one used by profiniteToCondensed. -/
noncomputable def stoneanCompHausProbePresentationMap
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶
        profiniteToCompHaus.obj
          (Stonean.toProfinite.obj T.presentation)) ⟶
      ULift.{u + 1} (U.compHaus ⟶
        profiniteToCompHaus.obj T) :=
  ↾fun z => ULift.up
    (z.down ≫ profiniteToCompHaus.map (Profinite.presentation.π T))

/-- Stonean projectivity splits the true CompHaus Hom-set map.
It does not produce a section T → P(T) of the profinite cover. -/
noncomputable def stoneanCompHausProbePresentationSplitEpi
    (T : Profinite.{u}) (U : Stonean.{u}) :
    SplitEpi (stoneanCompHausProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  letI : EffectiveEpi p := stoneanPresentation_effectiveEpi_profinite T
  letI : EffectiveEpi (profiniteToCompHaus.map p) := inferInstance
  haveI : Epi (profiniteToCompHaus.map p) := inferInstance
  refine {
    section_ := ↾fun z => ULift.up
      (Stonean.lift z.down (profiniteToCompHaus.map p))
    id := ?_
  }
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro z
  rcases z with ⟨q⟩
  exact congrArg ULift.up
    (Stonean.lift_lifts q (profiniteToCompHaus.map p))

/-- This is *exactly* the morphism of the true represented
condensed-set presheaves, evaluated at the Stonean CompHaus
test object, rather than merely an isomorphic alternative. -/
theorem stoneanCompHausProbePresentationMap_eq_condensed_app
    (T : Profinite.{u}) (U : Stonean.{u}) :
    stoneanCompHausProbePresentationMap T U =
      (profiniteToCondensed.map
        (Profinite.presentation.π T)).hom.app (op U.compHaus) := by
  rfl

/-- Full augmented Čech nerve of the exact represented
CompHaus Hom-set presentation map at Stonean U. -/
noncomputable def stoneanCompHausProbePresentationCechNerve
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  (Arrow.mk (stoneanCompHausProbePresentationMap T U)).augmentedCechNerve

/-- All-degree split-epi extra degeneracy of the REAL
CompHaus-site representable probe's Čech nerve. -/
noncomputable def stoneanCompHausProbePresentationExtraDegeneracy
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  Arrow.AugmentedCechNerve.extraDegeneracy
    (Arrow.mk (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbePresentationSplitEpi T U)

/-- Genuine free-module Čech contracting extra degeneracy on
the actual represented Hom sets, not sheaf evaluations. -/
noncomputable def stoneanCompHausProbeFreeExtraDegeneracy
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  (stoneanCompHausProbePresentationExtraDegeneracy T U).map
    (ModuleCat.free Coeff)

/-- All-degree homotopy equivalence of the actual CompHaus-site
free Hom-set Čech bar resolution. -/
noncomputable def stoneanCompHausProbeFreeCechHomotopyEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  (stoneanCompHausProbeFreeExtraDegeneracy T U).homotopyEquiv

/-- The actual CompHaus represented-free module bar complex. -/
noncomputable abbrev stoneanCompHausProbeFreeBarComplex
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ChainComplex (ModuleCat.{u + 1} Coeff) ℕ :=
  AlgebraicTopology.AlternatingFaceMapComplex.obj
    (SimplicialObject.Augmented.drop.obj
      (((SimplicialObject.Augmented.whiskering _ _).obj
        (ModuleCat.free Coeff)).obj
          (stoneanCompHausProbePresentationCechNerve T U)))

/-- Positive-degree exactness of the free bar complex formed
from the EXACT CompHaus-site representable presentation map. -/
theorem stoneanCompHausProbeFreeBarComplex_exactAt_positive
    (T : Profinite.{u}) (U : Stonean.{u}) (n : ℕ) :
    (stoneanCompHausProbeFreeBarComplex T U).ExactAt (n + 1) := by
  let e := stoneanCompHausProbeFreeCechHomotopyEquiv T U
  haveI : QuasiIso e.hom := e.quasiIso_hom
  exact (exactAt_iff_of_quasiIsoAt e.hom (n + 1)).2
    (ChainComplex.exactAt_succ_single_obj _ n)

#check stoneanCompHausProbePresentationSplitEpi
#check stoneanCompHausProbePresentationMap_eq_condensed_app
#check stoneanCompHausProbeFreeBarComplex_exactAt_positive

#print axioms stoneanCompHausProbePresentationSplitEpi
#print axioms stoneanCompHausProbePresentationMap_eq_condensed_app
#print axioms stoneanCompHausProbeFreeCechHomotopyEquiv
#print axioms stoneanCompHausProbeFreeBarComplex_exactAt_positive

end CMDG.CondensedCM5R0
