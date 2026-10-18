"""Erdos 41: alignment-free collision packing and integrality barrier.

Run: python -m unittest discover -s tests -p 'test_erdos41_alignment_free_integrality.py' -v
All calculations finite and independently cross-checked; the fractional
construction is NOT an infinite B3 set or a solution of Erdős #41.
"""
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement
from math import comb
import unittest

A = [
    1, 2, 5, 14, 33, 72, 125, 219, 376, 573, 745, 1209,
    1557, 2442, 3098, 4048, 5298, 6704, 7839, 10987,
    12332, 15465, 19144, 24546, 28974, 34406, 37769,
    45864, 50877,
]


def is_b3(xs):
    sums=[sum(v) for v in combinations_with_replacement(sorted(xs),3)]
    return len(sums)==len(set(sums))


def irregular_bins(xs, R=100):
    """Greedy disjoint fixed-width intervals; start positions are NOT a grid."""
    remain=list(sorted(xs))
    bins=[]
    while remain:
        b=remain[0]
        picked=[x for x in remain if b<=x<b+R]
        bins.append((b,picked))
        remain=[x for x in remain if x>=b+R]
    return bins


def pattern_weight(m,i,j,k):
    if i==j==k:
        return comb(m[i]+2,3)
    if i==j:
        return comb(m[i]+1,2)*m[k]
    if j==k:
        return m[i]*comb(m[j]+1,2)
    return m[i]*m[j]*m[k]


def candidate_triple_starts(bins):
    starts=[b for b,_ in bins]
    sizes=[len(p) for _,p in bins]
    counts=Counter()
    for i,j,k in combinations_with_replacement(range(len(bins)),3):
        counts[starts[i]+starts[j]+starts[k]]+=pattern_weight(sizes,i,j,k)
    return counts


def actual_triple_start_counts(bins):
    index={}
    for i,(_,block) in enumerate(bins):
        for a in block:
            index[a]=i
    base=[b for b,_ in bins]
    counts=Counter()
    xs=sorted(index)
    for a,b,c in combinations_with_replacement(xs,3):
        i,j,k=index[a],index[b],index[c]
        counts[base[i]+base[j]+base[k]]+=1
    return counts


def pair_difference_budget(bins,R):
    spectra=[]
    for _,block in bins:
        spectra.append({b-a for a,b in combinations(block,2)})
    return spectra, sum(map(len,spectra)),sum(comb(len(v),2) for _,v in bins)


def fractional_profile(N):
    return [0.0]+[0.25*i**(-2/3) for i in range(1,N+1)]


def fractional_expected_triple_sums(p):
    """Correct Bernoulli first moments incl. one reused selected vertex."""
    N=len(p)-1
    pair=[0.]*(2*N+1)
    for a in range(1,N+1):
        for b in range(1,N+1):
            pair[a+b]+=p[a]*p[b]
    triple_ordered=[0.]*(3*N+1)
    for s in range(2,2*N+1):
        for c in range(1,N+1):
            triple_ordered[s+c]+=pair[s]*p[c]

    exactly_two=[0.]*(3*N+1)
    repeated_weighted=[0.]*(3*N+1)
    all_equal=[0.]*(3*N+1)
    for a in range(1,N+1):
        all_equal[3*a]=p[a]
        for b in range(1,N+1):
            if a!=b:
                exactly_two[2*a+b]+=p[a]*p[a]*p[b]
                repeated_weighted[2*a+b]+=p[a]*p[b]
    expected=[0.]*(3*N+1)
    for s in range(3,3*N+1):
        distinct=(triple_ordered[s]-3*exactly_two[s]
                  -(p[s//3]**3 if s%3==0 else 0.))/6
        expected[s]=distinct+repeated_weighted[s]+all_equal[s]
    return expected,triple_ordered


class AlignmentFreeIntegralityTests(unittest.TestCase):
    def test_genuine_fixture_and_irregular_bin_centres(self):
        self.assertTrue(is_b3(A))
        bins=irregular_bins(A,R=100)
        self.assertEqual(sum(len(x) for _,x in bins),len(A))
        self.assertGreater(len(bins),10)
        gaps=[bins[i+1][0]-bins[i][0] for i in range(len(bins)-1)]
        self.assertGreater(len(set(gaps)),3)
        for (a,_),(b,_) in zip(bins,bins[1:]):
            self.assertGreaterEqual(b,a+100)

    def test_moving_window_hall_all_actual_anchor_patterns(self):
        R=100
        bins=irregular_bins(A,R)
        computed=candidate_triple_starts(bins)
        direct=actual_triple_start_counts(bins)
        self.assertEqual(computed,direct)
        self.assertEqual(sum(computed.values()),comb(len(A)+2,3))
        starts=list(computed)
        for D in (0,1,R//2,R,2*R,7*R):
            for S in starts:
                mass=sum(v for start,v in computed.items() if S<=start<=S+D)
                with self.subTest(S=S,D=D):
                    self.assertLessEqual(mass,D+3*R-2)

    def test_global_disjoint_internal_pair_differences(self):
        for R in (20,100,500,1000,5000):
            bins=irregular_bins(A,R)
            spectra,distinct,combinatorial=pair_difference_budget(bins,R)
            self.assertEqual(distinct,combinatorial)
            union=set().union(*spectra)
            self.assertEqual(len(union),distinct)
            self.assertLessEqual(distinct,R-1)
            self.assertTrue(all(1<=h<R for h in union))

    def test_fractional_mass_and_all_integer_difference_caps(self):
        for N in (3,10,100,300):
            p=fractional_profile(N)
            for cutoff in (1,N//2,N):
                if cutoff:
                    self.assertGreaterEqual(
                        sum(p[1:cutoff+1]) + 1e-12,
                        0.25 * cutoff**(1/3))
            for d in range(1,N):
                cap=sum(p[i]*p[i+d] for i in range(1,N-d+1))
                self.assertLessEqual(cap,0.25+1e-12)

    def test_fractional_bernoulli_sum_cap_including_repetitions(self):
        N=160
        p=fractional_profile(N)
        expected,ordered=fractional_expected_triple_sums(p)
        self.assertLess(max(expected),0.6)
        self.assertLess(max(ordered),35/64 + 1e-10)
        self.assertAlmostEqual(expected[3],p[1],places=12)
        self.assertAlmostEqual(expected[4],p[1]*p[2],places=12)
        for s in (3,4,5,6,7,9,12,20,35,50,100,250):
            brute=sum(
                __import__("math").prod(p[x] for x in set((a,b,c)))
                for a,b,c in combinations_with_replacement(range(1,N+1),3)
                if a+b+c==s
            ) if s<=35 else None
            if brute is not None:
                self.assertAlmostEqual(expected[s],brute,places=11)

    def test_disjoint_triple_collision_pairs_exist_abundantly(self):
        N=14
        pool=range(N+1,2*N+1)
        by_sum=defaultdict(list)
        for t in combinations(pool,3):
            by_sum[sum(t)].append(t)
        pairs=[
            (a,b) for triples in by_sum.values()
            for a,b in combinations(triples,2) if set(a).isdisjoint(b)
        ]
        self.assertGreater(len(pairs),N*N)
        probs={x:0.25*x**(-2/3) for x in pool}
        expectation=sum(
            __import__("math").prod(probs[x] for x in a+b)
            for a,b in pairs
        )
        self.assertGreater(expectation,0)
        self.assertLess(sum(probs.values()),N**(1/3))

    def test_fractional_capacity_all_overlapping_windows(self):
        N=120
        p=fractional_profile(N)
        e,_=fractional_expected_triple_sums(p)
        for width in (1,2,7,25,100):
            for start in (3,5,20,90,150,250):
                sums=e[start:start+width]
                self.assertLess(sum(sums),0.6*width+1e-8)
        # The same probabilities are used at every resolution/window.
        # No changing the profile to accommodate a different partition.


if __name__=="__main__":
    unittest.main()
