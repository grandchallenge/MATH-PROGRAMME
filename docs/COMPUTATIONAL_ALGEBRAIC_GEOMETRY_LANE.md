# Computational Algebraic Geometry Lane

<div class="programme-kicker">Reusable lane 02</div>

# Route the obligation, not the fashion

Computational algebraic geometry gives the programme several distinct ways to expose structure in polynomial problems. Groebner bases are one route. Resultants, quotient algebras, local standard bases, syzygies, Hilbert data, and sparse polyhedral methods are others.

The governing rule is simple:

> Choose the smallest exact method that matches the mathematical obligation and can emit an auditable witness.

This lane converts a polynomial model into a bounded campaign and a certificate-shaped handoff.

```text
source object or claim
  -> algebraic encoding
  -> structural forecast
  -> method router
  -> bounded exact computation
  -> minimized witness or explicit obstruction
  -> MATHCERT handoff
```

!!! warning "Not a universal solver"
    A polynomial encoding does not make an open problem computationally tractable. General Groebner computation has catastrophic worst-case behavior, resultants can produce enormous matrices, and numerical roots can conceal multiplicity or non-reality. Budget exhaustion is a result about the route, not evidence about the theorem.

## What the lane handles

Use this lane for local obligations involving:

- polynomial identities and ideal membership;
- elimination, projection, and implicitization;
- finite polynomial systems;
- exact real-root questions;
- singularity and multiplicity at a chosen point;
- algebraic dependencies among generators;
- dimension, degree, and graded structure;
- sparse Laurent systems and toric encodings;
- conversion between computationally favorable and explanatory term orders.

Do not use it merely because a problem contains symbols that can be forced into polynomial form. The encoding must preserve the intended mathematical objects under explicit side conditions.

## Pillar contract

<div class="programme-grid programme-grid--three" markdown>

<div class="programme-panel" markdown>
### MATHFORGE

Build and stress-test the encoding. Compare representations and methods. Emit candidate witnesses, forecasts, and failure ledgers.

**May say:** `candidate`, `external_output_only`, `witness_recorded`
</div>

<div class="programme-panel" markdown>
### MATHSOLVE

Select the route, set budgets, define the local theorem obligation, minimize the witness, and prepare independent replay.

**May say:** `route_selected`, `bounded_run_complete`, `ready_for_mathcert`
</div>

<div class="programme-panel" markdown>
### MATHCERT

Replay exact artifacts or formalize the local result. Own the promotion from evidence to theorem.

**May say:** `certified_by_mathcert`
</div>

</div>

## MATHFORGE discovery kit

MATHFORGE should treat algebraic representation as a hypothesis to test, not a neutral transcription.

### Algebraic encoding card

Every run begins with:

```yaml
coefficient_domain: QQ
variables:
  x: source quantity X
  y: source quantity Y
equations: []
inequations: []
auxiliary_variables: []
side_conditions: []
solution_correspondence: ""
known_spurious_components: []
expected_dimension: unknown
```

The card must explain how algebraic solutions map back to source objects. Denominator clearing, projective homogenization, auxiliary inverses, and excluded coordinate hyperplanes must be visible.

### Structural forecast

Before a large run, record:

- variables, equations, and total degrees;
- monomial support sizes;
- expected dimension and finiteness;
- dense Bezout estimate when relevant;
- mixed-volume estimate for sparse Laurent systems;
- anticipated quotient dimension;
- anticipated resultant matrix dimensions;
- likely local versus global character of the question.

A forecast is allowed to be wrong. Its purpose is to make method choice reviewable.

### Representation probes

MATHFORGE may emit:

| Artifact | Question answered |
| --- | --- |
| `TERM_ORDER_SWEEP` | Which leading-term view exposes useful structure without immediate blow-up? |
| `ELIMINATION_MAP` | Which variables can be removed, and what conditions are required to lift back? |
| `MODEL_CLEANING_LEDGER` | Which components or multiplicities belong to the encoding rather than the source problem? |
| `RESULTANT_FEASIBILITY_PROBE` | Is a determinant-style elimination route smaller than a full basis computation? |
| `QUOTIENT_ALGEBRA_MODEL` | Can a finite system be converted into exact linear algebra? |
| `REAL_ROOT_ISOLATION_LEDGER` | Which candidate solutions are provably real and distinct? |
| `LOCAL_SINGULARITY_CARD` | What happens at the selected point or component? |
| `SYZYGY_DEPENDENCY_MAP` | What relations exist among the chosen generators? |
| `HILBERT_PROFILE` | Does the encoding have the expected dimension and degree? |
| `SPARSE_SUPPORT_FORECAST` | Does support geometry give a sharper route than dense degree? |
| `ORDER_CONVERSION_PLAN` | Can an inexpensive basis be converted to the order needed for explanation? |

## MATHSOLVE method router

MATHSOLVE classifies the proof obligation before selecting software or an algorithm.

| Obligation | Preferred first route | Fallback or conversion |
| --- | --- | --- |
| Identity or ideal membership | Exact reduction plus coefficient witness | Small Groebner basis |
| Structured square elimination | Resultant or subresultant | Graded basis followed by conversion |
| General elimination | Favorable graded order | FGLM if zero-dimensional; Groebner walk otherwise |
| Finite-system solving | Quotient algebra and multiplication matrices | Lexicographic triangular form |
| Exact real solutions | Sturm or exact isolation plus lifting | Interval arithmetic with exact endpoints |
| One-point singularity | Local order, Mora normal form, local quotient | Global computation with localization data |
| Generator dependencies | Syzygy module | Direct structural derivation |
| Dimension and degree | Hilbert function or polynomial | Generic slicing or geometric proof |
| Sparse Laurent system | Newton polytopes, mixed volume, sparse resultant | Dense resultant or Groebner route |
| Combinatorial lattice model | Toric ideal | Integer or SAT formulation |

### Why resultants are first-class

For many structured applications, resultants can be more efficient than Groebner elimination. The programme therefore forbids the reflex:

```text
polynomial system -> compute a lex Groebner basis
```

The first comparison should be:

```text
resultant size
vs
quotient-algebra size
vs
graded-basis size plus conversion
vs
sparse support route
```

### Why quotient algebras matter

For a zero-dimensional ideal, the quotient algebra is finite-dimensional. Multiplication by each coordinate becomes an exact matrix. This can expose solution coordinates through characteristic data and eigenstructure without paying for a direct lexicographic computation.

Use:

```text
grevlex or another favorable order
  -> standard monomial basis
  -> multiplication matrices
  -> exact characteristic identities
  -> root extraction or certification
```

### Why local methods matter

A global basis can be the wrong object when the obligation concerns one singularity, one branch, or one point. Local orders and standard bases permit finite calculations in local quotients. Multiplicity and Milnor-style dimensions can turn qualitative degeneracy into a precise invariant.

### Why syzygies matter

Generators do not describe the whole structure. Their relations can expose redundancy, hidden compatibility, and the next theorem obligation. A syzygy matrix is often a better campaign artifact than another large list of equations.

### Why sparse geometry matters

Total degree ignores support. Newton polytopes and mixed volume can predict a much smaller number of isolated torus solutions and point toward sparse resultants or polyhedral homotopy. Coordinate-hyperplane solutions must be audited separately.

## Campaign protocol

Add `ALGEBRAIC_GEOMETRY_CAMPAIGN` as a MATHSOLVE Work Package type.

```text
AG-00  Encoding audit
AG-01  Dimension and support forecast
AG-02  Method comparison
AG-03  Bounded exact run
AG-04  Witness minimization
AG-05  Independent replay
AG-06  MATHCERT handoff
```

### AG-00: encoding audit

Prove or carefully delimit the correspondence between source objects and polynomial solutions. List every field assumption, inequation, chart, and saturation.

### AG-01: structural forecast

Estimate dimension, degree, support, quotient size, and likely matrix dimensions. State what would cause the forecast to fail.

### AG-02: method comparison

Compare at least two viable routes when the obligation is not trivial. Record why the selected route dominates under the declared budget.

### AG-03: bounded exact run

Use exact arithmetic wherever the intended output is exact. Log backend, version, order, runtime, memory, degree growth, intermediate terms, and matrix dimensions.

### AG-04: witness minimization

The final artifact should be smaller and easier to audit than the search that discovered it.

### AG-05: independent replay

Replay with a separate script, backend, exact checker, or proof assistant whenever practical. A repeated transcript from the same opaque computation is not independent replay.

### AG-06: MATHCERT handoff

State the precise local theorem, all assumptions, the witness schema, the checker, and the remaining trust boundary.

## Certificate menu

Prefer certificate-shaped outputs:

```text
ideal membership
  f = a1*g1 + ... + ak*gk

Groebner claim
  every required critical pair reduces to zero

elimination
  eliminant + lifting conditions + factor accounting

resultant
  determinant/subresultant identity + extraneous-factor audit

finite system
  standard monomial basis + exact multiplication matrices

real roots
  rational isolating intervals + sign-variation counts

local multiplicity
  explicit finite basis of the local quotient

syzygy
  relation matrix A with generator row G satisfying G*A = 0

resolution
  explicit matrices, consecutive products zero, exactness evidence

Hilbert data
  graded counts or resolution-derived rational series

sparse system
  support lists + mixed-volume computation + torus-domain audit
```

## Resource ledger

Every run records:

```yaml
coefficient_domain: QQ
variables: 0
equations: 0
expected_dimension: unknown
monomial_order: null
local_order: null
support_sizes: []
max_total_degree: 0
max_intermediate_terms: 0
max_basis_elements: 0
max_matrix_rows: 0
max_matrix_columns: 0
runtime_limit_seconds: 0
memory_limit_mb: 0
backend: ""
backend_version: ""
fallback_route: ""
termination_status: not_started
```

Allowed termination statuses:

- `completed_exact`;
- `completed_candidate_only`;
- `budget_exceeded`;
- `representation_rejected`;
- `route_switched`;
- `backend_failure`;
- `ready_for_mathcert`.

## Stop and switch rules

Change route when:

- direct lexicographic computation exceeds its term or degree budget;
- sparse support predicts a substantially smaller problem than dense degree;
- a resultant matrix is materially smaller than the anticipated basis;
- a zero-dimensional ideal permits FGLM or multiplication-matrix methods;
- the obligation is local but the computation is global;
- approximate roots cannot distinguish reality, multiplicity, or collision;
- the witness is larger than the theorem obligation it supports.

Do not suppress a failed route. It belongs in the campaign ledger because it narrows the next decision.

## Proof boundary

External algebra systems may discover, transform, and compress. They do not certify by default.

A successful run may support:

- a candidate theorem;
- a restricted hypothesis;
- a counterexample lead;
- a finite exact statement;
- a certification request.

It may not support `proved`, `resolved`, or `certified` until the declared proof boundary has been crossed.

## First fixture

The first implementation should use one small zero-dimensional system and force several routes to meet at the same exact answer:

```text
encode
  -> forecast degree and support
  -> compute a favorable graded basis
  -> build multiplication matrices
  -> convert order with FGLM
  -> derive a resultant eliminant
  -> isolate real roots exactly
  -> compare resource ledgers
  -> send the smallest witness to MATHCERT
```

The fixture succeeds only if it demonstrates method selection, artifact discipline, and independent replay. Returning the correct roots is not enough.

## Source basis

This lane is substantially informed by David A. Cox, John Little, and Donal O'Shea, *Using Algebraic Geometry*, second edition. The programme extracts its algorithmic architecture rather than treating the text as authority for any new theorem claim.
