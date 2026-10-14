"""EC-BULK-005 #812-821: finite definition and counterexample regressions only.

No source-cited infinite/asymptotic theorem or external formal proof is certified.
"""
import itertools
import math
import unittest

def edges_complete(n):
    return list(itertools.combinations(range(n),2))

def contains_monochromatic_triangle(n,red):
    E={frozenset(e) for e in red}
    for tri in itertools.combinations(range(n),3):
        sides=[frozenset(p) for p in itertools.combinations(tri,2)]
        if all(e in E for e in sides) or not any(e in E for e in sides):
            return True
    return False

def alpha_or_clique(vertices, edges, clique):
    S={frozenset(e) for e in edges}
    return max((len(C) for r in range(len(vertices)+1)
                for C in itertools.combinations(vertices,r)
                if all((frozenset(p) in S)==clique
                       for p in itertools.combinations(C,2))),default=0)

def min_degree(vertices,edges):
    V=set(vertices)
    assert V
    S={frozenset(e) for e in edges}
    return min(sum(frozenset((u,v)) in S for u in V if u!=v) for v in V)

def has_equal_degree_three_path(vertices,edges):
    S={frozenset(e) for e in edges}
    degree={v:sum(v in e for e in S) for v in vertices}
    return any(degree[a]==degree[d]
               and all(frozenset(pair) in S for pair in ((a,b),(b,c),(c,d)))
               for a,b,c,d in itertools.permutations(vertices,4))

def subset_sums(A):
    return {sum(t) for r in range(len(A)+1)
            for t in itertools.combinations(A,r)}

def has_nontrivial_ap3(S):
    return any((x+z)%2==0 and (x+z)//2 in S
               for x,z in itertools.combinations(sorted(S),2))

def truncated_sumset(A,N):
    return {a+b for a in A for b in A if a+b<=N}

def least_H(n,limit=30):
    for l in range(3,limit+1):
        for k in range(2,l):
            if math.gcd(k**n-1,l**n-1)==1:
                return l,k
    return None

def totient(n):
    x=n;r=n;p=2
    while p*p<=x:
        if x%p==0:
            while x%p==0:x//=p
            r-=r//p
        p+=1
    if x>1:r-=r//x
    return r

class FiniteErdos812To821(unittest.TestCase):
    def test_812_r3_and_linear_gap_small(self):
        # Unique 5-cycle coloring avoids monochromatic K3.
        cycle={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertFalse(contains_monochromatic_triangle(5,cycle))
        E=edges_complete(6)
        self.assertTrue(all(contains_monochromatic_triangle(6,
                       [e for i,e in enumerate(E) if mask&(1<<i)])
                       for mask in range(1<<len(E))))
        for n,first,second in [(2,2,6),(3,6,18)]:
            self.assertGreaterEqual(second-first,4*n-8)

    def test_813_every_seven_subset_has_triangle_k7_minus_edge(self):
        V=tuple(range(7))
        E=set(edges_complete(7))-{(0,1)}
        self.assertTrue(any(all(frozenset(x) in {frozenset(e) for e in E}
                 for x in itertools.combinations(C,2))
                 for C in itertools.combinations(V,3)))
        self.assertEqual(alpha_or_clique(V,E,True),6)

    def test_814_k3_edge_threshold_and_induced_core(self):
        k,n=3,5
        threshold=(k-1)*(n-k+2)+math.comb(k-2,2)+1
        E=set(edges_complete(n))-{(0,1)}
        self.assertEqual((threshold,len(E)),(9,9))
        self.assertEqual(min_degree((1,2,3,4),E),3)

    def test_815_degree_three_critical_k4(self):
        V=tuple(range(4));E=edges_complete(4)
        self.assertEqual(len(E),2*len(V)-2)
        self.assertTrue(all(min_degree(S,E)<=2
                    for k in range(1,len(V)) for S in itertools.combinations(V,k)))
        self.assertEqual(min_degree(V,E),3)

    def test_816_sharp_bipartite_obstruction_and_added_edge(self):
        V=tuple(range(5))
        E=[(a,b) for a in (0,1) for b in (2,3,4)]
        self.assertEqual(len(E),2**2+2)
        self.assertFalse(has_equal_degree_three_path(V,E))
        self.assertTrue(has_equal_degree_three_path(V,E+[(2,3)]))

    def test_817_ternary_subset_cube_avoids_nontrivial_three_ap(self):
        for n in range(1,8):
            A=[3**j for j in range(n)]
            S=subset_sums(A)
            self.assertEqual(len(S),2**n)
            self.assertEqual(max(A),3**(n-1))
            self.assertFalse(has_nontrivial_ap3(S))

    def test_818_sumset_productset_exact(self):
        A=(1,2,3,4)
        self.assertEqual({a+b for a in A for b in A},set(range(2,9)))
        self.assertEqual({a*b for a in A for b in A},{1,2,3,4,6,8,9,12,16})

    def test_819_exact_five_nine_sixteen_truncated(self):
        for N,want in ((5,3),(9,6),(16,10)):
            k=math.isqrt(N)
            best=max(len(truncated_sumset(A,N))
                     for A in itertools.combinations(range(1,N+1),k))
            self.assertEqual(best,want)
        self.assertEqual(len(truncated_sumset((1,3,4),9)),6)

    def test_820_gcd_minimal_bases_exact_ten(self):
        sequence=[3,3,3,6,3,18,3,6,3,12]
        for n,expected in enumerate(sequence,1):
            found=least_H(n,limit=20)
            self.assertIsNotNone(found)
            l,k=found
            self.assertEqual(l,expected)
            self.assertEqual(math.gcd(k**n-1,l**n-1),1)
            self.assertTrue(all(math.gcd(a**n-1,b**n-1)!=1
                    for b in range(3,l) for a in range(2,b)))
        self.assertEqual(math.gcd(5**4-1,6**4-1),1)

    def test_821_finite_totient_preimage_fibers(self):
        for target,expected in ((2,{3,4,6}),(4,{5,8,10,12})):
            fiber={m for m in range(1,301) if totient(m)==target}
            self.assertEqual(fiber,expected)
            self.assertTrue(all(totient(m)==target for m in fiber))

if __name__=="__main__":
    unittest.main()
