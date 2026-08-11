import CMDGCondensedCM4P2EFiniteMeasureTransport
import CMDGCondensedCM4P2EAlgebraic

/-!
# CMDG CM4-P2-E finite free-presheaf transport

This auxiliary fixture closes the finite presheaf-level free-side comparison required by E1. It
identifies the canonical finite coefficient-family presheaf with the locally-constant presheaf of
the small finite free module, proves the comparison natural on canonical delta generators, and
composes it with the already-certified finite measure/internal-dual transport.

No sheaf-level finite comparison or global P2-E equivalence is asserted here.
-/

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
attribute [local instance] FintypeCat.fintype

abbrev R := CMDG.CondensedCM4P2D.R.{u}

/-- The small finite free modules, realized as locally-constant module presheaves. -/
noncomputable abbrev finiteSmallFreePresheafFunctor :
    FintypeCat.{u} ⥤ (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R) :=
  CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule ⋙
    CondensedMod.LocallyConstant.functorToPresheaves R

/-- At a fixed finite set, the canonical coefficient family is the locally-constant presheaf of
the small finite free module. -/
noncomputable def finiteCoefficientFamilyFreeIso (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X ≅
      finiteSmallFreePresheafFunctor.obj X :=
  (CMDG.CondensedCM4P2E.FiniteTransport.finiteFunctionPresheafFamilyIso X).symm ≪≫
    (CondensedMod.LocallyConstant.functorToPresheaves R).mapIso
      ((Finsupp.linearEquivFunOnFinite R R X.obj).symm.toModuleIso)

/-- The canonical free-module delta inclusion at a finite point. -/
noncomputable def finiteSmallFreeCoordinateModuleMap
    (X : FintypeCat.{u}) (x : X.obj) :
    ModuleCat.of R R ⟶ CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule.obj X :=
  ModuleCat.ofHom (Finsupp.lsingle x)

/-- The corresponding delta inclusion after passage to locally-constant presheaves. -/
noncomputable def finiteSmallFreeCoordinateInclusion
    (X : FintypeCat.{u}) (x : X.obj) :
    CMDG.CondensedCM4P2D.coefficientPresheaf ⟶ finiteSmallFreePresheafFunctor.obj X :=
  (CondensedMod.LocallyConstant.functorToPresheaves R).map
    (finiteSmallFreeCoordinateModuleMap X x)

/-- Sectionwise action of the family/free comparison: unflip the finite family, then apply the
canonical finite `Pi`/`Finsupp` equivalence pointwise. -/
lemma finiteCoefficientFamilyFreeIso_hom_apply
    (X : FintypeCat.{u}) (S : CompHaus.{u}ᵒᵖ)
    (a : X.obj → LocallyConstant S.unop R) (s : ↑S.unop.toTop) :
    let b : LocallyConstant S.unop (X.obj →₀ R) :=
      (ConcreteCategory.hom ((finiteCoefficientFamilyFreeIso X).hom.app S)) a
    b s = (Finsupp.linearEquivFunOnFinite R R X.obj).symm (fun y => a y s) := by
  rfl

/-- Sectionwise action of a free coordinate inclusion is the canonical `Finsupp.single`. -/
lemma finiteSmallFreeCoordinateInclusion_apply
    (X : FintypeCat.{u}) (x : X.obj) (S : CompHaus.{u}ᵒᵖ)
    (h : LocallyConstant S.unop R) (s : ↑S.unop.toTop) :
    let b : LocallyConstant S.unop (X.obj →₀ R) :=
      (ConcreteCategory.hom ((finiteSmallFreeCoordinateInclusion X x).app S)) h
    b s = Finsupp.single x (h s) := by
  rfl

/-- Evaluation of the canonical inverse finite `Pi`/`Finsupp` equivalence. -/
lemma finitePiFinsuppSymm_apply
    (X : FintypeCat.{u}) (v : X.obj → R) (y : X.obj) :
    ((Finsupp.linearEquivFunOnFinite R R X.obj).symm v) y = v y := by
  rw [Finsupp.linearEquivFunOnFinite_symm_apply]

/-- The canonical coefficient-family coordinate has its input section in its own coordinate. -/
lemma finiteCoordinateInclusion_apply_self
    (X : FintypeCat.{u}) (x : X.obj) (S : CompHaus.{u}ᵒᵖ)
    (h : LocallyConstant S.unop R) (s : ↑S.unop.toTop) :
    let a : X.obj → LocallyConstant S.unop R :=
      (ConcreteCategory.hom ((finiteCoordinateInclusion X x).app S)) h
    a x s = h s := by
  classical
  change (if x = x then h else 0) s = h s
  simp

/-- Off the chosen coordinate, the canonical coefficient-family coordinate is zero. -/
lemma finiteCoordinateInclusion_apply_ne
    (X : FintypeCat.{u}) {x y : X.obj} (hy : y ≠ x) (S : CompHaus.{u}ᵒᵖ)
    (h : LocallyConstant S.unop R) (s : ↑S.unop.toTop) :
    let a : X.obj → LocallyConstant S.unop R :=
      (ConcreteCategory.hom ((finiteCoordinateInclusion X x).app S)) h
    a y s = 0 := by
  classical
  change (if y = x then h else 0) s = 0
  simp [hy]

/-- The family/free comparison sends the canonical coordinate inclusion to `Finsupp.single`. -/
lemma finiteCoordinateInclusion_freeIso
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ (finiteCoefficientFamilyFreeIso X).hom =
      finiteSmallFreeCoordinateInclusion X x := by
  classical
  ext S h
  let h' : LocallyConstant S.unop R := h
  let a : X.obj → LocallyConstant S.unop R :=
    (ConcreteCategory.hom ((finiteCoordinateInclusion X x).app S)) h'
  let b : LocallyConstant S.unop (X.obj →₀ R) :=
    (ConcreteCategory.hom ((finiteCoefficientFamilyFreeIso X).hom.app S)) a
  let c : LocallyConstant S.unop (X.obj →₀ R) :=
    (ConcreteCategory.hom ((finiteSmallFreeCoordinateInclusion X x).app S)) h'
  change b = c
  apply LocallyConstant.ext
  intro s
  have hb :
      b s = (Finsupp.linearEquivFunOnFinite R R X.obj).symm (fun y => a y s) := by
    exact finiteCoefficientFamilyFreeIso_hom_apply X S a s
  have hc : c s = Finsupp.single x (h' s) := by
    exact finiteSmallFreeCoordinateInclusion_apply X x S h' s
  rw [hb, hc]
  apply Finsupp.ext
  intro y
  rw [finitePiFinsuppSymm_apply X _ y]
  by_cases hy : y = x
  · subst y
    rw [finiteCoordinateInclusion_apply_self X x S h' s]
    simp
  · rw [finiteCoordinateInclusion_apply_ne X hy S h' s]
    simp [hy]

/-- Pushforward of a canonical small-free generator follows the finite map. -/
lemma finiteSmallFreeCoordinateModuleMap_naturality
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteSmallFreeCoordinateModuleMap X x ≫
        CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule.map f =
      finiteSmallFreeCoordinateModuleMap Y (f x) := by
  apply ModuleCat.hom_ext
  apply LinearMap.ext
  intro r
  change
    Finsupp.lmapDomain R R (fun z => f z) (Finsupp.single x r) =
      Finsupp.single (f x) r
  simp only [Finsupp.lmapDomain_apply, Finsupp.mapDomain_single]

/-- The locally-constant presheaf realization preserves the free-generator naturality square. -/
lemma finiteSmallFreeCoordinateInclusion_naturality
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteSmallFreeCoordinateInclusion X x ≫ finiteSmallFreePresheafFunctor.map f =
      finiteSmallFreeCoordinateInclusion Y (f x) := by
  change
    (CondensedMod.LocallyConstant.functorToPresheaves R).map
          (finiteSmallFreeCoordinateModuleMap X x) ≫
        (CondensedMod.LocallyConstant.functorToPresheaves R).map
          (CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule.map f) =
      (CondensedMod.LocallyConstant.functorToPresheaves R).map
        (finiteSmallFreeCoordinateModuleMap Y (f x))
  rw [← Functor.map_comp]
  rw [finiteSmallFreeCoordinateModuleMap_naturality]

/-- The transported internal-dual action and the explicit pushforward action are naturally
isomorphic by identity components, because their maps were already certified equal. -/
noncomputable def finiteCoefficientFamilyCovariantPushforwardNatIso :
    finiteCoefficientFamilyCovariantFunctor ≅ finiteCoefficientFamilyPushforwardFunctor :=
  NatIso.ofComponents
    (fun X => Iso.refl _)
    (by
      intro X Y f
      rw [Category.comp_id, Category.id_comp]
      exact finiteCoefficientFamilyCovariant_map_eq_pushforward f)

/-- The finite coefficient-family/free comparison is natural. The proof is generatorwise and uses
the certified coordinate resolution rather than any chosen basis. -/
noncomputable def finiteCoefficientFamilyFreeNatIso :
    finiteCoefficientFamilyPushforwardFunctor ≅ finiteSmallFreePresheafFunctor :=
  NatIso.ofComponents
    (fun X => finiteCoefficientFamilyFreeIso X)
    (by
      intro X Y f
      apply finiteCoefficientFamily_hom_ext
      intro x
      calc
        finiteCoordinateInclusion X x ≫
            (finiteCoefficientFamilyPushforwardFunctor.map f ≫
              (finiteCoefficientFamilyFreeIso Y).hom) =
          (finiteCoordinateInclusion X x ≫
              finiteCoefficientFamilyPushforwardFunctor.map f) ≫
            (finiteCoefficientFamilyFreeIso Y).hom := by
              rw [← Category.assoc]
        _ = finiteCoordinateInclusion Y (f x) ≫
              (finiteCoefficientFamilyFreeIso Y).hom := by
              rw [finiteCoordinateInclusion_pushforwardFunctor_map]
        _ = finiteSmallFreeCoordinateInclusion Y (f x) := by
              rw [finiteCoordinateInclusion_freeIso]
        _ = finiteSmallFreeCoordinateInclusion X x ≫
              finiteSmallFreePresheafFunctor.map f := by
              exact (finiteSmallFreeCoordinateInclusion_naturality f x).symm
        _ = (finiteCoordinateInclusion X x ≫
              (finiteCoefficientFamilyFreeIso X).hom) ≫
              finiteSmallFreePresheafFunctor.map f := by
              rw [finiteCoordinateInclusion_freeIso]
        _ = finiteCoordinateInclusion X x ≫
              ((finiteCoefficientFamilyFreeIso X).hom ≫
                finiteSmallFreePresheafFunctor.map f) := by
              rw [Category.assoc])

/-- Presheaf-level finite E1 comparison: the actual P2-D finite measure presheaf is naturally the
locally-constant presheaf of the canonical small finite free module. -/
noncomputable def finiteMeasureSmallFreePresheafNatIso :
    finiteMeasurePresheafFunctor ≅ finiteSmallFreePresheafFunctor :=
  finiteMeasurePresheafFamilyNatIso ≪≫
    finiteFamilyInternalHomNatIso ≪≫
    finiteCoefficientFamilyCovariantPushforwardNatIso ≪≫
    finiteCoefficientFamilyFreeNatIso

#check finiteSmallFreePresheafFunctor
#check finiteCoefficientFamilyFreeIso
#check finiteSmallFreeCoordinateModuleMap
#check finiteSmallFreeCoordinateInclusion
#check finiteCoefficientFamilyFreeIso_hom_apply
#check finiteSmallFreeCoordinateInclusion_apply
#check finitePiFinsuppSymm_apply
#check finiteCoordinateInclusion_apply_self
#check finiteCoordinateInclusion_apply_ne
#check finiteCoordinateInclusion_freeIso
#check finiteSmallFreeCoordinateModuleMap_naturality
#check finiteSmallFreeCoordinateInclusion_naturality
#check finiteCoefficientFamilyCovariantPushforwardNatIso
#check finiteCoefficientFamilyFreeNatIso
#check finiteMeasureSmallFreePresheafNatIso

#print axioms finiteCoefficientFamilyFreeIso
#print axioms finiteSmallFreeCoordinateModuleMap
#print axioms finiteSmallFreeCoordinateInclusion
#print axioms finiteCoefficientFamilyFreeIso_hom_apply
#print axioms finiteSmallFreeCoordinateInclusion_apply
#print axioms finitePiFinsuppSymm_apply
#print axioms finiteCoordinateInclusion_apply_self
#print axioms finiteCoordinateInclusion_apply_ne
#print axioms finiteCoordinateInclusion_freeIso
#print axioms finiteSmallFreeCoordinateModuleMap_naturality
#print axioms finiteSmallFreeCoordinateInclusion_naturality
#print axioms finiteCoefficientFamilyCovariantPushforwardNatIso
#print axioms finiteCoefficientFamilyFreeNatIso
#print axioms finiteMeasureSmallFreePresheafNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
