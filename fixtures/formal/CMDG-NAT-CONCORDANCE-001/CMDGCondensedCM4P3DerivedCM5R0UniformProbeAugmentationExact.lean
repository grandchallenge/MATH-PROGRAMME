import CMDGCondensedCM4P3DerivedCM5R0UniformStoneanInternalExact
import CMDGCondensedCM4P3DerivedCM5R0UniformSplitCechAugmentation
import CMDGCondensedCM4P3DerivedCM5R0UniformAugmentationExactTransfer

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private abbrev freeProbe (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :=
  (ModuleCat.free Coeff).obj
    (uniformProbeHomSet U (uniformRelationProfinite P T p n))

def uniformProbeBarEpsilon (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) :
    freeProbe U P T p 0 ⟶
      (ModuleCat.free Coeff).obj (uniformProbeHomSet U T) :=
  (ModuleCat.free Coeff).map
    (↾(fun z : uniformProbeHomSet U (uniformRelationProfinite P T p 0) =>
      ULift.up (z.down ≫
        profiniteToCompHaus.map (uniformRelationProjection0 P T p ≫ p))))

theorem uniformProbeBarEpsilon_square (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) :
    (uniformProbeBarIso U P T p 0).hom ≫
      splitBarBaseMap (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) =
    uniformProbeBarEpsilon U P T p := by
  change (ModuleCat.free Coeff).map (↾uniformProbeTupleEquiv U P T p 0) ≫
    (ModuleCat.free Coeff).map
      (↾splitCechBaseProjection (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p)) =
    (ModuleCat.free Coeff).map
      (↾(fun z : uniformProbeHomSet U (uniformRelationProfinite P T p 0) =>
        ULift.up (z.down ≫
          profiniteToCompHaus.map (uniformRelationProjection0 P T p ≫ p))))
  rw [← Functor.map_comp]
  congr 1

theorem uniformProbeBarEpsilon_comp_boundary_zero
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformProbeBarD U P T p 0 ≫
      uniformProbeBarEpsilon U P T p = 0 := by
  rw [← uniformProbeBarEpsilon_square]
  rw [← Category.assoc, uniformProbeBarD_square, Category.assoc,
    splitBarZeroBoundary_comp_augmentation, comp_zero]

def uniformProbeBarAugZeroShortComplex (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (uniformProbeBarD U P T p 0)
    (uniformProbeBarEpsilon U P T p)
    (uniformProbeBarEpsilon_comp_boundary_zero U P T p)

def uniformProbeBarAugZeroIso (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformProbeBarAugZeroShortComplex U P T p ≅
      splitBarZeroShortComplex (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) := by
  refine ShortComplex.isoMk
    (uniformProbeBarIso U P T p 1)
    (uniformProbeBarIso U P T p 0)
    (Iso.refl _) ?_ ?_
  · exact (uniformProbeBarD_square U P T p 0).symm
  · change (uniformProbeBarIso U P T p 0).hom ≫
        splitBarBaseMap (uniformProbeHomSet U P)
          (uniformProbeHomSet U T) (uniformProbeMap U P T p) =
        uniformProbeBarEpsilon U P T p ≫ (𝟙 _)
    simpa only [Category.comp_id] using
      (uniformProbeBarEpsilon_square U P T p)

theorem uniformProbeBarAugZeroExact (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T)
    (s : uniformProbeHomSet U T → uniformProbeHomSet U P)
    (hs : ∀ b, uniformProbeMap U P T p (s b) = b) :
    (uniformProbeBarAugZeroShortComplex U P T p).Exact := by
  exact ShortComplex.exact_of_iso
    (uniformProbeBarAugZeroIso U P T p).symm
    (splitBarZeroShortExact (uniformProbeHomSet U P)
      (uniformProbeHomSet U T) (uniformProbeMap U P T p) s hs)

theorem uniformProbePresheafAugmentation_eval
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T) :
    (uniformPresheafRelationAugmentation P T p).app
      (Opposite.op U.compHaus) =
    uniformProbeBarEpsilon U P T p := by
  rfl

/-- All split-probe zero-degree exactness results concern the
REAL Stonean-restricted represented CompHaus presheaf bar,
rather than an invented abstract functorial replacement. -/
theorem uniformStoneanRestrictedPresheafAugZeroExact
    (T : Profinite.{u}) :
    ((uniformPresheafRelationAugShortComplex
      (Stonean.toProfinite.obj T.presentation) T
      (Profinite.presentation.π T)).map
        stoneanPresheafRestriction).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let Q := ((uniformPresheafRelationAugShortComplex P T p).map
      stoneanPresheafRestriction).map
        ((evaluation Stoneanᵒᵖ (ModuleCat Coeff)).obj U)
  let W := uniformProbeBarAugZeroShortComplex U.unop P T p
  have hf : Q.f = W.f := by
    change (uniformPresheafRelationBoundary P T p 0).app
      (Opposite.op U.unop.compHaus) =
      uniformProbeBarD U.unop P T p 0
    unfold uniformPresheafRelationBoundary uniformProbeBarD
    rw [NatTrans.app_sum]
    simp only [NatTrans.app_zsmul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [uniformProbePresheafFace_eval U.unop P T p 0 k]
    rfl
  have hg : Q.g = W.g := by
    change (uniformPresheafRelationAugmentation P T p).app
      (Opposite.op U.unop.compHaus) =
      uniformProbeBarEpsilon U.unop P T p
    exact uniformProbePresheafAugmentation_eval U.unop P T p
  obtain ⟨s,hs⟩ := uniformStoneanProbeSplit T U.unop
  have hW : W.Exact := uniformProbeBarAugZeroExact U.unop
    P T p s hs
  change Q.Exact
  apply (Q.exact_iff_kernel_ι_comp_cokernel_π_zero).2
  rw [hf, hg]
  exact (W.exact_iff_kernel_ι_comp_cokernel_π_zero).1 hW

/-- **Unconditional** exactness at augmentation degree zero for
the actual condensed module free Stonean Čech resolution:
the image of d_0 is the kernel of the true augmentation. -/
theorem uniformStoneanFreeCechAugmentationExact
    (T : Profinite.{u}) :
    (ShortComplex.mk
      (uniformFreeRelationBoundary
        (Stonean.toProfinite.obj T.presentation) T
          (Profinite.presentation.π T) 0)
      (uniformFreeRelationAugmentation
        (Stonean.toProfinite.obj T.presentation) T
          (Profinite.presentation.π T))
      (uniformFreeRelationAugmentation_comp_boundary_zero
        (Stonean.toProfinite.obj T.presentation) T
          (Profinite.presentation.π T))).Exact := by
  exact uniformRelationAugZeroExact_of_stoneanPresheafExact
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T)
    (uniformStoneanRestrictedPresheafAugZeroExact T)

/-- The ENTIRE augmented genuine categorical free condensed Stonean
Čech chain complex is exact: all internal terms, augmentation at
degree zero, and epimorphism of the augmentation onto F_T.
This does not assert projectivity of nonzero degree terms. -/
theorem uniformStoneanFreeCechFullAugmentedExact
    (T : Profinite.{u}) :
    (∀ n : ℕ, (ShortComplex.mk
        (uniformFreeRelationBoundary
          (Stonean.toProfinite.obj T.presentation) T
            (Profinite.presentation.π T) (n + 1))
        (uniformFreeRelationBoundary
          (Stonean.toProfinite.obj T.presentation) T
            (Profinite.presentation.π T) n)
        (uniformFreeRelationBoundary_sq_zero
          (Stonean.toProfinite.obj T.presentation) T
            (Profinite.presentation.π T) n)).Exact) ∧
    (ShortComplex.mk
      (uniformFreeRelationBoundary
        (Stonean.toProfinite.obj T.presentation) T
          (Profinite.presentation.π T) 0)
      (uniformFreeRelationAugmentation
        (Stonean.toProfinite.obj T.presentation) T
          (Profinite.presentation.π T))
      (uniformFreeRelationAugmentation_comp_boundary_zero
        (Stonean.toProfinite.obj T.presentation) T
          (Profinite.presentation.π T))).Exact ∧
    Epi (uniformFreeRelationAugmentation
      (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T)) := by
  exact ⟨uniformStoneanFreeCechInternalExact T,
    uniformStoneanFreeCechAugmentationExact T,
    uniformFreeStoneanRelationAugmentation_epi T⟩

#print axioms uniformStoneanFreeCechFullAugmentedExact

#print axioms uniformProbeBarAugZeroExact
end CMDG.CondensedCM5R0
