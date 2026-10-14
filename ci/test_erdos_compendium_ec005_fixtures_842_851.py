"""EC-BULK-005 #842-851 exact finite fixtures; no infinite theorem certification."""
import itertools
import math
import unittest
from collections import Counter

def sf(n):
    return all(n%(p*p)!=0 for p in range(2,math.isqrt(n)+1))

def squares_subset_sums(nums):
    out={0}
    for a in nums:
        out|={v+a for v in tuple(out)}
    return out

def valid_complete_product(A):
    return all(not sf(a*b) for a in A for b in A)

def smooth_below(limit):
    return sorted(n for n in range(1,limit+1)
                  if all(p in (2,3) for p in prime_factors(n)))

def prime_factors(n):
    out=set();p=2
    while p*p<=n:
        if n%p==0:
            out.add(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.add(n)
    return out

def min_spread_smooth_witnesses(limit):
    nums=smooth_below(limit)
    results={}
    for a in nums:
        eligible=[b for b in nums if a<b<6*a]
        sums={a:(a,)}
        for b in eligible:
            for value,witness in tuple(sums.items()):
                nxt=value+b
                if nxt<=limit and nxt not in sums:
                    sums[nxt]=witness+(b,)
        results.update({n:w for n,w in sums.items() if n not in results})
    return results

def no_three_collinear(points):
    return all((b[0]-a[0])*(c[1]-a[1]) != (b[1]-a[1])*(c[0]-a[0])
               for a,b,c in itertools.combinations(points,3))

def is_three_ap_free(values):
    s=set(values)
    return all(x+z!=2*y for x,z in itertools.combinations(s,2)
               for y in s if x!=y and y!=z)

def binomial_pairs(value):
    hits=[(value,1)]
    for n in range(2,value):
        if math.comb(n,2)>value:
            # Only k=1 is still possible, already counted above.
            continue
        for k in range(2,n//2+1):
            if math.comb(n,k)==value:hits.append((n,k))
    return sorted(hits)

def factor_counts(n):
    distinct=0;with_multiplicity=0;p=2
    while p*p<=n:
        if n%p==0:
            distinct+=1
            while n%p==0:
                n//=p
                with_multiplicity+=1
        p+=1
    if n>1:
        distinct+=1
        with_multiplicity+=1
    return distinct,with_multiplicity

class EC005Finite842851(unittest.TestCase):
    def test_842_disjoint_triangles_cycle_and_3_coloring(self):
        triangles=[(0,1,2),(3,4,5)]
        old={frozenset(e) for t in triangles for e in itertools.combinations(t,2)}
        cycle=[0,3,1,4,2,5]
        new={frozenset((cycle[i],cycle[(i+1)%6])) for i in range(6)}
        self.assertEqual(len(old),6)
        self.assertEqual(len(new),6)
        self.assertFalse(old&new)
        coloring={0:0,1:1,2:2,3:2,4:0,5:1}
        self.assertTrue(all(coloring[a]!=coloring[b] for a,b in map(tuple,old|new)))

    def test_843_distinct_square_subset_sums_finite(self):
        sums=squares_subset_sums((1,4,9))
        self.assertEqual(sums,{0,1,4,5,9,10,13,14})
        self.assertNotIn(2,sums)
        self.assertTrue(all(i not in sums for i in range(15,21)))

    def test_844_squarefree_pair_intersection_exact_max(self):
        for N in (6,8,10):
            sq=[n for n in range(1,N+1) if sf(n)]
            good=[tuple(sq[i] for i in range(len(sq)) if mask>>i&1)
                  for mask in range(1<<len(sq))]
            maximum=max(len(A) for A in good if valid_complete_product(A))
            even_sq={v for v in sq if v%2==0}
            self.assertEqual(maximum,len(even_sq))
            candidate=tuple(n for n in range(1,N+1)
                            if n%2==0 or not sf(n))
            self.assertTrue(valid_complete_product(candidate))
            self.assertEqual(len(candidate),len(even_sq)+sum(not sf(v) for v in range(1,N+1)))
        self.assertEqual(set((2,4,6,8,9,10)),set(n for n in range(1,11) if n%2==0 or not sf(n)))

    def test_845_smooth_sum_strict_spread_up_to_100(self):
        results=min_spread_smooth_witnesses(100)
        self.assertTrue(all(n in results for n in range(1,101)))
        for n in range(1,101):
            terms=results[n]
            self.assertEqual(n,sum(terms))
            self.assertEqual(terms,tuple(sorted(set(terms))))
            self.assertLess(terms[-1],6*terms[0])
            self.assertTrue(all(prime_factors(t)<={2,3} for t in terms))
        self.assertIn(5,results)
        self.assertIn(7,results)

    def test_846_finite_general_position_is_not_infinite_counterexample(self):
        points=[(0,0),(0,1),(1,0),(1,3)]
        self.assertTrue(no_three_collinear(points))
        bad=[(0,0),(1,1),(2,2),(0,2)]
        self.assertFalse(no_three_collinear(bad))
        self.assertTrue(any(no_three_collinear(S) for S in itertools.combinations(bad,3)))

    def test_847_four_point_max_three_apfree(self):
        nums=(1,2,3,4)
        maxsize=max(len(sub) for k in range(5)
                    for sub in itertools.combinations(nums,k)
                    if is_three_ap_free(sub))
        self.assertEqual(maxsize,3)
        self.assertTrue(is_three_ap_free((1,2,4)))
        self.assertFalse(is_three_ap_free(nums))

    def test_848_two_roots_mod25_cannot_be_combined(self):
        self.assertEqual((7*7+1)%25,0)
        self.assertEqual((18*18+1)%25,0)
        self.assertTrue(all((a*b+1)%25==0 for a in (7,32,57)
                            for b in (7,32,57)))
        self.assertTrue(sf(7*18+1))
        self.assertEqual(7*18+1,127)

    def test_849_pascal_exact_three_and_four_multiplicity(self):
        self.assertEqual(binomial_pairs(120),[(10,3),(16,2),(120,1)])
        self.assertEqual(binomial_pairs(3003),[(14,6),(15,5),(78,2),(3003,1)])

    def test_850_two_shifts_match_three_fail(self):
        self.assertEqual(prime_factors(75),prime_factors(1215))
        self.assertEqual(prime_factors(76),prime_factors(1216))
        self.assertNotEqual(prime_factors(77),prime_factors(1217))
        self.assertEqual(prime_factors(77),{7,11})
        self.assertEqual(prime_factors(1217),{1217})

    def test_851_distinct_vs_multiplicity_prime_counts(self):
        self.assertEqual(factor_counts(9),(1,2))
        self.assertEqual(factor_counts(2),(1,1))
        self.assertEqual(10,2**0+9)
        self.assertEqual(10,2**3+2)

if __name__=="__main__":
    unittest.main()
