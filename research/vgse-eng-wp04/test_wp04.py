#!/usr/bin/env python3
from analyze_wp04 import summary, validate


def main() -> int:
    errors = validate()
    assert not errors, "\n".join(errors)
    replay = summary()
    assert replay["work_package"] == "VGSE-ENG-WP04"
    assert replay["independent_pair_count"] == 0
    assert replay["independently_varied_quotient_points"] == 0
    assert replay["h1_certified_distortion_lower_bound"] > 100.0
    assert replay["terminal_disposition"] == "GEOMETRY_QUOTIENT_NON_IDENTIFIABLE"
    print("VGSE-ENG-WP04 tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
