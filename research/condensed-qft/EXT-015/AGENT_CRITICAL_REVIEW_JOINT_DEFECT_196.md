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
