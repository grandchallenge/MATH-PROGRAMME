import CMDGCondensedCM4P3DerivedCM5R0ScalarCechH2ModuleBoundary
import CMDGCondensedCM4P3DerivedCM5R0StoneanCechTripleCocycle

/-!
# CMDG CM5 — genuine four-point Čech cancellation in the second relation

For arbitrary profinite T and four points x,y,z,w of the canonical
Stonean presentation with the same image in T, the true alternating
four-point combination of free condensed-module point maps has zero
composite with the genuine signed second Čech differential F_Q→F_R.

The proof is an explicit 12-face cancellation, using the protected
actual categorical Čech triple face maps and their checked point
identities. The kernel inclusion L_T→F_R is mono, so cancellation
descends to zero in L_T itself.

This lemma proves no global continuous section and does not assume
higher derived solidity or Ext² vanishing.
-/

noncomputable section
universe u
open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

private theorem fourPoints_altBoundary_zero
    {U Q R : Profinite.{u}}
    (xz xy yz : Q ⟶ R)
    (t_yzw t_xzw t_xyw t_xyz : U ⟶ Q)
    (r_yw r_yz r_zw r_xw r_xz r_xy : U ⟶ R)
    (h_yzw_xz : t_yzw ≫ xz = r_yw)
    (h_yzw_xy : t_yzw ≫ xy = r_yz)
    (h_yzw_yz : t_yzw ≫ yz = r_zw)
    (h_xzw_xz : t_xzw ≫ xz = r_xw)
    (h_xzw_xy : t_xzw ≫ xy = r_xz)
    (h_xzw_yz : t_xzw ≫ yz = r_zw)
    (h_xyw_xz : t_xyw ≫ xz = r_xw)
    (h_xyw_xy : t_xyw ≫ xy = r_xy)
    (h_xyw_yz : t_xyw ≫ yz = r_yw)
    (h_xyz_xz : t_xyz ≫ xz = r_xz)
    (h_xyz_xy : t_xyz ≫ xy = r_xy)
    (h_xyz_yz : t_xyz ≫ yz = r_yz) :
    (((Condensed.profiniteFree Coeff).map t_yzw -
        (Condensed.profiniteFree Coeff).map t_xzw) +
      (Condensed.profiniteFree Coeff).map t_xyw -
      (Condensed.profiniteFree Coeff).map t_xyz) ≫
      (((Condensed.profiniteFree Coeff).map xz -
        (Condensed.profiniteFree Coeff).map xy) -
        (Condensed.profiniteFree Coeff).map yz) = 0 := by
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, ← Functor.map_comp]
  rw [h_yzw_xz, h_yzw_xy, h_yzw_yz, h_xzw_xz, h_xzw_xy,
    h_xzw_yz, h_xyw_xz, h_xyw_xy, h_xyw_yz,
    h_xyz_xz, h_xyz_xy, h_xyz_yz]
  abel



noncomputable def cm5SingletonPointMap (X : Profinite.{u}) (x : X) :
    Profinite.of PUnit.{u + 1} ⟶ X :=
  ConcreteCategory.ofHom ⟨fun _ => x, continuous_const⟩

theorem cm5SingletonPointMap_comp {X Y : Profinite.{u}} (x : X) (f : X ⟶ Y) :
    cm5SingletonPointMap X x ≫ f = cm5SingletonPointMap Y (f.hom.hom x) := by
  apply ConcreteCategory.hom_ext
  intro a
  cases a
  rfl

private theorem cm5SingletonPointMap_triple_xz
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T x y z hxy hyz) ≫
      stoneanCechTripleXZ T =
    cm5SingletonPointMap (stoneanPresentationCechPairs T)
      (stoneanCechPairOfRelated T x z (hxy.trans hyz)) := by
  rw [cm5SingletonPointMap_comp, stoneanCechTripleOfRelated_xz]

private theorem cm5SingletonPointMap_triple_xy
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T x y z hxy hyz) ≫
      stoneanCechTripleXY T =
    cm5SingletonPointMap (stoneanPresentationCechPairs T)
      (stoneanCechPairOfRelated T x y hxy) := by
  rw [cm5SingletonPointMap_comp, stoneanCechTripleOfRelated_xy]

private theorem cm5SingletonPointMap_triple_yz
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T x y z hxy hyz) ≫
      stoneanCechTripleYZ T =
    cm5SingletonPointMap (stoneanPresentationCechPairs T)
      (stoneanCechPairOfRelated T y z hyz) := by
  rw [cm5SingletonPointMap_comp, stoneanCechTripleOfRelated_yz]

/-- The actual four-point alternating combination of categorical
triple points. This is a genuine free condensed-module morphism,
not an expression in an informal scalar quotient. -/
noncomputable def fourthPointAlternatingFreeMap
    (T : Profinite.{u})
    (x y z w : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w) :
    ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) :=
  (((Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T y z w hyz hzw))) -
   ((Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T x z w
          (hxy.trans hyz) hzw)))) +
   ((Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T x y w
          hxy (hyz.trans hzw)))) -
   ((Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T x y z hxy hyz)))

theorem fourthPointAlternatingFreeMap_comp_d2_zero
    (T : Profinite.{u})
    (x y z w : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w) :
    fourthPointAlternatingFreeMap T x y z w hxy hyz hzw ≫
      stoneanCechTripleBoundary T = 0 := by
  unfold fourthPointAlternatingFreeMap stoneanCechTripleBoundary
  exact fourPoints_altBoundary_zero
    (stoneanCechTripleXZ T) (stoneanCechTripleXY T)
    (stoneanCechTripleYZ T)
    (cm5SingletonPointMap _ (stoneanCechTripleOfRelated T y z w hyz hzw))
    (cm5SingletonPointMap _ (stoneanCechTripleOfRelated T x z w (hxy.trans hyz) hzw))
    (cm5SingletonPointMap _ (stoneanCechTripleOfRelated T x y w hxy (hyz.trans hzw)))
    (cm5SingletonPointMap _ (stoneanCechTripleOfRelated T x y z hxy hyz))
    (cm5SingletonPointMap _ (stoneanCechPairOfRelated T y w (hyz.trans hzw)))
    (cm5SingletonPointMap _ (stoneanCechPairOfRelated T y z hyz))
    (cm5SingletonPointMap _ (stoneanCechPairOfRelated T z w hzw))
    (cm5SingletonPointMap _ (stoneanCechPairOfRelated T x w ((hxy.trans hyz).trans hzw)))
    (cm5SingletonPointMap _ (stoneanCechPairOfRelated T x z (hxy.trans hyz)))
    (cm5SingletonPointMap _ (stoneanCechPairOfRelated T x y hxy))
    (cm5SingletonPointMap_triple_xz T y z w hyz hzw)
    (cm5SingletonPointMap_triple_xy T y z w hyz hzw)
    (cm5SingletonPointMap_triple_yz T y z w hyz hzw)
    (cm5SingletonPointMap_triple_xz T x z w (hxy.trans hyz) hzw)
    (cm5SingletonPointMap_triple_xy T x z w (hxy.trans hyz) hzw)
    (cm5SingletonPointMap_triple_yz T x z w (hxy.trans hyz) hzw)
    (cm5SingletonPointMap_triple_xz T x y w hxy (hyz.trans hzw))
    (cm5SingletonPointMap_triple_xy T x y w hxy (hyz.trans hzw))
    (cm5SingletonPointMap_triple_yz T x y w hxy (hyz.trans hzw))
    (cm5SingletonPointMap_triple_xz T x y z hxy hyz)
    (cm5SingletonPointMap_triple_xy T x y z hxy hyz)
    (cm5SingletonPointMap_triple_yz T x y z hxy hyz)


/-- The actual fourth alternating point boundary vanishes already
in the second-relation object L_T, by monicity of its kernel inclusion. -/
theorem fourthPointAlternatingFreeMap_comp_secondRelation_zero
    (T : Profinite.{u})
    (x y z w : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w) :
    fourthPointAlternatingFreeMap T x y z w hxy hyz hzw ≫
      stoneanCechTripleToSecondRelation T = 0 := by
  apply (cancel_mono (kernel.ι (stoneanCechRelationToKernel T))).1
  rw [Category.assoc, stoneanCechTripleToSecondRelation_comp_ι,
    zero_comp]
  exact fourthPointAlternatingFreeMap_comp_d2_zero
    T x y z w hxy hyz hzw

#print axioms fourthPointAlternatingFreeMap_comp_secondRelation_zero
#print axioms fourthPointAlternatingFreeMap_comp_d2_zero

#print axioms fourthPointAlternatingFreeMap_comp_d2_zero

#print axioms fourPoints_altBoundary_zero
end CMDG.CondensedCM5R0
