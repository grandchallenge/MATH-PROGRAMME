# MCORE-DOMAIN-SHADOW-001

## Status

`MCORE-DOMAIN-SHADOW-001` is the first read-only domain integration defined by ADR-0021. It materializes the protected Condensed Mathematics / CMDG state as a provenance-preserving MATH-CORE domain shadow.

The shadow is an observation layer. It is not a replacement claim ledger, not a certification surface, and not retroactive MATH-CORE event history.

## Exact source checkpoint

The first materialization is bound to:

`grandchallenge/MATH-PROGRAMME@a501eef7517ec9a3170ee8190a1d856c050da92c`

Source records are content-checked using their Git blob SHA-1 values. The shadow deliberately derives current protected status from later protected receipts while retaining the historical status text found in the original records. This avoids rewriting an older candidate artifact as though it had originally been emitted in its eventual protected state.

## Domain projection

The materialized path is:

```text
CM1  ->  CM2  ->  CM3  ->  Solid C05  ->  CM4 frontier
                                             |
                                             +-- P1 available
                                             +-- P2 protected-closed
                                             +-- P3 blocking
                                             +-- P5 blocking -> P4 blocking
                                             +-- P3 + P4 -> P6 partial-blocking
```

CM1, CM2, and CM3 are represented as protected dependency states with separate formal-replay evidence nodes. Solid C05 is represented as a protected definition boundary; the shadow preserves the source warning that its pinned unrestricted general-ring signature is not unrestricted semantic authority and does not imply a nontrivial solid-object theorem.

CM4 remains an open, uncertified frontier target. P2 is explicitly protected-closed and is not allowed to reappear as a blocker. The later P3 audit remains `OPEN_WITH_CHARACTERIZED_BLOCKER`: generic Ext and sheaf-cohomology infrastructure exists, but the required profinite/discrete acyclicity specialization or certified underived reduction has not been assembled at the pinned boundary.

## Blocker taxonomy

The shadow uses the architecture-controlled blocker classes:

- `MATHEMATICAL`: a required mathematical result remains unresolved;
- `FORMALIZATION`: a required machine-composable theorem, specialization, or proof bridge remains absent;
- `GOVERNANCE_EVIDENCE`: the mathematics may exist but required governed evidence or authority is missing;
- `EXECUTION_INFRASTRUCTURE`: runtime, CI, environment, or tool execution prevents progress.

At this exact snapshot, the CM4 P3/P4/P5/P6 frontier is represented as mathematical/formalization blockage. No execution-infrastructure blocker is asserted merely because a theorem has not yet been formalized.

## Read-only invariants

The materialization is fail-closed on the following invariants:

```text
retroactive_live_event_history = false
autonomous_allocation          = false
autonomous_pruning             = false
canonical_promotion            = false
certificate_issuance           = false
source_mutation                = false
```

Every shadow node has `live_event: false` and `canonical_claim_effect: NONE`. Every shadow edge has `authority_effect: NONE_DIRECT`.

These constraints are intentional. A protected dependency record, a formal replay, a certificate, and a canonical claim are different authority classes; the shadow does not collapse them.

## Validation

`ci/validate_math_core_domain_shadow.py` checks:

1. the JSON schema and exact source checkpoint;
2. exact Git blob identity for the protected source records;
3. forward protected-close lineage for CM1, CM2, CM3, and Solid C05;
4. the Solid C05 semantic boundary;
5. protected closure of CM4-P2;
6. the exact CM4 prerequisite matrix;
7. the later P3 characterized-blocker state;
8. consistency of shadow nodes, edges, blocker classes, and current frontier;
9. the no-promotion/no-live-execution claim boundary.

`ci/test_math_core_domain_shadow.py` supplies adversarial mutations for retroactive history, autonomous pruning, claim laundering, P2 regression, false P3 closure, source-blob drift, spurious runtime blocking, and C06 discharge.

## Stage boundary

This work package does not discharge `MCORE-ARCH-C03` through `MCORE-ARCH-C07`. In particular, C06 remains active: a read-only shadow may not be promoted beyond observation or used to drive live allocation or pruning without a separately governed stage that satisfies the relevant capability gates.

The natural next use of the shadow is therefore diagnostic: make the programme state explicit and queryable while leaving all mathematical, certification, canonical-recording, and execution authorities where they already reside.

## Claim boundary

This materialization proves no new mathematics, certifies no theorem or dependency edge, promotes no claim, upgrades no Condensed frontier, establishes no graph completeness/minimality/uniqueness result, and authorizes no publication, external claim, autonomous allocation, or autonomous pruning.
