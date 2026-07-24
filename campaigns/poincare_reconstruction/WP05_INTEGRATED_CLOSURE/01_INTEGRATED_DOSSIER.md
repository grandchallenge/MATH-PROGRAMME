# PC-WP05 — dependency-complete integrated dossier

## 1. Campaign posture

`PC-001` reconstructs and selectively certifies a solved classical theorem. The theorem is not reopened. The programme objective is to make the Hamilton–Perelman route source-normalized, dependency-explicit, adversarially guarded, pedagogically usable, and honest about the boundary between literature import and repository-native certification.

## 2. Canonical theorem and categories

Topological statement:

```text
M closed, connected, topological 3-manifold and pi1(M)=1
  => M homeomorphic to S3.
```

Smooth statement after the dimension-three category bridge:

```text
M closed, connected, smooth 3-manifold and pi1(M)=1
  => M diffeomorphic to S3.
```

The bridge is an imported classical theorem package. It is not inferred from Ricci flow and is not hidden inside the phrase “choose a metric.”

## 3. Work-package integration

### WP00 — source, normalization and equivalence

WP00 fixed the solved status, canonical theorem, category conventions, route hierarchy, source tiers, theorem spine, non-circularity constraints, claim ledger, proof debt, and certification boundary.

Authoritative artifact:

- `../WP00_SOURCE_EQUIVALENCE/00_README.md`

### WP01 — false-proof atlas

WP01 attached exact adversarial guards to the proof spine. It excludes homology-sphere substitutions, open-manifold substitutions, category suppression, smooth flow through singularities, pointed-limit/global-manifold confusion, deleted canonical-neighbourhood hypotheses, topology-preserving-surgery assumptions, extinction-as-classification, orientation suppression, source-version drift, local/global finiteness confusion, circular prime-factor discharge, and formalization overclaim.

Authoritative artifact:

- `../WP01_FALSE_PROOF_ATLAS/00_README.md`

### WP02 — Hamilton–Perelman theorem ledger

WP02 records nineteen source-normalized interfaces covering category entry, short-time flow, entropy and reduced geometry, noncollapsing, ancient limits, canonical neighbourhoods, cap and surgery control, all-time surgery, bounded-interval surgery finiteness, topology mutation, finite extinction, backward reconstruction, and terminal discharge.

Its status is theorem-interface reconstruction, not independent analytic proof.

Authoritative artifact:

- `../WP02_HAMILTON_PERELMAN_LEDGER/00_README.md`

### WP03 — surgery topology and extinction bookkeeping

WP03 converts the imported topology interfaces into a finite event language. It represents separating and nonseparating cuts, caps, active components, discarded standard components, ancestry, source bindings, bounded-interval finiteness, extinction evidence, and backward connected-sum reconstruction. Two valid and twelve malformed histories are executable in repository CI.

Authoritative artifact:

- `../WP03_SURGERY_TOPOLOGY/00_README.md`

### WP04 — bounded kernel-checked evaluator

WP04 formalizes finite factor expressions, event contracts, histories, a total backward evaluator, active-set coverage, exact support, no-component-loss extraction, evaluator correctness conditional on `ImportedEventRelation`, source preservation, and a bounded terminal compatibility predicate.

It does not formalize manifold connected sum, van Kampen, Ricci flow, surgery existence, or finite extinction.

Authoritative artifacts:

- `../WP04_BOUNDED_CERTIFICATION/00_README.md`
- `../../../fixtures/formal/PC-WP04/README.md`

## 4. Complete dependency chain

```text
PC-D000 definitions and category conventions
  -> PC-L001 Top/PL/Diff bridge
  -> PC-L003 smooth metric
  -> PC-L004 short-time Ricci flow
  -> PC-L005 entropy, reduced geometry, pseudolocality, noncollapsing
  -> PC-L006 ancient limits and canonical neighbourhoods
  -> PC-L007 standard caps, surgery and all-time continuation
  -> PC-L008 topology of cuts, caps and discarded components
  -> PC-L011 finite event history and backward reconstruction
  -> PC-L012 free-product/simple-connectivity discharge
  -> PC-C013 smooth Poincare
  -> PC-C014 topological Poincare.

PC-L002 simple connectivity implies orientability
  -> admissibility of the orientable surgery/extinction profile.

PC-L009 prime decomposition/no-aspherical-factor bridge
  -> PC-L010 finite extinction
  -> PC-L011.
```

Repository-native certification overlays only the final finite-history layer:

```text
WP02 imported event/extinction interfaces
  -> WP03 validated finite history
  -> WP04 formal event relation assumption
  -> kernel-checked finite evaluator consequences.
```

## 5. Source route

- Perelman I supplies entropy, reduced-volume, noncollapsing and singularity-model machinery, and sketches the geometrization programme.
- Perelman II constructs and controls Ricci flow with surgery, explicitly marks two earlier assertions as deferred or unjustified, and keeps those assertions outside the finite-extinction Poincaré route.
- Perelman III proves finite extinction for closed oriented 3-manifolds with no aspherical prime factors.
- Kleiner–Lott supplies a detailed reconstruction of Perelman I and II, including nonaccumulation, topology reversal and the finite-extinction handoff.
- Morgan–Tian supplies a complete detailed Poincaré proof following all three preprints, with explicit long-time surgery, topology-change, finite-extinction and terminal-reconstruction statements.

## 6. Critical logical separation

The archive keeps four propositions separate:

1. a valid analytic Ricci-flow-with-surgery solution exists;
2. its surgery events have the recorded topology;
3. the relevant flow becomes extinct in finite time;
4. a finite valid event history reconstructs the initial connected-sum expression.

WP03 and WP04 certify consequences of items 2–4 only after items 1–3 are imported through named source interfaces. Schema validity never implies event existence.

## 7. Terminal discharge

Backward reconstruction first yields an independent factor expression built from spherical space forms and sphere bundles. Only afterward is `pi1(M)=1` applied. Van Kampen/free-product reasoning excludes every nontrivial spherical quotient and every sphere-bundle factor. Remaining `S3` summands collapse under connected sum to `S3`.

No step assumes that an arbitrary simply connected prime 3-manifold is already `S3`.

## 8. Certification surface

| Layer | Status |
|---|---|
| Classical theorem | established in the literature |
| Primary analytic route | source imported |
| Detailed proof reconstruction | Morgan–Tian; Kleiner–Lott for Perelman I/II |
| Theorem-interface ledger | Referee promoted |
| Finite event schema and validator | repository tested |
| Finite backward evaluator | Lean kernel checked |
| Full analytic formalization | absent |
| Manifold-level connected-sum formalization | absent |
| Full Poincaré proof certificate | prohibited |

## 9. Closure conclusion

The dependency graph is complete for a qualified archival reconstruction: every edge is either literature-imported, executable, or kernel checked, and each transition is labeled accordingly. Remaining source-concordance and formalization debts are retained in `08_PROOF_DEBT.json`; none may be silently interpreted as discharged.