"""Infinite geometric-shell occupancy profile: exact countermodel to coarse
three-DISTINCT-colour interval-Hall inference, not an infinite B3 set.
"""
from itertools import combinations,combinations_with_replacement
from math import comb
import random
import unittest


def radii_and_masses(K,h):
    assert K>=5
    return [( (16*K)**3*64**j,K*4**j) for j in range(h)]


def interval_union_count(intervals):
    merged=[]
    for lo,hi in sorted(intervals):
        if merged and lo<=merged[-1][1]+1:
            merged[-1]=(merged[-1][0],max(merged[-1][1],hi))
        else:
            merged.append((lo,hi))
    return sum(hi-lo+1 for lo,hi in merged)


def hall_envelope_cut(Rm,family):
    R=[r for r,m in Rm]
    m=[m for r,m in Rm]
    demand=0
    intervals=[]
    for i,j,k in family:
        assert i<j<k
        demand+=m[i]*m[j]*m[k]
        rsum=R[i]+R[j]+R[k]
        intervals.append((rsum+3,2*rsum))
    return demand,interval_union_count(intervals)


def prime_at_least(n):
    def prime(x):
        if x<2:return False
        d=2
        while d*d<=x:
            if x%d==0:return False
            d+=1
        return True
    x=n
    while not prime(x):
        x+=1
    return x


def moment_code(p):
    B=3*p+1
    W=p*(1+B+B*B)+1
    return W,[1+i+B*(i*i%p)+B*B*(i*i*i%p) for i in range(p)]


def b3(xs):
    sums=[a+b+c for a,b,c in combinations_with_replacement(sorted(xs),3)]
    return len(sums)==len(set(sums))


def make_shell_B3(K,j):
    R,m=radii_and_masses(K,j+1)[j]
    p=prime_at_least(m)
    W,alphabet=moment_code(p)
    assert p<=2*m
    assert W<96*m**3 < R
    shell=[R+x for x in alphabet[:m]]
    return R,m,shell


class GeometricShellHallNoGoTests(unittest.TestCase):
    def test_true_single_shell_B3_codes_at_critical_local_order(self):
        for K,j in ((5,0),(5,1),(5,2),(6,0),(6,1),(7,2)):
            R,m,B=make_shell_B3(K,j)
            with self.subTest(K=K,j=j):
                self.assertEqual(len(set(B)),m)
                self.assertTrue(all(R<v<=2*R for v in B))
                self.assertEqual(16**3*m**3,R)
                self.assertTrue(b3(B))

    def test_cumulative_lower_density_at_all_scale_transition_extrema(self):
        for K in (5,7,11):
            rows=radii_and_masses(K,9)
            for j in range(1,8):
                R=rows[j][0]
                upper=rows[j+1][0]
                oldmass=sum(m for r,m in rows[:j])
                self.assertGreaterEqual(256**3*oldmass**3,upper)
                self.assertEqual(rows[j][1],K*4**j)
                # Even before the current block becomes populated,
                # the previous block already supplies positive lower density.
                self.assertGreaterEqual(oldmass,rows[j-1][1])
                self.assertTrue(2*rows[j-1][0]<R)

    def test_each_max_index_aggregate_demand_below_common_core(self):
        for K in (5,7):
            rows=radii_and_masses(K,12)
            for k in range(2,len(rows)):
                R,m=rows[k]
                M=sum(rows[i][1]*rows[j][1]*m
                      for i,j in combinations(range(k),2))
                core=R-2*rows[k-1][0]-2
                self.assertGreater(core,R//2)
                self.assertLess(M,R/73728)
                self.assertLess(M,core)

    def test_every_family_cut_on_five_geometric_windows(self):
        for K in (5,11):
            Rm=radii_and_masses(K,5)
            types=list(combinations(range(5),3))
            for mask in range(1,1<<len(types)):
                family=[t for j,t in enumerate(types) if mask>>j & 1]
                demand,capacity=hall_envelope_cut(Rm,family)
                self.assertLessEqual(demand,capacity)

    def test_irregular_multiscale_support_union_all_sampled_cuts(self):
        rng=random.Random(20261021)
        for K in (5,7):
            for h in (6,8,10):
                rows=radii_and_masses(K,h)
                types=list(combinations(range(h),3))
                samples=[[t] for t in types]+[types]
                for _ in range(400):
                    chosen=[t for t in types if rng.randrange(4)==0]
                    if chosen:samples.append(chosen)
                for family in samples:
                    demand,capacity=hall_envelope_cut(rows,family)
                    self.assertLessEqual(demand,capacity)

    def test_disjoint_envelopes_with_different_max_color_index(self):
        rows=radii_and_masses(5,8)
        for k in range(2,7):
            upper_k=max(2*sum(rows[i][0] for i in tup)
                        for tup in combinations(range(k+1),3)
                        if max(tup)==k)
            lower_next=min(sum(rows[i][0] for i in tup)+3
                           for tup in combinations(range(k+2),3)
                           if max(tup)==k+1)
            self.assertLess(upper_k,lower_next)

    def test_an_individually_valid_B3_shell_collection_is_not_certified_global(self):
        rows=[]
        for j in (0,1,2):
            _,_,block=make_shell_B3(5,j)
            rows.append(block)
        # A triple-window envelope count passing does not imply
        # a full B3 certificate for the union. No such claim is made.
        family=[(0,1,2)]
        demand,capacity=hall_envelope_cut(radii_and_masses(5,3),family)
        self.assertLess(demand,capacity)
        self.assertTrue(all(b3(block) for block in rows))
        self.assertTrue(all(set(rows[i]).isdisjoint(rows[j])
                            for i in range(3) for j in range(i+1,3)))


if __name__=="__main__":
    unittest.main()
