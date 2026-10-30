# EXT-015 REACH / 103 — non-author review of the logarithmic pushforward control

**Verdict: justified exact counterexample to blanket ordinary proper-pushforward closure of the broad finite-pole collar class.** The admitted input has an output with a nonzero logarithm, which cannot belong to the stated one-vertex finite-pole target or be restored to it by a finite-pole smooth correction. This does not prove failure of the required Gaussian/Wick generated subclass, a specified BV contraction, GB2, or original REACH. Full M2 and the original open obligations remain incomplete.

## 1. Role, exact sources and admission boundary

This is a separate delegated non-author critical pass after100. The parent authored102/104. I did not author that counterexample or its proof. I authored earlier reviews/dependency verifiers086/088 and reviews092/095/097/100, and supplied earlier plan-only type advice; the common sources and role history are disclosed. The exact nonincident-weight control supplied during100 concerned099, not the logarithmic computation here. This same-Codex logical-role scrutiny is not external or institutional certification.

The frozen source is **14cefb6b616c276cd51d1906fe7619ecf48ee055**, on research/reach-pushforward-log-source-frozen-20261030. I independently matched the following working-file byte identities without Git operations.

| Reviewed artifact or dependency | Git blob |
| --- | --- |
| [102, primary negative control](MIXED_PUSHFORWARD_LOGARITHM_OBSTRUCTION_102.md) | a4767b539bdd1127a001d51ac81c5ef1cf526e07 |
| [104, separate acceptance ledger](PUSHFORWARD_LOGARITHM_ACCEPTANCE_104.md) | 60fc5ceebfe3074c3ec5ccace1d95c6d868bc8c8 |
| [099, corrected collar-domain definition](COLLAR_STAGE_LIQUID_REALIZATION_099.md) | bcdd5328c52361403b54c24c662c336bff4ce7ae |
| [100, prior source-bound critic](AGENT_CRITICAL_REVIEW_COLLAR_REALIZATION_100.md) | 0b1e2edd4a0977a194e80eb608ebf04d37e31170 |

The parent's supplied custody places099's pending protected return in PR2932 at f7a48618d2489d1b1bf1cb57ba25fd77ed883531. This separate review does not assert that admission has occurred or add102/104 to that return. Its proof uses the explicit source/image definition of099, not protected admission of Theorem99.2, the boundary theorem or any unproved source operator. Final editorial acceptance, protected delivery, readback and tracker reconciliation belong to the parent. No producer, Git, checkpoint or tracker mutations were made in this role.

## 2. Actual input membership, density and properness

**Justified.** Take $g\in C_c^\infty$ with integral one and $\chi\in C_c^\infty$ equal to one on $[-a,a]$, with the supports small enough for the fixed interval basis. In coordinates $(x_0,x_1)=(c,c+y)$, the determinant is one. Thus ordinary forgetting of $x_1$ at fixed $x_0=c$ uses exactly the density $dy$; no factor from an averaged centre coordinate is present.

The family

$$
T_\epsilon(c,y)=g(c)\chi(y)(\epsilon^2+y^2)^{-1/2}
$$

has fixed compact physical support, independent of the regulator, and is smooth for every positive regulator. The restriction of $q(c,y)=c$ to that support is proper. Properness on this declared support, rather than properness of the unrestricted projection, is the condition needed for its physical distributional pushforward.

On the pair blowup, put $r=(\epsilon^2+y^2)^{1/2}$ and $B=y/r$. The normalized lift $r\beta^*T=g(c)\chi(rB)$ is scalar smooth, including both the front face and its intersections with the lifted temporal side face. If the stage's fixed front-face defining function differs from $r$, their ratio is a smooth nonvanishing unit and preserves this conclusion. Scalar collar extension therefore supplies an actual complete source stage with empty wavefront cone and one front-face pole. Its positive evaluation is an ordinary element of $\mathcal R_2$ by the image definition. Neither a distribution-valued extension theorem nor any choice of formal boundary representative is needed.

The input is permitted by the broad collar domain. Membership there does not place it in the original finite Gaussian/Wick generating family. In a regulator-dominated chart its uncut normalized relative profile is $(1+u^2)^{-1/2}$, which has polynomial tails rather than Schwartz decay. The distinction is material to the scope of the result.

## 3. Exact pushforward and the smooth remainder

**Justified.** Direct integration gives $q_*T=g(c)I(\epsilon)$. Because $\chi=1$ on $[-a,a]$, the inner integral is exactly $2\,\mathrm{arsinh}(a/\epsilon)$. For $\epsilon>0$ this is

$$
-2\log\epsilon+2\log\!\left(a+\sqrt{a^2+\epsilon^2}\right).
$$

The remainder outside $[-a,a]$ is an integral over a fixed compact set with $|y|\ge a$. For $|\epsilon|<a/2$, each fixed regulator derivative is bounded there by an integrable function independent of the regulator. Differentiation under that integral is therefore valid to every order. Both this remainder and the displayed logarithm of $a+\sqrt{a^2+\epsilon^2}$ extend as smooth even functions across zero. Consequently

$$
I(\epsilon)=-2\log\epsilon+H(\epsilon),\qquad
H\in C^\infty\text{ near }0.
$$

The coefficient $-2$ is exact and nonzero. It depends on the cutoff's unit plateau, not on positivity, parity or an asymptotic numerical fit. Contributions from the possibly nonsymmetric cutoff away from zero are entirely in $H$.

## 4. Nonmembership for every finite pole order

**Justified on ordinary image elements, which suffices to refute a blanket operator.** At one physical vertex there is no collision blowup. The only retained zero-scale boundary variable is the regulator. Its conormal exclusion makes every normalized source a smooth regulator family of physical distributions up to the boundary. A different defining function for that face is a smooth unit times $\epsilon$ and changes no finite-pole criterion. Pairing with a fixed compact physical test yields $\epsilon^{-N}F(\epsilon)$ for an integer $N\ge0$ and a scalar $F$ smooth at zero. Finite sums still have this form after increasing $N$.

The passage from source elements to ordinary elements of the evaluated liquid image is valid here. The free liquid module on the one-point test is compact projective, so an image element has a lift through the image epimorphism, and compactness restricts that lift to finitely many source summands. This uses projectivity only for the extremally disconnected point. It makes no arbitrary-profinite lift assertion.

Choose a compact smooth physical test equal to one near $\mathrm{supp}(g)$, so its pairing with $g$ is one. Target membership of $q_*T$ would imply that $\epsilon^NI(\epsilon)$ is smooth at zero for some finite $N$. At $N=0$ the logarithm diverges. For every positive integer $N$, Leibniz differentiation gives

$$
\partial_\epsilon^N(\epsilon^N\log\epsilon)
=N!\log\epsilon+C_N.
$$

Its logarithmic divergence cannot be cancelled by the bounded derivative of the smooth function $\epsilon^NH(\epsilon)$. Thus every finite normalization power fails. This proves an actual pointwise output nonmembership, not merely absence of a preferred formal record. No later profinite descent can supply a liquid morphism agreeing with this ordinary projection on all admitted inputs.

The correction statement is also valid. The finite-pole smooth target is additive. If an allowed correction and the corrected output both belonged to it, their sum would put the original output in it, contradicting the proof above. The conclusion concerns corrections inside this target, including finite Laurent polynomials. A logarithmic correction or a larger power/log target changes the contract and is not excluded by this argument.

## 5. Source-semantic scope verdict

**Accepted with the explicit limitations already present in102/104.** This rejects the universal claim $q_*\mathcal R_2\subset\mathcal R_1$ for ordinary proper physical forgetting on the whole broad collar class. Neither096 nor099 had proved that claim, so the example does not refute their accepted local or image/kernel results.

The argument does not identify ordinary forgetting with the actual renormalized BV contraction. The latter includes its specified kernel, arity operation, collision-centre deletion and density convention. It also does not prove that any required projection of the stipulated Gaussian/Wick generating family produces this logarithm, or that no generated admissible subdomain can remain closed. The277 proper-source calculations, both legal spinneys, finite normalizations and marked tangent identities are unchanged. No R1 uniformly regular endpoint or R3 cocycle is constructed or contradicted.

A common operator domain must now address this obstruction explicitly if it admits this extra family: retain the required logarithmic terms with suitable plots and transport, or establish a narrower operator-admissible class containing every original mandatory input and operation. Neither alternative is constructed by102. In particular a mere membership restriction without its closure proof would not satisfy the original objective. Source pushforward densities, output-stage estimates, flat-kernel preservation and required composition diagrams remain mathematical obligations. Full M2, M3, M5 and original R2/R3/R4 remain incomplete.

No correction of102/104 was required in this pass. Their exact negative-control statement, scope controls and delivery boundaries agree. Parent editorial acceptance and protected admission/readback remain separate; completing this review does not settle or close an original issue.

## 6. Validation and execution limits

No numerical fixture was introduced or replayed: the exact integral, smooth remainder proof and derivative obstruction cover all finite pole orders. Numerical samples cannot replace that universal argument. No new external mathematical input is required for these elementary identities; the liquid image and collar source conventions are the explicitly identified099 dependencies.

This report passes `ci/math_markdown_gate.py` at blob71356dcb861bb2eb4fb7cb93ee3075f787e2c065. Its bytes are UTF-8 without BOM, LF-terminated and free of trailing whitespace. The source guards match102/104 and099/100 as listed above. Gate execution uses the existing isolated Windows CPython3.12.12 at `F:/_codex/MATH/_evidence/reach-completion-20261027/.venv/Scripts/python.exe`, with explicit `UV_CACHE_DIR=C:/Users/jamie/AppData/Local/GCL/uv` and `PYTHONPYCACHEPREFIX=C:/Users/jamie/AppData/Local/GCL/PythonBytecodeCache`. There is no admitted root lockfile; this evidence environment remains unpinned. No installs, host-Python shortcut, hosted compute or deployment occurred.
