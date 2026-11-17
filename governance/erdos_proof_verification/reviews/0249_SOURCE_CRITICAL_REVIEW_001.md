# Erdős #249 — source-critical and adversarial review 001

**Disposition: QUALIFIED_PASS_T_ONLY.** The verified Lean theorem proves irrationality of the auxiliary *lacunary totient subseries*, not the original full series, which remains open. The actual formal author and this GCL adversarial role are operated by the **same authenticated ChatGPT agent**. This is a separate role-scoped critical pass, **not independently authored mathematical proof, different human review, or MATHCERT certification**.

## Exact evidence and evidence custody

- Original research problem: is the full sum $S=\sum_{n\geq1}\varphi(n)/2^n$ irrational? Its pinned statement-only provider is `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020`, file `FormalConjectures/ErdosProblems/249.lean` Git blob `ed4650c870f58a7cbfbc9ec8c4bc4c35175b074a`. This has `answer(sorry)` and `by sorry`; it is not a proof.
- Authored auxiliary proof: `experiments/erdos_proof_verification/0249/Erdos249Lacunary.lean`, SHA-256 **`6ec552e86902699f26472a3cddb6fdcf79e7dba1abb6ac3c3b486a2bda82cb99`**, 292 lines. Protected through PR #3446 at **`62ffaa1db3e2d1a5d120611e86fc189f1c24b50e`**.
- Verified Lean `leanprover/lean4:v4.35.0-rc3`, binary commit `470d5ce1400764999581fd26d5d72b00d990b0f4`, Mathlib exact `c55e6e786f49471c72fbddbec5415808896aec1e`; Lake dependency manifest SHA-256 `3b9de3758005c73d884250d11611c935882adf24f02d9a35dc698a033daadde2`. This is **not** the earlier unsuccessful 4.33.0 cache attempt.
- Real first replay + exact-head fresh-checkout replay: both exit 0, theorem type directly printed, only foundational axioms `[propext, Classical.choice, Quot.sound]`, no `sorryAx`, empty stderr, byte-identical stdout SHA-256 **`038d3d08c883f2c17394c2e39a9eaeaeda5d57970745626390528d360f9c9365`**. Machine receipt: `governance/erdos_proof_verification/evidence/0249/LACUNARY_LEAN_GREEN_001.receipt.json`.
- Hostile full-series changed-goal attempt failed with Lean type mismatch (exit 1, SHA-256 `5cc0d6ccb3b7a8ed27e283c9bc78a435984441bc0cb2faa4f810acc2e258f6ec`). This guards theorem identity; a type mismatch by itself is not a proof of mathematical non-implication.

## Adversarial theorem-level checks

**A1 — exactly the prescribed subseries and index shift: PASS.** The final Lean statement is

$$
\left(\sum_{m=0}^{\infty}
  \frac{\varphi(2^{m+1})}{2^{2^{m+1}}}\right)
\notin\operatorname{range}(\mathbb Q\hookrightarrow\mathbb R).
$$

By reindexing $j=m+1$, this is exactly the series $T$ in the already protected handwritten proof. The `Set.range Rat.cast` predicate is the definitional content of Mathlib's `Irrational` for real numbers. No implication concerning the full $S$ is present in the final theorem type.

**A2 — totient identity: PASS.** `totient_two_succ` uses Mathlib's proved `Nat.totient_prime_pow_succ Nat.prime_two`, not an asserted totient identity. It establishes $\varphi(2^{m+1})=2^m$, including $m=0$.

**A3 — exponent indexing and positivity: PASS.** The source defines $e_m=2^{m+1}-m$ for zero-based $m$, and proves its successor gap is $2^{m+1}-1$, strictly positive for every $m\geq0$. The first values are 2,3,6,13,28. The proof handles natural subtraction through explicit inequalities, including $e_m\geq2$, rather than silently using subtraction over integers.

**A4 — convergence and tail sign: PASS.** Summability follows from $e_m\geq m$ and comparison with the geometric series of powers of 1/2. The remaining tail begins at $e_{N+1}$, each subsequent term has exponent at least $e_{N+1}+j$, and is strictly positive. The computed bound is $0<R_N\leq 2^{1-e_{N+1}}$. Adjacent early digits do not cause a carry problem because this is a real positive-tail bound, not a uniqueness argument for binary expansions.

**A5 — finite dyadic numerator: PASS.** For each $N$, `partialSum_eq_rat` constructs a *natural* numerator $A_N$ with $T_N=A_N/2^{e_N}$. This does not require lowest terms. The induction uses the exact natural exponent gap.

**A6 — rational denominator obstruction: PASS.** Under an arbitrary rational $q$, take its positive denominator $b=q.den$ and set $N=b+1$. The integer $z=q.num\,2^{e_N}-bA_N$ is shown exactly equal (after real casting) to $b2^{e_N}R_N$. It is strictly positive, so $z\geq1$. The gap estimate proves $b2<2^{e_{N+1}-e_N}$; the geometric tail gives $z\leq b2/2^{e_{N+1}-e_N}<1$. Thus no rational $q$ can equal $T$. This is a denominator-separation argument, not an unproved binary nonperiodicity assertion. It works for zero, positive and negative hypothetical rational numerators because the contradiction only relies on the denominator being positive.

**A7 — axioms and source integrity: PASS WITH PROVENANCE LIMIT.** The actual axiom audit contains only three standard foundational Lean axioms; no `sorryAx`. A fresh source-lock replay returned exactly the original log bytes. But it shares a compiled Mathlib dependency cache from a pinned local development workspace and is **not** a clean-room dependency rebuild nor an independent operator signature. It is a valid kernel check of this specific imported source graph.

**A8 — purported original-series consequence: REJECTED.** Irrationality of a positive proper subseries does **not** entail irrationality of an encompassing positive series as a matter of logic. The omitted terms could change rationality. The provided hostile changed-goal test confirms Lean does not mistake the two expressions, but is not a universal theorem about arbitrary completions. The only accepted result is $T$ irrational; the full Erdős problem #249 remains **OPEN**.

## Residuals and decision

- The exact no-`sorry` Lean proof is authored in this GCL workstream, so the Referee and Adversary pass must **not** be presented as external mathematical independence. The logical adversarial checking and underlying kernel result have separate scopes, but are not independent humans.
- The pinned provider of original $S$ contains an admitted open conjecture statement, not a completed proof. No proof for original $S$ has been supplied. A future attempt must obtain its own source and theorem-level evidence rather than promote the auxiliary result.
- The actual tested toolchain is Lean 4.35.0-rc3/Mathlib c55e. No 4.33 result is claimed; no need to repeat enormous dependency builds simply to re-label the successful pinned 4.35 replay.
- **Adversarial review:** **PASS for the source-locked auxiliary $T$ theorem only**. Not certification, not a full conjecture solution. Internal Referee adjudication remains a separate logical decision with explicitly limited claim scope.

**Outcome:** `ERDOS249_T_SOURCE_CRITICAL_QUALIFIED_PASS__ORIGINAL_S_OPEN__NOT_MATHCERT`.
