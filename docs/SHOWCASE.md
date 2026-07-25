# Showcase

<p class="page-deck">The programme in one view: three mathematical execution modes, one continuity layer, eight governed domains, explicit handoffs, and a refusal to confuse momentum with completion.</p>

<div class="showcase-declaration">
  <span>Purpose</span>
  <p>Make mathematical work cumulative, inspectable, and difficult to fool.</p>
</div>

<div class="programme-spine programme-spine--page" aria-label="MATH-PROGRAMME workflow">
  <div class="programme-spine__stage">
    <span class="programme-spine__number">I</span>
    <span class="programme-spine__name">MATHFORGE</span>
    <span class="programme-spine__verb">Questions become maps</span>
  </div>
  <span class="programme-spine__arrow" aria-hidden="true">→</span>
  <div class="programme-spine__stage">
    <span class="programme-spine__number">II</span>
    <span class="programme-spine__name">MATHSOLVE</span>
    <span class="programme-spine__verb">Maps become campaigns</span>
  </div>
  <span class="programme-spine__arrow" aria-hidden="true">→</span>
  <div class="programme-spine__stage">
    <span class="programme-spine__number">III</span>
    <span class="programme-spine__name">MATHCERT</span>
    <span class="programme-spine__verb">Claims meet the boundary</span>
  </div>
</div>

`MATH-PROGRAMME` preserves governance, decisions, terminology, publication, archival state, and the authoritative integrated artifact. It is not a fourth proof stage.

## The central transformation

| Stage | Governing question | Required artifact | Change achieved |
|---|---|---|---|
| Curiosity | What might be worth studying? | Lead note | A direction becomes visible |
| Reconstruction | What was actually asked? | Source map | Ambiguity is removed |
| Campaign | What exact obligation can be attacked? | Work Package | Search becomes structured |
| Evidence | What proof, computation, or obstruction exists? | Claim ledger | Support becomes inspectable |
| Handoff | What can now be checked? | Certification packet | Dependencies become explicit |
| Certification | What crossed the declared boundary? | Checked artifact | Local reliance becomes warranted |
| Integration | What is the authoritative current account? | Ledger, reviews, ADRs, public page | Meaning survives revision |

## What the programme refuses

<div class="refusal-register">
  <div><span>01</span><strong>Promising ore presented as refined metal</strong><p>Discovery may be exciting without being authoritative.</p></div>
  <div><span>02</span><strong>Elegant exposition presented as discharged proof</strong><p>Understanding helps a proof; it does not replace one.</p></div>
  <div><span>03</span><strong>Finite computation presented as an infinite theorem</strong><p>The bridge must itself be proved.</p></div>
  <div><span>04</span><strong>Governance status presented as theorem status</strong><p>Completed, published, selected, and archived describe artifacts unless a mathematical support route says otherwise.</p></div>
</div>

## Status vocabulary

<div class="status-register status-register--left" aria-label="Reader-facing claim status vocabulary">
  <span class="claim-status claim-status--conjectural">Conjectural</span>
  <span class="claim-status claim-status--computed">Computed</span>
  <span class="claim-status claim-status--provisional">Provisional</span>
  <span class="claim-status claim-status--certified">Certified</span>
  <span class="claim-status claim-status--rejected">Rejected</span>
</div>

These compact labels summarize mathematical support. They are not the same as artifact lifecycle or campaign disposition. See the [Programme Status Taxonomy](STATUS_TAXONOMY.md).

## Domain portfolio

| Domain | Mathematical state | Current programme boundary |
|---|---|---|
| [01 · Union-Closed Sets](domains/union_closed.md) | Open conjecture | Foundational demonstration domain; local proofs and bounded certificates only |
| [02 · Navier–Stokes Critical Integrability](domains/navier_stokes.md) | Open problem | Equation-specific critical-integral routes; no regularity theorem |
| [03 · Hodge Conjecture](domains/hodge.md) | Open conjecture | Source and equivalence normalization; no new algebraicity result |
| [04 · Birch–Swinnerton-Dyer](domains/birch_swinnerton_dyer.md) | Open conjecture | WP00–WP04 promoted; selected restricted target remains unproved |
| [05 · Poincaré Reconstruction](domains/poincare_reconstruction.md) | Solved classical theorem | Qualified reconstruction archive; no new proof or complete formalization |
| [06 · Yang–Mills Existence and Mass Gap](domains/yang_mills.md) | Open problem | Source-normalized axiomatic dossier; no continuum construction or physical gap theorem |
| [07 · P versus NP](domains/p_vs_np.md) | Open problem | Machine and encoding lock; no equality, separation, algorithm, or unrestricted lower bound |
| [08 · Riemann Hypothesis](domains/riemann_hypothesis.md) | Open conjecture | Function and zero normalization; no proof, disproof, or newly certified zero range |

The catalogue is not a scoreboard. Different domains may legitimately produce a source audit, a false-proof atlas, a negative result, a selected target, a bounded certificate, or an archival dossier.

## Executable fixture 001 · Exact algebraic identity

<div class="fixture-showcase" aria-label="UF-INV-001 exact algebraic fixture">
  <header class="fixture-showcase__header">
    <div>
      <span class="fixture-showcase__index">UF-INV-001 · merged · CI enforced</span>
      <h3>One claim, three support boundaries</h3>
    </div>
    <a href="https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/fixtures/algebraic/UF-INV-001">Inspect the artifact <span>→</span></a>
  </header>

  <div class="fixture-statement">
    <span>Source statement</span>
    <strong>x² = 1 and x ≠ −1 <i>implies</i> x = 1</strong>
    <small>over every field extension of Q</small>
  </div>

  <div class="fixture-route" aria-label="Claim support route">
    <div class="fixture-route__stage fixture-route__stage--audited"><span>01 · Semantic compilation</span><strong>Audited</strong><p>Replace the inequation by an inverse variable.</p></div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked"><span>02 · Exact identity</span><strong>Checked</strong><p>Replay sparse polynomial arithmetic over exact rationals.</p></div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--audited"><span>03 · Source implication</span><strong>Audited</strong><p>Depends on both semantic translation and checked identity.</p></div>
  </div>

  <div class="fixture-witness"><div class="fixture-witness__label"><span>Exact witness</span><small>expanded coefficient by coefficient</small></div><code>x − 1 = t(x² − 1) + (1 − x)(t(x + 1) − 1)</code></div>
</div>

The fixture proves that a serialized witness can be checked and adversarially mutated without promoting the surrounding semantic implication beyond its audited bridge.

## Executable fixture 002 · Radical membership

<div class="fixture-showcase fixture-showcase--radical" aria-label="RAD-NIL-002 radical membership fixture">
  <header class="fixture-showcase__header">
    <div>
      <span class="fixture-showcase__index">RAD-NIL-002 · model-class audit</span>
      <h3>The exponent and the universe both matter</h3>
    </div>
    <a href="https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/fixtures/algebraic/RAD-NIL-002">Inspect the artifact <span>→</span></a>
  </header>

  <div class="fixture-statement">
    <span>Field-level statement</span>
    <strong>x² = 0 <i>implies</i> x = 0</strong>
    <small>over every field extension of Q</small>
  </div>

  <div class="fixture-model-boundary" aria-label="Valid and refuted model classes">
    <div class="fixture-model-boundary__valid"><span>Valid model class</span><strong>Field extensions of Q</strong><p>No nonzero nilpotent elements.</p></div>
    <div class="fixture-model-boundary__refuted"><span>Refuted generalization</span><strong>All commutative Q-algebras</strong><p>The dual numbers contain a nonzero nilpotent.</p></div>
  </div>
</div>

The checker distinguishes ideal membership from radical membership and preserves the false broader statement with its countermodel.

## Fixture 003: The logarithmic GCD kernel

<div class="fixture-showcase" aria-label="LOG-GCD-001 published certified Lean result">
  <header class="fixture-showcase__header">
    <div>
      <span class="fixture-showcase__index">Fixture 003 · PUB-LOG-GCD-001 · Publication status: published</span>
      <h3>Classical mathematics · certified formal artifact</h3>
    </div>
    <a href="LOG_GCD_PUBLICATION.md">Read the public note <span>→</span></a>
  </header>

  <div class="fixture-statement">
    <span>Certified Gram identity</span>
    <strong>K(m,n) = log(gcd(m,n)) = ⟨φ(m),φ(n)⟩</strong>
    <small>for positive inputs and a finitely supported divisor feature vector</small>
  </div>

  <div class="fixture-route" aria-label="LOG-GCD support route">
    <div class="fixture-route__stage fixture-route__stage--audited"><span>01 · Prior art</span><strong>Classical</strong><p>General GCD-matrix theory already supplies the incidence-factorization criterion.</p></div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked"><span>02 · Formal artifact</span><strong>Certified</strong><p>Lean checks positive semidefiniteness and the exact finite-support Gram realization.</p></div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked"><span>03 · Public claim</span><strong>Published</strong><p>The publication gate preserves every exclusion and makes no novelty claim.</p></div>
  </div>

  <div class="fixture-rejections">
    <span>No novelty or priority claim</span>
    <ul>
      <li>not a new theorem</li>
      <li>not a novel kernel</li>
      <li>not a first proof</li>
      <li>not a first feature representation</li>
      <li>not a first Lean formalization</li>
    </ul>
  </div>
</div>

Publication changed visibility, not mathematical history. The theorem remains classical; the formal and editorial contribution is stated without a priority claim.

## Review posture

> I know which domain I am reading, what is proved, what is computed, what is conjectural, what failed, what was ruled out, which artifact is authoritative, and what must happen next.
