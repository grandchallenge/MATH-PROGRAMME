import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneNormalizedBar

/-! Actual horizontally normalized reduced bar bicomplex and diagonal
simplicial abelian group. No Eilenberg-Zilber quasi-isomorphism is assumed. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
namespace CMDG.CondensedCM5R0.BreenDeligneBarTotal

theorem horizontalZero (A : AGrp) : IsZero (M A 0) := by
  have hz : IsZero (T A 0) := by
    apply (IsZero.iff_id_eq_zero _).mpr
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    exact Fin.elim0 i
  exact IsZero.of_epi (project A 0) (reducedFree_zero _ hz)

def horizontalMooreZ : AGrp ⥤ Ch :=
  horizontalMoore ⋙ toZModule.mapHomologicalComplex c

def verticalFirst (X : SimplicialObject AGrp) : HomologicalComplex₂ ZMod c c :=
  (alternatingFaceMapComplex Ch).obj (X ⋙ horizontalMooreZ)

/-- Horizontal degree is the outer index; vertical degree the inner one. -/
def barDouble (X : SimplicialObject AGrp) : HomologicalComplex₂ ZMod c c :=
  (verticalFirst X).flip

def barTotal (X : SimplicialObject AGrp) : Ch :=
  (barDouble X).total c

set_option backward.isDefEq.respectTransparency false in
def doubleColumnIso (X : SimplicialObject AGrp) (p : ℕ) :
    (barDouble X).X p ≅ actualVerticalColumn X p := by
  apply eqToIso
  have h := congrArg (fun F => F.obj (X ⋙ horizontalMooreZ))
    (AlgebraicTopology.map_alternatingFaceMapComplex (HomologicalComplex.eval ZMod c p))
  change (barDouble X).X p = _ at h
  exact h

theorem zeroColumn (X : SimplicialObject AGrp) (q : ℕ) :
    IsZero (((barDouble X).X 0).X q) := by
  change IsZero (toZModule.obj (M (X.obj (op (SimplexCategory.mk q))) 0))
  exact toZModule.map_isZero (horizontalZero _)

def totalFirstColumn (A : AGrp) (n : ℕ) :
    (barDouble ((EilenbergMacLaneModel.em n).obj A)).X 1 ≅ reducedChainsZ A n :=
  doubleColumnIso _ 1 ≪≫ actualFirstColumnIso A n

/-- The diagonal of the actual bisimplicial bar group. -/
def barDiagonal (X : SimplicialObject AGrp) : SimplicialObject AGrp where
  obj Δ := (bar (X.obj Δ)).obj Δ
  map {Δ Δ'} f := (barNat (X.map f)).app Δ ≫ (bar (X.obj Δ')).map f
  map_id Δ := by
    have h : (barNat (X.map (𝟙 Δ))).app Δ = 𝟙 _ := by
      rw [X.map_id]
      exact congrArg (fun g => g.app Δ) (barFunctor.map_id (X.obj Δ))
    rw [h,(bar (X.obj Δ)).map_id,Category.id_comp]
  map_comp {Δ Δ' Δ''} f g := by
    have h : (barNat (X.map (f ≫ g))).app Δ =
        (barNat (X.map f)).app Δ ≫ (barNat (X.map g)).app Δ := by
      rw [X.map_comp]
      exact congrArg (fun h => h.app Δ) (barFunctor.map_comp (X.map f) (X.map g))
    rw [h,Functor.map_comp]
    simp only [Category.assoc]
    rw [← (barNat (X.map g)).naturality_assoc]

def diagonalReducedChains (X : SimplicialObject AGrp) : Ch :=
  (alternatingFaceMapComplex ZMod).obj (barDiagonal X ⋙ reducedFree ⋙ toZModule)

#print axioms horizontalZero
#print axioms doubleColumnIso
#print axioms totalFirstColumn
#print axioms barDiagonal
end CMDG.CondensedCM5R0.BreenDeligneBarTotal
