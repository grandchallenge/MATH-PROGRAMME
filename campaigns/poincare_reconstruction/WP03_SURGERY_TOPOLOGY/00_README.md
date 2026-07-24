# PC-WP03 — Surgery topology and extinction bookkeeping

## Metadata

- Campaign: `PC-001`
- Work Package: `PC-WP03`
- Tracker: `MATH-PROGRAMME#75`
- Inputs: Referee-promoted `PC-WP01` and theorem-interface-promoted `PC-WP02`
- Governing imported interfaces: `PC02-T013`, `PC02-T014`, `PC02-T016`, `PC02-T017`
- Primary source anchors: Morgan–Tian Theorem 0.3, Proposition 15.3, Corollary 15.4
- State: `REFEREE_PROMOTED_CONDITIONAL_TOPOLOGY_CERTIFICATE`
- Claim boundary: finite combinatorial/topological certification conditional on imported surgery and extinction theorems

## Result-status box

| Field | Value |
|---|---|
| Result status | `WP03 REFEREE PROMOTED / CONDITIONAL TOPOLOGY CERTIFICATE` |
| Strongest supported claim | A source-bound finite event history satisfying the schema reconstructs its initial components as connected sums of the permitted factors; the simply connected orientable profile reduces to `S^3` without circular use of Poincaré |
| Imported, not proved | Existence and placement of surgery necks, metric cap estimates, canonical-neighbourhood theory, local finiteness of surgery times, and finite extinction |
| Certified in package | Identifier/reference integrity, event ordering, active-set evolution, separating/nonseparating transition equations, component ancestry, discard admissibility, finite-history derivation, backward substitution, and terminal group-profile discharge |
| Numerical evidence | None |
| Next stage | `PC-WP04` bounded formalization/certificate substrate |

## The source-level topology theorem

For a singular time `t`, Morgan–Tian Proposition 15.3 gives the governing backward statement:

> The pre-surgery slice is obtained from the disjoint union of the post-surgery slice, finitely many `S^2`-bundles over `S^1`, and finitely many spherical space forms by connected-sum operations.

This package turns that theorem interface into a finite event language. It does not infer the topology from a geometric picture alone.

## Event model

A history contains:

1. a finite registry of component intervals;
2. a finite registry of emitted topology factors;
3. a strictly ordered list of surgery or terminal-extinction transitions;
4. complete active-component sets immediately before and after each event;
5. cut, cap, discard, ancestry, reconstruction, and source-binding records;
6. local-finiteness and finite-extinction evidence;
7. a backward normal form for the initial component set.

The authoritative schema is `01_EVENT_SCHEMA.json`. Cross-record invariants that JSON Schema cannot express are enforced by `05_ADVERSARIAL_HISTORIES/validate_histories.py`.

## Primitive transition equations

### Separating cut

Cutting on a separating `2`-sphere and capping both new boundary spheres produces two post-surgery components:

```math
C^- \cong C_1^+ \# C_2^+.
```

### Nonseparating cut

Cutting on a nonseparating `2`-sphere and capping produces one post-surgery component and an `S^2`-bundle factor:

```math
C^- \cong C^+ \# H.
```

For the orientable Poincaré profile,

```math
H=S^2\times S^1.
```

The twisted bundle is retained only in the general no-locally-separating-`RP^2` profile.

### Discarded component

A discarded component must carry a source-bound topology certificate in the permitted list:

- spherical space form;
- orientable `S^2`-bundle over `S^1`;
- nonorientable `S^2`-bundle over `S^1`;
- `RP^3#RP^3`, normalized to two spherical factors.

### Topologically neutral cap replacement

Replacing a punctured `3`-ball by a `3`-ball does not change the diffeomorphism type. Metric suitability of the inserted cap remains the imported `PC02-T010` contract.

## Finite-history gate

The package deliberately rejects:

```text
discrete surgery times + finite extinction => finite history.
```

Discreteness alone is not the registered premise. The accepted derivation is:

```text
finitely many surgery times on every bounded interval
+ finite extinction time T_ext
=> finitely many events in [0,T_ext].
```

Both premises remain provenance-bearing imports.

## Backward reconstruction

At each event, every changed pre-component appears exactly once on the left of a reconstruction equation. Every new post-component appears exactly once as a right-hand summand. Forward surgery never merges components.

Starting from the empty terminal slice, substitute the event equations in reverse chronological order. Finiteness of the history makes the substitution terminate. The initial manifold becomes a connected sum of the factor registry's normalized summands.

## Non-circular Poincaré discharge

Only after the factor expression exists do we use `pi_1(M)=1`.

- nontrivial spherical space forms contribute nontrivial finite groups;
- `S^2`-bundles over `S^1` contribute infinite cyclic groups in the orientable case;
- `RP^3#RP^3` contributes `Z/2 * Z/2`;
- connected sum gives free product by van Kampen.

A trivial free product has no nontrivial factor group. The remaining spherical factors have trivial deck group and hence are `S^3`. Connected sum with `S^3` is neutral.

No step assumes that an arbitrary simply connected prime `3`-manifold is `S^3`.

## Delivered artifacts

```text
00_README.md
01_EVENT_SCHEMA.json
02_TRANSITION_CATALOGUE.md
03_COMPONENT_ANCESTRY.md
04_BACKWARD_RECONSTRUCTION.md
05_ADVERSARIAL_HISTORIES/
06_DEPENDENCY_DAG.json
09_PROOF_DEBT.json
10_CLAIM_LEDGER.yaml
11_CERT_HANDOFF.md
12_NEXT_EXECUTABLE_STEP.md
```

## Claim boundary

WP03 does not prove that a Ricci flow reaches a qualifying neck, that surgery parameters can be selected, that the post-surgery metric satisfies analytic estimates, or that extinction occurs. It proves and tests what follows from a finite source-compliant topology history once those imported facts are supplied.
