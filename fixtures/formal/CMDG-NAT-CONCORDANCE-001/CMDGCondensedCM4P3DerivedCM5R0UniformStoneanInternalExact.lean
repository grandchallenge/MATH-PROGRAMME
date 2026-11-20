import CMDGCondensedCM4P3DerivedCM5R0UniformProbeTupleComparison
import CMDGCondensedCM4P3DerivedCM5R0GlobalThirdRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0UniformInternalExactnessTransfer
import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeTrueDegreeOneExact

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private abbrev freeProbe (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :=
  (ModuleCat.free Coeff).obj
    (uniformProbeHomSet U (uniformRelationProfinite P T p n))

/-- True represented free-site all-degree face sum, evaluated
at the exact Stonean CompHaus test object. -/
def uniformProbeBarD (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    freeProbe U P T p (n + 1) ⟶ freeProbe U P T p n :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    (ModuleCat.free Coeff).map
      (↾uniformProbeFace U P T p n k)

/-- Actual free-module isomorphism from real represented
relation Hom-set to the split compatible-tuple bar object. -/
def uniformProbeBarIso (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    freeProbe U P T p n ≅
    (ModuleCat.free Coeff).obj
      (splitCechTuple (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n) :=
  (ModuleCat.free Coeff).mapIso
    (uniformProbeTupleEquiv U P T p n).toIso

theorem uniformProbeFace_bar_square (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (k : Fin (n + 2)) :
    (ModuleCat.free Coeff).map (↾uniformProbeFace U P T p n k) ≫
      (uniformProbeBarIso U P T p n).hom =
    (uniformProbeBarIso U P T p (n + 1)).hom ≫
      (ModuleCat.free Coeff).map
        (↾splitCechFace (uniformProbeHomSet U P)
          (uniformProbeHomSet U T) (uniformProbeMap U P T p) n k) := by
  change (ModuleCat.free Coeff).map (↾uniformProbeFace U P T p n k) ≫
      (ModuleCat.free Coeff).map
        (↾uniformProbeTupleEquiv U P T p n) =
    (ModuleCat.free Coeff).map (↾uniformProbeTupleEquiv U P T p (n + 1)) ≫
      (ModuleCat.free Coeff).map
        (↾splitCechFace (uniformProbeHomSet U P)
          (uniformProbeHomSet U T) (uniformProbeMap U P T p) n k)
  rw [← Functor.map_comp, ← Functor.map_comp]
  congr 1

theorem uniformProbeBarD_square (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformProbeBarD U P T p n ≫
      (uniformProbeBarIso U P T p n).hom =
    (uniformProbeBarIso U P T p (n + 1)).hom ≫
      splitBarD (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n := by
  unfold uniformProbeBarD splitBarD
  rw [Preadditive.sum_comp, Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro k hk
  rw [Preadditive.zsmul_comp, Preadditive.comp_zsmul,
    uniformProbeFace_bar_square]

theorem uniformProbeBarD_comp_D_zero (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformProbeBarD U P T p (n + 1) ≫
      uniformProbeBarD U P T p n = 0 := by
  apply (cancel_mono (uniformProbeBarIso U P T p n).hom).1
  calc
    (uniformProbeBarD U P T p (n + 1) ≫
      uniformProbeBarD U P T p n) ≫
        (uniformProbeBarIso U P T p n).hom =
        uniformProbeBarD U P T p (n + 1) ≫
          (uniformProbeBarD U P T p n ≫
            (uniformProbeBarIso U P T p n).hom) := Category.assoc _ _ _
    _ = uniformProbeBarD U P T p (n + 1) ≫
          ((uniformProbeBarIso U P T p (n + 1)).hom ≫
            splitBarD (uniformProbeHomSet U P)
              (uniformProbeHomSet U T) (uniformProbeMap U P T p) n) := by
            rw [uniformProbeBarD_square]
    _ = (uniformProbeBarD U P T p (n + 1) ≫
          (uniformProbeBarIso U P T p (n + 1)).hom) ≫
            splitBarD (uniformProbeHomSet U P)
              (uniformProbeHomSet U T) (uniformProbeMap U P T p) n :=
            (Category.assoc _ _ _).symm
    _ = ((uniformProbeBarIso U P T p (n + 2)).hom ≫
          splitBarD (uniformProbeHomSet U P)
            (uniformProbeHomSet U T) (uniformProbeMap U P T p) (n + 1)) ≫
              splitBarD (uniformProbeHomSet U P)
                (uniformProbeHomSet U T) (uniformProbeMap U P T p) n := by
            rw [uniformProbeBarD_square]
    _ = 0 := by rw [Category.assoc, splitBarD_comp_D_zero, comp_zero]

def uniformProbeBarShortComplex (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (uniformProbeBarD U P T p (n + 1))
    (uniformProbeBarD U P T p n)
    (uniformProbeBarD_comp_D_zero U P T p n)

def uniformProbeBarShortIso (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformProbeBarShortComplex U P T p n ≅
      splitBarShortComplex (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n := by
  refine ShortComplex.isoMk
    (uniformProbeBarIso U P T p (n + 2))
    (uniformProbeBarIso U P T p (n + 1))
    (uniformProbeBarIso U P T p n) ?_ ?_
  · exact (uniformProbeBarD_square U P T p (n + 1)).symm
  · exact (uniformProbeBarD_square U P T p n).symm

/-- A split presentation on genuine CompHaus Stonean Hom sets
implies exactness at every internal term of its TRUE probe bar. -/
theorem uniformProbeBarShortExact (U : Stonean.{u})
    (P T : Profinite.{u}) (p : P ⟶ T)
    (s : uniformProbeHomSet U T → uniformProbeHomSet U P)
    (hs : ∀ b, uniformProbeMap U P T p (s b) = b)
    (n : ℕ) :
    (uniformProbeBarShortComplex U P T p n).Exact := by
  exact ShortComplex.exact_of_iso
    (uniformProbeBarShortIso U P T p n).symm
    (splitBarShortComplex_exact (uniformProbeHomSet U P)
      (uniformProbeHomSet U T) (uniformProbeMap U P T p) s hs n)

/-- True Stonean-projective lifting splits the EXACT Hom-set
map used by our arity-uniform comparison (no global section P→T). -/
theorem uniformStoneanProbeSplit
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ∃ s : uniformProbeHomSet U T →
        uniformProbeHomSet U (Stonean.toProfinite.obj T.presentation),
      ∀ b, uniformProbeMap U
        (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T) (s b) = b := by
  let f := stoneanCompHausProbePresentationMap T U
  let s : uniformProbeHomSet U T →
      uniformProbeHomSet U (Stonean.toProfinite.obj T.presentation) :=
    (stoneanCompHausProbePresentationSplitEpi T U).section_
  refine ⟨s, ?_⟩
  intro b
  have h := (stoneanCompHausProbePresentationSplitEpi T U).id
  have hv := congrArg (fun g => g b) h
  exact hv

/-- Each actual free-presheaf face evaluated at a Stonean probe
is literally the free module map of the genuine representable
Hom-set face. This is the precise objectwise-vs-sheafification bridge. -/
theorem uniformProbePresheafFace_eval
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (k : Fin (n + 2)) :
    (freeCompHausModulePresheafFunctor.map
      (uniformRelationFace P T p n k)).app
        (Opposite.op U.compHaus) =
    (ModuleCat.free Coeff).map
      (↾uniformProbeFace U P T p n k) := by
  rfl

#print axioms uniformProbePresheafFace_eval

/-- The genuinely restricted CompHaus-site relation complex,
in ALL degrees, is exact as an abelian module PRESHEAF on Stonean.
No mistaken identification of a sheaf section with a free module
on the un-sheafified Hom set occurs. -/
theorem uniformStoneanRestrictedPresheafExact
    (T : Profinite.{u}) (n : ℕ) :
    ((uniformPresheafRelationShortComplex
      (Stonean.toProfinite.obj T.presentation) T
      (Profinite.presentation.π T) n).map
        stoneanPresheafRestriction).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  let Q := ((uniformPresheafRelationShortComplex
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T) n).map
      stoneanPresheafRestriction).map
        ((evaluation Stoneanᵒᵖ (ModuleCat Coeff)).obj U)
  let W := uniformProbeBarShortComplex U.unop
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T) n
  have hX₁ : Q.X₁ = W.X₁ := by
    rfl
  have hX₂ : Q.X₂ = W.X₂ := by
    rfl
  have hX₃ : Q.X₃ = W.X₃ := by
    rfl
  have hf : Q.f = W.f := by
    change (uniformPresheafRelationBoundary
      (Stonean.toProfinite.obj T.presentation) T
      (Profinite.presentation.π T) (n + 1)).app
        (Opposite.op U.unop.compHaus) =
      uniformProbeBarD U.unop (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T) (n + 1)
    unfold uniformPresheafRelationBoundary uniformProbeBarD
    rw [NatTrans.app_sum]
    simp only [NatTrans.app_zsmul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [uniformProbePresheafFace_eval U.unop
      (Stonean.toProfinite.obj T.presentation) T
      (Profinite.presentation.π T) (n + 1) k]
    rfl
  have hg : Q.g = W.g := by
    change (uniformPresheafRelationBoundary
      (Stonean.toProfinite.obj T.presentation) T
      (Profinite.presentation.π T) n).app
        (Opposite.op U.unop.compHaus) =
      uniformProbeBarD U.unop (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T) n
    unfold uniformPresheafRelationBoundary uniformProbeBarD
    rw [NatTrans.app_sum]
    simp only [NatTrans.app_zsmul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [uniformProbePresheafFace_eval U.unop
      (Stonean.toProfinite.obj T.presentation) T
      (Profinite.presentation.π T) n k]
    rfl
  obtain ⟨s0, hs0⟩ := uniformStoneanProbeSplit T U.unop
  have hW : W.Exact := uniformProbeBarShortExact U.unop
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T) s0 hs0 n
  change Q.Exact
  apply (Q.exact_iff_kernel_ι_comp_cokernel_π_zero).2
  rw [hf, hg]
  exact (W.exact_iff_kernel_ι_comp_cokernel_π_zero).1 hW

/-- Main result: the ACTUAL categorical free condensed-module Čech
complex of the canonical Stonean cover is internally exact at
every positive term C_(n+1), for ARBITRARY n. -/
theorem uniformStoneanFreeCechInternalExact
    (T : Profinite.{u}) (n : ℕ) :
    (ShortComplex.mk
      (uniformFreeRelationBoundary
        (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T) (n + 1))
      (uniformFreeRelationBoundary
        (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T) n)
      (uniformFreeRelationBoundary_sq_zero
        (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T) n)).Exact := by
  exact uniformRelationShortExact_of_stoneanPresheafExact
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T) n
    (uniformStoneanRestrictedPresheafExact T n)

#print axioms uniformStoneanFreeCechInternalExact

#print axioms uniformProbeBarShortExact

#print axioms uniformProbeBarD_square
end CMDG.CondensedCM5R0
