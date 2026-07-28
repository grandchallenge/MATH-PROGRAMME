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

