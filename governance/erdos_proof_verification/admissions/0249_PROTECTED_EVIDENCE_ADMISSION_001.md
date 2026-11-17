# Erdős #249 — bounded formal-result custody 001

**Proposed final status:** `VERIFIED_WITHOUT_CERTIFICATION` for the *auxiliary lacunary totient subseries only*. The original Erdős #249 full-series irrationality question remains **OPEN**. This is a final-custody **candidate**, not a claim that the candidate has been protected-merged. MATHCERT was not invoked.

## Canonical bounded theorem

For Euler's totient function $\varphi$, the precise result is

$$
T=\sum_{m=1}^{\infty}\frac{\varphi(2^m)}{2^{2^m}}
\quad\text{is irrational}.
$$

The exact Lean theorem uses the equivalent zero-based sum over $m+1$ and states that the real sum is not in the range of the natural embedding of rational numbers. The formal source is a complete no-`sorry`, 292-line proof, not a finite simulation.

## Exact protected evidence chain

| Stage | Protected artifact | Identity |
| --- | --- | --- |
| Actual Lean proof and replay | [PR #3446](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3446), merge `62ffaa1db3e2d1a5d120611e86fc189f1c24b50e` | Lean source SHA-256 `6ec552e86902699f26472a3cddb6fdcf79e7dba1abb6ac3c3b486a2bda82cb99` |
| Reproducibility receipt | `governance/erdos_proof_verification/evidence/0249/LACUNARY_LEAN_GREEN_001.receipt.json` | SHA-256 `1ea9b7416febb26115c968a479ec51b5fa13fab7c8e071c4066f81f8ea519e00` |
| Source-critical role pass | [PR #3447](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3447), merge `b9a122c4c8c0db9c83dae8a3f3be4e0b017d0188` | Review MD SHA-256 `8ff6b75a2d4458c9e7bea14203f332f382409a89ae56452cada970d6205b6943`; review JSON `0356652b9d08c3a7e6ba2a741ba931a4acbf86beccd2e872672d911f2d227365` |
| Internal Referee logical pass | Same PR #3447, exact protected SHA | Adjudication MD SHA-256 `13159251dcbe80165b1780f55f022ee3707b89cc31b6bcfe0a6566196502a596`; JSON `7f5f87a55a56347e49d9eb95a42966a502ef200843b14391648e9385c711c0f8` |
| Final evidence custody | This candidate PR | The manifest and machine custody receipt identify this bounded result, with no advance claim that this PR has been merged |

**Actual runtime evidence:** Lean 4.35.0-rc3 binary commit `470d5ce1400764999581fd26d5d72b00d990b0f4`, Mathlib SHA `c55e6e786f49471c72fbddbec5415808896aec1e`, Lake manifest SHA-256 `3b9de3758005c73d884250d11611c935882adf24f02d9a35dc698a033daadde2`. The real Lean process exited 0 on the original local isolated checkout and an exact GitHub source-lock fresh checkout; the stdout SHA-256 matched `038d3d08c883f2c17394c2e39a9eaeaeda5d57970745626390528d360f9c9365`. Stderr was empty; theorem `#check` and `#print axioms` confirmed exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`.

**Logical proof mechanism:** Let $e_m=2^{m+1}-m$. Totient at powers of two rewrites the series as $\sum_m2^{-e_m}$. The exponent gaps grow exactly as $2^{m+1}-1$; finite sums have a dyadic rational numerator, while the positive remaining tail is bounded by an explicit rapidly shrinking geometric estimate. Assuming the sum is rational produces a positive integer strictly less than 1. Every step is now a kernel-checked theorem in the same source.

## What has not been proved

**The original question remains open.** The full expression

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}
$$

contains positive terms not in the lacunary subseries. Knowing that a proper subseries is irrational does **not** logically determine the rationality of the complete series. A deliberately altered Lean goal tried to promote the auxiliary theorem to the full $S$ and produced an expected compiler type mismatch; that negative check is preserved in the packet. The pinned `google-deepmind/formal-conjectures` original statement still contains an unproved `by sorry` goal.

**The review roles are not independent persons.** The same authenticated GCL agent constructed the formal proof and performed logically distinct source-critical and Referee passes. The records explicitly disclose this; they must not be described as independent human assessment. A future public mathematical certification belongs to MATHCERT and was not requested.

**The toolchain is exactly the successful one.** The proof was checked with Lean 4.35.0-rc3 and Mathlib c55e using already compiled but commit-pinned dependency artifacts. A prior bounded 4.33.0 cache acquisition attempt timed out; this does not make the real 4.35 replay unsuccessful, but it must not be represented as a successful 4.33 or clean-room dependency build.

## Documentary continuity and terminal action

For the bounded #249 auxiliary verification, canonical objects, provenance, formal source identity, proof dependency pins, replay logs, adversarial scope checks, Referee record and the lack of mathematical certification are all represented in protected evidence. No known hidden material conflict prevents **internal verification of the bounded T theorem**. The original $S$ remains a substantive mathematical research obligation at parent [#3201](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3201), and any subsequent investigation must not reuse T as a purported solution to S.

This packet should advance `PROTECTED_EVIDENCE_ADMISSION=PASS` and `work_status=VERIFIED_WITHOUT_CERTIFICATION` only if the native protected merge and exact receipt/manifest readback succeed. Keep `literature_status=OPEN`, `certification_status=NOT_SUBMITTED`. After that readback, the bounded evidence issue [#3205](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3205) can close as completed **at auxiliary scope only** and the exact Project #2 Mathematics status be reconciled to Done; parent #3201 remains OPEN for programme-wide coverage and S.

**Classifier:** `ERDOS249_AUXILIARY_T_LEAN_VERIFIED__ORIGINAL_S_OPEN__NO_MATHCERT`.
