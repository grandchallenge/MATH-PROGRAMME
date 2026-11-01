# EXT-015 REACH / 121 — critical review of the admitted parameter-descent counterexample

**Disposition: the negative parameter-descent result is justified on the stated admitted family class.** The source curve is smooth in one fixed complete R1 graph space, its output is an actual joint analytic family, every evaluated slice is rapid, and its evaluated derivative is not rapid in any fixed Sobolev order. The scale-connection conclusion has the stated weight-one typing. One compact-localization clarification is requested before final corrected-source readback. This does not reject the connection on the retained joint-family quotient or the controlled R1 image, and does not close M5/R4.

## 1. Frozen identities and provenance

| Artifact | Exact identity |
| --- | --- |
| Primary frozen commit | ead6559df63e2b75d49d19abcf1136d1cd3a9451 |
| Primary frozen branch | `research/reach-parameter-descent-primary-frozen-20261101` |
| Primary120 | 732f08956e18f90cf79cab0e51fe816d546fd602 |
| Primary122 draft | 38a46456c64429e551018a4a4f53b6b751020f71 |
| Scientific input cut | ada64e23c6a6535b3b4847773521d20a4e387858 |
| Scalar stages105 | a8ce66ff0edec33e2aff299550fca2089d671033 |
| Mixed source108 | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Quantum source111 | b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| Unit source114 | ee4bfb46c5565b90d6f9015765edc8a773b0997a |
| Corrected comparison117 | e95b1155ebb2018a80d2dc559560730fd7ea6594 |
| Comparison critic118 | b712e319927dd4464b83f9d635cfb35ed6121c0b |
| Comparison ledger119 | 865e16fd2970bd30d17e3852d2a0badf5598fa0c |

Read-only byte hashing verifies both actual primary files and all twelve dependencies in `parameter-descent-input-manifest.json`. The reviewer did not author120. Earlier critics106/109/112/115/118 are this reviewer's shared reviewed dependencies. The parent is an author of120, having written it after the delegated construction role ended before writing files; that failed role return is not treated as a completed source or review. Parent and construction context jointly supplied the mathematical mechanism. This is distinct same-system nonauthor scrutiny, not external independent certification. No Git invocation, Python, tracker or external mutation is used in this review.

## 2. Inference matrix

| Critical inference | Verdict | Exact control |
| --- | --- | --- |
| Centre-only cone is R1-admissible | Justified | Physical covectors $(1,1)$ avoid the pair conormal $(1,-1)$, also at the zero parameter |
| One fixed $E_{2,K,\Gamma}$ contains the whole smooth curve | Justified | Positive-power bounds in the mollifier width for every graph seminorm and logarithmic width derivative |
| All parameter derivatives at zero | Justified | Linear delta term plus a graph-topology flat remainder |
| Scalar Schwartz profile is admitted | Justified with the stated compact localization | One fixed scalar stage, all moments zero, nonzero normal profile retained by105/108 |
| Actual joint source family120.6 | Justified | Smooth coefficient curve in one complete stage, fixed scalar stage and proper physical projection |
| Every fixed-parameter slice is rapid | Justified | Arbitrary Taylor depth for every regulator derivative; no uniformity in the parameter is asserted |
| Derivative formula and density factor two | Justified | Actual projection of the centre delta, with unit centre/difference density determinant |
| Every finite Sobolev order detects the derivative | Justified | Nonzero annular Fourier mass and a rapidly negligible cutoff error |
| Nonzero class in the actual liquid quotient | Justified | Any rapid lift over a cover of the point would contradict that same fixed-order lower bound |
| Evaluation kernel is not derivative invariant | Justified | A zero evaluated section has nonzero evaluated derivative; the obstruction persists locally |
| Specified scale connection fails to descend | Justified | Even output weight one has no pair contraction, so its connection is the parameter derivative |
| Lifted or controlled-image connection fails | Not asserted and not implied | The null relation upstairs is uniform mixed-jet rapidness, not pointwise rapidness |
| Full M5/R4 or original R3 verdict | Not supplied | Only the exact evaluated-family intertwining diagram is refuted |

## 3. One fixed complete source, including all parameter derivatives

The change of variables has absolute determinant one. The fixed source cone contains only centre covectors; in physical coordinates their two components have the same sign and magnitude. The only nonzero collision conormal in arity two has opposite components. Thus the cone has a uniform separation from the forbidden conormal, including where the mollifier collapses to a centre delta. There is no need to enlarge the cone or escape its source space near zero parameter.

For each logarithmic width derivative, the Fourier functions in120.3 are bounded by a constant times the minimum of the frequency magnitude and one. The first vanishes at zero because the mollifier has integral one; all later ones vanish there because they are logarithmic derivatives. With the stated fractional exponent, the weighted one-dimensional integral for the centre frequency is finite. The Schwartz transform of the fixed relative cutoff controls the remaining frequency. This gives the stated positive power of the width in the global negative Sobolev norm.

The off-cone argument also has the required rate. After a physical localization, subtract the value at the centre origin. For the higher logarithmic width derivatives the rescaled compact profile has integral zero, so the same subtraction is legitimate. The mean-value estimate supplies a positive width factor and one finite centre-frequency loss; arbitrary integration by parts in the relative variable supplies decay. Off the centre cone, that relative frequency is comparable to total frequency, so it absorbs every requested graph norm. Smoothing remainders of the fixed pseudodifferential cutoffs obey the corresponding localized finite-seminorm bound. No unrestricted claim about all distribution-valued smooth curves is used.

The width $e^{-1/a^2}$ turns every positive width power into a function flat in the parameter. Its logarithmic derivatives and their further parameter derivatives lose only finite powers of the parameter. Thus the difference between the coefficient curve and the linear curve $a\delta(c)\chi(t)$ is flat in every seminorm of the same Fréchet space, with the same conclusion for every parameter derivative. The stated smooth extension and its derivatives at zero follow. In particular the example does not rely on choosing a new Sobolev order for successive derivatives.

## 4. Actual source admission rather than pointwise moderation

The annular Fourier choice gives a nonzero real even Schwartz profile and all of its spatial moments vanish. This is a required retained normal-profile input of the earlier plan and accepted scalar/mixed stages, not an arbitrary element of the larger auxiliary-noise envelope. Its regulator-normalization and complementary-face tails are exactly those admitted by105/108.

The fixed coefficient curve tensored with this one scalar stage is a smooth curve in the complete mixed source. The admitted multiplier/projection map therefore supplies uniform joint source and graph-jet bounds for every mixed parameter/regulator derivative. This is much stronger than membership of each parameter slice in the target analytic image. Large pointwise heights of the narrow mollifier do not contradict those bounds: the single negative Sobolev norm and its fixed-cone graph estimates control the coefficient uniformly, while the scalar-source operator has only finite regulator losses.

For complete source typing, explicitly insert a fixed scalar physical cutoff equal to one on a neighborhood of the common source support $K$. That localized scalar factor belongs to the compact scalar105 stage. Its product with the coefficient curve, and with all its parameter derivatives, is unchanged. The draft already invokes compact physical localization, so this is an explicit representation clarification rather than a defect in the counterexample. Suppressing this harmless cutoff in120.6–120.10 is valid once it is named.

The projection forgets one physical vertex and is proper on the common support. It is a defining analytic-source operation; it is not being called a weight-preserving quantum cochain map from the two-vertex coefficient space. No illegal delta self-trace or overlapping singular counterterm product occurs.

## 5. Pointwise rapidness versus its nonrapid derivative

For a fixed nonzero parameter, the centre coefficient is a compact smooth function. Taylor-expand the smooth relative-variable factor to arbitrary order. Every polynomial term pairs to zero against the profile's moments. The relative cutoff changes the uncut pairing only by Schwartz tails away from the origin. Spatial derivatives give the same estimate. Each regulator derivative has a Schwartz rescaled profile with all moments still zero, together with a finite extra inverse regulator power. Increasing the Taylor order absorbs that power. Compact output support then gives rapidness in a fixed spatial norm for every regulator derivative. Constants may depend on this fixed parameter; the proof never upgrades them to uniform rapidness near zero.

At zero parameter the coefficient curve itself is zero. Thus every evaluated parameter value is the zero enriched class. This is precisely the kernel relation tested by evaluation.

Differentiation of the admitted continuous source map is legitimate by the fixed-stage smoothness. Its source derivative is the centre delta times the fixed relative cutoff. Projection sends $t$ to $x=t/2$ there, so its density is twice the displayed rescaled profile. Equivalently, integrating the relative-variable delta in120.7 has that same factor. The factor two is necessary and correctly retained.

The Fourier transform of the uncut derivative is the profile transform at the rescaled frequency shown in120.11. Its annular support is bounded away from zero, so the Sobolev weight is uniformly comparable to the stated power at every finite real order. The integral is strictly positive. The physical cutoff changes this norm only by a term rapid in every Sobolev norm, including every regulator derivative. Triangle inequalities preserve a lower bound of the stated finite power. No fixed finite negative Sobolev order can make this curve rapid to every order.

This also proves nonzero in the actual liquid quotient. A vanishing class would admit a rapid lift locally after a nonempty extremally disconnected cover of the point. Restricting such a lift along any point of that cover would make this same scalar-valued physical distribution curve rapid in one finite order. The lower bound excludes every such order. The argument uses concrete actual lifts, not a point-detection principle for an arbitrary liquid internal Hom.

## 6. The failed diagram and the scale connection

Parameter differentiation is already well-defined on the retained joint-family quotient because its null ideal requires all uniform mixed jets. The constructed section has zero point evaluation but its differentiated section has a nonzero evaluation at the zero parameter. Hence the evaluation kernel is not derivative invariant. A linear derivative on the evaluated rule intertwining the two maps would have to send the zero section to that nonzero derivative, an impossibility. The same construction exists on every sufficiently small parameter neighborhood of zero, so sheafification cannot remove the defect.

The related nonclosed-source statement is valid but is not used as a substitute for that derivative witness. Every fixed smooth centre mollifier maps to a rapid output and those mollifiers converge in the same complete source to the centre delta, whose output is not rapid. The preimage of the rapid ideal is therefore not closed. Completeness of the source cannot supply the missing closed-kernel theorem. The smooth flat-width curve proves actual derivative failure, which nonclosedness alone would not establish.

Put the parameter into a positive scale interval as stated. Choose the output slot even and total weight one. The nonnegative quantum convention leaves no other arity/power choice at that weight, and the even two-even scale contraction has no pair to contract. Its connection term is exactly zero. The specified upstairs scale connection is therefore the parameter derivative on this example, and its descent through evaluation fails by the same nonzero class. A pointwise linear correction of the zero evaluated input cannot fix that intertwining equation.

This is not an error in the fixed-scale transport maps or their cocycle. Nor is it a failure of the connection on the joint-family quotient. The counterexample is a nonzero joint-family class with zero evaluation, so it lies outside the controlled joint image of the R1 comparison, where117 proved evaluation faithful. Its evaluated point map is zero, but that does not turn this nonzero joint lift into the controlled zero lift. Thus the prior controlled-image result is preserved.

## 7. Exact negative scope and remaining obligations

The result refutes the exact parameter-differentiation and specified scale-connection descent through117's evaluated plot rule on all admitted joint families. It supplies a source-admitted example even with one fixed complete coefficient graph space and one fixed scalar stage. It is not an ambient moving-bump argument with unproved membership, an escaping-index construction or a parity-vacuous control.

It does not assert membership in the smaller algebraic span of raw finite Gaussian-polynomial graphs. The declared analytic class intentionally includes the full Schwartz normal sector, including the chosen moment-flat profile. Removing that admitted input would be a different domain choice. No failure of the smaller raw span is inferred here without its own membership proof.

The result does not prove that every Costello–Gwilliam differentiable sheaf is point-determined, that the retained joint-family quotient cannot carry its existing connection, or that every alternative parameter target is impossible. A later audit of the actual differentiable-sheaf/liquid interfaces must keep the nonzero evaluation kernel and test those actual definitions; it cannot silently identify the retained object with point-valued plots. Extended completed Weiss descent and the remaining lifting and comparison obligations stay open.

Accepted R0/R1/R2 and separate087–089 scopes are unaffected. Original R3's degree-two support equation and its two residual channels remain independent. This evaluation kernel is not a reserved R3 syzygy. One bounded negative M5 result does not close full M5/R4 or either parent programme.

## 8. Correction and final readback

The primary mathematical assessment is complete. The counterexample and its negative diagram are accepted under the stated compact-localization convention. The requested single clarification should name that fixed scalar cutoff, suppressing it in formulas only because it is one on the common source support. After exact corrected-source readback, this report will bind its final disposition to the actual120 blob. No further mechanism or construction cycle is requested. Source preflight, editorial integration, protected admission/readback and tracker reconciliation remain separate events. Only121 has been written in this pass; no Git invocation, Python, tracker or external mutation was performed.
