"""EC-BULK-005 Erdős #822–#831: finite definitions, certificates and conventions.

No infinite asymptotic theorem, unpublished primary proof or external
formal verification is certified by these finite assertions.
"""
import itertools
import math
import unittest
from collections import Counter
from fractions import Fraction

def divisors(n):
    return [d for d in range(1,n+1) if n%d==0]

def sigma(n):
    return sum(divisors(n))

def tau(n):
    return len(divisors(n))

def totient(n):
    return sum(math.gcd(n,k)==1 for k in range(1,n+1))

def omega(n):
    m=n;p=2;count=0
    while p*p<=m:
        if m%p==0:
            count+=1
            while m%p==0:m//=p
        p+=1
    return count+(m>1)

def subset_sum_possible(n, items):
    possible={0}
    for d in items:
        possible|={d+x for x in possible}
    return n in possible

def h_sigma(x):
    return sum(math.gcd(a,b)==1 and sigma(a)==sigma(b)
               for a in range(1,x) for b in range(a+1,x))

def sq_circumradius(triangle):
    a,b,c=triangle
    det=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    if not det:
        return None
    def d2(p,q):
        return (p[0]-q[0])**2+(p[1]-q[1])**2
    return Fraction(d2(a,b)*d2(a,c)*d2(b,c),4*det**2)

def radii4(points):
    assert len(points)==4
    out=[sq_circumradius(tri) for tri in itertools.combinations(points,3)]
    assert None not in out
    return out

def cube_pair_count(n,limit):
    return sum(a**3+b**3==n for a in range(1,limit+1)
               for b in range(1,limit+1))

def amicable_pairs(bound,include_diagonal=False):
    return {(a,b) for a in range(1,bound+1)
            for b in range(a if include_diagonal else a+1,bound+1)
            if sigma(a)==sigma(b)==a+b}

class FiniteErdos822To831(unittest.TestCase):
    def test_822_images_under_four_arithmetic_functions(self):
        self.assertEqual([n+totient(n) for n in range(1,7)],
                         [2,3,5,6,9,8])
        self.assertEqual([n+sigma(n) for n in range(1,7)],
                         [2,5,7,11,11,18])
        for f in (totient,sigma,tau,omega):
            output={n+f(n) for n in range(1,101)}
            self.assertTrue(output)
            self.assertLessEqual(len(output),100)
        self.assertLess(len({n+sigma(n) for n in range(1,7)}),6)

    def test_823_exact_sigma_equalities_not_limit_theorem(self):
        self.assertEqual((sigma(6),sigma(11)),(12,12))
        self.assertEqual(sigma(14),sigma(15))
        self.assertEqual(sigma(15),sigma(23))
        self.assertNotEqual(Fraction(11,6),Fraction(15,14))

    def test_824_gcd_and_strict_pair_range(self):
        self.assertEqual(math.gcd(6,11),1)
        self.assertEqual(math.gcd(14,15),1)
        self.assertEqual(sigma(20),sigma(26))
        self.assertEqual(math.gcd(20,26),2)
        pairs={(a,b) for a in range(1,31) for b in range(a+1,31)
               if math.gcd(a,b)==1 and sigma(a)==sigma(b)}
        self.assertEqual(len(pairs),h_sigma(31))
        self.assertIn((6,11),pairs)
        self.assertNotIn((20,26),pairs)
        self.assertLess(h_sigma(11),h_sigma(12))

    def test_825_70_weird_12_semiperfect(self):
        proper70=divisors(70)[:-1]
        proper12=divisors(12)[:-1]
        self.assertEqual(proper70,[1,2,5,7,10,14,35])
        self.assertEqual(sigma(70),144)
        self.assertGreater(sigma(70),2*70)
        self.assertFalse(subset_sum_possible(70,proper70))
        self.assertTrue(subset_sum_possible(12,proper12))
        self.assertEqual(6+4+2,12)

    def test_826_divisor_counts_bounded_only(self):
        self.assertEqual([tau(1+k) for k in range(1,6)],
                         [2,2,3,2,4])
        self.assertTrue(all(tau(1+k)<=4*k for k in range(1,101)))
        self.assertEqual(tau(12),6)

    def test_827_exact_distinct_circumradii_four_points(self):
        pts=((0,0),(0,1),(1,0),(1,2))
        rs=radii4(pts)
        self.assertEqual(rs,[Fraction(1,2),Fraction(5,2),
                             Fraction(5,4),Fraction(1,1)])
        self.assertEqual(len(set(rs)),4)

    def test_828_self_dividing_phi_exponent_restriction(self):
        self.assertEqual(totient(3),2)
        self.assertNotEqual(3%totient(3),0)
        self.assertNotEqual(9%totient(9),0)
        observed={n for n in range(1,201) if n%totient(n)==0}
        expected={1}
        for a in range(1,9):
            for b in range(0,6):
                n=2**a*3**b
                if n<=200:expected.add(n)
        self.assertEqual(observed,expected)

    def test_829_ordered_cube_convolution(self):
        self.assertEqual(1**3+12**3,1729)
        self.assertEqual(9**3+10**3,1729)
        self.assertEqual(cube_pair_count(1729,14),4)
        self.assertEqual(cube_pair_count(2,14),1)

    def test_830_amicable_distinct_and_diagonal_conventions(self):
        self.assertEqual(sigma(220),504)
        self.assertEqual(sigma(284),504)
        strict=amicable_pairs(300,False)
        weak=amicable_pairs(300,True)
        self.assertIn((220,284),strict)
        self.assertNotIn((6,6),strict)
        self.assertIn((6,6),weak)
        self.assertTrue(strict<weak)

    def test_831_general_position_does_not_force_unique_radii(self):
        points=((0,0),(0,1),(1,0),(1,3))
        rs=radii4(points)
        self.assertEqual(rs,[Fraction(1,2),Fraction(25,2),
                             Fraction(5,2),Fraction(5,2)])
        self.assertEqual(len(set(rs)),3)
        # Four points concyclic precisely when all four triple circles coincide.
        self.assertGreater(len(set(rs)),1)
        self.assertEqual(len(set(radii4(((0,0),(0,1),(1,0),(1,2))))),4)

if __name__=="__main__":
    unittest.main()
