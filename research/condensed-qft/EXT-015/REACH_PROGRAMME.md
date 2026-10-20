# EXT-015 / REACH — Differentiable, renormalized and derived QFT research programme

**Disposition: PROPOSED PLAN, NOT MATHEMATICAL CERTIFICATION.** Establish three separately falsifiable results; synthesize only after exact review. This file does not issue an ACTIVE worker lease, declare mathematical independence, authorize public release or close any tracker.

**Parent trackers:** [EXT-015D #2657](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2657); [QFT-COND-005 #2617](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617). **Protected mathematical premise:** [D14 Result 028](D14_REGULATED_BV_SYZYGY_028.md) and [critical audit 029](AGENT_CRITICAL_REVIEW_D14_029.md). **Unreviewed starting candidate:** [D21/030 PR #2788](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2788), exact candidate head 85fcf808582ee6bc505f19b5ce2ca739657dcd4b. **Plan branch initial protected base:** 153d4c80372d219919168073cde5d166731f4eb2. Recheck the materially relevant commits before every operation.

## The objective

Develop a nontrivial, precisely delimited **free zero-scale quantum prefactorization theory** of singular distributional kernels with **completed differentiable Weiss descent**, extend the theory to a **first class of excluded singularities by local renormalization**, and independently settle the **original fixed-source, degree-two liquid Ext comparison** via the actual first projective syzygy. Do not conflate these three independent mathematical questions or claim a general interacting QFT equivalence.

**Success can be positive or negative:** prove a theorem under explicit hypotheses or give an actual counterexample/obstruction in the correct category. Progress cannot mean merely issuing work tickets, having a green CI run or translating assumptions into notation.

## R0 — independent hostile audit of the zero-scale candidate (priority P0)

**Deliverable:** a source-locked distinct GCL mathematical critical review of D21 Theorems 30.1–30.3 and the algebraic Weiss corollary. Verify the full partial-diagonal conormal exclusion, wavefront products, proper pushforward, stability under *iterated* contraction, disjoint-open tensor products and graded permutations. Check signs in Wick conjugation, pointwise distributional regulator limit, and Cech exactness/quantum inverse limits. Attack the proposed theorem with four hostile controls: same-point Dirac products, simultaneous disjoint collisions, a singular kernel supported away from all diagonals, and moving-support/moving-cone parameter families.

**Gate G0:** distinct auditable ACCEPT / REVISE / REJECT for each theorem, including correction/counterexample and exact head. Independent logical review can use the same authenticated GitHub account, but must be a separate source-blind critical pass with independent reasoning and provenance. D21 is **not yet certified**. If refuted, repair/narrow its domain before any track relies on it; B and C can run without G0.

## Track A (R1) — the full differentiable/microlocal framework

**A1, define the topology.** For each arity, choose compact support and closed wavefront cone separated from all forbidden partial-diagonal conormals. Test a regular inductive system of the compactly supported distribution spaces with the **normal topology**, not an unsupported ordinary wavefront topology. Brouder–Dang–Helein and Alesker identify discontinuity of naive pullback/tensor operations; the normal topology supports continuous pullback/pushforward but some bilinear operations are only *hypocontinuous*. Specify completeness, regularity, bornology, and the precise cone/support indices; do not elevate hypocontinuity to joint continuity without proof.

**A2, define parameter plots.** Form smooth families parameterized by finite-dimensional manifolds with local uniform compact-support and cone control. Check parameter pullback, gluing, all derivatives, distributional contraction and integration, Wick operators, disjoint factorization, inclusions and zero-scale convergence. Require actual Costello–Gwilliam B.2 smooth multimorphisms, not just ordinary continuous linear maps. If uniform wavefront estimates fail, replace the plot class or provide a precise obstruction.

**A3, complete and descend.** For the actual filtered differentiable complexes, prove B.6.0.7 cofibrations and appropriate B.6.0.11 fibration/quotient properties; construct completed tensor and completed Cech maps. Keep compact-output support colimits, inverse limits of quantum weights and derived source resolution in the correct order. Reproduce GCL's existing support-completion noncommutation and Milnor/Roos hostile controls. Prove completed **differentiable** Weiss descent for a specified class, or produce a nonzero comparison cone / explicitly failed smooth lift. Algebraic Weiss descent alone is insufficient.

**Gate GA:** exact locally convex and DVS definitions; continuity or precise bounded/hypocontinuity statements; all filtered lifting diagrams and a true completed equivalence *or* sharp counterexample; independent critical audit.

## Track B (R2) — first renormalized singularities

**B1, exact extension benchmark.** On the punctured real line take the distribution equal to the function 1/|z|. Choose a smooth compact cutoff chi equal to 1 near zero and define, for each compactly supported smooth test function phi,

$$
\langle t_{\chi},\phi\rangle
=\int_{\mathbb R}
\frac{\phi(z)-\phi(0)\chi(z)}{|z|}\,dz .
$$

Near zero the numerator vanishes to first order, so the integral converges; away from zero it agrees with the original singular distribution. Changing chi changes the extension by a constant multiple of the Dirac delta. Prove its scaling degree is one, so among extensions preserving that degree the delta ambiguity is the complete local freedom, with no derivatives of delta. This explicit benchmark is an **extension theorem**, not yet renormalization of the BV operator.

**B2, attach to the D14 model.** Independently treat the actual coincident even/odd Dirac pair whose regulated BV contraction equals the regulator value at zero and diverges like 1/epsilon. Specify a counterterm, its locality, regulator dependence and finite ambiguity. Replace a single subtracted number by a **well-defined operator on an explicitly specified class of kernels**. Verify classical differential compatibility, graded BV relations, and translation/reflection symmetries. Characterize renormalized scale transport, not just uncorrected W transport.

**B3, nested and overlapping singularities.** Develop a scaling-degree/Epstein–Glaser or equivalent recursive extension on two intersecting diagonals; prove locality, consistency under restrictions, factorization and regulator/scheme change. Explicitly compute any obstruction to the master equation. An anomaly is an honest failed identity, not permission to assume the desired equation.

**Gate GB1:** exact proof of a nontrivial singular extension, full local ambiguity classification and independent review. **Gate GB2:** domain-wide counterterm operator, overlapping-diagonal/forest test, scale-transport coherence and renormalized BV/factorization identities; otherwise a precise counterexample. GB1 is valuable but does **not** establish GB2 or interacting QFT.

## Track C (R3) — original liquid first-syzygy higher Ext

Work in the actual real p-liquid category of Scholze Theorem 6.5, for 0 < p <= 1. Fix the projective measure-module cover constructed in [GCL review 016](AGENT_CRITICAL_REVIEW_AB_016.md) of the original source H (compact test functions supported on [-1,1]). Call its kernel K0. Construct an actual further projective cover P1 onto K0 and kernel K1. Verify maps, projectivity, exactness and kernel-pair relations in the liquid category; do not substitute a Fréchet space without proof.

**The decisive degree-two map** is

$$
\varinjlim_b
\operatorname{Ext}^1_{\mathrm{Liq}_p}(K_0,G_b)
\longrightarrow
\operatorname{Ext}^1_{\mathrm{Liq}_p}(K_0,G).
$$

Its source term is calculated by the genuine projective presentation of K0:

$$
\operatorname{Ext}^1(K_0,T)=
\operatorname{coker}
\bigl(\operatorname{Hom}(P_1,T)
\longrightarrow\operatorname{Hom}(K_1,T)\bigr).
$$

**C1, actual relations:** bind the objects and morphisms to the existing exact source, construct a concrete free-measure kernel-pair model, and show whether the relation module has a countably directed support-localization presentation, not merely whether P0 does.

**C2, opposed proof attempts:** a positive line proves every syzygy cocycle has eventual bounded output support *modulo all projective boundaries*; a negative line constructs a genuine liquid cocycle surviving every target quotient modulo every possible boundary. Prove injectivity and surjectivity separately via the long exact sequence for each target quotient. A map that only escapes support before quotienting by projective boundaries is not a counterexample.

**C3, hostile controls:** the actual Borel-jet nonsplitting liquid extension, auxiliary phantom non-Fréchet source, finite-dimensional scalar/projective cases, rapidly decreasing sequence sources, escaping supports and resolution homotopy invariance. Avoid converting a strict topological non-splitting argument into a liquid Ext claim without a categorical proof.

**Gate GC:** genuine liquid isomorphism or genuine liquid counterexample for K0, with explicit calculations, independent review and protected admission; if blocked, return an individually falsifiable missing lemma and preserve OPEN. Even a successful K0 computation proves **degree two only**. A uniform theorem for all higher degrees requires separately proving the localization criterion for every succeeding syzygy Ki.

## R4 — integration and exit

**I1:** Build a typed comparison diagram among the corrected scalar-liquid field dual, the microlocal free quantum observable model, and the B.6 differentiable completed pro-cochains. At every arrow record whether the claim is equality of complexes, quasi-isomorphism, DVS equivalence, liquid-derived equivalence, or an obstruction. Respect GCL's already-refuted wrong unit/arity-zero mapping in D10.

**I2:** Integrate genuinely renormalized counterterm transport and exact disjoint factorization only if GB2 succeeds; isolate anomalies otherwise. Verify formal quantum-weight towers and support restrictions, not only truncated power series.

**I3:** Subject the integrated comparison to independent mathematical red team, source audit and all hostile controls; protected readback and correct tracker statuses follow, without claiming general interacting-QFT certification.

**Strong exit:** G0, GA, GB2, GC and independently reviewed typed integration all succeed within their stated scope. **Minimum meaningful intermediate exit:** G0 reviewed; GA established or sharply obstructed; GB1 established; GC proved/refuted or reduced to a precisely specified unsolved lemma; all unfulfilled targets remain OPEN. The programme plan itself is never grounds for closing #2657 or #2617.

## Dependencies, priority, and agent execution

| Priority | Package | Inputs | Exact deliverable |
| --- | --- | --- | --- |
| P0 | R0: independent D21 hostile audit | PR #2788 exact candidate head | ACCEPT/REVISE/REJECT per mathematical claim |
| P0 | R2-B1: singular extension benchmark | admitted D14 | explicit extension, scaling degree, local ambiguity and adversarial checks |
| P0 | R3-C1/C2: original K0 syzygy | admitted 016, 019 and 028 | actual liquid projective maps, cocycles, boundaries and degree-two verdict |
| P1 | R1-A1/A2: microlocal topology and plots | G0 verdict or corrected D21 | cone/support topology, smooth plots and operator bounds |
| P1 | R2-B2/B3: counterterm BV coherence | B1 and relevant D21 audit | genuine operator, two-diagonal test, renormalized identities |
| P2 | R1-A3: completed B.6 Weiss | A1/A2 | true filtered cofibration/fibration proof or obstruction |
| P2 | R4: cross-framework integration | reviewed results of A, B and C | comparison diagram, preserved structures, obstruction ledger |

**Worker return discipline:** One bounded theorem, counterexample or exact computation per work package and PR; supply source version, categories, domain, definitions, complete proof, hostile tests, fixture and replay, limitations and independent critical audit. Codex/Lean/Colab optional; no invented separate GitHub accounts. Use the existing GCL authenticated controller and governed protected PR lifecycle. Queue issue creation is **PLANNED**, not an ACTIVE worker lease or certified RESULT/1. If this becomes a long-horizon autonomously executed workset, bind it to the existing governed continuity/checkpoint registry before the next material multi-stage transition; do not establish a competing registry.

**Immediate executable order:** (1) critique PR #2788 on exact bytes; (2) in parallel prove the singular extension and inspect actual K0 projective relations; (3) establish the normal-topology DVS after the audit; (4) proceed to multi-diagonal renormalization, B.6 completion and liquid degree-two conclusion; (5) integrate only admitted mathematical results.

## Primary literature

- [Scholze, Lectures on Analytic Geometry, Theorem 6.5](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf) (real liquid projectives and derived framework).
- [Costello–Gwilliam, Factorization Algebras Vol. I, Appendices B.2, B.5, B.6](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf).
- [Brouder–Dang–Helein, Continuity of the fundamental operations on distributions, Studia Mathematica 232 (2016)](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/232/3/91541/continuity-of-the-fundamental-operations-on-distributions-having-a-specified-wave-front-set-with-a-counterexample-by-semyon-alesker) (normal topology and Alesker counterexample).
- [Brunetti–Fredenhagen, Microlocal Analysis and Interacting Quantum Field Theories](https://arxiv.org/abs/math-ph/9903028) (singular extension / renormalization).
