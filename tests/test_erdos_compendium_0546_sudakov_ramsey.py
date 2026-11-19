"""Exact finite Ramsey and hypothesis checks for PROVED Erdős #546.

The general inequality R(G) <= 2^(250 sqrt(m)) is Sudakov's
2011 theorem, not established by these small enumerations.
"""
from itertools import combinations
from math import comb
import networkx as nx


def contains_subgraph_direct(host,pattern):
    from itertools import permutations
    V=tuple(host.nodes)
    P=tuple(pattern.nodes)
    if len(P)>len(V):
        return False
    E=tuple(pattern.edges)
    for image in permutations(V,len(P)):
        mapping=dict(zip(P,image))
        if all(host.has_edge(mapping[a],mapping[b]) for a,b in E):
            return True
    return False


def contains_subgraph_matcher(host,pattern):
    return nx.algorithms.isomorphism.GraphMatcher(host,pattern).subgraph_is_monomorphic()


def all_colorings(N):
    pairs=tuple(combinations(range(N),2))
    for mask in range(1<<len(pairs)):
        red=nx.Graph()
        blue=nx.Graph()
        red.add_nodes_from(range(N));blue.add_nodes_from(range(N))
        for i,e in enumerate(pairs):
            (red if mask&(1<<i) else blue).add_edge(*e)
        yield red,blue


def r_predicate(N,P,method):
    return all(method(a,P) or method(b,P) for a,b in all_colorings(N))


def patterns():
    return {
        'K2':nx.complete_graph(2),
        'P3':nx.path_graph(3),
        '2K2':nx.disjoint_union(nx.complete_graph(2),nx.complete_graph(2)),
        'K3':nx.complete_graph(3)
    }


def test_546_small_exact_ramsey_direct_and_matcher():
    expected={'K2':2,'P3':3,'2K2':5,'K3':6}
    P=patterns()
    for name,r in expected.items():
        assert not r_predicate(r-1,P[name],contains_subgraph_direct)
        assert r_predicate(r,P[name],contains_subgraph_direct)
    for name in ('K2','P3','2K2'):
        r=expected[name]
        assert not r_predicate(r-1,P[name],contains_subgraph_matcher)
        assert r_predicate(r,P[name],contains_subgraph_matcher)


def test_546_finite_subgraph_embedding_algorithms_agree():
    for G in nx.graph_atlas_g():
        if G.number_of_nodes()>5:continue
        for H in patterns().values():
            assert contains_subgraph_direct(G,H)==contains_subgraph_matcher(G,H)


def test_546_no_isolates_implies_n_le_twom():
    for G in nx.graph_atlas_g():
        n,m=G.number_of_nodes(),G.number_of_edges()
        if not n or not m:continue
        H=G.copy()
        H.remove_nodes_from(list(nx.isolates(H)))
        assert H.number_of_nodes()<=2*H.number_of_edges()
        assert sum(dict(H.degree()).values())==2*H.number_of_edges()


def test_546_isolated_vertices_make_fixed_m_unbounded():
    for q in (1,2,5,15,80):
        G=nx.Graph()
        G.add_nodes_from(range(q+2))
        G.add_edge(0,1)
        assert G.number_of_edges()==1
        assert len(list(nx.isolates(G)))==q
        assert G.number_of_nodes()==q+2
        # Any (non-induced) G embedding needs at least q+2 vertices.
        # R(G) is thus unbounded as q grows with m fixed.


# CI uses unittest discovery. Preserve the original bounded witness functions
# while explicitly exposing each as a standard unittest test method.
import unittest

class CompendiumWitnessTests(unittest.TestCase):
    def test_546_small_exact_ramsey_direct_and_matcher(self):
        test_546_small_exact_ramsey_direct_and_matcher()

    def test_546_finite_subgraph_embedding_algorithms_agree(self):
        test_546_finite_subgraph_embedding_algorithms_agree()

    def test_546_no_isolates_implies_n_le_twom(self):
        test_546_no_isolates_implies_n_le_twom()

    def test_546_isolated_vertices_make_fixed_m_unbounded(self):
        test_546_isolated_vertices_make_fixed_m_unbounded()
