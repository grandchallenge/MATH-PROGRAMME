# Erdős 27 — smooth-modulus decomposition, FFKPY Lemma 3.1

Assignment ERDOS-PV-0027-B, native claim 169ab6afa0108f9cfff2acac2d3576fafafc1862 (actor fyremael; protected source 927a81114d9dc20492c94a02d78297236cd4c0ca; manifest blob 3b886a28de3c07724510b692fd75eeeb6969d321; claim capture 00c678b6f4054235b9836467a685048b).

## Exact source and scope

FFKPY, *Sieving by large integers and covering systems of congruences*, 21 Dec 2006 manuscript, DOI 10.1090/S0894-0347-06-00549-2, printed manuscript p.10 (PDF index 9), Lemma 3.1. The Phase A byte-identified source acquisition (SHA256 aabca6f856644c89826e9f9c8c46f03a92c9f3e46c41ee443b4d6670463014e9; capture 60272c9e447249f9bd7b60dcb85ed9fc) is reused; the lemma page at the same URL https://ford126.web.illinois.edu/wwwpapers/coverings.pdf was separately visually read, not independently rehashed. Source defines finite sets of ordered pairs of positive integers (n,r); our proof allows integer representatives r, and duplicate congruences do not affect avoidance. Q is real >=2. The empty family is handled by lcm(empty)=1 and density 1, an explicit harmless extension.

## Reconstruction

Let C be a finite residue system. For each (n,r), factor n=a_n b_n where a_n is the product of all prime powers in n with prime <=Q; b_n is the complementary factor. Let M=lcm(a_n) and B=lcm(b_n) over C. Prime valuations immediately give gcd(M,B)=1, gcd(n,M)=a_n, and lcm(n)=MB. None of these uses distinctness of n or pairwise coprimality between different rough factors.

For each h in {0,...,M-1}, define C_h as the set of (b_n,r) from those (n,r) with r=h mod a_n. Then for an integer x with x=h mod M, n divides x-r iff both a_n and b_n divide x-r (since gcd(a_n,b_n)=1). The smooth condition is determined entirely by h. Thus avoidance of the original family within this fibre is exactly avoidance of C_h in the rough coordinate x mod B.

Write U_h for the set of residues y in Z/BZ avoiding all classes in C_h. The CRT map x mod MB -> (x mod M,x mod B) is a bijection. Restricting to first coordinate h gives a bijection between original uncovered residues in that fibre and U_h. The natural density of a periodic set with period d>0 is its residue count divided by d: partition [1,X] into complete periods and one remainder bounded by d, then let X tend to infinity. Since each b_n divides B, density(C_h)=|U_h|/B even when its minimal period is a proper divisor. Consequently

delta(C) = (sum_h |U_h|)/(MB) = (1/M) sum_h delta(C_h).

This is exactly the source identity, strengthened to a finite counting bijection without additional analytic input. A fibre with a modulus-one restriction has zero uncovered residues, and an empty fibre has density one. For arbitrary real Q, only primes <=Q enter; floor(Q) gives the same partition.

## Dependencies and next obligation

Dependencies: prime factorization, prime valuations of LCM, elementary divisibility under coprimality, finite CRT, periodic density. No sieve estimate, independence assumption between rough moduli, asymptotic prime theorem or probabilistic approximation. This completes the specified bounded reproduction of Lemma 3.1, not Lemmas 3.2–3.4 or full Theorem B. The exact finite CRT identity and Lemma 2.1 recurrence/weighted refinement are candidates for formalization in the pinned Lean lane; no kernel replay or new mathematical certification is asserted. The next analytic obligation is the uniform bound in Lemma 3.2 (including the rough-integer sieve, reciprocal prime tail and divisor sum). Source credit remains with FFKPY.
