import CMDGCondensedCM4P3DerivedCM5R0RealBoxCechPresheaf

/-! Exact augmented resolution on every compact probe, then exact
sheafification. This does not assume any global continuous section
of the coproduct cover. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.RealProductProjection
variable (S : Profinite.{u}) (I : Type u)

theorem boxCechPsh_sqZero (n : ℕ) :
    boxCechPshD S I (n+1) ≫ boxCechPshD S I n = 0 := by
  apply NatTrans.ext
  funext T
  change (boxCechPshD S I (n+1)).app T ≫ (boxCechPshD S I n).app T = 0
  apply (cancel_mono (boxCechEvalIso S I T.unop n).hom).1
  rw [Category.assoc,boxCechEvalD,← Category.assoc,boxCechEvalD,
    Category.assoc,splitBarD_comp_D_zero,comp_zero,zero_comp]

theorem boxCechPsh_augZero :
    boxCechPshD S I 0 ≫ boxCechPshAug S I = 0 := by
  apply NatTrans.ext
  funext T
  change (boxCechPshD S I 0).app T ≫ (boxCechPshAug S I).app T = 0
  rw [boxCechEvalAug,← Category.assoc,boxCechEvalD,Category.assoc,
    splitBarZeroBoundary_comp_augmentation,comp_zero]

abbrev boxCechPshSeq (n : ℕ) :=
  ShortComplex.mk (boxCechPshD S I (n+1)) (boxCechPshD S I n) (boxCechPsh_sqZero S I n)

abbrev boxCechPshAugSeq :=
  ShortComplex.mk (boxCechPshD S I 0) (boxCechPshAug S I) (boxCechPsh_augZero S I)

theorem boxCechPsh_exact (n : ℕ) : (boxCechPshSeq S I n).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro T
  let W := splitBarShortComplex _ _ (liftImage S I T.unop) n
  let Q := (boxCechPshSeq S I n).map ((evaluation _ _).obj T)
  have e : Q ≅ W := ShortComplex.isoMk (boxCechEvalIso S I T.unop (n+2))
    (boxCechEvalIso S I T.unop (n+1)) (boxCechEvalIso S I T.unop n)
    (boxCechEvalD S I T.unop (n+1)).symm (boxCechEvalD S I T.unop n).symm
  obtain ⟨s,hs⟩ := (liftImage_surj S I T.unop).hasRightInverse
  exact ShortComplex.exact_of_iso e.symm (splitBarShortComplex_exact _ _ _ s hs n)

theorem boxCechPsh_augExact : (boxCechPshAugSeq S I).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro T
  let W := splitBarZeroShortComplex _ _ (liftImage S I T.unop)
  let Q := (boxCechPshAugSeq S I).map ((evaluation _ _).obj T)
  have e : Q ≅ W := ShortComplex.isoMk (boxCechEvalIso S I T.unop 1)
    (boxCechEvalIso S I T.unop 0) (Iso.refl _)
    (boxCechEvalD S I T.unop 0).symm (by
      change (boxCechEvalIso S I T.unop 0).hom ≫ splitBarBaseMap _ _ _ =
        (boxCechPshAug S I).app T ≫ 𝟙 _
      rw [Category.comp_id,boxCechEvalAug])
  obtain ⟨s,hs⟩ := (liftImage_surj S I T.unop).hasRightInverse
  exact ShortComplex.exact_of_iso e.symm (splitBarZeroShortExact _ _ _ s hs)

theorem boxCechPsh_augEpi : Epi (boxCechPshAug S I) := by
  haveI : ∀ T, Epi ((boxCechPshAug S I).app T) := by
    intro T
    rw [boxCechEvalAug]
    obtain ⟨s,hs⟩ := (liftImage_surj S I T.unop).hasRightInverse
    have he : splitBarBaseSection _ _ (liftImage S I T.unop) s ≫
        splitBarBaseMap _ _ (liftImage S I T.unop) = 𝟙 _ := by
      unfold splitBarBaseSection splitBarBaseMap
      rw [← Functor.map_comp]
      have h : (↾splitCechBaseSection _ _ (liftImage S I T.unop) s) ≫
          (↾splitCechBaseProjection _ _ (liftImage S I T.unop)) = 𝟙 _ := by
        apply ConcreteCategory.hom_ext
        intro b
        exact hs b
      rw [h]
      exact (ModuleCat.free Coeff).map_id _
    haveI : IsSplitEpi (splitBarBaseMap _ _ (liftImage S I T.unop)) :=
      ⟨⟨splitBarBaseSection _ _ _ s,he⟩⟩
    infer_instance
  exact NatTrans.epi_of_epi_app _

abbrev boxCechTerm (n : ℕ) := moduleSheafification.obj (boxCechPsh S I n)
abbrev boxCechD (n : ℕ) := moduleSheafification.map (boxCechPshD S I n)
abbrev boxCechAug := moduleSheafification.map (boxCechPshAug S I)

def boxCechResolution : AcyclicResolution.Resolution.{u} where
  target := (freeProbeRealCocone S I).pt
  term := boxCechTerm S I
  aug := boxCechAug S I
  d := boxCechD S I
  aug_zero := by rw [← Functor.map_comp,boxCechPsh_augZero,Functor.map_zero]
  sq_zero n := by rw [← Functor.map_comp,boxCechPsh_sqZero,Functor.map_zero]
  aug_epi := by
    letI := boxCechPsh_augEpi S I
    exact moduleSheafification.map_epi _
  aug_exact := moduleSheafification_preservesExact _ (boxCechPsh_augExact S I)
  exact n := moduleSheafification_preservesExact _ (boxCechPsh_exact S I n)

#print axioms boxCechPsh_exact
#print axioms boxCechPsh_augExact
#print axioms boxCechResolution
end CMDG.CondensedCM5R0.RealProductProjection
