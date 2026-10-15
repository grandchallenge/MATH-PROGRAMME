# QFT-COND-005 / EXT-015 — SPEC

**Status:** PLAN PROTECTED-ADMITTED in [PR #2652](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2652), exact protected head dabaeff025eaffdd1295563bc4d6be589031adb3. EXT-015A/B handoffs are being prepared separately; mathematical conclusions remain open.

**Canonical guiding question**

> Can an extension carry genuinely global analytic information that no compact-support stage can capture?

**Research tracker:** [QFT-COND-005](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617).

**Principal references:** [LFO-013](../LFO3_SURJECTIVITY_THEOREM_013.md) proves underived fixed-source LF-output Hom factorization; [DRM-014](../DERIVED_MAPPING_OBSTRUCTION_014.md) derives source-stage inverse-limit mapping and supplies an algebraic counterexample to automatic higher Ext factorization; [LPR-012](../LIQUID_ROOS_PERSISTENCE_LFO3_012.md) analyzes a liquid Roos obstruction under explicitly stated axioms; [LFO-010](../STRICT_LF_OUTPUT_DERIVED_BOUNDARY_010.md) contains the strict Fréchet Borel-jet hostile control.

## 1. Precise objective and permitted conclusions

Fix a real liquid parameter $0<p\leq1$, $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$, opens $U,V\subseteq\mathbb R^d$, and nested compact exhaustions. For the first concrete case take $U=V=\mathbb R$, $K=[-1,1]$, and $L_b=[-b,b]$ for $b\geq1$. Set

$$
H=\underline{\mathcal D_K(U)},\qquad
G_b=\underline{\mathcal D_{L_b}(V)},\qquad
G=\varinjlim_bG_b.
$$

The primary question is whether the **canonical** filtered-colimit comparison

$$
\theta^1:
\varinjlim_b \mathrm{Ext}^1_{\mathcal A_p}(H,G_b)
\longrightarrow
\mathrm{Ext}^1_{\mathcal A_p}(H,G)
\tag{EXT-015.1}
$$

is injective and/or surjective. There is no liberty to replace the right side with an Ext group in a more convenient exact category without proving a comparison.

An extension is a Yoneda short exact sequence of **liquid modules**

$$
0\longrightarrow G\longrightarrow E\longrightarrow H\longrightarrow0.
$$

A surjective comparison means every such extension comes, up to equivalence, from push-forward of an extension with a finite output support stage $G_b$. A negative result requires a **genuine liquid** class outside the image, not a class proved nonzero only in strict nuclear Fréchet spaces or an auxiliary module category.

**Success definitions.** Accept either (A) a theorem establishing (EXT-015.1) is an isomorphism under precisely identified natural support-stage hypotheses, or (B) a fully defined counterexample in $\mathcal A_p$ with a nonzero comparison cokernel and verified exact sequence. A partial positive theorem or precisely proven failure mode is publishable as a bounded intermediate result, but it must retain an OPEN status for the remaining obligation.

## 2. Grounded dependencies and hypotheses to verify

1. **Category gate C0.** Confirm the exact inclusion of $\mathcal A_p$ in condensed real modules, extension closure, and the comparison of Yoneda Ext in those categories. Clausen–Scholze, *Condensed Mathematics and Complex Geometry*, Theorem 3.11, states extension closure and a fully faithful derived embedding for liquid groups; verify the specialized real module assertion and its naturality, rather than assuming any strict locally convex exact structure has the same Ext.
2. **Support gate C1.** $G_b$ is nuclear Fréchet, $G_b\hookrightarrow G_c$ is a closed topological embedding, and $G\cong\underline{\mathcal D(V)}$ as a liquid object for the regular strict LF filtration. Use the exact hypotheses and proof of LFO-013.
3. **Quotient gate C2.** Put $Q_b=G/G_b$. Verify that the canonical morphism

$$
\varinjlim_{c\geq b}\underline{G_c/G_b}\longrightarrow Q_b
\tag{EXT-015.2}
$$

is an isomorphism in liquid modules. Check that each locally convex quotient $G_c/G_b$ realizes the categorical liquid quotient, that successive quotient inclusions are closed embeddings, and that profinite plots compute the indicated filtered colimit.
4. **Analytic gate C3.** Establish continuity of scalar probes on each $G_c/G_b$ sufficient to apply Baire to the preimages of support stages. This must not silently assume that a closed monomorphism in the liquid heart has closed image in every topological model.
5. **Resolution gate C4.** Define an actual projective presentation of $H$ in $\mathcal A_p$ and verify the exactness and projectivity of its terms using the selected measure modules. Flatness and nuclearity do not imply projectivity.
6. **Derived/enrichment gate C5.** No implication about smooth Costello–Gwilliam B.6 mapping objects or quantum-weight completion may be drawn until their specific cofibration, fibration, filtration and smooth multilinear structures are addressed.

## 3. Strategy: first settle injectivity

For each $b$, the short exact sequence in $\mathcal A_p$

$$
0\longrightarrow G_b\longrightarrow G\longrightarrow Q_b\longrightarrow0
$$

induces the exact fragment

$$
\mathrm{Hom}(H,Q_b)\xrightarrow{\delta_b}
\mathrm{Ext}^1(H,G_b)\longrightarrow\mathrm{Ext}^1(H,G).
\tag{EXT-015.3}
$$

**Candidate quotient factorization lemma (EXT-015A, not yet admitted as proved):**

$$
\varinjlim_{c\geq b}
\mathrm{Hom}_{\mathcal A_p}(H,\underline{G_c/G_b})
\xrightarrow{\sim}
\mathrm{Hom}_{\mathcal A_p}(H,Q_b).
\tag{EXT-015.4}
$$

Proof programme: (i) establish C2; (ii) for each $c\geq b$, describe the preimage in the Fréchet source $H$ of a quotient support stage by continuous scalar evaluation outside $L_c$; (iii) use Baire's theorem to force one common $c$; (iv) use closed quotient-stage embeddings and profinite-plot factorization to promote pointwise control to a liquid map. Verify that the chosen scalar probes **separate the quotient** and descend through $G_b$.

If EXT-015.4 is proved, any class vanishing after push-forward to $G$ is a boundary $\delta_b(f)$ with $f:H\to Q_b$; factor $f$ through $G_c/G_b$ and apply naturality of connecting homomorphisms to show the class becomes zero in $\mathrm{Ext}^1(H,G_c)$. Hence **injectivity follows**. This is a proof blueprint; do not mark EXT-015A accepted until C2–C3 and the lifting diagram are checked.

## 4. The decisive problem: surjectivity

Let $\xi\in\mathrm{Ext}^1(H,G)$, and let $\xi_b$ denote its push-forward along $G\to Q_b$. The long exact sequence for $0\to G_b\to G\to Q_b\to0$ gives the exact criterion

$$
\xi\text{ comes from a finite output support stage}
\iff
\exists b:\ \xi_b=0\text{ in }\mathrm{Ext}^1(H,Q_b).
\tag{EXT-015.5}
$$

Thus a **positive** result is an eventual-vanishing theorem for all genuine liquid extension classes; a **negative** result is one class whose images $\xi_b$ remain nonzero for every $b$.

The two tracks must proceed independently and use the same definition of liquid Ext. The positive track attempts a stage-bounded extension classification or an analytic constraint on projective cocycles. The negative track attempts to construct a liquid cocycle escaping every quotient stage and to prove that no boundary eliminates its escaping support.

## 5. Common projective-presentation method

Seek an actual short exact projective presentation in $\mathcal A_p$

$$
0\longrightarrow R_H\longrightarrow P_H\longrightarrow H\longrightarrow0
$$

with $P_H$ projective. The first-syzygy model gives

$$
\mathrm{Ext}^1(H,G)\cong
\mathrm{coker}\bigl(
\mathrm{Hom}(P_H,G)\longrightarrow\mathrm{Hom}(R_H,G)
\bigr).
\tag{EXT-015.6}
$$

If a single-step projective presentation cannot be certified, replace it with a specified genuine projective resolution and derive the Ext group honestly.

**Critical risk:** $R_H$ need not be Fréchet even when $H$ is nuclear Fréchet. The LFO-013 Baire argument does **not** automatically apply to the syzygy. The strategy must either prove an appropriate replacement for relative cocycle support or construct an explicit non-stage-bounded cocycle modulo boundaries. A formally written resolution with no proof of exactness/projectivity is not acceptance evidence.

## 6. Minimal test sequence

1. **Finite-dimensional control:** take $H=\mathbb R^m$ in $\mathcal A_p$; verify whether projectivity and vanishing of positive Ext follow from the chosen liquid generators, with precise references.
2. **Intermediate analytic controls:** take rapidly decreasing sequences $s$ and jet space $\mathbb R^{\mathbb N_0}$; compare their genuine liquid extensions with known strict Fréchet behavior. The full Borel jet nonsplitting extension is a **hostile control**, not an assumed nonzero liquid class.
3. **Primary actual test functions:** $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$; $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$; compute whether (EXT-015.1) is an isomorphism.
4. **Escaping spatial support:** repeat on an explicitly described disconnected open and preserve the fixed source-stage requirement.

Do not mistake exact finite models or successful bounded truncations for infinite-dimensional liquid Ext computations.

## 7. Work packages and bounded execution

| Package | Obligation | Independent deliverable | Acceptance |
| --- | --- | --- | --- |
| EXT-015A | Prove/refute quotient-stage lemma and injectivity | Exact quotient-stage theorem and natural long-exact-sequence diagram | Source-verified C0–C3, independently checked |
| EXT-015B | Build and test projective resolution with controls | Explicit $P_H$, $R_H$, projectivity/exactness receipts and Borel-jet assessment | C4 verified; no transfer by analogy |
| EXT-015C | Positive/negative surjectivity duel | Proof of eventual quotient vanishing **or** persistent nonzero $\xi_b$; may return a typed unresolved lemma | Real liquid Ext witness; exact cocycle/boundary accounting |
| EXT-015D | Integrate Ext outcome with B.6 and quantum completion | Bounded finite-filtration comparison and gap map | Smooth cofibrations, multimorphisms, derived limits, and Weiss descent separated |

See [WORK_PACKAGES.md](WORK_PACKAGES.md) for queue-ready instructions, [EXTENSION_DOCKET.md](EXTENSION_DOCKET.md) for adversarial controls, and [RUN_MATRIX.md](RUN_MATRIX.md) for falsifiable gates.

## 8. Admission, provenance and execution discipline

- The plan was protected-merged in PR #2652; its exact admitted SHA is recorded above. **Handoff preparation is not worker dispatch**. Individual work packages may be activated only after protected handoff admission, exact readback, and authorized controller dispatch.
- Apply established GCL authenticated issue/worker return discipline to executable tasks. Mathematical assertions require independently checkable proofs and source citations. Routine documentation merges follow existing protected policy; do not invent review signatures or bypass protection.
- Preserve explicit states: PLANNED, ACTIVE, RETURNED, REVIEWED, PROVED, REFUTED, BLOCKED, and ADMITTED. A returned lemma is not automatically a proved theorem.
- Every substantive claim has a theorem statement, proof or counterexample, exact category, revision SHA, mathematical limitations, and independent critical review. Save evidence before heavy rendering. Do not replace mathematical evidence with a finite numerical fixture.
- Native GitHub/MkDocs rendering: inline dollar syntax with separation from adjacent prose; standalone display delimiters; no unsupported operator-name commands; execute the repository math Markdown CI gate.
- Codex is **optional** for specialised code work, not a project dependency. CHAD and the existing runner may perform exact fixtures. No arbitrary GPU or Lean prerequisites are imposed.
- On unexpected infrastructure failures, attempt authenticated diagnosis and repair within existing governance before declaring an external blocker.

## 9. Exit criteria and next decision

The transaction is mathematically complete only upon a genuine liquid Ext conclusion as in Section 1 with exact evidence and the formal consequences for the restricted derived comparison recorded. A verified positive theorem gives a conditional route toward the differentiable pro-cochain bridge; a negative liquid example establishes the first genuine analytical boundary. Neither by itself proves a complete quantum BV factorization equivalence.

**First executable action after admission:** EXT-015A, verification of quotient object (EXT-015.2) and proof or refutation of (EXT-015.4). EXT-015B can be independently prepared while A proceeds. Start C only with the agreed Ext presentation model; start D only after A–C provide actual mathematical outputs.

## Primary literature

- Clausen–Scholze, [*Condensed Mathematics and Complex Geometry*](https://arxiv.org/abs/2605.11731), especially Theorem 3.11 and subsequent flat/projective discussion.
- Scholze, [*Lectures on Analytic Geometry*](https://arxiv.org/abs/2605.03655), derived liquid coefficients.
- Costello–Gwilliam, [*Factorization Algebras in Quantum Field Theory*, Vol. 1](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), Appendix B.6.
- Existing GCL research notes linked in the preamble (protected repository evidence).
