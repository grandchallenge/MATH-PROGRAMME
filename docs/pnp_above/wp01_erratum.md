# PNP-ABOVE — Source erratum and WP01 mathematical update

**Edition:** 1 November 2026  
**Record type:** documentary erratum and research-status update  
**Source:** [Ji et al., MIP*=RE, arXiv:2001.04383v4](https://arxiv.org/pdf/2001.04383v4)  
**GCL research record:** [MATHSOLVE PR #1152](https://github.com/grandchallenge/MATHSOLVE/pull/1152)  
**Claim level:** source-interpretation discrepancy and bounded classical facts; no mathematical certification.

## Theorem 12.1: statement versus proof

The displayed **statement** of Theorem 12.1 on printed page 184 gives, for the specified bounded nine-level input verifier and sufficiently large index,

$$
\mathcal E(V_n^{\mathrm{compr}},1/2)
\geq
\max\left\{
\frac12\mathcal E(V_{2^n},1/2),
2^{(2^n)^\lambda-1}
\right\}.
$$

However Table 2 (printed page 186) and the **last displayed proof chain** (printed page 189) yield only

$$
\mathcal E(V_n^{\mathrm{compr}},1/2)
\geq
\frac12\max\left\{
\mathcal E(V_{2^n},1/2),
2^{(2^n)^\lambda-1}
\right\}.
$$

The bounds differ by a factor of two in the second branch of the maximum. Earlier GCL material described the *weaker proof-supported form* as the **exact statement** of Theorem 12.1. That description was inaccurate; the same weaker formula remains a justified conservative consequence of the displayed proof.

The source may admit an additional argument recovering the stronger second term, or this may be a typographical discrepancy. **Neither possibility has been established.** In the absence of a reconciliation, GCL uses the weaker proof-backed quantitative statement, and does not present either reading as a new GCL theorem.

For the nine-level diagonal input used in WP00, this provides the conservative bound

$$
\mathcal E(G_n,1/2)\geq 2^{2^{\lambda n}-2}
$$

under the source theorem's encoded-input, normal-form, boundedness, and index hypotheses. The resource is Schmidt rank, not classical running time.

The version 0.1 PDF preprint is preserved unchanged as an issued research edition. This erratum is its **public companion correction**, not a silent alteration of the binary PDF.

## A classical sampling bound

For a classical verifier that must produce exactly uniform m-bit output itself from at most r fair random bits, without additional randomness, the output distribution P obeys

$$
d_{\mathrm{TV}}(P,U_m)\geq 1-2^{r-m}\qquad(0\leq r\leq m).
$$

Reason: there are at most $2^r$ possible random seeds, so the output has at most that many support points among the $2^m$ uniform targets. The lower bound is sharp: an injective seed map into m-bit outputs attains it.

For nine bits, eight random bits entail at least $1/2$ total-variation error. This is an information-theoretic sampler-output bound, **not** an NP computation bound, and it does not constrain prover-assisted quantum introspection where the verifier does not itself emit the full output.

## What SAT can actually construct

For an **explicitly tabulated** two-prover game G, define one Boolean variable for each possible answer to each player's question, require exactly one per question, and prohibit every losing answer pair on every supported question pair. The resulting formula $F_G$ is satisfiable precisely when there is a **perfect deterministic classical local strategy**.

If SAT is in P, solve $F_G$ and self-reduce one variable at a time. At most $M+1$ satisfiability decisions recover the entire strategy for a formula with M variables. The reduction and reconstruction are polynomial in the **explicit game table length**.

This statement does **not** transfer to:
- a game with a perfect quantum strategy but no perfect classical strategy (such as the magic square);
- a succinctly indexed game whose explicit table takes exponentially many bits;
- a claim that classical SAT time must scale with entangled Schmidt rank.

The research problem is to construct a new **succinct** classical resource invariant with a corresponding uniform SAT-to-strategy-representation transfer, and then prove a genuine lower bound for that same invariant.

## Reproducible checks

The [WP01 source record](https://github.com/grandchallenge/MATHSOLVE/pull/1152) includes source-encoding and finite classical-SAT scripts. Tested results: 54 exact rational randomness cases, a SAT-compatible eight-variable toy game, magic-square local-strategy UNSAT, and a perfect deterministic strategy for the 512-pair nine-level identity input.

Neither script executes the quantum-introspection/PCP/repetition transformations of the published Figure 15 compressor. The source's machine transition encoding, effective universal parameters and full quantum compression implementation remain open.

## Claim status

**Maintained:** PNP-001 is an unsolved Millennium problem; GCL has not produced an unrestricted circuit lower bound or SAT separation, and has not submitted a new paper to arXiv. The current documentary and [versioned preprint record](preprint.md) are research communication, not proof certification.
