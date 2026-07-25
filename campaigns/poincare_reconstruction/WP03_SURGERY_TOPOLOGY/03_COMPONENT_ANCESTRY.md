# PC-WP03 — Component ancestry

## 1. Purpose

Ricci flow with surgery changes the set of connected components. A proof that records only the sequence of time-slice diffeomorphism types can lose which post-surgery component came from which pre-surgery component. The ancestry graph prevents this loss.

## 2. Component intervals

A component identifier denotes one connected component over a maximal interval between topology events.

Each component record contains:

- a unique identifier;
- orientation;
- birth endpoint;
- death endpoint.

Birth is either the initial slice or one event. Death is either a surgery/discard event or the finite-extinction time.

## 3. Active-set invariant

Let `A_i^-` and `A_i^+` be the complete active-component sets before and after event `i`.

The history must satisfy:

```math
A_0^- = A_{initial},
```

```math
A_{i+1}^- = A_i^+,
```

and

```math
A_{N-1}^+ = A_{terminal}=\varnothing.
```

Using complete sets, rather than only affected components, makes omissions detectable.

## 4. Forward ancestry is a forest

For each new post-surgery component `D`, there is exactly one pre-surgery parent `C`.

Allowed edges are:

- `separating_child`;
- `nonseparating_child`;
- `unchanged` when an implementation elects to mint a new identifier for an unchanged component.

The committed profile preserves the same identifier for unchanged components, so explicit `unchanged` edges are unnecessary.

Forward surgery does not merge two old components into one new component. An ancestry child with two parents is malformed.

## 5. Branching rules

### Separating cut

```text
       C
      / \
     A   B
```

The parent has two children and the backward equation is `C = A#B`.

### Nonseparating cut

```text
       C
       |
       A        emitted factor H
```

The parent has one child; the lost handle is recorded as the bundle factor `H`.

### Discard

```text
       C        emitted factor F
       x
```

A discarded component has no child. Its factor certificate preserves the information needed for backward reconstruction.

## 6. No silent component loss

For every changed pre-component, exactly one of the following must hold:

1. it is the parent of a separating cut;
2. it is the parent of a nonseparating cut;
3. it has a discard certificate.

If none holds, the component has vanished without a theorem-governed transition and the validator emits `PC03-E009`.

## 7. Acyclicity

Strictly increasing event times orient every ancestry edge forward. Because a component is born no earlier than its parent's death event, directed cycles are impossible in a valid history.

The validator checks the stronger local conditions:

- child is active after the event;
- parent is active before the event;
- each new child has exactly one parent;
- the set of ancestry children equals the set of newly created post-components.

## 8. Component ancestry versus connected-sum ancestry

Component ancestry and factor reconstruction are distinct:

- component ancestry follows surviving geometric pieces forward;
- connected-sum reconstruction restores removed topology backward.

A nonseparating cut has only one component child but two backward summands. The second summand is a factor, not another geometric child.

Conflating these graphs is a common source of missing `S^2 x S^1` factors.

## 9. Locally finite versus finite ancestry

The all-time surgery flow supplies finitely many surgery times on every bounded interval. That does not by itself produce a globally finite forest.

Finite extinction supplies a time `T_ext`. Restricting the locally finite event set to `[0,T_ext]` yields a finite ancestry forest. The schema records these as two separate evidence fields and one derived certificate.

## 10. Terminal roots and leaves

The roots are `initial_active_components`. The forward leaves are either:

- discarded at a surgery transition; or
- removed at the terminal extinction transition.

Every leaf contributes a permitted factor certificate. Backward substitution collects these factor leaves into the connected-sum normal form.
