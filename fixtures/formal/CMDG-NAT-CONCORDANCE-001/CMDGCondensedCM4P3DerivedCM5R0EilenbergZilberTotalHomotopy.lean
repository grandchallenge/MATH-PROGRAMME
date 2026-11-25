import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberShuffle

/-! Totalization preserves a homotopy in the horizontal chain direction.
The vertical terms cancel using the Koszul sign. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy

abbrev BC := HomologicalComplex₂ ZMod c c

def liftDegree {K L : BC} (s : ∀ p, K.X p ⟶ L.X (p+1)) (n : ℕ) :
    (K.total c).X n ⟶ (L.total c).X (n+1) :=
  K.totalDesc (fun p q h => (s p).f q ≫ L.ιTotal c (p+1) q (n+1) (by
    change p+q=n at h
    change p+1+q=n+1
    omega))

@[reassoc]
theorem liftDegree_summand {K L : BC} (s : ∀ p, K.X p ⟶ L.X (p+1))
    (n p q : ℕ) (h : p+q=n) :
    K.ιTotal c p q n h ≫ liftDegree s n =
      (s p).f q ≫ L.ιTotal c (p+1) q (n+1) (by change p+1+q=n+1; omega) := by
  unfold liftDegree
  rw [HomologicalComplex₂.ι_totalDesc]

-- Explicit horizontal/vertical components, including the boundary axes.
@[reassoc]
theorem horizontal_succ (K : BC) (p q n m : ℕ) (h : p+1+q=n) (h' : p+q=m) :
    K.ιTotal c (p+1) q n h ≫ K.D₁ c n m =
      (K.d (p+1) p).f q ≫ K.ιTotal c p q m h' := by
  rw [HomologicalComplex₂.ι_D₁, HomologicalComplex₂.d₁_eq K c (i₁ := p+1) (i₁' := p) (by rfl) q m h']
  change (1 : ℤˣ) • _ = _
  rw [one_smul]

@[reassoc]
theorem vertical_succ (K : BC) (p q n m : ℕ) (h : p+(q+1)=n) (h' : p+q=m) :
    K.ιTotal c p (q+1) n h ≫ K.D₂ c n m =
      (-1 : ℤ)^p • ((K.X p).d (q+1) q ≫ K.ιTotal c p q m h') := by
  rw [HomologicalComplex₂.ι_D₂, HomologicalComplex₂.d₂_eq K c p (i₂ := q+1) (i₂' := q) (by rfl) m h']
  rfl

@[reassoc]
theorem horizontal_axis (K : BC) (q n m : ℕ) (h : 0+q=n) :
    K.ιTotal c 0 q n h ≫ K.D₁ c n m = 0 := by
  rw [HomologicalComplex₂.ι_D₁]
  exact HomologicalComplex₂.d₁_eq_zero K c 0 q m (by decide)

@[reassoc]
theorem vertical_axis (K : BC) (p n m : ℕ) (h : p+0=n) :
    K.ιTotal c p 0 n h ≫ K.D₂ c n m = 0 := by
  rw [HomologicalComplex₂.ι_D₂]
  exact HomologicalComplex₂.d₂_eq_zero K c p 0 m (by decide)

set_option backward.isDefEq.respectTransparency false in
theorem lift_horizontal {K L : BC} (s : ∀ p, K.X p ⟶ L.X (p+1))
    (p q n : ℕ) (h : p+q=n) :
    K.ιTotal c p q n h ≫ liftDegree s n ≫ L.D₁ c (n+1) n =
      ((s p).f q ≫ (L.d (p+1) p).f q) ≫ L.ιTotal c p q n h := by
  rw [liftDegree_summand_assoc, horizontal_succ, Category.assoc]

set_option backward.isDefEq.respectTransparency false in
theorem lift_vertical_cancel {K L : BC} (s : ∀ p, K.X p ⟶ L.X (p+1))
    (n : ℕ) :
    (show (K.total c).X (n+1) ⟶ (L.total c).X (n+1) from K.D₂ c (n+1) n ≫ liftDegree s n) +
      (show (K.total c).X (n+1) ⟶ (L.total c).X (n+1) from liftDegree s (n+1) ≫ L.D₂ c (n+2) (n+1)) = 0 := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=n+1 at h
  rw [Preadditive.comp_add, comp_zero, ← Category.assoc, liftDegree_summand_assoc]
  cases q with
  | zero =>
    rw [vertical_axis,zero_comp,vertical_axis,comp_zero,add_zero]
  | succ q =>
    rw [vertical_succ K p q (n+1) n h (by omega)]
    rw [Preadditive.zsmul_comp,Category.assoc,liftDegree_summand]
    rw [vertical_succ L (p+1) q (n+2) (n+1) (by omega) (by omega),Preadditive.comp_zsmul]
    rw [← Category.assoc ((s p).f (q+1)), (s p).comm (q+1) q]
    rw [Category.assoc,pow_succ,mul_neg,mul_one,neg_smul,add_neg_cancel]

set_option backward.isDefEq.respectTransparency false in
theorem lift_horizontal_comm {K L : BC} {f g : K ⟶ L} (H : Homotopy f g) (n : ℕ) :
    (HomologicalComplex₂.total.map f c).f (n+1) =
      (show (K.total c).X (n+1) ⟶ (L.total c).X (n+1) from
        K.D₁ c (n+1) n ≫ liftDegree (fun p => H.hom p (p+1)) n) +
      (show (K.total c).X (n+1) ⟶ (L.total c).X (n+1) from
        liftDegree (fun p => H.hom p (p+1)) (n+1) ≫ L.D₁ c (n+2) (n+1)) +
      (HomologicalComplex₂.total.map g c).f (n+1) := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=n+1 at h
  rw [Preadditive.comp_add,Preadditive.comp_add,HomologicalComplex₂.ιTotal_map,
    HomologicalComplex₂.ιTotal_map,← Category.assoc, lift_horizontal]
  cases p with
  | zero =>
    rw [horizontal_axis,zero_comp,zero_add,← Preadditive.add_comp]
    have he := H.comm 0
    rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex,zero_add] at he
    have hh := congrArg (fun k => k.f q) he
    rw [hh]
    rfl
  | succ p =>
    rw [horizontal_succ K p q (n+1) n h (by omega),Category.assoc,liftDegree_summand,
      ← Category.assoc,← Preadditive.add_comp,← Preadditive.add_comp]
    have he := H.comm (p+1)
    rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex] at he
    have hh := congrArg (fun k => k.f q) he
    rw [hh]
    rfl

set_option backward.isDefEq.respectTransparency false in
theorem lift_comm_zero {K L : BC} {f g : K ⟶ L} (H : Homotopy f g) :
    (HomologicalComplex₂.total.map f c).f 0 =
      liftDegree (fun p => H.hom p (p+1)) 0 ≫ (L.total c).d 1 0 +
      (HomologicalComplex₂.total.map g c).f 0 := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=0 at h
  have hp : p=0 := by omega
  have hq : q=0 := by omega
  subst p
  subst q
  rw [Preadditive.comp_add,HomologicalComplex₂.ιTotal_map,HomologicalComplex₂.ιTotal_map,
    liftDegree_summand_assoc]
  change _ = (H.hom 0 1).f 0 ≫ (L.ιTotal c 1 0 1 rfl ≫
    (L.D₁ c 1 0 + L.D₂ c 1 0)) + _
  rw [Preadditive.comp_add,horizontal_succ,vertical_axis,add_zero,← Category.assoc,← Preadditive.add_comp]
  have he := H.comm 0
  rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex,zero_add] at he
  rw [congrArg (fun k => k.f 0) he]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem lift_comm_succ {K L : BC} {f g : K ⟶ L} (H : Homotopy f g) (n : ℕ) :
    (HomologicalComplex₂.total.map f c).f (n+1) =
      (K.total c).d (n+1) n ≫ liftDegree (fun p => H.hom p (p+1)) n +
      liftDegree (fun p => H.hom p (p+1)) (n+1) ≫ (L.total c).d (n+2) (n+1) +
      (HomologicalComplex₂.total.map g c).f (n+1) := by
  let s := fun p => H.hom p (p+1)
  have hh := lift_horizontal_comm H n
  have hv := lift_vertical_cancel s n
  change _ =
    (show (K.total c).X (n+1) ⟶ (L.total c).X (n+1) from
      (K.D₁ c (n+1) n + K.D₂ c (n+1) n) ≫ liftDegree s n) +
    (show (K.total c).X (n+1) ⟶ (L.total c).X (n+1) from
      liftDegree s (n+1) ≫ (L.D₁ c (n+2) (n+1) + L.D₂ c (n+2) (n+1))) + _
  rw [Preadditive.add_comp,Preadditive.comp_add,hh]
  -- regroup the two vertical terms and apply their cancellation
  let a : (K.total c).X (n+1) ⟶ (L.total c).X (n+1) := K.D₁ c (n+1) n ≫ liftDegree s n
  let b : (K.total c).X (n+1) ⟶ (L.total c).X (n+1) := K.D₂ c (n+1) n ≫ liftDegree s n
  let e : (K.total c).X (n+1) ⟶ (L.total c).X (n+1) := liftDegree s (n+1) ≫ L.D₁ c (n+2) (n+1)
  let d' : (K.total c).X (n+1) ⟶ (L.total c).X (n+1) := liftDegree s (n+1) ≫ L.D₂ c (n+2) (n+1)
  change a+e+_ = (a+b)+(e+d')+_
  change b+d'=0 at hv
  rw [show (a+b)+(e+d') = a+e+(b+d') by abel, hv,add_zero]

set_option backward.isDefEq.respectTransparency false in
def liftHomotopy {K L : BC} {f g : K ⟶ L} (H : Homotopy f g) :
    Homotopy (HomologicalComplex₂.total.map f c) (HomologicalComplex₂.total.map g c) where
  hom i j := if h : i+1=j then liftDegree (fun p => H.hom p (p+1)) i ≫
    eqToHom (by subst j; rfl) else 0
  zero i j hij := dif_neg (by intro h; apply hij; exact h)
  comm i := by
    cases i with
    | zero =>
      rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex]
      simpa using lift_comm_zero H
    | succ n =>
      rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex]
      simpa using lift_comm_succ H n

#print axioms liftDegree_summand
#print axioms lift_horizontal
#print axioms lift_vertical_cancel
#print axioms liftHomotopy
end CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
