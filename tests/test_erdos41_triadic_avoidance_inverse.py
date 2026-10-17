"""Exact triadic arithmetic-avoidance certificates for Erdős #41.

Research-only: proves finite B2/B3 weighted gap-triangle bounds, not
the unresolved persistent-density or multiscale deduction.
Run: python -m unittest discover -s tests -p 'test_erdos41_triadic_avoidance_inverse.py' -v
"""
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement
from math import comb, prod
from fractions import Fraction
import unittest

A = [
    1, 2, 5, 14, 33, 72, 125, 219, 376, 573, 745,
    1209, 1557, 2442, 3098, 4048, 5298, 6704, 7839,
    10987, 12332, 15465, 19144, 24546, 28974,
    34406, 37769, 45864, 50877,
]


def is_b2(xs):
    sums = [sum(t) for t in combinations_with_replacement(xs, 2)]
    return len(sums) == len(set(sums))


def is_b3(xs):
    sums = [sum(t) for t in combinations_with_replacement(xs, 3)]
    return len(sums) == len(set(sums))


def pair_sums(u):
    return {a+b for a,b in combinations_with_replacement(sorted(u), 2)}


def half_difference_weights(u, L):
    # Sparse exact pair-sum difference counting. Scaling the source by a
    # large modulus must not create an O(L*|P|) verification bottleneck.
    p=pair_sums(u)
    result=Counter()
    for a in p:
        for b in p:
            if a>b and (a-b)%2==0:
                h=(a-b)//2
                if h<=L:
                    result[h]+=1
    return result


def weighted_correlation(r, w):
    return sum(r[b-a] for a,b in combinations(sorted(w), 2))


def triangle_candidates(r, L):
    return sorted(
        (r[a]+r[b]+r[a+b],a,b)
        for a in range(1, L)
        for b in range(1, L-a+1)
        if a != b
    )


def triadic_certificate(u, w, threshold=1):
    assert len(w)>=3 and is_b2(w)
    L=max(w)-min(w)
    r=half_difference_weights(u,L)
    observed=weighted_correlation(r,w)
    m=len(w)
    candidates=triangle_candidates(r,L)
    k=comb(m,3)
    assert len(candidates)>=k
    bound_numerator=sum(x[0] for x in candidates[:k])
    good=sum(1 for cost,a,b in candidates if
             r[a]<threshold and r[b]<threshold and r[a+b]<threshold)
    threshold_lower=max(0,threshold*(k-good))
    return r,observed,bound_numerator,threshold_lower,candidates


def three_bin_certificate(u,Y,Z,V,Q):
    assert max(Y)<min(Z)<max(V) and max(Z)<min(V)
    assert is_b2(Y+Z+V)
    low_a,min_hi_a=min(Z)-max(Y),max(Z)-min(Y)
    low_b,min_hi_b=min(V)-max(Z),max(V)-min(Z)
    low_sum,high_sum=min(V)-max(Y),max(V)-min(Y)
    r=half_difference_weights(u, high_sum)
    weight_candidates=defaultdict(list)
    for a in range(low_a,min_hi_a+1):
        for b in range(low_b,min_hi_b+1):
            if a==b or not low_sum<=a+b<=high_sum:
                continue
            weight_candidates[(a%Q,b%Q)].append(
                r[a]+r[b]+r[a+b]
            )
    occupancy=Counter(
        ((z-y)%Q,(v-z)%Q)
        for y in Y for z in Z for v in V
    )
    bound=0
    zero_capacity={}
    for cls,k in occupancy.items():
        weights=sorted(weight_candidates[cls])
        assert len(weights)>=k
        bound+=sum(weights[:k])
        zero_capacity[cls]=sum(value==0 for value in weights)
    observed=sum(
        r[z-y]+r[v-z]+r[v-y]
        for y in Y for z in Z for v in V
    )
    myz=sum(r[z-y] for y in Y for z in Z)
    mzv=sum(r[v-z] for z in Z for v in V)
    myv=sum(r[v-y] for y in Y for v in V)
    assert observed==len(V)*myz+len(Y)*mzv+len(Z)*myv
    return observed,bound,occupancy,zero_capacity,(myz,mzv,myv)


def prime_residue_budget(u,Y,Z,primes,threshold=1):
    """Exact-cube verification of the robust localized Cauchy-Davenport gate.

    The budget B has an irrational cube root, so test (positive part)^3
    <= B^3 using Fraction, without floating point.
    """
    assert min(Z)>max(Y) and is_b3(Y+Z)
    dy=max(Y)-min(Y)
    dz=max(Z)-min(Z)
    Q=prod(primes)
    assert Q<=min(dy,dz)
    assert len(set(primes))==len(primes)
    assert all(p>1 and all(p%d for d in range(2,int(p**.5)+1))
               for p in primes)
    lo=min(Z)-max(Y)
    hi=max(Z)-min(Y)
    r=half_difference_weights(u,hi)
    observed=sum(r[z-y] for y in Y for z in Z)
    prod_caps=Fraction(1,1)
    evidence={}
    for p in primes:
        e=len({h%p for h in range(lo,hi+1) if r[h]<threshold})
        c=Fraction(e+1,2) if e<p else Fraction(p,1)
        evidence[p]=(e,p,c)
        prod_caps*=c*c
    # Cube of ((144 dy dz / Q²)^(1/3) prod c_p²).
    Bcubed=Fraction(144*dy*dz,Q*Q)*prod_caps**3
    m=len(Y)*len(Z)
    x=max(Fraction(0),Fraction(m)-
          Fraction(observed*max(len(Y),len(Z)),threshold))
    assert x**3<=Bcubed
    return observed,x,Bcubed,evidence


def exact_residue_biclique_capacity(Q, allowed):
    """Brute exact maximum |S||T| when T-S is contained in allowed."""
    assert Q>=1
    E={e%Q for e in allowed}
    shifts=[]
    for s in range(Q):
        shifts.append(sum(1<<((s+e)%Q) for e in E))
    all_bits=(1<<Q)-1
    common=[all_bits]*(1<<Q)
    optimum=0
    for mask in range(1,1<<Q):
        bit=mask & -mask
        i=bit.bit_length()-1
        common[mask]=common[mask ^ bit] & shifts[i]
        optimum=max(optimum,mask.bit_count()*common[mask].bit_count())
    return optimum


def composite_residue_budget(u,Y,Z,Q,threshold=1):
    """Verify the exact cube form of the composite arithmetic gate."""
    assert min(Z)>max(Y) and is_b3(Y+Z)
    dy=max(Y)-min(Y)
    dz=max(Z)-min(Z)
    assert 1<=Q<=min(dy,dz)
    lo=min(Z)-max(Y)
    hi=max(Z)-min(Y)
    r=half_difference_weights(u,hi)
    E={h%Q for h in range(lo,hi+1) if r[h]<threshold}
    beta=exact_residue_biclique_capacity(Q,E)
    observed=sum(r[z-y] for y in Y for z in Z)
    Bcube=Fraction(144*dy*dz,Q*Q)*beta**3
    discrepancy=max(Fraction(0),Fraction(len(Y)*len(Z))
                    -Fraction(observed*max(len(Y),len(Z)),threshold))
    assert discrepancy**3<=Bcube
    return observed,discrepancy,Bcube,beta,E


class TriadicAvoidanceTests(unittest.TestCase):
    def test_b3_fixture(self):
        self.assertEqual(len(A),29)
        self.assertTrue(is_b3(A))
        self.assertTrue(is_b2(A))

    def test_triangle_weight_identity_for_sidons(self):
        fixtures = (
            ([1,2,5],[20,23,28]),
            (A[:3],A[3:6]),
            (A[:10],A[10:13]),
            (A[:10],A[10:14]),
            (A[:12],A[12:15]),
        )
        for u,w in fixtures:
            with self.subTest(u=u,w=w):
                self.assertTrue(is_b2(w))
                r,observed,numerator,threshold_lower,candidates=triadic_certificate(
                    u,w,1)
                m=len(w)
                cost_sum=sum(
                    r[y-x]+r[z-y]+r[z-x]
                    for x,y,z in combinations(sorted(w),3))
                self.assertEqual(cost_sum,(m-2)*observed)
                self.assertLessEqual(numerator,(m-2)*observed)
                self.assertLessEqual(threshold_lower,(m-2)*observed)
                self.assertGreaterEqual(len(candidates),comb(m,3))

    def test_pair_capacity_passes_but_triadic_rejects_zero(self):
        u=[1,2,5]
        w=[20,23,28]
        r,observed,numerator,threshold_lower,candidates=triadic_certificate(
            u,w,1)
        self.assertTrue(is_b3(u))
        self.assertTrue(is_b2(w))
        self.assertEqual(max(w)-min(w),8)
        self.assertEqual(observed,1)
        self.assertGreaterEqual(numerator,1)
        self.assertGreaterEqual(threshold_lower,1)
        # If the window expands to span ten, the pairwise Q=1
        # capacity still permits three B2-independent centers.
        L=10
        r=half_difference_weights(u,L)
        zeros=[h for h in range(1,L+1) if r[h]==0]
        self.assertEqual(zeros,[5,6,7,8,9,10])
        self.assertGreaterEqual(2*len(zeros),3*2)
        self.assertEqual(len([1 for a,b in ((a,b) for a in zeros
                                           for b in zeros)
                              if a != b and a+b<=L]),0)
        self.assertEqual(len(pair_sums(u))*3,18)
        self.assertEqual(2*(max(u)-min(u))+L+1,19)

    def test_non_b2_graph_independent_three_term_progression(self):
        u=[1,2,5]; w=[20,25,30]
        self.assertFalse(is_b2(w))
        r=half_difference_weights(u,10)
        self.assertEqual(weighted_correlation(r,w),0)
        self.assertEqual((w[1]-w[0],w[2]-w[1]),(5,5))
        # The theorem forbids equal adjacent gaps; no false application.

    def test_three_bin_oriented_zero_with_genuine_b3(self):
        u=A[:3]
        Y,Z,V=A[3:5],A[5:7],A[7:9]
        self.assertTrue(is_b3(u+Y+Z+V))
        for Q in (1,2,3,5,7,13,500):
            with self.subTest(Q=Q):
                observed,bound,K,Zcap,pair_energies=three_bin_certificate(
                    u,Y,Z,V,Q)
                self.assertEqual(observed,0)
                self.assertEqual(bound,0)
                self.assertEqual(sum(K.values()),len(Y)*len(Z)*len(V))
                self.assertTrue(all(K[c]<=Zcap[c] for c in K))
                self.assertEqual(pair_energies,(0,0,0))

    def test_three_bin_positive_real_b3(self):
        u=A[:10]
        Y,Z,V=A[10:11],A[11:12],A[12:13]
        self.assertTrue(is_b3(u+Y+Z+V))
        for Q in (1,2,3,7,500):
            with self.subTest(Q=Q):
                observed,bound,K,Zcap,energies=three_bin_certificate(
                    u,Y,Z,V,Q)
                self.assertEqual(observed,1)
                self.assertLessEqual(bound,observed)
                self.assertEqual(sum(K.values()),1)
                self.assertEqual(observed,sum(energies))

    def test_three_bin_positive_two_midpoints(self):
        # Both triples have positive genuine correlations (2 and 1).
        u=A[:14]
        Y,Z,V=A[14:15],A[15:17],A[17:18]
        self.assertTrue(is_b3(u+Y+Z+V))
        for Q in (1,2,5):
            with self.subTest(Q=Q):
                observed,bound,K,Zcap,energies=three_bin_certificate(
                    u,Y,Z,V,Q)
                self.assertGreater(observed,0)
                self.assertLessEqual(bound,observed)
                self.assertEqual(sum(K.values()),2)

    def test_threshold_counts_nonnegative_and_bounded(self):
        u=[1,2,5]
        for w in ([20,23,28],[20,24,29],[20,26,33]):
            if not is_b2(w):
                continue
            for threshold in (1,2,3):
                with self.subTest(w=w,threshold=threshold):
                    r,observed,weighted,unscaled,_=triadic_certificate(
                        u,w,threshold)
                    self.assertGreaterEqual((len(w)-2)*observed,unscaled)


    def test_robust_prime_crt_budget_on_actual_b3_bins(self):
        # Explicitly distinguish a correct but often vacuous bound from
        # the missing universal prime-residue deficiency lemma.
        fixtures=(
            (A[:3],A[3:5],A[5:7],(2,3)),
            (A[:10],A[10:12],A[12:14],(2,3)),
            (A[:14],A[14:16],A[16:18],(2,3,5)),
            (A[:16],A[16:18],A[18:20],(2,3,5,7)),
        )
        for u,Y,Z,proposed in fixtures:
            for threshold in (1,2,3):
                for primes in ((2,), (3,), (2,3), proposed):
                    if prod(primes)>min(Y[-1]-Y[0],Z[-1]-Z[0]):
                        continue
                    with self.subTest(n=len(u),Y=Y,Z=Z,
                                      primes=primes,threshold=threshold):
                        M,x,Bcube,e=prime_residue_budget(
                            u,Y,Z,primes,threshold)
                        self.assertGreaterEqual(M,0)
                        self.assertGreaterEqual(Bcube,x**3)
                        self.assertTrue(all(0<=v[0]<=v[1]
                                            for v in e.values()))

    def test_prime_residue_support_structural_control(self):
        # With a dense enough allowed difference interval, every small
        # prime is represented, explaining why the CRT bound can be
        # vacuous despite genuine B3 persistent-window aspirations.
        u=A[:3]
        Y,Z=A[3:5],A[5:7]
        M,x,Bcube,e=prime_residue_budget(u,Y,Z,(2,3),1)
        self.assertEqual(M,0)
        self.assertEqual(e[2][0],2)
        self.assertEqual(e[3][0],3)
        self.assertGreaterEqual(Bcube,Fraction(len(Y)*len(Z))**3)

    def test_prime_residue_critical_density_cost_algebra(self):
        # The CRT cube form comes directly from the cubic shadow
        # and is independently replayed against genuine finite B3.
        for n in (5,8,14,20):
            x=A[:n]
            D=x[-1]-x[0]
            for primes in ((2,3),(2,3,5),(3,5,7)):
                Q=prod(primes)
                if Q>D:
                    continue
                tQ=len({v%Q for v in x})
                with self.subTest(n=n,primes=primes):
                    self.assertLessEqual(n**3*Q,12*D*tQ**3)


    def test_prime_residue_deficiency_gives_positive_finite_bound(self):
        # Separate-carrier control: U and W are each exact B3, but their
        # UNION is not B3. The theorem uses their separate B3 properties.
        # This checks a genuinely positive numerical certificate.
        u=[1,2,5,14,33]
        Y,Z=[100,102],[105,114]
        self.assertTrue(is_b3(u))
        self.assertTrue(is_b3(Y+Z))
        self.assertFalse(is_b3(u+Y+Z))
        M,x,Bcube,e=prime_residue_budget(u,Y,Z,(2,),1)
        self.assertEqual(M,12)
        self.assertEqual(e[2][0],0)
        self.assertEqual(Bcube,Fraction(81,8))
        self.assertLess(Bcube,Fraction(len(Y)*len(Z))**3)
        self.assertGreater(M,0)


    def test_composite_strictly_improves_prime_projection_capacity(self):
        u=[1,2,5,14]
        Y,Z=[100,106],[108,115]
        self.assertTrue(is_b3(u))
        self.assertTrue(is_b3(Y+Z))
        self.assertFalse(is_b3(u+Y+Z))
        M,x,Bcube,beta,E=composite_residue_budget(u,Y,Z,6,1)
        self.assertEqual(E,{2,3,4})
        self.assertEqual(beta,4)
        self.assertEqual({d%2 for d in E},{0,1})
        self.assertEqual({d%3 for d in E},{0,1,2})
        self.assertLess(beta,6**2)
        self.assertEqual(M,6)
        self.assertEqual(Bcube,Fraction(144*6*7,6**2)*4**3)
        self.assertLessEqual(x**3,Bcube)

    def test_composite_gate_on_actual_joint_b3_carriers(self):
        fixtures=(
            (A[:3],A[3:5],A[5:7],(2,3,6)),
            (A[:10],A[10:12],A[12:14],(2,3,6,10)),
            (A[:14],A[14:16],A[16:18],(2,3,6,10,12)),
        )
        for u,Y,Z,moduli in fixtures:
            self.assertTrue(is_b3(u+Y+Z))
            for Q in moduli:
                if Q>min(Y[-1]-Y[0],Z[-1]-Z[0]):
                    continue
                for threshold in (1,2,3):
                    with self.subTest(n=len(u),Q=Q,t=threshold):
                        M,x,Bcube,beta,E=composite_residue_budget(
                            u,Y,Z,Q,threshold)
                        self.assertGreaterEqual(M,0)
                        self.assertGreaterEqual(Bcube,x**3)
                        self.assertLessEqual(beta,Q**2)
                        self.assertLessEqual(len(E),Q)

    def test_composite_capacity_on_small_all_and_empty_difference_sets(self):
        for Q in (1,2,3,4,5,6,7,8):
            self.assertEqual(exact_residue_biclique_capacity(
                Q,range(Q)),Q*Q)
            self.assertEqual(exact_residue_biclique_capacity(Q,()),0)
        self.assertEqual(exact_residue_biclique_capacity(
            6,{2,3,4}),4)


    def test_joint_b3_digit_lift_has_zero_overlap_and_full_small_residues(self):
        # Genuine 29-point B3 countercontrol: all outer center differences
        # are q-multiples, yet the zero-correlation distances meet EVERY
        # residue mod 2,3,6,12 in long narrow-bin candidate intervals.
        q=151
        digits=[0,11,42,43]
        u=[q*a+digits[i//3] for i,a in enumerate(A[:12])]
        w=[q*a for a in A[12:]]
        self.assertTrue(is_b3(u+w))
        r=half_difference_weights(u,max(w)-min(w))
        self.assertEqual(weighted_correlation(r,w),0)
        Y,Z=w[:3],w[3:6]
        for Q in (2,3,6,12):
            with self.subTest(Q=Q):
                M,x,Bcube,beta,E=composite_residue_budget(u,Y,Z,Q,1)
                self.assertEqual(M,0)
                self.assertEqual(E,set(range(Q)))
                self.assertEqual(beta,Q*Q)
                self.assertGreaterEqual(Bcube,Fraction(len(Y)*len(Z))**3)


    def test_fixed_modulus_panel_escape_by_genuine_b3_dilation(self):
        # Concrete finite universal no-go for any fixed residue panel.
        # Scaling preserves B3 and zero complete correlation but dilutes
        # normalized finite density by k^(-1/3).
        u=A[:8]
        w=A[8:]
        Y,Z=w[:2],w[2:4]
        self.assertTrue(is_b3(u+w))
        q=len(pair_sums(u))
        Q0=12
        H=(max(Y)-min(Y))+(max(Z)-min(Z))
        k=(Q0*(q*(q-1)//2+1)-1+H-1)//H
        self.assertGreaterEqual(k*H+1,Q0*(q*(q-1)//2+1))
        scaled_u=[k*x for x in u]
        scaled_w=[k*x for x in w]
        scaled_Y=[k*x for x in Y]
        scaled_Z=[k*x for x in Z]
        self.assertTrue(is_b3(scaled_u+scaled_w))
        r=half_difference_weights(scaled_u,max(scaled_w)-min(scaled_w))
        self.assertEqual(weighted_correlation(r,scaled_w),0)
        for Q in range(1,Q0+1):
            with self.subTest(Q=Q):
                M,x,Bcube,beta,E=composite_residue_budget(
                    scaled_u,scaled_Y,scaled_Z,Q,1)
                self.assertEqual(M,0)
                self.assertEqual(E,set(range(Q)))
                self.assertEqual(beta,Q*Q)


if __name__ == "__main__":
    unittest.main()
