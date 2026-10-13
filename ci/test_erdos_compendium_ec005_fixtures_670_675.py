"""Finite arithmetic fixtures for EC-BULK-005 Erdős #670-675.

Exact checks only: not source-proof replay, asymptotic certification, CI
deployment, independent critical review, or V2 admission.
"""
import math
import itertools
import unittest
from fractions import Fraction


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def squarefree(n):
    return all(n % (p*p) != 0 for p in range(2, math.isqrt(n) + 1))


def sum_of_two_squares(n):
    return any(a*a + b*b == n for a in range(math.isqrt(n) + 1)
               for b in range(math.isqrt(n) + 1))


def first_translation(n, pred, limit=200):
    pattern = tuple(pred(a) for a in range(1, n + 1))
    for t in range(1, limit + 1):
        if all(pred(a+t) == pattern[a-1] for a in range(1, n+1)):
            return t
    return None


def prime_factorization(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


class EC005Fixtures(unittest.TestCase):
    def test_670_separated_diameter_golomb_ruler(self):
        pts = [0, 1, 4, 6]
        d = sorted(y-x for x, y in itertools.combinations(pts, 2))
        self.assertEqual(d, [1, 2, 3, 4, 5, 6])
        self.assertEqual(max(pts)-min(pts), 6)

    def test_671_interpolation_lebesgue_at_half(self):
        x = Fraction(1, 2)
        values = [x*(x-1)/2, 1-x*x, x*(x+1)/2]
        self.assertEqual(values, [Fraction(-1,8),
                                  Fraction(3,4), Fraction(3,8)])
        self.assertEqual(sum(values), 1)
        self.assertEqual(sum(map(abs, values)), Fraction(5,4))
        self.assertEqual(values[0]*1 + values[1]*0 + values[2]*1,
                         Fraction(1,4))

    def test_672_positive_three_term_square_and_signed_four(self):
        self.assertEqual(math.gcd(1, 24), 1)
        self.assertEqual(1*25*49, 35**2)
        self.assertEqual(math.gcd(18, 7), 1)
        self.assertEqual(18*25*32, 120**2)
        self.assertEqual((-6)*(-1)*4*9, 6**3)

    def test_673_divisor_successor_ratio_correction(self):
        ds = divisors(12)
        self.assertEqual(ds, [1,2,3,4,6,12])
        val = sum((Fraction(a,b) for a, b in zip(ds, ds[1:])),
                  Fraction(0))
        self.assertEqual(val, Fraction(37, 12))
        self.assertGreaterEqual(val, Fraction(len(divisors(6)), 2))
        self.assertEqual(sum(Fraction(a,b)
                             for a,b in zip(divisors(5),divisors(5)[1:])),
                         Fraction(1,5))
        self.assertNotEqual(Fraction(1,5), len(divisors(5)))

    def test_674_ko_family_prime_valuation_identity(self):
        for r in range(2, 6):
            u, v = 2**r, 2**r-1
            T = 2**(2*u*(v-r)) * v**(2*v)
            x, y, z = T*u*u, T*v*v, 2*T*u*v
            self.assertEqual(z*z, 4*x*y)
            primes = prime_factorization(v)
            base_two = 2*u*(v-r)
            vx = {2: base_two + 2*r}
            vy = {2: base_two}
            vz = {2: base_two + r+1}
            for p, e in primes.items():
                vx[p] = 2*v*e
                vy[p] = (2*v+2)*e
                vz[p] = (2*v+1)*e
            for p in set(vx)|set(vy)|set(vz):
                self.assertEqual(vx.get(p,0)*x + vy.get(p,0)*y,
                                 vz.get(p,0)*z)
        self.assertEqual((2**12)*(3**6), 2985984)
        self.assertEqual((2**8)*(3**8), 1679616)
        self.assertEqual((2**11)*(3**7), 4478976)

    def test_675_squarefree_minimal_shifts(self):
        self.assertEqual(first_translation(5, squarefree), 12)
        self.assertEqual(first_translation(8, squarefree), 28)

    def test_675_two_square_minimal_shifts(self):
        self.assertEqual(first_translation(5, sum_of_two_squares), 48)
        self.assertEqual(first_translation(8, sum_of_two_squares), 96)


if __name__ == "__main__":
    unittest.main(verbosity=2)
