import CMDGCondensedCM4P3D
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Sites.Subcanonical
import Mathlib.Topology.Category.Profinite.AsLimit
import Mathlib.Topology.Category.Profinite.Nobeling.Induction

/-!
# CMDG CM4-P3-G — coefficient finite-stage mapping-out attack

This fixture attacks the single coefficient-object residual left by protected P3-D.
It identifies lower Hom with locally constant coefficient functions, proves finite-quotient
factorization on the lower/free side, constructs the corresponding finite-stage extension on
the solid side, and proves surjectivity of coefficient solidification precomposition.

The sole deliberately unproved proposition introduced below is
`CoefficientFiniteStageMappingOut`: every morphism from `profiniteSolid X` to the discrete
coefficient object is already represented at one finite quotient stage. The terminal theorems
prove that this exact proposition is equivalent to the remaining injectivity theorem and hence,
through protected P3-D, to `CondensedMod.IsSolid R coefficientObject`.
-/

namespace CMDG.CondensedCM4P3G

universe u

open CategoryTheory Limits Opposite
open scoped Topology

abbrev R := CMDG.CondensedCM4P3D.R.{u}

noncomputable abbrev coefficientObject : CondensedMod.{u} R :=
  CMDG.CondensedCM4P3D.coefficientObject.{u}

abbrev LowerHom (X : Profinite.{u}) :=
  (Condensed.profiniteFree R).obj X ⟶ coefficientObject

abbrev CoefficientSections (X : Profinite.{u}) :=
  ((Condensed.forget R).obj coefficientObject).obj.obj
    (op ((profiniteToCompHaus).obj X))

noncomputable def lowerHomSectionsEquiv (X : Profinite.{u}) :
    LowerHom X ≃ CoefficientSections X := by
  change
    (((Condensed.free R).obj ((profiniteToCondensed).obj X) ⟶ coefficientObject) ≃
      CoefficientSections X)
  refine ((Condensed.freeForgetAdjunction R).homEquiv
    ((profiniteToCondensed).obj X) coefficientObject).trans ?_
  change
    (((coherentTopology CompHaus.{u}).uliftYoneda.obj ((profiniteToCompHaus).obj X) ⟶
      (Condensed.forget R).obj coefficientObject) ≃ CoefficientSections X)
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv

noncomputable def lowerHomEquiv (X : Profinite.{u}) :
    LowerHom X ≃ LocallyConstant X R := by
  exact lowerHomSectionsEquiv X

theorem lowerHomSectionsEquiv_apply (X : Profinite.{u}) (g : LowerHom X) :
    lowerHomSectionsEquiv X g =
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction R).homEquiv
          ((profiniteToCondensed).obj X) coefficientObject g) := by
  rfl

theorem lowerHomSectionsEquiv_precomp {X Y : Profinite.{u}}
    (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomSectionsEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      ((Condensed.forget R).obj coefficientObject).obj.map
        ((profiniteToCompHaus).map q).op (lowerHomSectionsEquiv Y g) := by
  rw [lowerHomSectionsEquiv_apply X, lowerHomSectionsEquiv_apply Y]
  have hfree :
      (Condensed.profiniteFree R).map q =
        (Condensed.free R).map ((profiniteToCondensed).map q) := by
    rfl
  rw [hfree]
  rw [(Condensed.freeForgetAdjunction R).homEquiv_naturality_left]
  simpa [GrothendieckTopology.uliftYoneda, profiniteToCondensed,
    compHausToCondensed, compHausToCondensed', Condensed.ulift, Functor.comp_map] using
    ((coherentTopology CompHaus.{u}).uliftYonedaEquiv_naturality
      ((Condensed.freeForgetAdjunction R).homEquiv
        ((profiniteToCondensed).obj Y) coefficientObject g)
      ((profiniteToCompHaus).map q)).symm

theorem lowerHomEquiv_precomp {X Y : Profinite.{u}} (q : X ⟶ Y) (g : LowerHom Y) :
    lowerHomEquiv X ((Condensed.profiniteFree R).map q ≫ g) =
      (lowerHomEquiv Y g).comap q.hom.hom := by
  change lowerHomSectionsEquiv X ((Condensed.profiniteFree R).map q ≫ g) = _
  rw [lowerHomSectionsEquiv_precomp]
  rfl

/-- The canonical projection from a profinite space to one of its finite discrete quotients. -/
noncomputable def finiteQuotientMap (X : Profinite.{u}) (j : DiscreteQuotient X) :
    X ⟶ X.diagram.obj j :=
  X.asLimitCone.π.app j

theorem finiteQuotientMap_surjective (X : Profinite.{u}) (j : DiscreteQuotient X) :
    Function.Surjective (finiteQuotientMap X j).hom.hom := by
  change Function.Surjective j.proj
  exact j.proj_surjective

/-- Every lower/free-side coefficient morphism already factors through one finite quotient. -/
theorem lowerHom_factors_finite (X : Profinite.{u}) (g : LowerHom X) :
    ∃ (j : DiscreteQuotient X) (gQ : LowerHom (X.diagram.obj j)),
      g = (Condensed.profiniteFree R).map (finiteQuotientMap X j) ≫ gQ := by
  obtain ⟨j, fQ, hf⟩ :=
    Profinite.exists_locallyConstant X.asLimitCone X.asLimit (lowerHomEquiv X g)
  change lowerHomEquiv X g =
    LocallyConstant.comap (finiteQuotientMap X j).hom.hom fQ at hf
  refine ⟨j, (lowerHomEquiv (X.diagram.obj j)).symm fQ, ?_⟩
  apply (lowerHomEquiv X).injective
  rw [lowerHomEquiv_precomp]
  simpa using hf

/-- Precomposition on lower Hom is injective along any surjective profinite map. -/
theorem lowerHom_precomp_injective_of_surjective {X Y : Profinite.{u}}
    (q : X ⟶ Y) (hq : Function.Surjective q.hom.hom) :
    Function.Injective
      (fun g : LowerHom Y => (Condensed.profiniteFree R).map q ≫ g) := by
  intro g₁ g₂ h
  apply (lowerHomEquiv Y).injective
  apply LocallyConstant.comap_injective q.hom.hom hq
  rw [← lowerHomEquiv_precomp q g₁, ← lowerHomEquiv_precomp q g₂]
  exact congrArg (lowerHomEquiv X) h

@[reassoc]
theorem finiteSolidification_counit (Q : FintypeCat.{u}) :
    (Condensed.profiniteSolidification R).app (FintypeCat.toProfinite.obj Q) ≫
        (Condensed.profiniteSolidCounit R).app Q =
      𝟙 ((Condensed.finFree R).obj Q) := by
  simpa [Condensed.profiniteSolidification] using
    (Functor.liftOfIsRightKanExtension_fac_app
      (Condensed.profiniteSolid R)
      (Condensed.profiniteSolidCounit R)
      (Condensed.profiniteFree R)
      (𝟙 (Condensed.finFree R)) Q)

/-- Extend a lower morphism defined on one finite quotient stage to the right-Kan/solid object. -/
noncomputable def finiteStageExtension
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (gQ : LowerHom (X.diagram.obj j)) :
    (Condensed.profiniteSolid R).obj X ⟶ coefficientObject :=
  (Condensed.profiniteSolid R).map (finiteQuotientMap X j) ≫
    (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ gQ

/-- The finite-stage extension is a genuine lift of the corresponding lower/free-side morphism. -/
theorem finiteStageExtension_precomp
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (gQ : LowerHom (X.diagram.obj j)) :
    (Condensed.profiniteSolidification R).app X ≫ finiteStageExtension X j gQ =
      (Condensed.profiniteFree R).map (finiteQuotientMap X j) ≫ gQ := by
  unfold finiteStageExtension
  rw [← (Condensed.profiniteSolidification R).naturality_assoc]
  have hfin :
      (Condensed.profiniteSolidification R).app (X.diagram.obj j) ≫
          (Condensed.profiniteSolidCounit R).app (X.fintypeDiagram.obj j) ≫ gQ = gQ := by
    simpa only [Functor.comp_obj] using
      (finiteSolidification_counit_assoc (X.fintypeDiagram.obj j) gQ)
  rw [hfin]

/-- The coefficient precomposition map is already surjective; only injectivity remains. -/
theorem coefficient_homPrecomp_surjective (X : Profinite.{u}) :
    Function.Surjective
      (CMDG.CondensedCM4P3D.homPrecomp coefficientObject X) := by
  intro g
  obtain ⟨j, gQ, hg⟩ := lowerHom_factors_finite X g
  refine ⟨finiteStageExtension X j gQ, ?_⟩
  change
    (Condensed.profiniteSolidification R).app X ≫ finiteStageExtension X j gQ = g
  rw [finiteStageExtension_precomp]
  exact hg.symm

/-- Pointwise scalar extension from integral locally constant functions to the lifted ring. -/
noncomputable def locallyConstantIntegralLiftEquiv (X : Profinite.{u}) :
    LocallyConstant X ℤ ≃+* LocallyConstant X R :=
  LocallyConstant.congrRightRingEquiv (X := X)
    (ULift.ringEquiv.symm : ℤ ≃+* R)

/-- Transport an `R`-linear scalar functional back to integral coefficients. This is the
narrow coefficient change needed for the Nöbeling argument; no global lifted freeness instance
is required. -/
noncomputable def liftedIntFunctionalDown (X : Profinite.{u})
    (μ : LocallyConstant X R →ₗ[R] R) :
    LocallyConstant X ℤ →ₗ[ℤ] ℤ where
  toFun f := (μ (locallyConstantIntegralLiftEquiv X f)).down
  map_add' f g := by
    simp [locallyConstantIntegralLiftEquiv]
  map_smul' r f := by
    simp [locallyConstantIntegralLiftEquiv, smul_eq_mul]

/-- A locally constant map on a Boolean product is determined at the all-true point by its
finite-coordinate truncations. -/
theorem locallyConstant_boolPi_allTrue_of_finsetPiecewise
    {ι β : Type*} [DecidableEq ι]
    (f : LocallyConstant (ι → Bool) β) (c : β)
    (h : ∀ I : Finset ι,
      f (I.piecewise (fun _ => true) (fun _ => false)) = c) :
    f (fun _ => true) = c := by
  have hs :
      {x : ι → Bool | f x = f (fun _ => true)} ∈ 𝓝 (fun _ => true) :=
    f.isLocallyConstant.eventually_eq (fun _ => true)
  obtain ⟨I, hI⟩ :=
    exists_finset_piecewise_mem_of_mem_nhds hs (fun _ => false)
  change
    f (I.piecewise (fun _ => true) (fun _ => false)) =
      f (fun _ => true) at hI
  exact hI.symm.trans (h I)

/-- The constant map from the one-point compact Hausdorff space to a chosen point. -/
noncomputable def coefficientPointProbeMap
    (T : CompHaus.{u}) (t : T) : CompHaus.of PUnit.{u + 1} ⟶ T :=
  ConcreteCategory.ofHom
    { toFun := fun _ => t
      continuous_toFun := continuous_const }

/-- A morphism into the discrete coefficient object is determined by its one-point component. -/
theorem coefficient_hom_ext_point
    {A : CondensedMod.{u} R} {f g : A ⟶ coefficientObject}
    (hpoint :
      f.hom.app (op (CompHaus.of PUnit.{u + 1})) =
        g.hom.app (op (CompHaus.of PUnit.{u + 1}))) :
    f = g := by
  apply ObjectProperty.hom_ext
  apply NatTrans.ext'
  funext T
  apply ModuleCat.hom_ext
  apply LinearMap.ext
  intro a
  change
    (show LocallyConstant T.unop R from f.hom.app T a) =
      (show LocallyConstant T.unop R from g.hom.app T a)
  ext t
  let p : CompHaus.of PUnit.{u + 1} ⟶ T.unop :=
    coefficientPointProbeMap T.unop t
  have hf := ConcreteCategory.congr_hom (f.hom.naturality p.op) a
  have hg := ConcreteCategory.congr_hom (g.hom.naturality p.op) a
  have hp := ConcreteCategory.congr_hom hpoint (A.obj.map p.op a)
  change
    f.hom.app (op (CompHaus.of PUnit.{u + 1})) (A.obj.map p.op a) =
      LocallyConstant.comap p.hom.hom
        (show LocallyConstant T.unop R from f.hom.app T a) at hf
  change
    g.hom.app (op (CompHaus.of PUnit.{u + 1})) (A.obj.map p.op a) =
      LocallyConstant.comap p.hom.hom
        (show LocallyConstant T.unop R from g.hom.app T a) at hg
  have hf' := congrArg
    (fun q : LocallyConstant (CompHaus.of PUnit.{u + 1}) R => q PUnit.unit) hf
  have hg' := congrArg
    (fun q : LocallyConstant (CompHaus.of PUnit.{u + 1}) R => q PUnit.unit) hg
  have hp' := congrArg
    (fun q : LocallyConstant (CompHaus.of PUnit.{u + 1}) R => q PUnit.unit) hp
  exact congrArg ULift.down (hf'.symm.trans (hp'.trans hg'))

/-- The exact remaining mathematical boundary: every solid-side coefficient morphism is already
visible at one finite discrete quotient stage. This proposition is deliberately not asserted. -/
def CoefficientFiniteStageMappingOut : Prop :=
  ∀ (X : Profinite.{u})
    (h : (Condensed.profiniteSolid R).obj X ⟶ coefficientObject),
    ∃ (j : DiscreteQuotient X) (gQ : LowerHom (X.diagram.obj j)),
      h = finiteStageExtension X j gQ

/-- The injective half left after the independently certified surjectivity theorem. -/
def CoefficientMappingOutInjectivity : Prop :=
  ∀ X : Profinite.{u},
    Function.Injective (CMDG.CondensedCM4P3D.homPrecomp coefficientObject X)

/-- Finite-stage mapping-out implies the remaining injectivity theorem. -/
theorem coefficientMappingOutInjectivity_of_finiteStage
    (hstage : CoefficientFiniteStageMappingOut.{u}) :
    CoefficientMappingOutInjectivity.{u} := by
  intro X h₁ h₂ hh
  change
    (Condensed.profiniteSolidification R).app X ≫ h₁ =
      (Condensed.profiniteSolidification R).app X ≫ h₂ at hh
  have hprezero :
      (Condensed.profiniteSolidification R).app X ≫ (h₁ - h₂) = 0 := by
    rw [Preadditive.comp_sub, hh, sub_self]
  obtain ⟨j, gQ, hfac⟩ := hstage X (h₁ - h₂)
  have hgpre :
      (Condensed.profiniteFree R).map (finiteQuotientMap X j) ≫ gQ = 0 := by
    rw [← finiteStageExtension_precomp X j gQ]
    rw [← hfac]
    exact hprezero
  have hgQ : gQ = 0 := by
    apply lowerHom_precomp_injective_of_surjective
      (finiteQuotientMap X j) (finiteQuotientMap_surjective X j)
    simpa using hgpre
  have hdiff : h₁ - h₂ = 0 := by
    rw [hfac, hgQ]
    simp [finiteStageExtension]
  exact sub_eq_zero.mp hdiff

/-- Conversely, injectivity makes the lower/free finite factorization unique on the solid side. -/
theorem coefficientFiniteStageMappingOut_of_injectivity
    (hinj : CoefficientMappingOutInjectivity.{u}) :
    CoefficientFiniteStageMappingOut.{u} := by
  intro X h
  obtain ⟨j, gQ, hg⟩ := lowerHom_factors_finite X
    (CMDG.CondensedCM4P3D.homPrecomp coefficientObject X h)
  refine ⟨j, gQ, ?_⟩
  apply hinj X
  change
    (Condensed.profiniteSolidification R).app X ≫ h =
      (Condensed.profiniteSolidification R).app X ≫ finiteStageExtension X j gQ
  rw [finiteStageExtension_precomp]
  exact hg

theorem coefficientFiniteStageMappingOut_iff_injectivity :
    CoefficientFiniteStageMappingOut.{u} ↔ CoefficientMappingOutInjectivity.{u} := by
  constructor
  · exact coefficientMappingOutInjectivity_of_finiteStage
  · exact coefficientFiniteStageMappingOut_of_injectivity

/-- Since surjectivity is already proved, the protected coefficient residual is exactly injectivity. -/
theorem coefficientResidualHomTheorem_iff_injectivity :
    CMDG.CondensedCM4P3D.CoefficientResidualHomTheorem.{u} ↔
      CoefficientMappingOutInjectivity.{u} := by
  constructor
  · intro h X
    exact (h X).1
  · intro h X
    exact ⟨h X, coefficient_homPrecomp_surjective X⟩

/-- Exact terminal characterization: the new finite-stage boundary is neither stronger nor weaker
than the protected P3-D coefficient-solidity blocker. -/
theorem coefficientFiniteStageMappingOut_iff_isSolid :
    CoefficientFiniteStageMappingOut.{u} ↔
      CondensedMod.IsSolid.{u} R coefficientObject := by
  exact coefficientFiniteStageMappingOut_iff_injectivity.{u}.trans
    (coefficientResidualHomTheorem_iff_injectivity.{u}.symm.trans
      CMDG.CondensedCM4P3D.coefficientResidualHomTheorem_iff_isSolid.{u})

#check lowerHomEquiv
#check lowerHomEquiv_precomp
#check finiteQuotientMap_surjective
#check lowerHom_factors_finite
#check lowerHom_precomp_injective_of_surjective
#check finiteSolidification_counit
#check finiteStageExtension_precomp
#check coefficient_homPrecomp_surjective
#check locallyConstantIntegralLiftEquiv
#check liftedIntFunctionalDown
#check locallyConstant_boolPi_allTrue_of_finsetPiecewise
#check coefficientPointProbeMap
#check coefficient_hom_ext_point
#check CoefficientFiniteStageMappingOut
#check CoefficientMappingOutInjectivity
#check coefficientFiniteStageMappingOut_iff_injectivity
#check coefficientResidualHomTheorem_iff_injectivity
#check coefficientFiniteStageMappingOut_iff_isSolid

#print axioms lowerHomEquiv
#print axioms lowerHomEquiv_precomp
#print axioms finiteQuotientMap_surjective
#print axioms lowerHom_factors_finite
#print axioms lowerHom_precomp_injective_of_surjective
#print axioms finiteSolidification_counit
#print axioms finiteStageExtension_precomp
#print axioms coefficient_homPrecomp_surjective
#print axioms locallyConstantIntegralLiftEquiv
#print axioms liftedIntFunctionalDown
#print axioms locallyConstant_boolPi_allTrue_of_finsetPiecewise
#print axioms coefficient_hom_ext_point
#print axioms coefficientFiniteStageMappingOut_iff_injectivity
#print axioms coefficientResidualHomTheorem_iff_injectivity
#print axioms coefficientFiniteStageMappingOut_iff_isSolid

end CMDG.CondensedCM4P3G