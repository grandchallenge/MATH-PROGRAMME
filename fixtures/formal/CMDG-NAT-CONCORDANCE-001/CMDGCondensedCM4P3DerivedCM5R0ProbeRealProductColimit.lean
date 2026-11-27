import CMDGCondensedCM4P3DerivedCM5R0CompactBoxProjectionHom

/-! Actual relative box colimit in condensed sets and free modules.
The target is the genuine space of continuous maps into the real
product with the external profinite probe retained. -/
noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
namespace CMDG.CondensedCM5R0.RealProductProjection
open CompactCover.Dyadic RealProductCondensedColimit RealProductCompactExhaustion
variable (S : Profinite.{u}) (I : Type u)

def radiusDiagram : Radius I ⥤ CompHaus.{u} where
  obj := radiusBox S I
  map := radiusInclusion S I
  map_id r := by
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · rfl
    · funext i
      apply Subtype.ext
      rfl
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · rfl
    · funext i
      apply Subtype.ext
      rfl

def probeRealSet : CondensedSet.{u} :=
  topCatToCondensedSet.obj (TopCat.of (ULift.{u+1,u} (S × (I → ℝ))))

def radiusToReal (r : Radius I) :
    C(radiusBox S I r, ULift.{u+1,u} (S × (I → ℝ))) :=
  ⟨fun x => ⟨(x.1,inclusion r.val x.2)⟩,
    continuous_uliftUp.comp
      (continuous_fst.prodMk ((inclusion r.val).continuous.comp continuous_snd))⟩

def probeRealCocone : Cocone (radiusDiagram S I ⋙ compHausToCondensed) where
  pt := probeRealSet S I
  ι :=
    { app := fun r =>
        (coherentTopology CompHaus.{u}).uliftYonedaEquiv.symm (radiusToReal S I r)
      naturality := by
        intro r t f
        change compHausToCondensed.map (radiusInclusion S I f) ≫
            (coherentTopology CompHaus.{u}).uliftYonedaEquiv.symm (radiusToReal S I t) = _
        rw [(coherentTopology CompHaus.{u}).uliftYonedaEquiv_symm_naturality_left]
        rfl }

theorem probeRealCocone_app_apply (r : Radius I) (T : CompHaus.{u}ᵒᵖ)
    (x : T.unop ⟶ radiusBox S I r) :
    ((probeRealCocone S I).ι.app r).hom.app T ⟨x⟩ =
      (radiusToReal S I r).comp x.hom.hom := by
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv_symm_app_apply
    (F := probeRealSet S I) (radiusToReal S I r) T x

def probeRealSectionsColimit (T : CompHaus.{u}ᵒᵖ) :
    IsColimit (((evaluation CompHaus.{u}ᵒᵖ (Type (u+1))).obj T).mapCocone
      (forgetSheaf.mapCocone (probeRealCocone S I))) := by
  apply Types.FilteredColimit.isColimitOf
  · intro x
    change C(T.unop, ULift.{u+1,u} (S × (I → ℝ))) at x
    let f : C(T.unop,I → ℝ) :=
      ⟨fun s => (x s).down.2, continuous_snd.comp (continuous_uliftDown.comp x.continuous)⟩
    obtain ⟨r,hr,g,hg⟩ := compactProbe_factors f
    let z : T.unop ⟶ radiusBox S I ⟨r,hr⟩ :=
      CompHausLike.ofHom _ (⟨fun s => ((x s).down.1,g s),
        (continuous_fst.comp (continuous_uliftDown.comp x.continuous)).prodMk g.continuous⟩ :
        C(T.unop,S × Box r))
    refine ⟨⟨r,hr⟩,⟨z⟩,?_⟩
    change x = ((probeRealCocone S I).ι.app ⟨r,hr⟩).hom.app T ⟨z⟩
    rw [probeRealCocone_app_apply]
    apply ContinuousMap.ext
    intro s
    apply ULift.ext
    apply Prod.ext
    · rfl
    · exact (congrArg (fun k : C(T.unop,I → ℝ) => k s) hg).symm
  · intro r t x y h
    obtain ⟨b,hb,hr,ht⟩ := common_box r.val t.val
    refine ⟨⟨b,hb⟩,homOfLE hr,homOfLE ht,?_⟩
    change ((probeRealCocone S I).ι.app r).hom.app T x =
      ((probeRealCocone S I).ι.app t).hom.app T y at h
    rcases x with ⟨x⟩
    rcases y with ⟨y⟩
    rw [probeRealCocone_app_apply,probeRealCocone_app_apply] at h
    apply ULift.ext
    apply ConcreteCategory.hom_ext
    intro s
    have hs := congrArg (fun k : C(T.unop, ULift.{u+1,u} (S × (I → ℝ))) =>
      (k s).down) h
    apply Prod.ext
    · exact congrArg Prod.fst hs
    · apply inclusion_injective b
      exact congrArg Prod.snd hs

def probeRealIsColimit : IsColimit (probeRealCocone S I) := by
  apply isColimitOfReflects forgetSheaf
  exact evaluationJointlyReflectsColimits _ (probeRealSectionsColimit S I)

def freeProbeRealCocone := (Condensed.free Coeff).mapCocone (probeRealCocone S I)

def freeProbeRealIsColimit : IsColimit (freeProbeRealCocone S I) := by
  letI := (Condensed.freeForgetAdjunction Coeff).isLeftAdjoint
  exact isColimitOfPreserves _ (probeRealIsColimit S I)

/-- Projection induced by the compatible actual compact projections. -/
def projectionCocone : Cocone ((radiusDiagram S I ⋙ compHausToCondensed) ⋙
    Condensed.free Coeff) where
  pt := compactFreeFunctor.obj (profiniteToCompHaus.obj S)
  ι :=
    { app := fun r => compactFreeFunctor.map (radiusProjection S I r)
      naturality := by
        intro r t f
        change compactFreeFunctor.map (radiusInclusion S I f) ≫
          compactFreeFunctor.map (radiusProjection S I t) = _
        rw [← Functor.map_comp,radiusInclusion_projection] }

def realProjection : (freeProbeRealCocone S I).pt ⟶
    compactFreeFunctor.obj (profiniteToCompHaus.obj S) :=
  (freeProbeRealIsColimit S I).desc (projectionCocone S I)

theorem realProjection_restrict (r : Radius I) :
    (freeProbeRealCocone S I).ι.app r ≫ realProjection S I =
      compactFreeFunctor.map (radiusProjection S I r) :=
  (freeProbeRealIsColimit S I).fac (projectionCocone S I) r

/-- The projection remains the actual Hom equivalence on the full union.
The proof uses the colimit universal property, not a limit exactness
assumption. -/
theorem realProjection_hom_bijective :
    Function.Bijective (fun g : compactFreeFunctor.obj (profiniteToCompHaus.obj S) ⟶
      discreteIntegerCoeff => realProjection S I ≫ g) := by
  constructor
  · intro g h he
    let r : Radius I := ⟨fun _ => 0,fun _ => le_rfl⟩
    apply (radiusHomEquiv S I r).injective
    change compactFreeFunctor.map (radiusProjection S I r) ≫ g =
      compactFreeFunctor.map (radiusProjection S I r) ≫ h
    rw [← realProjection_restrict S I r,Category.assoc,Category.assoc,he]
  · intro g
    let r₀ : Radius I := ⟨fun _ => 0,fun _ => le_rfl⟩
    let a := (radiusHomEquiv S I r₀).symm ((freeProbeRealCocone S I).ι.app r₀ ≫ g)
    refine ⟨a,?_⟩
    apply (freeProbeRealIsColimit S I).hom_ext
    intro r
    rw [← Category.assoc,realProjection_restrict]
    let f : r₀ ⟶ r := homOfLE (fun i => r.property i)
    have hr : compactFreeFunctor.map (radiusInclusion S I f) ≫
        ((freeProbeRealCocone S I).ι.app r ≫ g) =
        (freeProbeRealCocone S I).ι.app r₀ ≫ g := by
      rw [← Category.assoc]
      exact congrArg (fun z => z ≫ g) ((freeProbeRealCocone S I).ι.naturality f)
    obtain ⟨b,hb⟩ := (radiusHomEquiv S I r).surjective
      ((freeProbeRealCocone S I).ι.app r ≫ g)
    have hab : b = a := by
      apply (radiusHomEquiv S I r₀).injective
      change radiusHomEquiv S I r₀ b = radiusHomEquiv S I r₀ ((radiusHomEquiv S I r₀).symm _)
      rw [Equiv.apply_symm_apply]
      rw [← hr,← hb,radiusHomEquiv_natural]
    change radiusHomEquiv S I r a = _
    rw [← hab,hb]

#print axioms probeRealIsColimit
#print axioms freeProbeRealIsColimit
#print axioms realProjection_hom_bijective
end CMDG.CondensedCM5R0.RealProductProjection
