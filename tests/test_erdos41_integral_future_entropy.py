"""Erdos 41: exact B3 pair-sum difference cap and future batch entropy.

Mathematical status: integral extension-count deficit, NOT a cardinality
capacity decrement or an Erdős #41 solution.
Run: python -m unittest discover -s tests -p 'test_erdos41_integral_future_entropy.py' -v
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from math import comb, exp
import unittest

A=[1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
   3098,4048,5298,6704,7839,10987,12332,15465,19144,
   24546,28974,34406,37769,45864,50877]


def is_b3(xs):
    tri=[sum(t) for t in combinations_with_replacement(sorted(xs),3)]
    return len(tri)==len(set(tri))


def pair_sums(xs):
    return {a+b for a,b in combinations_with_replacement(sorted(xs),2)}


def pair_diff_profile(xs):
    q=pair_sums(xs)
    return Counter(u-v for u in q for v in q if u>v)


def graph_edges(xs,R):
    ds=set(pair_diff_profile(xs))
    return sum(R-d for d in ds if d<R)


def graph_adjacency(xs,R):
    diffs=set(pair_diff_profile(xs))
    return {u:{v for v in range(1,R+1)
               if u!=v and abs(u-v) in diffs}
            for u in range(1,R+1)}


def independent_set_count(graph,k):
    vertices=sorted(graph)
    return sum(
        all(v not in graph[u] for u,v in combinations(t,2))
        for t in combinations(vertices,k)
    )


def actual_future_batches(p,R,k,y):
    assert y>6*R
    j=range(2*y-R,2*y-min(p)+1)
    return [
        t for t in combinations(j,k)
        if is_b3(p+[y]+list(t))
    ]


def exact_lower_bound(n,R):
    return n**3*R/512


def independent_entropy_upper(L,k,epsilon):
    assert 0<epsilon<=1/4
    assert 2<=k<=epsilon*L
    return 2*exp(-epsilon*(k-1)/4)*comb(L,k)


class IntegralFutureEntropyTests(unittest.TestCase):
    def test_fixture_genuine_b3(self):
        self.assertTrue(is_b3(A))

    def test_pointwise_pair_sum_multiplicity_cap(self):
        for n in (4,5,8,12,20,29):
            with self.subTest(n=n):
                p=A[:n]
                r=pair_diff_profile(p)
                self.assertTrue(all(v<=n for v in r.values()))
                original_differences={a-b for a in p for b in p if a>b}
                self.assertTrue(all(r[d]==n for d in original_differences))
                self.assertTrue(all(r[d]<n for d in r if d not in original_differences))
                self.assertEqual(sum(r.values()),comb(len(pair_sums(p)),2))

    def test_short_differences_and_edge_density(self):
        for n,R in ((4,14),(5,33),(8,219),(12,1210),
                    (20,11000),(29,51000)):
            p=A[:n]
            self.assertLessEqual(max(p),R)
            q=pair_sums(p)
            short={d for d in pair_diff_profile(p) if 1<=d<=R//2}
            with self.subTest(n=n,R=R):
                self.assertGreaterEqual(len(short)+1e-9,n**3/256)
                e=graph_edges(p,R)
                self.assertGreaterEqual(e+1e-9,exact_lower_bound(n,R))
                self.assertLessEqual(e,comb(R,2))
                self.assertEqual(len(q),comb(n+1,2))

    def test_future_batches_must_be_graph_independent(self):
        p=[1,2,5,14]
        R=14
        y=100
        adjacency=graph_adjacency(p,R)
        for k in (1,2,3):
            for x in actual_future_batches(p,R,k,y):
                t={2*y-z for z in x}
                self.assertTrue(all(u not in adjacency[v]
                                    for u,v in combinations(sorted(t),2)))

    def test_entropy_lemma_complete_bipartite_and_clique(self):
        # Exact independent-set polynomials for dense hostile graphs.
        for left,right in ((10,10),(12,18),(20,20)):
            L=left+right
            eps=min(0.25,left*right/L**2)
            kmax=int(eps*L)
            for k in range(2,kmax+1):
                count=sum(comb(left,i)*comb(right,k-i)
                          for i in range(max(0,k-right),min(k,left)+1)
                          if i==0 or i==k)
                with self.subTest(graph="bipartite",L=L,k=k):
                    self.assertLessEqual(
                        count,independent_entropy_upper(L,k,eps)+1e-8)
        for L,clique in ((20,8),(30,12),(60,24)):
            eps=min(0.25,clique*(clique-1)/(2*L*L))
            for k in range(2,int(eps*L)+1):
                count=comb(L-clique,k) if k<=L-clique else 0
                if k>=1 and k-1<=L-clique:
                    count+=clique*comb(L-clique,k-1)
                with self.subTest(graph="clique",L=L,k=k):
                    self.assertLessEqual(
                        count,independent_entropy_upper(L,k,eps)+1e-8)

    def test_future_graph_bound_even_with_optimized_batch_shapes(self):
        p=[1,2,5,14]
        R=14
        G=graph_adjacency(p,R)
        e=sum(len(s) for s in G.values())//2
        eps=min(0.25,e/R**2)
        y=100
        for k in range(2,int(eps*R)+1):
            with self.subTest(k=k):
                batches=actual_future_batches(p,R,k,y)
                independent=independent_set_count(G,k)
                self.assertLessEqual(len(batches),independent)
                self.assertLessEqual(
                    independent,independent_entropy_upper(R,k,eps)+1e-8)

    def test_multiscale_branching_product_is_valid_combinatorially(self):
        # The theorem is a uniform conditional branching count, not an
        # assertion that arbitrarily many prescribed stages stay populated.
        p=[1,2,5,14]
        R=14
        y=8*R
        stage=[t for t in combinations(range(2*y-R,2*y-min(p)+1),1)
               if is_b3(p+[y]+list(t))]
        self.assertLessEqual(len(stage),R)
        self.assertTrue(all(min(t)>=15*R for t in stage))
        self.assertTrue(all(max(t)<16*R for t in stage))


if __name__=="__main__":
    unittest.main()
