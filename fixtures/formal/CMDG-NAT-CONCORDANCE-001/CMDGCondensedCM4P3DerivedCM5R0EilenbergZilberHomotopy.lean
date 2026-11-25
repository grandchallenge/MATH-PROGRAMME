import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberFilling

/-! Explicit acyclic-model homotopies on diagonal chains. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberFilling
namespace CMDG.CondensedCM5R0.EilenbergZilberHomotopy

def dNat (F : Bi ⥤ Ch) (n : ℕ) : degree F (n+1) ⟶ degree F n where
  app B := (F.obj B).d (n+1) n
  naturality {_B _C} f := (F.map f).comm (n+1) n

def mapDeg {F G : Bi ⥤ Ch} (f : F ⟶ G) (n : ℕ) :
    degree F n ⟶ degree G n :=
  Functor.whiskerRight f (HomologicalComplex.eval ZMod c n)

set_option backward.isDefEq.respectTransparency false in
def H (f g : D ⟶ D) : ∀ n : ℕ, degree D n ⟶ degree D (n+1)
  | 0 => 0
  | n+1 => evalLift (degree D (n+2)) (n+1) (n+1)
      (cone (n+1) (n+1) (n+1)
        (let B := model (n+1) (n+1)
         let x := modelGenerator (n+1) (n+1)
         (f.app B).f (n+1) x - (g.app B).f (n+1) x -
           (show (D.obj B).X (n+1) from (H f g n).app B ((D.obj B).d (n+1) n x))))

set_option backward.isDefEq.respectTransparency false in
theorem H_comm (f g : D ⟶ D) (h0 : mapDeg f 0 = mapDeg g 0) (n : ℕ) :
    mapDeg f (n+1) - mapDeg g (n+1) =
      dNat D n ≫ H f g n + H f g (n+1) ≫ dNat D (n+1) := by
  induction n with
  | zero =>
    apply eval_ext (degree D 1) 1 1
    let B := model 1 1
    let x := modelGenerator 1 1
    let z := (f.app B).f 1 x - (g.app B).f 1 x
    have hz : (D.obj B).d 1 0 z = 0 := by
      dsimp only [z]
      rw [map_sub]
      have hf := CategoryTheory.congr_fun ((f.app B).comm 1 0) x
      have hg := CategoryTheory.congr_fun ((g.app B).comm 1 0) x
      change (D.obj B).d 1 0 ((f.app B).f 1 x) = _ at hf
      change (D.obj B).d 1 0 ((g.app B).f 1 x) = _ at hg
      rw [hf,hg]
      have he := CategoryTheory.congr_fun (congrArg (fun k => k.app B) h0) ((D.obj B).d 1 0 x)
      exact sub_eq_zero.mpr he
    change z = _ + _
    rw [H, H, comp_zero]
    change z = (0 : (D.obj B).X 1) + (D.obj B).d 2 1
      ((evalLift (degree D 2) 1 1 (cone 1 1 1 (z - (0 : (D.obj B).X 1)))).app B x)
    rw [zero_add,sub_zero]
    rw [evalLift_generator,cone_fill 1 1 0 z hz]
  | succ n ih =>
    apply eval_ext (degree D (n+2)) (n+2) (n+2)
    let B := model (n+2) (n+2)
    let x := modelGenerator (n+2) (n+2)
    let y := (D.obj B).d (n+2) (n+1) x
    let z := (f.app B).f (n+2) x - (g.app B).f (n+2) x - (show (D.obj B).X (n+2) from (H f g (n+1)).app B y)
    have hz : (D.obj B).d (n+2) (n+1) z = 0 := by
      dsimp only [z]
      rw [map_sub,map_sub]
      have hf := CategoryTheory.congr_fun ((f.app B).comm (n+2) (n+1)) x
      have hg := CategoryTheory.congr_fun ((g.app B).comm (n+2) (n+1)) x
      change (D.obj B).d (n+2) (n+1) ((f.app B).f (n+2) x) = (f.app B).f (n+1) y at hf
      change (D.obj B).d (n+2) (n+1) ((g.app B).f (n+2) x) = (g.app B).f (n+1) y at hg
      rw [hf,hg]
      have he := CategoryTheory.congr_fun (congrArg (fun k => k.app B) ih) y
      change (f.app B).f (n+1) y - (g.app B).f (n+1) y =
        (show (D.obj B).X (n+1) from (H f g n).app B ((D.obj B).d (n+1) n y)) +
          (D.obj B).d (n+2) (n+1) ((H f g (n+1)).app B y) at he
      have hdy : (D.obj B).d (n+1) n y = 0 := by
        exact CategoryTheory.congr_fun ((D.obj B).d_comp_d (n+2) (n+1) n) x
      rw [hdy,map_zero,zero_add] at he
      exact sub_eq_zero.mpr he
    change (f.app B).f (n+2) x - (g.app B).f (n+2) x =
      (show (D.obj B).X (n+2) from (H f g (n+1)).app B y) +
        (D.obj B).d (n+3) (n+2) ((H f g (n+2)).app B x)
    change _ = _ + (D.obj B).d (n+3) (n+2)
      ((evalLift (degree D (n+3)) (n+2) (n+2) (cone (n+2) (n+2) (n+2) z)).app B x)
    rw [evalLift_generator,cone_fill (n+2) (n+2) (n+1) z hz]
    dsimp only [z]
    exact (show ∀ a b : (D.obj B).X (n+2), a = b + (a-b) from by intros; abel) _ _

set_option backward.isDefEq.respectTransparency false in
/-- Any two natural diagonal chain maps agreeing in degree zero have
a chain homotopy, constructed by filling universal cycles. -/
def diagonalHomotopy (f g : D ⟶ D) (h0 : mapDeg f 0 = mapDeg g 0) (B : Bi) :
    Homotopy (f.app B) (g.app B) where
  hom i j := if h : i+1=j then (H f g i).app B ≫ eqToHom (by subst j; rfl) else 0
  zero i j hij := dif_neg (by intro h; apply hij; change i+1=j; exact h)
  comm i := by
    cases i with
    | zero =>
      rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex]
      simp [H,zero_comp]
      exact congrArg (fun k => k.app B) h0
    | succ n =>
      rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex]
      simp only [eqToHom_refl,Category.comp_id]
      have h := congrArg (fun k => k.app B) (H_comm f g h0 n)
      exact sub_eq_iff_eq_add.mp h

#print axioms H_comm
#print axioms diagonalHomotopy
end CMDG.CondensedCM5R0.EilenbergZilberHomotopy
