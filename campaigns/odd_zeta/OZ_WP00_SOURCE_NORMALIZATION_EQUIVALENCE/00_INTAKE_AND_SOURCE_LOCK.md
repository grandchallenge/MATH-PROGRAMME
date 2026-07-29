# OZ-WP00 — Intake and Source-Lock Contract

**Artifact ID:** `OZ-WP00-INTAKE-SOURCE-LOCK`  
**Campaign:** Odd zeta values  
**Work Package:** `OZ-WP00`  
**Status:** `OPEN_INTAKE / PROMOTION GATED`  
**Claim class:** `PROVENANCE AND IDENTIFIER CONTROL / NON-SOLUTION ARTIFACT`

## 1. Immediate obligation

Before theorem audit, novelty review, formal correspondence review, or mechanism generation, the programme must acquire and checksum-lock the complete source corpus. It must then assign one permanent identifier to every in-scope object:

| Object class | Stable identifier |
|---|---|
| manuscript statement | `OZ-MSS-S###` |
| recurrence | `OZ-REC-R###` |
| harmonic formula | `OZ-HAR-H###` |
| congruence | `OZ-CON-C###` |
| Lean declaration | `OZ-L4-T###` |
| certificate | `OZ-CER-E###` |
| computation | `OZ-CMP-X###` |
| literature source | `OZ-LIT-B###` |
| missing irrationality bridge | `OZ-BRG-G###` |

The machine-readable authority is `01_INTAKE_SOURCE_LOCK.yaml`.

## 2. Source-lock rule

A source is locked only when the manifest records:

1. its stable source-lock ID;
2. its object class and exact version;
3. a persistent locator or repository path;
4. byte length;
5. SHA-256 digest;
6. acquisition date;
7. exact local anchors for each imported object.

A title, manuscript equation number, Git branch name, or Lean declaration name is not an identity by itself. It is a locator inside a locked source.

Any source change creates a new lock. Existing stable object IDs remain in place and receive a version or supersession edge. IDs are never silently recycled.

## 3. Record boundary

Every mathematical or evidentiary record must separate four questions:

- What is the exact statement?
- What support exists?
- What is the support's scope?
- What remains unproved?

The status vocabulary therefore separates:

- human proof;
- literature derivation;
- Lean formalization;
- exact finite computation;
- conjecture;
- novelty assessment;
- review state.

A Lean theorem is not automatically the manuscript theorem. A semantic-correspondence record must show that the hypotheses, types, quantifiers, normalization, and conclusion agree.

A finite computation is not an unbounded theorem. Its domain, arithmetic mode, inputs, outputs, code revision, environment, and replay command must be explicit.

## 4. Irrationality bridge register

The intake must create a bridge record for every missing implication between the audited identities and any irrationality conclusion. The register must at least test for:

- construction of integer linear forms with exact coefficients;
- proof that coefficient integrality or denominator clearing holds uniformly;
- nonvanishing of the linear forms;
- quantitative decay of the linear forms;
- denominator or height growth control;
- isolation of the target odd zeta value from other periods or zeta values;
- an irrationality criterion whose hypotheses match the constructed sequence;
- an infinite argument not replaced by finite verification.

A recurrence, congruence, or harmonic identity may be correct and still leave all decisive bridges open.

## 5. Novelty rule

The initial novelty state is `NOT_ASSESSED`.

`NEW_AFTER_AUDIT` requires:

1. an explicit audited literature corpus;
2. theorem-level comparison against the nearest sources;
3. normalization and equivalence checks;
4. a documented search boundary;
5. specialist review.

“Not found” and “not recognized” are not novelty findings.

## 6. Validation

Structural validation:

```bash
python3 campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/tools/validate_intake_manifest.py \
  campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/01_INTAKE_SOURCE_LOCK.yaml
```

This command succeeds when the contract is internally well-formed. It does not imply completion.

Completion validation:

```bash
python3 campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/tools/validate_intake_manifest.py \
  --require-complete \
  campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/01_INTAKE_SOURCE_LOCK.yaml
```

This command fails until all governed object classes are populated, every source is locked, no intake item remains unresolved, and `promotion_ready` is true.

## 7. Current disposition

The repository does not yet contain an authoritative OZ manuscript source, pinned Lean corpus, certificate corpus, computation corpus, or audited bibliography under an OZ source lock. The manifest records these as explicit unresolved intake items rather than guessing their identities.

Therefore:

```text
OZ-WP00 status: OPEN INTAKE
Promotion status: GATED
OZ-WP01 / OZ-WP02: NOT AUTHORIZED
Mechanism generation: GATED
New numerical experimentation: GATED
Irrationality claims: NOT SUPPORTED
```

## 8. First executable next step

Acquire the authoritative source corpus. Compute byte lengths and SHA-256 digests. Register the source locks. Then enumerate every manuscript statement, recurrence, harmonic formula, congruence, Lean declaration, certificate, computation, literature source, and missing irrationality bridge under the stable-ID namespaces.
