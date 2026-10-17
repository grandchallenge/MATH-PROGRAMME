# Research and Results

<p class="page-deck">A selection of mathematical work published or examined by Grand Challenge Labs. Each example explains what has been established, why it matters, and what remains uncertain.</p>

## What you will find here

Our work ranges from explaining well-known mathematical questions to checking proofs with computer software and studying problems that are not yet solved. These are different kinds of achievements, and we identify them accordingly.

An article that explains a theorem is not the same as a new proof of that theorem. Likewise, a computer-checked proof confirms a precisely stated mathematical result; it does not, by itself, establish that the result is new.

## The Erdős Compendium: making difficult questions more accessible

The mathematician Paul Erdős posed or inspired a remarkable collection of questions, many of which continue to shape research. Our [Erdős Compendium](erdos/index.md) brings together **1,221 numbered problems**, their original sources, and explanations intended to help readers understand the questions and what is known about them.

<!-- GCL_ERDOS_SHOWCASE_STATUS -->

The collection is still growing. A reviewed article explains the problem and reports established results with supporting references; it does **not** mean that GCL has independently proved every statement discussed.

You can begin with [problem 7](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0007/), [problem 665](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0665/), or [problem 836](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0836/). Each has its own explanation and links to the supporting record.

We have also corrected mathematical equations that previously appeared incorrectly on some pages. The [first set of repairs](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2690) covered 25 articles; [a further correction](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2698) covered four. Both were checked on the published website. The [editorial record](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2701) describes how another group of articles was reviewed and published.

[Browse all the problems](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/catalogue/) · [See how articles are prepared](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_compendium/EDITORIAL_PROTOCOL.md) · [Follow work still in progress](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2552)

## Ten mathematical proofs checked by computer

We independently rebuilt the mathematical files supplied for [OpenAI's Ten Proofs project](OPENAI_TEN_PROOFS_VERIFICATION.md). Using **Lean**, software that checks each step of a formal proof, we confirmed that all ten supplied files could be built and that twelve principal mathematical statements passed the proof checker.

This is evidence about the precise computer-readable proofs and the statements they establish. It is not a claim that we discovered the mathematics, nor that every sentence in the accompanying written explanations has been separately checked.

[Read what was checked and see the supporting records](OPENAI_TEN_PROOFS_VERIFICATION.md)

## A mathematical fact about greatest common divisors

The greatest common divisor of two whole numbers is the largest positive integer that divides both. There is a useful relationship between greatest common divisors and a kind of mathematical structure called a **positive semidefinite matrix**.

We produced and checked a Lean proof of this classical relationship. We also gave an explicit way to represent it using vectors. The result is not a new theorem; the contribution is a documented, computer-checked version of established mathematics.

[Explore the result and an example](LOG_GCD_PUBLICATION.md) · [Read about earlier work](LOG_GCD_PRIOR_ART_AUDIT.md)

## Understanding how folding mechanisms move

In our mathematical research on folding mechanisms, we have established **four specific claims** about a restricted model. A fifth proposed claim remains unsupported, and we do not treat it as proved.

Later work examined the small movements permitted by hinges in the model. The current study asks whether a desired pattern of hinge movement can be achieved by designing a suitable mechanism. There may be several possible designs, and the evidence does not establish that any one design is unique.

These findings concern the mathematical model. They do not show that a physical device can fold without collisions, withstand forces, or be manufactured successfully.

[Read the current folding research and its limitations](CURRENT_WORK.md#vgse-001--mechanical-semantics)

## The Poincaré conjecture: examining an established achievement

The Poincaré conjecture is a celebrated theorem about the shape of three-dimensional spaces. It was solved before this programme began.

Our [reconstruction archive](POINCARE_RECONSTRUCTION_ARCHIVE.md) brings together an examination of the established proof and its sources. It is intended to make the reasoning and its history easier to follow. We do not present it as a new solution.

[Explore the archive](POINCARE_RECONSTRUCTION_ARCHIVE.md) · [Read the accompanying account](documentaries/poincare.md)

## Two small examples of how proofs are checked

Some of the clearest demonstrations of our methods concern elementary mathematics. They show how a claim can be stated precisely, proved, checked, and explained without the complications of an unsolved research problem.

The first example follows the [Euclidean method for finding the greatest common divisor](EUCLID_GCD_E2E_001_PROOF_TRACE.md). The second examines [when an equation involving two whole-number variables has a whole-number solution](EUCLID_DIOPHANTINE_E2E_002_PROOF_TRACE.md).

These are well-known results. Their purpose here is to make the checking process understandable and open to inspection.

## Testing mathematical statements — including their limits

We also publish small experiments that check mathematical identities and examine what happens when their assumptions are changed. One verifies an algebraic identity. Another shows why a statement that holds for one class of mathematical objects cannot automatically be extended to a more general class.

A counterexample can be as valuable as a successful proof: it shows exactly where a claim stops being true.

[Explore these examples](FIXTURE_LEDGER.md)

## Where to follow current research

This page describes work with something concrete to examine: an article, a verified proof, a reconstruction, or a carefully stated result. It is not a list of everything we are trying to solve, and publication here is not evidence of novelty or practical usefulness.

For open questions and continuing investigations, see [Current Work](CURRENT_WORK.md). For the wider research areas and archives, see [Mathematical Estate](domains/index.md).
