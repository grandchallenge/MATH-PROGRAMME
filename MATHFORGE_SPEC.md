# MATHFORGE_SPEC.md

## Purpose

MATHFORGE is the discovery and exploration pillar of the Grand Challenge mathematical platform. It finds candidate problems, reconstructs their source context, generates examples, performs finite searches, clusters related questions, and produces problem cards suitable for MATHSOLVE intake.

MATHFORGE is deliberately not a certification layer. It may propose. It may speculate. It may search. It may fail. It may produce conjectural structure. It must not promote a conjectural result into a theorem.

## Motto

> MATHFORGE finds the ore.

## Responsibilities

MATHFORGE owns:

1. **Problem intake** from ResearchMath-style datasets, Open Problem Garden, arXiv, survey papers, books, problem lists, seminars, and user-curated programmes.
2. **Source reconstruction**: locate the original source, author, date, problem formulation, and surrounding context.
3. **Status triage**: classify candidate status as open, solved, partially solved, unknown, malformed, duplicate, or stale.
4. **Domain clustering**: group adjacent problems into coherent research neighbourhoods.
5. **Reconnaissance computation**: enumerate small cases, search for examples/counterexamples, build toy models, generate ledgers, and compare bounded exact methods.
6. **Representation search**: test equivalent formulations, polynomial encodings, normal forms, coordinate choices, term orders, sparse supports, and localizations as explicit hypotheses.
7. **Reduction-system reconnaissance**: identify the intended congruence, termination measure, critical overlaps, parametric branches, and provenance needed for replay.
8. **Conjecture mining**: produce candidate patterns, reductions, or formulations for MATHSOLVE to evaluate.
9. **Danger labelling**: flag likely false folklore, unstable source status, extraction errors, representation artifacts, or problems requiring specialist audit.

## Non-responsibilities

MATHFORGE does not:

- certify mathematical truth;
- assert that an open problem is still open without current audit;
- declare a proof complete;
- hide failed searches;
- conflate numerical evidence with proof;
- treat a CAS transcript as a certificate;
- infer confluence from one successful reduction path;
- alter MATHCERT ledgers.

## Inputs

A MATHFORGE domain may ingest:

```text
problem datasets
papers and surveys
known theorem lists
existing code repositories
formal libraries
finite examples
counterexamples
symbolic computations
polynomial and toric encodings
reduction systems and rewrite rules
SAT/SMT encodings
interval search outputs
human notes
```

## Outputs

Every MATHFORGE candidate should emit a problem card:

```yaml
problem_id: MF-UC-0001
title: Frankl union-closed sets conjecture
source_status: open-signal
source_urls:
  - https://en.wikipedia.org/wiki/Union-closed_sets_conjecture
  - https://arxiv.org/abs/2306.12351
domain: finite-combinatorics
forge_outputs:
  - exact enumeration n <= 4
  - equivalent formulation notes
risk_flags:
  - attractive false-proof target
  - many known special cases
recommended_mathsolve_entry: WP01 status spine
recommended_mathcert_route: Lean definitions + finite-family verifier
```

For an algebraic reconnaissance run, MATHFORGE may additionally emit:

```text
ALGEBRAIC_ENCODING_CARD
REDUCTION_SYSTEM_CARD
ADEQUACY_AND_CONFLUENCE_NOTE
TERM_ORDER_SWEEP
ORDER_ROBUSTNESS_REPORT
ELIMINATION_MAP
MODEL_CLEANING_LEDGER
RESULTANT_FEASIBILITY_PROBE
QUOTIENT_ALGEBRA_MODEL
REAL_ROOT_ISOLATION_LEDGER
LOCAL_SINGULARITY_CARD
SYZYGY_DEPENDENCY_MAP
CRITICAL_PAIR_LEDGER
STANDARD_REPRESENTATION_CERTIFICATE
GENERATOR_TRANSFORMATION_CERTIFICATE
WORD_PROBLEM_COMPILATION
PARAMETRIC_BRANCH_LEDGER
HILBERT_PROFILE
SPARSE_SUPPORT_FORECAST
ORDER_CONVERSION_PLAN
TORIC_ENCODING_CARD
TRANSFER_VALIDITY_AUDIT
```

These are discovery artifacts. Each must carry provenance, side conditions, backend details, resource measurements, and a non-certification status.

## Required directory structure

```text
MATHFORGE/
  README.md
  SPEC.md
  forge/
    intake/
      researchmath14k/
      openproblemgarden/
      arxiv/
    domains/
      union_closed/
      erdos_straus/
      hadamard/
      alon_tarsi/
      osp_recoupling/
      lax_pairs/
      billiards/
      convex_symplectic/
    reports/
      problem_cards/
      status_triage/
      reconnaissance/
      algebraic_encodings/
      reduction_systems/
      route_comparisons/
      parametric_branches/
  schemas/
    candidate_problem.schema.json
    forge_run_ledger.schema.json
    algebraic_encoding_card.schema.json
    algebraic_route_probe.schema.json
    reduction_system_card.schema.json
    critical_pair_ledger.schema.json
```

## Quality gates

A MATHFORGE artifact may pass to MATHSOLVE only if it includes:

1. Problem statement in source language or reconstructed form.
2. Source trail with at least one primary or reputable secondary source.
3. Preliminary status classification.
4. Domain classification.
5. Reason for Grand Challenge relevance.
6. Failure-mode notes.
7. Candidate first Work Package.

An algebraic artifact must also state:

1. coefficient domain and exact representation;
2. variables and their source meanings;
3. equations, inequations, and side conditions;
4. solution-correspondence argument or caveat;
5. intended equivalence relation and adequacy statement;
6. term order, reduction strategy, and termination measure;
7. expected dimension or finiteness;
8. resource budget and termination status;
9. provenance route from generated objects to source generators;
10. at least one fallback route when the computation is nontrivial.

## Grand Challenge expectations

A MATHFORGE output should be generous with possibility but severe with status. The right tone is not “we found a solvable problem.” The right tone is “we found a problem neighbourhood whose structure may support disciplined attack.”

For computational algebra, the corresponding tone is not “the system returned zero.” It is “under this encoding, domain, order, reduction contract, and budget, the system produced this candidate witness for independent replay.”

## MATHFORGE-to-MATHSOLVE handoff packet

Each handoff contains:

```text
PROBLEM_CARD.md
SOURCE_MAP.md
STATUS_TRIAGE.md
RECONNAISSANCE_LEDGER.json
FAILURE_RISKS.md
SUGGESTED_WP01.md
CERTIFICATION_ROUTE_SKETCH.md
```

When the computational algebraic geometry lane is used, append:

```text
ALGEBRAIC_ENCODING_CARD.yaml
REDUCTION_SYSTEM_CARD.yaml
STRUCTURAL_FORECAST.json
ROUTE_COMPARISON.md
CANDIDATE_WITNESS.json
GENERATOR_TRANSFORMATIONS.json
RESOURCE_LEDGER.json
FAILED_ROUTES.md
```

When parameters are present, also append:

```text
PARAMETRIC_BRANCH_LEDGER.json
BRANCH_INTERPRETATION.md
```

## Computational algebraic geometry route

The detailed method router is defined in `docs/COMPUTATIONAL_ALGEBRAIC_GEOMETRY_LANE.md`. Its proof-engineering foundation is defined in `docs/REDUCTION_CERTIFICATE_FOUNDATIONS.md`.

MATHFORGE's role is to expose alternatives. A polynomial system must not automatically trigger a direct lexicographic Groebner computation. Compare resultants, quotient-algebra methods, favorable graded orders plus conversion, local methods, and sparse support geometry where applicable.

## First domain: Union-Closed Sets

The first active domain is `union_closed`. MATHFORGE begins with exact enumeration of small universes, source reconstruction, equivalent formulations, known special-case discovery, and candidate Lean-friendly definitions. It must not pretend that small enumeration informs the asymptotic conjecture except as a validation of definitions and tooling.
