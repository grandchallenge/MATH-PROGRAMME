# PC-WP03 — Transition catalogue

## 1. Governing source interface

Let `M_{t^-}` denote a slice immediately before a surgery time and `M_t` the post-surgery slice. Morgan–Tian Proposition 15.3 states, under the controlled-surgery assumptions, that `M_{t^-}` is diffeomorphic to a manifold obtained by:

1. taking the disjoint union of `M_t`;
2. adjoining finitely many `S^2`-bundles over `S^1`;
3. adjoining finitely many closed spherical space forms;
4. performing connected sums among subsets of these components.

The event schema records a refinement of this backward statement. The refinement is valid only under the imported `PC02-T014` topology interface.

## 2. Batch-event semantics

A surgery time may contain finitely many disjoint neck operations and whole-component removals. One event therefore contains arrays of cuts, caps, discards, ancestry edges, and reconstruction groups.

The event is atomic with respect to the ordered history:

```text
active_before -- one source-governed surgery transition --> active_after.
```

The schema does not impose an artificial ordering among disjoint operations performed at the same time.

## 3. Separating sphere cut

### Forward record

```text
parent C
cut along separating S^2
cap both boundary spheres by D^3
produce children A and B
```

Required fields:

- one active parent;
- exactly two distinct child component identifiers;
- exactly two cap identifiers, one for each side;
- two ancestry edges `C -> A` and `C -> B`;
- one backward reconstruction group.

### Backward equation

```math
C \cong A\#B.
```

An `S^3` child is permitted and is neutral after normal-form reduction. The validator does not silently delete it before the source-bound factor certificate is present.

## 4. Nonseparating sphere cut

### Forward record

```text
parent C
cut along nonseparating S^2
cap both boundary spheres by D^3
produce one child A
emit one S^2-bundle factor H
```

Required backward equation:

```math
C\cong A\#H.
```

For an orientable history, `H` must be the orientable bundle `S^2 x S^1`. For the more general source profile, the twisted bundle may occur.

A nonseparating cut without the bundle factor is rejected by `PC03-E007`.

## 5. Cap insertion

Every cut has two cap records:

```yaml
topological_type: D3
metric_contract_ref: PC02-T010
```

The topology layer uses only the `D^3` attachment. The metric cap quality, pinching preservation, and restart estimates are not re-proved.

## 6. Punctured standard pieces

The proof of Proposition 15.3 distinguishes several local replacements.

### `D^3` or `S^2 x (0,1)` pieces

Replacing a punctured `D^3` by a `D^3` is topologically neutral. Replacing `S^2 x I` by two balls realizes the separating or nonseparating sphere-surgery rules above.

### `RP^3 \setminus B^3`

Replacing a punctured `RP^3` by a ball extracts an `RP^3` connected-sum factor. The schema represents the extracted factor as a spherical space form.

### `RP^3#RP^3`

A whole discarded component may carry the exact source label `rp3_connected_sum_rp3`. Its required normal form is:

```text
RP3 # RP3
= two nontrivial spherical-space-form summands.
```

This prevents the auxiliary source label from becoming a new terminal prime type.

## 7. Whole-component discard

A discard record requires:

- the removed component identifier;
- an associated factor certificate;
- a reason code;
- source bindings;
- a reconstruction equation containing that factor.

Permitted exact source classes are:

| Schema class | Source-level meaning | Normal form |
|---|---|---|
| `spherical_space_form` | closed manifold admitting constant positive curvature | one spherical factor |
| `s2_bundle_over_s1_orientable` | `S^2 x S^1` | one orientable bundle factor |
| `s2_bundle_over_s1_nonorientable` | twisted `S^2`-bundle | one nonorientable bundle factor |
| `rp3_connected_sum_rp3` | exceptional listed discard type | two `RP^3` spherical factors |

No `unknown`, `canonical`, or visually inferred topology label is accepted.

## 8. Unaffected components

An unaffected active component may retain its identifier across an event. It appears in both `active_before` and `active_after` and requires no reconstruction equation.

A changed component must disappear from `active_after` and occur exactly once as a reconstruction left-hand side.

## 9. Terminal extinction transition

The final event has:

```text
event_type = terminal_extinction_transition
active_after = []
cuts = []
caps = []
ancestry_edges = []
```

Every active pre-component must have a permitted terminal factor certificate and a reconstruction group. This is the topology information that prevents the invalid inference “empty later slice implies arbitrary earlier topology.”

The analytic assertion that the flow is empty for all later times remains `PC02-T016`.

## 10. Source binding

Every event must bind to:

- the internal theorem interface used by the package; and
- at least one pinned external theorem location governing the topology transition.

The canonical anchors are:

- Morgan–Tian Theorem 0.3;
- Morgan–Tian Proposition 15.3;
- Morgan–Tian Corollary 15.4;
- the corresponding Perelman II surgery-topology discussion.

Quotation-level Perelman/Morgan–Tian/Kleiner–Lott alignment remains archival proof debt and may not weaken the transition contract.
