#!/usr/bin/env python3
"""Validate frozen evidence and replay the pinned bounded periodicity proof in CI."""
import argparse, hashlib, json, re, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'experiments/erdos_proof_verification/0002'
SRC=PKG/'Erdos2Periodicity.lean'
EV=ROOT/'governance/erdos_proof_verification/evidence/0002'
NAMES='period_dvd period_pos covered_iff_exists covered_period covers_all_iff covered_shift uncovered_residue empty_period empty_uncovered example_period example_moduli example_distinct example_finite example_cover hostile_miss repeated_cover repeated_not_distinct'.split()
def sha(b): return hashlib.sha256(b).hexdigest()
def axioms(log):
    assert 'error:' not in log and 'sorryAx' not in log
    rows=re.findall(r"'Erdos2\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",log)
    assert len(rows)==17 and {k for k,v in rows}==set(NAMES)
    out={k:v.split(', ') if v else [] for k,v in rows}
    assert all(set(v)<={'propext','Quot.sound'} for v in out.values())
    return out
def verify(execute=False):
    r=json.loads((EV/'C_LEAN_PERIODICITY_REPLAY_001.json').read_text()); src=SRC.read_bytes(); log=(EV/'C_LEAN_PERIODICITY_STDOUT_001.txt').read_bytes(); bad=(EV/'C_LEAN_PERIODICITY_HOSTILE_001.txt').read_bytes()
    assert r['assignment_id']=='ERDOS-PV-0002-C' and r['positive_exit_code']==0 and r['hostile_rejected'] is True and r['full_analytic_theorem_replayed'] is False and r['mathcert_certified'] is False
    assert sha(src)==r['source_sha256'] and sha(log)==r['positive_stdout_sha256'] and sha(bad)==r['hostile_log_sha256']
    assert re.findall(r'^import\s+([\w.]+)\s*$',src.decode(),re.M)==['Std'] and not re.search(r'\b(sorry|admit|axiom|unsafe)\b',src.decode())
    assert axioms(log.decode())==r['axioms']
    assert b'Erdos2.Covered Erdos2.hostileClasses 23' in bad and b'is false' in bad
    assert (PKG/'lean-toolchain').read_text().strip()==r['lean_toolchain']
    if execute:
        def run(args): return subprocess.run(['lake','env','lean',*args],cwd=PKG,text=True,capture_output=True,timeout=120)
        v=run(['--version']); assert v.returncode==0 and 'version 4.33.0' in v.stdout
        p=run([str(SRC)]); assert p.returncode==0 and axioms(p.stdout)==r['axioms'],p.stdout+p.stderr
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'Hostile.lean'; target.write_bytes(src+b'\nexample : Erdos2.Covered Erdos2.hostileClasses 23 := by decide\n')
            n=run([str(target)]); out=n.stdout+n.stderr
            assert n.returncode!=0 and 'Tactic `decide` proved that the proposition' in out and 'Erdos2.Covered Erdos2.hostileClasses 23' in out and 'is false' in out,out
    print('PASS: 17 bounded declarations; hostile false target rejected in frozen replay'+('; fresh kernel replay passed' if execute else ''))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');verify(p.parse_args().execute)
