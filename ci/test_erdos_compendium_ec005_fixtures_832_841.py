"""Erdős EC005 #832-841: exact finite checks; no asymptotic proof certification."""
import itertools
import math
import unittest
from collections import Counter

def fano():
    return {frozenset(((i-1),(j-1),(i^j)-1))
            for i in range(1,8) for j in range(i+1,8)}

def can_color(edges, vertices, k):
    edges=[frozenset(e) for e in edges]
    v=sorted(vertices)
    return any(all(len({color[x] for x in e})>=2 for e in edges)
               for choices in itertools.product(range(k),repeat=len(v))
               for color in [{a:b for a,b in zip(v,choices)}])

def alon_intersecting_r3():
    X=set(range(4));partitions={}
    for subset in itertools.combinations(sorted(X),2):
        A=frozenset(subset);B=frozenset(X-A)
        part=frozenset((A,B))
        partitions.setdefault(part,4+len(partitions))
    edges={frozenset(t) for t in itertools.combinations(X,3)}
    for part,y in partitions.items():
        for side in part:edges.add(frozenset(set(side)|{y}))
    return edges,set(range(4+len(partitions)))

def j_graph(k):
    verts=[frozenset(c) for c in itertools.combinations(range(2*k),k)]
    edges={i:set() for i in range(len(verts))}
    for i,j in itertools.combinations(range(len(verts)),2):
        if len(verts[i]&verts[j])==k-1:
            edges[i].add(j);edges[j].add(i)
    return verts,edges

def is_q_colorable(graph,q):
    n=len(graph);color=[-1]*n
    def search(used):
        if used==n:return True
        v=max((i for i in range(n) if color[i]<0),
              key=lambda i:(len({color[j] for j in graph[i] if color[j]>=0}),len(graph[i])))
        forbidden={color[j] for j in graph[v]}
        num_used=len(set(color)-{-1})
        for c in range(min(q,num_used+1)):
            if c in forbidden:continue
            color[v]=c
            if search(used+1):return True
            color[v]=-1
        return False
    return search(0)

def strict_inside_triangle(pt,triangle):
    def cross(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    A,B,C=triangle
    signs=[cross(A,B,pt),cross(B,C,pt),cross(C,A,pt)]
    return all(x>0 for x in signs) or all(x<0 for x in signs)

def convex_position(points):
    if len(points)<=3:return True
    return not any(strict_inside_triangle(p,[x for x in points if x!=p])
                   for p in points)

def convex_subset_count(points):
    return sum(convex_position(C) for k in range(len(points)+1)
               for C in itertools.combinations(points,k))

def no_earlier_block_sum(A):
    return all(A[i]!=sum(A[j:h])
               for i in range(len(A)) for j in range(i) for h in range(j+1,i+1))

def parity_primes(n):
    result=set();p=2
    while p*p<=n:
        bit=0
        while n%p==0:n//=p;bit^=1
        if bit:result.add(p)
        p+=1
    if n>1:result.add(n)
    return result

def t(n,limit=20):
    if math.isqrt(n)**2==n:return 0
    parity=parity_primes(n)
    # Exact GF(2) reachable parity vectors over suffix terms.
    reachable={frozenset()}
    for delta in range(1,limit+1):
        f=parity_primes(n+delta)
        reachable |= {frozenset(set(s)^f) for s in reachable}
        if frozenset(parity) in reachable:return delta
    return None

class TestErdos832841(unittest.TestCase):
    def test_832_fano_counterexample_small_k(self):
        E=fano();self.assertEqual(len(E),7)
        self.assertFalse(can_color(E,range(7),2))
        self.assertTrue(can_color(E,range(7),3))
        self.assertEqual(math.comb(5,3),10)

    def test_833_fano_degree_and_triangle(self):
        E=fano()
        self.assertEqual(Counter(v for e in E for v in e),{j:3 for j in range(7)})
        triangle=[(0,1),(1,2),(0,2)]
        self.assertFalse(can_color(triangle,range(3),2))
        self.assertTrue(can_color(triangle,range(3),3))

    def test_834_k5_complete_threeuniform_critical(self):
        E={frozenset(c) for c in itertools.combinations(range(5),3)}
        self.assertEqual(len(E),10)
        self.assertFalse(can_color(E,range(5),2))
        self.assertTrue(can_color(E,range(5),3))
        self.assertTrue(all(can_color(E-{e},range(5),2) for e in E))
        self.assertTrue(all(can_color([e for e in E if v not in e],set(range(5))-{v},2)
                            for v in range(5)))
        self.assertTrue(all(sum(v in e for e in E)==6 for v in range(5)))

    def test_835_johnson_small_chromatic_numbers(self):
        v2,g2=j_graph(2)
        self.assertEqual(len(v2),6)
        self.assertTrue(is_q_colorable(g2,3))
        self.assertFalse(is_q_colorable(g2,2))
        v3,g3=j_graph(3)
        self.assertEqual(len(v3),20)
        self.assertFalse(is_q_colorable(g3,4))

    def test_836_alon_r3_construct_intersecting_not_two_colorable(self):
        E,V=alon_intersecting_r3()
        self.assertEqual((len(E),len(V)),(10,7))
        self.assertTrue(all(a&b for a,b in itertools.combinations(E,2)))
        self.assertFalse(can_color(E,V,2))
        self.assertTrue(can_color(E,V,3))

    def test_837_bipartite_turan_density_sequence(self):
        for m in (3,4,8):
            n=2*m
            edges=m*m
            self.assertEqual(edges/math.comb(n,2),m/(2*m-1))
            self.assertGreater(edges/math.comb(n,2),0.5)
        self.assertLess(8/(2*8-1)-0.5,3/(2*3-1)-0.5)

    def test_838_exact_convex_position_four_point_counts(self):
        square=[(0,0),(2,0),(2,2),(0,2)]
        inside=[(0,0),(4,0),(0,4),(1,1)]
        self.assertEqual(convex_subset_count(square),16)
        self.assertEqual(convex_subset_count(inside),15)
        self.assertFalse(convex_position(inside))

    def test_839_consecutive_block_any_prior_interval(self):
        self.assertTrue(no_earlier_block_sum([1,2,4,8,16,32]))
        self.assertFalse(no_earlier_block_sum([1,3,5,7,9]))
        self.assertEqual(sum([1,3,5]),9)

    def test_840_unordered_pair_sums_true_sidon(self):
        A=[1,2,4,8]
        sums=[a+b for i,a in enumerate(A) for b in A[i:]]
        self.assertEqual(len(sums),math.comb(len(A)+1,2))
        self.assertEqual(len(set(sums)),10)
        self.assertNotEqual(len(set(sums)),math.comb(len(A),2))

    def test_841_square_exception_and_t6(self):
        self.assertEqual(t(4),0)
        self.assertEqual(t(6),6)
        self.assertEqual(6*8*12,24**2)
        self.assertNotEqual(t(6),3)

if __name__=="__main__":
    unittest.main()
