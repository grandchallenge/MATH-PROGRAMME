"""Exact rational witnesses for the marked-reset spectral Gibbs criterion.

The general proof is in G2_MARKED_RESET_SPECTRAL_CRITERION_20261123.md.
The verifier accepts a supplied rational spectral splitting and fails closed
when the splitting cannot be checked. No numerical spectral thresholds.
"""
from fractions import Fraction as F


def matrix(rows):
    a = tuple(tuple(F(x) for x in row) for row in rows)
    if not a or not a[0] or any(len(r) != len(a[0]) for r in a):
        raise ValueError("nonempty rectangular matrix required")
    return a


def identity(d):
    return tuple(tuple(F(i == j) for j in range(d)) for i in range(d))


def zero(d):
    return tuple((F(0),) * d for _ in range(d))


def multiply(a, b):
    if len(a[0]) != len(b):
        raise ValueError("matrix shape mismatch")
    return tuple(tuple(sum((x * y for x, y in zip(row, col)), F(0))
                       for col in zip(*b)) for row in a)


def add(a, b):
    return tuple(tuple(x+y for x,y in zip(r,s)) for r,s in zip(a,b))


def scale(a, c):
    return tuple(tuple(c*x for x in r) for r in a)


def power(a, n):
    if not isinstance(n, int) or n < 0 or len(a) != len(a[0]):
        raise ValueError("nonnegative integer square-matrix exponent required")
    b = identity(len(a))
    while n:
        if n % 2:
            b = multiply(b, a)
        a = multiply(a, a)
        n //= 2
    return b


def norm_inf(a):
    return max(sum(abs(x) for x in row) for row in a)


def positive(a):
    return all(x > 0 for row in a for x in row)


class MarkedReset:
    """T0=A; each positive marker has transfer U[:,a] V[a,:]."""
    def __init__(self, a, u, v):
        self.a, self.u, self.v = matrix(a), matrix(u), matrix(v)
        d = self.dimension = len(self.a)
        m = self.markers = len(self.v)
        if len(self.a[0]) != d or len(self.u) != d or len(self.u[0]) != m or len(self.v[0]) != d:
            raise ValueError("inconsistent hidden/marker dimensions")
        if any(x < 0 for row in self.a for x in row):
            raise ValueError("background transfer must be nonnegative")
        if not positive(self.u) or not positive(self.v):
            raise ValueError("reset vectors must be strictly positive")
        self.q = add(self.a, multiply(self.u,self.v))
        if any(sum(row) != 1 for row in self.q):
            raise ValueError("summed transfer must be stochastic")
        self.transfers = (self.a,) + tuple(
            tuple(tuple(self.u[i][k]*self.v[k][j] for j in range(d))
                  for i in range(d)) for k in range(m))

    def gap(self, n):
        return multiply(multiply(self.v, power(self.a,n)), self.u)

    def odds(self, left, right, i, j, a):
        if any(not isinstance(x,int) or not 0 <= x < self.markers
               for x in (i,j,a)):
            raise ValueError("marker index outside alphabet")
        x,y,z=self.gap(left),self.gap(right),self.gap(left+right+1)
        if z[i][j] == 0:
            raise ValueError("zero gap probability; outside full-support theorem")
        return x[i][a]*y[a][j]/z[i][j]

    def conditional(self,left,right,i,j):
        odds=tuple(self.odds(left,right,i,j,a) for a in range(self.markers))
        denominator=1+sum(odds)
        return (1/denominator,)+tuple(x/denominator for x in odds)

    def classify(self, lam, period, projector, contraction_power=1):
        """Check a spectral certificate, then classify Gibbs vs obstruction.

        With B=(A/lam)^period, E projects onto its generalized 1-eigenspace.
        We verify E^2=E, EB=BE, (B-I)^d E=0, and ||[B(I-E)]^t||_inf<1.
        A valid splitting proves the asymptotic expansion analytically.
        For irrational lam or unavailable splitting the caller must not
        pretend this rational verifier supplies a decision.
        """
        lam=F(lam)
        d=self.dimension
        E=matrix(projector)
        if not 0 < lam < 1 or not isinstance(period,int) or period < 1:
            raise ValueError("invalid leading eigenvalue or period")
        if not isinstance(contraction_power,int) or contraction_power < 1:
            raise ValueError("positive contraction exponent required")
        if len(E)!=d or len(E[0])!=d or E==zero(d):
            raise ValueError("nonzero square projector required")
        I=identity(d)
        B=scale(power(self.a,period),lam**(-period))
        N=add(B,scale(I,-1))
        if multiply(E,E)!=E or multiply(B,E)!=multiply(E,B):
            raise ValueError("projector must be idempotent and commute with B")
        if multiply(power(N,d),E)!=zero(d):
            raise ValueError("projector range not generalized unit eigenspace")
        remainder=multiply(B,add(I,scale(E,-1)))
        contraction=norm_inf(power(remainder,contraction_power))
        if contraction>=1:
            raise ValueError("complement contraction not certified")
        # F_(pk+r)/lam^(pk+r) = sum_j binom(k,j) C[r,j]+ exponentially small error.
        coefficients=[]
        for r in range(period):
            left=scale(multiply(self.v,power(self.a,r)),lam**(-r))
            coefficients.append(tuple(
                multiply(multiply(multiply(left,power(N,j)),E),self.u)
                for j in range(d)))
        degree=max((j for j in range(d)
                    if any(any(x!=0 for row in c[j] for x in row)
                           for c in coefficients)),default=-1)
        if degree<0 or not all(positive(c[degree]) for c in coefficients):
            raise ValueError("common strictly positive leading coefficient not certified")
        residues=tuple(c[degree] for c in coefficients)
        result={"degree":degree,"residues":residues,"lambda":lam,
                "period":period,"complement_norm":contraction,
                "contraction_power":contraction_power}
        if degree>0:
            return dict(result,outcome="polynomial_nonnull_obstruction")
        C=residues[0]
        if any(c!=C for c in residues):
            return dict(result,outcome="periodic_continuity_obstruction")
        if any(C[i][j]*C[0][0]!=C[i][0]*C[0][j]
               for i in range(self.markers) for j in range(self.markers)):
            return dict(result,outcome="rank_continuity_obstruction")
        alpha=tuple(row[0] for row in C)
        beta=tuple(x/C[0][0] for x in C[0])
        activity=tuple(alpha[i]*beta[i]/lam for i in range(self.markers))
        return dict(result,outcome="gibbs_exponential",alpha=alpha,beta=beta,
                    activities=activity)


def examples():
    # Same marker vectors and support for unequal and equal background diagonals.
    # Row sums of U are adjusted as the corresponding diagonal changes.
    V=((F(3,4),F(1,4)),(F(1,4),F(3,4)))
    diagonal=MarkedReset(((F(1,2),0),(0,F(1,4))),
        ((F(1,3),F(1,6)),(F(1,4),F(1,2))),V)
    rank=MarkedReset(((F(5,8),0),(0,F(5,8))),
        ((F(1,4),F(1,8)),(F(1,8),F(1,4))),V)
    jordan=MarkedReset(((F(1,4),F(1,4)),(0,F(1,4))),
        ((F(1,2),),(F(3,4),)),((F(1,2),F(1,2)),))
    periodic=MarkedReset(((0,F(1,4)),(F(9,16),0)),
        ((F(3,4),),(F(7,16),)),((F(3,4),F(1,4)),))
    return {
        "diagonal":(diagonal,F(1,2),1,((1,0),(0,0))),
        "rank":(rank,F(5,8),1,identity(2)),
        "jordan":(jordan,F(1,4),1,identity(2)),
        "periodic":(periodic,F(3,8),2,identity(2)),
    }
