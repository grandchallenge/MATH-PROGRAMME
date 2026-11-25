import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberAxes

/-! Acyclic-model inverse to Alexander–Whitney, independent of the
unproved interior signed-shuffle boundary calculation. It agrees with
the signed shuffle in degrees zero and one by construction. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberFilling
open CMDG.CondensedCM5R0.EilenbergZilberHomotopy
open CMDG.CondensedCM5R0.EilenbergZilberShuffle
open CMDG.CondensedCM5R0.EilenbergZilberTotalSide
open CMDG.CondensedCM5R0.EilenbergZilberZero
open CMDG.CondensedCM5R0.EilenbergZilberAxes
namespace CMDG.CondensedCM5R0.EilenbergZilberComparison

set_option backward.isDefEq.respectTransparency false in
def reverseDegree : ∀ n : ℕ, degree Tot n ⟶ degree D n
  | 0 => shuffleNatDegree 0
  | 1 => shuffleNatDegree 1
  | n+2 => totalLift (degree D (n+2)) (n+2) (fun i =>
      cone i.val.1 i.val.2 (n+1)
        (let B := model i.val.1 i.val.2
         let x := splitGenerator (n+2) i
         (reverseDegree (n+1)).app B ((Tot.obj B).d (n+2) (n+1) x)))

set_option backward.isDefEq.respectTransparency false in
theorem reverse_comm (n : ℕ) :
    reverseDegree (n+1) ≫ dNat D n = dNat Tot n ≫ reverseDegree n := by
  induction n with
  | zero =>
    apply NatTrans.ext
    funext B
    exact shuffle_comm_one B
  | succ n ih =>
    apply total_ext (degree D (n+1)) (n+2)
    intro i
    let B := model i.val.1 i.val.2
    let x := splitGenerator (n+2) i
    let y := (Tot.obj B).d (n+2) (n+1) x
    let z := (reverseDegree (n+1)).app B y
    have hz : (D.obj B).d (n+1) n z = 0 := by
      have he := CategoryTheory.congr_fun (congrArg (fun k => k.app B) ih) y
      change (D.obj B).d (n+1) n z =
        (reverseDegree n).app B ((Tot.obj B).d (n+1) n y) at he
      rw [he]
      have hy : (Tot.obj B).d (n+1) n y = 0 :=
        CategoryTheory.congr_fun ((Tot.obj B).d_comp_d (n+2) (n+1) n) x
      rw [hy,map_zero]
    change (D.obj B).d (n+2) (n+1)
      ((totalLift (degree D (n+2)) (n+2) _).app B x) = z
    rw [totalLift_generator]
    exact cone_fill i.val.1 i.val.2 n z hz

def reverseNat : Tot ⟶ D where
  app B := ChainComplex.ofHom (fun n => (reverseDegree n).app B) (fun n =>
    congrArg (fun k => k.app B) (reverse_comm n))
  naturality {_B _C} f := by
    apply HomologicalComplex.Hom.ext
    funext n
    exact (reverseDegree n).naturality f

set_option backward.isDefEq.respectTransparency false in
theorem aw_reverse_zero : mapDeg (awNat ≫ reverseNat) 0 = mapDeg (𝟙 D) 0 := by
  apply NatTrans.ext
  funext B
  exact aw_shuffle_zero B

set_option backward.isDefEq.respectTransparency false in
theorem reverse_aw_zero : mapDeg (reverseNat ≫ awNat) 0 = mapDeg (𝟙 Tot) 0 := by
  apply NatTrans.ext
  funext B
  exact shuffle_aw_zero B

/-- An actual, unconditional Eilenberg–Zilber chain homotopy equivalence,
with the already verified Alexander–Whitney map as forward map. -/
def comparison (B : Bi) : HomotopyEquiv (D.obj B) (Tot.obj B) where
  hom := awNat.app B
  inv := reverseNat.app B
  homotopyHomInvId := diagonalHomotopy (awNat ≫ reverseNat) (𝟙 D) aw_reverse_zero B
  homotopyInvHomId := totalHomotopy (reverseNat ≫ awNat) (𝟙 Tot) reverse_aw_zero B

/-- The signed inverse gives the same two homotopies once its remaining
universal boundary identity is supplied. No such identity is assumed
by comparison above. -/
def signedComparison (h : ∀ n (i : Split (n+1)),
    (shuffleResidual n).app _ (splitGenerator (n+1) i) = 0)
    (B : Bi) : HomotopyEquiv (D.obj B) (Tot.obj B) where
  hom := awNat.app B
  inv := (shuffleNat h).app B
  homotopyHomInvId := diagonalHomotopy (awNat ≫ shuffleNat h) (𝟙 D) (by
    apply NatTrans.ext
    funext C
    exact aw_shuffle_zero C) B
  homotopyInvHomId := totalHomotopy (shuffleNat h ≫ awNat) (𝟙 Tot) (by
    apply NatTrans.ext
    funext C
    exact shuffle_aw_zero C) B

#print axioms reverse_comm
#print axioms comparison
#print axioms signedComparison
end CMDG.CondensedCM5R0.EilenbergZilberComparison
