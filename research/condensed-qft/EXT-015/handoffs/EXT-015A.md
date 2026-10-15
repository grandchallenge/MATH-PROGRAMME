# GCL mathematical handoff — EXT-015A

**Handoff status:** PREPARED; NOT DISPATCHED. **Task docket:** [MATH-PROGRAMME #2653](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2653). **Parent:** [QFT-COND-005 #2617](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617). **Source custody:** protected base commit `1f28f95d7c0e4059685830391ba4dfe37760d043`. A separate controller-issued dispatch/lease is required before this can be called an active worker task.

**Guiding question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

## Immutable-source bundle (do not follow moving main for mathematical premises)

- [EXT-015 SPEC](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/SPEC.md), particularly C0–C3 and Section 3.
- [EXT-015 work packages](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/WORK_PACKAGES.md).
- [LFO-013 underived theorem](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/LFO3_SURJECTIVITY_THEOREM_013.md).
- [DRM-014 higher-Ext boundary](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/DERIVED_MAPPING_OBSTRUCTION_014.md).
- [RUN_MATRIX](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/RUN_MATRIX.md).
- External primary reference: Clausen–Scholze, [Condensed Mathematics and Complex Geometry](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), inspect the *specific* exactness/real-module claims rather than assuming them.

**No sibling-return dependency:** EXT-015A is independently executable alongside EXT-015B; do not use B's unpublished proof or claims to establish C0–C3.

## Exact objects

Fix $0<p\leq1$, the abelian category $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$, Euclidean opens $U,V$, a fixed compact $K\Subset U$ and a countable exhaustion $L_b\Subset V$. Initial example: $U=V=\mathbb R$, $K=[-1,1]$, $L_b=[-b,b]$ for positive integers $b$.

$$
H=\underline{\mathcal D_K(U)},\qquad
G_b=\underline{\mathcal D_{L_b}(V)},\qquad
G=\varinjlim_bG_b,\qquad Q_b=G/G_b.
$$

The goal is to **prove or refute** the two maps below, not merely the analogous strict Fréchet assertion.

$$
\alpha_b:
\varinjlim_{c\geq b}
\mathrm{Hom}_{\mathcal A_p}
(H,\underline{\mathcal D_{L_c}(V)/\mathcal D_{L_b}(V)})
\longrightarrow
\mathrm{Hom}_{\mathcal A_p}(H,Q_b).
\tag{A1}
$$

$$
\theta^1:
\varinjlim_b\mathrm{Ext}^1_{\mathcal A_p}(H,G_b)
\longrightarrow
\mathrm{Ext}^1_{\mathcal A_p}(H,G).
\tag{A2}
$$

**A-scope is injectivity of (A2); surjectivity belongs to EXT-015C.** An unproved hypothesis in A1 must not be concealed by a conclusion about A2.

## The bounded proof sequence

**A0 — category exactness.** State the exact theorem that $\mathcal A_p$ is extension-closed in condensed real modules, that filtered colimits are exact and that any relevant categorical cokernels and images can be computed in the ambient category. Verify the real-vector-space enhancement of any theorem originally formulated for liquid abelian groups. Give page/theorem and an explicit functor diagram.

**A1a — quotient objects.** Set $F_c=\mathcal D_{L_c}(V)$ and $F_b=\mathcal D_{L_b}(V)$. Prove or refute that the categorical cokernel of $\underline{F_b}\to\underline{F_c}$ equals $\underline{F_c/F_b}$ for the **Fréchet quotient topology**. A quotient by a closed Fréchet subspace is complete and Fréchet, but that fact alone does not establish that condensed cokernels coincide. Exhibit the quotient's universal property on arbitrary profinite test objects or provide a rigorous comparison theorem.

**A1b — closed successive quotient stages.** For $c\le d$, prove that the induced continuous injection $F_c/F_b\to F_d/F_b$ is a closed topological embedding. Explicitly use the closedness of $F_c$ and $F_b$ in $F_d$, with the proper quotient-topology statement, rather than merely set-theoretic support inclusion.

**A1c — quotient scalar probes.** Identify a family of continuous linear functionals on $F_d/F_b$ whose common kernels characterize $F_c/F_b$. Evaluations at points outside $L_c$ are candidates because they vanish on $F_b$ for $c\ge b$; prove that they characterize membership in $F_c/F_b$ without using a representative-dependent condition.

**A2 — liquid quotient colimit.** Establish whether

$$
\varinjlim_{c\geq b}\underline{F_c/F_b}\longrightarrow Q_b
\tag{A3}
$$

is an isomorphism; derive it from verified exactness and A1a, not from pointwise equality alone.

**A3 — Baire and profinite upgrade.** If A1a–A2 hold, let $f:H\to Q_b$ be liquid-linear. Use separating quotient probes to construct countably many closed linear source subspaces whose union is $H$. Baire produces a common output quotient stage. **Then** show maps on every profinite test set factor continuously through that one closed Fréchet quotient stage. Prove the resulting transformation is natural and liquid-linear. This is the possible proof of surjectivity of (A1). Prove injectivity of (A1) separately using monomorphisms.

**A4 — extension injection.** From the short exact sequence $0\to G_b\to G\to Q_b\to0$, write the entire natural exact fragment and compare with $0\to G_b\to G_c\to G_c/G_b\to0$. If a class from $\mathrm{Ext}^1(H,G_b)$ vanishes over $G$, exactness gives a boundary $\delta_b(f)$. Factor $f$ through a finite quotient stage and prove that the class vanishes in $\mathrm{Ext}^1(H,G_c)$. Then and only then conclude (A2) injective.

## Mandatory hostile tests

1. Confirm the quotient probes descend through $F_b$ and separate $F_c/F_b$ within larger stages.
2. Show why a claim from global-point equality alone would be insufficient for condensed morphisms.
3. Try a compact exhaustion with nonempty and empty quotient stages; handle $c=b$ correctly.
4. Test whether the proof accidentally asserts a **uniform output stage for all source stages** (the identity on $\mathcal D(V)$ prohibits that).
5. If any categorical quotient comparison is false, give an explicit failed map or typed missing lemma, and continue only with a correctly weakened statement.

## Required independent return and disposition

Deliver a precise theorem/counterexample note with the exact category, assumptions, primary references, the full quotient-commutation proof or identified gap, commutative long-exact-sequence diagram, and update suggestions for RUN_MATRIX rows C0/C1/C2/C3/A1/A2. Report one of **PROVED**, **REFUTED**, or **OPEN_WITH_NAMED_LEMMA**, distinguishing underived quotient Hom from liquid Ext. Produce authentic evidence in the return PR/issue, not a simulated RESULT/1. Preserve source HEAD and artifacts. Routine proof checking does not require Codex or Lean; computational tests only support finite examples.

**Review separation:** The A author may not supply the independent critical approval of their own new claim. No MATHCERT theorem certification, downstream C release, or protected merge follows automatically from a return.

**Controller handoff:** Existing [MATHSOLVE WORKERS.md](https://github.com/grandchallenge/MATHSOLVE/blob/main/WORKERS.md) governs actual pickup modes. This file is an **issue-bound candidate handoff**, not a protected Solve dispatch, worker lease, or permission to post a RESULT/1. The authorized controller must choose an allowed route and publish a distinct immutable launch artifact or exact issue-bound instruction before activation.
