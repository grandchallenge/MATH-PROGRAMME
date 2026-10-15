#!/usr/bin/env node
/**
 * Real-Chromium MathJax verification for GCL Erdős Compendium.
 *
 * npm install --prefix ~/.local/share/gcl-browser-qa --save-exact playwright-core@1.58.2
 * Node resolution uses NODE_PATH, the installed local tooling, or normal require().
 * CHAD's cached Chromium-for-Testing binary is reused; no manual browser setup.
 *
 * Run with an HTTP local MkDocs build (file:// does not adequately test deployment).
 * The public sample checks PUBLISHED pages, not unpublished cohort drafts.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const cp = require('child_process');

function arg(name, fallback) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 ? process.argv[i + 1] : fallback;
}
function loadPlaywright() {
  const candidates = [
    process.env.GCL_PLAYWRIGHT_CORE,
    'playwright-core',
    path.join(os.homedir(), '.local/share/gcl-browser-qa/node_modules/playwright-core')
  ].filter(Boolean);
  for (const name of candidates) {
    try { return require(name); } catch (e) {
      if (e.code !== 'MODULE_NOT_FOUND') throw e;
    }
  }
  throw new Error('playwright-core unavailable; install in ~/.local/share/gcl-browser-qa');
}
function findBrowser() {
  if (process.env.GCL_BROWSER_PATH) return process.env.GCL_BROWSER_PATH;
  const directory = path.join(os.homedir(), '.cache/ms-playwright');
  const versions = fs.readdirSync(directory).filter(s => /^chromium-\d+$/.test(s))
    .sort((a,b) => Number(b.split('-')[1])-Number(a.split('-')[1]));
  for (const ver of versions) {
    const file = path.join(directory,ver,'chrome-linux64/chrome');
    if (fs.existsSync(file)) return file;
  }
  throw new Error('No cached Chromium binary; run npx playwright install chromium');
}
function git(args) {
  try { return cp.execFileSync('git',args,{encoding:'utf8'}).trim(); }
  catch(e) { return 'UNKNOWN'; }
}
function sha256(file) {
  return require('crypto').createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}
const local = arg('local', 'http://127.0.0.1:18765');
const publicBase = arg('public', 'https://grandchallenge.github.io/MATH-PROGRAMME');
const output = arg('out', '/tmp/EC-BULK-007_BROWSER_RENDER_QA.json');
const shots = arg('screenshots', 'governance/erdos_compendium/batches/EC-BULK-007_BROWSER_SCREENSHOTS');
const register = JSON.parse(fs.readFileSync('governance/erdos_compendium/batches/EC-BULK-007.json','utf8'));
const localIds = register.items.filter(i => i.source_return).map(i => i.problem_id);
const publicIds = [1, 3, 41, 1052, 1112]; // already-published mathematical exemplars
function pageUrl(base,n) {
  return base.replace(/\/$/,'') + '/erdos/problems/' + String(n).padStart(4,'0') + '/';
}

(async()=>{
  fs.mkdirSync(shots,{recursive:true});
  const {chromium} = loadPlaywright();
  const executablePath = findBrowser();
  const browser = await chromium.launch({headless:true,executablePath,args:['--no-sandbox','--disable-dev-shm-usage']});
  const context = await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1});
  const page = await context.newPage();
  const results = [];
  let currentErrors=[];
  let ancillaryApiWarnings=[];
  // Site-wide GitHub repo/release badges request these unauthenticated public APIs.
  // The upstream API can return 403 without affecting any local MathJax geometry.
  // Retain such 403s explicitly as external-service warnings; do not mislabel them
  // as renderer failures, and never ignore an unexpected console/page error.
  const ancillaryGithubUrls=new Set([
    'https://api.github.com/repos/grandchallenge/MATH-PROGRAMME',
    'https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/releases/latest'
  ]);
  page.on('pageerror',e=>currentErrors.push('pageerror: '+e.message));
  page.on('console',m=>{
    if (m.type()!=='error' || m.text().includes('404')) return;
    const sourceUrl=m.location()?.url || '';
    if(ancillaryGithubUrls.has(sourceUrl) && m.text().includes('403')) {
      ancillaryApiWarnings.push('external GitHub API HTTP 403: '+sourceUrl);
    } else {
      currentErrors.push('console: '+m.text().slice(0,250)+' at '+sourceUrl);
    }
  });
  try {
    for (const [scope,ids,base] of [['local_drafts',localIds,local],
                                    ['public_accepted_sample',publicIds,publicBase]]) {
      for (const n of ids) {
        const url = pageUrl(base,n);
        currentErrors=[];
        ancillaryApiWarnings=[];
        let error = null;
        let status = 0;
        let stats = {};
        try {
          const response = await page.goto(url,{waitUntil:'domcontentloaded',timeout:25000});
          status = response.status();
          await page.waitForFunction(() => {
            const els = [...document.querySelectorAll('.arithmatex')];
            return els.length>0 && els.every(el => !!el.querySelector('mjx-container'));
          },null,{timeout:16000});
          await page.evaluate(async()=>{
            if(window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
          });
          stats = await page.evaluate(()=>{
            const maths = [...document.querySelectorAll('.arithmatex')];
            const rendered = maths.filter(el=>!!el.querySelector('mjx-container')).length;
            const errors = document.querySelectorAll('mjx-merror').length;
            const display = document.querySelectorAll('div.arithmatex').length;
            const draftWarning = document.body.innerText.includes('UNACCEPTED DRAFT');
            const example = maths.find(el=>el.querySelector('mjx-container'))?.querySelector('mjx-container');
            const bbox = example?.getBoundingClientRect();
            return {
              arithmatex:maths.length,rendered,mathjaxErrors:errors,
              displayMathBlocks:display,draftWarning,
              mathjaxLoaded:!!window.MathJax,
              sampleBoundingBox:bbox ? {width:bbox.width,height:bbox.height}:null
            };
          });
          if(stats.mathjaxErrors) throw Error('MathJax produced error markup');
          if(!stats.mathjaxLoaded) throw Error('Missing browser MathJax runtime');
          if(stats.arithmatex!==stats.rendered) throw Error('Incomplete MathJax processing');
          if(!stats.sampleBoundingBox?.height) throw Error('No visible mathematical glyph geometry');
          if(scope==='local_drafts' && !stats.draftWarning) throw Error('Missing UNACCEPTED DRAFT warning');
          if(scope==='public_accepted_sample' && stats.draftWarning) throw Error('Unexpected draft warning on public exemplar');
          if(currentErrors.length) throw Error('Unexpected browser console errors: '+currentErrors.join(' | '));
        } catch(e) {error = e.message;}
        let screenshot = null;
        let screenshotSha256 = null;
        if (!error && ((scope==='local_drafts' && [1053,1084,1087,1090,1094,1097,1099,1101,1104,1110,1115,1119,1121,1123,1127,1131,1133,1135,1138,1141,1143,1146,1151,1157,1159,1162,1164,1167,1169,1172,1173].includes(n))
          || (scope==='public_accepted_sample' && n===1052))) {
          screenshot = path.join(shots,scope+'-'+n+'.png');
          await page.screenshot({path:screenshot});
          screenshotSha256 = sha256(screenshot);
        }
        const result={scope,problem_id:n,url,status,pass:!error,...stats,
          browserErrors:currentErrors.slice(),externalServiceWarnings:ancillaryApiWarnings.slice(),
          error,screenshot,screenshot_sha256:screenshotSha256};
        console.log(JSON.stringify({scope,problem_id:n,pass:!error,rendered:stats.rendered,
          math:stats.arithmatex,error}));
        results.push(result);
      }
    }
  } finally {
    await browser.close();
  }
  const passed=results.filter(x=>x.pass).length;
  const receipt={
    record_type:'EC_BULK_007_BROWSER_RENDER_QA/1',
    checked_at_utc:new Date().toISOString(),cohort_id:'EC-BULK-007',
    git_head:git(['rev-parse','HEAD']),git_branch:git(['branch','--show-current']),
    renderer:'Real headless Chromium + MathJax 3.2.2 via public CDN',
    browser_executable:executablePath,chromium_version:browser.version(),
    playwright_core_version:require(path.join(os.homedir(),'.local/share/gcl-browser-qa/node_modules/playwright-core/package.json')).version,
    local_base:local,public_base:publicBase,public_sample_note:
      'The public pages are ALREADY PUBLISHED articles. This does not certify public deployment of current cohort drafts.',
    local_drafts_accepted:false,protected_admission_certification:false,
    tested:results.length,passed,failed:results.length-passed,
    externalServiceWarningCount:results.reduce((a,r)=>a+r.externalServiceWarnings.length,0),
    externalServiceWarningPolicy:'Only exact public GitHub repository/release API HTTP 403 responses are classified ancillary; unexpected errors fail the page. All external warnings remain visible in each result.',
    results};
  fs.mkdirSync(path.dirname(output),{recursive:true});
  fs.writeFileSync(output,JSON.stringify(receipt,null,2)+'\n');
  console.log('BROWSER_QA_SUMMARY',JSON.stringify({tested:results.length,passed,failed:results.length-passed,receipt:output}));
  if(passed!==results.length) process.exitCode=2;
})().catch(e=>{console.error('BROWSER_QA_FATAL',e.stack);process.exit(1)});
