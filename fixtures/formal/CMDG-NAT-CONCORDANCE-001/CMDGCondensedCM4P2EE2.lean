import CMDGCondensedCM4P2EE1
import Mathlib.Condensed.Discrete.Characterization
import Mathlib.CategoryTheory.Monoidal.Closed.Braided
import Mathlib.CategoryTheory.Limits.Opposites
import Mathlib.CategoryTheory.Sites.Limits
import Mathlib.Topology.Category.Profinite.Extend
import Mathlib.CategoryTheory.Functor.KanExtension.Pointwise

/-!
# CMDG CM4-P2-E E2 — measure-side right Kan reconstruction

This fixture is separate from the certified E1 layer. It identifies the P2-D continuous-function
source as the filtered colimit of its finite quotients and dualizes that colimit into the limit
data needed for the protected measure functor.

No E3 uniqueness statement or final comparison with `Condensed.profiniteSolid` is asserted here.
-/

namespace CMDG.CondensedCM4P2E.RightKanReconstruction

universe u

open CategoryTheory Limits Opposite
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P2D.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- The coefficient condensed module whose underlying presheaf is the protected P2-D coefficient
presheaf. -/
noncomputable abbrev coefficientCondensed : CondensedMod.{u} R :=
  (CondensedMod.LocallyConstant.functor R).obj (ModuleCat.of R R)

lemma coefficientCondensed_mem_locallyConstant :
    (CondensedMod.LocallyConstant.functor R).essImage coefficientCondensed :=
  ⟨ModuleCat.of R R, ⟨Iso.refl _⟩⟩

/-- The protected continuous-function module on a profinite set is the filtered colimit of the
continuous-function modules on its canonical finite quotients. This is the module-valued form of
the pinned discrete-object characterization. -/
noncomputable def continuousFunctionsIsColimit (S : Profinite.{u}) :
    IsColimit
      (CMDG.CondensedCM4P2D.continuousFunctions.mapCocone S.asLimitCone.op) := by
  have h :=
    ((CondensedMod.isDiscrete_tfae R coefficientCondensed).out 3 6).mp
      coefficientCondensed_mem_locallyConstant
  change IsColimit
    ((profiniteToCompHaus.op ⋙ coefficientCondensed.obj).mapCocone S.asLimitCone.op)
  exact (h S).some

/-- The same finite-quotient colimit after applying the canonical locally-constant/discrete
condensed-module functor. The cocone is written as an explicit mapped cocone so no associativity
transport is hidden in the statement. -/
noncomputable def discreteContinuousCondensedMappedIsColimit (S : Profinite.{u}) :
    IsColimit
      ((CondensedMod.LocallyConstant.functor R).mapCocone
        (CMDG.CondensedCM4P2D.continuousFunctions.mapCocone S.asLimitCone.op)) := by
  letI : (CondensedMod.LocallyConstant.functor R).IsLeftAdjoint :=
    (CondensedMod.LocallyConstant.adjunction R).isLeftAdjoint
  exact isColimitOfPreserves
    (CondensedMod.LocallyConstant.functor R)
    (continuousFunctionsIsColimit S)

/-- Transpose two compact variables of a nested locally-constant function. Compactness of the
outer variable makes the range finite; after factoring through that finite range, the pinned
`LocallyConstant.unflip` construction performs the transpose without an infinite intersection of
open fibres. -/
noncomputable def locallyConstantSwap (T S : CompHaus.{u})
    (f : LocallyConstant T (LocallyConstant S R)) :
    LocallyConstant S (LocallyConstant T R) := by
  classical
  let A : Finset (LocallyConstant S R) := f.range_finite.toFinset
  let q : LocallyConstant T {g // g ∈ A} :=
    { toFun := fun t => ⟨f t, by simp [A]⟩
      isLocallyConstant := by
        apply IsLocallyConstant.desc
          (fun t => (⟨f t, by simp [A]⟩ : {g // g ∈ A}))
          (fun g => (g.1 : LocallyConstant S R))
        · simpa [Function.comp_def] using f.isLocallyConstant
        · exact Subtype.val_injective }
  let family : {g // g ∈ A} → LocallyConstant S R := fun g => g.1
  let transposedValues : LocallyConstant S ({g // g ∈ A} → R) :=
    LocallyConstant.unflip family
  exact transposedValues.map (fun values => q.map values)

@[simp]
lemma locallyConstantSwap_apply (T S : CompHaus.{u})
    (f : LocallyConstant T (LocallyConstant S R)) (s : S) (t : T) :
    locallyConstantSwap T S f s t = f t s := by
  classical
  rfl

/-- The transpose is linear in the coefficient module and involutive. -/
noncomputable def locallyConstantSwapLinearEquiv (T S : CompHaus.{u}) :
    LocallyConstant T (LocallyConstant S R) ≃ₗ[R]
      LocallyConstant S (LocallyConstant T R) where
  toFun := locallyConstantSwap T S
  invFun := locallyConstantSwap S T
  left_inv f := by
    ext t s
    rw [locallyConstantSwap_apply, locallyConstantSwap_apply]
  right_inv f := by
    ext s t
    rw [locallyConstantSwap_apply, locallyConstantSwap_apply]
  map_add' f g := by
    apply LocallyConstant.ext
    intro s
    apply LocallyConstant.ext
    intro t
    change f t s + g t s =
      locallyConstantSwap T S f s t + locallyConstantSwap T S g s t
    rw [locallyConstantSwap_apply, locallyConstantSwap_apply]
  map_smul' r f := by
    apply LocallyConstant.ext
    intro s
    apply LocallyConstant.ext
    intro t
    change r • f t s = r • locallyConstantSwap T S f s t
    rw [locallyConstantSwap_apply]

/-- For a fixed test compactum `T`, the target coefficient module is itself a discrete condensed
module. -/
noncomputable abbrev coefficientAtCondensed (T : CompHaus.{u}) : CondensedMod.{u} R :=
  (CondensedMod.LocallyConstant.functor R).obj
    (CMDG.CondensedCM4P2D.coefficientPresheaf.obj (op T))

lemma coefficientAtCondensed_mem_locallyConstant (T : CompHaus.{u}) :
    (CondensedMod.LocallyConstant.functor R).essImage (coefficientAtCondensed T) :=
  ⟨CMDG.CondensedCM4P2D.coefficientPresheaf.obj (op T), ⟨Iso.refl _⟩⟩

/-- The finite-quotient source after transposing the two compact variables. -/
noncomputable abbrev transposedContinuousFunctions (T : CompHaus.{u}) :
    Profinite.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R :=
  profiniteToCompHaus.op ⋙
    (CondensedMod.LocallyConstant.functorToPresheaves R).obj
      (CMDG.CondensedCM4P2D.coefficientPresheaf.obj (op T))

/-- Evaluation of the protected nested P2-D presheaf at a fixed test compactum. -/
noncomputable abbrev discreteContinuousPresheafAt (T : CompHaus.{u}) :
    Profinite.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R :=
  CMDG.CondensedCM4P2D.discreteContinuousPresheaf ⋙
    (evaluation (CompHaus.{u}ᵒᵖ) (ModuleCat.{u + 1} R)).obj (op T)

/-- Swapping the two compact variables identifies the discrete finite-quotient source with the
objectwise evaluation of the protected nested presheaf. -/
noncomputable def transposedContinuousFunctionsNatIso (T : CompHaus.{u}) :
    transposedContinuousFunctions T ≅ discreteContinuousPresheafAt T :=
  NatIso.ofComponents
    (fun S =>
      (locallyConstantSwapLinearEquiv
        (profiniteToCompHaus.obj S.unop) T).toModuleIso)
    (by
      intro X Y f
      apply ModuleCat.hom_ext
      apply LinearMap.ext
      intro h
      apply LocallyConstant.ext
      intro t
      apply LocallyConstant.ext
      intro s
      simp only [Functor.comp_map]
      rfl)

/-- The transposed objectwise source is a finite-quotient filtered colimit. -/
noncomputable def transposedContinuousFunctionsIsColimit
    (T : CompHaus.{u}) (S : Profinite.{u}) :
    IsColimit ((transposedContinuousFunctions T).mapCocone S.asLimitCone.op) := by
  have h :=
    ((CondensedMod.isDiscrete_tfae R (coefficientAtCondensed T)).out 3 6).mp
      (coefficientAtCondensed_mem_locallyConstant T)
  change IsColimit
    ((profiniteToCompHaus.op ⋙ (coefficientAtCondensed T).obj).mapCocone
      S.asLimitCone.op)
  exact (h S).some

/-- Hence every evaluation of the protected nested P2-D presheaf is the same finite-quotient
filtered colimit. -/
noncomputable def discreteContinuousPresheafAtIsColimit
    (T : CompHaus.{u}) (S : Profinite.{u}) :
    IsColimit ((discreteContinuousPresheafAt T).mapCocone S.asLimitCone.op) := by
  exact IsColimit.mapCoconeEquiv
    (transposedContinuousFunctionsNatIso T)
    (transposedContinuousFunctionsIsColimit T S)

/-- The complete protected nested P2-D source presheaf is reconstructed from the canonical finite
quotients of every profinite set. -/
noncomputable def discreteContinuousPresheafIsColimit (S : Profinite.{u}) :
    IsColimit
      (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.mapCocone
        S.asLimitCone.op) := by
  apply evaluationJointlyReflectsColimits
  intro T
  let E :=
    (evaluation (CompHaus.{u}ᵒᵖ) (ModuleCat.{u + 1} R)).obj T
  have h := discreteContinuousPresheafAtIsColimit T.unop S
  exact h.ofIsoColimit
    (Functor.mapCoconeMapCocone
      (H := CMDG.CondensedCM4P2D.discreteContinuousPresheaf)
      (H' := E) S.asLimitCone.op).symm

/-- Opposing the certified finite-quotient colimit produces the corresponding limit cone in the
opposite presheaf category. -/
noncomputable def discreteContinuousPresheafOpIsLimit (S : Profinite.{u}) :
    IsLimit
      (coneRightOpOfCocone
        (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.mapCocone
          S.asLimitCone.op)) :=
  isLimitConeRightOpOfCocone _ (discreteContinuousPresheafIsColimit S)

/-- Internal Hom into the protected coefficient presheaf, viewed as a right adjoint in the source
variable. -/
noncomputable abbrev internalHomIntoCoefficient : PresheafModuleᵒᵖ ⥤ PresheafModule :=
  MonoidalClosed.internalHom.flip.obj CMDG.CondensedCM4P2D.coefficientPresheaf

/-- The P2-D measure presheaf functor is exactly the contravariant internal Hom of the protected
nested locally-constant source into the coefficient presheaf. -/
noncomputable def measurePresheafInternalHomNatIso :
    CMDG.CondensedCM4P2D.discreteContinuousPresheaf.rightOp ⋙
        internalHomIntoCoefficient ≅
      CMDG.CondensedCM4P2D.measurePresheafFunctor :=
  NatIso.ofComponents (fun _ => Iso.refl _) (by
    intro X Y f
    rfl)

/-- On the canonical finite-quotient diagram, the opposite-source/internal-Hom presentation and
the protected measure-presheaf presentation are canonically the same diagram. -/
noncomputable def finiteQuotientMeasureDiagramIso (S : Profinite.{u}) :
    (S.diagram.op ⋙ CMDG.CondensedCM4P2D.discreteContinuousPresheaf).rightOp ⋙
        internalHomIntoCoefficient ≅
      S.diagram ⋙ CMDG.CondensedCM4P2D.measurePresheafFunctor :=
  NatIso.ofComponents (fun _ => Iso.refl _) (by
    intro X Y f
    rfl)

/-- The dualized finite-quotient cone is the protected measure cone transported across the explicit
diagram identification. -/
noncomputable def finiteQuotientMeasureConeIso (S : Profinite.{u}) :
    internalHomIntoCoefficient.mapCone
        (coneRightOpOfCocone
          (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.mapCocone
            S.asLimitCone.op)) ≅
      (Cone.postcompose (finiteQuotientMeasureDiagramIso S).inv).obj
        (CMDG.CondensedCM4P2D.measurePresheafFunctor.mapCone S.asLimitCone) :=
  Cone.ext (Iso.refl _) (by
    intro j
    rfl)

/-- Internal Hom into the protected coefficient presheaf turns the finite-quotient source colimit
into the required limit cone for the protected measure presheaf functor. -/
noncomputable def measurePresheafFunctorMapConeIsLimit (S : Profinite.{u}) :
    IsLimit
      (CMDG.CondensedCM4P2D.measurePresheafFunctor.mapCone S.asLimitCone) := by
  have hdual :
      IsLimit
        (internalHomIntoCoefficient.mapCone
          (coneRightOpOfCocone
            (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.mapCocone
              S.asLimitCone.op))) :=
    isLimitOfPreserves internalHomIntoCoefficient
      (discreteContinuousPresheafOpIsLimit S)
  exact
    (IsLimit.postcomposeInvEquiv
      (finiteQuotientMeasureDiagramIso S)
      (CMDG.CondensedCM4P2D.measurePresheafFunctor.mapCone S.asLimitCone))
      (hdual.ofIsoLimit (finiteQuotientMeasureConeIso S))

/-- Forget a condensed `R`-module to its underlying presheaf. This is exactly the inclusion of the
full subcategory of sheaves and therefore reflects limits without introducing an extra universe. -/
noncomputable abbrev condensedModuleToPresheaf : CondensedMod.{u} R ⥤ PresheafModule :=
  ObjectProperty.ι (Presheaf.IsSheaf (coherentTopology CompHaus.{u}))

/-- The protected P2-D measure functor preserves the canonical finite-quotient limit after lifting
from the presheaf calculation to condensed modules. -/
noncomputable def measureFunctorMapConeIsLimit (S : Profinite.{u}) :
    IsLimit (CMDG.CondensedCM4P2D.measureFunctor.mapCone S.asLimitCone) := by
  apply isLimitOfReflects condensedModuleToPresheaf
  change IsLimit
    (CMDG.CondensedCM4P2D.measurePresheafFunctor.mapCone S.asLimitCone)
  exact measurePresheafFunctorMapConeIsLimit S

/-- Extend the finite-quotient limit to the full structured-arrow diagram of finite quotients. -/
noncomputable def measureFunctorStructuredArrowIsLimit (S : Profinite.{u}) :
    IsLimit (Profinite.Extend.cone CMDG.CondensedCM4P2D.measureFunctor S) :=
  Profinite.Extend.isLimitCone S.asLimitCone CMDG.CondensedCM4P2D.measureFunctor
    S.asLimit (measureFunctorMapConeIsLimit S)

/-- The right-extension object whose counit is exactly the certified E1 finite comparison. -/
noncomputable def measureRightExtension :
    Functor.RightExtension FintypeCat.toProfinite (Condensed.finFree R) :=
  Functor.RightExtension.mk CMDG.CondensedCM4P2D.measureFunctor
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom

/-- Whisker the certified E1 comparison over the structured-arrow finite diagram. -/
noncomputable def structuredArrowFiniteComparisonIso (S : Profinite.{u}) :
    StructuredArrow.proj S FintypeCat.toProfinite ⋙
        (FintypeCat.toProfinite ⋙ CMDG.CondensedCM4P2D.measureFunctor) ≅
      StructuredArrow.proj S FintypeCat.toProfinite ⋙ Condensed.finFree R :=
  Functor.isoWhiskerLeft
    (StructuredArrow.proj S FintypeCat.toProfinite)
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso

/-- Pulling the pointwise right-extension cone back across E1 recovers exactly the structured-arrow
measure cone. -/
noncomputable def structuredArrowMeasureConeIso (S : Profinite.{u}) :
    Profinite.Extend.cone CMDG.CondensedCM4P2D.measureFunctor S ≅
      (Cone.postcompose (structuredArrowFiniteComparisonIso S).inv).obj
        (measureRightExtension.coneAt S) :=
  Cone.ext (Iso.refl _) (by
    intro j
    change
      CMDG.CondensedCM4P2D.measureFunctor.map j.hom =
        𝟙 _ ≫
          (CMDG.CondensedCM4P2D.measureFunctor.map j.hom ≫
            CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom.app j.right) ≫
          CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.inv.app j.right
    simp)

/-- E2 pointwise form: at every profinite set the E1-counit right-extension cone is limiting. -/
noncomputable def measureRightExtensionIsPointwiseAt (S : Profinite.{u}) :
    measureRightExtension.IsPointwiseRightKanExtensionAt S := by
  have hpost :
      IsLimit
        ((Cone.postcompose (structuredArrowFiniteComparisonIso S).inv).obj
          (measureRightExtension.coneAt S)) :=
    (measureFunctorStructuredArrowIsLimit S).ofIsoLimit
      (structuredArrowMeasureConeIso S)
  exact
    (IsLimit.postcomposeInvEquiv
      (structuredArrowFiniteComparisonIso S)
      (measureRightExtension.coneAt S)) hpost

/-- E2 pointwise certificate. -/
noncomputable def measureRightExtensionIsPointwise :
    measureRightExtension.IsPointwiseRightKanExtension :=
  fun S => measureRightExtensionIsPointwiseAt S

/-- E2 ordinary form: the protected P2-D measure functor is a right Kan extension of the pinned
finite-free functor along `FintypeCat.toProfinite`, using the certified E1 comparison as counit. -/
theorem measureFunctorIsRightKanExtension :
    CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
  measureRightExtensionIsPointwise.isRightKanExtension

#check continuousFunctionsIsColimit
#check discreteContinuousCondensedMappedIsColimit
#check locallyConstantSwap
#check locallyConstantSwapLinearEquiv
#check transposedContinuousFunctionsNatIso
#check transposedContinuousFunctionsIsColimit
#check discreteContinuousPresheafAtIsColimit
#check discreteContinuousPresheafIsColimit
#check discreteContinuousPresheafOpIsLimit
#check measurePresheafInternalHomNatIso
#check finiteQuotientMeasureDiagramIso
#check finiteQuotientMeasureConeIso
#check measurePresheafFunctorMapConeIsLimit
#check measureFunctorMapConeIsLimit
#check measureFunctorStructuredArrowIsLimit
#check measureRightExtension
#check structuredArrowFiniteComparisonIso
#check structuredArrowMeasureConeIso
#check measureRightExtensionIsPointwiseAt
#check measureRightExtensionIsPointwise
#check measureFunctorIsRightKanExtension

#print axioms continuousFunctionsIsColimit
#print axioms discreteContinuousCondensedMappedIsColimit
#print axioms locallyConstantSwap
#print axioms locallyConstantSwapLinearEquiv
#print axioms transposedContinuousFunctionsNatIso
#print axioms transposedContinuousFunctionsIsColimit
#print axioms discreteContinuousPresheafAtIsColimit
#print axioms discreteContinuousPresheafIsColimit
#print axioms discreteContinuousPresheafOpIsLimit
#print axioms measurePresheafInternalHomNatIso
#print axioms finiteQuotientMeasureDiagramIso
#print axioms finiteQuotientMeasureConeIso
#print axioms measurePresheafFunctorMapConeIsLimit
#print axioms measureFunctorMapConeIsLimit
#print axioms measureFunctorStructuredArrowIsLimit
#print axioms measureRightExtension
#print axioms structuredArrowFiniteComparisonIso
#print axioms structuredArrowMeasureConeIso
#print axioms measureRightExtensionIsPointwiseAt
#print axioms measureRightExtensionIsPointwise
#print axioms measureFunctorIsRightKanExtension

end CMDG.CondensedCM4P2E.RightKanReconstruction