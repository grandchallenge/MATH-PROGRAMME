# RH-WP00 — Charter

**Artifact ID:** `RH-WP00-00-CHARTER`  
**Campaign:** `RH-001`  
**Challenge:** Riemann Hypothesis  
**Work Package:** `RH-WP00`  
**Status:** `LOCKED FOR WP00`  
**Version:** 0.1.0  
**Audit date:** 2026-07-25  
**Claim class:** `SOURCE-NORMALIZED / NON-SOLUTION ARTIFACT`

---

## 1. Binding proposition

For `Re(s)>1`, define

```math
\zeta(s)=\sum_{n=1}^{\infty}n^{-s}.
```

The Riemann zeta function is the meromorphic continuation of this Dirichlet series to `C`, with one simple pole at `s=1`. Define Riemann's completed entire function

```math
\xi(s)=\frac12 s(s-1)\pi^{-s/2}\Gamma\!\left(\frac{s}{2}\right)\zeta(s).
```

It satisfies

```math
\xi(s)=\xi(1-s).
```

A **nontrivial zero** is a zero of `zeta` other than the zeros at the negative even integers. Equivalently, the nontrivial zeros of `zeta` are exactly the zeros of `xi`.

The binding proposition is

```math
\forall \rho\in\mathbb C,
\qquad
\xi(\rho)=0
\Longrightarrow
\operatorname{Re}(\rho)=\frac12.
```

Equivalently, with

```math
\Xi(t)=\xi\!\left(\frac12+it\right),
```

the conjecture states that every zero of the entire function `Xi` is real.

The programme uses `xi(s)` for the completed function in the `s`-plane and `Xi(t)` for its critical-line reparametrization. Bombieri's official description uses `xi(t)` for the latter object; that notation is translated into the present registry rather than copied silently.

## 2. Normative source authority

The binding problem statement is Enrico Bombieri, *Problems of the Millennium: the Riemann Hypothesis*, the official Clay Mathematics Institute problem description:

- <https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf>

Current institutional status is taken from:

- <https://www.claymath.org/millennium/Riemann-Hypothesis/>

The historical statement is source-bound to Riemann's 1859 memoir, with the Clay manuscript collection and the Wilkins English translation used for concordance:

- <https://www.claymath.org/library/historical/riemann/>

Function definitions and standard analytic normalization are cross-checked against the NIST Digital Library of Mathematical Functions:

- <https://dlmf.nist.gov/25.2>
- <https://dlmf.nist.gov/25.4>
- <https://dlmf.nist.gov/25.10>

Later literature may refine zero-free regions, density estimates, verified heights, equivalent criteria, or strategic routes. It may not silently alter the target proposition.

## 3. Object and quantifier lock

The theorem concerns one fixed meromorphic function and **all** of its nontrivial zeros.

The quantifier structure is

```math
\forall \rho\in\mathbb C,
\quad
\bigl[\zeta(\rho)=0\ \land\ \rho\notin\{-2,-4,-6,\ldots\}\bigr]
\Longrightarrow
\operatorname{Re}(\rho)=\frac12.
```

The following are binding:

- zeros are considered with their analytic multiplicities;
- the assertion is global and has no height cutoff;
- the critical line is `Re(s)=1/2`;
- the critical strip is `0<Re(s)<1`;
- the pole at `s=1` is not a zero;
- the zeros at `-2,-4,-6,...` are trivial zeros and are outside the target;
- a proof must cover every nontrivial zero, including multiple zeros if any exist;
- a refutation requires one rigorously certified nontrivial zero off the critical line;
- the classical Riemann Hypothesis is not the Generalized Riemann Hypothesis for Dirichlet or automorphic `L`-functions.

## 4. Admissible terminal outcomes

### 4.1 Proof outcome

A valid proof must establish

```math
\xi(\rho)=0
\Longrightarrow
\operatorname{Re}(\rho)=\frac12
```

without assuming an equivalent or stronger unproved statement.

If the proof proceeds through an equivalent criterion, it must provide or import with exact hypotheses:

1. the criterion's definitions and function spaces;
2. both implication directions;
3. all endpoint, closure, convergence, and multiplicity conventions;
4. the bridge from the proved criterion to the canonical zero statement; and
5. the absence of hidden RH, GRH, simplicity, or spectral-completeness assumptions.

A proof of a finite-height statement, a density-one statement, a positive proportion on the line, a zero-free region, or a consequence of RH is not a terminal proof.

### 4.2 Refutation outcome

A valid refutation must produce a complex number `rho` and an auditable certificate establishing

```math
\zeta(\rho)=0,
\qquad
0<\operatorname{Re}(\rho)<1,
\qquad
\operatorname{Re}(\rho)\ne\frac12.
```

A decimal approximation is not a certificate. An acceptable computational route must include a certified isolating region, a proof that the region contains a zero with the asserted multiplicity, and rigorous bounds excluding intersection with the critical line.

## 5. Core normalization boundaries

The following objects are distinct until an exact correspondence is stated:

- the Dirichlet series for `zeta`, valid initially only for `Re(s)>1`;
- the meromorphic continuation of `zeta`;
- the Euler product, valid in its absolute-convergence region;
- the symmetric meromorphic completion `Lambda(s)`;
- the entire completion `xi(s)`;
- the critical-line entire function `Xi(t)`;
- Hardy's real-valued `Z(t)`;
- the logarithm `log zeta(s)`, which requires a zero-free domain and branch choice;
- the logarithmic derivative `-zeta'(s)/zeta(s)`, which has poles at zeros and at the pole of `zeta`;
- a numerical approximation to a zero and a certified zero enclosure.

The companion `02_FUNCTION_AND_ZERO_LOCK.md` is authoritative for these distinctions.

## 6. Scope exclusions

The following are separate statements or evidence lanes until connected by an explicit theorem:

- the Generalized Riemann Hypothesis;
- Riemann hypotheses for Dedekind, Dirichlet, automorphic, or geometric zeta functions;
- the Weil conjectures over finite fields;
- the Lindelof hypothesis;
- simplicity of the nontrivial zeros;
- Montgomery pair correlation;
- GUE or random-matrix spacing laws;
- zero-density estimates;
- statements that almost all or a positive proportion of zeros lie on the critical line;
- finite verification of zeros;
- prime-counting estimates with the wrong error term or missing uniformity;
- positivity of finitely many Li coefficients;
- spectral resemblance without a self-adjoint operator and exact spectral correspondence;
- formal derivations that import the functional equation, explicit formula, or zero distribution as untracked axioms.

These lanes may support strategy. They do not inherit equivalence to RH by resemblance.

## 7. Claim boundary

This charter claims only that the challenge statement, analytic object, quantifiers, admissible terminal outcomes, and exclusion boundaries have been fixed for `RH-WP00`.

It does **not** claim:

- a proof or disproof of RH;
- a new zero-free region;
- a new proportion of zeros on the critical line;
- a new prime-number error term;
- a new equivalent criterion;
- a Hilbert-Polya operator;
- a certified off-line zero;
- a novelty result.

## 8. Authorization rule

No proposed route may enter mechanism generation or theorem promotion until it states:

1. which normalized function it uses;
2. the domain on which every series, product, integral, and logarithm is valid;
3. all branch and contour conventions;
4. its treatment of the pole and trivial zeros;
5. whether zeros are counted with multiplicity;
6. the exact test-function, Hilbert-space, sequence, or arithmetic criterion used;
7. both directions of every claimed equivalence;
8. whether any step assumes RH, GRH, simplicity, density, or spectral completeness;
9. the arithmetic mode and certification method of every computation; and
10. the exact theorem that connects the local result to the canonical zero statement.

The companion function-and-zero lock is authoritative for items 1-5 and 9.