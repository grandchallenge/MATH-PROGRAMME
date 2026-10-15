"""Exact source-semantics fixtures for EC-BULK-005 conflicts #730..#784.

Finite checks only. Neither asymptotic bounds nor external formal proof claims
are certified by these calculations.
"""
import itertools
import math
import unittest
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ED = ROOT / "governance/erdos_compendium/editorial"

def prime_support_central(n):
    c = math.comb(2*n,n)
    primes = set()
    p=2
    while p*p<=c:
        if c%p==0:
            primes.add(p)
            while c%p==0:c//=p
        p+=1 if p==2 else 2
    if c>1:primes.add(c)
    return primes

def all_edges(vertices):
    return list(itertools.combinations(vertices,2))

def distance(adj,start,goal):
    if start==goal:return 0
    frontier={start};seen={start}
    for depth in range(1,len(adj)+2):
        frontier=set().union(*(adj[v] for v in frontier))-seen
        if goal in frontier:return depth
        if not frontier:return math.inf
        seen|=frontier
    return math.inf

def max_distance(vertices,edges):
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    return max(distance(adj,x,y) for x,y in itertools.combinations(vertices,2))

def is_sidon(A):
    pairs=[a+b for i,a in enumerate(A) for b in A[i:]]
    return len(pairs)==len(set(pairs))

class EC005Conflict02(unittest.TestCase):
    def test_730_support_same_is_not_infinitude(self):
        for a,b in ((87,88),(607,608)):
            self.assertEqual(prime_support_central(a),prime_support_central(b))
            self.assertNotEqual(math.comb(2*a,a),math.comb(2*b,b))
        text=(ED/"0730.md").read_text()
        self.assertIn("infinitely",text)

    def test_741_strict_vs_upper_density_are_distinct_definitions(self):
        N=1000
        even=sum(n%2==0 for n in range(N))
        odd=sum(n%2==1 for n in range(N))
        self.assertEqual((even,odd),(500,500))
        self.assertEqual({2*n for n in range(20)}.intersection(set(range(20,40))),
                         {2*n for n in range(10,20)})
        text=(ED/"0741.md").read_text()
        for word in ("upper", "lower", "density"):
            self.assertIn(word,text.lower())

    def test_742_bipartite_diameter_critical_5_vertices(self):
        vertices=range(5)
        E={(a,b) for a in (0,1) for b in (2,3,4)}
        self.assertEqual(len(E),6)
        self.assertEqual(max_distance(vertices,E),2)
        for e in E:
            self.assertGreater(max_distance(vertices,E-{e}),2)
        self.assertEqual(len(E),5*5//4)

    def test_745_critical_vs_supercritical_parameter_and_scaling(self):
        for n in (100,1000,10000):
            critical=Fraction(1,n)
            supercritical=Fraction(2,n)
            self.assertGreater(supercritical,critical)
            self.assertGreater(n**(2/3),math.log(n))
        text=(ED/"0745.md").read_text()
        self.assertIn("λ>1",text)
        self.assertIn("p=1/n",text)
        self.assertIn("Aldous",text)

    def test_750_c5_is_finite_not_infinite_chromatic(self):
        V=set(range(5))
        E={(min(i,(i+1)%5),max(i,(i+1)%5)) for i in V}
        def independent(T):
            S=set(T)
            return all(not(a in S and b in S) for a,b in E)
        for size in range(6):
            for subset in itertools.combinations(V,size):
                alpha=max(sum(independent(T) for T in itertools.combinations(subset,k))>0
                          and k or 0 for k in range(size+1))
                self.assertGreaterEqual(alpha,math.floor(size/2))
        self.assertEqual(len(V),5)
        self.assertIn("infinite chromatic", (ED/"0750.md").read_text().lower())

    def test_765_c4_free_common_neighbor_bound(self):
        V=set(range(5))
        E={(min(i,(i+1)%5),max(i,(i+1)%5)) for i in V}
        adj={v:set() for v in V}
        for a,b in E:adj[a].add(b);adj[b].add(a)
        self.assertTrue(all(len(adj[a]&adj[b])<=1 for a,b in itertools.combinations(V,2)))
        self.assertLessEqual(sum(math.comb(len(adj[v]),2) for v in V),math.comb(len(V),2))
        self.assertEqual(len(E),5)
        self.assertIn("Ma", (ED/"0765.md").read_text())

    def test_770_collective_gcd_not_pairwise_coprimality(self):
        terms=[pow(j,4)-1 for j in range(2,6)]
        self.assertEqual(terms,[15,80,255,624])
        self.assertEqual(math.gcd(*terms[:3]),5)
        self.assertEqual(math.gcd(*terms),1)
        self.assertEqual(math.gcd(terms[0],terms[1]),5)
        self.assertEqual(math.gcd(pow(2,2)-1,pow(3,2)-1),1)

    def test_772_ordered_convolution_k2_and_k1(self):
        A=[1,2,4,8]
        ordered=Counter(a+b for a in A for b in A)
        self.assertEqual(max(ordered.values()),2)
        self.assertTrue(is_sidon(A))
        for c in itertools.combinations(range(1,9),4):
            d=Counter(a+b for a in c for b in c)
            if max(d.values())<=2:self.assertTrue(is_sidon(c))
        collision=Counter(a+b for a in (1,2,3) for b in (1,2,3))
        self.assertEqual(collision[4],3)
        self.assertIn("H_2(n)=n",(ED/"0772.md").read_text().replace("$","").replace(" ",""))

    def test_783_pairwise_coprime_sieve_example(self):
        survivors=[m for m in range(1,11) if m%2 and m%3]
        self.assertEqual(survivors,[1,5,7])
        self.assertEqual(Fraction(1,2)+Fraction(1,3),Fraction(5,6))

    def test_784_one_loophole_and_corrected_union_bound(self):
        uncovered=[m for m in range(1,13) if m%2 and m%3]
        self.assertEqual(uncovered,[1,5,7,11])
        self.assertEqual([m for m in range(1,13) if m%1],[ ])
        for n in (12,100):
            A={2,3};weight=Fraction(5,6)
            covered=sum(any(i%a==0 for a in A) for i in range(1,n+1))
            self.assertLessEqual(covered,math.floor(n*weight))
if __name__=="__main__":
    unittest.main()
