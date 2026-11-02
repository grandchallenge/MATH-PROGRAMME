# EXT-015 REACH / 130 — nonauthor review of current pro-cochain applicability

**Primary disposition: REVISE the sequence-cofibrancy and completed-homotopy-colimit claims.** The cited generic criterion C.5.6.1 is incorrect for its stated nonpositive-integer projective diagram model. Explicit vector-space counterexamples are given below, including a strictly complete product-tail filtration. Thus129 has not justified that its filtration sequence is projectively cofibrant, or its dependent use of the cited completed-cone proof. This does not refute the final completed-cone statement itself. The direct C.4 pro-cochain object, strict completion, additive filtered maps, base cochain cofibrations, unit-cone tests, kernel right-lifting criterion and explicit weightwise cone calculation are justified independently. One consolidated correction must either supply an independent repaired argument or withhold the affected conclusions.

## 1. Frozen custody and provenance

| Artifact | Exact identity |
| --- | --- |
| Supplied frozen primary commit |c8555f50db715112a7d0e55a4fa1a8ff3c64f24d |
| Preserved primary branch | `research/reach-procochain-primary-frozen-20261102` |
| Actual primary129 |9f7adcbb4776bd084b23fa71703d61a391cc84c1 |
| Actual draft131 |aa64e6ed6817f185a882d5fb238ad9d087d7464e |
| Frozen input cut |a2e14adab7d4fe11827ff7eabc6f66736649c2a1 |
|59-input manifest SHA256 |5ceaa2c0c993365556e04be391a37afa8c3ca0099f5eed90132743183cf929fb |
| Accepted source-controlled126 |5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| Its final127 |74c47f1329d414fdf65f85cb3fdda8712852e65f |
| Its ledger128 |0084cc18ad122d5e5d4e30032f51bbd096d3e15e |

Read-only byte calculations match the actual129/131 files and all59 manifest entries to their frozen identities. Relevant hypotheses and uses of126/127/128, the unit audit114 and the retained quantum/R1 comparisons were checked. Full-manifest byte verification is not a new mathematical audit of every historical source.

The actual full primary [author-linked university PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/8/48667/files/2025/04/vol1may8.pdf) and native text are retained. Their SHA256 identities are respectively `267c00893175fd955bf2408afa7b6dcb63647f3e4d2b0ec6553255040bc3f4c4` and `1a50485d2285722e79f6462c4479d7048042c7df52fa8a4e714ee96d50af1a68`, both independently verified. The retained official-page bytes contain that exact link and match `c5617b79d05a0b368e9a118a71a89a8ed7c0c005fd054a5654c2a6306a435a6c`. Metadata matches `f59fd4c706adde0729b26cf19f3fb5751e776fafdb3680e9eac2055bdbEAFC6A` case-insensitively. The actual Appendix C definitions and proof body were read, particularly printed294–306. No identity with the older522-page concrete edition is inferred, and the earlier MPIM403 operation was untouched.

The parent and construction context authored129. This reviewer did not. The parent supplied the proposed hostile tests; they were independently checked against the literal source conventions, and the proofs below are the review's reason for its adverse finding. Informal producer repair notes are not frozen source evidence and are not preapproved. Shared earlier critics106/109/112/115/118/121/124/127 are disclosed. This is distinct same-system nonauthor scrutiny, not external independent certification. The earlier service interruption produced no130 artifact or completed verdict. Only130 is written; no Git invocation, Python, tracker or external mutation is used.

## 2. Critical inference matrix

| Inference | Verdict | Exact reason or boundary |
| --- | --- | --- |
| Current module-sheaf convention differs from old concrete convention | Justified | The actual definitions and source-controlled nonconcrete domain remain explicit |
| Each fixed profinite test gives a differentiable module sheaf | Justified | Evaluation preserves matching limits and the finite cotangent idempotent; no exactness assumption on arbitrary profinite evaluation |
| Negative weight-tail filtration and strict completion | Justified | Actual monomorphic tails, finite-prefix quotients and coordinate-wise inverse limit |
| Additive filtered structural multimaps | Justified | Total quantum weight adds, with finite formulas per output weight |
| Generic C.5.6.1 monomorphism criterion | INCORRECT as stated | Sections3–4 give objectwise trivial fibrations with no diagram lift |
| Actual129 tails are projective-sequence cofibrant | UNRESOLVED / unsupported | Monomorphic split maps do not imply it; no direct diagram lifting proof is supplied |
| Tails are base injective-model cochain cofibrations | Justified | Degreewise monicity is the actual base criterion, independent of sequence cofibrancy |
| Real-axis R1 and source-controlled comparison are base cofibrations | Justified | Actual module-sheaf monicity; no statement about all profinite evaluation or projective sequences follows |
| Wick and scale isomorphisms are filtered weak equivalences | Justified | Actual inverse maps and weight preservation at every fixed coefficient test |
| R1 and physical comparisons fail the required equivalence test | Justified | Nonzero weight-zero point cones; no higher-weight boundary removes a split factor |
| A split projection is fibrant exactly when its kernel is fibrant | Justified | Pullback of the kernel map and converse pullback square |
| All actual weight/tail kernels are fibrant | Unresolved | No extension against every acyclic monomorphism is supplied |
| Cited C.5.6.6 applicability via cofibrant sequences | NOT ESTABLISHED by the primary | Its imported proof uses the false sequence identification; an independent argument or restriction is needed |
| The completed-cone theorem's final statement is false | Not demonstrated | The counterexamples refute the stated cofibrancy criterion, not that final universal property |
| Explicit associated-graded cone identity129.8a | Justified independently | Finite prefixes, exact coproducts and coordinate completion compute the specified bar-cone object |
| That formal cone identity proves a homotopy-colimit universal property | Not justified | Its algebraic computation and the universal property are different inferences |
| Whole quotient tower is eventually constant | Not asserted; would be incorrect | Stabilization of each fixed prefix is weaker |
| Reverse source-history localization129.9 | Unresolved | Output cutoff support does not rehost forgotten source vertices |
| Full recovery126.14, target Weiss, original R3 or full M5/R4 | Open | None is settled by the surviving categorical calculations |

## 3. A literal counterexample to the generic sequence criterion

Use the Grothendieck category of real vector spaces and its stated injective cochain model. The indexing category really is the nonpositive integers with a map from a smaller integer to a larger integer. It has no initial index. Fibrations and weak equivalences in the specified projective sequence model are objectwise ones.

Let $X_n=\mathbb R[0]$ for every $n\le0$, with identity transition maps. Set

$$
E_n=\bigoplus_{k\ge-n}\mathbb R e_k,
\qquad
\sigma_n\left(\sum a_ke_k\right)=\sum a_k,
\qquad K_n=\ker\sigma_n.
$$

All sums here are finite. The transition maps are the evident inclusions of these tails, and the augmentations commute with them. Define $Y_n=[K_n\hookrightarrow E_n]$ in degrees minus one and zero, with its augmentation $p_n:Y_n\to X_n$ given by $\sigma_n$.

Each augmentation is degreewise onto and a quasi-isomorphism. Its kernel is the contractible disk $[K_n\xrightarrow{1}K_n]$. This disk is an injective object of the category of cochain complexes over vector spaces: a cochain map into it is specified by one linear map from the degree-zero term, which extends across any degreewise monomorphism. Thus $p_n$ has the required right lifting property, in fact against every degreewise monomorphism. Consequently $p:Y\to X$ is an objectwise trivial fibration in the stated projective sequence model.

If the sequence $X$ were cofibrant, the lifting square for $0\to X$ against $p$, with bottom map the identity of $X$, would have a lift. At degree zero it would choose $v_n\in E_n$ with $\sigma_n(v_n)=1$, compatible under every inclusion. Viewed in $E_0$, all these vectors would equal one vector in

$$
\bigcap_{n\le0}E_n=0.
$$

That contradicts their augmentation being one. Hence the constant sequence is not projectively cofibrant, although every successive map is an isomorphism and therefore a base cofibration. This refutes the generic equivalence in the literal C.5.6.1. It is not a sign, enrichment or reindexing issue. The usual induction from a leftmost stage cannot start on this category.

## 4. The failure persists for a strictly complete product-tail filtration

The preceding constant sequence is not complete, so a separate hostile control is needed for the actual completion setting. Put

$$
F_n=\prod_{k\ge-n}\mathbb R,
\qquad n\le0,
$$

and include it in $F_0=\mathbb R^{\mathbb N}$ by zero in the earlier coordinates. All transitions are monomorphisms with split retractions. Its finite quotient is the corresponding finite coordinate prefix, so the canonical completion map from $F_0$ to the inverse limit of these prefixes is an actual isomorphism.

For $j\le0$, let $P_j(F_j)$ be the free diagram whose value at $n$ is $F_j$ when $j\le n$ and zero otherwise, with identity transition maps on its nonzero portion. There is a natural degreewise surjection

$$
\varepsilon:E=\bigoplus_{j\le0}P_j(F_j)\longrightarrow F.
$$

At index $n$ it sums the inclusions of $F_j$ for $j\le n$; the summand $j=n$ makes it onto. Write $K=\ker\varepsilon$. Exactly as in section3, the sequence of two-term cochain resolutions $[K_n\hookrightarrow E_n]\to F_n[0]$ is an objectwise trivial fibration.

A lift of the identity of $F$ would give a natural linear section $s:F\to E$. At index zero let $t_j:F_0\to F_j$ be its component in the summand indexed by $j$. Naturality forces $t_j$ to vanish on $F_{j-1}$, since that summand is absent from $E_{j-1}$. Therefore $t_j$ factors through the finite-dimensional prefix $F_0/F_{j-1}$ and has finite-dimensional image. The image of $\varepsilon_0s_0$ is contained in the algebraic sum of countably many such finite-dimensional images and is consequently at most countable-dimensional.

But $F_0$ has uncountable Hamel dimension: the geometric sequences $(1,a,a^2,\ldots)$, for real $a$, form a linearly independent family by the finite Vandermonde determinant. Thus $\varepsilon_0s_0$ cannot be its identity. This proves that the strictly complete monomorphic product-tail sequence also need not be projectively cofibrant.

These are counterexamples to the generic source claim in its permitted base category. They do not, without an additional differentiable-category trivial-fibration witness, prove that the specific129 filtration fails projective cofibrancy. They do prove that the candidate's inference from its split monomorphic tails is invalid. Replacing completion by the observation that their intersection is zero would not fix this example either.

## 5. What survives and what requires an independent argument

The direct C.4 definition only asks for a differentiable cochain complex with a monomorphic negative filtration and its completion quasi-isomorphism. The source-controlled model has the stronger strict coordinate-completion identity in129.5. Evaluation at a fixed profinite test preserves parameter sheaf matching limits, scalar actions and the finite cotangent idempotent. It therefore gives the actual module-sheaf connection with its correct global algebraic one-form tensor target. The quantum grading, finite weight sums and actual connection-compatible maps are already defined on that model. These proofs remain valid after removing the false sequence-cofibrancy conclusion.

Ordinary and matching Wick structural maps satisfy additive total-weight bounds by their finite slot/quantum count and accepted source estimates. The Wick and scale isomorphisms have actual inverses and hence are filtered weak equivalences. The R1 and physical maps have the accepted nonzero weight-zero cones, with the shifts in129.7 correct under the cohomological convention. A finite binary split keeps those factors in the completed cone; no infinite-product cohomology theorem is being smuggled in. The singleton coefficient test suffices to refute an all-test equivalence claim. For any nonempty profinite test the same constant coefficient witness can also be pulled back and detected again along a point. No assertion of a failure on an empty test is needed.

Base cochain cofibrations are degreewise monomorphisms in the stated injective model; tails and the specified monic real-axis arrows meet that criterion. Lemma129.2 is also correct independently: a split projection is a pullback of its kernel map to zero, and the kernel map is a pullback of the projection. Stability of right lifting under pullback gives the equivalence. Neither a split section nor the false sequence criterion proves fibrancy of those kernels. That remains a separate unresolved condition, not a new prerequisite for basic C.4 object membership.

The imported homotopy-colimit proof is different. Source C.5.6 defines its filtered category as the projectively cofibrant sequences and identifies it with monomorphic filtrations using the failed criterion. Its completed-cone argument then passes through that identification and the completion localization. Primary129 repeats the identification in Theorem129.1, section7 and its exit statement. Those conclusions must be suspended unless replaced by a correct independent argument for the actual category being used. A generic theorem may still have a valid final statement after repairing its proof; this review has not produced a counterexample to that universal property.

An acceptable repair must specify the actual relative categories and weak equivalences, justify any replacement of arbitrary sequences by monomorphic ones without the false converse, and justify the relation of ordinary completion to the homotopical localization in this differentiable category. Merely deleting the word cofibrant while retaining the same cited application is insufficient. Informal proposed partition-of-unity/exact-section and derived-localization arguments may be useful, but their precise hypotheses and proof must appear in the frozen correction before they can support acceptance.

## 6. The formal cone criterion and the genuine support gap

The algebraic calculation129.8a survives independently for the explicitly defined completed bar-cone object of a strict weight-preserving diagram. At each finite prefix, direct-sum totalization and the finite sum over weights commute; coproducts are exact in the stated Grothendieck category. Coordinate completion then gives the product of its weightwise ordinary cones. The specified associated graded is the indicated individual cone. The augmentation criterion follows from the definition of a filtered weak equivalence and still requires the differentiable all-manifold quasi-isomorphism test. This is not by itself a proof that the bar-cone object is the categorical homotopy colimit.

The support warning129.9 is well typed and materially necessary for the proposed reuse of R1's gluing argument. Multiplying the output of a source history by a cutoff pulls that cutoff back to the source but leaves forgotten auxiliary coordinates in the original physical open. Forward support/naturality is not a reverse rehosting theorem. A local representative modulo uniform rapidness of every mixed jet would be sufficient for the stated localization step, with further compatible intersection relations still needed for a full Cech argument. Neither that local representative nor target Weiss augmentation equivalences are proved. The proposed near/far auxiliary-vertex mechanism remains future work. It must retain the entire completed source class and profiles, not only scalar finite coefficients.

The support equation is independent of the larger retained-family recovery equation126.14. The audit correctly keeps both open and does not transfer source-controlled properties to the larger sheaf. The finite normal/profile, legal forest, quantum sign and unit controls remain in their accepted domains.

## 7. One consolidated correction request and primary return

1. Record the demonstrated generic C.5.6.1 error and both literal counterproofs or equivalent complete evidence. Remove the unsupported conclusion that the actual129 tails are projective-sequence cofibrant. Keep base cochain cofibrations distinct.
2. Either give a complete independent repaired proof of the completed-bar homotopy-colimit applicability on the declared module-sheaf category, or mark that applicability unresolved. In particular justify the relative-category comparison and completion step rather than cite the false equivalence. The final source theorem itself is not declared refuted.
3. Preserve the direct C.4 object, strict completion, additive structural maps, filtered isomorphisms/non-equivalences, right-lifting kernel criterion and formal129.8a calculation on their actual hypotheses. Make their independence from sequence cofibrancy explicit in129/131 and subsequent records.
4. Keep source-localization129.9, full recovery126.14, actual target Weiss, original R3 and full M5/R4 open. The next step must follow the corrected accepted scope; no new fibration assumption or automatic descent result should be invented to replace the failed inference.

This is the single consolidated primary request. The author may repair the proof or narrow the claimed result in one correction, then freeze it for exact-source readback. Until that source exists, the sequence-cofibrancy claim and dependent homotopy-colimit application are not accepted. No prior accepted R1 or126 result is reopened: neither used the new projective-sequence inference. R0/R1/R2 and separate087–089 retain completed reviewed scopes; all remaining original obligations keep their actual open dispositions. Mathematical scrutiny, local checks, final editorial integration, protected admission/readback and tracker reconciliation remain distinct events.
