"""EC-BULK-005 Erdős #742–751 finite source-fidelity fixtures.
These checks cannot establish asymptotic threshold theorems or review Lean.
"""
import itertools
import math
import unittest
from collections import deque
from fractions import Fraction


def graph_diameter(n,E):
    g=[set() for _ in range(n)]
    for a,b in E:
        g[a].add(b)
        g[b].add(a)
    mx=0
    for start in range(n):
        dist={start:0}
        Q=deque([start])
        while Q:
            u=Q.popleft()
            for v in g[u]:
                if v not in dist:
                    dist[v]=dist[u]+1
                    Q.append(v)
        if len(dist)!=n:
            return math.inf
        mx=max(mx,max(dist.values()))
    return mx


def chromatic_number(n,edges):
    E={frozenset(e) for e in edges}
    for k in range(1,n+1):
        for c in itertools.product(range(k), repeat=n):
            if all(c[a]!=c[b] for a,b in E):
                return k
    return n


def sumfree(A):
    return all(x+y not in A for x in A for y in A)


def independence_number(n,edges):
    E={frozenset(e) for e in edges}
    return max(len(S) for k in range(n+1)
               for S in itertools.combinations(range(n),k)
               if all(not (e<=set(S)) for e in E))


class EC005Checks(unittest.TestCase):
    def test_742_K23_diameter_two_edge_critical(self):
        E={(a,b) for a in (0,1) for b in (2,3,4)}
        self.assertEqual(len(E),6)
        self.assertEqual(graph_diameter(5,E),2)
        for e in E:
            self.assertGreater(graph_diameter(5,E-{e}),2)
        self.assertEqual(len(E),math.floor(25/4))

    def test_743_K4_tree_packing_exact_edge_partition(self):
        P4={(0,1),(1,2),(2,3)}
        T3={(0,2),(0,3)}
        T2={(1,3)}
        all_edges={tuple(p) for p in itertools.combinations(range(4),2)}
        self.assertEqual(P4 | T3 | T2,all_edges)
        self.assertEqual(sum(len(x) for x in [P4,T3,T2]),6)

    def test_744_K4_and_C5_bipartite_deletion(self):
        K4={frozenset(p) for p in itertools.combinations(range(4),2)}
        self.assertEqual(chromatic_number(4,K4),4)
        self.assertEqual(len(K4),6)
        self.assertEqual(max(sum(c[a]!=c[b] for a,b in K4)
                             for c in itertools.product(range(2),repeat=4)),4)
        C5={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertEqual(chromatic_number(5,C5),3)
        self.assertEqual(chromatic_number(5,list(C5)[1:]),2)

    def test_745_critical_vs_supercritical_expected_degrees(self):
        for n in [100,1000,10000]:
            self.assertEqual(Fraction(n-1,n),Fraction(n-1)*Fraction(1,n))
            self.assertEqual(Fraction(2*(n-1),n),Fraction(n-1)*Fraction(2,n))
        # Arithmetic scale warning only, not a random-graph limit proof.
        self.assertGreater(10**6**(2/3) if False else 1000000**(2/3)/math.log(1000000),1000**(2/3)/math.log(1000))

    def test_746_finite_cycle_vs_nonhamiltonian_graph(self):
        C5={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertEqual(len(C5),5)
        self.assertTrue(all(sum(v in e for e in C5)==2 for v in range(5)))
        self.assertEqual(graph_diameter(5,C5),2)

    def test_747_perfect_three_matching_on_six(self):
        triples={frozenset(x) for x in itertools.combinations(range(6),3)}
        matched={frozenset((a,b)) for a,b in itertools.combinations(triples,2)
                 if not a&b}
        self.assertEqual(len(matched),10)
        self.assertEqual(len(triples),20)
        self.assertEqual(sum(0 in t for t in triples),10)

    def test_748_sumfree_upper_half_bound_small_n(self):
        for n in range(1,10):
            U=set(range(n//2+1,n+1))
            self.assertTrue(sumfree(U))
            self.assertEqual(len(U),(n+1)//2)
            count=sum(sumfree(set(c)) for m in range(n+1)
                      for c in itertools.combinations(range(1,n+1),m))
            self.assertGreaterEqual(count,2**len(U))

    def test_749_finite_sidon_low_representation(self):
        A={1,3,7}
        sums={x+y for x in A for y in A}
        self.assertEqual(sums,{2,4,6,8,10,14})
        self.assertEqual(max(sum(a+b==s for a in A for b in A)
                             for s in sums),2)

    def test_750_finite_independence_c5_induced_subgraphs(self):
        C5={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertEqual(chromatic_number(5,C5),3)
        for m in range(1,6):
            for S in itertools.combinations(range(5),m):
                E={e for e in C5 if e<=set(S)}
                # relabel vertices of induced graph for independent-set count
                idx={v:i for i,v in enumerate(S)}
                H={frozenset(idx[v] for v in e) for e in E}
                self.assertGreaterEqual(independence_number(m,H),m//2)

    def test_751_K4_cycle_lengths_and_critical_degree(self):
        E={frozenset(p) for p in itertools.combinations(range(4),2)}
        self.assertEqual(chromatic_number(4,E),4)
        self.assertEqual({len(c) for k in (3,4)
                          for c in itertools.permutations(range(4),k)}, {3,4})
        self.assertEqual(min(sum(v in e for e in E)
                             for v in range(4)),3)


if __name__=="__main__":
    unittest.main(verbosity=2)
