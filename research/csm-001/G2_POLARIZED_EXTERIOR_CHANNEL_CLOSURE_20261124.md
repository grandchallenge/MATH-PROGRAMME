# CSM-G2-WP08 — channel-closed polarized exterior-square separation

**Status:** internally proved finite certificate and exact coupled example. Originality UNADJUDICATED; no MATHCERT or independent mathematical certification. Depends on the uniform observable factorization and anchored cone theorem in WP07.

## 1. Why individual contraction is not compositional

A memoryless stochastic output channel replaces a family of labelled transfers by nonnegative linear combinations. Even when every original matrix has tiny exterior square, the exterior square of their sum can be large: sums of rank-one matrices need not have rank one. Thus checking only the individual generators is not a reliable certificate of closure under arbitrary stochastic postprocessing.

For square matrices define the symmetric bilinear polarization of the exterior square, indexed by ordered index pairs $i<j$ and $k<l$:

$$
\mathcal P(A,B)_{ij,kl}
=\frac12(A_{ik}B_{jl}+B_{ik}A_{jl}
-A_{il}B_{jk}-B_{il}A_{jk}).
$$

It satisfies $\mathcal P(A,A)=\bigwedge^2 A$. For any finite nonnegative linear combination,

$$
\bigwedge^2\left(\sum_a t_a A_a\right)
=\sum_{a,b}t_at_b\mathcal P(A_a,A_b).
$$

The identity follows by expanding the two-by-two minors. It involves no spectral approximation.

## 2. The channel-closed theorem

Use the setting of WP07: nonnegative stationary finite-state labelled transfers $T_a$, positive common pivot $T_a(h,h)>0$, and invariant anchored nonnegative row and column cones containing the stationary row and all-ones column. Let the associated WP07 quasi-Bernoulli constant be $b>0$. Suppose the finite pairwise check gives

$$
\eta=\max_{a,b}
\frac{\|\mathcal P(T_a,T_b)\|_\infty}
     {T_a(h,h)T_b(h,h)}<1.
\tag{1}
$$

**Theorem (internal candidate).** Every sitewise stochastic output channel with no unused output labels preserves the same anchored cones, the same quasi-Bernoulli lower bound, and the same upper bound $\eta$ on the mixed exterior-square ratios. Consequently every finite cascade of such channels satisfies the uniform observable factorization bound

$$
|E_w(u,v)|\le
\frac{\eta^{|w|}}{\pi_h^2b^2\min_i\pi_i}.
\tag{2}
$$

Each fixed output law has strictly positive exponential reverse conditional probabilities and an exponentially summable two-sided Gibbs interaction. This conclusion does not require invertibility of the postprocessed matrices.

**Proof.** Write the channel as a row-stochastic matrix $H(a,z)$ with nonnegative entries and at least one nonzero entry in each output column. Its exact edge transfer is

$$
S_z=\sum_a H(a,z)T_a.
$$

The summed transition $\sum_z S_z$ remains $Q$; hence the stationary row is unchanged. Each pivot is positive. The cones are defined by linear homogeneous inequalities and are convex, so they are invariant under nonnegative combinations of the original cone-preserving maps. This preserves the same $b$. In particular every output word has positive probability, since its product has positive pivot.

By bilinearity and the triangle inequality,

$$
\begin{aligned}
\|\mathcal P(S_z,S_t)\|_\infty
&\le \sum_{a,c}H(a,z)H(c,t)
       \|\mathcal P(T_a,T_c)\|_\infty\\
&\le \eta\left(\sum_a H(a,z)T_a(h,h)\right)
          \left(\sum_c H(c,t)T_c(h,h)\right)\\
&=\eta S_z(h,h)S_t(h,h).
\end{aligned}
$$

This reproduces (1) for the new alphabet. Setting $z=t$ gives the one-block exterior-square contraction of WP07, so (2) and the constructive Gibbs conclusion follow. The invariant mixed certificate persists under every subsequent channel by induction. Normalization of each new conditional is bounded below by $b\,p(z)$, which is positive for each fixed channel; no common positive lower bound over channels allowing arbitrarily rare output labels is claimed. Channel composition agrees with ordinary multiplication of the stochastic matrices. QED.

The theorem gives a finite sufficient certificate closed under stochastic output-channel composition. It is not a necessary condition; failure of (1) is not a non-Gibbs decision. It is not a general overlapping-block closure theorem, because arbitrary pair kernels on a single track introduce additional hidden dependencies not represented by sitewise mixtures on the original transfer alphabet.

## 3. A genuinely coupled overlapping composition

Let $d=1/1024$ and use the base transfers

$$
A_0=\begin{pmatrix}1/2&0\\0&d\end{pmatrix},\quad
A_1=\begin{pmatrix}1/4&d\\0&d\end{pmatrix},\quad
A_2=\begin{pmatrix}1/4-d&0\\1-3d&d\end{pmatrix}.
$$

Their sum is positive stochastic with stationary row

$$
\pi_*=(1021/1022,1/1022).
$$

Each generator is invertible. Let $A_i^{\rm obs},B_i^{\rm obs}$ denote independent stationary output tracks of this edge channel. The first layer reads adjacent microscopic hidden states of the two chains to emit their two observed letters as $Y_i$. The second layer uses both $Y_i,Y_{i+1}$ to produce the raw staggered pair

$$
Z_i^{\rm raw}=(A_i^{\rm obs},B_{i+1}^{\rm obs}).
$$

Because the two tracks are independent and stationary, the raw pair law has exact four-state transfer family $B_{(a,c)}=A_a\otimes A_c$ and stationary row $\pi_*\otimes\pi_*$. This is an exact cylinder-law identity, not an independence assumption about the overlapping microscopic hidden variables.

Now, independently at each site, exchange the raw pair labels $(1,1)$ and $(2,2)$ with probability $\epsilon=1/4096$ and leave all other pair labels unchanged. This is part of the stochastic second-layer pair channel; it is not two separate single-coordinate noise channels. The two affected transfers are

$$
S_{11}=(1-\epsilon)B_{11}+\epsilon B_{22},
\qquad
S_{22}=\epsilon B_{11}+(1-\epsilon)B_{22}.
$$

All others are unchanged. Thus the second layer both overlaps and couples the coordinate outputs.

## 4. Exact certificate and non-reset proof

Using the pivot at the first hidden coordinate and anchored cone bounds

$$
L=(1,1,1,1),\qquad R=(1,5,5,25),
$$

the raw nine-symbol model satisfies all row and column vertex inequalities exactly. The 81 ordered generator-pair mixed exterior checks yield

$$
\eta=\frac{1044484}{16581375}<\frac{63}{1000},
\qquad b=\frac{261121}{1052676}.
$$

Hence the theorem certifies every stochastic channel applied to these raw overlapping pair labels, including the specific coupling. The direct one-step ratio for the coupled family is even slightly smaller, exactly

$$
\frac{4467410150099971}{70938546239953921}.
$$

The following exact results distinguish this example from the independent-track specimen:

- The one-site joint distribution of the two output coordinates is not the product of its two marginals: exact tests check two of the discrepancies after the exchange.
- The summed hidden transition is strictly positive, and all nine coupled matrices have rank four.
- The minimal observable dimension is four, as computed by rational Hankel rank. Since each generator is invertible, every word matrix in the minimal realization is invertible. By WP07's observable Hankel slice argument no equivalent finite representation can possess a rank-one word.
- The unchanged all-zero pair transfer is diagonal and retains structural zeros in every power. Therefore a global eventual positivity assumption on labelled products does not apply.

The channel-closed theorem proves exponential Gibbs regularity by an all-word bound rather than observed finite-horizon decay. The example is genuinely coupled at the output and still uses a restricted staggered-pair architecture; we do not claim arbitrary two-layer pair kernels preserve Gibbsianness. We also make no claim that the positive output lacks every equivalent strictly positive representation.

## 5. Replay

The reference code is polarized_exterior_channel.py. The independent tests check the exact mixed quadratic identity, all-pair contraction, dense and deterministic coarse channels, a one-symbol channel, channel cascade equality, coupled coordinate dependence, full ranks, exact microscopic enumeration for every final word up to length three, and invalid channel rejection. The latter enumeration sums over compatible raw pair words and computes their probabilities by direct hidden-path sums of the two base chains, independently of the mixed transfer evaluator.

Six local tests passed at exact code/test candidate 1e9b04059129498afa3fca4c50ff1f1323d4e82b, authenticated local capture 4b7b94c2cc8e4ef8ad45c61084a26f55, independent attestation false. Final source gate and protected native CI bind the final candidate.

## 6. Source posture and remaining research

The mixed-polarization identity is elementary exterior algebra. The conversion of one-block contraction to Gibbs regularity is WP07, which explicitly attributes classical projective and dominated-cocycle inputs. Related established Gibbs-preservation results include Piraino's single-site factor theorem and fiber-mixing criteria; the present finite mixed-minor witness is a concrete sufficient mechanism for a specified class, not an originality claim. The complete prior-art comparison must distinguish uniform ordinary mixing, weak Gibbs, positive Hölder conditional kernels, and the two-sided DLR conclusion. In particular the planar domination and thermodynamic-formalism results of Bárány–Käenmäki–Morris, arXiv:1802.01916v3, Section 2, already identify almost multiplicativity and uniform singular gaps as central mechanisms. The new composition certificate remains UNADJUDICATED for novelty.

**Exact primary-source audit.** Bochi–Gourmelon, [arXiv:0808.3811v2, Theorem A](https://arxiv.org/html/0808.3811v2) requires invertible cocycles over a compact base and equates an all-orbit singular gap with a dominated splitting; WP07 uses this theorem in exactly that setting. Bárány–Käenmäki–Morris, [arXiv:1802.01916v3](https://arxiv.org/html/1802.01916v3), Theorem 2.9 treats irreducible invertible **planar** matrix norm-potential equilibrium states: Hölder Gibbs is equivalent to a strongly invariant multicone or strong conformality. Proposition 2.7 identifies the strongly conformal case with an ergodic Bernoulli equilibrium in its stated setting; Example 2.10(2) gives an identity-generator quasi-Bernoulli but non-Hölder-Gibbs obstruction. The latter is closely related to WP07's scalar-background control; do not claim its mechanism novel. WP07's general-dimension minimal observable criterion is a different statement, with a direct proof; the precise extent of its overlap with the literature remains unadjudicated. No full independent replay of either external paper has been completed.

Pinned original bytes (PDF magic checked): arXiv:0808.3811v2, 300957 bytes, SHA-256 `6bcda9573874342c613a02073b0c145490997f08269a02d94c00ec3669d51553`; arXiv:1802.01916v3, 346628 bytes, SHA-256 `ad90b183b728d6e99b11c335affae18d8c5875a686a1b773d4941b7f4eec91bc`. CHAD local source acquisition capture `d340149676f043ceb0a3590669e1c997`, independent attestation=false. Published-edition full concordance remains open.

**Remaining substantive boundary:** CSM-G2_GENERAL_COUPLED_BLOCK_LIFT_AND_SINGULAR_DOMINATION_OPEN. Seek an invariant observable mixed-minor/cone witness under arbitrary genuinely coupled finite-range block lifts (not just the certified staggered architecture followed by stochastic mixing), and establish or refute the singular minimal spectral-only implication. No MATHCERT or public originality promotion.
