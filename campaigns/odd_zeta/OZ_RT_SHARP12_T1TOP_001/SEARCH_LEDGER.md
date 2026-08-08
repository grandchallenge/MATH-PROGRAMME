# OZ-RT-SHARP12-T1TOP-001 — symbolic search ledger

## Locked objective

Prove or refute, uniformly for every integer `n >= 0`, the source-locked identity

`P_n = sum_{0<=k,l<=n} T(n,k,l) * w5_I(n,k,l)`.

The governed source is `790685b7ee4f642a8a88a1bd120636d1b8b39ea8`, tree `646ee73dd9066e059b043fad64fb20959f111cbf`, Sharp-12 blob `6a347e2a483ec781afac98016635ce1d73b3c38e`.

## Existing search evidence

The retained source does not contain a completed unbounded certificate for this target.

1. `work/Z5CF_CERT.md`, blob `a38046e879d1dbb09eb69d85c8be231f827d56e9`, records the closest general weight-5 holonomic attempt. `Annihilator[w5]` timed out after 1800 seconds while resident memory rose only to about 1.12 GB. The source classifies this as `NOT MEASURED`, not as impossibility.
2. The same ledger localizes a principal weight-5 closure wall at the mixed degree-two factor `alpha*Psi`: direct annihilator and `DFiniteTimes` attempts each time-aborted after 1200 seconds. Restricted single-direction and unmixed products can succeed, so the failure is structurally localized rather than a blanket rank or symbol-count obstruction.
3. `work/z5la/t_w5.py`, blob `826bcdbc2de5cb82b6c95eda30396b8b081fee5f`, and `work/z5la/t_w5.log`, blob `72badf10e33596aabb9e70f45ae7806d09e3bae8`, provide modular component checks only at `p=4194301`, `n=5,9`. They do not emit a uniform telescoper, rational certificate functions, or a source-normalized T1-top proof object.
4. `work/Z5CF_TELESCOPER.md`, blob `a634b070d5d95d09749137c26bc51012f318683b`, reports a successful minimal order-7 certificate for the weight-3 companion. This is useful methodology but has no T1-top theorem effect.
5. `work/z5la/t_full.py` and `work/z5la/o_areco.py` operate on `w3` sampled modular systems. They are not the locked T1-top producer.

No source result above proves that a weight-5 certificate does not exist. The governed conclusion is only that an independently replayable T1-top certificate is not present in the admitted source tree.

## Next admissible search

A reopening search should avoid repeating the monolithic weight-5 annihilator call. The preferred deterministic programme is:

1. Encode the exact `w5_I` representative and its full shift-closure basis from the Sharp-12 source, separately from the compact `w5` and `w5_sym` representatives.
2. Seek a recurrence for `S_n = sum T*w5_I` through block-triangular linear algebra over `Q(n,k,l)` or modular images with deterministic rational reconstruction.
3. Use the known hypergeometric rank-one structure of `T` and decompose the harmonic shift module before elimination; do not treat the failed 1800-second monolithic annihilator call as the default architecture.
4. Search bounded recurrence orders and certificate denominator families in increasing canonical order. Every bound must be written to the producer manifest before execution.
5. Any modular search may propose a candidate only. Promotion requires exact rational reconstruction and direct symbolic verification of every certificate identity.
6. Verify all four finite-sum edges and four corners separately; do not infer boundary cancellation from interior rational identities.
7. Compare the resulting recurrence exactly with `L_BZ`, or prove an exact recurrence implication sufficient to identify `S_n=P_n`, including propagation nonvanishing and sufficient exact initial values.
8. Serialize the candidate telescoper, rational certificates, denominator/singularity manifest, boundary witnesses, recurrence comparison, and initial-value witnesses into a deterministic proof object.
9. Verify that object with an implementation that does not invoke the producer's search, solving, rank, or creative-telescoping routines.

## Stop conditions

A bounded search that produces no candidate must record its recurrence-order bound, certificate basis, numerator/denominator degree bounds, primes or exact field used, row counts, resource ceiling, and failure state. Such a result may characterize a searched class but may not refute T1-top.

A candidate that agrees for finitely many `n`, survives modular checks, or reconstructs numerically but lacks direct rational verification remains evidence only.

## Current terminal state

`OPEN_WITH_CHARACTERIZED_BLOCKER`

`proof_effect: NONE`

`promotion_effect: NONE`
