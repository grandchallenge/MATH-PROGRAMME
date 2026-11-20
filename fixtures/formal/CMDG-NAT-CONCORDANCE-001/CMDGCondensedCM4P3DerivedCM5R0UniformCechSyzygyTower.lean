import CMDGCondensedCM4P3DerivedCM5R0UniformKernelFactorShortExact
import CMDGCondensedCM4P3DerivedCM5R0UniformProbeAugmentationExact
import CMDGCondensedCM4P3DerivedCM5R0UniformCategoricalCechHom
import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct

/-!
# True syzygy tower of fully exact augmented Stonean Čech resolution

No false projectivity assumption on closed-relation terms.
-/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private abbrev P (T : Profinite.{u}) : Profinite.{u} :=
  Stonean.toProfinite.obj T.presentation
private abbrev p (T : Profinite.{u}) : P T ⟶ T :=
  Profinite.presentation.π T

def cechTerm (T : Profinite.{u}) (n : ℕ) : Ambient :=
  (Condensed.profiniteFree Coeff).obj (uniformRelationProfinite (P T) T (p T) n)

def cechD (T : Profinite.{u}) (n : ℕ) :
    cechTerm T (n + 1) ⟶ cechTerm T n :=
  uniformFreeRelationBoundary (P T) T (p T) n

def cechAug (T : Profinite.{u}) :
    cechTerm T 0 ⟶ (Condensed.profiniteFree Coeff).obj T :=
  uniformFreeRelationAugmentation (P T) T (p T)

def cechSyzygy (T : Profinite.{u}) : ℕ → Ambient
  | 0 => kernel (cechAug T)
  | n+1 => kernel (cechD T n)

def cechSyzygyι (T : Profinite.{u}) :
    (n : ℕ) → cechSyzygy T n ⟶ cechTerm T n
  | 0 => kernel.ι (cechAug T)
  | n+1 => kernel.ι (cechD T n)

def cechSyzygyCover (T : Profinite.{u}) :
    (n : ℕ) → cechTerm T (n + 1) ⟶ cechSyzygy T n
  | 0 => kernel.lift (cechAug T) (cechD T 0)
      (uniformFreeRelationAugmentation_comp_boundary_zero (P T) T (p T))
  | n+1 => kernel.lift (cechD T n) (cechD T (n+1))
      (uniformFreeRelationBoundary_sq_zero (P T) T (p T) n)

theorem cechSyzygyCover_comp_ι (T : Profinite.{u}) (n : ℕ) :
    cechSyzygyCover T n ≫ cechSyzygyι T n = cechD T n := by
  cases n with
  | zero => exact kernel.lift_ι _ _ _
  | succ n => exact kernel.lift_ι _ _ _

theorem cechSyzygyCover_epi (T : Profinite.{u}) (n : ℕ) :
    Epi (cechSyzygyCover T n) := by
  cases n with
  | zero =>
    let sc := ShortComplex.mk (cechD T 0) (cechAug T)
      (uniformFreeRelationAugmentation_comp_boundary_zero (P T) T (p T))
    have h : sc.Exact := uniformStoneanFreeCechAugmentationExact T
    exact (sc.exact_iff_epi_kernel_lift).mp h
  | succ n =>
    let sc := ShortComplex.mk (cechD T (n+1)) (cechD T n)
      (uniformFreeRelationBoundary_sq_zero (P T) T (p T) n)
    have h : sc.Exact := uniformStoneanFreeCechInternalExact T n
    exact (sc.exact_iff_epi_kernel_lift).mp h

theorem cechSyzygyι_mono (T : Profinite.{u}) (n : ℕ) :
    Mono (cechSyzygyι T n) := by
  cases n with
  | zero =>
    change Mono (kernel.ι (cechAug T))
    infer_instance
  | succ n =>
    change Mono (kernel.ι (cechD T n))
    infer_instance

theorem cechSyzygyι_comp_cover_zero
    (T : Profinite.{u}) (n : ℕ) :
    cechSyzygyι T (n + 1) ≫ cechSyzygyCover T n = 0 := by
  letI : Mono (cechSyzygyι T n) := cechSyzygyι_mono T n
  apply (cancel_mono (cechSyzygyι T n)).1
  rw [Category.assoc, cechSyzygyCover_comp_ι, zero_comp]
  exact kernel.condition (cechD T n)

theorem cechSyzygy_shortExact (T : Profinite.{u}) (n : ℕ) :
    (ShortComplex.mk (cechSyzygyι T (n + 1))
      (cechSyzygyCover T n)
      (cechSyzygyι_comp_cover_zero T n)).ShortExact := by
  letI : Epi (cechSyzygyCover T n) := cechSyzygyCover_epi T n
  letI : Mono (cechSyzygyι T n) := cechSyzygyι_mono T n
  letI : Mono (cechSyzygyι T (n+1)) := cechSyzygyι_mono T (n+1)
  have hlimit :
      IsLimit (KernelFork.ofι
        (cechSyzygyι T (n + 1))
        (cechSyzygyι_comp_cover_zero T n)) := by
    exact isKernelOfComp (f := cechSyzygyCover T n)
      (cechSyzygyι T n) (cechD T n)
      (kernelIsKernel (cechD T n))
      (cechSyzygyι_comp_cover_zero T n)
      (cechSyzygyCover_comp_ι T n)
  exact ShortComplex.ShortExact.mk
    ((ShortComplex.mk (cechSyzygyι T (n + 1))
      (cechSyzygyCover T n)
      (cechSyzygyι_comp_cover_zero T n)).exact_of_f_is_kernel hlimit)

theorem cechSyzygy_hom_extends_to_term
    (T S : Profinite.{u}) (n : ℕ)
    (f : cechSyzygy T (n + 1) ⟶
      (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) :
    ∃ g : cechTerm T (n + 1) ⟶
      (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S,
      cechSyzygyι T (n + 1) ≫ g = f := by
  letI : Epi (cechSyzygyCover T (n+1)) :=
    cechSyzygyCover_epi T (n+1)
  have hc :
      cechD T (n+2) ≫ (cechSyzygyCover T (n+1) ≫ f) = 0 := by
    have hz : cechD T (n+2) ≫ cechSyzygyCover T (n+1) = 0 := by
      letI : Mono (cechSyzygyι T (n+1)) := cechSyzygyι_mono T (n+1)
      apply (cancel_mono (cechSyzygyι T (n+1))).1
      rw [Category.assoc, cechSyzygyCover_comp_ι, zero_comp]
      exact uniformFreeRelationBoundary_sq_zero (P T) T (p T) (n+1)
    rw [← Category.assoc, hz, zero_comp]
  obtain ⟨g,hg⟩ := uniformFreeRelationBoundary_genuineSolidHom_exact
    (P T) T S (p T) (n+1)
    (cechSyzygyCover T (n+1) ≫ f) hc
  refine ⟨g, ?_⟩
  apply (cancel_epi (cechSyzygyCover T (n+1))).1
  calc
    cechSyzygyCover T (n+1) ≫ (cechSyzygyι T (n+1) ≫ g) =
      (cechSyzygyCover T (n+1) ≫ cechSyzygyι T (n+1)) ≫ g := (Category.assoc _ _ _).symm
    _ = cechD T (n+1) ≫ g := by rw [cechSyzygyCover_comp_ι]
    _ = cechSyzygyCover T (n+1) ≫ f := hg

/-- First higher derived consequence: every actual syzygy of
the augmented Stonean Čech resolution has vanishing Ext¹ into
the GENUINE free-solid target. No projectivity of Čech terms. -/
theorem cechSyzygy_extOne_genuineSolid_zero
    (T S : Profinite.{u}) (n : ℕ) :
    ∀ e : Abelian.Ext (cechSyzygy T n)
      ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S) 1,
      e = 0 := by
  let Q := ShortComplex.mk (cechSyzygyι T (n+1))
      (cechSyzygyCover T n)
      (cechSyzygyι_comp_cover_zero T n)
  have hQ : Q.ShortExact := cechSyzygy_shortExact T n
  apply shortExact_extOne_right_zero_of_hom_extensions
    Q hQ ((Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S)
  · exact freeProfinite_extOne_genuineSolid_vanishes
      (uniformRelationProfinite (P T) T (p T) (n+1)) S
  · intro f
    exact cechSyzygy_hom_extends_to_term T S n f

#print axioms cechSyzygy_extOne_genuineSolid_zero

#print axioms cechSyzygy_hom_extends_to_term
#print axioms cechSyzygy_shortExact

#print axioms cechSyzygyCover_epi
end CMDG.CondensedCM5R0
