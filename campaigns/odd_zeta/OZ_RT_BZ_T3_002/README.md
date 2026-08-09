# OZ-RT-BZ-T3-002

This package executes the first bounded certificate-generation phase authorized by issue #315. It does not repeat the fixed-letter/local-residue classes closed by `OZ-RT-BZ-T3-001`.

The retained exact target evaluator is reconstructed from the source-locked Brown-Zudilin kernel, rational-part formulas, nested harmonic sums and compact `w5_sym` representative. It reproduces the finite T3 zero sum for every sampled `n`; this finite replay has theorem effect `NONE`.

The executed search is the first-order fibre route. Let `V(n,k)` be the exact `l`-fibre sum and `G(n,k)=sum_{j<k} V(n,j)`. A first-order telescoper of the tested form would have `G=qV` with `q=N/D`, where `N,D in Q[n,k]`. For total degrees `d=0..9`, the producer constructs the homogeneous rational system `D*G-N*V=0` on exact finite sample grids.

To certify a negative rank result efficiently and exactly, every rational matrix is reduced modulo the fixed prime `p=1000003`; all entry denominators are required to be coprime to `p`. Full column rank modulo `p` exhibits a nonzero square minor modulo `p`, so the corresponding rational minor is nonzero. Thus full column rank modulo `p` certifies full column rank over `Q`; this is not a heuristic modular-to-rational lift and it is not used to assert a positive T3 identity. The independent verifier reconstructs the rational matrices and performs its own modular elimination.

Every tested system has certified full column rank. Degrees 0 through 6 are closed on 65 equations with `1<=n<=10`; degree 7 is rank 72/72 on 90 equations through `n=12`; degree 8 is rank 90/90 on 119 equations through `n=14`; degree 9 is rank 110/110 on 135 equations through `n=15`. Therefore no nonzero `(N,D)` exists in the entire bounded ansatz class with total degree at most 9. This is a genuine exact negative result for the declared certificate class, not evidence that T3 is false.

The next admissible work is mathematically broader: a direct two-dimensional delta certificate over `Q(n,k,l)`, a fibre telescoper carrying the finite rational shift module/harmonic basis, or a separately budgeted higher-degree first-order rational search.

The producer, independent verifier, and admission validator are separately registered in the governed campaign-replay registry. `target.py` is a passive shared exact-evaluation library and is not an autonomous replay authority.

Terminal candidate disposition: `OPEN_WITH_CHARACTERIZED_BLOCKER`. T3 remains neither proved nor refuted. T1-top, DEPTH, Sharp-12, primes 2/3, MATHCERT and external claims are unchanged.
