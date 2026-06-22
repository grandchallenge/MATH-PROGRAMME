# Chaidez Pedagogical Protocol

The Chaidez programme treated exposition as part of mathematical control. A
plain-language companion was not added after the mathematics; it was used to
test whether the object, obstruction, claim, and remaining debt had actually
been understood.

This protocol adopts that discipline for MATHSOLVE. It is a campaign-level
instance of the [Grand Challenge Pedagogy Standard](GRAND_CHALLENGE_PEDAGOGY_STANDARD.md).
New Work Packages should also follow the [Foundation-Aware MATH-PROGRAMME Doctrine](FOUNDATION_AWARE_MATH_PROGRAMME.md).

## The campaign is one theorem spine

A domain is not a pile of Work Packages. It is one evolving theorem spine with
a dependency graph.

Every Work Package must name:

- the global spine node it advances;
- the dependencies it consumes;
- the local claim or obstruction it establishes;
- the proof debt it creates, discharges, or leaves unchanged;
- the foundational profile or unresolved foundation gap;
- the first executable step that follows.

Opening another package is not progress unless the current spine and debt
register have been audited.

## Begin with result status

Every Work Package begins with a result-status box.

| Field | Required content |
|---|---|
| Result status | Proved, checked, conditional, negative, open, rejected, or superseded |
| Conditional on | Every hypothesis or unresolved bridge needed by the result |
| Strongest supported claim | The strongest sentence the artifact supports |
| Not claimed | Nearby statements that the artifact does not establish |
| Support-route class | One class from the support-route taxonomy, or `NONE` |
| Foundational profile | Present, inherited, or explicitly deferred |
| Certification state | Unreviewed, audited, replayed, formally checked, or blocked |
| First executable step | One bounded action with a visible completion test |

Conditional language belongs here, not in a late qualification.

## The exposition sequence

Use this sequence for the body of a serious Work Package.

1. **Status box.** State the result status, support route, foundation profile,
   and first executable step.
2. **Plain object.** Name the object and target without leading with machinery.
3. **Exact obstruction.** Show the smallest calculation, counterexample, or
   failed mechanism that exposes why the target resists the naive route.
4. **Working model.** Give a finite, visual, or local model the reader can hold.
5. **Restricted claim.** State the claim actually under investigation.
6. **Spine location.** Place it in the theorem spine and dependency DAG.
7. **Support route.** Give the proof, computation, replay, formalization, or
   negative result and classify it.
8. **Debt audit and claim boundary.** Record every missing lemma, semantic
   bridge, replay, source check, or foundation gap.
9. **First executable step.** End with one action that can be started now.

This sequence may be compressed, but no stage may be silently omitted.

## The object-obstruction pair

The reader should meet the object and its obstruction together.

Do not say only that a problem is difficult. Identify the mechanism that fails:
a non-monotone quantity, an exceptional parameter branch, a semantic mismatch,
a missing compactness step, a coefficient explosion, a false local-to-global
inference, or an implicit foundation assumption.

A small exact failure is often more pedagogically valuable than a large
successful computation because it reveals the boundary of the method.

## Theorem spine and dependency DAG

The global spine contains the claims that would make the campaign cohere. Each
node must have:

- a stable identifier;
- a role: definition, reduction, bridge, theorem, obstruction, or certificate;
- a claim status;
- incoming dependencies;
- a support-route class;
- a discharge criterion;
- linked proof-debt items.

A Work Package carries a local slice of this graph. It must not present its
local theorem list as if it were independent of the campaign.

## Proof-debt register

Proof debt is mathematical state, not editorial cleanup. Classify each item as:

```text
MISSING_LEMMA
UNPROVED_BRIDGE
EXTERNAL_SOURCE
COMPUTATIONAL_REPLAY
SEMANTIC_CORRESPONDENCE
FOUNDATIONAL_PROFILE_GAP
ANALYTIC_ESTIMATE
FORMALIZATION_BLOCKER
```

Each item records the blocked spine node, present evidence, discharge
condition, and intended route or owner. A package may add debt, but it may not
hide it.

## Support-route taxonomy

Every substantial support route is classified as exactly one of:

1. **Exploratory evidence**: finds patterns or candidate statements.
2. **Regression audit**: checks that definitions, code, or prior examples
   continue to behave as expected.
3. **Exact finite verification**: proves a finite, explicitly bounded claim.
4. **Certificate replay**: checks a local claim through a replayable certificate
   or verifier artifact.
5. **Formal proof**: checks a statement in a trusted formal environment.
6. **Continuum proof**: participates in a proof covering the full stated
   domain, with all analytic, semantic, and foundational obligations discharged.
7. **Negative result**: rules out a route or isolates an obstruction.

The class must agree with the claim ledger. Exact finite verification is not
continuum proof. Certificate replay is not automatic theoremhood; it supports
only the local claim named by the certificate.

## The trust quartet

Every Work Package displays these four answers together:

1. What is proved?
2. What is checked?
3. What remains open?
4. What requires external verification?

The quartet is the compact public account of the package. Its entries must
agree with the claim ledger, proof-debt register, foundation profile, and
MATHCERT handoff.

## Negative results

A negative-result package is complete only if it states:

- the attempted route and why it was plausible;
- the smallest exact obstruction available;
- what the obstruction rules out;
- what it does not rule out;
- the next viable restricted problem.

The deliverable is a better model of the problem, not a narrative of effort.

## The first executable step

End with a bounded action, not a research aspiration.

Good:

> Derive the coefficient identity for spine node `BRIDGE-03` in the
> two-parameter case and replay it over exact rationals.

Bad:

> Continue investigating the conjecture.

The step must name its input, output, and completion test.

## Escalation gate

A new Work Package may be opened or promoted only when:

- the current theorem-spine slice has been audited;
- all dependencies are named;
- the proof-debt register is current;
- the trust quartet is complete;
- the foundational profile is present or explicitly deferred;
- the first executable step is explicit;
- the proposed package names the spine node it advances.

This gate prevents package proliferation from being mistaken for mathematical
progress.

## Pillar use

**MATHFORGE** should produce a candidate spine node, likely dependencies,
principal obstruction, foundational texture, and first falsification or exact-screen task.

**MATHSOLVE** owns the theorem spine, dependency DAG, debt register, result
status, support-route classification, negative-result analysis, and next step.

**MATHCERT** receives only named claims and debt items selected for
certification. Certification state remains distinct from mathematical status.
