---
hide:
  - toc
---

# OpenAI Ten Proofs

<p class="page-deck">An independent, protected-main verification of the exact supplied Lean formalizations for all ten advertised results.</p>

<div class="showcase-declaration">
  <span>Public disposition</span>
  <p>Ten of ten source modules rebuilt. Twelve of twelve headline declarations accepted by the Lean kernel.</p>
</div>

<div class="status-register status-register--left" aria-label="OpenAI Ten Proofs verification status">
  <span class="claim-status claim-status--certified">Kernel verified</span>
  <span class="claim-status claim-status--certified">Independently reviewed</span>
  <span class="claim-status claim-status--certified">Protected replay passed</span>
</div>

## The exact subject

| Field | Bound value |
|---|---|
| Repository | [`openai/ten-proofs`](https://github.com/openai/ten-proofs) |
| Commit | `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6` |
| Tree | `174289e4d4958cb0509874e6e53400e098213de7` |
| Lean | `4.32.0` |
| mathlib | `81a5d257c8e410db227a6665ed08f64fea08e997` |
| MATHCERT protected merge | `2aeb5875532152310331662e18327cf9dc3c736e` |

## Ten advertised results

| # | Result | Lean module | Disposition |
|---:|---|---|---|
| 1 | High-dimensional sphere packing | `SpherePacking` | Kernel verified |
| 2 | Binary and spherical codes | `MetricCodes` | Kernel verified |
| 3 | Non-sofic groups | `NonSoficGroup` | Kernel verified |
| 4 | Connes rigidity counterexample | `ConnesRigidity` | Kernel verified |
| 5 | Permanent circuit and formula lower bounds | `Permanent` | Kernel verified |
| 6 | Quantum parallel repetition | `QuantumParallelRepetition` | Kernel verified |
| 7 | Closest-vector and decoding hardness | `GapCVP` | Kernel verified |
| 8 | Sharp Ehrhart volume inequality | `EhrhartVolumeInequality` | Kernel verified |
| 9 | Multicolor triangle Ramsey numbers | `MulticolorTriangleRamsey` | Kernel verified |
| 10 | Extremal graph counterexamples | `CompactnessAndDegeneracy` | Kernel verified |

## What “verified” means here

<div class="programme-spine programme-spine--page" aria-label="Corpus verification chain">
  <div class="programme-spine__stage">
    <span class="programme-spine__number">I</span>
    <span class="programme-spine__name">IDENTITY</span>
    <span class="programme-spine__verb">Pin exact source and toolchain</span>
  </div>
  <span class="programme-spine__arrow" aria-hidden="true">→</span>
  <div class="programme-spine__stage">
    <span class="programme-spine__number">II</span>
    <span class="programme-spine__name">KERNEL</span>
    <span class="programme-spine__verb">Build modules and check declarations</span>
  </div>
  <span class="programme-spine__arrow" aria-hidden="true">→</span>
  <div class="programme-spine__stage">
    <span class="programme-spine__number">III</span>
    <span class="programme-spine__name">PROTECT</span>
    <span class="programme-spine__verb">Review, merge, read back, replay</span>
  </div>
</div>

Lean kernel acceptance of each headline declaration checks its complete formal
dependency graph. The axiom audit found only the programme’s permitted standard
axioms: `Classical.choice`, `Quot.sound`, and `propext`.

The final candidate received fresh independent non-author review on its exact
commit before expected-head merge. The complete corpus workflow then passed
again from protected main.

## Evidence you can inspect

| Surface | Record |
|---|---|
| Machine-readable disposition | [Protected corpus verification record](https://github.com/grandchallenge/MATHCERT/blob/main/governance/corpus_verifications/OPENAI-TEN-PROOFS-001.json) |
| Exact integration and review | [MATHCERT pull request #290](https://github.com/grandchallenge/MATHCERT/pull/290) |
| Protected-main replay | [Workflow run 34838818609](https://github.com/grandchallenge/MATHCERT/actions/runs/34838818609) |
| Corrective tracker and closure | [MATHCERT issue #289](https://github.com/grandchallenge/MATHCERT/issues/289) |
| Upstream source tree | [`openai/ten-proofs` at the verified commit](https://github.com/openai/ten-proofs/tree/94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6) |

## The boundary remains visible

> The exact supplied Lean formalizations for all ten advertised results were
> independently rebuilt and accepted by the Lean kernel on their recorded
> headline declarations, under the statement qualifications retained in the
> protected MATHCERT certificates.

This does not assert literal line-by-line identity with the accompanying PDF
exposition. It makes no novelty, priority, authorship, or publication claim.
It grants no authority to unlisted statements or broader paraphrases.

That precision is the point: GCL publishes what crossed the proof boundary—and
keeps everything else on the correct side of it.
