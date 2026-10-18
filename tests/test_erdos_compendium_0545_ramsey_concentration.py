"""Exact small graph Ramsey counterexample for OPEN eventual Erdős #545.

Literal all-m claim fails at m=2; this does NOT disprove an
eventual uniform comparison for all sufficiently large m.
"""
from itertools import combinations
from math import comb
import networkx as nx


def colex(n,t):
    assert n>=2 and 0<=t<n
    G=nx.complete_graph(n)
    if t:
        G.add_node(n)
        G.add_edges_from((n,i) for i in range(t))
    return G


def monochromatic_contains_P3(n,red):
    pairs=tuple(combinations(range(n),2))
    reds={frozenset(e) for e in red}
    for a,b,c in combinations(range(n),3):
        ab=frozenset((a,b));ac=frozenset((a,c));bc=frozenset((b,c))
        for x,y in ((ab,ac),(ab,bc),(ac,bc)):
            if (x in reds)==(y in reds):
                return True
    return False


def monochromatic_contains_2K2(n,red):
    reds={frozenset(e) for e in red}
    for a,b,c,d in combinations(range(n),4):
        for p,q in (((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))):
            if (frozenset(p) in reds)==(frozenset(q) in reds):
                return True
    return False


def all_colorings(n):
    pairs=tuple(combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        yield {pairs[i] for i in range(len(pairs)) if mask&(1<<i)}


def ramsey_predicate(n,pattern):
    return all(pattern(n,red) for red in all_colorings(n))


def test_545_exact_ramsey_p3_is_three():
    assert not ramsey_predicate(2,monochromatic_contains_P3)
    assert ramsey_predicate(3,monochromatic_contains_P3)
    assert colex(2,1).number_of_edges()==2
    assert sorted(d for v,d in colex(2,1).degree())==[1,1,2]


def test_545_exact_ramsey_matching_two_is_five():
    assert not ramsey_predicate(4,monochromatic_contains_2K2)
    assert ramsey_predicate(5,monochromatic_contains_2K2)
    # Independent lower coloring K4: red star and blue K3.
    star={(0,1),(0,2),(0,3)}
    assert not monochromatic_contains_2K2(4,star)
    G=nx.Graph()
    G.add_edges_from(((0,1),(2,3)))
    assert G.number_of_edges()==2
    assert all(d==1 for v,d in G.degree())


def test_545_small_literal_counterexample_and_not_eventual_resolution():
    assert ramsey_predicate(3,monochromatic_contains_P3)
    assert ramsey_predicate(5,monochromatic_contains_2K2)
    assert 5>3
    # Finite m=2 failure contradicts universal all-m comparison,
    # but not the eventual (m>=m0) Erdős-Graham conjecture.


def test_545_colex_edge_count_no_isolates_and_remainder():
    for n in range(2,8):
        for t in range(n):
            G=colex(n,t)
            assert G.number_of_edges()==comb(n,2)+t
            assert all(d>0 for _,d in G.degree())
            assert G.number_of_nodes()==n+(t>0)
            if t:
                assert G.degree(n)==t
                assert sum(G.degree(v) for v in G)==2*(comb(n,2)+t)


def test_545_2_uniform_intersecting_family_upper_on_five_vertices():
    edges=set(map(frozenset,combinations(range(5),2)))
    for k in (5,6):
        for family in combinations(tuple(edges),k):
            assert any(not a.intersection(b) for a,b in combinations(family,2))
    # In particular each color class avoiding 2K2 has <=4 edges;
    # two such classes cannot partition 10 K5 edges.
