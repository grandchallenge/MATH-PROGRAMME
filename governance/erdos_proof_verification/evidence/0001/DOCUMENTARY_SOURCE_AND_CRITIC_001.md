# Erdős #1 — documentary proof-verification audit

**Task:** `ERDOS-PV-0001-D`; cohort [#3251](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3251).

**Scope:** bounded public-accountability adjudication of independently reconstructed binary-block mathematics and the source-pinned Lean replay. This is neither an independent complete mathematical reconstruction of the 2026 disproof nor MATHCERT certification.

## Historical problem and source lock

The original conjecture asked for one universal constant $C>0$ such that every nonzero $N$ and positive-integer set $A\subseteq\{1,\ldots,N\}$ having distinct sums for all subsets would satisfy $C2^{|A|}<N$. The author-maintained 2026 disproof refutes that universal assertion. The pinned FormalConjectures historical positive statement retains a `sorry` placeholder and cannot itself be cited as a proof.

Primary proof source: `tadamcz/erdos1@db6f9091dfaf9bac704e6b28fb3a094594869328:Erdos1/Resolutions/Erdos1_219usd_38h.lean`, Git blob `07d2f36647a2319e65c0c8c756527460925e9075`, SHA256 `b99ae0ce768fd02ee21c05f1392e9f6ab01988fbca9d2d359a4c51fd5e345107`; Lean `v4.28.0`; Mathlib commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`. Source-audit issue [#1270](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1270), protected source-scope Phase A, and bounded proof Phase B [#3225](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3225) are distinct evidence stages.

## Precisely established claims

Protected GitHub Actions [replay #43541084973](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43541084973) built 8,028 jobs with exit 0. Its separate positive readback of `ErdosCounter.exists_binary_block_set` and `Erdos1.erdos_1.disproof` exited 0; `#print axioms` yielded only `propext`, `Classical.choice`, and `Quot.sound`. A deliberately altered theorem application with the indispensable `RelationFree` hypothesis omitted failed compilation (exit 1). Evidence was protected-admitted by [PR #3320](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3320) and custody-rebound by [PR #3321](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3321).

The [compiler receipt](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_proof_verification/evidence/0001/LEAN_REPLAY_43541084973/RECEIPT.json) and [role-scoped replay adjudication](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_proof_verification/evidence/0001/LEAN_REPLAY_43541084973/INDEPENDENT_GCL_REVIEW.json) explicitly distinguish the conditional binary-block lemma from the full source declaration.

GCL independently reconstructed the conditional mathematical transfer: relation-free positive weights with every integer-relation coefficient of magnitude less than $2^k$ lead to $dk$ binary-block weights with injective subset sums and a controlled maximum. A falsification test shows why weakening the relation threshold to $2^{k-1}$ is invalid: $a=(1,3)$ at $k=2$ yields $[1,2,3,6]$ and the collision $1+2=3$. The actual source retains the correct $2^k$ premise. The advanced global source theorem uses additional lattice/cube-gadget constructions which GCL has **not** independently reconstructed and adjudicated mathematically in full.

**Three separate verdicts:** Bounded mathematics has a documented internal proof and adversarial review; the source-authored global Lean theorem and bounded lemma passed a pinned kernel check; independent human mathematical refereeing, independent full global proof interpretation, and MATHCERT certification have **not** been obtained.

## Critical editorial pass

A role-scoped critic (not a distinct human referee) compared the source issue, bounded Phase B, pinned Phase C logs, public problem #1 manuscript, and editorial-policy restrictions.

1. The existing public article's statement that GCL had not replayed the proof was stale. The exact Lean replay above now supplies a real compiler transcript.
2. The correction must **not** turn the green kernel check into a claim of independent mathematical rederivation of all deeper disproof lemmas.
3. The source's uniform positive-constant conjecture is disproved; that does not imply polynomially bounded sum-distinct examples or any particular optimal asymptotic family.
4. The four-element example must genuinely have 16 distinct subset sums. For $A=\{3,5,6,7\}$, direct enumeration gives 16 distinct sums.
5. The site must continue distinguishing source audit, mathematical lemma verification, formal replay, editorial review and MathCERT certification. A single role-scoped self-critique is not independent human endorsement.

The corrected `governance/erdos_compendium/editorial/0001.md` retains the six required explanatory sections, direct links to the replay/receipt and explicit limits on GCL's verification. Its stripped-manuscript SHA256 is `64026cab37a6ba0bbe18d154ad64b38fe311d933dd0804e2c1a3414a9802cf78` (to be independently checked by the editorial-admission gate).

## Publication and protected-close requirements

The intended public page is [Erdős Compendium problem #1](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0001/). This is currently a **legacy explanatory exemplar**, not an admitted editorial article in the SHA256-bound `governance/erdos_compendium/EDITORIAL_ADMISSIONS.json` ledger. A manuscript PR is not editorial admission: first protected-merge the correction and verify the deployed HTML/math rendering, then submit a distinct editorial-admission PR tied to the exact manuscript hash, critical review and public readback.

Only then should Stage D be marked protected-admitted with its exact documentary evidence, and only after the accepted D custody has been read back should the reservation be released and the individual `closure_status` be set to `ADMITTED_BOUNDED_COMPLETE`. The cohort issue remains OPEN until all 100 problems have their own dispositions. Global proof verification and any MATHCERT handoff remain separate.

**Current disposition:** scoped content and source review PASS; live corrected public HTML and editorial admission PENDING; full independent disproof audit/MATHCERT NOT COMPLETED.
