# Erdős #560 — Phase D source-to-publication admission review

**Assignment:** `ERDOS-PV-0560-D`. **Actor:** authenticated GCL operator `fyremael`, with a separate logical-role Adversary pass but no distinct external mathematical referee. **Claim:** `refs/heads/gcl-pv-claims/ERDOS-PV-0560-D`, exact SHA `0ac8ec3ce8d59868e1d260f8974fb62c36ab0b85`. **Source issue:** #1831, source body SHA-256 `2bafa6656b0d797f8b7637be2d7ff77e7682e329467a9c858da7e9b7708c1`. **Cohort:** 501–600, Phase D issue #3256. The D record is a **candidate until protected PR admission**.

## Documentary chain and claim classes

| Evidentiary class | Protected evidence | Scope accepted | Scope not accepted |
| --- | --- | --- | --- |
| A: source lock | `triage/0560-0564.json`, selected problem #560 and source audit comment #6916199376 | Correct original Erdős question and known literature | A bibliography is not an independent proof |
| B: ordinary mathematics | [`#3434`](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3434), merge `997a3d8068c3b2a036d5811bfabfce2b92a4be15`; custody [`#3436`](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3436), merge `123701f543f32c7bf92197f77f39405a3702f8f4` | Independently reconstructed known off-diagonal size Ramsey counting lower bound, (sgeq2, tgeq s+2) | Original diagonal conjecture, new mathematical priority, earlier primary proofs re-derived |
| C: formal applicability | [`#3443`](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3443), merge `2371fb3feda35d98f6da19855a0a1348ca284afa`; custody [`#3449`](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3449), merge `1f2c11fe2c3f40c9083ebf8603f0fd25e36d5f21` | Twelve Lean 4.33.0 **auxiliary** theorems compiled; three false targets rejected; adversarial source-scope review | No-hole full published theorem, kernel-checked Mathlib equivalence, complete colour-count proof |
| D: document and evidence audit | `docs/erdos/proof-verification-0560.md`; `D_DOCUMENTARY_REVIEW_001.json`; `D_EDITORIAL_ADVERSARIAL_REVIEW_001.md` | Complete, scope-qualified public status and proof/claim ledger consistency | Mathematical/MathCERT certification or immediate 100-item cohort closure |

**Source authority:** `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml`, entry #560, source Git blob `4e60263a80af6207aca494d2e1388e44fa372889`; historical status `open`. The indexed [maintained #560 entry](https://www.erdosproblems.com/560) also reports open. The main positive result is independently reconstructed from *Conlon, Fox, Wigderson, Three early problems on size Ramsey numbers*, *Combinatorica* 43 (2023), 743–768, [arXiv:2111.05420v2](https://arxiv.org/abs/2111.05420), Proposition 2.2, not an invented publication. The original 1978 and 1993 papers are cited for external context only, not claimed re-proved.

**Accepted bounded disposition:** `REVIEWED_VERIFIED_BOUNDED_OFF_DIAGONAL_LEMMA__ORIGINAL_PROBLEM_OPEN`. For all finite simple host graphs with (q) edges and (sgeq2, tgeq s+2), the proof reconstructs (N_{s,t}(H)leq(4e^2q/st)^t) (and therefore the published weaker 8 constant), followed by a first-moment colouring bound (widehat r(K_{s,t})>st2^s/100). Its exact scope excludes (K_{n,n}). Independent finite regression enumerates 36,168 graphs and 987 rational parameter cases; these are **not** used as a replacement for the general ordinary mathematical argument.

**Correct formal claim:** twelve specific auxiliary declarations were checked by Lean v4.33.0 and their axiom reports read back. The exact still-unproved formal bridges are: the degree-ranked finite-copy bucket injection; power-tail/analytic summation; and finite edge-colouring/first moment in a typed Mathlib graph context. `FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT` is not an infrastructure-only warning and is not waived. The frozen FormalConjectures source at `85f863718beeec7b58a3a1926ee92e3472bc2020` had no #560 formal file.

## Public access and reproducibility

Published target (after protected merge): `/MATH-PROGRAMME/erdos/proof-verification-0560/` via the MkDocs site. The page is linked from the Compendium index and explicit MkDocs navigation. It distinguishes its claims from the separately generated [catalogue #560 entry](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0560/). It includes the technical count, historical question, source references, strong negative results, exact B/C worker-return and custody PR links, and a named next obligation.

Read-only reproducibility commands from the repository root:

```sh
python3 ci/erdos_pv_bipartite_count_0560.py
python3 ci/test_erdos_pv_bipartite_count_0560.py
python3 ci/erdos_pv_0560_formal_replay.py
python3 ci/test_erdos_pv_0560_formal_replay.py
python3 ci/validate_erdos_pv_full_coverage.py
python3 ci/test_erdos_pv_full_coverage.py
python3 ci/test_erdos_pv_queue.py
python3 ci/math_markdown_gate.py --file docs/erdos/proof-verification-0560.md
```

The `erdos_pv_0560_formal_replay.py` command by default verifies a frozen exact toolchain/compiler receipt, whereas `--execute` requires the pinned locally installed Lean compiler to actually recompile and regenerate evidence. The formal-validation GitHub lane also builds the Lean source under its governed Lake target; neither action proves the complete published result.

## Verdict, residual and protected-admission boundary

The document reports an **independently reconstructed, bounded known lemma**, a **separately source-scoped adversarial review by the same operator**, and **partial actual Lean verification** without falsely claiming a complete theorem proof or independent external reviewer. The original question remains OPEN, source-to-Mathlib completeness is NOT PROVED, and MATHCERT is NOT_SUBMITTED. This review is eligible for **bounded documentary admission**, not mathematical certification.

Protected acceptance requires: one authenticated `RESULT/1` returned for `ERDOS-PV-0560-D`; reviewer and public-document receipt with exact byte hashes; CI and repository checks; protected merge; separate immutable custody readback; and atomic worker-claim release. Only after that can the individual #560 four-stage **bounded documentary** record close. The wider 501–600 cohort and parent programme remain open.

**Next executable mathematical obligation:** a source-typed Mathlib finite graph copy-count theorem establishing the (i)-th bucket injection, followed by the analytic tail and edge-colouring count with a hostile missing-multiplicity test. This is a new proof obligation and cannot be silently included as accomplished in documentary Phase D.
