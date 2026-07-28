# OZ-WP00 — Source Acquisition Docket

**Artifact ID:** `OZ-WP00-SOURCE-ACQUISITION-DOCKET`  
**Status:** `OPEN / EXTERNAL SOURCE DELIVERY REQUIRED`  
**Authority:** OZ-WP00 intake contract

## 1. Purpose

This docket converts the remaining source-lock obligation into an exact delivery contract. It does not replace the missing sources and does not infer their identities from screenshots, summaries, repository names, or conversation text.

## 2. Required source bundle

The authoritative delivery must contain this logical structure. Equivalent paths are permitted only when the intake map records the change.

```text
OZ-SOURCE-BUNDLE/
  MANUSCRIPT/
    authoritative-manuscript.*
    statement-index.yaml
  LEAN/
    repository.json
    lean-toolchain
    lake-manifest.json
    theorem-index.yaml
    axiom-report.txt
  CERTIFICATES/
    certificate-index.yaml
    wz/
    gosper/
    other/
  COMPUTATION/
    computation-index.yaml
    environment-lock.*
    code/
    inputs/
    outputs/
  LITERATURE/
    literature-index.yaml
    primary-sources/
  NEGATIVE_RESULTS/
    negative-result-index.yaml
  PROVENANCE/
    authorship-and-generation.yaml
    transformation-log.yaml
    SOURCE_SHA256SUMS
```

## 3. Manuscript intake requirements

The manuscript delivery must identify one exact authoritative version. It must include:

- the complete manuscript or technical note;
- the author-supplied statement index;
- every recurrence and initial condition;
- every harmonic-sum formula and notation convention;
- every congruence, modulus, valuation, localization, prime restriction, and quantifier;
- every theorem, lemma, proposition, corollary, conjecture, computation claim, and novelty claim;
- the relation between the Apéry, Franel, quartic-binomial, and sporadic-sequence sections;
- all superseded statement labels.

The intake must reject a partial screenshot collection as the authoritative source.

## 4. Lean intake requirements

The Lean delivery must bind:

- repository URL;
- exact commit;
- `lean-toolchain`;
- `lake-manifest.json`;
- every relevant `.lean` file;
- theorem declaration names;
- imported axioms;
- `sorry`, `admit`, and placeholder scan results;
- clean build command and result;
- one semantic-correspondence record for each manuscript-to-Lean claim.

A declaration that compiles is not yet evidence that it formalizes the manuscript statement.

## 5. Certificate intake requirements

Each WZ, Gosper, or other certificate must state:

- the exact identity certified;
- the summand and parameter domain;
- boundary terms;
- recurrence operator or telescoping relation;
- certificate generator and version;
- independent verifier and replay command;
- exact input and output hashes.

A generated certificate without an independent replay path remains `UNVERIFIED`.

## 6. Computation intake requirements

Each finite verification must state:

- the exact proposition tested;
- bounded domain;
- prime range and exceptional primes;
- integer, rational, modular, or p-adic arithmetic mode;
- code revision;
- environment lock;
- inputs and outputs;
- replay command;
- negative and failed cases;
- the reason the computation has no unbounded consequence.

## 7. Literature intake requirements

The literature corpus must include primary sources for:

- Apéry-style recurrences and irrationality methods;
- linear forms in odd zeta values;
- known results concerning `zeta(5)`, `zeta(7)`, `zeta(9)`, and `zeta(11)`;
- cellular approximations to `zeta(5)`;
- the fifteen sporadic Apéry-like sequences;
- Lucas, Gessel-Lucas, and supercongruence results;
- formal proof of the irrationality of `zeta(3)` in Lean 4;
- any source claimed to be the nearest prior art for the submitted formulas or congruences.

The initial source-identification ledger is `04_PRIOR_ART_SEED_LEDGER.yaml`. Identification is not theorem-level audit and is not a novelty finding.

## 8. Acceptance conditions

A delivered bundle is admissible only when:

1. every file has a byte length and SHA-256 digest;
2. every internal index resolves;
3. no authoritative item depends only on an unversioned web page;
4. manuscript labels, Lean declarations, certificates, computations, and literature sources can be joined deterministically;
5. all generated material has provenance;
6. negative results are retained;
7. no missing bridge is hidden by a proof-status label.

## 9. Current disposition

The source bundle has not been delivered. The bridge decomposition and prior-art seed ledger now exist, but neither closes the source lock.

```text
OZ-WP00: IN PROGRESS
SOURCE ACQUISITION: OPEN
SOURCE LOCK: INCOMPLETE
NOVELTY REVIEW: NOT AUTHORIZED
OZ-WP01 / OZ-WP02: NOT AUTHORIZED
IRRATIONALITY CLAIMS: NOT SUPPORTED
```
