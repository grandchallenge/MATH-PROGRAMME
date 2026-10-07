# GCL Research Surface Contract

<p class="page-deck">Every material research campaign has three deliberately different surfaces: a live operational tracker, a protected authority chain, and a Chaidez-compliant human model. No surface may silently assume the function of another.</p>

## Governing invariant

```text
LIVE                         AUTHORITY                       EXPOSITION
GitHub issue          ->     protected repository record -> MkDocs
mutable                      protected/reviewed              explanatory
operational                  epistemic authority             pedagogical
current                      durable                         readable
```

**LIVE answers:** What is happening now?  
**AUTHORITY answers:** What has actually been established within a declared boundary?  
**EXPOSITION answers:** What should a serious reader understand?

## Precedence

1. If MkDocs and a live tracker disagree about current work, the live tracker governs current work.
2. If MkDocs and a protected record disagree about a certified/promoted claim, the protected record governs the claim.
3. A live tracker may describe newer candidate work than a protected record, but it cannot retroactively mutate the protected claim.
4. Closing an issue never creates theorem, certification, publication, or promotion authority by itself.

## LIVE surface

A canonical GitHub issue is the mutable controller for route, blocker, active work packages, pending returns, review state, and next executable step. A terminal campaign may retain a closed canonical tracker. Child issues may carry active specialist routes.

A live tracker must link to the protected baseline and the human-facing page when those exist.

## AUTHORITY surface

A protected record carries exact claim scope, support route, evidence identities, review/protected-merge provenance, dependencies, nonclaims, and supersession. Historical records are not rewritten merely because a successor exists.

Protected records should identify their campaign surface ID and, where practical, the live tracker and exposition page.

## EXPOSITION surface

MkDocs is a projection, not another claim ledger. Serious campaign pages follow the Chaidez sequence:

1. status;
2. plain object;
3. exact obstruction;
4. working model;
5. restricted claim;
6. theorem-spine / DAG location;
7. support route;
8. debt audit and claim boundary;
9. first executable step.

Pages intended for handoff also provide or link an Accessible Research Guide.

Every registered page must display an authority box naming the live tracker and protected authority source.

## Trust quartet

Every serious exposition surface makes four answers visible together:

- What is proved?
- What is checked?
- What remains open?
- What requires external verification?

## Lifecycle

```text
live issue
  -> candidate work / evidence
  -> protected PR admission
  -> authority record / receipt
  -> MkDocs reconciliation
  -> terminal or successor live state
```

The protected merge may trigger a reconciliation diagnostic. It must never automatically promote a mathematical claim.

## Drift classes

- **Operational drift:** the live tracker no longer reflects active work. Repair the issue.
- **Authority drift:** protected successor evidence exists but the registered authority pointer is stale. Repair through protected reconciliation.
- **Expository drift:** MkDocs explains an obsolete frontier. Repair through a documentation PR.

## Machine contract

The registry is `governance/research_surfaces.json`, validated against
`schemas/research_surface_registry.schema.json` by
`ci/validate_research_surfaces.py`.

The registry is a routing/consistency index. It is not mathematical authority.

## Rollout

CM4 is the canonical reference implementation. The initial pilot cohort covers:

- CM4 — terminal theorem plus active external-review/upstream children;
- RH-001 — active multi-route campaign;
- OPENMATH-2026 — worker/intake-heavy distributed campaign;
- YM-001 — source/evidence-bound campaign;
- EUCLID-GCD-E2E-001 — certified formal/certificate exemplar;
- PC-WP01 — negative-result / false-proof atlas.

Active estate migration comes first. Historical material is migrated when touched unless separately prioritized.

## Authority boundary

This contract changes research-state, documentation, and consistency governance only. It grants no mathematical, certification, publication, source-semantic, security, release, or protected-bypass authority.
