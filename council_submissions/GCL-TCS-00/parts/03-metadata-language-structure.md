# 10. Mandatory metadata

## 10.1 General rule

Every governed artifact MUST have a machine-readable conformance declaration. Human-readable front matter MAY duplicate the declaration but MUST NOT replace it.

A required field MUST be present even when its value is an empty list or `not_applicable`. Silent omission is not permitted.

## 10.2 Core artifact fields

The declaration MUST contain these fields:

| Field | Requirement |
|---|---|
| `schema_version` | Version of the conformance declaration schema |
| `standard` | Exact GCL-TCS-00 version |
| `artifact_id` | Stable, unique identifier |
| `title` | Canonical artifact title |
| `artifact_type` | Controlled artifact classification |
| `version` | Artifact version |
| `date` | Issue or revision date |
| `owner` | Accountable owner |
| `authority_status` | Candidate, admitted, authoritative, superseded, or withdrawn |
| `promotion_status` | Current lifecycle state |
| `primary_profile` | One profile identifier and version |
| `secondary_profiles` | Zero or more profile identifiers and versions |
| `impact_class` | IC-0 through IC-3 |
| `audience` | Intended reader classes |
| `scope` | What the artifact covers |
| `out_of_scope` | Material exclusions |
| `source_location` | Repository, document system, or canonical location |
| `source_revision` | Commit, immutable version, or content hash |
| `dependencies` | Governed upstream artifacts and external authorities |
| `terminology_registry` | Canonical terminology or explicit not-applicable reason |
| `notation_registry` | Canonical notation or explicit not-applicable reason |
| `claim_register` | Claim ledger location or explicit empty ledger |
| `evidence_register` | Evidence ledger location or explicit empty ledger |
| `review_register` | Review records |
| `exceptions` | Active and historical exception records |
| `conformance_dimensions` | Assessment state for each applicable dimension |
| `supersedes` | Earlier artifacts replaced by this artifact |
| `superseded_by` | Later artifact, when known |
| `licence_and_access` | Use, distribution, and access constraints |
| `generated_content` | Whether machine-generated or machine-assisted content is present and how it was reviewed |

## 10.3 Claim record fields

Each consequential claim MUST have a stable claim record with these fields:

- `claim_id`
- `statement` or an immutable pointer to the statement
- `claim_type`
- `claim_status`
- `scope`
- `assumptions`
- `dependencies`
- `supporting_evidence`
- `counterevidence`
- `falsifiers`
- `limitations`
- `owner`
- `last_reviewed`

Approved claim types are:

- definition
- assumption
- observation
- hypothesis
- conjecture
- lemma
- proposition
- theorem
- empirical_result
- engineering_result
- interpretation
- recommendation
- speculation

Approved claim statuses are:

- proposed
- illustrative
- tested
- replicated
- independently_reproduced
- conditionally_established
- formally_verified
- falsified
- superseded
- withdrawn

A project annex MAY add a status. It MUST define its relation to these statuses.

## 10.4 Evidence record fields

Each evidence record MUST contain:

- `evidence_id`
- `evidence_type`
- `location`
- `version_or_hash`
- `method`
- `result_summary`
- `scope`
- `limitations`
- `created_by`
- `created_at`

Evidence types can include source text, derivation, formal proof, test result, experiment, dataset, plot, benchmark, review finding, or external authority.

## 10.5 Review record fields

Each review record MUST contain:

- `review_id`
- `gate_id`
- `reviewer`
- `review_role`
- `independence_statement`
- `date`
- `decision`
- `findings`
- `required_actions`
- `resolved_actions`
- `evidence`
- `reviewed_revision`

## 10.6 Promotion status values

The machine-readable promotion status MUST be one of:

- `working_draft`
- `registered`
- `review_ready`
- `in_review`
- `verified`
- `promoted`
- `published`
- `superseded`
- `withdrawn`

Display text MAY use a reader-friendly label, but the machine-readable value remains authoritative.

# 11. Minimum language and structure requirements

These requirements apply until GCL-TCS-01 replaces them.

## 11.1 Terms

An artifact MUST use the same term for the same technical object unless it explicitly introduces an alias.

A new technical term MUST be defined before the document depends on it. The definition SHOULD state the term's scope and distinguish it from nearby concepts.

A term MUST NOT silently change meaning between prose, equations, code, figures, and metadata.

## 11.2 Sentences

A sentence SHOULD make one principal assertion. An author SHOULD split a sentence that contains independent claims, hidden conditions, or multiple procedural actions.

Explanatory prose SHOULD normally use no more than 25 words per sentence. This is a diagnostic threshold, not an automatic correctness rule.

The following content is exempt from a mechanical word limit:

- theorem and definition statements;
- equations and symbolic expressions;
- code and command syntax;
- schema fields and identifiers;
- exact quotations;
- legal or source-locked text;
- table cells where splitting would reduce clarity.

## 11.3 Voice and agents

An artifact SHOULD use active voice when the agent is known and relevant.

Passive voice MAY be used when the agent is unknown, irrelevant, intentionally generalized, or less important than the affected object. The construction MUST remain technically correct.

A procedure MUST identify the responsible actor when responsibility is not the reader's.

## 11.4 Paragraphs

A paragraph SHOULD address one topic. It SHOULD start with a sentence that identifies that topic when the topic is not already clear from a heading.

A prose paragraph SHOULD normally contain no more than six sentences. Longer paragraphs require a structural reason.

## 11.5 Lists and procedures

A complex enumeration SHOULD use a vertical list.

A procedural step MUST contain one primary action. It MAY contain a closely coupled result or condition when separation would make the sequence unsafe or ambiguous.

Prerequisites, warnings, expected results, and recovery steps MUST appear before the reader needs them.

## 11.6 Figures, tables, and equations

A figure, table, or equation MUST have enough context to interpret it. The surrounding text MUST state what it shows and why it matters.

A plot MUST identify the quantity, population or sample, aggregation, uncertainty representation, filtering, and exploratory or confirmatory status when these items are applicable.

Alternative text or an equivalent description MUST be available for material visual content in a public artifact.

