# EXT-015 REACH-R2 / 036 — a no-go theorem for smooth moving-atom Wick renormalization

**Disposition: NEW EXACT MATHEMATICAL CANDIDATE; independent mathematical critical review required.** This is a sharp **obstruction**, not a claim that renormalized quantum field theory is impossible. It proves that assigning arbitrary finite counterterm values **only at coincident point pairs** cannot make the zero-scale free Wick propagator into a differentiable scalar pairing for independently moving Dirac atoms while preserving its exact off-diagonal values.

**Source basis:** admitted D14 [028](D14_REGULATED_BV_SYZYGY_028.md), D21 [030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md), and the finite-part extension / scale anomaly [032](R2_LOCAL_FINITE_PART_032.md). Protected source main at start: 1b6e1897a24ea7d4d898a2f0b90b22ee2e435399. Parent: [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

## 1. The actual local Wick kernel, viewed on moving atoms

On an interval $U\subset\mathbb R$, let $\delta_a$ denote the Dirac functional at $a\in U$. For distinct $a,b$, the admitted zero-scale free symmetric propagator gives the exact scalar pair contraction

$$
B_0(\delta_a,\delta_b)=P_0(a,b)=\tfrac12|a-b|.
\tag{36.1}
$$

This statement concerns two independently moving even source atoms, not the singular mixed even/odd delta BV contraction. At $a=b$, the absolute-value propagator has a well-defined **function value** zero, whereas its first derivative has incompatible one-sided values and its distributional second derivative is a Dirac delta. The subtlety is *smoothness as $a,b$ move*, not mere finiteness of (36.1).

Let a **diagonal-only finite point counterterm** mean any finite real-valued function $c:U^2\to\mathbb R$ with $c(a,b)=0$ whenever $a\ne b$. There is no assumption that $c$ is continuous or constant on the diagonal.

**Theorem 36.1 (diagonal-only finite Wick renormalization cannot be $C^1$).** No real-valued function

$$
F(a,b)=\tfrac12|a-b|+c(a,b)
\tag{36.2}
$$

with a diagonal-only finite point counterterm $c$ is continuously differentiable on any neighborhood of a diagonal point $(a_0,a_0)$. In fact, if $F$ is continuous there then necessarily $c(a_0,a_0)=0$, and its one-variable directional derivative in the relative coordinate does not exist at that point.

**Proof.** For fixed $a_0$, approach $(a_0,a_0)$ along points with $b\ne a_0$. Their values are $|a_0-b|/2$, which tend to zero. Continuity requires $F(a_0,a_0)=0$, so the diagonal counterterm is zero there. Along $b=a_0+h$ with $h\ne0$, the difference quotient is

$$
\frac{F(a_0,a_0+h)-F(a_0,a_0)}{h}
=\frac{|h|}{2h}
=
\begin{cases}
+\frac12,&h>0,\\
-\frac12,&h<0.
\end{cases}
\tag{36.3}
$$

The one-sided limits disagree; the directional derivative fails to exist. Therefore no $C^1$ extension exists. $\square$

**Corollary 36.2 (necessary change of the renormalization problem).** Consider a proposed differentiably enriched zero-scale Wick operation on a source class containing the two-parameter family $(a,b)\mapsto(\delta_a,\delta_b)$ as an allowed smooth pair of inputs. If evaluating this operation on that family produces a finite real-valued $C^1$ parameter map and agrees with $P_0(a,b)$ for every $a\ne b$, then the proposal is impossible. At least one of those conditions must change: restrict the allowed plots near collisions, modify off-diagonal propagation, use a distribution-valued rather than pointwise scalar parameter output, or weaken the demanded differentiability.

**Proof.** The assumed operation supplies exactly the $F$ ruled out by Theorem 36.1. $\square$

The last alternative need not be physically appropriate; it is listed to isolate the logical hypotheses. The theorem is a **conditional no-go** for this naive smooth atomic extension, not an obstruction to legitimate local distributional counterterms in Epstein–Glaser or factorization-algebra frameworks.

## 2. Why the mixed BV contraction is an even sharper problem

Away from coincidence, the mixed kernel $K_0(a,b)=\delta(a-b)$ vanishes as an ordinary function. At coincidence it is a **distribution in parameter space** and has no canonical finite scalar point value. In D14, the regulated atomic mixed-pair contraction obeys

$$
\Delta_\epsilon(\delta_a^{\mathrm{even}}\delta_a^{\mathrm{odd}})
=\kappa_\epsilon(0)=\frac{\kappa(0)}{\epsilon}.
\tag{36.4}
$$

A pointwise subtraction may produce a finite value for this one pair but does not define a continuous mixed contraction of **all** moving atoms; a continuous real-valued function vanishing off the diagonal must vanish everywhere. More elaborate distributional counterterms can be supported on the parameter diagonal, but their action is on *test functions*, not a scalar evaluation at an individual moving pair.

The renormalized structure needs either a suitable distribution-valued parameter object with compatible wavefront control or a restricted smooth-plot class that disallows arbitrary independent collisions. Otherwise the same parameter-level obstruction persists even if each separate coincident pair receives a finite assigned value.

## 3. Exact sign and jump hostile check

Let $h\ne0$. The zero-scale Wick differences obey

$$
\frac{P_0(a,a+h)-P_0(a,a)}{h}=
\begin{cases}+\frac12,&h>0,\\-\frac12,&h<0.\end{cases}
\tag{36.5}
$$

For a smooth mollifier the regulated propagator $P_\epsilon$ can be $C^\infty$ for every positive $\epsilon$, but the one-sided slopes of $P_0$ cannot be made equal by changing only diagonal point values. The rational fixture [036](fixtures/check_moving_atom_cusp_036.py) verifies these exact slopes for arbitrarily small rational displacements and checks the smooth-regularized comparison. It does not substitute for the one-line differentiability proof.

## 4. Consequences for the next genuine GB2 theorem

1. **Domain choice first.** Specify a concrete class of atomic jets and allowed moving-location plots; distinguish fixed atom locations, separated configurations and collision strata. A fixed-location atom class may admit algebraic renormalized pairings but gives no automatic smooth family for freely colliding atoms.
2. **Counterterm operator next.** Define an actual linear/coderivation operator on a specified polynomial/jet class; check the entire list of mixed contractions, distributional derivatives and Leibniz/BV second-order relations. Scalar subtraction of $\kappa_\epsilon(0)$ is insufficient.
3. **Coherence under collisions.** For multiple atoms, impose renormalized configuration-space extension across partial diagonals, nested collisions, locality, regulator change and the quantum master equation. Any necessary anomaly is recorded as a mathematical obstruction.
4. **Compatibility with R1.** Fixed admissible-wavefront normal sectors from [R1 issue #2796](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2796) offer a valid setting for **fixed-cone singular contractions** but do not automatically contain the collision-crossing two-atom smooth plot forbidden here.

**Acceptance boundary:** Theorem 36.1 and Corollary 36.2 are new *conditional* no-go mathematics, pending adversarial review. They do not refute valid distributional renormalization, the finite-part scale law 032 or the restricted D21 algebraic zero-scale theory. They identify a specific missing assumption in attempts to promote a pointwise counterterm into full differentiable BV.
