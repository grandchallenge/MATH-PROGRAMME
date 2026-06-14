# External Corpus Intake Standard

<p class="page-deck">External corpora can feed MATHFORGE, but they may not govern the programme. This standard defines what must be preserved, what must be audited, and what must never be promoted merely because a dataset field says so.</p>

## Scope

This standard applies to ResearchMath-like sources:

- benchmark datasets;
- problem collections;
- extracted problem corpora;
- theorem-mining datasets;
- generated reasoning traces;
- scraped status evidence;
- literature-derived metadata packs.

The standard does not distrust such corpora. It prevents them from becoming authorities accidentally.

## Intake principle

```text
External corpus
  -> preserved source object
  -> reliability register
  -> audited problem card
  -> route classification
  -> Work Package seed
```

No external corpus row may skip the audit layer.

## Required source fields

Every imported row must preserve:

| Field | Purpose |
| --- | --- |
| corpus name and version | identifies the source object |
| license | determines allowed downstream use |
| split or subset | makes the row reproducible |
| row identifier | enables round-trip auditing |
| original statement | preserves source wording |
| normalized statement | enables mathematical processing |
| source link | grounds provenance |
| taxonomy | assists route classification |
| imported status | records the corpus claim |
| evidence links | permits independent review |
| extraction timestamp or commit | fixes the intake event |

## Reliability register

A corpus must receive a reliability register before its rows are used for campaign selection.

| Register field | Question |
| --- | --- |
| source authority | Who made the corpus and from what sources? |
| row provenance | Can this row be traced to a human-readable source? |
| license clarity | May we preserve, transform, and publish derived artifacts? |
| status authority | Who claims the problem is open, solved, unknown, or partial? |
| evidence quality | Are status links primary, secondary, generated, or missing? |
| known failure modes | Does the corpus contain hallucinated references, stale statuses, or malformed statements? |
| audit depth | Was the row merely preserved, independently checked, or formally reconstructed? |

## Status policy

Imported status is metadata, not programme status.

| Imported corpus status | MATHFORGE default |
| --- | --- |
| `open` | `STATUS_UNVERIFIED_OPEN` |
| `unknown` | `STATUS_UNVERIFIED_UNKNOWN` |
| `solved` | `STATUS_UNVERIFIED_SOLVED` |
| `partially_solved` | `STATUS_UNVERIFIED_PARTIAL` |
| missing or unclear | `STATUS_UNVERIFIED_MISSING` |

A status may be promoted only after independent source reconstruction.

## Problem-card requirements

A MATHFORGE problem card derived from a corpus row must include:

- the preserved source-row hash;
- original and normalized statements;
- taxonomy and route classification;
- imported status and audited status;
- promotion blockers;
- semantic boundary;
- first executable step;
- excluded inferences;
- proof-debt register or handoff debt;
- source evidence links.

## Excluded inferences

Every corpus-derived problem card must forbid at least one overclaim. Common forbidden inferences include:

- dataset `open_status` proves the problem is currently open;
- normalized problem statement is semantically equivalent to the source without audit;
- finite search proves an infinite statement;
- generated reasoning constitutes a proof;
- taxonomy determines the correct method;
- a source URL is a status certificate;
- a problem-card handoff is a theorem result.

## MATHSOLVE handoff requirements

A corpus-derived MATHSOLVE handoff must include:

1. motivating object;
2. obstruction;
3. theorem spine seed;
4. proof-debt register;
5. first executable step;
6. negative-result protocol;
7. forbidden promotions;
8. explicit statement of what MATHCERT cannot yet certify.

## Acceptance tests

An intake fixture should be rejected if it:

- changes imported status to a stronger programme status;
- omits source links;
- drops license information;
- loses the original statement;
- lacks a source-row hash;
- lacks excluded inferences;
- lacks a first executable step;
- marks a handoff solved;
- claims certification without a certificate;
- removes forbidden promotions.

## Corpus-to-campaign ladder

| Stage | Artifact | Boundary |
| --- | --- | --- |
| preservation | source row | no interpretation |
| audit | reliability register | status still unverified |
| extraction | problem card | no theorem claim |
| classification | route proposal | method not yet justified |
| handoff | Work Package seed | no certification target unless local theorem exists |
| campaign | MATHSOLVE Work Package | support route must be explicit |
| certification | MATHCERT artifact | only the checked local claim crosses the boundary |

## ResearchMath as first instance

`RM-DIO-004` is the first executable instance of this standard. It preserves a ResearchMath row, downgrades imported status to unverified unknown, extracts the Diophantine curve, classifies the route, and hands off a finite exact sanity screen.

The fixture is successful because it refuses to become impressive. It does the smaller necessary thing: it proves that external mathematical corpora can enter the programme without weakening the claim boundary.
