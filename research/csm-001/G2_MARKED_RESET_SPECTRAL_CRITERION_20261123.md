# CSM-G2-WP06 — marked-reset spectral Gibbs criterion

**Status:** new internal theorem candidate with explicit proof and exact-rational witness implementation; **originality unadjudicated**, no MATHCERT certification. The one-marker renewal reduction has important prior art; the multi-marker leading-residue rank obstruction is the specific candidate extension, not an established originality claim.

## 1. Setting and exact statement

Let the observed alphabet be $\{0,1,\ldots,m\}$, with $m\ge1$. A finite hidden chain has nonnegative labelled transfers

$$
T_0=A,\qquad T_a=u_a v_a^\top\quad(1\le a\le m),
$$

where every coordinate of every $u_a,v_a$ is strictly positive, and $Q=A+\sum_a T_a$ is row-stochastic. Assume $\lambda=\rho(A)>0$. The row sums of $A$ are strictly below one, hence $0<\lambda<1$. The sum $Q$ is strictly positive, so the hidden chain is primitive and has a unique strictly positive stationary probability row $\pi$. In particular, this is not the disconnected-sector construction of WP05.

Set $U=[u_1\,\cdots\,u_m]$, let $V$ have rows $v_a^\top$, and define the marked gap matrix

$$
F_n=VA^nU,\qquad n\ge0.
$$

All its entries are positive: $A^n$ is nonnegative and nonzero, and $U,V$ are positive. Every finite output word has positive probability, including pure zero words.

**Theorem (internal candidate).** The following conditions are equivalent:

1. The stationary observed measure is Gibbsian for a translation-invariant uniformly absolutely summable interaction on the full shift.
2. It admits a strictly positive, quasilocal two-sided specification.
3. There exists a strictly positive rank-one matrix $C$ such that $\lambda^{-n}F_n\to C$.
4. There are a strictly positive rank-one matrix $C$, constants $M<\infty$, $0<\theta<1$, such that

$$
\max_{i,j}|\lambda^{-n} F_n(i,j)-C(i,j)|\le M\theta^n
\quad(n\ge0).
$$

The conclusion includes an explicit exponentially summable interval interaction. Neither strict positivity of $A$ nor eventual positivity of every labelled product is assumed. The necessity is a statement about the observed measure, not a particular representation, and therefore a negative instance cannot be observationally equivalent to a strictly positive labelled-transfer model.

## 2. Exact conditional odds

Suppose the nearest nonzero symbol to the left of the origin is marker $i$, separated from the origin by $L$ zeros, and the nearest on the right is marker $j$, separated by $R$ zeros. Comparing the central symbol $a$ with central symbol zero, the rank-one factorizations cancel all exterior factors:

$$
O_a(L,R;i,j)=
\frac{\nu(X_0=a\mid\text{exterior})}
{\nu(X_0=0\mid\text{exterior})}
=
\frac{F_L(i,a)F_R(a,j)}{F_{L+R+1}(i,j)}.
\tag{1}
$$

Indeed the cylinder for a central zero contributes $v_i^\top A^{L+R+1}u_j$; inserting marker $a$ splits it into $v_i^\top A^L u_a$ and $v_a^\top A^R u_j$. The common outside factors are strictly positive. The same cancellation holds for arbitrary further observed constraints outside these two markers, including arbitrary exterior cylinder events. Markers occur almost surely on both sides, since the probability of seeing $n$ consecutive zeros is at most the maximum row sum of $A$ to the power $n$. Thus (1) gives the conditional almost everywhere, and fixes its value on each positive-probability nearest-marker cylinder for any continuous version.

## 3. Spectral expansion with positive leading coefficients

We give the finite-matrix argument to make the scope of the asymptotic classification explicit.

By putting $A$ in block triangular form using its strongly connected components and applying Perron–Frobenius to each irreducible diagonal block, every eigenvalue of modulus $\lambda$ is $\lambda$ times a root of unity. Choose an integer $p\ge1$ divisible by the periods of all components with spectral radius $\lambda$. Then $B=A^p/\lambda^p$ has only the eigenvalue 1 on the unit circle.

Let $E$ be the spectral projection of $B$ onto the generalized eigenspace at 1. On that space $B=I+N$, with $N$ nilpotent of index at most the hidden dimension $d$; on its complementary invariant subspace the spectral radius is less than one. For every residue $r$ between 0 and $p-1$, the expansion is

$$
\lambda^{-(pk+r)}F_{pk+r}
=\sum_{h=0}^{d-1}\binom{k}{h}C_{r,h}
+O(\eta^k)
$$

for some $0<\eta<1$, entrywise, with

$$
C_{r,h}=\lambda^{-r}VA^r(B-I)^h EU.
$$

This is just the binomial formula on the generalized unit eigenspace and the exponentially decaying powers on its complement. Jordan polynomial factors in the complement are absorbed by increasing $\eta$ within $(0,1)$.

There is a common degree $h_*$ and strictly positive leading coefficient matrices $C_r=C_{r,h_*}$ for all residues. Here is a justification that does not silently discard cancellations. Write $s_n=\mathbf1^\top A^n\mathbf1$. Because $U,V$ are strictly positive, each entry of $F_n$ is between fixed positive multiples of $s_n$. The sequence $\lambda^{-n}s_n$ has a nonzero polynomial leading term on at least one residue: otherwise the normalized powers $A^n/\lambda^n$ would decay entrywise, contradicting their spectral radius one. Let the maximum degree on these residues be $h_*$. Nonnegativity implies the nonzero leading coefficients are positive. For every $n$ and each fixed $t\ge0$,

$$
s_{n+t}\le \|A^t\|_\infty s_n.
$$

For any residue one can advance by at most $p-1$ to a residue of maximum degree. This bounds $s_n/\lambda^n$ below by a positive multiple of $n^{h_*}$ on every residue for sufficiently large $n$. The expansion bounds it above by a constant times $n^{h_*}$. Entrywise comparison transfers these two bounds to $F_n$, proving that every entry and residue has degree exactly $h_*$ and positive leading coefficient. Therefore no assumption of a single irreducible block for $A$ is needed.

## 4. Necessity: three distinct obstructions

If a strictly positive continuous two-sided specification exists, the central conditional at the all-zero exterior is strictly positive for every symbol. As both $L,R\to\infty$, its odds must tend to a finite positive constant $K_a$, independent of the types $i,j$ and of how the two distances tend to infinity. This follows from continuity and the exact cylinder identity (1).

**Polynomial obstruction.** If $h_*>0$, take $L=R=pk$ and let $k\to\infty$. The numerator in (1) has polynomial degree $2h_*$ and the denominator has degree $h_*$, with all leading coefficients positive. The exponential factors cancel except for $\lambda^{-1}$. The odds diverge like a positive multiple of $k^{h_*}$. In particular the conditional probability of zero tends to zero at the all-zero exterior, contradicting strict positivity. This establishes non-Gibbsianness in the stated sense, not necessarily an essential discontinuity.

Now suppose $h_*=0$. Taking $L,R$ to infinity in prescribed residues $r,s$ modulo $p$ gives

$$
C_r(i,a)C_s(a,j)=\lambda K_a C_{r+s+1}(i,j),
\tag{2}
$$

where subscripts are taken modulo $p$.

**Periodic obstruction.** Fix $a$ and put $i=j=a$. The strictly positive function $f(r)=C_r(a,a)/(\lambda K_a)$ satisfies $f(r)f(s)=f(r+s+1)$. Under the translated residue coordinate $r+1$, it is a homomorphism from a finite cyclic group into the positive multiplicative reals. Such a homomorphism is identically one. Hence $C_r(a,a)=\lambda K_a$ for all residues. Set $j=a$ in (2) to see that $C_r(i,a)=C_{r+s+1}(i,a)$ for arbitrary $s$, so the whole column $a$ is residue-independent. Similarly the whole row $a$ is residue-independent. Equation (2) now forces every entry to be residue-independent. Thus failure of residue constancy contradicts continuity at the all-zero exterior.

**Marked-rank obstruction.** With common residue matrix $C$, equation (2) reads

$$
C(i,j)=\frac{C(i,a)C(a,j)}{C(a,a)}.
\tag{3}
$$

For any fixed marker $a$, this forces rank one. A positive matrix with rank greater than one yields two distinct limits of the conditional odds along exterior cylinders converging to all zeros. Since all limiting odds are finite and positive, differing odds imply differing limiting conditional probability vectors. Each cylinder has positive probability, and the exact conditional is fixed throughout that cylinder almost everywhere. No change on a null set can restore continuity.

Equations (2) and (3) prove that condition 2 implies condition 3. They also separate the three possible failure modes. Condition 1 implies condition 2 by uniform absolute summability and compactness of the full shift.

## 5. Sufficiency: construct the interaction, not merely a one-sided kernel

Suppose condition 3 holds. The spectral expansion forces $h_*=0$ and all $C_r=C$. Its complementary exponential bound, after adjusting constants for residues and finitely many initial lengths, proves condition 4.

Factor $C(i,j)=\alpha_i\beta_j$ with all $\alpha_i,\beta_j>0$. Define the positive marker activities and gap corrections by

$$
c_a=\frac{\alpha_a\beta_a}{\lambda},\qquad
G_n(i,j)=\frac{F_n(i,j)}{\lambda^n\alpha_i\beta_j}.
$$

Condition 4 implies $|\log G_n(i,j)|\le M'\theta^n$ for suitable $M'<\infty$; all finitely many short gaps are strictly positive and can be absorbed into $M'$.

Use a translation-invariant interaction with a site energy $-\log c_a$ on a marker of type $a$ and zero site energy on a background symbol. For an interval of length $n+2$, use energy $-\log G_n(i,j)$ if its endpoints are markers $i,j$ and all interior symbols are zero; otherwise set the interval energy to zero. All other interaction terms vanish. Since

$$
\sum_{n\ge0}(n+2)M'\theta^n<\infty,
$$

the interaction is uniformly absolutely summable, with an exponential length bound.

For any finite interval conditioned between exterior markers, multiply the transfer factors for all successive gaps between the fixed outer markers. In the product of factors $\lambda^n\alpha_i\beta_j$, all endpoint factors cancel between competing configurations, while each internal marker contributes precisely $c_a$ after accounting for its replacement of a zero site. The remaining factors are exactly the $G_n$ gap corrections. Consequently the Gibbs weights of this interaction give the same conditional ratios as the transfer model for arbitrary configurations in the interval. Exterior factors beyond the fixed markers cancel by rank-one factorization. Markers exist on both sides almost surely, so the stationary observed measure satisfies these finite-volume DLR kernels almost surely. Arbitrary finite subsets follow by conditioning within an enclosing interval. Uniform absolute summability defines strictly positive continuous kernels on every exterior, including the all-zero exterior. This proves condition 4 implies condition 1 and completes the equivalence.

For the all-zero exterior the resulting conditional odds are simply $c_a$. The construction is explicitly two-sided and does not appeal to a general one-sided-to-two-sided bridge.

## 6. Exact rational examples

The examples use two hidden states; every reset vector is positive, $Q$ is positive and each background matrix has a permanent zero in every positive power.

- **Gibbs despite nonpositive products:** $A=\mathrm{diag}(1/2,1/4)$, $U=((1/3,1/6),(1/4,1/2))$ and $V=((3/4,1/4),(1/4,3/4))$. The normalized gap matrix is exactly $C+(1/2)^n D$, with $C(i,j)=V(i,1)U(1,j)$ strictly positive of rank one. The limiting odds are $1/2$ and $1/12$. The output has infinite Markov memory: for every finite all-zero future prefix, changing the type of the next marker changes the conditional distribution of the preceding marker, since $U,V$ are invertible and $A^n$ is invertible. More explicitly, the row of conditional numerator weights for preceding markers includes the independent rows $v_a^\top A^k$ with positive multipliers $\pi u_a$; these rows cannot all be proportional to $\pi A^k$, and evaluation on the two independent columns $u_b$ exposes the difference. This proves that no finite reverse order exists. We **do not** assert that this positive example lacks any equivalent strictly positive representation.
- **Marked-rank obstruction without polynomial or periodic correction:** $A=(5/8)I$, $U=((1/4,1/8),(1/8,1/4))$ with the same $V$. The leading gap matrix is exactly

$$
C=\frac1{32}\begin{pmatrix}7&5\\5&7\end{pmatrix}
$$

for every normalized gap, with determinant $3/128>0$. Although all gaps have exact pure exponential dependence on length, the central odds for marker 1 are $7/20$ when both exterior markers are type 1, and $5/28$ when both are type 2, independent of distance. Thus the output is essentially discontinuous at all zeros. There is no equivalent strictly positive transfer presentation, since such a presentation would yield exponentially regular non-null conditionals and a Gibbs measure by the established positive-transfer theorem. This isolates a specifically multi-marker obstruction that cannot be reduced to a scalar gap-decay exponent.
- **Polynomial obstruction:** $A=((1/4,1/4),(0,1/4))$, $u=(1/2,3/4)^\top$, $v=(1/2,1/2)^\top$. Here $F_n=(1/4)^n(5/8+3n/8)$; (1) gives vanishing central zero probability as both gaps grow comparably.
- **Periodic obstruction:** $A=((0,1/4),(9/16,0))$, $u=(3/4,7/16)^\top$, $v=(3/4,1/4)^\top$. Since $A^2=(3/8)^2I$, the two normalized gap residues are unequal and positive. Taking even and odd equal left/right gaps yields distinct limiting odds.

All examples are edge-observation channels of the irreducible hidden chain, with $K(a\mid s,t)=T_a(s,t)/Q(s,t)$. They can also be implemented as overlapping pair channels of the form in WP02 by taking an identity readout of the first observation as the second layer. This is a scoped class of overlapping transformations, not a theorem for arbitrary nontrivial compositions of multiple overlapping layers.

## 7. Executable exact spectral certificates

The verifier in marked_reset_spectral.py accepts a proposed rational $\lambda$, period $p$, spectral projector $E$, and a finite contraction exponent $t$. It checks exactly that $E^2=E$, $BE=EB$, $(B-I)^dE=0$, and

$$
\|[B(I-E)]^t\|_\infty<1.
$$

These checks prove the invariant splitting and exponential residual bound without a floating-point eigenvalue decision. It computes every coefficient $C_{r,h}$, requires a common strictly positive leading degree across all entries and residues, and returns the polynomial, periodic, rank or Gibbs disposition. Rational positive spectral radii and supplied rational splittings are the executable scope; the general mathematical theorem is not restricted to rational eigenvalues, and no numerical universal decision algorithm is claimed.

The independent regression compares conditional vectors against stationary cylinder probabilities obtained by the existing WP04 transfer evaluator, checks all four spectral regimes, rejects false projectors, and verifies exact asymptotic witnesses. All seven preliminary local tests passed at candidate 1e066f6020481cf21e65618b6cdee45f121df2c6, receipt GCL_CONTROL_BASH_RESULT/1 ebcf78e1a7fb4f05892d5801670f4cab, independent attestation false. Final exact-head source preflight and protected CI must bind the final revision.

## 8. Novelty and scientific scope

Fernández, Gallo and Maillard, [Regular g-measures are not always Gibbsian (2011), arXiv:1106.4188v1](https://arxiv.org/abs/1106.4188), Theorem 3.1 and equations (3.10)–(3.13), already analyze two-sided conditional ratios between the nearest renewal symbols; their construction shows how nonconvergent scalar renewal products cause essential discontinuity. The one-marker gap-splitting mechanism here is therefore prior mathematics, not new. Their example has general variable-length renewal probabilities, whereas the present class has a finite nonnegative matrix realization and multiple marked reset types. The primary statement interfaces are identified; exhaustive source-proof concordance is not claimed.

Related source classes requiring further theorem-level comparison include Chazottes–Ugalde on projection/symbol amalgamation; Boyle–Petersen on hidden Markov measures and periodic-point criteria; Yayama 2026 on almost-additive relative pressure and restricted factor maps; positive realization theory; and the matrix cocycle literature. In particular, the search so far does **not** establish that the marked rank-one leading-residue classification is absent from all previous results.

**Disposition:** explicit internally proved candidate equivalence in a genuinely irreducible structural-zero class, with a multi-marker rank obstruction, direct DLR construction, and exact rational witnesses. **Novelty remains UNADJUDICATED.** No mathematical independence or MATHCERT is asserted. The more general problem of arbitrary overlapping products without a rank-one reset structure remains open. In particular, finding a Gibbs-positive example proved to lack every equivalent positive presentation remains a separate obligation.
