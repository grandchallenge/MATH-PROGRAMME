# EXT-015 REACH / 196 — source-locked critical review of the conic joint-defect construction

**Overall verdict on the frozen primary: CORRECTION REQUIRED.** The microlocal split and the two proposed source histories survive the present attack. The decisive all-corner scalar estimate is not yet stated with sufficient precision to accept Lemma195.1. One consolidated author correction must separate the actual localized smooth heat contribution from its finite Taylor polynomial, and carry the resulting differentiated estimates explicitly through the remaining three-vertex collision charts. This review identifies a repairable proof gap, not a counterexample to the proposed source membership.

## 1. Source, scope and review provenance

The reviewed primary is [JOINT_DEFECT_SOURCE_AUDIT_195.md](JOINT_DEFECT_SOURCE_AUDIT_195.md), frozen commit `160395b9d5d2e060ebec5dc1519fa55b4fef9534`, Git blob `0d9574214d8026f62a8b148d278eae19008df153`, on `research/reach-joint-profile195-primary-frozen-20261115`, with input `80e3288b06aacfa900e95e8f45f10b144952cf75`. Direct computation of the Git blob hash from the actual file bytes agrees with that identity. The current durable checkpoint is CP215, which records the CP214 construction assignment and this review-pending source cut. No Git or GitHub mutation was used in this review.

The actual contracts read were protocol090, scalar105, completed mixed108, parameter126, first/second cores165, second-arm168, no-hidden171, hidden-bridge174, zero-energy192 and critical193. The full collision geometry096 was consulted for the remaining partial faces. The criterion is the existing general fixed-index scalar power/logarithmic sector105.5 and the finite completed source image108.6–108.7. It is not the larger auxiliary-noise envelope105.2 and is not a finite-raw-Gaussian formula criterion.

This is a distinct nonauthor agent context. The parent contributed the proposed mechanism to the producer and did not perform this review in place of the critic. Producer, parent and critic share the Codex system and historical protected dependencies. This is neither external mathematical certification nor an independently authenticated referee approval. No numerical experiment or Python execution is needed for this analytic review.

## 2. Critical inference verdicts

| Inference in195 | Verdict on this frozen source | Reason and boundary |
| --- | --- | --- |
| Exact Fourier symbol195.6 | ACCEPT | Away from the frequency axis, the equation $e''=\delta_0$ gives $\widehat e=-\xi^{-2}$. The multiplier vanishes in a neighborhood of that axis, killing every distribution supported there. The low-frequency cutoff is retained exactly. |
| Point singularity and associated-homogeneous logarithm195.8–195.10 | ACCEPT | The angular symbol is smooth because its support avoids $\xi=0$. Radial finite part at critical degree $-2$ in dimension2 has a scaling anomaly supported at frequency zero; inverse transformation gives the displayed constant logarithm. The compact-frequency difference is smooth with polynomial growth. The chosen finite part, rather than an arbitrary extension with uncontrolled scaling, is the one used here. |
| Smoothness and inverse-regulator moderation of the partial heat smoothing | ACCEPT | On the high-frequency support, $|\eta|$ is bounded below by a positive multiple of $|(\xi,\eta)|$. Gaussian damping in $\eta$ therefore controls every differentiated Fourier integral. The low-frequency distribution has compact support. The smooth correction $G$ has the stated polynomial growth and ordinary differentiated heat estimates. |
| Exact smooth front profile195.11 | ACCEPT | Associated homogeneity and Gaussian mass one give the exact scaling law. The conic Fourier estimate makes $F=H_1$ smooth, including at $R_1=0$. This avoids introducing a positive-scale cusp as a scalar coefficient. |
| Uniform strict-annular expansion195.12 | CORRECTION REQUIRED | The phrase “local smooth heat Taylor part” does not specify whether the subtracted object is the actual localized heat convolution or its finite Taylor polynomial. The latter interpretation makes the claimed rapidness false. The negative-order rapid estimate and the positive-norm moderation must refer to the same actual separated contribution. |
| Strict/front compatibility195.13 | CONDITIONAL | The exact scaling identity is correct. Its use as a full corner theorem requires the corrected uniform differentiated annular estimate, with regulator-derivative losses stated. Leading coefficients or pointwise Taylor expansions do not suffice. |
| Further partial-collision blowups and one fixed105 stage | CORRECTION REQUIRED | Smooth angular coefficients are promising, but the source currently compresses the pullback of all remainder seminorms into a sentence. The correction must display the local b-vector-field changes and the resulting uniform weights at the extra faces. |
| Good R1 coefficient195.14 | ACCEPT | At $x=y=0$, the removed high-frequency cone contains an open neighborhood of the forbidden opposite covectors. Away from that point the remaining singularity has pure $y$ covectors at $y=0,x\ne0$. Compact localization preserves this exclusion. In three slots, the zero $z$ covector reduces the only possible forbidden cases to the $x=y$ block and full coincident block, both already excluded. |
| Pure-anchor R1 coefficient195.16 | ACCEPT | A nonzero pure $h$ covector cannot have zero sum in the collision block containing $h$. It therefore avoids every nonzero partial-partition conormal. |
| Proper densities and exact sum195.15–195.18 | ACCEPT, conditional only on scalar admission | Delta pairing has coefficient one and the difference coordinates introduce no integration determinant. Fixed compact decorations make the forgetting maps proper. The same $\eta_0$ occurs in both summands, so low-frequency and cutoff corrections cancel exactly. |
| Completed tensor sources108.6 | ACCEPT, conditional on Lemma195.1 | Two simple tensors in fixed complete stages require no escaping indices or finite-separable expansion of a completed element. Existing108 evaluation continuity is the relevant completion mechanism. |
| Source-controlled126 rows | ACCEPT in the stated cutoff families, conditional on the scalar seminorm proof | Fixed-support cutoff variation differentiates actual coefficient tensors in fixed histories. This supplies within-row coefficient identities and cross-row entire evaluations. It does not prove arbitrary output families lift, nor full126.14. |
| Membership of $D$ and the particular165/168 outputs | CONDITIONAL | Subtraction from the admitted $\widetilde A$ gives $D$ once $A$ is admitted. The already reviewed165/168 reductions then give the stated particular labelled and symmetric outputs. No general Green inverse follows. |

## 3. One consolidated correction request

The sole correction should replace the ambiguous strict-annular argument and expand its further-face consequence. No source enlargement, new operation, cutoff-dependent conic partition or change to the rapid ideal is requested.

First, on a fixed output annulus, explicitly choose an input point cutoff and define two **actual** partial heat convolutions: a compact point-singular contribution and the smooth complementary contribution. The cutoff must make the Gaussian argument uniformly separated from zero wherever the point-singular contribution is nonzero on that annulus. Its smooth complement must be a globally smooth input on the relevant compact $r$ sets, with polynomial growth in the heat integration variable. State their exact sum before performing any Taylor truncation.

For every fixed regulator derivative, prove that the compact point contribution is rapid in one fixed negative Sobolev order, independent of the requested rapid power. Its polynomial positive-Sobolev bounds should follow by subtracting the **actual smooth heat convolution** from the already moderate whole $H_\epsilon$. Interpolation then makes this same point contribution rapid in each requested positive norm. The finite Taylor remainder of the smooth heat convolution is a different object and has only the prescribed finite-order bound. In particular, a nonzero coefficient at the next heat order would give $\epsilon^{2N+2}$ after truncation and cannot be called rapid.

State the combined estimate explicitly. With $T_N$ denoting the truncation through heat order $N$, an acceptable target is a uniform annular bound of the form

$$
\left\|\partial_\epsilon^k\bigl(H_\epsilon-T_N\bigr)\right\|_{C^m}
\le C_{N,k,m}\epsilon^{2N+2-k},
\tag{196.1}
$$

with the corresponding physical derivatives and $\epsilon\partial_\epsilon$ estimates, and with the separated conormal term separately rapid at every power. The right side may become a weak bound when $k>2N+2$; sufficiently deeper truncations must give every requested finite ordinary derivative and hence smooth extension of the scaled annular heat family to its strict face. Constants must be uniform over the complete angular annulus, including $r=0,s\ne0$, and over bounded fixed-support cutoff families.

Second, pass to the full-origin chart

$$
r=a\omega_r,\qquad s=a\omega_s,\qquad \epsilon=a\sigma.
\tag{196.2}
$$

Show that the corrected remainder bounds hold under all finite products of $a\partial_a$, $\sigma\partial_\sigma$ and angular derivatives, with the $c_0\log a$ term kept separately. Ordinary regulator derivatives have their actual finite factor $a^{-k}$ in this chart; they must not be silently assigned unchanged scalar indices. Smooth physical cutoffs have their ordinary Taylor expansions in $a$ and should be included in the same estimate.

For each remaining pair-collision direction choose an angular coordinate $v$ vanishing on the corresponding line $r=0$, $s=0$ or $r=s$. The three line directions are separated after blowing up the full origin. The additional local blowup is therefore the blowup of $\{\sigma=v=0\}$ at one direction at a time. The correction should exhibit, for example, the following two local chart changes and their action on the controlled derivatives:

$$
\begin{array}{lll}
\sigma=\tau,\ v=\tau V:
&\tau\partial_\tau=\sigma\partial_\sigma+v\partial_v,
&\partial_V=\sigma\partial_v,\\
v=\pm\tau,\ \sigma=\tau S:
&\tau\partial_\tau=\sigma\partial_\sigma+v\partial_v,
&S\partial_S=\sigma\partial_\sigma.
\end{array}
\tag{196.3}
$$

The common radial derivative $a\partial_a$ persists. In the second chart, a uniform $O(\sigma^L)$ remainder becomes $O(\tau^L S^L)$; the first chart has $O(\tau^L)$. Use these identities, or equally explicit smooth-extension estimates, to justify every new coefficient/remainder seminorm. A bare assertion that a smooth leading angular coefficient pulls back smoothly is insufficient for the remainder. The fixed nonnegative integer saturation, logarithmic degree bound, and one auxiliary lower-weight vector strictly below zero should then be identified on all faces, including recursive coefficients. Fixed compact center decorations and their derivatives must remain covered.

These items form **one consolidated correction**, not a request for successive new mechanisms. The exact two-history equality should remain unchanged. The corrected primary must be frozen and rereviewed before any affirmative scientific disposition.

## 4. Hostile controls and decision boundary

The proposed construction does not contradict171: each history has a forgotten physical vertex. It does not contradict174: the bad history has genuine retained-output relative scalar dependence and is not a terminal single Gaussian bridge with an effective R1 input independent of retained $z$. Nor does192's static-target argument exclude this nonterminal general105 scalar. These are actual hypothesis differences, not cancellations assumed to bypass a prior exclusion theorem.

The source bounds are needed in the complete105 topology, not just on compact positive-regulator intervals. Exact equality195.18 would make the equality defect zero under every mixed derivative and every unchanged rapid seminorm; no Gaussian inverse or weak-to-rapid inference is needed. The nonzero order-two test coefficient of $D$ remains nonzero, so admission of a source would not make the defect rapid or identify it with zero in the enriched boundary.

**Decision at this frozen source: CORRECTION REQUIRED; $A$ and $D$ are not yet accepted.** All other attacked components have the bounded dispositions in section2. Universal150.L, residual $W$ acyclicity, originalR3, full126.14, higher weights, actual lifting and M5/R4 integration remain OPEN. Editorial integration, protected admission and exact-main readback are separate from this source-bound scientific review.

## 5. Exact corrected-source rereview and final scientific verdict

**Final verdict: BOUNDED ACCEPT after the sole consolidated author correction.** Sections1–4 above preserve the initial CORRECTION REQUIRED disposition on the original primary; they are not the final disposition of the corrected source identified here.

The rereviewed source is exact corrected commit `3d6494ebee0fc2fb4044cdc879322d466f17adee`, branch `research/reach-joint-profile195-corrected-frozen-20261115`, Git blob `fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0`. Direct computation of the Git blob hash from the current file bytes agrees with that exact blob. The primary correction request remains preserved at commit `6c395353bcb36eb786df0260da649ceceaf1602d`, branch `research/reach-joint-profile195-primary-review-frozen-20261115`. The rereview uses the same actual105/108/126 contracts and the same distinct nonauthor context and same-system provenance disclosed above. No Git/GitHub mutation, numerical fixture or Python execution was used by this critic.

The following are the exact requested repairs and their corrected-source dispositions.

| Requested obligation | Rereview verdict | Corrected-source evidence and critical check |
| --- | --- | --- |
| Separate actual heat convolutions before truncation | PASS |195.12a defines $H_{\rm sm}$, the actual smooth heat family $S_\epsilon$, and the actual compact point contribution $Z_\epsilon$, with exact equality $H_\epsilon=S_\epsilon+Z_\epsilon$. The point cutoff is fixed and its support radius is strictly smaller than the output annulus. |
| Smooth heat input and all differentiated Taylor estimates | PASS |195.12b is the ordinary differentiated integral for a globally smooth input with polynomial growth. Gaussian moments justify every mixed derivative and a signed smooth even extension through zero. On the output annulus this input equals $H$, so195.12 is its actual Taylor polynomial. |
| One fixed weak order for all rapid powers | PASS | On the nonzero support of $Z_\epsilon$ in the annulus, $r$ is small and $s$ is separated from every input $t$. Every differentiated kernel multiplier is exponentially small with only a fixed inverse-regulator loss. Compact distribution order and proper partial projection give195.12c with $t_k$ independent of $L$. Annular localization and physical derivatives incur fixed additional orders only. |
| Interpolate the same actual contribution | PASS | The positive norms are obtained from the exact difference $Z_\epsilon=H_\epsilon-S_\epsilon$, using the conic Fourier bounds for the first term and the actual smooth integral for the second. Thus195.12d follows for $Z_\epsilon$ itself. No finite Taylor polynomial is substituted in this subtraction. |
| Keep finite-order Taylor remainder distinct from rapidness | PASS |195.12e has the correct loss $2N+2-k$ after $k$ ordinary regulator derivatives. For deeper derivative requests one takes a deeper truncation. The corrected source explicitly limits rapidness to $Z_\epsilon$ and gives only a finite Taylor bound for $S_\epsilon-T_N$. |
| Uniform annular/angular estimates, including $r=0,s\ne0$ | PASS | The fixed point cutoff and separation work uniformly on the complete compact annulus. Positive-norm interpolation and195.12b supply every ordinary derivative there. Therefore the scaled annular family is actually smooth up to $\sigma=0$, with195.13a and all angular derivatives; this is stronger than a leading-coefficient assertion. |
| Full-front radial and ordinary derivative bookkeeping | PASS |195.13 retains $c_0\log a$ separately.195.13a controls the remainder independent of $a$, while195.13b–195.13c retain the actual $a^{-k}$ regulator and $a^{-1}$ physical derivative factors. Smooth decorations and the smooth $G$ heat term have their genuine Taylor/remainder estimates in these same charts. |
| First additional pair-collision chart | PASS | Under $\sigma=\tau,v=\tau V$, the displayed vector fields are correct. Products of $\tau\partial_\tau$ and $\partial_V$ are controlled combinations of the original angular and $\sigma$ derivatives; the remainder is $O(\tau^L)$. Each finite coefficient becomes $\tau^{2j}c_j(\tau V)$ and has the asserted differentiated Taylor remainders. |
| Second additional pair-collision chart and its corner | PASS | Under $v=\pm\tau,\sigma=\tau S$, the displayed b-vector fields are correct. The remainder is $O(\tau^LS^L)$, and $k$ ordinary $S$ derivatives give $O(\tau^LS^{L-k})$. Finite terms are $\tau^{2j}S^{2j}c_j(\pm\tau)$. Taking $L$ and finite coefficient Taylor depth above the prescribed two face depths supplies all recursive corner remainders. |
| Further derivative poles | PASS |195.13e follows by differentiating at fixed physical $(r,s)$, hence fixed $(a,v)$: the first chart has $a^{-1}\tau^{-1}(\tau\partial_\tau-V\partial_V)$, while the second has $a^{-1}\tau^{-1}\partial_S$. The resulting finite integer stage shifts are retained rather than assigned unchanged lower indices. |
| Fixed indices, auxiliary weights and all remaining faces | PASS | The three pair lines have separated angular directions after the full-origin blowup; there is no unresolved intersection between two of their strict lifts. The corrected local charts and the smooth strict region cover the remaining centers. The undifferentiated indices $\mathbb N_0\times\{0,1\}$ contain every term, and the single vector $\mathbf b=(-1)_H$ absorbs the only retained logarithm also in recursive coefficient spaces. Ordinary derivatives pass to their computed shifted stages and fixed lower weights. |
| Continuity in the complete scalar topology | PASS | Each target coefficient/remainder seminorm uses a finite Taylor depth, finitely many cutoff derivatives, and finitely many uniform estimates just checked. This is a finite seminorm bound on fixed-support smooth decorations, including center derivatives. Neither the indices nor auxiliary weights depend on approximation, truncation requests or profinite parameters within a stage. |

The patch closes the two outstanding entries of section2: the strict-annular estimate is an estimate of the actual partial heat family, and the additional collision blowups preserve the full differentiated remainders. The smooth strict-face extension also directly confirms that no hidden nonsmooth angular coefficient is introduced at a further pair face. The only logarithmic anomaly is the one already retained at the full front; the subsequent charts leave its defining variable $a$ unchanged.

I therefore accept Lemma195.1 as membership of the particular scalar $B$ in one existing complete105.5 stage on the actual three-vertex relative collision space. I rechecked the unchanged coefficient cones, supports, proper densities and exact sum195.14–195.18 against this scalar admission. They give two legal finite original108.7 histories and an **exact source representative of $A$ before the rapid quotient**. Their two simple tensors lie in fixed completed108.6 stages; no source-index escape, arbitrary singular product or additional integration operation is required.

The continuous fixed-support cutoff maps give actual coefficient derivatives in those same histories. These supply the stated126 rows and their entire-family equalities, including the original cover-local semantics on profinite tests. This accepts the explicit parameter families in195, not recovery of all previously admitted families in126.14.

Subtracting this source from the admitted $\widetilde A$ gives an actual original source of $D$. Its exact joint profile and nonzero order-two test coefficient from192 remain unchanged, so $D$ remains nonrapid and its enriched-boundary class is nonzero. The equalities used in the source construction have zero equality defect under every mixed derivative. No inversion of a Gaussian, infinite delta-jet sum or inference from a weak limit is used.

The bounded consequences for the particular labelled and symmetric Green outputs follow from the already reviewed165/168 source reductions. The existence of these particular primitives supplies no continuous source-level antiderivative for arbitrary mixed histories. Both constructed histories have a forgotten vertex, and the bad scalar has retained-output dependence, so the hypotheses of the prior171/174/192 exclusions remain different.

**Final exact-source decision: ACCEPT195 at blob `fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0` within the stated fixed central test and explicit source-controlled parameter families.** One primary and one author correction were used. No further author correction is requested. Universal150.L, residual $W$ acyclicity, originalR3, full126.14, higher weights, actual lifting and M5/R4 integration remain OPEN. This logically distinct same-system scientific review does not supply external certification, editorial clearance, protected admission, exact-main readback or programme completion.
