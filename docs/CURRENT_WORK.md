# Current Work

<p class="page-deck">The mathematical questions GCL is investigating, what recent work has clarified and what researchers still need to establish. This is a selected overview, not a list of every active task.</p>

Some projects aim to prove long-standing conjectures. Others try to understand exactly why an attempted proof is incomplete, or to find out what a mathematical model can reliably predict. A careful negative result or a precisely identified gap can be useful progress even when the central problem remains unsolved.

Research changes quickly. The links below lead to the original work and its latest recorded status. A completed work package is not necessarily a solved mathematical problem.

<a id="bsd-001--literal-p2-inverse-limit-replay"></a>

## Elliptic curves: the Birch–Swinnerton-Dyer conjecture

One of the great open problems in number theory asks how much can be learned about the rational solutions of an elliptic curve from a function associated with that curve. The full Birch–Swinnerton-Dyer conjecture has not been proved.

GCL has been examining a technically difficult case involving the prime number **2**. The challenge is to connect results that hold at individual, finite stages to the stronger statement needed when those stages are brought together. This connection requires additional assumptions; it cannot be declared valid simply because the finite calculations succeed.

An earlier study of this particular transition, known internally as *WP60S*, is **closed**. The larger [BSD research programme](https://github.com/grandchallenge/MATHSOLVE/issues/215) remains open. Its continuing work concerns the parts of the argument that are not yet adequately justified, including delicate questions of nonvanishing and compatibility.

**What is established:** selected finite-stage arguments and bounded investigations have been recorded and reviewed. **What remains:** a complete proof of the relevant broader conclusions without relying on assumptions that have not been established. Closing an intermediate study does not solve the BSD conjecture.

[Follow the overall research](https://github.com/grandchallenge/MATHSOLVE/issues/215) · [Read the completed inverse-limit study](https://github.com/grandchallenge/MATHSOLVE/issues/245)

## The odd zeta values: can a large calculation become an exact proof?

At odd positive integers, values of the Riemann zeta function have properties that are still difficult to understand. One line of work examines intricate algebraic identities related to these values.

Researchers have identified a **576-dimensional space of allowable changes** in one order-seven calculation. This is a genuine structural result: it greatly narrows what a successful calculation could look like. It is not yet the final mathematical certificate being sought.

The next obstacle is to find a simpler expression that satisfies all the required identities, then check that expression exactly. A pattern that works in many numerical tests is not enough to prove that it works in general.

**What is established:** the restricted calculation's underlying structure has been identified. **What remains:** a complete, independently checked certificate for the intended broader claim. No proof or refutation of the larger T3 target is claimed.

[Examine the current order-seven investigation](https://github.com/grandchallenge/MATH-PROGRAMME/issues/964)

<a id="vgse-001--mechanical-semantics"></a>

## Folding mechanisms: can a desired movement determine a design?

Imagine a network of rigid panels joined by hinges. If we specify how strongly each hinge should participate in a small movement, can we work backwards to find a suitable arrangement of panels and hinges?

Earlier research isolated **four independent ways** in which a restricted mathematical model of such a mechanism can move. The current study investigates whether desired patterns of hinge participation can be realized by one or more designs.

A central difficulty is that different arrangements may produce the same reported pattern. The question is therefore not necessarily to recover *the one correct design*, but to identify suitable examples while keeping track of genuine alternatives.

**What is established:** the four-dimensional motion space and certain distinctions between geometric arrangements in the restricted model. **What remains:** a dependable method for finding designs with chosen movement profiles and understanding when the information is insufficient to distinguish them.

The model concerns tiny motions around a flat configuration. It does **not** establish that a physical structure can fold through a large movement without collision, withstand loads or be manufactured successfully.

[Read the continuing design study](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1179) · [Explore the broader mechanical-semantics research](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1084)

## P versus NP from above: quantum verification and classical lower bounds

A new bounded line of inquiry asks whether the recursive compression techniques underlying the established theorem $\mathsf{MIP}^{*}=\mathsf{RE}$ can reveal a structural invariant of finite **classical** computation. Existing work has isolated an important obstacle: very large entanglement requirements for winning a nonlocal game do not by themselves imply that the corresponding yes/no question is difficult to decide.

The first GCL work package records a magic-square calibration, a source-pinned compression ledger and a nine-level finite verifier with an exhaustive 512-vector emulator. A theorem-derived cofinite-language observation makes the resource-versus-decision distinction explicit. **What remains:** an exact encoded compression instance, an independently proved classical resource lower bound and the missing uniform SAT-to-realization transfer. No new P versus NP theorem is claimed.

[Explore the PNP-ABOVE documentary](pnp_above/index.md) · [Read the technical record](pnp_above/technical.md) · [Follow the Solve-owned research obligation](https://github.com/grandchallenge/MATHSOLVE/issues/1136)

## Other investigations worth following

### Condensed mathematics

This area studies ways of organizing topological and algebraic objects so that difficult operations behave more reliably. GCL has formalized particular mathematical steps and is working on further claims and independent review. A previously highlighted finite-stage assignment, [#662](https://github.com/grandchallenge/MATH-PROGRAMME/issues/662), is **complete**; it should not be mistaken for an unfinished task.

The current questions include [separation at a one-point component](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1162) and [independent mathematical review](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222). These concern particular results and their assumptions, not the resolution of every problem in condensed mathematics.

[Introduction for new readers](CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md) · [Published mathematical result and qualifications](CMDG_CM4.md)

### The mathematics of fluid flow

The Navier–Stokes equations describe fluid motion. A major unresolved question is whether their three-dimensional solutions can develop singularities from smooth starting conditions.

GCL is examining a narrower question involving how certain measures of a solution's size behave over time. Establishing an estimate for that restricted setting would be useful, but it would not by itself prove smoothness for all three-dimensional flows.

[Follow the Navier–Stokes investigation](https://github.com/grandchallenge/MATH-PROGRAMME/issues/55) · [Explore the research area](domains/navier_stokes.md)

## Following the evidence

These summaries explain selected research directions; the linked studies provide precise definitions, calculations, assumptions and unresolved steps. Their dates and task statuses may change as work advances.

A numerical check proves only the cases actually checked. A computer-verified formal proof establishes the exact statement submitted to its checker, including its assumptions. Neither automatically settles a stronger question written in ordinary language.

For established results and accessible examples, visit [Research and Results](SHOWCASE.md). For the broader landscape of mathematical questions, see the [Mathematical Estate](domains/index.md).
