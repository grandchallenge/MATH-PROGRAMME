# OPENMATH-2026 sprint profile

**Campaign:** `OPENMATH-2026`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#1072`  
**Applies:** 2026-09-27 through 2026-10-02, plus bounded closeout

## Governing idea

Use the smallest process that preserves the evidence boundary.

The sprint profile is a scheduling and artifact-minimization profile. It does not weaken source, semantic, certification, independence, security, or promotion requirements.

## Per-hill minimum packet

A live hill lane should maintain:

```text
HILL_LOCK.json
CLAIM_LEDGER.json
OBLIGATION_GRAPH.md
ROUTE_LEDGER.md
FAILURE_LEDGER.md
FORMAL_ENVIRONMENT.md
PROVENANCE.md
NEXT_ACTION.md
```

Additional artifacts are created only when mathematically useful.

## Work cadence

For each locked hill:

1. establish semantic/source lock;
2. identify the smallest useful formal target;
3. fan out distinct routes, not duplicate full-problem attempts;
4. checkpoint any proof-quality lemma, counterexample, reduction, or formal API before starting another expensive branch;
5. terminate routes explicitly when falsified or dominated;
6. minimize surviving evidence into a replayable handoff;
7. route claim-bearing output to MATHCERT;
8. prepare competition submission only from the exact adjudicated/certified artifact appropriate to its claim.

## Priority classes

### P0 — source and evaluator integrity

Statement identity, current status, evaluator/checker version, formal environment, and competition-rule semantics.

### P1 — enabling mathematics

Definitions, formal APIs, missing-library lemmas, reductions, exact examples, counterexamples, and tractable restricted claims.

### P2 — main-target attack

Only after P0 and sufficient P1 support. Main-target work may run concurrently across distinct routes.

### P3 — exposition and post-event synthesis

Deferred when it competes with proof work, except where needed for semantic adjudication or submission requirements.

## Stop rules

Stop or narrow a route when:

- the statement lock changes;
- a counterexample kills the claim;
- the route depends on an unproved imported lemma that dominates the target;
- formalization exposes a materially different theorem;
- exact computation falsifies the working conjecture;
- resource use exceeds the declared budget without new structural information;
- another route strictly subsumes the same obligation with stronger replay evidence.

Record the failure before disposal.

## Submission firewall

Before external submission, verify separately:

1. machine acceptance in the pinned environment;
2. exact statement correspondence;
3. dependency and axiom disclosure;
4. provenance and tool disclosure;
5. novelty/classification status to the extent required by the competition;
6. authorship attribution;
7. exact artifact identity.

No one item substitutes for another.

## Post-event residue

The durable output is the research graph, not only the leaderboard result.

Closeout should preserve:

- accepted and rejected claims;
- failed routes and why they failed;
- counterexamples;
- reusable formal lemmas and APIs;
- dependency gaps;
- source/status corrections;
- exact competition artifacts and checker receipts;
- MATHCERT dispositions;
- next research targets.
