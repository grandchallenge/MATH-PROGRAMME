import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeYonedabar
import CMDGCondensedCM4P3DerivedCM5R0CechPresheafFaceComparison
import Mathlib.CategoryTheory.Limits.Preserves.Shapes.Pullbacks

/-!
# CMDG CM5 — genuine profinite Čech pullbacks on the CompHaus site

For an arbitrary profinite span A → C ← B, the fully faithful
profinite-to-CompHaus inclusion creates limits. Consequently the
CompHaus Hom set of the ACTUAL profinite pullback is canonically
equivalent to the set of compatible pairs of CompHaus morphisms.
This is the missing representable, pointwise pullback comparison.

Specializing to p:P(T) → T first identifies the original Čech pair
R=P×_T P. Specializing again to R → T ← P identifies the actual
triple Q=R×_T P. The projection equations are proved using the
categorical pullback comparison, not an unstated assumption of
definitional equality of the two pullback objects.

Remaining follow-on: transport the free-module differentials,
including the three signed degree-two faces, through these
equivalences to prove actual Stonean restricted-presheaf exactness.
Neither global second-relation epi nor Ext² vanishing is asserted.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Hom into an ACTUAL profinite pullback is exactly the
compatible-pair Hom set on the genuine CompHaus site. -/
noncomputable def compHausHomProfinitePullbackEquiv
    (U : CompHaus.{u}) {A B C : Profinite.{u}}
    (f : A ⟶ C) (g : B ⟶ C) :
    (U ⟶ profiniteToCompHaus.obj (pullback f g)) ≃
      {xy : (U ⟶ profiniteToCompHaus.obj A) ×
          (U ⟶ profiniteToCompHaus.obj B) //
        xy.1 ≫ profiniteToCompHaus.map f =
          xy.2 ≫ profiniteToCompHaus.map g} := by
  let F := profiniteToCompHaus
  let e : F.obj (pullback f g) ≅
      pullback (F.map f) (F.map g) :=
    PreservesPullback.iso F f g
  have he_fst :
      e.hom ≫ pullback.fst (F.map f) (F.map g) =
        F.map (pullback.fst f g) :=
    PreservesPullback.iso_hom_fst F f g
  have he_snd :
      e.hom ≫ pullback.snd (F.map f) (F.map g) =
        F.map (pullback.snd f g) :=
    PreservesPullback.iso_hom_snd F f g
  have he_inv_fst :
      e.inv ≫ F.map (pullback.fst f g) =
        pullback.fst (F.map f) (F.map g) :=
    PreservesPullback.iso_inv_fst F f g
  have he_inv_snd :
      e.inv ≫ F.map (pullback.snd f g) =
        pullback.snd (F.map f) (F.map g) :=
    PreservesPullback.iso_inv_snd F f g
  refine {
    toFun := fun z => ⟨⟨z ≫ F.map (pullback.fst f g),
      z ≫ F.map (pullback.snd f g)⟩, ?_⟩
    invFun := fun xy =>
      pullback.lift xy.1.1 xy.1.2 xy.2 ≫ e.inv
    left_inv := ?_
    right_inv := ?_
  }
  · have h := (pullback.condition :
        pullback.fst f g ≫ f = pullback.snd f g ≫ g)
    exact (by simpa only [Functor.map_comp, Category.assoc]
      using congrArg (fun a => z ≫ F.map a) h)
  · intro z
    apply (cancel_mono e.hom).1
    rw [Category.assoc, e.inv_hom_id, Category.comp_id]
    apply pullback.hom_ext
    · calc
        z ≫ F.map (pullback.fst f g) =
            z ≫ (e.hom ≫ pullback.fst (F.map f) (F.map g)) :=
          congrArg (fun k => z ≫ k) he_fst.symm
        _ = (z ≫ e.hom) ≫ pullback.fst (F.map f) (F.map g) :=
          (Category.assoc _ _ _).symm
    · calc
        z ≫ F.map (pullback.snd f g) =
            z ≫ (e.hom ≫ pullback.snd (F.map f) (F.map g)) :=
          congrArg (fun k => z ≫ k) he_snd.symm
        _ = (z ≫ e.hom) ≫ pullback.snd (F.map f) (F.map g) :=
          (Category.assoc _ _ _).symm
  · intro xy
    apply Subtype.ext
    apply Prod.ext
    · calc
        (pullback.lift xy.1.1 xy.1.2 xy.2 ≫ e.inv) ≫
            F.map (pullback.fst f g) =
          pullback.lift xy.1.1 xy.1.2 xy.2 ≫
            (e.inv ≫ F.map (pullback.fst f g)) :=
          Category.assoc _ _ _
        _ = pullback.lift xy.1.1 xy.1.2 xy.2 ≫
            pullback.fst (F.map f) (F.map g) :=
          congrArg (fun k => pullback.lift xy.1.1 xy.1.2 xy.2 ≫ k) he_inv_fst
        _ = xy.1.1 := pullback.lift_fst _ _ _
    · calc
        (pullback.lift xy.1.1 xy.1.2 xy.2 ≫ e.inv) ≫
            F.map (pullback.snd f g) =
          pullback.lift xy.1.1 xy.1.2 xy.2 ≫
            (e.inv ≫ F.map (pullback.snd f g)) :=
          Category.assoc _ _ _
        _ = pullback.lift xy.1.1 xy.1.2 xy.2 ≫
            pullback.snd (F.map f) (F.map g) :=
          congrArg (fun k => pullback.lift xy.1.1 xy.1.2 xy.2 ≫ k) he_inv_snd
        _ = xy.1.2 := pullback.lift_snd _ _ _

/-- Honest pair object R=P×_T P in CompHaus-site Hom coordinates. -/
noncomputable abbrev stoneanCompHausProbeCechPairEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechPairs T)) ≃
      {xy : (U.compHaus ⟶ profiniteToCompHaus.obj
          (Stonean.toProfinite.obj T.presentation)) ×
          (U.compHaus ⟶ profiniteToCompHaus.obj
          (Stonean.toProfinite.obj T.presentation)) //
        xy.1 ≫ profiniteToCompHaus.map (Profinite.presentation.π T) =
          xy.2 ≫ profiniteToCompHaus.map (Profinite.presentation.π T)} :=
  compHausHomProfinitePullbackEquiv U.compHaus
    (Profinite.presentation.π T) (Profinite.presentation.π T)

/-- Honest triple Q=R×_T P, not the triple of an alternative cover. -/
noncomputable abbrev stoneanCompHausProbeCechTripleEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) ≃
      {xy : (U.compHaus ⟶
          profiniteToCompHaus.obj (stoneanPresentationCechPairs T)) ×
          (U.compHaus ⟶ profiniteToCompHaus.obj
          (Stonean.toProfinite.obj T.presentation)) //
        xy.1 ≫ profiniteToCompHaus.map
            (pullback.fst (Profinite.presentation.π T)
              (Profinite.presentation.π T) ≫ Profinite.presentation.π T) =
          xy.2 ≫ profiniteToCompHaus.map (Profinite.presentation.π T)} :=
  compHausHomProfinitePullbackEquiv U.compHaus
    (pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The first pair projection of the actual triple is preserved
by the genuine CompHaus pullback comparison. -/
theorem stoneanCompHausProbeTripleEquiv_xy
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) :
    (stoneanCompHausProbeCechTripleEquiv T U z).1.1 =
      z ≫ profiniteToCompHaus.map (stoneanCechTripleXY T) := by
  rfl

/-- The third endpoint projection of the actual triple is preserved. -/
theorem stoneanCompHausProbeTripleEquiv_z
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) :
    (stoneanCompHausProbeCechTripleEquiv T U z).1.2 =
      z ≫ profiniteToCompHaus.map (stoneanCechTripleZ T) := by
  rfl

/-- The actual (x,z) face's first endpoint is x. -/
theorem stoneanCompHausProbeTripleXZ_fst
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) :
    (z ≫ profiniteToCompHaus.map (stoneanCechTripleXZ T)) ≫
      profiniteToCompHaus.map
        (pullback.fst (Profinite.presentation.π T)
          (Profinite.presentation.π T)) =
    (z ≫ profiniteToCompHaus.map (stoneanCechTripleXY T)) ≫
      profiniteToCompHaus.map
        (pullback.fst (Profinite.presentation.π T)
          (Profinite.presentation.π T)) := by
  simp only [Category.assoc, ← Functor.map_comp,
    stoneanCechTripleXZ, pullback.lift_fst]

/-- The actual (x,z) face's second endpoint is z. -/
theorem stoneanCompHausProbeTripleXZ_snd
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) :
    (z ≫ profiniteToCompHaus.map (stoneanCechTripleXZ T)) ≫
      profiniteToCompHaus.map
        (pullback.snd (Profinite.presentation.π T)
          (Profinite.presentation.π T)) =
    z ≫ profiniteToCompHaus.map (stoneanCechTripleZ T) := by
  simp only [Category.assoc, ← Functor.map_comp,
    stoneanCechTripleXZ, pullback.lift_snd]

/-- The actual (y,z) face's first endpoint is y. -/
theorem stoneanCompHausProbeTripleYZ_fst
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) :
    (z ≫ profiniteToCompHaus.map (stoneanCechTripleYZ T)) ≫
      profiniteToCompHaus.map
        (pullback.fst (Profinite.presentation.π T)
          (Profinite.presentation.π T)) =
    (z ≫ profiniteToCompHaus.map (stoneanCechTripleXY T)) ≫
      profiniteToCompHaus.map
        (pullback.snd (Profinite.presentation.π T)
          (Profinite.presentation.π T)) := by
  simp only [Category.assoc, ← Functor.map_comp,
    stoneanCechTripleYZ, pullback.lift_fst]

/-- The actual (y,z) face's second endpoint is z. -/
theorem stoneanCompHausProbeTripleYZ_snd
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : U.compHaus ⟶
      profiniteToCompHaus.obj (stoneanPresentationCechTriples T)) :
    (z ≫ profiniteToCompHaus.map (stoneanCechTripleYZ T)) ≫
      profiniteToCompHaus.map
        (pullback.snd (Profinite.presentation.π T)
          (Profinite.presentation.π T)) =
    z ≫ profiniteToCompHaus.map (stoneanCechTripleZ T) := by
  simp only [Category.assoc, ← Functor.map_comp,
    stoneanCechTripleYZ, pullback.lift_snd]

#check compHausHomProfinitePullbackEquiv
#check stoneanCompHausProbeCechPairEquiv
#check stoneanCompHausProbeCechTripleEquiv

#print axioms compHausHomProfinitePullbackEquiv
#print axioms stoneanCompHausProbeTripleEquiv_xy
#print axioms stoneanCompHausProbeTripleEquiv_z
#print axioms stoneanCompHausProbeTripleXZ_fst
#print axioms stoneanCompHausProbeTripleXZ_snd
#print axioms stoneanCompHausProbeTripleYZ_fst
#print axioms stoneanCompHausProbeTripleYZ_snd

end CMDG.CondensedCM5R0
