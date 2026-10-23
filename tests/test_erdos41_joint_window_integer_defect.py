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
