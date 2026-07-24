# NS-CI-WP04 — Restricted theorem target scorecard

## Status

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP04`
- Tracker: `MATH-PROGRAMME#61`
- State: `ACTIVE_TARGET_SELECTION_GATE`
- Inputs: Referee-promoted WP01 and WP02 artifacts
- Output: one selected target `NS-CI-R014`, or an explicit no-selection decision

WP04 is the next controlled stage after WP01 and WP02. It admits and ranks restricted theorem targets. It does not authorize broad mechanism generation, broad numerical experimentation, or continuum regularity claims.

WP03, the quantitative concentration observatory, remains closed until WP04 identifies a target for which computation has a precise falsification role.

## Admission contract

Every candidate must provide:

1. domain, forcing, viscosity, initial-data class, solution class, and quantifiers;
2. exact additional hypothesis or restricted regime;
3. theorem conclusion and relationship to

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt;
```

4. Navier–Stokes scaling class of every hypothesis and conclusion;
5. WP01 fixture-clearance record;
6. WP02 theorem interfaces consumed;
7. nearest known theorem and source-audit state;
8. proof-obligation DAG;
9. strongest anticipated counterexample or failure mode;
10. falsification protocol;
11. formalization boundary;
12. proof that the candidate is narrower than the open theorem rather than a restatement of regularity.

## Hard rejection rules

A candidate is rejected before scoring if it:

- triggers an unresolved WP01 fixture;
- assumes `L^4_tL^6_x`, `L^\infty_tH^1_x`, or an equivalent regularity norm without a strictly weaker independently checkable hypothesis;
- hides a scale-breaking constant needed uniformly in a cutoff or mollification parameter;
- silently narrows the Fefferman data class or universal Leray–Hopf quantifier;
- relies on an imported theorem without source and hypothesis normalization;
- is already a classical theorem in the stated regime and offers no distinct bridge or quantitative refinement;
- uses numerical evidence as continuum proof;
- uses a formal interface as proof of its imported analytic fields.

## Candidate families

| ID | Candidate family | Initial state | Primary risk |
|---|---|---|---|
| `NS-CI-R014-A` | scale-summable dyadic frequency-envelope control | audit | criterion may already encode critical regularity |
| `NS-CI-R014-B` | quantitative geometric depletion of vortex stretching | audit | hypothesis may be nonlocal or unverifiable |
| `NS-CI-R014-C` | concentration or sparsity control of high-vorticity regions | audit | supercritical geometry or hidden measure assumptions |
| `NS-CI-R014-D` | flux or commutator compensation for cutoff/mollification losses | audit | failure to close a scale-uniform estimate |
| `NS-CI-R014-E` | compact-support-to-Schwartz extension bridge | audit | solution-map stability may be as hard as the target |
| `NS-CI-R014-F` | exact symmetry or structural class | audit | likely classical or too remote from the full problem |

These are audit families, not novelty claims.

## Council scorecard

Each admissible candidate receives an integer score from 0 to 5 on:

- leverage toward the full theorem;
- non-circularity;
- distance from established results;
- scale compatibility;
- proof tractability;
- formalizability;
- falsifiability;
- relevance to the full data and solution classes;
- information value if the candidate is false;
- governance and execution cost.

The scorecard is not a vote. A high aggregate score cannot override a hard rejection condition or an unresolved semantic conflict.

## Three-pillar execution

### MATHFORGE

Tracker: `grandchallenge/MATHFORGE#18`.

Produce the candidate/prior-art ledger, source states, WP01 fixture map, and a shortlist of at most three candidates.

### MATHSOLVE

Tracker: `grandchallenge/MATHSOLVE#22`.

Normalize the shortlisted theorem statements, build proof-obligation DAGs, test non-circularity, and recommend at most one `NS-CI-R014` target.

### MATHCERT

Tracker: `grandchallenge/MATHCERT#21`.

Audit scaling, mixed-norm algebra, imported-interface visibility, and formalization feasibility. Do not formalize the open universal estimate.

## Acceptance criteria

WP04 completes only when:

- every candidate has a source and prior-art disposition;
- rejected candidates have explicit route-termination records;
- every surviving candidate clears all relevant WP01 fixtures;
- WP02 dependencies and imported hypotheses are exact;
- the scorecard contains rationale rather than bare numbers;
- the Council selects at most one target, or records no selection;
- the Referee approves the selected statement and claim boundary;
- WP03 is either authorized for a precise falsification task or remains closed.

## Current decision

No target is selected at initialization. Candidate generation and prior-art audit are now open. Broad numerical work and theorem promotion remain closed.