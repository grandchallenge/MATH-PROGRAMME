# QFT-COND-005 / EXT-015 — EXTENSION DOCKET

**Status:** OPEN ADVERSARIAL TEST REGISTER. The examples below are **not** assumed to exhibit genuine liquid Ext classes.

**Question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

## Common exact data

Coefficient category: $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$ at fixed $0<p\leq1$. The source is a **fixed** nuclear Fréchet realization $H$. Output stages $G_b$ form a strict compact-support LF sequence. Quotient $Q_b=G/G_b$ is computed in the abelian liquid category. A proposed extension class $\xi\in\mathrm{Ext}^1(H,G)$ is escaping **if and only if** each image $\xi_b\in\mathrm{Ext}^1(H,Q_b)$ is nonzero.

This definition concerns extension classes modulo liquid boundaries; it is not enough that a particular cocycle has large support.

## Docket entries

### E0 — finite-dimensional source (positive calibration)

**Input:** $H=\underline{\mathbb R^m}$. **Test:** prove directly from the free liquid generator whether $H$ is projective and check $\mathrm{Ext}^1(H,G_b)$ and $\mathrm{Ext}^1(H,G)$. **Trap:** do not assume projectivity from vector-space semisimplicity in the underlying real-vector-space category alone. **Outcome:** NOT RUN.

### E1 — rapidly decreasing sequences (analytic calibration)

**Input:** $H=\underline{s}$ with $s$ nuclear Fréchet. **Test:** build a genuine liquid projective presentation and classify degree-one extension classes into compact-support LF output. Compare carefully with DLI-011's *inverse limit* Roos obstruction; it is not by itself a target-colimit Ext witness. **Outcome:** NOT RUN.

### E2 — product jets and the Borel quotient (hostile transfer)

**Input:** $\mathcal D_{[-1,1]}(\mathbb R)\to\mathbb R^{\mathbb N_0}$, the continuous Borel full jet map. **Known:** finite jet sections exist; the full continuous section does not, yielding a nonsplit strict nuclear Fréchet extension. **Test:** Does the strict exact sequence become an exact sequence of liquid modules? If so, does it remain nonsplit by a liquid-linear map? Would a split in liquid imply a continuous linear splitting between those Fréchet realizations? Name exact hypotheses. **Trap:** do not conclude liquid nonvanishing solely from strict nonsplitting without checking exactness. **Outcome:** TRANSFER OPEN.

### E3 — principal test-function pair (primary target)

**Input:** $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$, $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$. **Test:** identify quotient stages and determine the degree-one filtered-colimit comparison. Seek a proof of eventual $\xi_b$ vanishing, or an escaping class with full nonvanishing proof. **Outcome:** OPEN.

### E4 — disconnected open (escaping spatial support)

**Input:** choose a countable union of disjoint relatively compact intervals as $V$, with an explicit exhaustion through finitely many components; fix one source compact support stage. **Test:** construct a candidate extension cocycle whose target components drift to infinity. Check whether a liquid boundary removes the drift. **Trap:** the identity on $\mathcal D(V)$ is a counterexample to **uniformity across varying source stages**, not a fixed-Fréchet-source extension class. **Outcome:** OPEN.

### E5 — auxiliary square-zero ring (negative logic calibration)

**Input:** DRM-014's square-zero algebra and split target inclusions. **Known:** degree-zero Hom comparison can be an isomorphism while the degree-one Ext comparison is not surjective. **Test:** use only to challenge invalid implications; never identify its modules with liquid test-function stages. **Outcome:** ESTABLISHED AUXILIARY CONTROL, NOT A LIQUID COUNTEREXAMPLE.

## Adversarial proof checklist

For any proposed counterexample record:

1. Exact site, coefficient category, source $H$, support exhaustion, quotient diagram and extension class.
2. A short exact sequence in liquid modules or a cocycle in a verified liquid projective resolution.
3. A proof that the class is not a boundary in the liquid category; the argument must consider **all** admissible liquid boundaries.
4. For every $b$, a source-grounded detection functional, map, or cohomological invariant proving $\xi_b\ne0$.
5. An explicit reason finite stage support cannot absorb the class. Pointwise escaped support for one representative is insufficient.
6. Exact distinction between a new result, a classical theorem and a bounded computational fixture.

For a positive theorem, dualize the checklist: prove that **every** class admits a finite cutoff and give an actual cutoff-producing argument, not only vanishing for selected examples.

## Review cautions

Do not exchange $\varprojlim$ with $\varinjlim$ without a theorem; do not treat nuclear flatness as projectivity; do not replace derived Hom with underived Hom; do not confuse classical strict topological cokernels and abelian liquid cokernels without comparison. Keep finite quantum-weight truncations distinct from complete pro-systems.

**First acceptance gate:** EXT-015A, the actual quotient-stage liquid realization and its naturality. All additional assertions remain conditional pending verified stage relationships.
