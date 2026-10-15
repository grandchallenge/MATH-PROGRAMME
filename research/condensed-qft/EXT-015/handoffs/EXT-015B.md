# GCL mathematical handoff — EXT-015B

**Handoff status:** PREPARED; NOT DISPATCHED. **Task docket:** [MATH-PROGRAMME #2654](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2654). **Parent:** [QFT-COND-005 #2617](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617). **Source custody:** protected base commit 1f28f95d7c0e4059685830391ba4dfe37760d043. An authenticated, authorized execution dispatch remains separate from this research preparation.

**Guiding question:** Can an extension carry genuinely global analytic information that no compact-support stage can capture?

## Frozen source bundle

- [EXT-015 SPEC](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/SPEC.md), especially C0/C4 and Sections 5–6.
- [EXT-015 work packages](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/WORK_PACKAGES.md).
- [EXT-015 hostile extension docket](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/EXTENSION_DOCKET.md).
- [LFO-010 strict Borel-jet extension](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/STRICT_LF_OUTPUT_DERIVED_BOUNDARY_010.md).
- [DRM-014 source-side derived mapping and auxiliary ring control](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/DERIVED_MAPPING_OBSTRUCTION_014.md).
- [Verification matrix](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1f28f95d7c0e4059685830391ba4dfe37760d043/research/condensed-qft/EXT-015/RUN_MATRIX.md).
- Primary analytic reference: Clausen–Scholze, [Condensed Mathematics and Complex Geometry](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), including the specific derived/flat/projective results actually used.

EXT-015B is independently executable in parallel with A. Treat A's new quotient factorization as an **unproved sibling hypothesis**, never as an input theorem. Do not inspect unpublished A findings if operating in an independent collection phase.

## Exact mathematical target

Fix $0<p\leq1$ and the liquid real module category $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$. Start with

$$
H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}
$$

as an object of its abelian heart. We seek a **genuine** presentation

$$
0\longrightarrow R_H
\xrightarrow{i}P_H
\xrightarrow{\varepsilon}H
\longrightarrow0
\tag{B1}
$$

for which $P_H$ is projective in $\mathcal A_p$, $\varepsilon$ is an epimorphism there, and $R_H$ is exactly its kernel there. Then for any actual liquid coefficient target $T$, derive

$$
\mathrm{Ext}^1_{\mathcal A_p}(H,T)
\cong
\mathrm{coker}\bigl(
\mathrm{Hom}_{\mathcal A_p}(P_H,T)
\longrightarrow
\mathrm{Hom}_{\mathcal A_p}(R_H,T)
\bigr).
\tag{B2}
$$

The presentation need not have projective syzygy: one projective $P_H$ suffices for the first-Ext cokernel **provided exactness is verified**. If the chosen category lacks such projective covers, demonstrate the precise obstruction and replace B1 with a legitimate Yoneda construction or a resolution in an appropriate derived category, with a proved comparison.

## Bounded work and evidence obligations

**B0 — pin the category.** Verify the exact ambient real analytic ring, heart and projective generators. State whether the projectives are free liquid measures on extremally disconnected profinite sets, whether projectivity survives passage from condensed real modules to liquid real modules, and precisely what theorem says so. Beware conflating a generating family with individual projective objects.

**B1 — construct the cover.** Specify a set-indexed family of projective generators and a map onto $H$. For example, free liquid objects indexed by maps from compact extremally disconnected test spaces into $H$ may yield an epimorphism; establish the existence, smallness and projectivity of the coproduct, the epimorphic condition (tested on an appropriate generating family), and the induced kernel object. Give the indexing set or an allowed cardinal bound to avoid an illegal proper-class coproduct. Explain which construction is functorial and which choices are auxiliary.

**B2 — calculate the first syzygy.** Identify $R_H$ explicitly enough to describe morphisms $R_H\to T$ and coboundaries from $P_H\to T$ for at least the test targets below. If only an abstract generator cover is accessible, state what property of this kernel remains the real support-factorization lemma rather than claiming an Ext computation. Do not treat $R_H$ as Fréchet without proving its topology/realization.

**B3 — derive the cokernel.** Use the long exact sequence of Hom/Ext for B1, including why $\mathrm{Ext}^1(P_H,T)=0$. Verify that (B2) is the genuine Yoneda first Ext and not an extension group in the strict locally convex exact category. Explain which target maps preserve the class.

**B4 — test liquid Borel-jet transfer.** Use the known strict nuclear Fréchet sequence

$$
0\longrightarrow\ker J
\longrightarrow\mathcal D_{[-1,1]}(\mathbb R)
\xrightarrow{J}\mathbb R^{\mathbb N_0}
\longrightarrow0.
\tag{B3}
$$

Check independently whether applying the condensed/liquid realization yields a short exact sequence *in the liquid heart*. In particular determine whether continuous surjectivity of $J$ implies an epimorphism of liquid modules: is surjectivity on global points enough for this specific quotient, and are there continuous lifts of arbitrary profinite plots? Then check whether a liquid-linear section, if it existed, would have to be a continuous linear Fréchet section. Only when both checks pass may one infer a nonzero liquid Yoneda extension. Finite-jet continuous splittings are controls, not proof of a full splitting.

**B5 — hostile controls.** (i) Finite-dimensional $H=\underline{\mathbb R^m}$: verify projectivity in this category rather than relying on semisimplicity of real vector spaces. (ii) $H=\underline s$ for rapidly decreasing sequences: distinguish higher source-limit Roos classes from extension classes. (iii) The product jet space: state whether a countable product of finite-dimensional liquid objects is projective or not and justify, rather than assume stability of projectivity under products. (iv) The DRM-014 square-zero ring obstruction is a *logical warning*, never a genuine liquid test-function counterexample.

**B6 — relate to real output stages.** Set

$$
G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)},\qquad
G=\varinjlim_bG_b.
$$

Form a natural comparison of B2 on each $G_b$ with B2 on $G$ and explicitly identify the remaining issue: whether syzygy morphisms $R_H\to G$ become stage-bounded **modulo** morphisms $P_H\to G$. If this is not provable, report it as a named independent lemma for EXT-015C rather than relabelling a presentation as surjectivity.

## Required adverse trials

1. Construct a fake tempting presentation whose terms are nuclear/flat but not known projective; diagnose exactly why B2 cannot be inferred.
2. Test the purported Borel class against the possibility of *liquid non-exactness*; seek a profinite test set with a nonlifting plot or invoke a rigorously applicable quotient theorem.
3. Test the full Borel map for continuous non-splitting by the fixed-stage proof, then independently test the implication liquid-split implies continuous-split.
4. For a proposed support-escaping cocycle, check every boundary from $P_H$, not just those with finite target support.
5. Maintain a typed distinction between strict Fréchet Ext, condensed real-module Ext, liquid Ext, and the derived stable mapping object.

## Return contract and independent review

Return an authenticated research PR and/or issue evidence with exact source SHA, numbered theorem and hypotheses, generator choices, verification of projectivity/cover/kernel, true first-Ext formula or precise failure, a separate Borel-transfer verdict, and RUN_MATRIX rows C0/C4/B1/B2/B3. Explicitly label **PROVED**, **REFUTED**, **CONDITIONAL**, or **OPEN_WITH_NAMED_LEMMA** per claim. Provide source theorem/page citations and a correct infinite mathematical argument. An exact Python fixture or Lean build may accompany but never replace that argument.

Worker identity, mathematical specialist judgement, and non-author review must remain independent from any automated admission check. No upgrade to C-positive/C-negative or B.6 follows just from B1. Codex is optional.

**Controller handoff:** Follow [MATHSOLVE WORKERS.md](https://github.com/grandchallenge/MATHSOLVE/blob/main/WORKERS.md) for exact authorized pickup and RESULT/1 practice after dispatch. This file is **only a protected-candidate mathematical handoff**. No unapproved queue labels, fabricated launch receipt, claim, execution lease or RESULT/1 is authorized by publishing it.
