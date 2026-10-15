#!/usr/bin/env python3
"""Run headless Chromium MathJax paint checks on built EC-BULK-005 pages.

Local MkDocs build and live MathJax CDN are necessary. This tests browser paint,
not production deployment or mathematical theorem correctness.
"""
import argparse
import asyncio
import json
import subprocess
import socket
import time
from pathlib import Path
from playwright.async_api import async_playwright

async def main(args):
    base=Path(args.site)
    assert (base/"index.html").is_file()
    socket_test=socket.socket()
    socket_test.bind(("127.0.0.1",0))
    port=socket_test.getsockname()[1]
    socket_test.close()
    server=subprocess.Popen(
        ["python3","-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(base.resolve())],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    all_results=[]
    started=time.monotonic()
    try:
        await asyncio.sleep(.35)
        async with async_playwright() as pw:
            browser=await pw.chromium.launch(headless=True,args=["--no-sandbox"])
            context=await browser.new_context()
            semaphore=asyncio.Semaphore(args.parallel)
            async def audit(n):
                async with semaphore:
                    p=await context.new_page()
                    exceptions=[]
                    p.on("pageerror",lambda e: exceptions.append(str(e)[:240]))
                    try:
                        response=await p.goto("http://127.0.0.1:%s/erdos/problems/%04d/"%(port,n),wait_until="domcontentloaded",timeout=18000)
                        if response is None or response.status!=200:
                            raise ValueError("HTTP %s"%(response.status if response is not None else "?"))
                        expected=await p.locator(".arithmatex").count()
                        if expected:
                            await p.wait_for_function("document.querySelectorAll('mjx-container').length === document.querySelectorAll('.arithmatex').length",timeout=10000)
                        observed=await p.evaluate("() => ({painted:document.querySelectorAll('mjx-container').length,errors:document.querySelectorAll('mjx-merror').length,loader:!!document.querySelector('script[src*=\"tex-mml-chtml\"]'),title:document.title})")
                        good=(observed["painted"]==expected and observed["errors"]==0 and not exceptions)
                        if expected and not observed["loader"]: good=False
                        result={"problem_id":n,"arithmatex":expected,"painted":observed["painted"],
                                "mathjax_errors":observed["errors"],"javascript_errors":exceptions,
                                "title":observed["title"],"pass":good}
                    except Exception as e:
                        result={"problem_id":n,"pass":False,"error":str(e)[:350]}
                    finally:
                        await p.close()
                    return result
            jobs=[asyncio.create_task(audit(n)) for n in range(args.first,args.last+1)]
            all_results=await asyncio.gather(*jobs)
            await browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    record={"record_type":"EC_BULK_005_CHROMIUM_MATHJAX_BROWSER_QA/1","first":args.first,
            "last":args.last,"mode":"LOCAL_BUILT_MKDOCS_CHROMIUM_LIVE_MATHJAX_CDN_NOT_DEPLOYED",
            "browser":"Playwright Chromium","summary":{
                "total":len(all_results),"pass":sum(x.get("pass",False) for x in all_results),
                "failed":sum(not x.get("pass",False) for x in all_results),
                "pages_with_math":sum(x.get("arithmatex",0)>0 for x in all_results),
                "formulas_painted":sum(x.get("painted",0) for x in all_results),
                "seconds":round(time.monotonic()-started,2)},
            "failures":[x for x in all_results if not x.get("pass",False)],
            "per_problem":all_results}
    Path(args.json).write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    print("BROWSER_RESULT",json.dumps(record["summary"]))
    for x in record["failures"][:20]:print("FAIL",json.dumps(x))
    return int(record["summary"]["failed"]!=0)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",default="site")
    parser.add_argument("--first",type=int,default=652)
    parser.add_argument("--last",type=int,default=851)
    parser.add_argument("--parallel",type=int,default=4)
    parser.add_argument("--json",required=True)
    raise SystemExit(asyncio.run(main(parser.parse_args())))
