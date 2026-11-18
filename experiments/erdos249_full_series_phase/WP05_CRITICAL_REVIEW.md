# Erdős #249 WP05 — source-critical and adversarial mathematical audit

**Role:** non-authoring logical Adversary/Referee pass, staffed by the *same* authenticated GCL agent as the manuscript author. No separately authenticated reviewer, independent human review, Lean theorem verification, MATHCERT certification, or novelty decision is claimed.  
**Original conjecture:** OPEN.  
**Reviewed manuscript SHA-256:** 56b75a6bda4ed0aabe1bc2e38f3d3f37b52c6a330a6d14fad6d4f2be3359afd8.  
**Reviewed executable SHA-256:** c885a1b83899003e6b7957a22b7fb109ee2cb9ed63f7e6ab4cfbcfdab8946f8f.  
**Reviewed tests SHA-256:** 0bf21b79437e3a079e260841f190f9ee7c1c178920ff609036d0e7ddae9271f6.  
**Exact executed input branch head:** cfa063ae3cfcb6d9a07ef6a0ed2a762953605ea5.

## Challenge 1 — Are the CRT congruences really reduced?

Yes. The construction chooses distinct auxiliary primes $q_t$ exceeding all positive offsets, with $q_t\equiv1\pmod{2^{K_0}}$. The desired base class is three modulo four, a unit. At every auxiliary modulus the chosen residue is $-t$, nonzero because $0<t<q_t$. Each modulus is pairwise coprime, so the CRT class is a unit modulo its full product. Dirichlet's theorem applies to it, including the cofinal quantified bound $p>B$.

## Challenge 2 — Can a shared offset invalidate the finite-family claim?

No. When two shifts refer to the same integer offset, the construction uses a **set**, not duplicate incongruent assignments. One prime $q_t$ forces the required divisibility for all appearances of that offset. Duplicate shifts and overlapping offset intervals therefore cannot introduce conflicting congruences. The unit class remains valid for any **fixed finite** family; neither a single class for infinitely many shifts nor uniformity in a moving family is claimed.

## Challenge 3 — Does divisibility of the totient follow if the constructed prime divides the argument to a higher power?

Yes. For every positive integer $n$ divisible by a prime $q$, the Euler totient formula contains the multiplicative factor $q-1$. Thus $q-1\mid\varphi(n)$ even when $q^2\mid n$. The argument does not require a squarefree multiple. Since $q_t\equiv1\pmod{2^{K_0}}$, the stated power-of-two divisibility follows.

## Challenge 4 — Is the infinite-tail conclusion being oversold?

No. The finite-front sum is integral when $K\ge L$, but its omitted difference has only a valid **upper** bound proportional to $p/2^L$. Divergence of that bound at fixed depth is not divergence or nonintegrality of the actual error. A rational finite-prefix comparator can reproduce a fixed finite pattern. Therefore no irrationality statement follows. We explicitly reject any use of finite prime searches as a proof of Dirichlet or of nonintegrality of the full tail.

## Challenge 5 — Does the Cook midpoint same-depth no-go really apply to every residue?

Yes. Under Cook Proposition 6.92, $K\ge2$ makes the $j=1$ condition available, and $2^K\mid\varphi(p-1)$ holds. This is a strictly positive integer at least $2^K$, while $\varphi(p-1)\le p-1$. Thus $p+2>2^K-1$, which exceeds **every** possible residue modulo $2^K$. The necessary lower inequality in Cook's directed finite certificate cannot hold at that same start and same depth, regardless of the midpoint congruence. This does not contradict the proposition, and does not rule out deeper certification, sharper tail estimates or other prime families. It is a statement about the standard **same-depth** test.

## Challenge 6 — Antecedents and epistemic independence

Cook's 2026 Propositions 6.69, 6.70, 6.91 and 6.92 already establish the critical context, a mod-four pulse, and a high-valuation backward-window witness. The forward simultaneous finite-family adaptation is an elementary CRT/Dirichlet deduction, not claimed as a discovery of the underlying method or as novel. The critical logical audit is not by a separate human or authenticated specialist identity. Mathematical manuscript arguments, machine tests, CI admission, and reserved mathematical certification remain separate.

## Critical disposition

**ACCEPT_WITH_SCOPE** for the bounded research manuscript, exact-source tests and clearly qualified same-depth obstruction. **NO** full-series irrationality proof, theorem certification, independent endorsement, or automatic source priority claim. Continue only to a well-quantified two-scale arithmetic-plus-analytic criterion, with honest bounds and falsification against rational controls.

**Execution before this review:** CHAD authenticated operator shell ran twelve standard-library test cases, all PASS, and the mathematical Markdown source gate PASS at the exact reviewed source head. Test stdout SHA-256 f6fb36880d4f930052e9c6d6ad31bb3b4105ea2901758d79ec5be9e7cbccdafe; gate log SHA-256 d4e8fa67794c1c864f92783e049a32dc4a554a844b44e191677da8ccc910e1cc. Protected admission remains a separate operation.
