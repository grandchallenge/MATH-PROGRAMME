# CLAIM_LEDGER_STANDARD.md

## Status

Binding canonical claim-ledger contract, version 1.1.0.

## Purpose

The claim ledger is the trust spine of a governed mathematical artifact. Every meaningful assertion must identify what kind of claim it is, what supports it, its present review state, the assumptions under which it is stated, and the exact condition required for promotion.

If a claim is not in the governing ledger, it must not be treated as part of the package's mathematical content.

The prose standard, `schemas/claim_ledger.schema.json`, and `templates/claim_ledger_template.yaml` define one contract. A file called a claim ledger is canonical only when it validates against that schema and is registered for programme validation.

## Ledger envelope

Every canonical ledger is YAML or JSON with exactly these top-level fields:

```yaml
schema_version: 1.1.0
ledger_contract: canonical_claim_ledger
ledger_id: DOMAIN-WP##-CLAIMS
claims: []
```

- `schema_version` identifies the machine contract.
- `ledger_contract` prevents unrelated or legacy YAML from being mistaken for a canonical ledger.
- `ledger_id` is a stable repository identifier.
- `claims` contains one or more canonical claim entries.

Legacy ledgers may remain as historical evidence, but they are not canonical until migrated and registered.

## Claim classes

```text
PROVED_IN_PACKAGE
FORMALIZED
COMPUTED_EXACTLY
ALGEBRAIC_CERTIFIED
GROEBNER_CERTIFIED
INTERVAL_CERTIFIED
SAT_SMT_CERTIFIED
LITERATURE_DERIVED
HEURISTIC
CONJECTURAL
FAILED_ATTEMPT
NEEDS_AUDIT
SUPERSEDED
REFUTED
```

## Support types

```text
HUMAN_PROOF
LEAN_PROOF
COQ_PROOF
ISABELLE_PROOF
EXACT_RATIONAL_COMPUTATION
ALGEBRAIC_CERTIFICATE
GROEBNER_CERTIFICATE
CAS_CERTIFICATE
LEAN_KERNEL_CHECKED_CERTIFICATE
INTERVAL_CERTIFICATE
SAT_SMT_CERTIFICATE
SOURCE_CITATION
NUMERICAL_EVIDENCE
HEURISTIC_ARGUMENT
EXTERNAL_SPECIALIST_PENDING
```

Claim class and support type answer different questions and must not be collapsed.

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

## Certainty values

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

Do not invent compound certainty tokens. Qualification belongs in `support_summary`, `assumptions`, or `promotion_condition`.

## Required claim fields

Every claim entry must contain the following fields, plus the optional `foundational_profile` object when needed:

```yaml
claim_id: UC-WP01-C001
short_name: Frankl statement
claim_text: Every finite nontrivial union-closed family has an element present in at least half its members.
claim_class: LITERATURE_DERIVED
mathematical_domain: finite combinatorics
support_type: SOURCE_CITATION
support_summary: Open conjecture stated from governing sources; no proof is supplied here.
status: OPEN_PROBLEM
certainty: STRONGLY_SUPPORTED
source_or_artifact:
  - DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md
assumptions:
  - finite nontrivial union-closed set family
promotion_condition: A proof or certified reduction covering every finite nontrivial family.
related_files:
  - WP01_UNION_CLOSED_STATUS_SPINE.md
knowledge_graph_refs:
  - UC-CONJECTURE-FRANKL
```

Field meanings:

- `claim_id`: stable unique identifier within the ledger.
- `short_name`: concise human-facing label.
- `claim_text`: complete mathematical or documentary assertion.
- `claim_class`: epistemic class from the controlled vocabulary.
- `mathematical_domain`: concise subject domain, not a proof claim.
- `support_type`: mechanism carrying the current support.
- `support_summary`: what the support establishes and what it does not.
- `status`: current review or claim state.
- `certainty`: controlled confidence label.
- `source_or_artifact`: nonempty list of governing sources, files, proofs, certificates, or replay artifacts.
- `assumptions`: explicit assumptions; use an empty list only when none are required.
- `promotion_condition`: concrete action or proof obligation required for stronger status.
- `related_files`: repository files materially connected to the claim; may be empty.
- `knowledge_graph_refs`: provenance and navigation identifiers; may be empty and never supply proof.
- `foundational_profile`: optional structured foundational metadata governed by its own schema.

## Promotion conditions

Every claim must state an executable or mathematically precise promotion condition. “More evidence,” “further work,” and similar indefinite language are insufficient.

Examples include formalizing a lemma, auditing a primary theorem, replaying an exact certificate, replacing floating-point evidence with interval certification, obtaining specialist review, proving a missing inequality, or constructing a counterexample.

## Ledger formats and registration

The canonical ledger format is YAML. JSON is permitted for generated tooling when it validates against the same schema. Markdown tables are summaries only.

Canonical ledgers must be explicitly registered in the programme validator. CI also discovers every schema-valid canonical ledger under governed repository roots and rejects:

- a discovered canonical ledger absent from the registry;
- a registered ledger absent from the repository;
- duplicate ledger paths or ledger IDs;
- a malformed registered ledger;
- unresolved knowledge-graph references where the programme graph governs them.

This two-way check prevents both silent omission and accidental authority by filename alone.

## Anti-hallucination rule

A citation cannot promote a claim beyond the cited source. A computation cannot promote a theorem beyond the domain it exhausts. A proof sketch cannot promote a claim to certification. A formal statement containing an admitted placeholder is not a proof. Repository merge, CI success, publication, and documentary presentation are not additional mathematical support types.
