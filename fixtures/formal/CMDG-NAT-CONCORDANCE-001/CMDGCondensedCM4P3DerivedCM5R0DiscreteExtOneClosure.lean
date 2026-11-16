import CMDGCondensedCM4P3DerivedCM5R0CechTriplePointGeometry
import CMDGCondensedCM4P3DerivedCM5R0ProductTargetExtension

/-!
# CMDG CM5 — genuine discrete coefficient Ext¹ closure

The actual Stonean relation-to-kernel map is epi for any profinite test T.
Previous protected results prove that its induced relation cochains
satisfy the categorical triple identity, that the corresponding scalar
locally constant cocycles have continuous primitives, and that genuine
free-profinite morphisms into the discrete integer sheaf are equivalent
to locally constant integer functions.

Here we assemble those results, rather than merely restate an Ext
criterion: every actual kernel morphism into the discrete integral
coefficient object extends from K_T to F_(P(T)). Hence Ext¹(F_T,Z_disc)=0
for any (including infinite) profinite T. Product assembly then gives
Ext¹(F_T,∏ Z_disc)=0 without a false uniform finite-quotient condition.

Transport to the genuine solid target G_S remains explicitly
conditional on an actual categorical isomorphism G_S ≅ ∏ Z_disc.
Higher Ext and derived solidity are NOT established here.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- All points of the actual Stonean Čech pair pullback arise from
a genuine pair of source points with equal base images. -/
theorem stoneanCechPair_exists_related
    (T : Profinite.{u}) (q : stoneanPresentationCechPairs T) :
    ∃ (x y : Stonean.toProfinite.obj T.presentation)
      (h : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y),
      q = stoneanCechPairOfRelated T x y h := by
  let p := Profinite.presentation.π T
  let x := (pullback.fst p p).hom.hom q
  let y := (pullback.snd p p).hom.hom q
  have h : p.hom.hom x = p.hom.hom y := by
    have hcat : pullback.fst p p ≫ p = pullback.snd p p ≫ p :=
      pullback.condition
    have hh := congrArg
      (fun m : stoneanPresentationCechPairs T ⟶ T => m.hom.hom q) hcat
    exact hh
  refine ⟨x, y, h, ?_⟩
  apply stoneanCechPair_eq_of_endpoints T
  · exact (stoneanCechPairOfRelated_fst T x y h).symm
  · exact (stoneanCechPairOfRelated_snd T x y h).symm

/-- The real discrete-integer section equivalence preserves addition. -/
theorem freeProfiniteDiscreteIntegerHomScalarEquiv_add
    (X : Profinite.{u})
    (f g : (Condensed.profiniteFree Coeff).obj X ⟶
      discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv X (f + g) =
      freeProfiniteDiscreteIntegerHomScalarEquiv X f +
        freeProfiniteDiscreteIntegerHomScalarEquiv X g := by
  ext x
  rfl

/-- Transport the *actual* Stonean Čech morphism into the one-coordinate
locally constant difference, with the pinned lifted ring. -/
theorem stoneanCechDifference_discreteInteger_scalar
    (T : Profinite.{u})
    (g : (Condensed.profiniteFree Coeff).obj
      (Stonean.toProfinite.obj T.presentation) ⟶
        discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T)
        (stoneanCechDifference T ≫ g) =
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (Stonean.toProfinite.obj T.presentation) g).comap
          (pullback.fst (Profinite.presentation.π T)
            (Profinite.presentation.π T)).hom.hom -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (Stonean.toProfinite.obj T.presentation) g).comap
          (pullback.snd (Profinite.presentation.π T)
            (Profinite.presentation.π T)).hom.hom := by
  unfold stoneanCechDifference
  rw [Preadditive.sub_comp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]

/-- The genuine K_T-induced cochain satisfies the EXACT pointwise
cocycle condition required by the protected scalar H¹-zero theorem.
This is deduced from the actual categorical triple identity, not
postulated. -/
theorem stoneanCechKernelDiscreteScalar_cocycle
    (T : Profinite.{u})
    (f : stoneanPresentationKernel T ⟶ discreteIntegerCoeff) :
    ∀ (x y z : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z),
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T)
        (stoneanCechRelationToKernel T ≫ f))
          (stoneanCechPairOfRelated T x z (hxy.trans hyz)) =
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T)
        (stoneanCechRelationToKernel T ≫ f))
          (stoneanCechPairOfRelated T x y hxy) +
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T)
        (stoneanCechRelationToKernel T ≫ f))
          (stoneanCechPairOfRelated T y z hyz) := by
  let c := freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechPairs T)
      (stoneanCechRelationToKernel T ≫ f)
  have hcat := stoneanCechKernelCochain_triple T discreteIntegerCoeff f
  have hs := congrArg
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T)) hcat
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp] at hs
  intro x y z hxy hyz
  let t := stoneanCechTripleOfRelated T x y z hxy hyz
  have hv := congrArg
    (fun v : LocallyConstant (stoneanPresentationCechTriples T) ℤ => v t) hs
  change c ((stoneanCechTripleXZ T).hom.hom t) =
    c ((stoneanCechTripleXY T).hom.hom t) +
      c ((stoneanCechTripleYZ T).hom.hom t) at hv
  dsimp only [t] at hv
  rw [stoneanCechTripleOfRelated_xz T x y z hxy hyz,
    stoneanCechTripleOfRelated_xy T x y z hxy hyz,
    stoneanCechTripleOfRelated_yz T x y z hxy hyz] at hv
  exact hv

/-- Construct an ACTUAL extension K_T → Z_disc across the kernel
inclusion into F_(P(T)), for arbitrary profinite T. -/
theorem discreteInteger_kernelHom_extends
    (T : Profinite.{u})
    (f : stoneanPresentationKernel T ⟶ discreteIntegerCoeff) :
    ∃ g : (Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation) ⟶
          discreteIntegerCoeff,
      kernel.ι (freeStoneanPresentationMap T) ≫ g = f := by
  let R := stoneanPresentationCechPairs T
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let c : LocallyConstant R ℤ :=
    freeProfiniteDiscreteIntegerHomScalarEquiv R
      (stoneanCechRelationToKernel T ≫ f)
  obtain ⟨b, hb⟩ :=
    integerStoneanCechCocycle_hasPotential T c
      (stoneanCechKernelDiscreteScalar_cocycle T f)
  let g : (Condensed.profiniteFree Coeff).obj P ⟶
      discreteIntegerCoeff :=
    (freeProfiniteDiscreteIntegerHomScalarEquiv P).symm b
  have hdelta :
      stoneanCechDifference T ≫ g =
        stoneanCechRelationToKernel T ≫ f := by
    apply (freeProfiniteDiscreteIntegerHomScalarEquiv R).injective
    change freeProfiniteDiscreteIntegerHomScalarEquiv R
      (stoneanCechDifference T ≫ g) = c
    rw [stoneanCechDifference_discreteInteger_scalar,
      Equiv.apply_symm_apply]
    ext q
    obtain ⟨x, y, hxy, hq⟩ :=
      stoneanCechPair_exists_related T q
    subst q
    change b ((pullback.fst p p).hom.hom
      (stoneanCechPairOfRelated T x y hxy)) -
        b ((pullback.snd p p).hom.hom
          (stoneanCechPairOfRelated T x y hxy)) =
        c (stoneanCechPairOfRelated T x y hxy)
    rw [stoneanCechPairOfRelated_fst,
      stoneanCechPairOfRelated_snd]
    exact (hb x y hxy).symm
  letI : Epi (stoneanCechRelationToKernel T) :=
    stoneanCechRelationToKernel_epi T
  refine ⟨g, ?_⟩
  apply (cancel_epi (stoneanCechRelationToKernel T)).1
  calc
    stoneanCechRelationToKernel T ≫
        (kernel.ι (freeStoneanPresentationMap T) ≫ g) =
      (stoneanCechRelationToKernel T ≫
        kernel.ι (freeStoneanPresentationMap T)) ≫ g :=
        (Category.assoc _ _ _).symm
    _ = stoneanCechDifference T ≫ g := by
      rw [stoneanCechRelationToKernel_comp_ι]
    _ = stoneanCechRelationToKernel T ≫ f := hdelta

/-- Unconditional Ext¹(F_T, Z_disc) vanishing for arbitrary profinite T,
in the genuine condensed-module category. -/
theorem freeProfinite_extOne_discreteInteger_vanishes
    (T : Profinite.{u}) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      discreteIntegerCoeff 1, e = 0 := by
  apply (freeProfinite_extOne_vanishes_iff_kernel_hom_extends
    T discreteIntegerCoeff).2
  intro f
  exact discreteInteger_kernelHom_extends T f

/-- Unconditional Ext¹(F_T,∏ Z_disc)=0 for arbitrary profinite T
and arbitrary coefficient index type. -/
theorem freeProfinite_extOne_discreteProduct_vanishes
    (T : Profinite.{u}) {ι : Type (u + 1)} :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      (∏ᶜ (fun _ : ι => discreteIntegerCoeff)) 1, e = 0 := by
  apply freeProfinite_extOne_product_vanishes_of_components T
    (fun _ : ι => discreteIntegerCoeff)
  intro i
  exact freeProfinite_extOne_discreteInteger_vanishes T

/-- Explicit CONDITIONAL transport to the genuine G_S. The
categorical product model is required and not proved by this theorem. -/
theorem freeProfinite_extOne_solid_vanishes_of_discreteProductModel
    (T S : Profinite.{u}) {ι : Type (u + 1)}
    (e : underivedObject S ≅
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    ∀ x : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T) (underivedObject S) 1,
      x = 0 := by
  exact freeProfinite_extOne_solid_vanishes_of_productModel
    T S discreteIntegerCoeff e
    (freeProfinite_extOne_discreteInteger_vanishes T)

#print axioms stoneanCechPair_exists_related
#print axioms freeProfiniteDiscreteIntegerHomScalarEquiv_add
#print axioms stoneanCechDifference_discreteInteger_scalar
#print axioms stoneanCechKernelDiscreteScalar_cocycle
#print axioms discreteInteger_kernelHom_extends
#print axioms freeProfinite_extOne_discreteInteger_vanishes
#print axioms freeProfinite_extOne_discreteProduct_vanishes
#print axioms freeProfinite_extOne_solid_vanishes_of_discreteProductModel

end CMDG.CondensedCM5R0
