"""Exact lag correlation: true B3 fixtures and forbidden fake-log arithmetic."""
from collections import Counter
from itertools import combinations_with_replacement as pairs
from random import Random
import unittest

A29 = (1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
       3098,4048,5298,6704,7839,10987,12332,15465,
       19144,24546,28974,34406,37769,45864,50877)


def is_b3(A):
    s=[sum(t) for t in pairs(A,3)]
    return len(s)==len(set(s))


def pair_sums(X):
    return {a+b for a,b in pairs(X,2)}


def fiber(X,Y):
    return Counter(p-2*y for p in pair_sums(X) for y in Y)


def cross_difference(P,Q):
    return Counter(p-q for p in P for q in Q)


def outer_difference(Y):
    return Counter(a-b for a in Y for b in Y)


def exact_overlap(P,Q,Y):
    cross=cross_difference(P,Q)
    r=outer_difference(Y)
    return sum(cross[2*h]*mult for h,mult in r.items())


class CrossScaleOverlapEnergyTests(unittest.TestCase):
    def test_genuine_B3_exact_overlap_and_self_excess(self):
        self.assertTrue(is_b3(A29))
        rng=Random(593)
        for width in (1,2,3,4,5,6):
            for k in (2,3,4):
                A=list(A29)
                rng.shuffle(A)
                inner=[tuple(A[i*width:(i+1)*width]) for i in range(k)]
                Y=tuple(A[k*width:])
                if any(not X for X in inner) or not Y:continue
                assert len(set(a for X in inner for a in X))==k*width
                fs=[fiber(X,Y) for X in inner]
                ps=[pair_sums(X) for X in inner]
                for i,fi in enumerate(fs):
                    qi=len(ps[i])
                    self.assertEqual(sum(fi.values()),qi*len(Y))
                    energy=sum(c*c for c in fi.values())
                    expected=exact_overlap(ps[i],ps[i],Y)
                    self.assertEqual(energy,expected)
                    self.assertEqual(energy-qi*len(Y),
                                     sum(c*(c-1) for c in fi.values()))
                    self.assertEqual(
                        energy-qi*len(Y),
                        sum(cross_difference(ps[i],ps[i])[2*h]*r
                            for h,r in outer_difference(Y).items() if h))
                for i in range(k):
                    for j in range(i+1,k):
                        actual=sum(v*fs[j][d] for d,v in fs[i].items())
                        self.assertEqual(actual,exact_overlap(ps[i],ps[j],Y))
                        self.assertTrue(ps[i].isdisjoint(ps[j]))
                        self.assertEqual(
                            actual,
                            sum(cross_difference(ps[i],ps[j])[2*h]*r
                                for h,r in outer_difference(Y).items() if h))

    def test_exact_energy_pressure_and_partition_budget(self):
        for k in (2,3,4,5):
            Xs=[A29[3*i:3*i+3] for i in range(k)]
            Y=A29[3*k:]
            fs=[fiber(X,Y) for X in Xs]
            ps=[pair_sums(X) for X in Xs]
            S=sum((f for f in fs), Counter())
            T=sum(S.values())
            total=sum(v*v for v in S.values())
            E=sum(sum(v*v for v in fi.values()) for fi in fs)
            overlap=sum(sum(v*fs[j][d] for d,v in fs[i].items())
                        for i in range(k) for j in range(i+1,k))
            self.assertEqual(total-E,2*overlap)
            H=max(A29)
            L=2*H
            self.assertTrue(all(-L<=d<=-1 for d in S))
            self.assertGreaterEqual(L*total,T*T)
            self.assertGreaterEqual(2*overlap*L,T*T-L*E)
            self.assertEqual(T,len(Y)*sum(len(P) for P in ps))
            n=sum(map(len,Xs))
            self.assertLessEqual(T,len(Y)*n*(n+1)//2)

    def test_genuine_B3_zero_and_nonzero_cross_scale_overlap(self):
        self.assertTrue(is_b3(A29))
        for k,expected in ((2,0),(3,0),(4,1),(5,0)):
            Xs=[A29[3*i:3*i+3] for i in range(k)]
            Y=A29[3*k:]
            fs=[fiber(X,Y) for X in Xs]
            overlaps=sum(sum(f[d]*fs[j][d] for d in f)
                         for i,f in enumerate(fs)
                         for j in range(i+1,len(fs)))
            self.assertEqual(overlaps,expected)
        Xs=[A29[:3],A29[3:6]];Y=A29[6:]
        f,g=[fiber(X,Y) for X in Xs]
        self.assertEqual(len(f),138)
        self.assertEqual(len(g),138)
        self.assertFalse(set(f)&set(g))

    def test_cross_same_center_exclusion_requires_B2(self):
        X0=(1,2);X1=(0,3);Y=(20,25)
        self.assertFalse(is_b3(X0+X1+Y))
        P0=pair_sums(X0);P1=pair_sums(X1)
        self.assertIn(3,P0&P1)
        h0=len(Y)*len(P0&P1)
        self.assertGreater(h0,0)
        overlap=exact_overlap(P0,P1,Y)
        self.assertGreaterEqual(overlap,h0)
        self.assertEqual(
            h0, sum(cross_difference(P0,P1)[2*h]*r
                    for h,r in outer_difference(Y).items() if h==0))

    def test_cross_pair_difference_support_matching_and_y_sidon(self):
        self.assertTrue(is_b3(A29))
        for n_i,n_j in ((2,3),(3,4),(5,5),(8,10),(14,15)):
            X=A29[:n_i]
            Z=A29[n_i:n_i+n_j]
            Y=A29[n_i+n_j:]
            if not Y:continue
            Pi=pair_sums(X);Pj=pair_sums(Z)
            diff=Counter()
            grouped={}
            pi_repr={a+b:(a,b) for a,b in pairs(X,2)}
            pj_repr={a+b:(a,b) for a,b in pairs(Z,2)}
            for p in Pi:
                for q in Pj:
                    t=p-q
                    diff[t]+=1
                    grouped.setdefault(t,[]).append((pi_repr[p],pj_repr[q]))
            for t,reps in grouped.items():
                self.assertLessEqual(len(reps),min(n_i,n_j))
                supports_pos=[set(z[0]) for z in reps]
                supports_neg=[set(z[1]) for z in reps]
                self.assertEqual(len(set().union(*supports_pos)),
                                 sum(len(z) for z in supports_pos))
                self.assertEqual(len(set().union(*supports_neg)),
                                 sum(len(z) for z in supports_neg))
            dY=outer_difference(Y)
            self.assertTrue(all(v==1 for d,v in dY.items() if d))
            cross=exact_overlap(Pi,Pj,Y)
            self.assertEqual(cross,sum(diff[2*d] for d in dY if d))
            self.assertLessEqual(cross,len(Y)*(len(Y)-1)*min(n_i,n_j))

    def test_many_scales_never_create_more_one_color_positive_pairs(self):
        A=A29[:24]
        n=len(A)
        rng=Random(470)
        for k in (1,2,3,4,6,8,12,24):
            B=list(A);rng.shuffle(B)
            Xi=[B[j::k] for j in range(k)]
            demand=sum(len(pair_sums(X)) for X in Xi)
            expected=sum(len(X)*(len(X)+1)//2 for X in Xi)
            self.assertEqual(demand,expected)
            self.assertLessEqual(demand,n*(n+1)//2)
            self.assertEqual(n*(n+1)//2-demand,
                             sum(len(Xi[i])*len(Xi[j])
                                 for i in range(k) for j in range(i+1,k)))

    def test_no_forced_cross_overlap_even_with_two_distant_b3_blocks(self):
        A=A29
        X=A[:3];Z=A[3:6];Y=A[6:]
        self.assertTrue(is_b3(A))
        self.assertLess(max(X),min(Y))
        self.assertLess(max(Z),min(Y))
        self.assertEqual(exact_overlap(pair_sums(X),pair_sums(Z),Y),0)


if __name__=="__main__":
    unittest.main()
