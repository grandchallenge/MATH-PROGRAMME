"""CSM G2: exact conditional probabilities for a biased Bernoulli XOR sliding-block image.

X_i are iid Bernoulli(p) on Z; Y_i = X_i XOR X_{i+1}.
A left observed exterior pattern is zeros^k followed by ones^L,
and a right pattern is ones^R followed by zeros^k.
All computations are finite rational and require no stochastic simulation.
"""
from fractions import Fraction


def _validate(L, R, K, p):
    if any(not isinstance(x, int) or x < 0 for x in (L, R, K)):
        raise ValueError("pattern lengths must be nonnegative integers")
    p = Fraction(p)
    if not 0 < p < 1:
        raise ValueError("the hidden Bernoulli parameter must lie strictly between 0 and 1")
    return p


def endpoint_likelihoods(pattern, p, reverse=False):
    """Weights for endpoint bits 0,1 given consecutive XOR edges.

    For reverse=True, the specified pattern is ordered left to right and the
    endpoint lies at its right end. For reverse=False the endpoint is leftmost.
    """
    p = Fraction(p)
    if not 0 < p < 1 or any(y not in (0, 1) for y in pattern):
        raise ValueError("invalid p or observed XOR pattern")
    observations = tuple(reversed(tuple(pattern))) if reverse else tuple(pattern)
    likelihoods = []
    for endpoint in (0, 1):
        hidden_bit = endpoint
        mass = p if endpoint else 1 - p
        for symbol in observations:
            hidden_bit ^= symbol
            mass *= p if hidden_bit else 1 - p
        likelihoods.append(mass)
    return tuple(likelihoods)


def exterior_conditional(L, R, K, p=Fraction(3, 4)):
    """P(Y_0=1 | finite exterior zeros^K ones^L | ones^R zeros^K)."""
    p = _validate(L, R, K, p)
    lw = endpoint_likelihoods((0,) * K + (1,) * L, p, reverse=True)
    rw = endpoint_likelihoods((1,) * R + (0,) * K, p)
    mass = sum(lw) * sum(rw)
    # Independent hidden segments: probability X_0 != X_1
    return (lw[0] * rw[1] + lw[1] * rw[0]) / mass


def cylinder_probability(observations, p=Fraction(3, 4)):
    """Independent two-path enumeration for any observed XOR word."""
    p = Fraction(p)
    if not 0 < p < 1 or any(y not in (0, 1) for y in observations):
        raise ValueError("invalid p or XOR observations")
    return sum(endpoint_likelihoods(tuple(observations), p))
