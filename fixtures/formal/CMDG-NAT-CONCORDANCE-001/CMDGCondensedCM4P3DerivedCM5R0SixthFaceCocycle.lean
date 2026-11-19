import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthBoundaryScalarHom
import CMDGCondensedCM4P3DerivedCM5R0ExtFourFourthRelationCriterion

/-!
# CMDG CM5 Ext4: genuine six-face cancellation into fourth relation

The actual fivefold free condensed module receives an alternating
six-point singleton chain. Its fifth differential is zero, so
the resulting fivefold scalar cochain on the genuine fourth-relation
kernel satisfies the required six-face cocycle condition automatically.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Evaluate the true fifth free-module boundary at a singleton of
the actual closed fivefold Čech Profinite object. -/
theorem stoneanCechExplicitFifthBoundary_pointFormula
    (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap
        (stoneanCechExplicitQuintupleProfinite T) r) ≫
      stoneanCechExplicitFifthBoundary T =
    (((((Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap
        (stoneanCechExplicitQuadrupleProfinite T)
        ((quintupleFace0 T).hom.hom r)) -
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap
        (stoneanCechExplicitQuadrupleProfinite T)
        ((quintupleFace1 T).hom.hom r))) +
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap
        (stoneanCechExplicitQuadrupleProfinite T)
        ((quintupleFace2 T).hom.hom r))) -
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap
        (stoneanCechExplicitQuadrupleProfinite T)
        ((quintupleFace3 T).hom.hom r))) +
      (Condensed.profiniteFree Coeff).map
      (cm5SingletonPointMap
        (stoneanCechExplicitQuadrupleProfinite T)
        ((quintupleFace4 T).hom.hom r))) := by
  unfold stoneanCechExplicitFifthBoundary
  simp only [Preadditive.comp_sub,Preadditive.comp_add,
    ← Functor.map_comp, cm5SingletonPointMap_comp]

/-- Six-point alternating free condensed-module singleton chain
on the actual true closed Čech fivefold relation. -/
noncomputable def stoneanCechSixthPointAlternatingFreeMap
    (T : Profinite.{u})
    (x y z w v r : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v)
    (hvr : (Profinite.presentation.π T).hom.hom v =
      (Profinite.presentation.π T).hom.hom r) :
    ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) := by
  let Q := stoneanCechExplicitQuintupleProfinite T
  let r0 : Q := ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩
  let r1 : Q := ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩
  let r2 : Q := ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩
  let r3 : Q := ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩
  let r4 : Q := ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩
  let r5 : Q := ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩
  let a (q : Q) :=
    (Condensed.profiniteFree Coeff).map (cm5SingletonPointMap Q q)
  exact (((((a r0 - a r1) + a r2) - a r3) + a r4) - a r5)

private theorem quintupleFace0_atClosedSixth (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace0 T).hom.hom r =
      (⟨(r.val.2.1,(r.val.2.2.1,
        (r.val.2.2.2.1,r.val.2.2.2.2))),
          ⟨r.property.2.1,r.property.2.2.1,r.property.2.2.2⟩⟩ :
            stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace1_atClosedSixth (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace1 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.2.1,(r.val.2.2.2.1,r.val.2.2.2.2))),
        ⟨r.property.1.trans r.property.2.1,r.property.2.2.1,r.property.2.2.2⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace2_atClosedSixth (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace2 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.1,(r.val.2.2.2.1,r.val.2.2.2.2))),
        ⟨r.property.1,r.property.2.1.trans r.property.2.2.1,r.property.2.2.2⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace3_atClosedSixth (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace3 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.1,(r.val.2.2.1,r.val.2.2.2.2))),
        ⟨r.property.1,r.property.2.1,r.property.2.2.1.trans r.property.2.2.2⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace4_atClosedSixth (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace4 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.1,(r.val.2.2.1,r.val.2.2.2.1))),
        ⟨r.property.1,r.property.2.1,r.property.2.2.1⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl


/-- Genuine degree-four six-face boundary-of-boundary cancellation. -/
theorem stoneanCechSixthPointAlternating_comp_explicitFifth_zero
    (T : Profinite.{u})
    (x y z w v r : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v)
    (hvr : (Profinite.presentation.π T).hom.hom v =
      (Profinite.presentation.π T).hom.hom r) :
    stoneanCechSixthPointAlternatingFreeMap
      T x y z w v r hxy hyz hzw hwv hvr ≫
      stoneanCechExplicitFifthBoundary T = 0 := by
  let Q := stoneanCechExplicitQuintupleProfinite T
  let r0 : Q := ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩
  let r1 : Q := ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩
  let r2 : Q := ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩
  let r3 : Q := ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩
  let r4 : Q := ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩
  let r5 : Q := ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩
  let a (q : Q) :=
    (Condensed.profiniteFree Coeff).map (cm5SingletonPointMap Q q)

  have h01 :
      (quintupleFace0 T).hom.hom r0 =
      (quintupleFace0 T).hom.hom r1 := by
    apply Subtype.ext
    rfl
  have h02 :
      (quintupleFace1 T).hom.hom r0 =
      (quintupleFace0 T).hom.hom r2 := by
    apply Subtype.ext
    rfl
  have h03 :
      (quintupleFace2 T).hom.hom r0 =
      (quintupleFace0 T).hom.hom r3 := by
    apply Subtype.ext
    rfl
  have h04 :
      (quintupleFace3 T).hom.hom r0 =
      (quintupleFace0 T).hom.hom r4 := by
    apply Subtype.ext
    rfl
  have h05 :
      (quintupleFace4 T).hom.hom r0 =
      (quintupleFace0 T).hom.hom r5 := by
    apply Subtype.ext
    rfl
  have h12 :
      (quintupleFace1 T).hom.hom r1 =
      (quintupleFace1 T).hom.hom r2 := by
    apply Subtype.ext
    rfl
  have h13 :
      (quintupleFace2 T).hom.hom r1 =
      (quintupleFace1 T).hom.hom r3 := by
    apply Subtype.ext
    rfl
  have h14 :
      (quintupleFace3 T).hom.hom r1 =
      (quintupleFace1 T).hom.hom r4 := by
    apply Subtype.ext
    rfl
  have h15 :
      (quintupleFace4 T).hom.hom r1 =
      (quintupleFace1 T).hom.hom r5 := by
    apply Subtype.ext
    rfl
  have h23 :
      (quintupleFace2 T).hom.hom r2 =
      (quintupleFace2 T).hom.hom r3 := by
    apply Subtype.ext
    rfl
  have h24 :
      (quintupleFace3 T).hom.hom r2 =
      (quintupleFace2 T).hom.hom r4 := by
    apply Subtype.ext
    rfl
  have h25 :
      (quintupleFace4 T).hom.hom r2 =
      (quintupleFace2 T).hom.hom r5 := by
    apply Subtype.ext
    rfl
  have h34 :
      (quintupleFace3 T).hom.hom r3 =
      (quintupleFace3 T).hom.hom r4 := by
    apply Subtype.ext
    rfl
  have h35 :
      (quintupleFace4 T).hom.hom r3 =
      (quintupleFace3 T).hom.hom r5 := by
    apply Subtype.ext
    rfl
  have h45 :
      (quintupleFace4 T).hom.hom r4 =
      (quintupleFace4 T).hom.hom r5 := by
    apply Subtype.ext
    rfl
  change (((((a r0 - a r1) + a r2) - a r3) + a r4) - a r5) ≫
    stoneanCechExplicitFifthBoundary T = 0
  simp only [Preadditive.add_comp, Preadditive.sub_comp]
  rw [stoneanCechExplicitFifthBoundary_pointFormula T r0,
    stoneanCechExplicitFifthBoundary_pointFormula T r1,
    stoneanCechExplicitFifthBoundary_pointFormula T r2,
    stoneanCechExplicitFifthBoundary_pointFormula T r3,
    stoneanCechExplicitFifthBoundary_pointFormula T r4,
    stoneanCechExplicitFifthBoundary_pointFormula T r5]
  simp only [h01, h02, h03, h04, h05, h12, h13, h14, h15, h23, h24, h25, h34, h35, h45]
  abel


/-- Exact sixth-point cancellation through the ACTUAL fifth boundary
whose target is the fourth categorical Čech pullback. -/
theorem stoneanCechSixthPointAlternating_comp_fifthBoundary_zero
    (T : Profinite.{u})
    (x y z w v r : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v)
    (hvr : (Profinite.presentation.π T).hom.hom v =
      (Profinite.presentation.π T).hom.hom r) :
    stoneanCechSixthPointAlternatingFreeMap
      T x y z w v r hxy hyz hzw hwv hvr ≫
      stoneanCechFifthBoundary T = 0 := by
  rw [stoneanCechFifthBoundary_explicit_factor,
    ← Category.assoc,
    stoneanCechSixthPointAlternating_comp_explicitFifth_zero,
    zero_comp]

/-- The six-point alternating map lands in the actual fourth
relation with ZERO composition; detect the equality through the
genuine monomorphism kernel inclusion. -/
theorem stoneanCechSixthPointAlternating_comp_fourthRelation_zero
    (T : Profinite.{u})
    (x y z w v r : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z)
    (hzw : (Profinite.presentation.π T).hom.hom z =
      (Profinite.presentation.π T).hom.hom w)
    (hwv : (Profinite.presentation.π T).hom.hom w =
      (Profinite.presentation.π T).hom.hom v)
    (hvr : (Profinite.presentation.π T).hom.hom v =
      (Profinite.presentation.π T).hom.hom r) :
    stoneanCechSixthPointAlternatingFreeMap
      T x y z w v r hxy hyz hzw hwv hvr ≫
      stoneanCechFifthToFourthRelation T = 0 := by
  apply (cancel_mono
    (kernel.ι (stoneanCechFourthToThirdRelation T))).1
  rw [Category.assoc,
    stoneanCechFifthToFourthRelation_comp_inclusion,
    zero_comp]
  exact stoneanCechSixthPointAlternating_comp_fifthBoundary_zero
    T x y z w v r hxy hyz hzw hwv hvr

#print axioms stoneanCechSixthPointAlternating_comp_fourthRelation_zero

private theorem sixAlternatingScalar_zero
    {X Y : Profinite.{u}}
    (a0 a1 a2 a3 a4 a5 :
      ((Condensed.profiniteFree Coeff).obj X) ⟶
      ((Condensed.profiniteFree Coeff).obj Y))
    (g : ((Condensed.profiniteFree Coeff).obj Y) ⟶ discreteIntegerCoeff)
    (pt : X)
    (hz : (((((a0 - a1) + a2) - a3) + a4) - a5) ≫ g = 0) :
    (((((freeProfiniteDiscreteIntegerHomScalarEquiv X (a0 ≫ g) pt -
      freeProfiniteDiscreteIntegerHomScalarEquiv X (a1 ≫ g) pt) +
      freeProfiniteDiscreteIntegerHomScalarEquiv X (a2 ≫ g) pt) -
      freeProfiniteDiscreteIntegerHomScalarEquiv X (a3 ≫ g) pt) +
      freeProfiniteDiscreteIntegerHomScalarEquiv X (a4 ≫ g) pt) -
      freeProfiniteDiscreteIntegerHomScalarEquiv X (a5 ≫ g) pt) = 0 := by
  have h := congrArg (fun k : ((Condensed.profiniteFree Coeff).obj X) ⟶
    discreteIntegerCoeff =>
      (freeProfiniteDiscreteIntegerHomScalarEquiv X k) pt) hz
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub] at h
  have hz0 : (freeProfiniteDiscreteIntegerHomScalarEquiv X
    (0 : ((Condensed.profiniteFree Coeff).obj X) ⟶
      discreteIntegerCoeff)) pt = 0 := rfl
  rw [hz0] at h
  simpa only [LocallyConstant.add_apply, LocallyConstant.sub_apply] using h

private theorem stoneanCechSixthProduct_eval_atSingleton
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (i : ι) (r : stoneanCechExplicitQuintupleProfinite T) :
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (Profinite.of PUnit.{u + 1})
      ((Condensed.profiniteFree Coeff).map
        (cm5SingletonPointMap
          (stoneanCechExplicitQuintupleProfinite T) r) ≫
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)))
      PUnit.unit =
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) h i) r := by
  let Q := stoneanCechExplicitQuintupleProfinite T
  let point := cm5SingletonPointMap Q r
  calc
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (Profinite.of PUnit.{u + 1})
      ((Condensed.profiniteFree Coeff).map point ≫
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))) PUnit.unit =
      (freeProfiniteDiscreteIntegerHomScalarEquiv Q
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))
          (point.hom.hom PUnit.unit) := by
            rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
            rfl
    _ = (freeProfiniteDiscreteProductHomScalarEquiv Q h i) r := by
        unfold point cm5SingletonPointMap
        rfl


/-- A six-term vanishing of genuine free-module singleton maps forces
the exact six-face scalar product Čech cocycle, coordinatewise, on
every genuine closed related sextuple. -/
theorem stoneanCechClosedProductSixCocycle_ofSixthZero
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hz : ∀ (x y z w v r : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w)
      (hwv : (Profinite.presentation.π T).hom.hom w =
        (Profinite.presentation.π T).hom.hom v)
      (hvr : (Profinite.presentation.π T).hom.hom v =
        (Profinite.presentation.π T).hom.hom r),
      stoneanCechSixthPointAlternatingFreeMap
        T x y z w v r hxy hyz hzw hwv hvr ≫ h = 0) :
    stoneanCechClosedProductSixCocycle T h := by
  intro i x y z w v r hxy hyz hzw hwv hvr
  let Q := stoneanCechExplicitQuintupleProfinite T
  let r0 : Q := ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩
  let r1 : Q := ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩
  let r2 : Q := ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩
  let r3 : Q := ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩
  let r4 : Q := ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩
  let r5 : Q := ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩
  let a (q : Q) :=
    (Condensed.profiniteFree Coeff).map (cm5SingletonPointMap Q q)
  have hz_i := congrArg
    (fun k : ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff) =>
      k ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
    (hz x y z w v r hxy hyz hzw hwv hvr)
  rw [Category.assoc, zero_comp] at hz_i
  have hz_i' :
      (((((a r0 - a r1) + a r2) - a r3) + a r4) - a r5) ≫
      (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i) = 0 := by
    exact hz_i
  have hs := sixAlternatingScalar_zero
    (a r0) (a r1) (a r2) (a r3) (a r4) (a r5)
    (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
    PUnit.unit hz_i'
  rw [stoneanCechSixthProduct_eval_atSingleton T h i r0,
    stoneanCechSixthProduct_eval_atSingleton T h i r1,
    stoneanCechSixthProduct_eval_atSingleton T h i r2,
    stoneanCechSixthProduct_eval_atSingleton T h i r3,
    stoneanCechSixthProduct_eval_atSingleton T h i r4,
    stoneanCechSixthProduct_eval_atSingleton T h i r5] at hs
  exact hs

/-- Every *actual* fourth-relation Hom into an arbitrary categorical
product of discrete integer coefficients automatically satisfies the
true six-face Čech condition. No cocycle hypothesis is supplied. -/
theorem stoneanCechFourthRelation_product_sixCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : stoneanCechFourthRelationKernel T ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    stoneanCechClosedProductSixCocycle T
      (stoneanCechFifthToFourthRelation T ≫ f) := by
  apply stoneanCechClosedProductSixCocycle_ofSixthZero T
    (stoneanCechFifthToFourthRelation T ≫ f)
  intro x y z w v r hxy hyz hzw hwv hvr
  calc
    stoneanCechSixthPointAlternatingFreeMap
      T x y z w v r hxy hyz hzw hwv hvr ≫
      (stoneanCechFifthToFourthRelation T ≫ f) =
      (stoneanCechSixthPointAlternatingFreeMap
        T x y z w v r hxy hyz hzw hwv hvr ≫
          stoneanCechFifthToFourthRelation T) ≫ f :=
            (Category.assoc _ _ _).symm
    _ = (0 : ((Condensed.profiniteFree Coeff).obj
      (Profinite.of PUnit.{u + 1})) ⟶
        stoneanCechFourthRelationKernel T) ≫ f := by
          rw [stoneanCechSixthPointAlternating_comp_fourthRelation_zero]
    _ = 0 := zero_comp

#print axioms stoneanCechFourthRelation_product_sixCocycle
#print axioms stoneanCechClosedProductSixCocycle_ofSixthZero
#print axioms sixAlternatingScalar_zero
#print axioms stoneanCechSixthProduct_eval_atSingleton
#print axioms stoneanCechSixthPointAlternating_comp_explicitFifth_zero
end CMDG.CondensedCM5R0
