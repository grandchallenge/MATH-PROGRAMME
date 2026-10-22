"""Erdos #41: exact mixed-colour 3-block resonance and multiscale Hall pressure.

All integer arithmetic exact; repeated summands permitted in global B3.
Cauchy bounds are finite mathematical theorems, not an infinite-density proof.
"""
from collections import Counter
from itertools import combinations,combinations_with_replacement,product
from math import comb
import unittest


def b3(xs):
    sums=[sum(t) for t in combinations_with_replacement(sorted(xs),3)]
    return len(sums)==len(set(sums))


def sixth_defect(xs):
    r=Counter(sum(t) for t in product(xs,repeat=3))
    n=len(xs)
    return sum(v*v for v in r.values())-(6*n**3-9*n*n+4*n)


def rgb(X,Y,Z):
    return Counter(x+y+z for x in X for y in Y for z in Z)


def rgb_defect(X,Y,Z):
    r=rgb(X,Y,Z)
    M=len(X)*len(Y)*len(Z)
    return 36*(sum(v*v for v in r.values())-M)


def kxy(X,Y):
    sums=Counter(x+y for x in X for y in Y)
    assert all(v==1 for v in sums.values()),"X union Y must be B2"
    return Counter({d:sum(1 for q in sums for qq in sums if q-qq==d)
                    for d in {q-qq for q in sums for qq in sums if q>qq}})


def gpos(X):
    return Counter(x-y for x in X for y in X if x>y)


def mixed_resonance(X,Y,Z):
    K=kxy(X,Y)
    G=gpos(Z)
    return 72*sum(v*G[d] for d,v in K.items())


def span(X):
    return max(X)-min(X)


def hall_pressure(X,Y,Z):
    M=len(X)*len(Y)*len(Z)
    S=span(X)+span(Y)+span(Z)+1
    return 36*max(0,M*M/S-M)


def colour_family_info(blocks,family):
    hist=Counter()
    envelopes=[]
    count=0
    for a,b,c in family:
        X,Y,Z=blocks[a],blocks[b],blocks[c]
        hist.update(rgb(X,Y,Z))
        count+=len(X)*len(Y)*len(Z)
        envelopes.append((min(X)+min(Y)+min(Z),
                          max(X)+max(Y)+max(Z)))
    union_envelope=set()
    for lo,hi in envelopes:
        union_envelope.update(range(lo,hi+1))
    return hist,count,len(union_envelope)


def family_pressure(blocks,family):
    _,M,S=colour_family_info(blocks,family)
    return 36*max(0,M*M/S-M)


def base_code(p):
    B=3*p+1
    return [1+i+B*(i*i%p)+B*B*(i*i*i%p) for i in range(p)]


class MultiscaleMixedColourResonanceTests(unittest.TestCase):
    def test_true_pairwise_b3_all_resonances_zero_but_tripartite_collides(self):
        X=[2,18];Y=[20,35];Z=[43,44]
        self.assertTrue(all(b3(S) for S in
                            (X,Y,Z,X+Y,X+Z,Y+Z)))
        self.assertFalse(b3(X+Y+Z))
        self.assertEqual(rgb(X,Y,Z)[81],2)
        self.assertEqual(2+35+44,18+20+43)
        self.assertEqual(rgb_defect(X,Y,Z),72)
        self.assertEqual(mixed_resonance(X,Y,Z),72)
        self.assertEqual(sixth_defect(X+Y+Z),174)
        self.assertGreater(sixth_defect(X+Y+Z),rgb_defect(X,Y,Z))
        self.assertEqual(hall_pressure(X,Y,Z),0)

    def test_tripartite_cauchy_pressure_arbitrary_blocks(self):
        configs=[
            ([2,18],[20,35],[43,44]),
            ([1,2],[10,11],[20,21]),
            ([1,2,3,4],[10,11,12,13],[20,21,22,23]),
            ([1],[5],[15]),
            ([0,1,2,3,4],[7,8,9,10,11],[15,16,17,18,19]),
        ]
        for X,Y,Z in configs:
            with self.subTest(X=X,Y=Y,Z=Z):
                self.assertTrue(set(X).isdisjoint(Y) and
                                set(Y).isdisjoint(Z) and
                                set(X).isdisjoint(Z))
                self.assertGreaterEqual(rgb_defect(X,Y,Z),hall_pressure(X,Y,Z))
                self.assertGreaterEqual(sixth_defect(X+Y+Z),rgb_defect(X,Y,Z))

    def test_mix_correlation_equals_energy_on_pairwise_b3_blocks(self):
        sample=[2,18,20,35,43,44]
        for group_a in combinations(sample,2):
            X=list(group_a)
            remaining=[x for x in sample if x not in X]
            for group_b in combinations(remaining,2):
                Y=list(group_b)
                Z=[x for x in remaining if x not in Y]
                if b3(X+Y):
                    with self.subTest(X=X,Y=Y,Z=Z):
                        self.assertEqual(rgb_defect(X,Y,Z),
                                         mixed_resonance(X,Y,Z))

    def test_independent_translation_of_three_colours_preserves_resonance(self):
        X=[2,18];Y=[20,35];Z=[43,44]
        target=rgb_defect(X,Y,Z)
        for dx,dy,dz in ((0,0,0),(1000,0,2000),(0,10000,-10000),
                         (550,120000,25000)):
            XX=[x+dx for x in X]
            YY=[y+dy for y in Y]
            ZZ=[z+dz for z in Z]
            self.assertTrue(set(XX).isdisjoint(YY) and
                            set(XX).isdisjoint(ZZ) and
                            set(YY).isdisjoint(ZZ))
            self.assertEqual(rgb_defect(XX,YY,ZZ),target)
            self.assertEqual(mixed_resonance(XX,YY,ZZ),target)

    def test_multiscale_family_bound_even_when_multiple_envelopes_overlap(self):
        blocks=[[2,18],[20,35],[43,44],[71,84]]
        indices=list(combinations(range(4),3))
        for mask in range(1,1<<len(indices)):
            family=[t for j,t in enumerate(indices) if mask>>j&1]
            histogram,M,S=colour_family_info(blocks,family)
            exact=36*(sum(v*v for v in histogram.values())-M)
            bound=family_pressure(blocks,family)
            with self.subTest(family=family):
                self.assertGreaterEqual(exact,bound)
                self.assertGreaterEqual(
                    sixth_defect([a for block in blocks for a in block]),exact)

    def test_many_adjacent_critically_populated_blocks_forced_to_collide(self):
        h=8;R=12;m=2
        blocks=[[i*R+1,i*R+2] for i in range(h)]
        M=comb(h,3)*m**3
        S=3*h*R
        self.assertGreater(M,S)
        lo=36*(M*M/S-M)
        family=list(combinations(range(h),3))
        measured=family_pressure(blocks,family)
        whole=[v for b in blocks for v in b]
        self.assertGreater(measured,0)
        self.assertGreaterEqual(measured,lo)
        self.assertGreaterEqual(sixth_defect(whole),measured)
        self.assertFalse(b3(whole))

    def test_genuine_b3_partition_has_no_false_positive_at_any_colour_family(self):
        code=base_code(23)
        self.assertTrue(b3(code))
        W=max(code)
        # Distinct blocks are actual integer translates of DISJOINT
        # elements from the one global B3 code; all 3-sum collisions
        # are separated by the large block-tag spacing.
        blocks=[]
        for i in range(4):
            segment=code[5*i:5*i+5]
            blocks.append([i*(4*W)+x for x in segment])
        total=[v for b in blocks for v in b]
        self.assertTrue(b3(total))
        self.assertEqual(sixth_defect(total),0)
        for family_mask in range(1,1<<4):
            all_types=list(combinations(range(4),3))
            family=[t for j,t in enumerate(all_types) if family_mask>>j&1]
            self.assertEqual(family_pressure(blocks,family),0)

    def test_individual_three_type_pressures_cannot_just_be_summed_across_overlap(self):
        blocks=[[2,18],[20,35],[43,44],[71,84]]
        all_types=list(combinations(range(4),3))
        # Exact per-type energies are disjoint collision families,
        # but family-level overlapping estimates must not be added.
        all_exact=sum(rgb_defect(*[blocks[i] for i in t]) for t in all_types)
        whole=[a for block in blocks for a in block]
        self.assertGreaterEqual(sixth_defect(whole),all_exact)
        self.assertGreaterEqual(
            sixth_defect(whole),family_pressure(blocks,all_types))


if __name__=="__main__":
    unittest.main()
