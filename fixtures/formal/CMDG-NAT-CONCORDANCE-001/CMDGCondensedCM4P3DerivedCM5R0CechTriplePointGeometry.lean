import CMDGCondensedCM4P3DerivedCM5R0StoneanCechTripleCocycle
import CMDGCondensedCM4P3DerivedCM5R0StoneanScalarCechPrimitive

/-!
# CM5: exact point geometry of the canonical Stonean Čech triple

The preceding categorical cocycle theorem is an equality of genuine
condensed-module morphisms on the triple pullback.  This file connects
that categorical triple to arbitrary specified equal-image points of
the canonical Stonean source.  In particular it does not assume
the projection P(T) → T has a continuous section.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

private noncomputable def singletonProfinitePointMap
    (X : Profinite.{u}) (x : X) :
    Profinite.of PUnit.{u + 1} ⟶ X :=
  ConcreteCategory.ofHom ⟨fun _ => x, continuous_const⟩

private theorem singletonProfinitePointMap_apply
    (X : Profinite.{u}) (x : X) :
    (singletonProfinitePointMap X x).hom.hom PUnit.unit = x := rfl

/-- The abstract Stonean Čech pair's first endpoint really is
the supplied first point. -/
theorem stoneanCechPairOfRelated_fst
    (T : Profinite.{u})
    (x y : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y) :
    (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
        (stoneanCechPairOfRelated T x y hxy) = x := by
  change (stoneanCechExplicitToAbstract T ≫
    pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom ⟨(x, y), hxy⟩ = x
  let P := Stonean.toProfinite.obj T.presentation
  let f : stoneanCechRelatedProfinite T ⟶ P :=
    CompHausLike.ofHom _
      (⟨(fun z : stoneanCechRelatedProfinite T => z.val.1),
        continuous_fst.comp continuous_subtype_val⟩ :
        C(stoneanCechRelatedProfinite T, P))
  have hmap :
      stoneanCechExplicitToAbstract T ≫
        pullback.fst (Profinite.presentation.π T)
          (Profinite.presentation.π T) = f := by
    unfold stoneanCechExplicitToAbstract
    exact pullback.lift_fst _ _ _
  have hh := congrArg
    (fun m : stoneanCechRelatedProfinite T ⟶ P =>
      m.hom.hom ⟨(x, y), hxy⟩) hmap
  exact hh

/-- The second endpoint of the actual categorical pair. -/
theorem stoneanCechPairOfRelated_snd
    (T : Profinite.{u})
    (x y : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y) :
    (pullback.snd (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
        (stoneanCechPairOfRelated T x y hxy) = y := by
  change (stoneanCechExplicitToAbstract T ≫
    pullback.snd (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom ⟨(x, y), hxy⟩ = y
  let P := Stonean.toProfinite.obj T.presentation
  let g : stoneanCechRelatedProfinite T ⟶ P :=
    CompHausLike.ofHom _
      (⟨(fun z : stoneanCechRelatedProfinite T => z.val.2),
        continuous_snd.comp continuous_subtype_val⟩ :
        C(stoneanCechRelatedProfinite T, P))
  have hmap :
      stoneanCechExplicitToAbstract T ≫
        pullback.snd (Profinite.presentation.π T)
          (Profinite.presentation.π T) = g := by
    unfold stoneanCechExplicitToAbstract
    exact pullback.lift_snd _ _ _
  have hh := congrArg
    (fun m : stoneanCechRelatedProfinite T ⟶ P =>
      m.hom.hom ⟨(x, y), hxy⟩) hmap
  exact hh

/-- Points in a categorical profinite pair pullback are determined
by their two endpoint values. -/
theorem stoneanCechPair_eq_of_endpoints
    (T : Profinite.{u})
    (a b : stoneanPresentationCechPairs T)
    (hfst : (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom a =
      (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom b)
    (hsnd : (pullback.snd (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom a =
      (pullback.snd (Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom b) : a = b := by
  let pa := singletonProfinitePointMap (stoneanPresentationCechPairs T) a
  let pb := singletonProfinitePointMap (stoneanPresentationCechPairs T) b
  have ha : pa ≫ pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) =
      pb ≫ pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) := by
    ext s
    exact hfst
  have hb : pa ≫ pullback.snd (Profinite.presentation.π T)
        (Profinite.presentation.π T) =
      pb ≫ pullback.snd (Profinite.presentation.π T)
        (Profinite.presentation.π T) := by
    ext s
    exact hsnd
  have h : pa = pb := pullback.hom_ext ha hb
  have hh := congrArg
    (fun m : Profinite.of PUnit.{u + 1} ⟶
      stoneanPresentationCechPairs T => m.hom.hom PUnit.unit) h
  exact hh

/-- Assemble any three Stonean points with equal base images into
one *actual* point of the categorical Stonean triple pullback. -/
noncomputable def stoneanCechTripleOfRelated
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    stoneanPresentationCechTriples T := by
  let p := Profinite.presentation.π T
  let xy := stoneanCechPairOfRelated T x y hxy
  let a := singletonProfinitePointMap (stoneanPresentationCechPairs T) xy
  let b := singletonProfinitePointMap (Stonean.toProfinite.obj T.presentation) z
  have h : a ≫ (pullback.fst p p ≫ p) = b ≫ p := by
    ext s
    change p.hom.hom ((pullback.fst p p).hom.hom xy) = p.hom.hom z
    rw [stoneanCechPairOfRelated_fst]
    exact hxy.trans hyz
  exact (pullback.lift a b h).hom.hom PUnit.unit

theorem stoneanCechTripleOfRelated_xy
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (stoneanCechTripleXY T).hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz) =
        stoneanCechPairOfRelated T x y hxy := by
  let p := Profinite.presentation.π T
  let xy := stoneanCechPairOfRelated T x y hxy
  let a := singletonProfinitePointMap (stoneanPresentationCechPairs T) xy
  let b := singletonProfinitePointMap (Stonean.toProfinite.obj T.presentation) z
  have h : a ≫ (pullback.fst p p ≫ p) = b ≫ p := by
    ext s
    change p.hom.hom ((pullback.fst p p).hom.hom xy) = p.hom.hom z
    rw [stoneanCechPairOfRelated_fst]
    exact hxy.trans hyz
  have hmap : pullback.lift a b h ≫ stoneanCechTripleXY T = a :=
    pullback.lift_fst _ _ _
  have hh := congrArg
    (fun m : Profinite.of PUnit.{u + 1} ⟶
      stoneanPresentationCechPairs T => m.hom.hom PUnit.unit) hmap
  exact hh

theorem stoneanCechTripleOfRelated_z
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (stoneanCechTripleZ T).hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz) = z := by
  let p := Profinite.presentation.π T
  let xy := stoneanCechPairOfRelated T x y hxy
  let a := singletonProfinitePointMap (stoneanPresentationCechPairs T) xy
  let b := singletonProfinitePointMap (Stonean.toProfinite.obj T.presentation) z
  have h : a ≫ (pullback.fst p p ≫ p) = b ≫ p := by
    ext s
    change p.hom.hom ((pullback.fst p p).hom.hom xy) = p.hom.hom z
    rw [stoneanCechPairOfRelated_fst]
    exact hxy.trans hyz
  have hmap : pullback.lift a b h ≫ stoneanCechTripleZ T = b :=
    pullback.lift_snd _ _ _
  have hh := congrArg
    (fun m : Profinite.of PUnit.{u + 1} ⟶
      Stonean.toProfinite.obj T.presentation => m.hom.hom PUnit.unit) hmap
  exact hh

/-- The categorical triple's XZ projection on any specified
fiber-related triple is exactly the canonical (x,z) pair. -/
theorem stoneanCechTripleOfRelated_xz
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (stoneanCechTripleXZ T).hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz) =
      stoneanCechPairOfRelated T x z (hxy.trans hyz) := by
  let p := Profinite.presentation.π T
  let t := stoneanCechTripleOfRelated T x y z hxy hyz
  apply stoneanCechPair_eq_of_endpoints T
  · have h := congrArg (fun m : stoneanPresentationCechTriples T ⟶
        Stonean.toProfinite.obj T.presentation => m.hom.hom t)
        (pullback.lift_fst
          (stoneanCechTripleXY T ≫ pullback.fst p p)
          (stoneanCechTripleZ T)
          (show (stoneanCechTripleXY T ≫ pullback.fst p p) ≫ p =
            stoneanCechTripleZ T ≫ p from by
              simpa only [Category.assoc] using
                (pullback.condition : stoneanCechTripleXY T ≫
                  (pullback.fst p p ≫ p) = stoneanCechTripleZ T ≫ p)))
    change (pullback.fst p p).hom.hom ((stoneanCechTripleXZ T).hom.hom t) =
      (pullback.fst p p).hom.hom ((stoneanCechTripleXY T).hom.hom t) at h
    rw [stoneanCechTripleOfRelated_xy, stoneanCechPairOfRelated_fst] at h
    rw [h, stoneanCechPairOfRelated_fst]
  · have h := congrArg (fun m : stoneanPresentationCechTriples T ⟶
        Stonean.toProfinite.obj T.presentation => m.hom.hom t)
        (pullback.lift_snd
          (stoneanCechTripleXY T ≫ pullback.fst p p)
          (stoneanCechTripleZ T)
          (show (stoneanCechTripleXY T ≫ pullback.fst p p) ≫ p =
            stoneanCechTripleZ T ≫ p from by
              simpa only [Category.assoc] using
                (pullback.condition : stoneanCechTripleXY T ≫
                  (pullback.fst p p ≫ p) = stoneanCechTripleZ T ≫ p)))
    change (pullback.snd p p).hom.hom ((stoneanCechTripleXZ T).hom.hom t) =
      (stoneanCechTripleZ T).hom.hom t at h
    rw [stoneanCechTripleOfRelated_z] at h
    rw [h, stoneanCechPairOfRelated_snd]

/-- The categorical triple's YZ projection gives the actual (y,z) pair. -/
theorem stoneanCechTripleOfRelated_yz
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (stoneanCechTripleYZ T).hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz) =
      stoneanCechPairOfRelated T y z hyz := by
  let p := Profinite.presentation.π T
  let t := stoneanCechTripleOfRelated T x y z hxy hyz
  apply stoneanCechPair_eq_of_endpoints T
  · have h := congrArg (fun m : stoneanPresentationCechTriples T ⟶
        Stonean.toProfinite.obj T.presentation => m.hom.hom t)
        (pullback.lift_fst
          (stoneanCechTripleXY T ≫ pullback.snd p p)
          (stoneanCechTripleZ T)
          (show (stoneanCechTripleXY T ≫ pullback.snd p p) ≫ p =
            stoneanCechTripleZ T ≫ p from by
              calc
                (stoneanCechTripleXY T ≫ pullback.snd p p) ≫ p =
                  stoneanCechTripleXY T ≫ (pullback.snd p p ≫ p) :=
                  Category.assoc _ _ _
                _ = stoneanCechTripleXY T ≫ (pullback.fst p p ≫ p) := by
                  rw [← pullback.condition]
                _ = stoneanCechTripleZ T ≫ p := pullback.condition))
    change (pullback.fst p p).hom.hom ((stoneanCechTripleYZ T).hom.hom t) =
      (pullback.snd p p).hom.hom ((stoneanCechTripleXY T).hom.hom t) at h
    rw [stoneanCechTripleOfRelated_xy, stoneanCechPairOfRelated_snd] at h
    rw [h, stoneanCechPairOfRelated_fst]
  · have h := congrArg (fun m : stoneanPresentationCechTriples T ⟶
        Stonean.toProfinite.obj T.presentation => m.hom.hom t)
        (pullback.lift_snd
          (stoneanCechTripleXY T ≫ pullback.snd p p)
          (stoneanCechTripleZ T)
          (show (stoneanCechTripleXY T ≫ pullback.snd p p) ≫ p =
            stoneanCechTripleZ T ≫ p from by
              calc
                (stoneanCechTripleXY T ≫ pullback.snd p p) ≫ p =
                  stoneanCechTripleXY T ≫ (pullback.snd p p ≫ p) :=
                  Category.assoc _ _ _
                _ = stoneanCechTripleXY T ≫ (pullback.fst p p ≫ p) := by
                  rw [← pullback.condition]
                _ = stoneanCechTripleZ T ≫ p := pullback.condition))
    change (pullback.snd p p).hom.hom ((stoneanCechTripleYZ T).hom.hom t) =
      (stoneanCechTripleZ T).hom.hom t at h
    rw [stoneanCechTripleOfRelated_z] at h
    rw [h, stoneanCechPairOfRelated_snd]

#print axioms stoneanCechPairOfRelated_fst
#print axioms stoneanCechPairOfRelated_snd
#print axioms stoneanCechPair_eq_of_endpoints
#print axioms stoneanCechTripleOfRelated_xy
#print axioms stoneanCechTripleOfRelated_z
#print axioms stoneanCechTripleOfRelated_xz
#print axioms stoneanCechTripleOfRelated_yz

end CMDG.CondensedCM5R0
