import CMDGCondensedCM4P3DerivedCM5R0RealBoxCechCoproduct

/-! The actual Hom complex on the sheafified box resolution
identifies with the full ordered simplex of radius labels with
constant coefficients. No artificial scalar differential. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.RealProductProjection
open CompactCover CompactCover.Dyadic RealProductCondensedColimit
variable (S : Profinite.{u}) (I : Type u)

abbrev ProbeHom := compactFreeFunctor.obj (profiniteToCompHaus.obj S) ⟶ discreteIntegerCoeff
abbrev BoxCochain (n : ℕ) := labels I n → ProbeHom S

def radiusHomAddEquiv (r : Radius I) :
    ProbeHom S ≃+ (compactFreeFunctor.obj (radiusBox S I r) ⟶ discreteIntegerCoeff) where
  toEquiv := radiusHomEquiv S I r
  map_add' g h := by
    change compactFreeFunctor.map (radiusProjection S I r) ≫ (g+h) =
      compactFreeFunctor.map (radiusProjection S I r) ≫ g +
      compactFreeFunctor.map (radiusProjection S I r) ≫ h
    rw [Preadditive.comp_add]

def boxScalar (n : ℕ) (f : boxCechTerm S I n ⟶ discreteIntegerCoeff) : BoxCochain S I n :=
  fun r => (radiusHomAddEquiv S I (intersectionRadius I n r)).symm
    (boxCechLeg S I n r ≫ f)

def boxScalarLift (n : ℕ) (c : BoxCochain S I n) :
    boxCechTerm S I n ⟶ discreteIntegerCoeff :=
  (boxCechCofanIsColimit S I n).desc (Cofan.mk _
    (fun r => radiusHomAddEquiv S I (intersectionRadius I n r) (c r)))

theorem boxScalarLift_leg (n : ℕ) (c : BoxCochain S I n) (r : labels I n) :
    boxCechLeg S I n r ≫ boxScalarLift S I n c =
      radiusHomAddEquiv S I (intersectionRadius I n r) (c r) :=
  (boxCechCofanIsColimit S I n).fac _ ⟨r⟩

theorem boxScalar_lift (n : ℕ) (c : BoxCochain S I n) :
    boxScalar S I n (boxScalarLift S I n c) = c := by
  funext r
  unfold boxScalar
  rw [boxScalarLift_leg,AddEquiv.symm_apply_apply]

theorem boxScalar_injective (n : ℕ) : Function.Injective (boxScalar S I n) := by
  intro f g h
  apply (boxCechCofanIsColimit S I n).hom_ext
  rintro ⟨r⟩
  exact (radiusHomAddEquiv S I (intersectionRadius I n r)).symm.injective (congrFun h r)

def scalarD (n : ℕ) (c : BoxCochain S I n) : BoxCochain S I (n+1) :=
  fun r => ∑ k : Fin (n+2), (-1 : ℤ)^(k : ℕ) • c (k.removeNth r)

theorem boxScalar_face (n : ℕ) (k : Fin (n+2))
    (f : boxCechTerm S I n ⟶ discreteIntegerCoeff) (r : labels I (n+1)) :
    boxScalar S I (n+1) (moduleSheafification.map (boxCechPshFace S I n k) ≫ f) r =
      boxScalar S I n f (k.removeNth r) := by
  unfold boxScalar
  apply (radiusHomAddEquiv S I (intersectionRadius I (n+1) r)).injective
  rw [AddEquiv.apply_symm_apply,← Category.assoc,boxCechLeg_face,Category.assoc]
  let e := radiusHomAddEquiv S I (intersectionRadius I n (k.removeNth r))
  let g := boxCechLeg S I n (k.removeNth r) ≫ f
  have h := radiusHomEquiv_natural S I (homOfLE (intersection_face_le I n k r)) (e.symm g)
  change compactFreeFunctor.map (radiusInclusion S I (homOfLE (intersection_face_le I n k r))) ≫
    e (e.symm g) = _
    at h
  rw [AddEquiv.apply_symm_apply] at h
  exact h

theorem boxScalar_add (n : ℕ) (f g : boxCechTerm S I n ⟶ discreteIntegerCoeff) :
    boxScalar S I n (f+g) = boxScalar S I n f + boxScalar S I n g := by
  funext r
  exact (by unfold boxScalar; rw [Preadditive.comp_add,map_add]; rfl)

def boxScalarAddHom (n : ℕ) :
    (boxCechTerm S I n ⟶ discreteIntegerCoeff) →+ BoxCochain S I n where
  toFun := boxScalar S I n
  map_zero' := by funext r; unfold boxScalar; rw [comp_zero,map_zero]; rfl
  map_add' := boxScalar_add S I n

theorem boxScalar_d (n : ℕ) (f : boxCechTerm S I n ⟶ discreteIntegerCoeff) :
    boxScalar S I (n+1) (boxCechD S I n ≫ f) =
      scalarD S I n (boxScalar S I n f) := by
  change boxScalarAddHom S I (n+1) (moduleSheafification.map (boxCechPshD S I n) ≫ f) = _
  unfold boxCechPshD
  rw [Functor.map_sum]
  simp only [Functor.map_zsmul,Preadditive.sum_comp,Preadditive.zsmul_comp,map_sum,map_zsmul]
  funext r
  rw [Finset.sum_apply]
  unfold scalarD
  apply Finset.sum_congr rfl
  intro k hk
  rw [Pi.smul_apply]
  exact congrArg (fun x : ProbeHom S => (-1 : ℤ)^(k : ℕ) • x)
    (boxScalar_face S I n k f r)

def zeroRadius : Radius I := ⟨fun _ => 0,fun _ => le_rfl⟩

def scalarH (n : ℕ) (c : BoxCochain S I (n+1)) : BoxCochain S I n :=
  fun r => c (Fin.cons (zeroRadius I) r)

theorem fullTuple_prepend_face {V : Type u} (v₀ : V)
    (n : ℕ) (r : Fin (n+2) → V) (k : Fin (n+2)) :
    k.succ.removeNth (Fin.cons v₀ r : Fin (n+3) → V) =
      (Fin.cons v₀ (k.removeNth r) : Fin (n+2) → V) := by
  funext i
  refine Fin.cases ?_ ?_ i
  · rfl
  · intro j
    change (Fin.cons v₀ r : Fin (n+3) → V) (k.succ.succAbove j.succ) = r (k.succAbove j)
    rw [Fin.succ_succAbove_succ]
    rfl

theorem fullTuple_contraction {V : Type u} {M : Type v} [AddCommGroup M]
    (v₀ : V) (n : ℕ) (c : (Fin (n+2) → V) → M) (r : Fin (n+2) → V) :
    (∑ k : Fin (n+2), (-1 : ℤ)^(k : ℕ) • c (Fin.cons v₀ (k.removeNth r))) +
    (∑ k : Fin (n+3), (-1 : ℤ)^(k : ℕ) • c (k.removeNth (Fin.cons v₀ r : Fin (n+3) → V))) = c r := by
  rw [Fin.sum_univ_succ (n := n+2)]
  simp only [Fin.val_zero,pow_zero,one_smul,Fin.val_succ,pow_succ,mul_neg,mul_one,
    neg_smul,fullTuple_prepend_face]
  have h0 : (0 : Fin (n+3)).removeNth (Fin.cons v₀ r : Fin (n+3) → V) = r := rfl
  rw [h0]
  rw [Finset.sum_neg_distrib]
  abel

theorem scalar_contraction (n : ℕ) (c : BoxCochain S I (n+1)) :
    scalarD S I n (scalarH S I n c) +
      scalarH S I (n+1) (scalarD S I (n+1) c) = c := by
  funext r
  exact fullTuple_contraction (zeroRadius I) n c r

theorem boxCech_homExact :
    AcyclicResolution.HomExact (boxCechResolution S I) discreteIntegerCoeff := by
  intro n f hf
  change boxCechD S I (n+1) ≫ f = 0 at hf
  have hc : scalarD S I (n+1) (boxScalar S I (n+1) f) = 0 := by
    rw [← boxScalar_d,hf]
    exact (boxScalarAddHom S I (n+2)).map_zero
  refine ⟨boxScalarLift S I n (scalarH S I n (boxScalar S I (n+1) f)),?_⟩
  apply boxScalar_injective S I (n+1)
  change boxScalar S I (n+1) (boxCechD S I n ≫ boxScalarLift S I n
    (scalarH S I n (boxScalar S I (n+1) f))) = _
  rw [boxScalar_d,boxScalar_lift]
  have h := scalar_contraction S I n (boxScalar S I (n+1) f)
  rw [hc] at h
  have hz : scalarH S I (n+1) (0 : BoxCochain S I (n+2)) = 0 := rfl
  rw [hz,add_zero] at h
  exact h

/-- Actual free relative real product, arbitrary I and profinite S:
all positive Ext against the discrete integers vanish. -/
theorem freeProbeReal_extPositive_zero (q : ℕ)
    (e : Abelian.Ext (freeProbeRealCocone S I).pt discreteIntegerCoeff (q+1)) : e=0 :=
  AcyclicResolution.target_extZero (boxCechResolution S I) discreteIntegerCoeff
    (boxCechTerm_extZero S I) (boxCech_homExact S I) q e

/-- The canonical projection induces a bijection in every nonnegative Ext degree. -/
theorem realProjection_ext_bijective (n : ℕ) :
    Function.Bijective (fun e : Abelian.Ext
      (compactFreeFunctor.obj (profiniteToCompHaus.obj S)) discreteIntegerCoeff n =>
      (Abelian.Ext.mk₀ (realProjection S I)).comp e (zero_add n)) := by
  cases n with
  | zero =>
    constructor
    · intro x y h
      apply Abelian.Ext.addEquiv₀.injective
      apply (realProjection_hom_bijective S I).1
      change realProjection S I ≫ Abelian.Ext.addEquiv₀ x =
        realProjection S I ≫ Abelian.Ext.addEquiv₀ y
      apply Abelian.Ext.addEquiv₀.symm.injective
      change Abelian.Ext.mk₀ _ = Abelian.Ext.mk₀ _
      rw [← Abelian.Ext.mk₀_comp_mk₀, ← Abelian.Ext.mk₀_comp_mk₀,
        Abelian.Ext.mk₀_addEquiv₀_apply, Abelian.Ext.mk₀_addEquiv₀_apply]
      exact h
    · intro x
      obtain ⟨g,hg⟩ := (realProjection_hom_bijective S I).2 (Abelian.Ext.addEquiv₀ x)
      refine ⟨Abelian.Ext.mk₀ g, ?_⟩
      change (Abelian.Ext.mk₀ (realProjection S I)).comp (Abelian.Ext.mk₀ g) _ = x
      change realProjection S I ≫ g = Abelian.Ext.addEquiv₀ x at hg
      rw [Abelian.Ext.mk₀_comp_mk₀,hg,Abelian.Ext.mk₀_addEquiv₀_apply]
  | succ q =>
    constructor
    · intro x y _
      rw [freeProfinite_extPositive_scalar_zero S q x,
        freeProfinite_extPositive_scalar_zero S q y]
    · intro x
      refine ⟨0,?_⟩
      change (Abelian.Ext.mk₀ (realProjection S I)).comp 0 _ = x
      rw [Abelian.Ext.comp_zero,freeProbeReal_extPositive_zero S I q x]

#print axioms realProjection_ext_bijective
#print axioms scalar_contraction
#print axioms boxCech_homExact
#print axioms freeProbeReal_extPositive_zero
end CMDG.CondensedCM5R0.RealProductProjection
