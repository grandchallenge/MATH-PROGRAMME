# GCL Controlled Epistemic Interface

## Independent intelligence intake without institutional assimilation

**Control surface:** `GCL-CEI-001`  
**Documentary lifecycle:** `active`  
**Documentary role:** governed human-readable operational description of the protected independent-intelligence intake path  
**Initial protected admission:** MATH-PROGRAMME PR #1041, merge `598a13d8a390fcab722b84b4a494921fc50d0e56`  
**Controller:** `MP-NSCI-INTAKE-PR-CONTROLLER-001`, machine status `ACTIVE`  
**Claim boundary:** this interface transports and preserves bounded mathematical contributions. It does not certify mathematics, promote claims, merge protected state, or substitute for MATHCERT.

## 1. The point

GCL sometimes needs a contribution from an intelligent reasoner that has **not** been assimilated into the institution's accumulated context, vocabulary, preferred proof routes, or local consensus.

The purpose is not anonymity and not mystique. It is epistemic separation.

The controlled interface therefore does two things at once:

1. gives the independent reasoner enough information to solve one bounded problem well; and
2. prevents the reasoner from needing to become an internal GCL agent in order to contribute.

The governing sentence is:

> **GCL defines the whole problem world. Independent intelligence reasons inside that bounded world. Only the returned contribution crosses the boundary. GCL then preserves, falsifies, adjudicates, and, if warranted, routes the result through existing protected knowledge controls.**

This is a contribution interface, not an authority interface.

## 2. Core topology

```text
+------------------------------+
|         GCL DISPATCH         |
| defines the whole problem    |
| world and return contract    |
+--------------+---------------+
               |
               v
+------------------------------+
|   INDEPENDENT INTELLIGENCE   |
| reasons without repository   |
| or institutional assimilation|
+--------------+---------------+
               |
               v
+------------------------------+
|           RESULT/1           |
| one bounded mathematical     |
| contribution                 |
+--------------+---------------+
               |
               v
+------------------------------+
|        GITHUB INTAKE         |
| authenticate · validate      |
| hash · preserve              |
+--------------+---------------+
               |
               v
+------------------------------+
|       MATHSOLVE EVIDENCE     |
| immutable raw result         |
| + machine receipt            |
+--------------+---------------+
               |
               v
+------------------------------+
|       GCL ADJUDICATION       |
| compare · falsify · narrow   |
| synthesize · admit/reject    |
+--------------+---------------+
               |
               v
+------------------------------+
|  MATHCERT / PROTECTED STATE  |
| only through the pre-existing|
| governed route               |
+------------------------------+
```

The implementation contains one additional control-plane hop between intake evidence and the ordinary evidence pull request:

```text
validated intake branch
        |
        v
bounded Release Trust controller
        |
        v
ordinary MATHSOLVE evidence PR
```

That controller can validate and open the PR. It cannot adjudicate, approve, merge, certify, promote, publish, or mutate campaign state.

## 3. What "independent" means here

Independence is a **work-context property**.

For a zero-context dispatch, the contributing reasoner receives the dispatch/bootstrap and ordinary mathematical background knowledge, but does not need repository history, prior agent discussion, institutional preferences, hidden campaign state, or GCL's internal theory of what the answer "should" be.

This produces a useful kind of separation:

- the contributor is not trained during the task into GCL's current local consensus;
- the problem statement is explicit enough that missing chat history is not a hidden dependency;
- the result can disagree with internal expectations without protocol failure;
- the returned object can be judged on its mathematical content rather than on institutional fluency.

It does **not** establish statistical independence, cryptographic independence, lack of common pretraining, or philosophical neutrality. Those are different claims.

The useful invariant is narrower:

> **A valid contribution must be understandable and executable as intellectual work from the dispatch itself.**

## 4. Dispatch contract

A dispatch is responsible for defining the complete bounded work-set.

It should contain, as applicable:

- the mathematical target;
- definitions and notation;
- exact assumptions;
- imported lemmas or facts the contributor may use;
- excluded assumptions;
- the permitted contribution class;
- falsification or rejection conditions;
- resource or time bounds;
- authority and claim boundaries;
- the exact return grammar;
- the exact place where the result must be returned.

The dispatch should be written so that "read the repository first" is unnecessary.

For the protected NS-CI pilot, the bootstrap explicitly tells the contributor that the document is the entire work-set and binds the contributor to a single bounded response object.

## 5. RESULT/1: the narrow crossing

The contributor returns exactly one object under the `GCL-CONTRIBUTION-RESULT/1` grammar.

The narrow return surface is deliberate.

A valid result is not accompanied by an informal cloud of attachments, private notes, side files, hidden calculations, or unbounded follow-up artifacts that the receiving institution must interpret.

The interface therefore prefers:

```text
one dispatch
    ->
one bounded reasoning task
    ->
one RESULT/1
    ->
one immutable evidence object
```

over:

```text
open-ended conversation
    ->
many partially authoritative artifacts
    ->
ambiguous provenance
```

The one-result rule improves provenance, hashing, replay, first-result locking, and adversarial review.

## 6. GitHub intake is a preservation boundary

The intake layer does not decide whether the mathematics is correct.

Its function is mechanical and evidentiary:

1. authenticate the GitHub actor and source comment;
2. bind the result to the exact registered dispatch;
3. validate the RESULT/1 grammar and field order;
4. reject unsupported links, attachments, or additional contribution objects;
5. enforce the first-valid-result lock;
6. preserve the raw returned bytes;
7. compute and retain the raw result digest;
8. emit a machine receipt;
9. mark the object `received_unadjudicated`;
10. retain `canonical_claim_effect=false`.

The intake must not execute contributor-supplied material.

A syntactically valid result is therefore **evidence received**, not **mathematics accepted**.

## 7. Evidence shape

The durable MATHSOLVE intake result has two primary objects:

```text
raw result snapshot
machine receipt
```

The receipt binds the contribution to the evidence chain, including the dispatch identity, source issue/comment identity, contributor actor, bootstrap or handoff identities, raw-result digest, schema state, and non-adjudicated claim state.

This creates a simple reconstruction property:

> A later reviewer should be able to identify exactly what the outside reasoner returned, who returned it through GitHub, what dispatch it answered, and whether the preserved bytes are unchanged.

The receipt is provenance. It is not a proof certificate.

## 8. Bounded Release Trust controller

The active controller is:

`governance/ns_ci_intake_pr_controller.json`

with control ID:

`MP-NSCI-INTAKE-PR-CONTROLLER-001`.

Protected readback after PR #1040 reports:

```text
status: ACTIVE
target repository: MATHSOLVE
contents: read
pull_requests: write
```

Its permitted role is intentionally small:

- read protected MATHSOLVE dispatch records;
- read the already-created intake branch;
- compare its raw result and receipt against protected requirements;
- open an ordinary pull request from that existing validated branch.

It may not:

- write repository contents;
- create or alter intake evidence branches;
- merge or approve pull requests;
- modify protected main;
- modify campaign state;
- perform mathematical adjudication;
- certify or promote claims;
- acquire Actions-write, workflow-write, checks-write, or administration authority.

The controller therefore closes an automation gap without collapsing intake, adjudication, and acceptance into one actor.

## 9. Wake and persistence

The controller is a repository-bound GitHub Actions workflow.

Protected workflow behavior now includes all three wake paths:

1. scheduled reconciliation every ten minutes;
2. manual replay;
3. a bounded `workflow_run` wake after successful completion of the existing **Administrative maintenance dispatcher**.

The `workflow_run` path is success-gated.

This was admitted by MATH-PROGRAMME PR #1039 and protected at merge commit:

`536e377529dd6a313e79c2f91c1dc2567ad924a5`.

The wake path changes latency and persistence only. It does not change credential scope or claim authority.

## 10. Adjudication is intentionally separate

GCL adjudication occurs only after raw preservation.

This ordering matters.

The preserved external result is not rewritten into the form GCL wishes the contributor had supplied. Instead, adjudication may:

- verify a derivation;
- identify an actual useful lemma inside an overclaim;
- construct counterexamples;
- compare the result with internal evidence;
- narrow a statement;
- reject unsupported implications;
- preserve negative information;
- admit only the fragment that survives scrutiny.

This allows GCL to use independent intelligence without outsourcing institutional judgment.

The correct semantic sequence is:

```text
receive
!=
believe
!=
admit
!=
certify
```

Each transition has a different owner.

## 11. Protected pilot evidence

The interface has been exercised on real mathematical content.

### Cooperative contribution

The protected NS-CI contribution from issue #426 / comment `5768723180` was adjudicated in MATHSOLVE PR #436.

Protected merge:

`b9e41f38a438fd3e039cf55fb59d7cd1ae0d1bc8`

The adjudication admitted only a reduced theorem and explicitly rejected stronger unsupported packet-realizability and necessity/sufficiency claims.

This is the intended behavior of the interface: useful mathematics may survive even when the contributor's strongest formulation does not.

### Release Trust qualification

The bounded Release Trust controller independently revalidated the adversarial fixture dispatch `NSCI-C2-B-ADV-999` and opened MATHSOLVE PR #445 as `gcl-release-trust[bot]`.

That PR preserved exactly the raw result and machine receipt and merged at:

`78c31d50671ad98305062c7104ed1e3c1812fc0c`.

Its body explicitly records that it does not adjudicate mathematics, infer independence, certify a claim, or alter campaign state.

Together these two cases exercise both sides of the interface:

```text
outside mathematical contribution
        +
trusted mechanical preservation
        +
separate institutional adjudication
```

## 12. Housekeeping closure

Two post-qualification residuals were identified and are now closed.

### Residual A — deterministic recurring wake

PR #1039 added the successful Administrative maintenance dispatcher completion as a bounded recurring wake source while preserving the ten-minute schedule and manual replay.

Protected merge:

`536e377529dd6a313e79c2f91c1dc2567ad924a5`

Protected readback confirms the `workflow_run` trigger and success gate are present.

### Residual B — stale controller lifecycle metadata

The machine controller contract still described itself as `CANDIDATE` after successful live qualification.

PR #1040 changed only:

```text
CANDIDATE -> ACTIVE
```

No token scope, permitted action, prohibited action, validation rule, first-result lock, or claim boundary changed.

Protected merge establishing that closure:

`01b334c14dec59b49cca3cc014acafd0870d7011`

Protected readback at that closure confirmed:

`"status": "ACTIVE"`.

That SHA is retained as historical closure evidence, not as a claim about the repository's current head. Current controller state is read from the protected machine contract `governance/ns_ci_intake_pr_controller.json`.

Disposition:

`HOUSEKEEPING_RESIDUALS_CLOSED__PROTECTED_READBACK_CONFIRMED`.

## 13. Failure semantics

The interface fails closed by layer.

### Dispatch failure

If the problem cannot be specified without hidden institutional context, it is not ready for zero-context dispatch.

### Contributor return failure

Malformed, multi-object, out-of-contract, attachment-dependent, or otherwise invalid return material is not silently normalized into a valid RESULT/1.

### Intake failure

If actor identity, dispatch binding, grammar, digest, receipt, or first-result-lock conditions fail, no trusted evidence PR should be created.

### Preservation failure

An unprotected branch or issue comment is not canonical mathematical evidence merely because it exists.

### Adjudication failure

If the mathematics cannot be justified, the contribution remains evidence of an attempted route, not an admitted theorem.

### Certification boundary

MATHSOLVE evidence and GCL adjudication do not create MATHCERT certification by implication. Certification, when applicable, must traverse the existing MATHCERT route.

## 14. Operational recipe

For a new controlled independent contribution:

1. identify one bounded contribution worth externalizing;
2. write a complete zero-context dispatch/bootstrap;
3. bind exact assumptions, exclusions, output grammar, and authority boundary;
4. publish the dispatch through the governed route;
5. provide the bootstrap to the independent reasoner;
6. require one RESULT/1 through the declared GitHub comment surface;
7. let the intake workflow authenticate, validate, hash, and preserve the result;
8. let the bounded Release Trust controller open the ordinary evidence PR when the intake branch is valid;
9. protect the raw evidence through ordinary repository controls;
10. adjudicate the mathematics separately;
11. admit, narrow, reject, or retain negative knowledge according to evidence;
12. use MATHCERT only through its existing independent route where certification is actually required.

Do not merge these stages for convenience.

## 15. Source-of-truth surfaces

The principal protected implementation and documentary anchors are:

| Function | Protected surface |
|---|---|
| Controller machine contract | `governance/ns_ci_intake_pr_controller.json` |
| Controller implementation | `ci/ns_ci_intake_pr_controller.py` |
| Persistent controller workflow | `.github/workflows/ns-ci-intake-pr-controller.yml` |
| GH-OS workflow registry | `.ghos-routing/workflows.json` |
| Execution/recovery doctrine | `docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md` |
| Routing-control doctrine | `docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md` |
| Institutional authority doctrine | `docs/governance/GCL_TRUTH_SPINE.md` |
| Cooperative adjudication evidence | MATHSOLVE PR #436 |
| Release Trust qualification evidence | MATHSOLVE PR #445 |
| Deterministic wake admission | MATH-PROGRAMME PR #1039 |
| ACTIVE lifecycle reconciliation | MATH-PROGRAMME PR #1040 |

The raw contribution and receipt remain MATHSOLVE evidence. This document explains the interface and its invariants; it does not replace those evidence objects.

## 16. The architectural lesson

The controlled epistemic interface is useful because it preserves a productive asymmetry:

> **Outside intelligence is allowed to be intellectually foreign. Inside governance remains responsible for what becomes institutional knowledge.**

The interface therefore separates **generation** from **assimilation**, **evidence** from **belief**, and **useful contribution** from **authority**.

In compact form:

```text
GCL supplies the world.
Independent intelligence supplies a bounded thought.
GitHub preserves the thought.
GCL tests the thought.
Protected knowledge changes only through the existing governed route.
```

That separation is the feature.
