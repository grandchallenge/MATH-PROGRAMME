# EXT-015 REACH / 034 — distinct mathematical critique of the singular extension and actual liquid syzygy reduction

**Role:** Non-authoring GCL mathematical critical pass, performed under the authenticated GCL identity with separate review and source-lock. This is not an external-referee certificate and does not create a second GitHub identity. **Reviewed source candidates:** [R2/032 PR #2805](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2805), exact candidate head 6cdb50f1ef59fd633dd5af02ffba40fe664f44c6; [R3/031 PR #2806](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2806), exact candidate head 38e2750c6155c81823d1ffbcf9114e23e4b8867a. Actual prior category/source: protected review [016](AGENT_CRITICAL_REVIEW_AB_016.md) and the original admitted real-liquid projective cover. This is a distinct hostile derivation of the mathematical facts, not merely a repetition of CI.

## A. Adversarial review of R2/032

Let $\chi\in C_c^\infty(\mathbb R)$ equal one near zero. The proposed pairing with $t_\chi$ is continuous because near zero its numerator is $O(|z|)$, with a uniform first-derivative seminorm bound. Any difference of extensions of $1/|z|$ is supported at zero. Point-supported distributions are finite sums of delta derivatives, with scaling degree $k+1$ for derivative order $k$.

**Independent scaling check.** For $\varphi$ supported in a compact annulus separated from zero, $\varphi(0)=0$ and the rescaled pairing of $t_\chi$ is $\lambda^{-1}$ times the same nonzero integral; therefore the scaling degree cannot be less than one. For a general test, the subtraction introduces a logarithm, of size $\lambda^{-1}|\log\lambda|$, which is less singular than any $\lambda^{-\omega}$ for $\omega>1$; hence the scaling degree is exactly one. The only point-supported correction preserving the bound is $c\delta$. This argument does not claim uniqueness without fixing the local renormalization constant.

**Independent scale-law check.** The difference $t_R-t_S$ is supported at zero. Differentiate its coefficient against $\log R$ and substitute $u=z/R$; integration of $\mathrm{sgn}(u)\chi'(u)$ yields $-2\chi(0)=-2$. Thus the relation is precisely $-2\log(R/S)\delta$, not a scheme-dependent unknown coefficient. The subtraction-scale cocycle is exact.

**Hostile limitations:** (i) if $\chi(0)$ were not normalized to one, the log coefficient would change; the submission does require normalization; (ii) the polynomial cutoff fixture is not $C^\infty$ at its boundary, as correctly disclosed, so the fixture is an algebra check only; (iii) the D14 atomic divergence $\kappa(0)/\epsilon$ is a *different* distributional problem, so scalar finite-part renormalization cannot certify a BV operator. The submission correctly refuses this inference.

**Verdict R2:** **ACCEPT within GB1 benchmark scope**, pending protected admission and independent source/claim classification. **REJECT** any promotion to GB2, interacting QFT, or a domain-wide counterterm operator without further mathematics.

## B. Adversarial review of R3/031

In the exact real-liquid projective presentation of review 016, the singleton generator of the summand indexed by $w\in E$ maps to $w$. Fix $v\ne0$. The relations $r_n=e_{2nv}+e_v-e_{(2n+1)v}$ therefore land in the kernel of the **actual** cover; no invented Fréchet realization occurs.

**Independent splitting check.** The countable coproduct $Q=\bigoplus_n\underline{\mathbb R}$ has a map $s$ to the kernel sending its $n$th basis to $r_n$. The map $q$ from the kernel to $Q$ is the restriction of the map on the projective cover that sends only the singleton generator labeled $2nv$ to the generator indexed by $n$ of $Q$ and all other projective summands to zero. Hence $qs(e_n)=e_n$ for every $n$; coproduct naturality gives $qs=\mathrm{id}_Q$. This is a split short exact decomposition **in the abelian real-liquid category**, and the summand is projective as a countable coproduct of singleton projectives. Consequently the higher Ext functors of the syzygy agree naturally with those of the complementary kernel for each positive degree and each target module.

**Independent hostile escaping map.** Choose target test functions $g_n$ with supports escaping every compact output stage. The coproduct morphism $j:Q\to G$ sends its $n$th basis to $g_n$. Its composite $j q:K_0\to G$ takes the relation $r_n$ to $g_n$, so no finite-stage factorization exists. However it extends to $P_0$ by $j\widetilde q$, and is therefore zero as a projective-cokernel Ext class of the original source. This is a **real liquid category** counterexample to the false slogan that an escaping syzygy representative implies a nonzero Ext obstruction.

**Hostile limitations:** (i) this split projective summand is deliberately constructed from redundant singleton relation generators in a highly nonminimal projective cover; the result is not claimed invariant for every possible minimal cover. What is invariant is the actual Ext group; (ii) the quotient/complement $K_0^{\mathrm{red}}$ is not proved Fréchet, compact, projective or relative-Ext-continuous; (iii) a vanishing Ext class is not a counterexample to the target Ext comparison. The claim is strictly a new simplification and an adversarial normalization rule.

**Verdict R3:** **ACCEPT the explicit split-summand and escaping-boundary theorem within the chosen actual 016 presentation**, subject to protected admission. **OPEN** the decisive first-Ext comparison for the complementary first syzygy, hence the degree-two comparison for the original test-function source.

## C. Disposition and next mathematics

| Obligation | Result |
| --- | --- |
| GB1 extension $1/|z|$ with scaling degree one and local delta freedom | ACCEPT, bounded benchmark |
| Exact renormalization-scale log cocycle | ACCEPT, bounded benchmark |
| Domain-wide renormalized BV and overlapping diagonals | OPEN |
| Split countably generated projective relation summand of actual liquid $K_0$ | ACCEPT, cover-dependent construction |
| Explicit escaping support map which is Ext-zero boundary | ACCEPT, hostile positive-control |
| True first-Ext output-stage comparison for $K_0^{\mathrm{red}}$ | OPEN |
| All higher liquid Ext / Costello–Gwilliam completed equivalence | OPEN |

**Next independent mathematical task R2:** generalize beyond the scalar finite part to **an operator on a specified singular BV jet domain**, accounting for every mixed-pair contraction, differential and nested collision. **Next R3:** obtain a concrete profinite-relation/projective presentation of the *complement* $K_0^{\mathrm{red}}$ and test support factorization modulo all boundaries. These are directly researchable and do not require user approval or another GitHub account; specialist certification and external mathematical claims remain governed.
