# Programme Atlas

<p class="page-deck">The canonical public map of how a mathematical question changes state as it moves through discovery, solving, certification, and programme integration.</p>

## What the Atlas represents

The Atlas describes programme transitions. It does not certify any theorem.

A mathematical object can move through several support states without reaching certification. The programme preserves each transition so that a later reader can recover what changed and why.

![State transition from a question or source signal through MATHFORGE, MATHSOLVE, and MATHCERT. Fail-closed exits record an obstruction, proof debt, or non-promotion.](assets/claim-state-transition.svg)

The diagram is schematic. The arrows represent allowed research-state transitions, not logical implication between mathematical statements.

## Three mathematical execution pillars

| Pillar | Governing question | Typical artifacts | Boundary preserved |
| --- | --- | --- | --- |
| **MATHFORGE** | What object, source, obstruction, or candidate route is actually available? | source records, problem cards, reconnaissance, finite screens, route suggestions | discovery evidence does not become a mathematical result by presentation alone |
| **MATHSOLVE** | Which exact obligations must close before the target can advance? | theorem spines, work packages, proof-debt registers, local lemmas, handoffs | active work does not become a completed result |
| **MATHCERT** | Which exact claim survives the declared checks? | formal statements, exact replays, certificate checks, adjudications, claim dispositions | evidence and exposition do not become certified truth without the required gate |

`MATH-PROGRAMME` is the integration layer. It preserves programme state, routing, terminology, decisions, publication surfaces, and archives. It is not a fourth mathematical support route.

## State changes

| Research state | Main question | Minimum reader-visible result |
| --- | --- | --- |
| Question or source signal | What is worth reconstructing? | object and source identity |
| Reconstructed object | What was actually stated or observed? | normalized statement, provenance, and imported assumptions |
| Solving campaign | What finite obligation can be attacked? | theorem-spine location, dependencies, and completion test |
| Local evidence | What proof, computation, certificate, or obstruction exists? | classified support route and limitations |
| Certification handoff | What exact claim is ready to be checked? | immutable statement, dependencies, evidence, and replay contract |
| Checked claim | What survived the declared gate? | bounded disposition and retained exclusions |
| Integrated record | What is the authoritative current account? | protected record with review, provenance, and continuation state |

Not every object reaches the last row. A failed route can be a complete programme result when it records the exact obstruction and narrows the remaining search space.

## Fail-closed exits

### MATHFORGE exit · recorded obstruction

A source may be incomplete, inconsistent, unavailable, or insufficient for the intended claim. MATHFORGE records that obstruction instead of inventing the missing bridge.

### MATHSOLVE exit · proof debt

A campaign may isolate a theorem-level dependency that is not yet proved. MATHSOLVE records the dependency, its role, and the conditions that would discharge it.

### MATHCERT exit · non-promotion

A certificate, formalization, or replay may fail, or it may support only a narrower claim than the proposed output. MATHCERT preserves the narrower boundary and refuses the unsupported promotion.

## Support-route classes

The public explanation should identify which class supports a consequential statement.

| Support class | What it can establish |
| --- | --- |
| Exploratory evidence | patterns and candidate hypotheses |
| Regression audit | continued agreement among definitions, examples, and code paths |
| Exact finite verification | the explicitly bounded finite claim |
| Certificate replay | the local claim represented by the replayable certificate |
| Formal proof | the formal statement accepted by the declared trusted environment |
| Continuum proof | the full mathematical statement over the stated domain |
| Negative result | a bounded obstruction that rules out a declared route or claim |

The classes are not interchangeable. Exact finite verification is not continuum proof. A visualization is not mathematical evidence by itself. A formal proof of the wrong statement does not establish the intended human claim.

## Semantic bridge

Every formal or computational route must preserve the bridge between the human claim and the checked object.

A reader should be able to recover:

1. the human statement;
2. the formal or computational statement;
3. assumptions added or removed in translation;
4. model-class or foundational restrictions;
5. the evidence that supports the bridge;
6. what would falsify or downgrade the bridge.

If the bridge remains unaudited, the formal or computational artifact can still be useful. The broader human claim remains below certification.

## How to route a new item

Use the smallest pillar that matches the present state.

- Send an unclear source, object, or candidate route to **MATHFORGE**.
- Send a normalized target with unresolved mathematics to **MATHSOLVE**.
- Send an exact claim with a declared replay or proof surface to **MATHCERT**.
- Use **MATH-PROGRAMME** to preserve cross-pillar routing, public state, governance, and archival continuity.

Do not route by prestige. Route by the support state of the object.

## Reader continuation

For live work, use [Current Work](CURRENT_WORK.md). For bounded checked outputs, use [Results and Exemplars](SHOWCASE.md). For standing domains, use the [Mathematical Estate](domains/index.md). For review posture, use the [Grand Challenge Reader Guide](GRAND_CHALLENGE_READER_GUIDE.md).
