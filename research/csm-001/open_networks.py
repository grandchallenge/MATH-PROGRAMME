"""Typed finite open factor networks with exact nonnegative rational semantics.

CSM-01-WP01: finite elementary semantics, not mathematical certification.
A variable shared across factor scopes represents one shared state value.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from finite_semantics import matrix


def assignments(spaces, names):
    """Enumerate assignments in port order, including the empty assignment."""
    return product(*(spaces[n] for n in names))


@dataclass(frozen=True)
class Factor:
    scope: tuple[str, ...]
    table: tuple[tuple[tuple[object, ...], Fraction], ...]

    @classmethod
    def make(cls, scope, table):
        if len(set(scope)) != len(scope):
            raise ValueError("a factor may mention each variable only once")
        converted = tuple((tuple(k), Fraction(v)) for k, v in table.items())
        if any(v < 0 for _, v in converted):
            raise ValueError("weights must be nonnegative")
        if len({k for k, _ in converted}) != len(converted):
            raise ValueError("duplicate factor assignments")
        return cls(tuple(scope), converted)

    def value(self, configuration):
        return dict(self.table)[tuple(configuration[v] for v in self.scope)]


@dataclass(frozen=True)
class Network:
    """Factor hypergraph with ordered typed input and output variable ports.

    Every variable has a nonempty finite state set. Factor tables are total.
    A variable may be on both the input and output boundary (identity wire),
    but may not be repeated within a single boundary list. Internal variables
    are summed, while boundary variables are held fixed and type checked.
    """
    variables: tuple[tuple[str, tuple[object, ...]], ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    factors: tuple[Factor, ...] = ()

    def __post_init__(self):
        spaces = dict(self.variables)
        if len(spaces) != len(self.variables):
            raise ValueError("duplicate variables")
        if any(not domain or len(set(domain)) != len(domain) for domain in spaces.values()):
            raise ValueError("domains must be nonempty finite sets without repetitions")
        if (len(set(self.inputs)) != len(self.inputs) or
                len(set(self.outputs)) != len(self.outputs)):
            raise ValueError("duplicate port on the same boundary")
        if not set(self.inputs + self.outputs) <= set(spaces):
            raise ValueError("boundary port without variable")
        for f in self.factors:
            if not set(f.scope) <= set(spaces) or len(set(f.scope)) != len(f.scope):
                raise ValueError("invalid factor scope")
            expected = set(assignments(spaces, f.scope))
            actual = {k for k, _ in f.table}
            if expected != actual or len(f.table) != len(actual):
                raise ValueError("factor must supply one weight for every assignment")
            if any(v < 0 for _, v in f.table):
                raise ValueError("negative factor")

    @property
    def spaces(self):
        return dict(self.variables)

    def evaluate(self):
        """Exact matrix: rows output assignments, columns input assignments."""
        spaces = self.spaces
        hidden = tuple(v for v in spaces if v not in self.inputs and v not in self.outputs)
        tables = tuple((f.scope, dict(f.table)) for f in self.factors)
        out = []
        for y in assignments(spaces, self.outputs):
            row = []
            for x in assignments(spaces, self.inputs):
                config = dict(zip(self.inputs, x))
                if any(v in config and config[v] != z for v, z in zip(self.outputs, y)):
                    row.append(Fraction(0))
                    continue
                config.update(zip(self.outputs, y))
                total = Fraction(0)
                for h in assignments(spaces, hidden):
                    full = dict(config)
                    full.update(zip(hidden, h))
                    term = Fraction(1)
                    for scope, table in tables:
                        term *= table[tuple(full[v] for v in scope)]
                    total += term
                row.append(total)
            out.append(row)
        return matrix(out)


def renamed(n, name_map):
    return Network(
        tuple((name_map[k], d) for k, d in n.variables),
        tuple(name_map[k] for k in n.inputs),
        tuple(name_map[k] for k in n.outputs),
        tuple(Factor(tuple(name_map[k] for k in f.scope), f.table) for f in n.factors),
    )


def tensor_network(left, right):
    """Disjoint union with ordered left then right ports."""
    l = renamed(left, {k: "l/" + k for k, _ in left.variables})
    r = renamed(right, {k: "r/" + k for k, _ in right.variables})
    return Network(l.variables + r.variables, l.inputs + r.inputs,
                   l.outputs + r.outputs, l.factors + r.factors)


def glue(first, second):
    """Compose second after first, identifying and summing internal interfaces."""
    if len(first.outputs) != len(second.inputs):
        raise ValueError("boundary arity mismatch")
    if any(first.spaces[a] != second.spaces[b]
           for a, b in zip(first.outputs, second.inputs)):
        raise ValueError("boundary domain mismatch")
    f = renamed(first, {k: "f/" + k for k, _ in first.variables})
    mapping = {k: "g/" + k for k, _ in second.variables}
    for port1, port2 in zip(f.outputs, second.inputs):
        mapping[port2] = port1
    g = renamed(second, mapping)
    unified = dict(f.variables)
    for k, d in g.variables:
        if k in unified and unified[k] != d:
            raise ValueError("glued domain mismatch")
        unified[k] = d
    return Network(tuple(unified.items()), f.inputs, g.outputs, f.factors + g.factors)


def identity_network(domains):
    variables = tuple((f"p{i}", tuple(d)) for i, d in enumerate(domains))
    ports = tuple(v for v, _ in variables)
    return Network(variables, ports, ports)


def swap_network(left_domain, right_domain):
    return Network((("a", tuple(left_domain)), ("b", tuple(right_domain))),
                   ("a", "b"), ("b", "a"))


def copy_network(domain):
    d = tuple(domain)
    spaces = {"i": d, "o0": d, "o1": d}
    table = {values: int(values[0] == values[1] == values[2])
             for values in assignments(spaces, ("i", "o0", "o1"))}
    return Network(tuple(spaces.items()), ("i",), ("o0", "o1"),
                   (Factor.make(("i", "o0", "o1"), table),))


def delete_network(domain):
    return Network((("i", tuple(domain)),), ("i",), ())


def star_network():
    """Three visible binary spins; hidden spin has a positive field of 2:1."""
    domains = {name: (0, 1) for name in ("a", "b", "c", "u")}
    factors = [Factor.make(("u",), {(0,): 1, (1,): 2})]
    for v in ("a", "b", "c"):
        factors.append(Factor.make(("u", v), {
            (i, j): 2 if i == j else 1 for i, j in product((0, 1), repeat=2)
        }))
    return Network(tuple(domains.items()), (), ("a", "b", "c"), tuple(factors))
