import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCondensedChainProofs
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Abel
set_option backward.isDefEq.respectTransparency false


/-!
# CMDG CM5: genuine degree-three hexagon and symmetric-involution syzygies

The actual Breen–Deligne free condensed abelian source terms satisfy
the hexagon relation connecting associativity with commutativity:
  A(a,b,c) - A(b,a,c) + A(b,c,a)
    = C(a,b+c) - C(a,b) - C(a,c),
where A and C are the genuine prior categorical boundaries.
Nine exact polynomial-face pairings are proved as CondensedAb
morphism equalities. The second syzygy is C(a,b)+C(b,a)=0, proved
via the involution of pair swapping. Combining these yields a genuine
partial degree-three coherence chain
    Z[A³] ⊕ Z[A²] → F₂(A) → F₁(A)
with zero composition for any compact Hausdorff abelian group A,
including arbitrary products of circles.

This is a partial degree-three chain, NOT proof of exactness at F₂,
a full degree-three generator basis, an all-degree finite-type
resolution, the analytic derived-real/circle comparisons, or the
canonical solidification-unit evaluation map.
-/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneCondensed

variable (A : Type u) [TopologicalSpace A] [CompactSpace A]
  [T2Space A] [AddCommGroup A] [ContinuousAdd A]

def hexSwap : C(A × (A × A), A × (A × A)) :=
  ⟨fun p => (p.2.1, (p.1,p.2.2)), by fun_prop⟩
def hexRotate : C(A × (A × A), A × (A × A)) :=
  ⟨fun p => (p.2.1, (p.2.2,p.1)), by fun_prop⟩

def hexPair0 : C(A × (A × A), A × A) :=
  ⟨fun p => (p.1,p.2.1+p.2.2), by fun_prop⟩
def hexPair1 : C(A × (A × A), A × A) :=
  ⟨fun p => (p.1,p.2.1), by fun_prop⟩
def hexPair2 : C(A × (A × A), A × A) :=
  ⟨fun p => (p.1,p.2.2), by fun_prop⟩

def hexAssoc : src2assoc A ⟶ src2assoc A :=
  𝟙 _ - polyMap (hexSwap A) + polyMap (hexRotate A)

def hexComm : src2assoc A ⟶ src1 A :=
  -polyMap (hexPair0 A) + polyMap (hexPair1 A) + polyMap (hexPair2 A)

def hexBoundary : src2assoc A ⟶ src2 A :=
  (hexAssoc A ≫ biprod.inl) + (hexComm A ≫ biprod.inr)

def hexFlip : C(A × A,A × A) :=
  ⟨fun p => (p.2,p.1), continuous_snd.prodMk continuous_fst⟩

theorem hex_cancel_0 :
    polyMap (assocBC A) =
    polyMap ((assocAB A).comp (hexRotate A)) := by
  congr 1

theorem hex_cancel_1 :
    polyMap (assocAB_C A) =
    polyMap ((assocAB_C A).comp (hexSwap A)) := by
  congr 1
  ext p
  · exact add_comm p.1 p.2.1
  · rfl

theorem hex_cancel_2 :
    polyMap (assocA_BC A) =
    polyMap (hexPair0 A) := by
  congr 1

theorem hex_cancel_3 :
    polyMap (assocAB A) =
    polyMap (hexPair1 A) := by
  congr 1

theorem hex_cancel_4 :
    polyMap ((assocBC A).comp (hexSwap A)) =
    polyMap (hexPair2 A) := by
  congr 1

theorem hex_cancel_5 :
    polyMap ((assocA_BC A).comp (hexSwap A)) =
    polyMap ((assocA_BC A).comp (hexRotate A)) := by
  congr 1
  ext p
  · rfl
  · exact add_comm p.1 p.2.2

theorem hex_cancel_6 :
    polyMap ((assocAB A).comp (hexSwap A)) =
    polyMap ((hexFlip A).comp (hexPair1 A)) := by
  congr 1

theorem hex_cancel_7 :
    polyMap ((assocBC A).comp (hexRotate A)) =
    polyMap ((hexFlip A).comp (hexPair2 A)) := by
  congr 1

theorem hex_cancel_8 :
    polyMap ((assocAB_C A).comp (hexRotate A)) =
    polyMap ((hexFlip A).comp (hexPair0 A)) := by
  congr 1
theorem hexAssoc_comp_d2assoc_add_hexComm_comp_d2comm_zero :
    hexAssoc A ≫ d2assoc A + hexComm A ≫ d2comm A = 0 := by
  dsimp only [src2assoc,src1] at *
  change ((𝟙 _) - polyMap (hexSwap A) + polyMap (hexRotate A)) ≫
      (polyMap (assocBC A) - polyMap (assocAB_C A) +
        polyMap (assocA_BC A) - polyMap (assocAB A)) +
      (-polyMap (hexPair0 A) + polyMap (hexPair1 A) +
        polyMap (hexPair2 A)) ≫
      ((𝟙 _) - polyMap (hexFlip A)) = 0
  simp only [Preadditive.add_comp,Preadditive.sub_comp,
    Preadditive.comp_add,Preadditive.comp_sub,
    Preadditive.neg_comp,Category.id_comp,Category.comp_id,polyMap_comp]
  rw [hex_cancel_0 A,hex_cancel_1 A,hex_cancel_2 A,
    hex_cancel_3 A,hex_cancel_4 A,hex_cancel_5 A,
    hex_cancel_6 A,hex_cancel_7 A,hex_cancel_8 A]
  abel

theorem hexBoundary_comp_d2_zero : hexBoundary A ≫ d2 A = 0 := by
  change ((hexAssoc A ≫ biprod.inl) +
    (hexComm A ≫ biprod.inr)) ≫
    biprod.desc (d2assoc A) (d2comm A) = 0
  rw [Preadditive.add_comp]
  simp only [Category.assoc,biprod.inl_desc,biprod.inr_desc]
  exact hexAssoc_comp_d2assoc_add_hexComm_comp_d2comm_zero A

/-- Swap of the two entries of the commutativity relation. -/
def hexSwapPair : C(A × A, A × A) :=
  ⟨fun p => (p.2,p.1), continuous_snd.prodMk continuous_fst⟩

theorem swapPair_square_id :
    polyMap (hexSwapPair A) ≫ polyMap (hexSwapPair A) =
      (𝟙 (src1 A)) := by
  rw [polyMap_comp]
  have h : (hexSwapPair A).comp (hexSwapPair A) =
      ContinuousMap.id (A × A) := by
    ext p <;> rfl
  rw [h,polyMap_id]

/-- Third explicit kind of degree-three syzygy: the involution
C(a,b)+C(b,a)=0. -/
def symBoundary : src1 A ⟶ src2 A :=
  (𝟙 (src1 A) + polyMap (hexSwapPair A)) ≫ biprod.inr

theorem symBoundary_comp_d2_zero :
    symBoundary A ≫ d2 A = 0 := by
  change ((𝟙 (src1 A) + polyMap (hexSwapPair A)) ≫ biprod.inr) ≫
    biprod.desc (d2assoc A) (d2comm A) = 0
  rw [Category.assoc,biprod.inr_desc]
  change (𝟙 (src1 A) + polyMap (hexSwapPair A)) ≫
      (𝟙 (src1 A) - polyMap (hexSwapPair A)) = 0
  simp only [Preadditive.add_comp,Preadditive.comp_sub,
    Category.id_comp,Category.comp_id,swapPair_square_id]
  abel

#print axioms symBoundary_comp_d2_zero

/-- A genuine *partial* degree-three coherence source containing the
hexagon and symmetry-involution generators. No exactness claimed. -/
noncomputable abbrev hexSymSource : CondensedAb.{u} :=
  src2assoc A ⊞ src1 A

def hexSymBoundary : hexSymSource A ⟶ src2 A :=
  biprod.desc (hexBoundary A) (symBoundary A)

theorem hexSymBoundary_comp_d2_zero :
    hexSymBoundary A ≫ d2 A = 0 := by
  change biprod.desc (hexBoundary A) (symBoundary A) ≫ d2 A = 0
  rw [biprod.desc_eq,Preadditive.add_comp]
  simp only [Category.assoc,hexBoundary_comp_d2_zero,
    symBoundary_comp_d2_zero,comp_zero,add_zero]

theorem circleTorus_hexSymBoundary_comp_d2_zero (I : Type u) :
    hexSymBoundary (I → UnitAddCircle) ≫
      d2 (I → UnitAddCircle) = 0 :=
  hexSymBoundary_comp_d2_zero (I → UnitAddCircle)

#print axioms hexSymBoundary_comp_d2_zero
#print axioms circleTorus_hexSymBoundary_comp_d2_zero

#print axioms hexBoundary_comp_d2_zero
end CMDG.CondensedCM5R0.BreenDeligneCondensed
