# TROPIC-GROEBNER-001 Fixture Ledger

## Fixture identity

```yaml
fixture_id: TROPIC-GROEBNER-001
route: TROPIC_GROEBNER
stage: Route 01
status: planned_for_replay
source_problem: tropical line with exact initial-form witnesses
coefficient_domain: QQ
valuation: trivial
variables: [x, y]
ideal: <x + y + 1>
```

## Purpose

This fixture proves the minimum programme behaviour for the TROPIC-GROEBNER route:

1. accept a weight only when the weighted initial form is not a monomial;
2. reject a weight when the weighted initial form is a monomial;
3. preserve the exact witness, not merely the tropical drawing;
4. state that sampled weights are not a complete tropical variety computation.

## Source generators

```text
f = x + y + 1
I = <f> in QQ[x, y]
```

The coefficient valuation is trivial, so each nonzero coefficient has valuation `0`. For a monomial `x^a y^b`, the score under weight `(w_x, w_y)` is

```text
w_x a + w_y b.
```

The initial form keeps the terms with minimal score.

## Weight ledger

| Tuple | Weight | Term scores `(x, y, 1)` | Initial form | Monomial witness | Route decision |
| --- | --- | --- | --- | --- | --- |
| `TG001-A` | `(0, 0)` | `(0, 0, 0)` | `x + y + 1` | none | retained |
| `TG001-B` | `(1, 0)` | `(1, 0, 0)` | `y + 1` | none | retained |
| `TG001-C` | `(-1, 0)` | `(-1, 0, 0)` | `x` | `x ∈ in_w(I)` | rejected |
| `TG001-D` | `(1, 2)` | `(1, 2, 0)` | `1` | `1 ∈ in_w(I)` | rejected |

## Expected artifacts

```text
MATHFORGE
  tropical_weight_probe.json
  initial_form_witnesses.json

MATHSOLVE
  route_decision_report.md
  weight_score_ledger.json

MATHCERT
  algebraic certificate JSON records for accepted and rejected weights
  replay script checking initial-form selection and monomial witnesses
```

## Certificate shape

A retained tuple should emit:

```yaml
certificate_kind: tropical_initial_ideal
weight: [0, 0]
initial_generators: [x + y + 1]
contains_monomial: false
route_decision: retained
trusted_boundary: external_certificate_recorded
```

A rejected tuple should emit:

```yaml
certificate_kind: tropical_initial_ideal
weight: [-1, 0]
initial_generators: [x]
contains_monomial: true
monomial_witness: x
route_decision: rejected
trusted_boundary: external_certificate_recorded
```

## Checked claim boundary

The fixture may claim:

```text
For the four sampled weights, the listed initial forms follow from the declared weight convention.
For the two rejected weights, the listed initial ideal contains the displayed monomial.
For the two retained weights, the principal initial generator is not a monomial.
```

The fixture may not claim:

```text
The entire tropical variety has been enumerated.
Any non-sampled cone has been certified.
The original algebraic problem has been solved.
The route is efficient on larger systems.
```

## Promotion target

The next promotion is `script_replayed`: a MATHCERT replay script should parse the sparse polynomial, recompute term scores for each sampled weight, derive the initial form, and check the monomial witness predicate.

A later Lean target may state the same four sampled-weight facts over `MvPolynomial (Fin 2) QQ`; it should not attempt to formalize the full tropical variety in the first pass.
