#!/usr/bin/env python3
# shared-mechanism: sshlg-skills/owner-process-controls-v1
# diverges: none
# Case functions use the existing bespoke super-ux board diagnostics.
"""Real board/release validator controls in owned copies; original source is untouched."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
BOARD='docs/evidence/backlog.md'
RELEASE='.github/workflows/release.yml'
board=(ROOT/BOARD).read_text()
rows=re.findall(r'^\| (?:B|SU)-\d+ \|.*$',board,re.M)
assert rows, 'existing board has no row for the retained control'
row=next((line for line in rows if 'closed' in line.lower()),rows[0])
identifier=row.split('|')[1].strip()
def duplicate(text):
    assert text.count(row)==1, 'board plant must identify exactly one source row'
    return text.replace(row,row+'\n'+row,1)
def shifted(text):
    assert text.count(row)==1, 'board plant must identify exactly one source row'
    left,ident,rest=row.split('|',2)
    return text.replace(row,left+'|'+ident+'| planted extra cell |'+rest,1)
cases=[
 ('healthy',BOARD,lambda s:s,None),
 ('duplicate board id',BOARD,duplicate,f'{BOARD}: {identifier} appears 2 times'),
 ('extra board cell',BOARD,shifted,'its header declares -- an unescaped'),
 ('ancestry removed',RELEASE,lambda s:s.replace('git merge-base --is-ancestor','git merge-base-removed --is-ancestor',1),'release ancestry guard'),
 ('shallow',RELEASE,lambda s:s.replace('fetch-depth: 0','fetch-depth: 1',1),'release full-history checkout'),
 ('quoted full depth',RELEASE,lambda s:s.replace('fetch-depth: 0','fetch-depth: "0"',1),None),
]
observed=[]
for label,relative,mutate,needle in cases:
    with tempfile.TemporaryDirectory(prefix='r30-owner-process-') as temporary:
        base=Path(temporary);copy=base/'repo';home=base/'home';home.mkdir();tmp=base/'tmp';tmp.mkdir()
        shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','node_modules','__pycache__','.agent-sync'))
        target=copy/relative;before=target.read_text();after=mutate(before)
        assert label=='healthy' or after!=before,label
        target.write_text(after)
        env=os.environ.copy();env.update(HOME=str(home),TMPDIR=str(tmp),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,PYTHONDONTWRITEBYTECODE='1')
        p=subprocess.run([sys.executable,str(copy/'test/validate.py')],cwd=copy,env=env,text=True,capture_output=True,timeout=180)
        output=p.stdout+p.stderr
        good=(p.returncode==1 and needle in output) if needle else p.returncode==0
        observed.append({'case':label,'returncode':p.returncode,'expected_diagnostic':needle,'accepted':good,'output':output})
        if not good:print(json.dumps(observed,indent=2));raise SystemExit(1)
print(json.dumps({'source_hashes':{path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in ['test/validate.py','test/owner_release.py']},'cases':observed},indent=2))
