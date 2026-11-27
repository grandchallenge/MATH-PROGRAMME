import CMDGCondensedCM4P3DerivedCM5R0CompactBoxProbeAcyclic
import CMDGCondensedCM4P3DerivedCM5R0RealProductCondensedColimit
import Mathlib.Topology.Order.IntermediateValue

/-! Canonical degree-zero comparison, natural in every compact-box
inclusion. The source is the genuine free condensed module, not a
substitute built from points. -/
noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic

variable (S : Profinite.{u}) (I : Type u)
variable (a b : I → ℝ) (h : ∀ i, a i ≤ b i)

def compactIntegerHom (T : CompHaus.{u}) :
    (compactFreeFunctor.obj T ⟶ discreteIntegerCoeff) ≃ LocallyConstant T Coeff :=
  ((Condensed.freeForgetAdjunction Coeff).homEquiv
    (compHausToCondensed.obj T) discreteIntegerCoeff).trans
    ((coherentTopology CompHaus.{u}).uliftYonedaEquiv)

theorem compactIntegerHom_precomp {X Y : CompHaus.{u}} (q : X ⟶ Y)
    (g : compactFreeFunctor.obj Y ⟶ discreteIntegerCoeff) :
    compactIntegerHom X (compactFreeFunctor.map q ≫ g) =
      (compactIntegerHom Y g).comap q.hom.hom := by
  unfold compactIntegerHom
  change (coherentTopology CompHaus.{u}).uliftYonedaEquiv
    ((Condensed.freeForgetAdjunction Coeff).homEquiv (compHausToCondensed.obj X)
      discreteIntegerCoeff ((Condensed.free Coeff).map (compHausToCondensed.map q) ≫ g)) = _
  rw [(Condensed.freeForgetAdjunction Coeff).homEquiv_naturality_left]
  exact ((coherentTopology CompHaus.{u}).uliftYonedaEquiv_naturality
    ((Condensed.freeForgetAdjunction Coeff).homEquiv
      (compHausToCondensed.obj Y) discreteIntegerCoeff g) q).symm

def boxToProbe : probeBoxT S I a b ⟶ profiniteToCompHaus.obj S :=
  CompHausLike.ofHom _ (⟨Prod.fst,continuous_fst⟩ :
    C((S × (∀ i, Set.Icc (a i) (b i))),S))

def probeToBox : profiniteToCompHaus.obj S ⟶ probeBoxT S I a b :=
  CompHausLike.ofHom _ (⟨fun s => (s,fun i => ⟨a i,le_rfl,h i⟩),
    continuous_id.prodMk continuous_const⟩ :
    C(S,(S × (∀ i, Set.Icc (a i) (b i)))))

theorem probeToBox_boxToProbe :
    probeToBox S I a b h ≫ boxToProbe S I a b = 𝟙 _ := by
  apply ConcreteCategory.hom_ext
  intro x
  rfl

/-- Constant on each connected box fiber, including degenerate axes. -/
theorem boxFiberConstant (f : LocallyConstant (probeBoxT S I a b) Coeff)
    (s : S) (x y : ∀ i, Set.Icc (a i) (b i)) : f (s,x) = f (s,y) := by
  letI (i : I) : ConnectedSpace (Set.Icc (a i) (b i)) :=
    Subtype.connectedSpace (isConnected_Icc (h i))
  let g : LocallyConstant (∀ i, Set.Icc (a i) (b i)) Coeff :=
    f.comap ⟨fun z => (s,z),continuous_const.prodMk continuous_id⟩
  exact g.apply_eq_of_preconnectedSpace x y

/-- The inverse of precomposition with the projection is evaluation
on a continuous section. Fiber constancy makes the inverse independent
of the section. -/
def boxProjectionHomEquiv :
    (compactFreeFunctor.obj (profiniteToCompHaus.obj S) ⟶ discreteIntegerCoeff) ≃
    (compactFreeFunctor.obj (probeBoxT S I a b) ⟶ discreteIntegerCoeff) where
  toFun g := compactFreeFunctor.map (boxToProbe S I a b) ≫ g
  invFun f := compactFreeFunctor.map (probeToBox S I a b h) ≫ f
  left_inv g := by
    change compactFreeFunctor.map (probeToBox S I a b h) ≫
      (compactFreeFunctor.map (boxToProbe S I a b) ≫ g) = g
    rw [← Category.assoc, ← Functor.map_comp, probeToBox_boxToProbe]
    rw [compactFreeFunctor.map_id,Category.id_comp]
  right_inv f := by
    change compactFreeFunctor.map (boxToProbe S I a b) ≫
      (compactFreeFunctor.map (probeToBox S I a b h) ≫ f) = f
    apply (compactIntegerHom (probeBoxT S I a b)).injective
    rw [compactIntegerHom_precomp,compactIntegerHom_precomp]
    apply DFunLike.ext
    intro z
    exact boxFiberConstant S I a b h (compactIntegerHom _ f) z.1
      (fun i => ⟨a i,le_rfl,h i⟩) z.2

theorem boxProjectionHomEquiv_apply
    (g : compactFreeFunctor.obj (profiniteToCompHaus.obj S) ⟶ discreteIntegerCoeff) :
    boxProjectionHomEquiv S I a b h g =
      compactFreeFunctor.map (boxToProbe S I a b) ≫ g := rfl

end CMDG.CondensedCM5R0.CompactCover.Dyadic

namespace CMDG.CondensedCM5R0.RealProductProjection
open CompactCover.Dyadic
open RealProductCondensedColimit
open RealProductCompactExhaustion
variable (S : Profinite.{u}) (I : Type u)

def radiusBox (r : Radius I) : CompHaus.{u} :=
  probeBoxT S I (fun i => -r.val i) r.val

theorem radiusNonempty (r : Radius I) (i : I) : -r.val i ≤ r.val i := by
  linarith [r.property i]

def radiusProjection (r : Radius I) : radiusBox S I r ⟶ profiniteToCompHaus.obj S :=
  boxToProbe S I _ _

def radiusInclusion {r t : Radius I} (f : r ⟶ t) :
    radiusBox S I r ⟶ radiusBox S I t :=
  CompHausLike.ofHom _ (⟨fun x => (x.1,enlarge (leOfHom f) x.2),
    continuous_fst.prodMk ((enlarge (leOfHom f)).continuous.comp continuous_snd)⟩ :
    C((S × Box r.val),(S × Box t.val)))

theorem radiusInclusion_projection {r t : Radius I} (f : r ⟶ t) :
    radiusInclusion S I f ≫ radiusProjection S I t = radiusProjection S I r := by
  apply ConcreteCategory.hom_ext
  intro x
  rfl

def radiusHomEquiv (r : Radius I) :=
  boxProjectionHomEquiv S I (fun i => -r.val i) r.val (radiusNonempty I r)

theorem radiusHomEquiv_natural {r t : Radius I} (f : r ⟶ t)
    (g : compactFreeFunctor.obj (profiniteToCompHaus.obj S) ⟶ discreteIntegerCoeff) :
    compactFreeFunctor.map (radiusInclusion S I f) ≫ radiusHomEquiv S I t g =
      radiusHomEquiv S I r g := by
  change compactFreeFunctor.map (radiusInclusion S I f) ≫
    (compactFreeFunctor.map (radiusProjection S I t) ≫ g) =
    compactFreeFunctor.map (radiusProjection S I r) ≫ g
  rw [← Category.assoc,← Functor.map_comp,radiusInclusion_projection]

def radiusZero (r : Radius I) : profiniteToCompHaus.obj S ⟶ radiusBox S I r :=
  CompHausLike.ofHom _ (⟨fun s => (s,zeroPoint r.val r.property),
    continuous_id.prodMk continuous_const⟩ : C(S,S × Box r.val))

theorem radiusZero_projection (r : Radius I) :
    radiusZero S I r ≫ radiusProjection S I r = 𝟙 _ := by
  apply ConcreteCategory.hom_ext
  intro s
  rfl

theorem radiusHomEquiv_symm_zero (r : Radius I)
    (g : compactFreeFunctor.obj (radiusBox S I r) ⟶ discreteIntegerCoeff) :
    (radiusHomEquiv S I r).symm g = compactFreeFunctor.map (radiusZero S I r) ≫ g := by
  obtain ⟨a,rfl⟩ := (radiusHomEquiv S I r).surjective g
  rw [Equiv.symm_apply_apply]
  change a = compactFreeFunctor.map (radiusZero S I r) ≫
    (compactFreeFunctor.map (radiusProjection S I r) ≫ a)
  rw [← Category.assoc,← Functor.map_comp,radiusZero_projection]
  rw [compactFreeFunctor.map_id,Category.id_comp]

theorem radiusExtZero (r : Radius I) (q : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (radiusBox S I r))
      discreteIntegerCoeff (q+1)) : e = 0 :=
  probe_box_extPositive_zero S I _ _ (radiusNonempty I r) q e

#print axioms boxProjectionHomEquiv
#print axioms radiusHomEquiv_natural
#print axioms radiusHomEquiv_symm_zero
#print axioms radiusExtZero
end CMDG.CondensedCM5R0.RealProductProjection
