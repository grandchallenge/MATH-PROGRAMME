"""Erdos #41: coupled PPZ graph, PZZ hypergraph and new-block B3 tests.

Repeated summands are allowed. Finite results only; not a c-persistent
density contradiction or independent mathematical certification.
"""
from collections import Counter,defaultdict
from itertools import combinations,combinations_with_replacement,product
import unittest


def b3(seq):
    words=[sum(t) for t in combinations_with_replacement(sorted(seq),3)]
    return len(words)==len(set(words))


def pair_sums(seq):
    return {a+b for a,b in combinations_with_replacement(sorted(seq),2)}


def differences(seq):
    seq=sorted(set(seq))
    return {b-a for a,b in combinations(seq,2)}


def ppz_free(P,Z):
    return differences(Z).isdisjoint(differences(pair_sums(P)))


def pzz_free(P,Z):
    return differences(P).isdisjoint(differences(pair_sums(Z)))


def exact_sixth_defect(seq):
    r=Counter(sum(t) for t in product(seq,repeat=3))
    n=len(seq)
    return sum(v*v for v in r.values())-(6*n**3-9*n*n+4*n)


def graph_edges(P,J):
    excluded=differences(pair_sums(P))
    return {frozenset((a,b)) for a,b in combinations(J,2)
            if b-a in excluded}


def pzz_hyperedges(P,J):
    delta=differences(P)
    pairs=list(combinations_with_replacement(sorted(J),2))
    out=set()
    for i in range(len(pairs)):
        a,b=pairs[i]
        for c,d in pairs[i+1:]:
            if abs((a+b)-(c+d)) in delta:
                out.add(frozenset((a,b,c,d)))
    return out


def new_b3_hyperedges(J):
    hist=defaultdict(list)
    for tup in combinations_with_replacement(sorted(J),3):
        hist[sum(tup)].append(tup)
    out=set()
    for tuples in hist.values():
        for left,right in combinations(tuples,2):
            out.add(frozenset(left+right))
    return out


def hypergraph_free(Z,edges):
    selected=set(Z)
    return not any(edge<=selected for edge in edges)


def gap_transition_ok(P,Z):
    ds=differences(pair_sums(P))
    dp=differences(P)
    s=sorted(Z)
    for a,b in combinations(s,2):
        if b-a in ds:
            return False
    gaps=[b-a for a,b in zip(s,s[1:])]
    for a,b in zip(gaps,gaps[1:]):
        if abs(a-b) in dp or a==b:
            return False
    return True


def lower_span(k):
    n=max(k-1,0)
    return 8*(n//2)+3*(n%2)


class CoupledGapHypergraphTests(unittest.TestCase):
    def setUp(self):
        self.P=[1,2]
        self.J=list(range(100,108))

    def test_old_difference_spectra_and_exact_channel_witnesses(self):
        P=self.P
        self.assertTrue(b3(P))
        self.assertEqual(pair_sums(P),{2,3,4})
        self.assertEqual(differences(P),{1})
        self.assertEqual(differences(pair_sums(P)),{1,2})
        z_ppz=[100,103,107]
        z_pzz=[100,102,107]
        self.assertTrue(b3(z_ppz) and b3(z_pzz))
        self.assertTrue(ppz_free(P,z_ppz))
        self.assertFalse(pzz_free(P,z_ppz))
        self.assertEqual(2+103+103,1+100+107)
        self.assertTrue(pzz_free(P,z_pzz))
        self.assertFalse(ppz_free(P,z_pzz))
        self.assertEqual(1+1+102,2+2+100)

    def test_joint_capacity_strictly_below_both_separate_capacities(self):
        P,J=self.P,self.J
        out=[]
        for k in range(5):
            ps=[];zs=[];both=[];union=[]
            for Z in combinations(J,k):
                if b3(Z) and ppz_free(P,Z):
                    ps.append(Z)
                if b3(Z) and pzz_free(P,Z):
                    zs.append(Z)
                if b3(Z) and ppz_free(P,Z) and pzz_free(P,Z):
                    both.append(Z)
                if b3(P+list(Z)):
                    union.append(Z)
            out.append((len(ps),len(zs),len(both),len(union)))
            self.assertEqual(both,union)
        self.assertEqual(out[3],(2,2,0,0))
        self.assertEqual(out[4],(0,0,0,0))
        self.assertTrue(out[2][-1]>0)
        self.assertEqual(max(k for k,row in enumerate(out) if row[0]),3)
        self.assertEqual(max(k for k,row in enumerate(out) if row[1]),3)
        self.assertEqual(max(k for k,row in enumerate(out) if row[2]),2)

    def test_all_three_point_gap_configurations_obstructed(self):
        for Z in combinations(self.J,3):
            x,y,z=Z
            a=y-x
            b=z-y
            if a>=3 and b>=3:
                self.assertIn((a,b),((3,3),(3,4),(4,3)))
                if a==b:
                    self.assertFalse(b3(Z))
                else:
                    self.assertIn(abs(a-b),differences(self.P))
                    self.assertFalse(pzz_free(self.P,Z))
            else:
                self.assertFalse(ppz_free(self.P,Z))
            self.assertFalse(b3(self.P+list(Z)))

    def test_exact_defect_minimum_is_eighteen(self):
        values=[(exact_sixth_defect(self.P+list(Z)),Z)
                for Z in combinations(self.J,3)]
        self.assertEqual(min(v for v,_ in values),18)
        self.assertIn((18,(100,102,107)),values)
        self.assertTrue(all(v>=18 for v,_ in values))
        for Z in combinations(self.J,4):
            self.assertGreaterEqual(
                exact_sixth_defect(self.P+list(Z)),18)

    def test_universal_adjacent_old_pair_short_window_exclusion(self):
        prefixes=[[1,2],[1,2,5,14],[10,11,14,23]]
        for P in prefixes:
            self.assertTrue(b3(P))
            self.assertTrue({1,2}<=differences(pair_sums(P)))
            self.assertIn(1,differences(P))
            J=range(200,208)
            for Z in combinations(J,3):
                with self.subTest(P=P,Z=Z):
                    self.assertFalse(b3(P+list(Z)))

    def test_nine_position_sharpness_of_local_exclusion(self):
        P=[1,2]
        Z=[100,103,108]
        self.assertEqual(max(Z)-min(Z),8)
        self.assertTrue(b3(Z))
        self.assertTrue(ppz_free(P,Z))
        self.assertTrue(pzz_free(P,Z))
        self.assertTrue(b3(P+Z))

    def test_gap_transition_necessary_for_genuine_B3(self):
        code=[1,2,5,14,33,72,125,219]
        self.assertTrue(b3(code))
        P=code[:2]
        for k in range(2,len(code)-1):
            Z=code[2:k+2]
            self.assertTrue(b3(P+Z))
            self.assertTrue(gap_transition_ok(P,Z))
            self.assertGreaterEqual(max(Z)-min(Z),lower_span(len(Z)))

    def test_gap_span_lower_bound_is_locally_sharp(self):
        for k in range(1,14):
            gap_seq=[3 if i%2==0 else 5 for i in range(k-1)]
            Z=[100]
            for gap in gap_seq:
                Z.append(Z[-1]+gap)
            self.assertEqual(Z[-1]-Z[0],lower_span(k))
            self.assertTrue(gap_transition_ok(self.P,Z))
            # Only the LOCAL graph/gap conditions are asserted.
            # The full B3 condition is intentionally not claimed.

    def test_hypergraph_encoding_is_exact_for_both_channels(self):
        P=self.P
        J=self.J
        graph=graph_edges(P,J)
        z_hyper=pzz_hyperedges(P,J)
        b_hyper=new_b3_hyperedges(J)
        self.assertTrue(all(len(edge)==2 for edge in graph))
        self.assertTrue(all(2<=len(edge)<=4 for edge in z_hyper))
        self.assertTrue(all(2<=len(edge)<=6 for edge in b_hyper))
        for k in range(0,len(J)+1):
            for Z in combinations(J,k):
                with self.subTest(Z=Z):
                    self.assertEqual(hypergraph_free(Z,graph),ppz_free(P,Z))
                    self.assertEqual(hypergraph_free(Z,z_hyper),pzz_free(P,Z))
                    self.assertEqual(hypergraph_free(Z,b_hyper),b3(Z))
                    both=(hypergraph_free(Z,graph)
                          and hypergraph_free(Z,z_hyper)
                          and hypergraph_free(Z,b_hyper))
                    self.assertEqual(both,b3(P+list(Z)))

    def test_farfield_equivalence_for_varied_genuine_B3_prefixes(self):
        Pchoices=[[1,2],[1,2,5,14],[1,3,9]]
        for P in Pchoices:
            if not b3(P):
                continue
            L=1000
            J=list(range(L,L+10))
            for k in range(0,5):
                for Z in combinations(J,k):
                    with self.subTest(P=P,Z=Z):
                        self.assertEqual(b3(P+list(Z)),
                                         b3(Z) and ppz_free(P,Z)
                                         and pzz_free(P,Z))


if __name__=="__main__":
    unittest.main()
