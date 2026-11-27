---
description: An illustrated reader guide to collision information, renormalization and gluing for the one-dimensional free scalar field studied by REACH.
hide:
  - navigation
---

# What survives a collision?

<p class="page-deck">A reader’s guide to the renormalized free scalar. Follow two field positions as they come together, then see why a cover by two separate intervals misses nine products.</p>

[Download the illustrated reader guide (PDF)](../assets/reach-reader-guide.pdf)

!!! note "Research status · 26 November 2026"
    The proofs cover the declared one-dimensional Gaussian/Wick model and its controlled singular kernels. They give a renormalized quantum structure, a liquid model that retains collision information, and completed gluing. The original support-stage equivalence fails in ZFC. The original strong completion criterion remains unmet.

## What happens when two slots meet?

A scalar field associates one quantity with each place on a line. A local observable tests the field against a smooth function supported in a region. When we combine several tests, the kernels that describe their joint behavior have several positions, called **slots**.

As two positions come together, part of a kernel can concentrate along their coincidence. The construction first controls that approach with a regulator. It then subtracts the singular terms and keeps a record of how they approached the collision. Further operations use the record. A separate readout gives the finite physical answer.

For two positions $x_1,x_2$, let $c$ be their midpoint and $z=x_1-x_2$ their separation. The three pair-collision measurements use these tests:

$$
1,\qquad c,\qquad x_1x_2=c^2-\frac{z^2}{4}.
$$

The last test picks up a second derivative across the collision, because it contains the square of the separation. The midpoint alone would miss that contribution. In the liquid model the corresponding coordinates stay available for composition. [Pair moments and the normal derivative](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/COLLISION_LIQUID_WEIGHT_TWO_UC092.md)

## Why use a liquid model?

Liquid mathematics gives continuous families, their coefficient spaces and their derived products a common setting. The construction keeps smooth parameter derivatives and respects the rule for discarding differences that decay rapidly as the regulator is removed. Every group of coincident slots has its own polynomial moment coordinates.

Separated regions compose over one shared vacuum algebra. The empty region supplies that same unit. Each finite-weight term can involve only finitely many components, while different weights may use different components. The completed model holds these weights together. The derived product also works for two general complete inputs. For an example, take two copies of the vacuum with the formal quantum parameter $\hbar$ set to zero. The derived product keeps an extra relation class that records this shared constraint. [All-weight collision model](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) · [Completed derived product](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md)

## Why nine products go missing

On a single interval, the simpler field tests use an affine function $a+bx$, given by its intercept and slope. Its square has three coefficients. The **affine readout** replaces each independent pair-collision measurement by the corresponding quadratic expression in the one-slot measurements. Each difference is a relation that the readout sends to zero. The derived comparison records one class for each such relation, at **weight two and degree minus one**. Here total weight counts one per slot and two per power of $\hbar$.

Now take two disjoint intervals with relation coordinates $L_0,L_1,L_2$ and $R_0,R_1,R_2$. Exchanging the factors of a product of two relations reverses its sign, so each unordered pair of distinct coordinates counts once. There are three products using only left coordinates and three using only right coordinates. The nine mixed products have one coordinate from each side.

| Left factor | Right factor $R_0$ | Right factor $R_1$ | Right factor $R_2$ |
| --- | --- | --- | --- |
| $L_0$ | $L_0\wedge R_0$ | $L_0\wedge R_1$ | $L_0\wedge R_2$ |
| $L_1$ | $L_1\wedge R_0$ | $L_1\wedge R_1$ | $L_1\wedge R_2$ |
| $L_2$ | $L_2\wedge R_0$ | $L_2\wedge R_1$ | $L_2\wedge R_2$ |

The union has **15 products** in this sector, at weight four and degree minus two. A cover by the separate intervals sees the six products confined to a single patch. It misses **all nine mixed products**. [Derived relations and the interval merger](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/AFFINE_READOUT_DERIVED_RELATIONS_UC108.md)

<details>
<summary>Try it: what happens if both intervals sit inside one larger interval?</summary>
<p>The two triples of pair relations map to one by addition. L0 and R0 now denote the same class, and likewise for indices 1 and 2. The three products with matching indices vanish because an exterior product of a class with itself is zero.</p>
</details>

## Which covers suffice?

A cover that places any two chosen points in a common patch recovers all fifteen products in the example. The general result allows us to determine how many points a cover needs to see together. For the summand of weight $w$ and intrinsic cohomological degree $-q$, with $2q\le w$, it suffices that every set of up to $w-q$ points lies in one patch. These numbers count how many block centers a term can involve. The bound is sharp as a uniform guarantee. A **Weiss cover** has the joint containment property for every finite set, so it gives gluing at every weight, including on opens with infinitely many components. [All-open descent and the sharp example](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/AFFINE_RELATIONS_WEISS_DESCENT_UC111.md)

## Where the original programme stands

| Question | Supported result |
| --- | --- |
| Can the specified free-field singularities be handled consistently? | The subtraction records support the quantum identities and disjoint-region composition for the declared class. |
| Can liquid mathematics keep track of what happens at collisions? | The moment model retains the collision coordinates. The relations forgotten by the affine readout and their products have completed Weiss gluing. |
| Do the original liquid support stages match the observable stages? | Their proposed equivalence fails in ZFC. The difference is already visible at the vacuum. |

In the old diagram the larger support stages admit functions supported outside the smaller ones. Every stage of the actual vacuum has the same scalar algebra, with identity transitions. A stage-by-stage equivalence would have to take a strict inclusion to an isomorphism.

A separate degree-two question asks whether every global liquid extension class comes from a bounded support stage. In ZFC the classes from bounded stages stay distinct. The continuum hypothesis gives a global class outside all bounded stages, while the partition principle PH1 gives bounded-stage representatives under its hypotheses. The class under the continuum hypothesis survives in the intermediate smooth extension group and vanishes under evaluation on actual observables. [Qualified programme verdict and exact foundation assumptions](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/REACH_QUALIFIED_CLOSEOUT_UC088.md)

## Proofs and further reading

- [The renormalized quantum rules](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/RENORMALIZED_QUANTUM_STRUCTURE_111.md)
- [Evidence and review for the gluing theorem](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/EXT-015/AFFINE_RELATIONS_WEISS_ACCEPTANCE_UC113.md)
- [Maintained research guide](https://github.com/grandchallenge/MATH-PROGRAMME/blob/6d62912eae2c3f37004822513204d29864bc75d9/research/condensed-qft/ACCESSIBLE_RESEARCH_GUIDE.md)
- [An introduction to condensed mathematics](../CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md)
