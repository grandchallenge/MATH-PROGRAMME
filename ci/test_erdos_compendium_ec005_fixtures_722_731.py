"""Exact bounded EC-BULK-005 Erdős #722-731 source fixtures.
Not proofs of infinite/asymptotic theorems, historical papers, or Lean certification.
"""
import itertools
import math
import unittest
from fractions import Fraction


def primes_upto(n):
    return [p for p in range(2,n+1)
            if all(p%d for d in range(2,math.isqrt(p)+1))]


def vfact(n,p):
    out=0
    while n:
        n//=p
        out+=n
    return out


def prime_support_central(n):
    return {p for p in primes_upto(2*n)
            if vfact(2*n,p)-2*vfact(n,p)>0}


def first_nondivisor(n):
    b=math.comb(2*n,n)
    return next(m for m in range(1,b+2) if b%m)


class EC005Fixtures(unittest.TestCase):
    def test_722_fano_steiner_seven_lines(self):
        lines=[frozenset({j%7,(j+1)%7,(j+3)%7}) for j in range(7)]
        self.assertEqual(len(set(lines)),7)
        for pair in itertools.combinations(range(7),2):
            self.assertEqual(sum(set(pair)<=x for x in lines),1)
        self.assertEqual(math.comb(7,2)//math.comb(3,2),7)

    def test_723_order_two_projective_plane_and_order_six(self):
        lines=[{j%7,(j+1)%7,(j+3)%7} for j in range(7)]
        self.assertEqual(len(lines),7)
        self.assertEqual(sum(len(L) for L in lines),21)
        self.assertFalse(any(a*a+b*b==6
                             for a in range(3) for b in range(3)))

    def test_724_two_orthogonal_latin_squares_order_three(self):
        N=3
        A=[[(i+j)%N for j in range(N)] for i in range(N)]
        B=[[(i+2*j)%N for j in range(N)] for i in range(N)]
        for L in [A,B]:
            self.assertTrue(all(set(row)==set(range(N)) for row in L))
            self.assertTrue(all({L[i][j] for i in range(N)}==set(range(N))
                                for j in range(N)))
        self.assertEqual(len({(A[i][j],B[i][j])
                              for i in range(N) for j in range(N)}),N*N)

    def test_725_exact_two_row_latin_rectangle_count(self):
        import itertools
        for n,expected in [(2,2),(3,12),(4,216)]:
            p=list(itertools.permutations(range(n)))
            cnt=sum(all(a[j]!=b[j] for j in range(n))
                    for a in p for b in p)
            self.assertEqual(cnt,expected)

    def test_726_strict_remainders_and_p_two_exception(self):
        for n in [10,11,15]:
            ps=primes_upto(n)
            direct=sum((Fraction(1,p) for p in ps
                        if 2*(n%p)>p),Fraction(0))
            odd_floor=sum((Fraction((2*n)//p-2*(n//p),p)
                           for p in ps if p!=2),Fraction(0))
            self.assertEqual(direct,odd_floor)
            raw=sum((Fraction((2*n)//p-2*(n//p),p)
                     for p in ps),Fraction(0))
            self.assertEqual(raw-direct,Fraction(n%2,2))
        self.assertEqual(sum((Fraction(1,p) for p in primes_upto(11)
                             if 2*(11%p)>p),Fraction(0)),Fraction(10,21))

    def test_727_legendre_factorial_obstruction(self):
        self.assertFalse(math.factorial(2*3)%
                         (math.factorial(3+2)**2)==0)
        n,k=3,2
        self.assertTrue(any(vfact(2*n,p)-2*vfact(n+k,p)<0
                            for p in primes_upto(2*n)))

    def test_728_literal_trivial_factorial_witness(self):
        n=100
        a=b=n
        C=5
        self.assertEqual(math.factorial(a)*math.factorial(b),
                         math.factorial(n)*math.factorial(a+b-n))
        self.assertGreater(a+b,n+C*math.log(n))

    def test_729_reduced_rational_denominator(self):
        q=Fraction(math.factorial(6),math.factorial(4)**2)
        self.assertEqual(q,Fraction(5,4))
        self.assertEqual(q.denominator,4)

    def test_730_two_prime_support_coincidences(self):
        self.assertEqual(prime_support_central(87),prime_support_central(88))
        self.assertEqual(prime_support_central(607),prime_support_central(608))
        self.assertNotEqual(math.comb(174,87),math.comb(176,88))

    def test_731_first_central_binomial_nondivisors(self):
        self.assertEqual([first_nondivisor(n) for n in range(1,5)],
                         [3,4,3,3])
        self.assertEqual(math.comb(4,2),6)
        self.assertEqual(6%4,2)


if __name__=="__main__":
    unittest.main(verbosity=2)
