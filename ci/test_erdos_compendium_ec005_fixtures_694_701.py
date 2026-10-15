"""EC-BULK-005 source-bound exact finite checks for Erdős #694-701.

No test certifies asymptotic theorems, historical proof text, Lean kernels,
or editorial admission. This suite uses Python 3 standard library only.
"""
import itertools
import math
import unittest
from fractions import Fraction


def prime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))


def totient(n):
    return sum(math.gcd(n,k)==1 for k in range(1,n+1))


def proper_divisors(n):
    return [d for d in range(1,n+1) if n%d==0]


def f_gcd_binomial(n):
    return min(math.gcd(n,math.comb(n,k)) for k in range(2,n//2+1))


class EC005Fixtures(unittest.TestCase):
    def test_694_totient_fiber_four(self):
        self.assertEqual([m for m in range(1,200) if totient(m)==4],
                         [5,8,10,12])
        self.assertEqual(Fraction(12,5),Fraction(max(m for m in range(1,200)
            if totient(m)==4),min(m for m in range(1,200)
            if totient(m)==4)))

    def test_695_prime_chain(self):
        chain=[2,3,7,29,59]
        self.assertTrue(all(prime(p) for p in chain))
        self.assertTrue(all(p<q and q%p==1
                            for p,q in itertools.pairwise(chain)))

    def test_696_prime_divisor_chain(self):
        n=1218
        pchain=[2,3,7,29]
        dchain=[1,2,3,7,29]
        self.assertEqual(math.prod(pchain),n)
        self.assertTrue(all(n%p==0 and prime(p) for p in pchain))
        self.assertTrue(all(q%p==1 for p,q in itertools.pairwise(pchain)))
        self.assertTrue(all(n%d==0 for d in dchain))
        self.assertTrue(all(q%d==1%d for d,q in itertools.pairwise(dchain)))

    def test_697_small_modulus_density(self):
        divisors=[3,5,7]
        self.assertTrue(all(d%2==1 for d in divisors))
        period=math.lcm(*divisors)
        covered=sum(any(t%d==0 for d in divisors)
                    for t in range(1,period+1))
        self.assertEqual(Fraction(covered,period),Fraction(19,35))

    def test_698_binomial_common_divisor(self):
        self.assertEqual(math.gcd(math.comb(10,2),math.comb(10,3)),15)
        self.assertEqual(math.gcd(math.comb(12,2),math.comb(12,4)),33)

    def test_699_strict_vs_nonstrict_prime_factor(self):
        g=math.gcd(math.comb(28,5),math.comb(28,14))
        self.assertEqual(g,1080)
        self.assertEqual(g%(2**3*3**3*5),0)
        self.assertEqual(max(p for p in range(2,g+1)
                            if prime(p) and g%p==0),5)
        # Bounded search only, not a proof of the open weak statement.
        for n in range(4,31):
            for i in range(1,n//2):
                for j in range(i+1,n//2+1):
                    g=math.gcd(math.comb(n,i),math.comb(n,j))
                    self.assertTrue(any(prime(p) and g%p==0
                                        for p in range(i,n+1)))

    def test_700_gcd_binomial_three_examples(self):
        self.assertEqual(f_gcd_binomial(12),3)
        self.assertEqual(f_gcd_binomial(25),5)
        self.assertEqual(f_gcd_binomial(30),6)
        self.assertEqual(f_gcd_binomial(25)**2,25)
        self.assertEqual(f_gcd_binomial(30),30//5)

    def test_701_full_powerset_star_bound(self):
        X={1,2,3}
        ps=[frozenset(c)
            for j in range(4) for c in itertools.combinations(X,j)]
        self.assertEqual(len(ps),8)
        self.assertEqual(sum(1 in a for a in ps),4)
        for r in range(5,9):
            for fam in itertools.combinations(ps,r):
                self.assertFalse(all(a & b for a,b in itertools.combinations(fam,2)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
