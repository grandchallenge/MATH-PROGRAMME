# PC-WP01 — False-proof and semantic-failure atlas

## Status

- Campaign: `PC-001`
- Work Package: `PC-WP01`
- Tracker: `MATH-PROGRAMME#72`
- Input: Referee-reviewed `PC-WP00`
- State: `INTEGRATION_READY`
- Primary role: eliminative audit
- Mathematical result status: the Poincaré theorem remains a solved classical theorem

This package rejects recurring invalid argument patterns in discussions and reconstructions of the Poincaré theorem and the Hamilton–Perelman proof. It does not produce a new proof. Passing every fixture is necessary for a trustworthy reconstruction, but it is not sufficient to establish any imported Ricci-flow theorem.

## Protected theorem spine

```text
PC-D000  category and hypothesis conventions
PC-L001  Top/PL/Diff bridge in dimension three
PC-L004  short-time Ricci flow
PC-L005  entropy, reduced geometry, and non-collapsing
PC-L006  high-curvature limits and canonical neighbourhoods
PC-L007  Ricci flow with surgery
PC-L008  topology of surgery and discarded components
PC-L009  simply connected input enters the extinction class
PC-L010  finite-time extinction
PC-L011  extinction plus surgery history gives connected-sum classification
PC-L012  terminal fundamental-group discharge
PC-C013  smooth Poincaré conclusion
PC-C014  topological Poincaré conclusion
```

## Fixture classes

| Fixture | Invalid substitution | Corrupted node |
|---|---|---|
| `PC-FP-001` | homology sphere for simply connected sphere | `PC-D000`, `PC-L012` |
| `PC-FP-002` | contractible open manifold for Euclidean space | `PC-D000` |
| `PC-FP-003` | compact with boundary for closed | `PC-D000` |
| `PC-FP-004` | category equivalence treated as definitional | `PC-L001` |
| `PC-FP-005` | smooth Ricci flow continued through singularity | `PC-L004`, `PC-L007` |
| `PC-FP-006` | pointed rescaled limit identified with original manifold | `PC-L006` |
| `PC-FP-007` | canonical-neighbourhood conclusion with hypotheses deleted | `PC-L006` |
| `PC-FP-008` | surgery treated as topology-preserving | `PC-L008` |
| `PC-FP-009` | finite extinction treated as topology-free | `PC-L010`, `PC-L011` |
| `PC-FP-010` | orientability and two-sided `RP²` exclusions suppressed | `PC-L007`, `PC-L009` |
| `PC-FP-011` | Poincaré, elliptization, and geometrization identified | `PC-B015`, `PC-B016` |
| `PC-FP-012` | Poincaré imported in the prime-factor discharge | `PC-L009`, `PC-L012` |
| `PC-FP-013` | formal implication interface advertised as analytic proof | `PC-T017` |
| `PC-FP-014` | locally finite surgeries replaced by globally finite surgeries | `PC-L007` |
| `PC-FP-015` | superseded Perelman-I assertions imported without correction | `PC-L005`–`PC-L007` |

## Trust boundary

Fixtures have one of three support forms:

1. an explicit counterexample;
2. a theorem-hypothesis mutation whose conclusion no longer follows;
3. a provenance or formalization boundary violation.

A triggered fixture requires one of:

- route termination;
- statement narrowing;
- restoration of the missing hypothesis;
- a new, independently justified bridge.

Avoiding a fixture does not certify a route. It only removes one known failure.

## Strongest conclusions

WP01 establishes:

- homology, contractibility, compactness, boundary, category, and fundamental-group hypotheses are not interchangeable;
- singularity models are local rescaled limits rather than global identifications;
- surgery and extinction require explicit topology bookkeeping;
- the stronger geometrization and elliptization routes are one-way implications into Poincaré;
- a formal theorem conditional on the Hamilton–Perelman interfaces does not formalize those interfaces;
- source-version corrections are mathematical dependencies, not editorial trivia.

WP01 does **not** establish:

- any Ricci-flow estimate;
- existence of surgery flow;
- finite extinction;
- the connected-sum classification;
- a new proof or formal proof of the Poincaré theorem.

## Integration with PC-WP02

Every theorem interface in `PC-WP02` carries `adversarial_guards` naming the relevant fixture identifiers. In particular:

```text
canonical neighbourhoods -> FP-006, FP-007, FP-015
surgery existence         -> FP-005, FP-008, FP-010, FP-014, FP-015
finite extinction         -> FP-009, FP-012
terminal discharge        -> FP-001, FP-011, FP-012
formalization handoff     -> FP-013
```

## Exit decision

The atlas is complete for the WP00-mandated failure classes and is integration-ready. It remains extensible. `PC-WP03` may open only after this atlas and the WP02 theorem ledger are jointly reviewed, because the surgery-history package must encode both the positive theorem interfaces and the prohibited shortcut transitions.
