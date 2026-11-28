import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCechPolynomial

/-! Extend an actual exact finite-type lattice complex. No lattice
existence theorem is assumed inside the extension construction. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe

structure LatticeBD where
  count : ℕ → ℕ
  arity : ∀ n, Fin (count n) → ℕ
  aug : incl.{u} ⋙ polynomial (arity 0) ⟶ incl
  d : ∀ n, incl.{u} ⋙ polynomial (arity (n+1)) ⟶ incl ⋙ polynomial (arity n)
  aug_zero : d 0 ≫ aug = 0
  sq_zero : ∀ n, d (n+1) ≫ d n = 0
  aug_epi : Epi aug
  aug_exact : (ShortComplex.mk (d 0) aug aug_zero).Exact
  exact : ∀ n, (ShortComplex.mk (d (n+1)) (d n) (sq_zero n)).Exact

structure PolynomialComplex where
  count : ℕ → ℕ
  arity : ∀ n, Fin (count n) → ℕ
  aug : polynomial (arity 0) ⟶ 𝟭 Mod.{u}
  d : ∀ n, polynomial (arity (n+1)) ⟶ polynomial (arity n)
  aug_zero : d 0 ≫ aug = 0
  sq_zero : ∀ n, d (n+1) ≫ d n = 0

def LatticeBD.extended (B : LatticeBD.{u}) : PolynomialComplex.{u} where
  count := B.count
  arity := B.arity
  aug := extend (B.arity 0) (G := 𝟭 Mod.{u}) B.aug
  d n := extend (B.arity (n+1)) (B.d n)
  aug_zero := by
    apply zero_of_restrict_zero
    change Functor.whiskerLeft incl
      (extend (B.arity 1) (B.d 0) ≫ extend (B.arity 0) (G:=𝟭 Mod.{u}) B.aug) = 0
    change Functor.whiskerLeft incl (extend (B.arity 1) (B.d 0)) ≫
      Functor.whiskerLeft incl (extend (B.arity 0) (G:=𝟭 Mod.{u}) B.aug) = 0
    rw [extend_restrict,extend_restrict,B.aug_zero]
  sq_zero n := by
    apply zero_of_restrict_zero
    change Functor.whiskerLeft incl (extend (B.arity (n+2)) (B.d (n+1))) ≫
      Functor.whiskerLeft incl (extend (B.arity (n+1)) (B.d n)) = 0
    rw [extend_restrict,extend_restrict,B.sq_zero]

namespace PolynomialComplex
variable (C : PolynomialComplex.{u})

abbrev row : ℕ → Mod.{u} ⥤ Mod.{u}
  | 0 => 𝟭 _
  | n+1 => polynomial (C.arity n)

def vertical : (n : ℕ) → C.row (n+1) ⟶ C.row n
  | 0 => C.aug
  | n+1 => C.d n

theorem vertical_sq (n : ℕ) : C.vertical (n+1) ≫ C.vertical n = 0 := by
  cases n with
  | zero => exact C.aug_zero
  | succ n => exact C.sq_zero n

def eval (A : Mod.{u}) (n : ℕ) : ShortComplex Mod.{u} :=
  ShortComplex.mk ((C.vertical (n+1)).app A) ((C.vertical n).app A)
    (NatTrans.congr_app (C.vertical_sq n) A)

abbrev ExactAt (A : Mod.{u}) : Prop :=
  Function.Surjective (C.aug.app A) ∧ ∀ n, (C.eval A n).Exact

theorem vertical_lift (A : Mod.{u}) (h : C.ExactAt A) (n : ℕ)
    (x : (C.row n).obj A)
    (hx : match n with | 0 => True | j+1 => (C.vertical j).app A x = 0) :
    ∃ y : (C.row (n+1)).obj A, (C.vertical n).app A y = x := by
  cases n with
  | zero => exact h.1 x
  | succ n => exact (ShortComplex.moduleCat_exact_iff _).1 (h.2 n) x hx

theorem aug_surj_all (h : Function.Surjective (C.aug.app (rank.{u} 1)))
    (M : Mod.{u}) : Function.Surjective (C.aug.app M) := by
  intro x
  obtain ⟨y,hy⟩ := h (generic 1 0)
  let f := tupleMap (fun _ : Fin 1 => x)
  refine ⟨(polynomial (C.arity 0)).map f y,?_⟩
  have hn := CategoryTheory.congr_fun (C.aug.naturality f) y
  change C.aug.app M ((polynomial (C.arity 0)).map f y) =
    f (C.aug.app (rank 1) y) at hn
  rw [hn,hy]
  exact tupleMap_generic (fun _ : Fin 1 => x) 0

theorem exact_free (h : ∀ n : ℕ, C.ExactAt (rank.{u} n))
    (X : Type (u+1)) : C.ExactAt (freeM X) := by
  refine ⟨C.aug_surj_all (h 1).1 _,?_⟩
  intro n
  cases n with
  | zero => exact free_exact (C.d 0) C.aug C.aug_zero (fun j => (h j).2 0) X
  | succ n => exact free_exact (C.d (n+1)) (C.d n) (C.sq_zero n) (fun j => (h j).2 (n+1)) X

theorem exact_iso {A B : Mod.{u}} (e : A ≅ B) (h : C.ExactAt A) : C.ExactAt B := by
  constructor
  · intro b
    obtain ⟨x,hx⟩ := h.1 (e.inv b)
    refine ⟨(polynomial (C.arity 0)).map e.hom x,?_⟩
    have hh := CategoryTheory.congr_fun (C.aug.naturality e.hom) x
    change C.aug.app B ((polynomial (C.arity 0)).map e.hom x) = e.hom (C.aug.app A x) at hh
    rw [hh,hx]
    exact CategoryTheory.congr_fun e.inv_hom_id b
  · intro n
    have e' : C.eval A n ≅ C.eval B n :=
      ShortComplex.isoMk ((C.row (n+2)).mapIso e) ((C.row (n+1)).mapIso e)
        ((C.row n).mapIso e)
        (by exact ((C.vertical (n+1)).naturality e.hom))
        (by exact ((C.vertical n).naturality e.hom))
    exact ShortComplex.exact_of_iso e' (h.2 n)

end PolynomialComplex

theorem LatticeBD.extended_exact (B : LatticeBD.{u}) (n : ℕ) :
    B.extended.ExactAt (rank.{u} n) := by
  have he := NatTrans.congr_app (extend_restrict (B.arity 0) (G:=𝟭 Mod.{u}) B.aug) n
  have hd (j : ℕ) := NatTrans.congr_app (extend_restrict (B.arity (j+1)) (B.d j)) n
  constructor
  · change Function.Surjective (extend (B.arity 0) (G:=𝟭 Mod.{u}) B.aug |>.app (rank n))
    change (extend (B.arity 0) (G:=𝟭 Mod.{u}) B.aug).app (rank n) = B.aug.app n at he
    rw [he]
    exact (ModuleCat.epi_iff_surjective _).1 ((NatTrans.epi_iff_epi_app _).1 B.aug_epi n)
  · intro j
    let E := (CategoryTheory.evaluation Latt.{u} Mod.{u}).obj n
    have h0 := B.aug_exact.map E
    have hs (j : ℕ) := (B.exact j).map E
    cases j with
    | zero =>
      apply (ShortComplex.moduleCat_exact_iff _).2
      intro x hx
      change (extend (B.arity 0) (G:=𝟭 Mod.{u}) B.aug).app (rank n) x = 0 at hx
      change (extend (B.arity 0) (G:=𝟭 Mod.{u}) B.aug).app (rank n) = B.aug.app n at he
      rw [he] at hx
      obtain ⟨y,hy⟩ := (ShortComplex.moduleCat_exact_iff _).1 h0 x hx
      refine ⟨y,?_⟩
      change (extend (B.arity 1) (B.d 0)).app (rank n) y = x
      exact (congrArg (fun f => f y) (hd 0)).trans hy
    | succ j =>
      apply (ShortComplex.moduleCat_exact_iff _).2
      intro x hx
      change (extend (B.arity (j+1)) (B.d j)).app (rank n) x = 0 at hx
      have hx' : (B.d j).app n x = 0 := by
        exact (congrArg (fun f => f x) (hd j)).symm.trans hx
      obtain ⟨y,hy⟩ := (ShortComplex.moduleCat_exact_iff _).1 (hs j) x hx'
      refine ⟨y,?_⟩
      change (extend (B.arity (j+2)) (B.d (j+1))).app (rank n) y = x
      exact (congrArg (fun f => f y) (hd (j+1))).trans hy

#print axioms PolynomialComplex.exact_free
#print axioms LatticeBD.extended_exact
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
