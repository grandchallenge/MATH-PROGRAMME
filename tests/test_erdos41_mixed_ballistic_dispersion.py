"""Exact finite B3 two-tail dispersion and mixed moment identities."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement as combos
from random import Random
import unittest


A29=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
     3098,4048,5298,6704,7839,10987,12332,15465,
     19144,24546,28974,34406,37769,45864,50877)


def b3(A):
    t=[sum(x) for x in combos(A,3)]
    return len(t)==len(set(t))


def weighted_mixed(X,Y):
    a=tuple(X)+tuple(Y)
    xs=set(X);ys=set(Y)
    w=Counter()
    for u,v in combos(a,2):
        for c in a:
            if (u in xs and v in xs and c in xs) or (
                u in ys and v in ys and c in ys):
                continue
            w[u+v-2*c]+=1 if u==v else 2
    return w


def moment_stats(Z):
    n=len(Z)
    mu=Fraction(sum(Z),n)
    var=sum((z-mu)**2 for z in Z)/n
    return mu,var


def pair_type_tail(X,Y):
    neg=Counter()
    pos=Counter()
    for a,b in combos(X,2):
        for c in Y:
            neg[a+b-2*c]+=1 if a==b else 2
    for a,b in combos(Y,2):
        for c in X:
            pos[a+b-2*c]+=1 if a==b else 2
    return neg,pos


class MixedBallisticTests(unittest.TestCase):
    def test_exact_first_and_second_mixed_moments_for_B3_partitions(self):
        self.assertTrue(b3(A29))
        rng=Random(41)
        cases=[(A29[:n],A29[n:]) for n in (1,2,3,5,10,14,20,28)]
        cases.extend((tuple((z:=rng.sample(A29,len(A29)))[:n]),
                      tuple(z[n:])) for n in (2,5,11,22))
        for X,Y in cases:
            if not X or not Y:continue
            x=len(X);y=len(Y);m=x+y
            mu_x,vx=moment_stats(X);mu_y,vy=moment_stats(Y)
            w=weighted_mixed(X,Y)
            self.assertEqual(sum(w.values()),3*x*y*m)
            self.assertEqual(sum(d*k for d,k in w.items()),0)
            expected=6*x*y*((2*x+y)*vx+(x+2*y)*vy+
                             m*(mu_y-mu_x)**2)
            self.assertEqual(sum(d*d*k for d,k in w.items()),expected)
            self.assertGreaterEqual(Fraction(expected,3*x*y*m),
                                    2*(mu_y-mu_x)**2)
            self.assertNotIn(0,w)

    def test_two_tail_sets_each_have_xy_support(self):
        for n in (1,2,3,4,5,6,8,10,14):
            X=A29[:n]
            Y=A29[n:n+min(n,len(A29)-n)]
            if not Y:continue
            self.assertTrue(b3(X+Y))
            x=len(X);y=len(Y);g=min(Y)-max(X)
            minus,plus=pair_type_tail(X,Y)
            self.assertLessEqual(max(minus),-2*g)
            self.assertGreaterEqual(min(plus),2*g)
            self.assertEqual(sum(minus.values()),x*x*y)
            self.assertEqual(sum(plus.values()),y*y*x)
            self.assertTrue(all(v<=x for v in minus.values()))
            self.assertTrue(all(v<=y for v in plus.values()))
            self.assertGreaterEqual(len(minus),x*y)
            self.assertGreaterEqual(len(plus),x*y)
            self.assertFalse(set(minus).intersection(plus))
            total=weighted_mixed(X,Y)
            self.assertGreaterEqual(
                sum(weight for d,weight in total.items()
                    if abs(d)>=2*g),
                (sum(total.values())//3))

    def test_geometrically_separated_genuine_B3_blocks(self):
        X=A29[:4];Y=A29[-7:]
        x=len(X);y=len(Y)
        g=min(Y)-max(X)
        minus,plus=pair_type_tail(X,Y)
        self.assertTrue(g>0)
        self.assertGreaterEqual(len(minus),x*y)
        self.assertGreaterEqual(len(plus),x*y)
        self.assertGreaterEqual(sum(minus.values()),x*x*y)
        self.assertGreaterEqual(sum(plus.values()),x*y*y)
        self.assertTrue(all(d<=-2*g for d in minus))
        self.assertTrue(all(d>=2*g for d in plus))

    def test_density_constants_and_macro_radii(self):
        for c in (Fraction(1),Fraction(1,2),Fraction(1,4)):
            R=(6/c)**3
            x_lower=c**3/36
            y_lower=c/2
            self.assertEqual(x_lower*y_lower,c**4/72)
            self.assertEqual(x_lower*x_lower*y_lower,c**7/2592)
            self.assertEqual(x_lower*y_lower*y_lower,c**5/144)
            separation=1/R-1/(R*R)
            self.assertGreater(separation,0)
            self.assertLess(separation,Fraction(1,2))
            self.assertEqual(2*(separation**2),2*(1/R-1/R**2)**2)

    def test_hostile_non_B3_union_fails_tail_support_bound(self):
        X=(1,2,3,4);Y=(10,11,12,13)
        self.assertFalse(b3(X+Y))
        minus,plus=pair_type_tail(X,Y)
        self.assertEqual(len(minus),13)
        self.assertEqual(len(plus),13)
        self.assertLess(len(minus),len(X)*len(Y))
        self.assertLess(len(plus),len(X)*len(Y))
        self.assertGreater(max(minus.values()),len(X))
        self.assertGreater(max(plus.values()),len(Y))

    def test_exhaustive_small_B3_two_tail_bound(self):
        checked=0
        for n in (2,3,4):
            for A in combinations(range(1,15),n):
                if not b3(A):continue
                checked+=1
                for split in range(1,n):
                    X=A[:split];Y=A[split:]
                    minus,plus=pair_type_tail(X,Y)
                    self.assertGreaterEqual(len(minus),len(X)*len(Y))
                    self.assertGreaterEqual(len(plus),len(X)*len(Y))
                    self.assertLessEqual(max(minus),-2*(min(Y)-max(X)))
                    self.assertGreaterEqual(min(plus),2*(min(Y)-max(X)))
        self.assertGreater(checked,100)


if __name__=="__main__":
    unittest.main()
