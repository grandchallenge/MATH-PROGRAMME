# BSD-WP00 — Source, normalization, status, and equivalence audit

## 1. Audit determination

The canonical challenge is the rank statement for every elliptic curve \(E/\mathbb Q\):

\[
\operatorname{rank}_{\mathbb Z}E(\mathbb Q)
=
\operatorname{ord}_{s=1}L(E,s).
\]

The source audit supports the following determinations.

1. The official Clay problem is still listed as unsolved as of `2026-07-24`.
2. Modularity supplies the analytic continuation and functional equation needed to define the analytic rank for every \(E/\mathbb Q\).
3. The rank statement is known when the analytic rank is \(0\) or \(1\).
4. In those low analytic-rank cases, Euler-system methods also give finiteness of \(\Sha(E/\mathbb Q)\).
5. The unrestricted converse direction from algebraic or Selmer data to complex analytic order is not known. Modern converse theorems impose material curve, prime, reduction, and residual-representation hypotheses.
6. The refined leading-term formula is stronger than rank equality. A proof of rank equality alone does not prove finiteness of \(\Sha\) or the numerical leading coefficient.
7. The \(p^\infty\)-Selmer corank is not generally equal to the Mordell–Weil rank without control of \(\Sha[p^\infty]\).
8. The phrase “\(p\)-adic BSD” denotes several normalization-dependent conjectures rather than one unqualified statement.
9. Family, density, average-rank, and finite-database theorems do not imply the universal individual-curve conjecture.
10. No numerical work is needed for WP00.

## 2. Canonical source corpus

### 2.1 Official and foundational sources

| ID | Source | Claim used | Audit state |
|---|---|---|---|
| `SRC-OFFICIAL-WILES` | Andrew Wiles, *The Birch and Swinnerton-Dyer Conjecture*, official Clay problem description | official rank statement; incomplete-to-completed normalization warning; low-rank theorem summary | `PRIMARY_AUDITED` |
| `SRC-CLAY-STATUS` | Clay Mathematics Institute, BSD Millennium Problem page | current unsolved status | `PRIMARY_AUDITED_2026-07-24` |
| `SRC-BSD-1965` | B. J. Birch and H. P. F. Swinnerton-Dyer, *Notes on elliptic curves II*, J. Reine Angew. Math. 218 (1965), 79–108 | historical conjecture and experimental origin | `PRIMARY_IDENTIFIED` |
| `SRC-MORDELL-1922` | L. J. Mordell, *On the rational solutions of the indeterminate equations of the third and fourth degrees* | finite generation over \(\mathbb Q\) | `PRIMARY_IDENTIFIED` |
| `SRC-BCDT-2001` | Breuil–Conrad–Diamond–Taylor, *On the modularity of elliptic curves over Q: wild 3-adic exercises*, JAMS 14 (2001), 843–939 | modularity of all elliptic curves over \(\mathbb Q\) | `PRIMARY_IDENTIFIED` |

### 2.2 Low-rank bridge and Euler-system sources

| ID | Source | Claim used | Audit state |
|---|---|---|---|
| `SRC-GZ-1986` | Gross–Zagier, *Heegner points and derivatives of L-series*, Invent. Math. 84 (1986), 225–320 | derivative-height bridge in analytic rank one | `PRIMARY_IDENTIFIED` |
| `SRC-KOLYVAGIN` | V. A. Kolyvagin, Euler-system papers on modular elliptic curves, including *Finiteness of E(Q) and Sha(E,Q) for a class of Weil curves* | rank \(0/1\) arithmetic consequences and finiteness of \(\Sha\) | `PRIMARY_IDENTIFIED; THEOREM_CONCORDANCE_DEFERRED_TO_WP02` |
| `SRC-COATES-WILES` | J. Coates and A. Wiles, *On the conjecture of Birch and Swinnerton-Dyer*, Invent. Math. 39 (1977), 223–251 | early CM rank-zero result | `PRIMARY_IDENTIFIED` |
| `SRC-RUBIN` | K. Rubin, CM Euler-system/Iwasawa results | refined CM low-rank consequences | `PRIMARY_IDENTIFIED; EXACT_INTERFACE_DEFERRED_TO_WP02` |
| `SRC-KATO` | K. Kato, *p-adic Hodge theory and values of zeta functions of modular forms*, Astérisque 295 (2004) | Euler-system and divisibility interfaces for rank-zero and \(p\)-parts | `PRIMARY_IDENTIFIED; EXACT_INTERFACE_DEFERRED_TO_WP02` |

### 2.3 Parity, converse, and leading-term sources

| ID | Source | Claim used | Audit state |
|---|---|---|---|
| `SRC-DD-2010` | T. Dokchitser and V. Dokchitser, *On the Birch–Swinnerton-Dyer quotients modulo squares*, Ann. of Math. 172 (2010), 567–596 | \(p\)-parity for all elliptic curves over \(\mathbb Q\) and all primes \(p\) | `PRIMARY_ABSTRACT_AUDITED` |
| `SRC-SKINNER-2020` | C. Skinner, *A converse to a theorem of Gross, Zagier, and Kolyvagin*, Ann. of Math. 191 (2020), 329–354 | rank-one converse for specified semistable curves | `PRIMARY_ABSTRACT_AUDITED` |
| `SRC-BT-2026` | A. Burungale and Y. Tian, *A rank zero p-converse to a theorem of Gross–Zagier, Kolyvagin and Rubin*, Ann. of Math. 203 (2026), 1–13 | CM rank-zero \(p\)-converse | `PRIMARY_ABSTRACT_AUDITED` |
| `SRC-JSW-2017` | D. Jetchev, C. Skinner, X. Wan, *The Birch and Swinnerton-Dyer formula for elliptic curves of analytic rank one*, Camb. J. Math. 5 (2017), 369–434 | specified odd-\(p\) parts of the rank-one formula | `PRIMARY_STATEMENT_AUDITED` |
| `SRC-BF-2022` | A. Burungale and M. Flach, *The conjecture of Birch and Swinnerton-Dyer for certain elliptic curves with complex multiplication* | complete CM strong-BSD results under explicit hypotheses | `PRIMARY_ABSTRACT_AUDITED` |

### 2.4 Family and computational boundary sources

| ID | Source | Claim used | Audit state |
|---|---|---|---|
| `SRC-BS-2015` | M. Bhargava and A. Shankar, *Ternary cubic forms having bounded invariants...*, Ann. of Math. 181 (2015), 587–621 | positive-proportion and average-Selmer/rank terrain | `PRIMARY_ABSTRACT_AUDITED` |
| `SRC-MILLER-2011` | R. L. Miller, *Proving the BSD conjecture for specific elliptic curves of analytic rank zero and one*, LMS J. Comput. Math. 14 (2011), 327–350 | rigorous finite individual-curve verification | `PRIMARY_ABSTRACT_AUDITED` |
| `SRC-BH-2026` | B. Banwait and X. Huang, arXiv:2601.16044 | algorithmic identification of twist families satisfying strong BSD, conditional on imported theorem criteria | `PREPRINT_AUDITED_AT_ABSTRACT; NOT_CANONICAL_FOR_UNIVERSAL_STATUS` |

## 3. Canonical complex \(L\)-function normalization

Let \(N_E\) be the conductor of \(E\). For each prime \(\ell\), write

\[
P_\ell(T)=
\begin{cases}
1-a_\ell T+\ell T^2, & \text{good reduction},\\
1-T, & \text{split multiplicative reduction},\\
1+T, & \text{nonsplit multiplicative reduction},\\
1, & \text{additive reduction}.
\end{cases}
\]

For good reduction,

\[
a_\ell=\ell+1-\#E(\mathbb F_\ell).
\]

The complete finite \(L\)-function is

\[
L(E,s)=\prod_\ell P_\ell(\ell^{-s})^{-1}.
\]

The completed function used in this campaign is

\[
\Lambda(E,s)
=
N_E^{s/2}(2\pi)^{-s}\Gamma(s)L(E,s),
\]

with functional equation

\[
\Lambda(E,s)=w_E\Lambda(E,2-s),
\qquad w_E\in\{\pm1\}.
\]

The central point is \(s=1\), and

\[
r_{\mathrm{an}}=\operatorname{ord}_{s=1}L(E,s)
=\operatorname{ord}_{s=1}\Lambda(E,s).
\]

The root number determines only parity:

\[
(-1)^{r_{\mathrm{an}}}=w_E.
\]

It does not determine the exact order of vanishing.

### 3.1 Concordance with the official Wiles statement

Wiles first writes an incomplete Euler product omitting primes dividing \(2\Delta\), and later restores the missing factors in a completed finite series denoted \(L^*(E,s)\). This campaign instead uses the standard complete finite Euler product from the outset.

Therefore:

- Wiles's initial \(L(C,s)\) is not symbol-for-symbol identical to this campaign's \(L(E,s)\);
- the order at \(s=1\) is unchanged after multiplying by nonzero omitted local factors;
- the leading coefficient changes by those local factors;
- no leading-term formula may combine Wiles's incomplete coefficient with this campaign's Tamagawa normalization without an explicit conversion.

## 4. Arithmetic normalization

Fix a global minimal Néron model and a minimal Néron differential \(\omega_E\).

- **Real period**
  \[
  \Omega_E=\int_{E(\mathbb R)}|\omega_E|.
  \]

- **Tamagawa number**
  \[
  c_\ell=[E(\mathbb Q_\ell):E^0(\mathbb Q_\ell)].
  \]

- **Regulator**  
  If \(P_1,\dots,P_r\) is a basis of \(E(\mathbb Q)/E(\mathbb Q)_{\mathrm{tors}}\),
  \[
  \operatorname{Reg}_E=\det(\langle P_i,P_j\rangle_{\mathrm{NT}}).
  \]
  For rank \(0\), the empty determinant is \(1\).

- **Tate–Shafarevich group**
  \[
  \Sha(E/\mathbb Q)
  =
  \ker\!\left(
  H^1(\mathbb Q,E)\longrightarrow\prod_v H^1(\mathbb Q_v,E)
  \right).
  \]

- **Strong formula**
  \[
  \frac{L^{(r)}(E,1)}{r!}
  =
  \frac{
  \Omega_E\operatorname{Reg}_E\#\Sha(E/\mathbb Q)\prod_\ell c_\ell
  }{
  \#E(\mathbb Q)_{\mathrm{tors}}^2
  }.
  \]

This formula presupposes \(r=r_{\mathrm{alg}}=r_{\mathrm{an}}\) and finiteness of \(\Sha\).

Conventions using \(\Omega_E^+\), a separate archimedean Tamagawa factor \(c_\infty\), an optimal curve in an isogeny class, a non-minimal differential, or a completed \(\Lambda\)-value require conversion factors. They are not interchangeable by typography alone.

## 5. Selmer correspondence audit

For every prime \(p\), the Kummer sequence gives

\[
0\longrightarrow
E(\mathbb Q)\otimes\mathbb Q_p/\mathbb Z_p
\longrightarrow
\operatorname{Sel}_{p^\infty}(E/\mathbb Q)
\longrightarrow
\Sha(E/\mathbb Q)[p^\infty]
\longrightarrow 0.
\]

Taking \(\mathbb Z_p\)-coranks yields

\[
\operatorname{corank}_{\mathbb Z_p}\operatorname{Sel}_{p^\infty}(E/\mathbb Q)
=
r_{\mathrm{alg}}
+
\operatorname{corank}_{\mathbb Z_p}\Sha(E/\mathbb Q)[p^\infty].
\]

Consequences:

1. Finite \(\Sha[p^\infty]\) implies Selmer corank \(=r_{\mathrm{alg}}\).
2. Selmer corank \(r\) alone does not prove Mordell–Weil rank \(r\).
3. A \(p\)-converse from Selmer corank to analytic order does not, by itself, prove the full complex BSD statement.
4. Control at one prime does not prove finiteness of the whole \(\Sha\) or the complete leading coefficient.

## 6. Statement lattice

### 6.1 Universal statements

- `BSD-RANK-Q`: \(r_{\mathrm{alg}}=r_{\mathrm{an}}\).
- `BSD-SHA-Q`: \(\Sha(E/\mathbb Q)\) is finite.
- `BSD-LEAD-Q`: the normalized leading-term identity holds.

No pair of these is silently identified with the third. In particular:

- rank equality does not imply finiteness of \(\Sha\);
- rank equality plus finiteness of \(\Sha\) does not determine the leading coefficient;
- the leading-term formula is recorded as including rank equality and finiteness, not as a free-standing numerical identity with undefined terms.

### 6.2 Low analytic rank

The official Wiles account records that, after modularity, the rank conjecture holds when

\[
r_{\mathrm{an}}\in\{0,1\}.
\]

The Gross–Zagier/Kolyvagin machinery also yields finiteness of \(\Sha\) in these cases. This does not settle arbitrary \(r_{\mathrm{an}}\ge2\).

### 6.3 Converse terrain

The reverse direction is not available without hypotheses.

- Skinner's 2020 theorem gives a rank-one converse for semistable curves satisfying specified multiplicative-reduction conditions, assuming rank \(1\) and finite \(\Sha\).
- Burungale–Tian's 2026 theorem gives a rank-zero \(p\)-converse for CM elliptic curves over \(\mathbb Q\).
- These are theorem-grade advances, not a universal algebraic-rank-to-analytic-rank bridge.

### 6.4 Parity terrain

Dokchitser–Dokchitser prove for every elliptic curve over \(\mathbb Q\) and every prime \(p\) that

\[
(-1)^{\operatorname{corank}_{\mathbb Z_p}\operatorname{Sel}_{p^\infty}}
=
w_E
=
(-1)^{r_{\mathrm{an}}}.
\]

To replace the Selmer corank by \(r_{\mathrm{alg}}\), one needs control of the divisible \(p\)-primary part of \(\Sha\), for example finiteness of \(\Sha[p^\infty]\).

### 6.5 Leading-term terrain

The literature contains many theorem families of the form:

- one \(p\)-part of the complex BSD formula;
- ordinary, multiplicative, or supersingular cases;
- CM or non-CM cases;
- rank \(0\) or rank \(1\);
- twist families;
- formulas modulo squares or modulo powers of \(p\).

Each result must retain its exact theorem hypotheses. The phrase “BSD is known” is prohibited unless the package specifies which rank, finiteness, primes, and normalization have been discharged.

## 7. \(p\)-adic normalization warning

There is no single unqualified \(p\)-adic BSD object.

At minimum, WP02 must separate:

1. good ordinary \(p\), with a Mazur–Swinnerton-Dyer \(p\)-adic \(L\)-function;
2. split multiplicative \(p\), where an exceptional zero and an \(\mathcal L\)-invariant alter the order and leading term;
3. supersingular \(p\), where signed or plus/minus \(p\)-adic \(L\)-functions and signed Selmer groups enter;
4. cyclotomic versus anticyclotomic variables;
5. primitive versus imprimitive Euler factors.

No arrow from a \(p\)-adic order of vanishing to the complex order is admitted without a named comparison or converse theorem.

## 8. Known theorem frontier

### 8.1 Supported theorem statements

- All elliptic curves over \(\mathbb Q\) are modular.
- Their \(L\)-functions have analytic continuation and the central functional equation.
- Analytic rank \(0\) or \(1\) gives the matching Mordell–Weil rank and finite \(\Sha\).
- \(p\)-Selmer parity agrees with analytic parity for all \(E/\mathbb Q\) and all primes \(p\).
- Rank-zero and rank-one converses are known in important restricted settings.
- Many \(p\)-parts and complete formulas are known for restricted curve classes and families.
- Rigorous computation can prove strong BSD for specified finite collections of low-rank curves.

### 8.2 Unsupported universal upgrades

The audit found no support for:

- a theorem for all curves of analytic rank at least \(2\);
- a universal proof of finiteness of \(\Sha\);
- a universal algebraic-rank or Selmer-corank converse;
- a universal strong leading-term formula;
- promotion of family density to an individual theorem;
- promotion of numerical agreement to a universal proof.

## 9. Proof-obligation DAG

The universal rank problem factors through two non-equivalent interfaces:

```text
complex analytic order
        |
        |  missing universal analytic-to-arithmetic bridge above rank 1
        v
p-primary Selmer coranks for suitable p
        |
        |  exact Kummer sequence
        v
Mordell-Weil rank + divisible p-primary Sha contribution
```

The strong formula adds a determinant-and-local-factor layer:

```text
leading Taylor coefficient
        |
        |  missing universal leading-term comparison
        v
real period × regulator × Tamagawa product × torsion correction × #Sha
```

The two principal universal obstructions are therefore:

1. controlling sufficiently many independent global arithmetic classes in higher rank;
2. proving both finiteness and exact size of the hidden local-to-global defect group.

This is an obstruction map, not a proposed proof mechanism.

## 10. Claim boundary

WP00 proves no new arithmetic theorem. It performs:

- primary-source and current-status audit;
- notation and normalization reconciliation;
- exact logical decomposition;
- identification of theorem interfaces and missing bridges;
- separation of universal, restricted, family, and computational claims.

The package does not claim that the conjecture is solved, nearly solved, reduced to a finite computation, or equivalent to any one \(p\)-adic main conjecture without additional hypotheses.

## 11. Promotion assessment

The mathematical source-and-equivalence objectives of WP00 passed repository policy checks and independent Referee reconstruction. The remaining work belongs to later packages:

- WP01: false-proof fixtures;
- WP02: exact theorem-by-theorem hypothesis ledger;
- MATHCERT: formal logical and normalization substrate.

WP00 is promoted. Repository policy workflow `30083374165` passed, Amanuensis integration is complete, and the Referee found no blocking semantic overclaim. The exact theorem concordance and formalization items remain recorded as nonblocking debt.
