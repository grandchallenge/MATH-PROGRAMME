import CMDGCondensedCM4P3DerivedCM5R0ExplicitClosedProductH3HomBridge
import CMDGCondensedCM4P3DerivedCM5R0GenuineFourthCechBoundary
import CMDGCondensedCM4P3DerivedCM5R0CategoricalScalarH2Potential

/-!
# CMDG CM5 — genuine fourth Čech pullback equals the closed equal-image quadruple space

For arbitrary profinite T, compare the actual iterated Profinite
pullback P(T)×_T P(T)×_T P(T)×_T P(T) with the genuine closed subset
of P(T)^4 defined by adjacent equal-image conditions. The forward
map is built from the explicit triple comparison and fourth projection
via the true pullback universal property. The reverse map is the
continuous ordered four-vertex tuple from the true categorical object.
Both composites equal the corresponding identities. The resulting
isomorphism has the actual categorical pullback as its target, not a
surrogate set with mismatched universes.

Full four-face and free-module boundary naturality, scalar/product
cocycle transport, and Ext³ vanishing are separate obligations.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

private noncomputable def explicitQuadrupleToTriple (T : Profinite.{u}) :
    stoneanCechExplicitQuadrupleProfinite T ⟶
      stoneanCechExplicitTripleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  let Q := stoneanCechExplicitQuadrupleProfinite T
  letI : CompactSpace
      (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  let toTriple : C(Q, ↥(profiniteCechTripleRelatedSet P T p)) := by
    refine ⟨fun q => ⟨(q.val.1,(q.val.2.1,q.val.2.2.1)),
      ⟨q.property.1,q.property.2.1⟩⟩, ?_⟩
    apply Continuous.subtype_mk
    exact (continuous_fst.comp continuous_subtype_val).prodMk
      ((continuous_fst.comp (continuous_snd.comp continuous_subtype_val)).prodMk
        (continuous_fst.comp
          (continuous_snd.comp (continuous_snd.comp continuous_subtype_val))))
  exact CompHausLike.ofHom _ toTriple

private noncomputable def explicitQuadrupleFourth (T : Profinite.{u}) :
    stoneanCechExplicitQuadrupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  let Q := stoneanCechExplicitQuadrupleProfinite T
  exact CompHausLike.ofHom _ (⟨fun q : Q => q.val.2.2.2,
    continuous_snd.comp (continuous_snd.comp
      (continuous_snd.comp continuous_subtype_val))⟩ : C(Q, _))

/-- Actual equal-image closed quadruple maps to the fourth iterated
categorical pullback by the universal property. -/
noncomputable def stoneanCechExplicitQuadrupleToAbstract
    (T : Profinite.{u}) :
    stoneanCechExplicitQuadrupleProfinite T ⟶
      stoneanPresentationCechQuadruples T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  let q := explicitQuadrupleToTriple T ≫
    stoneanCechExplicitTripleToAbstract T
  let w := explicitQuadrupleFourth T
  have h : q ≫ (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) =
      w ≫ p := by
    ext z
    let x := z.val.1
    let y := z.val.2.1
    let t := z.val.2.2.1
    have hxyz := stoneanCechExplicitTripleToAbstract_ofRelated
      T x y t z.property.1 z.property.2.1
    dsimp only [q, w]
    simp only [CategoryTheory.comp_apply]
    have hw : (explicitQuadrupleFourth T).hom.hom z =
        z.val.2.2.2 := by
      unfold explicitQuadrupleFourth
      rfl
    change p.hom.hom
      ((pullback.fst p p).hom.hom
        ((stoneanCechTripleXY T).hom.hom
          ((stoneanCechExplicitTripleToAbstract T).hom.hom
            ((explicitQuadrupleToTriple T).hom.hom z)))) =
      p.hom.hom ((explicitQuadrupleFourth T).hom.hom z)
    rw [hw]
    have hq : (explicitQuadrupleToTriple T).hom.hom z =
        (⟨(x,(y,t)),⟨z.property.1,z.property.2.1⟩⟩ :
          stoneanCechExplicitTripleProfinite T) := by
      unfold explicitQuadrupleToTriple
      rfl
    rw [hq, hxyz]
    rw [stoneanCechTripleOfRelated_xy,
      stoneanCechPairOfRelated_fst]
    exact z.property.1.trans
      (z.property.2.1.trans z.property.2.2)
  exact pullback.lift q w h


/-- True fourth categorical pullback maps to the explicit compact
closed relation, with its four ordered vertex coordinates. -/
noncomputable def stoneanCechCategoricalQuadrupleToExplicit
    (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
      stoneanCechExplicitQuadrupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let Q := stoneanPresentationCechQuadruples T
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  let q : Q ⟶ stoneanPresentationCechTriples T :=
    pullback.fst
      (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  let w : Q ⟶ P :=
    pullback.snd
      (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  let h : q ≫ (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) =
      w ≫ p := pullback.condition
  let triple : Q ⟶ stoneanCechExplicitTripleProfinite T :=
    q ≫ stoneanCechCategoricalTripleToExplicitProfinite T
  have hh (z : Q) :
      p.hom.hom ((triple.hom.hom z).val.2.2) =
        p.hom.hom (w.hom.hom z) := by
    have he := congrArg (fun f : Q ⟶ T => f.hom.hom z) h
    change p.hom.hom
      ((pullback.fst p p).hom.hom
        ((stoneanCechTripleXY T).hom.hom (q.hom.hom z))) =
      p.hom.hom (w.hom.hom z) at he
    have hz := stoneanCechCategoricalTripleToExplicit_third T
    have heq : (stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom
        (q.hom.hom z) =
        (triple.hom.hom z) := by
      exact (CategoryTheory.comp_apply q
        (stoneanCechCategoricalTripleToExplicitProfinite T) z).symm
    have hz3 := congrArg
      (fun f : stoneanPresentationCechTriples T ⟶ P =>
        f.hom.hom (q.hom.hom z)) hz
    have hxy : p.hom.hom ((triple.hom.hom z).val.1) =
        p.hom.hom ((triple.hom.hom z).val.2.2) :=
      (triple.hom.hom z).property.1.trans
        (triple.hom.hom z).property.2
    have hfirst : (triple.hom.hom z).val.1 =
      (pullback.fst p p).hom.hom
        ((stoneanCechTripleXY T).hom.hom (q.hom.hom z)) := by
      have hf := stoneanCechCategoricalTripleToExplicit_first T
      have hf' := congrArg
        (fun f : stoneanPresentationCechTriples T ⟶ P =>
          f.hom.hom (q.hom.hom z)) hf
      change ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom
          (q.hom.hom z)).val.1 =
        (pullback.fst p p).hom.hom
          ((stoneanCechTripleXY T).hom.hom (q.hom.hom z)) at hf'
      rw [heq] at hf'
      exact hf'
    exact (hxy.symm.trans (congrArg p.hom.hom hfirst)).trans he
  let toQuad : C(Q, ↥(profiniteCechQuadrupleRelatedSet P T p)) := by
    refine ⟨fun z => ⟨((triple.hom.hom z).val.1,
      ((triple.hom.hom z).val.2.1,
      ((triple.hom.hom z).val.2.2, w.hom.hom z))),
      ⟨(triple.hom.hom z).property.1,
        (triple.hom.hom z).property.2, hh z⟩⟩, ?_⟩
    apply Continuous.subtype_mk
    exact (((continuous_fst.comp continuous_subtype_val).comp
      triple.hom.hom.continuous).prodMk
      ((((continuous_fst.comp
        (continuous_snd.comp continuous_subtype_val)).comp
          triple.hom.hom.continuous)).prodMk
      ((((continuous_snd.comp
        (continuous_snd.comp continuous_subtype_val)).comp
          triple.hom.hom.continuous)).prodMk
          w.hom.hom.continuous)))
  exact CompHausLike.ofHom _ toQuad


theorem stoneanCechExplicitQuadruple_roundtrip
    (T : Profinite.{u}) :
    stoneanCechExplicitQuadrupleToAbstract T ≫
      stoneanCechCategoricalQuadrupleToExplicit T =
        𝟙 (stoneanCechExplicitQuadrupleProfinite T) := by
  let p := Profinite.presentation.π T
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let B := stoneanCechCategoricalQuadrupleToExplicit T
  let E := explicitQuadrupleToTriple T
  let W := explicitQuadrupleFourth T
  let Q := stoneanPresentationCechQuadruples T
  let fst : Q ⟶ stoneanPresentationCechTriples T :=
    pullback.fst (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  let snd : Q ⟶ Stonean.toProfinite.obj T.presentation :=
    pullback.snd (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  have hfst : A ≫ fst =
      E ≫ stoneanCechExplicitTripleToAbstract T := by
    change (pullback.lift (E ≫ stoneanCechExplicitTripleToAbstract T)
      W _) ≫ fst = _
    exact pullback.lift_fst _ _ _
  have hsnd : A ≫ snd = W := by
    change (pullback.lift (E ≫ stoneanCechExplicitTripleToAbstract T)
      W _) ≫ snd = W
    exact pullback.lift_snd _ _ _
  have htriple : (A ≫ fst) ≫
      stoneanCechCategoricalTripleToExplicitProfinite T = E := by
    rw [hfst, Category.assoc]
    have hiso := (stoneanCechExplicitTripleIso T).hom_inv_id
    change stoneanCechExplicitTripleToAbstract T ≫
      stoneanCechCategoricalTripleToExplicitProfinite T =
      𝟙 (stoneanCechExplicitTripleProfinite T) at hiso
    rw [hiso, Category.comp_id]
  apply ConcreteCategory.hom_ext
  intro z
  apply Subtype.ext
  simp only [CategoryTheory.comp_apply, CategoryTheory.id_apply]
  change ((B.hom.hom (A.hom.hom z)).val) = z.val
  let tp := fst ≫ stoneanCechCategoricalTripleToExplicitProfinite T
  have htp := congrArg
    (fun k : stoneanCechExplicitQuadrupleProfinite T ⟶
      stoneanCechExplicitTripleProfinite T => k.hom.hom z) htriple
  change (tp.hom.hom (A.hom.hom z)) = E.hom.hom z at htp
  have hw := congrArg
    (fun k : stoneanCechExplicitQuadrupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation => k.hom.hom z) hsnd
  change snd.hom.hom (A.hom.hom z) = W.hom.hom z at hw
  change ((tp.hom.hom (A.hom.hom z)).val.1,
      ((tp.hom.hom (A.hom.hom z)).val.2.1,
       ((tp.hom.hom (A.hom.hom z)).val.2.2,
        snd.hom.hom (A.hom.hom z)))) = z.val
  rw [htp, hw]
  have hE : E.hom.hom z =
      (⟨(z.val.1,(z.val.2.1,z.val.2.2.1)),
        ⟨z.property.1,z.property.2.1⟩⟩ :
          stoneanCechExplicitTripleProfinite T) := by
    unfold E explicitQuadrupleToTriple
    rfl
  have hW : W.hom.hom z = z.val.2.2.2 := by
    unfold W explicitQuadrupleFourth
    rfl
  rw [hE, hW]


theorem stoneanCechCategoricalQuadruple_roundtrip
    (T : Profinite.{u}) :
    stoneanCechCategoricalQuadrupleToExplicit T ≫
      stoneanCechExplicitQuadrupleToAbstract T =
        𝟙 (stoneanPresentationCechQuadruples T) := by
  let p := Profinite.presentation.π T
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let B := stoneanCechCategoricalQuadrupleToExplicit T
  let E := explicitQuadrupleToTriple T
  let W := explicitQuadrupleFourth T
  let Q := stoneanPresentationCechQuadruples T
  let fst : Q ⟶ stoneanPresentationCechTriples T :=
    pullback.fst (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  let snd : Q ⟶ Stonean.toProfinite.obj T.presentation :=
    pullback.snd (stoneanCechTripleXY T ≫ pullback.fst p p ≫ p) p
  have hfst : A ≫ fst = E ≫ stoneanCechExplicitTripleToAbstract T := by
    change (pullback.lift (E ≫ stoneanCechExplicitTripleToAbstract T)
      W _) ≫ fst = _
    exact pullback.lift_fst _ _ _
  have hsnd : A ≫ snd = W := by
    change (pullback.lift (E ≫ stoneanCechExplicitTripleToAbstract T)
      W _) ≫ snd = W
    exact pullback.lift_snd _ _ _
  have he : B ≫ E =
      fst ≫ stoneanCechCategoricalTripleToExplicitProfinite T := by
    apply ConcreteCategory.hom_ext
    intro z
    apply Subtype.ext
    change ((E.hom.hom (B.hom.hom z)).val) =
      ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom
        (fst.hom.hom z)).val
    unfold E B explicitQuadrupleToTriple
      stoneanCechCategoricalQuadrupleToExplicit
    rfl
  have hw : B ≫ W = snd := by
    apply ConcreteCategory.hom_ext
    intro z
    change W.hom.hom (B.hom.hom z) = snd.hom.hom z
    unfold W B explicitQuadrupleFourth
      stoneanCechCategoricalQuadrupleToExplicit
    rfl
  apply pullback.hom_ext
  · change (B ≫ A) ≫ fst = (𝟙 Q) ≫ fst
    calc
      (B ≫ A) ≫ fst = B ≫ (A ≫ fst) := Category.assoc _ _ _
      _ = B ≫ (E ≫ stoneanCechExplicitTripleToAbstract T) := by rw [hfst]
      _ = (B ≫ E) ≫ stoneanCechExplicitTripleToAbstract T :=
        (Category.assoc _ _ _).symm
      _ = (fst ≫ stoneanCechCategoricalTripleToExplicitProfinite T) ≫
          stoneanCechExplicitTripleToAbstract T := by rw [he]
      _ = fst ≫ (stoneanCechCategoricalTripleToExplicitProfinite T ≫
          stoneanCechExplicitTripleToAbstract T) := Category.assoc _ _ _
      _ = fst ≫ 𝟙 _ := by
        have hi := (stoneanCechExplicitTripleIso T).inv_hom_id
        change stoneanCechCategoricalTripleToExplicitProfinite T ≫
          stoneanCechExplicitTripleToAbstract T =
          𝟙 (stoneanPresentationCechTriples T) at hi
        rw [hi]
      _ = (𝟙 Q) ≫ fst := by simp
  · change (B ≫ A) ≫ snd = (𝟙 Q) ≫ snd
    calc
      (B ≫ A) ≫ snd = B ≫ (A ≫ snd) := Category.assoc _ _ _
      _ = B ≫ W := by rw [hsnd]
      _ = (𝟙 Q) ≫ snd := by simpa using hw

noncomputable def stoneanCechExplicitQuadrupleIso (T : Profinite.{u}) :
    stoneanCechExplicitQuadrupleProfinite T ≅
      stoneanPresentationCechQuadruples T where
  hom := stoneanCechExplicitQuadrupleToAbstract T
  inv := stoneanCechCategoricalQuadrupleToExplicit T
  hom_inv_id := stoneanCechExplicitQuadruple_roundtrip T
  inv_hom_id := stoneanCechCategoricalQuadruple_roundtrip T

#print axioms stoneanCechExplicitQuadrupleIso
#print axioms stoneanCechCategoricalQuadrupleToExplicit
#print axioms stoneanCechExplicitQuadrupleToAbstract
end CMDG.CondensedCM5R0
