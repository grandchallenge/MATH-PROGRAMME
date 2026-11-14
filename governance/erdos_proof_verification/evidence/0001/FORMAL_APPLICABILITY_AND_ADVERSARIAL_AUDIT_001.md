# Erdős #1, Phase C: formal applicability and adversarial review

**Work item:** `ERDOS-PV-0001-C`, cohort issue #3238.  
**Disposition:** source-formal applicability established; actual GCL kernel replay and axiom attestation **not yet verified**. No certification or final original-problem resolution is claimed by this record.

## Immutable mathematical authority

The frozen benchmark `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020:FormalConjectures/ErdosProblems/1.lean` (Git blob `c8aa6e1889b02f48b18164df3dce518a80409b27`) defines `Erdos1.IsSumDistinctSet A N` as containment in `Finset.Icc 1 N` together with injectivity of the subset-sum map on `A.powerset`. Its frozen `erdos_1` asserts the existence of a **single** positive real constant $C$ such that every admissible finite $A$ with nonzero $N$ satisfies $C2^{|A|}<N$. Its proof body is `sorry`, hence it is a statement, not a checked positive theorem.

The author-maintained source `tadamcz/erdos1@db6f9091dfaf9bac704e6b28fb3a094594869328:Erdos1/Resolutions/Erdos1_219usd_38h.lean` has Git blob `07d2f36647a2319e65c0c8c756527460925e9075`, 105,618 bytes, SHA256 `b99ae0ce768fd02ee21c05f1398e9f6ab01988fbca9d2d359a4c51fd5e345107`. It defines the same finite sum-distinct predicate, and its final `Erdos1.erdos_1.disproof` states the negation of that exact historical positive claim.

Source toolchain: `leanprover/lean4:v4.28.0`. The author Lake manifest Git blob is `8313c2070fbc6c323b32b67aca5f0751dbc24da6`, with Mathlib exact revision `8f9d9cff6bd728b17a24e163c9402775d9e6a365`. The examined primary source contains no lexical `sorry`, `admit`, `axiom` or `unsafe` token. This does **not** constitute a transitive import check, a compiler transcript or an axiom report.

## Bounded theorem and dependency structure

The author theorem `ErdosCounter.exists_binary_block_set` (line 158) assumes positive integers $d,k$, a family $a_i>0$ bounded by $W$, and the relation-freedom condition that every integer vector satisfying both $|c_i|<2^k$ for each $i$ and $\sum_i a_i c_i=0$ is zero. Its conclusion is a set $A$ of cardinality $dk$, contained in $[1,2^{k-1}W]$, with injective subset sums.

The actual author proof proceeds through `binary_sum_abs_lt` (line 62), `binary_sum_eq_zero` (line 84), `binary_block_relation_zero` (line 109), and `binary_block_sum_injective`, then maps the indexed weights $a_i2^j$ into a finite set. The indexed singleton argument establishes that distinct positions have distinct weights, which is essential for the claimed cardinality $dk$. The proof checks positivity and the endpoint bound, not just subset-sum injectivity.

The Phase B proof and the author proof use logically equivalent signed-binary uniqueness arguments. Their common essential inequality is $|\sum_{j<k}\varepsilon_j2^j|\leq 2^k-1$ for digits $\varepsilon_j\in\{-1,0,1\}$. The global author theorem `no_uniform_subset_bound` (line 2389) invokes additional lattice and cube-gadget constructions. Those constructions are not established by the bounded transfer theorem.

## Separate role-scoped critical pass

**Critic role:** challenge the exact assumptions and theorem boundary, rather than accept the source author's informal explanation. This is a distinct logical audit pass within GCL, not an independently staffed human or external referee.

**Hostile weakening:** Replace the hypothesis threshold $2^k$ with $2^{k-1}$. At $k=2$ and $a=(1,3)$ there is no nonzero integer relation with each coefficient of magnitude less than $2$, because the only permitted coefficients are $-1,0,1$. Nevertheless the binary blocks are $[1,2,3,6]$, and $1+2=3$ gives colliding subset sums. The weaker assertion is false. The pinned theorem correctly requires the stronger threshold $2^k$; the actual relation $(3,-1)$ violates that stronger premise.

**Cardinality attack:** Distinct subset sums on indexed positions imply injectivity of the individual weights by comparing singleton subsets. The author explicitly applies that argument before transporting to the image `Finset`. No cardinality gap is found.

**Quantifier attack:** The coefficient bounds are per-index and independent of $d$. The same $W$ bounds all weights. The source includes $k>0$, so the endpoint $2^{k-1}W$ is interpreted with a nonnegative exponent. The theorem is integer relation freedom, not real-linear independence; the latter would be an incorrect requirement when $d>1$.

**Overclaim attack:** The full Erdős #1 disproof requires separate existence constructions and cannot be inferred from the finite fixtures or the conditional transfer lemma. The frozen positive source contains `sorry`; the presence of a newer `disproof` declaration in source does not by itself certify its successful Lean kernel elaboration.

## Actual replay status and scoped execution path

The available CHAD environment exposed the exact Lean 4.28 executable, but even a minimal `import Init` smoke test exited **124** under a nine-second timeout without compiler output. An attempted larger finite test did not complete within a 28-second invocation budget. These are **non-verifications**, not positive compilation results.

The new manual-only workflow `.github/workflows/erdos-0001-pinned-replay.yml` is paired with `ci/erdos_pv_0001_replay_contract.py`. It requires the exact source commit, proof blob and SHA256, Lean toolchain, Lake manifest and Mathlib commit; it compiles the author library and independently type-checks the bounded theorem and final negation statement. It prints both axiom lists and rejects unexpected axioms or `sorryAx`. A separate deliberately invalid target **omits the relation-freedom hypothesis** and must fail compilation. The verifier reports an unadjudicated PASS only if all real compiler exit statuses, reports and negative results agree.

**Verdict:** `FORMAL_APPLICABILITY=YES`; `STATIC_SOURCE_AND_SEMANTIC_REVIEW=PASS`; `ADVERSARIAL_SCOPE_REVIEW=PASS`; `KERNEL_REPLAY=NOT_VERIFIED`; `AXIOM_REPORT=NOT_OBTAINED`. The next step is to run and independently adjudicate the pinned replay after protected workflow admission. The Phase C per-problem stage must remain incomplete, and Phase D must remain gated until its actual formal evidence requirements are met.
