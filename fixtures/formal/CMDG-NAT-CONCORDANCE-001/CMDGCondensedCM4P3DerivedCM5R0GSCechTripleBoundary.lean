import CMDGCondensedCM4P3DerivedCM5R0GSCechSecondRelation
import CMDGCondensedCM4P3DerivedCM5R0StoneanCechTripleCocycle
import Mathlib.CategoryTheory.EpiMono

/-!
# CMDG CM5: the genuine alternating triple-Cech boundary

For an arbitrary profinite T, the alternating xz-xy-yz map out of
F_{P(T) x_T P(T) x_T P(T)} has zero composite with the actual
Cech-pair relation map F_{P x_T P} -> K_T. It therefore factors through
the SECOND relation kernel L_T = ker(F_{P x_T P} -> K_T).

For a presentation p : P -> T with a section s : T -> P, there is an
explicit contraction using triples (x,y,s(p(x))). This proves that the
triple-to-second-kernel map is a split epimorphism, hence an epi, for
all split presentations. In particular this applies to Stonean T,
whose projectivity supplies a section of its canonical presentation.

The arbitrary-profinite epi case does not follow from this split
argument, and is NOT asserted. This does not prove Ext^2 vanishing,
the extension property for G_S, or derived solidity.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The ACTUAL alternating second Cech boundary. Our sign convention
matches the protected first boundary d1(x,y)=x-y. -/
noncomputable def stoneanCechTripleBoundary (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T) ⟶
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T) :=
  (Condensed.profiniteFree Coeff).map (stoneanCechTripleXZ T) -
    (Condensed.profiniteFree Coeff).map (stoneanCechTripleXY T) -
    (Condensed.profiniteFree Coeff).map (stoneanCechTripleYZ T)

/-- The alternating second differential is killed by the actual
relation epimorphism F_R -> K_T, for every profinite T. -/
theorem stoneanCechTripleBoundary_comp_relation_zero
    (T : Profinite.{u}) :
    stoneanCechTripleBoundary T ≫ stoneanCechRelationToKernel T = 0 := by
  unfold stoneanCechTripleBoundary
  simp only [Preadditive.sub_comp]
  rw [stoneanCechRelationToKernel_triple]
  abel

/-- Canonical lift of the genuine triple boundary into L_T,
the SECOND syzygy, for any profinite T. -/
noncomputable def stoneanCechTripleToSecondRelation
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T) ⟶
    stoneanCechSecondRelationKernel T :=
  kernel.lift (stoneanCechRelationToKernel T)
    (stoneanCechTripleBoundary T)
    (stoneanCechTripleBoundary_comp_relation_zero T)

/-- The lift is the actual alternating map after the kernel inclusion. -/
theorem stoneanCechTripleToSecondRelation_comp_ι
    (T : Profinite.{u}) :
    stoneanCechTripleToSecondRelation T ≫
      kernel.ι (stoneanCechRelationToKernel T) =
        stoneanCechTripleBoundary T := by
  simp [stoneanCechTripleToSecondRelation]

/-- The extra pair (x,s(p(x))) for a *split* Stonean presentation. -/
private noncomputable def stoneanCechExtraPair
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    Stonean.toProfinite.obj T.presentation ⟶
      stoneanPresentationCechPairs T := by
  let p := Profinite.presentation.π T
  refine pullback.lift (𝟙 _) (p ≫ s) ?_
  simp only [Category.id_comp, Category.assoc, hs, Category.comp_id]

/-- Extra triple (x,y,s(p(x))) on the actual Cech pair object. -/
private noncomputable def stoneanCechExtraTriple
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    stoneanPresentationCechPairs T ⟶
      stoneanPresentationCechTriples T := by
  let p := Profinite.presentation.π T
  refine pullback.lift (𝟙 _) ((pullback.fst p p ≫ p) ≫ s) ?_
  simp only [Category.id_comp, Category.assoc, hs, Category.comp_id]

private theorem stoneanCechExtraTriple_xy
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    stoneanCechExtraTriple T s hs ≫ stoneanCechTripleXY T =
      𝟙 (stoneanPresentationCechPairs T) := by
  simp [stoneanCechExtraTriple, stoneanCechTripleXY]

private theorem stoneanCechExtraTriple_xz
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    stoneanCechExtraTriple T s hs ≫ stoneanCechTripleXZ T =
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      stoneanCechExtraPair T s hs := by
  apply pullback.hom_ext
  · simp [stoneanCechTripleXZ, stoneanCechExtraTriple,
      stoneanCechExtraPair, Category.assoc]
  · simp [stoneanCechTripleXZ, stoneanCechExtraTriple,
      stoneanCechExtraPair, Category.assoc]

private theorem stoneanCechExtraTriple_yz
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    stoneanCechExtraTriple T s hs ≫ stoneanCechTripleYZ T =
      pullback.snd (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      stoneanCechExtraPair T s hs := by
  apply pullback.hom_ext
  · simp [stoneanCechTripleYZ, stoneanCechExtraTriple,
      stoneanCechExtraPair, Category.assoc]
  · simp [stoneanCechTripleYZ, stoneanCechExtraTriple,
      stoneanCechExtraPair, Category.assoc]

/-- Explicit contracting identity in the free condensed-module category:
d2(x,y,s(p(x))) = d1(x,y) carried into the split pair - (x,y).
It does NOT assume exactness or projectivity of the relation kernel. -/
theorem stoneanCechTripleBoundary_split_contraction
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    (Condensed.profiniteFree Coeff).map (stoneanCechExtraTriple T s hs) ≫
        stoneanCechTripleBoundary T =
      stoneanCechDifference T ≫
        (Condensed.profiniteFree Coeff).map (stoneanCechExtraPair T s hs) -
      𝟙 ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechPairs T)) := by
  unfold stoneanCechTripleBoundary stoneanCechDifference
  simp only [Preadditive.comp_sub, Preadditive.sub_comp, ← Functor.map_comp,
    stoneanCechExtraTriple_xy, stoneanCechExtraTriple_xz,
    stoneanCechExtraTriple_yz, Functor.map_id, Category.comp_id]
  abel

/-- Every triple relation generates the entire second kernel if the
profinite presentation has a global section. The proof supplies an
explicit splitting, not a nonconstructive epi assertion. -/
theorem stoneanCechTripleToSecondRelation_split
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    ∃ r : stoneanCechSecondRelationKernel T ⟶
      (Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechTriples T),
      r ≫ stoneanCechTripleToSecondRelation T =
        𝟙 (stoneanCechSecondRelationKernel T) := by
  let i := kernel.ι (stoneanCechRelationToKernel T)
  let h := (Condensed.profiniteFree Coeff).map
    (stoneanCechExtraTriple T s hs)
  have hi : i ≫ stoneanCechDifference T = 0 := by
    rw [← stoneanCechRelationToKernel_comp_ι, ← Category.assoc]
    simp [i]
  have hc : (i ≫ h) ≫ stoneanCechTripleBoundary T = -i := by
    rw [Category.assoc, show h ≫ stoneanCechTripleBoundary T =
      stoneanCechDifference T ≫
        (Condensed.profiniteFree Coeff).map (stoneanCechExtraPair T s hs) -
      𝟙 _ from stoneanCechTripleBoundary_split_contraction T s hs]
    simp only [Preadditive.comp_sub, ← Category.assoc, hi,
      zero_comp, Category.comp_id, zero_sub]
  refine ⟨-(i ≫ h), ?_⟩
  apply (cancel_mono i).1
  calc
    (-(i ≫ h) ≫ stoneanCechTripleToSecondRelation T) ≫ i =
      -((i ≫ h) ≫ stoneanCechTripleBoundary T) := by
        simp [Preadditive.neg_comp, Category.assoc,
          stoneanCechTripleToSecondRelation_comp_ι]
    _ = i := by rw [hc, neg_neg]
    _ = (𝟙 _) ≫ i := by simp

/-- For a split presentation, the genuine triple boundary generates
L_T epimorphically. -/
theorem stoneanCechTripleToSecondRelation_epi_of_section
    (T : Profinite.{u})
    (s : T ⟶ Stonean.toProfinite.obj T.presentation)
    (hs : s ≫ Profinite.presentation.π T = 𝟙 T) :
    Epi (stoneanCechTripleToSecondRelation T) := by
  obtain ⟨r, hr⟩ := stoneanCechTripleToSecondRelation_split T s hs
  exact (SplitEpi.mk r hr).epi

/-- In particular, Stonean T has a section of its canonical
presentation because Stonean objects are projective in Profinite. -/
theorem stoneanCechTripleToSecondRelation_epi_stonean
    (S : Stonean.{u}) :
    Epi (stoneanCechTripleToSecondRelation
      (Stonean.toProfinite.obj S)) := by
  let T := Stonean.toProfinite.obj S
  let p := Profinite.presentation.π T
  let s := Stonean.lift (𝟙 T) p
  have hs : s ≫ p = 𝟙 T := Stonean.lift_lifts (𝟙 T) p
  exact stoneanCechTripleToSecondRelation_epi_of_section T s hs

#print axioms stoneanCechTripleBoundary_comp_relation_zero
#print axioms stoneanCechTripleToSecondRelation_comp_ι
#print axioms stoneanCechTripleBoundary_split_contraction
#print axioms stoneanCechTripleToSecondRelation_split
#print axioms stoneanCechTripleToSecondRelation_epi_of_section
#print axioms stoneanCechTripleToSecondRelation_epi_stonean

end CMDG.CondensedCM5R0
