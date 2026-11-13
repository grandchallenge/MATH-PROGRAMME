import CMDGCondensedCM4P3DerivedCM5R0ActualCechSections
import CMDGCondensedCM4P3DerivedCM5R0StoneanSolidTargetExtension

/-!
# CM5: exact stage-descended genuine Čech potentials

For an arbitrary profinite source T and a second source U whose free
condensed module is projective (in particular U underlying a Stonean
space, including finite discrete stages), a *commuting morphism of
actual Stonean presentations* induces a genuine morphism K_T → K_U
of their kernels.

If a kernel functional K_T → A factors through that map, it extends
to the actual Stonean source F_{P(T)}. For the protected solid target
G_S, this constructs a genuine solid-sheaf Čech potential.

Consequently, if **each** kernel functional has such a Stonean-stage
factorization, the actual Ext¹(F_T,G_S) group vanishes. This last
statement is a conditional sufficient criterion. We do NOT prove that
each functional admits the factorization; no identification of
arbitrary condensed sections with finite-quotient cocycles or
infinite-profinite Ext¹ vanishing is asserted.

The maps are required to form a commuting presentation square.
Merely factoring a bare set-function through a finite quotient does
not satisfy that hypothesis.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Short names for the real category objects, with the original
universe-lifted integer coefficients unchanged. -/
abbrev stageFree (T : Profinite.{u}) : Ambient :=
  (Condensed.profiniteFree Coeff).obj T

abbrev stageStoneanFree (T : Profinite.{u}) : Ambient :=
  (Condensed.profiniteFree Coeff).obj
    (Stonean.toProfinite.obj T.presentation)

/-- A commutative morphism of projective Stonean presentations
induces the actual map between their kernel objects. -/
noncomputable def stoneanPresentationKernelStageMap
    (T U : Profinite.{u})
    (h₀ : stageStoneanFree T ⟶ stageStoneanFree U)
    (h₁ : stageFree T ⟶ stageFree U)
    (hsquare : h₀ ≫ freeStoneanPresentationMap U =
      freeStoneanPresentationMap T ≫ h₁) :
    stoneanPresentationKernel T ⟶ stoneanPresentationKernel U := by
  refine kernel.lift (freeStoneanPresentationMap U)
    (kernel.ι (freeStoneanPresentationMap T) ≫ h₀) ?_
  calc
    (kernel.ι (freeStoneanPresentationMap T) ≫ h₀) ≫
        freeStoneanPresentationMap U =
      kernel.ι (freeStoneanPresentationMap T) ≫
        (h₀ ≫ freeStoneanPresentationMap U) := Category.assoc _ _ _
    _ = kernel.ι (freeStoneanPresentationMap T) ≫
        (freeStoneanPresentationMap T ≫ h₁) := by rw [hsquare]
    _ = (kernel.ι (freeStoneanPresentationMap T) ≫
        freeStoneanPresentationMap T) ≫ h₁ := (Category.assoc _ _ _).symm
    _ = 0 := by simp

/-- The kernel stage map is compatible with the *actual* kernel
inclusions, rather than merely an abstract set-level restriction. -/
theorem stoneanPresentationKernelStageMap_comp_ι
    (T U : Profinite.{u})
    (h₀ : stageStoneanFree T ⟶ stageStoneanFree U)
    (h₁ : stageFree T ⟶ stageFree U)
    (hsquare : h₀ ≫ freeStoneanPresentationMap U =
      freeStoneanPresentationMap T ≫ h₁) :
    stoneanPresentationKernelStageMap T U h₀ h₁ hsquare ≫
        kernel.ι (freeStoneanPresentationMap U) =
      kernel.ι (freeStoneanPresentationMap T) ≫ h₀ := by
  simp [stoneanPresentationKernelStageMap]

/-- Explicitly extend a genuinely stage-descended kernel functional.
U is the underlying profinite space of a Stonean P, so the target
presentation splits by an already-protected concrete construction.
No extension is assumed for the arbitrary source T. -/
theorem extendKernelHom_of_stoneanStageFactor
    (T : Profinite.{u}) (P : Stonean.{u}) (A : Ambient)
    (h₀ : stageStoneanFree T ⟶
      stageStoneanFree (Stonean.toProfinite.obj P))
    (h₁ : stageFree T ⟶ stageFree (Stonean.toProfinite.obj P))
    (hsquare : h₀ ≫
        freeStoneanPresentationMap (Stonean.toProfinite.obj P) =
      freeStoneanPresentationMap T ≫ h₁)
    (fP : stoneanPresentationKernel (Stonean.toProfinite.obj P) ⟶ A)
    (f : stoneanPresentationKernel T ⟶ A)
    (hfactor :
      f = stoneanPresentationKernelStageMap T
        (Stonean.toProfinite.obj P) h₀ h₁ hsquare ≫ fP) :
    ∃ g : stageStoneanFree T ⟶ A,
      kernel.ι (freeStoneanPresentationMap T) ≫ g = f := by
  refine ⟨h₀ ≫ extendStoneanKernelHom P A fP, ?_⟩
  calc
    kernel.ι (freeStoneanPresentationMap T) ≫
        (h₀ ≫ extendStoneanKernelHom P A fP) =
      (kernel.ι (freeStoneanPresentationMap T) ≫ h₀) ≫
        extendStoneanKernelHom P A fP := (Category.assoc _ _ _).symm
    _ = (stoneanPresentationKernelStageMap T
        (Stonean.toProfinite.obj P) h₀ h₁ hsquare ≫
          kernel.ι (freeStoneanPresentationMap
            (Stonean.toProfinite.obj P))) ≫
        extendStoneanKernelHom P A fP := by
          rw [stoneanPresentationKernelStageMap_comp_ι]
    _ = stoneanPresentationKernelStageMap T
          (Stonean.toProfinite.obj P) h₀ h₁ hsquare ≫
        (kernel.ι (freeStoneanPresentationMap
          (Stonean.toProfinite.obj P)) ≫
            extendStoneanKernelHom P A fP) :=
      Category.assoc _ _ _
    _ = stoneanPresentationKernelStageMap T
          (Stonean.toProfinite.obj P) h₀ h₁ hsquare ≫ fP := by
      rw [extendStoneanKernelHom_restrict]
    _ = f := hfactor.symm

/-- Stage descent produces a genuine solid *section* potential on
the actual Stonean cover, not just a finite set-valued primitive. -/
theorem stoneanCechSectionPotential_of_stoneanStageFactor
    (T : Profinite.{u}) (P : Stonean.{u}) (S : Profinite.{u})
    (h₀ : stageStoneanFree T ⟶
      stageStoneanFree (Stonean.toProfinite.obj P))
    (h₁ : stageFree T ⟶ stageFree (Stonean.toProfinite.obj P))
    (hsquare : h₀ ≫
        freeStoneanPresentationMap (Stonean.toProfinite.obj P) =
      freeStoneanPresentationMap T ≫ h₁)
    (fP : stoneanPresentationKernel (Stonean.toProfinite.obj P) ⟶
      underivedObject S)
    (f : stoneanPresentationKernel T ⟶ underivedObject S)
    (hfactor :
      f = stoneanPresentationKernelStageMap T
        (Stonean.toProfinite.obj P) h₀ h₁ hsquare ≫ fP) :
    ∃ b : solidSections S (Stonean.toProfinite.obj T.presentation),
      stoneanCechSolidSectionCoboundary T S b =
        stoneanCechSolidRelationSection T S f := by
  obtain ⟨g, hg⟩ :=
    extendKernelHom_of_stoneanStageFactor T P
      (underivedObject S) h₀ h₁ hsquare fP f hfactor
  have hpot :
      ∃ g : stageStoneanFree T ⟶ underivedObject S,
        stoneanCechDifference T ≫ g =
          stoneanCechSolidRelationFunctional T S f :=
    (solidKernelHom_extends_iff_cechPotential_unconditional T S f).mp
      ⟨g, hg⟩
  exact (stoneanCechSectionPotential_iff_modulePotential T S f).mpr hpot

/-- The precise, verifiable condition that a kernel functional
descends along an actual commuting Stonean presentation square. -/
def HasStoneanStageFactorization
    (T : Profinite.{u}) (A : Ambient)
    (f : stoneanPresentationKernel T ⟶ A) : Prop :=
  ∃ (P : Stonean.{u})
    (h₀ : stageStoneanFree T ⟶
      stageStoneanFree (Stonean.toProfinite.obj P))
    (h₁ : stageFree T ⟶ stageFree (Stonean.toProfinite.obj P))
    (hsquare : h₀ ≫
      freeStoneanPresentationMap (Stonean.toProfinite.obj P) =
        freeStoneanPresentationMap T ≫ h₁)
    (fP : stoneanPresentationKernel (Stonean.toProfinite.obj P) ⟶ A),
    f = stoneanPresentationKernelStageMap T
      (Stonean.toProfinite.obj P) h₀ h₁ hsquare ≫ fP

/-- A uniform Stonean-stage descent theorem for every genuine
kernel functional *suffices* for arbitrary-profinite Ext¹ vanishing.
The premise is intentionally NOT proved or silently added as an
instance; it isolates the remaining source-semantic obligation. -/
theorem freeProfinite_extOne_vanishes_of_stoneanStageFactorizations
    (T S : Profinite.{u})
    (hstage : ∀ f : stoneanPresentationKernel T ⟶ underivedObject S,
      HasStoneanStageFactorization T (underivedObject S) f) :
    ∀ e : Abelian.Ext (stageFree T) (underivedObject S) 1,
      e = 0 := by
  apply (freeProfinite_extOne_vanishes_iff_kernel_hom_extends
    T (underivedObject S)).mpr
  intro f
  obtain ⟨P, h₀, h₁, hsquare, fP, hfactor⟩ := hstage f
  exact extendKernelHom_of_stoneanStageFactor T P
    (underivedObject S) h₀ h₁ hsquare fP f hfactor

#print axioms stoneanPresentationKernelStageMap
#print axioms stoneanPresentationKernelStageMap_comp_ι
#print axioms extendKernelHom_of_stoneanStageFactor
#print axioms stoneanCechSectionPotential_of_stoneanStageFactor
#print axioms freeProfinite_extOne_vanishes_of_stoneanStageFactorizations

end CMDG.CondensedCM5R0
