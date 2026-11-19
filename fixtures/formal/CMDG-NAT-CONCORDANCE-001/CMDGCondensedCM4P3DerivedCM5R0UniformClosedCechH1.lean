import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechCochains
import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverCocycleInduction

/-!
# Degree-one exactness of the actual all-tuples finite-closed Čech complex

This bridges the protected finite closed-family H1 potential theorem to
the uniform unrestricted tuple, genuine closed-intersection cochain
interface. A cocycle in degree one must be an actual coboundary in that
complex, including all index orders and repeated indices.
-/

noncomputable section
universe u v
open Set
namespace CMDG.CondensedCM5R0

theorem uniformClosedCechDegreeOne_cocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : uniformClosedCechLocalCochain X E 1)
    (hc : uniformClosedCechDifferential X E 1 c = 0) :
    ∃ b : uniformClosedCechLocalCochain X E 0,
      uniformClosedCechDifferential X E 0 b = c := by
  classical
  obtain ⟨C, rfl⟩ :=
    uniformClosedCechRestrict_surjective X E hclosed 1 c
  have hc' := hc
  rw [uniformClosedCechDifferential_restrict X E 1 C] at hc'
  have htrans (i j k : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j) (hk : x ∈ E k) :
      C ![i,k] x = C ![i,j] x + C ![j,k] x := by
    let σ : Fin 3 → I := ![i,j,k]
    have hx : x ∈ uniformClosedCechIntersection X E 2 σ := by
      simp only [uniformClosedCechIntersection, Set.mem_iInter]
      intro m
      fin_cases m <;> simp [σ, hi, hj, hk]
    have hz : (uniformClosedCechAmbientDifferential X I 1 C σ) x = 0 := by
      have h := congrArg
        (fun q : uniformClosedCechLocalCochain X E 2 => q σ ⟨x,hx⟩) hc'
      exact h
    rw [uniformClosedCechAmbientDifferential_apply] at hz
    change scalarCechDifferential 1 (fun τ => C τ x) σ = 0 at hz
    simp [scalarCechDifferential, Fin.sum_univ_succ, σ] at hz
    have hdel1 : Fin.removeNth (1 : Fin 3) ![i,j,k] = ![i,k] := by
      funext t
      fin_cases t <;> rfl
    have hdel2 : Fin.removeNth (2 : Fin 3) ![i,j,k] = ![i,j] := by
      funext t
      fin_cases t <;> rfl
    rw [hdel1,hdel2] at hz
    omega
  obtain ⟨a,ha⟩ :=
    integerFiniteClosedFamily_globalTransitions_coboundary
      X E hclosed (fun i j => C ![i,j]) htrans
  let B : uniformClosedCechAmbientCochain X I 0 :=
    fun σ => -(a (σ 0))
  refine ⟨uniformClosedCechRestrict X E 0 B, ?_⟩
  rw [uniformClosedCechDifferential_restrict]
  funext σ
  apply DFunLike.ext
  intro x
  change (uniformClosedCechAmbientDifferential X I 0 B σ) x.val =
    C σ x.val
  rw [uniformClosedCechAmbientDifferential_apply]
  simp [scalarCechDifferential, Fin.sum_univ_two, B]
  have hi : x.val ∈ E (σ 0) :=
    Set.mem_iInter.mp x.property (0 : Fin 2)
  have hj : x.val ∈ E (σ 1) :=
    Set.mem_iInter.mp x.property (1 : Fin 2)
  have hdel : Fin.removeNth (1 : Fin 2) σ (0 : Fin 1) = σ 0 := rfl
  have htail : Fin.tail σ (0 : Fin 1) = σ 1 := rfl
  rw [hdel, htail]
  have hσ : σ = ![σ 0, σ 1] := by
    funext k
    fin_cases k <;> rfl
  have hCσ : C σ x.val = C ![σ 0, σ 1] x.val :=
    congrArg (fun τ : Fin 2 → I => C τ x.val) hσ
  rw [hCσ]
  exact (ha (σ 0) (σ 1) x.val hi hj).symm

#print axioms uniformClosedCechDegreeOne_cocycle_coboundary
end CMDG.CondensedCM5R0
