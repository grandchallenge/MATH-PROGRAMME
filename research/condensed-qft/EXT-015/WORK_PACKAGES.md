# QFT-COND-005 / EXT-015 — WORK PACKAGES AND HANDOFF

**Canonical authority:** [SPEC.md](SPEC.md). **Parent tracker:** [QFT-COND-005 #2617](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617). **Verification:** [RUN_MATRIX.md](RUN_MATRIX.md).

**Question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

## Execution order

EXT-015A and EXT-015B can proceed independently after protected admission. EXT-015C has independent positive and negative tracks; it starts with a certified projective presentation or a separately verified Yoneda extension construction. EXT-015D can begin source auditing but cannot conclude before A–C. Use the existing GCL authenticated queue/controller and protected PR workflow. Never invent RESULT/1 records, worker identities or mathematical certifications.

## EXT-015A — Quotient-stage factorization and injectivity

**Inputs:** SPEC Section 3; LFO-013; Clausen–Scholze Theorem 3.11.

**Task:** For fixed $b$, verify the precise liquid relationship between $Q_b=G/G_b$ and the Fréchet quotients $G_c/G_b$. Prove or refute

$$
\varinjlim_{c\geq b}\mathrm{Hom}(H,\underline{G_c/G_b})
\longrightarrow\mathrm{Hom}(H,Q_b)
$$

and use naturality of the connecting homomorphism to deduce injectivity of the degree-one Ext comparison.

**Gates:** (1) Show the topology-derived Fréchet quotient equals the liquid categorical cokernel, or record the precise mismatch. (2) Prove successive quotient embeddings are closed and probes separate support stages. (3) Verify continuity of scalar probes and apply Baire to a **fixed** Fréchet source. (4) Upgrade to factorizations on profinite plots, not only global points. (5) Write the exact connecting diagram.

**Return:** an independently checkable theorem or counterexample note with source citations, category hypotheses, and an updated verification matrix. Do not mark injectivity proved from the proposed sketch alone.

## EXT-015B — Projective resolution and hostile controls

**Task:** Choose projective liquid measure modules, construct and verify a projective cover of $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$, identify its first syzygy $R_H$, and compute

$$
\mathrm{Ext}^1(H,G)
\cong
\mathrm{coker}\bigl(\mathrm{Hom}(P_H,G)\to\mathrm{Hom}(R_H,G)\bigr).
$$

If an accepted projective presentation is not available, specify an alternative genuine resolution and its mathematical gaps.

**Gates:** exact projectivity source; actual epimorphism in liquid modules; kernel object; proof of exactness; treatment of possibly non-Fréchet $R_H$. Test finite-dimensional sources, rapidly decreasing sequence space, product jet space, and the Borel infinite jet extension. The latter is a strict Fréchet nonsplitting example; any claim about its image in liquid Ext must have an independent proof.

**Return:** projective or Yoneda construction, exact maps and typed control outcomes. Nuclear flatness is not projectivity.

## EXT-015C-P — Positive eventual-vanishing proof

**Task:** Show every $\xi\in\mathrm{Ext}^1(H,G)$ has a support cutoff $b$ for which its quotient image $\xi_b$ is zero in $\mathrm{Ext}^1(H,Q_b)$. Use stage-factorization of liquid extension cocycles modulo boundaries or a direct extension classification.

**Return:** a theorem with verified analytic assumptions or the exact minimal missing lemma. Baire is allowed on a syzygy only if its required topological properties are proved.

## EXT-015C-N — Adversarial escaping-support proof

**Task:** Construct a genuine liquid extension class $\xi$ with nonzero image in $\mathrm{Ext}^1(H,Q_b)$ for every target stage. Seek a concrete test-function source; use a disconnected Euclidean open as a secondary test. Show every possible liquid boundary fails to remove the escape.

**Return:** a certified counterexample or typed failed candidate. Ordinary module examples and strict Fréchet extensions are controls, not liquid counterexamples.

## EXT-015D — Derived and differentiable integration

**Task:** Once A–C report, compare the actual derived liquid Hom with Costello–Gwilliam Appendix B.6 differentiable pro-cochains. Verify smooth multilinear mapping plots, cofibration/fibration hypotheses, filtration-compatible differentials, completed tensor, quantum-weight homotopy limits and Weiss descent **separately**.

**Return:** a precise bounded bridge or an explicit comparison obstruction. Do not infer a full derived equivalence from degree-one Ext.

## Standard authenticated worker return

Each return contains the work package ID, exact input head SHA, proof/counterexample file path, category and assumptions, theorem statements, sources, positive and hostile controls, unresolved lemmas, versioned verification matrix, and an authenticated GitHub PR or issue return. Complete routine documentation under ordinary GCL protected CI. New mathematics must receive independent critical review, without inventing certification authority or bypassing required checks.

Use clean, renderable mathematical Markdown from inception. Keep work packages in separate branches or controlled files so independent workers do not race on the same proof. Codex is optional for specialized work, never a prerequisite.

## Copy-ready worker prompts

**A:** Verify liquid quotient stages for $\mathcal D_{L_c}(V)/\mathcal D_{L_b}(V)$, prove or refute quotient Hom factorization and deduce or refute Ext-injectivity through the connecting-map diagram. Read SPEC, WORK_PACKAGES, RUN_MATRIX and LFO-013. Report exact hypotheses and no unsupported transfer.

**B:** Construct an explicit projective or honest Yoneda model for genuine liquid extensions of $\underline{\mathcal D_{[-1,1]}(\mathbb R)}$. Validate measure-module projectivity, first syzygy, and Borel jet hostile control. Do not import strict Fréchet Ext classes without proof.

**C positive:** Prove eventual quotient vanishing for every liquid extension class using the certified model. Record the exact support bound mechanism and any unresolved lemma.

**C negative:** Construct a liquid Ext class persistent in every support quotient and demonstrate nonvanishing modulo all liquid boundaries. Reject toy module or strict Fréchet-only evidence.

**D:** Integrate only admitted mathematical results with differentiable pro-cochain requirements; use a separate source-limit and weight-limit audit.
