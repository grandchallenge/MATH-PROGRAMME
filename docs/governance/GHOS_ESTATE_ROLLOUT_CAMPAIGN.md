# GH-OS estate rollout and conformance campaign

**Identifier:** `GHOS-ESTATE-ROLLOUT-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#724`  
**State:** Active; Phase 0 complete; Phase 1 ready  
**Canonical manifest:** `governance/ghos_estate_rollout_campaign.json`  
**Phase-1 handoff:** `handoffs/GHOS-ESTATE-ROLLOUT-001/PHASE1/HANDOFF.md`

## Protected admission

The campaign definition was admitted through merged PR `#726`:

- exact candidate: `d7888766a01d9e20153376a3c7f3cc4635911610`;
- protected merge: `06fdcda8c18f395403dc544274fb98fee36ef6ea`.

The earlier `Candidate pending protected admission` projection is superseded.

## Purpose

GH-OS has demonstrated the core control-plane properties needed for bounded, replaceable conversational agents: durable state, exact-head evidence binding, persistent-controller admission, candidate-independent routing enforcement, hostile rejection, and protected readback. The remaining institutional obligation is to make those guarantees estate-wide rather than repository-local.

This campaign rolls the execution-routing control across every active `grandchallenge` repository or records an explicit governed non-applicability disposition. It does not redesign GH-OS and does not create mathematical, certification, constitutional, publication, production, or commercial authority.

## Campaign invariant

For every active repository, a fresh operator must be able to answer from durable protected state:

1. What direct execution surfaces exist?
2. What safety-relevant features are present in their actual bytes?
3. What execution topology is therefore required?
4. Which exact controller, if any, is admitted to provide that topology?
5. Which candidate-independent required check enforces the routing decision?
6. Which exact evidence proves the protected repository is conformant?

No registry entry, README, issue statement, candidate-local validator, or agent assertion may downgrade a topology derived from executable workflow state.

## Reference pattern

`gcl-standards` and `MATH-PROGRAMME` are the reference implementations. The reusable pattern is:

`workflow bytes -> derived features -> derived topology -> controller compatibility -> candidate-independent routing check -> protected ruleset -> hostile proof -> protected readback`

The shared external gate is hosted in `grandchallenge/.github`; consumers pin governed gate bytes by immutable identity and digest rather than following mutable branch state.

Current admitted shared gate:

- commit `ef1cce6029233a68cf46063cea2384772fcae613`;
- path `scripts/ghos_execution_routing_gate.py`;
- blob `f9f85937713046eacdc79c532046c676cbb4550c`;
- SHA-256 `fc0a9a4d20de72e9fbc04c8cd54cffc3a6e4657fb09e7978b360616bd5e94a17`.

## Estate phases

### Phase 0: shared control — COMPLETE

Repositories:

- `grandchallenge/.github`;
- `grandchallenge/gcl-standards`;
- `grandchallenge/MATH-PROGRAMME`.

Phase-0 terminal state is `GHOS_ROUTING_ENFORCED` for all three repositories.

The shared-control tracker `grandchallenge/.github#67` is closed completed. Final protected `.github/main` for Phase 0 is `6a3693fe5a9c6ee6bb420a429f9421801e35457f`; final protected control blob is `21d04288a32321af09b3ee503e9cf4c9f6af5fee`. The classifier deviation `GHOS-CLASSIFIER-PROJECT-MUTATION-001` is closed. Successor-era hostile proofs in `.github`, `gcl-standards`, and `MATH-PROGRAMME` all failed closed and were closed unmerged.

Umbrella checkpoint: `MATH-PROGRAMME#724` comment `5493507033`.

Do not reopen Phase 0 merely because a later unrelated protected commit advances a reference repository head. Reopen only on a material protected control contradiction or routing regression.

### Phase 1: constitutional and MATH authority chain — READY

Repositories, in execution order:

1. `grandchallenge/INTELLECT` — tracker `#73`;
2. `grandchallenge/MATHFORGE` — tracker `#117`;
3. `grandchallenge/MATHSOLVE` — tracker `#131`;
4. `grandchallenge/MATHCERT` — tracker `#232`.

All four have applicable direct workflow surfaces, no `.ghos-routing/workflows.json` on the inspected protected baseline, and no mandatory `routing-enforcement` context. Phase 1 requires repository-specific hostile proof because routing defects here can affect constitutional policy, provenance, mathematical production, or certification state.

The complete independent-agent orientation and execution procedure lives in:

- `handoffs/GHOS-ESTATE-ROLLOUT-001/PHASE1/HANDOFF.md`;
- `handoffs/GHOS-ESTATE-ROLLOUT-001/PHASE1/STATE.json`;
- `handoffs/GHOS-ESTATE-ROLLOUT-001/PHASE1/GLIDEPATH.md`.

### Phase 2: persistent agentic coordination

Repository:

- `grandchallenge/AETHER`.

AETHER is not automatically admitted as its own persistent controller. Its durable wake, state, authorization, replacement, stale-evidence rejection, and recovery semantics must be demonstrated independently. GH-OS correctness must not become dependent on AETHER availability unless a later explicit authority decision says so.

### Phase 3: active technical programmes

Repositories:

- `grandchallenge/MODULUS`;
- `grandchallenge/GLOSS`;
- `grandchallenge/QUANTUM-TECHNOLOGIES`;
- `grandchallenge/TROVE-CURATA`.

Use a common rollout profile where repository topology is genuinely equivalent, but retain repository-specific workflow inventory, ruleset readback, and protected admission evidence.

### Phase 4: shared action and publication tooling

Repositories:

- `grandchallenge/lean-action`;
- `grandchallenge/upload-pages-artifact`.

These repositories require local routing conformance plus downstream trust analysis. Consumers must use immutable action identities; local conformance cannot make a floating consumer reference safe.

## Per-repository procedure

For each unresolved repository:

1. Bind repository ID, default branch, current protected head, ruleset identity, and workflow inventory.
2. Determine whether routing is applicable. A repository with no applicable execution surface may use `GHOS_GOVERNED_NON_APPLICABLE`, but only with protected evidence.
3. Derive execution features from every direct workflow byte-for-byte.
4. Derive the minimum topology. Do not copy declarations from another repository without re-derivation.
5. Bind an admitted controller to every non-bounded workflow, or decompose the workflow into independently resumable bounded transactions.
6. Add repository-local registry, deterministic validation evidence, and protected-base enforcement using the shared pinned gate where compatible.
7. Make `routing-enforcement` a required protected context with intended strictness and no unexpected bypass actor.
8. Run exact-head repository policy/security/conformance checks.
9. Execute hostile proof. For Phase 1, this is repository-specific. For lower-risk repositories, a shared profile proof may supplement but not replace repository-specific inventory and ruleset evidence.
10. Obtain required exact-revision review and authorized merge.
11. Read back protected main, enforcement bytes, registry, ruleset, controller identity, and successful post-merge checks.
12. Record one terminal repository disposition in the estate ledger.

## Phase-1 implementation note

The Phase-0 MATH-PROGRAMME enforcement workflow installs `protected-base/requirements/policy.txt`. The four Phase-1 repositories do not have that path on their recorded baselines. Therefore the reference enforcement workflow must be adapted rather than copied verbatim. The shared gate imports PyYAML, and protected `.github` routing tests use `PyYAML==6.0.3`; use a repository-appropriate reviewed dependency step while preserving the candidate-independent execution model.

For MATHCERT, existing ruleset `17137628` has non-strict required-status policy. Do not silently change that certification-profile policy. The default Phase-1 strategy is a separate active strict zero-bypass routing ruleset requiring `routing-enforcement`, unless an explicit repository-policy decision authorizes a broader change.

## Hostile proof

The hostile candidate should attempt enough of the following to prove that the mandatory decision is outside candidate control:

- remove or bypass candidate-local routing validation;
- add an unregistered scheduled or write-capable workflow;
- declare a weaker topology than derived from workflow bytes;
- bind an incompatible or absent controller;
- repin a reusable policy caller to a pre-enforcement revision;
- modify the enforcement workflow itself;
- alter a shared-gate path or digest without the governed upgrade route;
- carry stale review/check evidence to a new head.

Success means ordinary candidate-controlled checks may still pass, while the independently required routing gate fails and protected integration remains blocked.

## Persistent-controller admission

A controller satisfying `PERSISTENT_CONTROLLER_REQUIRED` needs evidence for:

- durable wake independent of conversational lifetime;
- durable state storage;
- exact controller and repository identity;
- supported feature classes;
- idempotent/recoverable transaction semantics where applicable;
- stale-evidence rejection;
- replacement recovery;
- interrupted or expired-operation recovery;
- unauthorized-transition refusal;
- separation of technical capability from governance authority.

The currently demonstrated repository-bound GitHub Actions controller may be reused only where the shared gate and local policy explicitly admit it for the repository and required features.

## Campaign-level controls

The campaign itself is `MULTI_SESSION_RESUMABLE` with persistent suboperations. A conversational agent may execute bounded transactions, but it is not the sole persistent controller. Every repository tracker and campaign transition must leave enough durable state for replacement without chat reconstruction.

Avoid broad polling. Bind asynchronous observations to exact repository, head, run, and job. A pending external job is an external wait, not a reason for the active conversational agent to remain alive.

## Terminal estate acceptance

The campaign may close only when:

- the canonical estate manifest matches the active organization repository inventory;
- every active repository has exactly one terminal disposition;
- every applicable direct workflow is registered;
- no declared topology is weaker than derived topology;
- every non-bounded workflow has an admitted compatible controller;
- routing enforcement is candidate-independent and required on protected integration;
- shared gate compatibility and immutable consumer pinning are proven;
- Phase 1 hostile proofs pass;
- every other distinct enforcement profile has hostile evidence;
- an estate-wide gap scan finds no unexplained repository, workflow, controller, or ruleset gap;
- archived/inactive repositories are explicitly accounted for;
- the terminal evidence receives independent exact-revision review;
- MATH-PROGRAMME documentary closure is completed by registered closure contract and protected readback receipt.

The only successful estate terminal is `GHOS_ESTATE_CONFORMANCE_GREEN`. A partially complete estate remains explicitly partial; repository-level success must not be inflated into organization-wide conformance.
