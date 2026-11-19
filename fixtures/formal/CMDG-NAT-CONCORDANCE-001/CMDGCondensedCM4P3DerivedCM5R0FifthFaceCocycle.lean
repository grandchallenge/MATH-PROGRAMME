import CMDGCondensedCM4P3DerivedCM5R0GenuineFourthBoundaryScalarHom
import CMDGCondensedCM4P3DerivedCM5R0GenuineFourthCechBoundary

/-!
# CM5: true fifth-point cancellation into the genuine third relation

Do not infer the five-face cocycle condition from scalar H3 alone.
Prove it by the actual signed categorical Čech fourth differential,
pointwise on true Profinite pullbacks; descend through its genuine
third-relation kernel factorization.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- An actual categorical fourth Čech point has precisely the
four-term signed free-condensed-module boundary, not merely a scalar
analogue or a setwise construction. -/
theorem stoneanCechFourthBoundary_pointFormula
    (T : Profinite.{u})
    (r : stoneanCechExplicitQuadrupleProfinite T) :
    (Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap (stoneanPresentationCechQuadruples T)
          ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r)) ≫
      stoneanCechFourthBoundary T =
    (((Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T
          r.val.2.1 r.val.2.2.1 r.val.2.2.2
          r.property.2.1 r.property.2.2)) -
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T
          r.val.1 r.val.2.2.1 r.val.2.2.2
          (r.property.1.trans r.property.2.1) r.property.2.2))) +
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T
          r.val.1 r.val.2.1 r.val.2.2.2
          r.property.1 (r.property.2.1.trans r.property.2.2)))) -
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap (stoneanPresentationCechTriples T)
        (stoneanCechTripleOfRelated T
          r.val.1 r.val.2.1 r.val.2.2.1
          r.property.1 r.property.2.1)) := by
  unfold stoneanCechFourthBoundary
  simp only [Preadditive.comp_sub, Preadditive.comp_add,
    ← Functor.map_comp, cm5SingletonPointMap_comp]
  rw [stoneanCechExplicitQuadruple_yzw_atPoint,
    stoneanCechExplicitQuadruple_xzw_atPoint,
    stoneanCechExplicitQuadruple_xyw_atPoint]
  congr 1
  congr 1
  congr 1
  exact stoneanCechExplicitQuadruple_xyz_atPoint T r


/-- Genuine five-vertex alternating fourth-chain map, not an
informal combinatorial or scalar surrogate. -/
noncomputable def stoneanCechFifthPointAlternatingFreeMap
    (T : Profinite.{u})
    (x y z w v : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v) :
    ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) := by
  let Q := stoneanPresentationCechQuadruples T
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let r0 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩
  let r1 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩
  let r2 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩
  let r3 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩
  let r4 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩
  let a (r : stoneanCechExplicitQuadrupleProfinite T) :=
    (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap Q (A.hom.hom r))
  exact (((a r0 - a r1) + a r2) - a r3) + a r4

theorem stoneanCechFifthPointAlternating_comp_fourthBoundary_zero
    (T : Profinite.{u})
    (x y z w v : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v) :
    stoneanCechFifthPointAlternatingFreeMap
      T x y z w v hxy hyz hzw hwv ≫
        stoneanCechFourthBoundary T = 0 := by
  unfold stoneanCechFifthPointAlternatingFreeMap
  simp only [Preadditive.add_comp, Preadditive.sub_comp]
  rw [stoneanCechFourthBoundary_pointFormula,
    stoneanCechFourthBoundary_pointFormula,
    stoneanCechFourthBoundary_pointFormula,
    stoneanCechFourthBoundary_pointFormula,
    stoneanCechFourthBoundary_pointFormula]
  dsimp only
  abel


/-- A scalar product-coordinate evaluation on the singleton point
is exactly evaluation on the genuine closed quadruple after applying
its categorical Profinite isomorphism. -/
private theorem stoneanCechClosedProduct_eval_atSingleton
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (i : ι) (r : stoneanCechExplicitQuadrupleProfinite T) :
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (Profinite.of PUnit.{u + 1})
      ((Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap (stoneanPresentationCechQuadruples T)
          ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r)) ≫
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)))
      PUnit.unit =
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T)
      ((Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuadrupleToAbstract T) ≫ h) i) r := by
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let point := cm5SingletonPointMap
    (stoneanPresentationCechQuadruples T) (A.hom.hom r)
  calc
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (Profinite.of PUnit.{u + 1})
      ((Condensed.profiniteFree Coeff).map point ≫
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))) PUnit.unit =
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechQuadruples T)
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))
          (point.hom.hom PUnit.unit) := by
            rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
            rfl
    _ = (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T)
      ((Condensed.profiniteFree Coeff).map A ≫ h) i) r := by
        rw [freeProfiniteDiscreteProductHomScalarEquiv_precomp]
        rfl


/-- A five-term identity of actual condensed-module maps implies
the correctly signed integer identity in every scalar coefficient. -/
private theorem fiveAlternatingScalar_zero
    {X Y : Profinite.{u}}
    (a0 a1 a2 a3 a4 :
      ((Condensed.profiniteFree Coeff).obj X) ⟶
      ((Condensed.profiniteFree Coeff).obj Y))
    (g : ((Condensed.profiniteFree Coeff).obj Y) ⟶ discreteIntegerCoeff)
    (u : X)
    (hz : ((((a0 - a1) + a2) - a3) + a4) ≫ g = 0) :
    (((((freeProfiniteDiscreteIntegerHomScalarEquiv X (a0 ≫ g)) u -
       (freeProfiniteDiscreteIntegerHomScalarEquiv X (a1 ≫ g)) u) +
       (freeProfiniteDiscreteIntegerHomScalarEquiv X (a2 ≫ g)) u) -
       (freeProfiniteDiscreteIntegerHomScalarEquiv X (a3 ≫ g)) u) +
       (freeProfiniteDiscreteIntegerHomScalarEquiv X (a4 ≫ g)) u) = 0 := by
  have h := congrArg (fun k : ((Condensed.profiniteFree Coeff).obj X) ⟶
      discreteIntegerCoeff =>
        (freeProfiniteDiscreteIntegerHomScalarEquiv X k) u) hz
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub] at h
  have hz0 : (freeProfiniteDiscreteIntegerHomScalarEquiv X
      (0 : ((Condensed.profiniteFree Coeff).obj X) ⟶
        discreteIntegerCoeff)) u = 0 := rfl
  rw [hz0] at h
  simpa only [LocallyConstant.add_apply, LocallyConstant.sub_apply] using h


/-- If the genuine five-point alternating fourth-chain map annihilates
an actual product-valued categorical cochain, that cochain obeys the
full five-face scalar Čech cocycle equation on the true closed relation,
with no additional cocycle assumption. -/
theorem stoneanCechClosedProductFiveCocycle_ofFifthZero
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hz : ∀ (x y z w v : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w)
      (hwv : (Profinite.presentation.π T).hom.hom w =
        (Profinite.presentation.π T).hom.hom v),
      stoneanCechFifthPointAlternatingFreeMap
        T x y z w v hxy hyz hzw hwv ≫ h = 0) :
    stoneanCechClosedProductFiveCocycle T
      ((Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuadrupleToAbstract T) ≫ h) := by
  intro i x y z w v hxy hyz hzw hwv
  let Q := stoneanPresentationCechQuadruples T
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let r0 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩
  let r1 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩
  let r2 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩
  let r3 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩
  let r4 : stoneanCechExplicitQuadrupleProfinite T :=
    ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩
  let a (r : stoneanCechExplicitQuadrupleProfinite T) :=
    (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap Q (A.hom.hom r))
  have hz_i := congrArg (fun k : ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff) =>
      k ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
    (hz x y z w v hxy hyz hzw hwv)
  rw [Category.assoc, zero_comp] at hz_i
  have hz_i' : ((((a r0 - a r1) + a r2) - a r3) + a r4) ≫
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i) = 0 := by
    exact hz_i
  have hs := fiveAlternatingScalar_zero
    (a r0) (a r1) (a r2) (a r3) (a r4)
    (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
    PUnit.unit hz_i'
  rw [stoneanCechClosedProduct_eval_atSingleton T h i r0,
    stoneanCechClosedProduct_eval_atSingleton T h i r1,
    stoneanCechClosedProduct_eval_atSingleton T h i r2,
    stoneanCechClosedProduct_eval_atSingleton T h i r3,
    stoneanCechClosedProduct_eval_atSingleton T h i r4] at hs
  exact hs


/-- The full five-point alternating map annihilates the genuine
third-relation factorization of the fourth Čech differential.
Monicity of the actual kernel inclusion is used; no scalar shortcut. -/
theorem stoneanCechFifthPointAlternating_comp_thirdRelation_zero
    (T : Profinite.{u})
    (x y z w v : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v) :
    stoneanCechFifthPointAlternatingFreeMap
      T x y z w v hxy hyz hzw hwv ≫
      stoneanCechFourthToThirdRelation T = 0 := by
  apply (cancel_mono
    (kernel.ι (stoneanCechTripleToSecondRelation T))).1
  calc
    (stoneanCechFifthPointAlternatingFreeMap
      T x y z w v hxy hyz hzw hwv ≫
        stoneanCechFourthToThirdRelation T) ≫
      kernel.ι (stoneanCechTripleToSecondRelation T) =
    stoneanCechFifthPointAlternatingFreeMap
      T x y z w v hxy hyz hzw hwv ≫
      (stoneanCechFourthToThirdRelation T ≫
        kernel.ι (stoneanCechTripleToSecondRelation T)) :=
        Category.assoc _ _ _
    _ = stoneanCechFifthPointAlternatingFreeMap
      T x y z w v hxy hyz hzw hwv ≫
        stoneanCechFourthBoundary T := by
          rw [stoneanCechFourthToThirdRelation_comp_inclusion]
    _ = 0 := stoneanCechFifthPointAlternating_comp_fourthBoundary_zero
      T x y z w v hxy hyz hzw hwv
    _ = (0 : ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
      stoneanCechThirdRelationKernel T) ≫
      kernel.ι (stoneanCechTripleToSecondRelation T) := by simp

/-- The five-point scalar cocycle hypothesis required for true
categorical H³ exactness is AUTOMATIC for arbitrary actual morphisms
from the genuine third-relation kernel to any categorical product
of discrete integer coefficients. -/
theorem stoneanCechThirdRelation_product_fiveCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : stoneanCechThirdRelationKernel T ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    stoneanCechClosedProductFiveCocycle T
      ((Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuadrupleToAbstract T) ≫
        (stoneanCechFourthToThirdRelation T ≫ f)) := by
  apply stoneanCechClosedProductFiveCocycle_ofFifthZero T
    (stoneanCechFourthToThirdRelation T ≫ f)
  intro x y z w v hxy hyz hzw hwv
  calc
    stoneanCechFifthPointAlternatingFreeMap
      T x y z w v hxy hyz hzw hwv ≫
      (stoneanCechFourthToThirdRelation T ≫ f) =
      (stoneanCechFifthPointAlternatingFreeMap
        T x y z w v hxy hyz hzw hwv ≫
        stoneanCechFourthToThirdRelation T) ≫ f :=
          (Category.assoc _ _ _).symm
    _ = (0 : ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
      stoneanCechThirdRelationKernel T) ≫ f := by
        rw [stoneanCechFifthPointAlternating_comp_thirdRelation_zero]
    _ = 0 := zero_comp

#print axioms stoneanCechFifthPointAlternating_comp_thirdRelation_zero
#print axioms stoneanCechThirdRelation_product_fiveCocycle
#print axioms stoneanCechClosedProductFiveCocycle_ofFifthZero
#print axioms fiveAlternatingScalar_zero
#print axioms stoneanCechClosedProduct_eval_atSingleton
#print axioms stoneanCechFifthPointAlternating_comp_fourthBoundary_zero
#print axioms stoneanCechFourthBoundary_pointFormula
end CMDG.CondensedCM5R0
