# GCL Council review docket: GCL-TCS-00 and GCL-POS-01

## Status

- Docket status: `OPEN_FOR_COUNCIL_REVIEW`
- Submission date: `2026-07-27`
- Submitted artifacts:
  - `GCL-TCS-00`, version `0.1.0`, candidate standard
  - `GCL-POS-01`, version `0.1.0`, candidate position
- Requested decision: approve the candidate framework for governed pilot use and approve the position piece as the bounded institutional statement that accompanies the pilot.
- Decisions not requested:
  - promotion of `GCL-TCS-00` to version `1.0`;
  - a claim that either artifact is formally ASD-STE100 compliant;
  - a claim that conformance establishes mathematical or empirical truth;
  - automatic replacement of existing MATH-PROGRAMME standards before integration review.

## Object

`GCL-TCS-00` defines a programme-wide technical communication hierarchy. It specifies conformance profiles, mandatory metadata, exception rules, review roles, promotion gates, fail-closed conditions, and an adoption sequence for later modules.

`GCL-POS-01` states the institutional position that technical communication is part of the research instrument. It demonstrates the candidate standard through a public-governance conformance package.

## Exact review question

Should MATH-PROGRAMME admit these artifacts as candidate programme governance authority for pilot use, subject to the limits and deferred gates recorded in their conformance files?

The Council can return one of four dispositions:

1. `APPROVE_CANDIDATE_PILOT`
2. `APPROVE_WITH_REQUIRED_CHANGES`
3. `RETURN_FOR_REVISION`
4. `REJECT`

Approval of the candidate pilot does not satisfy the version `1.0` acceptance criteria in `GCL-TCS-00` Section 20.

## Review locations

- Charter source parts: `council_submissions/GCL-TCS-00/parts/`
- Charter source assembler: `council_submissions/GCL-TCS-00/tools/assemble_source.py`
- Charter machine policy: `docs/council/submissions/GCL-TCS-00/GCL-TCS-00.policy.yaml`
- Charter conformance schema: `docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-conformance.schema.json`
- Position source: `council_submissions/GCL-POS-01/GCL-POS-01.md`
- Position conformance and review records: `docs/council/submissions/GCL-POS-01/`
- Submission manifest: `docs/council/submissions/SUBMISSION_MANIFEST.yaml`

The exact source files remain outside `docs/` because they are source-locked review artifacts, not admitted MkDocs pages.

## Relationship to current programme doctrine

The submission is intended to sit above and coordinate, not silently replace, the current operating standards:

- `docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md`
- `docs/PEDAGOGICAL_STYLE_GUIDE.md`
- `docs/ACCESSIBLE_RESEARCH_GUIDE_STANDARD.md`
- `docs/CHAIDEZ_PEDAGOGICAL_PROTOCOL.md`
- `docs/FOUNDATION_AWARE_MATH_PROGRAMME.md`
- `docs/CLAIM_BOUNDARY_DOCTRINE.md`
- `CLASSIFICATION_DISCOVERY_STANDARD.md`
- `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md`
- `CLAIM_LEDGER_STANDARD.md`
- `CERTIFICATION_LADDER.md`

The Council must check for duplicated authority, inconsistent status vocabularies, conflicting promotion gates, and incompatible metadata obligations before approval.

## Claim boundary

Supported by this submission:

- a complete candidate charter and conformance model exists;
- a machine-readable policy and schema accompany the charter;
- a position piece demonstrates the proposed profiles, registers, reviews, manifest, and validation approach;
- both artifacts identify their candidate status and deferred independent review.

Not supported by this submission:

- that the model is optimal;
- that the model reduces error or burden in practice;
- that internal machine-assisted checks are independent Council review;
- that all existing programme artifacts already conform;
- that pilot approval implies final adoption.

## Council review matrix

| Role | Required question | Requested record |
|---|---|---|
| Steward | Is the hierarchy compatible with programme authority and lifecycle rules? | disposition and integration conditions |
| Cartographer | Do the profiles and gates map cleanly onto the current doctrine stack? | dependency and overlap findings |
| Grammarian | Are language requirements exact, usable, and compatible with technical mathematics? | terminology and prose findings |
| Axiomatist | Are normative terms, scope, and non-waivable requirements sufficiently defined? | definition and assumption findings |
| Formalist | Are gate logic, exception logic, and status transitions non-circular? | logical-obligation findings |
| Verifier | Do schemas, policies, manifests, checksums, and validators agree? | replay record and defects |
| Adversary | Can missing records, stale revisions, or persuasive presentation bypass authority controls? | adversarial fixtures and blockers |
| Amanuensis | Are artifact identities, source locks, registries, reviews, and manifests complete and discoverable? | documentary admission finding |
| Referee | What exact authority, downstream use, and revision can be approved? | final promotion decision |

## Required pre-approval checks

- Run `python3 council_submissions/GCL-TCS-00/tools/assemble_source.py`.
- Confirm that the assembled charter has SHA-256 `ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9`.
- Confirm that the position source has SHA-256 `d8be180052a48655a02612b0d6ca883067abe93f0391c4b9c6561a3867ad4d2c`.
- Validate the position conformance declaration against the submitted schema.
- Confirm that the checked revision matches each review record.
- Confirm that the submission does not overwrite current binding doctrine by implication.
- Reconcile terminology with `CLAIM_LEDGER_STANDARD.md`, `CERTIFICATION_LADDER.md`, and `docs/CLAIM_BOUNDARY_DOCTRINE.md`.
- Decide whether candidate approval belongs in the README source-of-truth list or in a separate candidate-governance section.
- Identify the representative pilot artifacts required before version `1.0` review.

## Promotion gate

The pull request must remain draft until:

- repository validation passes;
- Council findings are recorded;
- blocking integration conflicts are resolved;
- an independent Referee states the approved revision and authorized downstream use.

A merge without an explicit disposition admits the files for review only. It does not promote them to binding programme authority.

## First executable step

Assemble and review `GCL-TCS-00`, then test its machine-readable policy against the existing claim, certification, pedagogy, and work-package standards. Record all conflicts before reviewing `GCL-POS-01` for institutional approval.
