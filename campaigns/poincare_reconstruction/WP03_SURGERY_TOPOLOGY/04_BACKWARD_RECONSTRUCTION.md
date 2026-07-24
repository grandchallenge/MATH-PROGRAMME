# PC-WP03 — Backward reconstruction theorem

## 1. Abstract history

Let

```text
E_0, E_1, ..., E_{N-1}
```

be a finite ordered source-compliant history. Let `A_i^-` and `A_i^+` be the active component sets before and after `E_i`.

For each changed component `C in A_i^-`, the event supplies one equation

```math
C\cong X_1\#\cdots\#X_k\#F_1\#\cdots\#F_m,
```

where:

- each `X_j` is a distinct new post-event component;
- each `F_j` is a permitted factor emitted at that event;
- unchanged components retain their identifiers;
- every new post-event component occurs in exactly one equation.

The terminal active set is empty.

## 2. Normal-form carrier

Define a factor expression as a finite multiset whose atoms are:

```text
S3
SPHERICAL_SPACE_FORM_NONTRIVIAL
S2_BUNDLE_OVER_S1_ORIENTABLE
S2_BUNDLE_OVER_S1_NONORIENTABLE
```

The source label `RP3#RP3` expands to two nontrivial spherical atoms.

Connected sum corresponds to multiset union, modulo:

- associativity and commutativity up to diffeomorphism;
- deletion of `S3` when another summand is present;
- the convention that a connected sum consisting only of `S3` atoms represents `S3`.

The machine-readable history retains explicit `S3` factors until terminal normalization.

## 3. Backward valuation

For each component identifier `C`, define `V(C)` recursively backward in event time.

At the terminal event, each removed component has a factor certificate, so `V(C)` is its factor normal form.

At a preceding event with equation

```math
C\cong X_1\#\cdots\#X_k\#F_1\#\cdots\#F_m,
```

set

```math
V(C)=V(X_1)\uplus\cdots\uplus V(X_k)
\uplus NF(F_1)\uplus\cdots\uplus NF(F_m),
```

where `uplus` is multiset union and `NF` expands the factor certificate.

## 4. Termination

The recursion terminates because:

1. event times are strictly ordered;
2. each component child is born after its parent;
3. the event list is finite;
4. every forward branch ends in a source-certified discard or terminal removal.

No appeal to manifold classification is needed for termination.

## 5. Reconstruction theorem

**Theorem `PC03-T001`.**  
For every schema-valid finite history, each initial component is diffeomorphic to a connected sum of the permitted factor atoms represented by its backward valuation.

**Proof.**

Proceed by reverse induction on event index.

At the last event, `active_after` is empty. Every active pre-component is source-certified as a permitted terminal factor, so the claim holds.

Assume the claim holds for every post-component of event `E_i`. The event reconstruction contract expresses each changed pre-component as a connected sum of those post-components and emitted factors. Substitute the inductive factor expressions for the post-components. Associativity of connected sum yields a factor expression for the pre-component. Unchanged components retain the already established expression.

Induction reaches the initial active set. ∎

## 6. Finite-history theorem

**Theorem `PC03-T002`.**  
The imported premises

```text
finitely many surgery times on every bounded interval
```

and

```text
empty for all t >= T_ext < infinity
```

imply that the event history used by `PC03-T001` is finite.

**Proof.**

All topology events relevant to reconstruction occur in the bounded interval `[0,T_ext]`. Local finiteness on bounded intervals gives finitely many such events. ∎

The proof does not replace local finiteness by the weaker phrase “the surgery times are discrete.”

## 7. Simply connected orientable discharge

**Theorem `PC03-T003`.**  
Suppose the history has one initial connected orientable component `M`, the backward normal form is valid, and `pi_1(M)=1`. Then the normal form reduces to `S3`, and `M` is diffeomorphic to `S^3`.

**Proof.**

Van Kampen gives the fundamental group of a connected sum as the free product of the factor groups.

- A nontrivial spherical space form has nontrivial finite fundamental group.
- `S^2 x S^1` has fundamental group `Z`.
- The twisted `S^2`-bundle is excluded by orientability.
- `RP^3#RP^3` normalizes to two `RP^3` factors and has group `Z/2 * Z/2`.

A free product is trivial only when every factor group is trivial. Therefore all retained spherical factors have trivial deck group and are `S^3`. Connected sum with `S^3` is neutral, so `M` is diffeomorphic to `S^3`. ∎

## 8. Non-circularity audit

The proof uses no statement of the form:

```text
a simply connected prime 3-manifold is S3.
```

The factor list is supplied independently by the surgery-topology theorem. Simple connectivity is applied only to the explicit factor groups after backward reconstruction.

## 9. Scope boundary

`PC03-T001`–`T003` are conditional on the event contract. They do not prove:

- that the recorded cut sphere is a geometric `delta`-neck;
- that standard caps satisfy the analytic restart estimates;
- that the all-time surgery flow exists;
- that finite extinction occurs.

Those remain the imported interfaces named in every certificate.
