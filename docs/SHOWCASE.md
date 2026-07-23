# Showcase

<p class="page-deck">The programme in one view: three distinct modes of work, joined by explicit handoffs, a visible proof boundary, and a refusal to confuse momentum with completion.</p>

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

## The central transformation

| Stage | Governing question | Required artifact | Change achieved |
| --- | --- | --- | --- |
| Curiosity | What might be worth studying? | Lead note | A direction becomes visible |
| Reconstruction | What was actually asked? | Source map | Ambiguity is removed |
| Campaign | What exact obligation can be attacked? | Work Package | Search becomes structured |
| Evidence | What computation or proof attempt exists? | Claim ledger | Support becomes inspectable |
| Handoff | What can now be checked? | Certification packet | Dependencies become explicit |
| Certification | What crossed the proof boundary? | Checked artifact | Reliance becomes warranted |

## What the programme refuses

<div class="refusal-register">
  <div><span>01</span><strong>Promising ore presented as refined metal</strong><p>Discovery may be exciting without being authoritative.</p></div>
  <div><span>02</span><strong>Elegant exposition presented as discharged proof</strong><p>Understanding helps a proof; it does not replace one.</p></div>
  <div><span>03</span><strong>Finite computation presented as an infinite theorem</strong><p>The bridge must itself be proved.</p></div>
  <div><span>04</span><strong>Formal syntax detached from intended meaning</strong><p>Certification must preserve semantic correspondence.</p></div>
</div>

## Status vocabulary

<div class="status-register status-register--left" aria-label="Claim status vocabulary">
  <span class="claim-status claim-status--conjectural">Conjectural</span>
  <span class="claim-status claim-status--computed">Computed</span>
  <span class="claim-status claim-status--provisional">Provisional</span>
  <span class="claim-status claim-status--certified">Certified</span>
  <span class="claim-status claim-status--rejected">Rejected</span>
</div>

These labels are not decoration. They prevent a promising observation, a successful computation, and a certified theorem from collapsing into the same rhetorical category.

## The first cross-pillar lane

<div class="certificate-lane" aria-label="Algebraic witness to certificate lane">
  <span>Polynomial obligation</span><b>→</b><span>Witness search</span><b>→</b><span>Explicit certificate</span><b>→</b><span>Exact replay</span><b>→</b><span>Local lemma</span>
</div>

This lane does not promise that Groebner bases solve open problems. It permits symbolic algebra to contribute inside a bounded obligation while respecting worst-case complexity and preserving an exact replay route.

## Executable progress

<div class="fixture-showcase" aria-label="UF-INV-001 exact algebraic fixture">
  <header class="fixture-showcase__header">
    <div>
      <span class="fixture-showcase__index">Fixture 001 · merged · CI enforced</span>
      <h3>One claim, three support boundaries</h3>
    </div>
    <a href="https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/fixtures/algebraic/UF-INV-001">Inspect the artifact <span>→</span></a>
  </header>

  <div class="fixture-statement">
    <span>Source statement</span>
    <strong>x² = 1 and x ≠ −1 <i>implies</i> x = 1</strong>
    <small>over every field extension of ℚ</small>
  </div>

  <div class="fixture-route" aria-label="Claim support route">
    <div class="fixture-route__stage fixture-route__stage--audited">
      <span>01 · Semantic compilation</span>
      <strong>Audited</strong>
      <p>Replace the inequation by an inverse variable: <code>t(x + 1) = 1</code>.</p>
    </div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked">
      <span>02 · Exact identity</span>
      <strong>Checked</strong>
      <p>Replay sparse polynomial arithmetic over exact rational coefficients.</p>
    </div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--audited">
      <span>03 · Source implication</span>
      <strong>Audited</strong>
      <p>Depends on both the semantic argument and the checked identity.</p>
    </div>
  </div>

  <div class="fixture-witness">
    <div class="fixture-witness__label">
      <span>Exact witness</span>
      <small>independently expanded coefficient by coefficient</small>
    </div>
    <code>x − 1 = t(x² − 1) + (1 − x)(t(x + 1) − 1)</code>
  </div>

  <div class="fixture-verdicts" aria-label="Fixture verification results">
    <div><strong>1</strong><span>identity checked</span></div>
    <div><strong>6</strong><span>mutations rejected</span></div>
    <div><strong>0</strong><span>unsupported promotions</span></div>
  </div>

  <div class="fixture-rejections">
    <span>Rejected by CI</span>
    <ul>
      <li>altered coefficient</li>
      <li>changed variable order</li>
      <li>duplicate monomial</li>
      <li>missing hypothesis</li>
      <li>false artifact hash</li>
      <li>premature certification</li>
    </ul>
  </div>
</div>

The important result is not the elementary theorem. It is that the programme checks a serialized mathematical witness, attacks it with malformed alternatives, and still refuses to call the surrounding theorem certified before its semantic bridge reaches a proof assistant.

<div class="fixture-showcase fixture-showcase--radical" aria-label="RAD-NIL-002 radical membership fixture">
  <header class="fixture-showcase__header">
    <div>
      <span class="fixture-showcase__index">Fixture 002 · radical membership · model-class audit</span>
      <h3>The exponent and the universe both matter</h3>
    </div>
    <a href="https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/fixtures/algebraic/RAD-NIL-002">Inspect the artifact <span>→</span></a>
  </header>

  <div class="fixture-statement">
    <span>Field-level statement</span>
    <strong>x² = 0 <i>implies</i> x = 0</strong>
    <small>over every field extension of ℚ</small>
  </div>

  <div class="fixture-route" aria-label="Radical membership support route">
    <div class="fixture-route__stage fixture-route__stage--audited">
      <span>01 · Target</span>
      <strong>Not ideal membership</strong>
      <p>The polynomial <code>x</code> does not belong to the ideal <code>(x²)</code>.</p>
    </div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked">
      <span>02 · Radical witness</span>
      <strong>Checked</strong>
      <p>The certificate carries exponent <code>N = 2</code> and verifies <code>xᴺ ∈ (x²)</code>.</p>
    </div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--audited">
      <span>03 · Field semantics</span>
      <strong>Audited</strong>
      <p>Fields have no nonzero nilpotents, so the checked radical fact supports the implication.</p>
    </div>
  </div>

  <div class="fixture-witness">
    <div class="fixture-witness__label">
      <span>Exponent-bearing witness</span>
      <small>the power is part of the proof object</small>
    </div>
    <code>xᴺ = 1 · x², where N = 2</code>
  </div>

  <div class="fixture-model-boundary" aria-label="Valid and refuted model classes">
    <div class="fixture-model-boundary__valid">
      <span>Valid model class</span>
      <strong>Field extensions of ℚ</strong>
      <p>No nonzero nilpotent elements.</p>
    </div>
    <div class="fixture-model-boundary__refuted">
      <span>Refuted generalization</span>
      <strong>All commutative ℚ-algebras</strong>
      <p><code>ℚ[ε]/(ε²)</code> has <code>ε² = 0</code> with <code>ε ≠ 0</code>.</p>
    </div>
  </div>

  <div class="fixture-verdicts" aria-label="Radical fixture verification results">
    <div><strong>1</strong><span>radical witness checked</span></div>
    <div><strong>9</strong><span>mutations rejected</span></div>
    <div><strong>1</strong><span>false generalization retained</span></div>
  </div>

  <div class="fixture-rejections">
    <span>Rejected by CI</span>
    <ul>
      <li>zero exponent</li>
      <li>exponent N = 1</li>
      <li>wrong certificate kind</li>
      <li>broadened model class</li>
      <li>altered target</li>
      <li>false artifact hash</li>
      <li>premature certification</li>
      <li>missing refutation</li>
      <li>removed countermodel</li>
    </ul>
  </div>
</div>

<div class="fixture-series-note">
  <strong>What advanced</strong>
  <p>The checker now distinguishes ordinary ideal membership from radical membership. The claim ledger also preserves a false generalization and its countermodel instead of allowing a valid field theorem to drift into an invalid ring theorem.</p>
</div>

## Fixture 003: The logarithmic GCD kernel

<div class="fixture-showcase" id="fixture-003-the-logarithmic-gcd-kernel" aria-label="LOG-GCD-001 published certified Lean result">
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
    <small>for positive inputs, with φ(n) a finitely supported divisor feature vector</small>
  </div>

  <div class="fixture-route" aria-label="LOG-GCD publication support route">
    <div class="fixture-route__stage fixture-route__stage--audited">
      <span>01 · Prior art</span>
      <strong>Classical</strong>
      <p>General GCD-matrix theory already supplies the incidence-factorization criterion.</p>
    </div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked">
      <span>02 · Formal artifact</span>
      <strong>Certified</strong>
      <p>Lean checks positive semidefiniteness and the exact <code>Finsupp</code> Gram realization.</p>
    </div>
    <b aria-hidden="true">→</b>
    <div class="fixture-route__stage fixture-route__stage--checked">
      <span>03 · Public claim</span>
      <strong>Published</strong>
      <p>Workflow <code>29997559180</code> checked the published statement, certification evidence, and permanent claim boundary.</p>
    </div>
  </div>

  <div class="fixture-witness">
    <div class="fixture-witness__label">
      <span>Divisor feature</span>
      <small>finite support is part of the Lean type</small>
    </div>
    <code>φ(n)₍d₎ = sqrt(Λ(d)) when d ∣ n, and 0 otherwise</code>
  </div>

  <div class="fixture-verdicts" aria-label="LOG-GCD publication results">
    <div><strong>2</strong><span>certified theorem claims</span></div>
    <div><strong>1</strong><span>publication gate passed</span></div>
    <div><strong>0</strong><span>novelty claims</span></div>
  </div>

  <div class="fixture-rejections">
    <span>No novelty or priority claim</span>
    <ul>
      <li>not a new theorem</li>
      <li>not a novel kernel</li>
      <li>not a first proof</li>
      <li>not a first feature representation</li>
      <li>not a first Lean formalization</li>
      <li>not strictly positive definite on the full domain</li>
    </ul>
  </div>
</div>

<div class="fixture-series-note">
  <strong>What advanced</strong>
  <p>A certified artifact has crossed the publication gate without changing its mathematical status. The public note makes the exact formal contribution inspectable while retaining the classical prior-art determination and every permanent exclusion.</p>
</div>

## Current demonstration domain

<div class="domain-brief domain-brief--compact">
  <div class="domain-brief__identity"><span>Domain 01</span><strong>Union-Closed Sets</strong><p>Method before grand claim.</p></div>
  <div class="domain-brief__body"><p>The first domain establishes definitions, finite sanity checks, status spines, Lean-facing statements, and certification handoffs. Its purpose is to demonstrate disciplined mathematical accumulation without pretending that infrastructure is a solution to Frankl's conjecture.</p></div>
</div>

## Review posture

> I know what is proved, what is computed, what is conjectural, what failed, what was ruled out, and what must happen next.
