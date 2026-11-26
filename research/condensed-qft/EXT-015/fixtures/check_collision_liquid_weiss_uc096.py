"""Exact finite component and Čech controls for UC096."""

from fractions import Fraction
from itertools import combinations, product


def rank(columns):
    """Column rank by exact sparse elimination."""
    pivots = {}
    for column in columns:
        remaining = {row: Fraction(value) for row, value in column.items() if value}
        while remaining:
            lead = min(remaining)
            factor = remaining[lead]
            if lead not in pivots:
                pivots[lead] = {row: value / factor for row, value in remaining.items()}
                break
            for row, value in pivots[lead].items():
                remainder = remaining.get(row, 0) - factor * value
                if remainder:
                    remaining[row] = remainder
                else:
                    remaining.pop(row, None)
    return len(pivots)


def ordered_component_cech(components, patches, centers):
    """Ordered Čech chains for patches that are unions of whole components."""
    center_tuples = tuple(product(components, repeat=centers))
    sizes = [len(center_tuples)]
    ranks = []
    for size in range(1, len(patches) + 1):
        columns = []
        for labels in combinations(range(len(patches)), size):
            for points in center_tuples:
                if all(set(points) <= patches[label] for label in labels):
                    columns.append({
                        (labels[:i] + labels[i + 1:], points): (-1)**i
                        for i in range(size)
                    })
        sizes.append(len(columns))
        ranks.append(rank(columns))
    ranks = [0, *ranks, 0]
    return tuple(size - ranks[i] - ranks[i + 1] for i, size in enumerate(sizes))


def boundary(labels):
    """Full labelled tuple differential, retaining repeated labels."""
    coefficients = {}
    for i in range(len(labels)):
        face = labels[:i] + labels[i + 1:]
        coefficients[face] = coefficients.get(face, 0) + (-1)**i
    return {face: value for face, value in coefficients.items() if value}


def check_cone_on_full_tuples():
    for size in range(1, 6):
        for labels in product(range(3), repeat=size):
            result = boundary((0, *labels))
            for face, value in boundary(labels).items():
                coned_face = (0, *face)
                result[coned_face] = result.get(coned_face, 0) + value
            assert {face: value for face, value in result.items() if value} == {labels: 1}


def check_vacuum_and_cover_sizes():
    components = (0, 1)
    patches = ({0}, {1}, {0})
    assert ordered_component_cech(components, patches, 0) == (0, 0, 0, 0)
    assert ordered_component_cech(components, patches, 1) == (0, 0, 0, 0)
    assert ordered_component_cech(components, patches, 2) == (2, 0, 0, 0)

    components = (0, 1, 2)
    pairs = tuple(set(pair) for pair in combinations(components, 2))
    assert ordered_component_cech(components, pairs, 2) == (0, 0, 0, 0)
    assert ordered_component_cech(components, pairs, 3) == (6, 0, 0, 0)

    prefixes = tuple(set(components[:size]) for size in range(1, 4))
    assert ordered_component_cech(components, prefixes, 3) == (0, 0, 0, 0)


def check_merging_intersection_components():
    # A=(0,2) union (4,6), B=(1,5), A union B=(0,6).
    # The two A-intersection-B components have separate signed faces.
    faces = ({"a_left": -1, "b": 1}, {"a_right": -1, "b": 1})
    assert all(sum(face.values()) == 0 for face in faces)
    augmentation = ({"whole": 1}, {"whole": 1}, {"whole": 1})
    assert rank(faces) == 3 - rank(augmentation) == 2

    # The one vacuum on A and B is identified even for a physically empty intersection.
    assert rank(({"a": -1, "b": 1},)) == 2 - rank(({"vacuum": 1}, {"vacuum": 1}))


if __name__ == "__main__":
    check_cone_on_full_tuples()
    check_vacuum_and_cover_sizes()
    check_merging_intersection_components()
    print("collision-liquid Weiss finite controls: PASS")
