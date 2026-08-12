import Mathlib.Algebra.Homology.DerivedCategory.Ext.EnoughInjectives
import Mathlib.Algebra.Homology.DerivedCategory.Ext.EnoughProjectives
import Mathlib.CategoryTheory.Preadditive.Projective.Internal
import Mathlib.CategoryTheory.Sites.Abelian
import Mathlib.CategoryTheory.Sites.GlobalSections
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.CategoryTheory.Sites.SheafCohomology.Cech
import Mathlib.Condensed.Discrete.Characterization
import Mathlib.Condensed.Epi
import Mathlib.Condensed.Light.InternallyProjective
import Mathlib.Topology.Category.Profinite.Projective
import Mathlib.Topology.Separation.Profinite

/-!
# CMDG CM4-P3 exact-tree audit probe

This file deliberately proves no CM4-P3 vanishing theorem. It certifies that the
pinned mathlib closure exposes the generic Ext, injective/projective vanishing,
sheaf-abelian, global-sections, sheaf-cohomology, Cech, discrete-condensed,
epimorphism, internal-projectivity, and profinite-topology interfaces recorded by
the governed CM4-P3 audit. The missing profinite/discrete acyclicity bridge remains
a separately governed blocking obligation.
-/

namespace CMDG.CondensedCM4P3Audit

#check CategoryTheory.HasExt
#check CategoryTheory.Abelian.Ext.eq_zero_of_injective
#check CategoryTheory.Abelian.Ext.subsingleton_of_injective
#check CategoryTheory.Abelian.Ext.eq_zero_of_projective
#check CategoryTheory.Abelian.Ext.subsingleton_of_projective
#check CategoryTheory.hasExt_of_enoughInjectives
#check CategoryTheory.sheafIsAbelian
#check CategoryTheory.Sheaf.Γ
#check CategoryTheory.Sheaf.ΓNatIsoSheafSections
#check CategoryTheory.Sheaf.ΓNatIsoLim
#check CategoryTheory.Sheaf.isLimitConeΓ
#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.H'
#check CategoryTheory.cechComplexFunctor
#check CategoryTheory.InternallyProjective
#check CondensedMod.LocallyConstant.functorIsoDiscrete
#check CondensedMod.LocallyConstant.adjunction
#check CondensedMod.isDiscrete_tfae
#check CondensedMod.epi_iff_locallySurjective_on_compHaus
#check CondensedMod.epi_iff_surjective_on_stonean
#check LightCondensed.internallyProjective_iff_tensor_condition
#check Profinite.projectivePresentation
#check exists_clopen_partition_of_clopen_cover

end CMDG.CondensedCM4P3Audit
