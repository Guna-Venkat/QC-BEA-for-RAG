#!/usr/bin/env python3
"""Read-only publication checks. No installation, inference, Git mutation or writes."""
import argparse,hashlib,json,re,sys,os
from pathlib import Path

LFS_PATHS=(
 '5_qbgf/results/4_frozen_decision/split_protocol/w12_split_freeze.json',
 'demo/application/results/week12/qbgf/v3/protocol/W12_SPLIT_FREEZE.json',
 'demo/application/demo/replay_data/v1/bundle.json',
)

def inventory(root):
 ignored={'.git','.venv','venv','sara_env','node_modules','__pycache__','.pytest_cache','local_checks'}
 paths=[]
 for current,dirs,files in os.walk(root,followlinks=False):
  dirs[:]=[d for d in dirs if d not in ignored]
  paths.extend(Path(current)/d for d in dirs if (Path(current)/d).is_symlink())
  paths.extend(Path(current)/f for f in files)
 return paths

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def requirement_lines(path,seen=None):
 seen=set() if seen is None else seen;path=Path(path).resolve()
 if path in seen:return []
 seen.add(path);out=[]
 for line in path.read_text().splitlines():
  line=line.strip()
  if not line or line.startswith('#'):continue
  if line.startswith('-r '):out.extend(requirement_lines(path.parent/line[3:].strip(),seen))
  else:out.append(line)
 return out

def environment_check(root,profile):
 from importlib.metadata import distribution,PackageNotFoundError
 from packaging.requirements import Requirement
 from packaging.utils import canonicalize_name
 requested=[Requirement(x) for x in requirement_lines(root/('requirements.txt' if profile=='saved' else f'requirements-{profile}.txt'))]
 problems=[];seen=set();queue=requested[:]
 while queue:
  req=queue.pop()
  if req.marker and not req.marker.evaluate({'extra':''}):continue
  name=canonicalize_name(req.name)
  try:dist=distribution(name)
  except PackageNotFoundError:problems.append(f'Missing dependency: {req}');continue
  if not req.specifier.contains(dist.version,prereleases=True):problems.append(f'{req.name} {dist.version} does not satisfy {req.specifier}')
  if name in seen:continue
  seen.add(name)
  for raw in dist.requires or []:
   child=Requirement(raw)
   if not child.marker or child.marker.evaluate({'extra':''}):queue.append(child)
 return dict(profile=profile,declared=len(requested),dependency_closure=len(seen),problems=sorted(set(problems)))

def check(root,environment=None):
 root=Path(root).resolve();errors=[];warnings=[];summary={};paths=inventory(root)
 links=[p for p in paths if p.is_symlink()]
 for p in links:
  if not p.exists():errors.append('Broken link: '+str(p.relative_to(root)))
  elif not p.resolve().is_relative_to(root):errors.append('External link: '+str(p.relative_to(root)))
 summary['internal_symlinks']=len(links)
 attributes=(root/'.gitattributes').read_text()
 for rel in LFS_PATHS:
  f=root/rel
  if f'/{rel} filter=lfs diff=lfs merge=lfs -text' not in attributes:errors.append('Missing exact LFS rule: '+rel)
  if not f.is_file():errors.append('Missing required large file: '+rel);continue
  with f.open('rb') as handle:pointer=handle.read(100).startswith(b'version https://git-lfs.github.com/spec/v1')
  if pointer:errors.append('LFS pointer not fetched: '+rel+'; run git lfs pull')
 for p in paths:
  if p.is_symlink() or not p.is_file() or '.git' in p.relative_to(root).parts or '.venv' in p.relative_to(root).parts:continue
  if p.stat().st_size>100*1024**2 and str(p.relative_to(root)) not in LFS_PATHS:errors.append('File exceeds ordinary Git limit without an LFS rule: '+str(p.relative_to(root)))
 app=root/'demo/application';copy=json.loads((root/'demo/COPY_MANIFEST.json').read_text())
 for row in copy['files']:
  path=app/row['path']
  if not path.is_file() or sha(path)!=row['sha256']:errors.append('Copied-payload checksum mismatch: '+row['path'])
 summary['payload_files_verified']=len(copy['files'])
 expected='d0188a3582d6aead0a3a31f9f15bad9b51a88a6b475b05ac79ae38e58f05366b'
 for rel in ['results/week12/W13_FINAL_METHOD_FREEZE.json','results/week12/qbgf/v3/W13_FINAL_METHOD_FREEZE.json']:
  if sha(app/rel)!=expected:errors.append('Final-method freeze changed: '+rel)
 split=[root/LFS_PATHS[0],root/LFS_PATHS[1]]
 if all(p.is_file() for p in split) and sha(split[0])!=sha(split[1]):errors.append('Frozen split copies differ')
 summary['freeze_sha256']=expected
 for name,row in json.loads((app/'demo/artifact_manifest.json').read_text())['sources'].items():
  path=app/row['path']
  if not path.is_file() or sha(path)!=row['sha256']:errors.append('Registered demo research source differs: '+name)
 publication=app/'demo/replay_data/v1';receipt=json.loads((publication/'PUBLISHED.json').read_text())
 if sha(publication/receipt['bundle'])!=receipt['sha256']:errors.append('Published curated bundle differs')
 summary['curated_conditions']=receipt['conditions']
 patterns={'HF token':rb'hf_[A-Za-z0-9]{25,}','GitHub token':rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})','Private key':rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----','AWS access key':rb'AKIA[A-Z0-9]{16}'}
 matches=[]
 for p in paths:
  if p.is_symlink() or not p.is_file() or p.suffix.lower() not in {'.py','.json','.ipynb','.md','.txt','.yaml','.yml','.sh','.toml','.csv','.log'}:continue
  if any(x in {'.git','.venv','local_checks'} for x in p.relative_to(root).parts):continue
  data=p.read_bytes()
  for label,pattern in patterns.items():
   if re.search(pattern,data):matches.append(dict(path=str(p.relative_to(root)),kind=label))
 summary['credential_pattern_matches']=matches
 if matches:errors.append('Potential credential patterns found; values withheld. Review reported paths.')
 summary['license']='MIT for project-authored material; third-party notices preserved'
 for rel in ['LICENSE','THIRD_PARTY_NOTICES.md','requirements.txt','requirements-live.txt','requirements-dev.txt','setup_demo.sh','INSTALLATION.md','PUBLICATION.md']:
  if not (root/rel).is_file():errors.append('Required publication file missing: '+rel)
 if environment:
  env=environment_check(root,environment);summary['environment']=env;errors.extend(env['problems'])
 warnings.append('Pattern scan is not a complete sensitive-data or redistribution-rights audit.')
 summary.update(status='READY' if not errors else 'BLOCKED',errors=errors,warnings=warnings)
 return summary

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--environment',choices=['saved','live','dev']);args=parser.parse_args()
 result=check(args.root,args.environment);print(json.dumps(result,indent=2));return 1 if result['errors'] else 0
if __name__=='__main__':sys.exit(main())
