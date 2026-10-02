# ResearchMath Intake Lane

## Purpose

ResearchMath-14k is useful to MATHFORGE as a sourcing corpus, not as a theorem oracle. Canonical intake now lives in MATHFORGE under `forge/intake/researchmath14k/` and is imported here at an immutable protected commit through `governance/mathforge_external_source_imports.json`. This Programme fixture is a conformance mirror: it demonstrates the source-row, problem-card, and handoff contract but is not the authoritative source reconstruction.

The fixture is deliberately modest:

```text
ResearchMath row
  -> source-row preservation
  -> audited problem card
  -> route classification
  -> MATHSOLVE handoff
```

## Fixture 004

Fixture `RM-DIO-004` ingests the ResearchMath viewer row whose original question asks for all integer pairs satisfying

```text
x^2 - x = y^5 - y.
```

The row is pinned to Hugging Face repository commit `f22d0f28b55e6e777acf82e722d97ae982dff02e`, LFS data object `3f6c96d18925a47ac223555717226c5408cc9c75e07a1e96bddcffde8a06f029`, config `ResearchMath-14k`, split `test`, row `0`. It imports status `unknown`, which remains `STATUS_UNVERIFIED_UNKNOWN`; no independent current-status reconstruction is claimed.

## Artifacts

| Artifact | Role |
| --- | --- |
| `source_row.json` | Preserves the dataset row, provenance, taxonomy, evidence URL, and imported status. |
| `problem_card.json` | Converts the row into a MATHFORGE problem card with canonical algebraic extraction. |
| `mathsolve_handoff.json` | Produces a MATHSOLVE-ready Work Package seed and first executable step. |
| `claim_ledger.json` | Marks only source reconstruction, route classification, and provisional handoff readiness. |

## Canonical extraction

The Diophantine equation is preserved as an integer-points problem over the affine plane curve

```text
x^2 - x - y^5 + y = 0.
```

This is an extraction, not a solution. The polynomial object supports finite screens and route planning; it does not prove complete integer classification.

## First executable MATHSOLVE step

The handoff proposes a finite exact sanity screen:

```text
for y in {-1, 0, 1, 2, 3}:
    compute D = 1 + 4(y^5 - y)
    retain y only when D is a nonnegative square
    lift corresponding x values exactly
```

The output is a finite-screen ledger of small branches. It is not a proof of completeness.

## CI rejection policy

The adversarial suite rejects attempts to:

- change the imported `unknown` status to `solved`;
- remove source provenance;
- falsify artifact hashes;
- allow status promotion;
- alter the extracted polynomial;
- remove the excluded inference;
- mark the handoff solved;
- remove the first executable step;
- certify the provisional handoff;
- remove forbidden promotions.

## Boundary

MATHFORGE may preserve, audit, classify, and hand off. MATHSOLVE may open a Chaidez-style campaign and run exact bounded screens. MATHCERT has no theorem to certify from this fixture.

The value is the intake machinery itself: a noisy research-problem corpus can feed Forge triage without becoming an authority. Programme admission, campaign authority, and certification remain separate transitions.
