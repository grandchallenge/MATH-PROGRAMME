# GCL-TCS-P04 application — TCM-C72-INTERFACE-001

**Pilot:** `GCL-TCS-P04-PILOT-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#819`  
**Subject repository:** `grandchallenge/QUANTUM-TECHNOLOGIES`  
**Subject operation:** `TCM-C72-INTERFACE-001`  
**Protected subject merge:** `aa53dc3c0e99c39f766f4ccb0c0d0629cd9093db`  
**Subject evidence:** `evidence/TCM-C72-INTERFACE-001-report.json`

## Purpose

This is a communication/conformance supplement over a completed computational result. It does not rerun, tune, reconstruct, republish, or alter the C72 experiment. The scientific result and its authority remain in `grandchallenge/QUANTUM-TECHNOLOGIES`; this package asks only whether the existing evidence can be communicated under `GCL-TCS-P04` while preserving its finite scope, negative evidence, execution provenance, and authority boundaries.

## Primary question and alternatives

The frozen scientific question was:

> Can the protected C72 exact TCM class scorer be exposed as a correction-valued syndrome decoder without changing TCM score, class-tie, representative, channel, or correctness semantics?

The frozen outcome space included `C72_TCM_SHARED_DECODER_INTERFACE_CERTIFIED`, `C72_TCM_INTERFACE_SEMANTIC_EQUIVALENCE_FAILED`, `C72_TCM_INTERFACE_CONSTRUCTION_NOT_CERTIFIED`, and `OPERATIONAL_EXECUTION_INCOMPLETE`. The observed adjudication was `C72_TCM_SHARED_DECODER_INTERFACE_CERTIFIED`.

No alternative was deleted after outcome inspection.

## Target observables

For each of three protected algebras over the frozen 329-input C72 corpus:

1. whether every returned object is correction-valued;
2. whether every returned correction is syndrome-consistent;
3. finite oracle success/failure under the frozen correctness oracle `e XOR c is in Row(H_X)`;
4. complete evaluation of all 4096 logical classes per input.

Observed finite counts:

| Algebra | Correction-valued | Syndrome-consistent | Oracle success | Oracle failure |
|---|---:|---:|---:|---:|
| soft tropical base-2 | 329/329 | 329/329 | 167 | 162 |
| sum-product BSC p=0.1 | 329/329 | 329/329 | 166 | 163 |
| min-plus Hamming | 329/329 | 329/329 | 152 | 177 |

These are exact finite counts on the frozen corpus, not population estimates.

## Intervention and controls

The intervention was an interface construction: expose the already-protected exact C72 TCM class scorer as `decode(full_HZ_syndrome, channel_metadata) -> correction | declared_failure` without exposing the injected error to the decoder or changing the protected score, tie-break, representative, channel, or correctness semantics.

The frozen C18 control fixed expected decision digests, success totals, and tie envelopes for all three algebras. Each C72 input had to evaluate all 4096 logical classes. Pruning, approximation, order search, early stopping, post-outcome tuning, and outcome-dependent restriction were prohibited.

## Data and model versions

- C72 corpus size: `329`.
- Corpus SHA-256: `23b49e39eafd70c9619f8837dfcb0046e13a1600cd7176d42a6018814f518050`.
- Corpus order: zero error, 72 unit errors, then 256 frozen SHA-derived BSC errors.
- Source corpus manifest payload SHA-256: `c68830f40733cde6957713060cec35adf317c75572cc960610c07d4d0e24d1e2`.
- Frozen experiment manifest payload SHA-256: `35e3715fa9b1d0d44cad63c8cafbee01a42c3426c7db21c37d3ff68073506ddf`.
- Frozen executable package head: `775586d32756463932e7c2717bdbbe8478186c89`.
- Activation-only execution head: `299e74f762b745986d2c930a875606660065d5af`.

## Seeds and environment

There is no runtime random seed in the C72 execution path. The nontrivial BSC portion of the corpus was already frozen by SHA-derived source data and is bound by the corpus digest above.

The exact hosted execution workflow used `ubuntu-latest`, Python `3.12`, 64 deterministic input-level shards, and `TCM_C72_WORKERS=4` per shard. `actions/checkout` and `actions/setup-python` were SHA-pinned. The worker count and host size were explicitly operational rather than scientific variables.

P04 defect `P04-D001` is retained: `ubuntu-latest` is a mutable runner label, so the durable environment identity is not an immutable runner-image identity. This weakens exact environment reconstruction but does not alter the frozen deterministic integer semantics or the protected finite result. No stronger reproducibility claim is made.

## Stopping and exclusion rules

- Every owned input had to evaluate every logical class; there was no scientific early-stop path.
- Aggregation required every shard.
- Historical compute caps were explicitly not scientific stop rules.
- OOM, timeout, storage failure, or unavailable compute mapped to `OPERATIONAL_EXECUTION_INCOMPLETE`, not to scientific infeasibility.
- No input or algebra was excluded after observing outcomes.

## Metrics, uncertainty, and sensitivity

Primary conformance-preserving metrics are complete correction-valued and syndrome-consistency counts. Secondary metrics are finite oracle success/failure counts by algebra.

There is no sampling uncertainty within the frozen 329-input corpus: the reported counts are exact for that corpus and exact execution path. The result does not estimate generalization uncertainty to C90, other code families, other channels, other corpora, other hardware, or asymptotic regimes. Variation among the three finite oracle-success counts is reported rather than collapsed into a superiority claim.

## Negative and null evidence

Negative outcomes are retained:

- soft tropical base-2: 162 oracle failures;
- sum-product BSC p=0.1: 163 oracle failures;
- min-plus Hamming: 177 oracle failures.

Syndrome-inconsistent outputs were zero for all three algebras, but this finite zero is not generalized beyond the frozen C72 subject. Resource failure was not observed as a scientific outcome and, by contract, could not be relabeled as infeasibility.

## Exact execution path

1. Protected start state: `53e2ac281eb8738e711f75b0d6be525eafab48a3`.
2. Frozen executable package: `775586d32756463932e7c2717bdbbe8478186c89`.
3. Activation-only head: `299e74f762b745986d2c930a875606660065d5af`.
4. Source execution run: `32709539233`; 64/64 shard artifacts bound to the activation head.
5. Frozen aggregate/scoring run: `32797057625`.
6. Aggregate artifact: `9545199159`; digest `sha256:715e4ab49498eca87bded7b2ded7708ba53c8d842aca4886fddebbc583f1ad29`.
7. Canonical aggregate payload: `b6caf79df378ac2a4b78e7bcdd360aa24548492d33e4e82189239372aac75de7`.
8. Canonical scored-row digest: `d2a8f9fa8eb89e5db24d0db9e2cef66ccd91f58488f12f69f8d1767ecc928327`.
9. Durable repository receipt: `evidence/TCM-C72-INTERFACE-001-report.json`.
10. Protected scientific merge: PR #111 → `aa53dc3c0e99c39f766f4ccb0c0d0629cd9093db`, after fresh independent approval.

## Plot provenance and interpretation limits

No plot is part of the protected C72 result package and no conclusion depends on a visual figure. Plot provenance is therefore not applicable to this subject. A later plot could visualize the exact finite counts only if it cited the same frozen corpus and evidence identities and did not convert the three finite comparisons into a population, superiority, threshold, family, or asymptotic claim.

## Claim and authority firewall

This P04 supplement preserves the source boundary exactly:

- finite C72 quality facts may be reported;
- C90 execution is not authorized here;
- no new C90 bound refinement is authorized;
- no approximation, tuning, learned decoding, or autonomous search is authorized;
- no family/asymptotic, threshold/circuit, or hardware-superiority claim is created;
- `QEC-CIRCUIT-003` and `QLDPC-FORGE` remain outside scope;
- GCL-TCS conformance review does not create or enlarge the scientific adjudication.

The durable subject receipt uses top-level status `candidate_executable_not_promoted` while separately recording scientific adjudication `C72_TCM_SHARED_DECODER_INTERFACE_CERTIFIED`. This supplement treats those as different status dimensions rather than silently upgrading artifact authority from the scientific result token.
