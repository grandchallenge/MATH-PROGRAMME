# EXT-015 REACH / 102 — logarithmic failure of finite-pole pushforward closure

**Disposition: explicit counterexample to a universal pushforward contract for the broad collar domain099.** Proper normal integration of an admitted weighted smooth kernel produces a nonzero logarithm. The output has no finite-pole smooth collar extension. This is not a counterexample to the mandatory eleven-edge Gaussian/Wick model, GB2, or the original REACH programme. It identifies a precise extra requirement for using the broad liquid domain as a common operator domain.

## 1. Objects, frozen inputs and the exact claim tested

Keep the one-dimensional physical spacetime, interval basis, real liquid heart with parameter $p$ and ZFC. Use the finite-weight collar-source class defined in099. The tested operator is ordinary physical projection, proper on the declared compact input support. The target at one physical vertex has no collision blowup: its zero-scale boundary is simply $\epsilon=0$.

| Input | Exact scientific identity |
| --- | --- |
| Protocol090 | 6b642bf10c3328bb64d37474e290810fb45cbca1 |
| Collision/local-profile source096 | ee15ed47d90123bdd958dcb4a93cd51b428c1702 |
| Its accepted critic097 | a3e56b7dcd6964d302f17fd6c729cf57072875c4 |
| Prior protected return | PR2930,49083b0c9516a5e7537a0af20bb6e9d4d453efa2 |
| Corrected collar source099 | bcdd5328c52361403b54c24c662c336bff4ce7ae |
| Corrected collar ledger101 | 715046e9c5b95d708a43b1bcb58307aba20a8bbf |
| Preserved099 source cut | 428970ab881d6828edf73670e3be15e013a0f443 |

The collar construction is frozen for its separate critic100 at this cut. The argument below uses its explicit complete-source/evaluated-image definition, not an assumption that its boundary kernel theorem has already received protected admission. The image membership/nonmembership tested here is independent of its boundary weight-unit correction.

Let $\mathcal R_2$ and $\mathcal R_1$ be the evaluated images of those finite-weight collar sources at two and one physical vertices. We test the proposed blanket implication

$$
q_*\mathcal R_2\subset\mathcal R_1
\tag{102.1}
$$

for a physical forgetful projection $q$, with proper fixed support. Neither096 nor099 claimed to have proved (102.1). Rejecting it does not refute their accepted positive subclaims. A smaller explicitly typed pushforward domain would need its own proof that every mandatory operation stays in it.

## 2. A kernel in the source class

Choose a compactly supported smooth $g(c)$ with integral one and support in a small interval. Choose $0<a<b$ and $\chi\in C_c^\infty(\mathbb R)$ with $\chi=1$ for $|y|\le a$, supported in $|y|<b$. Choose these supports small enough that $(x_0,x_1)=(c,c+y)$ lies in one fixed interval squared. The coordinate Jacobian has absolute value one.

Define the actual positive-regulator family

$$
T_\epsilon(c,y)
=g(c)\frac{\chi(y)}{\sqrt{\epsilon^2+y^2}},
\qquad q(c,y)=c .
\tag{102.2}
$$

It is a smooth physical kernel for every $\epsilon>0$, with one fixed compact support in $(c,y)$. Projection is proper on this support. This is an additional observable family in the broad collar class, not a replacement for the Gaussian propagator $\kappa_\epsilon$ or $P_\epsilon$ of the studied model.

The pair collision resolution blows up $\{\epsilon=y=0\}$. In polar coordinates

$$
r=\sqrt{\epsilon^2+y^2},\qquad
A=\epsilon/r,\qquad B=y/r,\qquad
A\ge0,\quad A^2+B^2=1,
\tag{102.3}
$$

the normalized lift is

$$
r\,\beta^*T=g(c)\chi(rB).
\tag{102.4}
$$

It is smooth up to every face, including $A=0$. It has an ordinary smooth scalar collar extension, hence is in a stage of099 with empty wavefront cone and one front-face pole. Its positive-scale actual family therefore defines an element of $\mathcal R_2$. This proof uses only scalar smooth extension and finite weights; no assertion about general distributional extension is needed.

## 3. Exact nonzero logarithm after integration

The projected family is $g(c)I(\epsilon)$, where

$$
I(\epsilon)=\int_{\mathbb R}
\frac{\chi(y)}{\sqrt{\epsilon^2+y^2}}\,dy .
\tag{102.5}
$$

Split at $|y|=a$. For $\epsilon>0$,

$$
I(\epsilon)
=2\,\mathrm{arsinh}(a/\epsilon)
+\int_{|y|\ge a}
\frac{\chi(y)}{\sqrt{\epsilon^2+y^2}}\,dy
=-2\log\epsilon+H(\epsilon),
\tag{102.6}
$$

with

$$
H(\epsilon)=
2\log\!\left(a+\sqrt{a^2+\epsilon^2}\right)
+\int_{|y|\ge a}
\frac{\chi(y)}{\sqrt{\epsilon^2+y^2}}\,dy .
\tag{102.7}
$$

The integral in(102.7) is over a fixed compact set bounded away from zero. All regulator derivatives are uniformly integrable for $|\epsilon|<a/2$. Its integrand, and the first term, are smooth even functions of $\epsilon$ there. Thus $H$ extends smoothly across zero. In particular the logarithmic coefficient is exactly $-2$, nonzero; no parity argument or numerical asymptotic fit is used.

This is a genuine proper physical pushforward of the actual positive-scale family, not a formal profile substitution.

## 4. The target class cannot contain this output

Every finite-weight collar source at one vertex, when paired with a fixed compact smooth physical test, gives a scalar family of the form $\epsilon^{-N}F(\epsilon)$ for some finite $N$ and $F$ smooth at zero. The target has just the regulator boundary; its conormal exclusion makes the normalized distribution a smooth regulator family. Finite sums have the same property after increasing $N$.

This property applies to every ordinary element of its evaluated liquid image. Indeed the free liquid module on a point is compact projective, so an element lifts through the image epimorphism to finitely many actual complete source stages. This uses projectivity only for the extremally disconnected one-point test.

Choose a physical test $\varphi(c)$ with $\langle g,\varphi\rangle\ne0$. If $q_*T$ were in $\mathcal R_1$, then for some $N$ the scalar function $\epsilon^NI(\epsilon)$ would be smooth at zero. For $N=0$ it diverges. For $N>0$,

$$
\frac{d^N}{d\epsilon^N}
\left(\epsilon^N\log\epsilon\right)
=N!\log\epsilon+C_N ,
\tag{102.8}
$$

so its derivative of order $N$ diverges; the corresponding derivative of $\epsilon^NH(\epsilon)$ is bounded. Equation(102.6) gives a contradiction for every $N$. Hence

$$
T\in\mathcal R_2,\qquad q_*T\notin\mathcal R_1 .
\tag{102.9}
$$

The failure is already at an ordinary element, so no choice of profinite descent or formal boundary representative can make (102.1) a map on the stated objects.

The same argument rules out restoring this finite-pole target by subtracting any finite Laurent polynomial or any finite-pole smooth counterterm. That target class is closed under addition; if both the correction and corrected result belonged to it, their sum would put $I$ in it, contradicting(102.8). A new logarithmic counterterm or logarithmic target is a change of the contract, not such a finite-pole correction.

## 5. Scope, hostile controls and the next mathematical requirement

The example respects compact physical support, properness, interval dimension, actual-kernel equality, empty wavefront cone at positive scale and a weighted smooth normalized collision lift. It therefore tests an actual inference omitted by a raw-lift or liquid-image proof. A nonzero coefficient is derived exactly.

The example does not belong to the stipulated finite Gaussian/Wick generating family merely because it belongs to the broader collar class. It does not change any of the277-source results, the two legal spinneys, normal derivatives, even-rank finite terms or the marked tangent identities of087/096. It does not refute completed R1: the family in(102.2) is not a uniformly regular zero-scale R1 plot. It does not provide a cocycle for original R3.

Ordinary projection here is also not automatically the renormalized BV contraction: the latter includes the specified Gaussian/Wick kernel and its actual arity operation. Therefore(102.9) proves failure of the blanket ordinary-pushforward contract. To restrict admissibility, one must specify and prove closure for the actual required Gaussian/Wick contractions, insertions and compositions. This source does not infer their failure from the present extra element.

One possible repair is a polyhomogeneous corner domain admitting powers and logarithms with explicit index sets. Even its scale action would require the additional rule $\log(s\epsilon)=\log\epsilon+\log s$, not only degree scaling. Another possible route is an explicitly closed generated subdomain that excludes the extra kernel while retaining every mandated source, decoration, R1 plot and operator. Either route needs a new closure proof; choosing a smaller original REACH objective is not a substitute.

The immediate next theorem is thus sharply typed: identify the admissible corner index class for all actual Gaussian/Wick source projections, prove the resolved map and density estimates, and show that every resulting logarithm, if any, is retained with compatible liquid plots and scheme transport. Boundary-kernel descent alone does not supply that theorem.

This is one primary exact counterexample attempt. It requires separate non-author critique103 and ledger104, followed by protected admission/readback before tracker reconciliation. There is no numerical fixture: the elementary exact integral and the derivative obstruction prove the result. Full M2, M3, R3, R4 and the original parent objectives remain incomplete.
