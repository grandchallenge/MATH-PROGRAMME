import CMDGCondensedCM4P3DerivedCM5R0UniformCategoricalCechChainComplex
import CMDGCondensedCM4P3DerivedCM5R0UniformSplitCechBarExact
import CMDGCondensedCM4P3DerivedCM5R0StoneanProbeBarDescent

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Real vertex map from the closed profinite related-tuple object. -/
def uniformRelationVertex (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (i : Fin (n + 1)) :
    uniformRelationProfinite P T p n ⟶ P := by
  letI : CompactSpace (↥(profiniteCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed n P T p).isCompact
  exact CompHausLike.ofHom _
    (⟨fun xs : ↥(profiniteCechArityRelatedSet n P T p) =>
        xs.val i, (continuous_apply i).comp continuous_subtype_val⟩)

def uniformProbeHomSet (U : Stonean.{u}) (P : Profinite.{u}) :=
  ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj P)

def uniformProbeMap (U : Stonean.{u}) (P T : Profinite.{u})
    (p : P ⟶ T) :
    uniformProbeHomSet U P → uniformProbeHomSet U T :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map p)

def uniformProbeVertex (U : Stonean.{u}) (P T : Profinite.{u})
    (p : P ⟶ T) (n : ℕ) (i : Fin (n + 1)) :
    uniformProbeHomSet U (uniformRelationProfinite P T p n) →
      uniformProbeHomSet U P :=
  fun z => ULift.up
    (z.down ≫ profiniteToCompHaus.map (uniformRelationVertex P T p n i))

theorem uniformProbeVertices_related
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (z : uniformProbeHomSet U
        (uniformRelationProfinite P T p n)) :
    ∀ i : Fin (n + 1),
      uniformProbeMap U P T p (uniformProbeVertex U P T p n i z) =
      uniformProbeMap U P T p (uniformProbeVertex U P T p n 0 z) := by
  intro i
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  change p.hom.hom ((z.down.hom.hom x).val i) =
    p.hom.hom ((z.down.hom.hom x).val 0)
  exact (z.down.hom.hom x).property i

/-- Genuine CompHaus representable points of relation R_n, assembled
as a compatible finite family of maps U→P. -/
def uniformProbeTuple
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) :
    uniformProbeHomSet U (uniformRelationProfinite P T p n) →
      splitCechTuple (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n :=
  fun z => ⟨fun i => uniformProbeVertex U P T p n i z,
    uniformProbeVertices_related U P T p n z⟩

/-- Inverse map: compatible continuous U→P coordinates assemble
into a genuine continuous U→R_n of closed equal-image tuples. -/
def uniformProbeTupleAssemble
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ)
    (xs : splitCechTuple (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n) :
    uniformProbeHomSet U (uniformRelationProfinite P T p n) := by
  letI : CompactSpace (↥(profiniteCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechArityRelatedSet_isClosed n P T p).isCompact
  let f : C(U.compHaus, (↥(profiniteCechArityRelatedSet n P T p))) :=
    ⟨fun z => ⟨(fun i => (xs.val i).down.hom.hom z), by
       intro i
       have hi := congrArg
         (fun y : uniformProbeHomSet U T => y.down.hom.hom z)
         (xs.property i)
       change p.hom.hom ((xs.val i).down.hom.hom z) =
         p.hom.hom ((xs.val 0).down.hom.hom z) at hi
       exact hi⟩, by
       apply Continuous.subtype_mk
       apply continuous_pi
       intro i
       exact (xs.val i).down.hom.hom.continuous⟩
  exact ⟨CompHausLike.ofHom _ f⟩

theorem uniformProbeTuple_assemble_left
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ)
    (z : uniformProbeHomSet U (uniformRelationProfinite P T p n)) :
    uniformProbeTupleAssemble U P T p n
      (uniformProbeTuple U P T p n z) = z := by
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  apply Subtype.ext
  funext i
  rfl

theorem uniformProbeTuple_assemble_right
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ)
    (xs : splitCechTuple (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n) :
    uniformProbeTuple U P T p n
      (uniformProbeTupleAssemble U P T p n xs) = xs := by
  apply Subtype.ext
  funext i
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  rfl

/-- Genuine all-arity representation comparison, not a bounded
list of degree-two-through-degree-five analogues. -/
def uniformProbeTupleEquiv
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    uniformProbeHomSet U (uniformRelationProfinite P T p n) ≃
      splitCechTuple (uniformProbeHomSet U P)
        (uniformProbeHomSet U T) (uniformProbeMap U P T p) n where
  toFun := uniformProbeTuple U P T p n
  invFun := uniformProbeTupleAssemble U P T p n
  left_inv := uniformProbeTuple_assemble_left U P T p n
  right_inv := uniformProbeTuple_assemble_right U P T p n

/-- Exact Hom-set face induced by an actual profinite relation map. -/
def uniformProbeFace
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (k : Fin (n + 2)) :
    uniformProbeHomSet U (uniformRelationProfinite P T p (n + 1)) →
      uniformProbeHomSet U (uniformRelationProfinite P T p n) :=
  fun z => ULift.up (z.down ≫
    profiniteToCompHaus.map (uniformRelationFace P T p n k))

theorem uniformProbeTuple_face
    (U : Stonean.{u}) (P T : Profinite.{u}) (p : P ⟶ T)
    (n : ℕ) (k : Fin (n + 2))
    (z : uniformProbeHomSet U (uniformRelationProfinite P T p (n + 1))) :
    uniformProbeTuple U P T p n
      (uniformProbeFace U P T p n k z) =
    splitCechFace (uniformProbeHomSet U P)
      (uniformProbeHomSet U T) (uniformProbeMap U P T p) n k
        (uniformProbeTuple U P T p (n + 1) z) := by
  apply Subtype.ext
  funext i
  apply ULift.ext
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  rfl

#print axioms uniformProbeTuple_face

#print axioms uniformProbeTupleEquiv

#print axioms uniformProbeVertices_related

end CMDG.CondensedCM5R0
