"""Erdos #41 exact integer-residue capacity and sixth-moment forcing tests.

Repetition-permitted B3 only; all tests use exact integer / rational
arithmetic. No infinite density-valley claim. Research candidate #2789.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import floor
import random
import unittest


def is_b3(values):
    seq=sorted(values)
    triples=[sum(t) for t in combinations_with_replacement(seq,3)]
    return len(triples)==len(set(triples))


def d6(values):
    reps=Counter(sum(t) for t in product(values,repeat=3))
    n=len(values)
    return sum(v*v for v in reps.values())-(6*n**3-9*n*n+4*n)


def mixed_reps(X,Y,Z):
    return Counter(x+y+z for x in X for y in Y for z in Z)


def mixed_defect(X,Y,Z):
    counts=mixed_reps(X,Y,Z)
    M=len(X)*len(Y)*len(Z)
    return 36*(sum(v*v for v in counts.values())-M)


def cross_Q(X,Y):
    Q={x+y for x in X for y in Y}
    assert len(Q)==len(X)*len(Y), "Require B2 X∪Y"
    return sorted(Q)


def merge_intervals(intervals):
    output=[]
    for lo,hi in sorted(intervals):
        assert lo<=hi
        if output and lo<=output[-1][1]+1:
            output[-1]=(output[-1][0],max(output[-1][1],hi))
        else:
            output.append((lo,hi))
    return output


def support_intervals(Q,J):
    lo,hi=J
    return merge_intervals((q+lo,q+hi) for q in Q)


def residue_interval_capacity(intervals,h):
    out=[0]*h
    for lo,hi in merge_intervals(intervals):
        for t in range(h):
            out[t]+=(hi-t)//h-(lo-1-t)//h
    return tuple(out)


def residue_histogram(xs,h):
    out=[0]*h
    for x in xs:
        out[x%h]+=1
    return tuple(out)


def modular_demand(Q,Z,h):
    q=residue_histogram(Q,h)
    z=residue_histogram(Z,h)
    return tuple(sum(q[r]*z[(t-r)%h] for r in range(h))
                 for t in range(h))


def modular_lower_bound(Q,Z,J,h):
    capacities=residue_interval_capacity(support_intervals(Q,J),h)
    load=modular_demand(Q,Z,h)
    out=Fraction(0)
    for n,c in zip(load,capacities):
        assert c or not n
        if c:
            out+=max(Fraction(0),Fraction(n*n,c)-n)
    return 36*out


def integral_capacity(Q,J,h):
    old=residue_histogram(Q,h)
    capacities=residue_interval_capacity(support_intervals(Q,J),h)
    per_residue=residue_interval_capacity([J],h)
    best=0
    for alloc in product(*(range(n+1) for n in per_residue)):
        demand=[sum(old[r]*alloc[(t-r)%h] for r in range(h))
                for t in range(h)]
        if all(demand[t]<=capacities[t] for t in range(h)):
            best=max(best,sum(alloc))
    return best


def moment_code(p):
    B=3*p+1
    return [1+i+B*(i*i%p)+B*B*(i*i*i%p) for i in range(p)]


def multisupport_pressure(blocks,types,h):
    intervals=[]
    loads=Counter()
    for i,j,k in types:
        assert i<j<k
        Q={x+y for x in blocks[i] for y in blocks[j]}
        J=(min(blocks[k]),max(blocks[k]))
        intervals.extend((q+J[0],q+J[1]) for q in Q)
        loads.update(x+y+z for x in blocks[i] for y in blocks[j]
                     for z in blocks[k])
    C=residue_interval_capacity(merge_intervals(intervals),h)
    N=[0]*h
    for total,multiplicity in loads.items():
        N[total%h]+=multiplicity
    return 36*sum((max(Fraction(0),Fraction(n*n,c)-n)
                   if c else Fraction(0))
                  for n,c in zip(N,C))


class IntegralModularResonanceTests(unittest.TestCase):
    def setUp(self):
        self.X=[1,2]
        self.Y=[1000,1003]
        self.Z=[10000,10004]
        self.J=(10000,10004)
        self.Q=cross_Q(self.X,self.Y)

    def test_cross_pair_sum_gaps_and_window_support_exact(self):
        self.assertTrue(is_b3(self.X+self.Y))
        self.assertEqual(self.Q,[1001,1002,1004,1005])
        intervals=support_intervals(self.Q,self.J)
        self.assertEqual(intervals,[(11001,11009)])
        W=self.J[1]-self.J[0]+1
        gap_formula=W+sum(min(W,b-a) for a,b in
                          zip(self.Q[:-1],self.Q[1:]))
        self.assertEqual(gap_formula,9)
        self.assertEqual(sum(hi-lo+1 for lo,hi in intervals),gap_formula)

    def test_pairwise_compatible_hostile_triple_collision(self):
        X,Y,Z=self.X,self.Y,self.Z
        self.assertTrue(all(is_b3(a+b) for a,b in
                            ((X,Y),(X,Z),(Y,Z))))
        self.assertFalse(is_b3(X+Y+Z))
        self.assertEqual(1+1000+10004,2+1003+10000)
        self.assertEqual(mixed_reps(X,Y,Z)[11005],2)
        self.assertEqual(mixed_defect(X,Y,Z),72)
        self.assertEqual(d6(X+Y+Z),72)

    def test_modulus_three_forces_batch_cardinality_one(self):
        self.assertEqual(len(self.Q)*2,8)
        self.assertEqual(sum(hi-lo+1 for lo,hi in
                             support_intervals(self.Q,self.J)),9)
        self.assertEqual(residue_histogram(self.Q,3),(2,0,2))
        self.assertEqual(residue_interval_capacity(
            support_intervals(self.Q,self.J),3),(3,3,3))
        self.assertEqual(integral_capacity(self.Q,self.J,1),2)
        self.assertEqual(integral_capacity(self.Q,self.J,3),1)
        self.assertEqual(modular_demand(self.Q,self.Z,3),(2,4,2))
        self.assertEqual(modular_lower_bound(
            self.Q,self.Z,self.J,1),0)
        self.assertEqual(modular_lower_bound(
            self.Q,self.Z,self.J,3),48)

    def test_fractional_occupancy_can_fake_two_points_but_integrality_cannot(self):
        # Actual window histogram is (1,2,2); the fractional choice
        # (2/3,2/3,2/3) fits every linear modular capacity.
        # Nonetheless every INTEGER occupancy vector of mass two fails.
        h=3
        a=residue_histogram(self.Q,h)
        C=residue_interval_capacity(support_intervals(self.Q,self.J),h)
        Jcap=residue_interval_capacity([self.J],h)
        v=(Fraction(2,3),)*3
        self.assertEqual(Jcap,(1,2,2))
        self.assertEqual(sum(v),2)
        self.assertTrue(all(v[t]<=Jcap[t] for t in range(h)))
        loads=[sum(a[r]*v[(t-r)%h] for r in range(h))
               for t in range(h)]
        self.assertEqual(loads,[Fraction(8,3)]*3)
        self.assertTrue(all(loads[t]<=C[t] for t in range(h)))
        self.assertEqual(integral_capacity(self.Q,self.J,h),1)

    def test_every_two_element_window_batch_is_incompatible(self):
        for Z in combinations(range(self.J[0],self.J[1]+1),2):
            self.assertFalse(is_b3(self.X+self.Y+list(Z)))
            self.assertTrue(any(
                n>c for n,c in zip(
                    modular_demand(self.Q,Z,3),
                    residue_interval_capacity(
                        support_intervals(self.Q,self.J),3))))

    def test_genuine_coded_b3_blocks_satisfy_modular_bounds(self):
        code=moment_code(17)
        self.assertTrue(is_b3(code))
        blocks=[code[:5],code[5:10],code[10:15]]
        X,Y,Z=blocks
        self.assertTrue(is_b3(X+Y+Z))
        Q=cross_Q(X,Y)
        J=(min(Z),max(Z))
        for h in (1,2,3,4,5,7,11,13):
            with self.subTest(h=h):
                C=residue_interval_capacity(support_intervals(Q,J),h)
                N=modular_demand(Q,Z,h)
                self.assertTrue(all(n<=c for n,c in zip(N,C)))
                self.assertEqual(modular_lower_bound(Q,Z,J,h),0)

    def test_exact_modular_lower_bounds_cannot_exceed_collision_ledger(self):
        random.seed(20261022)
        X=self.X
        Y=self.Y
        Q=self.Q
        for _ in range(100):
            Z=random.sample(range(9995,10012),2)
            J=(min(Z),max(Z))
            true=mixed_defect(X,Y,Z)
            for h in (1,2,3,4,5,7,11):
                with self.subTest(Z=tuple(Z),h=h):
                    self.assertLessEqual(
                        modular_lower_bound(Q,Z,J,h),true)

    def test_multicolour_modular_energy_is_bounded_by_global_defect(self):
        blocks=[
            [1,2],[1000,1003],[10000,10004],
            [25000,25006],
        ]
        total=[a for block in blocks for a in block]
        types=list(combinations(range(4),3))
        for mask in range(1,1<<len(types)):
            selected=[t for k,t in enumerate(types) if mask>>k&1]
            for h in (1,2,3,5,7):
                self.assertLessEqual(
                    multisupport_pressure(blocks,selected,h),d6(total))

    def test_multicolour_positive_pressure_in_known_hostile_set(self):
        blocks=[self.X,self.Y,self.Z]
        self.assertEqual(
            multisupport_pressure(blocks,[(0,1,2)],1),0)
        self.assertEqual(
            multisupport_pressure(blocks,[(0,1,2)],3),48)
        self.assertEqual(d6(self.X+self.Y+self.Z),72)

    def test_translation_invariance_of_capacity_and_modular_defect(self):
        Q=self.Q
        J=self.J
        for shift in (-100000,-333,-3,0,15,100001):
            shifted=[q+shift for q in Q]
            j2=(J[0]-shift,J[1]-shift)
            # Sums Q+J unchanged, but Q and J residue histograms
            # shift oppositely; the exact certificate is unchanged.
            self.assertEqual(
                support_intervals(shifted,j2),
                support_intervals(Q,J))
            Z=[z-shift for z in self.Z]
            for h in (1,3,5):
                self.assertEqual(
                    modular_lower_bound(shifted,Z,j2,h),
                    modular_lower_bound(Q,self.Z,J,h))
                self.assertEqual(
                    integral_capacity(shifted,j2,h),
                    integral_capacity(Q,J,h))


if __name__=="__main__":
    unittest.main()
