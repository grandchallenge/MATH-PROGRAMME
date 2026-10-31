# P versus NP from Above: What Quantum Verification Might Teach Us About Computational Difficulty

**GCL PNP-ABOVE · Working manuscript · 31 October 2026**  
**Audience:** Educated general reader  
**Status:** Expository and exploratory. No proof of P versus NP, no new lower-bound theorem, and no claim of mathematical certification.  
**Companion research obligation:** [PNP-ABOVE-WP00](https://github.com/grandchallenge/MATHSOLVE/issues/1136)  
**Parent programme:** [PNP-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162)

## The easy question that nobody knows how to answer

Imagine being given a vast jigsaw puzzle. Someone who has completed it can show you the picture. You can check that the pieces fit without working out how they were assembled. But does the existence of a fast way to check the result imply that there must be a fast way to find it?

This is the intuition behind the P versus NP problem. P is the class of yes-or-no problems that a deterministic computer can decide in time bounded by a polynomial in the length of the input. NP is the class whose *yes* instances have certificates that can be checked in polynomial time. A proposed satisfying assignment for a Boolean formula is a familiar example: checking it is easy, while no polynomial-time algorithm for finding one on every satisfiable input is known.

It is tempting to infer that solving must be harder than checking. That inference is not a proof. Sometimes a difficult-looking search problem conceals an efficient algorithm; sometimes a proposed certificate gives no hint about where to find one. Whether every problem in NP is in P remains unknown.

Our inquiry starts from an unconventional direction. Instead of examining only this local boundary, we look far above it, toward one of the strangest results in modern theoretical computer science.

## A verifier who consults two extraordinary witnesses

An *interactive proof* changes the checking process. A verifier asks questions of one or more provers and accepts or rejects after observing their replies. The verifier runs an efficient classical algorithm. The provers need not be efficient.

With several provers, the verifier can arrange that their answers must agree even though the provers are not allowed to communicate once the questioning begins. Think of two witnesses interviewed separately and cross-examined on related details. The verifier is not asking them to enumerate every fact. It asks a small number of pointed questions whose answers must fit a large common story.

The analogy has a limit: mathematical provers are strategies, not necessarily people or honest witnesses. Soundness says that *even cheating strategies* cannot make a false statement pass above a specified probability.

In classical multi-prover interactive proofs, the class MIP coincides with NEXP, a class of problems decidable by nondeterministic computation in exponential time. Giving the provers shared quantum entanglement changes the mathematical model. Quantum measurements can exhibit correlations unavailable to classical strategies.

In 2020, Zhengfeng Ji, Anand Natarajan, Thomas Vidick, John Wright and Henry Yuen proved the remarkable equality:

$$
\mathsf{MIP}^{*}=\mathsf{RE}.
$$

Here RE is the class of recursively enumerable languages: yes instances can eventually be recognized by a Turing machine, but the machine is not required to halt on no instances. It includes the Halting Problem, which is undecidable.

The theorem does **not** mean a small ordinary computer can solve the Halting Problem. It means that for each appropriate language there is a polynomial-time classical verification protocol with computationally unbounded entangled provers, under the completeness and soundness conventions of the theorem. The resources of those provers are not resources available to an ordinary efficient SAT algorithm.

This is the first crucial distinction: **efficient checking through a powerful interface is not efficient independent solving.**

## A small window onto a huge computation

The proof draws on a deep collection of ideas: algebraic consistency tests, rigidity against quantum strategies, and recursive compression of verification procedures.

For an intuition, imagine a building containing an immense archive. A visitor cannot read every document, but can ask a carefully designed set of questions that expose contradictions in a claimed index. A good audit is far smaller than the archive it checks.

Now imagine recursively auditing not only the archive but the method used to audit the archive. Descriptions of large verification tasks can be linked to smaller verification tasks, with sharply controlled completeness and soundness. The actual mathematical construction is far subtler than a literal nesting of boxes; in particular, each round must maintain quantitative guarantees under entangled strategies.

Recursive compression combines with computability-theoretic fixed-point reasoning in the MIP* = RE result. Together these techniques create a verification model powerful enough to recognize every recursively enumerable language.

The surprise is not that an infinite amount of computation has been squeezed into an ordinary fast algorithm. It has not. The surprise is how much difficulty can be delegated to a constrained interaction while keeping the verifier efficient.

## Why this might matter for P versus NP

There are two different kinds of compression:

1. **Verification compression:** a short protocol tests a property of an enormous computation or proof.
2. **Computational compression:** a short, efficient algorithm actually performs the work needed to decide the answer.

No theorem says the first must entail the second. P versus NP is difficult precisely because such gaps are hard to prove unavoidable in the classical finite setting.

Our research hypothesis is therefore not that MIP* = RE directly proves P is different from NP. It is narrower and testable:

**Some finite structural invariant of recursive verification compression might resist efficient classical realization, and might be expressible as a rigorous lower bound in a restricted classical computational model.**

An *invariant* here means a property that remains identifiable and controlled as the verification problem is transformed. A candidate might involve consistency constraints, a quantitative cost of implementing a family of games, or the inability of particular classes of classical strategies to preserve a verification gap.

The phrase “classical realization” is deliberately strict. Entanglement dimension, circuit size, running time, communication cost, proof length, and the size of a game's description are different resources. A lower bound for one cannot simply be relabelled a lower bound for another.

## The missing bridge

Suppose we construct a family of finite verification games, indexed by input length, and define a precise classical cost measure:

$$
\mathcal{C}_{\mathcal{A}}(G_n).
$$

The symbol means the least cost of implementing the desired game behavior using strategies from a declared classical model A. Before this quantity is meaningful, we must define that model: Are strategies deterministic or randomized? Can the provers communicate? Is advice allowed? How many bits are exchanged? What error is tolerated? Are the strategies required to be uniformly computable?

A substantive restricted result might show that this cost grows faster than every fixed polynomial for a carefully specified family. But that would still not solve P versus NP.

To use such a result, we would additionally need an implication of the form:

$$
\text{polynomial-time SAT algorithm}
\quad\Longrightarrow\quad
\mathcal{C}_{\mathcal{A}}(G_n)\leq n^{O(1)}.
$$

The implication must include a uniform construction and all size and error overheads. If it does not exist, the game lower bound tells us something about that game model, not about SAT.

This **transfer theorem** is the project's critical missing bridge. We should expect it to be hard, and we should not presume it exists.

Indeed, there is a simple warning. A verification game can demand enormous resources from particular players while the yes-or-no property associated with its instance is easy to decide. That does not contradict anything. A resource bound on how an interaction is implemented is not automatically a time bound on deciding a language.

## Quantum structure as an instrument, not a shortcut

The quantum aspect provides unusual mathematical leverage. Noncommuting measurements, algebraic tests and rigidity theorems can force behavior that is impossible or expensive for restricted classical strategies.

Perhaps a classical shadow of these constraints produces a new lower-bound technique. Perhaps the genuinely useful structure disappears as soon as the quantum resources are taken away. Both are informative outcomes.

The second possibility must be actively tested. Otherwise we risk proving that quantum strategies behave differently from classical strategies—which is already known—and mistaking that for progress on classical computational complexity.

A later proposed refinement of compression in the commuting-operator setting, including a weak-compressibility perspective, supplies another setting for comparison. It should not be confused with the tensor-product model or used to infer a classical complexity separation without proof.

## Barriers that cannot be wished away

Complexity theory has a history of apparently convincing proof strategies that cannot establish P versus NP by their intended means.

**Relativization.** Oracle results show that broad forms of black-box reasoning cannot settle P versus NP uniformly over arbitrary oracles.

**Natural proofs.** Under standard cryptographic assumptions, a wide class of constructive, broadly applicable properties cannot prove sufficiently strong general circuit lower bounds.

**Algebrization.** Even some techniques more sophisticated than ordinary relativization remain unable to resolve the problem if their conclusions persist under certain algebraic oracle extensions.

These are not universal impossibility theorems for every conceivable argument. But a serious research programme must identify exactly why a proposed method is not ruled out—or honestly state that it has not yet passed this test.

The fact that MIP* = RE uses quantum entanglement and self-reference does not, by itself, evade any of the three barriers.

## A finite experiment before a grand theorem

The sensible first move is modest.

Select one source-pinned, finite family of verification games arising from a compression construction. Write down every parameter. Choose one restricted classical strategy model. Identify one invariant and attempt one quantitative claim.

If the claim fails, find a counterexample. If it succeeds, compare it with known results to determine whether it is new. Then formulate the transfer to an ordinary classical decision problem. If the transfer fails, identify the exact missing or false lemma.

This process is not an exercise in producing a sequence of increasingly ambitious conjectures. It is a way to turn an attractive analogy into a chain of statements that can be independently checked or refuted.

The first work package, PNP-ABOVE-WP00, is intentionally limited to source normalization, a finite model, one restricted target, and the transfer audit. It does not authorize a claim about the full P versus NP problem.

## What success would look like

There are several meaningful outcomes.

A **negative transfer theorem** could prove that a tempting compression-to-SAT argument cannot work in a specified setting. That eliminates a false route and establishes a useful boundary.

A **restricted classical lower bound** could reveal a new invariant even if it does not transfer to all classical algorithms.

A **uniform transfer theorem** would be substantially more significant: it would connect a well-defined game cost to a familiar computational model, with quantitative overheads and without importing unbounded quantum resources.

Only after these steps could one contemplate an unrestricted complexity separation. A polynomial-size circuit lower bound for an explicit NP language, for example, would imply the stronger claim that NP is not contained in P/poly, and cannot be treated as an easy proxy for P versus NP.

The programme succeeds intellectually if it discovers exactly which form of verification compression creates an unavoidable classical cost—or proves that its proposed mechanism does not.

## The perspective from above

P versus NP asks whether efficiently checking an answer always means efficiently finding an answer. MIP* = RE reveals an extreme form of separation between the smallness of a verifier and the power of the resources answering it.

These are different questions, but they share a structural theme: **what is the price of converting evidence into computation?**

The value of approaching P versus NP “from above” is not that the higher theorem makes the lower problem easy. It is that it supplies an unfamiliar mathematical laboratory. We can study compression, rigidity and self-reference at scales where their mechanisms are unusually visible, then ask exactly which pieces survive when everything is reduced to finite classical computation.

The wager is that a useful invariant may survive the descent. Whether it does is the open research question.

---

## Reader's notes: terms and cautions

- **Polynomial time:** an upper bound of the form $n^k$ for a fixed exponent $k$, with input length $n$.
- **NP witness:** a polynomial-length certificate for a yes instance, verifiable by a deterministic polynomial-time algorithm.
- **RE:** semidecidable languages; yes instances are eventually recognized, while no instances need not terminate.
- **Entanglement:** quantum correlations that can exceed classical shared-randomness correlations in appropriately designed experiments.
- **Rigidity:** a theorem forcing successful strategies to exhibit a constrained mathematical structure.
- **Uniformity:** a single effective construction works across input lengths, rather than obtaining unrelated advice or circuits at each length.
- **Promise gap:** a specified separation between cases a verifier must accept with high probability and cases it must reject with high probability.

## Primary references and further reading

1. Z. Ji, A. Natarajan, T. Vidick, J. Wright and H. Yuen, “MIP*=RE,” [arXiv:2001.04383](https://arxiv.org/abs/2001.04383). Version 4 posted 16 October 2026; final-version and proof-detail audit pending WP00.
2. Z. Ji, A. Natarajan, T. Vidick, J. Wright and H. Yuen, “Quantum soundness of the classical low individual degree test,” [arXiv:2009.12982](https://arxiv.org/abs/2009.12982).
3. J. Lin, “MIPco=coRE,” [arXiv:2510.07162](https://arxiv.org/abs/2510.07162). Research preprint; its claims and technical dependencies require a separate source review.
4. T. Baker, J. Gill and R. Solovay, “Relativizations of the P=?NP Question,” SIAM Journal on Computing 4 (1975).
5. A. Razborov and S. Rudich, “Natural Proofs,” Journal of Computer and System Sciences 55 (1997).
6. S. Aaronson and A. Wigderson, “Algebrization: A New Barrier in Complexity Theory,” ACM Transactions on Computation Theory 1 (2009).
7. GCL, [PNP-001 campaign tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162), for the existing definition, encoding and certification boundaries.

*Editorial note: analogies are explanatory, not proof sketches. This manuscript describes an authorized exploration and will be updated only as source-pinned mathematical evidence is obtained.*
