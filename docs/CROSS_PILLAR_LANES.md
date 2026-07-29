# Cross-Pillar Lanes

## Why lanes exist

Some kinds of mathematical work recur across domains. A lane is a reusable route through the three pillars: discovery, campaign, certification.

A lane should state:

- what kind of mathematical obligation it handles;
- what MATHFORGE emits;
- what MATHSOLVE decides;
- what MATHCERT checks;
- what status words are allowed before certification.

## Lane 01: algebraic witness to certificate

This lane covers polynomial identities, Groebner-style normal forms, ideal membership, ideal equality, elimination, radical membership, and finite truncations of algebraic systems.

```text
MATHFORGE
  external CAS / exact search / symbolic exploration
  -> algebraic witness JSON

MATHSOLVE
  recognize algebraic subproblem
  -> invoke tactic or request witness
  -> prepare certification handoff

MATHCERT
  replay or Lean-check certificate
  -> promote only checked claims
```

### MATHFORGE responsibility

MATHFORGE may call SageMath, SymPy, Singular, Magma, or custom exact routines. Its artifact is a candidate witness with provenance, not a proof.

Allowed pre-certification statuses:

- `external_output_only`;
- `external_witness_recorded`;
- `script_replayed`;
- `ready_for_mathcert`.

### MATHSOLVE responsibility

MATHSOLVE decides whether the local proof obligation is genuinely algebraic and whether a Groebner-style tactic is appropriate.

Allowed tactical statuses:

- `candidate`;
- `witness_requested`;
- `witness_available`;
- `sent_to_mathcert`;
- `rejected`.

Only after MATHCERT accepts the artifact may the status become `certified_by_mathcert`.

### MATHCERT responsibility

MATHCERT owns the proof boundary. It may accept:

- a checked Lean theorem;
- an independently replayed exact certificate;
- a formalized reduction plus exact replay;
- another explicitly trusted proof-producing route.

External CAS output alone is never certification.

## Lane 02: computational algebraic geometry campaign

Lane 01 governs the final witness. Lane 02 governs the earlier choice of representation and method when several algebraic routes are possible.

It covers:

- polynomialization and encoding audits;
- elimination and resultants;
- zero-dimensional quotient algebras;
- exact real-root isolation;
- local singularity and multiplicity calculations;
- syzygies, resolutions, and Hilbert data;
- sparse systems, Newton polytopes, and mixed-volume forecasts;
- FGLM and Groebner-walk order conversion.

```text
MATHFORGE
  encode + forecast + compare routes
  -> representation probes and candidate witnesses

MATHSOLVE
  select method + declare budget + minimize witness
  -> bounded campaign and exact handoff

MATHCERT
  replay the smallest explicit artifact
  -> certify only the stated local obligation
```

The full contract is defined in [Computational Algebraic Geometry Lane](COMPUTATIONAL_ALGEBRAIC_GEOMETRY_LANE.md).

The routing rule is:

> Choose the smallest exact method that matches the obligation and can emit an auditable witness.

A polynomial system must not automatically trigger a direct lexicographic Groebner computation. MATHSOLVE compares resultants, quotient-algebra methods, favorable graded orders plus conversion, local methods, and sparse support routes before committing resources.

Allowed campaign statuses:

- `route_selected`;
- `bounded_run_complete`;
- `budget_exceeded`;
- `representation_rejected`;
- `route_switched`;
- `ready_for_mathcert`.

## Lane 03: exact finite enumeration to certificate

Use this lane when the obligation is finite and the complete carrier can be generated exactly. The reusable package fixes the carrier, bound, equivalence relation, generation rule, pruning rule, replay command, completeness scope, and bounded claim boundary.

- Doctrine: [Exact Finite Enumeration](lanes/EXACT_FINITE_ENUMERATION.md)
- Package: `lanes/exact_finite_enumeration`
- Proof boundary: exact bounded completeness, never an unbounded extrapolation.

## Lane 04: interval arithmetic to certified bound

Use this lane for outward-rounded enclosures on explicit domains. The reusable package fixes precision, rounding, backend, subdivision coverage, proof trace, and the exact local inequality implied by the enclosure.

- Doctrine: [Interval Arithmetic](lanes/INTERVAL_ARITHMETIC.md)
- Package: `lanes/interval_arithmetic`
- Proof boundary: the stated enclosure on the stated domain.

## Lane 05: SAT and SMT proof artifact to certificate

Use this lane for bounded Boolean or theory instances with an independently checkable model or proof artifact. The source-to-formula correspondence remains part of the proof obligation.

- Doctrine: [SAT and SMT Proof Artifacts](lanes/SAT_SMT_PROOF_ARTIFACTS.md)
- Package: `lanes/sat_smt_proof`
- Proof boundary: the checked encoded instance and its verified source interpretation.

## Lane 06: Lean formalization handoff

Use this lane to transfer a normalized theorem and assumption ledger into a reproducible Lean target. The reusable package requires pinned source, dependencies, build command, theorem name, source correspondence, and a no-`sorry`, no-local-axiom trust policy.

- Doctrine: [Lean Formalization Handoff](lanes/LEAN_FORMALIZATION_HANDOFF.md)
- Package: `lanes/lean_formalization_handoff`
- Proof boundary: the named compiled declaration under its imported foundations.

## Lane 07: literature synthesis to status spine

Use this lane to turn a dated source search into a source-normalized theorem and status ledger. The reusable package preserves terminology locks, source locators, unresolved conflicts, dependency debt, and a prohibition on unsupported novelty claims.

- Doctrine: [Literature Synthesis to Status Spine](lanes/LITERATURE_SYNTHESIS_STATUS_SPINE.md)
- Package: `lanes/literature_status_spine`
- Proof boundary: source correspondence and bounded status assertions at the stated cutoff.

## Executable package governance

The five reusable packages are registered in `governance/cross_pillar_lane_packages.json`. CI validates:

1. the human doctrine document;
2. the input schema;
3. the output or handoff schema;
4. the toy fixture;
5. allowed statuses;
6. the rejection policy;
7. the promotion route into MATHCERT.

The registry fails closed on missing or orphan packages, malformed schemas, invalid fixtures, status drift, incomplete rejection policies, missing doctrine sections, and toy fixtures that claim certification.

## How to add a new lane

A new lane should include:

1. a human doctrine document;
2. an input schema;
3. an output or handoff schema;
4. a toy fixture;
5. allowed statuses;
6. a rejection policy;
7. a promotion route into MATHCERT.

The first question is not "Can a tool do this?" The first question is "Where is the proof boundary?"
