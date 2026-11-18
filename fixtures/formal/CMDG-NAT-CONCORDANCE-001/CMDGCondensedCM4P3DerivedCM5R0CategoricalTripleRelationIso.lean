import CMDGCondensedCM4P3DerivedCM5R0ScalarCechH2ClosedRelation
import CMDGCondensedCM4P3DerivedCM5R0CechTriplePointGeometry

/-!
# CMDG CM5 — genuine categorical triple Čech pullback isomorphism

For any profinite T, identify the actual Profinite categorical Čech
triple of the Stonean presentation P(T) → T with the CLOSED equal-image
triple subspace of P(T)³, as a genuine isomorphism in Profinite.
The two continuous directions preserve all three vertex projections.
Both composites are identities, with explicit nested pullback face
checks; the pair coordinate comparison is also proved.

The type is the actual profinite pullback, not a surrogate or
universe-incorrect substitute. The result is a topological comparison,
not an unconditional Ext² vanishing or derived-solidity theorem.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCechCategoricalPairToExplicit
    (T : Profinite.{u}) :
    C(stoneanPresentationCechPairs T,
      ↥(profiniteCechRelatedSet
        (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T))) := by
  let p := Profinite.presentation.π T
  let f := pullback.fst p p
  let g := pullback.snd p p
  have h (r : stoneanPresentationCechPairs T) :
      p.hom.hom (f.hom.hom r) = p.hom.hom (g.hom.hom r) := by
    have hcond : f ≫ p = g ≫ p := pullback.condition
    exact congrArg (fun m : _ ⟶ T => m.hom.hom r) hcond
  refine ⟨(fun r => ⟨(f.hom.hom r, g.hom.hom r), h r⟩), ?_⟩
  exact (f.hom.hom.continuous.prodMk g.hom.hom.continuous).subtype_mk _

theorem stoneanCechCategoricalPairToExplicit_ofRelated
    (T : Profinite.{u})
    (x y : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y) :
    stoneanCechCategoricalPairToExplicit T
      (stoneanCechPairOfRelated T x y hxy) =
      ⟨(x,y), hxy⟩ := by
  apply Subtype.ext
  apply Prod.ext
  · exact stoneanCechPairOfRelated_fst T x y hxy
  · exact stoneanCechPairOfRelated_snd T x y hxy

/-- Closed triples are a genuine profinite space. -/
noncomputable abbrev stoneanCechExplicitTripleProfinite
    (T : Profinite.{u}) : Profinite.{u} := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  exact Profinite.of (↥(profiniteCechTripleRelatedSet P T p))

/-- Closed triple relation continuously maps into the actual
categorical profinite Čech triple. -/
noncomputable def stoneanCechExplicitTripleToAbstract
    (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ⟶
      stoneanPresentationCechTriples T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  let Q := stoneanCechExplicitTripleProfinite T
  let f : Q ⟶ P := CompHausLike.ofHom _
    (⟨fun z : Q => z.val.1,
      continuous_fst.comp continuous_subtype_val⟩ : C(Q, P))
  let g : Q ⟶ P := CompHausLike.ofHom _
    (⟨fun z : Q => z.val.2.1,
      continuous_fst.comp
        (continuous_snd.comp continuous_subtype_val)⟩ : C(Q, P))
  let h : Q ⟶ P := CompHausLike.ofHom _
    (⟨fun z : Q => z.val.2.2,
      continuous_snd.comp
        (continuous_snd.comp continuous_subtype_val)⟩ : C(Q, P))
  have hfg : f ≫ p = g ≫ p := by
    ext z
    change p.hom.hom z.val.1 = p.hom.hom z.val.2.1
    exact z.property.1
  let fg : Q ⟶ stoneanPresentationCechPairs T :=
    pullback.lift f g hfg
  have hfgh : fg ≫ (pullback.fst p p ≫ p) = h ≫ p := by
    calc
      fg ≫ (pullback.fst p p ≫ p) =
          (fg ≫ pullback.fst p p) ≫ p := (Category.assoc _ _ _).symm
      _ = f ≫ p := by
        change (pullback.lift f g hfg ≫ pullback.fst p p) ≫ p = f ≫ p
        rw [pullback.lift_fst]
      _ = h ≫ p := by
        ext z
        change p.hom.hom z.val.1 = p.hom.hom z.val.2.2
        exact z.property.1.trans z.property.2
  exact pullback.lift fg h hfgh


/-- Triple pullback maps continuously to the actual closed
equal-image triple relation, preserving every vertex projection. -/
noncomputable def stoneanCechCategoricalTripleToExplicit
    (T : Profinite.{u}) :
    C(stoneanPresentationCechTriples T,
      ↥(profiniteCechTripleRelatedSet
        (Stonean.toProfinite.obj T.presentation) T
        (Profinite.presentation.π T))) := by
  let p := Profinite.presentation.π T
  let xy := stoneanCechTripleXY T
  let z := stoneanCechTripleZ T
  let x : stoneanPresentationCechTriples T ⟶
      Stonean.toProfinite.obj T.presentation :=
    xy ≫ pullback.fst p p
  let y : stoneanPresentationCechTriples T ⟶
      Stonean.toProfinite.obj T.presentation :=
    xy ≫ pullback.snd p p
  have hxy : x ≫ p = y ≫ p := by
    change (xy ≫ pullback.fst p p) ≫ p =
      (xy ≫ pullback.snd p p) ≫ p
    simpa only [Category.assoc] using
      congrArg (fun m : stoneanPresentationCechPairs T ⟶ T => xy ≫ m)
        (pullback.condition : pullback.fst p p ≫ p = pullback.snd p p ≫ p)
  have hxz : x ≫ p = z ≫ p := by
    change (xy ≫ pullback.fst p p) ≫ p = z ≫ p
    simpa only [Category.assoc] using
      (pullback.condition : xy ≫ (pullback.fst p p ≫ p) = z ≫ p)
  have hyz : y ≫ p = z ≫ p := by
    exact hxy.symm.trans hxz
  have hh (q : stoneanPresentationCechTriples T) :
      p.hom.hom (x.hom.hom q) = p.hom.hom (y.hom.hom q) ∧
      p.hom.hom (y.hom.hom q) = p.hom.hom (z.hom.hom q) :=
    ⟨congrArg (fun m : _ ⟶ T => m.hom.hom q) hxy,
      congrArg (fun m : _ ⟶ T => m.hom.hom q) hyz⟩
  refine ⟨fun q => ⟨(x.hom.hom q, (y.hom.hom q, z.hom.hom q)), hh q⟩, ?_⟩
  exact (x.hom.hom.continuous.prodMk
    (y.hom.hom.continuous.prodMk z.hom.hom.continuous)).subtype_mk _


private noncomputable def explicitTripleFirst (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun z : stoneanCechExplicitTripleProfinite T => z.val.1,
      continuous_fst.comp continuous_subtype_val⟩ :
      C(stoneanCechExplicitTripleProfinite T, P))

private noncomputable def explicitTripleSecond (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun z : stoneanCechExplicitTripleProfinite T => z.val.2.1,
      continuous_fst.comp (continuous_snd.comp continuous_subtype_val)⟩ :
      C(stoneanCechExplicitTripleProfinite T, P))

private noncomputable def explicitTripleThird (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun z : stoneanCechExplicitTripleProfinite T => z.val.2.2,
      continuous_snd.comp (continuous_snd.comp continuous_subtype_val)⟩ :
      C(stoneanCechExplicitTripleProfinite T, P))

private noncomputable def explicitTriplePair (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ⟶
      stoneanPresentationCechPairs T := by
  let p := Profinite.presentation.π T
  let f := explicitTripleFirst T
  let g := explicitTripleSecond T
  have hfg : f ≫ p = g ≫ p := by
    ext z
    change p.hom.hom z.val.1 = p.hom.hom z.val.2.1
    exact z.property.1
  exact pullback.lift f g hfg

private theorem explicitTriplePair_first (T : Profinite.{u}) :
    explicitTriplePair T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) = explicitTripleFirst T := by
  unfold explicitTriplePair
  exact pullback.lift_fst _ _ _

private theorem explicitTriplePair_second (T : Profinite.{u}) :
    explicitTriplePair T ≫
      pullback.snd (Profinite.presentation.π T)
        (Profinite.presentation.π T) = explicitTripleSecond T := by
  unfold explicitTriplePair
  exact pullback.lift_snd _ _ _


private noncomputable def explicitTripleToAbstractAlt (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ⟶
      stoneanPresentationCechTriples T := by
  let p := Profinite.presentation.π T
  let e := explicitTriplePair T
  let h := explicitTripleThird T
  have he : e ≫ (pullback.fst p p ≫ p) = h ≫ p := by
    rw [← Category.assoc, explicitTriplePair_first]
    ext z
    change p.hom.hom z.val.1 = p.hom.hom z.val.2.2
    exact z.property.1.trans z.property.2
  exact pullback.lift e h he

private theorem explicitTripleToAbstractAlt_eq (T : Profinite.{u}) :
    explicitTripleToAbstractAlt T =
      stoneanCechExplicitTripleToAbstract T := by
  rfl

private theorem explicitTripleToAbstractAlt_xy (T : Profinite.{u}) :
    explicitTripleToAbstractAlt T ≫ stoneanCechTripleXY T =
      explicitTriplePair T := by
  unfold explicitTripleToAbstractAlt
  exact pullback.lift_fst _ _ _

private theorem explicitTripleToAbstractAlt_z (T : Profinite.{u}) :
    explicitTripleToAbstractAlt T ≫ stoneanCechTripleZ T =
      explicitTripleThird T := by
  unfold explicitTripleToAbstractAlt
  exact pullback.lift_snd _ _ _


theorem stoneanCechExplicitTriple_roundtrip
    (T : Profinite.{u})
    (q : stoneanCechExplicitTripleProfinite T) :
    stoneanCechCategoricalTripleToExplicit T
      ((stoneanCechExplicitTripleToAbstract T).hom.hom q) = q := by
  let p := Profinite.presentation.π T
  have hfst :
      (stoneanCechExplicitTripleToAbstract T ≫
        stoneanCechTripleXY T) ≫ pullback.fst p p =
          explicitTripleFirst T := by
    rw [← explicitTripleToAbstractAlt_eq T,
      explicitTripleToAbstractAlt_xy T, explicitTriplePair_first T]
  have hsnd :
      (stoneanCechExplicitTripleToAbstract T ≫
        stoneanCechTripleXY T) ≫ pullback.snd p p =
          explicitTripleSecond T := by
    rw [← explicitTripleToAbstractAlt_eq T,
      explicitTripleToAbstractAlt_xy T, explicitTriplePair_second T]
  have hz :
      stoneanCechExplicitTripleToAbstract T ≫
        stoneanCechTripleZ T = explicitTripleThird T := by
    rw [← explicitTripleToAbstractAlt_eq T,
      explicitTripleToAbstractAlt_z T]
  apply Subtype.ext
  apply Prod.ext
  · change ((stoneanCechExplicitTripleToAbstract T ≫
        stoneanCechTripleXY T ≫ pullback.fst p p).hom.hom q) = q.val.1
    rw [← Category.assoc, hfst]
    rfl
  · apply Prod.ext
    · change ((stoneanCechExplicitTripleToAbstract T ≫
          stoneanCechTripleXY T ≫ pullback.snd p p).hom.hom q) = q.val.2.1
      rw [← Category.assoc, hsnd]
      rfl
    · change ((stoneanCechExplicitTripleToAbstract T ≫
          stoneanCechTripleZ T).hom.hom q) = q.val.2.2
      rw [hz]
      rfl


noncomputable def stoneanCechCategoricalTripleToExplicitProfinite
    (T : Profinite.{u}) :
    stoneanPresentationCechTriples T ⟶
      stoneanCechExplicitTripleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace (↥(profiniteCechTripleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechTripleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (stoneanCechCategoricalTripleToExplicit T)

theorem stoneanCechCategoricalTripleToExplicit_first
    (T : Profinite.{u}) :
    stoneanCechCategoricalTripleToExplicitProfinite T ≫
      explicitTripleFirst T =
    stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) := by
  ext q
  rfl

theorem stoneanCechCategoricalTripleToExplicit_second
    (T : Profinite.{u}) :
    stoneanCechCategoricalTripleToExplicitProfinite T ≫
      explicitTripleSecond T =
    stoneanCechTripleXY T ≫
      pullback.snd (Profinite.presentation.π T)
        (Profinite.presentation.π T) := by
  ext q
  rfl

theorem stoneanCechCategoricalTripleToExplicit_third
    (T : Profinite.{u}) :
    stoneanCechCategoricalTripleToExplicitProfinite T ≫
      explicitTripleThird T =
    stoneanCechTripleZ T := by
  ext q
  rfl


/-- The other round-trip: the actual categorical Čech triple is
recovered from its three continuous vertex values. -/
theorem stoneanCechCategoricalTriple_roundtrip
    (T : Profinite.{u}) :
    stoneanCechCategoricalTripleToExplicitProfinite T ≫
      stoneanCechExplicitTripleToAbstract T =
        𝟙 (stoneanPresentationCechTriples T) := by
  let p := Profinite.presentation.π T
  let A := stoneanCechExplicitTripleToAbstract T
  let B := stoneanCechCategoricalTripleToExplicitProfinite T
  let xy := stoneanCechTripleXY T
  let z := stoneanCechTripleZ T
  have hfst :
      (A ≫ xy) ≫ pullback.fst p p =
        explicitTripleFirst T := by
    rw [show A = explicitTripleToAbstractAlt T from
      (explicitTripleToAbstractAlt_eq T).symm,
      explicitTripleToAbstractAlt_xy T, explicitTriplePair_first T]
  have hsnd :
      (A ≫ xy) ≫ pullback.snd p p =
        explicitTripleSecond T := by
    rw [show A = explicitTripleToAbstractAlt T from
      (explicitTripleToAbstractAlt_eq T).symm,
      explicitTripleToAbstractAlt_xy T, explicitTriplePair_second T]
  have hz :
      A ≫ z = explicitTripleThird T := by
    rw [show A = explicitTripleToAbstractAlt T from
      (explicitTripleToAbstractAlt_eq T).symm,
      explicitTripleToAbstractAlt_z T]
  have hxy : (B ≫ A) ≫ xy = xy := by
    apply pullback.hom_ext
    · calc
        ((B ≫ A) ≫ xy) ≫ pullback.fst p p =
            B ≫ ((A ≫ xy) ≫ pullback.fst p p) := by
              simp only [Category.assoc]
        _ = B ≫ explicitTripleFirst T := by rw [hfst]
        _ = xy ≫ pullback.fst p p :=
          stoneanCechCategoricalTripleToExplicit_first T
    · calc
        ((B ≫ A) ≫ xy) ≫ pullback.snd p p =
            B ≫ ((A ≫ xy) ≫ pullback.snd p p) := by
              simp only [Category.assoc]
        _ = B ≫ explicitTripleSecond T := by rw [hsnd]
        _ = xy ≫ pullback.snd p p :=
          stoneanCechCategoricalTripleToExplicit_second T
  have hz' : (B ≫ A) ≫ z = z := by
    calc
      (B ≫ A) ≫ z = B ≫ (A ≫ z) := Category.assoc _ _ _
      _ = B ≫ explicitTripleThird T := by rw [hz]
      _ = z := stoneanCechCategoricalTripleToExplicit_third T
  change B ≫ A = 𝟙 _
  apply pullback.hom_ext
  · simpa only [Category.id_comp] using hxy
  · simpa only [Category.id_comp] using hz'


/-- The genuine Profinite Čech triple pullback is isomorphic to
the closed subspace of P³ consisting of equal-image triples. -/
noncomputable def stoneanCechExplicitTripleIso (T : Profinite.{u}) :
    stoneanCechExplicitTripleProfinite T ≅
      stoneanPresentationCechTriples T where
  hom := stoneanCechExplicitTripleToAbstract T
  inv := stoneanCechCategoricalTripleToExplicitProfinite T
  hom_inv_id := by
    apply ConcreteCategory.hom_ext
    intro q
    exact stoneanCechExplicitTriple_roundtrip T q
  inv_hom_id := stoneanCechCategoricalTriple_roundtrip T

#check stoneanCechCategoricalPairToExplicit
#check stoneanCechExplicitTripleToAbstract
#print axioms stoneanCechCategoricalPairToExplicit_ofRelated
#print axioms stoneanCechExplicitTripleToAbstract
#print axioms stoneanCechCategoricalTripleToExplicit
#print axioms explicitTriplePair_first
#print axioms explicitTripleToAbstractAlt_eq
#print axioms explicitTripleToAbstractAlt_xy
#print axioms stoneanCechExplicitTriple_roundtrip
#print axioms stoneanCechCategoricalTripleToExplicit_first
#print axioms stoneanCechCategoricalTriple_roundtrip
#print axioms stoneanCechExplicitTripleIso

end CMDG.CondensedCM5R0
