# Programme Workflow Coverage

## Purpose

The programme workflow is a claim-boundary control. A green documentation build alone is insufficient. Campaign replays, repository tests, executable policy controls, formal fixtures, cross-repository evidence, provider contracts, exact publication artifacts, and repository administration must remain distinct and governed.

## Current audit disposition

The umbrella audit dated 2026-07-29 is recorded in `WORKFLOW_COVERAGE_AUDIT_2026_07_29.md` and `governance/workflow_coverage_audit.json`.

Its determination is:

- CI contract coverage: `COMPLETE`;
- technical umbrella children: `COMPLETE`;
- administrative umbrella children: `COMPLETE`;
- `operational_release_complete: true`;
- remaining blockers: none;
- umbrella issue #6: `CLOSE`.

The admitted administrative evidence is App-backed release-trust run `30450610588`, artifact `8723362498`, and canonical evidence SHA-256 `acd7e9c3ea10e9c03ea5dc81a0b84918d7241fea886426d2304e168b10c936f8`.

The historical audit remains a historical record. Current execution semantics are additionally governed by `MP-STREAMLINED-EXECUTION-001`, the policy-shard classifier and registry, and the formal-validation material-closure registry.

## Global policy gate

`.github/workflows/ci.yml` is the global `Programme policy checks` workflow. It runs on pull requests, pushes to `main`, merge groups, explicit manual audits, and scheduled policy assurance according to the workflow definition.

The workflow uses read-only repository permissions, bounded timeouts, non-persistent checkout credentials, immutable action references, fixed runner families, checked-in dependency pins, and concurrency cancellation.

The policy workflow is impact-routed. `ci/policy_impact.py` classifies only Programme policy obligations and selects policy shards from `governance/policy_shard_registry.json`. Formal proof replay is not a policy-shard side effect. The current policy shard set is:

- `core`;
- `fixtures`;
- `cmdg`;
- `oz`;
- `administrative`;
- `campaigns`;
- `contracts`;
- `docs`;
- `repository-regression`.

The required `validate-json` context is the aggregation gate for the routed policy DAG. It is not a monolithic executor and must not be interpreted as evidence that every shard ran on every candidate.

| Job / context | Controlled obligation |
|---|---|
| `Classify policy impact` | Determine affected policy shards from the material transition; unknown or central dependency-map changes fail closed |
| `Policy shard / <name>` | Execute only the selected governed shard commands under the registered execution envelope |
| `validate-json` | Aggregate the selected policy shards into the stable policy status context |

## Formal validation gate

`.github/workflows/formal-validation.yml` is the separate formal-validation workflow. `governance/formal_validation_registry.json` is the source of truth for formal lane identities, material dependency closures, promotion targets, and sentinel scope. `ci/formal_validation.py` validates that registry, classifies the exact transition, and constructs the dynamic lane matrix.

The governing rule is material closure: an ordinary candidate instantiates a substantive formal lane only when the exact candidate transition intersects that lane's declared material closure. A formal control-plane change conservatively selects the full formal lane set. An unknown managed formal or formal-executable path fails closed.

| Job / context | Controlled obligation |
|---|---|
| `Classify material formal closure` | Resolve the exact changed paths and select only materially affected formal lanes |
| `<formal lane id>` | Execute one selected formal lane under its registered package, validator, and proof-environment contract |
| `formal-validation / formal-validation` | Aggregate the exact selected lane matrix into the generic formal status context |

CMDG development validation compiles the changed Lean leaf plus its actual local import closure. It does not replay historical CMDG stages merely because they precede the changed theorem in the research programme. Shared CMDG environment changes still select all CMDG lanes because they can affect every lane.

Standalone CMDG workflows and `pc-wp04.yml` are promotion/manual replay surfaces, not ordinary PR triggers. CMDG promotion uses the complete registered lane source closure. Protected-main sentinels preserve periodic whole-family assurance independently of candidate-local development validation.

Candidate formal execution is deliberately unprivileged. The generic workflow has read-only contents permission, no repository secrets or write token, non-persistent checkout credentials, exact candidate-SHA checkout, pinned actions, and no GitHub Actions cache persistence. The pinned Lean action may run Mathlib's retrieval-only `lake exe cache get` path so the exact committed Lake dependency graph and precompiled Mathlib artifacts are materialized locally without a repository-wide source build; the resulting `.lake` state is not saved into a GitHub Actions cache. The Union-Closed external authority is a fixed audited `grandchallenge/MATHCERT` commit rather than candidate-controlled repository/ref data. Promotion workflows reject non-`main` execution before Python or Lean/cache setup.

During the required-context migration only, three compatibility jobs retain the legacy required context names. They perform no campaign replay; each depends only on the generic formal aggregate. After Programme ruleset `17137629` requires `formal-validation / formal-validation`, those compatibility aliases are removed. This bridge prevents an enforcement gap while avoiding duplicate substantive validation.

A successful policy or formal workflow records integration, execution, policy, artifact, or bounded-certification facts. It does not promote an open mathematical claim.

## Execution bounds and de-duplication

Policy execution is bounded at both command and unittest-module levels.

- The default policy-shard command timeout is 900 seconds.
- A longer command may exceed that bound only through an exact registry entry binding the shard, command index, exact argv, timeout, and reason.
- `ci/run_unittest_modules.py` bounds an individual module at 420 seconds and a unittest aggregate at 1620 seconds; timeout termination kills the subprocess process group.
- The runner emits module start, exclusion, timing, timeout, and aggregate timing records so a long computation is observable rather than appearing as a silent hang.

`repository-regression` is complementary coverage, not a second execution of every dedicated suite. Its governed exclusions remove test families already owned by the OZ, CMDG, fixture, administrative, campaign, and contract lanes. A full policy sentinel obtains full coverage by composing the dedicated shards with repository regression; it does not need repository regression to rerun those same suites serially.

The hardening admitted through PR #760 established the practical effect. Before de-duplication, repository regression largely repeated the expensive OZ suite and consumed roughly 24 minutes. The admitted full-sentinel validation reduced the routed repository-regression execution step to approximately 11 seconds while preserving its residual repository coverage. The same validation measured the then-monolithic OZ routed step at approximately 1024 seconds, identifying OZ computational replay as a distinct cost centre rather than a generic regression-runner problem.

## Odd Zeta computational replay routing

Odd Zeta is intentionally different from ordinary unit-test coverage. Some OZ tests reconstruct exact symbolic objects, execute bounded searches and rank computations, and independently replay mathematical producers and verifiers. Those operations are scientific replay evidence and can legitimately take minutes.

Protected merge #763 therefore separates frequent structural validation from expensive computational replay without sharing producer/verifier state and without caching mathematical conclusions.

The current rule is:

1. when the OZ lane owns a transition, all inexpensive OZ modules continue to run;
2. the measured expensive replay set runs only when its material computational dependency closure changes;
3. cumulative T3-010/T3-011 dependencies propagate forward, and relevant upstream T3-002/T3-005/T3-006/T3-009 computational changes invalidate the downstream replay closure conservatively;
4. shared computational helpers that cannot be assigned safely to a narrower stage fail closed to the applicable downstream replay set;
5. Odd Zeta campaign-source changes reach the same replay router through the `campaigns` shard;
6. scheduled and manual full sentinels replay the complete expensive set regardless of transition-local reuse;
7. producer and independent verifier computations remain independent; routing does not authorize shared mathematical state or result caching.

The protected-run profile used for admission identified 12 modules as approximately 98% of the previous OZ wall time. On PR #763, where those material inputs were unchanged, the router explicitly reported `heavy_selected=0` out of 12, ran 24 fast OZ modules successfully in 21.199 seconds, and completed the OZ shard in 22.161 seconds. Relative to the approximately 1024-second pre-routing OZ step, this is about a 46x reduction for an unrelated/control-plane transition. The campaign-side router also exited explicitly as `no-odd-zeta-material-change` in approximately 0.064 seconds.

These timings are operational evidence, not mathematical evidence. A material OZ transition still pays the computational replay cost required by its dependency closure, and scheduled/manual assurance still exercises the full expensive replay set.

## Covered repository surfaces

The global contract covers:

- recursive campaign executable discovery;
- executable CI-control reachability;
- policy-shard impact classification and formal material-closure routing as separate control planes;
- repository tests and experiment reachability;
- bounded command and unittest execution;
- symbolic resource budgets and failure ledgers;
- reusable cross-pillar lane packages;
- MATHFORGE provider imports;
- MATHSOLVE routing;
- programme-wide MATHCERT conformance;
- bounded MATHFORGE algebraic witness generation;
- bounded MATHSOLVE algebraic tactic routing;
- material-closure formal Lean development validation and protected promotion/sentinel replay;
- pinned external certification evidence;
- material-input-routed computational mathematics such as Odd Zeta replay;
- strict documentation construction;
- exact-artifact Pages publication semantics;
- governed fast-path workflows.

## Bounded algebraic provider chain

The algebraic lane now has explicit contracts at each provider boundary.

### MATHFORGE

A governed witness must record local scope, coefficient domain, variable and degree bounds, timeout, basis and term budgets, exact backend identity, observed execution, expected witness, fallback route, failure ledger, and content-addressed registry identity.

MATHFORGE outputs evidence. A `ready_for_mathcert` witness is not certified.

### MATHSOLVE

A governed tactic invocation must identify one local proof obligation, reject global open-problem encoding, declare resource limits and fallback conditions, identify the expected witness, pin its source, and state the exact MATHCERT checking obligation.

Packet readiness and submission are intake states. Only a content-addressed MATHCERT disposition can close the certification boundary.

## Policy-validated site artifact

On a successful push to `main`, the policy job packages the strict MkDocs output as a deterministic validated-site artifact. The Pages workflow deploys only that verified artifact and does not rebuild documentation independently.

Publication proceeds only when the policy run succeeded for a `main` push, the validated SHA remains the current `main` tip, artifact digests verify, safe extraction succeeds, and the site contains its required entry point.

This repository-side publication contract is complete. Issue #7 is closed: the release-trust evidence records the repository homepage, exact-main policy run, Pages deployment, validated-site artifact, and byte-identical public index.

## Protected-branch boundary

Exact-head workflow success alone does not prove that a repository administrator cannot bypass the workflow. Issue #125 is closed because the Release Trust App applied and read back the authoritative ruleset evidence for each mathematics governance repository.

The admitted administration record states:

- ruleset or protection identifier;
- required status-check context;
- strict or up-to-date requirement;
- review requirement;
- bypass actors or explicit absence of bypass;
- effective date and verification method.

Current streamlined execution permits non-strict protected status checks for concurrent development where the material evidence closure remains valid. Branch-head freshness is not itself a claim-boundary control.

## Closure rule

MATH-PROGRAMME issue #6 may close only when:

1. Pages issue #7 is complete;
2. protected-branch issue #125 is complete;
3. the MATHFORGE and MATHSOLVE technical children remain complete;
4. `remaining_blockers` is empty;
5. `operational_release_complete` is `true`.

Merge state, workflow success, test success, witness identity, certification, publication visibility, and mathematical theorem support remain separate facts.
