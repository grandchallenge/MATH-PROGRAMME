# Erdős #249 — bounded internal Referee adjudication 001

**Decision:** ACCEPT_AUXILIARY_LACUNARY_T_IRRATIONALITY_ONLY — NOT ORIGINAL ERDŐS #249, NOT MATHCERT. The full original question whether $S=\sum_{n\geq1}\varphi(n)/2^n$ is irrational remains **OPEN**. The admitted auxiliary theorem establishes irrationality of the proper lacunary subseries $T=\sum_{m\geq1}\varphi(2^m)/2^{2^m}$.

**Role and independence disclosure:** This distinct logical Referee pass is by the same authenticated GCL operator who authored the new Lean source and conducted the source-critical pass. Internal role-scoped review is permitted by current policy, but this must **not** be represented as external independent mathematics or independent human review. MATHCERT alone can certify public mathematical claims.

## Exact protected subject and reason for acceptance

- Source `experiments/erdos_proof_verification/0249/Erdos249Lacunary.lean`, SHA-256 `6ec552e86902699f26472a3cddb6fdcf79e7dba1abb6ac3c3b486a2bda82cb99`, protected from PR #3446, merge `62ffaa1db3e2d1a5d120611e86fc189f1c24b50e`, 292 lines with a complete proof. The source uses no `sorry` or `admit`.
- Actual pinned v4.35.0-rc3 Lean binary `470d5ce1400764999581fd26d5d72b00d990b0f4`, Mathlib commit `c55e6e786f49471c72fbddbec5415808896aec1e`, project manifest SHA-256 `3b9de3758005c73d884250d11611c935882adf24f02d9a35dc698a033daadde2`.
- Source-locked fresh-checkout replay succeeded with compiler exit 0 and identical complete stdout SHA-256 `038d3d08c883f2c17394c2e39a9eaeaeda5d57970745626390528d360f9c9365`; empty stderr. `#check` printed the exact natural index-shifted totient subseries excluded from the image of rational casting; `#print axioms` gave only `[propext, Classical.choice, Quot.sound]`. A supposed full-series conclusion inserted as a hostile changed-goal produced the required type error (exit 1) without affecting the positive proof.
- Separate mathematical-source adversarial role pass `0249_SOURCE_CRITICAL_REVIEW_001.md` (SHA-256 `334fe2621bca16973ee4a4af8b4be26725ce6753820d223a396aa3860b353887`) explicitly challenged the totient identity, first exponent, eventual gaps, natural subtraction, summability, tail positivity, dyadic numerator, irrational rational-denominator contradiction, and the original full-series non-implication.

## Referee logic and scope

The central proof defines $e_m=2^{m+1}-m$ for natural $m\geq0$; the source proves strict growth and

$$
e_{m+1}-e_m=2^{m+1}-1.
$$

It proves $\varphi(2^{m+1})=2^m$ via imported Mathlib, so the series T is exactly $\sum_{m\geq0}2^{-e_m}$. Each partial sum is $A_N/2^{e_N}$ with integer $A_N$, and the strictly positive tail obeys

$$
0<R_N\leq 2^{1-e_{N+1}}.
$$

If $T=q\in\mathbb Q$ with denominator $b>0$, the proof chooses $N=b+1$ and obtains the positive integer $z=q_{num}2^{e_N}-bA_N=b2^{e_N}R_N$. Exact gap bounds force $z<1$, contradicting integrality. The proof avoids any assumption about unique binary expansions or digit carrying. The zero-based index is exactly reconciled to the source's positive-index sum.

This is a genuine full kernel proof of **T irrational**, not merely a finite numerical verification. The result does not logically settle $S$; neither its present source nor the pinned `google-deepmind/formal-conjectures` research statement provides a theorem of irrationality for the full series.

## Adjudication, governance and documentary boundaries

1. **Mathematical scope:** accept only the auxiliary T result. Retain `literature_status=OPEN` for original #249 and `work_status=IN_PROGRESS` until final protected custody. Never replace the GCL or public claim on S with a statement about T.
2. **Formal source identity:** the proof is checked under the actually replayed Lean 4.35.0-rc3 and Mathlib c55e, not the earlier abortive Lean 4.33 cache attempt. Compiled Mathlib artifacts were reused under pinned SHA; no clean-room rebuild or independent human operator execution is asserted.
3. **Review independence:** source author, adversarial and Referee functions are logically separated but share one authenticated agent. Record the distinct role functions rather than inventing reviewer identities or independent proof derivation. If full external/public certification is later needed, follow MATHCERT.
4. **Open-proof boundary:** the original Formal Conjectures `Erdos249.erdos_249` contains `answer(sorry)` and `by sorry` and addresses $S$, not T. Its status stays OPEN. This is a hard parent-programme evidence exclusion, not a defect in the formal proof of T.
5. **Protected sequence:** this document and accompanying machine decision are a candidate for `ADVERSARIAL_REVIEW=PASS` and `INTERNAL_ADJUDICATION=PASS` **qualified to T**. Do not mark `PROTECTED_EVIDENCE_ADMISSION=PASS`, close #3205, change project status, or claim certification until an additional final protected admission and exact readback.
6. **Residuals:** additional independent rederivation/clean-room dependency replay may be useful for future public certification, not required to claim an actual Lean kernel run with recorded dependencies; proof of original $S$ remains separate open research.

**Adjudicated classification:** `BOUNDED_T_IRRATIONALITY_PROVED_IN_LEAN__S_OPEN__NO_MATHCERT`.
