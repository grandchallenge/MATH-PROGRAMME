"""EC-BULK-005 #782-791: reproducible exact finite definition fixtures.

These tests do not certify any published infinite or asymptotic statement.
"""
import itertools
import math
import unittest

def uncovered(N,A):
    return tuple(m for m in range(1,N+1) if all(m%a for a in A))

def legal_coprime(A):
    return all(math.gcd(a,b)==1 for a,b in itertools.combinations(A,2))

def legal_summands(A,ambient):
    return all(a+b not in ambient for a,b in itertools.combinations(A,2))

def no_unequal_subset_sums(A):
    sums={}
    for k in range(len(A)+1):
        for combo in itertools.combinations(A,k):
            total=sum(combo)
            if total in sums and sums[total]!=k:
                return False
            sums[total]=k
    return True

def strongly_sumfree(A):
    for x in A:
        other=[a for a in A if a!=x]
        if any(sum(items)==x for k in range(2,len(other)+1)
               for items in itertools.combinations(other,k)):
            return False
    return True

def additive_basis(A,n):
    s={a+b for a in A for b in A}
    return all(v in s for v in range(n+1))

class Fixture782Through791(unittest.TestCase):
    def test_782_positive_square_cube(self):
        corners={1,1+48,1+120,1+48+120}
        self.assertEqual(corners,{1,49,121,169})
        self.assertTrue(all(math.isqrt(v)**2==v for v in corners))
        self.assertEqual([4-1,9-4,16-9],[3,5,7])

    def test_783_coprime_sieve(self):
        self.assertTrue(legal_coprime((2,3)))
        self.assertFalse(legal_coprime((2,4)))
        self.assertEqual(uncovered(10,(2,3)),(1,5,7))
        self.assertLessEqual(1/2+1/3,1)

    def test_784_exclusion_one_and_union_bound(self):
        self.assertEqual(uncovered(12,(2,3)),(1,5,7,11))
        self.assertEqual(uncovered(12,(1,)),())
        for x in range(2,13):
            for A in ((2,),(3,),(2,3),(2,5),(3,5)):
                mass=sum(1/a for a in A)
                if mass<1:
                    self.assertGreaterEqual(len(uncovered(x,A)),x*(1-mass)-1e-9)

    def test_785_finite_additive_coverage(self):
        A,B=set(range(1,6)),{1,3,5}
        sums={a+b for a in A for b in B}
        self.assertTrue(set(range(2,11))<=sums)
        self.assertEqual(len(A)*len(B),15)

    def test_786_two_adic_product_length(self):
        A=[2,6,10,14]
        def v2(x):
            r=0
            while x%2==0: x//=2;r+=1
            return r
        self.assertTrue(all(v2(x)==1 for x in A))
        for r in range(1,4):
            for s in range(1,4):
                for left in itertools.product(A,repeat=r):
                    for right in itertools.product(A,repeat=s):
                        if math.prod(left)==math.prod(right):
                            self.assertEqual(r,s)
        self.assertEqual(2*2,4)

    def test_787_ambient_not_internal_sums(self):
        A={1,2,3,4}
        self.assertTrue(legal_summands((2,3,4),A))
        self.assertFalse(legal_summands((1,2),A))
        self.assertTrue(legal_summands((1,2),{1,2}))

    def test_788_minimax_exact_small(self):
        n=3
        middle=list(range(n+1,2*n))
        upper=list(range(2*n+1,4*n))
        self.assertEqual(middle,[4,5])
        self.assertEqual(upper,[7,8,9,10,11])
        values=[]
        for mask in range(1<<len(upper)):
            B={v for i,v in enumerate(upper) if mask&(1<<i)}
            max_c=max(len(C) for k in range(len(middle)+1)
                    for C in itertools.combinations(middle,k)
                    if legal_summands(C,B))
            values.append(len(B)+max_c)
        self.assertEqual(min(values),2)

    def test_789_cardinality_and_repetition_conflict(self):
        self.assertTrue(no_unequal_subset_sums((2,3)))
        self.assertFalse(no_unequal_subset_sums((1,2,3)))
        self.assertEqual(2+2+2,3+3)
        self.assertNotEqual(3,2)

    def test_790_all_distinct_multi_term_sums(self):
        self.assertTrue(strongly_sumfree((1,2,4)))
        self.assertFalse(strongly_sumfree((1,2,3)))
        self.assertFalse(strongly_sumfree((1,2,4,7)))

    def test_791_minimal_two_basis_n5(self):
        self.assertTrue(additive_basis((0,1,2,3),5))
        self.assertFalse(any(additive_basis(A,5)
                         for A in itertools.combinations(range(6),3)))
        self.assertEqual(len((0,1,2,3)),4)

if __name__=="__main__":
    unittest.main()
