#!/usr/bin/env python3
"""Validate PC-WP03 finite surgery-history fixtures.

This checks only the combinatorial/topological certificate. Hamilton–Perelman
analytic and geometric interfaces remain imported assumptions.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

PERMITTED = {
    "spherical_space_form",
    "s2_bundle_over_s1_orientable",
    "s2_bundle_over_s1_nonorientable",
    "rp3_connected_sum_rp3",
}
BUNDLES = {
    "s2_bundle_over_s1_orientable",
    "s2_bundle_over_s1_nonorientable",
}


def validate(h: dict[str, Any]) -> set[str]:
    err: set[str] = set()
    required = {
        "source_registry", "component_registry", "factor_registry", "events",
        "initial_active_components", "terminal_active_components",
        "surgery_time_control", "extinction", "finite_history_certificate",
        "backward_reconstruction_target", "input_profile", "orientation_profile",
    }
    if not required <= h.keys():
        return {"PC03-E000"}

    sources = h["source_registry"]
    components = {x.get("component_id"): x for x in h["component_registry"]}
    factors = {x.get("factor_id"): x for x in h["factor_registry"]}
    events = h["events"]
    event_ids = [e.get("event_id") for e in events]

    ids = list(components) + list(factors) + event_ids
    if None in ids or len(ids) != len(set(ids)):
        err.add("PC03-E001")

    def source_ok(bindings: Any) -> bool:
        return isinstance(bindings, list) and bool(bindings) and all(x in sources for x in bindings)

    for e in events:
        if not source_ok(e.get("source_bindings")):
            err.add("PC03-E002")
        for d in e.get("discarded_components", []):
            if not source_ok(d.get("source_bindings")):
                err.add("PC03-E002")
    for f in factors.values():
        if not source_ok(f.get("source_bindings")):
            err.add("PC03-E002")
    for k in ("surgery_time_control", "extinction"):
        if not source_ok(h[k].get("source_bindings")):
            err.add("PC03-E002")

    indices = [e.get("event_index") for e in events]
    times = [e.get("time") for e in events]
    t_ext = h["extinction"].get("time")
    if indices != list(range(len(events))):
        err.add("PC03-E003")
    if any(not isinstance(t, (int, float)) for t in times) or any(
        times[i] >= times[i + 1] for i in range(len(times) - 1)
    ) or not isinstance(t_ext, (int, float)) or any(t > t_ext for t in times if isinstance(t, (int, float))):
        err.add("PC03-E003")

    active = h["initial_active_components"]
    for e in events:
        if e.get("active_before") != active:
            err.add("PC03-E004")
        active = e.get("active_after", [])
    if active != h["terminal_active_components"]:
        err.add("PC03-E004")
    if h["terminal_active_components"] or not events or events[-1].get("event_type") != "terminal_extinction_transition" or events[-1].get("active_after") or not h["extinction"].get("empty_for_all_t_ge"):
        err.add("PC03-E013")

    factor_uses: set[str] = set()
    parent_counts: dict[str, int] = {}
    for e in events:
        before, after = set(e.get("active_before", [])), set(e.get("active_after", []))
        if not (before | after) <= components.keys():
            err.add("PC03-E005")
        if e.get("event_type") == "terminal_extinction_transition":
            if e.get("cuts") or e.get("caps") or e.get("ancestry_edges"):
                err.add("PC03-E016")
        elif e.get("event_type") != "surgery_transition":
            err.add("PC03-E016")

        caps = {c.get("cap_id"): c for c in e.get("caps", [])}
        expected_children: set[str] = set()
        cut_parents: set[str] = set()
        required_bundles: set[str] = set()
        for cut in e.get("cuts", []):
            parent = cut.get("parent_component_id")
            cut_parents.add(parent)
            if parent not in before:
                err.add("PC03-E005")
            cap_ids = cut.get("cap_ids", [])
            if len(cap_ids) != 2 or len(set(cap_ids)) != 2 or any(
                cid not in caps or caps[cid].get("cut_id") != cut.get("cut_id") for cid in cap_ids
            ):
                err.add("PC03-E006")
            kind = cut.get("operation_kind")
            if kind == "separating_cut":
                children = cut.get("child_component_ids", [])
                if len(children) != 2 or len(set(children)) != 2:
                    err.add("PC03-E006")
                expected_children.update(children)
            elif kind == "nonseparating_cut":
                child, fid = cut.get("child_component_id"), cut.get("bundle_factor_id")
                expected_children.add(child)
                required_bundles.add(fid)
                f = factors.get(fid, {})
                if f.get("factor_class") not in BUNDLES:
                    err.add("PC03-E007")
                if h["orientation_profile"] == "orientable" and f.get("factor_class") != "s2_bundle_over_s1_orientable":
                    err.add("PC03-E011")
            else:
                err.add("PC03-E006")

        new_children = after - before
        edges = e.get("ancestry_edges", [])
        edge_children: list[str] = []
        for edge in edges:
            p, c = edge.get("from_pre_component_id"), edge.get("to_post_component_id")
            if p not in before or c not in after:
                err.add("PC03-E008")
            edge_children.append(c)
            parent_counts[c] = parent_counts.get(c, 0) + 1
        if set(edge_children) != new_children or len(edge_children) != len(set(edge_children)) or new_children != expected_children:
            err.add("PC03-E008")

        groups = e.get("reconstruction_groups", [])
        lhs = [g.get("pre_component_id") for g in groups]
        if len(lhs) != len(set(lhs)):
            err.add("PC03-E009")
        changed = before - after
        if set(lhs) != changed:
            err.add("PC03-E009")
        group_map = {g.get("pre_component_id"): g for g in groups}
        used_children: list[str] = []
        used_factors: list[str] = []
        for g in groups:
            for s in g.get("summands", []):
                if s.get("kind") == "component":
                    cid = s.get("id")
                    used_children.append(cid)
                    if cid not in after:
                        err.add("PC03-E009")
                elif s.get("kind") == "factor":
                    fid = s.get("id")
                    used_factors.append(fid)
                    factor_uses.add(fid)
                    if fid not in factors:
                        err.add("PC03-E005")
        if set(used_children) != new_children or len(used_children) != len(set(used_children)):
            err.add("PC03-E009")
        if not required_bundles <= set(used_factors):
            err.add("PC03-E007")

        for cut in e.get("cuts", []):
            summands = group_map.get(cut.get("parent_component_id"), {}).get("summands", [])
            cs = {s.get("id") for s in summands if s.get("kind") == "component"}
            fs = {s.get("id") for s in summands if s.get("kind") == "factor"}
            if cut.get("operation_kind") == "separating_cut" and cs != set(cut.get("child_component_ids", [])):
                err.add("PC03-E009")
            if cut.get("operation_kind") == "nonseparating_cut" and (cs != {cut.get("child_component_id")} or cut.get("bundle_factor_id") not in fs):
                err.add("PC03-E007")

        discarded: set[str] = set()
        for d in e.get("discarded_components", []):
            cid, fid = d.get("component_id"), d.get("factor_id")
            discarded.add(cid)
            f = factors.get(fid, {})
            refs = {s.get("id") for s in group_map.get(cid, {}).get("summands", []) if s.get("kind") == "factor"}
            if cid not in before or cid in after or f.get("factor_class") not in PERMITTED or fid not in refs:
                err.add("PC03-E010")
        if changed - cut_parents - discarded:
            err.add("PC03-E009")

    if any(n != 1 for n in parent_counts.values()):
        err.add("PC03-E008")

    for f in factors.values():
        if f.get("factor_class") not in PERMITTED:
            err.add("PC03-E010")
        if h["orientation_profile"] == "orientable" and f.get("orientation") != "orientable":
            err.add("PC03-E011")
        if f.get("factor_class") == "rp3_connected_sum_rp3" and f.get("normal_form_summands") != ["SPHERICAL_SPACE_FORM_NONTRIVIAL", "SPHERICAL_SPACE_FORM_NONTRIVIAL"]:
            err.add("PC03-E015")
    if h["orientation_profile"] == "orientable" and any(c.get("orientation") != "orientable" for c in components.values()):
        err.add("PC03-E011")

    fh = h["finite_history_certificate"]
    if h["surgery_time_control"].get("property") != "finite_on_every_bounded_interval" or fh.get("derivation") != ["finite_on_every_bounded_interval", "finite_extinction_time"] or fh.get("interval") != [0, t_ext] or fh.get("event_count") != len(events) or fh.get("ordered_event_ids") != event_ids:
        err.add("PC03-E012")

    target = h["backward_reconstruction_target"]
    normal = target.get("normal_form", [])
    if target.get("initial_component_ids") != h["initial_active_components"] or set(normal) != factor_uses:
        err.add("PC03-E009")
    if any(fid not in factors for fid in normal):
        err.add("PC03-E005")
    if h["input_profile"] == "poincare_simply_connected":
        if target.get("terminal_group_discharge") != "required_non_circular" or any(
            factors.get(fid, {}).get("fundamental_group_profile") != "trivial" or factors.get(fid, {}).get("normal_form_summands") != ["S3"] for fid in normal
        ):
            err.add("PC03-E014")

    return err


def mutate(root: Any, mutation: dict[str, Any]) -> None:
    node = root
    for key in mutation["path"][:-1]:
        node = node[key]
    key = mutation["path"][-1]
    if mutation["op"] == "set":
        node[key] = mutation["value"]
    elif mutation["op"] == "append":
        node[key].append(mutation["value"])
    else:
        raise ValueError(f"unknown mutation {mutation['op']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures", nargs="?", type=Path, default=Path(__file__).with_name("fixtures.json"))
    args = parser.parse_args()
    data = json.loads(args.fixtures.read_text(encoding="utf-8"))
    failed = 0
    for case in data["cases"]:
        h = copy.deepcopy(data["base_histories"][case["base"]])
        h["source_registry"] = copy.deepcopy(data["shared_source_registry"])
        h["history_id"] = "PC-HIST-" + case["name"].upper().replace("_", "-")
        for m in case.get("mutations", []):
            mutate(h, m)
        actual = validate(h)
        expected = set(case.get("expected_error_codes", []))
        ok = (not actual) if case["expected_valid"] else bool(actual) and expected <= actual
        print(f"{'PASS' if ok else 'FAIL'} {case['name']}: {sorted(actual) if actual else 'valid'}")
        failed += int(not ok)
    print(f"{len(data['cases']) - failed}/{len(data['cases'])} fixtures passed")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
