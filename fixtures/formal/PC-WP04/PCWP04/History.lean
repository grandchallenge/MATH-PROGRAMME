import Mathlib

/-!
# PC-WP04 bounded surgery-history certificate

This file formalizes only the finite combinatorial evaluator exported by
PC-WP03. It does not formalize Ricci flow, neck detection, cap geometry,
surgery existence, noncollapsing, or finite extinction.

The imported boundary is represented by `ImportedEventRelation`: an explicit
relation asserting that a source-certified topology event has the recorded
reconstruction equations. All evaluator theorems are conditional on that
relation and on the structural `EventContract`.
-/

namespace PCWP04

abbrev ComponentId := Nat

inductive FactorAtom where
  | s3
  | sphericalSpaceFormNontrivial
  | s2BundleOverS1Orientable
  | s2BundleOverS1Nonorientable
  deriving DecidableEq, Repr, Inhabited

inductive FactorCertificate where
  | atom (value : FactorAtom)
  | rp3SumRp3
  deriving DecidableEq, Repr, Inhabited

abbrev FactorExpr := List FactorAtom

def normalizeCertificate : FactorCertificate → FactorExpr
  | .atom value => [value]
  | .rp3SumRp3 =>
      [.sphericalSpaceFormNontrivial, .sphericalSpaceFormNontrivial]

def normalizeCertificates (xs : List FactorCertificate) : FactorExpr :=
  xs.flatMap normalizeCertificate

structure SourceBinding where
  provider : String
  theoremId : String
  version : String
  locator : String
  importedAssumptions : List String
  deriving DecidableEq, Repr, Inhabited

structure Reconstruction where
  children : List ComponentId
  emitted : List FactorCertificate
  deriving DecidableEq, Repr, Inhabited

structure Event where
  eventId : String
  pre : List ComponentId
  post : List ComponentId
  unchanged : List ComponentId
  rebuild : ComponentId → Option Reconstruction
  source : SourceBinding

abbrev Valuation := ComponentId → Option FactorExpr
abbrev SemanticValuation := ComponentId → FactorExpr

def evalChildren (v : Valuation) : List ComponentId → Option FactorExpr
  | [] => some []
  | c :: cs => do
      let head ← v c
      let tail ← evalChildren v cs
      pure (head ++ tail)

def evalReconstruction (v : Valuation) (r : Reconstruction) : Option FactorExpr := do
  let children ← evalChildren v r.children
  pure (children ++ normalizeCertificates r.emitted)

def evalChildrenTotal (v : SemanticValuation) (children : List ComponentId) : FactorExpr :=
  children.flatMap v

def evalReconstructionTotal (v : SemanticValuation) (r : Reconstruction) : FactorExpr :=
  evalChildrenTotal v r.children ++ normalizeCertificates r.emitted

def stepBack (e : Event) (v : Valuation) : Valuation := fun c =>
  if hpre : c ∈ e.pre then
    if hunchanged : c ∈ e.unchanged then
      v c
    else
      match e.rebuild c with
      | some r => evalReconstruction v r
      | none => none
  else
    none

def Covers (v : Valuation) (active : List ComponentId) : Prop :=
  ∀ c, c ∈ active → ∃ expr, v c = some expr

def ExactSupport (v : Valuation) (active : List ComponentId) : Prop :=
  Covers v active ∧ ∀ c, c ∉ active → v c = none

def Encodes (v : Valuation) (semantic : SemanticValuation)
    (active : List ComponentId) : Prop :=
  ∀ c, c ∈ active → v c = some (semantic c)

def ChildOwnedBy (e : Event) (parent child : ComponentId) : Prop :=
  ∃ r, e.rebuild parent = some r ∧ child ∈ r.children

def NoComponentLoss (e : Event) : Prop :=
  ∀ child, child ∈ e.post →
    child ∈ e.unchanged ∨
      ∃! parent, parent ∈ e.pre ∧ parent ∉ e.unchanged ∧ ChildOwnedBy e parent child

structure EventContract (e : Event) : Prop where
  pre_nodup : e.pre.Nodup
  post_nodup : e.post.Nodup
  unchanged_nodup : e.unchanged.Nodup
  unchanged_pre : ∀ c, c ∈ e.unchanged → c ∈ e.pre
  unchanged_post : ∀ c, c ∈ e.unchanged → c ∈ e.post
  rebuilt : ∀ c, c ∈ e.pre → c ∉ e.unchanged →
    ∃ r, e.rebuild c = some r
  children_post : ∀ parent r child,
    e.rebuild parent = some r → child ∈ r.children → child ∈ e.post
  rebuild_none_outside : ∀ c, c ∉ e.pre → e.rebuild c = none
  source_provider : e.source.provider ≠ ""
  source_theorem : e.source.theoremId ≠ ""
  source_version : e.source.version ≠ ""
  source_locator : e.source.locator ≠ ""
  no_component_loss : NoComponentLoss e

structure CertifiedEvent where
  event : Event
  contract : EventContract event

def ImportedEventRelation (e : Event)
    (before after : SemanticValuation) : Prop :=
  (∀ c, c ∈ e.unchanged → before c = after c) ∧
  (∀ c, c ∈ e.pre → c ∉ e.unchanged →
    ∃ r, e.rebuild c = some r ∧ before c = evalReconstructionTotal after r)

def runBackward : List CertifiedEvent → Valuation → Valuation
  | [], v => v
  | e :: rest, v => stepBack e.event (runBackward rest v)

inductive ImportedHistoryRelation :
    List CertifiedEvent → SemanticValuation → SemanticValuation →
      List ComponentId → List ComponentId → Prop where
  | nil (semantic : SemanticValuation) (active : List ComponentId) :
      ImportedHistoryRelation [] semantic semantic active active
  | cons (head : CertifiedEvent) (tail : List CertifiedEvent)
      (before middle terminal : SemanticValuation)
      (terminalActive : List ComponentId)
      (headRelation : ImportedEventRelation head.event before middle)
      (tailRelation : ImportedHistoryRelation tail middle terminal
        head.event.post terminalActive) :
      ImportedHistoryRelation (head :: tail) before terminal
        head.event.pre terminalActive

structure Certificate where
  initialValuation : Valuation
  sources : List SourceBinding

def buildCertificate (events : List CertifiedEvent) (terminal : Valuation) : Certificate :=
  {
    initialValuation := runBackward events terminal
    sources := events.map (fun e => e.event.source)
  }

@[simp] theorem buildCertificate_sources
    (events : List CertifiedEvent) (terminal : Valuation) :
    (buildCertificate events terminal).sources =
      events.map (fun e => e.event.source) := rfl

theorem evalChildren_some_of_covers
    (v : Valuation) (children : List ComponentId)
    (h : ∀ c, c ∈ children → ∃ expr, v c = some expr) :
    ∃ expr, evalChildren v children = some expr := by
  induction children with
  | nil =>
      exact ⟨[], rfl⟩
  | cons c cs ih =>
      obtain ⟨head, hhead⟩ := h c (by simp)
      have htail : ∀ d, d ∈ cs → ∃ expr, v d = some expr := by
        intro d hd
        exact h d (by simp [hd])
      obtain ⟨tail, htailEval⟩ := ih htail
      exact ⟨head ++ tail, by simp [evalChildren, hhead, htailEval]⟩

theorem evalChildren_exact
    (v : Valuation) (semantic : SemanticValuation)
    (children : List ComponentId)
    (h : ∀ c, c ∈ children → v c = some (semantic c)) :
    evalChildren v children = some (evalChildrenTotal semantic children) := by
  induction children with
  | nil => rfl
  | cons c cs ih =>
      have hhead : v c = some (semantic c) := h c (by simp)
      have htail : ∀ d, d ∈ cs → v d = some (semantic d) := by
        intro d hd
        exact h d (by simp [hd])
      simp [evalChildren, evalChildrenTotal, hhead, ih htail]

theorem evalReconstruction_exact
    (v : Valuation) (semantic : SemanticValuation)
    (r : Reconstruction)
    (h : ∀ c, c ∈ r.children → v c = some (semantic c)) :
    evalReconstruction v r = some (evalReconstructionTotal semantic r) := by
  simp [evalReconstruction, evalReconstructionTotal,
    evalChildren_exact v semantic r.children h]

theorem eventContract_noComponentLoss
    (e : Event) (h : EventContract e) : NoComponentLoss e :=
  h.no_component_loss

theorem stepBack_covers
    (e : Event) (contract : EventContract e)
    (v : Valuation) (hv : Covers v e.post) :
    Covers (stepBack e v) e.pre := by
  intro c hcpre
  by_cases hunchanged : c ∈ e.unchanged
  · obtain ⟨expr, hexpr⟩ := hv c (contract.unchanged_post c hunchanged)
    exact ⟨expr, by simp [stepBack, hcpre, hunchanged, hexpr]⟩
  · obtain ⟨r, hr⟩ := contract.rebuilt c hcpre hunchanged
    have hchildren : ∀ child, child ∈ r.children →
        ∃ expr, v child = some expr := by
      intro child hchild
      exact hv child (contract.children_post c r child hr hchild)
    obtain ⟨expr, hexpr⟩ := evalChildren_some_of_covers v r.children hchildren
    exact ⟨expr ++ normalizeCertificates r.emitted, by
      simp [stepBack, hcpre, hunchanged, hr, evalReconstruction, hexpr]⟩

theorem stepBack_none_outside
    (e : Event) (v : Valuation) (c : ComponentId)
    (hc : c ∉ e.pre) : stepBack e v c = none := by
  simp [stepBack, hc]

theorem stepBack_exactSupport
    (e : Event) (contract : EventContract e)
    (v : Valuation) (hv : Covers v e.post) :
    ExactSupport (stepBack e v) e.pre := by
  constructor
  · exact stepBack_covers e contract v hv
  · intro c hc
    exact stepBack_none_outside e v c hc

theorem stepBack_correct
    (e : Event) (contract : EventContract e)
    (before after : SemanticValuation)
    (relation : ImportedEventRelation e before after)
    (v : Valuation) (hv : Encodes v after e.post) :
    Encodes (stepBack e v) before e.pre := by
  intro c hcpre
  by_cases hunchanged : c ∈ e.unchanged
  · have hpost := contract.unchanged_post c hunchanged
    have henc := hv c hpost
    have hsem := relation.1 c hunchanged
    simp [stepBack, hcpre, hunchanged, henc, hsem]
  · obtain ⟨r, hr, hbefore⟩ := relation.2 c hcpre hunchanged
    have hchildren : ∀ child, child ∈ r.children →
        v child = some (after child) := by
      intro child hchild
      exact hv child (contract.children_post c r child hr hchild)
    have heval := evalReconstruction_exact v after r hchildren
    simp [stepBack, hcpre, hunchanged, hr, heval, hbefore]

theorem runBackward_correct
    {events : List CertifiedEvent}
    {before terminal : SemanticValuation}
    {initialActive terminalActive : List ComponentId}
    (relation : ImportedHistoryRelation events before terminal
      initialActive terminalActive)
    (v : Valuation) (hv : Encodes v terminal terminalActive) :
    Encodes (runBackward events v) before initialActive := by
  induction relation with
  | nil semantic active =>
      simpa [runBackward] using hv
  | cons head tail before middle terminal terminalActive headRelation tailRelation ih =>
      exact stepBack_correct head.event head.contract before middle
        headRelation (runBackward tail v) (ih v hv)

theorem runBackward_covers
    {events : List CertifiedEvent}
    {before terminal : SemanticValuation}
    {initialActive terminalActive : List ComponentId}
    (relation : ImportedHistoryRelation events before terminal
      initialActive terminalActive)
    (v : Valuation) (hv : Covers v terminalActive) :
    Covers (runBackward events v) initialActive := by
  induction relation with
  | nil semantic active =>
      simpa [runBackward] using hv
  | cons head tail before middle terminal terminalActive headRelation tailRelation ih =>
      exact stepBack_covers head.event head.contract (runBackward tail v) (ih v hv)

def contributesNontrivialGroup : FactorAtom → Bool
  | .s3 => false
  | .sphericalSpaceFormNontrivial => true
  | .s2BundleOverS1Orientable => true
  | .s2BundleOverS1Nonorientable => true

def simplyConnectedCompatible (expr : FactorExpr) : Bool :=
  expr.all (fun atom => !(contributesNontrivialGroup atom))

theorem atom_eq_s3_of_group_trivial
    (atom : FactorAtom)
    (h : contributesNontrivialGroup atom = false) : atom = .s3 := by
  cases atom <;> simp [contributesNontrivialGroup] at h ⊢

theorem all_s3_of_simplyConnectedCompatible
    (expr : FactorExpr)
    (h : simplyConnectedCompatible expr = true) :
    ∀ atom, atom ∈ expr → atom = .s3 := by
  intro atom hatom
  have hfalse : contributesNontrivialGroup atom = false := by
    have hall : ∀ x ∈ expr, (!(contributesNontrivialGroup x)) = true := by
      simpa [simplyConnectedCompatible, List.all_eq_true] using h
    have hnot := hall atom hatom
    cases hvalue : contributesNontrivialGroup atom <;>
      simp [hvalue] at hnot ⊢
  exact atom_eq_s3_of_group_trivial atom hfalse

example : normalizeCertificate .rp3SumRp3 =
    [.sphericalSpaceFormNontrivial, .sphericalSpaceFormNontrivial] := rfl

example : simplyConnectedCompatible [.s3, .s3] = true := by decide

example : simplyConnectedCompatible
    [.s3, .s2BundleOverS1Orientable] = false := by decide

end PCWP04
