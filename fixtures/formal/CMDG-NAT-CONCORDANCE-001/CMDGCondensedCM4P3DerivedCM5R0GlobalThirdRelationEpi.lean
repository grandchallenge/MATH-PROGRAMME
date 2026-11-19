import CMDGCondensedCM4P3DerivedCM5R0ProbeDegreeTwoExact
import CMDGCondensedCM4P3DerivedCM5R0StoneanCechDegreeOneClosure
import CMDGCondensedCM4P3DerivedCM5R0GenuineFourthCechBoundary

/-!
# CMDG CM5 — global fourth Čech boundary onto the true third relation

For ANY profinite T, the original Stonean presentation gives
the actual categorical fourfold Čech pullback P(T)^4_T and
triple/pair relation maps. We prove a full genuine CompHaus
free-module presheaf fourth Čech differential with the correct
alternating face signs. Its composite with the triple differential
vanishes, and exact sheafification identifies it with the true
condensed-module fourth differential, not an ersatz finite model.

The pinned exact represented-degree-two theorem at every Stonean
probe gives exactness of the actual restricted presheaf complex.
The admitted dense Stonean sheaf equivalence and exact
sheafification transport this to global short-complex exactness
at F_{P(T)^3_T} for any profinite T.

The actual triple-to-second-relation epimorphism factors through
a monomorphism L_T→F_{P(T)^2_T}. The canonical kernel comparison
therefore identifies the exactness with *Epi* of the genuine
fourth-to-third relation morphism
    F_{P(T)^4_T} → M_T
where M_T=kernel(F_{P(T)^3_T}→L_T).

This proves global degree-two Čech exactness and third relation
generation for arbitrary profinite T. It does NOT establish
Ext³(F_T,G_S)=0, global scalar H³ primitives, all-shift derived
solidity or any Liquid-Tensor capstone. Coefficient-valued
extension is a separate substantive mathematical obligation.
-/

noncomputable section
universe u
open CategoryTheory Limits CategoryTheory.Functor
namespace CMDG.CondensedCM5R0

private noncomputable abbrev globalQuadXYZ (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
    stoneanPresentationCechTriples T :=
  pullback.fst
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- Actual fourth boundary in CompHaus module presheaves. -/
noncomputable def presheafStoneanCechFourthBoundary
    (T : Profinite.{u}) :
    freeCompHausModulePresheaf (stoneanPresentationCechQuadruples T) ⟶
    freeCompHausModulePresheaf (stoneanPresentationCechTriples T) :=
  freeCompHausModulePresheafFunctor.map (quadFaceYZW T) -
    freeCompHausModulePresheafFunctor.map (quadFaceXZW T) +
    freeCompHausModulePresheafFunctor.map (quadFaceXYW T) -
    freeCompHausModulePresheafFunctor.map (globalQuadXYZ T)

/-- The true presheaf fourth differential composes trivially
with the existing signed triple boundary, on the full CompHaus site. -/
theorem presheafStoneanCechFourthBoundary_comp_triple_zero
    (T : Profinite.{u}) :
    presheafStoneanCechFourthBoundary T ≫
      presheafStoneanCechTripleBoundary T = 0 := by
  unfold presheafStoneanCechFourthBoundary
    presheafStoneanCechTripleBoundary
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, ← Functor.map_comp]
  have hX : globalQuadXYZ T ≫ stoneanCechTripleXZ T =
      quadFaceXZW T ≫ stoneanCechTripleXY T := by
    unfold quadFaceXZW
    rw [pullback.lift_fst]
    rfl
  have hY : globalQuadXYZ T ≫ stoneanCechTripleYZ T =
      quadFaceYZW T ≫ stoneanCechTripleXY T := by
    unfold quadFaceYZW
    rw [pullback.lift_fst]
    rfl
  have hXY : globalQuadXYZ T ≫ stoneanCechTripleXY T =
      quadFaceXYW T ≫ stoneanCechTripleXY T := by
    unfold quadFaceXYW
    rw [pullback.lift_fst]
    rfl
  rw [quadFaceXZW_xw, quadFaceXYW_yw, quadFaceXZW_zw]
  rw [hX, hY, hXY]
  simp only [sub_eq_add_neg]
  abel

noncomputable def presheafStoneanCechDegreeTwoComplex
    (T : Profinite.{u}) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (presheafStoneanCechFourthBoundary T)
    (presheafStoneanCechTripleBoundary T)
    (presheafStoneanCechFourthBoundary_comp_triple_zero T)

/-- The differential sheafifies to the genuine protected quadruple
boundary of the same full Stonean Čech nerve. -/
theorem presheafStoneanCechFourthBoundary_sheafify
    (T : Profinite.{u}) :
    moduleSheafification.map (presheafStoneanCechFourthBoundary T) =
      stoneanCechFourthBoundary T := by
  unfold presheafStoneanCechFourthBoundary stoneanCechFourthBoundary
  rw [Functor.map_sub, Functor.map_add, Functor.map_sub]
  rfl

noncomputable abbrev stoneanRestrictedCechDegreeTwoComplex
    (T : Profinite.{u}) :
    ShortComplex (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  (presheafStoneanCechDegreeTwoComplex T).map
    stoneanPresheafRestriction

/-- Every Stonean probe sees degree-two exactness of the *actual*
CompHaus free presheaf fourth/triple Čech complex. -/
theorem stoneanRestrictedCechDegreeTwo_exact
    (T : Profinite.{u}) :
    (stoneanRestrictedCechDegreeTwoComplex T).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  change (trueProbeDegreeTwoComplex T U.unop).Exact
  exact trueProbeDegreeTwo_exact T U.unop


/-- The actual condensed-module fourth/triple Čech complex, not a
surrogate presheaf complex. -/
noncomputable def stoneanCechDegreeTwoComplex (T : Profinite.{u}) :
    ShortComplex Ambient :=
  ShortComplex.mk (stoneanCechFourthBoundary T)
    (stoneanCechTripleBoundary T)
    (stoneanCechFourthBoundary_comp_tripleBoundary_zero T)

/-- The genuine dense Stonean site transfers degree-two exactness
to the real sheafified condensed-module fourth/triple complex. -/
theorem stoneanCechDegreeTwo_exact_unconditional
    (T : Profinite.{u}) :
    (stoneanCechDegreeTwoComplex T).Exact := by
  let S := presheafStoneanCechDegreeTwoComplex T
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
  have hStonean : ((S.map R).map A).Exact :=
    (stoneanRestrictedCechDegreeTwo_exact T).map A
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
      kernel.ι (stoneanCechTripleBoundary T) ≫
      cokernel.π (stoneanCechFourthBoundary T) = 0 := by
    rw [← presheafStoneanCechTripleBoundary_sheafify T,
      ← presheafStoneanCechFourthBoundary_sheafify T]
    exact hZero
  exact ((stoneanCechDegreeTwoComplex T).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

/-- The degree-two exact complex with genuine third relation as
right term; compare via a monic inclusion L_T↪F_R. -/
noncomputable def stoneanCechDegreeTwoKernelComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk (stoneanCechFourthBoundary T)
    (stoneanCechTripleToSecondRelation T)
    (stoneanCechFourthBoundary_comp_secondRelation_zero T)

noncomputable def stoneanCechDegreeTwoKernelComparison
    (T : Profinite.{u}) :
    stoneanCechDegreeTwoKernelComplex T ⟶
      stoneanCechDegreeTwoComplex T :=
  ShortComplex.homMk
    (𝟙 _) (𝟙 _) (kernel.ι (stoneanCechRelationToKernel T))
    (by dsimp [stoneanCechDegreeTwoKernelComplex, stoneanCechDegreeTwoComplex]; simp)
    (by dsimp [stoneanCechDegreeTwoKernelComplex, stoneanCechDegreeTwoComplex]
        simpa only [Category.id_comp] using
          (stoneanCechTripleToSecondRelation_comp_ι T).symm)

/-- The actual fourth free condensed module epimorphically generates
the third relation kernel M_T, for every profinite T. -/
theorem stoneanCechFourthToThirdRelation_epi_unconditional
    (T : Profinite.{u}) :
    Epi (stoneanCechFourthToThirdRelation T) := by
  haveI : Epi (stoneanCechDegreeTwoKernelComparison T).τ₁ := by
    change Epi (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)))
    infer_instance
  haveI : IsIso (stoneanCechDegreeTwoKernelComparison T).τ₂ := by
    change IsIso (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)))
    infer_instance
  haveI : Mono (stoneanCechDegreeTwoKernelComparison T).τ₃ := by
    change Mono (kernel.ι (stoneanCechRelationToKernel T))
    infer_instance
  have h := stoneanCechDegreeTwo_exact_unconditional T
  have hk : (stoneanCechDegreeTwoKernelComplex T).Exact :=
    (ShortComplex.exact_iff_of_epi_of_isIso_of_mono
      (stoneanCechDegreeTwoKernelComparison T)).mpr h
  exact ((stoneanCechDegreeTwoKernelComplex T).exact_iff_epi_kernel_lift).mp hk

#print axioms stoneanCechDegreeTwo_exact_unconditional
#print axioms stoneanCechFourthToThirdRelation_epi_unconditional

#print axioms presheafStoneanCechFourthBoundary_comp_triple_zero
#print axioms presheafStoneanCechFourthBoundary_sheafify
#print axioms stoneanRestrictedCechDegreeTwo_exact

end CMDG.CondensedCM5R0
