import CMDGCondensedCM4P3DerivedCM5R0UniformGenuineSolidExtAcyclic
import CMDGCondensedCM4P3DerivedCM5R0UniformDerivedComparisonGeneric

/-!
# Genuine CMDG Stonean Cech augmentation as a derived isomorphism

The map is the ACTUAL chain augmentation to the free condensed object.
It is proved a quasi-isomorphism and inverted by the standard localization.
It is NOT the independent solidification unit F(T) -> G(T).
-/

noncomputable section
universe u
open CategoryTheory Limits HomologicalComplex

namespace CMDG.CondensedCM5R0

private abbrev P (T : Profinite.{u}) : Profinite.{u} :=
  Stonean.toProfinite.obj T.presentation
private abbrev p (T : Profinite.{u}) : P T ⟶ T :=
  Profinite.presentation.π T

/-- Actual Cech complex of genuine free condensed relation modules. -/
noncomputable def cechChain (T : Profinite.{u}) : ChainComplex Ambient ℕ :=
  uniformFreeRelationChainComplex (P T) T (p T)

theorem cechChain_aug_zero (T : Profinite.{u}) :
    (cechChain T).d 1 0 ≫ cechAug T = 0 := by
  change cechD T 0 ≫ cechAug T = 0
  exact uniformFreeRelationAugmentation_comp_boundary_zero (P T) T (p T)

/-- Canonical actual augmentation, as a morphism of chain complexes. -/
noncomputable def cechDerivedMap (T : Profinite.{u}) :
    cechChain T ⟶ (ChainComplex.single₀ Ambient).obj
      ((Condensed.profiniteFree Coeff).obj T) :=
  CMDG.DerivedComparison.chainAugmentation
    (cechChain T) ((Condensed.profiniteFree Coeff).obj T)
    (cechAug T) (cechChain_aug_zero T)

/-- Every strictly positive term of the genuine Cech chain is exact. -/
theorem cechChain_exactAt_positive (T : Profinite.{u}) (n : ℕ) :
    (cechChain T).ExactAt (n + 1) := by
  change (ShortComplex.mk
    (cechD T (n + 1)) (cechD T n)
    (uniformFreeRelationBoundary_sq_zero (P T) T (p T) n)).Exact
  exact (uniformStoneanFreeCechFullAugmentedExact T).1 n

/-- The actual degree-zero augmentation is exact in the real category. -/
theorem cechChain_augmentation_exact (T : Profinite.{u}) :
    (ShortComplex.mk ((cechChain T).d 1 0) (cechAug T)
      (cechChain_aug_zero T)).Exact := by
  change (ShortComplex.mk
    (cechD T 0) (cechAug T)
    (uniformFreeRelationAugmentation_comp_boundary_zero (P T) T (p T))).Exact
  exact (uniformStoneanFreeCechFullAugmentedExact T).2.1

/-- The actual Cech augmentation is a quasi-isomorphism in all degrees. -/
theorem cechDerivedMap_quasiIso (T : Profinite.{u}) :
    QuasiIso (cechDerivedMap T) := by
  letI : Epi (cechAug T) :=
    (uniformStoneanFreeCechFullAugmentedExact T).2.2
  exact CMDG.DerivedComparison.chainAugmentation_quasiIso
    (cechChain T) ((Condensed.profiniteFree Coeff).obj T)
    (cechAug T) (cechChain_aug_zero T)
    (cechChain_exactAt_positive T)
    (cechChain_augmentation_exact T)

/-- An actual isomorphism in the localization of the
nonnegative chain-complex category at quasi-isomorphisms. -/
theorem cechDerivedMap_localized_isIso (T : Profinite.{u}) :
    IsIso ((HomologicalComplexUpToQuasiIso.Q).map (cechDerivedMap T)) := by
  apply (HomologicalComplexUpToQuasiIso.isIso_Q_map_iff_mem_quasiIso
    (cechDerivedMap T)).2
  exact (HomologicalComplex.mem_quasiIso_iff
    (cechDerivedMap T)).2 (cechDerivedMap_quasiIso T)

#print axioms cechDerivedMap_localized_isIso
#print axioms cechDerivedMap_quasiIso
end CMDG.CondensedCM5R0
