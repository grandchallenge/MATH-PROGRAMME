#!/usr/bin/env python3
"""Compatibility entry point for reviewed MATHSOLVE routing validation."""

from mathsolve_routing_reviewed import (
    COMPLETE_CERT_STATES,
    EXPECTED_MANIFESTS,
    EXPECTED_PROVIDER_COMMIT,
    EXPECTED_PROVIDER_PULL_REQUEST,
    GATED_STAGES,
    POSITIVE_CERT_STATES,
    REQUIRED_WAIVER_APPROVERS,
    active_campaigns,
    canonical,
    load_json,
    main,
    provider_gate_errors,
    routing_errors,
    routing_portfolio,
    waiver_errors,
)

__all__ = [
    "COMPLETE_CERT_STATES",
    "EXPECTED_MANIFESTS",
    "EXPECTED_PROVIDER_COMMIT",
    "EXPECTED_PROVIDER_PULL_REQUEST",
    "GATED_STAGES",
    "POSITIVE_CERT_STATES",
    "REQUIRED_WAIVER_APPROVERS",
    "active_campaigns",
    "canonical",
    "load_json",
    "main",
    "provider_gate_errors",
    "routing_errors",
    "routing_portfolio",
    "waiver_errors",
]


if __name__ == "__main__":
    raise SystemExit(main())
