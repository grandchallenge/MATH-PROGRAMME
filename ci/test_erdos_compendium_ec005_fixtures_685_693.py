"""Bounded elementary fixtures for EC-BULK-005 Erdős #685-693.

These tests verify small examples and source semantics only. They cannot
prove or certify the asymptotic conjectures, published sieve theorems, or
formal proof status. The test suite uses Python standard library only.
"""
import itertools
import math
import unittest
from fractions import Fraction


def primes_upto(n):
    return [p for p in range(2, n+1)
            if all(p % d for d in range(2, math.isqrt(p)+1))]


def factors(n):
    out = {}
    for p in primes_upto(math.isqrt(n)):
        while n % p == 0:
            out[p] = out.get(p,0)+1
            n //= p
    if n>1: out[n] = out.get(n,0)+1
    return out


def lcm_ratio(n,k,m):
    return math.prod(m+i for i in range(1,k+1)), math.prod(n+i for i in range(1,k+1))


def best_min_cover(n, minimum_required=1):
    ps=primes_upto(n)
    best=-1
    for residues in itertools.product(*(range(p) for p in ps)):
        least=min(sum((m-r)%p==0 for p,r in zip(ps,residues))
                  for m in range(1,n+1))
        best=max(best,least)
        if best>=minimum_required:
            return best
    return best


def kth_density(primes,k):
    p=primes[-1]
    coeff=[Fraction(1)]
    for q in primes[:-1]:
        nxt=[Fraction(0)]*(len(coeff)+1)
        for j, c in enumerate(coeff):
            nxt[j]+=c*(1-Fraction(1,q))
            nxt[j+1]+=c*Fraction(1,q)
        coeff=nxt
    return coeff[k-1]/p if k<=len(coeff) else Fraction(0)


def delta_one(n,m):
    divisors=list(range(n+1,m))
    period=math.lcm(*divisors) if divisors else 1
    selected=sum(sum(x%d==0 for d in divisors)==1
                 for x in range(1,period+1))
    return Fraction(selected,period)


def divisor_rich_points(n,k):
    return [x for x in range(n,n**k+1)
            if any(x%d==0 for d in range(n+1,2*n))]


class EC005Fixtures(unittest.TestCase):
    def test_685_binomial_distinct_prime_divisors(self):
        self.assertEqual(math.comb(20,5),15504)
        self.assertEqual(factors(math.comb(20,5)),{2:4,3:1,17:1,19:1})
        self.assertEqual(len(factors(math.comb(20,5))),4)
        self.assertEqual(len(factors(math.comb(30,7))),5)

    def test_686_product_ratio_nine(self):
        numer,denom=lcm_ratio(11,3,25)
        self.assertEqual((numer,denom),(19656,2184))
        self.assertEqual(numer,9*denom)
        for y in range(1,500):
            target=4*y*(y+1)
            x=math.isqrt(target)
            self.assertNotEqual(x*(x+1),target)

    def test_687_one_residue_per_prime(self):
        self.assertGreaterEqual(best_min_cover(3,1),1)
        self.assertEqual(best_min_cover(3,2),1)
        residues=list(itertools.product(range(2),range(3)))
        self.assertFalse(any(all(m%2==a or m%3==b
                                 for m in range(1,5)) for a,b in residues))

    def test_688_large_moduli_cannot_cover_ten(self):
        ps=[3,5,7]
        self.assertEqual(sum(math.ceil(10/p) for p in ps),8)
        for residues in itertools.product(*(range(p) for p in ps)):
            self.assertFalse(all(any(m%p==r for p,r in zip(ps,residues))
                                 for m in range(1,11)))

    def test_689_two_cover_finite_failure(self):
        self.assertEqual(best_min_cover(5,2),1)
        self.assertEqual(best_min_cover(10,1),0)

    def test_690_prime_density_from_crt(self):
        self.assertEqual(kth_density([2],1),Fraction(1,2))
        self.assertEqual(kth_density([2,3],1),Fraction(1,6))
        self.assertEqual(kth_density([2,3,5],1),Fraction(1,15))
        self.assertEqual(kth_density([2,3],2),Fraction(1,6))
        self.assertEqual(kth_density([2,3,5],2),Fraction(1,10))

    def test_691_reciprocal_divergence_not_sufficient(self):
        ps=primes_upto(100)
        for n in range(1,101):
            covered=any(2*p<=n and n%(2*p)==0 for p in ps)
            self.assertEqual(covered, n>=4 and n%2==0)

    def test_692_exact_density_dip(self):
        self.assertEqual(delta_one(3,6),Fraction(7,20))
        self.assertEqual(delta_one(3,7),Fraction(1,3))
        self.assertEqual(delta_one(3,8),Fraction(38,105))
        self.assertGreater(delta_one(3,6),delta_one(3,7))
        self.assertLess(delta_one(3,7),delta_one(3,8))

    def test_693_divisor_rich_internal_gaps(self):
        for n,k,expected,count in [(10,2,4,51),(12,2,6,75)]:
            pts=divisor_rich_points(n,k)
            self.assertEqual(len(pts),count)
            self.assertEqual(max(b-a for a,b in itertools.pairwise(pts)),
                             expected)
            self.assertEqual(pts[0],n+1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
