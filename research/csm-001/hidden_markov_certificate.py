"""CSM-G2 positive hidden-Markov channel preservation certificate.

Finite exact arithmetic and forward/backward semantics; the Gibbs/regularity
result itself is classical and is not asserted as a novel GCL theorem.
All states and output symbols are represented by 0-based finite indices.
"""
from fractions import Fraction
from itertools import product


def rational_matrix(rows):
    result = tuple(tuple(Fraction(x) for x in row) for row in rows)
    if not result or not result[0] or any(len(r) != len(result[0]) for r in result):
        raise ValueError("nonempty rectangular rational matrix required")
    if any(x < 0 for r in result for x in r):
        raise ValueError("negative entries prohibited")
    return result


def compose_emissions(first, second):
    """Stochastic channel composition: hidden -> intermediate -> observed."""
    a, b = rational_matrix(first), rational_matrix(second)
    if len(a[0]) != len(b):
        raise ValueError("channel interface arity mismatch")
    if any(sum(r) != 1 for r in a + b):
        raise ValueError("channel must be row stochastic")
    return tuple(tuple(sum(a[i][j] * b[j][k] for j in range(len(b)))
                       for k in range(len(b[0]))) for i in range(len(a)))


class HiddenMarkovCertificate:
    """Positive transition; finite nonnegative observation channel; stationary law."""

    def __init__(self, transition, emission, stationary):
        p, e = rational_matrix(transition), rational_matrix(emission)
        pi = tuple(Fraction(v) for v in stationary)
        n, z = len(p), len(e[0])
        if any(len(r) != n for r in p) or len(e) != n or len(pi) != n:
            raise ValueError("state spaces do not match")
        if any(v <= 0 for row in p for v in row):
            raise ValueError("transition must be strictly positive")
        if any(sum(row) != 1 for row in p + e):
            raise ValueError("transition and emission must be stochastic")
        if any(v <= 0 for v in pi) or sum(pi) != 1:
            raise ValueError("strictly positive stationary probability required")
        if any(sum(pi[i] * p[i][j] for i in range(n)) != pi[j] for j in range(n)):
            raise ValueError("stationary law does not satisfy pi P = pi")
        masses = tuple(sum(pi[i] * e[i][a] for i in range(n)) for a in range(z))
        if any(m <= 0 for m in masses):
            raise ValueError("every output symbol must be possible")
        self.transition, self.emission, self.stationary = p, e, pi
        self.output_masses = masses
        self.ratio = max(x for row in p for x in row) / min(x for row in p for x in row)
        self.kappa = (self.ratio - 1) / (self.ratio + 1)

    def future_message(self, observed_future):
        """b(s) = Prob(Y_1,...,Y_m | S_0=s), exact."""
        p, e = self.transition, self.emission
        n, z = len(p), len(e[0])
        b = (Fraction(1),) * n
        for a in reversed(tuple(observed_future)):
            if not isinstance(a, int) or not (0 <= a < z):
                raise ValueError("invalid observation index")
            weighted = tuple(e[j][a] * b[j] for j in range(n))
            b = tuple(sum(p[i][j] * weighted[j] for j in range(n)) for i in range(n))
        assert all(v > 0 for v in b)
        return b

    def conditional_before_future(self, observed_future):
        """Exact q_m(a | Y_1,...,Y_m), for every a."""
        b = self.future_message(observed_future)
        pi, e = self.stationary, self.emission
        denominator = sum(pi[i] * b[i] for i in range(len(pi)))
        q = tuple(sum(pi[i] * e[i][a] * b[i] for i in range(len(pi))) /
                  denominator for a in range(len(e[0])))
        assert sum(q) == 1 and all(v > 0 for v in q)
        return q

    def word_probability(self, observed):
        """Transfer computation of stationary observed word probability."""
        observed = tuple(observed)
        if not observed:
            return Fraction(1)
        n, z = len(self.transition), len(self.emission[0])
        if any(not isinstance(a, int) or not (0 <= a < z) for a in observed):
            raise ValueError("invalid observation index")
        current = [self.stationary[i] * self.emission[i][observed[0]] for i in range(n)]
        for a in observed[1:]:
            current = [self.emission[j][a] *
                       sum(current[i] * self.transition[i][j] for i in range(n))
                       for j in range(n)]
        return sum(current)

    def word_probability_by_enumeration(self, observed):
        """Independent path enumeration; intentionally no matrix recursion."""
        observed = tuple(observed)
        if not observed:
            return Fraction(1)
        n, z = len(self.transition), len(self.emission[0])
        if any(not isinstance(a, int) or not (0 <= a < z) for a in observed):
            raise ValueError("invalid observation index")
        result = Fraction(0)
        for path in product(range(n), repeat=len(observed)):
            mass = self.stationary[path[0]]
            for k, a in enumerate(observed):
                mass *= self.emission[path[k]][a]
                if k:
                    mass *= self.transition[path[k-1]][path[k]]
            result += mass
        return result

    def positive_lower_bound(self, symbol):
        """Uniform q_m(symbol|future) >= p(symbol) / (max(P)/min(P))."""
        return self.output_masses[symbol] / self.ratio
