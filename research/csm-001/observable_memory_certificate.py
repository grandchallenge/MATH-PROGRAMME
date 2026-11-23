"""CSM-G2-WP04: rational observable-subspace finite-memory certificates.

A bounded exact realization of classical linear-representation/Hankel tests.
Not a novel Gibbs-classification theorem or a general continuity decision tool.

Transfer orientation: T[z][current_state][next_state].  For a word w,
P(w) = stationary_row * T[w] * all_ones_column.
"""
from collections import deque
from fractions import Fraction
from itertools import product
from math import comb


def _rat(x):
    return Fraction(x)


def _matrix(rows):
    a = tuple(tuple(_rat(x) for x in row) for row in rows)
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError("nonempty rectangular matrix required")
    if any(x < 0 for row in a for x in row):
        raise ValueError("nonnegative entries required")
    return a


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _rank(vectors):
    """Ordinary exact rational Gaussian elimination, treating vectors as rows."""
    if not vectors:
        return 0
    a = [list(map(Fraction, v)) for v in vectors]
    columns = len(a[0])
    if any(len(v) != columns for v in a):
        raise ValueError("inconsistent vector widths")
    r = 0
    for j in range(columns):
        pivot = next((i for i in range(r, len(a)) if a[i][j] != 0), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][j]
        for col in range(j, columns):
            a[r][col] /= scale
        for i in range(r + 1, len(a)):
            mult = a[i][j]
            if mult:
                for col in range(j, columns):
                    a[i][col] -= mult * a[r][col]
        r += 1
        if r == len(a):
            break
    return r


class ObservableFiniteMemory:
    def __init__(self, stationary, labelled_transfer):
        self.matrices = tuple(_matrix(matrix) for matrix in labelled_transfer)
        if not self.matrices:
            raise ValueError("nonempty output alphabet required")
        self.dimension = len(self.matrices[0])
        n = self.dimension
        if any(len(a) != n or len(a[0]) != n for a in self.matrices):
            raise ValueError("all labelled matrices must be square, same dimension")
        self.pi = tuple(_rat(x) for x in stationary)
        if len(self.pi) != n or any(x <= 0 for x in self.pi) or sum(self.pi) != 1:
            raise ValueError("positive normalized stationary row required")
        self.alphabet = len(self.matrices)
        self.Q = tuple(tuple(sum(a[i][j] for a in self.matrices)
                             for j in range(n)) for i in range(n))
        if any(sum(row) != 1 for row in self.Q):
            raise ValueError("sum_z T_z must be row-stochastic")
        if any(sum(self.pi[i] * self.Q[i][j] for i in range(n)) != self.pi[j]
               for j in range(n)):
            raise ValueError("stationary row does not satisfy pi Q = pi")
        self.ones = (Fraction(1),) * n
        self._right_basis = None
        self._left_basis = None

    def _word(self, word):
        word = tuple(word)
        if any(not isinstance(z, int) or not 0 <= z < self.alphabet for z in word):
            raise ValueError("invalid observed-symbol index")
        return word

    def _left_step(self, row, z):
        a = self.matrices[z]
        return tuple(sum(row[i] * a[i][j] for i in range(self.dimension))
                     for j in range(self.dimension))

    def _right_step(self, z, column):
        return tuple(_dot(row, column) for row in self.matrices[z])

    def message(self, word, terminal=None):
        """T[word] times terminal column, with the correct matrix order."""
        b = self.ones if terminal is None else tuple(map(Fraction, terminal))
        if len(b) != self.dimension:
            raise ValueError("terminal column arity mismatch")
        for z in reversed(self._word(word)):
            b = self._right_step(z, b)
        return b

    def word_probability(self, word):
        return _dot(self.pi, self.message(word))

    def full_support_obstruction(self):
        """Shortest forbidden output word via at most 2^dimension reachable sets.

        None means every output word has positive probability. This exact
        Boolean check is only a domain check, NOT a Gibbs classifier.
        """
        initial = frozenset(range(self.dimension))
        queue = deque([((), initial)])
        visited = {initial}
        while queue:
            prefix, active = queue.popleft()
            for z, a in enumerate(self.matrices):
                follow = frozenset(
                    j for i in active for j in range(self.dimension)
                    if a[i][j] > 0
                )
                if not follow:
                    return prefix + (z,)
                if follow not in visited:
                    visited.add(follow)
                    queue.append((prefix + (z,), follow))
        return None

    def _spanning_words(self, right=True):
        """Actual word-labelled basis of T_w * 1 or pi * T_w.

        Every retained word has length at most dimension minus one, because
        each added vector increases the rank from the initial rank-one span.
        """
        if right:
            seed = self.ones
        else:
            seed = self.pi
        basis = [((), seed)]
        k = 0
        while k < len(basis):
            word, vector = basis[k]
            for z in range(self.alphabet):
                new_vector = (self._right_step(z, vector) if right
                              else self._left_step(vector, z))
                if _rank([v for _, v in basis] + [new_vector]) > len(basis):
                    new_word = (z,) + word if right else word + (z,)
                    basis.append((new_word, new_vector))
            k += 1
        assert len(basis) <= self.dimension
        assert all(len(w) <= self.dimension - 1 for w, _ in basis)
        return tuple(basis)

    @property
    def right_basis(self):
        if self._right_basis is None:
            self._right_basis = self._spanning_words(True)
        return self._right_basis

    @property
    def left_basis(self):
        if self._left_basis is None:
            self._left_basis = self._spanning_words(False)
        return self._left_basis

    @property
    def minimal_linear_dimension(self):
        left = self.left_basis
        right = self.right_basis
        hankel = [tuple(_dot(l, r) for _, r in right) for _, l in left]
        return _rank(hankel)

    def check_reverse_order(self, k):
        """Decide whether future-conditional memory is at most k.

        Returns either a complete exact certificate, a concrete rational
        unequal-conditional witness, or a forbidden-word domain obstruction.
        """
        if not isinstance(k, int) or k < 0:
            raise ValueError("nonnegative memory order required")
        bad = self.full_support_obstruction()
        if bad is not None:
            return {"outcome": "outside_full_shift", "forbidden_word": bad}
        for prefix in product(range(self.alphabet), repeat=k):
            denominator = self.word_probability(prefix)
            assert denominator > 0
            for a in range(self.alphabet):
                baseline_numer = self.word_probability((a,) + prefix)
                for tail, b in self.right_basis:
                    tail_den = _dot(self.pi, self.message(prefix, b))
                    tail_numer = _dot(
                        self.pi, self.message((a,) + prefix, b))
                    if tail_numer * denominator != baseline_numer * tail_den:
                        assert tail_den > 0
                        return {
                            "outcome": "counterexample",
                            "order": k,
                            "symbol": a,
                            "prefix": prefix,
                            "tail": tail,
                            "baseline": baseline_numer / denominator,
                            "extended": tail_numer / tail_den,
                            "basis_dimension": len(self.right_basis),
                        }
        return {
            "outcome": "certified",
            "order": k,
            "basis_dimension": len(self.right_basis),
            "minimal_linear_dimension": self.minimal_linear_dimension,
            "max_witness_tail": max(map(lambda x: len(x[0]), self.right_basis)),
        }

    def find_finite_reverse_order(self, max_order=None):
        """Source-dependent global test using Béal et al. 2026 Thm 5.1.

        The order cutoff C(n,2) is an EXTERNAL theorem for invariant sofic
        measures and the minimal linear-representation dimension n.
        This function does not independently certify that published proof.
        """
        n = self.minimal_linear_dimension
        cutoff = comb(n, 2)
        if max_order is not None:
            if not isinstance(max_order, int) or max_order < 0:
                raise ValueError("invalid requested maximum order")
            limit = min(cutoff, max_order)
        else:
            limit = cutoff
        witnesses = []
        for k in range(limit + 1):
            result = self.check_reverse_order(k)
            if result["outcome"] == "certified":
                return {"outcome": "finite", "order": k,
                        "minimal_dimension": n, "external_cutoff": cutoff,
                        "certificate": result}
            if result["outcome"] == "outside_full_shift":
                return result
            witnesses.append(result)
        if max_order is not None and max_order < cutoff:
            return {"outcome": "undecided_above_budget",
                    "checked_to": limit, "external_cutoff": cutoff,
                    "witnesses": tuple(witnesses)}
        return {"outcome": "no_finite_order_under_external_theorem",
                "minimal_dimension": n, "external_cutoff": cutoff,
                "witnesses": tuple(witnesses)}


def two_layer_overlap(P, pi, K, H):
    """Exact finite Markov lift of two overlapping pair-output layers.

    Unlike a positive-transfer-only routine, K and H may contain zero
    probabilities (including deterministic channels). Zero-stationary lift
    states are pruned only after checking their exact stationary mass.
    """
    P = _matrix(P)
    n = len(P)
    if len(P[0]) != n or any(sum(r) != 1 for r in P):
        raise ValueError("hidden transition must be stochastic square")
    pi = tuple(_rat(v) for v in pi)
    if len(pi) != n or any(x <= 0 for x in pi) or sum(pi) != 1:
        raise ValueError("strictly positive hidden stationary law required")
    if any(sum(pi[i] * P[i][j] for i in range(n)) != pi[j] for j in range(n)):
        raise ValueError("hidden pi must be stationary")
    if len(K) != n or any(len(row) != n for row in K):
        raise ValueError("first-layer pair-channel dimensions")
    first = tuple(tuple(tuple(_rat(x) for x in vec) for vec in row) for row in K)
    m = len(first[0][0])
    if m == 0 or any(len(v) != m or any(x < 0 for x in v) or sum(v) != 1
                     for row in first for v in row):
        raise ValueError("first-layer channels must be stochastic")
    if len(H) != m or any(len(row) != m for row in H):
        raise ValueError("second-layer pair-channel dimensions")
    second = tuple(tuple(tuple(_rat(x) for x in vec) for vec in row) for row in H)
    zsize = len(second[0][0])
    if zsize == 0 or any(len(v) != zsize or any(x < 0 for x in v) or sum(v) != 1
                         for row in second for v in row):
        raise ValueError("second-layer channels must be stochastic")
    states = tuple((s, y) for s in range(n) for y in range(m))
    lam = tuple(sum(pi[u] * P[u][s] * first[u][s][y] for u in range(n))
                for s, y in states)
    live = tuple(i for i, x in enumerate(lam) if x > 0)
    if not live:
        raise AssertionError("no positive stationary lifted states")
    matrices = []
    for z in range(zsize):
        rows = []
        for i in live:
            s, y = states[i]
            rows.append(tuple(
                P[s][states[j][0]] * first[s][states[j][0]][states[j][1]]
                * second[y][states[j][1]][z]
                for j in live
            ))
        matrices.append(tuple(rows))
    result = ObservableFiniteMemory(tuple(lam[i] for i in live), matrices)
    result.lifted_states = tuple(states[i] for i in live)
    return result


def composed_xor_lift(p):
    """X iid, Y_i=X_i XOR X_(i+1), Z_i=Y_i XOR Y_(i+1).

    Thus Z_i=X_i XOR X_(i+2).  The fair and biased models have identical
    labelled support, but only the fair model has independent output.
    """
    p = Fraction(p)
    if not 0 < p < 1:
        raise ValueError("0 < p < 1 required")
    pi = (1-p, p)
    P = (pi, pi)
    K = tuple(tuple(tuple(int(y == (s ^ t)) for y in (0, 1))
                    for t in (0, 1)) for s in (0, 1))
    H = tuple(tuple(tuple(int(z == (y ^ w)) for z in (0, 1))
                    for w in (0, 1)) for y in (0, 1))
    return two_layer_overlap(P, pi, K, H)


def observed_markov(P, pi):
    """Current-state emission of a hidden Markov chain (may have zeros)."""
    q = _matrix(P)
    n = len(q)
    matrices = tuple(
        tuple(tuple(q[i][j] if i == symbol else Fraction(0)
                    for j in range(n)) for i in range(n))
        for symbol in range(n)
    )
    return ObservableFiniteMemory(pi, matrices)


def phase_mixture(p_minus, p_plus, weight=Fraction(1, 2)):
    """Stationary mixture of two iid Bernoulli output phases.

    The two hidden sectors are noncommunicating, so all labelled matrices
    have the same diagonal support for every 0<p_minus,p_plus<1.
    The Gibbs classification changes at exact observational equality.
    """
    a, b, weight = Fraction(p_minus), Fraction(p_plus), Fraction(weight)
    if not 0 < a < 1 or not 0 < b < 1 or not 0 < weight < 1:
        raise ValueError("strict positive phases and mixture weight required")
    T0 = ((1-a, Fraction(0)), (Fraction(0), 1-b))
    T1 = ((a, Fraction(0)), (Fraction(0), b))
    return ObservableFiniteMemory((weight, 1-weight), (T0, T1))


def phase_mixture_conditional_ones(p_minus, p_plus, ones, zeros=0,
                                   weight=Fraction(1, 2)):
    """Exact P(Y_0=1 | an exterior cylinder has ones and zeros counts).

    Both hidden phases are iid; disjoint left/right exterior positions
    contribute multiplicatively. Counts, not their positions, are relevant.
    """
    if not isinstance(ones, int) or ones < 0 or not isinstance(zeros, int) or zeros < 0:
        raise ValueError("nonnegative counts required")
    a, b, weight = Fraction(p_minus), Fraction(p_plus), Fraction(weight)
    if not 0 < a < 1 or not 0 < b < 1 or not 0 < weight < 1:
        raise ValueError("strict positive phases and mixture weight required")
    x = weight * (a ** ones) * ((1-a) ** zeros)
    y = (1-weight) * (b ** ones) * ((1-b) ** zeros)
    return (a*x + b*y) / (x+y)
