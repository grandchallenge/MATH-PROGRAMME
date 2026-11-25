import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberTotalModel

/-! Explicit acyclic-model homotopies on total chains. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberHomotopy
open CMDG.CondensedCM5R0.EilenbergZilberTotalModel
namespace CMDG.CondensedCM5R0.EilenbergZilberTotalSide

set_option backward.isDefEq.respectTransparency false in
def H (f g : Tot ⟶ Tot) : ∀ n : ℕ, degree Tot n ⟶ degree Tot (n+1)
  | 0 => 0
  | n+1 => totalLift (degree Tot (n+2)) (n+1) (fun i =>
      totalCone i.val.1 i.val.2 (n+1)
        (let B := model i.val.1 i.val.2
         let x := splitGenerator (n+1) i
         (f.app B).f (n+1) x - (g.app B).f (n+1) x -
           (show (Tot.obj B).X (n+1) from (H f g n).app B ((Tot.obj B).d (n+1) n x))))

set_option backward.isDefEq.respectTransparency false in
theorem H_comm (f g : Tot ⟶ Tot) (h0 : mapDeg f 0 = mapDeg g 0) (n : ℕ) :
    mapDeg f (n+1) - mapDeg g (n+1) =
      dNat Tot n ≫ H f g n + H f g (n+1) ≫ dNat Tot (n+1) := by
  induction n with
  | zero =>
    apply total_ext (degree Tot 1) 1
    intro i
    let B := model i.val.1 i.val.2
    let x := splitGenerator 1 i
    let z := (f.app B).f 1 x - (g.app B).f 1 x
    have hz : (Tot.obj B).d 1 0 z = 0 := by
      dsimp only [z]
      rw [map_sub]
      have hf := CategoryTheory.congr_fun ((f.app B).comm 1 0) x
      have hg := CategoryTheory.congr_fun ((g.app B).comm 1 0) x
      change (Tot.obj B).d 1 0 ((f.app B).f 1 x) = _ at hf
      change (Tot.obj B).d 1 0 ((g.app B).f 1 x) = _ at hg
      rw [hf,hg]
      have he := CategoryTheory.congr_fun (congrArg (fun k => k.app B) h0) ((Tot.obj B).d 1 0 x)
      exact sub_eq_zero.mpr he
    change z = _ + _
    rw [H, H, comp_zero]
    change z = (0 : (Tot.obj B).X 1) + (Tot.obj B).d 2 1
      ((totalLift (degree Tot 2) 1 _).app B x)
    rw [zero_add]
    rw [totalLift_generator]
    change z = (Tot.obj B).d 2 1 (totalCone i.val.1 i.val.2 1 (z - 0))
    rw [sub_zero,totalCone_fill i.val.1 i.val.2 0 z hz]
  | succ n ih =>
    apply total_ext (degree Tot (n+2)) (n+2)
    intro i
    let B := model i.val.1 i.val.2
    let x := splitGenerator (n+2) i
    let y := (Tot.obj B).d (n+2) (n+1) x
    let z := (f.app B).f (n+2) x - (g.app B).f (n+2) x - (show (Tot.obj B).X (n+2) from (H f g (n+1)).app B y)
    have hz : (Tot.obj B).d (n+2) (n+1) z = 0 := by
      dsimp only [z]
      rw [map_sub,map_sub]
      have hf := CategoryTheory.congr_fun ((f.app B).comm (n+2) (n+1)) x
      have hg := CategoryTheory.congr_fun ((g.app B).comm (n+2) (n+1)) x
      change (Tot.obj B).d (n+2) (n+1) ((f.app B).f (n+2) x) = (f.app B).f (n+1) y at hf
      change (Tot.obj B).d (n+2) (n+1) ((g.app B).f (n+2) x) = (g.app B).f (n+1) y at hg
      rw [hf,hg]
      have he := CategoryTheory.congr_fun (congrArg (fun k => k.app B) ih) y
      change (f.app B).f (n+1) y - (g.app B).f (n+1) y =
        (show (Tot.obj B).X (n+1) from (H f g n).app B ((Tot.obj B).d (n+1) n y)) +
          (Tot.obj B).d (n+2) (n+1) ((H f g (n+1)).app B y) at he
      have hdy : (Tot.obj B).d (n+1) n y = 0 := by
        exact CategoryTheory.congr_fun ((Tot.obj B).d_comp_d (n+2) (n+1) n) x
      rw [hdy,map_zero,zero_add] at he
      exact sub_eq_zero.mpr he
    change (f.app B).f (n+2) x - (g.app B).f (n+2) x =
      (show (Tot.obj B).X (n+2) from (H f g (n+1)).app B y) +
        (Tot.obj B).d (n+3) (n+2) ((H f g (n+2)).app B x)
    change _ = _ + (Tot.obj B).d (n+3) (n+2)
      ((totalLift (degree Tot (n+3)) (n+2) _).app B x)
    rw [totalLift_generator]
    change _ = _ + (Tot.obj B).d (n+3) (n+2)
      (totalCone i.val.1 i.val.2 (n+2) z)
    rw [totalCone_fill i.val.1 i.val.2 (n+1) z hz]
    dsimp only [z]
    exact (show ∀ a b : (Tot.obj B).X (n+2), a = b + (a-b) from by intros; abel) _ _

set_option backward.isDefEq.respectTransparency false in
/-- Any two natural total chain maps agreeing in degree zero have
a chain homotopy, constructed by filling universal cycles. -/
def totalHomotopy (f g : Tot ⟶ Tot) (h0 : mapDeg f 0 = mapDeg g 0) (B : Bi) :
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
#print axioms totalHomotopy
end CMDG.CondensedCM5R0.EilenbergZilberTotalSide
