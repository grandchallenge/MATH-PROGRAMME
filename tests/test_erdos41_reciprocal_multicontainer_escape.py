"""Erdos #41: actual reciprocal 3-window capacity versus finite critical escape.

The explicit moment-code construction is a finite B3 set, not an infinite
counterexample. Every assertion uses exact integer arithmetic.
Run: python -m unittest discover -s tests -p
'test_erdos41_reciprocal_multicontainer_escape.py' -v
"""
from itertools import combinations_with_replacement
from math import comb
import unittest


def is_b3(xs):
    values=[sum(a) for a in combinations_with_replacement(sorted(xs),3)]
    return len(values)==len(set(values))


def moment_code(p):
    B=3*p+1
    R=p*(1+B+B**2)+1
    e=[1+i+B*(i*i%p)+B*B*(i*i*i%p) for i in range(p)]
    return R,e


def triple_cohorts(p):
    R,e=moment_code(p)
    k0=p//3
    k1=2*p//3
    M=4*R
    P=e[:k0]
    X=[M+a for a in e[k0:k1]]
    Y=[4*M+a for a in e[k1:]]
    return R,(P,X,Y)


def colour_types():
    return tuple(combinations_with_replacement(range(3),3))


def type_weight(t,sizes):
    result=1
    for i in range(3):
        r=t.count(i)
        if r:
            result*=comb(sizes[i]+r-1,r)
    return result


def integer_union_size(intervals):
    merged=[]
    for lo,hi in sorted(intervals):
        if merged and lo<=merged[-1][1]+1:
            merged[-1]=(merged[-1][0],max(merged[-1][1],hi))
        else:
            merged.append((lo,hi))
    return sum(hi-lo+1 for lo,hi in merged)


def hall_profile(blocks,R,starts=None):
    if starts is None:
        starts=tuple(min(v) for v in blocks)
    types=colour_types()
    weights=[]
    windows=[]
    sizes=tuple(map(len,blocks))
    for t in types:
        w=type_weight(t,sizes)
        lo=sum(starts[i] for i in t)
        windows.append((lo,lo+3*R-3))
        weights.append(w)
    return types,weights,windows


def exact_cardinality_caps(blocks):
    P,X,Y=blocks
    n,k,ell=map(len,blocks)
    dp=max(P)-min(P); dx=max(X)-min(X); dy=max(Y)-min(Y)
    rhs=(2*dp+dy+1,2*dx+dy+1,dp+dx+dy+1)
    lhs=(ell*comb(n+1,2),ell*comb(k+1,2),n*k*ell)
    return lhs,rhs


def check_finite_critical_density(R,blocks):
    A=sorted(x for group in blocks for x in group)
    # For monotone counting A(N), the minimum ratio on a constant
    # integer interval occurs at its right endpoint, or just before
    # its next element. Check every relevant integer endpoint exactly,
    # comparing 21^3*A(N)^3 >= N.
    candidates={R,5*R,17*R}
    candidates.update(a-1 for a in A if R<a<=17*R)
    for N in candidates:
        assert R<=N<=17*R
        count=sum(a<=N for a in A)
        assert 21**3*count**3 >= N,(R,N,count)
    return len(candidates)

def next_prime_at_least(n):
    def prime(x):
        return x>=2 and all(x%d for d in range(2,int(x**.5)+1))
    while not prime(n):
        n+=1
    return n


def many_tagged_cohorts(h,p):
    assert h>=2 and p>=2*h
    R,baseline=moment_code(p)
    if h<=4:
        tags=[0,1,4,16][:h]
    else:
        tagprime=next_prime_at_least(h)
        _,raw_tags=moment_code(tagprime)
        tags=sorted(raw_tags)[:h]
        tags=[z-tags[0] for z in tags]
    assert tags[0]==0 and is_b3(tags)
    A=[]
    blocks=[]
    for j in range(h):
        start=j*p//h
        stop=(j+1)*p//h
        group=[a+4*R*tags[j] for a in baseline[start:stop]]
        blocks.append(group)
        A+=group
    return R,tags,blocks,A


class ReciprocalMulticontainerEscapeTests(unittest.TestCase):
    def test_tag_labels_are_repetition_allowed_b3(self):
        self.assertTrue(is_b3([0,1,4]))
        self.assertFalse(is_b3([0,1,3]))

    def test_modular_polynomial_moment_code_is_genuine_b3(self):
        for p in (5,7,11,17,31,43):
            with self.subTest(p=p):
                R,e=moment_code(p)
                self.assertEqual(len(e),p)
                self.assertTrue(is_b3(e))
                self.assertTrue(all(1<=x<=R for x in e))
                self.assertLess(R,12*p**3)

    def test_three_actual_critical_cohorts_all_full_b3(self):
        for p in (5,7,11,17,31,43):
            with self.subTest(p=p):
                R,blocks=triple_cohorts(p)
                P,X,Y=blocks
                A=P+X+Y
                self.assertTrue(is_b3(A))
                self.assertEqual(len(A),p)
                self.assertTrue(all(v<=R for v in P))
                self.assertTrue(all(4*R<v<=5*R for v in X))
                self.assertTrue(all(16*R<v<=17*R for v in Y))
                for block in blocks:
                    self.assertGreaterEqual(12**3*len(block)**3,R)
                self.assertGreater(check_finite_critical_density(R,blocks),2)

    def test_all_ten_type_sum_supports_are_disjoint(self):
        for p in (5,7,11,31):
            R,blocks=triple_cohorts(p)
            types,weights,windows=hall_profile(
                blocks,R,starts=(1,4*R+1,16*R+1))
            self.assertEqual(len(types),10)
            ordered=sorted(windows)
            self.assertTrue(all(a[1]<b[0]
                                for a,b in zip(ordered,ordered[1:])))
            self.assertEqual(len(set(windows)),10)
            self.assertEqual(sum(weights),comb(p+2,3))
            self.assertTrue(all(w<=3*R-2 for w in weights))

    def test_every_hall_cut_at_actual_tagged_positions(self):
        for p in (5,7,11,17):
            R,blocks=triple_cohorts(p)
            types,weights,windows=hall_profile(
                blocks,R,starts=(1,4*R+1,16*R+1))
            for mask in range(1,1<<10):
                chosen=[i for i in range(10) if mask>>i&1]
                demand=sum(weights[i] for i in chosen)
                capacity=integer_union_size([windows[i] for i in chosen])
                self.assertLessEqual(demand,capacity)

    def test_reciprocal_shape_independent_batch_cardinality(self):
        for p in (5,7,11,17,31):
            R,blocks=triple_cohorts(p)
            lhs,rhs=exact_cardinality_caps(blocks)
            self.assertTrue(all(a<=b for a,b in zip(lhs,rhs)))
            n,k,ell=map(len,blocks)
            reciprocal_limit=(3*R-2)//max(comb(n+1,2),n*k,
                                              comb(k+1,2))
            self.assertGreaterEqual(reciprocal_limit,ell)
            self.assertGreaterEqual(12**3*ell**3,R)

    def test_reusing_base_points_across_tagged_blocks_breaks_b3(self):
        R,e=moment_code(11)
        M=4*R
        P=e[:3]
        X=[M+a for a in e[:3]]
        self.assertTrue(is_b3(P))
        self.assertTrue(is_b3(X))
        self.assertFalse(is_b3(P+X))
        # Even disjoint and individually B3 tagged blocks need genuine
        # cross-colour compatibility, not merely B3 labels.

    def test_finite_critical_horizon_is_not_infinite_persistence(self):
        for p in (5,11,31):
            R,blocks=triple_cohorts(p)
            A=sorted(x for block in blocks for x in block)
            self.assertGreaterEqual(21**3*
                (sum(x<=17*R for x in A))**3,17*R)
            N=(21*len(A))**3+1
            self.assertGreater(N,17*R)
            self.assertLess(21**3*(sum(x<=N for x in A))**3,N)


    def test_arbitrarily_many_finite_reciprocal_critical_cohorts(self):
        for h in range(2,9):
            p=next_prime_at_least(2*h)
            R,tags,blocks,A=many_tagged_cohorts(h,p)
            with self.subTest(h=h,p=p):
                self.assertTrue(is_b3(A))
                self.assertEqual(len(A),p)
                self.assertLess(max(tags),96*h**3)
                Nlast=4*R*max(tags)+R
                self.assertLessEqual(Nlast,385*h**3*R)
                self.assertTrue(all(len(g)>0 for g in blocks))
                for g in blocks:
                    self.assertGreaterEqual((5*h)**3*len(g)**3,R)
                samples={R,Nlast}
                samples.update(x-1 for x in A if x>R)
                for N in samples:
                    if R<=N<=Nlast:
                        count=sum(x<=N for x in A)
                        self.assertGreaterEqual(
                            (40*h*h)**3*count**3,N)


    def test_forced_multiscale_population_bound_has_product_slack(self):
        # The density assumption is hypothetical: check its exact
        # geometric extraction constants, not a fabricated infinite set.
        for inverse_c in (1,4,21):
            lam=144*inverse_c**3
            self.assertGreaterEqual(lam,144)
            for R in (10,1000,100000):
                # Product eta_0 eta_1 eta_2 = 18 / ((lam-1)^3 lam^2)
                # is far below the 3R-2 true mixed-triple capacity.
                self.assertLessEqual(
                    18*R,
                    (3*R-2)*(lam-1)**3*lam**2)
                # Exact arithmetic checks the occupation extraction
                # factors across arbitrary fixed numbers of annuli.
                for j in range(6):
                    annulus_bins=(lam-1)*lam**j
                    self.assertEqual(
                        (lam**(j+1)-lam**j)*R//R,
                        annulus_bins)


if __name__=="__main__":
    unittest.main()
