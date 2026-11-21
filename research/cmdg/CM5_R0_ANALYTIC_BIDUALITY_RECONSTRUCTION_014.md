# CMDG CM5 R0 — analytic biduality and canonical unit (014)

**Scope:** independent mathematical reconstruction; not a Lean proof or MATHCERT certification. Base protected `main`: `4e837176fb65b9251b587f39b477bfb7db59fa7f`. Source: Scholze, *Lectures on Condensed Mathematics* (May 2026), Theorem 4.3 (printed pp. 25–27), Corollary 5.5 and Proposition 5.7 (pp. 34–35). The prior protected theorem `shiftedComparisonCandidate_iff_genuineSolidSourceExtZero` establishes the exact unfinished target, not its truth.

## 1. Exact canonical map

In derived condensed abelian groups put `D(X)=R internal Hom(X,Z)`; set `T=R/Z`. For any set `I`, write

$$
A_I=\bigoplus_I Z,\quad B_I=\prod_I Z,\quad
E_I=\prod_I R,\quad K_I=\prod_I T.
$$

The map to prove is **the evaluation**

$$
\eta_{A_I}:A_I\longrightarrow D^2(A_I)=D(B_I),
$$

rather than an abstract isomorphism. All products are categorical *condensed* products. The genuine CMDG objects `F_X` (free condensed), `G_X` (free solid), and their unit `u_X:F_X\to G_X` are the pinned `ZLift` constructions.

## 2. Bounded doubling: an independent complete proof

Let `C^\bullet` be a nonnegative Banach cochain complex with bounded differentials. Suppose `P` is a cochain endomorphism, `\|P_n\|\leq1`, and bounded maps `H_n:C^n\to C^{n-1}` (with `H_0=0`) satisfy

$$
2\,\mathrm{id}-P=dH+Hd.
$$

**Theorem.** This complex is acyclic. Moreover every positive-degree cocycle `f` has a primitive `s` with `\|s\|\leq\|H_n\|\|f\|`.

Indeed `P^k f` is closed and `dHP^kf=2P^kf-P^{k+1}f`. With

$$
s_N=\sum_{k=0}^{N-1}2^{-(k+1)}HP^kf
$$

direct finite telescoping gives

$$
ds_N=f-2^{-N}P^Nf.
$$

For `N>M`, the Banach estimate is

$$
\|s_N-s_M\|\leq
\|H_n\|\|f\|\sum_{k=M}^{N-1}2^{-(k+1)}
\leq 2^{-M}\|H_n\|\|f\|.
$$

Thus `s_N` converges, `d s=f` by boundedness of `d`, and the stated bound holds. In degree zero, a cocycle satisfies `2f=Pf`, so `\|f\|\leq\frac12\|f\|` and `f=0`. This proves the theorem without a formal/nonconvergent infinite sum or any nilpotence assumption.

## 3. The genuine real/circle inputs, separated

A finite-type functorial Breen–Deligne free-group resolution has degree `n` terms

$$
F_n(A)=\bigoplus_{j=1}^{m_n} Z[A^{r_{n,j}}],
$$

with **finite** `m_n`. For compact `A=K_I` and extremally disconnected profinite probe `S`, the real cochain candidate is

$$
C^n_I(S)=\bigoplus_{j=1}^{m_n}
 C(K_I^{r_{n,j}}\times S,R).
$$

These are Banach spaces in the supremum norm; the differential is a finite sum of pullbacks. The endomorphism `P=[2]^*` has norm at most one. The two free-resolution chain maps `F_\bullet([2])` and `2\mathrm{id}` lift the same multiplication-by-two augmentation. A functorial resolution comparison yields their homotopy; **degreewise finite integer-coefficient pullback formulas** are required to ensure its dual `H` is bounded. Once the *actual* resolution-to-derived-Hom comparison and this boundedness are constructed, Section 2 proves

$$
RHom(K_I,R)=0.
$$

This is the analytic real calculation, but it is **conditional at the genuine condensed/Lean realization**. A mere algebraic homotopy is not enough.

The circle-to-discrete-integers calculation is **different**:

$$
\bigoplus_{i\in I}M[-1]\xrightarrow{\sim}RHom(K_I,M)
$$

for discrete `M`, with components pulled back along the circle projections. For one circle, `0\to Z\to R\to T\to0` reduces it to `RHom(R,M)=0`. The resolution/Cech spectral sequence reduces this to cohomology of `R^r\times S`; contraction of `R^r` to zero identifies it with cohomology of `S`. For noncompact `R^r`, exhaust by compact cubes `[-n,n]^r` and pass through the derived inverse limit. For arbitrary `I`, compact finite-coordinate cylinder refinements and Cech continuity for surjective inverse systems give the finite-subset filtered colimit of circle derived-Homs. The relevant **derived condensed sheaf comparisons**, not just topological homotopy invariance, must be established in the pinned site.

## 4. Derived exact triangle and canonical biduality

The condensed AB4* property supplies the **actual** exact product sequence

$$
0\longrightarrow B_I\longrightarrow E_I
\longrightarrow K_I\longrightarrow0.
$$

The real scalar derived adjunction gives

$$
D(E_I)\simeq RHom_R(E_I,RHom_Z(R,Z))=0,
$$

using the single-real-to-discrete-integer vanishing. The preceding circle calculation gives `D(K_I)\simeq A_I[-1]`. The induced contravariant distinguished triangle therefore gives `D(B_I)\simeq A_I`.

**Map identification:** for each finite `J\subseteq I`, the coordinate projections give a morphism of the real/circle short exact sequences. The connecting morphisms commute with these morphisms, so finite coordinate pairings form a *natural* square. The map

$$
\mathop{\mathrm{colim}}_{J\subseteq_{\mathrm{fin}} I}D(B_J)
\longrightarrow D(B_I)
$$

is an equivalence by circle Cech continuity and the zero real term. The finite-stage canonical maps `A_J\to D^2(A_J)` are exactly standard coordinate evaluation. Naturality makes their filtered-colimit composite **equal to** `\eta_{A_I}`, since a finitely supported vector evaluates a product element using only its nonzero coordinates. Therefore **the canonical** `\eta_{A_I}` is invertible, conditional only on the genuine derived comparisons specified in Section 3 and exact products/adjunction.

## 5. Actual unit compatibility, not arbitrary isomorphism

For profinite `X`, the free-source calculation gives `D(F_X)\simeq C(X,Z)[0]`; Nobeling freeness identifies this with discrete `A_{I(X)}`. Hence `D^2(F_X)\simeq B_{I(X)}`, matching the protected categorical isomorphism `gsFreeSolidToCoefficientProductIso X`. The **additional** exact proof obligation is

$$
\theta_X\circ u_X=\eta_{F_X},\qquad
\theta_X:G_X\xrightarrow{\sim}D^2(F_X).
$$

By the free-object adjunction, the images of a point `x\in X` on both sides send a locally constant `f:X\to Z` to `f(x)`. Thus equality follows **once** the existing GCL product-coordinate maps and the derived internal-Hom evaluation are verified to be these same maps at `ZLift`.

Every derived duality satisfies the triangle identity

$$
D(\eta_Y)\circ\eta_{D(Y)}=\mathrm{id}_{D(Y)}.
$$

Since Section 4 makes `\eta_{D(F_X)}` invertible, `D(\eta_{F_X})` is invertible. With the unit equality, this is the **actual** `D(u_X):D(G_X)\to D(F_X)`. Finally, `G_S\cong\prod_j Z` by the true protected coefficient-product iso; exact derived Hom into target products transports this canonical equivalence componentwise to all `G_S`. That is the required mechanism for genuine solid-source positive Ext vanishing and all negative shifts.

## 6. Authority and reopening conditions

**Proved here as ordinary mathematics:** bounded-doubling contraction, finite telescoping and explicit norm estimate, and the canonical duality-triangle implication from the stated exact comparisons. **Previously Lean verified:** true `G_S` product model, all-positive free-source Ext vanishing, all-shifts iff criterion (#3589, protected merged 2026-11-20).

**Not yet independently Lean proved:** (BD) genuine finite-type functorial condensed resolution; (REAL) bounded chain homotopy and real derived-Hom comparison; (CIRCLE) cohomological homotopy invariance, exhaustion and finite-coordinate continuity *through the actual condensed-derived comparison*; (AB4*) exact real/circle product sequence and derived real scalar adjunction; (UNIT) `\theta_X u_X=\eta_{F_X}` for the actual `gsFreeSolidToCoefficientProductIso`; (TARGET) derived Hom into the genuine product with exact `comparisonAtShift` naturality.

Do **not** replace derived internal Hom by ordinary product-group Hom, a convergent primitive by a formal sum, or the actual unit by an unnamed iso. Do not add any of the open inputs as free Lean axioms.

**Terminal boundary:** `CM5_R0_GENUINE_REAL_CIRCLE_DERIVED_COMPARISONS_AND_UNIT_LEAN_REPLAY_OPEN`. No claim of full CM5 proof, MATHCERT certification, or protected theorem admission.
