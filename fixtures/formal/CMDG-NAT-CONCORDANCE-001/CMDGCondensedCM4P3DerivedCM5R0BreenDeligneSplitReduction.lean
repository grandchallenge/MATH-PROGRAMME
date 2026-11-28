import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedRealPower

/-! Exact reduction of an augmented resolution by a split chain
projection onto its value at zero.  Exactness is inherited by the
actual kernel complex, not imposed as an additional premise. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
open AcyclicResolution RealProductProjection

structure SplitResolution (R : Resolution.{u}) where
  base : ℕ → Ambient.{u}
  p : ∀ n, R.term n ⟶ base n
  s : ∀ n, base n ⟶ R.term n
  split : ∀ n, s n ≫ p n = 𝟙 _
  d : ∀ n, base (n+1) ⟶ base n
  p_chain : ∀ n, R.d n ≫ p n = p (n+1) ≫ d n
  s_chain : ∀ n, d n ≫ s n = s (n+1) ≫ R.d n
  s_aug : s 0 ≫ R.aug = 0

namespace SplitResolution
variable {R : Resolution.{u}} (B : SplitResolution R)

abbrev K (n : ℕ) := kernel (B.p n)
abbrev i (n : ℕ) : B.K n ⟶ R.term n := kernel.ι (B.p n)
abbrev r (n : ℕ) : R.term n ⟶ B.K n :=
  splitKernelRetraction (B.p n) (B.s n) (B.split n)

theorem ir (n : ℕ) : B.i n ≫ B.r n = 𝟙 _ :=
  splitKernelRetraction_retract _ _ _

theorem ri (n : ℕ) : B.r n ≫ B.i n = 𝟙 _ - B.p n ≫ B.s n :=
  splitKernelRetraction_spec _ _ _

def kd (n : ℕ) : B.K (n+1) ⟶ B.K n :=
  kernel.lift (B.p n) (B.i (n+1) ≫ R.d n) (by
    rw [Category.assoc,B.p_chain,← Category.assoc,kernel.condition,zero_comp])

theorem kd_i (n : ℕ) : B.kd n ≫ B.i n = B.i (n+1) ≫ R.d n :=
  kernel.lift_ι _ _ _

theorem d_r (n : ℕ) : R.d n ≫ B.r n = B.r (n+1) ≫ B.kd n := by
  apply (cancel_mono (B.i n)).1
  rw [Category.assoc,B.ri,Category.assoc,B.kd_i,← Category.assoc,B.ri]
  simp only [Preadditive.comp_sub,Preadditive.sub_comp,Category.comp_id,Category.id_comp,
    Category.assoc]
  rw [← Category.assoc (R.d n),B.p_chain,Category.assoc,B.s_chain]

def ka : B.K 0 ⟶ R.target := B.i 0 ≫ R.aug

theorem r_aug : B.r 0 ≫ B.ka = R.aug := by
  unfold ka
  rw [← Category.assoc,B.ri,Preadditive.sub_comp,Category.id_comp,Category.assoc,
    B.s_aug,comp_zero,sub_zero]

theorem ka_epi : Epi B.ka := by
  letI : Epi R.aug := R.aug_epi
  constructor
  intro Z f g h
  apply (cancel_epi R.aug).1
  rw [← B.r_aug,Category.assoc,Category.assoc,h]

theorem kd_sq (n : ℕ) : B.kd (n+1) ≫ B.kd n = 0 := by
  apply (cancel_mono (B.i n)).1
  rw [Category.assoc,B.kd_i,← Category.assoc,B.kd_i,Category.assoc,R.sq_zero,
    comp_zero,zero_comp]

theorem kd_ka : B.kd 0 ≫ B.ka = 0 := by
  unfold ka
  rw [← Category.assoc,B.kd_i,Category.assoc,R.aug_zero,comp_zero]

theorem exact_retract {C : Type*} [Category C] [Abelian C]
    {X Y : ShortComplex C} (f : X ⟶ Y) (g : Y ⟶ X) (h : f ≫ g = 𝟙 X)
    (hy : Y.Exact) : X.Exact := by
  apply (ShortComplex.exact_iff_isZero_homology X).2
  have hz := (ShortComplex.exact_iff_isZero_homology Y).1 hy
  have hh : ShortComplex.homologyMap f ≫ ShortComplex.homologyMap g = 𝟙 _ := by
    rw [← ShortComplex.homologyMap_comp,h,ShortComplex.homologyMap_id]
  apply (IsZero.iff_id_eq_zero _).mpr
  rw [← hh,hz.eq_of_tgt (ShortComplex.homologyMap f) 0,zero_comp]

def seq (n : ℕ) : ShortComplex Ambient.{u} :=
  ShortComplex.mk (B.kd (n+1)) (B.kd n) (B.kd_sq n)

theorem seq_exact (n : ℕ) : (B.seq n).Exact := by
  let T := ShortComplex.mk (R.d (n+1)) (R.d n) (R.sq_zero n)
  let f : B.seq n ⟶ T := ShortComplex.Hom.mk (B.i (n+2)) (B.i (n+1)) (B.i n)
    (B.kd_i (n+1)).symm (B.kd_i n).symm
  let g : T ⟶ B.seq n := ShortComplex.Hom.mk (B.r (n+2)) (B.r (n+1)) (B.r n)
    (B.d_r (n+1)).symm (B.d_r n).symm
  apply exact_retract f g _ (R.exact n)
  apply ShortComplex.hom_ext
  · exact B.ir (n+2)
  · exact B.ir (n+1)
  · exact B.ir n

def augSeq : ShortComplex Ambient.{u} :=
  ShortComplex.mk (B.kd 0) B.ka B.kd_ka

theorem augSeq_exact : B.augSeq.Exact := by
  let T := ShortComplex.mk (R.d 0) R.aug R.aug_zero
  let f : B.augSeq ⟶ T := ShortComplex.Hom.mk (B.i 1) (B.i 0) (𝟙 _)
    (B.kd_i 0).symm (by change B.ka = B.ka ≫ 𝟙 _; rw [Category.comp_id])
  let g : T ⟶ B.augSeq := ShortComplex.Hom.mk (B.r 1) (B.r 0) (𝟙 _)
    (B.d_r 0).symm (by change B.r 0 ≫ B.ka = R.aug ≫ 𝟙 _; rw [B.r_aug,Category.comp_id])
  apply exact_retract f g _ R.aug_exact
  apply ShortComplex.hom_ext
  · exact B.ir 1
  · exact B.ir 0
  · exact Category.id_comp _

def reducedResolution : Resolution.{u} where
  target := R.target
  term := B.K
  aug := B.ka
  d := B.kd
  aug_zero := B.kd_ka
  sq_zero := B.kd_sq
  aug_epi := B.ka_epi
  aug_exact := B.augSeq_exact
  exact := B.seq_exact

#print axioms reducedResolution
end SplitResolution
end CMDG.CondensedCM5R0
