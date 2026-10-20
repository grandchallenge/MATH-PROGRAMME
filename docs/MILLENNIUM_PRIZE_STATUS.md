# Millennium Prize Problems: Status in October 2026

<p class="page-deck">Where the seven famous problems stand, including the September Navier–Stokes announcement and new partial advances reported in October. Last checked against primary sources: 20 October 2026.</p>

In 2000, the Clay Mathematics Institute (CMI) named seven mathematical problems, each carrying a one million US dollars prize. One, the **Poincaré conjecture**, is officially solved. An announced Navier–Stokes breakthrough is receiving special attention, but its status has **not** yet changed to “Solved” on Clay's public list. Five other problems remain formally listed as unsolved.

These are **Clay's problem statuses**, not assessments of who deserves prize credit, and not labels for GCL's separate research projects.

## Current position

| Millennium problem | Clay's public status | Recent developments and limits | GCL material |
| --- | --- | --- | --- |
| **Navier–Stokes existence and smoothness** | **Active; announced resolution under evaluation** | On **8 September 2026**, OpenAI reported an analytical proof, with Lean formalization, of finite-time blow-up under smooth forcing, addressing alternatives **C and D** in the official problem formulation. On **11 September**, Clay stated that the problem had *apparently been settled*; its public listing remains **Active**, and the prize review process is continuing. | [Navier–Stokes study](domains/navier_stokes.md) |
| **Poincaré conjecture** | **Solved** | Grigori Perelman's work in 2002–03 established the theorem; Clay awarded its prize in 2010. GCL's material is a reconstruction of that known proof, not a new solution. | [Poincaré archive](domains/poincare_reconstruction.md) |
| **Riemann Hypothesis** | **Unsolved** | The OpenAI mathematics release of **6 October 2026** includes a claimed **zero-free half-plane Re(s) > 7/8**, with a Lean formalization. This is weaker than the hypothesis's critical-line claim **Re(s) = 1/2**; neither publication nor a formal check of a related statement establishes the Millennium conjecture. | [Riemann research](domains/riemann_hypothesis.md) |
| **Hodge conjecture** | **Unsolved** | The **6 October** collection includes a manuscript claiming the rational Hodge conjecture for **complex abelian varieties with complex multiplication**. This is a special family, not the full conjecture for every smooth projective complex variety; the manuscript must be assessed on its actual hypotheses and supporting proof. | [Hodge research](domains/hodge.md) |
| **Birch–Swinnerton-Dyer conjecture** | **Unsolved** | Many important special-case and conditional results are known; no general proof is recognized by Clay. | [Elliptic curves](domains/birch_swinnerton_dyer.md) |
| **Yang–Mills existence and mass gap** | **Unsolved** | Work on restricted settings and continuum constructions does not yet establish both parts of the complete four-dimensional problem. | [Yang–Mills research](domains/yang_mills.md) |
| **P versus NP** | **Unsolved** | Advances in computational complexity and related conjectures do not settle the full equality-or-separation question. | [Complexity research](domains/p_vs_np.md) |

[See Clay's official list of all seven problems](https://www.claymath.org/Millennium%20Problems/).

## The Navier–Stokes announcement needs two distinct labels

The **research announcement** and the **prize authority's disposition** are related, but they are not interchangeable.

OpenAI's [8 September 2026 account](https://openai.com/index/navier-stokes-solution/) describes a solution using smooth external forcing: a fluid starts at rest, has finite energy and nevertheless develops a singularity after finite time. The paper and a formalized Lean proof are publicly linked from that announcement. OpenAI says the result satisfies the *breakdown* alternatives C and D of Clay's official mathematical statement. That differs from showing that every smooth, unforced fluid remains regular.

On [11 September 2026, Clay said](https://www.claymath.org/news/navier-stokes-announcement/) that the problem had *apparently been settled* and that assessment and credit would follow the prize rules. Its [Millennium Problems list](https://www.claymath.org/Millennium%20Problems/) still places Navier–Stokes under **Active problems**, not the Solved category.

**For public reporting, the accurate status is “announced resolution under evaluation,” not an unqualified “solved” or “unsolved.”** GCL has not independently certified the announced global proof.

GCL's [NS-CI-001 campaign](domains/navier_stokes.md) asks a narrower, separate question involving a critical time-integrability estimate for certain unforced weak solutions. It should **not** be reclassified as solved simply because the broader prize problem has an announced forced-flow counterexample.

## What the October results mean for Hodge and Riemann

On [6 October 2026](https://openai.com/index/sharing-ai-progress-in-mathematics/), OpenAI published a large collection of mathematics manuscripts, with formal Lean proofs for some results but not all. The [public repository](https://github.com/openai/math) itself cautions that some unformalized results may require corrections.

Two manuscripts are especially relevant here:

- **Riemann:** [*The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8*](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/README.md). Even if its stated theorem is established, it is **not** the Riemann Hypothesis that all nontrivial zeros have real part 1/2.
- **Hodge:** [*The rational Hodge conjecture for CM abelian varieties*](https://github.com/openai/math/blob/main/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-October-6-2026/README.md). Its claim applies to a significant but **restricted class** of varieties; it is not a solution of the general Hodge conjecture.

These are **reported mathematical advances with their own verification status**, not additional Clay prizes awarded or proofs of the unrestricted Millennium statements. The OpenAI release and subsequent independent mathematical review should be examined at the level of exact theorem statements before any stronger status is published.

## How GCL reports progress

A mathematical **claim**, a machine-checked **formal statement**, an independently reviewed **proof**, a prize body's **public classification** and the decision to **award a prize** are different facts. None should be substituted for another.

For example, a complete and accepted proof of a restricted case of Hodge might be a substantial advance without solving the general conjecture. Similarly, a computer verification of a zero-free region beyond 7/8 is not proof of the critical-line requirement of the Riemann Hypothesis.

The status table is dated **20 October 2026**. It is not a live feed; the [Clay Mathematics Institute](https://www.claymath.org/Millennium%20Problems/) remains authoritative for its own classifications. GCL's domain records separately govern what GCL has actually proved, checked or left unresolved.
