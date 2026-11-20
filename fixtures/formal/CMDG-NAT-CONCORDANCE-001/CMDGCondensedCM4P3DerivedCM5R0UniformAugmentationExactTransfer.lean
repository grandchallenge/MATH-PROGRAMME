import CMDGCondensedCM4P3DerivedCM5R0UniformInternalExactnessTransfer
import CMDGCondensedCM4P3DerivedCM5R0UniformSplitCechBarExact

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Genuine CompHaus representable free-module presheaf augmentation,
before sheafification. -/
def uniformPresheafRelationAugmentation
    (P T : Profinite.{u}) (p : P ⟶ T) :
    freeCompHausModulePresheaf (uniformRelationProfinite P T p 0) ⟶
      freeCompHausModulePresheaf T :=
  freeCompHausModulePresheafFunctor.map
    (uniformRelationProjection0 P T p ≫ p)

theorem uniformPresheafRelationAugmentation_comp_boundary_zero
    (P T : Profinite.{u}) (p : P ⟶ T) :
    uniformPresheafRelationBoundary P T p 0 ≫
      uniformPresheafRelationAugmentation P T p = 0 := by
  unfold uniformPresheafRelationBoundary uniformPresheafRelationAugmentation
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero, pow_zero, one_smul, Fin.val_one,
    pow_one, neg_smul, ← sub_eq_add_neg,
    Preadditive.sub_comp, ← Functor.map_comp]
  rw [uniformRelationAugmentation_faces_agree]
  exact sub_self _

theorem uniformPresheafRelationAugmentation_sheafify
    (P T : Profinite.{u}) (p : P ⟶ T) :
    moduleSheafification.map
      (uniformPresheafRelationAugmentation P T p) =
      uniformFreeRelationAugmentation P T p := by
  rfl

def uniformPresheafRelationAugShortComplex
    (P T : Profinite.{u}) (p : P ⟶ T) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (uniformPresheafRelationBoundary P T p 0)
    (uniformPresheafRelationAugmentation P T p)
    (uniformPresheafRelationAugmentation_comp_boundary_zero P T p)

/-- Exact sheafification/dense-Stonean transfer at augmentation degree
zero for the actual free-module relation presentation. -/
theorem uniformRelationAugZeroExact_of_stoneanPresheafExact
    (P T : Profinite.{u}) (p : P ⟶ T)
    (h : ((uniformPresheafRelationAugShortComplex P T p).map
      stoneanPresheafRestriction).Exact) :
    (ShortComplex.mk
      (uniformFreeRelationBoundary P T p 0)
      (uniformFreeRelationAugmentation P T p)
      (uniformFreeRelationAugmentation_comp_boundary_zero P T p)).Exact := by
  let S := uniformPresheafRelationAugShortComplex P T p
  let R := stoneanPresheafRestriction
  let A := stoneanModuleSheafification
  let E := (Condensed.StoneanCompHaus.equivalence
    (ModuleCat Coeff)).inverse
  haveI : PreservesFiniteLimits A := by
    change PreservesFiniteLimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  haveI : PreservesFiniteColimits A := by
    change PreservesFiniteColimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  have hStonean : ((S.map R).map A).Exact := h.map A
  have hStonean' : (S.map (R ⋙ A)).Exact := by
    simpa only [ShortComplex.map_comp] using hStonean
  have hTransport :
      (S.map (moduleSheafification ⋙ E)).Exact :=
    ShortComplex.exact_of_iso
      (S.mapNatIso stoneanCompHausSheafificationCompatibility)
      hStonean'
  have hTransport' :
      ((S.map moduleSheafification).map E).Exact := by
    simpa only [ShortComplex.map_comp] using hTransport
  have hComp : (S.map moduleSheafification).Exact :=
    E.reflects_exact_of_faithful _ hTransport'
  have hZero :
      kernel.ι ((S.map moduleSheafification).g) ≫
      cokernel.π ((S.map moduleSheafification).f) = 0 :=
    ((S.map moduleSheafification).exact_iff_kernel_ι_comp_cokernel_π_zero).1 hComp
  have hZero' :
      kernel.ι (uniformFreeRelationAugmentation P T p) ≫
      cokernel.π (uniformFreeRelationBoundary P T p 0) = 0 := by
    rw [← uniformPresheafRelationAugmentation_sheafify P T p,
      ← uniformPresheafRelationBoundary_sheafify P T p 0]
    exact hZero
  exact ((ShortComplex.mk
    (uniformFreeRelationBoundary P T p 0)
    (uniformFreeRelationAugmentation P T p)
    (uniformFreeRelationAugmentation_comp_boundary_zero P T p)).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

#print axioms uniformRelationAugZeroExact_of_stoneanPresheafExact
end CMDG.CondensedCM5R0
