import CMDGCondensedCM4P2EFiniteDualNaturality

/-!
# CMDG CM4-P2-E canonical finite pushforward

This auxiliary fixture identifies the covariant finite coefficient-family action transported
through the certified internal duality with the canonical finite pushforward. The proof is
basis-free: it uses only the canonical coordinate inclusions/projections of a finite family and
their certified resolution of the identity.

This checkpoint does not yet identify the actual finite restriction of the P2-D measure functor
with `Condensed.finFree`, and therefore does not close E1.
-/

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- Pullback of a finite coefficient family followed by evaluation at `x` is evaluation at
`f x`. -/
lemma finiteCoefficientFamilyPresheafMap_projection
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op ≫
        finiteCoordinateProjection X x =
      finiteCoordinateProjection Y (f x) := by
  ext S a s
  rfl

/-- The named coordinate `pre` map is covariantly natural under the finite internal-dual map. -/
lemma finiteCoordinatePreProjectionNamed_internalHomMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteCoordinatePreProjectionNamed X x ≫ finiteFamilyInternalHomMap f =
      finiteCoordinatePreProjectionNamed Y (f x) := by
  change
    (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre
          (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      (MonoidalClosed.pre (finiteCoordinateProjection Y (f x))).app
        CMDG.CondensedCM4P2D.coefficientPresheaf
  have hpre := congrArg
    (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
    (MonoidalClosed.pre_map
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheafMap f.op)
      (finiteCoordinateProjection X x))
  rw [← hpre, finiteCoefficientFamilyPresheafMap_projection]

/-- The canonical coordinate extension is covariantly natural under the finite internal-dual
map. -/
lemma finiteCoordinateExtension_internalHomMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteCoordinateExtension X x ≫ finiteFamilyInternalHomMap f =
      finiteCoordinateExtension Y (f x) := by
  change
    (CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.inv ≫
        finiteCoordinatePreProjectionNamed X x) ≫
      finiteFamilyInternalHomMap f =
    CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.inv ≫
      finiteCoordinatePreProjectionNamed Y (f x)
  rw [Category.assoc, finiteCoordinatePreProjectionNamed_internalHomMap]

/-- The transported covariant action sends the canonical delta generator at `x` to the canonical
delta generator at `f x`. -/
lemma finiteCoordinateInclusion_covariant_map
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ finiteCoefficientFamilyCovariantFunctor.map f =
      finiteCoordinateInclusion Y (f x) := by
  change
    finiteCoordinateInclusion X x ≫
        (finiteFamilyExtension X ≫
          (finiteFamilyInternalHomMap f ≫ finiteFamilyEvaluation Y)) =
      finiteCoordinateInclusion Y (f x)
  rw [← Category.assoc, finiteCoordinateInclusion_familyExtension]
  rw [← Category.assoc, finiteCoordinateExtension_internalHomMap]
  exact finiteCoordinateExtension_familyEvaluation Y (f x)

/-- Canonical pushforward of a finite coefficient family, defined without a chosen basis: resolve
into its canonical coordinates and send each coordinate at `x` to the coordinate at `f x`. -/
noncomputable def finiteCoefficientFamilyPushforwardMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X ⟶
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf Y :=
  ∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateInclusion Y (f x)

/-- Canonical pushforward carries each delta generator to the delta generator at its image. -/
lemma finiteCoordinateInclusion_pushforwardMap
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ finiteCoefficientFamilyPushforwardMap f =
      finiteCoordinateInclusion Y (f x) := by
  classical
  unfold finiteCoefficientFamilyPushforwardMap
  rw [Preadditive.comp_sum Finset.univ]
  rw [Finset.sum_eq_single x]
  · rw [← Category.assoc, finiteCoordinateInclusion_projection_self]
    simp
  · intro y hy hyx
    rw [← Category.assoc,
      finiteCoordinateInclusion_projection_ne X (Ne.symm hyx)]
    simp
  · simp

/-- The canonical coordinate inclusions jointly detect morphisms out of a finite coefficient
family. -/
lemma finiteCoefficientFamily_hom_ext
    {X : FintypeCat.{u}}
    {Z : CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}}
    {p q : CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X ⟶ Z}
    (h : ∀ x, finiteCoordinateInclusion X x ≫ p = finiteCoordinateInclusion X x ≫ q) :
    p = q := by
  classical
  calc
    p = 𝟙 _ ≫ p := by simp
    _ = (∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x) ≫ p := by
      rw [finiteCoordinate_resolution]
    _ = ∑ x, (finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x) ≫ p := by
      rw [Preadditive.sum_comp Finset.univ]
    _ = ∑ x, (finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x) ≫ q := by
      apply Finset.sum_congr rfl
      intro x hx
      simp only [Category.assoc]
      rw [h x]
    _ = (∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x) ≫ q := by
      rw [Preadditive.sum_comp Finset.univ]
    _ = 𝟙 _ ≫ q := by
      rw [finiteCoordinate_resolution]
    _ = q := by simp

/-- The canonical finite-family pushforwards form a covariant functor. -/
noncomputable def finiteCoefficientFamilyPushforwardFunctor :
    FintypeCat.{u} ⥤
      (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) where
  obj X := CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X
  map f := finiteCoefficientFamilyPushforwardMap f
  map_id X := by
    apply finiteCoefficientFamily_hom_ext
    intro x
    rw [finiteCoordinateInclusion_pushforwardMap]
    simp
  map_comp f g := by
    apply finiteCoefficientFamily_hom_ext
    intro x
    change
      finiteCoordinateInclusion _ x ≫ finiteCoefficientFamilyPushforwardMap (f ≫ g) =
        finiteCoordinateInclusion _ x ≫
          (finiteCoefficientFamilyPushforwardMap f ≫ finiteCoefficientFamilyPushforwardMap g)
    rw [finiteCoordinateInclusion_pushforwardMap]
    rw [← Category.assoc,
      finiteCoordinateInclusion_pushforwardMap,
      finiteCoordinateInclusion_pushforwardMap]
    rfl

/-- Generator law with the pushforward packaged as a functor map. -/
lemma finiteCoordinateInclusion_pushforwardFunctor_map
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ finiteCoefficientFamilyPushforwardFunctor.map f =
      finiteCoordinateInclusion Y (f x) := by
  change
    finiteCoordinateInclusion X x ≫ finiteCoefficientFamilyPushforwardMap f =
      finiteCoordinateInclusion Y (f x)
  exact finiteCoordinateInclusion_pushforwardMap f x

/-- The transported internal-dual action is exactly the canonical finite pushforward. -/
lemma finiteCoefficientFamilyCovariant_map_eq_pushforward
    {X Y : FintypeCat.{u}} (f : X ⟶ Y) :
    finiteCoefficientFamilyCovariantFunctor.map f =
      finiteCoefficientFamilyPushforwardFunctor.map f := by
  apply finiteCoefficientFamily_hom_ext
  intro x
  calc
    finiteCoordinateInclusion X x ≫ finiteCoefficientFamilyCovariantFunctor.map f =
        finiteCoordinateInclusion Y (f x) := finiteCoordinateInclusion_covariant_map f x
    _ = finiteCoordinateInclusion X x ≫ finiteCoefficientFamilyPushforwardFunctor.map f :=
      (finiteCoordinateInclusion_pushforwardFunctor_map f x).symm

/-- Natural identification of the transported coefficient-family action with canonical finite
pushforward. -/
noncomputable def finiteCoefficientFamilyCovariantPushforwardNatIso :
    finiteCoefficientFamilyCovariantFunctor ≅ finiteCoefficientFamilyPushforwardFunctor :=
  NatIso.ofComponents
    (fun X => Iso.refl
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X))
    (by
      intro X Y f
      change
        finiteCoefficientFamilyCovariantFunctor.map f ≫
            𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf Y) =
          𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X) ≫
            finiteCoefficientFamilyPushforwardFunctor.map f
      rw [Category.comp_id, Category.id_comp]
      exact finiteCoefficientFamilyCovariant_map_eq_pushforward f)

#check finiteCoefficientFamilyPresheafMap_projection
#check finiteCoordinatePreProjectionNamed_internalHomMap
#check finiteCoordinateExtension_internalHomMap
#check finiteCoordinateInclusion_covariant_map
#check finiteCoefficientFamilyPushforwardMap
#check finiteCoordinateInclusion_pushforwardMap
#check finiteCoefficientFamily_hom_ext
#check finiteCoefficientFamilyPushforwardFunctor
#check finiteCoordinateInclusion_pushforwardFunctor_map
#check finiteCoefficientFamilyCovariant_map_eq_pushforward
#check finiteCoefficientFamilyCovariantPushforwardNatIso

#print axioms finiteCoefficientFamilyPresheafMap_projection
#print axioms finiteCoordinatePreProjectionNamed_internalHomMap
#print axioms finiteCoordinateExtension_internalHomMap
#print axioms finiteCoordinateInclusion_covariant_map
#print axioms finiteCoefficientFamilyPushforwardMap
#print axioms finiteCoordinateInclusion_pushforwardMap
#print axioms finiteCoefficientFamily_hom_ext
#print axioms finiteCoefficientFamilyPushforwardFunctor
#print axioms finiteCoordinateInclusion_pushforwardFunctor_map
#print axioms finiteCoefficientFamilyCovariant_map_eq_pushforward
#print axioms finiteCoefficientFamilyCovariantPushforwardNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
