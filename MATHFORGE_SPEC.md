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
5. **Reconnaissance computation**: enumerate small cases, search for examples/counterexamples, build toy models, and generate ledgers.
6. **Conjecture mining**: produce candidate patterns, reductions, or formulations for MATHSOLVE to evaluate.
7. **Danger labelling**: flag likely false folklore, unstable source status, extraction errors, or problems requiring specialist audit.

## Non-responsibilities

MATHFORGE does not:

- certify mathematical truth;
- assert that an open problem is still open without current audit;
- declare a proof complete;
- hide failed searches;
- conflate numerical evidence with proof;
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
  schemas/
    candidate_problem.schema.json
    forge_run_ledger.schema.json
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

## Grand Challenge expectations

A MATHFORGE output should be generous with possibility but severe with status. The right tone is not “we found a solvable problem.” The right tone is “we found a problem neighbourhood whose structure may support disciplined attack.”

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

## First domain: Union-Closed Sets

The first active domain is `union_closed`. MATHFORGE begins with exact enumeration of small universes, source reconstruction, equivalent formulations, known special-case discovery, and candidate Lean-friendly definitions. It must not pretend that small enumeration informs the asymptotic conjecture except as a validation of definitions and tooling.
