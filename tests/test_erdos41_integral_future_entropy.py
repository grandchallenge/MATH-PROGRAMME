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


def cubic_shadow(xs):
    return {a+b-c for a,b in combinations_with_replacement(sorted(xs),2)
                  for c in xs}


def survivor_graph_edges(xs,R):
    q=pair_sums(xs)
    ds={abs(a-b) for a in q for b in q if a!=b}
    survivors=set(range(1,R+1))-cubic_shadow(xs)
    e=sum(1 for t in survivors for d in ds if t+d in survivors)
    return survivors,e


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


    def test_supersaturation_after_deleting_all_singleton_forbidden_sites(self):
        for n,R in ((5,100),(8,500),(12,1209)):
            p=A[:n]
            q=len(pair_sums(p))
            V,e=survivor_graph_edges(p,R)
            v=len(V)
            self.assertGreaterEqual(v,R//2)
            self.assertGreaterEqual(v*q,6*R)
            exact_lower=(v*v*q*q/(3*R)-v*q)/(2*n)
            strengthened=v*v*q*q/(12*n*R)
            with self.subTest(n=n,R=R):
                self.assertGreaterEqual(e+1e-8,exact_lower)
                self.assertGreaterEqual(e+1e-8,strengthened)
                self.assertGreaterEqual(e+1e-8,n**3*v*v/(48*R))
                self.assertLessEqual(e,comb(v,2))

    def test_supersaturation_for_adversarial_survivor_subsets(self):
        p=[1,2,5,14,33]
        R=100
        V,e=survivor_graph_edges(p,R)
        for retain in (V, {x for x in V if x%2}, {x for x in V if x%3 !=1}):
            m=len(retain)
            if not m:
                continue
            ds=set(pair_diff_profile(p))
            edges=sum(1 for t in retain for d in ds if t+d in retain)
            q=len(pair_sums(p))
            lower=(m*m*q*q/(3*R)-m*q)/(2*len(p))
            self.assertGreaterEqual(edges+1e-8,lower)

    def test_survivor_graph_penalty_beyond_singleton_deletions(self):
        p=[1,2,5,14,33]
        R=100
        V,e=survivor_graph_edges(p,R)
        v=len(V)
        assert v>=R/2
        eps=min(0.25,e/(v*v))
        self.assertGreater(e,0)
        # Exact count among already singleton-legal integral batches.
        ds=set(pair_diff_profile(p))
        for k in (2,3):
            with self.subTest(k=k):
                independent=sum(
                    all(abs(a-b) not in ds for a,b in combinations(t,2))
                    for t in combinations(sorted(V),k))
                self.assertLessEqual(
                    independent,independent_entropy_upper(v,k,eps)+1e-8)

    def test_geometric_protocol_windows_are_disjoint_and_owned(self):
        R=50
        p=[1,2,5,14,33]
        for _ in range(4):
            y=8*R
            J=(15*R,16*R-min(p))
            self.assertGreater(J[0],y)
            self.assertGreater(y,6*R)
            self.assertLessEqual(J[1],16*R)
            self.assertEqual(J[1]-J[0]+1,R-min(p)+1)
            p=p+[y,J[0]]
            self.assertTrue(is_b3(p))
            R*=16
            self.assertLessEqual(max(p),R)


    def test_exact_survivor_clique_obstruction_to_size_four(self):
        p=[1,2,5,14,33]
        R=100
        y=701
        V,e=survivor_graph_edges(p,R)
        self.assertEqual(len(V),65)
        ds=set(pair_diff_profile(p))
        independent_triples=[
            t for t in combinations(sorted(V),3)
            if all(abs(a-b) not in ds for a,b in combinations(t,2))
        ]
        self.assertEqual(len(independent_triples),31)
        # Any independent four-set would contain an independent triple.
        # Search extensions of ONLY these 31 triples rather than all C(65,4).
        for t in independent_triples:
            possible_extensions=[
                z for z in V if z>t[-1] and
                all(abs(z-a) not in ds for a in t)
            ]
            self.assertFalse(possible_extensions)
        witness=(7,49,98)
        self.assertTrue(is_b3(p+[y]+[2*y-t for t in witness]))
        compatible_triples=sum(
            is_b3(p+[y]+[2*y-t for t in T])
            for T in independent_triples
        )
        self.assertEqual(compatible_triples,5)


if __name__=="__main__":
    unittest.main()
