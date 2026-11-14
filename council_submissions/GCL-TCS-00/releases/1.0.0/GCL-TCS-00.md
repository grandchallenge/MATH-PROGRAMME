---
title: "GCL-TCS-00: Technical Communication Charter and Conformance Model"
subtitle: "Candidate Standard 1.0.0"
author: "Grand Challenge Labs"
date: "2026-09-05"
lang: en-CA
geometry: margin=24mm
fontsize: 10.5pt
header-includes:
  - |
    \usepackage{longtable,booktabs,array}
  - |
    \usepackage{microtype}
  - |
    \usepackage{enumitem}
  - |
    \setlist{nosep}
---

# Document control

| Field | Value |
|---|---|
| Standard identifier | GCL-TCS-00 |
| Title | Technical Communication Charter and Conformance Model |
| Version | 1.0.0 |
| Status | Candidate standard |
| Date | 2026-09-05 |
| Authority | Grand Challenge Labs |
| Language | Canadian English |
| Supersedes | No effective supersession before G9; predecessor GCL-TCS-00@0.1.0 |
| Normative scope | All governed GCL technical communication artifacts |
| Baseline language reference | ASD-STE100 Simplified Technical English, Issue 9, January 2025 |

# 1. Purpose

GCL-TCS-00 defines the governance system for technical communication at Grand Challenge Labs. It establishes the standards hierarchy, conformance profiles, mandatory metadata, exception rules, and promotion gates.

This charter does not replace domain standards. It defines how domain standards are selected, combined, checked, and recorded.

The charter has five purposes:

1. Preserve technical correctness and claim boundaries.
2. Make each important statement traceable to evidence and authority.
3. Make research artifacts reproducible when reproduction is applicable.
4. Keep terminology and notation stable across documents, code, data, and public explanations.
5. Prevent incomplete or unreviewed artifacts from acquiring authority through presentation quality alone.

# 2. Scope

This charter applies to technical artifacts that GCL creates, maintains, reviews, promotes, or publishes. These artifacts include:

- research reports and work packages;
- mathematical statements, proofs, and proof audits;
- experimental protocols, notebooks, datasets, and plots;
- software repositories, APIs, schemas, and implementation notes;
- procedures, runbooks, and safety instructions;
- governance records, claim ledgers, source records, and review records;
- public web editions, explanatory articles, and release notes.

This charter applies to human-authored and machine-assisted content. The use of a language model does not change the required evidence, review, or authority.

Private scratch notes are outside the formal promotion system until a project registers them as governed artifacts. A promoted document must not depend on an unregistered scratch note as its only source of authority.

# 3. Normative language

The following words have special meanings in this standard:

- **MUST** identifies a mandatory requirement.
- **MUST NOT** identifies a prohibition.
- **SHOULD** identifies a strong default. A deviation requires a reason.
- **SHOULD NOT** identifies a practice that normally creates unacceptable risk.
- **MAY** identifies a permitted choice.

A statement marked MUST or MUST NOT is normative. Examples and explanatory notes are informative unless the text states otherwise.

# 4. Governing principles

## 4.1 Correctness before style

A writing rule MUST NOT change the technical meaning of a statement. A shorter sentence is not better when it removes a quantifier, condition, exception, uncertainty, or causal distinction.

When clarity and precision appear to conflict, the author MUST first try a structural solution. The author can use a definition, equation, table, list, diagram, or sequence of short statements. If precision still requires a more complex construction, the author MAY use it and record an exception when the applicable profile requires one.

## 4.2 Claim boundaries before persuasion

A document MUST distinguish established results from hypotheses, interpretations, recommendations, and speculation. Presentation quality MUST NOT raise the status of a claim.

A public explanation MUST preserve the claim status, scope, assumptions, and important limitations of its authoritative source.

## 4.3 Evidence before promotion

A consequential claim MUST link to evidence or to an accepted derivation. The evidence MUST be sufficient for the declared claim type and impact class.

A missing evidence record is not a neutral omission. It is a failed promotion condition.

## 4.4 Reproducibility before authority

An empirical or computational result MUST provide enough information to repeat the relevant procedure. When full reproduction is not possible, the artifact MUST state why and provide the strongest available substitute.

## 4.5 Stable terminology before stylistic variation

A technical object SHOULD have one canonical name in a project. Synonyms MAY appear for teaching or search, but the document MUST identify the canonical term.

Notation, code identifiers, schema fields, and prose terms SHOULD map to one another through a terminology or notation registry.

## 4.6 Explicit uncertainty before apparent completeness

An artifact MUST state material uncertainty, unresolved proof debt, missing controls, unsupported assumptions, and known failure cases.

An artifact MUST NOT use silence to imply that an unresolved question has been settled.

## 4.7 Fail-closed governance

The promotion system MUST fail closed. Missing mandatory metadata, ledgers, reviews, hashes, or exception records MUST block the applicable gate.

A tool MUST NOT infer a promotion state from display text. Machine-readable status fields are authoritative.

# 5. Relationship to Simplified Technical English

ASD-STE100 Issue 9 is the baseline language reference for ordinary technical prose. GCL adopts its central clarity practices, including controlled terminology, short and direct sentences, active voice when the agent is known, stable key terms, topic-bounded paragraphs, and explicit procedural steps.

GCL does not claim that all artifacts are formally ASD-STE100 compliant. Formal STE compliance also depends on its approved dictionary and full rule set.

GCL applies STE principles through profiles:

- The operational profile applies them most strictly.
- The research and public profiles apply them strongly to explanatory prose.
- The mathematical and software profiles permit defined notation, code syntax, formal grammar, identifiers, and logically atomic constructions.
- Exact quotations and source-locked text remain exact.

The detailed controlled-language module will be GCL-TCS-01. Until that module is adopted, this charter supplies the minimum language requirements in Section 11.

# 6. Standards hierarchy

## 6.1 Layers

The GCL technical communication system has six layers.

| Layer | Name | Function |
|---|---|---|
| H0 | External obligations | Applicable law, contract, safety rule, licence, source-locked specification, and authoritative external standard |
| H1 | Charter | GCL-TCS-00 and its governance requirements |
| H2 | Core modules | Cross-cutting standards for language, terminology, claims, evidence, provenance, review, accessibility, and change control |
| H3 | Conformance profiles | Artifact-class requirements for research, mathematics, experiments, software, operations, governance, and public exposition |
| H4 | Project annexes | Project-specific terminology, notation, source locks, schemas, metrics, and approved deviations |
| H5 | Artifact declarations | The exact profile, version, impact class, metadata, exceptions, reviews, and promotion state for one artifact |

Each lower layer specializes the layers above it. A lower layer MUST NOT silently weaken a higher-layer requirement.

## 6.2 Conflict order

The author or reviewer MUST resolve conflicts in this order:

1. Do not make a false, misleading, or technically unsafe statement.
2. Satisfy applicable legal, contractual, safety, security, and licence obligations.
3. Preserve source-locked meaning and exact formal semantics.
4. Apply GCL-TCS-00.
5. Apply the selected core modules and profiles.
6. Apply the project annex.
7. Apply local style preferences.

When these obligations cannot be reconciled, the artifact MUST NOT be promoted. The owner MUST record the conflict and request an authority decision.

## 6.3 Normative and informative content

Each standard and annex MUST identify normative and informative content. Examples, commentary, motivation, and teaching notes SHOULD be informative. Requirements, schemas, enumerations, and gate criteria SHOULD be normative.

## 6.4 Version selection

An artifact declaration MUST identify the exact version of this charter, each selected profile, and each project annex.

A project MUST NOT use an unspecified phrase such as "latest standard" as its only version lock.

## 6.5 Candidate and authoritative records

A candidate source, candidate theorem, candidate dataset, or candidate review is not authoritative because it exists in the repository.

Each governed record MUST have an authority status:

- `candidate`
- `admitted`
- `authoritative`
- `superseded`
- `withdrawn`

Only admitted or authoritative records MAY satisfy a promotion dependency. A project annex can impose a stricter rule.

# 7. Conformance model

## 7.1 Conformance is multidimensional

GCL does not use one averaged conformance score. An artifact conforms only when it passes every mandatory dimension for its declared profile and impact class.

The conformance dimensions are:

| Code | Dimension | Question |
|---|---|---|
| L | Language | Is the prose clear, controlled, and appropriate for the audience? |
| T | Terminology and notation | Are terms, symbols, units, and identifiers defined and stable? |
| S | Structure and accessibility | Can the reader locate, navigate, and interpret the content? |
| C | Claims | Are claim type, scope, assumptions, status, and limitations explicit? |
| E | Evidence | Does each consequential claim link to adequate evidence or derivation? |
| R | Reproducibility | Can a qualified reader repeat the applicable computation or procedure? |
| P | Provenance | Are sources, versions, hashes, transformations, and authority traceable? |
| V | Verification and review | Have the required independent checks occurred? |
| G | Governance | Are metadata, exceptions, gates, lifecycle, and supersession records complete? |

A profile MAY mark a dimension as mandatory, conditional, inherited, or not applicable.

## 7.2 Assessment states

Each mandatory dimension MUST have one of these assessment states:

- `UNASSESSED`: No conformance assertion has been made.
- `DECLARED`: The artifact owner has completed a documented self-assessment.
- `CHECKED`: A reviewer who did not author the relevant content has checked it.
- `ASSURED`: The required promotion gate has accepted the evidence for the declared impact class.
- `FAILED`: The dimension does not conform.
- `EXCEPTED`: An approved, active exception covers a specific requirement. This state does not waive other requirements in the dimension.

An artifact MUST NOT report a dimension as assured without a linked review record.

## 7.3 Overall conformance

Overall conformance is the minimum state across all mandatory dimensions after active exceptions are applied. A high state in one dimension does not compensate for failure in another dimension.

A conformance statement MUST include:

- the primary profile;
- all secondary profiles;
- the impact class;
- the target state;
- the state of each mandatory dimension;
- active exceptions;
- the promotion state;
- the date and standard versions.

## 7.4 Conformance does not establish truth

Conformance shows that the artifact followed the declared process. It does not by itself prove that a theorem is true, an experiment is correct, or a system is safe.

The artifact MUST separately record claim status and verification evidence.

# 8. Impact classes

Impact class determines review independence and gate strength.

| Class | Name | Typical use |
|---|---|---|
| IC-0 | Ephemeral | Private notes and temporary working material with no downstream authority |
| IC-1 | Routine | Internal technical notes, ordinary maintenance documentation, and low-consequence examples |
| IC-2 | Consequential | Research conclusions, public technical claims, reusable software guarantees, benchmark results, and governance decisions |
| IC-3 | Critical | Safety-, security-, legal-, or policy-critical instructions; major commercial claims; and claimed resolutions of open problems |

The owner MUST select the highest applicable class. A project annex MAY raise the class but MUST NOT lower a class that this charter makes mandatory.

Any artifact that claims to solve, disprove, or materially settle a recognized open problem MUST be IC-3.

# 9. Conformance profiles

## 9.1 General profile rules

Each governed artifact MUST declare one primary profile. It MAY declare secondary profiles.

The primary profile controls the artifact's main structure and audience. The complete obligation set is the union of the primary and secondary profile requirements.

When profile requirements conflict, the stricter requirement applies unless it changes technical meaning. A meaning-preserving exception MAY resolve the conflict.

## 9.2 GCL-TCS-P01 - Operational and procedural communication

Use this profile for procedures, runbooks, installation instructions, maintenance instructions, incident response, and safety instructions.

Mandatory emphasis:

- direct imperative steps;
- one main action per numbered step;
- explicit prerequisites and completion conditions;
- warnings before the action that creates the hazard;
- named agents and responsibilities;
- controlled vocabulary and units;
- tested step order;
- rollback or recovery instructions when applicable.

Language requirements are strict. Mathematical notation and code can appear when necessary, but the surrounding procedure MUST remain explicit.

Mandatory dimensions: L, T, S, C, E, P, V, G. Dimension R is mandatory when the procedure can be repeated or tested.

## 9.3 GCL-TCS-P02 - Research communication

Use this profile for research reports, work packages, literature audits, technical memoranda, preprints, and research programme records.

Mandatory emphasis:

- canonical question and scope;
- source and normalization locks;
- explicit assumptions and exclusions;
- claim ledger;
- evidence and counterevidence;
- comparison with alternatives;
- limitations and falsifiers;
- separation of results from interpretation;
- review provenance.

Mandatory dimensions: all dimensions. Dimension R can be marked not applicable only for a fully non-computational artifact with an explicit reason.

## 9.4 GCL-TCS-P03 - Mathematical and formal communication

Use this profile for definitions, conjectures, lemmas, theorems, proofs, proof audits, formal specifications, and proof-assistant interfaces.

Mandatory emphasis:

- ambient objects and domains;
- quantifier order;
- regularity, normalization, sign, and unit conventions;
- dependency and implication structure;
- exact statement versions;
- imported result provenance;
- proof obligations and unresolved proof debt;
- counterexample and boundary-case review;
- formalized and informal boundaries.

Formal notation MAY exceed ordinary language limits. A logically atomic definition or theorem statement SHOULD remain intact when splitting it would obscure scope.

Mandatory dimensions: T, S, C, E, P, V, G. Dimension L is mandatory for explanatory prose. Dimension R is conditional on computation, mechanized proof, or executable checking.

## 9.5 GCL-TCS-P04 - Experimental and computational communication

Use this profile for experiments, simulations, benchmarks, notebooks, computational proofs, data analyses, and visual results.

Mandatory emphasis:

- primary hypothesis and alternatives;
- target observable;
- intervention and controls;
- data and model versions;
- seeds and environment;
- stopping and exclusion rules;
- primary and secondary metrics;
- uncertainty and sensitivity;
- negative and null results;
- exact execution path;
- plot provenance and interpretation limits.

Mandatory dimensions: all dimensions.

## 9.6 GCL-TCS-P05 - Software, API, and notebook communication

Use this profile for repositories, packages, APIs, schemas, command-line tools, notebooks, and implementation documentation.

Mandatory emphasis:

- input and output contracts;
- types, shapes, units, and valid ranges;
- preconditions and postconditions;
- deterministic and nondeterministic behaviour;
- failure and error semantics;
- compatibility and version support;
- security and trust boundaries;
- executable examples;
- tests linked to documented guarantees;
- self-containment for teaching notebooks unless an external dependency is part of the lesson.

Mandatory dimensions: L, T, S, C, E, R, P, V, G.

## 9.7 GCL-TCS-P06 - Public technical exposition

Use this profile for web editions, public summaries, release pages, explanatory articles, and technical announcements.

Mandatory emphasis:

- audience-appropriate explanations;
- preserved claim status and limitations;
- links to authoritative sources;
- no promotion by paraphrase;
- accessible figures and equations;
- clear distinction between analogy and mechanism;
- disclosure of material uncertainty.

This profile MUST inherit claim status from authoritative source artifacts. It MUST NOT create a stronger technical claim than its sources support.

Mandatory dimensions: L, T, S, C, E, P, V, G. Reproducibility MAY be inherited through linked source artifacts.

## 9.8 GCL-TCS-P07 - Governance and documentary records

Use this profile for standards, charters, decision records, manifests, source registries, claim ledgers, terminology registries, and review records.

Mandatory emphasis:

- machine-readable status;
- explicit authority and ownership;
- fail-closed discovery and registration;
- stable identifiers;
- complete supersession links;
- no orphan governed records;
- atomic admission of related artifacts;
- review provenance.

Mandatory dimensions: all dimensions except R. Reproducibility becomes mandatory when a governance process includes executable validation.

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

# 12. Exception model

## 12.1 Types of exception

There are two exception types:

1. **Profile allowance.** A standing rule in a profile identifies content that does not require an artifact-specific exception. Examples include formal notation, code syntax, and exact quotations.
2. **Artifact exception.** A local deviation from a mandatory rule. It requires an exception record and approval.

An author MUST NOT label an unrecorded deviation as an implicit exception.

## 12.2 Acceptable grounds

An artifact exception MAY be approved only when strict application would:

- change technical meaning;
- damage mathematical or formal scope;
- conflict with an external authority;
- reduce safety or operational correctness;
- prevent faithful source quotation;
- break machine syntax or interoperability;
- create a larger accessibility problem than the rule prevents;
- impose a disproportionate burden without reducing material risk.

Convenience, preference, schedule pressure, and rhetorical effect are not sufficient grounds.

## 12.3 Required exception fields

Each artifact exception MUST include:

- `exception_id`
- `rule_id`
- `artifact_scope`
- `affected_content`
- `justification`
- `risk_assessment`
- `compensating_controls`
- `requested_by`
- `approved_by`
- `issued_date`
- `review_date` or `expiry_date`
- `status`

The exception MUST be as narrow as possible.

## 12.4 Non-waivable requirements

No exception can waive these requirements:

- truthful and non-misleading communication;
- explicit claim type, status, and material limitations;
- provenance for consequential evidence;
- disclosure of known safety hazards;
- legal, contractual, security, and licence obligations;
- registration of the exception itself;
- machine-readable promotion and authority status;
- independent review required for IC-2 and IC-3 artifacts;
- fail-closed behaviour for missing mandatory records;
- prohibition against fabricated evidence, reviews, or authority.

## 12.5 Exception lifecycle

An exception begins in `requested` status. It can become `approved`, `rejected`, `expired`, `revoked`, or `superseded`.

An approved exception MUST have a review or expiry date unless the governing profile defines it as permanent. A permanent exception still requires review when the standard or artifact has a major version change.

Promotion MUST fail when a required exception is expired, revoked, or missing.

# 13. Promotion gates

## 13.1 General rules

Promotion changes an artifact's authority. Promotion is not the same as file publication or repository merge.

Each gate decision MUST be one of:

- `PASS`
- `FAIL`
- `DEFERRED`
- `NOT_APPLICABLE`

`NOT_APPLICABLE` requires a reason and reviewer approval. `DEFERRED` does not satisfy a gate.

A gate MUST check the exact revision that is promoted. A material change after review invalidates the affected gate.

## 13.2 G0 - Registration and identity

Purpose: Establish the artifact as a governed object.

Pass conditions:

- stable artifact identifier exists;
- owner exists;
- source location and revision exist;
- candidate or authority status exists;
- the central registry can discover the artifact;
- no identifier collision exists.

Failure examples:

- unregistered claim ledger;
- orphan document;
- review record stored only in a local folder;
- ambiguous candidate and authoritative source records.

Primary reviewer: Amanuensis or registry steward.

## 13.3 G1 - Scope, profile, and authority lock

Purpose: Fix what the artifact claims to do and which rules apply.

Pass conditions:

- primary and secondary profiles are declared;
- impact class is justified;
- scope and out-of-scope items are explicit;
- dependencies and source authorities are locked;
- candidate sources are distinguished from admitted sources;
- exact standard and annex versions are recorded.

Primary reviewers: Owner, Axiomatist for formal work, and Steward.

## 13.4 G2 - Structural and metadata completeness

Purpose: Ensure that required records exist before technical review.

Pass conditions:

- all mandatory metadata fields are present;
- required ledgers and registries are discoverable;
- sections and appendices are navigable;
- figures, tables, equations, and code have identifiers when cited;
- supersession and licence records are complete;
- machine validation passes where a schema exists.

Primary reviewers: Amanuensis and Cartographer.

## 13.5 G3 - Language, terminology, and notation

Purpose: Ensure that the artifact communicates one stable technical meaning.

Pass conditions:

- terms and symbols are defined and used consistently;
- prose meets the selected profile's clarity requirements;
- ambiguous pronouns and hidden agents are removed where material;
- sentence and paragraph complexity is justified;
- units, dimensions, and identifiers are consistent;
- public accessibility requirements are met when applicable.

Primary reviewers: Grammarian and domain terminology reviewer.

## 13.6 G4 - Claim and evidence integrity

Purpose: Ensure that every consequential claim has the correct status and support.

Pass conditions:

- claim ledger is complete;
- each consequential claim has a type and status;
- assumptions, scope, and limitations are explicit;
- supporting evidence and counterevidence are linked;
- evidence supports the exact claim, not a nearby claim;
- public summaries do not inflate source claims;
- unresolved debt is visible.

Primary reviewers: Verifier and claim steward.

## 13.7 G5 - Domain verification

Purpose: Check technical validity using domain-appropriate methods.

Possible checks include:

- proof checking and theorem dependency review;
- source and equivalence audit;
- unit, dimensional, and boundary checks;
- code tests and contract tests;
- statistical review;
- independent calculation;
- safety or security review;
- formal verification.

Pass conditions depend on the profile and impact class. The review record MUST state what was checked and what was not checked.

Primary reviewers: Axiomatist, Formalist, Verifier, software reviewer, statistician, safety reviewer, or another named domain role.

## 13.8 G6 - Adversarial and falsification review

Purpose: Search for ways that the artifact can fail while appearing correct.

Pass conditions:

- plausible counterexamples and boundary cases were tested;
- alternative explanations were considered;
- omitted assumptions and source mismatches were sought;
- misleading visual or rhetorical framing was checked;
- negative evidence and failed tests were recorded;
- the artifact states its falsifiers or failure conditions.

Primary reviewer: Adversary. IC-3 artifacts require a reviewer independent of the authoring team.

## 13.9 G7 - Reproducibility and provenance

Purpose: Verify that evidence and transformations can be traced and repeated.

Pass conditions when applicable:

- data, code, model, environment, seed, and configuration versions are fixed;
- commands or workflows are executable;
- artifacts and outputs have hashes or immutable versions;
- plots trace to source data and code;
- a clean or independent run succeeds, or the limitation is explicitly accepted;
- derived documents trace to authoritative source artifacts;
- no governed file or required record is orphaned.

Primary reviewers: Verifier and Amanuensis.

## 13.10 G8 - Referee promotion decision

Purpose: Decide whether the evidence supports the requested authority.

Pass conditions:

- all mandatory earlier gates pass;
- no unresolved blocking finding remains;
- all active exceptions are valid;
- the referee states what is established and what is not established;
- the authorized downstream uses are explicit;
- the promoted revision is fixed.

Primary reviewer: Referee. The artifact owner MUST NOT be the sole referee for IC-2 or IC-3 artifacts.

## 13.11 G9 - Release and atomic admission

Purpose: Ensure that the promoted artifact and its required records enter the release system together.

Pass conditions:

- artifact manifest is complete;
- required ledgers, source records, assets, schemas, and reviews are included or linked;
- public and private boundaries are enforced;
- static assets and non-code files are covered by orphan detection;
- release identifiers and hashes are final;
- publication does not precede authority admission;
- rollback and supersession paths exist.

Primary reviewers: Release steward and Amanuensis.

# 14. Gate applicability matrix

Legend:

- **M**: mandatory
- **C**: conditional on content or impact class
- **I**: can be inherited from a promoted authoritative source, but inheritance must be checked

| Gate | P01 OPS | P02 RES | P03 MATH | P04 EXP | P05 SW | P06 PUB | P07 GOV |
|---|---:|---:|---:|---:|---:|---:|---:|
| G0 Registration | M | M | M | M | M | M | M |
| G1 Scope/profile lock | M | M | M | M | M | M | M |
| G2 Structure/metadata | M | M | M | M | M | M | M |
| G3 Language/terminology | M | M | M | M | M | M | M |
| G4 Claims/evidence | M | M | M | M | M | M | M |
| G5 Domain verification | M | M | M | M | M | I | M |
| G6 Adversarial review | C | M | M | M | C | M | M |
| G7 Reproducibility/provenance | C | C | C | M | M | I | C |
| G8 Referee decision | M | M | M | M | M | M | M |
| G9 Atomic admission | M | M | M | M | M | M | M |

A conditional gate becomes mandatory when the artifact contains the relevant material. For example, G7 is mandatory for executable experiments, computational proofs, generated plots, and claimed reproducibility.

IC-3 artifacts MUST pass G6 and G7 unless the referee approves a documented `NOT_APPLICABLE` decision that does not weaken a non-waivable requirement.

# 15. Review roles and separation of duties

Roles identify review functions. They do not confer authority without a review record.

| Role | Primary function |
|---|---|
| Owner | Accountable scope, maintenance, and response to findings |
| Steward | Standards selection, impact class, and lifecycle governance |
| Cartographer | Structure, dependency map, navigation, and cross-document integration |
| Grammarian | Controlled language, terminology, notation, and reader clarity |
| Axiomatist | Definitions, assumptions, ambient setting, and source normalization |
| Formalist | Proof structure, formalization boundary, and logical obligations |
| Verifier | Calculations, tests, experiments, implementation, and reproducibility |
| Adversary | Counterexamples, omitted cases, claim inflation, and failure search |
| Amanuensis | Registry, manifests, provenance, terminology records, and review history |
| Referee | Independent final judgment and promotion scope |

One person or agent MAY hold more than one role for IC-0 or IC-1 work. IC-2 and IC-3 artifacts MUST record material role overlap.

For IC-3 artifacts:

- the author MUST NOT be the sole G5 reviewer;
- the authoring team MUST NOT supply the only G6 review;
- the owner MUST NOT be the sole referee;
- the release steward MUST verify the exact promoted revision.

Automated checks MAY satisfy part of a gate. They MUST NOT impersonate an independent human or institutional decision. The review record MUST identify automated and judgment-based checks separately.

# 16. Fail-closed controls

A conforming implementation of this charter MUST block promotion when any of these conditions occurs:

- a required claim ledger is absent or undiscoverable;
- a required review is absent or references another revision;
- an authority status is missing;
- a candidate source is used as authoritative without admission;
- a required exception is absent, expired, or revoked;
- a mandatory metadata field is omitted;
- a public claim has no authoritative source;
- an artifact manifest omits a required governed file;
- a required asset, source record, or static file is orphaned;
- a machine-readable status conflicts with display text;
- a hash or immutable revision does not match the reviewed artifact.

A warning is not sufficient for a fail-closed condition.

# 17. Change control

GCL-TCS-00 uses semantic versioning:

- A major version changes normative meaning or compatibility.
- A minor version adds a backward-compatible requirement, profile, or field.
- A patch version corrects wording, examples, formatting, or an unambiguous defect without changing normative meaning.

Each release MUST include:

- a change log;
- a migration note for changed fields or gate requirements;
- a statement of compatibility;
- the previous and new standard identifiers;
- a review and promotion record.

A project MUST review active exceptions after a major version change.

A superseded standard remains available for provenance. It MUST NOT remain the default for new artifacts unless an approved project annex locks it.

# 18. Adoption sequence

GCL SHOULD adopt the standards family in this order:

1. GCL-TCS-00 - Charter and conformance model.
2. GCL-TCS-01 - Controlled technical language.
3. GCL-TCS-02 - Terminology, notation, and ontology.
4. GCL-TCS-03 - Claims and epistemic status.
5. GCL-TCS-04 - Mathematical exposition and proof records.
6. GCL-TCS-05 - Experimental and computational reporting.
7. GCL-TCS-06 - Software, API, and notebook documentation.
8. GCL-TCS-07 - Artifact, provenance, and manifest integrity.
9. GCL-TCS-08 - Review, promotion, and referee practice.
10. GCL-TCS-09 - Audience and publication profiles.

The detailed modules MUST conform to this charter. A later module can specialize a rule but cannot silently remove a non-waivable requirement.

# 19. Minimum conformance declaration

The following example is informative. The machine-readable templates in this package are normative for version 1.0.0.

```yaml
schema_version: "1.0.0"
standard:
  id: "GCL-TCS-00"
  version: "1.0.0"
artifact_id: "EXAMPLE-ARTIFACT-001"
title: "Example technical artifact"
artifact_type: "research_report"
version: "1.0.0"
date: "2026-09-05"
owner: "Example owner"
authority_status: "candidate"
promotion_status: "registered"
primary_profile:
  id: "GCL-TCS-P02"
  version: "1.0.0"
secondary_profiles: []
impact_class: "IC-2"
audience: ["researcher"]
scope: "The exact subject covered by the artifact."
out_of_scope: ["An explicit exclusion."]
source_location: "repository/path"
source_revision: "immutable-revision-or-hash"
dependencies: []
terminology_registry: "registry/TERMS.yaml"
notation_registry: "registry/NOTATION.yaml"
claim_register: "claims/CLAIMS.yaml"
evidence_register: "evidence/EVIDENCE.yaml"
review_register: []
exceptions: []
conformance_dimensions:
  L: "DECLARED"
  T: "DECLARED"
  S: "DECLARED"
  C: "DECLARED"
  E: "UNASSESSED"
  R: "UNASSESSED"
  P: "DECLARED"
  V: "UNASSESSED"
  G: "DECLARED"
supersedes: []
superseded_by: null
licence_and_access:
  licence: "project-defined"
  access: "internal"
generated_content:
  present: true
  method: "machine-assisted drafting"
  review: "Human technical review required before promotion"
```

# 20. Acceptance criteria for GCL-TCS-00 version 1.0

This candidate can become version 1.0 only when:

1. The policy manifest and conformance schema agree with the normative text.
2. Each profile has an approved owner and review role map.
3. Mandatory fields have machine-readable definitions and validation tests.
4. The exception workflow has fail-closed tests.
5. Gate records bind to immutable artifact revisions.
6. Candidate and authoritative source records are distinct in the schema.
7. Orphan detection covers documents, web pages, source records, candidate records, assets, static text, TeX, JSON, and directories where applicable.
8. At least one mathematical, experimental, software, operational, governance, and public artifact has completed a pilot conformance review.
9. The pilots record false positives, false negatives, burden, and unresolved ambiguities.
10. The Referee approves promotion with an explicit statement of remaining limitations.

# Appendix A - Profile selection guide

Use the following questions:

1. Does the artifact tell a reader how to do something in sequence? Select P01.
2. Does it report or evaluate a research question? Select P02.
3. Does it define or prove mathematical statements? Select P03.
4. Does it depend on data, simulation, computation, or plots? Select P04.
5. Does it define software behaviour, interfaces, or executable notebooks? Select P05.
6. Is it intended primarily for a public audience? Select P06.
7. Does it govern records, authority, review, or lifecycle? Select P07.

Select all applicable profiles. Use the main reader task to choose the primary profile.

# Appendix B - Exception decision test

A reviewer SHOULD reject an exception when any answer is no:

1. Is the exact rule identified?
2. Is the affected content narrow and identifiable?
3. Would strict compliance create a material problem?
4. Does the reason concern correctness, authority, safety, interoperability, accessibility, or disproportionate burden?
5. Are the risks explicit?
6. Are compensating controls adequate?
7. Is the approver authorized and independent enough for the impact class?
8. Is a review or expiry date present?
9. Does the exception preserve all non-waivable requirements?

# Appendix C - Promotion decision statement

A G8 referee decision SHOULD use this structure:

- **Artifact and revision:** Exact identifier and immutable revision.
- **Requested authority:** What promotion permits.
- **Established:** Claims and properties supported by the completed review.
- **Not established:** Claims and properties that remain outside the evidence.
- **Exceptions:** Active exceptions and their effects.
- **Residual risk:** Known uncertainty and unresolved debt.
- **Downstream use:** Authorized and prohibited uses.
- **Decision:** PASS, FAIL, or DEFERRED.

# Appendix D - Reference basis

This charter uses ASD-STE100 Simplified Technical English, Issue 9, as a baseline for ordinary technical prose. Relevant baseline topics include controlled words and technical terms, active voice, clear sentence structure, procedural writing, stable key terms, short descriptive sentences, topic-bounded paragraphs, and limited paragraph length.

GCL adds claim governance, mathematical precision, experimental reporting, software contracts, provenance, exception control, and promotion gates. These additions are necessary because linguistic clarity alone does not establish technical validity or authority.
