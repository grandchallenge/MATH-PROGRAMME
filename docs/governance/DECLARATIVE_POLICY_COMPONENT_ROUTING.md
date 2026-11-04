# Declarative component impact routing

**Contract:** MP-POLICY-IMPACT-GATING-001, declarative component extension (November 2026). This is an extension of the protected policy classifier, not a second controller or an exception to protected admission.

## Adding a programme

Add one version-controlled JSON manifest to `governance/policy_components/<component_id>.json` using `schemas/policy_component_manifest.schema.json`. No edit to `ci/policy_impact.py` is needed. Each component must declare its stable ID, ownership, policy-shard obligations, zero or more upstream component dependencies, and the files it owns using exact paths, directory prefixes, or test-module prefixes. For example:

```json
{
  "schema_version": "1.0.0",
  "component_id": "example",
  "owner": "Example research programme",
  "shards": ["docs", "repository-regression"],
  "depends_on": ["oai26"],
  "paths": {
    "exact": [],
    "prefixes": ["governance/example/"],
    "test_prefixes": ["tests/test_example_"]
  }
}
```

New files beneath these declared scopes are discovered automatically. The new manifest itself is a protected control-plane modification: its PR always runs full policy validation before admission. A new test file outside any recognized route is rejected on the exact PR/push diff; unrecognized existing paths continue to trigger full policy fanout. Thus *discovery is automatic but authority is not*. A new experimental programme with no connection to OAI26 should use `depends_on: []`, not the example dependency shown above.

## Dependency semantics and safety

`depends_on` means the named component consumes the upstream component. When upstream source changes, the classifier runs the upstream's shards and all transitive downstream consumer shards. When only a downstream consumer changes, unrelated upstream shards are not unnecessarily replayed. Two manifests owning the same changed file, missing dependencies, dependency cycles, unknown shards, unsafe paths, and control-plane capture fail the classifier. Pattern matching uses declared boundaries, not arbitrary substrings. Versioned schema validation and exact-name matching prevent silent typos.

Routing manifests define **what to test**, not proof validity, mathematical certification, independent review, public release, or merge authority. Protected required contexts, the formal-validation router, merge-group full validation, scheduled full sentinels, and existing protected GitHub queue policy remain authoritative. Updating the classifier, component manifests, or manifest schema forces full policy replay.

## Drift and adversarial acceptance

The protected core shard runs `python3 ci/policy_impact.py validate` and `python3 ci/test_policy_impact.py` on each applicable policy execution. The tests demonstrate automatic discovery of a previously unknown programme, direct and transitive dependency propagation, ambiguous owners, cycles, missing targets, undefined shards, and control-plane capture. The exact-transition source guard rejects newly added Python test modules whose paths are not covered by a bounded declared or legacy route. Existing legacy routes remain in place during adoption to prevent unrelated changes in coverage.

A future compendium PR adding `governance/oai26_documentary/editorial/NNN.md` and updating `tests/test_oai26_compendium.py` must select only `core`, `contracts`, `docs`, and `repository-regression` on the PR transition, with no unknown paths. Conversely a change to a shared component must propagate to registered dependent consumers. The protected full-suite sentinel remains the backstop against underclassification.

## Operator diagnostics and recovery

For a failing `Classify policy impact` job, examine the exact-head JSON `changed_paths`, `unknown_paths`, `policy_shards`, and `event_mode`. If a new test lacks an owner, create or update its component manifest on the same candidate and replay exact-head CI; do not label the missing route a safety block or weaken required checks. If ownership collides, resolve which programme truly owns the file, or move shared material to a dedicated upstream component with explicit dependents. If a manifest edit changes the routing graph, the control-plane change intentionally replays all shards. Do not bypass or reinterpret formal-validation, protected merge-group checks, or certification boundaries.

## Extension limits

The discovery mechanism requires an explicit version-controlled ownership/dependency declaration. It does **not** infer semantic dependencies from source imports or invent ownership for entirely new programme names. If the declared programme uses a new shard rather than an existing shard, extending the protected shard execution registry is a separate control-plane modification with full replay. These limitations are deliberate: silent guessing would undermine the fail-closed contract.
