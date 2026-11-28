import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeComplex

/-! Instantiate the commuting double-complex descent with the actual
module Čech nerve, finite polynomial terms and identity augmentation. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension.PolynomialComplex
open BreenDeligneProbe
variable (C : PolynomialComplex.{u}) {M N : Mod.{u}} (p : M ⟶ N)

abbrev column : ℕ → Mod.{u}
  | 0 => N
  | j+1 => rel p j

def horizontal (n : ℕ) : (j : ℕ) →
    (C.row n).obj (column p (j+1)) ⟶ (C.row n).obj (column p j)
  | 0 => (C.row n).map (relAug p)
  | j+1 => ∑ i : Fin (j+2), (-1 : ℤ)^i.val • (C.row n).map (relFace p j i)

theorem horizontal_sq (n j : ℕ) : C.horizontal p n (j+1) ≫ C.horizontal p n j = 0 := by
  cases n with
  | zero =>
    cases j with
    | zero => exact relD_aug p
    | succ j => exact relD_sq p j
  | succ n =>
    cases j with
    | zero => exact polyD_aug p (C.arity n)
    | succ j => exact polyD_sq p (C.arity n) j

theorem commute (n j : ℕ) :
    C.horizontal p (n+1) j ≫ (C.vertical n).app (column p j) =
      (C.vertical n).app (column p (j+1)) ≫ C.horizontal p n j := by
  cases j with
  | zero => exact (C.vertical n).naturality (relAug p)
  | succ j =>
    unfold horizontal
    rw [Preadditive.sum_comp,Preadditive.comp_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [Preadditive.zsmul_comp,Preadditive.comp_zsmul]
    exact congrArg (fun f => (-1 : ℤ)^i.val • f)
      ((C.vertical n).naturality (relFace p j i))

def cechDouble : DoubleAugmented.{u} where
  obj n j := (C.row n).obj (column p j)
  v n j := (C.vertical n).app (column p j)
  h := C.horizontal p
  vv n j := NatTrans.congr_app (C.vertical_sq n) (column p j)
  hh := C.horizontal_sq p
  commute := C.commute p

theorem cech_HExact (hp : Function.Surjective p) : (C.cechDouble p).HExact := by
  intro n j x hx
  cases n with
  | zero =>
    cases j with
    | zero => exact relAug_surj p hp x
    | succ j =>
      cases j with
      | zero => exact rel_zero_exact p x hx
      | succ j => exact rel_exact p j x hx
  | succ n =>
    cases j with
    | zero => exact polyAug_surj p (C.arity n) hp x
    | succ j =>
      cases j with
      | zero =>
        exact (ShortComplex.moduleCat_exact_iff _).1 (poly_zero_exact p (C.arity n) hp) x hx
      | succ j =>
        exact (ShortComplex.moduleCat_exact_iff _).1 (poly_exact p (C.arity n) hp j) x hx

theorem cech_VExact (h : ∀ j, C.ExactAt (rel p j)) : (C.cechDouble p).VExactPositive := by
  intro n j x hx
  cases n with
  | zero => exact (h j).1 x
  | succ n => exact (ShortComplex.moduleCat_exact_iff _).1 ((h j).2 n) x hx

theorem cech_descend (hp : Function.Surjective p) (h : ∀ j, C.ExactAt (rel p j)) :
    C.ExactAt N := by
  have H := (C.cechDouble p).augmentation_exact (C.cech_HExact p hp) (C.cech_VExact p h)
  constructor
  · intro x
    exact H 0 x trivial
  · intro n
    apply (ShortComplex.moduleCat_exact_iff _).2
    intro x hx
    exact H (n+1) x hx

#print axioms cech_descend
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension.PolynomialComplex
