# PC-WP02 — Parameter and normalization registry

## Purpose

Ricci flow with surgery is controlled by a hierarchy of scales and tolerances. Statements such as “choose the surgery parameter small” are insufficient: a later parameter is chosen relative to earlier geometric data, and several quantities are stage-dependent. This registry records dependency order rather than pretending that all sources use identical symbols.

## Geometric normalization

### Initial metric

A normalized closed Riemannian `3`-manifold is taken in the standard Hamilton–Perelman sense used by the selected reconstruction: curvature is uniformly bounded at unit scale and unit balls satisfy a fixed lower volume bound. Exact numerical constants are convention-dependent and must be taken from the pinned source statement.

The normalization is achieved by constant rescaling of an arbitrary smooth metric. Rescaling changes the time and curvature scales but not the manifold topology.

### Parabolic rescaling

For `lambda>0`, the Ricci-flow rescaling convention is

```math
\tilde g(s)=\lambda g(t_0+\lambda^{-1}s),
```

when `lambda` denotes a curvature scale. Distances scale by `lambda^(1/2)` and curvature by `lambda^(-1)` under metric multiplication. Every blow-up statement must declare its convention because some sources parameterize by a length scale instead.

## Core quantities

| Symbol | Role | Dependency and boundary |
|---|---|---|
| `epsilon` | accuracy of neck/cap/canonical-neighbourhood approximation | fixed sufficiently small before the surgery induction; not a curvature scale |
| `kappa` | noncollapsing constant | depends on time horizon and prior control in local theorems; represented stagewise in all-time construction |
| `r` | canonical-neighbourhood scale | below this curvature radius, sufficiently high-curvature points have controlled models; stagewise nonincreasing |
| `delta` | quality threshold for a surgery neck | chosen sufficiently small after the preceding accuracy and scale data; stagewise control is nonincreasing |
| `h` | radius of the neck on which surgery is performed | derived from `delta`, `r`, and preceding geometric control; much smaller than the ambient canonical-neighbourhood scale |
| `D` | dimensionless cutoff multiplier | determines a surgery-trigger curvature comparable to `D h^{-2}` under the source convention |
| `rho` | curvature radius / local scale placeholder | must not be confused with the canonical-neighbourhood threshold `r` |
| `Q` or `R` | scalar-curvature threshold | notation differs by source and theorem; always translate to a declared curvature scale |
| `T_i` | stage endpoint | partitions the all-time construction into bounded intervals; exact sequence is a bookkeeping convention |

## Dependency order

The safe abstract order is:

```text
fix dimension and canonical accuracy epsilon
  -> establish pinching and short-time background constants
  -> obtain noncollapsing data kappa on the current stage
  -> choose canonical-neighbourhood scale r
  -> choose delta sufficiently small relative to prior data
  -> derive surgery radius h and cutoff factor D
  -> run until cutoff, perform permitted surgeries, restart
  -> propagate pinching, noncollapsing, and canonical-neighbourhood estimates
  -> repeat on the next stage with nonincreasing control sequences.
```

This diagram is an order constraint, not a claim that every source defines the quantities in precisely this sequence.

## Stagewise controls

The all-time theorem is represented by sequences

```text
K = (kappa_1, kappa_2, ...),
R = (r_1, r_2, ...),
Delta = (delta_1, delta_2, ...),
```

or equivalent time-dependent piecewise-constant/nonincreasing functions. Required semantic properties:

- each stage covers a bounded time interval;
- surgery times are finite in number on each bounded interval;
- later tolerances may depend on all earlier choices;
- `delta_i` cannot be chosen independently of `r_i` and the noncollapsing/canonical-neighbourhood induction;
- no positive lower bound on all surgery radii is asserted without an explicit theorem;
- global finiteness of surgeries follows in the Poincaré lane only after finite extinction is known.

## Canonical-neighbourhood profile

At a point whose scalar curvature exceeds the scale threshold, after rescaling by the local curvature, the relevant spacetime neighbourhood is close to one of the standard models specified by the source theorem, such as:

- an evolving strong neck;
- a cap attached to a neck;
- a positively curved compact component;
- a region controlled by an ancient `kappa`-solution.

The exact list and closeness norms depend on whether the theorem concerns a smooth flow or a surgery flow and on which strengthened version is being invoked.

The ledger therefore prohibits the shorthand

```text
high curvature -> neck
```

without the full alternative list and hypotheses.

## Surgery trigger and restart

A typical surgery step has the following typed inputs:

```text
controlled surgery flow up to time t
pinching and canonical-neighbourhood estimates
maximum curvature reaches the declared cutoff
sufficiently small delta
```

and outputs:

```text
finite collection of delta-necks
cuts at radius h
standard caps inserted
specified components discarded
post-surgery metric satisfying pinching and restart bounds
explicit topology event record.
```

`h` and `D` are outputs of a parameter-selection lemma, not free knobs at the surgery time.

## Extinction parameters

The finite-extinction proof introduces a topological/geometric width or minimal-disk functional. Its evolution inequality is interpreted between surgery times and controlled across surgery times. The exact notation varies, but the logical constants must distinguish:

- a leading negative term forcing decay;
- curvature/time correction terms;
- regularization error when the minimax family is nonsmooth;
- surgery comparison error or monotonicity statement;
- the finite threshold at which positivity of the width becomes impossible.

No scalar ODE may be quoted unless its geometric functional, differentiability sense, and surgery-time behaviour are named.

## Adversarial checks

- `PC-FP-005`: short-time parameters do not imply all-time smooth flow.
- `PC-FP-006`: rescaling parameters describe pointed local limits.
- `PC-FP-007`: `epsilon`, `kappa`, and `r` hypotheses cannot be deleted.
- `PC-FP-008`: surgery parameters do not erase topology events.
- `PC-FP-014`: stagewise local finiteness is not global finiteness.
- `PC-FP-015`: parameter claims must come from corrected source versions.

## Formalization boundary

MATHCERT may encode the dependency partial order and reject illegal parameter configurations before formalizing any geometric existence theorem. Such a validator certifies bookkeeping only. It does not prove that admissible parameters exist or that a Ricci flow satisfies their geometric contracts.
