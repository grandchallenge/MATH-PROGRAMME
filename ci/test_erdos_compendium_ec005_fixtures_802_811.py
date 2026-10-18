"""EC-BULK-005 Erdős 802-811, exact finite fixtures, not theorem certificates."""
import itertools
import math
from collections import Counter
from collections import deque
import unittest

def independent(V, E):
    vertices=set(V)
    return all(not ({a,b} <= vertices) for a,b in E)

def clique(V,E):
    edge_set={frozenset(e) for e in E}
    return all(frozenset(pair) in edge_set for pair in itertools.combinations(V,2))

def alpha(V,E):
    return max(len(C) for k in range(len(V)+1) for C in itertools.combinations(V,k)
               if independent(C,E))

def omega(V,E):
    return max(len(C) for k in range(len(V)+1) for C in itertools.combinations(V,k)
               if clique(C,E))

def induced_edges(V,E):
    selected=set(V)
    return [edge for edge in E if set(edge)<=selected]

def balanced_graph(degree,D):
    if not degree or min(degree)==0:
        return False
    return max(degree)<=D*min(degree)

def min_biclique_edge_partition(V,E):
    V=tuple(V)
    all_edges={frozenset(e) for e in E}
    list_edges=list(all_edges)
    index={e:i for i,e in enumerate(list_edges)}
    candidate_masks=set()
    for assign in itertools.product((0,1,2),repeat=len(V)):
        left={v for v,c in zip(V,assign) if c==1}
        right={v for v,c in zip(V,assign) if c==2}
        if not left or not right:continue
        cross={frozenset((a,b)) for a in left for b in right}
        if cross<=all_edges:
            candidate_masks.add(sum(1<<index[e] for e in cross))
    target=(1<<len(list_edges))-1
    q=deque([(0,0)]);seen={0}
    while q:
        used,k=q.popleft()
        if used==target:return k
        for sub in candidate_masks:
            if used&sub:continue
            nxt=used|sub
            if nxt not in seen:
                seen.add(nxt);q.append((nxt,k+1))
    return None

def restricted_sets(A,E):
    A=set(A)
    assert all(u in A and v in A and u!=v for u,v in E)
    return ({u+v for u,v in E},{u*v for u,v in E})

def all_cycle4_edge_sets(V,E):
    S={frozenset(e) for e in E}
    seen=set()
    for vertices in itertools.combinations(V,4):
        for order in itertools.permutations(vertices[1:]):
            route=(vertices[0],)+order
            cycle=frozenset(frozenset((route[i],route[(i+1)%4])) for i in range(4))
            if len(cycle)==4 and cycle<=S:
                seen.add(cycle)
    return seen

def every_cycle4_rainbow(V,E,colors):
    return all(len({colors[e] for e in cyc})==4 for cyc in all_cycle4_edge_sets(V,E))

class Tranche802To811(unittest.TestCase):
    def test_802_triangle_free_cycle5_independence(self):
        V=tuple(range(5))
        E={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertEqual(alpha(V,E),2)
        self.assertEqual(omega(V,E),2)
        self.assertEqual(sum(2*1 for _ in E)/5,2)
        self.assertFalse(clique((0,1,2),E))

    def test_803_degree_balance_uses_positive_minimum(self):
        self.assertTrue(balanced_graph((2,2,2),1))
        self.assertTrue(balanced_graph((3,1,1,1),3))
        self.assertFalse(balanced_graph((3,1,1,1),2))
        self.assertFalse(balanced_graph((3,1,1,0),100))

    def test_804_induced_vs_global_independence(self):
        V=tuple(range(4))
        complete=[(a,b) for a,b in itertools.combinations(V,2)]
        self.assertEqual(alpha(V,complete),1)
        self.assertEqual(alpha(V,()),4)
        self.assertTrue(all(alpha(S,())==2 for S in itertools.combinations(V,2)))
        self.assertTrue(all(alpha(S,complete)==1 for S in itertools.combinations(V,2)))

    def test_805_every_three_vertices_of_cycle5_have_both_pairs(self):
        V=tuple(range(5))
        E={frozenset((i,(i+1)%5)) for i in range(5)}
        for S in itertools.combinations(V,3):
            self.assertGreaterEqual(alpha(S,induced_edges(S,E)),2)
            self.assertGreaterEqual(omega(S,induced_edges(S,E)),2)
        self.assertFalse(all(omega(S,())>=2 for S in itertools.combinations(V,3)))

    def test_806_twofold_sumset_with_repetition(self):
        A={2,4,6}
        B={1,3}
        self.assertLessEqual(len(A),math.isqrt(9))
        self.assertTrue(A<={a+b for a in B for b in B})
        self.assertEqual({a+b for a,b in itertools.combinations(B,2)},{4})

    def test_807_biclique_exact_edge_partition_k4(self):
        V=tuple(range(4))
        E=list(itertools.combinations(V,2))
        self.assertEqual(alpha(V,E),1)
        self.assertEqual(min_biclique_edge_partition(V,E),3)
        path=[(0,1),(1,2),(2,3)]
        self.assertLessEqual(min_biclique_edge_partition(V,path),3)

    def test_808_restricted_vs_all_sum_product(self):
        A={1,2,3,4}
        E={(1,2),(1,3),(2,4)}
        sums,products=restricted_sets(A,E)
        self.assertEqual(sums,{3,4,6})
        self.assertEqual(products,{2,3,8})
        self.assertLess(len(sums),len({a+b for a in A for b in A}))
        self.assertLess(len(products),len({a*b for a in A for b in A}))

    def test_809_above_mantel_threshold_always_triangle_n4(self):
        V=tuple(range(4))
        full=list(itertools.combinations(V,2))
        target=math.floor(len(V)**2/4)+1
        self.assertEqual(target,5)
        for E in itertools.combinations(full,target):
            self.assertTrue(any(clique(S,E) for S in itertools.combinations(V,3)))
        self.assertNotEqual(2*3+1,2*4+1) # C7 and C9 are distinct cases

    def test_810_rainbow_c4_vs_repeated_color(self):
        V=tuple(range(4))
        E=[(0,1),(1,2),(2,3),(0,3)]
        color={frozenset(e):i for i,e in enumerate(E)}
        self.assertEqual(len(all_cycle4_edge_sets(V,E)),1)
        self.assertTrue(every_cycle4_rainbow(V,E,color))
        color[frozenset(E[3])]=color[frozenset(E[0])]
        self.assertFalse(every_cycle4_rainbow(V,E,color))

    def test_811_cyclic_distance_balanced_k7_three_colors(self):
        V=tuple(range(7))
        E=list(itertools.combinations(V,2))
        colors={frozenset((i,j)):min((j-i)%7,(i-j)%7) for i,j in E}
        self.assertEqual(set(colors.values()),{1,2,3})
        for v in V:
            deg=Counter(colors[frozenset((v,u))] for u in V if u!=v)
            self.assertEqual(deg,{1:2,2:2,3:2})
        self.assertEqual([colors[frozenset(e)] for e in ((0,1),(1,3),(0,3))],[1,2,3])

if __name__=="__main__":
    unittest.main()
