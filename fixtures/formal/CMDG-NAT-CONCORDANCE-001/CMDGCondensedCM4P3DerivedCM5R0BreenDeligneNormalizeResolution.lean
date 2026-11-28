import CMDGCondensedCM4P3DerivedCM5R0BreenDelignePolynomialSum
import CMDGCondensedCM4P3DerivedCM5R0CanonicalUnitLatticeBD
import Mathlib.CategoryTheory.Limits.Preserves.Shapes.Biproducts

/-! Normalize the actual coherent small-lattice resolution to finite
polynomial arity families in the lifted category and instantiate the
Breen–Deligne package without hypotheses. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory CategoryTheory.Limits
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneProbe
open CMDG.CondensedCM5R0.BreenDeligneUniverseLift
open CMDG.CondensedCM5R0.BreenDeligneLiftRepresentable
open CMDG.CondensedCM5R0.BreenDelignePolynomialSum
open CMDG.CondensedCM5R0.BreenDeligneLatticeFP
open CMDG.CondensedCM5R0.BreenDeligneLatticePseudocoherence
open CMDG.CondensedCM5R0.BreenDeligneCoherentResolution
namespace CMDG.CondensedCM5R0.BreenDeligneNormalizeResolution

abbrev Poly {k : ℕ} (a : Fin k → ℕ) : BC.{u} :=
  UniversalExtension.incl ⋙ polynomial a

theorem emptyPoly_zero : IsZero (Poly.{u} (fun i : Fin 0 => i.elim0)) := by
  apply (IsZero.iff_id_eq_zero _).mpr
  apply NatTrans.ext
  funext r
  apply ModuleCat.free_hom_ext
  rintro ⟨j,x⟩
  exact j.elim0

def transportSumIso (F G : BreenDeligneLatticeFP.LC) :
    BreenDeligneUniverseLift.transport.{u}.obj (F ⊞ G) ≅ BreenDeligneUniverseLift.transport.obj F ⊞ BreenDeligneUniverseLift.transport.obj G := by
  let T := BreenDeligneUniverseLift.transport.{u}
  haveI : T.Additive := by infer_instance
  refine { hom := Functor.biprodComparison T F G
           inv := Functor.biprodComparison' T F G
           hom_inv_id := ?_
           inv_hom_id := Functor.biprodComparison'_comp_biprodComparison T F G }
  rw [Functor.biprodComparison,Functor.biprodComparison',biprod.lift_desc,
    ← T.map_comp,← T.map_comp,← T.map_add,biprod.total,T.map_id]

theorem finite_normal {F : BreenDeligneLatticeFP.LC} (h : FinitePoly F) :
    ∃ k : ℕ, ∃ a : Fin k → ℕ, Nonempty (BreenDeligneUniverseLift.transport.{u}.obj F ≅ Poly a) := by
  induction h with
  | zero =>
    refine ⟨0,fun i => i.elim0,⟨?_⟩⟩
    exact (BreenDeligneUniverseLift.transport.{u}.map_isZero (isZero_zero BreenDeligneLatticeFP.LC)).iso emptyPoly_zero
  | rep r => exact ⟨1,singleArity r,⟨repIso r⟩⟩
  | @sum F G hF hG iF iG =>
    obtain ⟨k,a,⟨e⟩⟩ := iF
    obtain ⟨l,b,⟨e'⟩⟩ := iG
    exact ⟨k+l,append a b,⟨transportSumIso F G ≪≫ biprod.mapIso e e' ≪≫
      polynomialSumIso a b⟩⟩

structure NormalForm (F : BreenDeligneLatticeFP.LC) where
  count : ℕ
  arity : Fin count → ℕ
  iso : BreenDeligneUniverseLift.transport.{u}.obj F ≅ Poly arity

def normalize (F : BreenDeligneLatticeFP.LC) (h : FinitePoly F) : NormalForm.{u} F :=
  Classical.choice (show Nonempty (NormalForm.{u} F) from by
    obtain ⟨k,a,⟨e⟩⟩ := finite_normal.{u} h
    exact ⟨⟨k,a,e⟩⟩)

abbrev oldTerm (n : ℕ) := term latFinite identity_fp n

def normal (n : ℕ) : NormalForm.{u} (oldTerm n) :=
  normalize _ (ordinary_finite n)

abbrev newTerm (n : ℕ) : BC.{u} := Poly (normal.{u} n).arity
abbrev e (n : ℕ) : BreenDeligneUniverseLift.transport.{u}.obj (oldTerm n) ≅ newTerm n := (normal n).iso

def aug' : newTerm.{u} 0 ⟶ UniversalExtension.incl :=
  (e 0).inv ≫ BreenDeligneUniverseLift.transport.map (aug latFinite identity_fp) ≫ identityIso.hom

def d' (n : ℕ) : newTerm.{u} (n+1) ⟶ newTerm n :=
  (e (n+1)).inv ≫ BreenDeligneUniverseLift.transport.map (d latFinite identity_fp n) ≫ (e n).hom

theorem aug'_zero : d'.{u} 0 ≫ aug' = 0 := by
  unfold d' aug'
  simp only [Category.assoc,Iso.hom_inv_id_assoc,← Functor.map_comp_assoc,aug_zero,
    Functor.map_zero,zero_comp,comp_zero]

theorem d'_sq (n : ℕ) : d'.{u} (n+1) ≫ d' n = 0 := by
  unfold d'
  simp only [Category.assoc,Iso.hom_inv_id_assoc,← Functor.map_comp_assoc,sq_zero,
    Functor.map_zero,zero_comp,comp_zero]

theorem aug'_epi : Epi aug'.{u} := by
  haveI : Epi (aug latFinite identity_fp) := cover_epi latFinite identity_fp 0
  haveI := transport_epi.{u} (aug latFinite identity_fp)
  unfold aug'
  infer_instance

theorem aug'_exact : (ShortComplex.mk (d'.{u} 0) aug' aug'_zero).Exact := by
  let S := ShortComplex.mk (d latFinite identity_fp 0) (aug latFinite identity_fp)
    (aug_zero latFinite identity_fp)
  have h : (S.map BreenDeligneUniverseLift.transport.{u}).Exact := transport_exact _ (aug_exact latFinite identity_fp)
  apply ShortComplex.exact_of_iso (ShortComplex.isoMk (e 1) (e 0) identityIso
    (by simp [d',S]) (by simp [aug',S])) h

theorem d'_exact (n : ℕ) :
    (ShortComplex.mk (d'.{u} (n+1)) (d' n) (d'_sq n)).Exact := by
  let S := ShortComplex.mk (d latFinite identity_fp (n+1)) (d latFinite identity_fp n)
    (sq_zero latFinite identity_fp n)
  have h : (S.map BreenDeligneUniverseLift.transport.{u}).Exact := transport_exact _ (BreenDeligneCoherentResolution.exact latFinite identity_fp n)
  apply ShortComplex.exact_of_iso (ShortComplex.isoMk (e (n+2)) (e (n+1)) (e n)
    (by simp [d',S]) (by simp [d',S])) h

def actualLatticeBD : UniversalExtension.LatticeBD.{u} where
  count n := (normal n).count
  arity n := (normal n).arity
  aug := aug'
  d := d'
  aug_zero := aug'_zero
  sq_zero := d'_sq
  aug_epi := aug'_epi
  aug_exact := aug'_exact
  exact := d'_exact

#print axioms actualLatticeBD
end CMDG.CondensedCM5R0.BreenDeligneNormalizeResolution
