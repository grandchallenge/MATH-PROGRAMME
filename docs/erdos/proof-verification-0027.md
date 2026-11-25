# Erdős problem 27: why a short interval of moduli cannot cover almost everything

*Verification record, 25 November 2026; Grand Challenge Labs.*

**Literature status: disproved.** We reconstructed the ordinary mathematical proof of Theorem B of Filaseta, Ford, Konyagin, Pomerance and Yu (2007), including its implication for the original question. We also kernel-checked two finite mathematical components. The complete analytic theorem is not yet formalized in Lean; MATHCERT has not been submitted.

[Original problem](https://www.erdosproblems.com/27) · [Compendium](index.md) · [Verification programme](../ERDOS_PROOF_VERIFICATION.md)

## The question and its answer

Could a fixed constant $C>1$ suffice so that, for every positive tolerance and every sufficiently large starting point $N$, a collection of distinct moduli in $[N,CN]$ covers all but that tolerance of the integers? Each modulus permits a single residue class. The original question quantifies over every starting point; disproving it for arbitrarily large starting points suffices.

A modulus $n$ covers a fraction $1/n$ of the integers. The uncovered fraction for a finite collection is its natural density, computed exactly on a common period. If the events were independent, the uncovered fraction would be the product of the individual avoidance probabilities. In general they are not independent, but the theorem shows that the optimal coverage approaches this product in the specified asymptotic regime.

Let $S$ be a finite set of distinct moduli in $(N,KN]$, and let $\delta^-(S)$ be the minimum uncovered density over all residue assignments. Define

$$
\alpha(S)=\prod_{n\in S}(1-1/n).
$$

For fixed $0<c<1/2$, Theorem B establishes uniformly for $1<K\leq\exp(c\log N\,\log\log\log N/\log\log N)$ that

$$
\delta^-(S)=(1+o(1))\alpha(S).
$$

Take a fixed $C>1$, put $N'=N-1$ and $K=2C$ for integer $N\geq2$, and apply the theorem to the inclusive interval $[N,CN]$. The product is bounded below by the full-interval telescoping product:

$$
\alpha(S)\geq\frac{N-1}{\lfloor CN\rfloor}\longrightarrow\frac1C.
$$

For all sufficiently large integer $N$, every choice of residues leaves density at least $1/(2C)$. Choosing tolerance $1/(4C)$ disproves the assertion. This is a reconstruction of the published disproof, not a new priority claim.

## The mathematical mechanism

1. The finite correlation inequality (Lemma 2.1) bounds the extra coverage obtainable from correlated events.
2. The smooth/rough decomposition (Lemma 3.1) splits each modulus into its small-prime and large-prime factors. The Chinese remainder theorem gives an exact average of uncovered densities over smooth fibres.
3. Lemma 3.2 bounds the average correlation cost. Lemma 3.3 controls the geometric mean of the positive fibre products, accounting for fibres covered by a modulus-one projection. Lemma 3.4 combines these estimates.
4. A tilted finite Euler product gives the smooth reciprocal tail (Lemma 4.1), without importing a smooth-number distribution theorem. Choosing an intermediate cutoff exponent strictly between $c$ and $1/2$ makes both the smooth-only coverage and relative correlation error tend to zero. A greedy residue assignment supplies the matching upper bound.

The [complete ordinary reconstruction](https://github.com/grandchallenge/MATH-PROGRAMME/blob/0f3715ad5c6721ae7255ee36f70ca568e9a8c708/governance/erdos_proof_verification/evidence/0027/THEOREM_B_ELEMENTARY_RECONSTRUCTION_001.md) and companion proofs are stored in the protected evidence directory. This reconstruction covers distinct-modulus Theorem B, not the paper's more general multiplicity theorem.

## What Lean actually checked

The first module proves the exact rational finite-density average from explicit coprime factorization and divisibility hypotheses, using the CRT equivalence. Six declarations were audited for axioms; three false variants were rejected and their negations proved.

The second module proves the finite event-counting inequality and its propagation over an arbitrary finite sequence, conditional on the joint-independence identity. Thirteen positive declarations and three named counterexamples were checked. Both modules use Lean 4.33.0 and pinned Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`. All audited declarations use only the standard axioms propext, Classical.choice and Quot.sound; no sorryAx.

The remaining formal work includes deriving joint independence and each event's mass from the arithmetic CRT model, constructing the prime-power split and common period, proving natural-density convergence, and formalizing the analytic inequalities. Finite regression evidence and ordinary proofs do not stand in for those kernel obligations.

## Evidence and reproducibility

| Scope | Protected admission |
| --- | --- |
| Source and finite correlation proof | [#3705](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3705), [custody #3715](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3715) |
| Smooth/rough decomposition and correlation analysis | [#3720](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3720), [#3727](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3727), [#3728](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3728) |
| Complete distinct-modulus Theorem B | [#3736](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3736) |
| Finite CRT Lean proof | [#3735](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3735), [custody #3741](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3741) |
| Finite weighted recurrence Lean proof | [#3743](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3743) |

The [protected evidence directory](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/governance/erdos_proof_verification/evidence/0027) contains the ordinary proofs, exact finite replay programs, kernel source references, compiler stdout and hostile controls. Reproduce the finite checks using the Python programs there, and the formal proofs using the registered `erdos-pv-0027-crt` lane in `governance/formal_validation_registry.json`. Author and critic roles were separately scoped but performed by the same accountable GCL operator, not independent external referees. The [cohort ledger](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_proof_verification/coverage/cohorts/0001-0100.json) controls documentary admission, not mathematical certification.

**Primary source:** Filaseta, Ford, Konyagin, Pomerance and Yu, *Sieving by large integers and covering systems of congruences*, Journal of the American Mathematical Society 20 (2007), 495–517, [DOI](https://doi.org/10.1090/S0894-0347-06-00549-2), [author manuscript](https://ford126.web.illinois.edu/wwwpapers/coverings.pdf), 21 December 2006, Theorem B and Lemmas 2.1, 3.1–3.4, 4.1. Original Er95 scan was not inspected independently. **MATHCERT: NOT_SUBMITTED.**
