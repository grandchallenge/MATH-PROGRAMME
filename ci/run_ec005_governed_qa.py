#!/usr/bin/env python3
"""Run the registered EC-BULK-005 finite source fixtures and optional browser QA.

The governed policy shard runs standard-library finite fixtures. Local
maintainers can also invoke --browser-local after a strict MkDocs build and
Playwright/Chromium install. This is an actual execution root for all
registered modules, not a reachability exemption.
"""
import argparse
import asyncio
import inspect
import unittest
from pathlib import Path
import audit_erdos_compendium_ec005_browser as browser_qa
import test_erdos_compendium_ec005_source_lock_25 as source_lock_25
import test_erdos_compendium_ec005_conflicts_04 as conflict_04
import test_erdos_compendium_ec005_conflicts_03 as conflict_03
import test_erdos_compendium_ec005_conflicts_02 as conflicts_02
import test_erdos_compendium_ec005_conflicts_01 as conflict_01
import test_erdos_compendium_ec005_772_semantics as _module_00
import test_erdos_compendium_ec005_773_squares as _module_01
import test_erdos_compendium_ec005_774_dissociation as _module_02
import test_erdos_compendium_ec005_fixtures as _module_03
import test_erdos_compendium_ec005_fixtures_663_669 as _module_04
import test_erdos_compendium_ec005_fixtures_670_675 as _module_05
import test_erdos_compendium_ec005_fixtures_677_684 as _module_06
import test_erdos_compendium_ec005_fixtures_685_693 as _module_07
import test_erdos_compendium_ec005_fixtures_694_701 as _module_08
import test_erdos_compendium_ec005_fixtures_702_711 as _module_09
import test_erdos_compendium_ec005_fixtures_712_721 as _module_10
import test_erdos_compendium_ec005_fixtures_722_731 as _module_11
import test_erdos_compendium_ec005_fixtures_732_741 as _module_12
import test_erdos_compendium_ec005_fixtures_732_741_coord_review as _module_13
import test_erdos_compendium_ec005_fixtures_742_751 as _module_14
import test_erdos_compendium_ec005_fixtures_752_761 as _module_15
import test_erdos_compendium_ec005_fixtures_762_771 as _module_16
import test_erdos_compendium_ec005_fixtures_775_781 as _module_17
import test_erdos_compendium_ec005_fixtures_782_791 as _module_18
import test_erdos_compendium_ec005_fixtures_792_801 as _module_19
import test_erdos_compendium_ec005_fixtures_802_811 as _module_20
import test_erdos_compendium_ec005_fixtures_812_821 as _module_21
import test_erdos_compendium_ec005_fixtures_822_831 as _module_22
import test_erdos_compendium_ec005_fixtures_832_841 as _module_23
import test_erdos_compendium_ec005_fixtures_842_851 as _module_24

MODULES=(
    source_lock_25,
    conflict_04,
    conflict_03,
    conflicts_02,
    conflict_01,
    _module_00,
    _module_01,
    _module_02,
    _module_03,
    _module_04,
    _module_05,
    _module_06,
    _module_07,
    _module_08,
    _module_09,
    _module_10,
    _module_11,
    _module_12,
    _module_13,
    _module_14,
    _module_15,
    _module_16,
    _module_17,
    _module_18,
    _module_19,
    _module_20,
    _module_21,
    _module_22,
    _module_23,
    _module_24,
)

def verify_finite_fixtures() -> int:
    suite=unittest.TestSuite()
    functions=0
    for module in MODULES:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
        for name,value in inspect.getmembers(module,inspect.isfunction):
            if name.startswith("test_") and not inspect.signature(value).parameters:
                suite.addTest(unittest.FunctionTestCase(value,description=f"{module.__name__}.{name}"))
                functions+=1
    test_count=suite.countTestCases()
    assert test_count>200 and functions==6,(test_count,functions)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"EC005_GOVERNED_QA tests={result.testsRun} functions={functions} failures={len(result.failures)} errors={len(result.errors)}")
    return 0 if result.wasSuccessful() else 1

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--browser-local",action="store_true")
    parser.add_argument("--site",default="site")
    parser.add_argument("--first",type=int,default=652)
    parser.add_argument("--last",type=int,default=851)
    parser.add_argument("--parallel",type=int,default=4)
    parser.add_argument("--json",default="/tmp/ec005-browser-governed.json")
    args=parser.parse_args()
    if args.browser_local:
        return asyncio.run(browser_qa.main(args))
    return verify_finite_fixtures()

if __name__=="__main__":
    raise SystemExit(main())
