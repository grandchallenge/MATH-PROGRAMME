from __future__ import annotations


def producer_factor_map(core, channel: str, strata: list[dict]):
    x0_factor, x1_factor = core.p.channel_coordinate_factors(channel)
    out = {}
    for st in strata:
        x0 = core.a.specialize_rat(core.a.rc.r_factor(x0_factor, exponent=1), st["k_offset"], st["l_offset"])
        x1 = core.a.specialize_rat(core.a.rc.r_factor(x1_factor, exponent=1), st["k_offset"], st["l_offset"])
        out[st["id"]] = {
            "x0": core._single_rat_monomial(x0, f"{channel}:{st['id']}:x0"),
            "x1": core._single_rat_monomial(x1, f"{channel}:{st['id']}:x1"),
        }
    return out


def verifier_factor_map(verifier, channel: str, strata: list[dict]):
    x0_factor, x1_factor = verifier.p.channel_coordinate_factors(channel)
    out = {}
    for st in reversed(strata):
        x0 = verifier.a.specialize_rat(verifier.a.rc.r_factor(x0_factor, exponent=1), st["k_offset"], st["l_offset"])
        x1 = verifier.a.specialize_rat(verifier.a.rc.r_factor(x1_factor, exponent=1), st["k_offset"], st["l_offset"])
        out[st["id"]] = {
            "x0": verifier._single_rat_monomial(x0, f"{channel}:{st['id']}:x0"),
            "x1": verifier._single_rat_monomial(x1, f"{channel}:{st['id']}:x1"),
        }
    return out
