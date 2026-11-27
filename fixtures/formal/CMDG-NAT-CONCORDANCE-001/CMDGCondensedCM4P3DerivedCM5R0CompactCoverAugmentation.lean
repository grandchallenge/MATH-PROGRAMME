import CMDGCondensedCM4P3DerivedCM5R0CompactCoverInternalExact

/-! Augmentation and its exactness for a genuinely compact Hausdorff
base of a profinite cover. All higher terms remain the actual
free condensed modules of the profinite equal-image tuple spaces. -/
noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0.CompactCover

abbrev compactFreePresheafFunctor :
    CompHaus.{u} ⥤ (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  compHausToCondensed ⋙
    sheafToPresheaf (coherentTopology CompHaus) (Type (u + 1)) ⋙
      (Functor.whiskeringRight _ _ _).obj (ModuleCat.free Coeff)

abbrev compactFreeFunctor : CompHaus.{u} ⥤ Ambient :=
  compHausToCondensed ⋙ Condensed.free Coeff

def compactRelationProjection0
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactRelationProfinite P T p 0 ⟶ P := by
  letI : CompactSpace (↥(compactCechArityRelatedSet 0 P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed 0 P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun xs => xs.val 0, by
      change Continuous
        (fun xs : ↥(compactCechArityRelatedSet 0 P T p) =>
          xs.val 0)
      exact (continuous_apply (0 : Fin 1)).comp
        continuous_subtype_val⟩)

def compactRelationSingleton
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    P ⟶ compactRelationProfinite P T p 0 := by
  letI : CompactSpace (↥(compactCechArityRelatedSet 0 P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed 0 P T p).isCompact
  let f : C(P, ↥(compactCechArityRelatedSet 0 P T p)) :=
    ⟨fun x => ⟨fun _ : Fin 1 => x, by
        intro i
        rfl⟩, by
      apply Continuous.subtype_mk
      apply continuous_pi
      intro i
      exact continuous_id⟩
  exact CompHausLike.ofHom _ f

theorem compactRelationSingleton_projection
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactRelationSingleton P T p ≫
      compactRelationProjection0 P T p = 𝟙 P := by
  ext x
  simp only [ConcreteCategory.comp_apply, ConcreteCategory.id_apply]
  rfl

theorem compactRelationProjection_singleton
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactRelationProjection0 P T p ≫
      compactRelationSingleton P T p =
        𝟙 (compactRelationProfinite P T p 0) := by
  ext xs
  simp only [ConcreteCategory.comp_apply, ConcreteCategory.id_apply]
  apply Subtype.ext
  funext i
  fin_cases i
  rfl

def compactRelationProjection0Iso
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactRelationProfinite P T p 0 ≅ P where
  hom := compactRelationProjection0 P T p
  inv := compactRelationSingleton P T p
  hom_inv_id := compactRelationProjection_singleton P T p
  inv_hom_id := compactRelationSingleton_projection P T p

def compactRelationAugMap (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) :
    profiniteToCompHaus.obj (compactRelationProfinite P T p 0) ⟶ T :=
  profiniteToCompHaus.map (compactRelationProjection0 P T p) ≫ p

theorem compactRelationAugmentation_faces_agree
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    profiniteToCompHaus.map (compactRelationFace P T p 0 (0 : Fin 2)) ≫
      compactRelationAugMap P T p =
    profiniteToCompHaus.map (compactRelationFace P T p 0 (1 : Fin 2)) ≫
      compactRelationAugMap P T p := by
  ext xs
  change p.hom.hom (xs.val 1) = p.hom.hom (xs.val 0)
  exact xs.property 1

def compactFreeRelationAugmentation
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    (Condensed.profiniteFree Coeff).obj (compactRelationProfinite P T p 0) ⟶
      compactFreeFunctor.obj T :=
  compactFreeFunctor.map (compactRelationAugMap P T p)

theorem compactFreeRelationAugmentation_comp_boundary_zero
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactFreeRelationBoundary P T p 0 ≫ compactFreeRelationAugmentation P T p = 0 := by
  unfold compactFreeRelationBoundary compactFreeRelationAugmentation
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero,pow_zero,one_smul,Fin.val_one,pow_one,neg_smul,← sub_eq_add_neg,
    Preadditive.sub_comp]
  change compactFreeFunctor.map (profiniteToCompHaus.map (compactRelationFace P T p 0 0)) ≫
      compactFreeFunctor.map (compactRelationAugMap P T p) -
    compactFreeFunctor.map (profiniteToCompHaus.map (compactRelationFace P T p 0 1)) ≫
      compactFreeFunctor.map (compactRelationAugMap P T p) = 0
  rw [← Functor.map_comp,← Functor.map_comp,compactRelationAugmentation_faces_agree,sub_self]

def compactPresheafRelationAugmentation
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    freeCompHausModulePresheaf (compactRelationProfinite P T p 0) ⟶
      compactFreePresheafFunctor.obj T :=
  compactFreePresheafFunctor.map (compactRelationAugMap P T p)

theorem compactPresheafRelationAugmentation_comp_boundary_zero
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactPresheafRelationBoundary P T p 0 ≫ compactPresheafRelationAugmentation P T p = 0 := by
  unfold compactPresheafRelationBoundary compactPresheafRelationAugmentation
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero,pow_zero,one_smul,Fin.val_one,pow_one,neg_smul,← sub_eq_add_neg,
    Preadditive.sub_comp]
  change compactFreePresheafFunctor.map (profiniteToCompHaus.map (compactRelationFace P T p 0 0)) ≫
      compactFreePresheafFunctor.map (compactRelationAugMap P T p) -
    compactFreePresheafFunctor.map (profiniteToCompHaus.map (compactRelationFace P T p 0 1)) ≫
      compactFreePresheafFunctor.map (compactRelationAugMap P T p) = 0
  rw [← Functor.map_comp,← Functor.map_comp,compactRelationAugmentation_faces_agree,sub_self]

theorem compactPresheafRelationAugmentation_sheafify
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    moduleSheafification.map
      (compactPresheafRelationAugmentation P T p) =
      compactFreeRelationAugmentation P T p := by
  rfl

def compactPresheafRelationAugShortComplex
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (compactPresheafRelationBoundary P T p 0)
    (compactPresheafRelationAugmentation P T p)
    (compactPresheafRelationAugmentation_comp_boundary_zero P T p)

/-- Exact sheafification/dense-Stonean transfer at augmentation degree
zero for the actual free-module relation presentation. -/
theorem compactRelationAugZeroExact_of_stoneanPresheafExact
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (h : ((compactPresheafRelationAugShortComplex P T p).map
      stoneanPresheafRestriction).Exact) :
    (ShortComplex.mk
      (compactFreeRelationBoundary P T p 0)
      (compactFreeRelationAugmentation P T p)
      (compactFreeRelationAugmentation_comp_boundary_zero P T p)).Exact := by
  let S := compactPresheafRelationAugShortComplex P T p
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
      kernel.ι (compactFreeRelationAugmentation P T p) ≫
      cokernel.π (compactFreeRelationBoundary P T p 0) = 0 := by
    rw [← compactPresheafRelationAugmentation_sheafify P T p,
      ← compactPresheafRelationBoundary_sheafify P T p 0]
    exact hZero
  exact ((ShortComplex.mk
    (compactFreeRelationBoundary P T p 0)
    (compactFreeRelationAugmentation P T p)
    (compactFreeRelationAugmentation_comp_boundary_zero P T p)).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

private abbrev compactAugFreeProbe (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :=
  (ModuleCat.free Coeff).obj
    (uniformProbeHomSet U (compactRelationProfinite P T p n))

def compactProbeBarEpsilon (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactAugFreeProbe U P T p 0 ⟶
      (ModuleCat.free Coeff).obj (compactProbeHomSet U T) :=
  (ModuleCat.free Coeff).map
    (↾(fun z : uniformProbeHomSet U (compactRelationProfinite P T p 0) =>
      ULift.up (z.down ≫
        (profiniteToCompHaus.map (compactRelationProjection0 P T p) ≫ p))))

theorem compactProbeBarEpsilon_square (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    (compactProbeBarIso U P T p 0).hom ≫
      splitBarBaseMap (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) =
    compactProbeBarEpsilon U P T p := by
  change (ModuleCat.free Coeff).map (↾compactProbeTupleEquiv U P T p 0) ≫
    (ModuleCat.free Coeff).map
      (↾splitCechBaseProjection (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p)) =
    (ModuleCat.free Coeff).map
      (↾(fun z : uniformProbeHomSet U (compactRelationProfinite P T p 0) =>
        ULift.up (z.down ≫
          (profiniteToCompHaus.map (compactRelationProjection0 P T p) ≫ p))))
  rw [← Functor.map_comp]
  congr 1

theorem compactProbeBarEpsilon_comp_boundary_zero
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactProbeBarD U P T p 0 ≫
      compactProbeBarEpsilon U P T p = 0 := by
  rw [← compactProbeBarEpsilon_square]
  rw [← Category.assoc, compactProbeBarD_square, Category.assoc,
    splitBarZeroBoundary_comp_augmentation, comp_zero]

def compactProbeBarAugZeroShortComplex (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (compactProbeBarD U P T p 0)
    (compactProbeBarEpsilon U P T p)
    (compactProbeBarEpsilon_comp_boundary_zero U P T p)

def compactProbeBarAugZeroIso (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    compactProbeBarAugZeroShortComplex U P T p ≅
      splitBarZeroShortComplex (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) := by
  refine ShortComplex.isoMk
    (compactProbeBarIso U P T p 1)
    (compactProbeBarIso U P T p 0)
    (Iso.refl _) ?_ ?_
  · exact (compactProbeBarD_square U P T p 0).symm
  · change (compactProbeBarIso U P T p 0).hom ≫
        splitBarBaseMap (uniformProbeHomSet U P)
          (compactProbeHomSet U T) (compactProbeMap U P T p) =
        compactProbeBarEpsilon U P T p ≫ (𝟙 _)
    simpa only [Category.comp_id] using
      (compactProbeBarEpsilon_square U P T p)

theorem compactProbeBarAugZeroExact (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (s : compactProbeHomSet U T → uniformProbeHomSet U P)
    (hs : ∀ b, compactProbeMap U P T p (s b) = b) :
    (compactProbeBarAugZeroShortComplex U P T p).Exact := by
  exact ShortComplex.exact_of_iso
    (compactProbeBarAugZeroIso U P T p).symm
    (splitBarZeroShortExact (uniformProbeHomSet U P)
      (compactProbeHomSet U T) (compactProbeMap U P T p) s hs)

theorem compactProbePresheafAugmentation_eval
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    (compactPresheafRelationAugmentation P T p).app
      (Opposite.op U.compHaus) =
    compactProbeBarEpsilon U P T p := by
  rfl

theorem compactStoneanRestrictedPresheafAugZeroExact
    (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] :
    ((compactPresheafRelationAugShortComplex P T p).map
        stoneanPresheafRestriction).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  let Q := ((compactPresheafRelationAugShortComplex P T p).map
      stoneanPresheafRestriction).map
        ((evaluation Stoneanᵒᵖ (ModuleCat Coeff)).obj U)
  let W := compactProbeBarAugZeroShortComplex U.unop P T p
  have hf : Q.f = W.f := by
    change (compactPresheafRelationBoundary P T p 0).app
      (Opposite.op U.unop.compHaus) = compactProbeBarD U.unop P T p 0
    unfold compactPresheafRelationBoundary compactProbeBarD
    rw [NatTrans.app_sum]
    simp only [NatTrans.app_zsmul]
    apply Finset.sum_congr rfl
    intro k hk
    rw [compactProbePresheafFace_eval U.unop P T p 0 k]
  have hg : Q.g = W.g := compactProbePresheafAugmentation_eval U.unop P T p
  obtain ⟨s,hs⟩ := compactProbeSplit U.unop P T p
  have hW : W.Exact := compactProbeBarAugZeroExact U.unop P T p s hs
  change Q.Exact
  apply (Q.exact_iff_kernel_ι_comp_cokernel_π_zero).2
  rw [hf,hg]
  exact (W.exact_iff_kernel_ι_comp_cokernel_π_zero).1 hW

theorem compactFreeCechAugmentationExact
    (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] :
    (ShortComplex.mk (compactFreeRelationBoundary P T p 0)
      (compactFreeRelationAugmentation P T p)
      (compactFreeRelationAugmentation_comp_boundary_zero P T p)).Exact :=
  compactRelationAugZeroExact_of_stoneanPresheafExact P T p
    (compactStoneanRestrictedPresheafAugZeroExact P T p)

theorem compactFreeCechAugmentationEpi
    (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] :
    Epi (compactFreeRelationAugmentation P T p) := by
  let f := compactPresheafRelationAugmentation P T p
  let R := stoneanPresheafRestriction
  let A := stoneanModuleSheafification
  let E := (Condensed.StoneanCompHaus.equivalence (ModuleCat Coeff)).inverse
  haveI : Epi (R.map f) := by
    apply (NatTrans.epi_iff_epi_app _).2
    intro U
    change Epi (compactProbeBarEpsilon U.unop P T p)
    let g : uniformProbeHomSet U.unop (compactRelationProfinite P T p 0) →
        compactProbeHomSet U.unop T := fun z =>
      ULift.up (z.down ≫ (profiniteToCompHaus.map (compactRelationProjection0 P T p) ≫ p))
    haveI : Epi (↾g) := (CategoryTheory.ofHom_epi_iff_surjective g).2 (by
      intro b
      obtain ⟨s,hs⟩ := compactProbeSplit U.unop P T p
      refine ⟨ULift.up ((s b).down ≫
        profiniteToCompHaus.map (compactRelationSingleton P T p)), ?_⟩
      apply ULift.ext
      change ((s b).down ≫ profiniteToCompHaus.map (compactRelationSingleton P T p)) ≫
        (profiniteToCompHaus.map (compactRelationProjection0 P T p) ≫ p) = b.down
      rw [Category.assoc,← Category.assoc (profiniteToCompHaus.map
        (compactRelationSingleton P T p)),← Functor.map_comp,
        compactRelationSingleton_projection,Functor.map_id,Category.id_comp]
      exact congrArg ULift.down (hs b))
    exact (ModuleCat.free Coeff).map_epi (↾g)
  haveI : Epi ((R ⋙ A).map f) := by
    change Epi (A.map (R.map f))
    infer_instance
  let i : R ⋙ A ≅ moduleSheafification ⋙ E := stoneanCompHausSheafificationCompatibility
  have he := i.hom.naturality f
  haveI : Epi ((R ⋙ A).map f ≫ i.hom.app _) := inferInstance
  haveI : Epi ((moduleSheafification ⋙ E).map f) := epi_of_epi_fac he.symm
  have hepi : Epi (moduleSheafification.map f) :=
    E.epi_of_epi_map (show Epi (E.map (moduleSheafification.map f)) from inferInstance)
  exact hepi

#print axioms compactFreeCechAugmentationExact
#print axioms compactFreeCechAugmentationEpi
end CMDG.CondensedCM5R0.CompactCover
