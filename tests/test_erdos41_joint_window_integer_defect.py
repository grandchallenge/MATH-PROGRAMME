"""Erdos #41: joint-window integer sixth-defect forcing.

All triple sums are with repeated summands permitted. Integer-residue
optimization is exact on bounded finite instances. No infinite B3
positive-density conclusion or independent mathematical certification.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import random
import unittest


def b3(xs):
    t=[sum(x) for x in combinations_with_replacement(sorted(xs),3)]
    return len(t)==len(set(t))


def d6(xs):
    r=Counter(sum(x) for x in product(xs,repeat=3))
    n=len(xs)
    return sum(v*v for v in r.values())-(6*n**3-9*n*n+4*n)


def qxy(X,Y):
    q={x+y for x in X for y in Y}
    assert len(q)==len(X)*len(Y)  # X union Y has B2
    return q


def support(Q,windows):
    return {q+v for q in Q
            for L,U in windows
            for v in range(L,U+1)}


def hist(values,h):
    out=[0]*h
    for x in values:
        out[x%h]+=1
    return tuple(out)


def phi(N,C):
    assert N>=0 and C>=0
    if C==0:
        if N==0:return 0
        raise ValueError("nonempty load with zero actual support")
    a,b=divmod(N,C)
    return C*a*(a-1)+2*a*b


def integer_energy_bound(load,capacity):
    return 36*sum(phi(n,c) for n,c in zip(load,capacity))


def loads(Q,Z,h):
    q=hist(Q,h)
    z=hist(Z,h)
    return tuple(sum(q[r]*z[(t-r)%h] for r in range(h))
                 for t in range(h))


def charge(Q,Z,windows,h):
    C=hist(support(Q,windows),h)
    return integer_energy_bound(loads(Q,Z,h),C)


def mixed_energy(Q,Z):
    r=Counter(q+z for q in Q for z in Z)
    return 36*(sum(v*v for v in r.values())-len(Q)*len(Z))


def joint_capacity(Q,windows,h,required):
    """Exact bounded integer optimization using sparse residue allocations.

    Enumerate only occupied residues of actual candidate positions;
    never iterate over an exponential product of empty modulus classes.
    Equal residue histograms are deduplicated. This is an exact
    combinatorial reference implementation, not a scalable ILP solver.
    """
    assert len(windows)==len(required)
    assert h>=1
    capacities=hist(support(Q,windows),h)
    aq=Counter(q%h for q in Q)
    possible=[]
    for (L,U),k in zip(windows,required):
        if k<0 or k>U-L+1:
            return None,None
        distributions=set()
        for picked in combinations(range(L,U+1),k):
            distribution=Counter(v%h for v in picked)
            distributions.add(tuple(sorted(distribution.items())))
        possible.append(sorted(distributions))
    best=None
    witness=None
    for choice in product(*possible):
        z=Counter()
        for distribution in choice:
            for r,count in distribution:
                z[r]+=count
        load=Counter()
        for q_r,q_count in aq.items():
            for z_r,z_count in z.items():
                load[(q_r+z_r)%h]+=q_count*z_count
        val=36*sum(phi(n,capacities[t]) for t,n in load.items())
        if best is None or val<best:
            best,witness=val,choice
    return best,witness

def cumulative_capacity(Q,windows,h,minimums):
    """Exact joint energy minimum under PREFIX rather than local demands.

    minimums[j] is the required total count through window j
    (zero-based). No window is artificially required to be populated.
    """
    assert len(minimums)==len(windows)
    assert h>=1
    C=hist(support(Q,windows),h)
    aq=Counter(q%h for q in Q)
    options=[]
    for L,U in windows:
        unique=set()
        for k in range(U-L+2):
            for picked in combinations(range(L,U+1),k):
                unique.add((k,tuple(sorted(Counter(v%h for v in picked).items()))))
        options.append(sorted(unique))
    best=None
    witness=None
    for chosen in product(*options):
        subtotal=0
        valid=True
        for j,(count,_) in enumerate(chosen):
            subtotal+=count
            if subtotal<minimums[j]:
                valid=False
                break
        if not valid:
            continue
        z=Counter()
        for _,allocation in chosen:
            for r,count in allocation:
                z[r]+=count
        demand=Counter()
        for r,a in aq.items():
            for t,n in z.items():
                demand[(r+t)%h]+=a*n
        value=36*sum(phi(n,C[t]) for t,n in demand.items())
        if best is None or value<best:
            best,witness=value,chosen
    return best,witness


def old_pair_sum_weights(P):
    """Q(P), with the exact 1/2 ordered-old-pair multiplicities."""
    out={}
    for p,q in combinations_with_replacement(sorted(P),2):
        assert p+q not in out, "P must be B2, hence B3"
        out[p+q]=1 if p==q else 2
    return out


def full_prefix_mixed_defect(P,Z):
    """Exact positive sixth-defect contribution of old-old-new triples."""
    qweights=old_pair_sum_weights(P)
    weighted=Counter()
    for q,w in qweights.items():
        for z in Z:
            weighted[q+z]+=w
    n=len(P)
    return 9*(sum(v*v for v in weighted.values())
              -(2*n*n-n)*len(Z))


def full_prefix_integer_bound(P,Z,windows,h):
    """Sound unweighted residue lower bound with repeated old pairs."""
    Q=set(old_pair_sum_weights(P))
    U=support(Q,windows)
    cap=hist(U,h)
    load=loads(Q,Z,h)
    return 9*sum(phi(n,c) for n,c in zip(load,cap))


def full_prefix_cumulative_bound(P,windows,h,checkpoint_minimums):
    """All-old-pair PPZ bound: factor NINE, not distinct-colour 36."""
    Q=set(old_pair_sum_weights(P))
    value,witness=cumulative_capacity(Q,windows,h,checkpoint_minimums)
    return (value//4 if value is not None else None),witness


def minimum_integer_squares(W,C):
    """Sharp square-sum lower bound for W integer units and C slots."""
    assert W>=0 and C>=0
    if C==0:
        if W==0:
            return 0
        raise ValueError("nonzero load with no actual support")
    v,w=divmod(W,C)
    return (C-w)*v*v+w*(v+1)*(v+1)


def full_prefix_weighted_modular_bound(P,Z,windows,h):
    """Rigorous weighted old-old-new defect bound, exact at fine modulus."""
    qw=old_pair_sum_weights(P)
    capacities=hist(support(qw,windows),h)
    masses=Counter()
    squares=Counter()
    counts=Counter()
    for q,w in qw.items():
        for z in Z:
            t=(q+z)%h
            masses[t]+=w
            squares[t]+=w*w
            counts[t]+=1
    total=0
    for t in range(h):
        c=capacities[t]
        n=counts[t]
        w=masses[t]
        b=squares[t]
        if not c:
            assert n==w==b==0
            continue
        total+=max(phi(n,c),minimum_integer_squares(w,c)-b,0)
    return 9*total


def weighted_cumulative_capacity(P,windows,h,minimums):
    """Exact finite enumeration, deduplicated by residues where possible."""
    assert len(windows)==len(minimums)
    best=None
    for batches in product(*[
        [
            selected
            for count in range(U-L+2)
            for selected in combinations(range(L,U+1),count)
        ]
        for L,U in windows
    ]):
        count=0
        legal=True
        for j,selected in enumerate(batches):
            count+=len(selected)
            if count<minimums[j]:
                legal=False
                break
        if not legal:
            continue
        z=tuple(v for selected in batches for v in selected)
        val=full_prefix_weighted_modular_bound(P,z,windows,h)
        best=val if best is None else min(best,val)
    return best


def brute_integer_collision_min(N,C):
    best=None
    for cells in product(range(N+1),repeat=C):
        if sum(cells)!=N:
            continue
        val=sum(v*(v-1) for v in cells)
        best=val if best is None else min(best,val)
    return best


def moment_code(p):
    B=3*p+1
    return [1+i+B*(i*i%p)+B*B*(i*i*i%p) for i in range(p)]


class JointWindowIntegerDefectTests(unittest.TestCase):
    def setUp(self):
        self.X=[1,2]
        self.Y=[1000,1003]
        self.Q=qxy(self.X,self.Y)
        self.windows=[(10000,10001),(10003,10004)]

    def test_integer_fibre_formula_is_exact_for_discrete_capacity(self):
        for C in range(1,5):
            for N in range(0,10):
                with self.subTest(C=C,N=N):
                    self.assertEqual(phi(N,C),brute_integer_collision_min(N,C))
        self.assertEqual(phi(4,3),2)
        self.assertEqual(36*phi(4,3),72)
        self.assertEqual(phi(0,0),0)
        with self.assertRaises(ValueError):
            phi(1,0)

    def test_joint_scalar_and_separate_modular_cuts_pass(self):
        Q=self.Q
        self.assertTrue(b3(self.X+self.Y))
        self.assertEqual(Q,{1001,1002,1004,1005})
        self.assertEqual(len(support(Q,self.windows[:1])),6)
        self.assertEqual(len(support(Q,self.windows[1:])),6)
        self.assertEqual(support(Q,self.windows),set(range(11001,11010)))
        self.assertLessEqual(4*2,9)
        for window in self.windows:
            self.assertEqual(joint_capacity(Q,[window],3,[1])[0],0)
            for z in range(window[0],window[1]+1):
                self.assertTrue(b3(self.X+self.Y+[z]))
        self.assertEqual(joint_capacity(Q,self.windows,1,[1,1])[0],0)

    def test_joint_modular_forcing_is_strict_and_exactly_attained(self):
        Q=self.Q
        self.assertEqual(hist(Q,3),(2,0,2))
        self.assertEqual(hist(support(Q,self.windows),3),(3,3,3))
        gamma,allocation=joint_capacity(Q,self.windows,3,[1,1])
        self.assertEqual(gamma,72)
        self.assertIsNotNone(allocation)
        Z=[10000,10004]
        self.assertEqual(charge(Q,Z,self.windows,3),72)
        self.assertEqual(mixed_energy(Q,Z),72)
        self.assertEqual(d6(self.X+self.Y+Z),72)
        self.assertFalse(b3(self.X+self.Y+Z))
        self.assertEqual(1+1000+10004,2+1003+10000)
        for (a,b) in ((self.X,self.Y),(self.X,Z),(self.Y,Z)):
            self.assertTrue(b3(a+b))

    def test_every_joint_selection_has_nonzero_sixth_defect(self):
        for z0 in range(*[self.windows[0][0],self.windows[0][1]+1]):
            for z1 in range(*[self.windows[1][0],self.windows[1][1]+1]):
                Z=[z0,z1]
                actual=mixed_energy(self.Q,Z)
                bound=charge(self.Q,Z,self.windows,3)
                with self.subTest(Z=Z):
                    self.assertGreaterEqual(bound,72)
                    self.assertGreaterEqual(actual,bound)
                    self.assertGreaterEqual(d6(self.X+self.Y+Z),actual)
                    self.assertFalse(b3(self.X+self.Y+Z))

    def test_residue_refinement_pointwise_for_multiple_actual_batches(self):
        rng=random.Random(20261023)
        X=self.X
        Y=self.Y
        Q=self.Q
        for _ in range(80):
            low=rng.randint(9990,10001)
            w1=(low,low+rng.randint(1,3))
            w2=(w1[1]+2,w1[1]+rng.randint(4,7))
            windows=[w1,w2]
            Z=[rng.randint(*w1),rng.randint(*w2)]
            true=mixed_energy(Q,Z)
            for h,H in ((1,2),(1,3),(1,6),(2,6),(3,6),(3,9),(1,9)):
                coarse=charge(Q,Z,windows,h)
                refined=charge(Q,Z,windows,H)
                with self.subTest(Z=Z,h=h,H=H):
                    self.assertLessEqual(coarse,refined)
                    self.assertLessEqual(refined,true)
                    self.assertLessEqual(true,d6(X+Y+Z))

    def test_joint_optimum_monotone_along_divisible_moduli(self):
        for windows,required in (
            (self.windows,[1,1]),
            ([(10000,10002),(10004,10006)],[1,1]),
            ([(10000,10002),(10004,10006)],[2,1]),
        ):
            values=[joint_capacity(self.Q,windows,h,required)[0]
                    for h in (1,3,9)]
            self.assertTrue(values[0]<=values[1]<=values[2])
        self.assertEqual(
            [joint_capacity(self.Q,self.windows,h,[1,1])[0]
             for h in (1,3,9)],
            [0,72,72])

    def test_actual_b3_carrier_produces_zero_joint_minimum(self):
        code=moment_code(17)
        self.assertTrue(b3(code))
        X,Y=code[:3],code[3:6]
        Z0,Z1=code[6:7],code[7:8]
        Q=qxy(X,Y)
        windows=[(Z0[0],Z0[0]),(Z1[0],Z1[0])]
        self.assertTrue(b3(X+Y+Z0+Z1))
        for h in (1,2,3,5,9,11):
            with self.subTest(h=h):
                self.assertEqual(charge(Q,Z0+Z1,windows,h),0)
                self.assertEqual(joint_capacity(Q,windows,h,[1,1])[0],0)

    def test_fine_modulus_is_complete_for_actual_mixed_triple_avoidance(self):
        rng=random.Random(4159)
        examples=[
            (self.windows,[1,1]),
            ([(10000,10002),(10004,10006)],[1,1]),
            ([(10000,10002),(10004,10006)],[2,1]),
        ]
        for _ in range(30):
            start=9995+rng.randrange(10)
            J0=(start,start+rng.randrange(1,4))
            J1=(J0[1]+2,J0[1]+2+rng.randrange(1,4))
            ks=[rng.randint(0,J0[1]-J0[0]+1),
                rng.randint(0,J1[1]-J1[0]+1)]
            examples.append(([J0,J1],ks))
        for windows,ks in examples:
            U=support(self.Q,windows)
            H=max(U)-min(U)+1
            value,_=joint_capacity(self.Q,windows,H,ks)
            from itertools import combinations as choose
            selections=[
                list(choose(range(L,U+1),k))
                for (L,U),k in zip(windows,ks)
            ]
            brute=min(
                mixed_energy(self.Q,[x for cohort in picked for x in cohort])
                for picked in product(*selections)
            )
            with self.subTest(windows=windows,ks=ks,H=H):
                self.assertEqual(value,brute)
        self.assertEqual(joint_capacity(
            self.Q,self.windows,9,[1,1])[0],72)

    def test_fine_modulus_zero_only_asserts_one_mixed_type(self):
        carrier=[1,2,5,14,33,72]
        self.assertTrue(b3(carrier))
        X,Y=carrier[:2],carrier[2:4]
        Q=qxy(X,Y)
        z0,z1=carrier[4],carrier[5]
        windows=[(z0,z0),(z1,z1)]
        U=support(Q,windows)
        H=max(U)-min(U)+1
        exact,_=joint_capacity(Q,windows,H,[1,1])
        self.assertEqual(exact,0)
        self.assertEqual(mixed_energy(Q,[z0,z1]),0)

    def test_cumulative_requirement_forces_without_each_window_lower_bound(self):
        # Total two across two windows is the only population demand;
        # no separate window has a prescribed positive cardinality.
        for h in (1,3,9):
            direct,choice=cumulative_capacity(
                self.Q,self.windows,h,[0,2])
            separate,_=joint_capacity(
                self.Q,self.windows,h,[1,1])
            with self.subTest(h=h):
                self.assertEqual(direct,separate)
                self.assertIsNotNone(choice)
        self.assertEqual(
            cumulative_capacity(self.Q,self.windows,1,[0,2])[0],0)
        self.assertEqual(
            cumulative_capacity(self.Q,self.windows,3,[0,2])[0],72)
        self.assertEqual(
            cumulative_capacity(self.Q,self.windows,3,[0,1])[0],0)

    def test_cumulative_modulus_refinement_and_fine_exactness(self):
        from itertools import combinations as choose
        rng=random.Random(10123)
        examples=[(self.windows,[0,2])]
        for _ in range(15):
            a=9998+rng.randrange(5)
            J0=(a,a+rng.randrange(1,3))
            J1=(J0[1]+2,J0[1]+2+rng.randrange(1,3))
            total=(J0[1]-J0[0]+1)+(J1[1]-J1[0]+1)
            first=rng.randrange(0,J0[1]-J0[0]+2)
            bound=rng.randrange(first,total+1)
            examples.append(([J0,J1],[first,bound]))
        for windows,thresholds in examples:
            U=support(self.Q,windows)
            H=max(U)-min(U)+1
            fine=cumulative_capacity(self.Q,windows,H,thresholds)[0]
            coarse=cumulative_capacity(self.Q,windows,1,thresholds)[0]
            self.assertLessEqual(coarse,fine)
            choices=[]
            for L,R in windows:
                choices.append([
                    selected
                    for n in range(R-L+2)
                    for selected in choose(range(L,R+1),n)
                ])
            brute=min(
                mixed_energy(self.Q,[v for cohort in selection for v in cohort])
                for selection in product(*choices)
                if len(selection[0])>=thresholds[0]
                and sum(map(len,selection))>=thresholds[1]
            )
            with self.subTest(windows=windows,thresholds=thresholds):
                self.assertEqual(fine,brute)

    def test_cumulative_bounds_safe_for_genuine_b3_prefix(self):
        carrier=[1,2,5,14,33,72]
        X,Y=carrier[:2],carrier[2:4]
        Q=qxy(X,Y)
        windows=[(carrier[4],carrier[4]),(carrier[5],carrier[5])]
        self.assertTrue(b3(carrier))
        for h in (1,3,9,101):
            self.assertEqual(
                cumulative_capacity(Q,windows,h,[1,2])[0],0)


    def test_complete_old_pair_sum_weighted_ledger_matches_triple_enumeration(self):
        P=[1,2,5,14]
        self.assertTrue(b3(P))
        Q=old_pair_sum_weights(P)
        self.assertEqual(len(Q),10)
        self.assertEqual(sum(Q.values()),len(P)**2)
        self.assertEqual(sum(w*w for w in Q.values()),2*len(P)**2-len(P))
        for Z in ([1000],[1000,1002],[1001,1003],[1000,1001,1003]):
            with self.subTest(Z=Z):
                weighted=Counter()
                words=list(combinations_with_replacement(P,2))
                for p,q in words:
                    for z in Z:
                        weighted[p+q+z]+=3*(1 if p==q else 2)
                exact=(sum(v*v for v in weighted.values())
                       -sum((3*(1 if p==q else 2))**2
                            for p,q in words for z in Z))
                self.assertEqual(full_prefix_mixed_defect(P,Z),exact)
                self.assertLessEqual(exact,d6(P+Z))
                self.assertEqual(exact==0,
                                 len({q+z for q in Q for z in Z})
                                 ==len(Q)*len(Z))

    def test_full_prefix_cumulative_modular_cut_improves_selected_cross_pair(self):
        P=[1,2,5,14]
        windows=[(1000,1001),(1002,1003)]
        Q=set(old_pair_sum_weights(P))
        U=support(Q,windows)
        self.assertTrue(b3(P))
        self.assertEqual(len(Q),10)
        self.assertEqual(len(U),24)
        self.assertGreaterEqual(len(U),2*len(Q))
        self.assertEqual(hist(U,6),(3,4,5,4,4,4))
        # Cumulative total two; neither window individually required.
        self.assertEqual(cumulative_capacity(Q,windows,1,[0,2])[0],0)
        self.assertEqual(full_prefix_cumulative_bound(P,windows,6,[0,2])[0],18)
        for z0 in (1000,1001):
            for z1 in (1002,1003):
                with self.subTest(z0=z0,z1=z1):
                    Z=[z0,z1]
                    self.assertTrue(all(b3(P+[z]) for z in Z))
                    self.assertGreater(full_prefix_mixed_defect(P,Z),0)
                    self.assertGreater(full_prefix_integer_bound(
                        P,Z,windows,6),0)
                    self.assertLessEqual(full_prefix_integer_bound(
                        P,Z,windows,6),full_prefix_mixed_defect(P,Z))
                    self.assertFalse(b3(P+Z))
        X=[1,2];Y=[5,14];Z=[1000,1002]
        self.assertEqual(mixed_energy(qxy(X,Y),Z),0)
        self.assertGreater(full_prefix_mixed_defect(P,Z),0)


    def test_full_prefix_minimum_uses_nine_not_three_colour_thirty_six(self):
        P=[1,2,5,14]
        windows=[(1000,1001),(1002,1003)]
        self.assertEqual(
            full_prefix_cumulative_bound(P,windows,1,[0,2])[0],0)
        self.assertEqual(
            full_prefix_cumulative_bound(P,windows,6,[0,2])[0],18)
        self.assertEqual(
            full_prefix_cumulative_bound(P,windows,50,[0,2])[0],36)
        best_exact=min(
            full_prefix_mixed_defect(P,list(selected))
            for selected in combinations(range(1000,1004),2))
        self.assertEqual(best_exact,54)
        self.assertLessEqual(
            full_prefix_cumulative_bound(P,windows,50,[0,2])[0],
            best_exact)
    def test_full_prefix_residue_charge_safe_on_genuine_critical_code(self):
        code=moment_code(17)
        self.assertTrue(b3(code))
        P=code[:8];Z=code[8:10]
        windows=[(Z[0],Z[0]),(Z[1],Z[1])]
        self.assertEqual(full_prefix_mixed_defect(P,Z),0)
        for h in (1,2,3,6,9,17,50):
            self.assertEqual(full_prefix_integer_bound(P,Z,windows,h),0)

    def test_weighted_full_prefix_exactness_at_fine_modulus(self):
        P=[1,2,5,14]
        windows=[(1000,1001),(1002,1003)]
        Q=set(old_pair_sum_weights(P))
        U=support(Q,windows)
        H=max(U)-min(U)+1
        self.assertEqual(H,30)
        expected=min(full_prefix_mixed_defect(P,Z)
                     for Z in combinations(range(1000,1004),2))
        self.assertEqual(expected,54)
        self.assertEqual(weighted_cumulative_capacity(
            P,windows,50,[0,2]),54)
        self.assertEqual(weighted_cumulative_capacity(
            P,windows,H,[0,2]),54)
        self.assertEqual(full_prefix_cumulative_bound(
            P,windows,H,[0,2])[0],36)
        self.assertEqual(weighted_cumulative_capacity(
            P,windows,1,[0,2]),0)
        for Z in combinations(range(1000,1004),2):
            with self.subTest(Z=Z):
                self.assertEqual(
                    full_prefix_weighted_modular_bound(P,Z,windows,H),
                    full_prefix_mixed_defect(P,Z))
                self.assertLessEqual(
                    full_prefix_integer_bound(P,Z,windows,H),
                    full_prefix_weighted_modular_bound(P,Z,windows,H))
                self.assertLessEqual(
                    full_prefix_weighted_modular_bound(P,Z,windows,H),
                    d6(P+list(Z)))

    def test_weighted_pressure_is_sound_at_all_resolutions(self):
        import random
        rng=random.Random(20261023)
        P=[1,2,5,14]
        for _ in range(45):
            base=1000+rng.randint(0,15)
            J0=(base,base+2)
            J1=(base+4,base+6)
            windows=[J0,J1]
            Z=[rng.randint(*J0),rng.randint(*J1)]
            exact=full_prefix_mixed_defect(P,Z)
            for h in (1,2,3,4,5,6,8,12,20,32,64):
                val=full_prefix_weighted_modular_bound(P,Z,windows,h)
                with self.subTest(Z=Z,h=h):
                    self.assertGreaterEqual(val,0)
                    self.assertLessEqual(val,exact)
                    self.assertLessEqual(exact,d6(P+Z))
            for h,H in ((1,2),(1,3),(2,4),(3,6),(4,12),(8,32)):
                self.assertLessEqual(
                    full_prefix_weighted_modular_bound(P,Z,windows,h),
                    full_prefix_weighted_modular_bound(P,Z,windows,H))

    def test_weighted_certificate_zero_for_genuine_b3_carrier(self):
        carrier=moment_code(17)
        self.assertTrue(b3(carrier))
        P=carrier[:8]
        Z=carrier[8:10]
        windows=[(Z[0],Z[0]),(Z[1],Z[1])]
        self.assertEqual(full_prefix_mixed_defect(P,Z),0)
        for h in (1,2,3,5,6,11,31,101):
            self.assertEqual(full_prefix_weighted_modular_bound(
                P,Z,windows,h),0)
    def test_cauchy_fractional_pressure_is_strictly_weaker_on_hostile_case(self):
        Z=[10000,10004]
        C=hist(support(self.Q,self.windows),3)
        N=loads(self.Q,Z,3)
        real_pressure=36*sum(
            max(Fraction(0),Fraction(n*n,c)-n)
            for n,c in zip(N,C))
        integer_pressure=charge(self.Q,Z,self.windows,3)
        self.assertEqual(N,(2,4,2))
        self.assertEqual(real_pressure,48)
        self.assertEqual(integer_pressure,72)

    def test_extra_multiplicity_can_never_hide_from_integer_ledger(self):
        Q=self.Q
        windows=self.windows
        for Z in ([10000,10004],[10000,10003],[10001,10004]):
            for h in (1,2,3,5,9,13):
                self.assertLessEqual(charge(Q,Z,windows,h),mixed_energy(Q,Z))


if __name__=="__main__":
    unittest.main()
