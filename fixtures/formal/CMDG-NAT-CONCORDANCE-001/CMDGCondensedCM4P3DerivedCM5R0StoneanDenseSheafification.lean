import CMDGCondensedCM4P3DerivedCM5R0FreeSheafificationComparison
import Mathlib.CategoryTheory.Sites.DenseSubsite.SheafEquiv
import Mathlib.Algebra.Homology.QuasiIso
import Mathlib.Algebra.Homology.SingleHomology

/-!
# CMDG CM5 — dense Stonean-site sheafification compatibility

The genuine free condensed module on any profinite X is naturally
isomorphic to the sheafification of its ordinary free-module
representable presheaf on CompHaus (prior module).

The pinned dense-subsite comparison theorem supplies the exact
NATURAL ISOMORPHISM between the Stonean restriction of this
CompHaus sheafification and the sheafification of the Stonean
restriction of the unsheafified free presheaf. This directly
accounts for local clopen gluing; it does NOT identify the free
presheaf itself with the sheaf.

Separately, the previously verified Stonean-probe free-Hom Čech
homotopy equivalence yields ACTUAL exactness in EVERY POSITIVE
DEGREE of the bar complex at each Stonean probe. This is a
module-category exactness result rather than a mere split-epi
statement on Hom sets.

The remaining global obligation is to assemble these natural
identifications into the Čech simplicial chain complex, then
transport the degree-one exactness through the exact sheafification
and check that the alternating differential coincides (up to the
explicit sign convention) with the genuine second kernel map
F_triples → L_T. No global epi or Ext² claim is made here.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- **Genuine pinned dense-subsite theorem.** Sheafification of
module presheaves on CompHaus, then restriction to Stonean, is
naturally isomorphic to restriction first and then Stonean
sheafification. The target is the *actual* Stonean-to-CompHaus
condensed-module equivalence, not a new artificial module category. -/
noncomputable def stoneanCompHausSheafificationCompatibility :
    (Functor.whiskeringLeft _ _ (ModuleCat.{u + 1} Coeff)).obj
        Stonean.toCompHaus.op ⋙
          presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff)
      ≅
    moduleSheafification ⋙
        (Condensed.StoneanCompHaus.equivalence
          (ModuleCat Coeff)).inverse := by
  exact Functor.IsDenseSubsite.sheafEquivSheafificationCompatibility
    Stonean.toCompHaus (coherentTopology Stonean)
      (coherentTopology CompHaus) (ModuleCat Coeff)

/-- Canonical sheafified comparison at ANY profinite X:
the Stonean sheafification of the free-Hom presheaf is the
Stonean restriction of the GENUINE free condensed module F_X.
In particular it includes every clopen-local section. -/
noncomputable def genuineFreeStoneanSheafificationIso
    (X : Profinite.{u}) :
    (presheafToSheaf (coherentTopology Stonean)
      (ModuleCat Coeff)).obj
      (((Functor.whiskeringLeft _ _ (ModuleCat Coeff)).obj
        Stonean.toCompHaus.op).obj (freeCompHausModulePresheaf X))
      ≅
    (Condensed.StoneanCompHaus.equivalence
      (ModuleCat Coeff)).inverse.obj
        ((Condensed.profiniteFree Coeff).obj X) := by
  change
    (presheafToSheaf (coherentTopology Stonean)
      (ModuleCat Coeff)).obj
      (((Functor.whiskeringLeft _ _ (ModuleCat Coeff)).obj
        Stonean.toCompHaus.op).obj (freeCompHausModulePresheaf X))
      ≅
    (Condensed.StoneanCompHaus.equivalence
      (ModuleCat Coeff)).inverse.obj
        (moduleSheafification.obj (freeCompHausModulePresheaf X))
  exact stoneanCompHausSheafificationCompatibility.app
    (freeCompHausModulePresheaf X)

/-- The ACTUAL free Hom-set alternating Čech chain complex of
the projective Stonean probe, not the sheafified complex. -/
noncomputable abbrev stoneanProbeFreeBarComplex
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ChainComplex (ModuleCat.{u + 1} Coeff) ℕ :=
  AlgebraicTopology.AlternatingFaceMapComplex.obj
    (SimplicialObject.Augmented.drop.obj
      (((SimplicialObject.Augmented.whiskering _ _).obj
        (ModuleCat.free Coeff)).obj
          (stoneanProbePresentationCechNerve T U)))

/-- For EACH Stonean U and EVERY degree n+1, the actual objectwise
free-Hom bar complex is exact. We use the true quasi-isomorphism
induced by the previously established chain-homotopy equivalence
to the degree-zero augmentation, not an informal pointwise claim. -/
theorem stoneanProbeFreeBarComplex_exactAt_positive
    (T : Profinite.{u}) (U : Stonean.{u}) (n : ℕ) :
    (stoneanProbeFreeBarComplex T U).ExactAt (n + 1) := by
  let e := stoneanProbeFreeCechHomotopyEquiv T U
  haveI : QuasiIso e.hom := e.quasiIso_hom
  exact (HomologicalComplex.exactAt_iff_of_quasiIsoAt
    e.hom (n + 1)).2
    (ChainComplex.exactAt_succ_single_obj _ n)

#check genuineFreeStoneanSheafificationIso
#check stoneanProbeFreeBarComplex_exactAt_positive
#print axioms genuineFreeStoneanSheafificationIso
#print axioms stoneanProbeFreeBarComplex_exactAt_positive

end CMDG.CondensedCM5R0
