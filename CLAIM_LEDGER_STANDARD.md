# CLAIM_LEDGER_STANDARD.md

## Purpose

The claim ledger is the trust spine of the programme. Every meaningful assertion must have a claim type, support route, status, source or artifact link, and promotion condition.

If a claim is not in the ledger, it should not be treated as part of the package's mathematical content.

## Claim classes

```text
PROVED_IN_PACKAGE
  A proof is supplied in the Work Package. Not necessarily machine checked.

FORMALIZED
  The claim is checked in Lean/Coq/Isabelle/etc.

COMPUTED_EXACTLY
  The claim follows from exact rational/integer/symbolic computation with replayable code.

INTERVAL_CERTIFIED
  The claim follows from a validated interval arithmetic certificate.

SAT_SMT_CERTIFIED
  The claim follows from a proof-producing SAT/SMT/MILP certificate.

LITERATURE_DERIVED
  The claim is taken from a cited source and not reproved here.

HEURISTIC
  The claim is a plausible guide, analogy, or informal expectation.

CONJECTURAL
  The claim is explicitly proposed but not proved.

FAILED_ATTEMPT
  The claim or route was attempted and failed; the failure is informative.

NEEDS_AUDIT
  The claim may be true but requires specialist or source verification.

SUPERSEDED
  The claim has been replaced by a stronger or corrected claim.

REFUTED
  The claim is false or the proposed route is invalid.
```

## Required fields

Every claim entry must include:

```yaml
claim_id: UC-WP01-C001
short_name: Frankl statement
claim_text: "Every finite nontrivial union-closed family has an element present in at least half its members."
claim_class: LITERATURE_DERIVED
mathematical_domain: finite-combinatorics
source_or_artifact:
  - source-url-or-file
support_summary: "Open conjecture stated for orientation; not proved here."
status: OPEN_PROBLEM
certainty: HIGH_FOR_STATEMENT_LOW_FOR_SOLUTION
promotion_condition: "Would require proof or certified reduction to checked cases."
related_files:
  - WP01_UNION_CLOSED_STATUS_SPINE.md
  - WP02_UNION_CLOSED_LEAN_HANDOFF.md
knowledge_graph_refs:
  - UC-CONJECTURE-FRANKL
```

`knowledge_graph_refs` is optional. It carries stable provenance and navigation
links only; it does not supply proof, promote a claim, or change certification
status.

## Claim status values

```text
DRAFT
UNDER_REVIEW
AUDITED
CHECKED
CERTIFIED
OPEN_PROBLEM
PARTIAL
FAILED
REJECTED
SUPERSEDED
```

## Support types

```text
HUMAN_PROOF
LEAN_PROOF
COQ_PROOF
ISABELLE_PROOF
EXACT_RATIONAL_COMPUTATION
INTERVAL_CERTIFICATE
SAT_SMT_CERTIFICATE
SOURCE_CITATION
NUMERICAL_EVIDENCE
HEURISTIC_ARGUMENT
EXTERNAL_SPECIALIST_PENDING
```

## Certainty language

Use precise certainty labels:

```text
CERTIFIED
PROVED_NOT_FORMALIZED
EXACTLY_COMPUTED
STRONGLY_SUPPORTED
PLAUSIBLE
SPECULATIVE
UNKNOWN
FALSE
```

Do not use vague phrases such as “clearly,” “obviously,” “likely solved,” or “essentially proved” unless the ledger explains exactly what they mean.

## Promotion conditions

Every non-certified claim must say what would promote it. Examples:

- formalize lemma in Lean;
- reproduce source theorem and cite primary paper;
- run exact rational certificate verifier;
- replace floating-point computation with interval proof;
- obtain specialist audit;
- prove missing inequality;
- produce counterexample.

## Ledger formats

The canonical ledger format is YAML. JSON is allowed for automated tooling. Markdown tables are allowed only as human-readable summaries.

## Anti-hallucination rule

A citation cannot promote a claim beyond the cited source. A computation cannot promote a theorem beyond the domain it exhausts. A proof sketch cannot promote a claim to certification. A formal statement with `sorry` is not a proof.

## Example ledger entry

```yaml
- claim_id: UC-WP01-C004
  short_name: small-universe sanity check
  claim_text: "The exact enumerator finds no Frankl violations for all union-closed families on universes of size n <= 4."
  claim_class: COMPUTED_EXACTLY
  support_type: EXACT_RATIONAL_COMPUTATION
  source_or_artifact:
    - MATHFORGE/domains/union_closed/enumerate_small_families.py
    - MATHFORGE/domains/union_closed/union_closed_small_audit.json
  status: AUDITED
  promotion_condition: "Lean-check the enumerator logic or verify emitted certificates in MATHCERT."
```
