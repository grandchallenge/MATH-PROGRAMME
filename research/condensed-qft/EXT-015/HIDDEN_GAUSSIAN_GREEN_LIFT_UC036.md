# EXT-015 REACH / UC036 — hidden Gaussian histories through simultaneous collisions

**Candidate result.** The whole-stage construction UC034 extends to any fixed finite collection of old block coordinates, with at least one Gaussian edge incident to the integrated block and with every scalar factor depending on that block supplied by a finite product of such Gaussians. Arbitrary admitted spectator scalars may depend on all the other blocks. In particular a two-edge hidden Gaussian bridge has an exact lift for an arbitrary admissible complete three-variable graph coefficient. The result uses the original sources and rapid rule at simultaneous collisions. Freely coupled non-Gaussian dependence on the integrated block remains open.

## 1. Domain and construction boundary

Use the original category, cutoffs, moments, Green kernel, and filtered operator of [UC034](UNIFORM_GAUSSIAN_GREEN_LIFT_UC034.md). Take old independent block coordinates $(u,v)$ of dimension $n\ge2$, where $u$ is integrated, $v=(v_j)_{j\ne u}$ includes the other retained block $c$, and any additional blocks are hidden. Use a compact admissible complete graph stage for $T(u,v)$ as in 108.1. Retain the coordinate density or absorb a fixed smooth history factor before evaluating. The scalar stage on the remaining blocks is an arbitrary fixed admissible $S_\lambda$. For a simple tensor the preprojection input is

$$
A_\epsilon(v)\prod_{e=1}^\ell \kappa_{\sigma_e\epsilon}(u-v_{j(e)})\,T(u,v),
\qquad \ell\ge1,\quad A\in S_\lambda,\quad \sigma_e>0.
\tag{UC36.1}
$$

Include fixed compact physical multipliers independent of regulator in the graph factor and use arbitrary fixed compact smooth output localization. The scalar $A$ includes Gaussian or Wick edges not incident to $u$. The theorem uses fixed positive widths and the displayed Gaussian incident factors. Smooth or regulated factors depending arbitrarily on $u$ are beyond this domain. Preserve the actual completed projective input $E\widehat\otimes_\pi S_\lambda$.

Let $J$ be the nonempty set of incident neighbors in $v$, put $\lambda_j=\sum_{e:j(e)=j}\sigma_e^{-2}$, $\Lambda=\sum_{j\in J}\lambda_j$, and set

$$
m(v)=\Lambda^{-1}\sum_{j\in J}\lambda_jv_j,\qquad
b=\Lambda^{-1/2},\qquad
\mathcal V(v)=\sum_{j\in J}\lambda_j(v_j-m(v))^2 .
$$

Completing the square in the actual $du$ density gives

$$
\prod_{e=1}^\ell \kappa_{\sigma_e\epsilon}(u-v_{j(e)})
=C\,\epsilon^{-(\ell-1)}
e^{-\mathcal V(v)/(2\epsilon^2)}
\kappa_{b\epsilon}(u-m(v)),\qquad
C=(2\pi)^{-(\ell-1)/2}b\prod_e\sigma_e^{-1}.
\tag{UC36.2}
$$

Here $\mathcal V=\Lambda^{-1}\sum_{j<k\ \mathrm{in}\ J}\lambda_j\lambda_k(v_j-v_k)^2$. Each exponential factor on the right is an unnormalized fixed Gaussian on an actual pair difference and is already a scalar in the complete stages. The identity includes repeated edges. For a single neighbor its variance is zero. All possible means in (UC36.2) are in a fixed compact hull inside the physical interval when the physical remaining coordinates are in the compact hulls used for the histories. Choose the fixed integration window $\theta$ to be one near both that mean hull and the original integrated support.

## 2. Good coefficient at every partition

Use the difference coordinate $t=x-u$, compact kernel $k=\varphi e$, and the fixed joint selector of UC034 in $(\tau,\alpha,\zeta)$ dual to $(t,u,v)$, with $|(\alpha,\zeta)|\le|\tau|/4$ on its support. The compactly localized good part of $k(t)T(u,v)$ gives an allowed graph coefficient in the variables $(x,u,v)$. For clarity the partition test is independent of dimension. A nonzero $\tau$ requires $x=u$. Join the two blocks containing them in any putative forbidden partition and delete the $x$ slot. This recovers the old covector $(\alpha,\zeta)$ as a forbidden conormal on its original partition, because the added $\tau$ and the subtracted $\tau$ cancel inside the merged block. If $\tau=0$ just delete the zero slot. Thus a forbidden nonzero augmented covector can only be the removed axis with zero old covector. The remaining compact cone is closed and permitted. The complete continuity and finite Sobolev bound are exactly the fixed-factor tensor, order-zero multiplier, linear pullback and closed-graph proof in UC034 §2, in this dimension.

Multiply by the original scalar in (UC36.1), fixed cutoffs including the actual $\theta$, and project properly by forgetting $u$ and the old hidden blocks. This is an original history. The hypotheses on $T$ include every simultaneous old partition collision; there is no spectator independence condition on the distributional coefficient.

## 3. A scalar on the actual doubled vertex space

Use the genuine physical output and remaining vertices $(x,v)$ and independent old copies $a=(a_u,(a_j)_{j\ne u})$. Before forgetting old copies, the exact unrestricted $u$ integral of the removed part has kernel given by (UC36.2) without its last Gaussian, times

$$
F_\epsilon(z_1)=(2\pi)^{-(n+1)}
\int e^{iz_1\cdot(\tau,\alpha,\zeta)}
q(\tau,\alpha,\zeta)\widehat k(\tau)
e^{-b^2\epsilon^2(\alpha-\tau)^2/2}\,d\tau\,d\alpha\,d\zeta ,
$$

where

$$
z_1=(x-m(v),m(v)-a_u,(v_j-a_j)_{j\ne u}).
\tag{UC36.3}
$$

Indeed set $u=m(v)+r$ in the phase $\tau(x-u)+\alpha(u-a_u)+\sum_j\zeta_j(v_j-a_j)$. With the normalized Gaussian the $r$ integral gives exactly the displayed multiplier, with unit $du/dr$. The symbol on the cone has the single high-frequency homogeneous term of degree $-2$ and a Schwartz difference. In dimension $n+1\ge3$ its homogeneous extension at frequency zero is locally integrable. The positive smoothing is elliptic on the support cone since $|\alpha-\tau|\ge3|\tau|/4$. Thus the dimension-independent proof of UC034 §3 gives an ordinary smooth kernel plus the actual homogeneous family of degree $1-n$ in $(\epsilon,z_1)$. Its central front coefficients and its strict extension off $z_1=0$ have the same differentiated estimates, using the appropriate frequency dimension in the integration by parts. This proof gives finite polynomial growth in $\epsilon^{-1}$ for every such derivative on compact sets even where $z_1=0$.

The weighted mean alone need not give a partition center. To check the original heat domain keep the variance factor in the integral. Fix $j_0\in J$ and append

$$
z_2=(v_j-v_{j_0})_{j\in J\setminus\{j_0\}}.
$$

The combined linear forms $(z_1,z_2)$ have full rank $n+|J|$: the independent slots $x,a_u,a_j$ give rank $n+1$ in $z_1$, and the independent differences in the $v$ slots give rank $|J|-1$ in $z_2$. Their joint zero locus is a true partition diagonal. One block contains $x,a_u$ and all $v_j,a_j$ with $j\in J$. Each remaining index has the pair $v_j=a_j$. For $|J|=1$ the variance is absent, and (UC36.3) alone has this same partition description.

Write $\rho=(\epsilon^2+|z_1|^2+|z_2|^2)^{1/2}$, $\sigma=\epsilon/\rho$, and $\omega_i=z_i/\rho$. The full heat space principalizes $(\epsilon,z_1,z_2)$ as in UC013 §4. In particular $\rho$ is a monomial times a positive smooth unit and the angular coordinates are smooth. The smooth difference of the conic kernel in (UC36.3) has an ordinary lift and can be multiplied directly by the admitted Gaussian variance factors and the Laurent power in (UC36.2). For the homogeneous part use just two kinds of angular charts near the strict corner $\sigma=0$:

- Where $|\omega_1|$ is bounded below, the homogeneous conic kernel is $\rho^{1-n}$ times a smooth coefficient of $(\sigma,\omega_1)$. Multiply by the original admitted product $C\epsilon^{-(\ell-1)}\exp(-\mathcal V(v)/(2\epsilon^2))$. Its pair heat stages supply any smaller collision scales left along $\omega_2=0$.
- On the complement where $|\omega_2|$ is bounded below, $\mathcal V(\omega_2)$ is bounded below by a positive constant. All polynomial derivative losses of the conic kernel in $\sigma^{-1}$ are absorbed by $\exp(-\mathcal V(\omega_2)/(2\sigma^2))$. On the angular patch that product extends flatly across $\sigma=0$ with every prescribed derivative. The homogeneous term therefore has the scalar form $\rho^{1-n}$ times a smooth angular coefficient and the fixed factor $\epsilon^{-(\ell-1)}$. For $|J|=1$ this second chart is unnecessary.

A fixed smooth angular partition of unity on the normalized front and a chart with $\sigma$ bounded below complete the cover. Every chart has fixed physical and angular data independent of the graph coefficient. Taylor bounds of these smooth angular functions pull back to all recursive corners under the monomial description. Integer-saturated scalar index sets can be chosen using the face orders of $\rho^{1-n}\epsilon^{-(\ell-1)}$, with a fixed extra lower weight on each face. The unnormalized variance Gaussians carry nonnegative face orders and their full corner bounds by their original relative scalar pullbacks. Thus no progressively lower orders are needed to extract successive coefficients. This step checks the actual simultaneous collision even when the mean does not preserve any particular old pair diagonal.

To restore the $\theta$ window, take the Fourier transform of $(1-\theta(m+r))\kappa_{b\epsilon}(r)$ in $r$ in place of the heat multiplier. The support separation from $r=0$ gives all mixed physical and regulator derivatives arbitrary flat powers in the Schwartz norms, uniformly for $m$ in its fixed hull. By the same full frequency control on the bad cone this gives a smooth flat kernel in the actual augmented physical arguments. Multiplication by the variance factor and the fixed Laurent power costs only finitely many regulator powers in each requested derivative, so the tail remains smooth and flat. Subtract it exactly. This supplies one fixed complete scalar stage on the original augmented collision space, with $A_\epsilon(v)$ then included by the admitted scalar pullback and multiplication.

## 4. Exact history and consequences

Tensor $T(a)$ with fixed compact smooth functions in the $x,v$ slots equal to one on the needed support, multiply by the scalar just constructed and all required compact output and spectator cutoffs, then properly forget $a$ and the hidden $v$ slots. In the enlarged graph all new covectors are zero. Deleting them from a putative forbidden partition yields a forbidden old covector, so the graph factor is a permitted fixed stage. The compact original $T$ has polynomial Fourier growth. On the bad cone the normalized Gaussian with the window kept gives sufficient full frequency decay at every positive regulator to justify the exact paired inverse integral. The same computation with ordinary pushforward tests recovers the removed part of the original cusp integral, with no collapsed-partition density factor. Recombine with the good part before including the existing affine moments and subtracting $h_1C_2$ on the actual original input.

The good graph map is continuous and the bad scalar is fixed before varying the input. Multiplication by the arbitrary spectator $A$ is continuous between fixed scalar stages. The projective seminorm bounds therefore extend the identity on simple tensors to the original complete input. Compact supports, cones, scalar indices, auxiliary weights and history lists work across the supplied graph-order rows. Their actual equality graphs use the same fixed-order rapid estimate as UC034 §4, independently of representation. For a derivative of regulator order $j$ the same finite list of input Sobolev orders and input rapid power $N+j$ suffice, after taking account of the fixed filtered operator. No statement about recovering older parameter families is used.

For the requested **one-hidden-vertex bridge**, take $v=(c,d)$, incident edge $\kappa_\epsilon(u-d)$, and spectator factor $\kappa_\epsilon(d-c)$. Then $m=d$ and $\mathcal V=0$. In (UC36.3) the bad center has the joined block $x=d=a_u=a_d$ and the pair $c=a_c$. The spectator Gaussian then also sees $d=c$. The original full heat space resolves both, including their simultaneous intersection. The graph $T(u,c,d)$ is arbitrary on its fixed complete permitted stage. There is no use of hidden-variable integration against a smooth graph amplitude. As a control with a moving singularity take a compact cutoff of $\delta(u+c+d)$, whose covectors have nonzero total sum. Both Gaussian edges and the graph singularity meet when all three old coordinates vanish. The proof applies to this coefficient and to its bounded graph-stage families. As a control of the multiple-incident step take both $\kappa_\epsilon(u-c)$ and $\kappa_\epsilon(u-d)$: the mean is $(c+d)/2$, variance $(c-d)^2/2$ and effective width $\epsilon/\sqrt2$. The apparent mean collision at separated $c,d$ lies in the flat angular branch, while the actual joint center has $c=d$. Neither branch is omitted from the exact kernel.

The extension was constructed after the bounded acceptance of the exact whole-stage UC034 primary. It covers fixed finite Gaussian incident networks with admitted spectator factors, which includes the planned hidden Gaussian test. The remaining general source problem requires replacing the explicit Gaussian incident formula by an argument for freely coupled scalar stages depending on $u$. Universal 150.L, residual cohomology, full parameter family recovery, and final integration stay open.
