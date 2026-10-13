#!/usr/bin/env python3
# shared-mechanism: sshlg-skills/owner-process-controls-v1
# diverges: release-only cases; existing board is not mutated.
"""Real release validator controls in owned copies; the board is unchanged."""
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
cases=[
 ('healthy',BOARD,lambda s:s,None),
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
