# EC-BULK-004 — Erdős #484 mathematical source-exception review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-021  
Observed: 2026-10-14  
Authenticated accountable identity: fyremael. This is an adversarial documentary/mathematical pass by the same operator, **not** an independent-person referee or GCL Lean certification.  
Decision: **CRITICAL_DRAFT_PASS_WITH_EXTERNAL_LEAN_REPLAY_PENDING**.

## Original statement and exact distinctness boundary

The original source is P. Erdős, “Some unsolved problems” (1961), printed p.230, Problem I.16, https://users.renyi.hu/~p_erdos/1961-22.pdf#page=10 , read directly from the scanned page. Its colored-class sums are described without an explicit $a\ne b$ restriction. Without distinct summands the problem would be trivial because every even $s\le N$ has $s=s/2+s/2$ in any coloring. The actual nontrivial statement attributed to Roth is exactly clarified in the resolving primary paper, P. Erdős, A. Sárközy and V. T. Sós, *On a conjecture of Roth and some related problems. I* (1989), *Irregularities of Partitions*, pp.47–59, full PDF https://real.mtak.hu/110587/1/1989-14.pdf : p.47 explicitly specifies **two different same-color summands** and p.48 remarks that repeated summands would trivialize it.

For all $k\ge1$ the quantifier is $\exists c>0$ ABSOLUTE, $\forall k\ge1$, $\exists N_0(k)$, $\forall N\ge N_0(k)$, $\forall k$-colorings $f$, the set of DISTINCT representable targets $s\in[1,N]$ has cardinality at least $cN$. A per-$k$ constant, a single monochromatic triple, representations counted with multiplicity, and a statement valid for all small $N$ are non-equivalent readings.

## Full primary theorem and source-proof critical audit

The complete 13-page resolving primary is accessible in the Hungarian Academy's repository and was inspected, not merely cited. Theorem 1(i), p.48: for every fixed $k\ge2$ the count of even representable targets is
$$
|C_N^{\mathrm{even}}|>\frac N2-3N^{1-2^{-(k+1)}}
$$
for $N>N_0(k)$. This has error $o(N)$ for fixed $k$, so eventually exceeds $N/4$, giving a universal $c=1/4$. The theorem's formal $k\ge2$ range was **not** silently extended: for $k=1$ and all $N\ge3$ every target $s\in\{3,\ldots,N\}$ has distinct representation $1+(s-1)$, and $|C_N|=N-2\ge N/4$ for $N\ge4$.

The 1989 proof p.49 Lemma 1 constructs a density Hilbert cube; pp.50–51 use its $k+1$ **distinct positive generators** $v_i$ and even base $u=2z$. Among distinct integers $z+v_i$, two share a color. Their sum $u+v_i+v_j$ belongs to the presumed *missing* even targets and is a representation with distinct same-color summands: contradiction. The full published lemma proves its own density threshold; GCL has inspected the proof but has not independently recreated a kernel-certified version.

Theorem 1(ii) p.48 yields missing even targets $O(\log N)$ with two colors. Its p.51 proof shows a sequence of missing even integers satisfies $b_{j+2}\ge b_j+b_{j+1}$: if strict reverse held, three **positive and distinct** half-sum combinations $x,y,z$ would have pair sums equal to missing targets, and some pair shares a color. Theorem 1(iii), proved p.51, constructs a 2-coloring omitting **all powers of two** as distinct-summand monochromatic targets, so a logarithmic deficit is possible. These are not counterexamples to $cN$ positive density.

The modern #484 source is **PROVED** mathematically; the adjacent #483 Schur forcing exponential-growth question remains OPEN and allows equal summands. This difference is tested and explained.

## Independently replayed finite fixtures and important limitations

Five source-specific tests in tests/test_erdos_compendium_0484_roth_sums.py passed at source commit 7222a21bca39081e976b6b67eb375cbd46a27529. Tests enumerate **distinct target sets** by two different algorithms, examine all $2^{10}$ two-colorings and all $3^8$ three-colorings (and small one-color), assert the exceptional $a=b$ prohibition ($N=2$ has zero valid targets), check $k=1$ all $N$ in 3..59, verify the 2-color odd-part $\pmod4$ construction through $N=512$ omits every power of two, and test missing-even Fibonacci inequalities over all 2-colorings for $3\le N\le11$. This is bounded finite support, not a proof of the all-$k$ 1989 density lemma.

The local worktree already contained a substantial untracked 0484.md. Its original bytes were preserved at /tmp/EC004-0484-original-local-draft-20261014.md (original SHA-256 **7efe8f56e1b796ade6fffc7ac21f8d6ef1f71a0dc349bc518127edbd01445892**) before the article was completed, reorganized into six mandatory sections, hash-checked and committed by the authenticated CHAD git identity. No other untracked project evidence was overwritten.

## Formal and provenance boundary

Current unpinned google-deepmind/formal-conjectures main file FormalConjectures/ErdosProblems/484.lean, Git blob **c7c15cb5c36622301408b4ea7546dd21d7fec6f9**, has faithful quantifiers and a≠b but its main theorem body is **by sorry**. The pinned GCL FC-GDM-85F86371 version has no #484 file. It cites externally asserted Lean proof plby/lean-proofs@1d7b3f00780b85ed0462e79a1cd5650ee9055655 src/v4.29.1/ErdosProblems/Erdos484.lean, source Git blob **4f4bc324e8701df270f7108b5310158e9184db2d**, whose file defines a density-cube argument and proves a target count ≥$\lfloor N/8\rfloor$, with printed axiom claim [propext, Classical.choice, Quot.sound]. GCL has **NOT** independently compiled the exact transitive Lean project, validated axioms, or bridged this integer floor theorem to the modern real bound. For $N\ge16$, $\lfloor N/8\rfloor\ge N/16$ shows how a formal adapter could work; the $N$ cutoff and natural-to-real casts must be explicit. Catalogue “PROVED (LEAN)” and its contradictory “Formalised statement? No” metadata are documented as an external report, not local certification.

Issue-bound six-section authenticated RESULT/1: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1754#issuecomment-6179979100, exact author fyremael, normalized LF body SHA256 **0b5df561fc8771ae2a5ec29c3852892f2a35ba2f2f94b710e088e3c6b12bf101**, disposition SOURCE_LOCK_READY for documentary 1961/1989 sources, not GCL MathCert.

Article governance/erdos_compendium/editorial/0484.md, six mandatory headings each exactly once and balanced math delimiters, SHA256(UTF8(strip())) **5600c406dfcd055ae00d90dce8d105fce7dc7d7828d17419b040986e13446a61**, raw SHA256 **6f863d1cd83770ea0d8b1e31a8bc1aba0e25af08d4e99ee83096ad80f1d9b6ef**. Other cohorts untouched; article is UNACCEPTED_DRAFT.

## Review outcome and bounded successor

CRITICAL_DRAFT_PASS_DOCUMENTARY_AND_FINITE_MATH, with source/MathCert exception: independent Lean kernel replay, actual external axiom list, exact adapter and public HTML/MathJax final review still pending. Source-lock original and full 1989 primary with page hashes, then formally prove separate density-cube existence and pigeonhole contradiction lemmas, independently compile plby source with actual lean-toolchain/lake manifest, and check a bridge from ≥floor(N/8) to ∃c>0 ∀N≥N₀ count≥cN. Falsify on repeated summands, wrong finite target-set cardinality, insufficient cube dimension, k=1 mishandling or invalid rounding. Stop at the named proof/source gap and do not manufacture a GCL Lean certificate. This is an extra source-critical pass, **not** one of the fixed deterministic 20-article sample items, and does not constitute public-browser verification or protected V2 admission.
