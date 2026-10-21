# EXT-015 REACH-R1 / 035 — continuous zero-scale contractions on fixed normal-topology cones

**Status: NEW BOUNDED MATHEMATICAL CANDIDATE; separate critical audit required.** This is an analytic advance beyond the fixed-distribution algebraic statement D21/030 and addresses the obstruction of R0/033, but does **not** prove Costello–Gwilliam B.6 completed differentiable Weiss descent, an inductive-limit smooth enrichment or unrestricted smooth moving-point sources.

**Starting protected source:** MATH-PROGRAMME main at 1b6e1897a24ea7d4d898a2f0b90b22ee2e435399; [D21 result 030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md), [critical audit 033](R0_CRITICAL_AUDIT_D21_033.md), [REACH plan](REACH_PROGRAMME.md). **Analytic source:** Brouder–Dang–Helein, [Continuity of the fundamental operations on distributions having a specified wave front set](https://arxiv.org/abs/1409.7662), published in *Studia Mathematica* 232 (2016), proves normal-topology continuity of transversal pullbacks/proper pushforwards and hypocontinuity of transversal products. Their theorem is the explicitly imported analytic input; the particular microlocal output-cone calculation here is source-specific.

## 1. Fixed sectors, not pointwise-varying admissibility

Fix an open $U\subset\mathbb R$, polynomial arity $n\ge2$, compact $K\Subset U^n$, and a closed conic set $\Gamma\subset T^*U^n\setminus0$ such that

$$
\Gamma\cap\mathfrak N_n(U)=\varnothing,
\tag{35.1}
$$

where $\mathfrak N_n$ is the finite union of nonzero conormals of **all partial diagonals**, including simultaneous collisions, defined in D21 (30.2). Put

$$
\mathscr C_{n;K,\Gamma}^{\,N}(U)=
\{T\in\mathcal E'(U^n):
\mathrm{supp}T\subset K,\quad \mathrm{WF}(T)\subset\Gamma\},
\tag{35.2}
$$

with its **induced normal locally convex topology** from the distribution space with specified cone $\Gamma$, not the ordinary strong topology on all compact distributions. All support/properness statements below are made on this **single fixed sector** or a specified target sector. For a finite family of sectors, pass to a common support and cone only if their union still avoids $\mathfrak N_n$; there is no asserted regular or complete LF limit over all admissible cones.

## 2. A continuous diagonal BV contraction

Choose distinct slot positions $i,j$. Let

$$
\iota_{ij}:U^{n-1}\hookrightarrow U^n
$$

insert a duplicate coordinate $u$ in the two slots $i,j$, and let $q:U^{n-1}\to U^{n-2}$ delete this collision coordinate. The operation on a smooth kernel is

$$
C^{K_0}_{ij}(T)=q_*(\iota_{ij}^*T),
\tag{35.3}
$$

with $K_0(x_i,x_j)=\delta(x_i-x_j)$. The Jacobian of the change of variables from $(x_i,x_j)$ to $(u=x_i,v=x_j-x_i)$ has absolute value one, so (35.3) agrees exactly with D21's multiplication by the diagonal delta and contraction, **not** with an extra volume normalization.

**Theorem 35.1 (fixed-sector normal continuity of singular BV contraction).** For every $K,\Gamma$ satisfying (35.1), there exist a compact $K'\Subset U^{n-2}$ and a closed output cone $\Gamma'\subset T^*U^{n-2}\setminus0$ disjoint from $\mathfrak N_{n-2}(U)$ such that the linear map

$$
C^{K_0}_{ij}:
\mathscr C_{n;K,\Gamma}^{\,N}(U)
\longrightarrow
\mathscr C_{n-2;K',\Gamma'}^{\,N}(U)
\tag{35.4}
$$

is **continuous in the normal topology** (with the arity-zero scalar space understood conventionally). Consequently it carries every Bastiani-smooth finite-dimensional parameter map into the fixed input sector to a Bastiani-smooth map into the fixed output sector.

**Proof.** The normal bundle of the embedding $\iota_{ij}$ is exactly the pair-diagonal conormal supported in the slots $i,j$. It is a subset of $\mathfrak N_n$. Condition (35.1) implies transversality of the fixed closed cone to the embedding. The normal-topology pullback theorem of Brouder–Dang–Helein gives a continuous linear pullback

$$
\iota_{ij}^*:
\mathcal D'_\Gamma(U^n)\longrightarrow
\mathcal D'_{\iota_{ij}^*\Gamma}(U^{n-1}).
$$

On the subspace supported in $K$, its image is supported in the compact inverse image $\iota_{ij}^{-1}(K)$. Projection $q$ is proper on that compact support, so the cited normal-topology pushforward theorem makes $q_*$ continuous, with output wavefront cone contained in the closed projected cone obtained by the usual pushforward estimate. Taking the compact image $K'=q(\iota_{ij}^{-1}K)$ makes this a compact-support map.

The output closed cone avoids every remaining partial-diagonal conormal. Indeed, a nonzero output covector $\eta$ on a remaining partition diagonal would require an input covector $\iota_{ij,*}(q^*\eta)$ over a collision point in $\Gamma$. Such an input covector must have zero sum over the contracted pair and zero sum over every block of the remaining partition. It would therefore belong to the forbidden simultaneous-partition conormal in $\mathfrak N_n$, contradicting (35.1). More explicitly, the condition on the pullback cone provides an input covector whose two collision components sum to zero and whose other components are the corresponding components of $\eta$; this is a forbidden partial-diagonal conormal. Compact support and closedness of the input cone make the calculated output cone closed and separated from the forbidden conormals on compact base sets. Choose $\Gamma'$ to be that image cone, with harmless closure at the zero section omitted.

Composition of two continuous linear maps proves (35.4). A continuous linear map between locally convex spaces preserves every derivative of a Bastiani-smooth curve or finite-dimensional plot; hence the final statement. $\square$

## 3. Continuous Wick contraction with the cusp propagator

Set $P_0(x_i,x_j)=|x_i-x_j|/2$. Its wavefront set is contained in the pair conormal; outside the pair diagonal the function is smooth.

**Theorem 35.2 (fixed-sector normal continuity of the zero-scale Wick contraction).** Under (35.1), the map

$$
C^{P_0}_{ij}(T)
=p_{ij,*}\bigl(P_0(x_i,x_j)\,T\bigr)
\tag{35.5}
$$

is continuous linear between the same kind of fixed compact-support normal-cone sectors, with a target cone avoiding all output partial-diagonal conormals.

**Proof.** Localize the fixed factor $P_0$ by a smooth compactly supported cutoff equal to one near $K$; this does not alter the product on $K$. The fixed factor has wavefront contained in the pair conormal $\Lambda$. The cones $\Gamma$ and $-\Lambda$ are disjoint by (35.1). The normal-topology product theorem of Brouder–Dang–Helein makes the product of distributions **hypocontinuous bilinear** in its two arguments between the corresponding specified-cone spaces. Holding the propagator fixed gives a **continuous linear** map in $T$; this does not assert arbitrary joint continuity of a varying pair of singular factors.

The product wavefront is contained in the usual union of $\Gamma$, $\Lambda$, and nonzero sums $\Gamma+\Lambda$ at the same base point. It has compact support in $K$. Proper projection to the remaining $n-2$ coordinates is continuous by the normal-topology pushforward theorem. The output avoids all forbidden conormals by the same simultaneous-partition calculation used in D21's microlocal closure proof: an output covector on a remaining partial diagonal would demand either an input forbidden conormal to that partition with singleton pair slots, or one on the simultaneous partition with the contracted pair as an additional block. Compactness permits a closed output cone avoiding these directions. $\square$

**Corollary 35.3 (finite-arity Wick plot transport).** Fix finite polynomial arity and a finite collection of compact-support input sectors satisfying (35.1), and assume all successive contractions are assigned the compatible target sectors obtained by Theorems 35.1–35.2. Then each finite coefficient of the operators $B_0$, $\Delta_0$, $W_0$ and $W_0^{-1}$ is a finite sum/composite of continuous linear maps between these normal sectors. They preserve Bastiani-smooth finite-dimensional parameter plots in these *fixed* sectors. The result is the correct positive local complement to R0's oscillatory counterexample.

The assertion is only about **linear contraction operators on fixed cone sectors**. It does not treat joint smoothness of exterior tensor products of varying inputs, variable support/cone inductive limits, the zero-scale **uniform** regulator endpoint in normal topology, or completed DVS homotopy limits.

## 4. Critical adversarial checks and exact limitations

**R0 oscillatory curve excluded:** Its fibers are smooth (empty wavefront) but the family of high-frequency oscillations fails to converge to zero in the normal topology on any fixed sector whose input cone excludes the collision-normal oscillation directions. In the special cone $\Gamma=\varnothing$, the normal topology agrees with the smooth-function topology, where derivatives of the kernels grow like $|t|^{-m}$. Thus R0's negative theorem and the positive fixed-sector normal-continuity theorem do not contradict each other.

**Simultaneous collision is essential:** Omitting conormals to two disjoint simultaneous pair diagonals would permit D21's hostile four-variable distribution to create a forbidden output singularity after contraction. The full family $\mathfrak N_n$ remains mandatory.

**Hypocontinuous is not jointly continuous:** With a *fixed* $P_0$ the map $T\mapsto P_0 T$ is continuous. There is no claim that varying two singular distributions jointly yields a continuous bilinear product, nor that all relevant Costello–Gwilliam B.6 multilinear smooth morphisms have been constructed.

**Topological completion not proved:** Theorems 35.1–35.2 are on chosen sectors. Their inductive-limit regularity, appropriate smooth gluing of plots across sectors, B.6.0.7 cofibrations, B.6.0.11 fibration controls, Weiss Cech homotopy completion, and derived quantum-weight limits are separate gates. The familiar difference between fixed compact support and strict-LF support completion must be retained.

**New substantive deliverable:** a bounded positive normal-topology continuity theorem for exact zero-scale singular BV and Wick contractions, alongside the already-admitted ambient strong-topology obstruction. **Parent:** [REACH-R1 #2796](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2796). **Audit:** separate source-locked specialist mathematical review still needed before admission as mathematics.
