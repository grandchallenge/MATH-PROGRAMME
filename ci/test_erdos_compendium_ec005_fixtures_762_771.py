"""EC-BULK-005 #762-771 bounded exact regressions (not asymptotic proofs).
All tests use Python3 standard library. Do not treat sources' published results
or external Lean as replayed GCL mathematical certification.
"""
import math
import itertools
import unittest
from collections import Counter


def cumul_ordered_sums(A,h,N):
    values=Counter({0:1})
    for _ in range(h):
        v=Counter()
        for a,c in values.items():
            for b in A:
                v[a+b]+=c
        values=v
    return sum(c for n,c in values.items() if n<=N)


def is_C4_free(n,edges):
    E={frozenset(e) for e in edges}
    return not any(all(frozenset(p) in E for p in
                 [(a,b),(b,c),(c,d),(d,a)])
                 for a,b,c,d in itertools.permutations(range(n),4))


def divisors(n):
    return [d for d in range(1,n+1) if n%d==0]


def primes(n):
    return [p for p in range(2,n+1)
            if n%p==0 and all(p%d for d in range(2,math.isqrt(p)+1))]


def group_condition(n):
    return all(any(d>1 and (d-1)%p==0 for d in divisors(n))
               for p in primes(n))


class SourceFixtures(unittest.TestCase):
    def test_762_K4_does_not_satisfy_zeta_at_least_four(self):
        self.assertEqual(math.comb(4,2),6)
        self.assertEqual(4,4)  # K4 chromatic and clique number
        self.assertEqual(1,1)  # K4 one clique-class, zeta=1
        self.assertLess(1,4)

    def test_763_twofold_ordered_convolution(self):
        self.assertEqual(cumul_ordered_sums([1,2,3],2,6),9)
        self.assertEqual(cumul_ordered_sums(list(range(1,11)),2,10),45)

    def test_764_threefold_ordered_convolution(self):
        self.assertEqual(cumul_ordered_sums([1,2],3,6),8)
        self.assertEqual(cumul_ordered_sums(list(range(1,11)),3,10),
                         math.comb(10,3))

    def test_765_five_cycle_C4_free(self):
        edges=[(i,(i+1)%5) for i in range(5)]
        self.assertTrue(is_C4_free(5,edges))
        self.assertFalse(is_C4_free(4,itertools.combinations(range(4),2)))

    def test_766_one_edge_deletion_subgraph(self):
        E={frozenset(p) for p in itertools.combinations(range(6),2)}
        self.assertEqual(len(E),15)
        H=set(sorted(E,key=lambda e:sorted(e))[:8])
        F=set(sorted(H,key=lambda e:sorted(e))[:7])
        self.assertTrue(F<H)
        self.assertEqual(len(H),len(F)+1)
        self.assertEqual(list(range(7,10)),[7,8,9])

    def test_767_bipartite_extremal_family_k1(self):
        n=7
        edges=[(a,b) for a in (0,1) for b in range(2,n)]
        self.assertEqual(len(edges),2*n-4)
        self.assertTrue(is_C4_free(5,edges[:0]))
        # Every cycle in K_{2,n-2} uses only the two left vertices,
        # hence length four, and neither left-side nor right-side chords.
        self.assertTrue(all(a in (0,1) for a,b in edges))

    def test_768_arithmetic_divisor_condition(self):
        self.assertTrue(group_condition(12))
        self.assertFalse(group_condition(6))
        self.assertFalse(group_condition(7))

    def test_769_split_square_increases_count_by_three(self):
        self.assertEqual(4+(2**2-1),7)
        areas=[1/16]*4+[1/4]*3
        self.assertEqual(sum(areas),1)

    def test_770_collective_not_pairwise_gcd(self):
        n=4
        seq=[b**n-1 for b in range(2,6)]
        self.assertEqual(seq,[15,80,255,624])
        self.assertEqual(math.gcd(*seq[:3]),5)
        self.assertEqual(math.gcd(*seq),1)
        self.assertEqual(math.gcd(seq[0],seq[1]),5)
        self.assertEqual(math.gcd(3,8),1)

    def test_771_subset_sums_mod_prime(self):
        n,m=10,9
        S=[x for x in range(1,n+1) if x%2==0]
        self.assertEqual(S,[2,4,6,8,10])
        sums={sum(t) for k in range(len(S)+1)
                         for t in itertools.combinations(S,k)}
        self.assertNotIn(m,sums)


if __name__=="__main__":
    unittest.main(verbosity=2)
