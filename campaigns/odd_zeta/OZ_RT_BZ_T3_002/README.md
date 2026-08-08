# OZ-RT-BZ-T3-002

This package executes the first bounded certificate-generation phase authorized by issue #315. It does not repeat the fixed-letter/local-residue classes closed by `OZ-RT-BZ-T3-001`.

The retained exact target evaluator is reconstructed from the source-locked Brown-Zudilin kernel, rational-part formulas, nested harmonic sums and compact `w5_sym` representative. It reproduces the finite T3 zero sum for `1 <= n <= 10`; this finite replay has theorem effect `NONE`.

The executed search is the first-order fibre route. Let `V(n,k)` be the exact `l`-fibre sum and `G(n,k)=sum_{j<k} V(n,j)`. A first-order telescoper of the tested form would have `G=qV` with `q=N/D`, where `N,D in Q[n,k]`. For each total degree `d=0..6`, the producer constructs the homogeneous system `D*G-N*V=0` on all 65 exact cells with `1<=n<=10`, `0<=k<=n`. The independent verifier reconstructs the matrices and computes their ranks with a separately implemented exact elimination routine.

Every tested system has full column rank. At the strongest frontier, degree 6 gives 65 equations, 56 unknown coefficients and rank 56. Therefore no nonzero `(N,D)` exists in this bounded ansatz class. This is a genuine negative result for the declared certificate class, not evidence that T3 is false.

The next admissible work is mathematically broader: a direct two-dimensional delta certificate over `Q(n,k,l)`, a fibre telescoper carrying the finite rational shift module/harmonic basis, or a separately budgeted higher-degree first-order rational search.

Terminal candidate disposition: `OPEN_WITH_CHARACTERIZED_BLOCKER`. T3 remains neither proved nor refuted. T1-top, DEPTH, Sharp-12, primes 2/3, MATHCERT and external claims are unchanged.
