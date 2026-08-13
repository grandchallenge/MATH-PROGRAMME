#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"
sys.path.insert(0, str(HERE))

import t3_011_d as d
import verify_t3_011_d as v


def expect_fail(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except AssertionError:
        return
    raise AssertionError("mutation did not fail closed")


def main():
    expect_fail(d.validate_operation_parameters, degree=1)
    expect_fail(d.validate_operation_parameters, degree=3)
    bad = dict(d.CHANNEL_INCREMENT); bad["n2"] = 1
    expect_fail(d.validate_operation_parameters, increments=bad)
    expect_fail(d.validate_operation_parameters, pairs_admitted=True)
    expect_fail(d.validate_operation_parameters, mixed_channels_admitted=True)
    result = d.build()
    verified = v.verify(result)
    assert result["terminal"] in (d.POSITIVE_TERMINAL, d.NEGATIVE_TERMINAL)
    assert result["residual_sum_zero_proved"] is False
    assert result["proof_effect"] == "NONE"
    assert result["promotion_effect"] == "NONE"
    assert result["t3_status"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"
    assert verified["terminal"] == result["terminal"]
    if result["terminal"] == d.POSITIVE_TERMINAL:
        assert result["first_cokernel_breaking_direction"] is not None
        assert result["polynomial_degree_alone_breaks_cokernel_obstruction"] is True
    else:
        assert result["tested_independent_prefix_count"] == 311
        assert result["mirror_l1"]["tested_prefix_count"] == 110
        assert result["polynomial_degree_alone_breaks_cokernel_obstruction"] is False
    print("T3-011-D adversarial replay complete")


if __name__ == "__main__":
    main()
