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

