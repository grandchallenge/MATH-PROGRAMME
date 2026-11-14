# EXT-015 REACH / 171 — a completed no-hidden obstruction for the first anchored Green core

**Primary disposition: NEW BOUNDED NEGATIVE THEOREM.** The first Green core \(A_\epsilon=\chi(x)e(x)\rho(z)\kappa_\epsilon(z)\) has **no finite representation, even modulo the original uniform rapid ideal, by any collection of existing 108.7 histories without forgotten physical vertices**. The assertion includes every fixed completed \(E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda\) coefficient, arbitrary fixed finite jet order, scalar power/log indices and legal partition inclusions in that subclass. It is **not** a nonmembership result in the whole 108.7 source: hidden-vertex histories can produce arbitrarily high absolute-anchor Gaussian jets. Universal 150.L, residual \(W\)-acyclicity and original R3 remain OPEN.

## 1. Frozen contract and precise domain

Use protected 105 (Git blob \`a8ce66ff0edec33e2aff299550fca2089d671033\`), 108 (\`587c15fd6e24f6e6b14de574ff878221cdbd5cb6\`), 126 (\`5b05c6147d237ca1d22e4dcbce9262b0f038c163\`), 150 (\`03deca9212a9bea56743e482e5cb79edb46b9d7f\`), 165 (\`24b82716d41d309438fcb7a97bbacab0b724afde\`), and the protected B-arm 168 primary (\`e2c43f218c9175b919c51f371acb8c04e659faea\`), review169 (\`fb43b4ba450f95deb105fd65b297864979a6ed52\`) and bounded ledger170 (\`600ffd88d260c5d8460cc67a6553534f138f78d9\`). Checkpoint CP189 is the governing current continuation; this theorem does not change the source class, its completion or its quotient.

Work on the original interval \(U\ni0\) and the same fixed \(\rho,\chi\in C_c^\infty(U)\), with \(\rho(0)\ne0\), \(\chi=1\) near the joint anchor. Put
\[
e(t)=|t|/2,\qquad
\kappa_\epsilon(t)=(\sqrt{2\pi}\epsilon)^{-1}e^{-t^2/(2\epsilon^2)},\qquad
A_\epsilon(x,z)=\chi(x)e(x)\rho(z)\kappa_\epsilon(z). \tag{171.1}
\]
The second core \(B\) is source-admitted by 168. The admitted labelled and symmetric membership questions are consequently both equivalent to membership of \(A\), not yet decided.

Let \(\mathcal P_2^{\mathrm{nh}}\) denote the **evaluated finite additive image** of the existing 108.7 histories for which \(q\) forgets no physical vertex. Completed coefficient tensors within every one fixed stage are fully allowed. Every history has a fixed finite partition, source derivative multiindex, physical support, source cone, Sobolev order and scalar index family. Its input and output physical coordinate counts are both two. Thus its partition is either the identity \(\{x\}\mid\{z\}\), or the same-block diagonal \(\{x,z\}\). This is a *subcollection* of, not a modification to, the original source. The fixed source stage may vary from one member of a finite sum to another; its maximum Sobolev and derivative order is still finite.

## 2. Uniform-order strict-face lemma for no-hidden sources

**Lemma 171.1.** Let \(V\Subset U^2\) have positive distance from the two-retained-vertex diagonal \(x=z\). For any \(S\in\mathcal P_2^{\mathrm{nh}}\), the actual family \(S_\epsilon|_V\) has its intrinsic 108.2 bounded-below power/log expansion, and there is **one finite integer \(N_S(V)\)** such that *every* distributional coefficient of that expansion, at every power and logarithmic degree, has local distribution order at most \(N_S(V)\). The claim holds for completed projective coefficients and for all fixed source-controlled 126 parameter rows with finite graph-order relaxations.

**Proof.** All source terms supported on \(x=z\), including any fixed finite normal derivatives of their diagonal inclusions, vanish after restriction to \(V\). For the remaining identity-partition terms, \(q\) and \(i_\sigma\) are identities, up to an ordinary invertible coordinate relabelling with fixed Jacobian; each summand has the form \(\partial^\beta(a_\epsilon T)\) with a fixed compact graph \(R1\) coefficient and a scalar 105 stage.

The only physical two-point heat collision center is \(x=z\). On \(V\), its resolved heat space is just a smooth strict regulator collar; all scalar source coefficients and their asymptotic remainders have ordinary \(C^\infty(V)\)-valued expansions there, even when the allowed powers are rational and logarithms occur. A fixed scalar-stage coefficient map at any index is continuous into \(C^\infty(V)\), by 105.5. Therefore for a completed tensor source the induced map at that index is continuous
\[
E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda
\longrightarrow E_{s,K,\Gamma}\widehat\otimes_\pi C^\infty(V)
\longrightarrow \mathcal D'(V). \tag{171.2}
\]
Each element of the **same fixed** \(E_{s,K,\Gamma}\) is in \(H^{-s}_K\), so on \(V\) it is a distribution of order bounded by a fixed integer depending only on \(s,K,V\), not on the index depth. Multiplication by a smooth coefficient does not increase this order; the fixed physical derivative \(\beta\) increases it by at most \(|\beta|\). The completed-tensor continuity in 108.6 preserves this bound, rather than allowing a different graph Sobolev order for every scalar index coefficient. The maximum over the finite list is \(N_S(V)\). Parameter differentiation acts on the same fixed heat stages and coefficients, with the finite permitted graph-order relaxations of 126, so the same argument applies to each genuine parameter row. No estimate on a history with a forgotten vertex is asserted. \(\square\)

The conclusion is stronger than the general 108.2 statement that each output coefficient has *some* finite order, perhaps growing with expansion depth: the **no-hidden** identity-pushdown geometry keeps one fixed order at every depth.

## 3. The anchored Gaussian has unbounded strict-face order away from all collisions

Choose a nonzero \(a\in U\) close enough to zero that \(\chi(a)=1\). Fix a small product patch
\[
V=I_a\times I_0\Subset U^2,\qquad
a\in I_a,\quad0\in I_0,\quad I_a\cap I_0=\varnothing. \tag{171.3}
\]
Choose \(\phi\in C_c^\infty(I_a)\) for which
\(c_\phi=\int\chi(x)e(x)\phi(x)\,dx\ne0\). Such a test exists because \(e(a)=|a|/2>0\).

For every \(\psi\in C_c^\infty(I_0)\), the exact Gaussian moment expansion is
\[
\begin{aligned}
\langle A_\epsilon,\phi\otimes\psi\rangle
&=c_\phi\int \rho(z)\psi(z)\kappa_\epsilon(z)\,dz\\
&=c_\phi\sum_{n=0}^{M}
 \frac{\epsilon^{2n}}{2^n n!}
 (\rho\psi)^{(2n)}(0)+O_{\phi,\psi,M}(\epsilon^{2M+2}).
\end{aligned}\tag{171.4}
\]
This follows by Taylor's theorem and Gaussian moments, with the usual strong distributional remainder bounds on every fixed bounded test set. Since \(\rho(0)\ne0\), the \(\epsilon^{2n}\) coefficient as a distribution in \(z\) is
\[
\frac{c_\phi}{2^n n!}\,\rho(z)\delta_0^{(2n)}(z), \tag{171.5}
\]
whose **exact local distribution order is \(2n\)**: the coefficient of \(\psi^{(2n)}(0)\) is \(c_\phi\rho(0)/(2^n n!)\ne0\), and no lower-order distribution represents that functional. Hence the orders \(0,2,4,\ldots\) are unbounded. This is detected on a patch **strictly away from the only output collision** \(x=z\); it is not a joint-normal-profile heuristic.

**Theorem 171.2 (finite no-hidden source exclusion).**
\[
A\notin\mathcal P_2^{\mathrm{nh}},
\qquad
\not\exists S\in\mathcal P_2^{\mathrm{nh}}
\text{ with } A-S\in\mathcal I_2^{\mathrm{rap}}. \tag{171.6}
\]

**Proof.** Suppose such a finite no-hidden \(S\) existed. Apply Lemma 171.1 on \(V\), integrate over \(x\) against \(\phi\), and denote its common finite coefficient-order bound by \(N\). Equality for every positive regulator, or equality modulo the fixed finite-order rapid ideal, implies by uniqueness of strong distribution-valued power/log asymptotics that all coefficients of \(S\) equal the coefficients of \(A\). In particular at any integer power \(\epsilon^{2n}\) the coefficient after \(\phi\)-pairing must equal (171.5). Pick \(n>N/2\); (171.5) has order \(2n>N\), contradicting the coefficient bound for \(S\). Rational/logarithmic auxiliary indices cannot evade coefficient uniqueness: any extra terms cancel, and the surviving \(\epsilon^{2n}(\log\epsilon)^0\) coefficient must still have the asserted bounded order. The rapid ideal vanishes to every requested power in a fixed finite-order topology, so it cannot alter any of these coefficients. \(\square\)

This rules out **all** finite no-hidden histories at once, including completed R1 tensors and arbitrary fixed scalar polyhomogeneous index depths. It is strictly stronger than ruling out one Wick-plus-finitely-many-jet ansatz. It does not constrain hidden-source histories for which the pushforward b-fibration can create arbitrarily high physical derivative orders at successive asymptotic depths.

## 4. Sharp hostile control: one hidden vertex destroys the order invariant

The preceding obstruction cannot be promoted to full source nonmembership. With a fixed smooth compact function \(f(x)\), consider the three-vertex history with retained \((x,z)\), hidden \(y\), identity partition, fixed \(R1\) coefficient
\[
T(x,z,y)=f(x)\,\theta(z)\delta_0(y),
\qquad a_\epsilon(x,z,y)=\eta(x,z,y)\kappa_\epsilon(z-y). \tag{171.7}
\]
Here \(\theta\in C_c^\infty(U)\) is fixed and equal to one near zero, and the additional smooth cutoffs equal one on the compact support of \(f(x)\theta(z)\delta_0(y)\). The R1 wavefront is only in the \(y\) covector and avoids every nonzero partial-partition conormal. The scalar Gaussian edge is a permitted relative heat stage, and forgetting \(y\) is proper on the fixed compact coefficient support. The exact output is
\[
q_*[a_\epsilon T]=f(x)\theta(z)\kappa_\epsilon(z). \tag{171.8}
\]
Its expansion on the same off-diagonal \(V\) has unbounded \(\delta_0^{(2n)}(z)\) orders. This shows **by an existing legal source** that Lemma 171.1 genuinely depends on *no hidden vertices*, rather than extending by an unsupported pullback/pushforward order estimate.

To replace the fixed smooth \(f(x)\) by the cusp \(\chi(x)e(x)\) in (171.7) would introduce the augmented coefficient \(e(x)\delta_0(y)\). At \(x=y=0\) its wavefront contains nonzero \((\tau,-\tau)\) components conormal to the \(x=y\) partition, so it is **not** a legal \(R1\) coefficient. This rejects only that particular repair. Other legal hidden histories, including sums and cancelled completed coefficients, remain to be classified.

## 5. Obligations, bounds and successor

| Test | Result |
| --- | --- |
| No-hidden diagonal histories | Vanish identically on the off-diagonal detecting patch |
| No-hidden identity histories, including completed tensors | One fixed distribution-order bound across all strict-face scalar coefficients |
| \(A\)'s strict-face Gaussian expansion at an absolute anchor | Nonzero delta derivatives of unbounded order, explicit coefficients (171.4) |
| Exact \(A\) source in the entire no-hidden 108.7 subcollection | **EXCLUDED** |
| Rapid-equivalent \(A\) source in that no-hidden subcollection | **EXCLUDED** |
| Source obstruction with hidden vertices | **NOT PROVED**; (171.7) explicitly breaks this invariant |
| Full source membership/nonmembership of \(A\) in \(\mathcal P_2\) | **OPEN** |
| Universal 150.L, residual \(W\)-acyclicity, R3, 126.14, higher weights, M5/R4 | **OPEN** |

**Exact next mathematical target 174 (subject to critical review 172 and bounded ledger 173):** Classify the complete hidden-vertex mechanisms capable of generating an absolute Gaussian \(\delta^{(2n)}(z)\) tower while retaining the independently singular first-coordinate Green cusp, without a forbidden R1 partial-partition conormal. A positive construction must give one finite fixed 108.7 history and a complete 126 row; a negative result must exclude all allowable finite hidden histories and their completed cancellations. The no-hidden theorem alone is not a universal source invariant or a \(W\) cohomology computation.

This primary has not been independently certified. Native protected admission and logically separate mathematical criticism must be recorded against its exact head; do not use this draft to close QFT-COND-005, EXT-015D or the REACH checkpoint.