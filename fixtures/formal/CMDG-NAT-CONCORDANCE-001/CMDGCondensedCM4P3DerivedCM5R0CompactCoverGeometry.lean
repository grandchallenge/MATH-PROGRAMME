import CMDGCondensedCM4P3DerivedCM5R0UniformProbeAugmentationExact

/-! Genuine equal-image tuples for an arbitrary compact Hausdorff
target of a profinite cover. Every relation object is profinite.
The actual Stonean Hom-set comparison and the signed free bar
contraction hold without assuming the target itself is profinite.
Generalized from the admitted uniform profinite relation proofs. -/
noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0.CompactCover

def compactCechArityRelatedSet
    (n : ℕ) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    Set (Fin (n + 1) → P) :=
  {xs | ∀ i : Fin (n + 1),
    p.hom.hom (xs i) = p.hom.hom (xs 0)}

theorem compactCechArityRelatedSet_isClosed
    (n : ℕ) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) :
    IsClosed (compactCechArityRelatedSet n P T p) := by
  have hi (i : Fin (n+1)) :
      IsClosed {xs : Fin (n+1) → P |
        p.hom.hom (xs i) = p.hom.hom (xs 0)} := by
    exact isClosed_eq
      (p.hom.hom.continuous.comp (continuous_apply i))
      (p.hom.hom.continuous.comp (continuous_apply 0))
  have h : IsClosed (⋂ i : Fin (n+1),
      {xs : Fin (n+1) → P |
        p.hom.hom (xs i) = p.hom.hom (xs 0)}) :=
    isClosed_iInter hi
  simpa only [compactCechArityRelatedSet, Set.setOf_forall] using h

def compactRelationFaceMap
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ)
    (k : Fin (n + 2)) :
    C(↥(compactCechArityRelatedSet (n + 1) P T p),
      ↥(compactCechArityRelatedSet n P T p)) :=
  ⟨fun xs =>
    ⟨xs.val ∘ k.succAbove, by
      intro i
      exact (xs.property (k.succAbove i)).trans
        (xs.property (k.succAbove 0)).symm⟩,
    Continuous.subtype_mk
      (by
        apply continuous_pi
        intro i
        exact (continuous_apply (k.succAbove i)).comp
          continuous_subtype_val) _⟩

def compactRelationProfinite
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) : Profinite.{u} :=
  letI : CompactSpace (↥(compactCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed n P T p).isCompact
  Profinite.of (↥(compactCechArityRelatedSet n P T p))

/-- Continuous face deletion as an honest Profinite morphism. -/
def compactRelationFace
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ)
    (k : Fin (n + 2)) :
    compactRelationProfinite P T p (n + 1) ⟶
      compactRelationProfinite P T p n := by
  letI : CompactSpace (↥(compactCechArityRelatedSet (n + 1) P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed (n + 1) P T p).isCompact
  letI : CompactSpace (↥(compactCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed n P T p).isCompact
  exact CompHausLike.ofHom _
    (compactRelationFaceMap P T p n k)

def compactRelationVertex (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (i : Fin (n + 1)) :
    compactRelationProfinite P T p n ⟶ P := by
  letI : CompactSpace (↥(compactCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed n P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun xs : ↥(compactCechArityRelatedSet n P T p) =>
        xs.val i, (continuous_apply i).comp continuous_subtype_val⟩)

def compactProbeHomSet (U : Stonean.{u}) (T : CompHaus.{u}) :=
  ULift.{u + 1} (U.compHaus ⟶ T)

def compactProbeMap (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) :
    uniformProbeHomSet U P → compactProbeHomSet U T :=
  fun z => ULift.up (z.down ≫ p)

def compactProbeVertex (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u})
    (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) (i : Fin (n + 1)) :
    uniformProbeHomSet U (compactRelationProfinite P T p n) →
      uniformProbeHomSet U P :=
  fun z => ULift.up
    (z.down ≫ profiniteToCompHaus.map (compactRelationVertex P T p n i))

theorem compactProbeVertices_related
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (z : uniformProbeHomSet U
        (compactRelationProfinite P T p n)) :
    ∀ i : Fin (n + 1),
      compactProbeMap U P T p (compactProbeVertex U P T p n i z) =
      compactProbeMap U P T p (compactProbeVertex U P T p n 0 z) := by
  intro i
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  change p.hom.hom ((z.down.hom.hom x).val i) =
    p.hom.hom ((z.down.hom.hom x).val 0)
  exact (z.down.hom.hom x).property i

/-- Genuine CompHaus representable points of relation R_n, assembled
as a compatible finite family of maps U→P. -/
def compactProbeTuple
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) :
    uniformProbeHomSet U (compactRelationProfinite P T p n) →
      splitCechTuple (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n :=
  fun z => ⟨fun i => compactProbeVertex U P T p n i z,
    compactProbeVertices_related U P T p n z⟩

/-- Inverse map: compatible continuous U→P coordinates assemble
into a genuine continuous U→R_n of closed equal-image tuples. -/
def compactProbeTupleAssemble
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ)
    (xs : splitCechTuple (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n) :
    uniformProbeHomSet U (compactRelationProfinite P T p n) := by
  letI : CompactSpace (↥(compactCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (compactCechArityRelatedSet_isClosed n P T p).isCompact
  let f : C(U.compHaus, (↥(compactCechArityRelatedSet n P T p))) :=
    ⟨fun z => ⟨(fun i => (xs.val i).down.hom.hom z), by
       intro i
       have hi := congrArg
         (fun y : compactProbeHomSet U T => y.down.hom.hom z)
         (xs.property i)
       change p.hom.hom ((xs.val i).down.hom.hom z) =
         p.hom.hom ((xs.val 0).down.hom.hom z) at hi
       exact hi⟩, by
       apply Continuous.subtype_mk
       apply continuous_pi
       intro i
       exact (xs.val i).down.hom.hom.continuous⟩
  exact ⟨CompHausLike.ofHom _ f⟩

theorem compactProbeTuple_assemble_left
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ)
    (z : uniformProbeHomSet U (compactRelationProfinite P T p n)) :
    compactProbeTupleAssemble U P T p n
      (compactProbeTuple U P T p n z) = z := by
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  apply Subtype.ext
  funext i
  rfl

theorem compactProbeTuple_assemble_right
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ)
    (xs : splitCechTuple (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n) :
    compactProbeTuple U P T p n
      (compactProbeTupleAssemble U P T p n xs) = xs := by
  apply Subtype.ext
  funext i
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  rfl

/-- Genuine all-arity representation comparison, not a bounded
list of degree-two-through-degree-five analogues. -/
def compactProbeTupleEquiv
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    uniformProbeHomSet U (compactRelationProfinite P T p n) ≃
      splitCechTuple (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n where
  toFun := compactProbeTuple U P T p n
  invFun := compactProbeTupleAssemble U P T p n
  left_inv := compactProbeTuple_assemble_left U P T p n
  right_inv := compactProbeTuple_assemble_right U P T p n

/-- Exact Hom-set face induced by an actual profinite relation map. -/
def compactProbeFace
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (k : Fin (n + 2)) :
    uniformProbeHomSet U (compactRelationProfinite P T p (n + 1)) →
      uniformProbeHomSet U (compactRelationProfinite P T p n) :=
  fun z => ULift.up (z.down ≫
    profiniteToCompHaus.map (compactRelationFace P T p n k))

theorem compactProbeTuple_face
    (U : Stonean.{u}) (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (k : Fin (n + 2))
    (z : uniformProbeHomSet U (compactRelationProfinite P T p (n + 1))) :
    compactProbeTuple U P T p n
      (compactProbeFace U P T p n k z) =
    splitCechFace (uniformProbeHomSet U P)
      (compactProbeHomSet U T) (compactProbeMap U P T p) n k
        (compactProbeTuple U P T p (n + 1) z) := by
  apply Subtype.ext
  funext i
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  rfl

private abbrev compactFreeProbe (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :=
  (ModuleCat.free Coeff).obj
    (uniformProbeHomSet U (compactRelationProfinite P T p n))

/-- True represented free-site all-degree face sum, evaluated
at the exact Stonean CompHaus test object. -/
def compactProbeBarD (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactFreeProbe U P T p (n + 1) ⟶ compactFreeProbe U P T p n :=
  ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    (ModuleCat.free Coeff).map
      (↾compactProbeFace U P T p n k)

/-- Actual free-module isomorphism from real represented
relation Hom-set to the split compatible-tuple bar object. -/
def compactProbeBarIso (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactFreeProbe U P T p n ≅
    (ModuleCat.free Coeff).obj
      (splitCechTuple (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n) :=
  (ModuleCat.free Coeff).mapIso
    (compactProbeTupleEquiv U P T p n).toIso

theorem compactProbeFace_bar_square (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (n : ℕ) (k : Fin (n + 2)) :
    (ModuleCat.free Coeff).map (↾compactProbeFace U P T p n k) ≫
      (compactProbeBarIso U P T p n).hom =
    (compactProbeBarIso U P T p (n + 1)).hom ≫
      (ModuleCat.free Coeff).map
        (↾splitCechFace (uniformProbeHomSet U P)
          (compactProbeHomSet U T) (compactProbeMap U P T p) n k) := by
  change (ModuleCat.free Coeff).map (↾compactProbeFace U P T p n k) ≫
      (ModuleCat.free Coeff).map
        (↾compactProbeTupleEquiv U P T p n) =
    (ModuleCat.free Coeff).map (↾compactProbeTupleEquiv U P T p (n + 1)) ≫
      (ModuleCat.free Coeff).map
        (↾splitCechFace (uniformProbeHomSet U P)
          (compactProbeHomSet U T) (compactProbeMap U P T p) n k)
  rw [← Functor.map_comp, ← Functor.map_comp]
  congr 1

theorem compactProbeBarD_square (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactProbeBarD U P T p n ≫
      (compactProbeBarIso U P T p n).hom =
    (compactProbeBarIso U P T p (n + 1)).hom ≫
      splitBarD (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n := by
  unfold compactProbeBarD splitBarD
  rw [Preadditive.sum_comp, Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro k hk
  rw [Preadditive.zsmul_comp, Preadditive.comp_zsmul,
    compactProbeFace_bar_square]

theorem compactProbeBarD_comp_D_zero (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactProbeBarD U P T p (n + 1) ≫
      compactProbeBarD U P T p n = 0 := by
  apply (cancel_mono (compactProbeBarIso U P T p n).hom).1
  calc
    (compactProbeBarD U P T p (n + 1) ≫
      compactProbeBarD U P T p n) ≫
        (compactProbeBarIso U P T p n).hom =
        compactProbeBarD U P T p (n + 1) ≫
          (compactProbeBarD U P T p n ≫
            (compactProbeBarIso U P T p n).hom) := Category.assoc _ _ _
    _ = compactProbeBarD U P T p (n + 1) ≫
          ((compactProbeBarIso U P T p (n + 1)).hom ≫
            splitBarD (uniformProbeHomSet U P)
              (compactProbeHomSet U T) (compactProbeMap U P T p) n) := by
            rw [compactProbeBarD_square]
    _ = (compactProbeBarD U P T p (n + 1) ≫
          (compactProbeBarIso U P T p (n + 1)).hom) ≫
            splitBarD (uniformProbeHomSet U P)
              (compactProbeHomSet U T) (compactProbeMap U P T p) n :=
            (Category.assoc _ _ _).symm
    _ = ((compactProbeBarIso U P T p (n + 2)).hom ≫
          splitBarD (uniformProbeHomSet U P)
            (compactProbeHomSet U T) (compactProbeMap U P T p) (n + 1)) ≫
              splitBarD (uniformProbeHomSet U P)
                (compactProbeHomSet U T) (compactProbeMap U P T p) n := by
            rw [compactProbeBarD_square]
    _ = 0 := by rw [Category.assoc, splitBarD_comp_D_zero, comp_zero]

def compactProbeBarShortComplex (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (compactProbeBarD U P T p (n + 1))
    (compactProbeBarD U P T p n)
    (compactProbeBarD_comp_D_zero U P T p n)

def compactProbeBarShortIso (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) (n : ℕ) :
    compactProbeBarShortComplex U P T p n ≅
      splitBarShortComplex (uniformProbeHomSet U P)
        (compactProbeHomSet U T) (compactProbeMap U P T p) n := by
  refine ShortComplex.isoMk
    (compactProbeBarIso U P T p (n + 2))
    (compactProbeBarIso U P T p (n + 1))
    (compactProbeBarIso U P T p n) ?_ ?_
  · exact (compactProbeBarD_square U P T p (n + 1)).symm
  · exact (compactProbeBarD_square U P T p n).symm

/-- A split presentation on genuine CompHaus Stonean Hom sets
implies exactness at every internal term of its TRUE probe bar. -/
theorem compactProbeBarShortExact (U : Stonean.{u})
    (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
    (s : compactProbeHomSet U T → uniformProbeHomSet U P)
    (hs : ∀ b, compactProbeMap U P T p (s b) = b)
    (n : ℕ) :
    (compactProbeBarShortComplex U P T p n).Exact := by
  exact ShortComplex.exact_of_iso
    (compactProbeBarShortIso U P T p n).symm
    (splitBarShortComplex_exact (uniformProbeHomSet U P)
      (compactProbeHomSet U T) (compactProbeMap U P T p) s hs n)

/-- Surjectivity of the true map on each Stonean Hom set,
not a global splitting of the compact Hausdorff cover. -/
theorem compactProbeSplit (U : Stonean.{u}) (P : Profinite.{u})
    (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] :
    ∃ s : compactProbeHomSet U T → uniformProbeHomSet U P,
      ∀ b, compactProbeMap U P T p (s b) = b := by
  refine ⟨fun z => ULift.up (CompHaus.lift z.down p), ?_⟩
  intro z
  rcases z with ⟨q⟩
  exact congrArg ULift.up (CompHaus.lift_lifts q p)

theorem compactProbeBarExact (U : Stonean.{u}) (P : Profinite.{u})
    (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] (n : ℕ) :
    (compactProbeBarShortComplex U P T p n).Exact := by
  obtain ⟨s,hs⟩ := compactProbeSplit U P T p
  exact compactProbeBarShortExact U P T p s hs n

#print axioms compactCechArityRelatedSet_isClosed
#print axioms compactRelationProfinite
#print axioms compactProbeTupleEquiv
#print axioms compactProbeTuple_face
#print axioms compactProbeBarExact
end CMDG.CondensedCM5R0.CompactCover
