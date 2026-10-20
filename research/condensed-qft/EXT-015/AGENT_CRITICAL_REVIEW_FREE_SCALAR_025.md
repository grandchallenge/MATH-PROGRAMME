# EXT-015D / 025 — mathematical critical audit of actual free-scalar B.6 and Weiss proof

**Disposition:** ACCEPT the **bounded** classical and formal free BV results of [024](FREE_SCALAR_DIFFERENTIABLE_WEISS_024.md), with corrections to overinterpretation explicitly rejected. This is an auditable critical mathematical **function** within GCL, not a fictitious external referee, additional credential, human approval or formal proof-assistant certification.

**Protected research proof:** [result 024, PR #2779](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2779), merged commit `c7707ead006cbd5fbdd29b0c5dfbad4145806c7f`. Its mathematical Markdown gate and exact bounded BV/Weiss fixture passed. This audit reviews that immutable result, not an unmerged return.

**Primary mathematical text:** Costello and Gwilliam, [*Factorization Algebras in Quantum Field Theory*, Vol. I](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf): §§4.2.1, 4.2.6; Lemma **4.2.1.1** and Appendix **B.10** for smooth compact-support versus distributional elliptic complexes; B.6.0.7–B.6.1.1 (printed 469–471) for filtered differentiable categories; §6.1 for Weiss covers. This audit makes no claim that these source-backed statements are newly invented mathematical theorems.

## I. The actual category and field model

The free scalar field is the explicit elliptic two-term cochain complex on an interval $U\subseteq\mathbb R$ with kinetic operator $\partial_x^2$. The regular linear observable complex is

$$
L_{\mathrm{sm}}(U)=
[\mathcal D(U)^{-1}\xrightarrow{\partial_x^2}\mathcal D(U)^0].
$$

The distributional complex uses **compactly supported distributions**, not the Fréchet space of smooth fields or the liquid dual object; the comparison is extension of the canonical smooth-density inclusion.

**Source check:** In §4.2.1 (printed pp. 61–62), Costello–Gwilliam identify the symmetric homogeneous smooth polynomial kernels and distributional polynomial kernels, and Lemma 4.2.1.1 states precisely that their inclusion is a **smooth cochain homotopy equivalence**. Their B.10 Atiyah–Bott/Tarkhanov elliptic comparison supplies the analytical input. It is inappropriate to replace this with a claim that every continuous linear map is automatically smooth between unrelated differentiable spaces. Here the plot structures and smooth maps are the actual ones from convenient compact-support test functions and distributional DVS.

The source's smooth inverse and chain homotopies need not commute with **every** extension-by-zero map; only the original comparison is required to be natural. That is what 024 uses.

## II. Exact B.6 filtration/fibration audit

In the **classical polynomial arity completion** $\prod_n\mathrm{Sym}^nL_{\mathrm{sm}}(U)$, every $F^N$ is a product of the arities $n\ge N$, with inherited product plots. Finite-weight quotients are smoothly split finite products. Therefore:
 
1. Their tail inclusions are *differentiable cofibrations* in the precise induced-plot sense of B.6.0.7, not merely algebraic injections.
2. The projections to smaller finite prefixes are differentiable fibrations, split at the level of differentiable cochain complexes.
3. For each fixed weight cutoff $k$, finite quotient towers stabilize once the stage index exceeds $k$.
4. The kernel comparison of one successive projection is exactly the smooth homotopy equivalence of homogeneous arity $n$ from Lemma 4.2.1.1.

These directly verify **all three** hypotheses of B.6.0.11. The resulting complete differentiable pro-cochain comparison is a weak equivalence **in every cohomological degree**; it does not require an unsupported commutation of all cohomology with general inverse limits.

## III. Independent higher-cohomology check on a connected interval

For compactly supported $g$ on an interval, the equation $f''=g$ has a compactly supported smooth solution **if and only if**

$$
\int g\,dx=0,\qquad\int xg\,dx=0.
$$

When the two moments vanish, $f(x)=\int_{-\infty}^x(x-t)g(t)\,dt$ is a compactly supported smooth solution. Conversely, integration by parts shows the moments vanish for every second derivative, and a compactly supported affine function is zero. The moment map has a smooth finite-rank splitting using two small bumps with independent moments. This yields an actual smooth contraction of the two-term observable complex to a two-dimensional vector space in cohomological degree zero.

The completed projective tensor and graded symmetric functors preserve a **specific smoothly split contraction**, by tensoring its homotopies and averaging over the finite symmetric groups. Thus classical regular polynomial observables on the interval have no cohomology outside degree zero, and their degree-zero cohomology is $\mathrm{Sym}(\mathbb R^2)$; the arity-completed version has $\mathbb R[[a,b]]$ in degree zero. The smooth-to-distributional comparison has the same outcome in **all degrees**, via Lemma 4.2.1.1.

The result is about the actual field-observable complex, not higher $\mathrm{Ext}^q_{\mathrm{Liq}_p}$ of the earlier fixed liquid source.

## IV. Adversarial Weiss Čech audit

The key Weiss property is **not** ordinary single-point coverage. For every tuple $(x_1,\ldots,x_n)\in U^n$, one Weiss member contains **all** its coordinates; hence the same-index product opens $U_i^n$ cover the complete space $U^n$. Intersections obey $(\cap_iU_i)^n=\cap_i(U_i^n)$.

The homogeneous regular observable kernels are compactly supported sections of a finite-rank graded bundle on $U^n$, modulo an exact finite graded symmetric-group action. A locally finite partition of unity on $U^n$ gives the augmented Čech resolution of these kernel spaces, with continuous linear/smooth maps on locally uniformly supported parameter families. Although multiplication by a cutoff does not generally commute with the kinetic differential $\partial_x^2$, the Čech resolution is exact in each kernel cochain degree. Its total double complex is a quasi-isomorphism by filtration in the bounded internal cohomological degree at **fixed** arity. This is the correct argument, not a false claim that the individual partition homotopies commute with $\partial_x^2$.

For arity zero the augmented nerve of a Weiss cover is acyclic: any finite family of nerve simplices has finitely many chosen points in their intersections; Weiss coverage gives one new open meeting **all** those intersections, thereby coning off the finite nerve subcomplex. Thus even the constant-unit weight is controlled.

Completing the Čech direct sums **after** finite arity quotients is mandatory under B.6.0.8. The split-arity tower and the established kernelwise comparisons invoke B.6.0.11 to obtain completed differentiable Weiss descent, with no illicit replacement by a naive support colimit.

## V. Free BV differential and honest quantum boundary

On **smooth smeared** polynomial kernels there is a well-defined continuous/smooth odd BV second-order operator, contracting even–odd generator pairs with the **local integration pairing**. Since $\partial_x^2$ is formally self-adjoint, the two odd differential operators $d_{\mathrm{cl}}$ and $\Delta_{\mathrm{BV}}$ anticommute; the BV operator also squares to zero. Hence

$$
d_{\mathrm q}=d_{\mathrm{cl}}+\hbar\Delta_{\mathrm{BV}}
$$

is a true differential on $A(U)[[\hbar]]$, $A(U)=\bigoplus_n\mathrm{Sym}^nL_{\mathrm{sm}}(U)$.

For disjoint opens the **cross** BV pairing vanishes, so the graded symmetric product of extension-by-zero images is a cochain map and obeys the factorization associativity/symmetry axioms. At each finite $\hbar$ quotient all operations are smooth finite sums of compact-kernel multilinear operations. In the complete limit, coordinatewise smoothness proves B.6.1.1. Filtration tails and quotient fibrations are smoothly split **as graded differentiable spaces**; the splitting need not be a cochain map, which is not required for these fibrations.

On the associated graded for the filtration in $\hbar$, the quantum differential reduces exactly to the classical differential. For every Weiss cover the corresponding kernel of the Čech-to-value map at each successive $\hbar$ truncation is precisely the classical Weiss comparison, already a differentiable quasi-isomorphism. The quotient towers stabilize modulo each fixed power of $\hbar$. The B.6.0.11 fiber criterion therefore proves quantum Weiss descent in **all cohomological degrees** for this *formal smeared free BV model*.

A second higher-degree check uses the interval's classical cohomology concentrated in degree zero. Induction over finite $\hbar$ quotients shows no other cohomology; the degree-zero tower is surjective and has vanishing $\varprojlim^1$. The quantum inverse limit thus also has no cohomology outside degree zero. This conclusion **does not** require or imply that the BV quantum differential is a derivation at the same open, or that same-open classical multiplication survives on quantum cohomology.

**Fatal forbidden shortcut:** Distributions supported on the diagonal do **not** generally admit unrestricted BV contractions. The classical map from smooth polynomial kernels to *all* distributional polynomial kernels has no automatic quantum lift. The proof's quantum model uses smooth smeared coefficients only.

## VI. Independent finite regression review

The bounded exact fixture [024](fixtures/check_free_scalar_bv_weiss_024.py) checks the symmetric kinetic operator and free BV model with exact rational arithmetic. Its reported controls include 108 basis monomials with $d_{\mathrm{cl}}^2=\Delta_{\mathrm{BV}}^2=d_{\mathrm q}^2=0$, 36 disjoint factorization Leibniz identities and 1,554 finite Weiss tuple-containment checks. None can certify an infinite-dimensional analytical statement. The smooth kernel proofs, B.6 source axioms and partition-of-unity argument do that work.

## VII. Accepted conclusion and the separate open bridge

**ACCEPT within this precise setting:** the actual one-dimensional free real scalar has a smooth classical polynomial regular-to-distributional homotopy comparison, a complete differentiable pro-cochain comparison across formal arity, an all-cohomological-degree local result on connected intervals, and a **formal smeared free BV quantum** differentiable prefactorization algebra satisfying completed Weiss descent.

**DO NOT ACCEPT outside that setting:** a natural equivalence between the differentiable observable complexes of 024 and the entirely different real-liquid derived Hom functors of [022](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md), or a higher-degree liquid Ext support theorem, or interacting/renormalized QFT. In 022 the mapping object is $\mathrm{RHom}_{\mathrm{Liq}}(\mathrm{Sym}^wH,G)$, whereas in 024 the field observable kernels represent smooth multilinear functionals on a smooth **field space**. These objects have different variances and no constructed canonical comparison. The mathematical next step is to define an explicit functor/intertwiner, with a source and target on **both** sites and a compatibility proof, or exhibit a precise no-go obstruction.

**Audit verdict:** bounded free-model statements accepted; the actual liquid-to-DVS bridge and generalized higher derived/QFT claims remain OPEN.
