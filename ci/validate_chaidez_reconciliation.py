#!/usr/bin/env python3
"""Offline shape/accounting check; authenticated Git replay remains explicit."""
import json
from reconcile_chaidez_conformance import ROOT, validate_receipt


def main():
    manifest = json.loads((ROOT / "governance/chaidez_reconciliation_manifest.json").read_text())
    receipt = json.loads((ROOT / "governance/chaidez_reconciliation_receipt.json").read_text())
    validate_receipt(receipt, manifest)
    print("Chaidez reconciliation receipt shape/accounting valid; this offline check is not a cross-repository replay")


if __name__ == "__main__":
    main()
